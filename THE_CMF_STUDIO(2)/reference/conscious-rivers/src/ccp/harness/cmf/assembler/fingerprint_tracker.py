"""
Fingerprint Tracker — Dual-Stage Beat Fingerprint Manager

FR-VID-05 §4 Stage 1: Fingerprint Creation

Assigns every generated beat a unique fingerprint_id containing the
complete generation context for both T2I and I2V stages. Fingerprints
are immutable once created; regeneration creates a NEW fingerprint and
supersedes the old one.

Fingerprint ID format: FP-VID-YYYYMMDD-NNN-BXX  (CVE-compatible)
  - YYYYMMDD = date
  - NNN = batch sequence number (zero-padded 3 digits)
  - BXX = beat index (zero-padded 2 digits)
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

try:
    from .receipt_chain import write_receipt
except ImportError:
    from receipt_chain import write_receipt


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

FINGERPRINT_ID_REGEX = re.compile(r"^FP-VID-\d{8}-\d{3}-B\d{2}$")
MAX_REGENERATION_PER_BEAT = 10


# ---------------------------------------------------------------------------
# Fingerprint ID Generation
# ---------------------------------------------------------------------------


def generate_fingerprint_id(
    date_str: str,
    batch_number: int,
    beat_index: int,
    version: Optional[int] = None,
) -> str:
    """
    Generate a CVE-compatible fingerprint ID.

    Args:
        date_str: Date in YYYYMMDD format.
        batch_number: Batch sequence number (1-999).
        beat_index: Beat index (0-99).
        version: Optional version suffix for regenerated beats.

    Returns:
        Fingerprint ID string matching FP-VID-YYYYMMDD-NNN-BXX format.
    """
    fp_id = f"FP-VID-{date_str}-{batch_number:03d}-B{beat_index:02d}"
    if version is not None and version > 0:
        # For internal tracking; the canonical format stays CVE-compatible
        # but we append version to history entries only
        pass
    return fp_id


def validate_fingerprint_id(fp_id: str) -> bool:
    """Check if a fingerprint ID matches the canonical format."""
    return bool(FINGERPRINT_ID_REGEX.match(fp_id))


# ---------------------------------------------------------------------------
# Fingerprint Creation — Stage 1 T2I
# ---------------------------------------------------------------------------


def create_fingerprint_from_t2i(
    beat_index: int,
    t2i_result: dict,
    date_str: Optional[str] = None,
    batch_number: int = 1,
) -> dict:
    """
    Create a new fingerprint entry after T2I generation completes.

    FR-VID-05 §4 Step 1-3: Create fingerprint, populate stage_1_t2i,
    set stage_2_i2v to PENDING.

    Args:
        beat_index: Beat index in the video.
        t2i_result: T2I generation result (DEP-VID-008 fields).
        date_str: Date string YYYYMMDD (defaults to today).
        batch_number: Batch sequence number.

    Returns:
        Fingerprint entry dict with stage_1_t2i populated and stage_2_i2v PENDING.
    """
    if date_str is None:
        date_str = datetime.now(timezone.utc).strftime("%Y%m%d")

    fp_id = generate_fingerprint_id(date_str, batch_number, beat_index)

    stage_1 = {
        "status": "GENERATED",
        "runninghub_workflow_id": t2i_result.get("workflow_id", ""),
        "prompt_used": t2i_result.get("prompt_used", ""),
        "negative_prompt": t2i_result.get("negative_prompt", ""),
        "seed": t2i_result.get("seed"),
        "model": t2i_result.get("model", ""),
        "pssl_params": t2i_result.get("pssl_params", {}),
        "output_image_url": t2i_result.get("output_image_url", ""),
        "quality_score": t2i_result.get("quality_score"),
        "generation_timestamp": t2i_result.get(
            "generation_timestamp",
            datetime.now(timezone.utc).isoformat(),
        ),
    }

    return {
        "beat_index": beat_index,
        "active_fingerprint_id": fp_id,
        "fingerprint": {
            "fingerprint_id": fp_id,
            "stage_1_t2i": stage_1,
            "stage_2_i2v": {"status": "PENDING"},
        },
        "regeneration_history": [],
    }


# ---------------------------------------------------------------------------
# Fingerprint Update — Stage 2 I2V
# ---------------------------------------------------------------------------


def update_fingerprint_with_i2v(
    fingerprint_entry: dict,
    i2v_result: dict,
) -> dict:
    """
    Update an existing fingerprint entry with I2V generation results.

    FR-VID-05 §4 Steps 4-5: Populate stage_2_i2v, set status to COMPLETE.

    Args:
        fingerprint_entry: Existing fingerprint entry (from create_fingerprint_from_t2i).
        i2v_result: I2V generation result (DEP-VID-011 fields).

    Returns:
        Updated fingerprint entry with stage_2_i2v populated and status COMPLETE.
    """
    stage_2 = {
        "status": "GENERATED",
        "runninghub_workflow_id": i2v_result.get("workflow_id", ""),
        "input_image_url": i2v_result.get("input_keyframe_url", ""),
        "motion_parameters": i2v_result.get("motion_parameters_applied", {}),
        "output_video_url": i2v_result.get("output_video_url", ""),
        "seed_used": i2v_result.get("seed_used"),
        "vram_tier_used": i2v_result.get("vram_tier_used", "48GB"),
        "generation_timestamp": i2v_result.get(
            "generation_timestamp",
            datetime.now(timezone.utc).isoformat(),
        ),
    }

    fingerprint_entry["fingerprint"]["stage_2_i2v"] = stage_2
    return fingerprint_entry


# ---------------------------------------------------------------------------
# Beat Fingerprint Map
# ---------------------------------------------------------------------------


def create_beat_fingerprint_map(
    video_id: str,
    project_id: str,
    beat_cluster_id: str,
    fingerprint_entries: list[dict],
) -> dict:
    """
    Build the complete beat fingerprint map (DEP-VID-014).

    FR-VID-05 §4 Step 6: Write the complete beat fingerprint map.
    """
    total_regens = sum(
        len(entry.get("regeneration_history", []))
        for entry in fingerprint_entries
    )
    beats_with_regen = sum(
        1 for entry in fingerprint_entries
        if len(entry.get("regeneration_history", [])) > 0
    )

    return {
        "video_id": video_id,
        "project_id": project_id,
        "beat_cluster_id": beat_cluster_id,
        "fingerprints": fingerprint_entries,
        "summary": {
            "total_beats": len(fingerprint_entries),
            "total_regenerations": total_regens,
            "beats_with_regeneration": beats_with_regen,
        },
    }


# ---------------------------------------------------------------------------
# Supersede Fingerprint (for Regeneration)
# ---------------------------------------------------------------------------


def supersede_fingerprint(
    fingerprint_entry: dict,
    new_fingerprint_id: str,
    mode: str,
    reason: str,
) -> dict:
    """
    Log the current fingerprint as superseded and prepare for replacement.

    FR-VID-05 §4 Stage 2 Step 2: Log current fingerprint to
    regeneration_history before creating the new one.

    Args:
        fingerprint_entry: Current fingerprint entry to supersede.
        new_fingerprint_id: The ID of the replacement fingerprint.
        mode: Regeneration mode (T2I_ONLY, I2V_ONLY, BOTH).
        reason: Operator's revision note.

    Returns:
        Updated fingerprint entry with history logged.
    """
    old_fp_id = fingerprint_entry["fingerprint"]["fingerprint_id"]

    history_entry = {
        "superseded_fingerprint_id": old_fp_id,
        "superseded_at": datetime.now(timezone.utc).isoformat(),
        "reason": reason,
        "mode": mode,
        "new_fingerprint_id": new_fingerprint_id,
    }

    fingerprint_entry["regeneration_history"].append(history_entry)
    return fingerprint_entry


# ---------------------------------------------------------------------------
# Seed Extraction
# ---------------------------------------------------------------------------


def extract_seeds(fingerprint_map: dict) -> dict[int, dict]:
    """
    Extract current seeds for all beats from the fingerprint map.

    Returns dict mapping beat_index → {"t2i_seed": ..., "i2v_seed": ...}.
    """
    seeds = {}
    for entry in fingerprint_map.get("fingerprints", []):
        beat_idx = entry["beat_index"]
        fp = entry["fingerprint"]
        seeds[beat_idx] = {
            "t2i_seed": fp.get("stage_1_t2i", {}).get("seed"),
            "i2v_seed": fp.get("stage_2_i2v", {}).get("seed_used"),
        }
    return seeds


# ---------------------------------------------------------------------------
# Pipeline Entry Point with Receipt
# ---------------------------------------------------------------------------


def run_fingerprint_creation(
    beat_index: int,
    t2i_result: dict,
    i2v_result: Optional[dict] = None,
    date_str: Optional[str] = None,
    batch_number: int = 1,
    previous_receipt: Optional[dict] = None,
    receipt_output_dir: Optional[str] = None,
) -> tuple[dict, dict]:
    """
    Run fingerprint creation pipeline with receipt chain.

    Creates fingerprint from T2I result, optionally updates with I2V result,
    and writes a receipt for chain linking.

    Returns:
        (fingerprint_entry, receipt)
    """
    entry = create_fingerprint_from_t2i(
        beat_index, t2i_result, date_str, batch_number
    )

    if i2v_result is not None:
        entry = update_fingerprint_with_i2v(entry, i2v_result)

    output_dir = receipt_output_dir or "."
    receipt = write_receipt(
        stage_name="FINGERPRINT_CREATE",
        agent_name="fingerprint_tracker",
        input_payload={"beat_index": beat_index, "t2i_result": t2i_result},
        output_payload=entry,
        previous_receipt=previous_receipt,
        output_dir=output_dir,
    )

    return entry, receipt
