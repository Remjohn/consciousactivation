"""Read-only, version-aware access to immutable CAE registry snapshots."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

import psycopg


class RegistryResolutionError(RuntimeError):
    """A registry ID cannot be resolved safely from the selected snapshot."""

    def __init__(self, message: str, *, canonical_id: str | None = None, snapshot_id: str | None = None, reason_code: str = "REGISTRY_RESOLUTION_ERROR"):
        super().__init__(message)
        self.canonical_id = canonical_id
        self.snapshot_id = snapshot_id
        self.reason_code = reason_code


class RegistryItemNotFoundError(RegistryResolutionError):
    """Registry item was not found in the specified snapshot."""

    def __init__(self, message: str, *, canonical_id: str | None = None, snapshot_id: str | None = None):
        super().__init__(message, canonical_id=canonical_id, snapshot_id=snapshot_id, reason_code="MISSING_RECORD")


class RegistryItemQuarantinedError(RegistryResolutionError):
    """Registry item or reference is permanently quarantined."""

    def __init__(self, message: str, *, canonical_id: str | None = None, snapshot_id: str | None = None, subtype: str = "PERMANENTLY_QUARANTINED"):
        super().__init__(message, canonical_id=canonical_id, snapshot_id=snapshot_id, reason_code=subtype)
        self.subtype = subtype


class RegistryItemAmbiguousError(RegistryResolutionError):
    """Registry item has multiple ambiguous definitions."""

    def __init__(self, message: str, *, canonical_id: str | None = None, snapshot_id: str | None = None):
        super().__init__(message, canonical_id=canonical_id, snapshot_id=snapshot_id, reason_code="AMBIGUOUS_IDENTITY")


class RegistryItemVersionlessError(RegistryResolutionError):
    """Registry item lacks explicit per-record semantic versioning."""

    def __init__(self, message: str, *, canonical_id: str | None = None, snapshot_id: str | None = None):
        super().__init__(message, canonical_id=canonical_id, snapshot_id=snapshot_id, reason_code="UNVERSIONED_RECORD")


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

    def get_item(
        self,
        *,
        registry_snapshot_id: str,
        canonical_id: str,
        require_versioned: bool = False,
    ) -> RegistryItem:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT registry_snapshot_id, source_registry, source_id,
                       source_record_version, source_path, source_hash,
                       canonical_id, record_kind, payload, migration_status
                FROM cae.registry_item
                WHERE registry_snapshot_id = %s AND canonical_id = %s
                ORDER BY registry_item_id
                """,
                (registry_snapshot_id, canonical_id),
            )
            rows = cursor.fetchall()

        if len(rows) == 0:
            raise RegistryItemNotFoundError(
                f"registry item not found: {registry_snapshot_id}/{canonical_id}",
                canonical_id=canonical_id,
                snapshot_id=registry_snapshot_id,
            )

        imported_rows = [r for r in rows if r[9] == "IMPORTED"]
        quarantined_rows = [r for r in rows if r[9] == "QUARANTINED"]

        if len(imported_rows) == 0 and len(quarantined_rows) > 0:
            raise RegistryItemQuarantinedError(
                f"registry item is permanently quarantined: {registry_snapshot_id}/{canonical_id}",
                canonical_id=canonical_id,
                snapshot_id=registry_snapshot_id,
            )

        if len(imported_rows) > 1:
            raise RegistryItemAmbiguousError(
                f"registry item is ambiguous with multiple definitions: {registry_snapshot_id}/{canonical_id}",
                canonical_id=canonical_id,
                snapshot_id=registry_snapshot_id,
            )

        if len(imported_rows) != 1:
            raise RegistryResolutionError(
                f"registry item is missing, quarantined, or ambiguous: {registry_snapshot_id}/{canonical_id}",
                canonical_id=canonical_id,
                snapshot_id=registry_snapshot_id,
            )

        row = imported_rows[0]
        raw_version = row[3]
        if require_versioned and raw_version is None:
            raise RegistryItemVersionlessError(
                f"registry item lacks explicit record version: {registry_snapshot_id}/{canonical_id}",
                canonical_id=canonical_id,
                snapshot_id=registry_snapshot_id,
            )

        # Manifest-version inheritance (Route A variant ratified by operator):
        # When a record lacks an explicit source_record_version, it inherits manifest version (1.0 per registry_manifest.yaml)
        source_version = str(raw_version) if raw_version is not None and str(raw_version).strip() else "1.0"
        item = RegistryItem(
            snapshot_id=str(row[0]),
            source_registry=str(row[1]),
            source_id=str(row[2]),
            source_record_version=source_version,
            source_path=str(row[4]),
            source_hash=str(row[5]),
            canonical_id=str(row[6]),
            record_kind=str(row[7]),
            payload=dict(row[8]),
        )

        return item

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
