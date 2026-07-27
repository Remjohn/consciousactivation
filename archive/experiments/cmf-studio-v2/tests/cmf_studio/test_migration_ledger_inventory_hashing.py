from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope
from ccp_studio.contracts.legacy import LegacyAssetStatus, LegacyDisposition, new_target_map
from ccp_studio.services.command_bus import create_in_memory_command_bus
from ccp_studio.services.migration_service import (
    MigrationService,
    MigrationServiceError,
    register_migration_command_handlers,
)


def _target(reviewer_actor_id=None):
    return new_target_map(
        target_python_package="ccp_studio.services.calibration",
        pydantic_contract_target="ccp_studio.contracts.voice.CalibrationReport",
        dspy_program_target="ccp_studio.dspy_programs.AntiDraftCalibrationProgram",
        fixture_target="tests/fixtures/voice_dna_calibration_samples.json",
        eval_target="tests/evals/anti_draft_calibration_test.py",
        reviewer_actor_id=reviewer_actor_id or uuid4(),
    )


def _entry(service=None, actor_id=None):
    service = service or MigrationService()
    entry = service.propose_asset(
        source_path="src/ccp/services/anti_draft_calibrator.py",
        legacy_type="service_module",
        registry_family="Voice DNA Verification",
        canonicality_confidence=0.95,
        source_owner="CMF Core Team",
        runtime_language="Python",
        valuable_mechanics=["checks edited narrative against client speech patterns"],
        known_defects=["slow synchronous API calls"],
        content="legacy anti draft code v1",
        disposition=LegacyDisposition.reference_implementation,
        actor_id=actor_id,
    )
    return service, entry


def test_ledger_entry_records_inventory_fields_hash_and_status():
    service, entry = _entry()
    item = next(iter(service.repository.inventory_items.values()))

    assert entry.source_path == "src/ccp/services/anti_draft_calibrator.py"
    assert entry.legacy_type == "service_module"
    assert entry.registry_family == "Voice DNA Verification"
    assert entry.canonicality_confidence == 0.95
    assert entry.source_owner == "CMF Core Team"
    assert entry.runtime_language == "Python"
    assert "client speech patterns" in entry.valuable_mechanics[0]
    assert entry.known_defects == ["slow synchronous API calls"]
    assert len(entry.content_hash) == 64
    assert entry.status == LegacyAssetStatus.proposed
    assert item.content_hash == entry.content_hash


def test_target_map_required_before_activation_or_approval():
    service, entry = _entry()

    with pytest.raises(MigrationServiceError) as exc:
        service.activate_asset(entry.source_path)
    assert exc.value.code == "MIGRATION_TARGET_REQUIRED"

    with pytest.raises(MigrationServiceError) as approve_exc:
        service.approve_asset(entry_id=entry.migration_ledger_entry_id, reviewer_actor_id=uuid4())
    assert approve_exc.value.code == "MIGRATION_TARGET_REQUIRED"


def test_propose_map_approve_writes_migration_receipts():
    reviewer_id = uuid4()
    service, entry = _entry(actor_id=reviewer_id)

    mapped = service.map_asset(
        entry_id=entry.migration_ledger_entry_id,
        target_map=_target(reviewer_id),
        actor_id=reviewer_id,
    )
    approved = service.approve_asset(entry_id=entry.migration_ledger_entry_id, reviewer_actor_id=reviewer_id)
    receipts = service.repository.receipts_for_entry(entry.migration_ledger_entry_id)

    assert mapped.status == LegacyAssetStatus.mapped
    assert approved.status == LegacyAssetStatus.approved
    assert [receipt.decision_code for receipt in receipts] == [
        "LEGACY_ASSET_PROPOSED",
        "MIGRATION_TARGET_MAPPED",
        "LEGACY_ASSET_APPROVED",
    ]
    assert service.activate_asset(entry.source_path).status == LegacyAssetStatus.approved


def test_hash_change_flags_asset_for_review_without_silent_hash_update():
    reviewer_id = uuid4()
    service, entry = _entry(actor_id=reviewer_id)
    service.map_asset(entry_id=entry.migration_ledger_entry_id, target_map=_target(reviewer_id), actor_id=reviewer_id)
    service.approve_asset(entry_id=entry.migration_ledger_entry_id, reviewer_actor_id=reviewer_id)

    flag = service.refresh_hash(
        entry_id=entry.migration_ledger_entry_id,
        content="legacy anti draft code v2",
        actor_id=reviewer_id,
    )
    refreshed = service.repository.get_entry(entry.migration_ledger_entry_id)

    assert flag is not None
    assert flag.decision_code == "LEGACY_HASH_REVIEW_REQUIRED"
    assert flag.prior_content_hash == entry.content_hash
    assert flag.observed_content_hash != entry.content_hash
    assert refreshed.content_hash == entry.content_hash
    assert refreshed.status == LegacyAssetStatus.needs_hash_review


def test_blocked_asset_reference_returns_reason_and_replacement_target():
    reviewer_id = uuid4()
    service, entry = _entry(actor_id=reviewer_id)

    service.block_asset(
        entry_id=entry.migration_ledger_entry_id,
        reason="shell-coupled runtime cannot be imported",
        replacement_target="ccp_studio.dspy_programs.AntiDraftCalibrationProgram",
        actor_id=reviewer_id,
    )
    resolution = service.resolve_reference(source_path=entry.source_path)

    assert resolution.allowed is False
    assert resolution.decision_code == "LEGACY_ASSET_BLOCKED"
    assert resolution.reason == "shell-coupled runtime cannot be imported"
    assert resolution.replacement_target == "ccp_studio.dspy_programs.AntiDraftCalibrationProgram"


def test_unknown_legacy_asset_cannot_activate_or_resolve_as_allowed():
    service = MigrationService()

    resolution = service.resolve_reference(source_path="legacy/missing.py")
    with pytest.raises(MigrationServiceError) as exc:
        service.activate_asset("legacy/missing.py")

    assert resolution.allowed is False
    assert resolution.decision_code == "LEGACY_ASSET_NOT_LEDGERED"
    assert exc.value.code == "LEGACY_ASSET_NOT_LEDGERED"


def test_approved_status_requires_configured_reviewer():
    reviewer_id = uuid4()
    service, entry = _entry(actor_id=reviewer_id)
    service.map_asset(entry_id=entry.migration_ledger_entry_id, target_map=_target(reviewer_id), actor_id=reviewer_id)

    with pytest.raises(MigrationServiceError) as exc:
        service.approve_asset(entry_id=entry.migration_ledger_entry_id, reviewer_actor_id=uuid4())

    assert exc.value.code == "MIGRATION_REVIEWER_REQUIRED"


def test_migration_commands_run_through_command_bus_and_write_receipt():
    service = MigrationService()
    bus = create_in_memory_command_bus()
    register_migration_command_handlers(bus, service)
    org_id = uuid4()
    brand_id = uuid4()
    actor = ActorContext(actor_id=uuid4(), actor_type=ActorType.human, role_ids=["owner"])
    bus.brands.add_scope(org_id, brand_id)
    envelope = new_command_envelope(
        command_type="ProposeLegacyAssetCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "source_path": "legacy/receipt_chain.py",
            "legacy_type": "schema_module",
            "registry_family": "Receipt Chain",
            "canonicality_confidence": 0.9,
            "source_owner": "CMF Core Team",
            "runtime_language": "Python",
            "valuable_mechanics": ["receipt doctrine"],
            "known_defects": [],
            "content": "receipt chain v1",
            "disposition": LegacyDisposition.doctrine.value,
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert service.inspect_by_source_path("legacy/receipt_chain.py").status == LegacyAssetStatus.proposed
    assert next(iter(service.repository.receipts.values())).decision_code == "LEGACY_ASSET_PROPOSED"
