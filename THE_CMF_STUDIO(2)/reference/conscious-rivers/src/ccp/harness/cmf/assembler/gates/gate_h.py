"""
Gate H — Pre-Regeneration Constraint Network (Surgical Regeneration Assurance)

FR-VID-05 §6 Skill Definition

Five validation questions that MUST all pass before executing any
regeneration request. If ANY answer is NO, the agent must resolve
the issue before regenerating.

Each function returns: (passed: bool, diagnostic: str)

Build Prompt Rule 7: These are executable validation functions, NOT
documentation-only comments.
"""

try:
    from .regeneration_handler import (
        map_revision_to_blocks,
        MAX_REGENERATION_PER_BEAT,
    )
except ImportError:
    from regeneration_handler import (
        map_revision_to_blocks,
        MAX_REGENERATION_PER_BEAT,
    )


# ---------------------------------------------------------------------------
# Q1: Cascade Completeness
# FR-VID-05 §6 Gate H Q1
# ---------------------------------------------------------------------------


def check_cascade_completeness(
    mode: str,
    plan: dict,
) -> tuple[bool, str]:
    """
    Gate H Q1: If mode is T2I_ONLY, is the subsequent I2V regeneration
    step scheduled?

    Regenerating T2I without scheduling I2V leaves a stale video clip
    in the manifest — the operator sees the old motion on the new keyframe.
    """
    if mode == "T2I_ONLY":
        if not plan.get("cascade_i2v", False):
            return False, (
                "I2V_CASCADE_MISSING: T2I_ONLY regeneration must schedule "
                "I2V regeneration. Set cascade_i2v: true."
            )
        if "FR-VID-03" not in plan.get("pipeline_calls", []):
            return False, (
                "I2V_CASCADE_MISSING: T2I_ONLY regeneration plan does not "
                "include FR-VID-03 in pipeline_calls."
            )
    return True, "Cascade completeness verified."


# ---------------------------------------------------------------------------
# Q2: Neighbor Seed Preservation
# FR-VID-05 §6 Gate H Q2
# ---------------------------------------------------------------------------


def check_seed_preservation(
    target_beat_indices: set[int],
    seed_locks: dict[int, dict],
    total_beats: int,
) -> tuple[bool, str]:
    """
    Gate H Q2: Are all non-target beats locked to their current seeds?

    If seed preservation fails, approved beats change unpredictably.
    """
    expected_locked = total_beats - len(target_beat_indices)
    actual_locked = len(seed_locks)

    if actual_locked < expected_locked:
        missing = expected_locked - actual_locked
        return False, (
            f"SEED_PRESERVATION_FAILED: {missing} non-target beat(s) missing "
            f"seed locks. Expected {expected_locked} locked, found {actual_locked}."
        )

    # Verify no target beats are in the lock set
    for beat_idx in target_beat_indices:
        if beat_idx in seed_locks:
            return False, (
                f"SEED_LOCK_CONFLICT: target beat {beat_idx} should NOT be "
                f"seed-locked. Remove it from seed_locks."
            )

    return True, "Seed preservation verified."


# ---------------------------------------------------------------------------
# Q3: Revision Note Specificity
# FR-VID-05 §6 Gate H Q3
# ---------------------------------------------------------------------------


def check_revision_note_specificity(
    revision_note: str,
) -> tuple[bool, str]:
    """
    Gate H Q3: Does the operator's revision note name a specific dimension
    to change?

    Vague notes produce prompt enhancements that change the wrong thing.
    Request clarification if the note lacks specificity.
    """
    if not revision_note or not revision_note.strip():
        return False, (
            "REVISION_NOTE_EMPTY: A revision note is required to guide "
            "prompt enhancement."
        )

    mapping = map_revision_to_blocks(revision_note)
    if mapping["unmappable"]:
        return False, (
            f"REVISION_NOTE_VAGUE: '{revision_note}' does not map to any "
            f"known prompt block or I2V parameter. Request clarification: "
            f"which dimension should change (lighting, character, environment, "
            f"cinematography, motion)?"
        )

    return True, "Revision note specificity verified."


# ---------------------------------------------------------------------------
# Q4: Budget Impact
# FR-VID-05 §6 Gate H Q4
# ---------------------------------------------------------------------------


def check_budget_impact(
    fingerprint_entry: dict,
    regen_cost_estimate: float = 0.09,
    per_video_budget: float = 5.0,
    total_spent: float = 0.0,
    regen_warn_threshold: int = 3,
) -> tuple[bool, str]:
    """
    Gate H Q4: Will this regeneration stay within budget?

    Each T2I+I2V regeneration costs ~$0.06-0.12. If a beat has already
    been regenerated 3+ times, the operator should review upstream.
    """
    history_count = len(fingerprint_entry.get("regeneration_history", []))
    projected = total_spent + regen_cost_estimate

    if projected > per_video_budget:
        return False, (
            f"BUDGET_EXCEEDED: Projected spend ${projected:.2f} exceeds "
            f"per-video budget ${per_video_budget:.2f}."
        )

    if history_count >= regen_warn_threshold:
        return False, (
            f"REGENERATION_EXCESSIVE: beat {fingerprint_entry['beat_index']} "
            f"has been regenerated {history_count} times. Review visual prompts "
            f"upstream before brute-forcing generation."
        )

    return True, "Budget impact within acceptable range."


# ---------------------------------------------------------------------------
# Q5: History Integrity
# FR-VID-05 §6 Gate H Q5
# ---------------------------------------------------------------------------


def check_history_integrity(
    fingerprint_entry: dict,
    plan_has_history_step: bool,
) -> tuple[bool, str]:
    """
    Gate H Q5: Is the superseded fingerprint correctly logged in
    regeneration_history before the new fingerprint is created?

    Skipping history logging destroys the audit trail.
    """
    if not plan_has_history_step:
        return False, (
            "HISTORY_LOGGING_MISSING: Regeneration plan does not include "
            "a history logging step. The superseded fingerprint must be "
            "logged before creating the new one."
        )

    return True, "History integrity verified."


# ---------------------------------------------------------------------------
# Gate H Runner
# ---------------------------------------------------------------------------


def run_gate_h(
    mode: str,
    plan: dict,
    target_beat_indices: set[int],
    seed_locks: dict[int, dict],
    total_beats: int,
    revision_note: str,
    fingerprint_entry: dict,
    plan_has_history_step: bool = True,
    regen_cost_estimate: float = 0.09,
    per_video_budget: float = 5.0,
    total_spent: float = 0.0,
) -> dict:
    """
    Run all 5 Gate H questions.

    Returns:
        {
            "gate": "H",
            "passed": bool,
            "results": [
                {"question": 1, "passed": bool, "diagnostic": str},
                ...
            ]
        }
    """
    checks = [
        (1, check_cascade_completeness(mode, plan)),
        (2, check_seed_preservation(target_beat_indices, seed_locks, total_beats)),
        (3, check_revision_note_specificity(revision_note)),
        (4, check_budget_impact(
            fingerprint_entry, regen_cost_estimate, per_video_budget, total_spent
        )),
        (5, check_history_integrity(fingerprint_entry, plan_has_history_step)),
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
        "gate": "H",
        "passed": all_passed,
        "results": results,
    }
