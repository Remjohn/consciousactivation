"""
Beat Cluster Parser — Parse EDL into canonical beat array with frame timings.

FR-VID-01 §4 Stage 1: Beat Cluster Parsing

Validates raw beat cluster JSON from the CMF narrative pipeline,
computes frame-accurate timing (ceil rounding), and assigns transitions
from DEP-VID-003 based on arc_stage + beat_type.

Technical Decision 1: Beat cluster IS the EDL — no re-analysis.
Technical Decision 2: frames = ceil(duration_sec × fps) — always round up.
Technical Decision 3: Transitions are deterministic from arc_stage mapping.
"""

import json
from math import ceil
from pathlib import Path
from typing import Any, Optional

import yaml

try:
    from .receipt_chain import write_receipt
except ImportError:
    from receipt_chain import write_receipt


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REQUIRED_TOP_LEVEL = {"beat_cluster_id", "arc_type", "project_id", "beats"}
REQUIRED_PER_BEAT = {"beat_index", "beat_type", "duration_sec", "arc_stage"}
DEFAULT_FPS = 24
DEFAULT_ARC_SEQUENCE = ["opening", "rising_action", "tension", "climax", "falling_action", "resolution"]

# Path to transition preset library relative to this file
_SCHEMA_DIR = Path(__file__).parent / "schemas"


# ---------------------------------------------------------------------------
# Transition Preset Library Loader
# ---------------------------------------------------------------------------


def load_transition_presets(
    preset_path: Optional[str] = None,
) -> dict:
    """
    Load the DEP-VID-003 transition preset library.

    Returns dict with keys: arc_stage_defaults, beat_type_overrides, arc_sequences.
    """
    if preset_path is None:
        preset_path = str(_SCHEMA_DIR / "dep_vid_003_transition_preset_library.yaml")

    with open(preset_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_transition(
    arc_stage: str,
    beat_type: str,
    presets: dict,
) -> Optional[dict]:
    """
    Resolve transition preset for a beat based on arc_stage + beat_type.

    FR-VID-01 §4 Stage 1 Step 5: Beat type overrides take priority
    over arc_stage defaults when the combination exists.
    """
    # Check beat_type override first
    overrides = presets.get("beat_type_overrides", {})
    if arc_stage in overrides and beat_type in overrides[arc_stage]:
        return dict(overrides[arc_stage][beat_type])

    # Fall back to arc_stage default
    defaults = presets.get("arc_stage_defaults", {})
    if arc_stage in defaults:
        return dict(defaults[arc_stage])

    return None


# ---------------------------------------------------------------------------
# Beat Cluster Validation
# ---------------------------------------------------------------------------


def validate_beat_cluster(raw: dict) -> tuple[bool, list[str]]:
    """
    Validate required fields in a raw beat cluster JSON.

    Returns:
        (valid, missing_fields_list)
    """
    missing = []
    for field in REQUIRED_TOP_LEVEL:
        if field not in raw:
            missing.append(f"top-level: {field}")

    beats = raw.get("beats", [])
    if not isinstance(beats, list):
        missing.append("beats must be an array")
        return False, missing

    for i, beat in enumerate(beats):
        for field in REQUIRED_PER_BEAT:
            if field not in beat:
                missing.append(f"beat[{i}]: {field}")

        # Safety: reject zero or negative durations
        dur = beat.get("duration_sec", 0)
        if isinstance(dur, (int, float)) and dur <= 0:
            missing.append(f"beat[{i}]: duration_sec must be positive (got {dur})")

    return len(missing) == 0, missing


# ---------------------------------------------------------------------------
# Legacy Fallback — §7 Backward Compatibility
# ---------------------------------------------------------------------------


def apply_legacy_fallbacks(
    raw: dict,
    total_video_duration: Optional[float] = None,
) -> dict:
    """
    Apply backward-compatibility fallbacks for legacy beat cluster formats.

    FR-VID-01 §7:
    - Missing arc_stage: sequential assignment based on position.
    - Missing duration_sec: equal distribution.
    - Missing visual_prompt_ref: flagged ASSET_MISSING.
    - Missing narration_text: empty string (no captions).
    """
    beats = raw.get("beats", [])
    if not isinstance(beats, list):
        return raw
    beat_count = len(beats)
    is_legacy = False

    for i, beat in enumerate(beats):
        if "arc_stage" not in beat:
            # Assign sequentially from default arc sequence
            idx = min(i, len(DEFAULT_ARC_SEQUENCE) - 1)
            beat["arc_stage"] = DEFAULT_ARC_SEQUENCE[idx]
            is_legacy = True

        if "duration_sec" not in beat:
            if total_video_duration and beat_count > 0:
                beat["duration_sec"] = total_video_duration / beat_count
            else:
                beat["duration_sec"] = 4.0  # safe default
            is_legacy = True

        if "visual_prompt_ref" not in beat:
            beat["visual_prompt_ref"] = None
            is_legacy = True

        if "narration_text" not in beat:
            beat["narration_text"] = ""

        if "beat_type" not in beat:
            beat["beat_type"] = beat.get("arc_stage", "unknown")
            is_legacy = True

        if "beat_index" not in beat:
            beat["beat_index"] = i
            is_legacy = True

    if is_legacy:
        raw.setdefault("_warnings", [])
        raw["_warnings"].append("LEGACY_BEAT_CLUSTER")

    return raw


# ---------------------------------------------------------------------------
# Frame Timing Computation
# ---------------------------------------------------------------------------


def compute_frame_timings(
    beats: list[dict],
    fps: int = DEFAULT_FPS,
) -> list[dict]:
    """
    Compute frame-accurate timing for each beat.

    FR-VID-01 §3 TD2: frames = ceil(duration_sec × fps).
    Start frame = cumulative sum of all previous beat durations.
    """
    cumulative = 0
    timed_beats = []

    for beat in beats:
        duration_sec = beat["duration_sec"]
        duration_frames = ceil(duration_sec * fps)

        timed_beat = dict(beat)
        timed_beat["start_frame"] = cumulative
        timed_beat["duration_frames"] = duration_frames
        timed_beat["duration_sec"] = duration_sec

        cumulative += duration_frames
        timed_beats.append(timed_beat)

    return timed_beats


# ---------------------------------------------------------------------------
# Parse Beat Cluster → Canonical Beat Array
# ---------------------------------------------------------------------------


def parse_beat_cluster(
    raw: dict,
    fps: int = DEFAULT_FPS,
    presets: Optional[dict] = None,
) -> dict:
    """
    Parse a raw beat cluster JSON into a canonical beat array.

    FR-VID-01 §4 Stage 1: Full pipeline — validate, apply fallbacks,
    compute timings, assign transitions.

    Returns:
        {
            "status": "PARSED" | "PARSE_ERROR",
            "beat_cluster_id": str,
            "arc_type": str,
            "project_id": str,
            "fps": int,
            "beats": [...],
            "total_frames": int,
            "total_duration_sec": float,
            "warnings": [...],
            "errors": [...],
        }
    """
    # Apply legacy fallbacks first
    raw = apply_legacy_fallbacks(raw)

    # Validate
    valid, missing = validate_beat_cluster(raw)
    if not valid:
        return {
            "status": "PARSE_ERROR",
            "errors": missing,
            "beats": [],
            "total_frames": 0,
        }

    # Load transition presets if not provided
    if presets is None:
        try:
            presets = load_transition_presets()
        except FileNotFoundError:
            presets = {"arc_stage_defaults": {}, "beat_type_overrides": {}}

    # Compute frame timings
    beats = compute_frame_timings(raw["beats"], fps)

    # Assign transitions
    for beat in beats:
        transition = resolve_transition(
            beat.get("arc_stage", ""), beat.get("beat_type", ""), presets
        )
        beat["transition"] = transition

    total_frames = sum(b["duration_frames"] for b in beats)
    total_duration = sum(b["duration_sec"] for b in beats)

    return {
        "status": "PARSED",
        "beat_cluster_id": raw.get("beat_cluster_id", ""),
        "arc_type": raw.get("arc_type", ""),
        "project_id": raw.get("project_id", ""),
        "fps": fps,
        "beats": beats,
        "total_frames": total_frames,
        "total_duration_sec": total_duration,
        "warnings": raw.get("_warnings", []),
        "errors": [],
    }


# ---------------------------------------------------------------------------
# Pipeline Entry Point with Receipt
# ---------------------------------------------------------------------------


def run_beat_cluster_parse(
    raw: dict,
    fps: int = DEFAULT_FPS,
    previous_receipt: Optional[dict] = None,
    receipt_output_dir: Optional[str] = None,
) -> tuple[dict, dict]:
    """
    Run beat cluster parsing with receipt chain.

    Returns:
        (parsed_result, receipt)
    """
    parsed = parse_beat_cluster(raw, fps)

    output_dir = receipt_output_dir or "."
    receipt = write_receipt(
        stage_name="BEAT_CLUSTER_PARSE",
        agent_name="beat_cluster_parser",
        input_payload=raw,
        output_payload=parsed,
        previous_receipt=previous_receipt,
        output_dir=output_dir,
    )

    return parsed, receipt
