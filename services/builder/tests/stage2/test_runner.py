import json
import pytest
from pathlib import Path
from cmf_builder.stage2.runner import Stage2Runner, Stage2Config


def test_stage2_runner_pass(tmp_path):
    stage1_report_file = tmp_path / "format02_c01_STAGE1_REPORT.json"
    stage1_data = {
        "harness_id": "format02_c01",
        "stage1_complete": True,
        "input_receipt": {"source_zip_sha256": "a" * 64},
        "wrong_reading_locks": ["Badge locked"]
    }
    with open(stage1_report_file, "w") as f:
        json.dump(stage1_data, f)
        
    config = Stage2Config(
        harness_id="format02_c01",
        stage1_report_path=stage1_report_file,
        output_dir=tmp_path / "stage2_output"
    )
    runner = Stage2Runner(config)
    res = runner.run()
    
    assert res.status == "PASS"
    assert res.stage2_complete is True
    assert res.spec_path is not None and res.spec_path.exists()
    assert res.report_path.exists()
    assert res.deduplication_hash.startswith("sha256:")


def test_stage2_runner_missing_report(tmp_path):
    config = Stage2Config(
        harness_id="nonexistent",
        stage1_report_path=tmp_path / "missing_STAGE1_REPORT.json",
        output_dir=tmp_path / "stage2_output"
    )
    runner = Stage2Runner(config)
    res = runner.run()
    
    assert res.status == "FAIL"
    assert res.stage2_complete is False
    assert res.spec_path is None
    assert len(res.findings) > 0
