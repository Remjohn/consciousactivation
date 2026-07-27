"""
Gate F Violation Tests — FR-VID-03 Constraint Network

Build Prompt Stage 5 Completion Gate 5: "For each gate question, name the
validation function and show a test case that demonstrates it catches a violation."

Tests all 5 Gate F validation functions. Each test demonstrates the gate
correctly catches a specific violation, returning False with a diagnostic.
"""

from gates.gate_f import (
    check_keyframe_quality_approved,
    check_motion_arc_coherence,
    check_duration_frame_feasibility,
    check_input_resolution_match,
    check_budget_checkpoint,
    run_gate_f,
)


# ---- Q1 Violation: Unapproved keyframes submitted to I2V ----


def test_gate_f_q1_violation_regenerate_verdict():
    """Q1: Keyframe with REGENERATE verdict → returns False."""
    verdicts = [
        {"beat_index": 0, "verdict": "APPROVED"},
        {"beat_index": 1, "verdict": "REGENERATE"},
    ]
    passed, diagnostic = check_keyframe_quality_approved(verdicts)
    assert not passed, "Q1 should FAIL: beat 1 is REGENERATE, not APPROVED"
    assert "not approved" in diagnostic.lower()


def test_gate_f_q1_violation_manual_review():
    """Q1: Keyframe with MANUAL_REVIEW → returns False."""
    verdicts = [{"beat_index": 3, "verdict": "MANUAL_REVIEW"}]
    passed, diagnostic = check_keyframe_quality_approved(verdicts)
    assert not passed, "Q1 should FAIL: MANUAL_REVIEW beats must not go to I2V"
    assert "regenerate" in diagnostic.lower()


def test_gate_f_q1_passes_all_approved():
    """Q1: All APPROVED → returns True."""
    verdicts = [
        {"beat_index": 0, "verdict": "APPROVED"},
        {"beat_index": 1, "verdict": "APPROVED"},
        {"beat_index": 2, "verdict": "APPROVED"},
    ]
    passed, _ = check_keyframe_quality_approved(verdicts)
    assert passed, "Q1 should PASS: all keyframes approved"


# ---- Q2 Violation: Motion contradicts arc emotional trajectory ----


def test_gate_f_q2_violation_climax_gentle():
    """Q2: Climax beat with gentle_drift → returns False."""
    configs = [
        {
            "beat_index": 5,
            "status": "CONFIGURED",
            "arc_stage": "climax",
            "motion_parameters": {"camera_motion": "gentle_drift"},
        }
    ]
    passed, diagnostic = check_motion_arc_coherence(configs)
    assert not passed, "Q2 should FAIL: climax + gentle_drift undermines tension"
    assert "climax" in diagnostic.lower()


def test_gate_f_q2_violation_hook_static():
    """Q2: Hook beat with static motion → returns False."""
    configs = [
        {
            "beat_index": 0,
            "status": "CONFIGURED",
            "arc_stage": "hook",
            "motion_parameters": {"camera_motion": "static"},
        }
    ]
    passed, diagnostic = check_motion_arc_coherence(configs)
    assert not passed, "Q2 should FAIL: hook + static fails attention capture"


def test_gate_f_q2_passes_climax_dynamic():
    """Q2: Climax beat with dynamic_push_forward → returns True."""
    configs = [
        {
            "beat_index": 5,
            "status": "CONFIGURED",
            "arc_stage": "climax",
            "motion_parameters": {"camera_motion": "dynamic_push_forward"},
        }
    ]
    passed, _ = check_motion_arc_coherence(configs)
    assert passed, "Q2 should PASS: climax + dynamic_push_forward is coherent"


def test_gate_f_q2_passes_resolution_gentle():
    """Q2: Resolution beat with gentle_drift → returns True."""
    configs = [
        {
            "beat_index": 10,
            "status": "CONFIGURED",
            "arc_stage": "resolution",
            "motion_parameters": {"camera_motion": "gentle_drift"},
        }
    ]
    passed, _ = check_motion_arc_coherence(configs)
    assert passed, "Q2 should PASS: resolution + gentle_drift is appropriate"


# ---- Q3 Violation: Frames exceed model max without segmentation ----


def test_gate_f_q3_violation_no_segmentation():
    """Q3: 144 frames (no segments) on 96-frame max model → returns False."""
    configs = [
        {
            "beat_index": 2,
            "status": "CONFIGURED",
            "motion_parameters": {"duration_frames": 144},
            "segment_count": 1,
        }
    ]
    passed, diagnostic = check_duration_frame_feasibility(configs, model_max_frames=96)
    assert not passed, "Q3 should FAIL: 144 frames > 96 max, no segmentation"
    assert "segment" in diagnostic.lower()


def test_gate_f_q3_passes_within_limit():
    """Q3: 72 frames within 96 max → returns True."""
    configs = [
        {
            "beat_index": 0,
            "status": "CONFIGURED",
            "motion_parameters": {"duration_frames": 72},
            "segment_count": 1,
        }
    ]
    passed, _ = check_duration_frame_feasibility(configs, model_max_frames=96)
    assert passed, "Q3 should PASS: 72 frames within 96 max"


def test_gate_f_q3_passes_segmented():
    """Q3: 144 frames with 2 segments → returns True."""
    configs = [
        {
            "beat_index": 2,
            "status": "CONFIGURED",
            "motion_parameters": {"duration_frames": 144},
            "segment_count": 2,
        }
    ]
    passed, _ = check_duration_frame_feasibility(configs, model_max_frames=96)
    assert passed, "Q3 should PASS: segmentation configured for long beat"


# ---- Q4 Violation: Resolution mismatch ----


def test_gate_f_q4_violation_wrong_resolution():
    """Q4: 512×512 keyframe for 1080×1920 I2V → returns False."""
    resolutions = [{"beat_index": 0, "width": 512, "height": 512}]
    passed, diagnostic = check_input_resolution_match(resolutions, 1080, 1920)
    assert not passed, "Q4 should FAIL: 512×512 doesn't match 1080×1920"
    assert "mismatch" in diagnostic.lower()


def test_gate_f_q4_violation_landscape():
    """Q4: 1920×1080 landscape keyframe → returns False."""
    resolutions = [{"beat_index": 1, "width": 1920, "height": 1080}]
    passed, diagnostic = check_input_resolution_match(resolutions, 1080, 1920)
    assert not passed, "Q4 should FAIL: landscape orientation"


def test_gate_f_q4_passes_correct_resolution():
    """Q4: 1080×1920 keyframe → returns True."""
    resolutions = [
        {"beat_index": 0, "width": 1080, "height": 1920},
        {"beat_index": 1, "width": 1080, "height": 1920},
    ]
    passed, _ = check_input_resolution_match(resolutions, 1080, 1920)
    assert passed, "Q4 should PASS: all resolutions match"


# ---- Q5 Violation: Budget exceeded ----


def test_gate_f_q5_violation_over_budget():
    """Q5: 20 clips × $0.08 = $1.60 > $0.96 ceiling → returns False."""
    passed, diagnostic = check_budget_checkpoint(20, 0.08, 0.96)
    assert not passed, "Q5 should FAIL: $1.60 > $0.96 ceiling"
    assert "exceeds" in diagnostic.lower()


def test_gate_f_q5_passes_within_budget():
    """Q5: 12 clips × $0.08 = $0.96 ≤ $0.96 ceiling → returns True."""
    passed, _ = check_budget_checkpoint(12, 0.08, 0.96)
    assert passed, "Q5 should PASS: $0.96 = ceiling"


def test_gate_f_q5_passes_low_cost():
    """Q5: 6 clips × $0.04 = $0.24 → returns True."""
    passed, _ = check_budget_checkpoint(6, 0.04, 0.96)
    assert passed, "Q5 should PASS: well within budget"


# ---- Full Gate F Runner ----


def test_gate_f_full_run_all_pass():
    """Full Gate F returns True when all 5 questions pass."""
    verdicts = [{"beat_index": i, "verdict": "APPROVED"} for i in range(12)]
    configs = [
        {
            "beat_index": i,
            "status": "CONFIGURED",
            "arc_stage": "hook" if i == 0 else "rising_action",
            "motion_parameters": {
                "camera_motion": "slow_zoom_in" if i == 0 else "steady_push_forward",
                "duration_frames": 72,
            },
            "segment_count": 1,
        }
        for i in range(12)
    ]
    resolutions = [{"beat_index": i, "width": 1080, "height": 1920} for i in range(12)]

    all_passed, results = run_gate_f(
        quality_verdicts=verdicts,
        job_configs=configs,
        keyframe_resolutions=resolutions,
        batch_size=12,
    )
    assert all_passed, f"Gate F should PASS: {[r for r in results if not r['passed']]}"
    assert len(results) == 5
    assert all(r["passed"] for r in results)


def test_gate_f_full_run_with_violation():
    """Full Gate F returns False when Q1 fails (unapproved keyframe)."""
    verdicts = [
        {"beat_index": 0, "verdict": "APPROVED"},
        {"beat_index": 1, "verdict": "REGENERATE"},
    ]
    configs = [
        {
            "beat_index": 0,
            "status": "CONFIGURED",
            "arc_stage": "hook",
            "motion_parameters": {"camera_motion": "slow_zoom_in", "duration_frames": 72},
            "segment_count": 1,
        }
    ]
    resolutions = [{"beat_index": 0, "width": 1080, "height": 1920}]

    all_passed, results = run_gate_f(
        quality_verdicts=verdicts,
        job_configs=configs,
        keyframe_resolutions=resolutions,
        batch_size=1,
    )
    assert not all_passed, "Gate F should FAIL: Q1 unapproved keyframe"
    q1 = next(r for r in results if r["question"] == 1)
    assert not q1["passed"]


def test_gate_f_full_run_multiple_failures():
    """Full Gate F reports all failures when multiple questions fail."""
    verdicts = [{"beat_index": 0, "verdict": "REGENERATE"}]
    configs = [
        {
            "beat_index": 0,
            "status": "CONFIGURED",
            "arc_stage": "climax",
            "motion_parameters": {"camera_motion": "gentle_drift", "duration_frames": 200},
            "segment_count": 1,
        }
    ]
    resolutions = [{"beat_index": 0, "width": 512, "height": 512}]

    all_passed, results = run_gate_f(
        quality_verdicts=verdicts,
        job_configs=configs,
        keyframe_resolutions=resolutions,
        batch_size=20,
    )
    assert not all_passed, "Gate F should FAIL: multiple violations"
    failed = [r for r in results if not r["passed"]]
    assert len(failed) >= 4  # Q1, Q2, Q3, Q4 all fail
