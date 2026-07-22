"""
Gate E — Pre-Assembly Constraint Network (Manifest Integrity Assurance)

FR-VID-01 §6 Skill Definition

Five validation questions that MUST all pass before emitting the final
Remotion manifest. Never emit an inconsistent manifest — black frames,
misaligned audio, or broken narrative grammar corrupt the operator's review.

Each function returns: (passed: bool, diagnostic: str)

Build Prompt Rule 7: These are executable validation functions, NOT
documentation-only comments.
"""

from typing import Optional


# ---------------------------------------------------------------------------
# Q1: Frame Count Continuity
# FR-VID-01 §6 Gate E Q1
# ---------------------------------------------------------------------------


def check_frame_count_continuity(
    beats: list[dict],
    declared_total_frames: int,
) -> tuple[bool, str]:
    """
    Gate E Q1: Does the sum of all beat duration_frames equal the
    manifest's declared total_frames?

    A mismatch creates black frames or overlapping sequences in Remotion.
    """
    computed = sum(b.get("duration_frames", 0) for b in beats)
    if computed != declared_total_frames:
        return False, (
            f"FRAME_COUNT_MISMATCH: sum of beat frames ({computed}) != "
            f"declared total_frames ({declared_total_frames})"
        )
    return True, "Frame count continuity verified."


# ---------------------------------------------------------------------------
# Q2: Asset Completeness
# FR-VID-01 §6 Gate E Q2
# ---------------------------------------------------------------------------


def check_asset_completeness(
    beats: list[dict],
    manifest_status: str,
) -> tuple[bool, str]:
    """
    Gate E Q2: Does every beat have at least one resolvable asset URL?
    If any beat has ASSET_MISSING, is the manifest status correctly set
    to ASSEMBLED_WITH_GAPS?
    """
    missing_beats = [
        b["beat_index"] for b in beats
        if b.get("asset_status") == "ASSET_MISSING"
    ]

    if missing_beats and manifest_status != "ASSEMBLED_WITH_GAPS":
        return False, (
            f"ASSET_STATUS_INCONSISTENCY: beats {missing_beats} have "
            f"ASSET_MISSING but manifest status is '{manifest_status}' "
            f"instead of 'ASSEMBLED_WITH_GAPS'"
        )

    if not missing_beats and manifest_status == "ASSEMBLED_WITH_GAPS":
        return False, (
            "ASSET_STATUS_INCONSISTENCY: no beats have ASSET_MISSING but "
            "manifest status is 'ASSEMBLED_WITH_GAPS'"
        )

    return True, "Asset completeness verified."


# ---------------------------------------------------------------------------
# Q3: Audio-Beat Alignment
# FR-VID-01 §6 Gate E Q3
# ---------------------------------------------------------------------------


def check_audio_beat_alignment(
    ducking_curve_length: int,
    declared_total_frames: int,
) -> tuple[bool, str]:
    """
    Gate E Q3: Does the ducking curve length match the manifest's
    declared total_frames?

    A mismatched ducking curve produces incorrect music volume levels
    during beat transitions or silence at the end of the video.
    """
    if ducking_curve_length != declared_total_frames:
        return False, (
            f"DUCKING_CURVE_MISMATCH: curve length ({ducking_curve_length}) != "
            f"total_frames ({declared_total_frames})"
        )
    return True, "Audio-beat alignment verified."


# ---------------------------------------------------------------------------
# Q4: Transition Budget
# FR-VID-01 §6 Gate E Q4
# ---------------------------------------------------------------------------


def check_transition_budget(
    beats: list[dict],
) -> tuple[bool, str]:
    """
    Gate E Q4: Do transition duration_frames leave at least 50% of each
    beat's duration as non-transition content?

    A 3-second beat with a 2-second crossfade leaves only 1 second of
    visible content — insufficient for visual comprehension.
    """
    violations = []
    for beat in beats:
        transition = beat.get("transition")
        if transition is None:
            continue
        trans_frames = transition.get("duration_frames", 0)
        beat_frames = beat.get("duration_frames", 0)
        if beat_frames <= 0:
            continue
        if trans_frames > beat_frames * 0.5:
            violations.append(
                f"beat[{beat['beat_index']}]: transition {trans_frames}f > "
                f"50% of beat {beat_frames}f"
            )

    if violations:
        return False, (
            f"TRANSITION_BUDGET_EXCEEDED: {'; '.join(violations)}"
        )
    return True, "Transition budget verified."


# ---------------------------------------------------------------------------
# Q5: Arc Stage Sequence
# FR-VID-01 §6 Gate E Q5
# ---------------------------------------------------------------------------


def check_arc_stage_sequence(
    beats: list[dict],
    arc_type: str,
    arc_sequences: Optional[dict] = None,
) -> tuple[bool, str]:
    """
    Gate E Q5: Do the beats' arc_stage values follow the arc type's
    required sequence?

    A Witness arc must not have a resolution before a climax —
    this breaks the narrative grammar.
    """
    if arc_sequences is None:
        return True, "No arc sequences loaded — skipping validation."

    valid_sequence = arc_sequences.get(arc_type)
    if valid_sequence is None:
        return True, f"No sequence defined for arc_type '{arc_type}' — skipping."

    # Build position map: arc_stage → expected position order
    position_map = {stage: idx for idx, stage in enumerate(valid_sequence)}

    last_position = -1
    for beat in beats:
        arc_stage = beat.get("arc_stage", "")
        if arc_stage not in position_map:
            continue  # Unknown stages are allowed (montage, transition, etc.)
        pos = position_map[arc_stage]
        if pos < last_position:
            return False, (
                f"ARC_SEQUENCE_VIOLATION: beat[{beat['beat_index']}] has "
                f"arc_stage '{arc_stage}' (position {pos}) after a stage "
                f"at position {last_position} — violates {arc_type} sequence"
            )
        last_position = pos

    return True, "Arc stage sequence verified."


# ---------------------------------------------------------------------------
# Gate E Runner
# ---------------------------------------------------------------------------


def run_gate_e(
    beats: list[dict],
    declared_total_frames: int,
    manifest_status: str,
    ducking_curve_length: int,
    arc_type: str = "",
    arc_sequences: Optional[dict] = None,
) -> dict:
    """
    Run all 5 Gate E questions.

    Returns:
        {
            "gate": "E",
            "passed": bool,
            "results": [
                {"question": 1, "passed": bool, "diagnostic": str},
                ...
            ]
        }
    """
    checks = [
        (1, check_frame_count_continuity(beats, declared_total_frames)),
        (2, check_asset_completeness(beats, manifest_status)),
        (3, check_audio_beat_alignment(ducking_curve_length, declared_total_frames)),
        (4, check_transition_budget(beats)),
        (5, check_arc_stage_sequence(beats, arc_type, arc_sequences)),
    ]

    results = []
    all_passed = True
    for q_num, (passed, diagnostic) in checks:
        results.append({
            "question": q_num,
            "passed": passed,
            "diagnostic": diagnostic,
        })
        if not passed:
            all_passed = False

    return {
        "gate": "E",
        "passed": all_passed,
        "results": results,
    }
