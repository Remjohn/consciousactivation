"""Legacy migration ledger service for TS-CMF-013."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.legacy import (
    BlockedReferenceResolution,
    HashReviewFlag,
    LegacyAssetInventoryItem,
    LegacyAssetStatus,
    LegacyDisposition,
    MigrationLedgerEntry,
    MigrationReceipt,
    MigrationTargetMap,
    new_migration_receipt,
    new_target_map,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.repositories.migration_ledger_entries import InMemoryMigrationLedgerRepository
from ccp_studio.services.command_bus import CommandBus


class MigrationServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class MigrationService:
    repository: InMemoryMigrationLedgerRepository = field(default_factory=InMemoryMigrationLedgerRepository)

    @staticmethod
    def content_hash(content: str | bytes) -> str:
        if isinstance(content, str):
            content = content.encode("utf-8")
        return hashlib.sha256(content).hexdigest()

    def propose_asset(
        self,
        *,
        source_path: str,
        legacy_type: str,
        registry_family: str | None,
        canonicality_confidence: float,
        source_owner: str,
        runtime_language: str | None,
        valuable_mechanics: list[str],
        known_defects: list[str],
        content: str | bytes,
        disposition: LegacyDisposition,
        actor_id: UUID | None = None,
    ) -> MigrationLedgerEntry:
        content_hash = self.content_hash(content)
        now = utc_now()
        inventory_item = LegacyAssetInventoryItem(
            schema_version="cmf.legacy_asset_inventory_item.v1",
            legacy_asset_inventory_item_id=uuid4(),
            source_path=source_path,
            legacy_type=legacy_type,
            registry_family=registry_family,
            canonicality_confidence=canonicality_confidence,
            source_owner=source_owner,
            runtime_language=runtime_language,
            valuable_mechanics=valuable_mechanics,
            known_defects=known_defects,
            content_hash=content_hash,
            created_at=now,
        )
        self.repository.put_inventory_item(inventory_item)
        entry = MigrationLedgerEntry(
            schema_version="cmf.migration_ledger_entry.v1",
            migration_ledger_entry_id=uuid4(),
            source_path=source_path,
            legacy_type=legacy_type,
            registry_family=registry_family,
            canonicality_confidence=canonicality_confidence,
            source_owner=source_owner,
            runtime_language=runtime_language,
            valuable_mechanics=valuable_mechanics,
            known_defects=known_defects,
            content_hash=content_hash,
            disposition=disposition,
            target_map=new_target_map(),
            status=LegacyAssetStatus.proposed,
            created_at=now,
            updated_at=now,
        )
        self.repository.put_entry(entry)
        self._write_receipt(
            entry,
            action="ProposeLegacyAssetCommand",
            decision_code="LEGACY_ASSET_PROPOSED",
            actor_id=actor_id,
            evidence_refs=[content_hash],
        )
        return entry

    def map_asset(
        self,
        *,
        entry_id: UUID,
        target_map: MigrationTargetMap,
        actor_id: UUID | None = None,
    ) -> MigrationLedgerEntry:
        entry = self._require_entry(entry_id)
        self._validate_target_map(target_map)
        updated = entry.model_copy(
            update={
                "target_map": target_map,
                "status": LegacyAssetStatus.mapped,
                "updated_at": utc_now(),
            }
        )
        self.repository.put_entry(updated)
        self._write_receipt(
            updated,
            action="MapLegacyAssetCommand",
            decision_code="MIGRATION_TARGET_MAPPED",
            actor_id=actor_id,
            evidence_refs=[
                target_map.target_python_package or "",
                target_map.pydantic_contract_target or "",
                target_map.fixture_target or "",
                target_map.eval_target or "",
            ],
        )
        return updated

    def approve_asset(self, *, entry_id: UUID, reviewer_actor_id: UUID) -> MigrationLedgerEntry:
        entry = self._require_entry(entry_id)
        self._validate_target_map(entry.target_map)
        if entry.target_map.reviewer_actor_id != reviewer_actor_id:
            raise MigrationServiceError("MIGRATION_REVIEWER_REQUIRED", "Approved reviewer must match target map.")
        if entry.status == LegacyAssetStatus.needs_hash_review:
            raise MigrationServiceError("LEGACY_HASH_REVIEW_REQUIRED", "Hash review is required before approval.")
        updated = entry.model_copy(
            update={
                "status": LegacyAssetStatus.approved,
                "updated_at": utc_now(),
            }
        )
        self.repository.put_entry(updated)
        self._write_receipt(
            updated,
            action="ApproveLegacyAssetCommand",
            decision_code="LEGACY_ASSET_APPROVED",
            actor_id=reviewer_actor_id,
            evidence_refs=[updated.content_hash],
        )
        return updated

    def block_asset(
        self,
        *,
        entry_id: UUID,
        reason: str,
        replacement_target: str | None,
        actor_id: UUID | None = None,
    ) -> MigrationLedgerEntry:
        entry = self._require_entry(entry_id)
        updated = entry.model_copy(
            update={
                "status": LegacyAssetStatus.blocked,
                "block_reason": reason,
                "replacement_target": replacement_target,
                "updated_at": utc_now(),
            }
        )
        self.repository.put_entry(updated)
        self._write_receipt(
            updated,
            action="BlockLegacyAssetCommand",
            decision_code="LEGACY_ASSET_BLOCKED",
            actor_id=actor_id,
            evidence_refs=[reason, replacement_target or ""],
        )
        return updated

    def refresh_hash(
        self,
        *,
        entry_id: UUID,
        content: str | bytes,
        actor_id: UUID | None = None,
    ) -> HashReviewFlag | None:
        entry = self._require_entry(entry_id)
        observed_hash = self.content_hash(content)
        if observed_hash == entry.content_hash:
            self._write_receipt(
                entry,
                action="RefreshLegacyAssetHashCommand",
                decision_code="LEGACY_HASH_UNCHANGED",
                actor_id=actor_id,
                evidence_refs=[entry.content_hash],
            )
            return None
        updated = entry.model_copy(update={"status": LegacyAssetStatus.needs_hash_review, "updated_at": utc_now()})
        self.repository.put_entry(updated)
        flag = HashReviewFlag(
            schema_version="cmf.hash_review_flag.v1",
            hash_review_flag_id=uuid4(),
            migration_ledger_entry_id=entry.migration_ledger_entry_id,
            source_path=entry.source_path,
            prior_content_hash=entry.content_hash,
            observed_content_hash=observed_hash,
            decision_code="LEGACY_HASH_REVIEW_REQUIRED",
            created_at=utc_now(),
        )
        self.repository.put_hash_review_flag(flag)
        self._write_receipt(
            updated,
            action="RefreshLegacyAssetHashCommand",
            decision_code="LEGACY_HASH_REVIEW_REQUIRED",
            actor_id=actor_id,
            evidence_refs=[entry.content_hash, observed_hash],
        )
        return flag

    def resolve_reference(self, *, source_path: str) -> BlockedReferenceResolution:
        entry = self.repository.get_by_source_path(source_path)
        if entry is None:
            return BlockedReferenceResolution(
                schema_version="cmf.blocked_reference_resolution.v1",
                source_path=source_path,
                allowed=False,
                decision_code="LEGACY_ASSET_NOT_LEDGERED",
            )
        if entry.status == LegacyAssetStatus.blocked:
            return BlockedReferenceResolution(
                schema_version="cmf.blocked_reference_resolution.v1",
                source_path=source_path,
                allowed=False,
                decision_code="LEGACY_ASSET_BLOCKED",
                reason=entry.block_reason,
                replacement_target=entry.replacement_target,
                migration_ledger_entry_id=entry.migration_ledger_entry_id,
            )
        if entry.status == LegacyAssetStatus.deprecated:
            return BlockedReferenceResolution(
                schema_version="cmf.blocked_reference_resolution.v1",
                source_path=source_path,
                allowed=False,
                decision_code="LEGACY_ASSET_DEPRECATED",
                reason=entry.block_reason,
                replacement_target=entry.replacement_target,
                migration_ledger_entry_id=entry.migration_ledger_entry_id,
            )
        return BlockedReferenceResolution(
            schema_version="cmf.blocked_reference_resolution.v1",
            source_path=source_path,
            allowed=True,
            decision_code="LEGACY_ASSET_LEDGERED",
            migration_ledger_entry_id=entry.migration_ledger_entry_id,
        )

    def inspect_by_source_path(self, source_path: str) -> MigrationLedgerEntry:
        entry = self.repository.get_by_source_path(source_path)
        if entry is None:
            raise MigrationServiceError("LEGACY_ASSET_NOT_LEDGERED", "Legacy asset is not ledgered.")
        return entry

    def activate_asset(self, source_path: str) -> MigrationLedgerEntry:
        entry = self.repository.get_by_source_path(source_path)
        if entry is None:
            raise MigrationServiceError("LEGACY_ASSET_NOT_LEDGERED", "Legacy asset is not ledgered.")
        if entry.status == LegacyAssetStatus.blocked:
            raise MigrationServiceError("LEGACY_ASSET_BLOCKED", entry.block_reason or "Legacy asset is blocked.")
        if entry.status == LegacyAssetStatus.needs_hash_review:
            raise MigrationServiceError("LEGACY_HASH_REVIEW_REQUIRED", "Hash review is required.")
        self._validate_target_map(entry.target_map)
        if entry.status != LegacyAssetStatus.approved:
            raise MigrationServiceError("LEGACY_ASSET_NOT_APPROVED", "Legacy asset is not approved.")
        return entry

    def _write_receipt(
        self,
        entry: MigrationLedgerEntry,
        *,
        action: str,
        decision_code: str,
        actor_id: UUID | None,
        evidence_refs: list[str],
    ) -> MigrationReceipt:
        return self.repository.put_receipt(
            new_migration_receipt(
                migration_ledger_entry_id=entry.migration_ledger_entry_id,
                source_path=entry.source_path,
                action=action,
                decision_code=decision_code,
                actor_id=actor_id,
                evidence_refs=evidence_refs,
            )
        )

    def _require_entry(self, entry_id: UUID) -> MigrationLedgerEntry:
        entry = self.repository.get_entry(entry_id)
        if entry is None:
            raise MigrationServiceError("LEGACY_ASSET_NOT_LEDGERED", "Legacy asset is not ledgered.")
        return entry

    @staticmethod
    def _validate_target_map(target_map: MigrationTargetMap) -> None:
        missing = [
            field_name
            for field_name in [
                "target_python_package",
                "pydantic_contract_target",
                "fixture_target",
                "eval_target",
                "reviewer_actor_id",
            ]
            if getattr(target_map, field_name) in {None, ""}
        ]
        if missing:
            raise MigrationServiceError(
                "MIGRATION_TARGET_REQUIRED",
                f"Migration target map is missing: {', '.join(missing)}.",
            )


@dataclass
class MigrationCommandHandler:
    command_type: str
    service: MigrationService
    aggregate_type: str = "migration_ledger_entry"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "ProposeLegacyAssetCommand":
            entry = self.service.propose_asset(
                source_path=payload["source_path"],
                legacy_type=payload["legacy_type"],
                registry_family=payload.get("registry_family"),
                canonicality_confidence=payload["canonicality_confidence"],
                source_owner=payload["source_owner"],
                runtime_language=payload.get("runtime_language"),
                valuable_mechanics=payload["valuable_mechanics"],
                known_defects=payload.get("known_defects", []),
                content=payload["content"],
                disposition=LegacyDisposition(payload["disposition"]),
                actor_id=envelope.actor.actor_id,
            )
            return entry.model_dump(mode="json")
        if self.command_type == "MapLegacyAssetCommand":
            entry = self.service.map_asset(
                entry_id=UUID(payload["migration_ledger_entry_id"]),
                target_map=MigrationTargetMap(**payload["target_map"]),
                actor_id=envelope.actor.actor_id,
            )
            return entry.model_dump(mode="json")
        if self.command_type == "ApproveLegacyAssetCommand":
            return self.service.approve_asset(
                entry_id=UUID(payload["migration_ledger_entry_id"]),
                reviewer_actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "BlockLegacyAssetCommand":
            return self.service.block_asset(
                entry_id=UUID(payload["migration_ledger_entry_id"]),
                reason=payload["reason"],
                replacement_target=payload.get("replacement_target"),
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "RefreshLegacyAssetHashCommand":
            flag = self.service.refresh_hash(
                entry_id=UUID(payload["migration_ledger_entry_id"]),
                content=payload["content"],
                actor_id=envelope.actor.actor_id,
            )
            return flag.model_dump(mode="json") if flag else {"decision_code": "LEGACY_HASH_UNCHANGED"}
        if self.command_type == "InspectMigrationLedgerCommand":
            return self.service.inspect_by_source_path(payload["source_path"]).model_dump(mode="json")
        raise MigrationServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("migration_ledger_entry_id")
        return UUID(raw) if raw else envelope.brand_id


def register_migration_command_handlers(bus: CommandBus, service: MigrationService) -> None:
    for command_type in [
        "ProposeLegacyAssetCommand",
        "MapLegacyAssetCommand",
        "ApproveLegacyAssetCommand",
        "BlockLegacyAssetCommand",
        "RefreshLegacyAssetHashCommand",
        "InspectMigrationLedgerCommand",
    ]:
        bus.register_handler(MigrationCommandHandler(command_type=command_type, service=service))
