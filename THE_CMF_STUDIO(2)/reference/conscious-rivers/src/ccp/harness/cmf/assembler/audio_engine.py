"""
FR-VID-06 — Audio Engine (Whisper + Demucs + Ducking)

CMF Video Pipeline — Three-stage Audio Processing Pipeline

  Stage 1: WHISPER_TRANSCRIPTION — Transcribe voiceover with word-level timestamps
  Stage 2: DEMUCS_SEPARATION — Conditionally isolate vocals via Demucs
  Stage 3: DUCKING_CURVE_COMPUTE — Per-frame music ducking curve

Spec Reference: FR-VID-06 §4 Implementation Plan
Produces: DEP-VID-004 (Whisper Transcript), DEP-VID-005 (Ducking Curve),
          DEP-VID-019 (Separated Stems, optional)
Consumes: DEP-VID-017 (Voiceover Audio), DEP-VID-018 (Background Music)
"""

import json
import logging
import math
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger("cmf.audio_engine")

# ---------------------------------------------------------------------------
# Constants from FR-VID-06 spec
# ---------------------------------------------------------------------------

WHISPER_MODEL = "large-v3"                  # §4 Stage 1 Step 2
DEFAULT_LANGUAGE = "en"                     # §4 Stage 1 Step 2
SNR_THRESHOLD_DB = 20.0                     # §4 Stage 2 Step 2: "> 20 dB"
DEMUCS_MODEL = "htdemucs_ft"               # §4 Stage 2 Step 3
DEFAULT_DUCKING_TARGET = 0.15               # §4 Stage 3: "default 0.15"
EASE_FRAMES = 6                             # §4 Stage 3 Step 4: "6 frames"
SENTENCE_PAD_BEFORE = 3                     # §4 Stage 3 Step 3: "3 frames before"
SENTENCE_PAD_AFTER = 6                      # §4 Stage 3 Step 3: "6 frames after"
WORD_COUNT_TOLERANCE = 0.10                 # §4 Stage 1 Step 5: "±10%"
DURATION_TOLERANCE_SEC = 5.0                # §6 Gate I Q1: "±5 seconds"


# ---------------------------------------------------------------------------
# Audio File Utilities
# ---------------------------------------------------------------------------


def get_audio_metadata(audio_path: Path) -> dict:
    """
    Extract audio file metadata using ffprobe.

    Returns dict with keys: duration_sec, sample_rate, channels, codec, format.
    Raises ValueError on invalid / unreadable files.
    """
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        str(audio_path),
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30, check=True,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as exc:
        raise ValueError(f"AUDIO_INVALID: Cannot read audio file '{audio_path}': {exc}") from exc

    probe = json.loads(result.stdout)
    fmt = probe.get("format", {})
    streams = [s for s in probe.get("streams", []) if s.get("codec_type") == "audio"]
    if not streams:
        raise ValueError(f"AUDIO_INVALID: No audio stream found in '{audio_path}'")

    stream = streams[0]
    duration = float(fmt.get("duration", 0))
    if duration <= 0:
        raise ValueError(f"AUDIO_INVALID: Zero-duration audio file '{audio_path}'")

    return {
        "duration_sec": duration,
        "sample_rate": int(stream.get("sample_rate", 44100)),
        "channels": int(stream.get("channels", 1)),
        "codec": stream.get("codec_name", "unknown"),
        "format": fmt.get("format_name", "unknown"),
        "file_path": str(audio_path),
    }


def compute_snr_db(audio_path: Path) -> float:
    """
    Estimate signal-to-noise ratio of an audio file using FFmpeg astats filter.

    FR-VID-06 §4 Stage 2 Step 1: "Compute signal-to-noise ratio (SNR)."
    Returns SNR in dB. Higher = cleaner audio.
    """
    cmd = [
        "ffmpeg",
        "-i", str(audio_path),
        "-af", "astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level",
        "-f", "null", "-",
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        logger.warning("SNR computation failed for %s — defaulting to 25dB (clean)", audio_path)
        return 25.0

    # Parse RMS levels from FFmpeg output
    rms_values = []
    for line in result.stderr.split("\n"):
        if "lavfi.astats.Overall.RMS_level" in line:
            parts = line.strip().split("=")
            if len(parts) >= 2:
                try:
                    rms_values.append(float(parts[-1]))
                except ValueError:
                    continue

    if not rms_values:
        logger.warning("No RMS data from %s — defaulting to 25dB (clean)", audio_path)
        return 25.0

    # Estimate SNR from RMS distribution (simplified: median - noise floor)
    rms_values.sort()
    median_rms = rms_values[len(rms_values) // 2]
    noise_floor = rms_values[0] if rms_values[0] < -60 else -70.0
    snr_estimate = abs(median_rms - noise_floor)

    return snr_estimate


# ===========================================================================
# Stage 1: Whisper Transcription (WHISPER_TRANSCRIPTION)
# FR-VID-06 §4 Stage 1
# ===========================================================================


def transcribe_voiceover(
    voiceover_path: Path,
    fps: int = 24,
    language: str = DEFAULT_LANGUAGE,
    expected_word_count: int | None = None,
) -> dict:
    """
    Stage 1: Transcribe voiceover with word-level timestamps.

    FR-VID-06 §4 Stage 1 Steps 1-5.
    Uses Whisper large-v3 with word_timestamps=True.
    Converts timestamps from seconds to frame numbers at project FPS.

    Args:
        voiceover_path: Path to voiceover audio file (MP3/WAV/M4A).
        fps: Project frames per second (default 24).
        language: Whisper language setting.
        expected_word_count: Optional expected narration word count for ±10% validation.

    Returns:
        DEP-VID-004 Whisper Transcript JSON dict.

    Raises:
        ValueError: AUDIO_INVALID on bad input, TRANSCRIPTION_FAILED on Whisper error.
    """
    import whisper

    voiceover_path = Path(voiceover_path)

    # Step 1: Load voiceover audio file
    audio_meta = get_audio_metadata(voiceover_path)
    total_duration_sec = audio_meta["duration_sec"]
    total_frames = int(total_duration_sec * fps)

    logger.info(
        "Transcribing %s (%.1fs, %d frames @ %dfps)",
        voiceover_path.name, total_duration_sec, total_frames, fps,
    )

    # Step 2: Run Whisper large-v3 with word_timestamps=True
    model = whisper.load_model(WHISPER_MODEL)
    result = model.transcribe(
        str(voiceover_path),
        word_timestamps=True,
        language=language,
    )

    # Step 3: Parse output into structured JSON
    segments = []
    all_words = []

    for seg_idx, segment in enumerate(result.get("segments", [])):
        words = []
        for word_data in segment.get("words", []):
            word_text = word_data.get("word", "").strip()
            if not word_text:
                continue

            start_sec = word_data["start"]
            end_sec = word_data["end"]

            # Step 4: Convert timestamps from seconds to frame numbers
            start_frame = int(start_sec * fps)
            end_frame = int(end_sec * fps)

            # Clamp to valid range
            start_frame = max(0, min(start_frame, total_frames))
            end_frame = max(0, min(end_frame, total_frames))

            word_entry = {
                "word": word_text,
                "start_sec": round(start_sec, 3),
                "end_sec": round(end_sec, 3),
                "start_frame": start_frame,
                "end_frame": end_frame,
                "confidence": round(word_data.get("probability", 0.0), 3),
            }
            words.append(word_entry)
            all_words.append(word_entry)

        if words:
            seg_entry = {
                "segment_id": seg_idx,
                "text": segment.get("text", "").strip(),
                "start_sec": round(segment.get("start", 0.0), 3),
                "end_sec": round(segment.get("end", 0.0), 3),
                "start_frame": words[0]["start_frame"],
                "end_frame": words[-1]["end_frame"],
                "words": words,
            }
            segments.append(seg_entry)

    # Step 5: Validate word count if expected (±10% tolerance)
    actual_word_count = len(all_words)
    if expected_word_count is not None and expected_word_count > 0:
        lower = int(expected_word_count * (1 - WORD_COUNT_TOLERANCE))
        upper = int(expected_word_count * (1 + WORD_COUNT_TOLERANCE))
        if actual_word_count < lower or actual_word_count > upper:
            logger.warning(
                "Word count %d outside ±10%% of expected %d (range %d-%d)",
                actual_word_count, expected_word_count, lower, upper,
            )

    # Validate monotonic timestamps (AC1)
    for i in range(1, len(all_words)):
        if all_words[i]["start_frame"] < all_words[i - 1]["start_frame"]:
            logger.warning(
                "Non-monotonic timestamp: word '%s' start_frame=%d < previous start_frame=%d",
                all_words[i]["word"],
                all_words[i]["start_frame"],
                all_words[i - 1]["start_frame"],
            )

    # Build DEP-VID-004 output
    transcript_id = f"TR-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"

    dep_vid_004 = {
        "transcript_id": transcript_id,
        "source_audio": voiceover_path.name,
        "model": f"whisper-{WHISPER_MODEL}",
        "language": language,
        "total_duration_sec": round(total_duration_sec, 1),
        "total_frames": total_frames,
        "fps": fps,
        "word_count": actual_word_count,
        "segments": segments,
    }

    return dep_vid_004


# ===========================================================================
# Stage 2: Demucs Stem Separation (DEMUCS_SEPARATION)
# FR-VID-06 §4 Stage 2
# ===========================================================================


def separate_stems(
    voiceover_path: Path,
    output_dir: Path,
    transcript: dict | None = None,
    fps: int = 24,
    language: str = DEFAULT_LANGUAGE,
) -> dict:
    """
    Stage 2: Conditionally run Demucs stem separation.

    FR-VID-06 §4 Stage 2 Steps 1-4.
    If SNR > 20dB: skip Demucs, use original.
    If SNR ≤ 20dB: run Demucs htdemucs_ft, re-run Whisper on clean stem.

    Args:
        voiceover_path: Path to voiceover audio.
        output_dir: Directory for separated stems.
        transcript: Optional existing transcript from Stage 1 (re-run if Demucs used).
        fps: Project FPS.
        language: Whisper language setting.

    Returns:
        Dict with keys: demucs_used, vocals_path, snr_original, snr_separated,
        updated_transcript (if re-transcribed).
    """
    voiceover_path = Path(voiceover_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Compute SNR
    snr_original = compute_snr_db(voiceover_path)
    logger.info("Voiceover SNR: %.1f dB (threshold: %.1f dB)", snr_original, SNR_THRESHOLD_DB)

    result = {
        "demucs_used": False,
        "vocals_path": str(voiceover_path),
        "snr_original_db": round(snr_original, 1),
        "snr_separated_db": None,
        "snr_improvement_db": None,
        "updated_transcript": None,
    }

    # Step 2: If SNR > 20 dB — clean audio, skip Demucs
    if snr_original > SNR_THRESHOLD_DB:
        logger.info("SNR %.1f dB > %.1f dB — skipping Demucs (clean voiceover)", snr_original, SNR_THRESHOLD_DB)
        return result

    # Step 3: Run Demucs htdemucs_ft for vocal isolation
    logger.info("SNR %.1f dB ≤ %.1f dB — running Demucs %s", snr_original, SNR_THRESHOLD_DB, DEMUCS_MODEL)

    demucs_output_dir = output_dir / "demucs"
    cmd = [
        "python", "-m", "demucs",
        "--name", DEMUCS_MODEL,
        "--out", str(demucs_output_dir),
        "--two-stems", "vocals",
        str(voiceover_path),
    ]

    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=120, check=True)
    except subprocess.CalledProcessError as exc:
        logger.error("Demucs failed: %s", exc.stderr[:500] if exc.stderr else str(exc))
        raise RuntimeError(f"DEMUCS_FAILED: {exc}") from exc

    # Locate the separated vocals stem
    stem_name = voiceover_path.stem
    vocals_path = demucs_output_dir / DEMUCS_MODEL / stem_name / "vocals.wav"
    if not vocals_path.exists():
        raise RuntimeError(
            f"DEMUCS_FAILED: Expected vocals stem not found at {vocals_path}"
        )

    # Measure SNR improvement
    snr_separated = compute_snr_db(vocals_path)
    snr_improvement = snr_separated - snr_original

    result["demucs_used"] = True
    result["vocals_path"] = str(vocals_path)
    result["snr_separated_db"] = round(snr_separated, 1)
    result["snr_improvement_db"] = round(snr_improvement, 1)

    logger.info(
        "Demucs complete: SNR improved from %.1f to %.1f dB (+%.1f dB)",
        snr_original, snr_separated, snr_improvement,
    )

    # Step 4: Re-run Whisper on the clean stem for improved accuracy
    logger.info("Re-transcribing clean stem for improved word-level accuracy")
    updated_transcript = transcribe_voiceover(vocals_path, fps=fps, language=language)
    result["updated_transcript"] = updated_transcript

    return result


# ===========================================================================
# Stage 3: Ducking Curve Computation (DUCKING_CURVE_COMPUTE)
# FR-VID-06 §4 Stage 3
# ===========================================================================


def compute_ducking_curve(
    transcript: dict,
    fps: int = 24,
    total_duration_sec: float | None = None,
    ducking_target: float = DEFAULT_DUCKING_TARGET,
    ease_frames: int = EASE_FRAMES,
    pad_before: int = SENTENCE_PAD_BEFORE,
    pad_after: int = SENTENCE_PAD_AFTER,
) -> dict:
    """
    Stage 3: Compute per-frame ducking curve from Whisper transcript.

    FR-VID-06 §4 Stage 3 Steps 1-5.

    Args:
        transcript: DEP-VID-004 Whisper transcript.
        fps: Project frames per second.
        total_duration_sec: Override total duration (else from transcript).
        ducking_target: Volume during voiceover (default 0.15).
        ease_frames: Cosine easing transition length (default 6).
        pad_before: Frames to pad before first word of sentence (default 3).
        pad_after: Frames to pad after last word of sentence (default 6).

    Returns:
        DEP-VID-005 Ducking Curve JSON dict.
    """
    if total_duration_sec is None:
        total_duration_sec = transcript.get("total_duration_sec", 0)

    total_frames = int(total_duration_sec * fps)
    if total_frames <= 0:
        raise ValueError(
            f"DUCKING_INVALID: total_frames={total_frames} "
            f"(duration={total_duration_sec}s, fps={fps})"
        )

    # Step 1: Initialize per-frame array, all values = 1.0 (full music volume)
    curve = [1.0] * total_frames

    # Step 2-3: For each word, mark ducking range. Add sentence padding.
    for segment in transcript.get("segments", []):
        words = segment.get("words", [])
        if not words:
            continue

        # Step 3: Extend ducking with sentence padding
        seg_start = words[0]["start_frame"] - pad_before
        seg_end = words[-1]["end_frame"] + pad_after

        # Step 2: Set ducking target for the full padded range
        for frame in range(max(0, seg_start), min(total_frames, seg_end + 1)):
            curve[frame] = ducking_target

    # Step 4: Apply cosine easing to all transitions
    curve = _apply_cosine_easing(curve, ducking_target, ease_frames, total_frames)

    # Step 5: Validate — all values between 0.0 and 1.0
    for i, val in enumerate(curve):
        curve[i] = max(0.0, min(1.0, val))

    # Build DEP-VID-005 output
    curve_id = f"DC-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"

    dep_vid_005 = {
        "curve_id": curve_id,
        "total_frames": total_frames,
        "fps": fps,
        "ducking_target": ducking_target,
        "ease_frames": ease_frames,
        "pad_before_frames": pad_before,
        "pad_after_frames": pad_after,
        "total_duration_sec": round(total_duration_sec, 1),
        "values": [round(v, 4) for v in curve],
    }

    return dep_vid_005


def _apply_cosine_easing(
    curve: list[float],
    ducking_target: float,
    ease_frames: int,
    total_frames: int,
) -> list[float]:
    """
    Apply cosine easing to transitions between full volume (1.0) and ducking target.

    FR-VID-06 §4 Stage 3 Step 4: "Cosine eased over 6 frames (~250ms at 24fps)
    to prevent jarring volume changes."

    AC3: "transitions span exactly 6 frames and follow a cosine curve (not linear)."
    """
    # Find transition points (edges between ducked and non-ducked regions)
    i = 0
    while i < total_frames:
        # Detect falling edge: 1.0 → ducking_target (duck-in)
        if (
            i < total_frames - 1
            and curve[i] == 1.0
            and curve[i + 1] == ducking_target
        ):
            # Apply cosine ease-in over ease_frames frames
            ease_start = max(0, i + 1 - ease_frames)
            for j in range(ease_frames):
                frame_idx = ease_start + j
                if 0 <= frame_idx < total_frames:
                    # Cosine ease from 1.0 down to ducking_target
                    t = (j + 1) / ease_frames
                    eased = 1.0 - (1.0 - ducking_target) * (1 - math.cos(t * math.pi)) / 2
                    # Only reduce, don't raise values already ducked
                    curve[frame_idx] = min(curve[frame_idx], eased)

        # Detect rising edge: ducking_target → 1.0 (duck-out)
        if (
            i < total_frames - 1
            and curve[i] == ducking_target
            and curve[i + 1] == 1.0
        ):
            # Apply cosine ease-out over ease_frames frames
            for j in range(ease_frames):
                frame_idx = i + 1 + j
                if 0 <= frame_idx < total_frames:
                    # Cosine ease from ducking_target up to 1.0
                    t = (j + 1) / ease_frames
                    eased = ducking_target + (1.0 - ducking_target) * (1 - math.cos(t * math.pi)) / 2
                    # Only raise, don't reduce values already at full
                    curve[frame_idx] = max(curve[frame_idx], eased) if curve[frame_idx] < 1.0 else eased

        i += 1

    return curve


# ===========================================================================
# Full Pipeline Orchestrator
# ===========================================================================


def process_audio(
    voiceover_path: Path,
    music_path: Path,
    output_dir: Path,
    fps: int = 24,
    language: str = DEFAULT_LANGUAGE,
    ducking_target: float = DEFAULT_DUCKING_TARGET,
    expected_video_duration_sec: float | None = None,
    expected_word_count: int | None = None,
    receipt_output_dir: Path | None = None,
) -> dict:
    """
    Execute the complete audio processing pipeline (Stages 1-3) with Gate I
    enforcement and receipt chain writes.

    Top-level entry point called by Pipeline Commander (FR-VID-09).

    Args:
        voiceover_path: DEP-VID-017 — voiceover audio file.
        music_path: DEP-VID-018 — background music file.
        output_dir: Directory for outputs (stems, transcripts, curves).
        fps: Project FPS.
        language: Whisper language.
        ducking_target: Music volume during voiceover (default 0.15).
        expected_video_duration_sec: Expected video duration for Gate I validation.
        expected_word_count: Expected narration word count.
        receipt_output_dir: Directory for receipt chain files.

    Returns:
        Dict with transcript (DEP-VID-004), ducking_curve (DEP-VID-005),
        stems_result, and receipt_chain metadata.
    """
    from .gates.gate_i import run_gate_i
    from .receipt_chain import write_receipt

    voiceover_path = Path(voiceover_path)
    music_path = Path(music_path)
    output_dir = Path(output_dir)
    receipt_dir = Path(receipt_output_dir) if receipt_output_dir else output_dir / "receipts"

    # Gate I enforcement — FR-VID-06 §6
    gate_pass, gate_results = run_gate_i(
        voiceover_path=voiceover_path,
        music_path=music_path,
        language=language,
        ducking_target=ducking_target,
        expected_video_duration_sec=expected_video_duration_sec,
    )

    if not gate_pass:
        failed_qs = [g for g in gate_results if not g["passed"]]
        diagnostics = "; ".join(
            f"Q{g['question']}: {g['diagnostic']}" for g in failed_qs
        )
        raise RuntimeError(f"Gate I FAILED — {diagnostics}")

    logger.info("Gate I PASS — all 4 questions satisfied")

    # Stage 1: Whisper Transcription
    transcript = transcribe_voiceover(
        voiceover_path, fps=fps, language=language,
        expected_word_count=expected_word_count,
    )

    receipt_1 = write_receipt(
        stage_name="WHISPER_TRANSCRIPTION",
        agent_name="audio_engine",
        input_payload={"voiceover": voiceover_path.name, "language": language},
        output_payload={
            "transcript_id": transcript["transcript_id"],
            "word_count": transcript["word_count"],
            "segments_count": len(transcript["segments"]),
        },
        previous_receipt=None,
        output_dir=str(receipt_dir),
    )

    # Stage 2: Demucs Stem Separation (conditional)
    stems_dir = output_dir / "intermediate" / "audio"
    stems_result = separate_stems(
        voiceover_path, stems_dir,
        transcript=transcript, fps=fps, language=language,
    )

    # If Demucs ran and produced updated transcript, use it
    if stems_result["updated_transcript"] is not None:
        transcript = stems_result["updated_transcript"]
        logger.info("Using Demucs-improved transcript (re-transcribed from clean stem)")

    receipt_2 = write_receipt(
        stage_name="DEMUCS_SEPARATION",
        agent_name="audio_engine",
        input_payload={
            "voiceover": voiceover_path.name,
            "snr_original_db": stems_result["snr_original_db"],
        },
        output_payload={
            "demucs_used": stems_result["demucs_used"],
            "snr_separated_db": stems_result["snr_separated_db"],
        },
        previous_receipt=receipt_1,
        output_dir=str(receipt_dir),
    )

    # Stage 3: Ducking Curve Computation
    vo_meta = get_audio_metadata(voiceover_path)
    ducking_curve = compute_ducking_curve(
        transcript, fps=fps,
        total_duration_sec=vo_meta["duration_sec"],
        ducking_target=ducking_target,
    )

    receipt_3 = write_receipt(
        stage_name="DUCKING_CURVE_COMPUTE",
        agent_name="audio_engine",
        input_payload={
            "transcript_id": transcript["transcript_id"],
            "fps": fps,
            "total_duration_sec": vo_meta["duration_sec"],
        },
        output_payload={
            "curve_id": ducking_curve["curve_id"],
            "total_frames": ducking_curve["total_frames"],
        },
        previous_receipt=receipt_2,
        output_dir=str(receipt_dir),
    )

    # Write outputs to disk
    transcript_path = output_dir / "dep_vid_004_transcript.json"
    transcript_path.parent.mkdir(parents=True, exist_ok=True)
    transcript_path.write_text(json.dumps(transcript, indent=2), encoding="utf-8")

    curve_path = output_dir / "dep_vid_005_ducking_curve.json"
    curve_path.write_text(json.dumps(ducking_curve, indent=2), encoding="utf-8")

    return {
        "transcript": transcript,
        "ducking_curve": ducking_curve,
        "stems_result": {
            "demucs_used": stems_result["demucs_used"],
            "vocals_path": stems_result["vocals_path"],
            "snr_original_db": stems_result["snr_original_db"],
            "snr_improvement_db": stems_result["snr_improvement_db"],
        },
        "output_files": {
            "transcript_path": str(transcript_path),
            "ducking_curve_path": str(curve_path),
        },
        "receipt_chain": {
            "final_receipt_id": receipt_3["receipt_id"],
            "chain_length": 3,
            "stages": [
                "WHISPER_TRANSCRIPTION",
                "DEMUCS_SEPARATION",
                "DUCKING_CURVE_COMPUTE",
            ],
        },
    }
