from __future__ import annotations

import json
import subprocess
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any

from ca_contracts import bytes_sha256

from .domain import make_media_asset
from .errors import ValidationError


class MediaInspector:
    def inspect(self, path: str | Path, *, logical_uri: str, media_type: str) -> dict[str, Any]:
        source = Path(path)
        if not source.is_file():
            raise ValidationError(f"media file does not exist: {source}")
        data = source.read_bytes()
        technical = self._ffprobe(source)
        return make_media_asset(logical_uri=logical_uri, sha256=bytes_sha256(data), bytes_count=len(data), media_type=media_type, technical=technical)

    @staticmethod
    def _ffprobe(path: Path) -> dict[str, Any]:
        command = ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)]
        completed = subprocess.run(command, text=True, capture_output=True)
        if completed.returncode != 0:
            return {"probe_status": "UNAVAILABLE_OR_UNSUPPORTED", "duration_ms": 0, "streams": [], "limitations": ["FFPROBE_FAILED"]}
        parsed = json.loads(completed.stdout)
        duration = parsed.get("format", {}).get("duration")
        duration_ms = int((Decimal(str(duration)) * 1000).quantize(Decimal("1"), rounding=ROUND_HALF_UP)) if duration else 0
        streams = []
        for item in parsed.get("streams", []):
            stream = {"index": int(item.get("index", 0)), "codec_type": str(item.get("codec_type", "unknown")), "codec_name": str(item.get("codec_name", "unknown"))}
            for key in ["width", "height", "sample_rate", "channels"]:
                if item.get(key) is not None:
                    stream[key] = int(item[key])
            rate = item.get("avg_frame_rate") or item.get("r_frame_rate")
            if rate and "/" in rate:
                num, den = rate.split("/", 1)
                stream["frame_rate"] = {"numerator": int(num), "denominator": int(den)}
            streams.append(stream)
        return {"probe_status": "PROBED", "duration_ms": duration_ms, "streams": streams, "format_name": str(parsed.get("format", {}).get("format_name", "unknown")), "limitations": []}
