import pytest
from pathlib import Path
import zipfile
from cmf_builder.stage1.stage1_cli import main

def test_stage1_cli_success(tmp_path: Path):
    zip_path = tmp_path / "test_harness.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("01.jpg", b"fake_jpeg_content")

    output_dir = tmp_path / "output"
    
    argv = [
        "--harness-id", "TEST-001",
        "--source-zip", str(zip_path),
        "--output-dir", str(output_dir)
    ]
    
    code = main(argv)
    assert code == 0
    assert (output_dir / "TEST-001_STAGE1_REPORT.json").exists()

def test_stage1_cli_missing_file(tmp_path: Path):
    argv = [
        "--harness-id", "TEST-001",
        "--source-zip", str(tmp_path / "non_existent.zip")
    ]
    code = main(argv)
    assert code == 1
