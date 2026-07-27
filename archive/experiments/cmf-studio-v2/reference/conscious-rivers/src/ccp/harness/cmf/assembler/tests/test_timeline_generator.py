"""
Timeline Generator & Gate E Test Suite — FR-VID-01

Tests asset URL resolution, manifest assembly, partial manifest update,
ducking curve embedding, URL sanitization, and Gate E (5 questions).

Maps to FR-VID-01 §9 AC4-AC5, §6 Gate E, §11 Testing Strategy.
"""

import copy
import tempfile
from math import ceil
from pathlib import Path

from timeline_generator import (
    sanitize_url,
    resolve_asset_urls,
    validate_ducking_curve,
    assemble_manifest,
    update_manifest_beats,
    run_asset_resolution,
    run_manifest_assembly,
)
from gates.gate_e import (
    check_frame_count_continuity,
    check_asset_completeness,
    check_audio_beat_alignment,
    check_transition_budget,
    check_arc_stage_sequence,
    run_gate_e,
)
from beat_cluster_parser import (
    parse_beat_cluster,
    load_transition_presets,
)


# ===================================================================
# Helpers
# ===================================================================


def _make_parsed_beat(index, duration_sec, arc_stage="hook",
                      beat_type="hook", fps=24):
    frames = ceil(duration_sec * fps)
    return {
        "beat_index": index,
        "beat_type": beat_type,
        "arc_stage": arc_stage,
        "duration_sec": duration_sec,
        "duration_frames": frames,
        "start_frame": 0,  # Caller will fix start_frame
        "visual_prompt_ref": f"prompt-{index}",
        "narration_text": f"Beat {index} narration.",
        "transition": {
            "preset_id": f"TR-{arc_stage.upper()}",
            "type": "crossfade",
            "duration_frames": 12,
        },
    }


def _build_beats(count=5, fps=24):
    durations = [4.0, 3.5, 5.0, 2.5, 3.0]
    stages = ["opening", "hook", "rising_action", "tension", "climax"]
    beats = []
    start = 0
    for i in range(count):
        d = durations[i % len(durations)]
        b = _make_parsed_beat(i, d, stages[i % len(stages)], fps=fps)
        b["start_frame"] = start
        start += b["duration_frames"]
        beats.append(b)
    return beats


def _make_fingerprint_map(beats, missing_indices=None):
    """Create a fingerprint map in the DEP-VID-014 format expected by resolve_asset_urls."""
    missing_indices = missing_indices or []
    fingerprints = []
    for b in beats:
        idx = b["beat_index"]
        if idx in missing_indices:
            fingerprints.append({
                "beat_index": idx,
                "fingerprint": {
                    "fingerprint_id": f"FP-{idx:04d}",
                    "stage_1_t2i": {"status": "PENDING"},
                    "stage_2_i2v": {"status": "PENDING"},
                },
            })
        else:
            fingerprints.append({
                "beat_index": idx,
                "fingerprint": {
                    "fingerprint_id": f"FP-{idx:04d}",
                    "stage_1_t2i": {
                        "status": "GENERATED",
                        "output_image_url": f"https://cdn.example.com/images/beat-{idx}.png",
                    },
                    "stage_2_i2v": {
                        "status": "GENERATED",
                        "output_video_url": f"https://cdn.example.com/clips/beat-{idx}.mp4",
                    },
                },
            })
    return {"fingerprints": fingerprints}


def _make_fingerprint_map_image_only(beat_index):
    """Fingerprint entry with image but no video — triggers KEN_BURNS_FALLBACK."""
    return {
        "fingerprints": [{
            "beat_index": beat_index,
            "fingerprint": {
                "fingerprint_id": f"FP-{beat_index:04d}",
                "stage_1_t2i": {
                    "status": "GENERATED",
                    "output_image_url": f"https://cdn.example.com/images/beat-{beat_index}.png",
                },
                "stage_2_i2v": {"status": "PENDING"},
            },
        }],
    }


def _make_ducking_curve(total_frames):
    """Generate a valid ducking curve of the right length."""
    return [0.5] * total_frames


def _make_full_parsed_result(beats=None, fps=24):
    """Build a minimal parse_beat_cluster result."""
    beats = beats or _build_beats()
    total = sum(b["duration_frames"] for b in beats)
    total_dur = sum(b["duration_sec"] for b in beats)
    return {
        "status": "PARSED",
        "beat_cluster_id": "BC-WITNESS-42",
        "arc_type": "witness",
        "project_id": "03_50-12",
        "fps": fps,
        "total_frames": total,
        "total_duration_sec": total_dur,
        "beats": beats,
        "warnings": [],
    }


# ===================================================================
# URL Sanitization
# ===================================================================


class TestURLSanitization:
    def test_valid_https_url(self):
        url = "https://cdn.example.com/clips/beat-0.mp4"
        assert sanitize_url(url) == url

    def test_reject_javascript_uri(self):
        assert sanitize_url("javascript:alert(1)") is None

    def test_reject_http(self):
        assert sanitize_url("http://insecure.com/clip.mp4") is None

    def test_reject_data_uri(self):
        assert sanitize_url("data:text/html,<h1>evil</h1>") is None

    def test_none_input(self):
        assert sanitize_url(None) is None

    def test_empty_string(self):
        assert sanitize_url("") is None

    def test_reject_ftp(self):
        assert sanitize_url("ftp://files.example.com/video.mp4") is None


# ===================================================================
# Asset Resolution — AC4
# ===================================================================


class TestAssetResolution:
    def test_all_assets_resolved(self):
        beats = _build_beats()
        fp_map = _make_fingerprint_map(beats)
        resolved = resolve_asset_urls(beats, fp_map)
        for b in resolved:
            assert b["asset_status"] == "RESOLVED"
            assert b["video_clip_url"].startswith("https://")

    def test_ac4_missing_assets(self):
        """AC4: beat 3 has no assets → ASSET_MISSING."""
        beats = _build_beats()
        fp_map = _make_fingerprint_map(beats, missing_indices=[3])
        resolved = resolve_asset_urls(beats, fp_map)
        assert resolved[3]["asset_status"] == "ASSET_MISSING"
        for i in [0, 1, 2, 4]:
            assert resolved[i]["asset_status"] == "RESOLVED"

    def test_ken_burns_fallback(self):
        """If video missing but image exists, use KEN_BURNS_FALLBACK."""
        beats = _build_beats(count=1)
        fp_map = _make_fingerprint_map_image_only(0)
        resolved = resolve_asset_urls(beats, fp_map)
        assert resolved[0]["asset_status"] == "KEN_BURNS_FALLBACK"


# ===================================================================
# Ducking Curve — AC5
# ===================================================================


class TestDuckingCurve:
    def test_ac5_valid_1440_curve(self):
        """AC5: 1440-value ducking curve, all values in [0.0, 1.0]."""
        curve = [0.5] * 1440
        valid, msg = validate_ducking_curve(curve, 1440)
        assert valid
        assert msg == ""

    def test_wrong_length(self):
        curve = [0.5] * 100
        valid, msg = validate_ducking_curve(curve, 1440)
        assert not valid

    def test_out_of_range_values(self):
        curve = [1.5] * 1440
        valid, msg = validate_ducking_curve(curve, 1440)
        assert not valid

    def test_negative_values(self):
        curve = [-0.1] * 1440
        valid, msg = validate_ducking_curve(curve, 1440)
        assert not valid


# ===================================================================
# Manifest Assembly
# ===================================================================


class TestManifestAssembly:
    def test_assembled_status(self):
        beats = _build_beats()
        fp_map = _make_fingerprint_map(beats)
        resolved = resolve_asset_urls(beats, fp_map)
        parsed = _make_full_parsed_result(beats)
        curve = _make_ducking_curve(parsed["total_frames"])
        manifest = assemble_manifest(parsed, resolved, ducking_curve=curve)
        assert manifest["status"] == "ASSEMBLED"
        assert manifest["total_frames"] == parsed["total_frames"]

    def test_assembled_with_gaps(self):
        """AC4: any ASSET_MISSING → status must be ASSEMBLED_WITH_GAPS."""
        beats = _build_beats()
        fp_map = _make_fingerprint_map(beats, missing_indices=[2])
        resolved = resolve_asset_urls(beats, fp_map)
        parsed = _make_full_parsed_result(beats)
        curve = _make_ducking_curve(parsed["total_frames"])
        manifest = assemble_manifest(parsed, resolved, ducking_curve=curve)
        assert manifest["status"] == "ASSEMBLED_WITH_GAPS"

    def test_ducking_curve_embedded(self):
        beats = _build_beats()
        fp_map = _make_fingerprint_map(beats)
        resolved = resolve_asset_urls(beats, fp_map)
        parsed = _make_full_parsed_result(beats)
        curve = _make_ducking_curve(parsed["total_frames"])
        manifest = assemble_manifest(parsed, resolved, ducking_curve=curve)
        assert manifest["audio"]["ducking_curve"] == curve
        assert len(manifest["audio"]["ducking_curve"]) == parsed["total_frames"]

    def test_manifest_beat_fields(self):
        beats = _build_beats(count=2)
        fp_map = _make_fingerprint_map(beats)
        resolved = resolve_asset_urls(beats, fp_map)
        parsed = _make_full_parsed_result(beats)
        curve = _make_ducking_curve(parsed["total_frames"])
        manifest = assemble_manifest(parsed, resolved, ducking_curve=curve)
        for mb in manifest["beats"]:
            assert "beat_index" in mb
            assert "start_frame" in mb
            assert "duration_frames" in mb
            assert "transition" in mb


# ===================================================================
# Partial Manifest Update — §3 TD5
# ===================================================================


class TestPartialManifestUpdate:
    def test_update_single_beat(self):
        beats = _build_beats()
        fp_map = _make_fingerprint_map(beats)
        resolved = resolve_asset_urls(beats, fp_map)
        parsed = _make_full_parsed_result(beats)
        curve = _make_ducking_curve(parsed["total_frames"])
        manifest = assemble_manifest(parsed, resolved, ducking_curve=curve)

        # Regenerate beat 2 with new fingerprint entry
        updated_entry = {
            "beat_index": 2,
            "fingerprint": {
                "fingerprint_id": "FP-0002-v2",
                "stage_1_t2i": {
                    "status": "GENERATED",
                    "output_image_url": "https://cdn.example.com/images/beat-2-v2.png",
                },
                "stage_2_i2v": {
                    "status": "GENERATED",
                    "output_video_url": "https://cdn.example.com/clips/beat-2-v2.mp4",
                },
            },
        }

        updated = update_manifest_beats(manifest, [updated_entry])
        assert updated["beats"][2]["video_clip_url"].endswith("-v2.mp4")
        assert updated["beats"][2]["fingerprint_id"] == "FP-0002-v2"
        # Other beats untouched
        assert updated["beats"][0]["video_clip_url"] == manifest["beats"][0]["video_clip_url"]


# ===================================================================
# Gate E — §6 (5 Questions)
# ===================================================================


class TestGateEQ1FrameCountContinuity:
    def test_valid_frame_count(self):
        beats = _build_beats()
        parsed = _make_full_parsed_result(beats)
        ok, msg = check_frame_count_continuity(parsed["beats"], parsed["total_frames"])
        assert ok, msg

    def test_mismatch_frame_count(self):
        beats = _build_beats()
        parsed = _make_full_parsed_result(beats)
        ok, msg = check_frame_count_continuity(parsed["beats"], parsed["total_frames"] + 100)
        assert not ok


class TestGateEQ2AssetCompleteness:
    def test_all_resolved(self):
        beats = _build_beats()
        fp_map = _make_fingerprint_map(beats)
        resolved = resolve_asset_urls(beats, fp_map)
        parsed = _make_full_parsed_result(beats)
        curve = _make_ducking_curve(parsed["total_frames"])
        manifest = assemble_manifest(parsed, resolved, ducking_curve=curve)
        ok, msg = check_asset_completeness(manifest["beats"], manifest["status"])
        assert ok, msg

    def test_missing_asset_detected(self):
        beats = _build_beats()
        fp_map = _make_fingerprint_map(beats, missing_indices=[1])
        resolved = resolve_asset_urls(beats, fp_map)
        parsed = _make_full_parsed_result(beats)
        curve = _make_ducking_curve(parsed["total_frames"])
        manifest = assemble_manifest(parsed, resolved, ducking_curve=curve)
        # Force wrong status to trigger Gate failure
        ok, msg = check_asset_completeness(manifest["beats"], "ASSEMBLED")
        assert not ok


class TestGateEQ3AudioBeatAlignment:
    def test_matching_curve(self):
        beats = _build_beats()
        parsed = _make_full_parsed_result(beats)
        total = parsed["total_frames"]
        ok, msg = check_audio_beat_alignment(total, total)
        assert ok, msg

    def test_wrong_length_curve(self):
        ok, msg = check_audio_beat_alignment(10, 1440)
        assert not ok


class TestGateEQ4TransitionBudget:
    def test_valid_transitions(self):
        beats = _build_beats()
        ok, msg = check_transition_budget(beats)
        assert ok, msg

    def test_excessive_transition(self):
        beats = _build_beats()
        # Make transition longer than 50% of beat
        beats[0]["transition"]["duration_frames"] = beats[0]["duration_frames"]
        ok, msg = check_transition_budget(beats)
        assert not ok


class TestGateEQ5ArcStageSequence:
    def test_valid_witness_sequence(self):
        """Valid witness arc sequence passes."""
        beats = _build_beats()
        presets = load_transition_presets()
        arc_sequences = presets.get("arc_sequences", {})
        ok, msg = check_arc_stage_sequence(beats, "witness", arc_sequences)
        assert ok, msg

    def test_invalid_sequence(self):
        """Swapping arc stages to break order."""
        beats = _build_beats()
        beats[0]["arc_stage"] = "resolution"
        beats[4]["arc_stage"] = "opening"
        presets = load_transition_presets()
        arc_sequences = presets.get("arc_sequences", {})
        ok, msg = check_arc_stage_sequence(beats, "witness", arc_sequences)
        assert not ok


class TestGateERunner:
    def test_all_pass(self):
        beats = _build_beats()
        fp_map = _make_fingerprint_map(beats)
        resolved = resolve_asset_urls(beats, fp_map)
        parsed = _make_full_parsed_result(beats)
        curve = _make_ducking_curve(parsed["total_frames"])
        manifest = assemble_manifest(parsed, resolved, ducking_curve=curve)
        presets = load_transition_presets()
        arc_sequences = presets.get("arc_sequences", {})
        result = run_gate_e(
            manifest["beats"],
            manifest["total_frames"],
            manifest["status"],
            len(manifest["audio"]["ducking_curve"]),
            parsed["arc_type"],
            arc_sequences,
        )
        assert result["gate"] == "E"
        assert result["passed"] is True
        assert len(result["results"]) == 5

    def test_fail_on_violation(self):
        beats = _build_beats()
        fp_map = _make_fingerprint_map(beats, missing_indices=[0, 1, 2])
        resolved = resolve_asset_urls(beats, fp_map)
        parsed = _make_full_parsed_result(beats)
        curve = _make_ducking_curve(parsed["total_frames"])
        manifest = assemble_manifest(parsed, resolved, ducking_curve=curve)
        presets = load_transition_presets()
        arc_sequences = presets.get("arc_sequences", {})
        # Force status mismatch: manifest has ASSEMBLED_WITH_GAPS but we say ASSEMBLED
        result = run_gate_e(
            manifest["beats"],
            manifest["total_frames"],
            "ASSEMBLED",  # Wrong: should be ASSEMBLED_WITH_GAPS
            len(manifest["audio"]["ducking_curve"]),
            parsed["arc_type"],
            arc_sequences,
        )
        assert result["passed"] is False


# ===================================================================
# Pipeline — Receipt Chain
# ===================================================================


class TestTimelineGeneratorPipeline:
    def test_asset_resolution_receipt(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            beats = _build_beats()
            fp_map = _make_fingerprint_map(beats)
            result, receipt = run_asset_resolution(beats, fp_map, receipt_output_dir=tmpdir)
            assert receipt["stage_name"] == "ASSET_RESOLUTION"
            assert receipt["agent_name"] == "timeline_generator"

    def test_manifest_assembly_receipt(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            beats = _build_beats()
            fp_map = _make_fingerprint_map(beats)
            resolved = resolve_asset_urls(beats, fp_map)
            parsed = _make_full_parsed_result(beats)
            curve = _make_ducking_curve(parsed["total_frames"])
            manifest, receipt = run_manifest_assembly(
                parsed, resolved, ducking_curve=curve,
                receipt_output_dir=tmpdir,
            )
            assert receipt["stage_name"] == "MANIFEST_ASSEMBLY"
            assert manifest["status"] == "ASSEMBLED"

    def test_manifest_assembly_legitimacy_outputs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            beats = _build_beats()
            fp_map = _make_fingerprint_map(beats)
            resolved = resolve_asset_urls(beats, fp_map)
            parsed = _make_full_parsed_result(beats)
            curve = _make_ducking_curve(parsed["total_frames"])
            manifest, receipt = run_manifest_assembly(
                parsed, resolved, ducking_curve=curve,
                receipt_output_dir=tmpdir,
            )

            assert "constraint_manifest" in manifest
            assert "subsystem_runtime_asset" in manifest
            assert "scene_intelligence_runtime_asset" in manifest
            assert Path(manifest["subsystem_runtime_asset"]["path"]).exists()
            assert Path(manifest["scene_intelligence_runtime_asset"]["path"]).exists()
            assert "assembly_decisions" in manifest
            assert manifest["assembly_decisions"]["scene_type_selector"]["subsystem_id"] == "CS-031"
            assert manifest["assembly_decisions"]["scene_type_selector"]["scene_intelligence_asset_id"] == "SIRT-SCENE-BUILDER-v1"
            assert manifest["assembly_decisions"]["audio_primer"]["subsystem_id"] == "CS-010"
            assert manifest["assembly_decisions"]["av_sync"]["subsystem_id"] == "CS-022"
            assert manifest["assembly_decisions"]["temporal_binding"]["subsystem_id"] == "CS-027"
            assert manifest["assembly_decisions"]["rhythm_generator"]["subsystem_id"] == "CS-023"
            assert manifest["assembly_decisions"]["shot_duration"]["subsystem_id"] == "CS-015"
            assert manifest["assembly_decisions"]["peak_end_budget"]["subsystem_id"] == "CS-011"
            assert manifest["assembly_decisions"]["cta_fusion"]["subsystem_id"] == "CS-012"
            assert manifest["assembly_decisions"]["isc_quality"]["subsystem_id"] == "CS-029"
            assert manifest["assembly_decisions"]["isc_quality"]["score"] >= 80
            assert manifest["assembly_decisions"]["scene_type_selector"]["selected_beat_count"] == len(manifest["beats"])
            assert manifest["assembly_decisions"]["rhythm_generator"]["verdict"] == "REVISE"
            assert manifest["assembly_decisions"]["shot_duration"]["verdict"] == "PASS"
            assert manifest["assembly_decisions"]["cta_fusion"]["verdict"] == "PASS"
            assert manifest["call_to_action"]["fused_with_end_state"] is True
            assert manifest["scene_type_plan"]
            boosted = manifest["assembly_decisions"]["peak_end_budget"]["boosted_beat_indices"]
            assert boosted
            assert receipt["previous_receipt_hash"] != "GENESIS"
            assert Path(manifest["constraint_manifest"]["path"]).exists()

    def test_manifest_assembly_decision_snapshot(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            beats = _build_beats()
            fp_map = _make_fingerprint_map(beats)
            resolved = resolve_asset_urls(beats, fp_map)
            parsed = _make_full_parsed_result(beats)
            curve = _make_ducking_curve(parsed["total_frames"])
            manifest, _ = run_manifest_assembly(
                parsed, resolved, ducking_curve=curve,
                receipt_output_dir=tmpdir,
            )

            scene_selector = manifest["assembly_decisions"]["scene_type_selector"]
            assert scene_selector["subsystem_id"] == "CS-031"
            assert scene_selector["scene_intelligence_asset_id"] == "SIRT-SCENE-BUILDER-v1"
            assert scene_selector["selected_beat_count"] == 5
            assert scene_selector["selected_scene_types"][0]["selected_scene_template_id"] == "HOOK-1-AB-2"
            assert scene_selector["selected_scene_types"][0]["selected_effect_stack"]
            assert scene_selector["selected_scene_types"][0]["estimated_scene_cls"] >= 1.0
            assert scene_selector["selected_scene_types"][4]["selected_scene_template_id"] in {
                "TURNING_POINT-1-B-1",
                "TURNING_POINT-2-B-1",
                "TURNING_POINT-3-BB-2",
                "TURNING_POINT-4-BA-2",
            }

            assert manifest["assembly_decisions"]["audio_primer"]["subsystem_id"] == "CS-010"
            assert manifest["assembly_decisions"]["av_sync"]["subsystem_id"] == "CS-022"
            assert manifest["assembly_decisions"]["temporal_binding"]["subsystem_id"] == "CS-027"
            assert manifest["assembly_decisions"]["rhythm_generator"]["subsystem_id"] == "CS-023"
            assert manifest["assembly_decisions"]["peak_end_budget"]["subsystem_id"] == "CS-011"
            assert manifest["assembly_decisions"]["cognitive_rhythm_validator"]["validator_id"] == "CRV-SCENE-BUILDER-v1"
            assert manifest["assembly_decisions"]["cognitive_rhythm_validator"]["verdict"] in {"PASS", "REVISE", "BLOCK"}
            assert manifest["assembly_decisions"]["cognitive_rhythm_validator"]["gates"]

            first_beat = manifest["beats"][0]
            assert first_beat["selected_container"] == "HOOK"
            assert first_beat["selected_component"] == "HOOK"
            assert first_beat["selected_scene_template_id"] == "HOOK-1-AB-2"
            assert first_beat["selected_effect_stack"]
            assert first_beat["effect_recommendations"][0]["mechanical_score"] > 0
            assert first_beat["scene_research_profile"]["target_attention_mode"] == "orienting"
