"""
Caption Engine Test Suite — FR-VID-07

Tests emphasis detection, word-to-beat assignment (midpoint rule),
line breaking, style presets, color contrast, and full pipeline.

Maps to FR-VID-07 §8 AC1-AC5, §6 Gate J, §3 Technical Decisions.
"""

import tempfile
from math import floor

from caption_engine import (
    detect_emphasis,
    assign_words_to_beats,
    break_into_lines,
    get_style_animation,
    compute_contrast_ratio,
    extract_words_from_transcript,
    prepare_caption_data,
    run_caption_prepare,
    VALID_STYLE_PRESETS,
    DEFAULT_SAFE_ZONE,
    MAX_LINES,
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
    """Build a minimal DEP-VID-004 transcript from a flat word list."""
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
    """Build beat array with uniform durations."""
    beats = []
    for i in range(count):
        start = i * duration_sec
        frames = int(duration_sec * fps)
        beats.append({
            "beat_index": i,
            "start_sec": start,
            "duration_sec": duration_sec,
            "start_frame": int(start * fps),
            "duration_frames": frames,
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


# ===================================================================
# Emphasis Detection — AC3
# ===================================================================


class TestEmphasisDetection:
    def test_ac3_never(self):
        """AC3: 'NEVER' must be tagged emphasis: true."""
        assert detect_emphasis("NEVER") is True

    def test_ac3_everything(self):
        """AC3: 'everything' must be tagged emphasis: true."""
        assert detect_emphasis("everything") is True

    def test_ac3_secret(self):
        """AC3: 'secret' must be tagged emphasis: true."""
        assert detect_emphasis("secret") is True

    def test_all_caps_3_plus(self):
        """ALL-CAPS words of 3+ letters get emphasis."""
        assert detect_emphasis("WOW") is True
        assert detect_emphasis("HUGE") is True

    def test_short_caps_no_emphasis(self):
        """Short ALL-CAPS (< 3 chars) don't get emphasis."""
        assert detect_emphasis("OK") is False

    def test_normal_word_no_emphasis(self):
        assert detect_emphasis("the") is False
        assert detect_emphasis("and") is False

    def test_punctuation_stripped(self):
        """Punctuation doesn't affect keyword match."""
        assert detect_emphasis("NEVER,") is True
        assert detect_emphasis("secret!") is True

    def test_keyword_case_insensitive(self):
        assert detect_emphasis("Breakthrough") is True
        assert detect_emphasis("IMPOSSIBLE") is True


# ===================================================================
# Word-to-Beat Assignment — TD5
# ===================================================================


class TestWordToBeatAssignment:
    def test_midpoint_rule_basic(self):
        """Word midpoint within beat range → assigned to that beat."""
        words = [
            _make_word("hello", 0.5, 1.0),  # midpoint 0.75 → beat 0 [0, 3)
            _make_word("world", 3.5, 4.0),  # midpoint 3.75 → beat 1 [3, 6)
        ]
        beats = _make_beats(count=3, duration_sec=3.0)
        assignments = assign_words_to_beats(words, beats)
        assert len(assignments[0]) == 1
        assert assignments[0][0]["word"] == "hello"
        assert len(assignments[1]) == 1
        assert assignments[1][0]["word"] == "world"

    def test_midpoint_boundary_tie(self):
        """Midpoint exactly on beat boundary → assign to later beat."""
        words = [
            _make_word("boundary", 2.5, 3.5),  # midpoint 3.0 exactly on beat 1 start
        ]
        beats = _make_beats(count=3, duration_sec=3.0)
        assignments = assign_words_to_beats(words, beats)
        # Should go to beat 1 (later beat)
        assert len(assignments[1]) == 1

    def test_tolerance_fallback(self):
        """Word just outside beat range but within ±125ms tolerance."""
        words = [
            _make_word("near", 8.9, 9.1),  # midpoint 9.0, beats end at 9.0
        ]
        beats = _make_beats(count=3, duration_sec=3.0)  # [0,3) [3,6) [6,9)
        assignments = assign_words_to_beats(words, beats)
        # Should fall back via tolerance to beat 2
        assigned_count = sum(len(v) for v in assignments.values())
        assert assigned_count == 1

    def test_multiple_words_same_beat(self):
        words = [
            _make_word("word1", 0.0, 0.5),
            _make_word("word2", 0.5, 1.0),
            _make_word("word3", 1.0, 1.5),
        ]
        beats = _make_beats(count=2, duration_sec=3.0)
        assignments = assign_words_to_beats(words, beats)
        assert len(assignments[0]) == 3
        assert len(assignments[1]) == 0


# ===================================================================
# Line Breaking — TD4, AC5
# ===================================================================


class TestLineBreaking:
    def test_ac5_15_words_max_2_lines(self):
        """AC5: 15-word sentence → at most 2 lines."""
        words = [_make_word(f"word{i}", i * 0.3, (i + 1) * 0.3) for i in range(15)]
        lines = break_into_lines(words)
        assert len(lines) <= 2
        total = sum(len(l) for l in lines)
        assert total == 15

    def test_short_sentence_one_line(self):
        words = [_make_word("hi", 0, 0.5), _make_word("there", 0.5, 1.0)]
        lines = break_into_lines(words)
        assert len(lines) == 1

    def test_phrase_boundary_break(self):
        """Break at comma when present near midpoint."""
        words = [
            _make_word("before", 0, 0.5),
            _make_word("middle,", 0.5, 1.0),  # comma = phrase boundary
            _make_word("after", 1.0, 1.5),
            _make_word("end", 1.5, 2.0),
        ]
        lines = break_into_lines(words)
        assert len(lines) == 2
        # Break after "middle," (the comma word)
        assert lines[0][-1]["word"] == "middle,"

    def test_empty_input(self):
        lines = break_into_lines([])
        assert lines == []

    def test_single_word(self):
        words = [_make_word("solo", 0, 1)]
        lines = break_into_lines(words)
        assert len(lines) == 1
        assert len(lines[0]) == 1

    def test_no_phrase_boundary_splits_at_midpoint(self):
        """Without punctuation, splits at the midpoint of word count."""
        words = [_make_word(f"w{i}", i * 0.2, (i + 1) * 0.2) for i in range(6)]
        lines = break_into_lines(words)
        assert len(lines) == 2


# ===================================================================
# Style Presets — AC2
# ===================================================================


class TestStylePresets:
    def test_ac2_four_distinct_styles(self):
        """AC2: 4 styles with unique animation classes."""
        classes = set()
        for preset in VALID_STYLE_PRESETS:
            anim = get_style_animation(preset)
            assert "animation_class" in anim
            classes.add(anim["animation_class"])
        assert len(classes) == 4

    def test_hormozi_scale_pop(self):
        anim = get_style_animation("hormozi")
        assert anim["word_animation"] == "scale_pop"

    def test_capcut_highlight(self):
        anim = get_style_animation("capcut")
        assert anim["word_animation"] == "highlight_sweep"

    def test_cinematic_lower_third(self):
        anim = get_style_animation("cinematic")
        assert anim.get("bar") == "lower_third"

    def test_minimal_fade(self):
        anim = get_style_animation("minimal")
        assert anim["word_animation"] == "fade_in_out"

    def test_unknown_style_falls_back(self):
        anim = get_style_animation("nonexistent")
        assert anim["animation_class"] == "caption-minimal"


# ===================================================================
# Color Contrast — WCAG AA
# ===================================================================


class TestColorContrast:
    def test_black_white_max_contrast(self):
        ratio = compute_contrast_ratio("#FFFFFF", "#000000")
        assert ratio >= 21.0

    def test_same_color_no_contrast(self):
        ratio = compute_contrast_ratio("#FF0000", "#FF0000")
        assert ratio == 1.0

    def test_wcag_aa_passes(self):
        """White text on black shadow > 4.5:1."""
        ratio = compute_contrast_ratio("#FFFFFF", "#000000")
        assert ratio >= 4.5

    def test_low_contrast_fails(self):
        """Light gray on white < 4.5:1."""
        ratio = compute_contrast_ratio("#CCCCCC", "#FFFFFF")
        assert ratio < 4.5


# ===================================================================
# Word Sync — AC1
# ===================================================================


class TestWordSync:
    def test_ac1_frame_accuracy(self):
        """AC1: Each word's visible frame range matches Whisper timestamp ±1 frame."""
        words = [
            _make_word("This", 0.0, 0.4),
            _make_word("is", 0.4, 0.6),
            _make_word("a", 0.6, 0.7),
            _make_word("test", 0.7, 1.2),
        ]
        transcript = _make_transcript(words)
        beats = _make_beats(count=1, duration_sec=2.0)
        config = _make_config()

        result = prepare_caption_data(transcript, beats, config)
        beat_cap = result["beats"][0]

        all_words = [w for line in beat_cap["lines"] for w in line["words"]]
        assert len(all_words) == 4

        for orig, cap in zip(words, all_words):
            assert abs(cap["start_frame"] - orig["start_frame"]) <= 1
            assert abs(cap["end_frame"] - orig["end_frame"]) <= 1


# ===================================================================
# Safe Zone — AC4
# ===================================================================


class TestSafeZone:
    def test_ac4_default_safe_zone(self):
        """AC4: Default safe zone is 10-90% x, 55-85% y."""
        words = [_make_word("test", 0.0, 0.5)]
        transcript = _make_transcript(words)
        beats = _make_beats(count=1, duration_sec=1.0)
        config = _make_config()

        result = prepare_caption_data(transcript, beats, config)
        pos = result["beats"][0]["position"]
        sz = pos["safe_zone"]

        assert sz["x_min"] == 0.10
        assert sz["x_max"] == 0.90
        assert sz["y_min"] == 0.55
        assert sz["y_max"] == 0.85

    def test_custom_safe_zone(self):
        words = [_make_word("test", 0.0, 0.5)]
        transcript = _make_transcript(words)
        beats = _make_beats(count=1, duration_sec=1.0)
        config = _make_config()
        config["safe_zone"] = {"x_min": 0.15, "x_max": 0.85, "y_min": 0.60, "y_max": 0.80}

        result = prepare_caption_data(transcript, beats, config)
        sz = result["beats"][0]["position"]["safe_zone"]
        assert sz["x_min"] == 0.15


# ===================================================================
# Full Pipeline
# ===================================================================


class TestFullPipeline:
    def test_prepare_caption_data(self):
        words = [
            _make_word("Nobody", 0.0, 0.4),
            _make_word("tells", 0.4, 0.8),
            _make_word("you", 0.8, 1.0),
            _make_word("the", 1.0, 1.2),
            _make_word("secret", 1.2, 1.8),  # emphasis keyword
        ]
        transcript = _make_transcript(words)
        beats = _make_beats(count=1, duration_sec=3.0)
        config = _make_config()

        result = prepare_caption_data(transcript, beats, config)
        assert result["status"] == "PREPARED"
        assert result["fps"] == 24
        assert result["font_family"] == "Inter"
        assert len(result["beats"]) == 1

        # Check emphasis on "secret"
        all_words = [w for line in result["beats"][0]["lines"] for w in line["words"]]
        secret_word = [w for w in all_words if w["word"] == "secret"]
        assert len(secret_word) == 1
        assert secret_word[0]["emphasis"] is True

    def test_multi_beat_distribution(self):
        words = [
            _make_word("beat0", 1.0, 1.5),   # midpoint 1.25 → beat 0 [0,3)
            _make_word("beat1", 4.0, 4.5),   # midpoint 4.25 → beat 1 [3,6)
            _make_word("beat2", 7.0, 7.5),   # midpoint 7.25 → beat 2 [6,9)
        ]
        transcript = _make_transcript(words)
        beats = _make_beats(count=3, duration_sec=3.0)
        config = _make_config()

        result = prepare_caption_data(transcript, beats, config)
        for i in range(3):
            beat_words = [
                w for line in result["beats"][i]["lines"] for w in line["words"]
            ]
            assert len(beat_words) == 1
            assert beat_words[0]["word"] == f"beat{i}"

    def test_invalid_style_falls_back(self):
        words = [_make_word("test", 0, 0.5)]
        transcript = _make_transcript(words)
        beats = _make_beats(count=1, duration_sec=1.0)
        config = _make_config()
        config["style_preset"] = "invalid_style"

        result = prepare_caption_data(transcript, beats, config)
        assert result["beats"][0]["style_preset"] == "minimal"


# ===================================================================
# Receipt Chain
# ===================================================================


class TestCaptionReceipt:
    def test_receipt_emitted(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            words = [_make_word("test", 0.0, 0.5)]
            transcript = _make_transcript(words)
            beats = _make_beats(count=1, duration_sec=1.0)
            config = _make_config()

            result, receipt = run_caption_prepare(
                transcript, beats, config, receipt_output_dir=tmpdir
            )
            assert receipt["stage_name"] == "CAPTION_PREPARE"
            assert receipt["agent_name"] == "caption_engine"
            assert result["status"] == "PREPARED"

    def test_receipt_chains(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            words = [_make_word("test", 0.0, 0.5)]
            transcript = _make_transcript(words)
            beats = _make_beats(count=1, duration_sec=1.0)
            config = _make_config()

            r1_result, r1 = run_caption_prepare(
                transcript, beats, config, receipt_output_dir=tmpdir
            )
            r2_result, r2 = run_caption_prepare(
                transcript, beats, config,
                previous_receipt=r1, receipt_output_dir=tmpdir,
            )
            assert r2["previous_receipt_hash"] != "GENESIS"
