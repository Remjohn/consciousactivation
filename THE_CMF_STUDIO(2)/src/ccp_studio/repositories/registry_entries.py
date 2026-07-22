"""Registry conversion repositories for TS-CMF-014."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.registry import (
    EvaluationTarget,
    FixtureSet,
    RegistryActivationReceipt,
    RegistryConflict,
    RegistryEntry,
)


@dataclass
class InMemoryRegistryRepository:
    registry_entries: dict[UUID, RegistryEntry] = field(default_factory=dict)
    fixture_sets: dict[UUID, FixtureSet] = field(default_factory=dict)
    evaluation_targets: dict[UUID, EvaluationTarget] = field(default_factory=dict)
    activation_receipts: dict[UUID, RegistryActivationReceipt] = field(default_factory=dict)
    conflicts: dict[UUID, RegistryConflict] = field(default_factory=dict)

    def put_entry(self, entry: RegistryEntry) -> RegistryEntry:
        self.registry_entries[entry.registry_entry_id] = entry
        return entry

    def put_fixture_set(self, fixture_set: FixtureSet) -> FixtureSet:
        self.fixture_sets[fixture_set.fixture_set_id] = fixture_set
        return fixture_set

    def put_evaluation_target(self, target: EvaluationTarget) -> EvaluationTarget:
        self.evaluation_targets[target.evaluation_target_id] = target
        return target

    def put_receipt(self, receipt: RegistryActivationReceipt) -> RegistryActivationReceipt:
        self.activation_receipts[receipt.registry_activation_receipt_id] = receipt
        return receipt

    def put_conflict(self, conflict: RegistryConflict) -> RegistryConflict:
        self.conflicts[conflict.registry_conflict_id] = conflict
        return conflict

    def unresolved_conflicts_for_entry(self, registry_entry_id: UUID) -> list[RegistryConflict]:
        return [
            conflict
            for conflict in self.conflicts.values()
            if not conflict.resolved
            and (
                conflict.proposed_registry_entry_id == registry_entry_id
                or conflict.existing_registry_entry_id == registry_entry_id
            )
        ]
