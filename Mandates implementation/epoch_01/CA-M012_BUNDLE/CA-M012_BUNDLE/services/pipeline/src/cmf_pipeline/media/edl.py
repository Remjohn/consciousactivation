from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from ..domain.errors import PipelineSourceLineageError, PipelineValidationError
from ..domain.validation import require_int, require_ref, require_string, reject_noncanonical, semantic_identity
from ..workflow.infrastructure.repository import PipelineRepository
from .source import SOURCE_MEDIA_AUTHORITY, SourceMediaService


class WordBoundaryEdlService:
    def __init__(self, repository: PipelineRepository):
        self.repository = repository
        self.source_media = SourceMediaService(repository)

    def compile(
        self,
        *,
        source_registration_ref: Mapping[str, Any],
        source_path: str | Path,
        expression_moment_ref: Mapping[str, Any],
        words: list[Mapping[str, Any]],
        selections: list[Mapping[str, Any]],
        allow_reorder: bool,
        idempotency_key: str,
    ) -> dict[str, Any]:
        source_ref = require_ref(source_registration_ref, "source_registration_ref")
        source_integrity = self.source_media.verify_source(
            source_registration_ref=source_ref,
            source_path=source_path,
        )
        if source_integrity["source_authority"] != SOURCE_MEDIA_AUTHORITY:
            raise PipelineSourceLineageError("EDL source authority is not sovereign media bytes")
        moment_ref = require_ref(expression_moment_ref, "expression_moment_ref")
        word_map = {}
        for i, word in enumerate(words):
            required = {
                "word_id",
                "text",
                "start_ms",
                "end_ms",
                "speaker_id",
                "protected_tail_ms",
            }
            if not isinstance(word, Mapping) or set(word) != required:
                raise PipelineValidationError(f"words[{i}] invalid")
            word_id = require_string(word["word_id"], "word_id")
            start = require_int(word["start_ms"], "start_ms")
            end = require_int(word["end_ms"], "end_ms", minimum=1)
            if end <= start:
                raise PipelineValidationError("word end must exceed start")
            word_map[word_id] = {
                "word_id": word_id,
                "text": require_string(word["text"], "text"),
                "start_ms": start,
                "end_ms": end,
                "speaker_id": require_string(word["speaker_id"], "speaker_id"),
                "protected_tail_ms": require_int(
                    word["protected_tail_ms"], "protected_tail_ms"
                ),
            }
        entries = []
        output_cursor = 0
        prior_source_start = -1
        for index, selection in enumerate(selections):
            required = {
                "selection_id",
                "start_word_id",
                "end_word_id",
                "function",
                "cut_in_class",
                "cut_out_class",
                "authorized_reorder",
            }
            if not isinstance(selection, Mapping) or set(selection) != required:
                raise PipelineValidationError(f"selections[{index}] invalid")
            start_id = require_string(selection["start_word_id"], "start_word_id")
            end_id = require_string(selection["end_word_id"], "end_word_id")
            if start_id not in word_map or end_id not in word_map:
                raise PipelineValidationError("selection word ID missing")
            start_word = word_map[start_id]
            end_word = word_map[end_id]
            if end_word["end_ms"] <= start_word["start_ms"]:
                raise PipelineValidationError("selection is reversed or empty")
            source_start = start_word["start_ms"]
            source_end = end_word["end_ms"] + end_word["protected_tail_ms"]
            authorized = bool(selection["authorized_reorder"])
            if source_start < prior_source_start and not (allow_reorder and authorized):
                raise PipelineValidationError("source reorder requires explicit authority")
            prior_source_start = source_start
            duration = source_end - source_start
            cut_in = require_string(selection["cut_in_class"], "cut_in_class")
            cut_out = require_string(selection["cut_out_class"], "cut_out_class")
            if cut_in not in {"WORD_BOUNDARY", "SILENCE_BOUNDARY", "AUDIO_EVENT_BOUNDARY"} or cut_out not in {
                "WORD_BOUNDARY",
                "SILENCE_BOUNDARY",
                "AUDIO_EVENT_BOUNDARY",
            }:
                raise PipelineValidationError("unsupported cut class")
            entries.append(
                {
                    "entry_id": require_string(selection["selection_id"], "selection_id"),
                    "source_start_ms": source_start,
                    "source_end_ms": source_end,
                    "output_start_ms": output_cursor,
                    "output_end_ms": output_cursor + duration,
                    "start_word_id": start_id,
                    "end_word_id": end_id,
                    "speaker_id": start_word["speaker_id"],
                    "function": require_string(selection["function"], "function"),
                    "cut_in_class": cut_in,
                    "cut_out_class": cut_out,
                    "authorized_reorder": authorized,
                }
            )
            output_cursor += duration
        if not entries:
            raise PipelineValidationError("EDL must contain at least one entry")
        core = {
            "source_registration_ref": source_ref,
            "source_media_ref": source_integrity["source_media_ref"],
            "source_media_sha256": source_integrity["source_media_sha256"],
            "source_authority": SOURCE_MEDIA_AUTHORITY,
            "source_integrity": source_integrity,
            "expression_moment_ref": moment_ref,
            "entries": entries,
            "output_duration_ms": output_cursor,
            "source_order_preserved": all(
                entries[i]["source_start_ms"] <= entries[i + 1]["source_start_ms"]
                for i in range(len(entries) - 1)
            ),
            "word_boundary_enforced": True,
            "original_talking_head_spine": True,
            "production_authorized": False,
        }
        reject_noncanonical(core)
        edl = {"edl_id": semantic_identity("word-boundary-edl", core), "edl_version": "1.0.0", **core}
        result = self.repository.store_object(
            "word_boundary_edl",
            edl,
            idempotency_key=idempotency_key,
            object_id=edl["edl_id"],
            lifecycle_state="COMPILED",
        )
        self.repository.add_edge(source_ref["object_id"], edl["edl_id"], "source_registration_input")
        self.repository.add_edge(source_integrity["source_media_ref"]["object_id"], edl["edl_id"], "sovereign_source_media_input")
        self.repository.add_edge(moment_ref["object_id"], edl["edl_id"], "expression_moment_input")
        return result
