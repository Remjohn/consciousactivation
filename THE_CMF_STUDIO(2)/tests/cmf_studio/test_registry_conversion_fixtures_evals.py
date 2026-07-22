from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.legacy import LegacyAssetStatus, LegacyDisposition, new_target_map
from ccp_studio.contracts.registry import RegistryFamily, RegistryStatus
from ccp_studio.services.migration_service import MigrationService
from ccp_studio.services.registry_service import RegistryService, RegistryServiceError


def _approved_ledger(disposition=LegacyDisposition.registry, source_path="legacy/archetypes/challenger.md"):
    reviewer_id = uuid4()
    migration = MigrationService()
    entry = migration.propose_asset(
        source_path=source_path,
        legacy_type="prompt_family",
        registry_family="Archetype",
        canonicality_confidence=0.94,
        source_owner="CMF Core Team",
        runtime_language="Markdown",
        valuable_mechanics=["route constraints and counter-positioning"],
        known_defects=["prompt-only legacy form"],
        content=f"{source_path}: challenger prompt v1",
        disposition=disposition,
        actor_id=reviewer_id,
    )
    migration.map_asset(
        entry_id=entry.migration_ledger_entry_id,
        target_map=new_target_map(
            target_python_package="ccp_studio.contracts.registry",
            pydantic_contract_target="ccp_studio.contracts.registry.RegistryEntry",
            dspy_program_target="ccp_studio.dspy_programs.registry_eval",
            fixture_target="tests/fixtures/registry/challenger.json",
            eval_target="tests/evals/test_registry_activation_eval.py",
            reviewer_actor_id=reviewer_id,
        ),
        actor_id=reviewer_id,
    )
    approved = migration.approve_asset(entry_id=entry.migration_ledger_entry_id, reviewer_actor_id=reviewer_id)
    assert approved.status == LegacyAssetStatus.approved
    return migration, approved, reviewer_id


def _registry_service(disposition=LegacyDisposition.registry, source_path="legacy/archetypes/challenger.md"):
    migration, entry, reviewer_id = _approved_ledger(disposition=disposition, source_path=source_path)
    return RegistryService(migration.repository), entry, reviewer_id


def _attach_fixture_and_eval(service, entry, registry_entry, failure_cases=None):
    fixture = service.create_fixture_set(
        migration_ledger_entry_id=entry.migration_ledger_entry_id,
        fixture_path="tests/fixtures/registry/challenger.json",
        golden_examples=["strong route example"],
        counterexamples=["weak centroid example"],
        failure_cases=["forced route failure"] if failure_cases is None else failure_cases,
    )
    target = service.create_evaluation_target(
        target_path="tests/evals/test_registry_activation_eval.py",
        threshold=0.85,
    )
    registry_entry = service.attach_fixture_set(
        registry_entry_id=registry_entry.registry_entry_id,
        fixture_set_id=fixture.fixture_set_id,
    )
    registry_entry = service.attach_evaluation_target(
        registry_entry_id=registry_entry.registry_entry_id,
        evaluation_target_id=target.evaluation_target_id,
    )
    return registry_entry, fixture, target


def test_approved_archetype_prompt_converts_to_typed_registry_with_fixtures_eval_and_receipt():
    service, entry, reviewer_id = _registry_service()
    draft = service.convert_legacy_asset_to_registry(
        migration_ledger_entry_id=entry.migration_ledger_entry_id,
        registry_family=RegistryFamily.archetype,
        payload={"name": "challenger", "route_constraints": ["must confront weak frame"], "examples": ["edge"]},
        reviewer_actor_id=reviewer_id,
    )
    draft, fixture, target = _attach_fixture_and_eval(service, entry, draft)

    active = service.activate_registry_entry(registry_entry_id=draft.registry_entry_id)
    receipt = next(iter(service.repository.activation_receipts.values()))

    assert active.status == RegistryStatus.active
    assert active.source_hash == entry.content_hash
    assert fixture.golden_examples and fixture.counterexamples
    assert target.required is True
    assert receipt.decision_code == "REGISTRY_ENTRY_ACTIVATED"
    assert str(fixture.fixture_set_id) in receipt.evidence_refs


def test_cognitive_primitive_activation_requires_examples_failure_cases_and_family():
    service, entry, reviewer_id = _registry_service(source_path="legacy/primitives/friction.md")
    draft = service.convert_legacy_asset_to_registry(
        migration_ledger_entry_id=entry.migration_ledger_entry_id,
        registry_family=RegistryFamily.cognitive_primitive,
        payload={"name": "productive_friction", "schema_fields": ["trigger", "movement"]},
        reviewer_actor_id=reviewer_id,
    )
    draft, _fixture, _target = _attach_fixture_and_eval(service, entry, draft, failure_cases=[])

    with pytest.raises(RegistryServiceError) as exc:
        service.activate_registry_entry(registry_entry_id=draft.registry_entry_id)

    assert exc.value.code == "FIXTURE_FAILURE_CASE_REQUIRED"


def test_sda_sfl_fixtures_support_downstream_extraction_audio_compression_and_eval_targets():
    service, entry, reviewer_id = _registry_service(source_path="legacy/sfl/sonic_profile.yml")
    draft = service.convert_legacy_asset_to_registry(
        migration_ledger_entry_id=entry.migration_ledger_entry_id,
        registry_family=RegistryFamily.sfl,
        payload={"name": "sonic_compression_profile", "schema_fields": ["audio", "compression", "evaluation"]},
        reviewer_actor_id=reviewer_id,
    )
    draft, fixture, target = _attach_fixture_and_eval(service, entry, draft)

    active = service.activate_registry_entry(registry_entry_id=draft.registry_entry_id)

    assert active.registry_family == RegistryFamily.sfl
    assert "registry" in fixture.fixture_path
    assert target.target_path.endswith("test_registry_activation_eval.py")


def test_cmf_engine_reference_not_approved_as_code_is_reference_behavior_only():
    service, entry, reviewer_id = _registry_service(
        disposition=LegacyDisposition.reference_implementation,
        source_path="legacy/cmf/audio_engine.py",
    )
    draft = service.convert_legacy_asset_to_registry(
        migration_ledger_entry_id=entry.migration_ledger_entry_id,
        registry_family=RegistryFamily.cmf_reference_behavior,
        payload={"name": "audio_ducking_behavior", "activation_mode": "production_code"},
        reviewer_actor_id=reviewer_id,
    )
    draft, _fixture, _target = _attach_fixture_and_eval(service, entry, draft)

    with pytest.raises(RegistryServiceError) as exc:
        service.activate_registry_entry(registry_entry_id=draft.registry_entry_id)

    assert exc.value.code == "REFERENCE_BEHAVIOR_ONLY"
    assert draft.payload["reference_behavior_only"] is True


def test_registry_entry_lacking_eval_coverage_is_blocked():
    service, entry, reviewer_id = _registry_service()
    draft = service.convert_legacy_asset_to_registry(
        migration_ledger_entry_id=entry.migration_ledger_entry_id,
        registry_family=RegistryFamily.archetype,
        payload={"name": "challenger", "route_constraints": ["must confront weak frame"]},
        reviewer_actor_id=reviewer_id,
    )
    fixture = service.create_fixture_set(
        migration_ledger_entry_id=entry.migration_ledger_entry_id,
        fixture_path="tests/fixtures/registry/challenger.json",
        golden_examples=["strong"],
        counterexamples=["weak"],
        failure_cases=["failure"],
    )
    draft = service.attach_fixture_set(registry_entry_id=draft.registry_entry_id, fixture_set_id=fixture.fixture_set_id)

    with pytest.raises(RegistryServiceError) as exc:
        service.activate_registry_entry(registry_entry_id=draft.registry_entry_id)

    assert exc.value.code == "EVALUATION_TARGET_REQUIRED"


def test_raw_prompt_cannot_become_active_registry():
    service, entry, reviewer_id = _registry_service()
    draft = service.convert_legacy_asset_to_registry(
        migration_ledger_entry_id=entry.migration_ledger_entry_id,
        registry_family=RegistryFamily.archetype,
        payload={"raw_prompt": "be a challenger"},
        reviewer_actor_id=reviewer_id,
    )
    draft, _fixture, _target = _attach_fixture_and_eval(service, entry, draft)

    with pytest.raises(RegistryServiceError) as exc:
        service.activate_registry_entry(registry_entry_id=draft.registry_entry_id)

    assert exc.value.code == "REGISTRY_SCHEMA_INVALID"


def test_duplicate_registry_truth_blocks_activation_until_conflict_review():
    service, entry, reviewer_id = _registry_service()
    first = service.convert_legacy_asset_to_registry(
        migration_ledger_entry_id=entry.migration_ledger_entry_id,
        registry_family=RegistryFamily.archetype,
        payload={"name": "challenger", "route_constraints": ["must confront weak frame"]},
        reviewer_actor_id=reviewer_id,
    )
    first, _fixture, _target = _attach_fixture_and_eval(service, entry, first)
    service.activate_registry_entry(registry_entry_id=first.registry_entry_id)
    _migration, second_entry, _second_reviewer = _approved_ledger(source_path="legacy/archetypes/challenger_alt.md")
    service.migration_repository.put_entry(second_entry)
    second = service.convert_legacy_asset_to_registry(
        migration_ledger_entry_id=second_entry.migration_ledger_entry_id,
        registry_family=RegistryFamily.archetype,
        payload={"name": "challenger", "route_constraints": ["alternate route"]},
        reviewer_actor_id=reviewer_id,
    )
    second, _fixture, _target = _attach_fixture_and_eval(service, second_entry, second)

    with pytest.raises(RegistryServiceError) as exc:
        service.activate_registry_entry(registry_entry_id=second.registry_entry_id)

    assert exc.value.code == "REGISTRY_CONFLICT_REQUIRES_REVIEW"
    assert len(service.repository.conflicts) == 1
