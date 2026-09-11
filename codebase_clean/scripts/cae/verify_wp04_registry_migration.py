"""Read-only staging proof for the WP-04 registry migration."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import psycopg


ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "packages" / "ca_runtime" / "src")]

from ca_runtime.registry import RegistryResolutionError, RegistryResolver  # noqa: E402

sys.path.insert(0, str(ROOT / "scripts" / "cae"))
from import_wp04_registries import connection_url, load_local_environment, plans  # noqa: E402


def main() -> int:
    snapshots, references, issues, _ = plans()
    expected_counts = {snapshot.registry_kind: len(snapshot.items) for snapshot in snapshots}
    expected_hashes = {snapshot.snapshot_id: snapshot.source_archive_sha256 for snapshot in snapshots}
    load_local_environment()
    with psycopg.connect(connection_url(), connect_timeout=10) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT snapshot.registry_kind, count(*)
                FROM cae.registry_item item
                JOIN cae.registry_snapshot snapshot ON snapshot.registry_snapshot_id = item.registry_snapshot_id
                GROUP BY snapshot.registry_kind
                ORDER BY snapshot.registry_kind
            """)
            actual_counts = dict(cursor.fetchall())
            cursor.execute("SELECT registry_snapshot_id, source_archive_sha256 FROM cae.registry_snapshot")
            actual_hashes = dict(cursor.fetchall())
            cursor.execute("SELECT count(*) FROM cae.registry_reference WHERE validation_status = 'UNRESOLVED_INTERNAL'")
            raw_unresolved_count = int(cursor.fetchone()[0])
            cursor.execute("""
                SELECT count(*) FROM cae.registry_reference reference
                WHERE NOT EXISTS (
                  SELECT 1 FROM cae.registry_reference_disposition disposition
                  WHERE disposition.registry_reference_id = reference.registry_reference_id
                    AND disposition.disposition = 'INVALID_CLASSIFICATION'
                )
            """)
            active_reference_count = int(cursor.fetchone()[0])
            cursor.execute("""
                SELECT count(*) FROM cae.registry_reference reference
                WHERE reference.validation_status = 'UNRESOLVED_INTERNAL'
                  AND NOT EXISTS (
                    SELECT 1 FROM cae.registry_reference_disposition disposition
                    WHERE disposition.registry_reference_id = reference.registry_reference_id
                      AND disposition.disposition = 'INVALID_CLASSIFICATION'
                  )
            """)
            unresolved_count = int(cursor.fetchone()[0])
            cursor.execute("SELECT count(*) FROM cae.registry_reference_disposition WHERE disposition = 'INVALID_CLASSIFICATION'")
            invalid_classifier_reference_count = int(cursor.fetchone()[0])
            cursor.execute("SELECT count(*) FROM cae.registry_integrity_issue")
            issue_count = int(cursor.fetchone()[0])
            cursor.execute("SELECT count(*) FROM cae.registry_integrity_issue WHERE issue_code <> 'REGISTRY_REFERENCE_AMBIGUOUS'")
            active_issue_count = int(cursor.fetchone()[0])
            cursor.execute("SELECT count(*) FROM cae.registry_item WHERE lineage_preserved = false")
            lineage_failures = int(cursor.fetchone()[0])
            cursor.execute("SELECT count(*) FROM pg_class WHERE relnamespace = 'cae'::regnamespace AND relname IN ('registry_import_run','registry_snapshot','registry_item','registry_reference','registry_integrity_issue','registry_reference_disposition') AND relrowsecurity")
            rls_table_count = int(cursor.fetchone()[0])
            cursor.execute("SELECT registry_snapshot_id FROM cae.registry_snapshot WHERE registry_kind = 'SDA'")
            sda_snapshot = str(cursor.fetchone()[0])
            cursor.execute("SELECT registry_snapshot_id FROM cae.registry_snapshot WHERE registry_kind = 'SFL'")
            sfl_snapshot = str(cursor.fetchone()[0])
            cursor.execute("SELECT registry_snapshot_id FROM cae.registry_snapshot WHERE registry_kind = 'PRIMITIVE'")
            primitive_snapshot = str(cursor.fetchone()[0])
        resolver = RegistryResolver(connection)
        sda_item = resolver.get_item(registry_snapshot_id=sda_snapshot, canonical_id="SDA-INV-001")
        sfl_item = resolver.get_item(registry_snapshot_id=sfl_snapshot, canonical_id="SFL-FAM-001")
        sda_crosswalk_references = resolver.references_for(registry_snapshot_id=sda_snapshot, canonical_id="SDA-XW-PI-001")
        missing_family_rejected = False
        duplicate_primitive_rejected = False
        try:
            resolver.get_item(registry_snapshot_id=sfl_snapshot, canonical_id="SFL-FAM-005")
        except RegistryResolutionError:
            missing_family_rejected = True
        try:
            resolver.get_item(registry_snapshot_id=primitive_snapshot, canonical_id="EXP-TRG-001")
        except RegistryResolutionError:
            duplicate_primitive_rejected = True
        mutation_rejected = False
        try:
            with connection.transaction(force_rollback=True):
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE cae.registry_item SET migration_notes = 'tamper' WHERE registry_snapshot_id = %s AND canonical_id = 'SDA-INV-001'", (sda_snapshot,))
        except psycopg.Error:
            mutation_rejected = True
    checks = {
        "source_counts": actual_counts == expected_counts,
        "source_archive_hashes": actual_hashes == expected_hashes,
        "raw_reference_count": len(references) == 67 and raw_unresolved_count == 10,
        "active_reference_count": active_reference_count == len(references) == 67,
        "classifier_artifacts_dispositioned": invalid_classifier_reference_count == 486,
        "unresolved_reference_count": unresolved_count == 6,
        "raw_issue_count": issue_count == 35,
        "active_issue_count": active_issue_count == len(issues) == 31,
        "lineage_preserved": lineage_failures == 0,
        "registry_rls": rls_table_count == 6,
        "sda_resolution": sda_item.canonical_id == "SDA-INV-001",
        "sfl_resolution": sfl_item.canonical_id == "SFL-FAM-001",
        "crosswalk_resolution": len(sda_crosswalk_references) == 3 and all(reference["validation_status"] == "RESOLVED" for reference in sda_crosswalk_references),
        "missing_family_quarantined": missing_family_rejected,
        "duplicate_primitive_quarantined": duplicate_primitive_rejected,
        "immutable_mutation_rejected": mutation_rejected,
    }
    for name, result in checks.items():
        print(f"{name}={'PASS' if result else 'FAIL'}")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
