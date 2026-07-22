from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.orchestration import StageRunStatus
from ccp_studio.contracts.spec_governance import SpecAuditStatus
from ccp_studio.services.orchestration import OrchestrationService
from ccp_studio.services.spec_governance import SpecGovernanceService, greenfield_lint
from ccp_studio.workflows.tech_spec_compiler import TechSpecCompilerWorkflow


STORY_PATH = "docs/stories/story-3-5-python-dspy-pi-bmad-spec-workflow.md"


def _open_governed_workflow():
    spec_service = SpecGovernanceService()
    orchestration_service = OrchestrationService()
    workflow = TechSpecCompilerWorkflow(spec_service, orchestration_service)
    governed = workflow.open(
        spec_id="TS-CMF-003",
        story_path=STORY_PATH,
        actor_id=uuid4(),
        feature_sources=[
            "docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md",
            "docs/architecture/april_updates/PROMPT_Spec_Audit.md",
            "docs/architecture/spec updates/CBAR_Constraint_Based_Adversarial_Reasoning_Epics_Stories.md",
        ],
    )
    return spec_service, orchestration_service, workflow, governed


def _record_required_governance(spec_service: SpecGovernanceService, governed):
    receipts = spec_service.record_files_read_receipts(
        workflow_id=governed.tech_spec_workflow.workflow_id,
        reader_actor_id=governed.tech_spec_workflow.actor_id,
    )
    requirement = spec_service.compile_requirement_trace(
        workflow_id=governed.tech_spec_workflow.workflow_id,
        fr_id="FR-CMF-03.07",
        spec_sections=["Requirement Trace", "Implementation Plan", "Testing Strategy"],
        acceptance_criteria_refs=["AC1", "AC2", "AC3", "AC4", "AC5", "AC6", "AC7", "AC8"],
        enforcement_mechanism="files-read, trace, CBAR, greenfield lint, and SpecAuditReceipt gates",
    )
    pipeline = spec_service.compile_pipeline_stage_trace(
        workflow_id=governed.tech_spec_workflow.workflow_id,
        pipeline_stage="spec-governance overlay",
        entry_object="epic/story/spec request",
        exit_object="SpecAuditReceipt",
        allowed_actor_or_service="PM Agent, Architect Agent, Tech Writer Agent, Pi Orchestrator, DSPy compiler, human approver",
        validation_contract="files-read, FR trace, pipeline trace, CBAR",
        required_receipt="spec audit receipt",
    )
    cbar = spec_service.run_cbar_check(
        workflow_id=governed.tech_spec_workflow.workflow_id,
        primitive_tension="Preserve BMAD discipline without carrying stale runtime assumptions.",
        failure_scenario="A generic spec omits Legacy Inventory, pipeline trace, CBAR, and Python/DSPy/Pi boundaries.",
        resolution_demand="Typed source receipts, traces, CBAR checks, and audit receipts replace prompt-only discipline.",
        downstream_proof="Tests block missing source, missing trace, old-stack assumptions, and weak RSCS evidence.",
        test_or_receipt_refs=["tests/cmf_studio/test_spec_governance.py", "SpecAuditReceipt"],
    )
    return receipts, requirement, pipeline, cbar


def _clean_spec_text() -> str:
    return """
## Files Read
Legacy Inventory, Product Brief, architecture, PRD, pipeline map, and story were read.
## Requirement Trace
FR-CMF-03.07 is enforced by typed source receipts and audit receipts.
## Pipeline Stage Trace
Spec-governance overlay emits SpecAuditReceipt.
## Greenfield Integration and Legacy Migration Context
Pydantic contracts define domain truth. DSPy programs compile traces. Pi orchestrates through the Command Bus and orchestration records.
## CBAR Constraint Pass
Tension, failure scenario, resolution demand, and downstream proof are named.
"""


def test_governed_workflow_opens_with_source_packet_and_orchestration_records():
    spec_service, orchestration_service, _workflow, governed = _open_governed_workflow()

    required_paths = {ref.path for ref in governed.source_packet.required_sources}

    assert "docs/migration/legacy-inventory.md" in required_paths
    assert "docs/cmf-studio-pipeline-map.md" in required_paths
    assert governed.stage_plan.pipeline_stage == "spec-governance overlay"
    assert governed.validation_contract.required_receipt_types == ["spec_audit_receipt"]
    assert governed.handoff_packet.required_downstream_receipt == "spec_audit_receipt"
    assert spec_service.repository.get_workflow(governed.tech_spec_workflow.workflow_id) is not None
    assert orchestration_service.repository.get_run(governed.orchestration_run.orchestration_run_id) is not None


def test_full_spec_governance_workflow_accepts_clean_spec_and_closes_stage():
    spec_service, orchestration_service, workflow, governed = _open_governed_workflow()
    receipts, requirement, pipeline, cbar = _record_required_governance(spec_service, governed)

    audit = spec_service.audit_workflow(
        workflow_id=governed.tech_spec_workflow.workflow_id,
        spec_text=_clean_spec_text(),
    )
    stage_receipt = workflow.close_with_audit_receipt(
        governed_workflow=governed,
        audit_receipt=audit,
    )

    assert audit.status == SpecAuditStatus.accepted
    assert len(receipts) == len(governed.source_packet.required_sources) + len(governed.source_packet.feature_sources)
    assert requirement.trace_id in spec_service.repository.requirement_traces
    assert pipeline.trace_id in spec_service.repository.pipeline_traces
    assert cbar.cbar_check_id in spec_service.repository.cbar_checks
    assert stage_receipt.receipt_type == "spec_audit_receipt"
    assert orchestration_service.repository.get_run(governed.orchestration_run.orchestration_run_id).status == StageRunStatus.succeeded


def test_missing_files_read_receipts_block_audit_with_legacy_inventory_visible():
    spec_service, _orchestration_service, _workflow, governed = _open_governed_workflow()

    audit = spec_service.audit_workflow(
        workflow_id=governed.tech_spec_workflow.workflow_id,
        spec_text=_clean_spec_text(),
    )

    assert audit.status == SpecAuditStatus.blocked
    assert any("FILES_READ_INCOMPLETE" in finding for finding in audit.findings)
    assert any("docs/migration/legacy-inventory.md" in finding for finding in audit.findings)


def test_missing_pipeline_trace_blocks_even_with_files_and_requirement_trace():
    spec_service, _orchestration_service, _workflow, governed = _open_governed_workflow()
    spec_service.record_files_read_receipts(
        workflow_id=governed.tech_spec_workflow.workflow_id,
        reader_actor_id=governed.tech_spec_workflow.actor_id,
    )
    spec_service.compile_requirement_trace(
        workflow_id=governed.tech_spec_workflow.workflow_id,
        fr_id="FR-CMF-03.07",
        spec_sections=["Requirement Trace"],
        acceptance_criteria_refs=["AC1"],
        enforcement_mechanism="SpecAuditReceipt gate",
    )
    spec_service.run_cbar_check(
        workflow_id=governed.tech_spec_workflow.workflow_id,
        primitive_tension="workflow discipline vs stale stack",
        failure_scenario="spec omits pipeline trace",
        resolution_demand="block until pipeline trace exists",
        downstream_proof="PIPELINE_TRACE_MISSING finding",
        test_or_receipt_refs=["test_missing_pipeline_trace"],
    )

    audit = spec_service.audit_workflow(
        workflow_id=governed.tech_spec_workflow.workflow_id,
        spec_text=_clean_spec_text(),
    )

    assert audit.status == SpecAuditStatus.blocked
    assert any(finding.startswith("PIPELINE_TRACE_MISSING") for finding in audit.findings)


def test_greenfield_lint_blocks_old_stack_and_projection_drift():
    findings = greenfield_lint(
        """
        Existing Backend Integration says TypeScript is the source of truth.
        The agent can direct legacy_runtime imports, bypass the Command Bus,
        and use Neo4j as canonical truth.
        """
    )

    assert any(finding.startswith("GREENFIELD_ALIGNMENT_FAILED") for finding in findings)
    assert any(finding.startswith("LEGACY_RUNTIME_IMPORT_FORBIDDEN") for finding in findings)
    assert any(finding.startswith("COMMAND_BUS_BYPASS_FORBIDDEN") for finding in findings)
    assert any(finding.startswith("PROJECTION_NOT_CANONICAL") for finding in findings)


def test_rscs_weak_project_context_requests_revision_not_block():
    spec_service, _orchestration_service, _workflow, governed = _open_governed_workflow()
    _record_required_governance(spec_service, governed)

    audit = spec_service.audit_workflow(
        workflow_id=governed.tech_spec_workflow.workflow_id,
        spec_text=_clean_spec_text() + "\nThis will improve user engagement with high quality content.",
    )

    assert audit.status == SpecAuditStatus.revision_requested
    assert any(finding.startswith("RSCS_PROJECT_CONTEXT_WEAK") for finding in audit.findings)


def test_spec_artifact_writer_requires_accepted_audit(tmp_path):
    spec_service, _orchestration_service, _workflow, governed = _open_governed_workflow()
    _record_required_governance(spec_service, governed)
    accepted = spec_service.audit_workflow(
        workflow_id=governed.tech_spec_workflow.workflow_id,
        spec_text=_clean_spec_text(),
    )

    target = spec_service.write_spec_artifact(
        audit_receipt=accepted,
        target_path=str(tmp_path / "accepted-spec.md"),
        content=_clean_spec_text(),
    )

    assert target.exists()
    assert target.read_text(encoding="utf-8").startswith("\n## Files Read")
