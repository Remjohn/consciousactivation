"""
Gate J Test Suite — FR-VID-07

Tests all 4 Gate J questions with pass and fail scenarios.

Maps to FR-VID-07 §6 Gate J: Timestamp Integrity, Safe Zone,
Readability, Color Contrast.
"""

from gates.gate_j import (
    check_timestamp_integrity,
    check_safe_zone,
    check_readability,
    check_color_contrast,
    run_gate_j,
)
from caption_engine import (
    prepare_caption_data,
    extract_words_from_transcript,
    DEFAULT_SAFE_ZONE,
)


# ===================================================================
# Helpers
# ===================================================================


def _make_word(text, start_sec, end_sec, fps=24):
    return {
        "word": text,
        "start_sec": start_sec,
        "end_sec": end_sec,
        "start_frame": int(start_sec * fps),
        "end_frame": int(end_sec * fps),
        "confidence": 0.95,
    }


def _make_transcript(words, fps=24):
    total_dur = words[-1]["end_sec"] if words else 0
    return {
        "transcript_id": "TR-TEST-001",
        "source_audio": "test.mp3",
        "model": "whisper-large-v3",
        "language": "en",
        "total_duration_sec": total_dur,
        "total_frames": int(total_dur * fps),
        "fps": fps,
        "word_count": len(words),
        "segments": [{
            "segment_id": 0,
            "text": " ".join(w["word"] for w in words),
            "start_sec": 0.0,
            "end_sec": total_dur,
            "start_frame": 0,
            "end_frame": int(total_dur * fps),
            "words": words,
        }],
    }


def _make_beats(count=3, duration_sec=3.0, fps=24):
    beats = []
    for i in range(count):
        start = i * duration_sec
        beats.append({
            "beat_index": i,
            "start_sec": start,
            "duration_sec": duration_sec,
            "start_frame": int(start * fps),
            "duration_frames": int(duration_sec * fps),
        })
    return beats


def _make_config(style="hormozi"):
    return {
        "style_preset": style,
        "font_family": "Inter",
        "font_size_base": 42,
        "font_size_emphasis": 63,
        "project_id": "03_50-12",
        "color_theme": {
            "base_text_color": "#FFFFFF",
            "emphasis_color": "#E74C3C",
            "shadow_color": "#000000",
        },
    }


def _make_valid_caption_data():
    """Build a valid caption data structure for testing."""
    words = [
        _make_word("Hello", 0.0, 0.5),
        _make_word("world", 0.5, 1.0),
        _make_word("testing", 1.0, 1.8),
    ]
    transcript = _make_transcript(words)
    beats = _make_beats(count=1, duration_sec=3.0)
    config = _make_config()
    return prepare_caption_data(transcript, beats, config)


# ===================================================================
# Q1: Timestamp Integrity
# ===================================================================


class TestGateJQ1TimestampIntegrity:
    def test_valid_timestamps(self):
        data = _make_valid_caption_data()
        ok, msg = check_timestamp_integrity(data, data["total_frames"])
        assert ok, msg

    def test_negative_frame(self):
        data = _make_valid_caption_data()
        data["beats"][0]["lines"][0]["words"][0]["start_frame"] = -5
        ok, msg = check_timestamp_integrity(data, data["total_frames"])
        assert not ok
        assert "negative" in msg.lower()

    def test_exceeds_total_frames(self):
        data = _make_valid_caption_data()
        data["beats"][0]["lines"][0]["words"][-1]["end_frame"] = 99999
        ok, msg = check_timestamp_integrity(data, data["total_frames"])
        assert not ok
        assert "total_frames" in msg

    def test_start_after_end(self):
        data = _make_valid_caption_data()
        w = data["beats"][0]["lines"][0]["words"][0]
        w["start_frame"] = 100
        w["end_frame"] = 10
        ok, msg = check_timestamp_integrity(data, 200)
        assert not ok

    def test_non_monotonic(self):
        """Words out of order → not monotonically increasing."""
        data = _make_valid_caption_data()
        words = data["beats"][0]["lines"][0]["words"]
        if len(words) >= 2:
            # Swap frames to break monotonicity
            words[1]["start_frame"] = 0
            words[1]["end_frame"] = 2
            ok, msg = check_timestamp_integrity(data, data["total_frames"])
            assert not ok
            assert "monotonically" in msg.lower()


# ===================================================================
# Q2: Safe Zone
# ===================================================================


class TestGateJQ2SafeZone:
    def test_valid_safe_zone(self):
        data = _make_valid_caption_data()
        ok, msg = check_safe_zone(data)
        assert ok, msg

    def test_x_min_violation(self):
        data = _make_valid_caption_data()
        data["beats"][0]["position"]["safe_zone"]["x_min"] = 0.05
        ok, msg = check_safe_zone(data, DEFAULT_SAFE_ZONE)
        assert not ok
        assert "x_min" in msg

    def test_y_max_violation(self):
        data = _make_valid_caption_data()
        data["beats"][0]["position"]["safe_zone"]["y_max"] = 0.95
        ok, msg = check_safe_zone(data, DEFAULT_SAFE_ZONE)
        assert not ok
        assert "y_max" in msg

    def test_missing_safe_zone(self):
        data = _make_valid_caption_data()
        data["beats"][0]["position"] = {}
        ok, msg = check_safe_zone(data)
        assert not ok
        assert "missing" in msg.lower()


# ===================================================================
# Q3: Readability
# ===================================================================


class TestGateJQ3Readability:
    def test_readable_caption(self):
        data = _make_valid_caption_data()
        ok, msg = check_readability(data, fps=24)
        assert ok, msg

    def test_too_fast_unreadable(self):
        """6 words in 3 frames (125ms) → 20.8ms/word < 100ms minimum."""
        data = {
            "beats": [{
                "beat_index": 0,
                "lines": [{
                    "line_index": 0,
                    "words": [
                        {"word": f"w{i}", "start_frame": 0, "end_frame": 3, "emphasis": False}
                        for i in range(6)
                    ],
                }],
                "style_preset": "hormozi",
                "position": {"anchor": "bottom-center", "safe_zone": DEFAULT_SAFE_ZONE},
                "color_theme": {"base_text_color": "#FFFFFF", "emphasis_color": "#E74C3C", "shadow_color": "#000000"},
            }],
        }
        ok, msg = check_readability(data, fps=24)
        assert not ok
        assert "READABILITY" in msg

    def test_zero_duration_line(self):
        data = {
            "beats": [{
                "beat_index": 0,
                "lines": [{
                    "line_index": 0,
                    "words": [
                        {"word": "flash", "start_frame": 10, "end_frame": 10, "emphasis": False}
                    ],
                }],
                "style_preset": "hormozi",
                "position": {"anchor": "bottom-center", "safe_zone": DEFAULT_SAFE_ZONE},
                "color_theme": {"base_text_color": "#FFFFFF", "emphasis_color": "#E74C3C", "shadow_color": "#000000"},
            }],
        }
        ok, msg = check_readability(data, fps=24)
        assert not ok


# ===================================================================
# Q4: Color Contrast
# ===================================================================


class TestGateJQ4ColorContrast:
    def test_high_contrast_passes(self):
        data = _make_valid_caption_data()
        ok, msg = check_color_contrast(data)
        assert ok, msg

    def test_low_contrast_fails(self):
        """Light gray text on white shadow → fails WCAG AA."""
        data = _make_valid_caption_data()
        data["beats"][0]["color_theme"] = {
            "base_text_color": "#CCCCCC",
            "emphasis_color": "#DDDDDD",
            "shadow_color": "#FFFFFF",
        }
        ok, msg = check_color_contrast(data)
        assert not ok
        assert "COLOR_CONTRAST" in msg

    def test_emphasis_contrast_checked(self):
        """Even if base passes, emphasis must also pass."""
        data = _make_valid_caption_data()
        data["beats"][0]["color_theme"] = {
            "base_text_color": "#FFFFFF",
            "emphasis_color": "#F0F0F0",  # Very light → low contrast vs white shadow
            "shadow_color": "#FFFFFF",
        }
        ok, msg = check_color_contrast(data)
        assert not ok


# ===================================================================
# Gate J Runner
# ===================================================================


class TestGateJRunner:
    def test_all_pass(self):
        data = _make_valid_caption_data()
        result = run_gate_j(data, data["total_frames"], fps=24)
        assert result["gate"] == "J"
        assert result["passed"] is True
        assert len(result["results"]) == 4

    def test_fail_on_timestamp_violation(self):
        data = _make_valid_caption_data()
        data["beats"][0]["lines"][0]["words"][0]["start_frame"] = -1
        result = run_gate_j(data, data["total_frames"], fps=24)
        assert result["passed"] is False
        # Q1 failed
        q1 = result["results"][0]
        assert q1["question"] == 1
        assert q1["passed"] is False

    def test_multiple_failures(self):
        """Both timestamp and safe zone violations."""
        data = _make_valid_caption_data()
        data["beats"][0]["lines"][0]["words"][0]["start_frame"] = -1
        data["beats"][0]["position"]["safe_zone"]["x_min"] = 0.01
        result = run_gate_j(data, data["total_frames"], fps=24)
        assert result["passed"] is False
        failed = [r for r in result["results"] if not r["passed"]]
        assert len(failed) >= 2
