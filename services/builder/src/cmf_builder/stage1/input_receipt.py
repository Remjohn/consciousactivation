import hashlib
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, timezone

@dataclass
class InputReceipt:
    harness_id: str
    source_zip_path: str
    source_zip_sha256_recorded: str
    source_zip_sha256_observed_now: str
    match: bool
    vision_model_used: str
    base_url: str
    deviation_from_documented_pipeline: bool
    operator_selected: bool
    selected_by: str
    selected_at: str

def compute_file_sha256(path: Path) -> str:
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def build_input_receipt(
    harness_id: str,
    source_zip_path: Path,
    recorded_sha256: str,
    vision_model: str,
    base_url: str,
    selected_by: str,
    documented_model: str = 'google/gemini-2.5-flash',
    documented_base_url: str = 'https://openrouter.ai/api/v1'
) -> InputReceipt:
    observed_sha256 = compute_file_sha256(source_zip_path)
    match = (observed_sha256 == recorded_sha256)
    deviation = (vision_model != documented_model) or (base_url != documented_base_url)
    
    return InputReceipt(
        harness_id=harness_id,
        source_zip_path=str(source_zip_path),
        source_zip_sha256_recorded=recorded_sha256,
        source_zip_sha256_observed_now=observed_sha256,
        match=match,
        vision_model_used=vision_model,
        base_url=base_url,
        deviation_from_documented_pipeline=deviation,
        operator_selected=True,
        selected_by=selected_by,
        selected_at=datetime.now(timezone.utc).isoformat()
    )
