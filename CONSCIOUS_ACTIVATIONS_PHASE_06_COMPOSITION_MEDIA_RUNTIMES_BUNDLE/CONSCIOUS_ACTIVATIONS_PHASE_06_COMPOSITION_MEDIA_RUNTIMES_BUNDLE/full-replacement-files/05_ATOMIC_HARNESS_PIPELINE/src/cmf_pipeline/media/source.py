from __future__ import annotations

import json
import subprocess
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Mapping

from ca_contracts import bytes_sha256, canonical_sha256

from ..domain.errors import PipelineValidationError
from ..domain.validation import require_ref, require_relative_path, require_string, reject_noncanonical, semantic_identity
from ..workflow.infrastructure.repository import PipelineRepository


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
            "ffprobe", "-v", "error", "-show_streams", "-show_format",
            "-of", "json", str(source),
        ],
        text=True,
        capture_output=True,
    )
    if process.returncode != 0:
        raise PipelineValidationError(f"ffprobe failed: {process.stderr.strip()}")
    payload = json.loads(process.stdout)
    streams=[]
    duration_candidates=[]
    for ordinal, stream in enumerate(payload.get("streams", [])):
        codec_type=str(stream.get("codec_type") or "unknown")
        item={
            "ordinal": ordinal,
            "codec_type": codec_type,
            "codec_name": str(stream.get("codec_name") or "unknown"),
            "time_base": _rate(str(stream.get("time_base") or "0/1")),
            "duration_ms": _decimal_ms(stream.get("duration") or 0, f"streams[{ordinal}].duration"),
        }
        if codec_type == "video":
            item.update({
                "width": int(stream.get("width") or 0),
                "height": int(stream.get("height") or 0),
                "average_frame_rate": _rate(str(stream.get("avg_frame_rate") or "0/1")),
                "real_frame_rate": _rate(str(stream.get("r_frame_rate") or "0/1")),
                "pixel_format": str(stream.get("pix_fmt") or "unknown"),
            })
        elif codec_type == "audio":
            item.update({
                "sample_rate_hz": int(stream.get("sample_rate") or 0),
                "channels": int(stream.get("channels") or 0),
                "channel_layout": str(stream.get("channel_layout") or "unknown"),
            })
        streams.append(item)
        duration_candidates.append(item["duration_ms"])
    format_duration=_decimal_ms(payload.get("format",{}).get("duration") or 0,"format.duration")
    duration_candidates.append(format_duration)
    result={
        "byte_count": source.stat().st_size,
        "media_sha256": bytes_sha256(source.read_bytes()),
        "duration_ms": max(duration_candidates or [0]),
        "format_name": str(payload.get("format",{}).get("format_name") or "unknown"),
        "streams": streams,
        "ffprobe_result_sha256": canonical_sha256(payload),
    }
    reject_noncanonical(result)
    return result


class SourceMediaService:
    def __init__(self, repository: PipelineRepository):
        self.repository=repository

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
        technical=ffprobe_media(source_path)
        uri=require_relative_path(logical_uri,"logical_uri")
        source_ref=require_ref(source_package_ref,"source_package_ref")
        transcript_ref=require_ref(transcript_alignment_ref,"transcript_alignment_ref")
        visual_ref=require_ref(visual_index_ref,"visual_index_ref")
        restrictions=[require_string(x,f"restrictions[{i}]") for i,x in enumerate(restrictions)]
        if restrictions != sorted(set(restrictions)):
            raise PipelineValidationError("restrictions must be sorted and unique")
        core={
            "logical_uri": uri,
            "source_package_ref": source_ref,
            "transcript_alignment_ref": transcript_ref,
            "visual_index_ref": visual_ref,
            "technical": technical,
            "restrictions": restrictions,
            "original_bytes_immutable": True,
            "registration_is_edit_authority": False,
            "production_authorized": False,
        }
        registration={"registration_id": semantic_identity("source-media-registration",core),"registration_version":"1.0.0",**core}
        stored=self.repository.store_object(
            "source_media_registration",registration,idempotency_key=idempotency_key,
            object_id=registration["registration_id"],lifecycle_state="VERIFIED",
        )
        for ref, rel in ((source_ref,"registers_source_package"),(transcript_ref,"registers_transcript_alignment"),(visual_ref,"registers_visual_index")):
            self.repository.add_edge(ref["object_id"],registration["registration_id"],rel)
        return stored
