from __future__ import annotations
import json
import re
from typing import Any


class TranscriptFormatError(RuntimeError):
    pass


def load_pre_aligned_transcript(raw: bytes) -> tuple[list[dict], list[dict]]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise TranscriptFormatError(f"pre-aligned transcript is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict) or set(payload) != {"words", "speaker_segments"}:
        raise TranscriptFormatError(
            "pre-aligned transcript must be an object with exactly 'words' and 'speaker_segments'"
        )
    return payload["words"], payload["speaker_segments"]


# NOTE: earlier drafts of this parser used a single regex with a nested
# quantifier -- `((?:.+\n?)+?)(?=\n\d+\s*\n|\Z)` -- to capture each cue's text
# lines up to the next cue. That pattern has catastrophic backtracking: on a
# real multi-line, multi-cue SRT file it hung indefinitely (confirmed via the
# verification harness -- a 3-cue fixture never returned within a 15s
# timeout). Splitting on blank-line boundaries first and parsing each block
# with a single anchored match is linear in input size and has no
# backtracking ambiguity.
_TIMESTAMP_LINE_RE = re.compile(
    r"^\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})"
)


def _ts_to_ms(h: str, m: str, s: str, ms: str) -> int:
    return ((int(h) * 3600 + int(m) * 60 + int(s)) * 1000) + int(ms)


def _parse_cues(text: str) -> list[dict[str, Any]]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    cues = []
    for block in re.split(r"\n\s*\n", normalized):
        lines = [ln for ln in block.split("\n") if ln.strip() != ""]
        if not lines:
            continue
        offset = 1 if lines[0].strip().isdigit() else 0
        if offset >= len(lines):
            continue
        match = _TIMESTAMP_LINE_RE.match(lines[offset])
        if not match:
            continue
        start_ms = _ts_to_ms(*match.group(1, 2, 3, 4))
        end_ms = _ts_to_ms(*match.group(5, 6, 7, 8))
        content = " ".join(ln.strip() for ln in lines[offset + 1:] if ln.strip())
        if content:
            cues.append({"start_ms": start_ms, "end_ms": end_ms, "text": content})
    cues.sort(key=lambda c: c["start_ms"])
    for prior, cue in zip(cues, cues[1:]):
        if cue["start_ms"] < prior["end_ms"]:
            raise TranscriptFormatError(
                "overlapping SRT cues imply undeclared multi-speaker content; "
                "not supported by single-speaker even-split ingestion"
            )
    return cues


def parse_srt_transcript(raw: bytes, *, speaker_id: str) -> tuple[list[dict], list[dict]]:
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise TranscriptFormatError(f"SRT file is not valid UTF-8: {exc}") from exc
    cues = _parse_cues(text)
    if not cues:
        raise TranscriptFormatError("SRT file contains no parseable cues")
    words: list[dict] = []
    segments: list[dict] = []
    index = 0
    for cue_i, cue in enumerate(cues):
        tokens = cue["text"].split()
        span = cue["end_ms"] - cue["start_ms"]
        per_word = span / len(tokens)
        cursor = cue["start_ms"]
        for pos, token in enumerate(tokens):
            is_last = pos == len(tokens) - 1
            end = cue["end_ms"] if is_last else cue["start_ms"] + round(per_word * (pos + 1))
            end = max(end, cursor + 1)
            words.append({
                "word_id": f"srt-w-{index:05d}",
                "index": index,
                "text": token,
                "start_ms": cursor,
                "end_ms": end,
                "speaker_id": speaker_id,
                "speaker_state": "RESOLVED",
                "epistemic_state": "INFERRED",
                "tag_refs": [],
                "event_refs": [],
            })
            cursor = end
            index += 1
        segments.append({
            "segment_id": f"srt-seg-{cue_i:04d}",
            "start_ms": cue["start_ms"],
            "end_ms": cue["end_ms"],
            "speaker_id": speaker_id,
            "speaker_state": "RESOLVED",
        })
    return words, segments
