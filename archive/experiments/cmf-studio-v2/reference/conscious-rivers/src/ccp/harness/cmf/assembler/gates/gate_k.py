"""
Gate K — Pre-Render Constraint Network (Render Quality Assurance).

FR-VID-08 §6: Before triggering any render job, the agent must answer
ALL 5 questions. Violations produce specific error codes preventing
wasted render cycles.

Gate K Questions:
  Q1: Manifest completeness — status == ASSEMBLED (not ASSEMBLED_WITH_GAPS)?
  Q2: Asset accessibility — all video clip URLs present (non-null)?
  Q3: Audio-video duration match — voiceover ≈ manifest ±0.5s, music ≥ manifest?
  Q4: Template compatibility — arc_type in registry, all arc stages covered?
  Q5: Render budget — final requires prior review approval?
"""

import logging
from typing import Any, Optional

try:
    from .render_orchestrator import (
        AUDIO_VIDEO_DURATION_TOLERANCE_SEC,
        DEFAULT_ARC_TEMPLATES,
        VALID_QUALITY_TIERS,
        check_arc_stage_coverage,
        resolve_template,
    )
except ImportError:
    from render_orchestrator import (
        AUDIO_VIDEO_DURATION_TOLERANCE_SEC,
        DEFAULT_ARC_TEMPLATES,
        VALID_QUALITY_TIERS,
        check_arc_stage_coverage,
        resolve_template,
    )


logger = logging.getLogger("cmf.gate_k")


# ---------------------------------------------------------------------------
# Q1 — Manifest Completeness
# ---------------------------------------------------------------------------


def check_manifest_completeness(
    status: str, operator_approved_gaps: bool = False
) -> tuple[bool, str]:
    """
    Q1: Is the manifest status ASSEMBLED (not ASSEMBLED_WITH_GAPS)?

    If status is ASSEMBLED_WITH_GAPS, only passes when the operator has
    explicitly approved rendering with placeholder beats.

    Returns (passed, violation_or_ok).
    """
    if status == "ASSEMBLED":
        return True, "OK"
    if status == "ASSEMBLED_WITH_GAPS":
        if operator_approved_gaps:
            return True, "OK_WITH_GAPS_APPROVED"
        return False, "MANIFEST_INCOMPLETE"
    return False, "MANIFEST_STATUS_INVALID"


# ---------------------------------------------------------------------------
# Q2 — Asset Accessibility
# ---------------------------------------------------------------------------


def check_asset_accessibility(beats: list) -> tuple[bool, str]:
    """
    Q2: Are all video clip URLs present for RESOLVED beats?

    Checks that every beat with asset_status == RESOLVED has a non-null
    video_clip_url. KEN_BURNS_FALLBACK beats must have fallback_image_url.
    ASSET_MISSING beats are flagged.

    Returns (passed, violation_or_ok).
    """
    missing_assets = []
    for beat in beats:
        idx = beat.get("beat_index", -1)
        status = beat.get("asset_status", "")

        if status == "RESOLVED":
            if not beat.get("video_clip_url"):
                missing_assets.append(f"beat_{idx}_missing_video_url")
        elif status == "KEN_BURNS_FALLBACK":
            if not beat.get("fallback_image_url"):
                missing_assets.append(f"beat_{idx}_missing_fallback_image")
        elif status == "ASSET_MISSING":
            missing_assets.append(f"beat_{idx}_asset_missing")

    if missing_assets:
        return False, f"ASSET_INACCESSIBLE:{','.join(missing_assets)}"
    return True, "OK"


# ---------------------------------------------------------------------------
# Q3 — Audio-Video Duration Match
# ---------------------------------------------------------------------------


def check_audio_video_duration(
    manifest_duration_sec: float,
    voiceover_duration_sec: Optional[float],
    music_duration_sec: Optional[float],
) -> tuple[bool, str]:
    """
    Q3: Does voiceover duration match manifest ±0.5s? Music ≥ manifest?

    Returns (passed, violation_or_ok).
    """
    tolerance = AUDIO_VIDEO_DURATION_TOLERANCE_SEC
    violations = []

    if voiceover_duration_sec is not None:
        diff = abs(voiceover_duration_sec - manifest_duration_sec)
        if diff > tolerance:
            violations.append(
                f"VOICEOVER_MISMATCH(diff={diff:.2f}s,tolerance={tolerance}s)"
            )

    if music_duration_sec is not None:
        if music_duration_sec < manifest_duration_sec:
            shortfall = manifest_duration_sec - music_duration_sec
            violations.append(
                f"MUSIC_TOO_SHORT(shortfall={shortfall:.2f}s)"
            )

    if violations:
        return False, ";".join(violations)
    return True, "OK"


# ---------------------------------------------------------------------------
# Q4 — Template Compatibility
# ---------------------------------------------------------------------------


def check_template_compatibility(
    arc_type: str, beats: list, registry: Optional[dict] = None
) -> tuple[bool, str]:
    """
    Q4: Does the manifest's arc_type match a registered template?
    Does the template handle all arc stages in the manifest?

    Returns (passed, violation_or_ok).
    """
    templates = registry if registry is not None else DEFAULT_ARC_TEMPLATES
    if arc_type not in templates:
        available = sorted(templates.keys())
        return False, f"TEMPLATE_NOT_FOUND(arc_type={arc_type},available={available})"

    covered, missing = check_arc_stage_coverage(arc_type, beats, registry)
    if not covered:
        return False, f"ARC_STAGES_UNSUPPORTED(missing={missing})"
    return True, "OK"


# ---------------------------------------------------------------------------
# Q5 — Render Budget
# ---------------------------------------------------------------------------


def check_render_budget(
    quality_tier: str, review_approved: bool = False
) -> tuple[bool, str]:
    """
    Q5: For final quality, has a review render been approved first?

    Final renders take 4× longer and produce large files. Never render
    at final quality without prior review approval.

    Returns (passed, violation_or_ok).
    """
    if quality_tier not in VALID_QUALITY_TIERS:
        return False, f"INVALID_TIER({quality_tier})"
    if quality_tier == "final" and not review_approved:
        return False, "FINAL_WITHOUT_REVIEW"
    return True, "OK"


# ---------------------------------------------------------------------------
# Gate K Runner
# ---------------------------------------------------------------------------


def run_gate_k(
    manifest: dict,
    quality_tier: str,
    voiceover_duration_sec: Optional[float] = None,
    music_duration_sec: Optional[float] = None,
    operator_approved_gaps: bool = False,
    review_approved: bool = False,
    registry: Optional[dict] = None,
) -> dict:
    """
    Run all 5 Gate K questions. Returns gate result dict.

    Args:
        manifest: The Remotion Video Manifest (DEP-VID-002).
        quality_tier: Target quality tier (preview/review/final).
        voiceover_duration_sec: Voiceover track duration (None if unknown).
        music_duration_sec: Music track duration (None if unknown).
        operator_approved_gaps: True if operator approved rendering with gaps.
        review_approved: True if a review-quality render was already approved.
        registry: Optional arc template registry override.
    """
    status = manifest.get("status", "")
    beats = manifest.get("beats", [])
    arc_type = manifest.get("arc_type", "")
    duration = manifest.get("total_duration_sec", 0.0)

    q1_pass, q1_detail = check_manifest_completeness(status, operator_approved_gaps)
    q2_pass, q2_detail = check_asset_accessibility(beats)
    q3_pass, q3_detail = check_audio_video_duration(
        duration, voiceover_duration_sec, music_duration_sec
    )
    q4_pass, q4_detail = check_template_compatibility(arc_type, beats, registry)
    q5_pass, q5_detail = check_render_budget(quality_tier, review_approved)

    results = [
        {"question": 1, "name": "manifest_completeness", "passed": q1_pass, "detail": q1_detail},
        {"question": 2, "name": "asset_accessibility", "passed": q2_pass, "detail": q2_detail},
        {"question": 3, "name": "audio_video_duration", "passed": q3_pass, "detail": q3_detail},
        {"question": 4, "name": "template_compatibility", "passed": q4_pass, "detail": q4_detail},
        {"question": 5, "name": "render_budget", "passed": q5_pass, "detail": q5_detail},
    ]

    all_passed = all(r["passed"] for r in results)

    if not all_passed:
        failed = [r for r in results if not r["passed"]]
        logger.warning(
            "Gate K FAILED — %d violation(s): %s",
            len(failed),
            [f"Q{r['question']}:{r['detail']}" for r in failed],
        )

    return {
        "gate": "K",
        "passed": all_passed,
        "results": results,
    }
