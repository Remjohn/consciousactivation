from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Mapping

from ca_contracts import bytes_sha256, canonical_sha256

from ..domain.errors import PipelineSourceLineageError, PipelineValidationError
from ..domain.validation import require_ref, require_string, reject_noncanonical, semantic_identity
from .source import SOURCE_MEDIA_AUTHORITY


class RenderedVideoEvaluator:
    def __init__(self, ffmpeg_binary: str = "ffmpeg", ffprobe_binary: str = "ffprobe"):
        self.ffmpeg = ffmpeg_binary
        self.ffprobe = ffprobe_binary

    def evaluate(
        self,
        *,
        artifact_path: str | Path,
        artifact_ref: Mapping[str, Any],
        program: Mapping[str, Any],
        edl: Mapping[str, Any],
        producer_actor_id: str,
        evaluator_actor_id: str,
        evidence_dir: str | Path,
    ) -> dict[str, Any]:
        if require_string(producer_actor_id, "producer_actor_id") == require_string(
            evaluator_actor_id, "evaluator_actor_id"
        ):
            raise PipelineValidationError("producer and evaluator must be distinct")
        path = Path(artifact_path)
        if not path.is_file():
            raise PipelineValidationError("artifact missing")
        ref = require_ref(artifact_ref, "artifact_ref")
        observed_sha = bytes_sha256(path.read_bytes())
        if observed_sha != ref["sha256"]:
            raise PipelineValidationError("artifact hash mismatch")

        for field in (
            "source_registration_ref",
            "source_media_ref",
            "source_media_sha256",
            "source_authority",
        ):
            if field not in program or field not in edl:
                raise PipelineSourceLineageError(f"evaluation inputs missing {field}")
        if program["source_authority"] != SOURCE_MEDIA_AUTHORITY or edl["source_authority"] != SOURCE_MEDIA_AUTHORITY:
            raise PipelineSourceLineageError("evaluation source authority is not sovereign media bytes")
        if program["source_media_ref"] != edl["source_media_ref"]:
            raise PipelineSourceLineageError("program and EDL source media identities differ")
        if program["source_media_sha256"] != edl["source_media_sha256"]:
            raise PipelineSourceLineageError("program and EDL source media digests differ")
        if program["source_registration_ref"] != edl["source_registration_ref"]:
            raise PipelineSourceLineageError("program and EDL source registrations differ")

        probe = subprocess.run(
            [
                self.ffprobe,
                "-v",
                "error",
                "-show_streams",
                "-show_format",
                "-of",
                "json",
                str(path),
            ],
            text=True,
            capture_output=True,
        )
        if probe.returncode != 0:
            raise PipelineValidationError("ffprobe failed")
        payload = json.loads(probe.stdout)
        evidence = Path(evidence_dir)
        evidence.mkdir(parents=True, exist_ok=True)
        cuts = []
        for idx, entry in enumerate(edl["entries"][:-1]):
            cut_ms = entry["output_end_ms"]
            frames = []
            for label, offset in [("before", max(0, cut_ms - 80)), ("after", cut_ms + 80)]:
                frame = evidence / f"cut-{idx:03d}-{label}.png"
                proc = subprocess.run(
                    [
                        self.ffmpeg,
                        "-y",
                        "-v",
                        "error",
                        "-ss",
                        f"{offset / 1000:.3f}",
                        "-i",
                        str(path),
                        "-frames:v",
                        "1",
                        str(frame),
                    ],
                    text=True,
                    capture_output=True,
                )
                if proc.returncode != 0:
                    raise PipelineValidationError("cut evidence extraction failed")
                frames.append(
                    {
                        "label": label,
                        "offset_ms": offset,
                        "logical_uri": frame.name,
                        "sha256": bytes_sha256(frame.read_bytes()),
                    }
                )
            cuts.append(
                {
                    "cut_index": idx,
                    "cut_ms": cut_ms,
                    "frames": frames,
                    "judgment_state": "INDEPENDENT_JUDGMENT_REQUIRED",
                }
            )
        streams = {str(stream.get("codec_type")) for stream in payload.get("streams", [])}
        checks = [
            {"check_id": "artifact_hash", "result": "PASS", "hard_gate": True},
            {
                "check_id": "video_stream",
                "result": "PASS" if "video" in streams else "FAIL",
                "hard_gate": True,
            },
            {
                "check_id": "audio_stream",
                "result": "PASS" if "audio" in streams else "NOT_APPLICABLE_BY_RULE",
                "hard_gate": False,
            },
            {
                "check_id": "a_roll_spine",
                "result": "PASS"
                if any(track["role"] == "PRIMARY_A_ROLL_SPINE" for track in program["tracks"])
                else "FAIL",
                "hard_gate": True,
            },
            {
                "check_id": "cut_evidence",
                "result": "PASS"
                if len(cuts) == max(0, len(edl["entries"]) - 1)
                else "FAIL",
                "hard_gate": True,
            },
            {
                "check_id": "sovereign_source_lineage",
                "result": "PASS",
                "hard_gate": True,
            },
        ]
        verdict = (
            "FAIL"
            if any(check["hard_gate"] and check["result"] == "FAIL" for check in checks)
            else "PASS_TECHNICAL_INDEPENDENT_JUDGMENT_PENDING"
        )
        core = {
            "artifact_ref": ref,
            "program_ref": {
                "object_id": program["program_id"],
                "version": program["program_version"],
                "sha256": canonical_sha256(program),
            },
            "edl_ref": {
                "object_id": edl["edl_id"],
                "version": edl["edl_version"],
                "sha256": canonical_sha256(edl),
            },
            "source_registration_ref": program["source_registration_ref"],
            "source_media_ref": program["source_media_ref"],
            "source_media_sha256": program["source_media_sha256"],
            "source_authority": SOURCE_MEDIA_AUTHORITY,
            "derivative_kind": "RENDERED_VIDEO_EVALUATION",
            "derivative_is_sovereign_source": False,
            "producer_actor_id": producer_actor_id,
            "evaluator_actor_id": evaluator_actor_id,
            "checks": checks,
            "cut_evidence": cuts,
            "probe_sha256": canonical_sha256(payload),
            "verdict": verdict,
            "production_eligible": False,
        }
        reject_noncanonical(core)
        return {"evaluation_id": semantic_identity("rendered-video-evaluation", core), "evaluation_version": "1.0.0", **core}
