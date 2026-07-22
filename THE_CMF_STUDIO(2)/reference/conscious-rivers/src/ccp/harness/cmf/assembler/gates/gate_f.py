"""
Gate F — Pre-I2V Constraint Network (Motion Quality Assurance)

FR-VID-03 §6 Skill Definition

Five validation questions that MUST all pass before submitting any I2V
generation batch to RunningHub. GPU time on I2V is 4-8× more expensive
than T2I. If ANY answer is NO, the agent must resolve the issue first.

Each function returns: (passed: bool, diagnostic: str)

Build Prompt Rule 7: These are executable validation functions, NOT
documentation-only comments.
"""

from math import ceil


# ---------------------------------------------------------------------------
# Q1: Keyframe Quality Approved
# FR-VID-03 §6 Gate F Q1
# ---------------------------------------------------------------------------


def check_keyframe_quality_approved(
    quality_verdicts: list[dict],
    threshold: float = 0.6,
) -> tuple[bool, str]:
    """
    Gate F Q1: Has every keyframe in this batch passed the FR-VID-04
    quality gate with a score ≥ threshold?

    Submitting a low-quality keyframe to I2V wastes expensive 48GB GPU
    time and produces an unusable clip — always regenerate T2I first.
    """
    failing_beats = []
    for verdict in quality_verdicts:
        beat_idx = verdict.get("beat_index", "?")
        v = verdict.get("verdict", "")
        if v != "APPROVED":
            failing_beats.append(f"beat {beat_idx} (verdict: {v})")

    if failing_beats:
        return (
            False,
            f"{len(failing_beats)} keyframe(s) not approved by quality gate: "
            f"{', '.join(failing_beats[:5])}. "
            f"Regenerate T2I before submitting to I2V.",
        )

    return (True, "All keyframes passed quality gate with APPROVED verdict.")


# ---------------------------------------------------------------------------
# Q2: Motion-Arc Coherence
# FR-VID-03 §6 Gate F Q2
# ---------------------------------------------------------------------------

# Incompatible arc_stage ↔ camera_motion combinations
ARC_MOTION_VIOLATIONS = {
    "climax": frozenset(["gentle_drift", "static", "subtle_breathe"]),
    "hook": frozenset(["static", "subtle_breathe"]),
    "resolution": frozenset(["dynamic_push_forward", "quick_zoom_out"]),
    "establishing": frozenset(["dynamic_push_forward", "quick_zoom_out"]),
}


def check_motion_arc_coherence(
    job_configs: list[dict],
) -> tuple[bool, str]:
    """
    Gate F Q2: Does every beat's assigned camera_motion match the emotional
    trajectory of its arc_stage?

    A climax beat with gentle_drift undermines dramatic tension.
    A hook beat with static motion fails to capture attention.
    """
    violations = []
    for jc in job_configs:
        if jc.get("status") != "CONFIGURED":
            continue
        arc_stage = jc.get("arc_stage", "")
        motion_params = jc.get("motion_parameters", {})
        camera_motion = motion_params.get("camera_motion", "")
        beat_idx = jc.get("beat_index", "?")

        invalid_motions = ARC_MOTION_VIOLATIONS.get(arc_stage, frozenset())
        if camera_motion in invalid_motions:
            violations.append(
                f"beat {beat_idx}: arc_stage='{arc_stage}' with "
                f"camera_motion='{camera_motion}' undermines emotional intent"
            )

    if violations:
        return (
            False,
            f"Motion-arc coherence violations: {'; '.join(violations[:3])}. "
            f"The motion IS the emotion — fix motion presets.",
        )

    return (True, "All motion assignments are coherent with arc stages.")


# ---------------------------------------------------------------------------
# Q3: Duration-Frame Feasibility
# FR-VID-03 §6 Gate F Q3
# ---------------------------------------------------------------------------


def check_duration_frame_feasibility(
    job_configs: list[dict],
    model_max_frames: int = 96,
) -> tuple[bool, str]:
    """
    Gate F Q3: Is every beat's duration_frames within the I2V model's
    supported range? For beats exceeding maximum: has segment-and-crossfade
    been configured?

    Requesting 200 frames from an SVD model that maxes at 96 produces
    a crash, not a compromise.
    """
    violations = []
    for jc in job_configs:
        if jc.get("status") != "CONFIGURED":
            continue
        beat_idx = jc.get("beat_index", "?")
        motion_params = jc.get("motion_parameters", {})
        duration_frames = motion_params.get("duration_frames", 0)
        segment_count = jc.get("segment_count", 1)

        if duration_frames > model_max_frames and segment_count <= 1:
            violations.append(
                f"beat {beat_idx}: {duration_frames} frames exceeds model max "
                f"{model_max_frames} but no segment-and-crossfade configured"
            )

    if violations:
        return (
            False,
            f"Frame feasibility violations: {'; '.join(violations[:3])}. "
            f"Configure segment-and-crossfade for long beats.",
        )

    return (True, "All beats have feasible frame counts or proper segmentation.")


# ---------------------------------------------------------------------------
# Q4: Input Resolution Match
# FR-VID-03 §6 Gate F Q4
# ---------------------------------------------------------------------------


def check_input_resolution_match(
    keyframe_resolutions: list[dict],
    expected_width: int = 1080,
    expected_height: int = 1920,
) -> tuple[bool, str]:
    """
    Gate F Q4: Does the keyframe's resolution match the I2V workflow's
    expected input dimensions?

    A 512×512 keyframe fed to a 1080p I2V workflow produces upscale
    artifacts. A 4K keyframe wastes detail.
    """
    violations = []
    for kf in keyframe_resolutions:
        beat_idx = kf.get("beat_index", "?")
        width = kf.get("width", 0)
        height = kf.get("height", 0)

        if width != expected_width or height != expected_height:
            violations.append(
                f"beat {beat_idx}: {width}×{height} != expected {expected_width}×{expected_height}"
            )

    if violations:
        return (
            False,
            f"Resolution mismatches: {'; '.join(violations[:3])}. "
            f"Keyframe resolution must match I2V workflow input dimensions.",
        )

    return (True, f"All keyframes match expected resolution {expected_width}×{expected_height}.")


# ---------------------------------------------------------------------------
# Q5: Budget Checkpoint
# FR-VID-03 §6 Gate F Q5
# ---------------------------------------------------------------------------


def check_budget_checkpoint(
    batch_size: int,
    cost_per_clip: float = 0.08,
    per_video_ceiling: float = 0.96,
) -> tuple[bool, str]:
    """
    Gate F Q5: Is the current batch's estimated GPU cost within the
    per-video budget ceiling?

    At $0.04-0.08 per I2V clip and 12 clips per video, costs spiral
    if regeneration loops are uncapped.
    """
    estimated_cost = batch_size * cost_per_clip

    if estimated_cost > per_video_ceiling:
        return (
            False,
            f"Estimated batch cost ${estimated_cost:.2f} exceeds per-video ceiling "
            f"${per_video_ceiling:.2f} ({batch_size} clips × ${cost_per_clip:.2f}). "
            f"Reduce batch size or get operator approval for budget override.",
        )

    return (
        True,
        f"Estimated batch cost ${estimated_cost:.2f} is within budget ceiling "
        f"${per_video_ceiling:.2f}.",
    )


# ---------------------------------------------------------------------------
# Gate F Runner — executes all 5 questions
# ---------------------------------------------------------------------------


def run_gate_f(
    quality_verdicts: list[dict],
    job_configs: list[dict],
    keyframe_resolutions: list[dict],
    batch_size: int,
    model_max_frames: int = 96,
    quality_threshold: float = 0.6,
    expected_width: int = 1080,
    expected_height: int = 1920,
    cost_per_clip: float = 0.08,
    per_video_ceiling: float = 0.96,
) -> tuple[bool, list[dict]]:
    """
    Run all 5 Gate F questions. Returns (all_passed, results_list).

    If ANY question returns False, the agent must resolve the issue
    before submitting the I2V batch — GPU time on I2V is 4-8× more
    expensive than T2I.
    """
    results = []

    q1_pass, q1_diag = check_keyframe_quality_approved(quality_verdicts, quality_threshold)
    results.append(
        {
            "question": 1,
            "name": "Keyframe Quality Approved",
            "passed": q1_pass,
            "diagnostic": q1_diag,
        }
    )

    q2_pass, q2_diag = check_motion_arc_coherence(job_configs)
    results.append(
        {
            "question": 2,
            "name": "Motion-Arc Coherence",
            "passed": q2_pass,
            "diagnostic": q2_diag,
        }
    )

    q3_pass, q3_diag = check_duration_frame_feasibility(job_configs, model_max_frames)
    results.append(
        {
            "question": 3,
            "name": "Duration-Frame Feasibility",
            "passed": q3_pass,
            "diagnostic": q3_diag,
        }
    )

    q4_pass, q4_diag = check_input_resolution_match(
        keyframe_resolutions, expected_width, expected_height
    )
    results.append(
        {
            "question": 4,
            "name": "Input Resolution Match",
            "passed": q4_pass,
            "diagnostic": q4_diag,
        }
    )

    q5_pass, q5_diag = check_budget_checkpoint(
        batch_size, cost_per_clip, per_video_ceiling
    )
    results.append(
        {
            "question": 5,
            "name": "Budget Checkpoint",
            "passed": q5_pass,
            "diagnostic": q5_diag,
        }
    )

    all_passed = all(r["passed"] for r in results)
    return (all_passed, results)
