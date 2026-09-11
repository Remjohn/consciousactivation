from __future__ import annotations

import json
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any, Mapping

from ca_contracts import canonical_sha256

from ..domain.errors import PipelineSourceIntegrityError, PipelineSourceLineageError, PipelineValidationError
from ..domain.validation import (
    immutable_ref,
    require_int,
    require_ref,
    require_sha,
    require_string,
    reject_noncanonical,
    semantic_identity,
)
from ..workflow.infrastructure.repository import PipelineRepository
from .source import SOURCE_MEDIA_AUTHORITY, SourceMediaService, ffprobe_media

EVIDENCE_MOMENT_VERSION = "1.0.0"
EVIDENCE_MOMENT_OBJECT_TYPE = "evidence_moment"
MICROSECOND_TIME_UNIT = "MICROSECOND"


def _probe_source_streams(path: str | Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source = Path(path)
    if not source.is_file():
        raise PipelineSourceIntegrityError("source media is missing")

    process = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_streams",
            "-show_format",
            "-of",
            "json",
            str(source),
        ],
        text=True,
        capture_output=True,
    )
    if process.returncode != 0:
        raise PipelineValidationError(f"ffprobe failed: {process.stderr.strip()}")

    try:
        payload = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise PipelineValidationError("ffprobe returned invalid JSON") from exc

    streams: list[dict[str, Any]] = []
    for ordinal, raw in enumerate(payload.get("streams", [])):
        time_base_raw = str(raw.get("time_base") or "")
        if "/" not in time_base_raw:
            raise PipelineValidationError(
                f"streams[{ordinal}].time_base is missing or invalid"
            )
        numerator_raw, denominator_raw = time_base_raw.split("/", 1)
        try:
            numerator = int(numerator_raw)
            denominator = int(denominator_raw)
        except ValueError as exc:
            raise PipelineValidationError(
                f"streams[{ordinal}].time_base is not an integer rational"
            ) from exc

        duration_raw = raw.get("duration")
        duration_seconds = None
        if duration_raw not in (None, "", "N/A"):
            try:
                duration_seconds = Fraction(str(duration_raw))
            except (ValueError, ZeroDivisionError) as exc:
                raise PipelineValidationError(
                    f"streams[{ordinal}].duration is invalid"
                ) from exc

        streams.append(
            {
                "ordinal": ordinal,
                "stream_index": int(raw.get("index") if raw.get("index") is not None else ordinal),
                "codec_type": str(raw.get("codec_type") or "unknown"),
                "timebase": {"numerator": numerator, "denominator": denominator},
                "duration_seconds": duration_seconds,
            }
        )

    try:
        format_duration = (
            Fraction(str(payload.get("format", {}).get("duration")))
            if payload.get("format", {}).get("duration") not in (None, "", "N/A")
            else None
        )
    except (ValueError, ZeroDivisionError) as exc:
        raise PipelineValidationError("format.duration is invalid") from exc

    return streams, {"duration_seconds": format_duration}


def _normalize_timebase(value: Any) -> dict[str, int]:
    if not isinstance(value, Mapping) or set(value) != {"numerator", "denominator"}:
        raise PipelineValidationError("timebase must contain exactly ['denominator', 'numerator']")
    numerator = require_int(value["numerator"], "timebase.numerator", minimum=1)
    denominator = require_int(value["denominator"], "timebase.denominator", minimum=1)
    return {"numerator": numerator, "denominator": denominator}


def _offset_to_source_ticks(offset_us: int, timebase: Mapping[str, int], field: str) -> int:
    if offset_us < 0:
        raise PipelineValidationError(f"{field} must be non-negative")
    numerator = int(timebase["numerator"])
    denominator = int(timebase["denominator"])
    ticks = Fraction(offset_us * denominator, 1_000_000 * numerator)
    if ticks.denominator != 1:
        raise PipelineValidationError(
            f"{field} cannot be represented exactly in the declared source timebase"
        )
    return int(ticks)


def _source_ticks_to_microseconds(ticks: int, timebase: Mapping[str, int], field: str) -> int:
    if ticks < 0:
        raise PipelineValidationError(f"{field} resolved to a negative source coordinate")
    numerator = int(timebase["numerator"])
    denominator = int(timebase["denominator"])
    microseconds = Fraction(ticks * numerator * 1_000_000, denominator)
    if microseconds.denominator != 1:
        raise PipelineValidationError(
            f"{field} source tick cannot be represented exactly in microseconds"
        )
    return int(microseconds)


def _validate_transcript_span(value: Any) -> str | dict[str, Any]:
    if value == "NOT_APPLICABLE":
        return value
    if not isinstance(value, Mapping):
        raise PipelineValidationError(
            "transcript_span must be NOT_APPLICABLE or a transcript span object"
        )
    required = {
        "alignment_ref",
        "start_word_id",
        "end_word_id",
        "start_char",
        "end_char",
    }
    if set(value) != required:
        raise PipelineValidationError(
            f"transcript_span must contain exactly {sorted(required)}"
        )
    alignment_ref = require_ref(value["alignment_ref"], "transcript_span.alignment_ref")
    start_word_id = require_string(
        value["start_word_id"], "transcript_span.start_word_id"
    )
    end_word_id = require_string(value["end_word_id"], "transcript_span.end_word_id")
    start_char = require_int(
        value["start_char"], "transcript_span.start_char", minimum=0
    )
    end_char = require_int(
        value["end_char"], "transcript_span.end_char", minimum=0
    )
    if end_char < start_char:
        raise PipelineValidationError("transcript_span.end_char must be >= start_char")
    return {
        "alignment_ref": alignment_ref,
        "start_word_id": start_word_id,
        "end_word_id": end_word_id,
        "start_char": start_char,
        "end_char": end_char,
    }


class TemporalEvidenceMomentService:
    """Owns canonical, source-resolvable temporal evidence moments."""

    def __init__(self, repository: PipelineRepository):
        self.repository = repository
        self.source_media = SourceMediaService(repository)

    @staticmethod
    def evidence_ref(moment: Mapping[str, Any], *, canonical_sha: str | None = None) -> dict[str, str]:
        object_id = require_string(moment["evidence_moment_id"], "evidence_moment_id")
        version = require_string(moment["evidence_moment_version"], "evidence_moment_version")
        sha = canonical_sha or canonical_sha256(moment)
        return immutable_ref(object_id, version, {**dict(moment)})

    def create(
        self,
        *,
        source_registration_ref: Mapping[str, Any],
        source_path: str | Path,
        stream_ordinal: Any = None,
        timebase: Any = None,
        start_offset_us: Any = None,
        end_offset_us: Any = None,
        transcript_span: Any = "NOT_APPLICABLE",
        idempotency_key: str,
    ) -> dict[str, Any]:
        source_ref = require_ref(source_registration_ref, "source_registration_ref")
        source_integrity = self.source_media.verify_source(
            source_registration_ref=source_ref,
            source_path=source_path,
        )
        if source_integrity["source_authority"] != SOURCE_MEDIA_AUTHORITY:
            raise PipelineSourceLineageError(
                "evidence source authority is not sovereign media bytes"
            )

        source_registration = self.repository.get_object(source_ref["object_id"])["payload"]
        technical_streams = source_registration.get("technical", {}).get("streams", [])
        if not technical_streams:
            raise PipelineValidationError("source registration contains no stream timing metadata")

        ordinal = require_int(stream_ordinal, "stream_ordinal", minimum=0)
        if ordinal >= len(technical_streams):
            raise PipelineValidationError("stream_ordinal is outside registered source stream set")

        normalized_timebase = _normalize_timebase(timebase)
        registered_stream = technical_streams[ordinal]
        registered_timebase = _normalize_timebase(registered_stream.get("time_base"))
        if normalized_timebase != registered_timebase:
            raise PipelineSourceLineageError(
                "evidence timebase does not match the registered sovereign source stream"
            )

        start_us = require_int(start_offset_us, "start_offset_us", minimum=0)
        end_us = require_int(end_offset_us, "end_offset_us", minimum=0)
        if end_us <= start_us:
            raise PipelineValidationError("evidence end_offset_us must exceed start_offset_us")

        start_ticks = _offset_to_source_ticks(start_us, normalized_timebase, "start_offset_us")
        end_ticks = _offset_to_source_ticks(end_us, normalized_timebase, "end_offset_us")
        if end_ticks <= start_ticks:
            raise PipelineValidationError("evidence source interval must contain at least one source tick")

        streams, format_info = _probe_source_streams(source_path)
        if ordinal >= len(streams):
            raise PipelineSourceLineageError(
                "evidence stream ordinal cannot be resolved in fresh source media"
            )
        observed_stream = streams[ordinal]
        observed_timebase = _normalize_timebase(observed_stream["timebase"])
        if observed_timebase != normalized_timebase:
            raise PipelineSourceLineageError(
                "fresh source stream timebase does not match evidence timebase"
            )

        duration_seconds = observed_stream["duration_seconds"] or format_info["duration_seconds"]
        if duration_seconds is None:
            raise PipelineValidationError(
                "source stream duration is unavailable; out-of-bounds anchors cannot be proven"
            )
        end_seconds = Fraction(end_us, 1_000_000)
        if end_seconds > duration_seconds:
            raise PipelineValidationError("evidence end_offset_us is outside source stream duration")

        normalized_transcript_span = _validate_transcript_span(transcript_span)
        source_media_ref = source_integrity["source_media_ref"]
        source_media_sha256 = require_sha(
            source_integrity["source_media_sha256"], "source_media_sha256"
        )
        core = {
            "source_registration_ref": source_ref,
            "source_media_ref": source_media_ref,
            "source_media_sha256": source_media_sha256,
            "source_authority": SOURCE_MEDIA_AUTHORITY,
            "stream": {
                "ordinal": ordinal,
                "stream_index": observed_stream["stream_index"],
                "codec_type": observed_stream["codec_type"],
            },
            "timebase": normalized_timebase,
            "start_offset_us": start_us,
            "end_offset_us": end_us,
            "start_source_tick": start_ticks,
            "end_source_tick": end_ticks,
            "transcript_span": normalized_transcript_span,
            "coordinate_unit": MICROSECOND_TIME_UNIT,
            "coordinate_contract": "SOURCE_STREAM_NATIVE_TIMEBASE_EXACT_MICROSECOND",
            "provenance": {
                "source_kind": "SOVEREIGN_SOURCE_BYTES",
                "source_media_ref": source_media_ref,
                "source_media_sha256": source_media_sha256,
                "source_registration_ref": source_ref,
            },
            "validation": {
                "status": "VERIFIED",
                "source_integrity": "VERIFIED",
                "stream_timebase": "VERIFIED",
                "interval_order": "VERIFIED",
                "bounds": "VERIFIED",
                "microsecond_precision": "VERIFIED",
            },
        }
        reject_noncanonical(core)
        moment = {
            "evidence_moment_id": semantic_identity("evidence-moment", core),
            "evidence_moment_version": EVIDENCE_MOMENT_VERSION,
            **core,
        }

        stored = self.repository.store_object(
            EVIDENCE_MOMENT_OBJECT_TYPE,
            moment,
            idempotency_key=idempotency_key,
            object_id=moment["evidence_moment_id"],
            semantic_version=EVIDENCE_MOMENT_VERSION,
            lifecycle_state="VERIFIED",
        )
        self.repository.add_edge(
            source_ref["object_id"],
            moment["evidence_moment_id"],
            "source_registration_input",
            evidence={"source_media_sha256": source_media_sha256},
        )
        self.repository.add_edge(
            source_media_ref["object_id"],
            moment["evidence_moment_id"],
            "sovereign_source_media_input",
            evidence={
                "source_media_sha256": source_media_sha256,
                "stream_ordinal": ordinal,
                "timebase": normalized_timebase,
            },
        )
        if normalized_transcript_span != "NOT_APPLICABLE":
            self.repository.add_edge(
                normalized_transcript_span["alignment_ref"]["object_id"],
                moment["evidence_moment_id"],
                "transcript_alignment_input",
                evidence={
                    "start_word_id": normalized_transcript_span["start_word_id"],
                    "end_word_id": normalized_transcript_span["end_word_id"],
                    "start_char": normalized_transcript_span["start_char"],
                    "end_char": normalized_transcript_span["end_char"],
                },
            )
        return stored

    def _load_moment(self, evidence_moment_ref: Mapping[str, Any]) -> dict[str, Any]:
        moment_ref = require_ref(evidence_moment_ref, "evidence_moment_ref")
        stored = self.repository.get_object(moment_ref["object_id"])
        if stored["object_type"] != EVIDENCE_MOMENT_OBJECT_TYPE:
            raise PipelineSourceLineageError(
                "evidence moment reference does not resolve to evidence_moment"
            )
        if stored["semantic_version"] != moment_ref["version"]:
            raise PipelineSourceLineageError("evidence moment version mismatch")
        if stored["canonical_sha256"] != moment_ref["sha256"]:
            raise PipelineSourceLineageError("evidence moment reference digest mismatch")
        payload = stored["payload"]
        if payload["evidence_moment_id"] != moment_ref["object_id"]:
            raise PipelineSourceLineageError("evidence moment object identity mismatch")
        return payload

    def resolve(
        self,
        *,
        evidence_moment_ref: Mapping[str, Any],
        source_path: str | Path,
    ) -> dict[str, Any]:
        moment = self._load_moment(evidence_moment_ref)
        source_ref = require_ref(moment["source_registration_ref"], "source_registration_ref")
        source_integrity = self.source_media.verify_source(
            source_registration_ref=source_ref,
            source_path=source_path,
        )

        if moment["source_media_ref"] != source_integrity["source_media_ref"]:
            raise PipelineSourceLineageError(
                "evidence source media reference does not match verified source registration"
            )
        if moment["source_media_sha256"] != source_integrity["source_media_sha256"]:
            raise PipelineSourceLineageError(
                "evidence source media digest does not match verified source"
            )
        if moment["provenance"]["source_media_sha256"] != source_integrity["source_media_sha256"]:
            raise PipelineSourceLineageError(
                "evidence provenance source digest does not match verified source"
            )
        if moment["provenance"]["source_media_ref"] != source_integrity["source_media_ref"]:
            raise PipelineSourceLineageError(
                "evidence provenance source media reference does not match verified source"
            )

        streams, format_info = _probe_source_streams(source_path)
        ordinal = require_int(moment["stream"]["ordinal"], "stream.ordinal", minimum=0)
        if ordinal >= len(streams):
            raise PipelineSourceLineageError(
                "evidence stream ordinal cannot be resolved in fresh source media"
            )
        observed_stream = streams[ordinal]
        expected_stream_index = require_int(
            moment["stream"]["stream_index"], "stream.stream_index", minimum=0
        )
        if observed_stream["stream_index"] != expected_stream_index:
            raise PipelineSourceLineageError(
                "evidence stream index does not match fresh source media"
            )
        if observed_stream["codec_type"] != moment["stream"]["codec_type"]:
            raise PipelineSourceLineageError(
                "evidence stream type does not match fresh source media"
            )

        timebase = _normalize_timebase(moment["timebase"])
        observed_timebase = _normalize_timebase(observed_stream["timebase"])
        if timebase != observed_timebase:
            raise PipelineSourceLineageError(
                "evidence timebase does not match fresh source media"
            )

        start_us = require_int(moment["start_offset_us"], "start_offset_us", minimum=0)
        end_us = require_int(moment["end_offset_us"], "end_offset_us", minimum=0)
        start_ticks = _offset_to_source_ticks(start_us, timebase, "start_offset_us")
        end_ticks = _offset_to_source_ticks(end_us, timebase, "end_offset_us")
        if end_ticks <= start_ticks:
            raise PipelineValidationError("evidence source interval must contain at least one source tick")

        if moment.get("start_source_tick") != start_ticks:
            raise PipelineSourceLineageError(
                "stored start_source_tick does not match exact microsecond coordinate"
            )
        if moment.get("end_source_tick") != end_ticks:
            raise PipelineSourceLineageError(
                "stored end_source_tick does not match exact microsecond coordinate"
            )

        duration_seconds = observed_stream["duration_seconds"] or format_info["duration_seconds"]
        if duration_seconds is None:
            raise PipelineValidationError(
                "source stream duration is unavailable; out-of-bounds anchors cannot be proven"
            )
        if Fraction(end_us, 1_000_000) > duration_seconds:
            raise PipelineValidationError("evidence end_offset_us is outside source stream duration")

        resolved_start_us = _source_ticks_to_microseconds(
            start_ticks, timebase, "resolved start source tick"
        )
        resolved_end_us = _source_ticks_to_microseconds(
            end_ticks, timebase, "resolved end source tick"
        )
        if (resolved_start_us, resolved_end_us) != (start_us, end_us):
            raise PipelineValidationError(
                "source media cannot resolve the evidence interval without coordinate loss"
            )

        result = {
            "status": "RESOLVED",
            "evidence_moment_ref": require_ref(
                {
                    "object_id": moment["evidence_moment_id"],
                    "version": moment["evidence_moment_version"],
                    "sha256": canonical_sha256(moment),
                },
                "evidence_moment_ref",
            ),
            "source_registration_ref": source_integrity["source_registration_ref"],
            "source_media_ref": source_integrity["source_media_ref"],
            "source_media_sha256": source_integrity["source_media_sha256"],
            "stream": {
                "ordinal": ordinal,
                "stream_index": expected_stream_index,
                "codec_type": observed_stream["codec_type"],
            },
            "timebase": timebase,
            "start_offset_us": start_us,
            "end_offset_us": end_us,
            "start_source_tick": start_ticks,
            "end_source_tick": end_ticks,
            "resolved_exactly": True,
            "source_read": "FRESH_FFPROBE",
            "source_duration_check": "PASS",
        }
        reject_noncanonical(result)
        return result

    def projection(
        self,
        evidence_moment_id: str,
        *,
        source_path: str | Path | None = None,
    ) -> dict[str, Any]:
        moment = self.repository.get_object(evidence_moment_id)
        if moment["object_type"] != EVIDENCE_MOMENT_OBJECT_TYPE:
            raise PipelineValidationError("object is not an evidence moment")
        payload = moment["payload"]
        projection = {
            "evidence_moment_ref": {
                "object_id": evidence_moment_id,
                "version": payload["evidence_moment_version"],
                "sha256": moment["canonical_sha256"],
            },
            "stream": payload["stream"],
            "timebase": payload["timebase"],
            "start_offset_us": payload["start_offset_us"],
            "end_offset_us": payload["end_offset_us"],
            "transcript_span": payload["transcript_span"],
            "source_media_ref": payload["source_media_ref"],
            "source_media_sha256": payload["source_media_sha256"],
            "source_authority": payload["source_authority"],
            "provenance": payload["provenance"],
            "validation": payload["validation"],
            "read_only": True,
        }
        if source_path is not None:
            projection["source_resolution"] = self.resolve(
                evidence_moment_ref=projection["evidence_moment_ref"],
                source_path=source_path,
            )
        else:
            projection["source_resolution"] = {"status": "NOT_CHECKED"}
        reject_noncanonical(projection)
        return projection
