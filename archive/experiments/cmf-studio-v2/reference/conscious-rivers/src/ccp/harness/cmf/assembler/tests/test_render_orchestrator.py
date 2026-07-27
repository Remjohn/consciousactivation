"""
Tests for render_orchestrator.py — FR-VID-08 Render Orchestration.

Covers: template resolution, quality presets, Ken Burns detection,
render job construction, render result validation, and receipt writing.
"""

import os
import tempfile

import pytest

from render_orchestrator import (
    AUDIO_VIDEO_DURATION_TOLERANCE_SEC,
    DEFAULT_ARC_TEMPLATES,
    QUALITY_PRESETS,
    VALID_QUALITY_TIERS,
    build_render_job,
    check_arc_stage_coverage,
    compute_render_efficiency,
    detect_ken_burns_beats,
    generate_render_id,
    get_composition_id,
    get_quality_preset,
    get_resolution_string,
    resolve_template,
    run_template_compile,
    run_video_render,
    validate_render_result,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_manifest(
    arc_type="Witness",
    status="ASSEMBLED",
    beats=None,
    total_frames=1440,
    total_duration_sec=60.0,
    fps=24,
):
    if beats is None:
        beats = [
            {
                "beat_index": 0,
                "arc_stage": "hook",
                "start_frame": 0,
                "duration_frames": 288,
                "asset_status": "RESOLVED",
                "video_clip_url": "https://cdn.example.com/beat0.mp4",
                "fallback_image_url": None,
            },
            {
                "beat_index": 1,
                "arc_stage": "build",
                "start_frame": 288,
                "duration_frames": 288,
                "asset_status": "RESOLVED",
                "video_clip_url": "https://cdn.example.com/beat1.mp4",
                "fallback_image_url": None,
            },
            {
                "beat_index": 2,
                "arc_stage": "climax",
                "start_frame": 576,
                "duration_frames": 288,
                "asset_status": "RESOLVED",
                "video_clip_url": "https://cdn.example.com/beat2.mp4",
                "fallback_image_url": None,
            },
        ]
    return {
        "manifest_id": "MAN-VID-20260321-001",
        "project_id": "03_50-12",
        "arc_type": arc_type,
        "fps": fps,
        "total_frames": total_frames,
        "total_duration_sec": total_duration_sec,
        "beats": beats,
        "audio": {
            "voiceover_path": "/audio/vo.mp3",
            "music_path": "/audio/music.mp3",
        },
        "status": status,
    }


def _make_render_result(status="COMPLETED", error=None):
    return {
        "render_id": "RENDER-20260321-001",
        "status": status,
        "output": {
            "file_path": "/renders/review/cmf-vid-001-review.mp4",
            "file_size_bytes": 18742300,
            "duration_sec": 60.0,
            "resolution": "720x1280",
            "fps": 24,
            "codec": "h264",
            "bitrate_kbps": 2500,
        },
        "render_stats": {
            "render_time_sec": 34.2,
            "frames_rendered": 1440,
            "frames_per_second": 42.1,
        },
        "error": error,
    }


# ---------------------------------------------------------------------------
# TestTemplateResolution
# ---------------------------------------------------------------------------


class TestTemplateResolution:
    """TD1: One composition per arc type — template resolution."""

    def test_resolve_witness(self):
        t = resolve_template("Witness")
        assert t["composition_id"] == "cmf-witness"
        assert "cmf-witness.tsx" in t["template_path"]

    def test_resolve_breakthrough(self):
        t = resolve_template("Breakthrough")
        assert t["composition_id"] == "cmf-breakthrough"

    def test_resolve_call_to_adventure(self):
        t = resolve_template("Call-to-Adventure")
        assert t["composition_id"] == "cmf-call-to-adventure"

    def test_unknown_arc_type_raises(self):
        with pytest.raises(ValueError, match="No template registered"):
            resolve_template("NonexistentArc")

    def test_custom_registry(self):
        custom = {"Custom": {"composition_id": "cmf-custom", "template_path": "custom.tsx",
                             "supported_arc_stages": ["hook"], "default_transitions": {},
                             "ken_burns_enabled": True}}
        t = resolve_template("Custom", registry=custom)
        assert t["composition_id"] == "cmf-custom"

    def test_get_composition_id(self):
        assert get_composition_id("Witness") == "cmf-witness"

    def test_returns_copy(self):
        """Ensure resolve_template returns a copy, not the original."""
        t1 = resolve_template("Witness")
        t1["composition_id"] = "modified"
        t2 = resolve_template("Witness")
        assert t2["composition_id"] == "cmf-witness"


class TestArcStageCoverage:
    """TD1: Verify template handles all arc stages in the manifest."""

    def test_all_stages_covered(self):
        beats = [{"arc_stage": "hook"}, {"arc_stage": "build"}, {"arc_stage": "climax"}]
        covered, missing = check_arc_stage_coverage("Witness", beats)
        assert covered is True
        assert missing == []

    def test_missing_stages(self):
        beats = [{"arc_stage": "hook"}, {"arc_stage": "unknown_stage"}]
        covered, missing = check_arc_stage_coverage("Witness", beats)
        assert covered is False
        assert "unknown_stage" in missing

    def test_empty_beats(self):
        covered, missing = check_arc_stage_coverage("Witness", [])
        assert covered is True
        assert missing == []

    def test_beats_without_arc_stage(self):
        beats = [{"beat_index": 0}]
        covered, missing = check_arc_stage_coverage("Witness", beats)
        assert covered is True


# ---------------------------------------------------------------------------
# TestQualityPresets
# ---------------------------------------------------------------------------


class TestQualityPresets:
    """TD3: 3-tier render quality."""

    def test_preview_preset(self):
        p = get_quality_preset("preview")
        assert p["width"] == 540
        assert p["height"] == 960
        assert p["crf"] > 25  # Lower quality

    def test_review_preset(self):
        p = get_quality_preset("review")
        assert p["width"] == 720
        assert p["height"] == 1280

    def test_final_preset(self):
        p = get_quality_preset("final")
        assert p["width"] == 1080
        assert p["height"] == 1920
        assert p["crf"] < 25  # Higher quality

    def test_invalid_tier_raises(self):
        with pytest.raises(ValueError, match="Invalid quality tier"):
            get_quality_preset("ultra")

    def test_resolution_string(self):
        assert get_resolution_string("preview") == "540x960"
        assert get_resolution_string("review") == "720x1280"
        assert get_resolution_string("final") == "1080x1920"

    def test_quality_tiers_ascending_bitrate(self):
        """Preview < review < final bitrate."""
        assert (
            QUALITY_PRESETS["preview"]["bitrate_kbps"]
            < QUALITY_PRESETS["review"]["bitrate_kbps"]
            < QUALITY_PRESETS["final"]["bitrate_kbps"]
        )

    def test_quality_tiers_ascending_resolution(self):
        """Preview < review < final width."""
        assert (
            QUALITY_PRESETS["preview"]["width"]
            < QUALITY_PRESETS["review"]["width"]
            < QUALITY_PRESETS["final"]["width"]
        )


# ---------------------------------------------------------------------------
# TestKenBurnsDetection
# ---------------------------------------------------------------------------


class TestKenBurnsDetection:
    """TD2: Ken Burns fallback for static images."""

    def test_no_ken_burns(self):
        beats = [
            {"beat_index": 0, "asset_status": "RESOLVED", "video_clip_url": "https://a.com/v.mp4", "fallback_image_url": None},
        ]
        assert detect_ken_burns_beats(beats) == []

    def test_ken_burns_by_status(self):
        beats = [
            {"beat_index": 0, "asset_status": "KEN_BURNS_FALLBACK", "video_clip_url": None, "fallback_image_url": "https://a.com/img.jpg"},
            {"beat_index": 1, "asset_status": "RESOLVED", "video_clip_url": "https://a.com/v.mp4", "fallback_image_url": None},
        ]
        assert detect_ken_burns_beats(beats) == [0]

    def test_ken_burns_by_missing_video(self):
        beats = [
            {"beat_index": 0, "asset_status": "RESOLVED", "video_clip_url": None, "fallback_image_url": "https://a.com/img.jpg"},
        ]
        assert detect_ken_burns_beats(beats) == [0]

    def test_ken_burns_multiple(self):
        beats = [
            {"beat_index": 0, "asset_status": "KEN_BURNS_FALLBACK", "video_clip_url": None, "fallback_image_url": "https://a.com/0.jpg"},
            {"beat_index": 1, "asset_status": "RESOLVED", "video_clip_url": "https://a.com/1.mp4", "fallback_image_url": None},
            {"beat_index": 2, "asset_status": "KEN_BURNS_FALLBACK", "video_clip_url": None, "fallback_image_url": "https://a.com/2.jpg"},
        ]
        assert detect_ken_burns_beats(beats) == [0, 2]

    def test_ac5_ken_burns_fallback(self):
        """AC5: Beat 5 with static image renders with Ken Burns fallback."""
        beats = [
            {"beat_index": i, "asset_status": "RESOLVED", "video_clip_url": f"https://a.com/{i}.mp4", "fallback_image_url": None}
            for i in range(12)
        ]
        beats[5] = {
            "beat_index": 5,
            "asset_status": "KEN_BURNS_FALLBACK",
            "video_clip_url": None,
            "fallback_image_url": "https://a.com/5_fallback.jpg",
        }
        kb = detect_ken_burns_beats(beats)
        assert 5 in kb
        assert len(kb) == 1


# ---------------------------------------------------------------------------
# TestRenderJobConstruction
# ---------------------------------------------------------------------------


class TestRenderJobConstruction:
    """§4 Stage 2: Render job construction."""

    def test_build_preview_job(self):
        manifest = _make_manifest()
        job = build_render_job(manifest, "preview", "PIPE-001")
        assert job["quality_tier"] == "preview"
        assert job["composition_id"] == "cmf-witness"
        assert job["resolution"] == "540x960"
        assert job["status"] == "PENDING"
        assert job["beat_count"] == 3

    def test_build_review_job(self):
        manifest = _make_manifest()
        job = build_render_job(manifest, "review", "PIPE-001")
        assert job["resolution"] == "720x1280"

    def test_final_requires_review_approval(self):
        manifest = _make_manifest()
        with pytest.raises(ValueError, match="prior review approval"):
            build_render_job(manifest, "final", "PIPE-001")

    def test_final_with_review_approval(self):
        manifest = _make_manifest()
        job = build_render_job(manifest, "final", "PIPE-001", operator_approved_review=True)
        assert job["quality_tier"] == "final"
        assert job["resolution"] == "1080x1920"

    def test_render_id_format(self):
        rid = generate_render_id()
        assert rid.startswith("RENDER-")
        parts = rid.split("-")
        assert len(parts) == 3
        assert len(parts[1]) == 8  # YYYYMMDD
        assert len(parts[2]) == 3  # NNN

    def test_ken_burns_beats_in_job(self):
        beats = [
            {"beat_index": 0, "arc_stage": "hook", "asset_status": "RESOLVED",
             "video_clip_url": "https://a.com/0.mp4", "fallback_image_url": None,
             "start_frame": 0, "duration_frames": 288},
            {"beat_index": 1, "arc_stage": "build", "asset_status": "KEN_BURNS_FALLBACK",
             "video_clip_url": None, "fallback_image_url": "https://a.com/1.jpg",
             "start_frame": 288, "duration_frames": 288},
        ]
        manifest = _make_manifest(beats=beats)
        job = build_render_job(manifest, "preview", "PIPE-001")
        assert job["ken_burns_beats"] == [1]

    def test_ac1_12_beat_composition(self):
        """AC1: 12-beat composition with correct start_frame and duration."""
        beats = [
            {
                "beat_index": i,
                "arc_stage": ["hook", "build", "rising", "climax", "resolution"][i % 5],
                "start_frame": i * 120,
                "duration_frames": 120,
                "asset_status": "RESOLVED",
                "video_clip_url": f"https://cdn.example.com/beat{i}.mp4",
                "fallback_image_url": None,
            }
            for i in range(12)
        ]
        manifest = _make_manifest(beats=beats, total_frames=1440)
        job = build_render_job(manifest, "review", "PIPE-001")
        assert job["beat_count"] == 12
        assert job["total_frames"] == 1440


# ---------------------------------------------------------------------------
# TestRenderResultValidation
# ---------------------------------------------------------------------------


class TestRenderResultValidation:
    """§5: Render result processing."""

    def test_valid_result(self):
        result = _make_render_result()
        valid, errors = validate_render_result(result)
        assert valid is True
        assert errors == []

    def test_failed_status(self):
        result = _make_render_result(status="FAILED")
        valid, errors = validate_render_result(result)
        assert valid is False
        assert any("COMPLETED" in e for e in errors)

    def test_missing_file_path(self):
        result = _make_render_result()
        result["output"]["file_path"] = ""
        valid, errors = validate_render_result(result)
        assert valid is False
        assert any("file_path" in e for e in errors)

    def test_zero_file_size(self):
        result = _make_render_result()
        result["output"]["file_size_bytes"] = 0
        valid, errors = validate_render_result(result)
        assert valid is False

    def test_error_present(self):
        result = _make_render_result(error="FFmpeg encoding failed")
        valid, errors = validate_render_result(result)
        assert valid is False
        assert any("error" in e.lower() for e in errors)

    def test_render_efficiency(self):
        result = _make_render_result()
        # frames_per_second=42.1, fps=24 → 42.1/24 ≈ 1.75
        eff = compute_render_efficiency(result)
        assert eff is not None
        assert eff > 1.0  # Faster than real-time

    def test_render_efficiency_missing_data(self):
        assert compute_render_efficiency({}) is None

    def test_ac4_quality_tiers_produce_different_sizes(self):
        """AC4: file sizes increase with quality tier (preview < review < final)."""
        for tier in ["preview", "review", "final"]:
            preset = get_quality_preset(tier)
            assert preset["bitrate_kbps"] > 0
        assert (
            QUALITY_PRESETS["preview"]["bitrate_kbps"]
            < QUALITY_PRESETS["review"]["bitrate_kbps"]
            < QUALITY_PRESETS["final"]["bitrate_kbps"]
        )


# ---------------------------------------------------------------------------
# TestReceiptWriting
# ---------------------------------------------------------------------------


class TestReceiptWriting:
    """Stage receipts: TEMPLATE_COMPILE and VIDEO_RENDER."""

    def test_template_compile_receipt(self):
        manifest = _make_manifest()
        with tempfile.TemporaryDirectory() as tmpdir:
            out = run_template_compile(manifest, output_dir=tmpdir)
            assert out["receipt"]["stage_name"] == "TEMPLATE_COMPILE"
            assert out["receipt"]["agent_name"] == "template_developer"
            assert out["result"]["composition_id"] == "cmf-witness"
            assert out["result"]["arc_stage_coverage"] is True

    def test_template_compile_missing_stages(self):
        beats = [{"arc_stage": "hook"}, {"arc_stage": "nonexistent"}]
        manifest = _make_manifest(beats=beats)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = run_template_compile(manifest, output_dir=tmpdir)
            assert out["result"]["arc_stage_coverage"] is False
            assert "nonexistent" in out["result"]["missing_arc_stages"]

    def test_video_render_receipt(self):
        manifest = _make_manifest()
        result = _make_render_result()
        with tempfile.TemporaryDirectory() as tmpdir:
            out = run_video_render(
                manifest, "review", "PIPE-001", result, output_dir=tmpdir
            )
            assert out["receipt"]["stage_name"] == "VIDEO_RENDER"
            assert out["receipt"]["agent_name"] == "remotion_render_server"
            assert out["result"]["valid"] is True
            assert out["result"]["render_efficiency"] is not None

    def test_video_render_receipt_failed(self):
        manifest = _make_manifest()
        result = _make_render_result(status="FAILED")
        with tempfile.TemporaryDirectory() as tmpdir:
            out = run_video_render(
                manifest, "review", "PIPE-001", result, output_dir=tmpdir
            )
            assert out["result"]["valid"] is False
            assert len(out["result"]["validation_errors"]) > 0
