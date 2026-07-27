"""
Receipt Chain Writer — Cryptographic audit trail for all pipeline stages.

Build Prompt Stage 4: Every stage that mutates data state writes a receipt.
Receipt schema: receipt_id + previous_receipt_hash + input_payload_hash +
output_payload_hash + stage_name + agent_name + timestamp.
"""

import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


def compute_payload_hash(payload: Any) -> str:
    """Compute SHA-256 hash of a JSON-serializable payload."""
    serialized = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def compute_receipt_hash(receipt: dict) -> str:
    """Compute SHA-256 hash of a receipt for chain linking."""
    serialized = json.dumps(receipt, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def write_receipt(
    stage_name: str,
    agent_name: str,
    input_payload: Any,
    output_payload: Any,
    previous_receipt: Optional[dict],
    output_dir: str,
) -> dict:
    """
    Write a receipt for a completed pipeline stage.

    The receipt is written to disk as JSON and returned for chaining
    to the next stage via previous_receipt_hash.

    Args:
        stage_name: Pipeline stage identifier (e.g., T2I_PAYLOAD_COMPILE).
        agent_name: Agent that executed the stage (e.g., runninghub_t2i_client).
        input_payload: Stage input data (hashed, not stored verbatim).
        output_payload: Stage output data (hashed, not stored verbatim).
        previous_receipt: Prior receipt in the chain (None for first stage).
        output_dir: Directory for receipt JSON files.

    Returns:
        The receipt dict for chaining to the next stage.
    """
    receipt_id = str(uuid.uuid4())
    previous_hash = (
        compute_receipt_hash(previous_receipt) if previous_receipt else "GENESIS"
    )
    input_hash = compute_payload_hash(input_payload)
    output_hash = compute_payload_hash(output_payload)

    receipt = {
        "receipt_id": receipt_id,
        "previous_receipt_hash": previous_hash,
        "input_payload_hash": input_hash,
        "output_payload_hash": output_hash,
        "stage_name": stage_name,
        "agent_name": agent_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    receipt_file = output_path / f"receipt_{stage_name}_{receipt_id[:8]}.json"
    receipt_file.write_text(json.dumps(receipt, indent=2))

    return receipt
