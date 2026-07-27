"""Migration ledger repositories for TS-CMF-013."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.legacy import (
    HashReviewFlag,
    LegacyAssetInventoryItem,
    MigrationLedgerEntry,
    MigrationReceipt,
)


@dataclass
class InMemoryMigrationLedgerRepository:
    inventory_items: dict[UUID, LegacyAssetInventoryItem] = field(default_factory=dict)
    ledger_entries: dict[UUID, MigrationLedgerEntry] = field(default_factory=dict)
    source_path_index: dict[str, UUID] = field(default_factory=dict)
    receipts: dict[UUID, MigrationReceipt] = field(default_factory=dict)
    hash_review_flags: dict[UUID, HashReviewFlag] = field(default_factory=dict)

    def put_inventory_item(self, item: LegacyAssetInventoryItem) -> LegacyAssetInventoryItem:
        self.inventory_items[item.legacy_asset_inventory_item_id] = item
        return item

    def put_entry(self, entry: MigrationLedgerEntry) -> MigrationLedgerEntry:
        self.ledger_entries[entry.migration_ledger_entry_id] = entry
        self.source_path_index[entry.source_path] = entry.migration_ledger_entry_id
        return entry

    def get_entry(self, entry_id: UUID) -> MigrationLedgerEntry | None:
        return self.ledger_entries.get(entry_id)

    def get_by_source_path(self, source_path: str) -> MigrationLedgerEntry | None:
        entry_id = self.source_path_index.get(source_path)
        return self.ledger_entries.get(entry_id) if entry_id else None

    def put_receipt(self, receipt: MigrationReceipt) -> MigrationReceipt:
        self.receipts[receipt.migration_receipt_id] = receipt
        return receipt

    def receipts_for_entry(self, entry_id: UUID) -> list[MigrationReceipt]:
        return [
            receipt
            for receipt in self.receipts.values()
            if receipt.migration_ledger_entry_id == entry_id
        ]

    def put_hash_review_flag(self, flag: HashReviewFlag) -> HashReviewFlag:
        self.hash_review_flags[flag.hash_review_flag_id] = flag
        return flag
