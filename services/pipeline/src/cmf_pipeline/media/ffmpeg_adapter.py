from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Mapping

from ca_contracts import bytes_sha256, canonical_sha256

from ..domain.errors import PipelineSourceLineageError, PipelineValidationError
from ..domain.validation import require_int, require_ref, require_relative_path, reject_noncanonical, semantic_identity
from ..workflow.infrastructure.repository import PipelineRepository
from .source import SOURCE_MEDIA_AUTHORITY, SourceMediaService


def _run(command: list[str]) -> None:
    process = subprocess.run(command, text=True, capture_output=True)
    if process.returncode != 0:
        raise PipelineValidationError(f"ffmpeg command failed: {process.stderr.strip()}")


class FFmpegSourceLedRenderer:
    def __init__(
        self,
        repository: PipelineRepository,
        ffmpeg_binary: str = "ffmpeg",
        ffprobe_binary: str = "ffprobe",
    ):
        self.ffmpeg_binary = ffmpeg_binary
        self.ffprobe_binary = ffprobe_binary
        self.source_media = SourceMediaService(repository)
        if shutil.which(ffmpeg_binary) is None or shutil.which(ffprobe_binary) is None:
            raise PipelineValidationError("ffmpeg and ffprobe are required")

    def render(
        self,
        *,
        source_path: str | Path,
        edl: Mapping[str, Any],
        output_dir: str | Path,
        logical_output_uri: str,
        audio_fade_ms: int = 10,
    ) -> dict[str, Any]:
        source = Path(source_path)
        outdir = Path(output_dir)
        outdir.mkdir(parents=True, exist_ok=True)
        if not source.is_file():
            raise PipelineValidationError("source media is missing")
        required_provenance = {
            "source_registration_ref",
            "source_media_ref",
            "source_media_sha256",
            "source_authority",
            "source_integrity",
        }
        missing = required_provenance - set(edl)
        if missing:
            raise PipelineSourceLineageError(
                f"rendered derivative is missing source lineage fields: {sorted(missing)}"
            )
        source_ref = require_ref(edl["source_registration_ref"], "source_registration_ref")
        if edl["source_authority"] != SOURCE_MEDIA_AUTHORITY:
            raise PipelineSourceLineageError("renderer source authority is not sovereign media bytes")
        source_integrity = self.source_media.verify_source(
            source_registration_ref=source_ref,
            source_path=source,
        )
        if source_integrity["source_media_ref"] != require_ref(edl["source_media_ref"], "source_media_ref"):
            raise PipelineSourceLineageError("EDL source media identity does not match its registration")
        if source_integrity["source_media_sha256"] != edl["source_media_sha256"]:
            raise PipelineSourceLineageError("EDL source media digest does not match its registration")
        if edl["source_integrity"] != source_integrity:
            raise PipelineSourceLineageError("EDL source integrity evidence is stale or forged")
        logical = require_relative_path(logical_output_uri, "logical_output_uri")
        fade_ms = require_int(audio_fade_ms, "audio_fade_ms", minimum=0)
        segments = []
        for index, entry in enumerate(edl["entries"]):
            duration_ms = entry["source_end_ms"] - entry["source_start_ms"]
            if duration_ms <= 0:
                raise PipelineValidationError("EDL contains an invalid source duration")
            segment = outdir / f"segment-{index:04d}.mp4"
            fade = min(fade_ms, max(0, duration_ms // 4))
            command = [
                self.ffmpeg_binary,
                "-y",
                "-v",
                "error",
                "-ss",
                f"{entry['source_start_ms'] / 1000:.3f}",
                "-i",
                str(source),
                "-t",
                f"{duration_ms / 1000:.3f}",
                "-map",
                "0:v:0",
                "-map",
                "0:a:0?",
                "-vf",
                "setpts=PTS-STARTPTS",
                "-af",
                f"asetpts=PTS-STARTPTS,afade=t=in:st=0:d={fade / 1000:.3f},afade=t=out:st={max(0, duration_ms - fade) / 1000:.3f}:d={fade / 1000:.3f}",
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-crf",
                "24",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "128k",
                "-movflags",
                "+faststart",
                str(segment),
            ]
            _run(command)
            segments.append(segment)
        concat_file = outdir / "concat.txt"
        concat_file.write_text(
            "".join(f"file '{path.name}'\n" for path in segments), encoding="utf-8"
        )
        output = outdir / Path(logical).name
        _run(
            [
                self.ffmpeg_binary,
                "-y",
                "-v",
                "error",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-c",
                "copy",
                str(output),
            ]
        )
        probe = subprocess.run(
            [
                self.ffprobe_binary,
                "-v",
                "error",
                "-show_streams",
                "-show_format",
                "-of",
                "json",
                str(output),
            ],
            text=True,
            capture_output=True,
        )
        if probe.returncode != 0:
            raise PipelineValidationError("rendered output failed ffprobe")
        probe_payload = json.loads(probe.stdout)
        output_sha256 = bytes_sha256(output.read_bytes())
        manifest_core = {
            "logical_uri": logical,
            "sha256": output_sha256,
            "edl_id": edl["edl_id"],
            "source_registration_ref": source_ref,
            "source_media_ref": source_integrity["source_media_ref"],
            "source_media_sha256": source_integrity["source_media_sha256"],
        }
        manifest = {
            "artifact_id": semantic_identity("rendered-video-artifact", manifest_core),
            "artifact_version": "1.0.0",
            "logical_uri": logical,
            "sha256": output_sha256,
            "byte_count": output.stat().st_size,
            "edl_ref": {
                "object_id": edl["edl_id"],
                "version": edl["edl_version"],
                "sha256": canonical_sha256(edl),
            },
            "source_registration_ref": source_ref,
            "source_media_ref": source_integrity["source_media_ref"],
            "source_media_sha256": source_integrity["source_media_sha256"],
            "source_authority": SOURCE_MEDIA_AUTHORITY,
            "source_integrity": source_integrity,
            "derivative_kind": "SOURCE_LED_RENDERED_VIDEO",
            "derivative_is_sovereign_source": False,
            "processing_revision": "1.0.0",
            "ffmpeg_binding": {
                "binary": "ffmpeg",
                "mode": "SOURCE_LED_SEGMENT_CONCAT",
                "audio_fade_ms": fade_ms,
            },
            "probe_sha256": canonical_sha256(probe_payload),
            "segment_count": len(segments),
            "production_authorized": False,
        }
        reject_noncanonical(manifest)
        return {
            "manifest": manifest,
            "output_path": str(output),
            "segment_paths": [str(path) for path in segments],
            "probe": probe_payload,
        }

    @staticmethod
    def srt(edl: Mapping[str, Any], captions: list[str], destination: str | Path) -> Path:
        if len(captions) != len(edl["entries"]):
            raise PipelineValidationError("caption count must equal EDL entry count")

        def stamp(ms: int) -> str:
            hours = ms // 3600000
            ms %= 3600000
            minutes = ms // 60000
            ms %= 60000
            seconds = ms // 1000
            millis = ms % 1000
            return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"

        lines = []
        for index, (entry, text) in enumerate(zip(edl["entries"], captions), 1):
            lines.extend(
                [
                    str(index),
                    f"{stamp(entry['output_start_ms'])} --> {stamp(entry['output_end_ms'])}",
                    str(text),
                    "",
                ]
            )
        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines), encoding="utf-8")
        return path
