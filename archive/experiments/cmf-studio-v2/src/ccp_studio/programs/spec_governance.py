"""Deterministic DSPy-compatible spec-governance programs for TS-CMF-003."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4

from ccp_studio.contracts.spec_governance import (
    CBARCheck,
    PipelineStageTrace,
    RequirementTrace,
    SpecAuditReceipt,
    SpecAuditStatus,
)
from ccp_studio.contracts.orchestration import utc_now


@dataclass(frozen=True)
class ProgramResult:
    program_name: str
    evidence_refs: list[str]
    output: object


class RequirementTraceCompiler:
    program_name = "RequirementTraceCompiler"
    program_family = "dspy"

    def compile(
        self,
        *,
        workflow_id: UUID,
        fr_id: str,
        story_id: str,
        spec_sections: list[str],
        acceptance_criteria_refs: list[str],
        enforcement_mechanism: str,
    ) -> ProgramResult:
        trace = RequirementTrace(
            schema_version="cmf.requirement_trace.v1",
            trace_id=uuid4(),
            workflow_id=workflow_id,
            fr_id=fr_id,
            story_id=story_id,
            spec_sections=spec_sections,
            acceptance_criteria_refs=acceptance_criteria_refs,
            enforcement_mechanism=enforcement_mechanism,
        )
        return ProgramResult(
            program_name=self.program_name,
            evidence_refs=[fr_id, story_id],
            output=trace,
        )


class PipelineStageTraceCompiler:
    program_name = "PipelineStageTraceCompiler"
    program_family = "dspy"

    def compile(
        self,
        *,
        workflow_id: UUID,
        pipeline_stage: str,
        entry_object: str,
        exit_object: str,
        allowed_actor_or_service: str,
        validation_contract: str,
        required_receipt: str,
    ) -> ProgramResult:
        trace = PipelineStageTrace(
            schema_version="cmf.pipeline_stage_trace.v1",
            trace_id=uuid4(),
            workflow_id=workflow_id,
            pipeline_stage=pipeline_stage,
            entry_object=entry_object,
            exit_object=exit_object,
            allowed_actor_or_service=allowed_actor_or_service,
            validation_contract=validation_contract,
            required_receipt=required_receipt,
        )
        return ProgramResult(
            program_name=self.program_name,
            evidence_refs=[pipeline_stage, required_receipt],
            output=trace,
        )


class CBARAuditor:
    program_name = "CBARAuditor"
    program_family = "dspy"

    def audit(
        self,
        *,
        workflow_id: UUID,
        primitive_tension: str,
        failure_scenario: str,
        resolution_demand: str,
        downstream_proof: str,
        test_or_receipt_refs: list[str],
    ) -> ProgramResult:
        check = CBARCheck(
            schema_version="cmf.cbar_check.v1",
            cbar_check_id=uuid4(),
            workflow_id=workflow_id,
            primitive_tension=primitive_tension,
            failure_scenario=failure_scenario,
            resolution_demand=resolution_demand,
            downstream_proof=downstream_proof,
            test_or_receipt_refs=test_or_receipt_refs,
        )
        return ProgramResult(
            program_name=self.program_name,
            evidence_refs=test_or_receipt_refs,
            output=check,
        )


class TechSpecAuditor:
    program_name = "TechSpecAuditor"
    program_family = "dspy"

    def receipt(
        self,
        *,
        workflow_id: UUID,
        spec_id: str,
        status: SpecAuditStatus,
        files_read_receipt_ids: list[UUID],
        requirement_trace_ids: list[UUID],
        pipeline_trace_ids: list[UUID],
        cbar_check_ids: list[UUID],
        findings: list[str],
    ) -> ProgramResult:
        receipt = SpecAuditReceipt(
            schema_version="cmf.spec_audit_receipt.v1",
            spec_audit_receipt_id=uuid4(),
            workflow_id=workflow_id,
            spec_id=spec_id,
            status=status,
            files_read_receipt_ids=files_read_receipt_ids,
            requirement_trace_ids=requirement_trace_ids,
            pipeline_trace_ids=pipeline_trace_ids,
            cbar_check_ids=cbar_check_ids,
            findings=findings,
            written_at=utc_now(),
        )
        return ProgramResult(
            program_name=self.program_name,
            evidence_refs=[str(item) for item in receipt.files_read_receipt_ids],
            output=receipt,
        )


class TechSpecCompiler:
    program_name = "TechSpecCompiler"
    program_family = "dspy"

    def compile(self, *, title: str, sections: dict[str, str]) -> ProgramResult:
        body = [f"# {title}"]
        for heading, content in sections.items():
            body.append(f"\n## {heading}\n\n{content.strip()}")
        return ProgramResult(
            program_name=self.program_name,
            evidence_refs=list(sections.keys()),
            output="\n".join(body).strip() + "\n",
        )


class EpicStoryCompiler:
    program_name = "EpicStoryCompiler"
    program_family = "dspy"

    def compile_story_summary(self, *, story_id: str, acceptance_criteria: list[str]) -> ProgramResult:
        output = {
            "story_id": story_id,
            "acceptance_criteria_count": len(acceptance_criteria),
            "acceptance_criteria_refs": [f"AC{i + 1}" for i in range(len(acceptance_criteria))],
        }
        return ProgramResult(
            program_name=self.program_name,
            evidence_refs=output["acceptance_criteria_refs"],
            output=output,
        )
