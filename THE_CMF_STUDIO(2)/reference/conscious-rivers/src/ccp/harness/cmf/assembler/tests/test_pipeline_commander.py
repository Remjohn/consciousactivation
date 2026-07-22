"""
Tests for pipeline_commander.py — FR-VID-09 Video Pipeline Commander.

Covers: state machine transitions, beat approvals, auto-approve, cost tracking,
checkpoint system, batch queue, review UI state, and receipt writing.
"""

import json
import os
import tempfile

import pytest

from pipeline_commander import (
    AUTO_APPROVE_THRESHOLD,
    COST_I2V_PER_CLIP,
    COST_T2I_PER_KEYFRAME,
    DEFAULT_CONCURRENT_LIMIT,
    MAX_REGENERATIONS_PER_BEAT,
    PIPELINE_STATES,
    PIPELINE_STATES_SET,
    VALID_TRANSITIONS,
    approve_all_beats,
    approve_beat,
    auto_approve_if_eligible,
    build_regeneration_dispatch,
    build_review_state,
    check_auto_approve_eligible,
    complete_job,
    compute_generation_cost,
    create_job_queue,
    create_pipeline_state,
    dequeue_next,
    enqueue_job,
    find_checkpoint,
    generate_pipeline_id,
    get_queue_status,
    load_checkpoint,
    request_regeneration,
    run_batch_queue_manage,
    run_pipeline_init,
    serialize_checkpoint,
    set_quality_scores,
    transition_state,
    transition_to_failed,
    update_cost,
    validate_transition,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_state(beat_count=4, current_state="PENDING"):
    state = create_pipeline_state("BC-TEST-001", "proj-01", beat_count)
    if current_state != "PENDING":
        # Walk through valid transitions to reach target state
        # For testing, just set directly
        state["current_state"] = current_state
        state["state_history"].append(
            {"state": current_state, "entered_at": "2026-03-21T00:00:00+00:00"}
        )
    return state


# ---------------------------------------------------------------------------
# TestStateMachine — TD1
# ---------------------------------------------------------------------------


class TestStateMachine:
    """TD1: Explicit state machine with validated transitions."""

    def test_16_states_defined(self):
        assert len(PIPELINE_STATES) == 16
        assert len(PIPELINE_STATES_SET) == 16

    def test_all_states_in_transitions(self):
        for state in PIPELINE_STATES:
            assert state in VALID_TRANSITIONS

    def test_valid_transition_pending_to_t2i(self):
        valid, reason = validate_transition("PENDING", "GENERATING_T2I")
        assert valid is True

    def test_valid_transition_pending_to_audio(self):
        valid, reason = validate_transition("PENDING", "PROCESSING_AUDIO")
        assert valid is True

    def test_illegal_transition_pending_to_final(self):
        """AC1: Illegal transition PENDING → RENDERING_FINAL is rejected."""
        valid, reason = validate_transition("PENDING", "RENDERING_FINAL")
        assert valid is False
        assert "Illegal transition" in reason

    def test_illegal_skip_quality_gate(self):
        """AC1: Cannot skip QUALITY_GATE — T2I → I2V directly."""
        valid, reason = validate_transition("GENERATING_T2I", "GENERATING_I2V")
        assert valid is False

    def test_unknown_state_rejected(self):
        valid, reason = validate_transition("NONEXISTENT", "PENDING")
        assert valid is False
        assert "Unknown" in reason

    def test_failed_is_terminal(self):
        assert VALID_TRANSITIONS["FAILED"] == set()

    def test_published_is_terminal(self):
        assert VALID_TRANSITIONS["PUBLISHED"] == set()

    def test_any_state_can_fail(self):
        """Every non-terminal state can transition to FAILED."""
        for state in PIPELINE_STATES:
            if state not in ("FAILED", "PUBLISHED", "APPROVED"):
                assert "FAILED" in VALID_TRANSITIONS[state], (
                    f"{state} should allow transition to FAILED"
                )


class TestStateTransitions:
    """State machine mutation via transition_state."""

    def test_transition_success(self):
        state = _make_state()
        success, reason = transition_state(state, "GENERATING_T2I")
        assert success is True
        assert state["current_state"] == "GENERATING_T2I"
        assert len(state["state_history"]) == 2

    def test_transition_failure(self):
        state = _make_state()
        success, reason = transition_state(state, "RENDERING_FINAL")
        assert success is False
        assert state["current_state"] == "PENDING"  # Unchanged

    def test_transition_with_metadata(self):
        state = _make_state()
        success, _ = transition_state(
            state, "GENERATING_T2I", metadata={"beat_count": 12}
        )
        assert success is True
        assert state["state_history"][-1]["metadata"]["beat_count"] == 12

    def test_transition_to_failed(self):
        state = _make_state()
        success = transition_to_failed(state, "T2I_TIMEOUT")
        assert success is True
        assert state["current_state"] == "FAILED"
        assert state["error"] == "T2I_TIMEOUT"

    def test_ac1_correct_sequence(self):
        """AC1: Full valid sequence without skipping states."""
        state = _make_state()
        sequence = [
            "GENERATING_T2I", "QUALITY_GATE", "GENERATING_I2V",
            "FINGERPRINTING", "ASSEMBLING_MANIFEST",
            "GENERATING_CAPTIONS", "RENDERING_PREVIEW", "READY_FOR_REVIEW",
            "RENDERING_FINAL", "APPROVED",
        ]
        for next_s in sequence:
            success, reason = transition_state(state, next_s)
            assert success is True, f"Failed transition to {next_s}: {reason}"
        assert state["current_state"] == "APPROVED"
        assert len(state["state_history"]) == 11  # PENDING + 10 transitions


# ---------------------------------------------------------------------------
# TestPipelineStateCreation
# ---------------------------------------------------------------------------


class TestPipelineStateCreation:
    """Pipeline state initialization."""

    def test_create_state(self):
        state = create_pipeline_state("BC-001", "proj-01", 12)
        assert state["current_state"] == "PENDING"
        assert state["beat_cluster_id"] == "BC-001"
        assert len(state["beat_approvals"]) == 12
        assert state["total_generation_cost_usd"] == 0.0

    def test_pipeline_id_format(self):
        pid = generate_pipeline_id()
        assert pid.startswith("PIPE-")
        parts = pid.split("-")
        assert len(parts) == 3
        assert len(parts[1]) == 8

    def test_beat_approvals_initialized(self):
        state = create_pipeline_state("BC-001", "proj-01", 4)
        for ba in state["beat_approvals"]:
            assert ba["status"] == "PENDING_REVIEW"
            assert ba["regeneration_count"] == 0
            assert ba["quality_score"] is None


# ---------------------------------------------------------------------------
# TestBeatApprovals
# ---------------------------------------------------------------------------


class TestBeatApprovals:
    """Beat-level approval management."""

    def test_approve_single_beat(self):
        state = _make_state(beat_count=4)
        success, _ = approve_beat(state, 2)
        assert success is True
        assert state["beat_approvals"][2]["status"] == "APPROVED"

    def test_approve_nonexistent_beat(self):
        state = _make_state(beat_count=4)
        success, reason = approve_beat(state, 99)
        assert success is False
        assert "not found" in reason

    def test_approve_all(self):
        state = _make_state(beat_count=6)
        count = approve_all_beats(state)
        assert count == 6
        assert all(ba["status"] == "APPROVED" for ba in state["beat_approvals"])

    def test_request_regeneration(self):
        state = _make_state(beat_count=4)
        success, _ = request_regeneration(state, 1, "T2I_ONLY", "warmer lighting")
        assert success is True
        assert state["beat_approvals"][1]["status"] == "REGENERATING"
        assert state["beat_approvals"][1]["regeneration_mode"] == "T2I_ONLY"
        assert state["beat_approvals"][1]["regeneration_count"] == 1
        assert state["total_regenerations"] == 1

    def test_regeneration_invalid_mode(self):
        state = _make_state()
        success, reason = request_regeneration(state, 0, "INVALID", "note")
        assert success is False
        assert "Invalid mode" in reason

    def test_regeneration_empty_note(self):
        state = _make_state()
        success, reason = request_regeneration(state, 0, "T2I_ONLY", "")
        assert success is False
        assert "required" in reason

    def test_regeneration_limit_enforced(self):
        """Safety: Infinite regeneration prevention."""
        state = _make_state(beat_count=1)
        for i in range(MAX_REGENERATIONS_PER_BEAT):
            success, _ = request_regeneration(state, 0, "T2I_ONLY", f"attempt {i+1}")
            assert success is True

        # 11th should fail
        success, reason = request_regeneration(state, 0, "T2I_ONLY", "one more")
        assert success is False
        assert "maximum" in reason

    def test_set_quality_scores(self):
        state = _make_state(beat_count=4)
        set_quality_scores(state, {0: 0.85, 1: 0.72, 2: 0.91, 3: 0.68})
        assert state["beat_approvals"][0]["quality_score"] == 0.85
        assert state["beat_approvals"][3]["quality_score"] == 0.68


class TestRegenerationDispatch:
    def test_build_dispatch_for_timing_rebalance(self):
        plan = {
            "mode": "T2I_ONLY",
            "pipeline_calls": ["FR-VID-02", "FR-VID-04", "FR-VID-03"],
            "patch_selection": {
                "target_beat_index": 3,
                "patch_profile": "TIMING_REBALANCE_PATCH",
                "timing_patch_required": True,
                "targeted_fields": [
                    "/beats/3/duration_sec",
                    "/beats/3/transition",
                    "/beats/3/fallback_image_url",
                    "/beats/3/video_clip_url",
                ],
                "neighbor_consultation_indices": [2, 4],
                "corrective_moves": ["retime_neighbor_window", "extend_hold"],
            },
        }

        dispatch = build_regeneration_dispatch(plan)

        assert dispatch["patch_profile"] == "TIMING_REBALANCE_PATCH"
        assert dispatch["module_dispatch"]["FR-VID-02"]["operation"] == "prompt_refresh"
        assert dispatch["module_dispatch"]["FR-VID-03"]["operation"] == "retime_neighbors"
        assert "/beats/3/fallback_image_url" in dispatch["module_dispatch"]["FR-VID-02"]["targeted_fields"]
        assert "/beats/3/duration_sec" in dispatch["module_dispatch"]["FR-VID-03"]["targeted_fields"]
        assert dispatch["manifest_patch"]["neighbor_consultation_indices"] == [2, 4]

    def test_build_dispatch_preserves_surprise_patch_contract(self):
        plan = {
            "mode": "I2V_ONLY",
            "pipeline_calls": ["FR-VID-03"],
            "patch_selection": {
                "target_beat_index": 1,
                "patch_profile": "TARGETED_VISUAL_PATCH",
                "timing_patch_required": False,
                "surprise_patch_required": True,
                "surprise_adjustment": "restore_surprise",
                "surprise_score": 0.22,
                "targeted_fields": [
                    "/beats/1/transition",
                    "/beats/1/video_clip_url",
                ],
                "neighbor_consultation_indices": [],
                "corrective_moves": ["escalate_schema_break"],
            },
        }

        dispatch = build_regeneration_dispatch(plan)

        assert dispatch["manifest_patch"]["surprise_patch_required"] is True
        assert dispatch["manifest_patch"]["surprise_adjustment"] == "restore_surprise"
        assert dispatch["manifest_patch"]["surprise_score"] == 0.22


# ---------------------------------------------------------------------------
# TestAutoApprove — TD5
# ---------------------------------------------------------------------------


class TestAutoApprove:
    """TD5: Auto-approve for all beats ≥ 0.8."""

    def test_eligible_all_high_scores(self):
        state = _make_state(beat_count=4)
        set_quality_scores(state, {0: 0.85, 1: 0.82, 2: 0.91, 3: 0.80})
        assert check_auto_approve_eligible(state) is True

    def test_not_eligible_one_low_score(self):
        state = _make_state(beat_count=4)
        set_quality_scores(state, {0: 0.85, 1: 0.72, 2: 0.91, 3: 0.80})
        assert check_auto_approve_eligible(state) is False

    def test_not_eligible_no_scores(self):
        state = _make_state(beat_count=4)
        assert check_auto_approve_eligible(state) is False

    def test_auto_approve_success(self):
        """AC5: All 12 beats ≥ 0.8 → auto-approve skips review."""
        state = _make_state(beat_count=12)
        scores = {i: 0.82 + (i * 0.01) for i in range(12)}
        set_quality_scores(state, scores)
        approved, reason = auto_approve_if_eligible(state)
        assert approved is True
        assert reason == "AUTO_APPROVED"
        assert all(ba["status"] == "APPROVED" for ba in state["beat_approvals"])

    def test_auto_approve_rejected(self):
        state = _make_state(beat_count=4)
        set_quality_scores(state, {0: 0.50, 1: 0.60, 2: 0.70, 3: 0.80})
        approved, reason = auto_approve_if_eligible(state)
        assert approved is False

    def test_threshold_value(self):
        assert AUTO_APPROVE_THRESHOLD == 0.8


# ---------------------------------------------------------------------------
# TestCostTracking — AC7
# ---------------------------------------------------------------------------


class TestCostTracking:
    """AC7: Correct cumulative cost based on T2I + I2V + regeneration costs."""

    def test_base_cost_12_beats(self):
        cost = compute_generation_cost(12)
        expected = 12 * (COST_T2I_PER_KEYFRAME + COST_I2V_PER_CLIP)
        assert cost == round(expected, 2)
        assert cost == 0.96

    def test_cost_with_regenerations(self):
        """AC7: 12 beats + 2 regenerations."""
        cost = compute_generation_cost(12, regeneration_count=2)
        base = 12 * 0.08
        regen = 2 * 0.08
        assert cost == round(base + regen, 2)
        assert cost == 1.12

    def test_update_cost_on_state(self):
        state = _make_state(beat_count=12)
        state["total_regenerations"] = 2
        cost = update_cost(state)
        assert cost == 1.12
        assert state["total_generation_cost_usd"] == 1.12

    def test_cost_constants(self):
        assert COST_T2I_PER_KEYFRAME == 0.02
        assert COST_I2V_PER_CLIP == 0.06


# ---------------------------------------------------------------------------
# TestCheckpointSystem — TD3
# ---------------------------------------------------------------------------


class TestCheckpointSystem:
    """TD3: Checkpoint + resume on every state transition."""

    def test_serialize_and_load(self):
        state = _make_state(beat_count=4)
        transition_state(state, "GENERATING_T2I")
        with tempfile.TemporaryDirectory() as tmpdir:
            path = serialize_checkpoint(state, tmpdir)
            assert os.path.exists(path)
            loaded = load_checkpoint(path)
            assert loaded is not None
            assert loaded["current_state"] == "GENERATING_T2I"
            assert loaded["pipeline_id"] == state["pipeline_id"]

    def test_load_nonexistent(self):
        assert load_checkpoint("/nonexistent/path.json") is None

    def test_find_checkpoint(self):
        """AC3: Detect existing checkpoint for a beat_cluster_id."""
        state = _make_state(beat_count=4)
        with tempfile.TemporaryDirectory() as tmpdir:
            serialize_checkpoint(state, tmpdir)
            found = find_checkpoint("BC-TEST-001", tmpdir)
            assert found is not None

    def test_find_checkpoint_not_found(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            found = find_checkpoint("BC-NONEXISTENT", tmpdir)
            assert found is None

    def test_checkpoint_preserves_state_history(self):
        state = _make_state(beat_count=4)
        transition_state(state, "GENERATING_T2I")
        transition_state(state, "QUALITY_GATE")
        with tempfile.TemporaryDirectory() as tmpdir:
            path = serialize_checkpoint(state, tmpdir)
            loaded = load_checkpoint(path)
            assert len(loaded["state_history"]) == 3

    def test_ac3_resume_skips_completed(self):
        """AC3: After checkpoint at I2V, resume should see T2I/audio as complete."""
        state = _make_state(beat_count=4)
        for s in ["GENERATING_T2I", "QUALITY_GATE", "GENERATING_I2V"]:
            transition_state(state, s)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = serialize_checkpoint(state, tmpdir)
            loaded = load_checkpoint(path)
            assert loaded["current_state"] == "GENERATING_I2V"
            # Verify history includes prior states
            history_states = [h["state"] for h in loaded["state_history"]]
            assert "GENERATING_T2I" in history_states
            assert "QUALITY_GATE" in history_states


# ---------------------------------------------------------------------------
# TestBatchQueue — §4 Stage 3
# ---------------------------------------------------------------------------


class TestBatchQueue:
    """Batch processing queue with priority and concurrent limits."""

    def test_create_queue(self):
        q = create_job_queue(concurrent_limit=3)
        assert q["concurrent_limit"] == 3
        assert q["jobs"] == []

    def test_enqueue_job(self):
        q = create_job_queue()
        job = enqueue_job(q, "PIPE-001", "BC-001", "proj-01")
        assert job["status"] == "QUEUED"
        assert len(q["jobs"]) == 1
        assert q["stats"]["total_queued"] == 1

    def test_dequeue_fifo(self):
        q = create_job_queue(concurrent_limit=3)
        enqueue_job(q, "PIPE-001", "BC-001")
        enqueue_job(q, "PIPE-002", "BC-002")
        job = dequeue_next(q)
        assert job["pipeline_id"] == "PIPE-001"
        assert job["status"] == "PROCESSING"

    def test_dequeue_priority(self):
        q = create_job_queue(concurrent_limit=3)
        enqueue_job(q, "PIPE-001", "BC-001", priority=50)
        enqueue_job(q, "PIPE-002", "BC-002", priority=100)
        job = dequeue_next(q)
        assert job["pipeline_id"] == "PIPE-002"  # Higher priority first

    def test_ac6_concurrent_limit(self):
        """AC6: Exactly 3 processing, 2 queued when limit=3 and 5 submitted."""
        q = create_job_queue(concurrent_limit=3)
        for i in range(5):
            enqueue_job(q, f"PIPE-{i}", f"BC-{i}")

        # Dequeue 3
        for _ in range(3):
            job = dequeue_next(q)
            assert job is not None

        # 4th should return None (at limit)
        assert dequeue_next(q) is None

        processing = sum(1 for j in q["jobs"] if j["status"] == "PROCESSING")
        queued = sum(1 for j in q["jobs"] if j["status"] == "QUEUED")
        assert processing == 3
        assert queued == 2

    def test_ac6_next_starts_after_completion(self):
        """AC6: As one completes, the next queued video starts."""
        q = create_job_queue(concurrent_limit=2)
        for i in range(4):
            enqueue_job(q, f"PIPE-{i}", f"BC-{i}")

        dequeue_next(q)  # PIPE-0 processing
        dequeue_next(q)  # PIPE-1 processing
        assert dequeue_next(q) is None  # At limit

        complete_job(q, "PIPE-0")  # Free a slot
        job = dequeue_next(q)  # PIPE-2 should start
        assert job is not None
        assert job["pipeline_id"] == "PIPE-2"

    def test_complete_job_success(self):
        q = create_job_queue()
        enqueue_job(q, "PIPE-001", "BC-001")
        dequeue_next(q)
        job = complete_job(q, "PIPE-001", success=True)
        assert job["status"] == "COMPLETED"
        assert q["stats"]["total_completed"] == 1

    def test_complete_job_failure(self):
        q = create_job_queue()
        enqueue_job(q, "PIPE-001", "BC-001")
        dequeue_next(q)
        job = complete_job(q, "PIPE-001", success=False)
        assert job["status"] == "FAILED"
        assert q["stats"]["total_failed"] == 1

    def test_queue_status(self):
        q = create_job_queue(concurrent_limit=3)
        for i in range(5):
            enqueue_job(q, f"PIPE-{i}", f"BC-{i}")
        dequeue_next(q)
        status = get_queue_status(q)
        assert status["concurrent_limit"] == 3
        assert status["total_jobs"] == 5
        assert status["total_processing"] == 1
        assert status["total_queued"] == 4


# ---------------------------------------------------------------------------
# TestReviewUIState
# ---------------------------------------------------------------------------


class TestReviewUIState:
    """Review UI state builder (DEP-VID-027)."""

    def test_build_in_review(self):
        state = _make_state(beat_count=4)
        review = build_review_state(state)
        assert review["review_status"] == "IN_REVIEW"
        assert review["render_final_enabled"] is False
        assert len(review["beats"]) == 4

    def test_build_all_approved(self):
        state = _make_state(beat_count=4)
        approve_all_beats(state)
        review = build_review_state(state)
        assert review["review_status"] == "ALL_APPROVED"
        assert review["render_final_enabled"] is True

    def test_auto_approve_eligible(self):
        state = _make_state(beat_count=4)
        set_quality_scores(state, {0: 0.9, 1: 0.85, 2: 0.88, 3: 0.92})
        review = build_review_state(state)
        assert review["auto_approve_eligible"] is True

    def test_auto_approve_not_eligible(self):
        state = _make_state(beat_count=4)
        set_quality_scores(state, {0: 0.9, 1: 0.5, 2: 0.88, 3: 0.92})
        review = build_review_state(state)
        assert review["auto_approve_eligible"] is False


# ---------------------------------------------------------------------------
# TestReceiptWriting
# ---------------------------------------------------------------------------


class TestReceiptWriting:
    """PIPELINE_INIT and BATCH_QUEUE_MANAGE receipts."""

    def test_pipeline_init_receipt(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out = run_pipeline_init("BC-001", "proj-01", 12, output_dir=tmpdir)
            assert out["receipt"]["stage_name"] == "PIPELINE_INIT"
            assert out["receipt"]["agent_name"] == "pipeline_commander"
            assert out["state"]["current_state"] == "PENDING"
            assert len(out["state"]["beat_approvals"]) == 12

    def test_batch_queue_manage_receipt(self):
        q = create_job_queue()
        with tempfile.TemporaryDirectory() as tmpdir:
            out = run_batch_queue_manage(
                q, "enqueue", output_dir=tmpdir,
                pipeline_id="PIPE-001", beat_cluster_id="BC-001",
            )
            assert out["receipt"]["stage_name"] == "BATCH_QUEUE_MANAGE"
            assert out["result"]["status"] == "QUEUED"

    def test_batch_queue_status_receipt(self):
        q = create_job_queue()
        with tempfile.TemporaryDirectory() as tmpdir:
            out = run_batch_queue_manage(q, "status", output_dir=tmpdir)
            assert out["result"]["total_jobs"] == 0
