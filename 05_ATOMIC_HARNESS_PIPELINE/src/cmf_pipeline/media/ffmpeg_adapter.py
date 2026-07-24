from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Mapping

from ca_contracts import bytes_sha256, canonical_sha256

from ..domain.errors import PipelineValidationError
from ..domain.validation import require_relative_path, reject_noncanonical, semantic_identity


def _run(command: list[str]) -> None:
    process=subprocess.run(command,text=True,capture_output=True)
    if process.returncode!=0: raise PipelineValidationError(f"ffmpeg command failed: {process.stderr.strip()}")


class FFmpegSourceLedRenderer:
    def __init__(self, ffmpeg_binary: str="ffmpeg", ffprobe_binary: str="ffprobe"):
        self.ffmpeg_binary=ffmpeg_binary;self.ffprobe_binary=ffprobe_binary
        if shutil.which(ffmpeg_binary) is None or shutil.which(ffprobe_binary) is None: raise PipelineValidationError("ffmpeg and ffprobe are required")

    def render(self, *, source_path: str|Path, edl: Mapping[str,Any], output_dir: str|Path, logical_output_uri: str, audio_fade_ms: int=10) -> dict[str,Any]:
        source=Path(source_path);outdir=Path(output_dir);outdir.mkdir(parents=True,exist_ok=True)
        if not source.is_file(): raise PipelineValidationError("source media is missing")
        logical=require_relative_path(logical_output_uri,"logical_output_uri")
        segments=[]
        for index,entry in enumerate(edl["entries"]):
            duration_ms=entry["source_end_ms"]-entry["source_start_ms"]
            segment=outdir/f"segment-{index:04d}.mp4"
            fade=min(audio_fade_ms,max(0,duration_ms//4))
            command=[self.ffmpeg_binary,"-y","-v","error","-ss",f"{entry['source_start_ms']/1000:.3f}","-i",str(source),"-t",f"{duration_ms/1000:.3f}",
                     "-map","0:v:0","-map","0:a:0?","-vf","setpts=PTS-STARTPTS","-af",f"asetpts=PTS-STARTPTS,afade=t=in:st=0:d={fade/1000:.3f},afade=t=out:st={max(0,duration_ms-fade)/1000:.3f}:d={fade/1000:.3f}",
                     "-c:v","libx264","-preset","veryfast","-crf","24","-pix_fmt","yuv420p","-c:a","aac","-b:a","128k","-movflags","+faststart",str(segment)]
            _run(command);segments.append(segment)
        concat_file=outdir/"concat.txt"
        concat_file.write_text("".join(f"file '{p.name}'\n" for p in segments),encoding="utf-8")
        output=outdir/Path(logical).name
        _run([self.ffmpeg_binary,"-y","-v","error","-f","concat","-safe","0","-i",str(concat_file),"-c","copy",str(output)])
        probe=subprocess.run([self.ffprobe_binary,"-v","error","-show_streams","-show_format","-of","json",str(output)],text=True,capture_output=True)
        if probe.returncode!=0: raise PipelineValidationError("rendered output failed ffprobe")
        probe_payload=json.loads(probe.stdout)
        manifest={
            "artifact_id":semantic_identity("rendered-video-artifact",{"logical_uri":logical,"sha256":bytes_sha256(output.read_bytes()),"edl_id":edl["edl_id"]}),
            "artifact_version":"1.0.0","logical_uri":logical,"sha256":bytes_sha256(output.read_bytes()),"byte_count":output.stat().st_size,
            "edl_ref":{"object_id":edl["edl_id"],"version":edl["edl_version"],"sha256":canonical_sha256(edl)},
            "ffmpeg_binding":{"binary":"ffmpeg","mode":"SOURCE_LED_SEGMENT_CONCAT","audio_fade_ms":audio_fade_ms},
            "probe_sha256":canonical_sha256(probe_payload),"segment_count":len(segments),"production_authorized":False,
        }
        reject_noncanonical(manifest)
        return {"manifest":manifest,"output_path":str(output),"segment_paths":[str(p) for p in segments],"probe":probe_payload}

    @staticmethod
    def srt(edl: Mapping[str,Any], captions: list[str], destination: str|Path) -> Path:
        if len(captions)!=len(edl["entries"]): raise PipelineValidationError("caption count must equal EDL entry count")
        def stamp(ms:int)->str:
            h=ms//3600000;ms%=3600000;m=ms//60000;ms%=60000;s=ms//1000;u=ms%1000
            return f"{h:02d}:{m:02d}:{s:02d},{u:03d}"
        lines=[]
        for index,(entry,text) in enumerate(zip(edl["entries"],captions),1):
            lines.extend([str(index),f"{stamp(entry['output_start_ms'])} --> {stamp(entry['output_end_ms'])}",str(text),""])
        path=Path(destination);path.parent.mkdir(parents=True,exist_ok=True);path.write_text("\n".join(lines),encoding="utf-8")
        return path
