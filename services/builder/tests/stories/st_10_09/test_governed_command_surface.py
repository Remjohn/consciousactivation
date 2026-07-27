import pytest

from cmf_builder.application.governed_command_surface import (
    CommandType,
    GovernedCommand,
    GovernedCommandError,
    InMemoryCommandLedger,
    export_receipt_bundle,
)


def command(command_id="cmd:1", command_type=CommandType.LIST_RUNS, **overrides):
    values = {
        "command_id": command_id,
        "command_type": command_type,
        "operator_identity": "operator:emilio",
        "authority_requirement": "read:development",
        "input_contract": {"subject": "run:1"},
        "requested_scope": "development",
        "source_revision": "rev:1",
        "execution_timestamp": "2026-07-17T00:00:00Z",
    }
    values.update(overrides)
    return GovernedCommand(**values)


def test_read_only_command_receipts_are_deterministic_and_idempotent():
    ledger = InMemoryCommandLedger()
    cmd = command()
    receipt1 = ledger.execute(cmd, authority_granted=True, result_payload={"runs": ["run:1"], "stale": False})
    receipt2 = ledger.execute(cmd, authority_granted=True, result_payload={"runs": ["changed"]})

    assert receipt1 == receipt2
    assert receipt1.result_status == "PASS"
    assert receipt1.certified is False


def test_authority_invalid_input_and_export_safety_fail_closed():
    ledger = InMemoryCommandLedger()
    with pytest.raises(GovernedCommandError) as auth:
        ledger.execute(command(), authority_granted=False, result_payload={})
    assert auth.value.code == "COMMAND_AUTHORITY_DENIED"

    with pytest.raises(GovernedCommandError) as invalid:
        ledger.execute(command(input_contract={}), authority_granted=True, result_payload={})
    assert invalid.value.code == "INVALID_COMMAND_INPUT"

    for payload, code in (
        ({"absolute_path": "C:/secret"}, "PORTABLE_EXPORT_ABSOLUTE_PATH"),
        ({"secret": "value"}, "SECRET_IN_COMMAND_RECEIPT"),
        ({"invalidated_as_active": True}, "INVALIDATED_RECORD_EXPORT_ACTIVE"),
        ({"production_ready": True}, "DEVELOPMENT_EXPORTED_AS_PRODUCTION_CERTIFICATION"),
    ):
        with pytest.raises(GovernedCommandError) as exc:
            ledger.execute(command(command_id=f"cmd:{code}"), authority_granted=True, result_payload=payload)
        assert exc.value.code == code


def test_receipt_and_evidence_bundle_export_is_portable_and_hash_bound():
    bundle = export_receipt_bundle(("receipt:1",), {"receipt:1": "a" * 64}, ({"receipt": "payload"},), ("redacted:1",))

    assert bundle["export_identity"]
    assert bundle["deterministic_manifest"]
    assert bundle["production_ready"] is False
    assert bundle["certified"] is False
    assert bundle["excluded_redacted_objects"] == ["redacted:1"]
