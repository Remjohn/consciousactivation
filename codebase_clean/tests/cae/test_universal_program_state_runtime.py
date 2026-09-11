"""Comprehensive Boundary Proof Tests for Universal Program State Runtime.

Governed by Phase 2 Mandate M19 (TS-CAE-PROG-001, 20_PHASE2_CAE_PI_STATE_MAPPING.md).

Proves:
1. Universal Program State Runtime supports multiple distinct Programs (e.g. interview_semantic_program,
   collision_discovery_program, editorial_storyboard_program) using the same authoritative engine.
2. Step-by-step state machine execution advances monotonic versions, updates SHA-256 state hashes,
   and records cryptographic execution receipts.
3. Invalid transitions are blocked fail-closed (illegal state jumps, terminal states).
4. Four Authority Lanes (HUNTER, ANALYST, COMPOSER, COMMANDER) are strictly enforced.
5. Precondition claims are validated fail-closed prior to initialization and transition.
6. Optimistic concurrency locking blocks stale expected_version updates.
7. State-local context is dynamically assembled with allowable transitions and active lane filtering.
8. State repair is strictly governed by the COMMANDER lane with dedicated repair receipts.
9. Subordinate Pi session projection binds CAE run identities while preserving state authority.
10. Durable SQLite persistence guarantees transactional ACID storage and lossless transition replay.
"""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
from typing import Any, Dict
from uuid import UUID, uuid4

import pytest

from ca_contracts import canonical_sha256
from ca_runtime.pi_adapter import (
    AuthorityLane,
    CaePiRuntimeAdapter,
    PiSession,
    PiSessionState,
)
from ca_runtime.program_registry import (
    ProgramManifest,
    ProgramPackage,
    ProgramRegistry,
)
from ca_runtime.program_state_runtime import (
    InMemoryProgramStateStore,
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
    ProgramStateAggregateNotFoundError,
    ProgramStateLifecycle,
    ProgramStateLocalContext,
    ProgramStateMachineDefinition,
    ProgramStateRepairError,
    ProgramStateRuntimeError,
    ProgramStateTransition,
    ProgramStateVersionConflictError,
    ProgramTransitionBlockedError,
    ProgramTransitionContract,
    ProgramTransitionResult,
    SideEffectClass,
    SqliteProgramStateStore,
    UniversalProgramStateRuntime,
    get_canonical_collision_state_machine,
    get_canonical_interview_state_machine,
    get_canonical_storyboard_state_machine,
)


@pytest.fixture
def programs_root() -> Path:
    return Path("programs").resolve()


@pytest.fixture
def program_registry(programs_root: Path) -> ProgramRegistry:
    registry = ProgramRegistry(discovery_roots=[programs_root])
    registry.discover()
    return registry


@pytest.fixture
def runtime(program_registry: ProgramRegistry) -> UniversalProgramStateRuntime:
    store = InMemoryProgramStateStore()
    return UniversalProgramStateRuntime(store=store, program_registry=program_registry)


# ============================================================================
# 1. Distinct Programs on Single State Runtime
# ============================================================================

def test_runtime_initializes_and_persists_distinct_programs(
    runtime: UniversalProgramStateRuntime,
    program_registry: ProgramRegistry,
) -> None:
    ws_id = str(uuid4())
    actor_id = "actor_operator_01"

    # Program 1: interview_semantic_program
    pkg_interview = program_registry.get_program("interview_semantic_program")
    agg_interview = runtime.initialize_program_state(
        program_package=pkg_interview,
        workspace_id=ws_id,
        actor_id=actor_id,
        initial_data={"guest_id": "guest_123"},
        context_claims=["workspace_active", "interview_brief_approved"],
    )

    # Program 2: collision_discovery_program
    pkg_collision = program_registry.get_program("collision_discovery_program")
    agg_collision = runtime.initialize_program_state(
        program_package=pkg_collision,
        workspace_id=ws_id,
        actor_id=actor_id,
        initial_data={"signal_count": 42},
        context_claims=["workspace_active", "guest_profile_verified"],
    )

    assert agg_interview.aggregate_id != agg_collision.aggregate_id
    assert agg_interview.program_id == "interview_semantic_program"
    assert agg_collision.program_id == "collision_discovery_program"
    assert agg_interview.current_state == "INITIAL"
    assert agg_collision.current_state == "INITIAL"
    assert agg_interview.version == 1
    assert agg_collision.version == 1
    assert agg_interview.lifecycle == ProgramStateLifecycle.INITIALIZED
    assert agg_collision.lifecycle == ProgramStateLifecycle.INITIALIZED
    assert len(agg_interview.state_hash) == 64
    assert len(agg_collision.state_hash) == 64


# ============================================================================
# 2. Lifecycle Execution & Monotonic Version Advances
# ============================================================================

def test_interview_program_state_machine_execution_lifecycle(
    runtime: UniversalProgramStateRuntime,
    program_registry: ProgramRegistry,
) -> None:
    ws_id = str(uuid4())
    actor_id = "actor_hunter_01"
    pkg = program_registry.get_program("interview_semantic_program")

    # 1. Initialize (v1)
    agg = runtime.initialize_program_state(
        program_package=pkg,
        workspace_id=ws_id,
        actor_id=actor_id,
        initial_data={"session_id": "sess_1"},
        context_claims=["workspace_active", "interview_brief_approved"],
    )
    assert agg.version == 1
    assert agg.current_state == "INITIAL"

    # 2. Transition: start_elicitation (INITIAL -> QUESTIONING, HUNTER lane) -> v2
    res1 = runtime.execute_transition(
        aggregate_id=agg.aggregate_id,
        transition_name="start_elicitation",
        actor_id=actor_id,
        actor_lane=AuthorityLane.HUNTER,
        context_claims=["workspace_active", "interview_brief_approved"],
        expected_version=1,
        state_updates={"audio_source_registered": True},
    )
    assert res1.aggregate.version == 2
    assert res1.aggregate.current_state == "QUESTIONING"
    assert res1.aggregate.lifecycle == ProgramStateLifecycle.RUNNING
    assert res1.aggregate.state_data["audio_source_registered"] is True
    assert res1.transition.from_state == "INITIAL"
    assert res1.transition.to_state == "QUESTIONING"
    assert res1.receipt["receipt_type"] == "cae_execution_receipt"
    assert len(res1.audit_digest) == 64

    # 3. Transition: record_turn (QUESTIONING -> QUESTIONING, HUNTER lane) -> v3
    res2 = runtime.execute_transition(
        aggregate_id=agg.aggregate_id,
        transition_name="record_turn",
        actor_id=actor_id,
        actor_lane=AuthorityLane.HUNTER,
        context_claims=["workspace_active"],
        expected_version=2,
        state_updates={"turns_count": 1},
    )
    assert res2.aggregate.version == 3
    assert res2.aggregate.current_state == "QUESTIONING"
    assert res2.aggregate.state_data["turns_count"] == 1

    # 4. Transition: begin_transcription (QUESTIONING -> TRANSCRIBING, ANALYST lane) -> v4
    res3 = runtime.execute_transition(
        aggregate_id=agg.aggregate_id,
        transition_name="begin_transcription",
        actor_id="actor_analyst_01",
        actor_lane=AuthorityLane.ANALYST,
        context_claims=["workspace_active"],
        expected_version=3,
        state_updates={"transcription_started": True},
    )
    assert res3.aggregate.version == 4
    assert res3.aggregate.current_state == "TRANSCRIBING"

    # 5. Transition: complete_interview (TRANSCRIBING -> COMPLETED, ANALYST lane) -> v5
    res4 = runtime.execute_transition(
        aggregate_id=agg.aggregate_id,
        transition_name="complete_interview",
        actor_id="actor_analyst_01",
        actor_lane=AuthorityLane.ANALYST,
        context_claims=["workspace_active"],
        expected_version=4,
        state_updates={"completed_at": "2026-08-31T06:00:00Z"},
    )
    assert res4.aggregate.version == 5
    assert res4.aggregate.current_state == "COMPLETED"
    assert res4.aggregate.lifecycle == ProgramStateLifecycle.COMPLETED


def test_collision_program_state_machine_execution_lifecycle(
    runtime: UniversalProgramStateRuntime,
    program_registry: ProgramRegistry,
) -> None:
    ws_id = str(uuid4())
    pkg = program_registry.get_program("collision_discovery_program")

    # 1. Initialize (v1)
    agg = runtime.initialize_program_state(
        program_package=pkg,
        workspace_id=ws_id,
        actor_id="actor_hunter_01",
        context_claims=["workspace_active", "guest_profile_verified"],
    )

    # 2. ingest_corpus (INITIAL -> CORPUS_LOADED, HUNTER lane) -> v2
    res1 = runtime.execute_transition(
        aggregate_id=agg.aggregate_id,
        transition_name="ingest_corpus",
        actor_id="actor_hunter_01",
        actor_lane=AuthorityLane.HUNTER,
        context_claims=["workspace_active", "guest_profile_verified"],
        expected_version=1,
    )
    assert res1.aggregate.version == 2
    assert res1.aggregate.current_state == "CORPUS_LOADED"

    # 3. hunt_signals (CORPUS_LOADED -> SIGNAL_HUNTING, HUNTER lane) -> v3
    res2 = runtime.execute_transition(
        aggregate_id=agg.aggregate_id,
        transition_name="hunt_signals",
        actor_id="actor_hunter_01",
        actor_lane=AuthorityLane.HUNTER,
        context_claims=["workspace_active"],
        expected_version=2,
    )
    assert res2.aggregate.version == 3
    assert res2.aggregate.current_state == "SIGNAL_HUNTING"

    # 4. form_hypothesis (SIGNAL_HUNTING -> HYPOTHESIS_FORMED, ANALYST lane) -> v4
    res3 = runtime.execute_transition(
        aggregate_id=agg.aggregate_id,
        transition_name="form_hypothesis",
        actor_id="actor_analyst_01",
        actor_lane=AuthorityLane.ANALYST,
        context_claims=["workspace_active"],
        expected_version=3,
        state_updates={"hypothesis": "Semantic resonance between acoustic resonance and cognitive load"},
    )
    assert res3.aggregate.version == 4
    assert res3.aggregate.current_state == "HYPOTHESIS_FORMED"

    # 5. evaluate_collision (HYPOTHESIS_FORMED -> EVALUATED, ANALYST lane) -> v5
    res4 = runtime.execute_transition(
        aggregate_id=agg.aggregate_id,
        transition_name="evaluate_collision",
        actor_id="actor_analyst_01",
        actor_lane=AuthorityLane.ANALYST,
        context_claims=["workspace_active"],
        expected_version=4,
        state_updates={"novelty_score_bps": 9400},
    )
    assert res4.aggregate.version == 5
    assert res4.aggregate.current_state == "EVALUATED"

    # 6. operator_approve (EVALUATED -> APPROVED, COMMANDER lane) -> v6
    res5 = runtime.execute_transition(
        aggregate_id=agg.aggregate_id,
        transition_name="operator_approve",
        actor_id="actor_commander_01",
        actor_lane=AuthorityLane.COMMANDER,
        context_claims=["workspace_active", "operator_confirmed"],
        expected_version=5,
    )
    assert res5.aggregate.version == 6
    assert res5.aggregate.current_state == "APPROVED"
    assert res5.aggregate.lifecycle == ProgramStateLifecycle.COMPLETED


# ============================================================================
# 3. Fail-Closed Boundary & Validation Tests
# ============================================================================

def test_invalid_transition_from_current_state_blocked_fail_closed(
    runtime: UniversalProgramStateRuntime,
    program_registry: ProgramRegistry,
) -> None:
    pkg = program_registry.get_program("interview_semantic_program")
    agg = runtime.initialize_program_state(
        program_package=pkg,
        workspace_id=str(uuid4()),
        actor_id="actor_hunter_01",
        context_claims=["workspace_active", "interview_brief_approved"],
    )

    # Cannot skip directly from INITIAL to TRANSCRIBING or COMPLETED
    with pytest.raises(ProgramTransitionBlockedError, match="Cannot transition from 'INITIAL' to 'COMPLETED'"):
        runtime.execute_transition(
            aggregate_id=agg.aggregate_id,
            transition_name="complete_interview",
            actor_id="actor_analyst_01",
            actor_lane=AuthorityLane.ANALYST,
            context_claims=["workspace_active"],
            expected_version=1,
        )


def test_authority_lane_violation_blocked_fail_closed(
    runtime: UniversalProgramStateRuntime,
    program_registry: ProgramRegistry,
) -> None:
    pkg = program_registry.get_program("interview_semantic_program")
    agg = runtime.initialize_program_state(
        program_package=pkg,
        workspace_id=str(uuid4()),
        actor_id="actor_hunter_01",
        context_claims=["workspace_active", "interview_brief_approved"],
    )

    # start_elicitation requires HUNTER lane; invoking from COMPOSER or COMMANDER raises ProgramAuthorityLaneViolationError
    with pytest.raises(ProgramAuthorityLaneViolationError) as exc_info:
        runtime.execute_transition(
            aggregate_id=agg.aggregate_id,
            transition_name="start_elicitation",
            actor_id="actor_composer_01",
            actor_lane=AuthorityLane.COMPOSER,
            context_claims=["workspace_active", "interview_brief_approved"],
            expected_version=1,
        )
    assert exc_info.value.details["actor_lane"] == "COMPOSER"
    assert exc_info.value.details["required_lane"] == "HUNTER"


def test_missing_preconditions_blocked_fail_closed(
    runtime: UniversalProgramStateRuntime,
    program_registry: ProgramRegistry,
) -> None:
    pkg = program_registry.get_program("interview_semantic_program")

    # Initialization fails closed if manifest preconditions are missing
    with pytest.raises(ProgramTransitionBlockedError, match="Unsatisfied manifest preconditions"):
        runtime.initialize_program_state(
            program_package=pkg,
            workspace_id=str(uuid4()),
            actor_id="actor_hunter_01",
            context_claims=["workspace_active"],  # Missing interview_brief_approved
        )

    # Initialize with valid claims
    agg = runtime.initialize_program_state(
        program_package=pkg,
        workspace_id=str(uuid4()),
        actor_id="actor_hunter_01",
        context_claims=["workspace_active", "interview_brief_approved"],
    )

    # Transition fails closed if transition contract preconditions are missing
    with pytest.raises(ProgramTransitionBlockedError, match="Unsatisfied transition preconditions"):
        runtime.execute_transition(
            aggregate_id=agg.aggregate_id,
            transition_name="start_elicitation",
            actor_id="actor_hunter_01",
            actor_lane=AuthorityLane.HUNTER,
            context_claims=[],  # Missing workspace_active and interview_brief_approved
            expected_version=1,
        )


def test_optimistic_concurrency_version_conflict_blocked(
    runtime: UniversalProgramStateRuntime,
    program_registry: ProgramRegistry,
) -> None:
    pkg = program_registry.get_program("interview_semantic_program")
    agg = runtime.initialize_program_state(
        program_package=pkg,
        workspace_id=str(uuid4()),
        actor_id="actor_hunter_01",
        context_claims=["workspace_active", "interview_brief_approved"],
    )

    # Advance to version 2
    runtime.execute_transition(
        aggregate_id=agg.aggregate_id,
        transition_name="start_elicitation",
        actor_id="actor_hunter_01",
        actor_lane=AuthorityLane.HUNTER,
        context_claims=["workspace_active", "interview_brief_approved"],
        expected_version=1,
    )

    # Stale version update with expected_version=1 must be rejected
    with pytest.raises(ProgramStateVersionConflictError) as exc_info:
        runtime.execute_transition(
            aggregate_id=agg.aggregate_id,
            transition_name="record_turn",
            actor_id="actor_hunter_01",
            actor_lane=AuthorityLane.HUNTER,
            context_claims=["workspace_active"],
            expected_version=1,  # Stale! Actual is 2
        )
    assert exc_info.value.details["expected_version"] == 1
    assert exc_info.value.details["actual_version"] == 2


def test_terminal_state_blocks_further_transitions(
    runtime: UniversalProgramStateRuntime,
    program_registry: ProgramRegistry,
) -> None:
    pkg = program_registry.get_program("interview_semantic_program")
    agg = runtime.initialize_program_state(
        program_package=pkg,
        workspace_id=str(uuid4()),
        actor_id="actor_hunter_01",
        context_claims=["workspace_active", "interview_brief_approved"],
    )

    # Fast forward to completed
    runtime.execute_transition(
        aggregate_id=agg.aggregate_id,
        transition_name="start_elicitation",
        actor_id="actor_hunter_01",
        actor_lane=AuthorityLane.HUNTER,
        context_claims=["workspace_active", "interview_brief_approved"],
    )
    runtime.execute_transition(
        aggregate_id=agg.aggregate_id,
        transition_name="begin_transcription",
        actor_id="actor_analyst_01",
        actor_lane=AuthorityLane.ANALYST,
        context_claims=["workspace_active"],
    )
    res_comp = runtime.execute_transition(
        aggregate_id=agg.aggregate_id,
        transition_name="complete_interview",
        actor_id="actor_analyst_01",
        actor_lane=AuthorityLane.ANALYST,
        context_claims=["workspace_active"],
    )
    assert res_comp.aggregate.lifecycle == ProgramStateLifecycle.COMPLETED

    # Any subsequent transition on completed aggregate must fail
    with pytest.raises(ProgramTransitionBlockedError, match="terminal lifecycle state"):
        runtime.execute_transition(
            aggregate_id=agg.aggregate_id,
            transition_name="record_turn",
            actor_id="actor_hunter_01",
            actor_lane=AuthorityLane.HUNTER,
            context_claims=["workspace_active"],
        )


# ============================================================================
# 4. State-Local Context Assembly
# ============================================================================

def test_state_local_context_assembly(
    runtime: UniversalProgramStateRuntime,
    program_registry: ProgramRegistry,
) -> None:
    pkg = program_registry.get_program("interview_semantic_program")
    agg = runtime.initialize_program_state(
        program_package=pkg,
        workspace_id=str(uuid4()),
        actor_id="actor_hunter_01",
        context_claims=["workspace_active", "interview_brief_approved"],
    )

    # 1. At INITIAL state: allowable transitions include start_elicitation
    ctx_initial = runtime.get_local_context(agg.aggregate_id)
    assert "start_elicitation" in ctx_initial.allowable_transitions
    assert ctx_initial.program_manifest is not None
    assert ctx_initial.program_manifest.id == "interview_semantic_program"

    # Filtered by HUNTER lane
    ctx_hunter = runtime.get_local_context(agg.aggregate_id, active_lane=AuthorityLane.HUNTER)
    assert "start_elicitation" in ctx_hunter.allowable_transitions

    # Filtered by COMPOSER lane -> empty
    ctx_composer = runtime.get_local_context(agg.aggregate_id, active_lane=AuthorityLane.COMPOSER)
    assert ctx_composer.allowable_transitions == []


# ============================================================================
# 5. Governed State Repair & Recovery
# ============================================================================

def test_repair_state_and_recovery_lifecycle(
    runtime: UniversalProgramStateRuntime,
    program_registry: ProgramRegistry,
) -> None:
    pkg = program_registry.get_program("interview_semantic_program")
    agg = runtime.initialize_program_state(
        program_package=pkg,
        workspace_id=str(uuid4()),
        actor_id="actor_hunter_01",
        context_claims=["workspace_active", "interview_brief_approved"],
    )

    # Move to QUESTIONING
    runtime.execute_transition(
        aggregate_id=agg.aggregate_id,
        transition_name="start_elicitation",
        actor_id="actor_hunter_01",
        actor_lane=AuthorityLane.HUNTER,
        context_claims=["workspace_active", "interview_brief_approved"],
    )

    # Operator performs state repair under COMMANDER lane
    repair_res = runtime.repair_state(
        aggregate_id=agg.aggregate_id,
        repair_action="rollback_corrupted_audio_segment",
        repair_payload={"reason": "Microphone dropout detected", "segment_index": 3},
        actor_id="actor_commander_01",
        actor_lane=AuthorityLane.COMMANDER,
        target_state="QUESTIONING",
        state_updates={"audio_repaired": True, "resumed_from_turn": 2},
    )

    assert repair_res.aggregate.version == 3
    assert repair_res.aggregate.state_data["audio_repaired"] is True
    assert repair_res.aggregate.state_data["resumed_from_turn"] == 2
    assert repair_res.transition.trigger_operation == "repair_state"
    assert repair_res.transition.lane == AuthorityLane.COMMANDER
    assert repair_res.receipt["validator_results"]["repair_gate"] == "OPERATOR_AUTHORIZED"


def test_repair_state_rejects_non_commander_lane(
    runtime: UniversalProgramStateRuntime,
    program_registry: ProgramRegistry,
) -> None:
    pkg = program_registry.get_program("interview_semantic_program")
    agg = runtime.initialize_program_state(
        program_package=pkg,
        workspace_id=str(uuid4()),
        actor_id="actor_hunter_01",
        context_claims=["workspace_active", "interview_brief_approved"],
    )

    with pytest.raises(ProgramAuthorityLaneViolationError):
        runtime.repair_state(
            aggregate_id=agg.aggregate_id,
            repair_action="unauthorized_repair",
            repair_payload={},
            actor_id="actor_hunter_01",
            actor_lane=AuthorityLane.HUNTER,  # Non-COMMANDER rejected!
        )


# ============================================================================
# 6. Pi Session Projection
# ============================================================================

def test_pi_session_projection_and_execution_boundary(
    runtime: UniversalProgramStateRuntime,
    program_registry: ProgramRegistry,
) -> None:
    pkg = program_registry.get_program("interview_semantic_program")
    agg = runtime.initialize_program_state(
        program_package=pkg,
        workspace_id=str(uuid4()),
        actor_id="actor_hunter_01",
        context_claims=["workspace_active", "interview_brief_approved"],
    )

    pi_adapter = CaePiRuntimeAdapter()
    session = runtime.project_to_pi_session(
        aggregate_id=agg.aggregate_id,
        pi_adapter=pi_adapter,
        actor_id="actor_hunter_01",
        lane=AuthorityLane.HUNTER,
    )

    assert isinstance(session, PiSession)
    assert session.cae_run_id == agg.cae_run_id
    assert session.lane == AuthorityLane.HUNTER
    assert session.metadata["aggregate_id"] == agg.aggregate_id
    assert session.metadata["program_id"] == "interview_semantic_program"
    assert session.metadata["current_state"] == "INITIAL"
    assert session.metadata["aggregate_version"] == 1


# ============================================================================
# 7. Durable SQLite Persistence & Replay
# ============================================================================

def test_durable_sqlite_persistence_and_replay(
    program_registry: ProgramRegistry,
    tmp_path: Path,
) -> None:
    db_file = tmp_path / "cae_program_state.db"
    store1 = SqliteProgramStateStore(db_file)
    runtime1 = UniversalProgramStateRuntime(store=store1, program_registry=program_registry)

    ws_id = str(uuid4())
    pkg = program_registry.get_program("interview_semantic_program")

    # 1. Initialize in store1
    agg = runtime1.initialize_program_state(
        program_package=pkg,
        workspace_id=ws_id,
        actor_id="actor_hunter_01",
        context_claims=["workspace_active", "interview_brief_approved"],
        initial_data={"init_key": "init_val"},
    )
    agg_id = agg.aggregate_id

    # 2. Transition 1 in store1
    runtime1.execute_transition(
        aggregate_id=agg_id,
        transition_name="start_elicitation",
        actor_id="actor_hunter_01",
        actor_lane=AuthorityLane.HUNTER,
        context_claims=["workspace_active", "interview_brief_approved"],
        state_updates={"turn_count": 1},
    )

    # 3. Transition 2 in store1
    runtime1.execute_transition(
        aggregate_id=agg_id,
        transition_name="record_turn",
        actor_id="actor_hunter_01",
        actor_lane=AuthorityLane.HUNTER,
        context_claims=["workspace_active"],
        state_updates={"turn_count": 2},
    )

    # 4. Open a completely new store instance on the same SQLite file
    store2 = SqliteProgramStateStore(db_file)
    runtime2 = UniversalProgramStateRuntime(store=store2, program_registry=program_registry)

    loaded_agg = runtime2.get_aggregate(agg_id)
    assert loaded_agg is not None
    assert loaded_agg.version == 3
    assert loaded_agg.current_state == "QUESTIONING"
    assert loaded_agg.state_data["turn_count"] == 2
    assert loaded_agg.state_data["init_key"] == "init_val"

    # Verify transitions audit log
    transitions = store2.list_transitions(agg_id)
    assert len(transitions) == 2
    assert transitions[0].transition_name == "start_elicitation"
    assert transitions[0].committed_version == 2
    assert transitions[1].transition_name == "record_turn"
    assert transitions[1].committed_version == 3

    # 5. Continue execution seamlessly in runtime2 -> begin_transcription -> v4
    res_trans = runtime2.execute_transition(
        aggregate_id=agg_id,
        transition_name="begin_transcription",
        actor_id="actor_analyst_01",
        actor_lane=AuthorityLane.ANALYST,
        context_claims=["workspace_active"],
        expected_version=3,
        state_updates={"transcribed": True},
    )
    assert res_trans.aggregate.version == 4
    assert res_trans.aggregate.current_state == "TRANSCRIBING"

    transitions_updated = store2.list_transitions(agg_id)
    assert len(transitions_updated) == 3
