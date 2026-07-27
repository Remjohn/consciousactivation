"""
Caption & Typography Engine — Word-by-word caption data preparation.

FR-VID-07 §4 Stage 1: Caption Data Preparation

Parses Whisper transcript (DEP-VID-004), detects emphasis words,
assigns words to beats via midpoint rule (TD5), breaks lines at
phrase boundaries (max 2 lines, TD4), applies PSSL color theming,
and produces per-beat caption data (DEP-VID-021) for Remotion rendering.

Technical Decision 1: Captions = React components, not SRT overlays.
Technical Decision 2: Emphasis via keyword list + heuristics.
Technical Decision 3: Safe zone 10-90% x, 55-85% y for 9:16.
Technical Decision 4: Max 2 lines per caption frame.
Technical Decision 5: Word-to-beat assignment uses temporal midpoint.
"""

import logging
import re
from math import floor
from typing import Any, Optional

try:
    from .receipt_chain import write_receipt
except ImportError:
    from receipt_chain import write_receipt


logger = logging.getLogger("cmf.caption_engine")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_STYLE_PRESETS = {"hormozi", "capcut", "cinematic", "minimal"}
VALID_FONT_FAMILIES = {"Inter", "Outfit", "Montserrat"}

# Safe zone for 9:16 mobile content — FR-VID-07 §3 TD3
DEFAULT_SAFE_ZONE = {
    "x_min": 0.10,
    "x_max": 0.90,
    "y_min": 0.55,
    "y_max": 0.85,
}

# Default emphasis scale — FR-VID-07 §3 TD2
DEFAULT_EMPHASIS_SCALE = 1.5

# Max caption lines per frame — FR-VID-07 §3 TD4
MAX_LINES = 2

# Midpoint tolerance — FR-VID-07 §3 TD5: ±125ms (3 frames at 24fps)
MIDPOINT_TOLERANCE_SEC = 0.125

# Minimum display time per word for readability — FR-VID-07 §6 Gate J Q3
MIN_DISPLAY_MS_PER_WORD = 100

# WCAG AA minimum contrast ratio — FR-VID-07 §6 Gate J Q4
WCAG_AA_CONTRAST_RATIO = 4.5

# Power words for emphasis detection — FR-VID-07 §3 TD2
EMPHASIS_KEYWORDS = {
    "never", "always", "everything", "nothing", "secret", "breakthrough",
    "impossible", "incredible", "amazing", "powerful", "critical",
    "essential", "transform", "destroy", "ultimate", "massive",
    "exactly", "absolutely", "guarantee", "proven", "truth",
    "dangerous", "mistake", "warning", "urgent", "immediately",
    "forever", "moment", "reality", "finally", "crucial",
}

# Phrase boundary punctuation for line breaking
PHRASE_BREAK_CHARS = {",", ";", ":", "—", "–", "-"}


# ---------------------------------------------------------------------------
# Emphasis Detection — §3 TD2, AC3
# ---------------------------------------------------------------------------


def detect_emphasis(word: str) -> bool:
    """
    Detect if a word is a "power word" that should receive emphasis styling.

    FR-VID-07 §3 TD2: Keyword list + ALL-CAPS heuristic.

    AC3: "NEVER", "everything", "secret" must all be tagged emphasis: true.
    """
    clean = re.sub(r"[^\w]", "", word).lower()
    if clean in EMPHASIS_KEYWORDS:
        return True
    # ALL-CAPS words of 3+ letters get emphasis
    alpha = re.sub(r"[^\w]", "", word)
    if len(alpha) >= 3 and alpha.isupper():
        return True
    return False


# ---------------------------------------------------------------------------
# Word-to-Beat Assignment — §3 TD5
# ---------------------------------------------------------------------------


def assign_words_to_beats(
    words: list[dict],
    beats: list[dict],
    fps: int = 24,
) -> dict[int, list[dict]]:
    """
    Assign transcript words to beats using the temporal midpoint rule.

    FR-VID-07 §3 TD5: midpoint = (start_sec + end_sec) / 2.
    Word belongs to the beat whose [start_sec, start_sec + duration_sec)
    contains the midpoint. Boundary ties go to the later beat.
    Tolerance: ±125ms.

    Returns: {beat_index: [word_dicts]}
    """
    beat_assignments: dict[int, list[dict]] = {
        b["beat_index"]: [] for b in beats
    }

    # Build beat time ranges
    beat_ranges = []
    for b in beats:
        start = b.get("start_sec", b.get("start_frame", 0) / fps)
        dur = b.get("duration_sec", b.get("duration_frames", 0) / fps)
        beat_ranges.append((b["beat_index"], start, start + dur))

    for w in words:
        midpoint = (w["start_sec"] + w["end_sec"]) / 2
        assigned = False

        for beat_idx, b_start, b_end in beat_ranges:
            if b_start <= midpoint < b_end:
                beat_assignments[beat_idx].append(w)
                assigned = True
                break
            # Boundary tie: midpoint exactly on beat boundary → later beat
            if abs(midpoint - b_start) < 1e-9 and beat_idx > 0:
                beat_assignments[beat_idx].append(w)
                assigned = True
                break

        # Tolerance fallback: ±125ms
        if not assigned:
            best_beat = None
            best_dist = float("inf")
            for beat_idx, b_start, b_end in beat_ranges:
                dist = min(abs(midpoint - b_start), abs(midpoint - b_end))
                if dist < best_dist:
                    best_dist = dist
                    best_beat = beat_idx
            if best_beat is not None and best_dist <= MIDPOINT_TOLERANCE_SEC:
                beat_assignments[best_beat].append(w)

    return beat_assignments


# ---------------------------------------------------------------------------
# Line Breaking — §3 TD4, AC5
# ---------------------------------------------------------------------------


def break_into_lines(
    words: list[dict],
    max_lines: int = MAX_LINES,
) -> list[list[dict]]:
    """
    Break a word list into display lines (max 2 lines per caption frame).

    FR-VID-07 §3 TD4: Line breaks at phrase boundaries (commas, natural
    pauses), not by character count. If no natural break exists, split
    at the midpoint of the word list.

    AC5: 15-word sentence → at most 2 lines at a natural phrase boundary.
    """
    if not words:
        return []

    if len(words) <= max_lines:
        return [words]

    # Find best break point: look for phrase boundary near the middle
    mid = len(words) // 2
    best_break = None
    best_dist = float("inf")

    for i in range(len(words) - 1):
        w_text = words[i]["word"].rstrip()
        has_break = any(w_text.endswith(c) for c in PHRASE_BREAK_CHARS)
        if has_break:
            dist = abs(i - mid)
            if dist < best_dist:
                best_dist = dist
                best_break = i + 1  # break AFTER this word

    # If no phrase boundary found, split at midpoint
    if best_break is None:
        best_break = mid + 1

    line1 = words[:best_break]
    line2 = words[best_break:]

    if max_lines <= 1:
        return [words]

    lines = [line1]
    if line2:
        lines.append(line2)

    return lines[:max_lines]


# ---------------------------------------------------------------------------
# Style Preset Animation Metadata
# ---------------------------------------------------------------------------


def get_style_animation(style_preset: str) -> dict:
    """
    Return animation metadata for the given caption style preset.

    FR-VID-07 §4 Stage 2: Each style produces distinct animation behavior.
    AC2: 4 styles with unique animation classes and DOM structures.
    """
    presets = {
        "hormozi": {
            "animation_class": "caption-hormozi",
            "word_animation": "scale_pop",
            "word_in_effect": "scale(0) → scale(1.0)",
            "word_out_effect": "scale(1.0) → scale(0)",
            "timing": "per_word",
        },
        "capcut": {
            "animation_class": "caption-capcut",
            "word_animation": "highlight_sweep",
            "word_in_effect": "background_accent",
            "word_out_effect": "background_dim",
            "timing": "per_word",
        },
        "cinematic": {
            "animation_class": "caption-cinematic",
            "word_animation": "typewriter_fade",
            "word_in_effect": "opacity(0) → opacity(1)",
            "word_out_effect": "none",
            "timing": "per_word",
            "bar": "lower_third",
        },
        "minimal": {
            "animation_class": "caption-minimal",
            "word_animation": "fade_in_out",
            "word_in_effect": "opacity(0) → opacity(1)",
            "word_out_effect": "opacity(1) → opacity(0)",
            "timing": "per_group",
        },
    }
    return presets.get(style_preset, presets["minimal"])


# ---------------------------------------------------------------------------
# Color Contrast — WCAG AA utility
# ---------------------------------------------------------------------------


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert #RRGGBB to (R, G, B)."""
    hex_color = hex_color.lstrip("#")
    return (
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )


def _relative_luminance(r: int, g: int, b: int) -> float:
    """WCAG 2.1 relative luminance formula."""
    def linearize(c: int) -> float:
        s = c / 255.0
        return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def compute_contrast_ratio(color1: str, color2: str) -> float:
    """
    Compute WCAG 2.1 contrast ratio between two hex colors.

    FR-VID-07 §6 Gate J Q4: Minimum 4.5:1 for AA compliance.
    """
    l1 = _relative_luminance(*_hex_to_rgb(color1))
    l2 = _relative_luminance(*_hex_to_rgb(color2))
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# ---------------------------------------------------------------------------
# Caption Data Preparation — Full Pipeline
# ---------------------------------------------------------------------------


def extract_words_from_transcript(transcript: dict) -> list[dict]:
    """
    Extract flat word list from DEP-VID-004 Whisper transcript.

    Each word gets: word, start_sec, end_sec, start_frame, end_frame, confidence.
    """
    words = []
    for segment in transcript.get("segments", []):
        for w in segment.get("words", []):
            words.append({
                "word": w["word"],
                "start_sec": w["start_sec"],
                "end_sec": w["end_sec"],
                "start_frame": w.get("start_frame", int(w["start_sec"] * transcript.get("fps", 24))),
                "end_frame": w.get("end_frame", int(w["end_sec"] * transcript.get("fps", 24))),
                "confidence": w.get("confidence", 0.0),
            })
    return words


def prepare_caption_data(
    transcript: dict,
    beats: list[dict],
    config: dict,
    fps: int = 24,
) -> dict:
    """
    Full caption data preparation pipeline.

    FR-VID-07 §4 Stage 1:
    1. Parse Whisper transcript → flat word array.
    2. Run emphasis detection on each word.
    3. Assign words to beats via midpoint rule.
    4. Break word groups into display lines (max 2).
    5. Apply style preset animation metadata.
    6. Apply PSSL color theme.
    7. Apply safe zone positioning.

    Returns DEP-VID-021 compatible output.
    """
    style_preset = config.get("style_preset", "minimal")
    if style_preset not in VALID_STYLE_PRESETS:
        style_preset = "minimal"

    font_family = config.get("font_family", "Inter")
    font_size_base = config.get("font_size_base", 42)
    emphasis_scale = config.get("emphasis_scale", DEFAULT_EMPHASIS_SCALE)
    font_size_emphasis = config.get(
        "font_size_emphasis", int(font_size_base * emphasis_scale)
    )
    color_theme = config.get("color_theme", {
        "base_text_color": "#FFFFFF",
        "emphasis_color": "#E74C3C",
        "shadow_color": "#000000",
    })
    safe_zone = dict(config.get("safe_zone", DEFAULT_SAFE_ZONE))
    max_lines = config.get("max_lines", MAX_LINES)

    # Step 1: Extract words
    words = extract_words_from_transcript(transcript)

    # Step 2: Emphasis detection
    for w in words:
        w["emphasis"] = detect_emphasis(w["word"])

    # Step 3: Word-to-beat assignment
    beat_words = assign_words_to_beats(words, beats, fps)

    # Steps 4-7: Build per-beat caption data
    beat_captions = []
    for beat in beats:
        beat_idx = beat["beat_index"]
        bw = beat_words.get(beat_idx, [])

        lines_raw = break_into_lines(bw, max_lines)
        lines = []
        for line_idx, line_words in enumerate(lines_raw):
            caption_words = []
            for w in line_words:
                caption_words.append({
                    "word": w["word"],
                    "start_frame": w["start_frame"],
                    "end_frame": w["end_frame"],
                    "emphasis": w["emphasis"],
                })
            lines.append({
                "line_index": line_idx,
                "words": caption_words,
            })

        beat_captions.append({
            "beat_index": beat_idx,
            "style_preset": style_preset,
            "lines": lines,
            "position": {
                "anchor": "bottom-center",
                "safe_zone": safe_zone,
            },
            "color_theme": color_theme,
            "animation": get_style_animation(style_preset),
        })

    total_frames = transcript.get("total_frames", 0)
    if not total_frames and beats:
        total_frames = max(
            b.get("start_frame", 0) + b.get("duration_frames", 0)
            for b in beats
        )

    return {
        "video_id": transcript.get("transcript_id", ""),
        "project_id": config.get("project_id", ""),
        "fps": fps,
        "total_frames": total_frames,
        "font_family": font_family,
        "font_size_base": font_size_base,
        "font_size_emphasis": font_size_emphasis,
        "beats": beat_captions,
        "status": "PREPARED",
    }


# ---------------------------------------------------------------------------
# Pipeline Entry Point with Receipt
# ---------------------------------------------------------------------------


def run_caption_prepare(
    transcript: dict,
    beats: list[dict],
    config: dict,
    fps: int = 24,
    previous_receipt: Optional[dict] = None,
    receipt_output_dir: Optional[str] = None,
) -> tuple[dict, dict]:
    """
    Run caption data preparation with receipt chain.

    Returns:
        (caption_data, receipt)
    """
    caption_data = prepare_caption_data(transcript, beats, config, fps)

    output_dir = receipt_output_dir or "."
    receipt = write_receipt(
        stage_name="CAPTION_PREPARE",
        agent_name="caption_engine",
        input_payload={
            "word_count": sum(
                len(line["words"])
                for beat in caption_data["beats"]
                for line in beat["lines"]
            ),
            "beat_count": len(caption_data["beats"]),
            "style_preset": config.get("style_preset", "minimal"),
        },
        output_payload={
            "status": caption_data["status"],
            "total_frames": caption_data["total_frames"],
        },
        previous_receipt=previous_receipt,
        output_dir=output_dir,
    )

    return caption_data, receipt
