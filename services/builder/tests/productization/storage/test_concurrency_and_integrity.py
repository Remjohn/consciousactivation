from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import sqlite3

from cmf_builder.adapters.sqlite_productization_repository import (
    SQLiteProductizationRepository,
)
from cmf_builder.application.productization_contracts import (
    DurableCommandReceipt,
    DurableRecord,
    ProductizationError,
    ProductizationErrorCode,
)


def _hash(payload: bytes) -> str:
    return f"sha256:{sha256(payload).hexdigest()}"


def _commit_candidate(path, command_id: str, payload: bytes) -> str:
    repository = SQLiteProductizationRepository(path, timeout_seconds=10.0)
    record = DurableRecord("builder_run", "run-1", 2, payload, _hash(payload))
    receipt = DurableCommandReceipt(
        command_id,
        _hash(command_id.encode()),
        record.record_kind,
        record.record_id,
        record.payload_hash,
    )
    try:
        repository.commit_record(record, command_receipt=receipt, expected_version=1)
    except ProductizationError as error:
        return error.code.value
    return "PASS"


def test_concurrent_expected_version_allows_exactly_one_writer(tmp_path) -> None:
    path = tmp_path / "builder.sqlite3"
    repository = SQLiteProductizationRepository(path)
    repository.initialize()
    initial_payload = b"initial"
    initial = DurableRecord("builder_run", "run-1", 1, initial_payload, _hash(initial_payload))
    initial_receipt = DurableCommandReceipt(
        "cmd-initial", _hash(b"cmd-initial"), "builder_run", "run-1", initial.payload_hash
    )
    repository.commit_record(initial, command_receipt=initial_receipt, expected_version=None)

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = tuple(
            executor.map(
                lambda item: _commit_candidate(path, *item),
                (("cmd-a", b"candidate-a"), ("cmd-b", b"candidate-b")),
            )
        )

    assert sorted(results) == [ProductizationErrorCode.CONFLICT.value, "PASS"]
    assert repository.get_record("builder_run", "run-1").version == 2
    assert repository.verify_integrity() == ()


def test_integrity_scan_detects_tampered_bytes(tmp_path) -> None:
    path = tmp_path / "builder.sqlite3"
    repository = SQLiteProductizationRepository(path)
    repository.initialize()
    payload = b"governed"
    record = DurableRecord("builder_run", "run-1", 1, payload, _hash(payload))
    receipt = DurableCommandReceipt(
        "cmd-1", _hash(b"cmd-1"), "builder_run", "run-1", record.payload_hash
    )
    repository.commit_record(record, command_receipt=receipt, expected_version=None)

    connection = sqlite3.connect(path)
    try:
        connection.execute(
            "UPDATE durable_records SET payload = ? WHERE record_kind = ? AND record_id = ?",
            (b"tampered", "builder_run", "run-1"),
        )
        connection.commit()
    finally:
        connection.close()

    assert repository.verify_integrity() == ("RECORD_HASH_MISMATCH:builder_run:run-1:1",)
    try:
        repository.get_record("builder_run", "run-1")
    except ProductizationError as error:
        assert error.code is ProductizationErrorCode.HASH_MISMATCH
    else:
        raise AssertionError("Tampered bytes must fail closed when loaded.")

