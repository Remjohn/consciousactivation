from __future__ import annotations
import json
from pathlib import Path
from cmf_pipeline.phase9_demo import run_phase9_demo

def test_phase9_reference_pilot(tmp_path):
    root=Path(__file__).resolve().parents[2]
    result=run_phase9_demo(tmp_path/'pilot',root)
    assert result['production_authorized'] is False
    assert result['certified'] is False
    assert result['format02_activated'] is False
    assert result['artifact_count']==5
    assert (tmp_path/'pilot'/'media'/'source-led-short.mp4').is_file()
    assert (tmp_path/'pilot'/'vae'/'reference-visual-asset.png').is_file()
    assert (tmp_path/'pilot'/'release_evidence.json').is_file()
