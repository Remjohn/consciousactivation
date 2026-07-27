"""
I2V Client Test Suite — FR-VID-03

Tests motion preset assignment, segment calculation, VRAM enforcement,
Ken Burns fallback, fingerprint emission, and pipeline orchestration.

Maps to FR-VID-03 §9 Acceptance Criteria AC1-AC6 and §11 Testing Strategy.
"""

import tempfile
from math import ceil

from i2v_client import (
    resolve_motion_preset,
    load_motion_presets,
    compute_segments,
    assign_motion_parameters,
    emit_i2v_fingerprint,
    build_ken_burns_fallback,
    check_service_availability_with_retries,
    run_i2v_pipeline_stage1,
    DEFAULT_MODEL_MAX_FRAMES,
    SEGMENT_OVERLAP_FRAMES,
    KEN_BURNS_RETRY_CYCLES,
)


# ===================================================================
# Motion Preset Lookup — §11 Unit Test + AC1
# ===================================================================


class TestMotionPresetLookup:
    def setup_method(self):
        self.presets = load_motion_presets()

    def test_ac1_climax_preset(self):
        """AC1: arc_stage=climax → dynamic_push_forward, motion_strength=0.8."""
        preset = resolve_motion_preset("climax", self.presets)
        assert preset is not None
        assert preset["camera_motion"] == "dynamic_push_forward"
        assert preset["motion_strength"] == 0.8

    def test_hook_preset(self):
        preset = resolve_motion_preset("hook", self.presets)
        assert preset is not None
        assert preset["camera_motion"] == "slow_zoom_in"
        assert preset["motion_strength"] == 0.6

    def test_resolution_preset(self):
        preset = resolve_motion_preset("resolution", self.presets)
        assert preset is not None
        assert preset["camera_motion"] == "gentle_drift"
        assert preset["motion_strength"] == 0.3

    def test_rising_action_preset(self):
        preset = resolve_motion_preset("rising_action", self.presets)
        assert preset is not None
        assert preset["camera_motion"] == "steady_push_forward"

    def test_falling_action_preset(self):
        preset = resolve_motion_preset("falling_action", self.presets)
        assert preset is not None
        assert preset["camera_motion"] == "slow_pull_back"

    def test_all_valid_arc_stages_have_presets(self):
        """§11 Unit Test: All valid arc stages resolve to non-null presets."""
        valid_stages = [
            "hook", "rising_action", "climax", "falling_action",
            "resolution", "transition", "establishing", "montage",
            "static", "coda",
        ]
        for stage in valid_stages:
            preset = resolve_motion_preset(stage, self.presets)
            assert preset is not None, f"Missing preset for {stage}"
            assert "camera_motion" in preset
            assert "motion_strength" in preset
            assert "fps" in preset
            assert "motion_bucket_id" in preset

    def test_invalid_arc_stage_returns_none(self):
        preset = resolve_motion_preset("nonexistent_stage", self.presets)
        assert preset is None

    def test_all_presets_have_fps_24(self):
        valid_stages = [
            "hook", "rising_action", "climax", "falling_action",
            "resolution", "transition", "establishing", "montage",
            "static", "coda",
        ]
        for stage in valid_stages:
            preset = resolve_motion_preset(stage, self.presets)
            assert preset["fps"] == 24, f"{stage} fps should be 24"


# ===================================================================
# Segment Calculation — §11 Unit Test + AC3
# ===================================================================


class TestSegmentCalculation:
    def test_ac3_6sec_24fps_two_segments(self):
        """AC3: 6.0s @ 24fps = 144 frames → 2 segments, 6-frame overlap."""
        segments = compute_segments(6.0, fps=24, max_frames=96, overlap_frames=6)
        assert len(segments) == 2
        # Segment 1: 96 frames
        assert segments[0]["frame_count"] == 96
        assert segments[0]["frame_start"] == 0
        assert segments[0]["frame_end"] == 95
        assert segments[0]["needs_crossfade"] is False
        # Segment 2: starts at overlap, covers remaining
        assert segments[1]["needs_crossfade"] is True
        assert segments[1]["frame_start"] == 90  # 95 - 6 + 1 = 90

    def test_short_beat_single_segment(self):
        """§11 Unit Test: 2.0s @ 24fps = 48 frames → 1 segment."""
        segments = compute_segments(2.0, fps=24, max_frames=96)
        assert len(segments) == 1
        assert segments[0]["frame_count"] == 48
        assert segments[0]["needs_crossfade"] is False

    def test_4sec_at_boundary(self):
        """§11 Unit Test: 4.0s @ 24fps = 96 frames → exactly 1 segment."""
        segments = compute_segments(4.0, fps=24, max_frames=96)
        assert len(segments) == 1
        assert segments[0]["frame_count"] == 96

    def test_8sec_two_segments(self):
        """§11 Unit Test: 8.0s @ 24fps = 192 frames → multiple segments."""
        segments = compute_segments(8.0, fps=24, max_frames=96, overlap_frames=6)
        assert len(segments) >= 2
        # All segments except last should be max_frames
        assert segments[0]["frame_count"] == 96

    def test_segment_overlap_correct(self):
        """Verify overlap frames between consecutive segments."""
        segments = compute_segments(6.0, fps=24, max_frames=96, overlap_frames=6)
        if len(segments) > 1:
            # Overlap: end of seg0 (95) - start of seg1 + 1 should be ≥ overlap_frames
            overlap = segments[0]["frame_end"] - segments[1]["frame_start"] + 1
            assert overlap == 6

    def test_segment_counts_match_spec_table(self):
        """§11 Unit Test: Verify segment counts for [2.0, 4.0, 6.0, 8.0] @ 24fps."""
        expected_counts = {2.0: 1, 4.0: 1, 6.0: 2, 8.0: 3}
        for duration, expected in expected_counts.items():
            segments = compute_segments(duration, fps=24, max_frames=96, overlap_frames=6)
            assert len(segments) == expected, (
                f"Duration {duration}s: expected {expected} segments, got {len(segments)}"
            )


# ===================================================================
# Motion Parameter Assignment — Stage 1
# ===================================================================


class TestAssignMotionParameters:
    def setup_method(self):
        self.presets = load_motion_presets()

    def test_basic_assignment(self):
        keyframes = [
            {"beat_index": 0, "output_image_url": "https://r2.cmf-assets.com/t2i/b0.png"},
        ]
        metadata = [
            {"beat_index": 0, "arc_stage": "climax", "duration_sec": 4.0},
        ]
        configs = assign_motion_parameters(keyframes, metadata, self.presets)
        assert len(configs) == 1
        assert configs[0]["status"] == "CONFIGURED"
        assert configs[0]["motion_parameters"]["camera_motion"] == "dynamic_push_forward"

    def test_missing_preset_returns_error(self):
        keyframes = [{"beat_index": 0, "output_image_url": "test.png"}]
        metadata = [{"beat_index": 0, "arc_stage": "nonexistent", "duration_sec": 3.0}]
        configs = assign_motion_parameters(keyframes, metadata, self.presets)
        assert configs[0]["status"] == "MOTION_PRESET_MISSING"

    def test_long_duration_gets_segments(self):
        keyframes = [{"beat_index": 0, "output_image_url": "test.png"}]
        metadata = [{"beat_index": 0, "arc_stage": "hook", "duration_sec": 6.0}]
        configs = assign_motion_parameters(keyframes, metadata, self.presets)
        assert configs[0]["status"] == "CONFIGURED"
        assert configs[0]["segments"] is not None
        assert configs[0]["segment_count"] == 2

    def test_normal_duration_no_segments(self):
        keyframes = [{"beat_index": 0, "output_image_url": "test.png"}]
        metadata = [{"beat_index": 0, "arc_stage": "hook", "duration_sec": 3.0}]
        configs = assign_motion_parameters(keyframes, metadata, self.presets)
        assert configs[0]["segments"] is None
        assert configs[0]["segment_count"] == 1

    def test_duration_frames_computation(self):
        keyframes = [{"beat_index": 0, "output_image_url": "test.png"}]
        metadata = [{"beat_index": 0, "arc_stage": "hook", "duration_sec": 3.5}]
        configs = assign_motion_parameters(keyframes, metadata, self.presets)
        expected_frames = ceil(3.5 * 24)  # 84
        assert configs[0]["motion_parameters"]["duration_frames"] == expected_frames

    def test_multi_beat_batch(self):
        keyframes = [
            {"beat_index": i, "output_image_url": f"img_{i}.png"} for i in range(5)
        ]
        metadata = [
            {"beat_index": 0, "arc_stage": "hook", "duration_sec": 3.0},
            {"beat_index": 1, "arc_stage": "rising_action", "duration_sec": 4.0},
            {"beat_index": 2, "arc_stage": "climax", "duration_sec": 3.5},
            {"beat_index": 3, "arc_stage": "falling_action", "duration_sec": 4.0},
            {"beat_index": 4, "arc_stage": "resolution", "duration_sec": 3.0},
        ]
        configs = assign_motion_parameters(keyframes, metadata, self.presets)
        assert len(configs) == 5
        assert all(c["status"] == "CONFIGURED" for c in configs)
        motions = [c["motion_parameters"]["camera_motion"] for c in configs]
        assert motions == [
            "slow_zoom_in", "steady_push_forward", "dynamic_push_forward",
            "slow_pull_back", "gentle_drift",
        ]


# ===================================================================
# Fingerprint Emission — AC5
# ===================================================================


class TestFingerprintEmission:
    def test_ac5_fingerprint_fields(self):
        """AC5: stage_2_i2v metadata contains required fields."""
        result = {
            "status": "GENERATED",
            "workflow_id": "RH-WF-CMF-I2V-SVD-001",
            "input_keyframe_url": "https://r2.cmf-assets.com/t2i/b0.png",
            "motion_parameters_applied": {
                "motion_bucket_id": 127,
                "motion_strength": 0.6,
                "camera_motion": "slow_zoom_in",
            },
            "output_video_url": "https://r2.cmf-assets.com/i2v/b0.mp4",
            "seed_used": 77204,
            "vram_tier_used": "48GB",
        }
        fp = emit_i2v_fingerprint(result)
        assert fp["runninghub_workflow_id"] == "RH-WF-CMF-I2V-SVD-001"
        assert fp["input_image_url"] == "https://r2.cmf-assets.com/t2i/b0.png"
        assert fp["motion_parameters"]["camera_motion"] == "slow_zoom_in"
        assert fp["output_video_url"] == "https://r2.cmf-assets.com/i2v/b0.mp4"
        assert "generation_timestamp" in fp
        assert fp["seed_used"] == 77204


# ===================================================================
# Ken Burns Fallback — AC6
# ===================================================================


class TestKenBurnsFallback:
    def test_ac6_three_failures_offers_ken_burns(self):
        """AC6: 3 failed retry cycles → OFFER_KEN_BURNS."""
        retry_results = [False, False, False]
        action, message = check_service_availability_with_retries(retry_results)
        assert action == "OFFER_KEN_BURNS"
        assert "ken burns" in message.lower()

    def test_service_available_after_retries(self):
        retry_results = [False, False, True]
        action, _ = check_service_availability_with_retries(retry_results)
        assert action == "SERVICE_AVAILABLE"

    def test_single_failure_retry(self):
        retry_results = [False]
        action, _ = check_service_availability_with_retries(retry_results)
        assert action == "RETRY"

    def test_two_failures_retry(self):
        retry_results = [False, False]
        action, _ = check_service_availability_with_retries(retry_results)
        assert action == "RETRY"

    def test_empty_retry_results_available(self):
        action, _ = check_service_availability_with_retries([])
        assert action == "SERVICE_AVAILABLE"

    def test_ken_burns_fallback_struct(self):
        """AC6: Ken Burns fallback has correct asset_type flag."""
        fallback = build_ken_burns_fallback(
            "https://r2.cmf-assets.com/t2i/b3.png", 3, 4.0
        )
        assert fallback["status"] == "KEN_BURNS_FALLBACK"
        assert fallback["asset_type"] == "ken_burns_fallback"
        assert fallback["beat_index"] == 3
        assert fallback["duration_sec"] == 4.0


# ===================================================================
# Pipeline Stage 1 with Receipt
# ===================================================================


class TestPipelineStage1:
    def test_stage1_produces_configs_and_receipt(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            keyframes = [
                {"beat_index": 0, "output_image_url": "img.png"},
            ]
            metadata = [
                {"beat_index": 0, "arc_stage": "hook", "duration_sec": 3.0},
            ]
            configs, receipt = run_i2v_pipeline_stage1(
                keyframes, metadata, receipt_output_dir=tmpdir
            )
            assert len(configs) == 1
            assert configs[0]["status"] == "CONFIGURED"
            assert receipt["stage_name"] == "I2V_MOTION_ASSIGN"
            assert receipt["agent_name"] == "runninghub_i2v_client"

    def test_stage1_receipt_has_genesis_or_chain(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            keyframes = [{"beat_index": 0, "output_image_url": "img.png"}]
            metadata = [{"beat_index": 0, "arc_stage": "hook", "duration_sec": 3.0}]
            configs, receipt = run_i2v_pipeline_stage1(
                keyframes, metadata, receipt_output_dir=tmpdir
            )
            assert receipt["previous_receipt_hash"] == "GENESIS"

    def test_stage1_with_previous_receipt_chains(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            prev = {"receipt_id": "fake", "stage_name": "T2I_QUALITY_VERDICT"}
            keyframes = [{"beat_index": 0, "output_image_url": "img.png"}]
            metadata = [{"beat_index": 0, "arc_stage": "hook", "duration_sec": 3.0}]
            configs, receipt = run_i2v_pipeline_stage1(
                keyframes, metadata,
                previous_receipt=prev,
                receipt_output_dir=tmpdir,
            )
            assert receipt["previous_receipt_hash"] != "GENESIS"
