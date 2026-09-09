"""
Beat Cluster Parser Test Suite — FR-VID-01

Tests beat cluster validation, frame timing computation, transition
assignment, legacy fallbacks, and URL sanitization safety.

Maps to FR-VID-01 §9 AC1-AC3, §11 Testing Strategy.
"""

from math import ceil
import tempfile

from beat_cluster_parser import (
    validate_beat_cluster,
    compute_frame_timings,
    resolve_transition,
    load_transition_presets,
    apply_legacy_fallbacks,
    parse_beat_cluster,
    run_beat_cluster_parse,
)


# ===================================================================
# Helpers
# ===================================================================


def _make_beat(index, duration, arc_stage="hook", beat_type="hook"):
    return {
        "beat_index": index,
        "beat_type": beat_type,
        "duration_sec": duration,
        "arc_stage": arc_stage,
        "visual_prompt_ref": f"prompt-{index}",
        "narration_text": f"Beat {index} narration.",
    }


def _make_12_beat_cluster():
    stages = [
        ("opening", "hook"), ("hook", "hook"), ("rising_action", "tension"),
        ("rising_action", "tension"), ("tension", "tension"), ("tension", "tension"),
        ("climax", "turning_point"), ("climax", "revelation"),
        ("falling_action", "reflection"), ("falling_action", "reflection"),
        ("resolution", "reflection"), ("coda", "callback"),
    ]
    durations = [4.2, 3.5, 5.0, 4.0, 3.5, 4.5, 3.0, 5.5, 4.0, 5.0, 4.5, 3.3]
    return {
        "beat_cluster_id": "BC-WITNESS-42",
        "arc_type": "witness",
        "project_id": "03_50-12",
        "beats": [
            _make_beat(i, durations[i], stages[i][0], stages[i][1])
            for i in range(12)
        ],
    }


# ===================================================================
# Validation — §11 Unit Test
# ===================================================================


class TestBeatClusterValidation:
    def test_valid_cluster_passes(self):
        raw = _make_12_beat_cluster()
        valid, missing = validate_beat_cluster(raw)
        assert valid
        assert missing == []

    def test_missing_beats_array(self):
        raw = {"beat_cluster_id": "x", "arc_type": "x", "project_id": "x"}
        valid, missing = validate_beat_cluster(raw)
        assert not valid
        assert any("beats" in m for m in missing)

    def test_missing_arc_type(self):
        raw = {"beat_cluster_id": "x", "project_id": "x", "beats": []}
        valid, missing = validate_beat_cluster(raw)
        assert not valid

    def test_zero_duration_beat(self):
        raw = {
            "beat_cluster_id": "x", "arc_type": "x", "project_id": "x",
            "beats": [{"beat_index": 0, "beat_type": "hook", "duration_sec": 0, "arc_stage": "hook"}],
        }
        valid, missing = validate_beat_cluster(raw)
        assert not valid
        assert any("positive" in m for m in missing)

    def test_negative_duration_beat(self):
        raw = {
            "beat_cluster_id": "x", "arc_type": "x", "project_id": "x",
            "beats": [{"beat_index": 0, "beat_type": "hook", "duration_sec": -2.0, "arc_stage": "hook"}],
        }
        valid, missing = validate_beat_cluster(raw)
        assert not valid

    def test_missing_per_beat_field(self):
        raw = {
            "beat_cluster_id": "x", "arc_type": "x", "project_id": "x",
            "beats": [{"beat_index": 0, "duration_sec": 3.0}],  # missing beat_type, arc_stage
        }
        valid, missing = validate_beat_cluster(raw)
        assert not valid
        assert any("beat_type" in m for m in missing)


# ===================================================================
# Frame Calculation — AC2, §11 Unit Test
# ===================================================================


class TestFrameCalculation:
    def test_ac2_4_2_sec_at_24fps(self):
        """AC2: 4.2s @ 24fps → ceil(100.8) = 101 frames."""
        beats = [_make_beat(0, 4.2)]
        timed = compute_frame_timings(beats, fps=24)
        assert timed[0]["duration_frames"] == 101

    def test_spec_durations(self):
        """§11: durations [1.0, 2.5, 4.2, 0.5, 3.3] at 24fps."""
        durations = [1.0, 2.5, 4.2, 0.5, 3.3]
        expected_frames = [24, 60, 101, 12, 80]
        expected_starts = [0, 24, 84, 185, 197]

        beats = [_make_beat(i, d) for i, d in enumerate(durations)]
        timed = compute_frame_timings(beats, fps=24)

        for i, beat in enumerate(timed):
            assert beat["duration_frames"] == expected_frames[i], (
                f"beat[{i}]: expected {expected_frames[i]}, got {beat['duration_frames']}"
            )
            assert beat["start_frame"] == expected_starts[i], (
                f"beat[{i}]: expected start {expected_starts[i]}, got {beat['start_frame']}"
            )

    def test_30fps_conversion(self):
        beats = [_make_beat(0, 2.0)]
        timed = compute_frame_timings(beats, fps=30)
        assert timed[0]["duration_frames"] == 60

    def test_60fps_conversion(self):
        beats = [_make_beat(0, 1.5)]
        timed = compute_frame_timings(beats, fps=60)
        assert timed[0]["duration_frames"] == 90

    def test_ceil_rounding(self):
        """Ensure rounding is always UP to prevent sub-frame gaps."""
        beats = [_make_beat(0, 1.01)]
        timed = compute_frame_timings(beats, fps=24)
        assert timed[0]["duration_frames"] == ceil(1.01 * 24)  # 25


# ===================================================================
# AC1: 12-Beat Parse — Full Pipeline
# ===================================================================


class TestFullParse:
    def test_ac1_12_beat_canonical_array(self):
        """AC1: 12 beats → canonical array, start_frames sum correctly."""
        raw = _make_12_beat_cluster()
        result = parse_beat_cluster(raw, fps=24)

        assert result["status"] == "PARSED"
        assert len(result["beats"]) == 12
        assert result["beat_cluster_id"] == "BC-WITNESS-42"

        # Verify frame continuity
        total = sum(b["duration_frames"] for b in result["beats"])
        assert total == result["total_frames"]

        # Verify start_frame cumulation
        expected_start = 0
        for beat in result["beats"]:
            assert beat["start_frame"] == expected_start
            expected_start += beat["duration_frames"]

    def test_parse_error_on_invalid(self):
        result = parse_beat_cluster({"beats": "not_a_list"}, fps=24)
        assert result["status"] == "PARSE_ERROR"


# ===================================================================
# Transition Assignment — AC3, §11 Unit Test
# ===================================================================


class TestTransitionAssignment:
    def setup_method(self):
        self.presets = load_transition_presets()

    def test_ac3_climax_turning_point(self):
        """AC3: climax + turning_point → TR-CLIMAX-TURNING-ZOOM."""
        t = resolve_transition("climax", "turning_point", self.presets)
        assert t is not None
        assert t["preset_id"] == "TR-CLIMAX-TURNING-ZOOM"
        assert t["type"] == "zoom_transition"

    def test_hook_default(self):
        t = resolve_transition("hook", "hook", self.presets)
        assert t is not None
        assert t["preset_id"] == "TR-HOOK-CROSSFADE"

    def test_hook_question_override(self):
        """Beat type override takes priority over arc_stage default."""
        t = resolve_transition("hook", "question", self.presets)
        assert t is not None
        assert t["preset_id"] == "TR-HOOK-QUESTION-CUT"
        assert t["type"] == "cut"

    def test_resolution_default(self):
        t = resolve_transition("resolution", "generic", self.presets)
        assert t is not None
        assert t["preset_id"] == "TR-RESOLUTION-CROSSFADE"

    def test_resolution_reflection_override(self):
        t = resolve_transition("resolution", "reflection", self.presets)
        assert t is not None
        assert t["preset_id"] == "TR-RESOLUTION-REFLECTION-DISSOLVE"

    def test_all_arc_stages_have_defaults(self):
        """§11: All valid arc stages resolve to non-null presets."""
        stages = [
            "opening", "hook", "rising_action", "tension", "climax",
            "falling_action", "resolution", "transition", "establishing",
            "montage", "static", "coda",
        ]
        for stage in stages:
            t = resolve_transition(stage, "generic", self.presets)
            assert t is not None, f"Missing transition for {stage}"
            assert "preset_id" in t

    def test_unknown_arc_stage_returns_none(self):
        t = resolve_transition("nonexistent", "generic", self.presets)
        assert t is None

    def test_full_parse_assigns_transitions(self):
        raw = _make_12_beat_cluster()
        result = parse_beat_cluster(raw, fps=24)
        for beat in result["beats"]:
            assert beat["transition"] is not None, (
                f"beat[{beat['beat_index']}] missing transition"
            )


# ===================================================================
# Legacy Fallback — §7
# ===================================================================


class TestLegacyFallback:
    def test_missing_arc_stage_gets_default(self):
        raw = {
            "beat_cluster_id": "x", "arc_type": "witness", "project_id": "x",
            "beats": [{"beat_index": 0, "beat_type": "hook", "duration_sec": 3.0}],
        }
        raw = apply_legacy_fallbacks(raw)
        assert raw["beats"][0]["arc_stage"] == "opening"
        assert "LEGACY_BEAT_CLUSTER" in raw.get("_warnings", [])

    def test_missing_duration_gets_equal(self):
        raw = {
            "beat_cluster_id": "x", "arc_type": "witness", "project_id": "x",
            "beats": [
                {"beat_index": 0, "beat_type": "hook", "arc_stage": "hook"},
                {"beat_index": 1, "beat_type": "hook", "arc_stage": "hook"},
            ],
        }
        raw = apply_legacy_fallbacks(raw, total_video_duration=8.0)
        assert raw["beats"][0]["duration_sec"] == 4.0
        assert raw["beats"][1]["duration_sec"] == 4.0

    def test_missing_visual_prompt_ref(self):
        raw = {
            "beat_cluster_id": "x", "arc_type": "x", "project_id": "x",
            "beats": [{"beat_index": 0, "beat_type": "hook", "duration_sec": 3.0, "arc_stage": "hook"}],
        }
        raw = apply_legacy_fallbacks(raw)
        assert raw["beats"][0]["visual_prompt_ref"] is None

    def test_non_legacy_no_warnings(self):
        raw = _make_12_beat_cluster()
        raw = apply_legacy_fallbacks(raw)
        assert "_warnings" not in raw


# ===================================================================
# Pipeline with Receipt
# ===================================================================


class TestBeatClusterParsePipeline:
    def test_produces_result_and_receipt(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            raw = _make_12_beat_cluster()
            result, receipt = run_beat_cluster_parse(raw, receipt_output_dir=tmpdir)
            assert result["status"] == "PARSED"
            assert receipt["stage_name"] == "BEAT_CLUSTER_PARSE"
            assert receipt["agent_name"] == "beat_cluster_parser"

    def test_receipt_chains(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            raw = _make_12_beat_cluster()
            r1_result, r1 = run_beat_cluster_parse(raw, receipt_output_dir=tmpdir)
            r2_result, r2 = run_beat_cluster_parse(
                raw, previous_receipt=r1, receipt_output_dir=tmpdir
            )
            assert r2["previous_receipt_hash"] != "GENESIS"
