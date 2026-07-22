"""Registry conversion and activation service for TS-CMF-014."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ccp_studio.contracts.legacy import LegacyAssetStatus, LegacyDisposition
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.registry import (
    EvaluationTarget,
    FixtureSet,
    RegistryConflict,
    RegistryEntry,
    RegistryFamily,
    RegistryStatus,
    new_evaluation_target,
    new_fixture_set,
    new_registry_activation_receipt,
)
from ccp_studio.repositories.migration_ledger_entries import InMemoryMigrationLedgerRepository
from ccp_studio.repositories.registry_entries import InMemoryRegistryRepository


class RegistryServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class RegistryService:
    migration_repository: InMemoryMigrationLedgerRepository
    repository: InMemoryRegistryRepository = field(default_factory=InMemoryRegistryRepository)

    def convert_legacy_asset_to_registry(
        self,
        *,
        migration_ledger_entry_id: UUID,
        registry_family: RegistryFamily,
        payload: dict,
        reviewer_actor_id: UUID,
    ) -> RegistryEntry:
        ledger_entry = self.migration_repository.get_entry(migration_ledger_entry_id)
        if ledger_entry is None or ledger_entry.status != LegacyAssetStatus.approved:
            raise RegistryServiceError("LEGACY_ASSET_NOT_APPROVED", "Approved legacy asset is required.")
        if registry_family == RegistryFamily.cmf_reference_behavior and ledger_entry.disposition == LegacyDisposition.reference_implementation:
            payload = {**payload, "reference_behavior_only": not payload.get("production_code_approved", False)}
        entry = RegistryEntry(
            schema_version="cmf.registry_entry.v1",
            registry_entry_id=uuid4(),
            registry_family=registry_family,
            migration_ledger_entry_id=migration_ledger_entry_id,
            source_hash=ledger_entry.content_hash,
            payload=payload,
            fixture_set_ids=[],
            evaluation_target_ids=[],
            known_defects=ledger_entry.known_defects,
            reviewer_actor_id=reviewer_actor_id,
            status=RegistryStatus.draft,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        self.repository.put_entry(entry)
        self._detect_conflicts(entry)
        return entry

    def create_fixture_set(
        self,
        *,
        migration_ledger_entry_id: UUID,
        fixture_path: str,
        golden_examples: list[str],
        counterexamples: list[str],
        failure_cases: list[str],
    ) -> FixtureSet:
        fixture_set = new_fixture_set(
            migration_ledger_entry_id=migration_ledger_entry_id,
            fixture_path=fixture_path,
            golden_examples=golden_examples,
            counterexamples=counterexamples,
            failure_cases=failure_cases,
        )
        return self.repository.put_fixture_set(fixture_set)

    def create_evaluation_target(
        self,
        *,
        target_path: str,
        threshold: float | None = None,
        required: bool = True,
    ) -> EvaluationTarget:
        return self.repository.put_evaluation_target(
            new_evaluation_target(target_path=target_path, threshold=threshold, required=required)
        )

    def attach_fixture_set(self, *, registry_entry_id: UUID, fixture_set_id: UUID) -> RegistryEntry:
        entry = self._entry(registry_entry_id)
        if fixture_set_id not in self.repository.fixture_sets:
            raise RegistryServiceError("FIXTURE_SET_REQUIRED", "Fixture set is required.")
        return self.repository.put_entry(
            entry.model_copy(update={"fixture_set_ids": [*entry.fixture_set_ids, fixture_set_id], "updated_at": utc_now()})
        )

    def attach_evaluation_target(self, *, registry_entry_id: UUID, evaluation_target_id: UUID) -> RegistryEntry:
        entry = self._entry(registry_entry_id)
        if evaluation_target_id not in self.repository.evaluation_targets:
            raise RegistryServiceError("EVALUATION_TARGET_REQUIRED", "Evaluation target is required.")
        return self.repository.put_entry(
            entry.model_copy(
                update={"evaluation_target_ids": [*entry.evaluation_target_ids, evaluation_target_id], "updated_at": utc_now()}
            )
        )

    def activate_registry_entry(self, *, registry_entry_id: UUID) -> RegistryEntry:
        entry = self._entry(registry_entry_id)
        self._validate_activation(entry)
        activated = entry.model_copy(update={"status": RegistryStatus.active, "updated_at": utc_now()})
        self.repository.put_entry(activated)
        receipt = new_registry_activation_receipt(
            registry_entry=activated,
            decision_code="REGISTRY_ENTRY_ACTIVATED",
            evidence_refs=[
                activated.source_hash,
                *[str(item) for item in activated.fixture_set_ids],
                *[str(item) for item in activated.evaluation_target_ids],
            ],
        )
        self.repository.put_receipt(receipt)
        return activated

    def block_registry_entry(self, *, registry_entry_id: UUID, reason: str) -> RegistryEntry:
        entry = self._entry(registry_entry_id)
        blocked = entry.model_copy(update={"status": RegistryStatus.blocked, "updated_at": utc_now(), "payload": {**entry.payload, "block_reason": reason}})
        self.repository.put_entry(blocked)
        self.repository.put_receipt(
            new_registry_activation_receipt(
                registry_entry=blocked,
                decision_code="REGISTRY_ENTRY_BLOCKED",
                evidence_refs=[reason],
            )
        )
        return blocked

    def _validate_activation(self, entry: RegistryEntry) -> None:
        if not entry.payload.get("name"):
            raise RegistryServiceError("REGISTRY_SCHEMA_INVALID", "Registry payload requires a name.")
        if "raw_prompt" in entry.payload and len(entry.payload.keys()) <= 2:
            raise RegistryServiceError("REGISTRY_SCHEMA_INVALID", "Raw prompt alone cannot become an active registry.")
        if entry.registry_family == RegistryFamily.archetype and not entry.payload.get("route_constraints"):
            raise RegistryServiceError("REGISTRY_SCHEMA_INVALID", "Archetype route constraints are required.")
        if entry.registry_family == RegistryFamily.cmf_reference_behavior and entry.payload.get("activation_mode") == "production_code" and entry.payload.get("reference_behavior_only"):
            raise RegistryServiceError("REFERENCE_BEHAVIOR_ONLY", "CMF reference behavior is not approved as production code.")
        if not entry.fixture_set_ids:
            raise RegistryServiceError("FIXTURE_SET_REQUIRED", "Fixture set is required.")
        if not entry.evaluation_target_ids:
            raise RegistryServiceError("EVALUATION_TARGET_REQUIRED", "Evaluation target is required.")
        fixtures = [self.repository.fixture_sets[item] for item in entry.fixture_set_ids]
        if not any(fixture.golden_examples for fixture in fixtures) or not any(fixture.counterexamples for fixture in fixtures):
            raise RegistryServiceError("FIXTURE_SET_REQUIRED", "Golden examples and counterexamples are required.")
        if entry.registry_family == RegistryFamily.cognitive_primitive and not any(fixture.failure_cases for fixture in fixtures):
            raise RegistryServiceError("FIXTURE_FAILURE_CASE_REQUIRED", "Cognitive primitives require failure cases.")
        if self.repository.unresolved_conflicts_for_entry(entry.registry_entry_id):
            raise RegistryServiceError("REGISTRY_CONFLICT_REQUIRES_REVIEW", "Registry conflict requires review.")

    def _detect_conflicts(self, proposed: RegistryEntry) -> None:
        conflict_key = proposed.payload.get("name") or proposed.payload.get("route_key")
        if not conflict_key:
            return
        for existing in self.repository.registry_entries.values():
            if existing.registry_entry_id == proposed.registry_entry_id:
                continue
            existing_key = existing.payload.get("name") or existing.payload.get("route_key")
            if existing.registry_family == proposed.registry_family and existing_key == conflict_key and existing.status != RegistryStatus.deprecated:
                self.repository.put_conflict(
                    RegistryConflict(
                        schema_version="cmf.registry_conflict.v1",
                        registry_conflict_id=uuid4(),
                        registry_family=proposed.registry_family,
                        existing_registry_entry_id=existing.registry_entry_id,
                        proposed_registry_entry_id=proposed.registry_entry_id,
                        conflict_key=str(conflict_key),
                        created_at=utc_now(),
                    )
                )

    def _entry(self, registry_entry_id: UUID) -> RegistryEntry:
        entry = self.repository.registry_entries.get(registry_entry_id)
        if entry is None:
            raise RegistryServiceError("REGISTRY_ENTRY_REQUIRED", "Registry entry is required.")
        return entry
