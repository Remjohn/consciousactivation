from __future__ import annotations

import json
import subprocess
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Mapping

from ca_contracts import bytes_sha256, canonical_sha256

from ..domain.errors import PipelineSourceIntegrityError, PipelineSourceLineageError, PipelineValidationError
from ..domain.validation import (
    immutable_ref,
    require_bool,
    require_int,
    require_ref,
    require_relative_path,
    require_sha,
    require_string,
    reject_noncanonical,
    semantic_identity,
)
from ..workflow.infrastructure.repository import PipelineRepository


SOURCE_MEDIA_AUTHORITY = "SOVEREIGN_SOURCE_MEDIA_BYTES"
SOURCE_MEDIA_ID_PREFIX = "source-media:"
SOURCE_MEDIA_VERSION = "1.0.0"


def _decimal_ms(value: Any, field: str) -> int:
    try:
        decimal = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise PipelineValidationError(f"{field} must be a decimal duration") from exc
    if decimal < 0:
        raise PipelineValidationError(f"{field} must be non-negative")
    return int((decimal * 1000).to_integral_value())


def _rate(value: str) -> dict[str, int]:
    if not isinstance(value, str) or "/" not in value:
        return {"numerator": 0, "denominator": 1}
    left, right = value.split("/", 1)
    try:
        numerator, denominator = int(left), int(right)
    except ValueError:
        return {"numerator": 0, "denominator": 1}
    if denominator == 0:
        denominator = 1
    return {"numerator": numerator, "denominator": denominator}


def ffprobe_media(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    if not source.is_file():
        raise PipelineValidationError(f"media file does not exist: {source}")
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
    payload = json.loads(process.stdout)
    streams = []
    duration_candidates = []
    for ordinal, stream in enumerate(payload.get("streams", [])):
        codec_type = str(stream.get("codec_type") or "unknown")
        item = {
            "ordinal": ordinal,
            "codec_type": codec_type,
            "codec_name": str(stream.get("codec_name") or "unknown"),
            "time_base": _rate(str(stream.get("time_base") or "0/1")),
            "duration_ms": _decimal_ms(
                stream.get("duration") or 0, f"streams[{ordinal}].duration"
            ),
        }
        if codec_type == "video":
            item.update(
                {
                    "width": int(stream.get("width") or 0),
                    "height": int(stream.get("height") or 0),
                    "average_frame_rate": _rate(
                        str(stream.get("avg_frame_rate") or "0/1")
                    ),
                    "real_frame_rate": _rate(
                        str(stream.get("r_frame_rate") or "0/1")
                    ),
                    "pixel_format": str(stream.get("pix_fmt") or "unknown"),
                }
            )
        elif codec_type == "audio":
            item.update(
                {
                    "sample_rate_hz": int(stream.get("sample_rate") or 0),
                    "channels": int(stream.get("channels") or 0),
                    "channel_layout": str(
                        stream.get("channel_layout") or "unknown"
                    ),
                }
            )
        streams.append(item)
        duration_candidates.append(item["duration_ms"])
    format_duration = _decimal_ms(
        payload.get("format", {}).get("duration") or 0, "format.duration"
    )
    duration_candidates.append(format_duration)
    result = {
        "byte_count": source.stat().st_size,
        "media_sha256": bytes_sha256(source.read_bytes()),
        "duration_ms": max(duration_candidates or [0]),
        "format_name": str(
            payload.get("format", {}).get("format_name") or "unknown"
        ),
        "streams": streams,
        "ffprobe_result_sha256": canonical_sha256(payload),
    }
    reject_noncanonical(result)
    return result


def _content_addressed_media_id(media_sha256: str) -> str:
    digest = require_sha(media_sha256, "media_sha256")
    return f"{SOURCE_MEDIA_ID_PREFIX}{digest}"


class SourceMediaService:
    def __init__(self, repository: PipelineRepository):
        self.repository = repository

    @staticmethod
    def registration_ref(registration: Mapping[str, Any]) -> dict[str, str]:
        return immutable_ref(
            require_string(registration["registration_id"], "registration_id"),
            require_string(registration["registration_version"], "registration_version"),
            registration,
        )

    def register(
        self,
        *,
        source_path: str | Path,
        logical_uri: str,
        source_package_ref: Mapping[str, Any],
        transcript_alignment_ref: Mapping[str, Any],
        visual_index_ref: Mapping[str, Any],
        restrictions: list[str],
        idempotency_key: str,
    ) -> dict[str, Any]:
        technical = ffprobe_media(source_path)
        uri = require_relative_path(logical_uri, "logical_uri")
        source_ref = require_ref(source_package_ref, "source_package_ref")
        transcript_ref = require_ref(transcript_alignment_ref, "transcript_alignment_ref")
        visual_ref = require_ref(visual_index_ref, "visual_index_ref")
        restrictions = [
            require_string(x, f"restrictions[{i}]") for i, x in enumerate(restrictions)
        ]
        if restrictions != sorted(set(restrictions)):
            raise PipelineValidationError("restrictions must be sorted and unique")

        media_identity = {
            "media_id": _content_addressed_media_id(technical["media_sha256"]),
            "media_version": SOURCE_MEDIA_VERSION,
            "media_sha256": technical["media_sha256"],
            "byte_count": technical["byte_count"],
            "authority": SOURCE_MEDIA_AUTHORITY,
            "derivative": False,
        }
        reject_noncanonical(media_identity)
        identity_stored = self.repository.store_object(
            "source_media_identity",
            media_identity,
            idempotency_key=f"{idempotency_key}:media-identity",
            object_id=media_identity["media_id"],
            semantic_version=SOURCE_MEDIA_VERSION,
            lifecycle_state="VERIFIED",
        )
        source_media_ref = immutable_ref(
            identity_stored["object"]["object_id"],
            identity_stored["object"]["semantic_version"],
            identity_stored["object"]["payload"],
        )

        core = {
            "logical_uri": uri,
            "source_package_ref": source_ref,
            "transcript_alignment_ref": transcript_ref,
            "visual_index_ref": visual_ref,
            "source_media_ref": source_media_ref,
            "source_media_sha256": technical["media_sha256"],
            "source_authority": SOURCE_MEDIA_AUTHORITY,
            "technical": technical,
            "restrictions": restrictions,
            "original_bytes_immutable": True,
            "registration_is_edit_authority": False,
            "production_authorized": False,
        }
        registration = {
            "registration_id": semantic_identity("source-media-registration", core),
            "registration_version": SOURCE_MEDIA_VERSION,
            **core,
        }
        stored = self.repository.store_object(
            "source_media_registration",
            registration,
            idempotency_key=idempotency_key,
            object_id=registration["registration_id"],
            lifecycle_state="VERIFIED",
        )
        self.repository.add_edge(
            source_ref["object_id"],
            registration["registration_id"],
            "registers_source_package",
        )
        self.repository.add_edge(
            transcript_ref["object_id"],
            registration["registration_id"],
            "registers_transcript_alignment",
        )
        self.repository.add_edge(
            visual_ref["object_id"],
            registration["registration_id"],
            "registers_visual_index",
        )
        self.repository.add_edge(
            source_media_ref["object_id"],
            registration["registration_id"],
            "sovereign_source_media_for_registration",
            evidence={
                "source_media_sha256": technical["media_sha256"],
                "authority": SOURCE_MEDIA_AUTHORITY,
            },
        )
        return stored

    def _load_registration(
        self, source_registration_ref: Mapping[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        source_ref = require_ref(source_registration_ref, "source_registration_ref")
        stored = self.repository.get_object(source_ref["object_id"])
        if stored["object_type"] != "source_media_registration":
            raise PipelineSourceLineageError(
                "source registration reference does not resolve to source_media_registration"
            )
        if stored["semantic_version"] != source_ref["version"]:
            raise PipelineSourceLineageError("source registration version mismatch")
        if stored["canonical_sha256"] != source_ref["sha256"]:
            raise PipelineSourceLineageError("source registration reference digest mismatch")

        registration = stored["payload"]
        if registration["registration_id"] != source_ref["object_id"]:
            raise PipelineSourceLineageError("source registration object identity mismatch")
        if registration["source_authority"] != SOURCE_MEDIA_AUTHORITY:
            raise PipelineSourceLineageError("source registration authority mismatch")
        require_bool(
            registration["original_bytes_immutable"], "original_bytes_immutable"
        )
        if not registration["original_bytes_immutable"]:
            raise PipelineSourceLineageError("source bytes are not marked immutable")

        media_ref = require_ref(registration["source_media_ref"], "source_media_ref")
        identity = self.repository.get_object(media_ref["object_id"])
        if identity["object_type"] != "source_media_identity":
            raise PipelineSourceLineageError(
                "source media reference does not resolve to source_media_identity"
            )
        if identity["semantic_version"] != media_ref["version"]:
            raise PipelineSourceLineageError("source media identity version mismatch")
        if identity["canonical_sha256"] != media_ref["sha256"]:
            raise PipelineSourceLineageError("source media identity reference digest mismatch")
        identity_payload = identity["payload"]
        if identity_payload["media_id"] != media_ref["object_id"]:
            raise PipelineSourceLineageError("source media identity object mismatch")
        if identity_payload["authority"] != SOURCE_MEDIA_AUTHORITY:
            raise PipelineSourceLineageError("source media identity authority mismatch")
        if identity_payload["derivative"] is not False:
            raise PipelineSourceLineageError("derivative media cannot be a sovereign source")
        if registration["source_media_sha256"] != identity_payload["media_sha256"]:
            raise PipelineSourceLineageError("registration and source identity digest mismatch")
        if registration["technical"]["media_sha256"] != identity_payload["media_sha256"]:
            raise PipelineSourceLineageError("registration technical digest mismatch")
        return stored, identity

    def verify_source(
        self,
        *,
        source_registration_ref: Mapping[str, Any],
        source_path: str | Path,
    ) -> dict[str, Any]:
        registration, identity = self._load_registration(source_registration_ref)
        source = Path(source_path)
        if not source.is_file():
            raise PipelineSourceIntegrityError("source media is missing")
        observed_sha256 = bytes_sha256(source.read_bytes())
        observed_byte_count = source.stat().st_size
        expected_sha256 = identity["payload"]["media_sha256"]
        expected_byte_count = identity["payload"]["byte_count"]
        if observed_sha256 != expected_sha256:
            raise PipelineSourceIntegrityError(
                "source media integrity mismatch: observed bytes do not match the sovereign source digest"
            )
        if observed_byte_count != expected_byte_count:
            raise PipelineSourceIntegrityError(
                "source media integrity mismatch: observed byte count does not match the sovereign source"
            )
        return {
            "status": "VERIFIED",
            "source_registration_ref": self.registration_ref(registration["payload"]),
            "source_media_ref": require_ref(
                registration["payload"]["source_media_ref"], "source_media_ref"
            ),
            "source_media_sha256": expected_sha256,
            "observed_sha256": observed_sha256,
            "byte_count": observed_byte_count,
            "source_authority": SOURCE_MEDIA_AUTHORITY,
        }

    def provenance(
        self,
        *,
        source_registration_ref: Mapping[str, Any],
        derivative_ref: Mapping[str, Any] | str = "NOT_APPLICABLE",
        source_path: str | Path | None = None,
    ) -> dict[str, Any]:
        registration_stored, identity = self._load_registration(source_registration_ref)
        registration = registration_stored["payload"]
        source_ref = self.registration_ref(registration)
        media_ref = require_ref(registration["source_media_ref"], "source_media_ref")
        inspection = {
            "source_authority": SOURCE_MEDIA_AUTHORITY,
            "source_kind": "SOVEREIGN_SOURCE_BYTES",
            "source_registration_ref": source_ref,
            "source_media_ref": media_ref,
            "source_media_sha256": identity["payload"]["media_sha256"],
            "source_media_byte_count": identity["payload"]["byte_count"],
            "derivative_kind": "NONE",
            "derivative_ref": "NOT_APPLICABLE",
            "derivative_is_sovereign_source": False,
        }
        if derivative_ref != "NOT_APPLICABLE":
            inspection["derivative_ref"] = require_ref(derivative_ref, "derivative_ref")
            inspection["derivative_kind"] = "DERIVATIVE_OUTPUT"
        if source_path is not None:
            inspection["integrity"] = self.verify_source(
                source_registration_ref=source_ref,
                source_path=source_path,
            )
        else:
            inspection["integrity"] = {"status": "NOT_CHECKED"}
        reject_noncanonical(inspection)
        return inspection
