"""
Regeneration Handler — 3-Mode Surgical Regeneration System

FR-VID-05 §4 Stage 2: Regeneration Handling

Supports 3 regeneration modes:
  - T2I_ONLY: New keyframe → cascades to new I2V (mandatory).
  - I2V_ONLY: Same keyframe, different motion parameters.
  - BOTH: Full re-generation of T2I + I2V.

Produces a regeneration plan for the Commander (FR-VID-09) to execute.
Handles seed preservation, revision note → prompt enhancement, and
regeneration history maintenance.
"""

import re
from copy import deepcopy
from datetime import datetime, timezone
from typing import Optional

try:
    from .fingerprint_tracker import (
        generate_fingerprint_id,
        supersede_fingerprint,
        extract_seeds,
        MAX_REGENERATION_PER_BEAT,
    )
    from .receipt_chain import write_receipt
    from .legitimacy_runner import (
        build_regeneration_legitimacy_context,
        run_legitimacy_check,
    )
    from .scene_intelligence_loader import load_compiled_scene_intelligence_runtime_asset
    from .subsystem_loader import STAGE_SUBSYSTEM_ID_MAP, load_compiled_subsystem_runtime_asset
    from .subsystem_decisions import build_regeneration_patch_selection
    from .pipeline_commander import build_regeneration_dispatch
except ImportError:
    from fingerprint_tracker import (
        generate_fingerprint_id,
        supersede_fingerprint,
        extract_seeds,
        MAX_REGENERATION_PER_BEAT,
    )
    from receipt_chain import write_receipt
    from legitimacy_runner import (
        build_regeneration_legitimacy_context,
        run_legitimacy_check,
    )
    from scene_intelligence_loader import load_compiled_scene_intelligence_runtime_asset
    from subsystem_loader import STAGE_SUBSYSTEM_ID_MAP, load_compiled_subsystem_runtime_asset
    from subsystem_decisions import build_regeneration_patch_selection
    from pipeline_commander import build_regeneration_dispatch


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_MODES = {"T2I_ONLY", "I2V_ONLY", "BOTH"}

# FR-VID-05 §3 Technical Decision 6: Keyword-to-Block Mapping
KEYWORD_BLOCK_MAP = {
    "lighting": [4],
    "warmer": [4],
    "cooler": [4],
    "brighter": [4],
    "darker": [4],
    "shadow": [4],
    "color": [4, 6],
    "hue": [4, 6],
    "palette": [4, 6],
    "warm tones": [4, 6],
    "cool tones": [4, 6],
    "character": [1],
    "person": [1],
    "face": [1],
    "expression": [1],
    "clothing": [1],
    "environment": [2],
    "setting": [2],
    "location": [2],
    "background": [2],
    "angle": [3],
    "shot": [3],
    "zoom": [3],
    "pan": [3],
    "framing": [3],
    "composition": [3],
    "motion": ["I2V"],
    "speed": ["I2V"],
    "movement": ["I2V"],
    "camera": ["I2V"],
}

BLOCK_NAMES = {
    1: "Character",
    2: "Environment",
    3: "Cinematography",
    4: "Lighting",
    5: "Negative",
    6: "Technical",
}


# ---------------------------------------------------------------------------
# Revision Note → Prompt Enhancement
# ---------------------------------------------------------------------------


def map_revision_to_blocks(revision_note: str) -> dict:
    """
    Map an operator's revision note to specific prompt blocks.

    FR-VID-05 §3 Technical Decision 6: Keyword detection maps revision
    notes to blocks. Returns which blocks to target and whether I2V
    parameters should be modified.

    Returns:
        {
            "target_blocks": [int, ...],  # Block numbers to enhance
            "i2v_redirect": bool,          # True if motion keywords detected
            "unmappable": bool,            # True if no keywords match
        }
    """
    note_lower = revision_note.lower()
    target_blocks = set()
    i2v_redirect = False

    for keyword, blocks in KEYWORD_BLOCK_MAP.items():
        if keyword in note_lower:
            for block in blocks:
                if block == "I2V":
                    i2v_redirect = True
                else:
                    target_blocks.add(block)

    return {
        "target_blocks": sorted(target_blocks),
        "i2v_redirect": i2v_redirect,
        "unmappable": len(target_blocks) == 0 and not i2v_redirect,
    }


def enhance_prompt_with_revision(
    original_prompt: str,
    revision_note: str,
    target_blocks: list[int],
) -> str:
    """
    Enhance the visual prompt by appending the revision directive to
    targeted blocks.

    FR-VID-05 §3: Targeted block replacement. The targeted block is
    enhanced in-place: `[Original block content]. REVISION: [revision note].`
    Non-targeted blocks remain unchanged.

    If target_blocks is empty or the prompt doesn't have clear block
    structure, append the revision at the end.
    """
    if not target_blocks:
        return f"{original_prompt}. REVISION: {revision_note}."

    # The enhanced prompt includes the revision directive
    block_names = [BLOCK_NAMES.get(b, f"Block {b}") for b in target_blocks]
    block_list = ", ".join(block_names)
    return (
        f"{original_prompt}. "
        f"REVISION ({block_list}): {revision_note}."
    )


# ---------------------------------------------------------------------------
# Regeneration Request Validation
# ---------------------------------------------------------------------------


def validate_regeneration_request(
    request: dict,
    fingerprint_map: dict,
) -> tuple[bool, str]:
    """
    Validate a regeneration request before processing.

    Checks:
    - beat_index exists in fingerprint map
    - mode is valid (T2I_ONLY, I2V_ONLY, BOTH)
    - revision_note is present

    Returns:
        (valid, error_message)
    """
    beat_index = request.get("beat_index")
    mode = request.get("mode")
    revision_note = request.get("revision_note", "")

    if beat_index is None:
        return False, "REGENERATION_REQUEST_INVALID: missing beat_index"

    if mode not in VALID_MODES:
        return False, f"REGENERATION_REQUEST_INVALID: invalid mode '{mode}'"

    if not revision_note or not revision_note.strip():
        return False, "REGENERATION_REQUEST_INVALID: missing revision_note"

    # Check beat_index exists in fingerprint map
    beat_indices = {
        entry["beat_index"]
        for entry in fingerprint_map.get("fingerprints", [])
    }
    if beat_index not in beat_indices:
        return False, f"INVALID_BEAT_INDEX: beat {beat_index} not found in fingerprint map"

    return True, ""


# ---------------------------------------------------------------------------
# Per-Beat Regeneration Limit
# ---------------------------------------------------------------------------


def check_regeneration_limit(
    fingerprint_entry: dict,
    limit: int = MAX_REGENERATION_PER_BEAT,
) -> tuple[bool, str]:
    """
    Check if a beat has exceeded its regeneration limit.

    FR-VID-05 §10: Per-beat limit (default 10) requires operator override.
    """
    history_len = len(fingerprint_entry.get("regeneration_history", []))
    if history_len >= limit:
        return False, (
            f"REGENERATION_LIMIT_EXCEEDED: beat {fingerprint_entry['beat_index']} "
            f"has {history_len} regenerations (limit: {limit}). "
            f"Operator override required."
        )
    return True, ""


# ---------------------------------------------------------------------------
# Seed Preservation
# ---------------------------------------------------------------------------


def compute_seed_locks(
    fingerprint_map: dict,
    target_beat_indices: set[int],
) -> dict[int, dict]:
    """
    Lock seeds for all non-target beats.

    FR-VID-05 §3 Technical Decision 4: Non-target beats preserve seeds.
    FR-VID-05 §3 Technical Decision 5: Multi-beat targets are the UNION
    of all requested beat indices; both are targets, not seed-locked.

    Returns:
        dict mapping non-target beat_index → {"t2i_seed": ..., "i2v_seed": ...}
    """
    all_seeds = extract_seeds(fingerprint_map)
    return {
        beat_idx: seeds
        for beat_idx, seeds in all_seeds.items()
        if beat_idx not in target_beat_indices
    }


# ---------------------------------------------------------------------------
# Regeneration Plan Builder
# ---------------------------------------------------------------------------


def build_regeneration_plan(
    request: dict,
    fingerprint_map: dict,
    fingerprint_entry: dict,
) -> dict:
    """
    Build a regeneration plan for the Commander to execute.

    FR-VID-05 §4 Stage 2 Steps 1-5.

    Args:
        request: Regeneration request with beat_index, mode, revision_note.
        fingerprint_map: Full DEP-VID-014 map.
        fingerprint_entry: The target beat's fingerprint entry.

    Returns:
        Regeneration plan dict for the Commander.
    """
    beat_index = request["beat_index"]
    mode = request["mode"]
    revision_note = request["revision_note"]

    # Map revision to blocks
    block_mapping = map_revision_to_blocks(revision_note)

    # Determine enhanced prompt (for T2I modes)
    original_prompt = fingerprint_entry["fingerprint"].get(
        "stage_1_t2i", {}
    ).get("prompt_used", "")

    enhanced_prompt = None
    if mode in ("T2I_ONLY", "BOTH"):
        enhanced_prompt = enhance_prompt_with_revision(
            original_prompt, revision_note, block_mapping["target_blocks"]
        )

    # Check for I2V redirect
    if block_mapping["i2v_redirect"] and mode == "T2I_ONLY":
        # Motion keywords detected but T2I_ONLY requested — suggest I2V_ONLY
        pass  # The Commander can use this info; plan still valid

    # Compute seed locks
    target_set = {beat_index}
    seed_locks = compute_seed_locks(fingerprint_map, target_set)

    # Build the plan based on mode
    if mode == "T2I_ONLY":
        plan = {
            "mode": "T2I_ONLY",
            "beat_index": beat_index,
            "cascade_i2v": True,  # Mandatory per §3 Technical Decision 3
            "pipeline_calls": ["FR-VID-02", "FR-VID-04", "FR-VID-03"],
            "enhanced_prompt": enhanced_prompt,
            "reuse_keyframe": False,
            "seed_locks": seed_locks,
            "revision_note": revision_note,
            "block_mapping": block_mapping,
        }
    elif mode == "I2V_ONLY":
        existing_keyframe = fingerprint_entry["fingerprint"].get(
            "stage_2_i2v", {}
        ).get("input_image_url", "")
        plan = {
            "mode": "I2V_ONLY",
            "beat_index": beat_index,
            "cascade_i2v": False,
            "pipeline_calls": ["FR-VID-03"],
            "enhanced_prompt": None,
            "reuse_keyframe": True,
            "reuse_keyframe_url": existing_keyframe,
            "seed_locks": seed_locks,
            "revision_note": revision_note,
            "block_mapping": block_mapping,
        }
    else:  # BOTH
        plan = {
            "mode": "BOTH",
            "beat_index": beat_index,
            "cascade_i2v": True,
            "pipeline_calls": ["FR-VID-02", "FR-VID-04", "FR-VID-03"],
            "enhanced_prompt": enhanced_prompt,
            "reuse_keyframe": False,
            "seed_locks": seed_locks,
            "revision_note": revision_note,
            "block_mapping": block_mapping,
        }

    subsystem_runtime = load_compiled_subsystem_runtime_asset(
        "editor_regeneration",
        STAGE_SUBSYSTEM_ID_MAP["editor_regeneration"],
    )
    scene_intelligence_runtime = load_compiled_scene_intelligence_runtime_asset("editor_regeneration")
    patch_selection = build_regeneration_patch_selection(
        request,
        plan,
        subsystem_runtime,
        scene_intelligence_runtime,
    )
    plan["regeneration_decisions"] = patch_selection["regeneration_decisions"]
    plan["patch_selection"] = patch_selection["patch_selection"]
    plan["commander_dispatch"] = build_regeneration_dispatch(plan)
    plan["subsystem_runtime_asset"] = {
        "runtime_stage": subsystem_runtime["runtime_stage"],
        "asset_id": subsystem_runtime["asset_id"],
        "path": subsystem_runtime["asset_path"],
    }
    plan["scene_intelligence_runtime_asset"] = {
        "runtime_stage": scene_intelligence_runtime["runtime_stage"],
        "asset_id": scene_intelligence_runtime["asset_id"],
        "path": scene_intelligence_runtime["asset_path"],
    }

    return plan


# ---------------------------------------------------------------------------
# Execute Regeneration (plan + history + receipt)
# ---------------------------------------------------------------------------


def execute_regeneration(
    request: dict,
    fingerprint_map: dict,
    date_str: Optional[str] = None,
    batch_number: int = 1,
    previous_receipt: Optional[dict] = None,
    receipt_output_dir: Optional[str] = None,
) -> tuple[dict, dict, dict]:
    """
    Execute a regeneration request: validate, build plan, log history, emit receipt.

    This does NOT call the actual generation modules — it produces a plan
    for the Commander to execute, logs the supersession, and writes a receipt.

    Args:
        request: Regeneration request (beat_index, mode, revision_note).
        fingerprint_map: Full DEP-VID-014 map.
        date_str: Date string for new fingerprint ID.
        batch_number: Batch sequence.
        previous_receipt: Prior receipt for chain linking.
        receipt_output_dir: Receipt output directory.

    Returns:
        (plan, updated_fingerprint_entry, receipt)

    Raises:
        ValueError: If request is invalid or beat not found.
    """
    # Validate
    valid, error = validate_regeneration_request(request, fingerprint_map)
    if not valid:
        raise ValueError(error)

    beat_index = request["beat_index"]
    mode = request["mode"]
    revision_note = request["revision_note"]

    # Find the target fingerprint entry
    target_entry = None
    for entry in fingerprint_map["fingerprints"]:
        if entry["beat_index"] == beat_index:
            target_entry = entry
            break

    if target_entry is None:
        raise ValueError(f"INVALID_BEAT_INDEX: beat {beat_index} not found")

    # Check regeneration limit
    within_limit, limit_msg = check_regeneration_limit(target_entry)
    if not within_limit:
        raise ValueError(limit_msg)

    # Build regeneration plan
    plan = build_regeneration_plan(request, fingerprint_map, target_entry)

    # Generate new fingerprint ID
    if date_str is None:
        date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    new_fp_id = generate_fingerprint_id(date_str, batch_number, beat_index)

    preview_entry = deepcopy(target_entry)
    supersede_fingerprint(preview_entry, new_fp_id, mode, revision_note)

    output_dir = receipt_output_dir or "."
    legitimacy_context, legitimacy_target_ref, project_id = build_regeneration_legitimacy_context(
        request,
        plan,
        preview_entry,
    )
    constraint_manifest, legitimacy_receipt = run_legitimacy_check(
        compile_target="EDITOR_REGENERATION",
        project_id=project_id,
        target_ref=legitimacy_target_ref,
        context=legitimacy_context,
        previous_receipt=previous_receipt,
        receipt_output_dir=output_dir,
    )
    if constraint_manifest["decision"] == "BLOCK":
        raise ValueError(
            "EDITOR_REGEN_LEGITIMACY_BLOCKED: "
            + "; ".join(constraint_manifest.get("required_actions", []))
        )

    # Log supersession in history only after legitimacy passes.
    supersede_fingerprint(target_entry, new_fp_id, mode, revision_note)
    plan["constraint_manifest"] = {
        "constraint_manifest_id": constraint_manifest["constraint_manifest_id"],
        "decision": constraint_manifest["decision"],
        "path": next(
            output["path"]
            for output in constraint_manifest["output_files"]
            if output["kind"] == "constraint_manifest"
        ),
    }

    # Write receipt
    receipt = write_receipt(
        stage_name="REGENERATION_EXECUTE",
        agent_name="regeneration_handler",
        input_payload=request,
        output_payload=plan,
        previous_receipt=legitimacy_receipt,
        output_dir=output_dir,
    )

    return plan, target_entry, receipt


# ---------------------------------------------------------------------------
# Multi-Beat Concurrent Regeneration
# ---------------------------------------------------------------------------


def merge_regeneration_requests(requests: list[dict]) -> set[int]:
    """
    Merge multiple regeneration requests into a single target set.

    FR-VID-05 §3 Technical Decision 5: The target set is the union of all
    requested beat indices.
    """
    return {req["beat_index"] for req in requests}
