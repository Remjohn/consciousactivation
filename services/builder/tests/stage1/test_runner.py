import zipfile
from pathlib import Path
from cmf_builder.stage1.runner import Stage1Runner, RunConfig, CheckpointResult
from cmf_builder.stage1.input_receipt import compute_file_sha256

def test_runner_full_run(tmp_path):
    zip_path = tmp_path / "specimen.zip"
    with zipfile.ZipFile(zip_path, 'w') as z:
        z.writestr("test.jpg", b"content")
        
    config = RunConfig(
        harness_id="h1",
        source_zip_path=zip_path,
        recorded_sha256=compute_file_sha256(zip_path),
        vision_model="model",
        base_url="http://url",
        selected_by="user1",
        output_dir=tmp_path / "out"
    )
    runner = Stage1Runner(config)
    result = runner.run()
    
    assert result.technical_status == "PASS"
    assert result.blocked_at is None
    assert result.contract_report is not None
    assert "08_final_receipt" in result.checkpoints_completed
    
    cp_dir = tmp_path / "out" / "checkpoints"
    assert (cp_dir / "01_input_receipt.json").exists()
    assert (cp_dir / "08_final_receipt.json").exists()

def test_runner_blocked_on_hash_mismatch(tmp_path):
    zip_path = tmp_path / "specimen.zip"
    with zipfile.ZipFile(zip_path, 'w') as z:
        z.writestr("test.jpg", b"content")
        
    config = RunConfig(
        harness_id="h1",
        source_zip_path=zip_path,
        recorded_sha256="wrong",
        vision_model="model",
        base_url="http://url",
        selected_by="user1",
        output_dir=tmp_path / "out2"
    )
    runner = Stage1Runner(config)
    result = runner.run()
    
    assert result.technical_status == "BLOCKED"
    assert result.blocked_at == "01_input_receipt"
    assert result.contract_report is None

def test_runner_resume(tmp_path):
    zip_path = tmp_path / "specimen.zip"
    with zipfile.ZipFile(zip_path, 'w') as z:
        z.writestr("test.jpg", b"content")
        
    out_dir = tmp_path / "out3"
    config = RunConfig(
        harness_id="h1",
        source_zip_path=zip_path,
        recorded_sha256=compute_file_sha256(zip_path),
        vision_model="model",
        base_url="http://url",
        selected_by="user1",
        output_dir=out_dir
    )
    runner = Stage1Runner(config)
    
    # Fake checkpoint 01
    runner.checkpoint_dir.mkdir(parents=True, exist_ok=True)
    import json
    with open(runner.checkpoint_dir / "01_input_receipt.json", "w") as f:
        json.dump({"checkpoint": "01_input_receipt", "status": "completed", "data": {"match": True}}, f)
        
    config.resume_from = "02_observation"
    runner2 = Stage1Runner(config)
    result = runner2.run()
    assert result.technical_status == "PASS"
    assert "01_input_receipt" in result.checkpoints_completed
