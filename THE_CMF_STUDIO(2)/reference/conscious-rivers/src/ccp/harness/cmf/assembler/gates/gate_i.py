"""
Gate I — Pre-Audio Processing Constraint Network

FR-VID-06 §6 Skill Definition

Four validation questions that MUST all pass before audio processing begins.
If ANY answer is False, the pipeline HALTS with the failing question's diagnostic.

Each function returns: (passed: bool, diagnostic: str)

Build Prompt Rule 7: These are executable validation functions, NOT
documentation-only comments.
"""

from pathlib import Path

try:
    from ..audio_engine import get_audio_metadata
except ImportError:
    from audio_engine import get_audio_metadata


# ---------------------------------------------------------------------------
# Q1: Audio File Integrity
# FR-VID-06 §6 Gate I Q1
# ---------------------------------------------------------------------------


def check_audio_file_integrity(
    voiceover_path: Path,
    expected_video_duration_sec: float | None = None,
) -> tuple[bool, str]:
    """
    Gate I Q1: Is the voiceover file a valid audio file (MP3/WAV/M4A)
    with duration matching the expected video length (±5 seconds)?

    A truncated voiceover file produces incomplete captions and a ducking
    curve that ends mid-video.
    """
    voiceover_path = Path(voiceover_path)

    # Check file exists
    if not voiceover_path.exists():
        return (False, f"Voiceover file not found: {voiceover_path}")

    # Check extension
    valid_extensions = {".mp3", ".wav", ".m4a", ".flac", ".ogg"}
    if voiceover_path.suffix.lower() not in valid_extensions:
        return (
            False,
            f"Voiceover file '{voiceover_path.suffix}' is not a supported audio "
            f"format. Supported: {', '.join(sorted(valid_extensions))}.",
        )

    # Check readable / valid audio
    try:
        meta = get_audio_metadata(voiceover_path)
    except ValueError as exc:
        return (False, str(exc))

    duration = meta["duration_sec"]

    # Check duration matches expected video length (±5 seconds)
    if expected_video_duration_sec is not None:
        tolerance = 5.0
        if abs(duration - expected_video_duration_sec) > tolerance:
            return (
                False,
                f"Voiceover duration ({duration:.1f}s) differs from expected video "
                f"duration ({expected_video_duration_sec:.1f}s) by "
                f"{abs(duration - expected_video_duration_sec):.1f}s "
                f"(tolerance: ±{tolerance}s). A truncated voiceover produces "
                f"incomplete captions and a ducking curve that ends mid-video.",
            )

    return (True, f"Voiceover file is valid ({duration:.1f}s, {meta['codec']}).")


# ---------------------------------------------------------------------------
# Q2: Language Correctness
# FR-VID-06 §6 Gate I Q2
# ---------------------------------------------------------------------------

SUPPORTED_LANGUAGES = {
    "en", "es", "fr", "de", "it", "pt", "nl", "ja", "ko", "zh",
    "ar", "hi", "ru", "tr", "pl", "sv", "da", "no", "fi",
}


def check_language_correctness(
    language: str,
    voiceover_path: Path | None = None,
) -> tuple[bool, str]:
    """
    Gate I Q2: Is the Whisper language setting correct for this voiceover?

    English voiceover transcribed with French model produces garbage timestamps
    that cascade into wrong captions.
    """
    if not language or not language.strip():
        return (
            False,
            "Whisper language setting is empty. Must specify the correct language "
            "code (e.g., 'en' for English). Empty language causes Whisper to guess, "
            "which may produce incorrect timestamps.",
        )

    language = language.strip().lower()

    if language not in SUPPORTED_LANGUAGES:
        return (
            False,
            f"Language '{language}' is not in the supported language list. "
            f"Verify the language code is correct for this voiceover. "
            f"Supported: {', '.join(sorted(SUPPORTED_LANGUAGES))}.",
        )

    return (True, f"Language '{language}' is a supported Whisper language.")


# ---------------------------------------------------------------------------
# Q3: Music Track Duration
# FR-VID-06 §6 Gate I Q3
# ---------------------------------------------------------------------------


def check_music_track_duration(
    voiceover_path: Path,
    music_path: Path,
) -> tuple[bool, str]:
    """
    Gate I Q3: Does the background music file duration ≥ the voiceover duration?

    Shorter music creates silence at the end. Longer music needs trimming with
    fade-out — is the fade-out duration configured?
    """
    voiceover_path = Path(voiceover_path)
    music_path = Path(music_path)

    if not music_path.exists():
        return (False, f"Background music file not found: {music_path}")

    try:
        vo_meta = get_audio_metadata(voiceover_path)
    except ValueError as exc:
        return (False, f"Cannot read voiceover for duration check: {exc}")

    try:
        music_meta = get_audio_metadata(music_path)
    except ValueError as exc:
        return (False, f"Cannot read music file: {exc}")

    vo_duration = vo_meta["duration_sec"]
    music_duration = music_meta["duration_sec"]

    if music_duration < vo_duration:
        deficit = vo_duration - music_duration
        return (
            False,
            f"Background music ({music_duration:.1f}s) is shorter than voiceover "
            f"({vo_duration:.1f}s) by {deficit:.1f}s. This creates silence at the "
            f"end of the video. Provide a longer music track or enable music looping.",
        )

    return (
        True,
        f"Background music ({music_duration:.1f}s) ≥ voiceover ({vo_duration:.1f}s). "
        f"Excess: {music_duration - vo_duration:.1f}s (will be trimmed with fade-out).",
    )


# ---------------------------------------------------------------------------
# Q4: Ducking Target Appropriateness
# FR-VID-06 §6 Gate I Q4
# ---------------------------------------------------------------------------


def check_ducking_target_appropriateness(
    ducking_target: float,
) -> tuple[bool, str]:
    """
    Gate I Q4: Is the ducking target appropriate for this music style?

    Loud percussive music may need a lower target (0.08). Subtle ambient music
    may need a higher target (0.25). The target should be tested with a
    5-second sample before processing the full video.

    FR-VID-06 §6 Q4: Range validation — target must be within [0.05, 0.40].
    Below 0.05 = inaudible. Above 0.40 = music competes with voiceover.
    """
    if ducking_target < 0.05:
        return (
            False,
            f"Ducking target {ducking_target} is below 0.05 — music would be "
            f"essentially inaudible during voiceover. Increase to at least 0.05.",
        )

    if ducking_target > 0.40:
        return (
            False,
            f"Ducking target {ducking_target} is above 0.40 — music will compete "
            f"with voiceover for listener attention, reducing speech clarity. "
            f"Reduce to at most 0.40.",
        )

    return (
        True,
        f"Ducking target {ducking_target} is within acceptable range [0.05, 0.40].",
    )


# ---------------------------------------------------------------------------
# Gate I Runner — executes all 4 questions
# ---------------------------------------------------------------------------


def run_gate_i(
    voiceover_path: Path,
    music_path: Path,
    language: str = "en",
    ducking_target: float = 0.15,
    expected_video_duration_sec: float | None = None,
) -> tuple[bool, list[dict]]:
    """
    Run all 4 Gate I questions. Returns (all_passed, results_list).

    If ANY question returns False, all_passed is False and audio processing
    MUST NOT proceed. The pipeline HALTS with the failing question's diagnostic.

    FR-VID-06 §6: "Before processing audio for any video, the agent must
    answer ALL 4 questions."
    """
    results = []

    q1_pass, q1_diag = check_audio_file_integrity(
        voiceover_path, expected_video_duration_sec
    )
    results.append({
        "question": 1,
        "name": "Audio File Integrity",
        "passed": q1_pass,
        "diagnostic": q1_diag,
    })

    q2_pass, q2_diag = check_language_correctness(language, voiceover_path)
    results.append({
        "question": 2,
        "name": "Language Correctness",
        "passed": q2_pass,
        "diagnostic": q2_diag,
    })

    q3_pass, q3_diag = check_music_track_duration(voiceover_path, music_path)
    results.append({
        "question": 3,
        "name": "Music Track Duration",
        "passed": q3_pass,
        "diagnostic": q3_diag,
    })

    q4_pass, q4_diag = check_ducking_target_appropriateness(ducking_target)
    results.append({
        "question": 4,
        "name": "Ducking Target Appropriateness",
        "passed": q4_pass,
        "diagnostic": q4_diag,
    })

    all_passed = all(r["passed"] for r in results)
    return (all_passed, results)
