"""
tests.cae.test_program_operator_runtime
---------------------------------------
Authoritative test suite for CAE Mandate M46:
ProgramOperatorRuntimeService, multi-lane authority, CAS concurrency,
artifact lineage graph projection, execution trace, and chat command grammar.
"""

from __future__ import annotations

import pytest
from pathlib import Path

from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_registry import ProgramRegistry
from ca_runtime.program_state_runtime import (
    InMemoryProgramStateStore,
    ProgramAuthorityLaneViolationError,
    ProgramStateLifecycle,
    ProgramStateVersionConflictError,
    ProgramTransitionBlockedError,
    UniversalProgramStateRuntime,
    get_canonical_interview_state_machine,
    get_canonical_collision_state_machine,
    get_canonical_storyboard_state_machine,
)
from ca_runtime.program_operator_runtime import (
    ArtifactLineageGraph,
    ChatCommandResult,
    ExecutionTraceProjection,
    LineageNodeType,
    LineageVerificationStatus,
    OperatorActionType,
    ProgramOperatorRuntimeService,
    RejectionDispositionRoute,
)


@pytest.fixture
def state_runtime() -> UniversalProgramStateRuntime:
    store = InMemoryProgramStateStore()
    runtime = UniversalProgramStateRuntime(store=store)
    runtime.register_state_machine(get_canonical_interview_state_machine())
    runtime.register_state_machine(get_canonical_collision_state_machine())
    runtime.register_state_machine(get_canonical_storyboard_state_machine())
    return runtime


@pytest.fixture
def operator_service(state_runtime: UniversalProgramStateRuntime) -> ProgramOperatorRuntimeService:
    registry = ProgramRegistry(discovery_roots=[Path("programs").resolve()])
    registry.discover()
    return ProgramOperatorRuntimeService(
        runtime=state_runtime,
        program_registry=registry,
    )


# ============================================================================
# 1. Catalog & Discovery Operations
# ============================================================================

def test_list_catalog_and_inspect_definition(operator_service: ProgramOperatorRuntimeService):
    catalog = operator_service.list_catalog()
    assert len(catalog) >= 3
    prog_ids = [p["program_id"] for p in catalog]
    assert "interview_semantic_program" in prog_ids
    assert "collision_discovery_program" in prog_ids

    defn = operator_service.inspect_program_definition("interview_semantic_program")
    assert defn["program_id"] == "interview_semantic_program"
    assert "lanes" in defn
    assert "HUNTER" in defn["lanes"]
    assert "COMMANDER" in defn["lanes"]
    assert len(defn["package_sha256"]) == 64


# ============================================================================
# 2. Program Execution Lifecycle & CAS Protection
# ============================================================================

def test_run_and_inspect_program(operator_service: ProgramOperatorRuntimeService):
    agg = operator_service.run_program(
        program_id="interview_semantic_program",
        workspace_id="ws-tenant-01",
        actor_id="operator-alice",
        initial_data={"guest_id": "gst-101", "brief_id": "brf-202"},
    )
    assert agg.aggregate_id.startswith("prog-state:")
    assert agg.workspace_id == "ws-tenant-01"
    assert agg.program_id == "interview_semantic_program"
    assert agg.lifecycle == ProgramStateLifecycle.INITIALIZED or agg.lifecycle == ProgramStateLifecycle.RUNNING
    assert agg.version >= 1
    assert len(agg.state_hash) == 64

    # Inspect
    inspect_agg, ctx = operator_service.get_execution(agg.aggregate_id)
    assert inspect_agg.aggregate_id == agg.aggregate_id
    assert len(ctx.allowable_transitions) >= 1


def test_pause_and_resume_execution(operator_service: ProgramOperatorRuntimeService):
    agg = operator_service.run_program(
        program_id="interview_semantic_program",
        workspace_id="ws-tenant-01",
    )

    # Pause
    paused_agg = operator_service.pause_program(
        aggregate_id=agg.aggregate_id,
        expected_version=agg.version,
        expected_state_sha256=agg.state_hash,
    )
    assert paused_agg.lifecycle == ProgramStateLifecycle.PAUSED
    assert paused_agg.version == agg.version + 1

    # Resume
    resumed_agg = operator_service.resume_program(
        aggregate_id=agg.aggregate_id,
        expected_version=paused_agg.version,
        expected_state_sha256=paused_agg.state_hash,
    )
    assert resumed_agg.lifecycle == ProgramStateLifecycle.RUNNING
    assert resumed_agg.version == paused_agg.version + 1


def test_pause_rejects_stale_concurrency_cas(operator_service: ProgramOperatorRuntimeService):
    agg = operator_service.run_program(
        program_id="interview_semantic_program",
        workspace_id="ws-tenant-01",
    )

    # Stale version
    with pytest.raises(ProgramStateVersionConflictError) as exc_info:
        operator_service.pause_program(
            aggregate_id=agg.aggregate_id,
            expected_version=agg.version + 99,
            expected_state_sha256=agg.state_hash,
        )
    assert exc_info.value.expected_version == agg.version + 99

    # Stale SHA256
    with pytest.raises(ProgramStateVersionConflictError) as exc_info2:
        operator_service.pause_program(
            aggregate_id=agg.aggregate_id,
            expected_version=agg.version,
            expected_state_sha256="0" * 64,
        )
    assert exc_info2.value.actual_version == agg.version


# ============================================================================
# 3. Milestone Gate Authorization & Disposition Routing
# ============================================================================

def test_approve_milestone_gate(operator_service: ProgramOperatorRuntimeService):
    agg = operator_service.run_program(
        program_id="interview_semantic_program",
        workspace_id="ws-tenant-01",
    )

    res = operator_service.approve_program(
        aggregate_id=agg.aggregate_id,
        actor_id="operator-commander",
        gate_id="BRIEF_GATE",
        decision="APPROVE",
        expected_version=agg.version,
        expected_state_sha256=agg.state_hash,
        payload={"signoff_notes": "All claims verified authentic."},
    )
    assert res.receipt_id is not None
    assert res.aggregate.version == agg.version + 1
    assert res.aggregate.state_data.get("approvals") is not None
    assert res.aggregate.state_data["approvals"][0]["decision"] == "APPROVE"


def test_reject_milestone_with_disposition(operator_service: ProgramOperatorRuntimeService):
    agg = operator_service.run_program(
        program_id="interview_semantic_program",
        workspace_id="ws-tenant-01",
    )

    res = operator_service.reject_program(
        aggregate_id=agg.aggregate_id,
        actor_id="operator-reviewer",
        rejection_reason="Insufficient semantic tension in turn 3",
        disposition_route=RejectionDispositionRoute.RETURN_TO_HUNTER,
        expected_version=agg.version,
        expected_state_sha256=agg.state_hash,
    )
    assert res.aggregate.version == agg.version + 1
    assert res.aggregate.state_data["last_rejection"]["disposition_route"] == "RETURN_TO_HUNTER"
    assert res.aggregate.state_data["last_rejection"]["rejection_reason"] == "Insufficient semantic tension in turn 3"


def test_state_repair_governed_mutation(operator_service: ProgramOperatorRuntimeService):
    agg = operator_service.run_program(
        program_id="interview_semantic_program",
        workspace_id="ws-tenant-01",
    )

    res = operator_service.repair_program(
        aggregate_id=agg.aggregate_id,
        actor_id="operator-repairman",
        repair_action="override_quarantine",
        repair_payload={"repaired_field": "val_fixed"},
        expected_version=agg.version,
        expected_state_sha256=agg.state_hash,
    )
    assert res.aggregate.version == agg.version + 1
    assert res.aggregate.state_data["repaired_field"] == "val_fixed"
    assert len(res.aggregate.state_data.get("repairs", [])) >= 1


# ============================================================================
# 4. Lossless Artifact Lineage & Execution Trace Projections
# ============================================================================

def test_artifact_lineage_projection(operator_service: ProgramOperatorRuntimeService):
    agg = operator_service.run_program(
        program_id="interview_semantic_program",
        workspace_id="ws-tenant-01",
        initial_data={
            "evidence_spans": [
                {"id": "ev-01", "sha256": "a" * 64, "label": "Source Quote Audio"},
                {"id": "ev-02", "sha256": "b" * 64, "label": "Transcript Segment"},
            ]
        },
    )

    lineage = operator_service.project_artifact_lineage(agg.aggregate_id)
    assert lineage.aggregate_id == agg.aggregate_id
    assert lineage.is_lossless is True
    assert lineage.verification_status == LineageVerificationStatus.VERIFIED
    assert len(lineage.root_evidence_ids) == 2
    assert len(lineage.verification_digest) == 64
    assert any(n.node_id == "ev-01" for n in lineage.nodes)


def test_execution_trace_projection(operator_service: ProgramOperatorRuntimeService):
    agg = operator_service.run_program(
        program_id="interview_semantic_program",
        workspace_id="ws-tenant-01",
    )

    trace = operator_service.project_execution_trace(agg.aggregate_id)
    assert trace.aggregate_id == agg.aggregate_id
    assert trace.program_id == "interview_semantic_program"
    assert trace.version == agg.version
    assert len(trace.trace_nodes) >= 0


# ============================================================================
# 5. Chat Command Grammar Dispatching
# ============================================================================

def test_chat_command_discover(operator_service: ProgramOperatorRuntimeService):
    res = operator_service.dispatch_chat_command(
        command_str="/discover",
        workspace_id="ws-test",
    )
    assert res.success is True
    assert res.action_type == OperatorActionType.DISCOVER
    assert res.lane == AuthorityLane.ANALYST
    assert "Discovered" in res.message


def test_chat_command_run_and_supervise(operator_service: ProgramOperatorRuntimeService):
    # Run
    run_res = operator_service.dispatch_chat_command(
        command_str="/run interview_semantic_program",
        workspace_id="ws-test",
    )
    assert run_res.success is True
    assert run_res.action_type == OperatorActionType.RUN
    assert run_res.lane == AuthorityLane.COMMANDER
    agg_id = run_res.aggregate_id
    assert agg_id is not None
    assert run_res.state_version >= 1

    # Pause
    pause_res = operator_service.dispatch_chat_command(
        command_str=f"/pause {agg_id}",
        workspace_id="ws-test",
        current_aggregate_id=agg_id,
        expected_version=run_res.state_version,
        expected_state_sha256=run_res.state_hash,
    )
    assert pause_res.success is True
    assert pause_res.action_type == OperatorActionType.PAUSE
    assert pause_res.state_version == run_res.state_version + 1

    # Resume
    resume_res = operator_service.dispatch_chat_command(
        command_str=f"/resume {agg_id}",
        workspace_id="ws-test",
        current_aggregate_id=agg_id,
        expected_version=pause_res.state_version,
        expected_state_sha256=pause_res.state_hash,
    )
    assert resume_res.success is True
    assert resume_res.action_type == OperatorActionType.RESUME
    assert resume_res.state_version == pause_res.state_version + 1

    # Approve
    approve_res = operator_service.dispatch_chat_command(
        command_str=f'/approve {agg_id} gate_id="TEST_GATE"',
        workspace_id="ws-test",
        current_aggregate_id=agg_id,
        expected_version=resume_res.state_version,
        expected_state_sha256=resume_res.state_hash,
    )
    assert approve_res.success is True
    assert approve_res.action_type == OperatorActionType.APPROVE
    assert approve_res.state_version == resume_res.state_version + 1


def test_chat_command_unknown_verb(operator_service: ProgramOperatorRuntimeService):
    res = operator_service.dispatch_chat_command(
        command_str="/teleport to mars",
        workspace_id="ws-test",
    )
    assert res.success is False
    assert "Unknown command" in res.message
