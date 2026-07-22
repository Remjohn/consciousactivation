"""
Audio Engine Unit Tests — FR-VID-06

Tests for the ducking curve computation algorithm (Stage 3),
verifying AC2 (array length) and AC3 (cosine easing).
These tests do NOT require Whisper, Demucs, or FFmpeg.
"""

import math

from audio_engine import compute_ducking_curve


def _make_transcript(words_spec: list[tuple], fps: int = 24, total_dur: float = 10.0) -> dict:
    """
    Build a minimal DEP-VID-004 transcript for testing.

    words_spec: list of (word_text, start_sec, end_sec) tuples.
    """
    words = []
    for word_text, start_sec, end_sec in words_spec:
        words.append({
            "word": word_text,
            "start_sec": start_sec,
            "end_sec": end_sec,
            "start_frame": int(start_sec * fps),
            "end_frame": int(end_sec * fps),
            "confidence": 0.99,
        })

    segments = []
    if words:
        segments.append({
            "segment_id": 0,
            "text": " ".join(w["word"] for w in words),
            "start_sec": words[0]["start_sec"],
            "end_sec": words[-1]["end_sec"],
            "start_frame": words[0]["start_frame"],
            "end_frame": words[-1]["end_frame"],
            "words": words,
        })

    return {
        "transcript_id": "TR-TEST-001",
        "source_audio": "test.wav",
        "model": "whisper-large-v3",
        "language": "en",
        "total_duration_sec": total_dur,
        "total_frames": int(total_dur * fps),
        "fps": fps,
        "word_count": len(words),
        "segments": segments,
    }


# ---- AC2: Ducking curve length ----


def test_curve_length_60s_24fps():
    """AC2: 60-second video at 24 FPS → exactly 1440 values."""
    transcript = _make_transcript([("hello", 1.0, 1.5)], fps=24, total_dur=60.0)
    result = compute_ducking_curve(transcript, fps=24, total_duration_sec=60.0)
    assert result["total_frames"] == 1440
    assert len(result["values"]) == 1440, f"Expected 1440, got {len(result['values'])}"


def test_curve_length_30s_30fps():
    """AC2: 30-second video at 30 FPS → exactly 900 values."""
    transcript = _make_transcript([("test", 2.0, 2.5)], fps=30, total_dur=30.0)
    result = compute_ducking_curve(transcript, fps=30, total_duration_sec=30.0)
    assert result["total_frames"] == 900
    assert len(result["values"]) == 900


def test_curve_length_90s_60fps():
    """AC2: 90-second video at 60 FPS → exactly 5400 values."""
    transcript = _make_transcript([("word", 5.0, 5.5)], fps=60, total_dur=90.0)
    result = compute_ducking_curve(transcript, fps=60, total_duration_sec=90.0)
    assert result["total_frames"] == 5400
    assert len(result["values"]) == 5400


# ---- Values range ----


def test_curve_values_in_range():
    """All values must be between 0.0 and 1.0."""
    transcript = _make_transcript(
        [("hello", 1.0, 1.5), ("world", 2.0, 2.5)],
        fps=24, total_dur=10.0,
    )
    result = compute_ducking_curve(transcript, fps=24, total_duration_sec=10.0)
    for i, v in enumerate(result["values"]):
        assert 0.0 <= v <= 1.0, f"Frame {i}: value {v} out of range"


# ---- Full music volume when no speech ----


def test_curve_full_volume_no_speech():
    """Silence-only transcript → all values at 1.0 (full music volume)."""
    transcript = _make_transcript([], fps=24, total_dur=10.0)
    result = compute_ducking_curve(transcript, fps=24, total_duration_sec=10.0)
    assert all(v == 1.0 for v in result["values"]), "No speech → all values should be 1.0"


# ---- Ducking target applied during speech ----


def test_curve_ducked_during_speech():
    """During speech (well inside the segment), values should be at ducking_target."""
    # words from 2.0-5.0 seconds → frames 48-120 at 24fps
    # With padding (3 before, 6 after) and easing (6 frames),
    # the core ducked region should be solidly at the target.
    transcript = _make_transcript(
        [("one", 2.0, 2.5), ("two", 3.0, 3.5), ("three", 4.0, 4.5)],
        fps=24, total_dur=10.0,
    )
    result = compute_ducking_curve(
        transcript, fps=24, total_duration_sec=10.0, ducking_target=0.15,
    )
    # Check a frame in the middle of speech (frame 72 = 3.0s)
    # This should be at (or very near) the ducking target
    mid_frame = 72
    assert result["values"][mid_frame] <= 0.20, (
        f"Frame {mid_frame} (during speech) should be ducked, got {result['values'][mid_frame]}"
    )


# ---- AC3: Cosine easing — no sudden jumps ----


def test_curve_no_sudden_jumps():
    """
    AC3: Transitions between ducked and full-volume must be smooth.
    No single-frame jump from 0.15 to 1.0 should exist.
    """
    transcript = _make_transcript(
        [("hello", 3.0, 4.0)],
        fps=24, total_dur=10.0,
    )
    result = compute_ducking_curve(
        transcript, fps=24, total_duration_sec=10.0, ducking_target=0.15,
    )
    values = result["values"]

    # Check that no adjacent frames have a jump > 0.5
    for i in range(1, len(values)):
        diff = abs(values[i] - values[i - 1])
        assert diff < 0.50, (
            f"Sudden jump at frame {i}: {values[i-1]:.3f} → {values[i]:.3f} "
            f"(diff={diff:.3f}). AC3 requires cosine easing over 6 frames."
        )


# ---- Output schema fields ----


def test_curve_output_schema_fields():
    """DEP-VID-005 output contains all required schema fields."""
    transcript = _make_transcript([("test", 1.0, 1.5)], fps=24, total_dur=5.0)
    result = compute_ducking_curve(transcript, fps=24, total_duration_sec=5.0)

    required_fields = [
        "curve_id", "total_frames", "fps", "ducking_target",
        "ease_frames", "values",
    ]
    for field in required_fields:
        assert field in result, f"Missing required field: {field}"

    assert result["fps"] == 24
    assert result["ducking_target"] == 0.15
    assert result["ease_frames"] == 6
    assert isinstance(result["values"], list)
