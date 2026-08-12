import hashlib
from pathlib import Path
from cmf_builder.stage1.input_receipt import build_input_receipt, compute_file_sha256

def test_compute_sha256(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello")
    expected = hashlib.sha256(b"hello").hexdigest()
    assert compute_file_sha256(file_path) == expected

def test_input_receipt_match(tmp_path):
    file_path = tmp_path / "test.zip"
    file_path.write_text("zipcontent")
    expected_hash = compute_file_sha256(file_path)
    
    receipt = build_input_receipt(
        "h1", file_path, expected_hash, "google/gemini-2.5-flash", "https://openrouter.ai/api/v1", "user1"
    )
    assert receipt.match is True
    assert receipt.deviation_from_documented_pipeline is False
    assert receipt.operator_selected is True

def test_input_receipt_mismatch(tmp_path):
    file_path = tmp_path / "test.zip"
    file_path.write_text("zipcontent")
    
    receipt = build_input_receipt(
        "h1", file_path, "wronghash", "modelX", "urlY", "user1"
    )
    assert receipt.match is False
    assert receipt.deviation_from_documented_pipeline is True
