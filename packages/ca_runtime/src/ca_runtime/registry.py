"""Read-only, version-aware access to immutable CAE registry snapshots."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

import psycopg


class RegistryResolutionError(RuntimeError):
    """A registry ID cannot be resolved safely from the selected snapshot."""


@dataclass(frozen=True, slots=True)
class RegistryItem:
    snapshot_id: str
    source_registry: str
    source_id: str
    source_record_version: str | None
    source_path: str
    source_hash: str
    canonical_id: str
    record_kind: str
    payload: Mapping[str, Any]


class RegistryResolver:
    """Resolve only uniquely imported records from a named immutable snapshot.

    The caller must pin `registry_snapshot_id`; this avoids silently selecting a
    newer source version. Quarantined or ambiguous source IDs never resolve.
    """

    def __init__(self, connection: psycopg.Connection[Any]):
        self.connection = connection

    def get_item(self, *, registry_snapshot_id: str, canonical_id: str) -> RegistryItem:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT registry_snapshot_id, source_registry, source_id,
                       source_record_version, source_path, source_hash,
                       canonical_id, record_kind, payload
                FROM cae.registry_item
                WHERE registry_snapshot_id = %s AND canonical_id = %s
                  AND migration_status = 'IMPORTED'
                ORDER BY registry_item_id
                """,
                (registry_snapshot_id, canonical_id),
            )
            rows = cursor.fetchall()
        if len(rows) != 1:
            raise RegistryResolutionError(
                f"registry item is missing, quarantined, or ambiguous: {registry_snapshot_id}/{canonical_id}"
            )
        row = rows[0]
        return RegistryItem(
            snapshot_id=str(row[0]),
            source_registry=str(row[1]),
            source_id=str(row[2]),
            source_record_version=None if row[3] is None else str(row[3]),
            source_path=str(row[4]),
            source_hash=str(row[5]),
            canonical_id=str(row[6]),
            record_kind=str(row[7]),
            payload=dict(row[8]),
        )

    def references_for(self, *, registry_snapshot_id: str, canonical_id: str) -> tuple[Mapping[str, Any], ...]:
        item = self.get_item(registry_snapshot_id=registry_snapshot_id, canonical_id=canonical_id)
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT reference.relation_type, reference.target_registry_kind, reference.target_id,
                       reference.target_snapshot_id, reference.validation_status, reference.rationale, reference.detail
                FROM cae.registry_reference reference
                JOIN cae.registry_item item ON item.registry_item_id = reference.source_registry_item_id
                WHERE item.registry_snapshot_id = %s AND item.canonical_id = %s
                  AND NOT EXISTS (
                    SELECT 1 FROM cae.registry_reference_disposition disposition
                    WHERE disposition.registry_reference_id = reference.registry_reference_id
                      AND disposition.disposition = 'INVALID_CLASSIFICATION'
                  )
                ORDER BY reference.registry_reference_id
                """,
                (registry_snapshot_id, canonical_id),
            )
            return tuple(
                {
                    "relation_type": str(row[0]),
                    "target_registry_kind": None if row[1] is None else str(row[1]),
                    "target_id": str(row[2]),
                    "target_snapshot_id": None if row[3] is None else str(row[3]),
                    "validation_status": str(row[4]),
                    "rationale": None if row[5] is None else str(row[5]),
                    "detail": dict(row[6]),
                }
                for row in cursor.fetchall()
            )
