"""
Gate J — Pre-Caption Constraint Network (Typography Quality Assurance)

FR-VID-07 §6 Skill Definition

Four validation questions that MUST all pass before rendering captions.
Each function returns: (passed: bool, diagnostic: str)

Build Prompt Rule 7: These are executable validation functions, NOT
documentation-only comments.
"""

from typing import Optional

try:
    from .caption_engine import (
        compute_contrast_ratio,
        WCAG_AA_CONTRAST_RATIO,
        MIN_DISPLAY_MS_PER_WORD,
        DEFAULT_SAFE_ZONE,
    )
except ImportError:
    from caption_engine import (
        compute_contrast_ratio,
        WCAG_AA_CONTRAST_RATIO,
        MIN_DISPLAY_MS_PER_WORD,
        DEFAULT_SAFE_ZONE,
    )


# ---------------------------------------------------------------------------
# Q1: Timestamp Integrity
# FR-VID-07 §6 Gate J Q1
# ---------------------------------------------------------------------------


def check_timestamp_integrity(
    caption_data: dict,
    total_frames: int,
) -> tuple[bool, str]:
    """
    Gate J Q1: Are all word timestamps monotonically increasing
    and within the video's frame range?

    A single out-of-order timestamp produces a caption flash or
    invisible word.
    """
    violations = []

    for beat in caption_data.get("beats", []):
        beat_idx = beat["beat_index"]
        prev_end = -1

        for line in beat.get("lines", []):
            for w in line.get("words", []):
                sf = w["start_frame"]
                ef = w["end_frame"]

                if sf < 0 or ef < 0:
                    violations.append(
                        f"beat[{beat_idx}] word '{w['word']}': "
                        f"negative frame ({sf}, {ef})"
                    )
                if ef > total_frames:
                    violations.append(
                        f"beat[{beat_idx}] word '{w['word']}': "
                        f"end_frame {ef} > total_frames {total_frames}"
                    )
                if sf > ef:
                    violations.append(
                        f"beat[{beat_idx}] word '{w['word']}': "
                        f"start_frame {sf} > end_frame {ef}"
                    )
                if sf < prev_end:
                    violations.append(
                        f"beat[{beat_idx}] word '{w['word']}': "
                        f"start_frame {sf} < previous end_frame {prev_end} "
                        f"(not monotonically increasing)"
                    )
                prev_end = ef

    if violations:
        return False, f"TIMESTAMP_INTEGRITY_FAILED: {'; '.join(violations[:5])}"
    return True, "Timestamp integrity verified."


# ---------------------------------------------------------------------------
# Q2: Safe Zone Verification
# FR-VID-07 §6 Gate J Q2
# ---------------------------------------------------------------------------


def check_safe_zone(
    caption_data: dict,
    safe_zone: Optional[dict] = None,
) -> tuple[bool, str]:
    """
    Gate J Q2: Do all caption positions fall within the safe zone
    (10-90% width, 55-85% height for 9:16)?

    FR-VID-07 §3 TD3: Mobile platforms overlay UI chrome at screen edges.
    """
    sz = safe_zone or DEFAULT_SAFE_ZONE

    violations = []
    for beat in caption_data.get("beats", []):
        beat_idx = beat["beat_index"]
        pos = beat.get("position", {})
        beat_sz = pos.get("safe_zone", {})

        if not beat_sz:
            violations.append(f"beat[{beat_idx}]: missing safe_zone definition")
            continue

        if beat_sz.get("x_min", 0) < sz["x_min"]:
            violations.append(
                f"beat[{beat_idx}]: x_min {beat_sz['x_min']} < {sz['x_min']}"
            )
        if beat_sz.get("x_max", 1) > sz["x_max"]:
            violations.append(
                f"beat[{beat_idx}]: x_max {beat_sz['x_max']} > {sz['x_max']}"
            )
        if beat_sz.get("y_min", 0) < sz["y_min"]:
            violations.append(
                f"beat[{beat_idx}]: y_min {beat_sz['y_min']} < {sz['y_min']}"
            )
        if beat_sz.get("y_max", 1) > sz["y_max"]:
            violations.append(
                f"beat[{beat_idx}]: y_max {beat_sz['y_max']} > {sz['y_max']}"
            )

    if violations:
        return False, f"SAFE_ZONE_VIOLATION: {'; '.join(violations[:5])}"
    return True, "Safe zone verification passed."


# ---------------------------------------------------------------------------
# Q3: Readability Check
# FR-VID-07 §6 Gate J Q3
# ---------------------------------------------------------------------------


def check_readability(
    caption_data: dict,
    fps: int = 24,
    min_ms_per_word: int = MIN_DISPLAY_MS_PER_WORD,
) -> tuple[bool, str]:
    """
    Gate J Q3: At the selected font size, can the longest caption line
    be read in the time it's displayed (minimum 100ms per word)?

    A 6-word line displayed for 300ms or less is physically impossible
    to read.
    """
    violations = []

    for beat in caption_data.get("beats", []):
        beat_idx = beat["beat_index"]
        for line in beat.get("lines", []):
            words = line.get("words", [])
            if not words:
                continue

            word_count = len(words)
            first_start = words[0]["start_frame"]
            last_end = words[-1]["end_frame"]
            display_frames = last_end - first_start

            if display_frames <= 0:
                violations.append(
                    f"beat[{beat_idx}] line[{line['line_index']}]: "
                    f"zero or negative display duration"
                )
                continue

            display_ms = (display_frames / fps) * 1000
            ms_per_word = display_ms / word_count

            if ms_per_word < min_ms_per_word:
                violations.append(
                    f"beat[{beat_idx}] line[{line['line_index']}]: "
                    f"{word_count} words in {display_ms:.0f}ms "
                    f"({ms_per_word:.0f}ms/word < {min_ms_per_word}ms minimum)"
                )

    if violations:
        return False, f"READABILITY_FAILED: {'; '.join(violations[:5])}"
    return True, "Readability check passed."


# ---------------------------------------------------------------------------
# Q4: Color Contrast
# FR-VID-07 §6 Gate J Q4
# ---------------------------------------------------------------------------


def check_color_contrast(
    caption_data: dict,
    min_contrast: float = WCAG_AA_CONTRAST_RATIO,
) -> tuple[bool, str]:
    """
    Gate J Q4: Does the caption text color provide sufficient contrast
    (WCAG AA: 4.5:1 minimum) against the shadow/background color?

    Captions are overlaid on varying backgrounds — the shadow color
    serves as the guaranteed minimum contrast partner.
    """
    violations = []

    for beat in caption_data.get("beats", []):
        beat_idx = beat["beat_index"]
        theme = beat.get("color_theme", {})

        base_color = theme.get("base_text_color", "#FFFFFF")
        shadow_color = theme.get("shadow_color", "#000000")
        emphasis_color = theme.get("emphasis_color", "#E74C3C")

        # Check base text vs shadow
        base_ratio = compute_contrast_ratio(base_color, shadow_color)
        if base_ratio < min_contrast:
            violations.append(
                f"beat[{beat_idx}]: base text '{base_color}' vs shadow "
                f"'{shadow_color}' contrast {base_ratio:.2f}:1 < {min_contrast}:1"
            )

        # Check emphasis vs shadow
        emphasis_ratio = compute_contrast_ratio(emphasis_color, shadow_color)
        if emphasis_ratio < min_contrast:
            violations.append(
                f"beat[{beat_idx}]: emphasis '{emphasis_color}' vs shadow "
                f"'{shadow_color}' contrast {emphasis_ratio:.2f}:1 < {min_contrast}:1"
            )

    if violations:
        return False, f"COLOR_CONTRAST_FAILED: {'; '.join(violations[:5])}"
    return True, "Color contrast check passed."


# ---------------------------------------------------------------------------
# Gate J Runner
# ---------------------------------------------------------------------------


def run_gate_j(
    caption_data: dict,
    total_frames: int,
    fps: int = 24,
    safe_zone: Optional[dict] = None,
) -> dict:
    """
    Run all 4 Gate J questions.

    Returns:
        {
            "gate": "J",
            "passed": bool,
            "results": [
                {"question": 1, "passed": bool, "diagnostic": str},
                ...
            ]
        }
    """
    checks = [
        (1, check_timestamp_integrity(caption_data, total_frames)),
        (2, check_safe_zone(caption_data, safe_zone)),
        (3, check_readability(caption_data, fps)),
        (4, check_color_contrast(caption_data)),
    ]

    results = []
    all_passed = True
    for q_num, (passed, diagnostic) in checks:
        results.append({
            "question": q_num,
            "passed": passed,
            "diagnostic": diagnostic,
        })
        if not passed:
            all_passed = False

    return {
        "gate": "J",
        "passed": all_passed,
        "results": results,
    }
