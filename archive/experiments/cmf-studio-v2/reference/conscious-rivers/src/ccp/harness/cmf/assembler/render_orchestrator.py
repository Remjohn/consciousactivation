"""
Render Orchestrator — Remotion render job preparation and result processing.

FR-VID-08 §4 Stages 1-2: Template resolution, quality presets, Ken Burns
detection, render job construction, and render result processing.

Technical Decision 1: One composition per arc type.
Technical Decision 2: <Video> components, Ken Burns fallback for static images.
Technical Decision 3: 3-tier quality (preview 480p, review 720p, final 1080p).
Technical Decision 4: Remotion Studio for preview.
"""

import logging
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

try:
    from .receipt_chain import write_receipt
except ImportError:
    from receipt_chain import write_receipt


logger = logging.getLogger("cmf.render_orchestrator")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_QUALITY_TIERS = {"preview", "review", "final"}

# 3-tier render quality presets — FR-VID-08 §3 TD3
QUALITY_PRESETS = {
    "preview": {
        "tier": "preview",
        "width": 540,
        "height": 960,
        "codec": "h264",
        "bitrate_kbps": 1000,
        "crf": 32,
        "pixel_format": "yuv420p",
        "audio_bitrate_kbps": 96,
    },
    "review": {
        "tier": "review",
        "width": 720,
        "height": 1280,
        "codec": "h264",
        "bitrate_kbps": 2500,
        "crf": 26,
        "pixel_format": "yuv420p",
        "audio_bitrate_kbps": 128,
    },
    "final": {
        "tier": "final",
        "width": 1080,
        "height": 1920,
        "codec": "h264",
        "bitrate_kbps": 5000,
        "crf": 18,
        "pixel_format": "yuv420p",
        "audio_bitrate_kbps": 192,
    },
}

# Default arc template registry — FR-VID-08 §3 TD1
DEFAULT_ARC_TEMPLATES = {
    "Witness": {
        "composition_id": "cmf-witness",
        "template_path": "packages/remotion-compositions/src/templates/cmf-witness.tsx",
        "supported_arc_stages": ["hook", "build", "rising", "climax", "resolution"],
        "default_transitions": {
            "hook_to_build": {"type": "crossfade", "duration_frames": 12},
            "build_to_rising": {"type": "crossfade", "duration_frames": 12},
            "rising_to_climax": {"type": "push", "duration_frames": 48},
            "climax_to_resolution": {"type": "crossfade", "duration_frames": 12},
        },
        "ken_burns_enabled": True,
    },
    "Breakthrough": {
        "composition_id": "cmf-breakthrough",
        "template_path": "packages/remotion-compositions/src/templates/cmf-breakthrough.tsx",
        "supported_arc_stages": ["hook", "build", "escalation", "climax", "resolution"],
        "default_transitions": {
            "hook_to_build": {"type": "cut", "duration_frames": 0},
            "build_to_escalation": {"type": "cut", "duration_frames": 0},
            "escalation_to_climax": {"type": "cut", "duration_frames": 2},
            "climax_to_resolution": {"type": "crossfade", "duration_frames": 12},
        },
        "ken_burns_enabled": True,
    },
    "Call-to-Adventure": {
        "composition_id": "cmf-call-to-adventure",
        "template_path": "packages/remotion-compositions/src/templates/cmf-call-to-adventure.tsx",
        "supported_arc_stages": ["hook", "exploration", "call", "return", "resolution"],
        "default_transitions": {
            "hook_to_exploration": {"type": "zoom", "duration_frames": 18},
            "exploration_to_call": {"type": "crossfade", "duration_frames": 12},
            "call_to_return": {"type": "push", "duration_frames": 18},
            "return_to_resolution": {"type": "crossfade", "duration_frames": 12},
        },
        "ken_burns_enabled": True,
    },
}

# Audio-video duration tolerance — FR-VID-08 §6 Gate K Q3
AUDIO_VIDEO_DURATION_TOLERANCE_SEC = 0.5

# Render ID pattern
RENDER_ID_PATTERN = re.compile(r"^RENDER-\d{8}-\d{3}$")


# ---------------------------------------------------------------------------
# Template Resolution — §4 Stage 1
# ---------------------------------------------------------------------------


def resolve_template(arc_type: str, registry: Optional[dict] = None) -> dict:
    """
    Resolve a Remotion composition template for the given arc type.

    Uses the provided registry or falls back to DEFAULT_ARC_TEMPLATES.
    Returns the template entry with composition_id, template_path, etc.

    Raises ValueError if arc_type is not found in registry.
    """
    templates = registry if registry is not None else DEFAULT_ARC_TEMPLATES
    if arc_type not in templates:
        raise ValueError(
            f"No template registered for arc_type '{arc_type}'. "
            f"Available: {sorted(templates.keys())}"
        )
    return dict(templates[arc_type])


def get_composition_id(arc_type: str, registry: Optional[dict] = None) -> str:
    """Return the Remotion composition_id for an arc type."""
    template = resolve_template(arc_type, registry)
    return template["composition_id"]


def check_arc_stage_coverage(
    arc_type: str, manifest_beats: list, registry: Optional[dict] = None
) -> tuple[bool, list]:
    """
    Check whether a template supports all arc stages present in the manifest.

    Returns (all_covered, missing_stages).
    """
    template = resolve_template(arc_type, registry)
    supported = set(template["supported_arc_stages"])
    manifest_stages = {beat.get("arc_stage") for beat in manifest_beats if beat.get("arc_stage")}
    missing = sorted(manifest_stages - supported)
    return len(missing) == 0, missing


# ---------------------------------------------------------------------------
# Quality Presets — §3 TD3
# ---------------------------------------------------------------------------


def get_quality_preset(tier: str) -> dict:
    """
    Return the quality preset config for the given tier.

    Raises ValueError if tier is invalid.
    """
    if tier not in VALID_QUALITY_TIERS:
        raise ValueError(
            f"Invalid quality tier '{tier}'. Must be one of: {sorted(VALID_QUALITY_TIERS)}"
        )
    return dict(QUALITY_PRESETS[tier])


def get_resolution_string(tier: str) -> str:
    """Return 'WIDTHxHEIGHT' string for the given quality tier."""
    preset = get_quality_preset(tier)
    return f"{preset['width']}x{preset['height']}"


# ---------------------------------------------------------------------------
# Ken Burns Detection — §3 TD2
# ---------------------------------------------------------------------------


def detect_ken_burns_beats(manifest_beats: list) -> list[int]:
    """
    Identify beats that require Ken Burns fallback rendering.

    A beat uses Ken Burns when:
    - asset_status == 'KEN_BURNS_FALLBACK', OR
    - video_clip_url is None/empty AND fallback_image_url is present
    """
    kb_indices = []
    for beat in manifest_beats:
        status = beat.get("asset_status", "")
        video_url = beat.get("video_clip_url")
        fallback_url = beat.get("fallback_image_url")
        if status == "KEN_BURNS_FALLBACK":
            kb_indices.append(beat.get("beat_index", -1))
        elif (not video_url) and fallback_url:
            kb_indices.append(beat.get("beat_index", -1))
    return kb_indices


# ---------------------------------------------------------------------------
# Render Job Construction — §4 Stage 2
# ---------------------------------------------------------------------------


def generate_render_id() -> str:
    """Generate a render ID in the pattern RENDER-YYYYMMDD-NNN."""
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    seq = str(uuid.uuid4().int % 1000).zfill(3)
    return f"RENDER-{date_str}-{seq}"


def build_render_job(
    manifest: dict,
    quality_tier: str,
    pipeline_id: str,
    registry: Optional[dict] = None,
    operator_approved_review: bool = False,
) -> dict:
    """
    Construct a render job specification from a manifest and quality tier.

    For 'final' tier, requires operator_approved_review=True (Gate K Q5).

    Returns a render job dict ready for submission to the render server.
    """
    arc_type = manifest.get("arc_type", "")
    template = resolve_template(arc_type, registry)
    preset = get_quality_preset(quality_tier)

    if quality_tier == "final" and not operator_approved_review:
        raise ValueError(
            "Final quality render requires prior review approval. "
            "Set operator_approved_review=True after a review render is approved."
        )

    beats = manifest.get("beats", [])
    ken_burns_indices = detect_ken_burns_beats(beats)

    render_id = generate_render_id()
    return {
        "render_id": render_id,
        "pipeline_id": pipeline_id,
        "video_id": manifest.get("manifest_id", "").replace("MAN-VID", "CMF-VID"),
        "project_id": manifest.get("project_id", ""),
        "quality_tier": quality_tier,
        "composition_id": template["composition_id"],
        "template_path": template["template_path"],
        "manifest_id": manifest.get("manifest_id", ""),
        "manifest_path": None,
        "fps": manifest.get("fps", 24),
        "total_frames": manifest.get("total_frames", 0),
        "total_duration_sec": manifest.get("total_duration_sec", 0.0),
        "resolution": f"{preset['width']}x{preset['height']}",
        "codec": preset["codec"],
        "bitrate_kbps": preset["bitrate_kbps"],
        "crf": preset["crf"],
        "pixel_format": preset["pixel_format"],
        "audio_bitrate_kbps": preset["audio_bitrate_kbps"],
        "beat_count": len(beats),
        "ken_burns_beats": ken_burns_indices,
        "status": "PENDING",
    }


# ---------------------------------------------------------------------------
# Render Result Processing — §5
# ---------------------------------------------------------------------------


def validate_render_result(result: dict) -> tuple[bool, list]:
    """
    Validate a render job result for completeness and consistency.

    Returns (valid, errors).
    """
    errors = []
    if result.get("status") != "COMPLETED":
        errors.append(f"Render status is '{result.get('status')}', expected 'COMPLETED'")

    output = result.get("output", {})
    if not output.get("file_path"):
        errors.append("Missing output file_path")
    if output.get("file_size_bytes", 0) <= 0:
        errors.append("Output file_size_bytes must be > 0")
    if output.get("duration_sec", 0) <= 0:
        errors.append("Output duration_sec must be > 0")
    if output.get("fps", 0) <= 0:
        errors.append("Output fps must be > 0")

    stats = result.get("render_stats", {})
    if stats.get("frames_rendered", 0) <= 0:
        errors.append("render_stats.frames_rendered must be > 0")

    if result.get("error") not in (None, ""):
        errors.append(f"Render error present: {result['error']}")

    return len(errors) == 0, errors


def compute_render_efficiency(result: dict) -> Optional[float]:
    """
    Compute render efficiency as frames_per_second / fps.

    Returns ratio > 1 means faster than real-time, None if data missing.
    """
    stats = result.get("render_stats", {})
    fps = result.get("output", {}).get("fps")
    render_fps = stats.get("frames_per_second")
    if fps and render_fps and fps > 0:
        return round(render_fps / fps, 2)
    return None


# ---------------------------------------------------------------------------
# Receipt-writing entry points — §4
# ---------------------------------------------------------------------------


def run_template_compile(
    manifest: dict,
    registry: Optional[dict] = None,
    output_dir: str = ".",
    previous_receipt: Optional[dict] = None,
) -> dict:
    """
    Stage 1: Template compilation — resolve template, check arc stage coverage,
    detect Ken Burns beats. Writes TEMPLATE_COMPILE receipt.
    """
    arc_type = manifest.get("arc_type", "")
    template = resolve_template(arc_type, registry)
    beats = manifest.get("beats", [])
    covered, missing = check_arc_stage_coverage(arc_type, beats, registry)
    ken_burns = detect_ken_burns_beats(beats)

    result = {
        "arc_type": arc_type,
        "composition_id": template["composition_id"],
        "template_path": template["template_path"],
        "arc_stage_coverage": covered,
        "missing_arc_stages": missing,
        "ken_burns_beats": ken_burns,
        "beat_count": len(beats),
    }

    if not covered:
        logger.warning(
            "Template '%s' missing arc stages: %s", arc_type, missing
        )

    receipt = write_receipt(
        stage_name="TEMPLATE_COMPILE",
        agent_name="template_developer",
        input_payload=manifest,
        output_payload=result,
        previous_receipt=previous_receipt,
        output_dir=output_dir,
    )

    return {"result": result, "receipt": receipt}


def run_video_render(
    manifest: dict,
    quality_tier: str,
    pipeline_id: str,
    render_result: dict,
    registry: Optional[dict] = None,
    output_dir: str = ".",
    previous_receipt: Optional[dict] = None,
) -> dict:
    """
    Stage 2: Video render — validate render result and write VIDEO_RENDER receipt.

    Takes a completed render_result (from the Remotion render server) and
    validates/records it in the receipt chain.
    """
    valid, errors = validate_render_result(render_result)
    efficiency = compute_render_efficiency(render_result)

    output = {
        "render_id": render_result.get("render_id"),
        "quality_tier": quality_tier,
        "status": render_result.get("status"),
        "valid": valid,
        "validation_errors": errors,
        "render_efficiency": efficiency,
        "output_file": render_result.get("output", {}).get("file_path"),
    }

    if not valid:
        logger.warning("Render result validation failed: %s", errors)

    receipt = write_receipt(
        stage_name="VIDEO_RENDER",
        agent_name="remotion_render_server",
        input_payload={"manifest_id": manifest.get("manifest_id"), "quality_tier": quality_tier},
        output_payload=output,
        previous_receipt=previous_receipt,
        output_dir=output_dir,
    )

    return {"result": output, "receipt": receipt}
