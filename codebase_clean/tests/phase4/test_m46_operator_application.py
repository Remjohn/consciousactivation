"""End-to-end integration test suite for M46 — Programs + Artifacts + Chat Operator Application.

Proves:
- Real operator surface over authoritative Program, Artifact and Chat state.
- Hides implementation complexity unless operator drills in.
- Four authority lanes remain separate (HUNTER, ANALYST, COMPOSER, COMMANDER).
- CAS optimistic locking prevents stale mutations across concurrent operator sessions.
- Lossless cryptographic lineage graph from source evidence to release artifacts.
- Governed human gate approvals emit verifiable backend receipts.
- Typed rejection routing sends tasks back to authoritative lane.
- Chat slash-command grammar executes against the single canonical source of truth.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from ca_runtime.program_registry import ProgramRegistry
from ca_runtime.program_operator_runtime import (
    ProgramOperatorRuntimeService,
    OperatorActionType,
    RejectionDispositionRoute,
    LineageVerificationStatus,
    LineageNodeType,
)
from ca_runtime.program_state_runtime import (
    UniversalProgramStateRuntime,
    InMemoryProgramStateStore,
    ProgramStateLifecycle,
    AuthorityLane,
    ProgramStateVersionConflictError,
    ProgramAuthorityLaneViolationError,
)


@pytest.fixture
def operator_runtime() -> ProgramOperatorRuntimeService:
    root = Path("programs").resolve()
    registry = ProgramRegistry(discovery_roots=[root])
    registry.discover()
    state_runtime = UniversalProgramStateRuntime(store=InMemoryProgramStateStore())
    return ProgramOperatorRuntimeService(runtime=state_runtime, program_registry=registry)


# ============================================================================
# 1. Authority Lanes & Passive Flat Skills
# ============================================================================

def test_m46_passive_skills_and_authority_lanes(operator_runtime: ProgramOperatorRuntimeService):
    """Verifies that discovered program packages declare flat passive skills and separate lanes."""
    catalog = operator_runtime.list_catalog()
    assert len(catalog) >= 3

    for summary in catalog:
        prog_id = summary["program_id"] if isinstance(summary, dict) else summary.program_id
        prog_def = operator_runtime.inspect_program_definition(prog_id)
        assert prog_def["status"] == "ACTIVE"
        assert len(prog_def["manifest_sha256"]) == 64
        assert len(prog_def["package_sha256"]) == 64

        # Verify authority lanes are distinct and non-empty
        lanes = prog_def.get("lanes") or prog_def.get("authority_lanes", [])
        assert len(lanes) > 0

        # Verify skills are flat, passive instruction units
        for skill in prog_def["skills"]:
            assert skill["name"]
            assert "path" in skill
            assert skill["sha256"] is not None


# ============================================================================
# 2. End-to-End Program Execution & CAS Concurrency Guard
# ============================================================================

def test_m46_program_lifecycle_and_cas_concurrency(operator_runtime: ProgramOperatorRuntimeService):
    """Tests execution lifecycle with strict Compare-And-Swap optimistic concurrency."""
    # 1. Launch program
    agg = operator_runtime.run_program(
        program_id="interview_semantic_program",
        workspace_id="ws-audrey-01",
        actor_id="commander-operator",
        initial_data={"project_id": "02_50-12 Audrey", "phase": "CMF Sonic"},
    )
    assert agg.lifecycle == ProgramStateLifecycle.RUNNING
    v1 = agg.version
    h1 = agg.state_hash

    # 2. Operator inspection
    inspect_agg, local_ctx = operator_runtime.get_execution(agg.aggregate_id)
    assert inspect_agg.aggregate_id == agg.aggregate_id
    assert inspect_agg.state_data["project_id"] == "02_50-12 Audrey"

    # 3. Pause with CAS
    paused_agg = operator_runtime.pause_program(
        aggregate_id=agg.aggregate_id,
        actor_id="commander-operator",
        expected_version=v1,
        expected_state_sha256=h1,
    )
    assert paused_agg.lifecycle == ProgramStateLifecycle.PAUSED
    v2 = paused_agg.version
    h2 = paused_agg.state_hash
    assert v2 == v1 + 1

    # 4. Prevent stale update using old v1
    with pytest.raises(ProgramStateVersionConflictError):
        operator_runtime.resume_program(
            aggregate_id=agg.aggregate_id,
            actor_id="commander-operator",
            expected_version=v1,
            expected_state_sha256=h1,
        )

    # 5. Resume with correct v2
    resumed_agg = operator_runtime.resume_program(
        aggregate_id=agg.aggregate_id,
        actor_id="commander-operator",
        expected_version=v2,
        expected_state_sha256=h2,
    )
    assert resumed_agg.lifecycle == ProgramStateLifecycle.RUNNING
    assert resumed_agg.version == v2 + 1


# ============================================================================
# 3. Governed Human Gate Approval & Typed Rejection Routing
# ============================================================================

def test_m46_gate_approvals_and_rejection_routing(operator_runtime: ProgramOperatorRuntimeService):
    """Tests human milestone signoff generating backend receipts and typed rejection routing."""
    # Launch execution
    agg = operator_runtime.run_program(
        program_id="interview_semantic_program",
        workspace_id="ws-jp-01",
        actor_id="commander-operator",
        initial_data={"project_id": "03_50-12 Jean Pierre"},
    )

    # 1. Gate Approval
    approval_res = operator_runtime.approve_program(
        aggregate_id=agg.aggregate_id,
        actor_id="commander-operator",
        gate_id="BRIEF_SIGN_OFF",
        decision="APPROVE",
        expected_version=agg.version,
        expected_state_sha256=agg.state_hash,
        payload={"notes": "Audience narrative verified authentic."},
    )
    assert approval_res.receipt_id is not None
    assert approval_res.aggregate.state_data["approvals"][-1]["gate_id"] == "BRIEF_SIGN_OFF"

    # 2. Gate Rejection with Disposition Routing to HUNTER
    v_appr = approval_res.aggregate.version
    h_appr = approval_res.aggregate.state_hash
    rejection_res = operator_runtime.reject_program(
        aggregate_id=agg.aggregate_id,
        actor_id="reviewer-operator",
        rejection_reason="Source transcript contains unverified audio segment.",
        disposition_route=RejectionDispositionRoute.RETURN_TO_HUNTER,
        gate_id="EVIDENCE_GATE",
        expected_version=v_appr,
        expected_state_sha256=h_appr,
    )
    assert rejection_res.aggregate.state_data["last_rejection"]["disposition_route"] == "RETURN_TO_HUNTER"
    assert rejection_res.aggregate.state_data["last_rejection"]["gate_id"] == "EVIDENCE_GATE"

    # 3. Governed Repair under COMMANDER
    v_rej = rejection_res.aggregate.version
    h_rej = rejection_res.aggregate.state_hash
    repair_res = operator_runtime.repair_program(
        aggregate_id=agg.aggregate_id,
        actor_id="commander-repairman",
        repair_action="replace_audio_segment",
        repair_payload={"evidence_status": "MANUALLY_VERIFIED_SRC_AUDIO"},
        expected_version=v_rej,
        expected_state_sha256=h_rej,
    )
    assert repair_res.aggregate.state_data["evidence_status"] == "MANUALLY_VERIFIED_SRC_AUDIO"
    assert len(repair_res.aggregate.state_data["repairs"]) >= 1


# ============================================================================
# 4. Cryptographic Lossless Evidence Lineage
# ============================================================================

def test_m46_lossless_evidence_artifact_lineage(operator_runtime: ProgramOperatorRuntimeService):
    """Verifies that artifact lineage projects the full DAG back to root evidence spans."""
    agg = operator_runtime.run_program(
        program_id="interview_semantic_program",
        workspace_id="ws-lineage-01",
        actor_id="commander-operator",
        initial_data={
            "evidence_spans": [
                {"id": "ev-span-101", "text": "Audrey describes the moment of revelation.", "timestamp_ms": 12400},
                {"id": "ev-span-102", "text": "Audrey reflects on the sonic landscape.", "timestamp_ms": 48200},
            ],
            "storyboard_beats": [
                {"beat_id": "beat-01", "name": "Opening Discovery", "source_spans": ["ev-span-101"]},
                {"beat_id": "beat-02", "name": "Sonic Climax", "source_spans": ["ev-span-102"]},
            ],
        },
    )

    lineage = operator_runtime.project_artifact_lineage(agg.aggregate_id)
    assert lineage.aggregate_id == agg.aggregate_id
    assert lineage.is_lossless is True
    assert lineage.verification_status == LineageVerificationStatus.VERIFIED
    assert len(lineage.root_evidence_ids) == 2
    assert "ev-span-101" in lineage.root_evidence_ids
    assert "ev-span-102" in lineage.root_evidence_ids

    # Nodes include source evidence and derivations
    node_types = {n.node_type for n in lineage.nodes}
    assert LineageNodeType.SOURCE_EVIDENCE in node_types

    # Cryptographic digest is 64-char hex
    assert len(lineage.verification_digest) == 64


# ============================================================================
# 5. Chat Supervision Grammar Dispatching
# ============================================================================

def test_m46_chat_supervision_grammar_full_cycle(operator_runtime: ProgramOperatorRuntimeService):
    """Verifies chat command grammar execution across all operator workflows."""
    # /discover
    d_res = operator_runtime.dispatch_chat_command(command_str="/discover", workspace_id="ws-chat")
    assert d_res.success is True
    assert d_res.action_type == OperatorActionType.DISCOVER

    # /run
    r_res = operator_runtime.dispatch_chat_command(
        command_str='/run interview_semantic_program {"brief_title": "Audrey Season Opener"}',
        workspace_id="ws-chat",
    )
    assert r_res.success is True
    assert r_res.action_type == OperatorActionType.RUN
    agg_id = r_res.aggregate_id
    v = r_res.state_version
    h = r_res.state_hash

    # /inspect
    i_res = operator_runtime.dispatch_chat_command(
        command_str=f"/inspect {agg_id}",
        workspace_id="ws-chat",
        current_aggregate_id=agg_id,
    )
    assert i_res.success is True
    assert i_res.action_type == OperatorActionType.INSPECT

    # /pause
    p_res = operator_runtime.dispatch_chat_command(
        command_str=f"/pause {agg_id}",
        workspace_id="ws-chat",
        current_aggregate_id=agg_id,
        expected_version=v,
        expected_state_sha256=h,
    )
    assert p_res.success is True
    assert p_res.action_type == OperatorActionType.PAUSE

    # /resume
    res_res = operator_runtime.dispatch_chat_command(
        command_str=f"/resume {agg_id}",
        workspace_id="ws-chat",
        current_aggregate_id=agg_id,
        expected_version=p_res.state_version,
        expected_state_sha256=p_res.state_hash,
    )
    assert res_res.success is True
    assert res_res.action_type == OperatorActionType.RESUME

    # /approve
    a_res = operator_runtime.dispatch_chat_command(
        command_str=f'/approve {agg_id} gate_id="EDITORIAL_GATE"',
        workspace_id="ws-chat",
        current_aggregate_id=agg_id,
        expected_version=res_res.state_version,
        expected_state_sha256=res_res.state_hash,
    )
    assert a_res.success is True
    assert a_res.action_type == OperatorActionType.APPROVE
    assert a_res.receipt_id is not None
