from __future__ import annotations
import subprocess
import pytest
from pathlib import Path

@pytest.fixture
def source_video(tmp_path:Path)->Path:
    path=tmp_path/'source.mp4'
    p=subprocess.run(['ffmpeg','-y','-v','error','-f','lavfi','-i','testsrc2=size=360x640:rate=30','-f','lavfi','-i','sine=frequency=330:sample_rate=48000','-t','4','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(path)],text=True,capture_output=True)
    assert p.returncode==0,p.stderr
    return path
