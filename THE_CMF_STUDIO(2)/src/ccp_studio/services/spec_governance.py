"""Spec-governance service for TS-CMF-003."""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
from uuid import UUID, uuid4

from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.spec_governance import (
    CBARCheck,
    FilesReadReceipt,
    PipelineStageTrace,
    RequirementTrace,
    SourceFileRef,
    SpecAuditReceipt,
    SpecAuditStatus,
    TechSpecSourcePacket,
    TechSpecWorkflow,
    TechSpecWorkflowStatus,
    default_spec_writing_protocol,
    new_source_packet,
    new_tech_spec_workflow,
)
from ccp_studio.project_paths import discover_project_root, resolve_project_path
from ccp_studio.programs.spec_governance import (
    CBARAuditor,
    PipelineStageTraceCompiler,
    RequirementTraceCompiler,
    TechSpecAuditor,
)
from ccp_studio.repositories.spec_governance import InMemorySpecGovernanceRepository


DEFAULT_REQUIRED_SOURCES = [
    ("05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md", "prd"),
    ("docs/architecture.md", "architecture"),
    ("product-brief-CMF_STUDIO-2026-06-19.md", "product_brief"),
    ("docs/migration/legacy-inventory.md", "legacy_inventory"),
    ("docs/cmf-studio-pipeline-map.md", "pipeline_map"),
]


BLOCKING_FINDING_PREFIXES = {
    "FILES_READ_INCOMPLETE",
    "REQUIREMENT_TRACE_MISSING",
    "PIPELINE_TRACE_MISSING",
    "CBAR_CHECK_MISSING",
    "GREENFIELD_ALIGNMENT_FAILED",
    "LEGACY_RUNTIME_IMPORT_FORBIDDEN",
    "COMMAND_BUS_BYPASS_FORBIDDEN",
    "PROJECTION_NOT_CANONICAL",
}


class SpecGovernanceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class SpecGovernanceService:
    repository: InMemorySpecGovernanceRepository = field(
        default_factory=InMemorySpecGovernanceRepository
    )
    workspace_root: Path = field(default_factory=discover_project_root)
    requirement_trace_compiler: RequirementTraceCompiler = field(
        default_factory=RequirementTraceCompiler
    )
    pipeline_stage_trace_compiler: PipelineStageTraceCompiler = field(
        default_factory=PipelineStageTraceCompiler
    )
    cbar_auditor: CBARAuditor = field(default_factory=CBARAuditor)
    tech_spec_auditor: TechSpecAuditor = field(default_factory=TechSpecAuditor)

    def open_workflow_from_story(
        self,
        *,
        spec_id: str,
        story_path: str,
        actor_id: UUID,
    ) -> TechSpecWorkflow:
        story_text = self._read_text(story_path)
        story_meta = parse_frontmatter(story_text)
        story_id = story_meta.get("story_id")
        status = story_meta.get("status")
        if not story_id:
            raise SpecGovernanceError("STORY_ID_MISSING", "Story frontmatter lacks story_id.")
        if status not in {"ready-for-tech-spec", "ready-for-development", "approved"}:
            raise SpecGovernanceError(
                "STORY_NOT_APPROVED",
                "TechSpecWorkflow requires an approved or ready story.",
            )
        workflow = new_tech_spec_workflow(
            spec_id=spec_id,
            story_id=story_id,
            story_path=story_path,
            actor_id=actor_id,
        )
        return self.repository.save_workflow(workflow)

    def resolve_source_packet(
        self,
        *,
        workflow_id: UUID,
        feature_sources: list[str] | None = None,
    ) -> TechSpecSourcePacket:
        workflow = self._require_workflow(workflow_id)
        required_sources = [
            SourceFileRef(path=path, required=True, source_role=role)
            for path, role in DEFAULT_REQUIRED_SOURCES
        ]
        required_sources.append(
            SourceFileRef(path=workflow.story_path, required=True, source_role="story")
        )
        feature_refs = [
            SourceFileRef(path=path, required=True, source_role="feature_source")
            for path in (feature_sources or [])
        ]
        packet = new_source_packet(
            workflow_id=workflow.workflow_id,
            required_sources=required_sources,
            feature_sources=feature_refs,
        )
        workflow.status = TechSpecWorkflowStatus.reading_sources
        workflow.updated_at = utc_now()
        self.repository.save_workflow(workflow)
        return self.repository.save_source_packet(packet)

    def record_files_read_receipts(
        self,
        *,
        workflow_id: UUID,
        reader_actor_id: UUID,
    ) -> list[FilesReadReceipt]:
        workflow = self._require_workflow(workflow_id)
        packet = self.repository.latest_source_packet_for_workflow(workflow.workflow_id)
        if packet is None:
            raise SpecGovernanceError(
                "SOURCE_PACKET_MISSING",
                "A TechSpecSourcePacket is required before files-read receipts.",
            )

        receipts: list[FilesReadReceipt] = []
        for ref in packet.required_sources + packet.feature_sources:
            text = self._read_text(ref.path)
            hydrated_ref = ref.model_copy(update={"content_hash": sha256_text(text)})
            receipt = FilesReadReceipt(
                schema_version="cmf.files_read_receipt.v1",
                receipt_id=uuid4(),
                workflow_id=workflow.workflow_id,
                file_ref=hydrated_ref,
                read_at=utc_now(),
                reader_actor_id=reader_actor_id,
                evidence_summary=(
                    f"Read {len(text)} characters from {ref.source_role}: {ref.path}"
                ),
            )
            receipts.append(self.repository.save_files_read_receipt(receipt))

        return receipts

    def compile_requirement_trace(
        self,
        *,
        workflow_id: UUID,
        fr_id: str,
        spec_sections: list[str],
        acceptance_criteria_refs: list[str],
        enforcement_mechanism: str,
    ) -> RequirementTrace:
        workflow = self._require_workflow(workflow_id)
        result = self.requirement_trace_compiler.compile(
            workflow_id=workflow.workflow_id,
            fr_id=fr_id,
            story_id=workflow.story_id,
            spec_sections=spec_sections,
            acceptance_criteria_refs=acceptance_criteria_refs,
            enforcement_mechanism=enforcement_mechanism,
        )
        workflow.status = TechSpecWorkflowStatus.tracing
        workflow.updated_at = utc_now()
        self.repository.save_workflow(workflow)
        return self.repository.save_requirement_trace(result.output)

    def compile_pipeline_stage_trace(
        self,
        *,
        workflow_id: UUID,
        pipeline_stage: str,
        entry_object: str,
        exit_object: str,
        allowed_actor_or_service: str,
        validation_contract: str,
        required_receipt: str,
    ) -> PipelineStageTrace:
        workflow = self._require_workflow(workflow_id)
        result = self.pipeline_stage_trace_compiler.compile(
            workflow_id=workflow.workflow_id,
            pipeline_stage=pipeline_stage,
            entry_object=entry_object,
            exit_object=exit_object,
            allowed_actor_or_service=allowed_actor_or_service,
            validation_contract=validation_contract,
            required_receipt=required_receipt,
        )
        workflow.status = TechSpecWorkflowStatus.tracing
        workflow.updated_at = utc_now()
        self.repository.save_workflow(workflow)
        return self.repository.save_pipeline_trace(result.output)

    def run_cbar_check(
        self,
        *,
        workflow_id: UUID,
        primitive_tension: str,
        failure_scenario: str,
        resolution_demand: str,
        downstream_proof: str,
        test_or_receipt_refs: list[str],
    ) -> CBARCheck:
        workflow = self._require_workflow(workflow_id)
        result = self.cbar_auditor.audit(
            workflow_id=workflow.workflow_id,
            primitive_tension=primitive_tension,
            failure_scenario=failure_scenario,
            resolution_demand=resolution_demand,
            downstream_proof=downstream_proof,
            test_or_receipt_refs=test_or_receipt_refs,
        )
        return self.repository.save_cbar_check(result.output)

    def audit_workflow(
        self,
        *,
        workflow_id: UUID,
        spec_text: str,
    ) -> SpecAuditReceipt:
        workflow = self._require_workflow(workflow_id)
        findings: list[str] = []
        findings.extend(self._source_findings(workflow))

        requirement_traces = self.repository.requirement_traces_for_workflow(workflow_id)
        pipeline_traces = self.repository.pipeline_traces_for_workflow(workflow_id)
        cbar_checks = self.repository.cbar_checks_for_workflow(workflow_id)

        if not requirement_traces:
            findings.append("REQUIREMENT_TRACE_MISSING: no FR-CMF trace recorded")
        if not pipeline_traces:
            findings.append("PIPELINE_TRACE_MISSING: no pipeline stage trace recorded")
        if not cbar_checks:
            findings.append("CBAR_CHECK_MISSING: no CBAR check recorded")

        findings.extend(greenfield_lint(spec_text))
        status = self._status_for_findings(findings)

        result = self.tech_spec_auditor.receipt(
            workflow_id=workflow.workflow_id,
            spec_id=workflow.spec_id,
            status=status,
            files_read_receipt_ids=[
                receipt.receipt_id
                for receipt in self.repository.files_read_for_workflow(workflow_id)
            ],
            requirement_trace_ids=[trace.trace_id for trace in requirement_traces],
            pipeline_trace_ids=[trace.trace_id for trace in pipeline_traces],
            cbar_check_ids=[check.cbar_check_id for check in cbar_checks],
            findings=findings,
        )
        receipt = self.repository.save_audit_receipt(result.output)
        workflow.status = TechSpecWorkflowStatus(status.value)
        workflow.updated_at = utc_now()
        self.repository.save_workflow(workflow)
        return receipt

    def write_spec_artifact(
        self,
        *,
        audit_receipt: SpecAuditReceipt,
        target_path: str,
        content: str,
    ) -> Path:
        if audit_receipt.status != SpecAuditStatus.accepted:
            raise SpecGovernanceError(
                "SPEC_NOT_ACCEPTED",
                "Only accepted specs may be written as canonical artifacts.",
            )
        resolved = self._resolve_path(target_path)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        resolved.write_text(content, encoding="utf-8")
        return resolved

    def _source_findings(self, workflow: TechSpecWorkflow) -> list[str]:
        packet = self.repository.latest_source_packet_for_workflow(workflow.workflow_id)
        if packet is None:
            return ["FILES_READ_INCOMPLETE: no source packet recorded"]

        read_paths = {
            receipt.file_ref.path
            for receipt in self.repository.files_read_for_workflow(workflow.workflow_id)
        }
        missing = [
            ref.path
            for ref in packet.required_sources + packet.feature_sources
            if ref.required and ref.path not in read_paths
        ]
        return [f"FILES_READ_INCOMPLETE: missing {path}" for path in missing]

    @staticmethod
    def _status_for_findings(findings: list[str]) -> SpecAuditStatus:
        if not findings:
            return SpecAuditStatus.accepted
        if any(
            finding.startswith(prefix)
            for finding in findings
            for prefix in BLOCKING_FINDING_PREFIXES
        ):
            return SpecAuditStatus.blocked
        return SpecAuditStatus.revision_requested

    def _require_workflow(self, workflow_id: UUID) -> TechSpecWorkflow:
        workflow = self.repository.get_workflow(workflow_id)
        if workflow is None:
            raise SpecGovernanceError("TECH_SPEC_WORKFLOW_NOT_FOUND", "Workflow not found.")
        return workflow

    def _read_text(self, path: str) -> str:
        resolved = self._resolve_path(path)
        if not resolved.exists():
            raise SpecGovernanceError("SOURCE_FILE_NOT_FOUND", f"{path} does not exist.")
        return resolved.read_text(encoding="utf-8")

    def _resolve_path(self, path: str) -> Path:
        return resolve_project_path(path, self.workspace_root)


def parse_frontmatter(markdown: str) -> dict[str, str]:
    normalized = markdown.lstrip("\ufeff\r\n\t ")
    if not normalized.startswith("---"):
        return dict()
    lines = normalized.splitlines()
    metadata: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    return metadata


def sha256_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def greenfield_lint(spec_text: str) -> list[str]:
    findings: list[str] = []
    lowered = spec_text.lower()
    protocol = default_spec_writing_protocol()

    if "existing backend integration" in lowered:
        findings.append(
            "GREENFIELD_ALIGNMENT_FAILED: replace Existing Backend Integration with Greenfield Integration and Legacy Migration Context"
        )
    if "typescript is the source of truth" in lowered or "typescript owns domain" in lowered:
        findings.append(
            "GREENFIELD_ALIGNMENT_FAILED: TypeScript cannot be domain contract authority"
        )
    if "legacy_runtime" in lowered or "direct legacy runtime import" in lowered:
        findings.append(
            "LEGACY_RUNTIME_IMPORT_FORBIDDEN: legacy runtime coupling is not allowed"
        )
    if "bypass the command bus" in lowered or "direct db write from pi" in lowered:
        findings.append(
            "COMMAND_BUS_BYPASS_FORBIDDEN: state mutation must go through Command Bus"
        )
    if "neo4j is canonical" in lowered or "neo4j as canonical truth" in lowered:
        findings.append(
            "PROJECTION_NOT_CANONICAL: Neo4j cannot authorize canonical state"
        )
    if "improve user engagement" in lowered or "high quality content" in lowered:
        findings.append(
            "RSCS_PROJECT_CONTEXT_WEAK: recommendation lacks project-specific source evidence"
        )
    for blocked_phrase in protocol.blocked_phrases:
        if blocked_phrase.lower() in lowered and not any(blocked_phrase in finding for finding in findings):
            findings.append(f"GREENFIELD_ALIGNMENT_FAILED: blocked phrase `{blocked_phrase}`")
    return findings
