"""
Tests for gates/gate_k.py — FR-VID-08 Gate K Pre-Render Constraint Network.

5 questions × pass + fail scenarios = comprehensive gate coverage.
"""

import pytest

from gates.gate_k import (
    check_asset_accessibility,
    check_audio_video_duration,
    check_manifest_completeness,
    check_render_budget,
    check_template_compatibility,
    run_gate_k,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_manifest(
    arc_type="Witness",
    status="ASSEMBLED",
    beats=None,
    total_duration_sec=60.0,
):
    if beats is None:
        beats = [
            {
                "beat_index": 0,
                "arc_stage": "hook",
                "asset_status": "RESOLVED",
                "video_clip_url": "https://cdn.example.com/beat0.mp4",
                "fallback_image_url": None,
            },
            {
                "beat_index": 1,
                "arc_stage": "build",
                "asset_status": "RESOLVED",
                "video_clip_url": "https://cdn.example.com/beat1.mp4",
                "fallback_image_url": None,
            },
            {
                "beat_index": 2,
                "arc_stage": "climax",
                "asset_status": "RESOLVED",
                "video_clip_url": "https://cdn.example.com/beat2.mp4",
                "fallback_image_url": None,
            },
        ]
    return {
        "manifest_id": "MAN-VID-20260321-001",
        "project_id": "03_50-12",
        "arc_type": arc_type,
        "fps": 24,
        "total_frames": 1440,
        "total_duration_sec": total_duration_sec,
        "beats": beats,
        "audio": {
            "voiceover_path": "/audio/vo.mp3",
            "music_path": "/audio/music.mp3",
        },
        "status": status,
    }


# ---------------------------------------------------------------------------
# TestGateKQ1ManifestCompleteness
# ---------------------------------------------------------------------------


class TestGateKQ1ManifestCompleteness:
    """Q1: Manifest status must be ASSEMBLED."""

    def test_assembled_passes(self):
        passed, detail = check_manifest_completeness("ASSEMBLED")
        assert passed is True
        assert detail == "OK"

    def test_assembled_with_gaps_fails(self):
        passed, detail = check_manifest_completeness("ASSEMBLED_WITH_GAPS")
        assert passed is False
        assert detail == "MANIFEST_INCOMPLETE"

    def test_gaps_approved_passes(self):
        passed, detail = check_manifest_completeness(
            "ASSEMBLED_WITH_GAPS", operator_approved_gaps=True
        )
        assert passed is True
        assert "APPROVED" in detail

    def test_invalid_status_fails(self):
        passed, detail = check_manifest_completeness("DRAFT")
        assert passed is False
        assert "INVALID" in detail


# ---------------------------------------------------------------------------
# TestGateKQ2AssetAccessibility
# ---------------------------------------------------------------------------


class TestGateKQ2AssetAccessibility:
    """Q2: All video clip URLs must be present for RESOLVED beats."""

    def test_all_resolved_passes(self):
        beats = [
            {"beat_index": 0, "asset_status": "RESOLVED", "video_clip_url": "https://a.com/0.mp4"},
            {"beat_index": 1, "asset_status": "RESOLVED", "video_clip_url": "https://a.com/1.mp4"},
        ]
        passed, detail = check_asset_accessibility(beats)
        assert passed is True

    def test_missing_video_url_fails(self):
        beats = [
            {"beat_index": 0, "asset_status": "RESOLVED", "video_clip_url": None},
        ]
        passed, detail = check_asset_accessibility(beats)
        assert passed is False
        assert "beat_0" in detail

    def test_ken_burns_with_fallback_passes(self):
        beats = [
            {"beat_index": 0, "asset_status": "KEN_BURNS_FALLBACK",
             "video_clip_url": None, "fallback_image_url": "https://a.com/img.jpg"},
        ]
        passed, detail = check_asset_accessibility(beats)
        assert passed is True

    def test_ken_burns_without_fallback_fails(self):
        beats = [
            {"beat_index": 0, "asset_status": "KEN_BURNS_FALLBACK",
             "video_clip_url": None, "fallback_image_url": None},
        ]
        passed, detail = check_asset_accessibility(beats)
        assert passed is False
        assert "fallback_image" in detail

    def test_asset_missing_fails(self):
        beats = [
            {"beat_index": 3, "asset_status": "ASSET_MISSING", "video_clip_url": None},
        ]
        passed, detail = check_asset_accessibility(beats)
        assert passed is False
        assert "beat_3_asset_missing" in detail


# ---------------------------------------------------------------------------
# TestGateKQ3AudioVideoDuration
# ---------------------------------------------------------------------------


class TestGateKQ3AudioVideoDuration:
    """Q3: Voiceover ≈ manifest ±0.5s, music ≥ manifest."""

    def test_matching_durations_pass(self):
        passed, detail = check_audio_video_duration(60.0, 60.0, 65.0)
        assert passed is True

    def test_voiceover_within_tolerance_passes(self):
        passed, detail = check_audio_video_duration(60.0, 60.4, 65.0)
        assert passed is True

    def test_voiceover_outside_tolerance_fails(self):
        passed, detail = check_audio_video_duration(60.0, 62.0, 65.0)
        assert passed is False
        assert "VOICEOVER_MISMATCH" in detail

    def test_music_too_short_fails(self):
        passed, detail = check_audio_video_duration(60.0, 60.0, 55.0)
        assert passed is False
        assert "MUSIC_TOO_SHORT" in detail

    def test_none_durations_pass(self):
        """If durations are not provided, skip those checks."""
        passed, detail = check_audio_video_duration(60.0, None, None)
        assert passed is True

    def test_both_violations(self):
        passed, detail = check_audio_video_duration(60.0, 70.0, 50.0)
        assert passed is False
        assert "VOICEOVER_MISMATCH" in detail
        assert "MUSIC_TOO_SHORT" in detail


# ---------------------------------------------------------------------------
# TestGateKQ4TemplateCompatibility
# ---------------------------------------------------------------------------


class TestGateKQ4TemplateCompatibility:
    """Q4: Arc type must be registered and cover all manifest arc stages."""

    def test_known_arc_type_passes(self):
        beats = [{"arc_stage": "hook"}, {"arc_stage": "build"}, {"arc_stage": "climax"}]
        passed, detail = check_template_compatibility("Witness", beats)
        assert passed is True

    def test_unknown_arc_type_fails(self):
        passed, detail = check_template_compatibility("Nonexistent", [])
        assert passed is False
        assert "TEMPLATE_NOT_FOUND" in detail

    def test_missing_arc_stages_fails(self):
        beats = [{"arc_stage": "hook"}, {"arc_stage": "brand_new_stage"}]
        passed, detail = check_template_compatibility("Witness", beats)
        assert passed is False
        assert "ARC_STAGES_UNSUPPORTED" in detail

    def test_all_three_arc_types(self):
        for arc in ["Witness", "Breakthrough", "Call-to-Adventure"]:
            passed, detail = check_template_compatibility(arc, [])
            assert passed is True, f"Arc type {arc} should be registered"


# ---------------------------------------------------------------------------
# TestGateKQ5RenderBudget
# ---------------------------------------------------------------------------


class TestGateKQ5RenderBudget:
    """Q5: Final requires prior review approval."""

    def test_preview_passes(self):
        passed, detail = check_render_budget("preview")
        assert passed is True

    def test_review_passes(self):
        passed, detail = check_render_budget("review")
        assert passed is True

    def test_final_without_review_fails(self):
        passed, detail = check_render_budget("final", review_approved=False)
        assert passed is False
        assert "FINAL_WITHOUT_REVIEW" in detail

    def test_final_with_review_passes(self):
        passed, detail = check_render_budget("final", review_approved=True)
        assert passed is True

    def test_invalid_tier_fails(self):
        passed, detail = check_render_budget("ultra")
        assert passed is False
        assert "INVALID_TIER" in detail


# ---------------------------------------------------------------------------
# TestGateKRunner
# ---------------------------------------------------------------------------


class TestGateKRunner:
    """Full Gate K runner — all 5 questions."""

    def test_all_pass(self):
        manifest = _make_manifest()
        result = run_gate_k(
            manifest,
            quality_tier="review",
            voiceover_duration_sec=60.0,
            music_duration_sec=65.0,
        )
        assert result["gate"] == "K"
        assert result["passed"] is True
        assert len(result["results"]) == 5
        assert all(r["passed"] for r in result["results"])

    def test_single_failure(self):
        manifest = _make_manifest(status="ASSEMBLED_WITH_GAPS")
        result = run_gate_k(manifest, quality_tier="review")
        assert result["passed"] is False
        q1 = result["results"][0]
        assert q1["question"] == 1
        assert q1["passed"] is False

    def test_multiple_failures(self):
        manifest = _make_manifest(
            arc_type="Nonexistent",
            status="ASSEMBLED_WITH_GAPS",
        )
        result = run_gate_k(
            manifest,
            quality_tier="final",
            voiceover_duration_sec=100.0,
            music_duration_sec=30.0,
        )
        assert result["passed"] is False
        failed_qs = [r["question"] for r in result["results"] if not r["passed"]]
        # Q1 (gaps), Q3 (voiceover + music), Q4 (template), Q5 (final w/o review)
        assert 1 in failed_qs
        assert 3 in failed_qs
        assert 4 in failed_qs
        assert 5 in failed_qs

    def test_final_with_all_approvals(self):
        manifest = _make_manifest()
        result = run_gate_k(
            manifest,
            quality_tier="final",
            voiceover_duration_sec=60.0,
            music_duration_sec=65.0,
            review_approved=True,
        )
        assert result["passed"] is True

    def test_result_structure(self):
        manifest = _make_manifest()
        result = run_gate_k(manifest, quality_tier="preview")
        assert "gate" in result
        assert "passed" in result
        assert "results" in result
        for r in result["results"]:
            assert "question" in r
            assert "name" in r
            assert "passed" in r
            assert "detail" in r
