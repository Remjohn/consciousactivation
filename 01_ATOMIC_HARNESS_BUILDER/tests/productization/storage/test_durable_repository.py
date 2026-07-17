from __future__ import annotations

from dataclasses import replace
from hashlib import sha256

import pytest

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


def _record(version: int = 1, payload: bytes = b'{"run":"one"}\n') -> DurableRecord:
    return DurableRecord("builder_run", "run-1", version, payload, _hash(payload))


def _receipt(record: DurableRecord, command_id: str = "cmd-1") -> DurableCommandReceipt:
    return DurableCommandReceipt(
        command_id=command_id,
        payload_hash=_hash(f"command:{command_id}".encode()),
        result_kind=record.record_kind,
        result_id=record.record_id,
        result_hash=record.payload_hash,
    )


def test_record_and_receipt_commit_atomically_and_survive_reopen(tmp_path) -> None:
    path = tmp_path / "builder.sqlite3"
    first = SQLiteProductizationRepository(path)
    first.initialize()
    record = _record()
    receipt = _receipt(record)

    assert first.commit_record(record, command_receipt=receipt, expected_version=None) == receipt

    reopened = SQLiteProductizationRepository(path)
    reopened.initialize()
    assert reopened.get_record(record.record_kind, record.record_id) == record
    assert reopened.get_command_receipt(receipt.command_id) == receipt
    assert reopened.verify_integrity() == ()


def test_repeated_exact_command_is_payload_safe_and_conflict_fails_closed(tmp_path) -> None:
    repository = SQLiteProductizationRepository(tmp_path / "builder.sqlite3")
    repository.initialize()
    record = _record()
    receipt = _receipt(record)
    repository.commit_record(record, command_receipt=receipt, expected_version=None)

    assert repository.commit_record(record, command_receipt=receipt, expected_version=None) == receipt

    conflicting = replace(receipt, payload_hash=_hash(b"different command"))
    with pytest.raises(ProductizationError) as captured:
        repository.commit_record(
            record,
            command_receipt=conflicting,
            expected_version=None,
        )
    assert captured.value.code is ProductizationErrorCode.CONFLICT
    assert repository.get_command_receipt(receipt.command_id) == receipt


def test_expected_version_and_monotonic_version_are_enforced(tmp_path) -> None:
    repository = SQLiteProductizationRepository(tmp_path / "builder.sqlite3")
    repository.initialize()
    first = _record(version=7)
    repository.commit_record(first, command_receipt=_receipt(first), expected_version=None)
    second = _record(version=8, payload=b'{"run":"two"}\n')
    receipt = _receipt(second, "cmd-2")

    with pytest.raises(ProductizationError) as stale:
        repository.commit_record(second, command_receipt=receipt, expected_version=6)
    assert stale.value.code is ProductizationErrorCode.CONFLICT
    assert repository.get_record("builder_run", "run-1") == first

    repository.commit_record(second, command_receipt=receipt, expected_version=7)
    assert repository.get_record("builder_run", "run-1") == second


@pytest.mark.parametrize("boundary", ["after_record", "after_receipt"])
def test_injected_failure_rolls_back_record_and_receipt(tmp_path, boundary: str) -> None:
    repository = SQLiteProductizationRepository(tmp_path / "builder.sqlite3")
    repository.initialize()
    record = _record()
    receipt = _receipt(record)
    repository.inject_next_commit_failure(boundary)

    with pytest.raises(ProductizationError) as captured:
        repository.commit_record(record, command_receipt=receipt, expected_version=None)

    assert captured.value.code is ProductizationErrorCode.STORAGE_INTEGRITY
    assert repository.get_record(record.record_kind, record.record_id) is None
    assert repository.get_command_receipt(receipt.command_id) is None
    assert repository.verify_integrity() == ()


def test_altered_payload_is_rejected_before_write(tmp_path) -> None:
    repository = SQLiteProductizationRepository(tmp_path / "builder.sqlite3")
    repository.initialize()
    record = _record()
    altered = replace(record, payload=b"altered")

    with pytest.raises(ProductizationError) as captured:
        repository.commit_record(
            altered,
            command_receipt=_receipt(record),
            expected_version=None,
        )
    assert captured.value.code is ProductizationErrorCode.HASH_MISMATCH
    assert repository.get_record(record.record_kind, record.record_id) is None


def test_non_integer_versions_fail_closed(tmp_path) -> None:
    repository = SQLiteProductizationRepository(tmp_path / "builder.sqlite3")
    repository.initialize()
    record = replace(_record(), version=1.5)

    with pytest.raises(ProductizationError) as captured:
        repository.commit_record(
            record,
            command_receipt=_receipt(record),
            expected_version=None,
        )

    assert captured.value.code is ProductizationErrorCode.CONFLICT
