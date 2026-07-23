from __future__ import annotations

import wave
from pathlib import Path

import sys
ROOT = Path(__file__).resolve().parents[2]
for candidate in reversed([ROOT / "packages/ca_contracts/src", ROOT / "packages/ca_runtime/src", ROOT / "06_INTERVIEW_EXPRESSION/src"]):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))
from conscious_activations_interview_expression.media import MediaInspector


def test_ffprobe_reads_real_wav_and_preserves_portable_uri(tmp_path: Path) -> None:
    wav_path = tmp_path / "one_second.wav"
    sample_rate = 8_000
    with wave.open(str(wav_path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        handle.writeframes(b"\x00\x00" * sample_rate)

    asset = MediaInspector().inspect(
        wav_path,
        logical_uri="workspace://phase4/probe/one_second.wav",
        media_type="audio/wav",
    )

    assert asset["logical_uri"] == "workspace://phase4/probe/one_second.wav"
    assert asset["bytes"] == wav_path.stat().st_size
    assert asset["technical"]["probe_status"] == "PROBED"
    assert 990 <= asset["technical"]["duration_ms"] <= 1010
    assert any(stream["codec_type"] == "audio" for stream in asset["technical"]["streams"])
