from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

from cmf_builder.adapters.sqlite_productization_repository import (
    SQLiteProductizationRepository,
)
from cmf_builder.application.productization_contracts import (
    DurableCommandReceipt,
    DurableRecord,
)


def _hash(payload: bytes) -> str:
    return f"sha256:{sha256(payload).hexdigest()}"


def test_committed_record_is_readable_in_fresh_python_process(tmp_path) -> None:
    path = tmp_path / "builder.sqlite3"
    repository = SQLiteProductizationRepository(path)
    repository.initialize()
    payload = b'{"portable":true}\n'
    record = DurableRecord("builder_run", "run-fresh", 4, payload, _hash(payload))
    receipt = DurableCommandReceipt(
        "cmd-fresh", _hash(b"cmd-fresh"), "builder_run", "run-fresh", record.payload_hash
    )
    repository.commit_record(record, command_receipt=receipt, expected_version=None)

    root = Path(__file__).parents[3]
    helper = root / "tests" / "fixtures" / "productization" / "storage" / "read_durable_record.py"
    environment = dict(os.environ)
    source = str(root / "src")
    environment["PYTHONPATH"] = os.pathsep.join(
        item for item in (source, str(root), environment.get("PYTHONPATH", "")) if item
    )
    completed = subprocess.run(
        [
            sys.executable,
            str(helper),
            str(path),
            record.record_kind,
            record.record_id,
            receipt.command_id,
        ],
        cwd=root,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )

    observed = json.loads(completed.stdout)
    assert observed == {
        "integrity_issues": [],
        "receipt_hash": record.payload_hash,
        "record_hash": record.payload_hash,
        "record_version": 4,
    }

