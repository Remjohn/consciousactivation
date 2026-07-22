"""
Gate I Violation Tests — FR-VID-06 Constraint Network

Build Prompt Stage 5 Completion Gate 5: "For each gate question, name the
validation function and show a test case that demonstrates it catches a violation."

Tests use temporary audio files created via FFmpeg for real file validation.
Gate I Q1 and Q3 require actual audio files (they call ffprobe). Tests that need
real files are marked to skip if ffprobe is not available.
"""

import subprocess
import tempfile
from pathlib import Path

import pytest

from gates.gate_i import (
    check_audio_file_integrity,
    check_language_correctness,
    check_music_track_duration,
    check_ducking_target_appropriateness,
    run_gate_i,
)


def _has_ffprobe() -> bool:
    try:
        subprocess.run(["ffprobe", "-version"], capture_output=True, timeout=5)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


needs_ffprobe = pytest.mark.skipif(
    not _has_ffprobe(), reason="ffprobe not available"
)


@pytest.fixture
def temp_audio_files(tmp_path):
    """Create temporary valid audio files using FFmpeg for testing."""
    vo_path = tmp_path / "voiceover.wav"
    music_path = tmp_path / "music.wav"

    # Create a 10-second silent voiceover WAV
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "lavfi", "-i",
            "anullsrc=r=44100:cl=mono", "-t", "10",
            str(vo_path),
        ],
        capture_output=True, timeout=30,
    )

    # Create a 15-second silent music WAV (longer than voiceover)
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "lavfi", "-i",
            "anullsrc=r=44100:cl=stereo", "-t", "15",
            str(music_path),
        ],
        capture_output=True, timeout=30,
    )

    return vo_path, music_path


@pytest.fixture
def short_music_file(tmp_path):
    """Create a music file shorter than any reasonable voiceover."""
    music_path = tmp_path / "short_music.wav"
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "lavfi", "-i",
            "anullsrc=r=44100:cl=stereo", "-t", "3",
            str(music_path),
        ],
        capture_output=True, timeout=30,
    )
    return music_path


# ---- Q1 Violation: Non-existent audio file ----


def test_gate_i_q1_violation_file_not_found():
    """Q1: Non-existent voiceover file → returns False."""
    fake_path = Path("/nonexistent/voiceover.mp3")
    passed, diagnostic = check_audio_file_integrity(fake_path)
    assert not passed, "Q1 should FAIL: file does not exist"
    assert "not found" in diagnostic.lower()


def test_gate_i_q1_violation_wrong_extension(tmp_path):
    """Q1: File with unsupported extension → returns False."""
    txt_file = tmp_path / "voiceover.txt"
    txt_file.write_text("not audio")
    passed, diagnostic = check_audio_file_integrity(txt_file)
    assert not passed, "Q1 should FAIL: .txt is not a supported audio format"
    assert "supported" in diagnostic.lower() or "format" in diagnostic.lower()


@needs_ffprobe
def test_gate_i_q1_violation_duration_mismatch(temp_audio_files):
    """Q1: 10s voiceover with expected duration 60s → returns False (±5s tolerance)."""
    vo_path, _ = temp_audio_files
    passed, diagnostic = check_audio_file_integrity(vo_path, expected_video_duration_sec=60.0)
    assert not passed, "Q1 should FAIL: 10s voiceover vs 60s expected"
    assert "duration" in diagnostic.lower() or "differs" in diagnostic.lower()


@needs_ffprobe
def test_gate_i_q1_passes_valid_file(temp_audio_files):
    """Q1: Valid WAV file with matching duration → returns True."""
    vo_path, _ = temp_audio_files
    passed, _ = check_audio_file_integrity(vo_path, expected_video_duration_sec=12.0)
    assert passed, "Q1 should PASS: 10s voiceover ≈ 12s expected (within ±5s)"


# ---- Q2 Violation: Invalid language ----


def test_gate_i_q2_violation_empty_language():
    """Q2: Empty language string → returns False."""
    passed, diagnostic = check_language_correctness("")
    assert not passed, "Q2 should FAIL: empty language"
    assert "empty" in diagnostic.lower()


def test_gate_i_q2_violation_unsupported_language():
    """Q2: Unsupported language code → returns False."""
    passed, diagnostic = check_language_correctness("xx")
    assert not passed, "Q2 should FAIL: 'xx' is not a supported language"
    assert "supported" in diagnostic.lower()


def test_gate_i_q2_passes_english():
    """Q2: English language → returns True."""
    passed, _ = check_language_correctness("en")
    assert passed, "Q2 should PASS: 'en' is supported"


# ---- Q3 Violation: Music shorter than voiceover ----


@needs_ffprobe
def test_gate_i_q3_violation_short_music(temp_audio_files, short_music_file):
    """Q3: 3s music track with 10s voiceover → returns False."""
    vo_path, _ = temp_audio_files
    passed, diagnostic = check_music_track_duration(vo_path, short_music_file)
    assert not passed, "Q3 should FAIL: music shorter than voiceover"
    assert "shorter" in diagnostic.lower()


@needs_ffprobe
def test_gate_i_q3_passes_longer_music(temp_audio_files):
    """Q3: 15s music with 10s voiceover → returns True."""
    vo_path, music_path = temp_audio_files
    passed, _ = check_music_track_duration(vo_path, music_path)
    assert passed, "Q3 should PASS: music longer than voiceover"


def test_gate_i_q3_violation_missing_music_file(tmp_path):
    """Q3: Music file does not exist → returns False."""
    vo_path = tmp_path / "vo.wav"
    vo_path.write_bytes(b"")  # Exists but won't matter — music check first
    music_path = tmp_path / "nonexistent_music.mp3"
    passed, diagnostic = check_music_track_duration(vo_path, music_path)
    assert not passed, "Q3 should FAIL: music file not found"
    assert "not found" in diagnostic.lower()


# ---- Q4 Violation: Ducking target out of range ----


def test_gate_i_q4_violation_too_low():
    """Q4: Ducking target 0.02 (below 0.05) → returns False."""
    passed, diagnostic = check_ducking_target_appropriateness(0.02)
    assert not passed, "Q4 should FAIL: 0.02 is below 0.05"
    assert "inaudible" in diagnostic.lower() or "below" in diagnostic.lower()


def test_gate_i_q4_violation_too_high():
    """Q4: Ducking target 0.55 (above 0.40) → returns False."""
    passed, diagnostic = check_ducking_target_appropriateness(0.55)
    assert not passed, "Q4 should FAIL: 0.55 is above 0.40"
    assert "compete" in diagnostic.lower() or "above" in diagnostic.lower()


def test_gate_i_q4_passes_default():
    """Q4: Default ducking target 0.15 → returns True."""
    passed, _ = check_ducking_target_appropriateness(0.15)
    assert passed, "Q4 should PASS: 0.15 is within [0.05, 0.40]"


def test_gate_i_q4_passes_edge_low():
    """Q4: Edge case 0.05 → returns True."""
    passed, _ = check_ducking_target_appropriateness(0.05)
    assert passed, "Q4 should PASS: 0.05 is the lower bound"


def test_gate_i_q4_passes_edge_high():
    """Q4: Edge case 0.40 → returns True."""
    passed, _ = check_ducking_target_appropriateness(0.40)
    assert passed, "Q4 should PASS: 0.40 is the upper bound"
