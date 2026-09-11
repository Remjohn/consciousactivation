"""Structural proof for the WP-02a CAE staging foundation.

All mutation attempts occur within a transaction that is explicitly rolled
back. The script reports only proof labels, never credentials or data rows.
"""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlsplit

import psycopg


ENVIRONMENT_VARIABLE = "CAE_SUPABASE_DATABASE_URL"
PROJECT_REF = "evnxdssbxxrsesftdvgx"
REQUIRED_TABLES = {
    "schema_migrations",
    "workspace",
    "project",
    "actor",
    "media_asset",
    "source_package",
    "interview_session",
    "interview_turn",
    "evidence_item",
    "evidence_span",
    "evidence_authentication",
    "semantic_assessment",
    "assessment_evidence_link",
    "semantic_operation",
    "command",
    "state_aggregate",
    "state_transition_contract",
    "state_transition",
    "event",
    "receipt",
    "legacy_import_run",
    "legacy_import_record",
}


def load_local_environment() -> None:
    for line in Path(".env").read_text(encoding="utf-8-sig").splitlines():
        key, separator, value = line.partition("=")
        if separator and key and not key.lstrip().startswith("#"):
            os.environ.setdefault(key.strip(), value.strip())


def connection_url() -> str:
    url = os.environ.get(ENVIRONMENT_VARIABLE, "")
    parsed = urlsplit(url)
    if not (
        parsed.hostname
        and parsed.hostname.endswith(".pooler.supabase.com")
        and parsed.port == 5432
        and parsed.username == f"postgres.{PROJECT_REF}"
    ):
        raise RuntimeError("connection is not the approved CAE staging session pooler")
    return url


def main() -> int:
    load_local_environment()
    try:
        with psycopg.connect(connection_url(), connect_timeout=10) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'cae' AND table_type = 'BASE TABLE'
                    """
                )
                tables = {row[0] for row in cursor.fetchall()}
                cursor.execute(
                    """
                    SELECT id, public
                    FROM storage.buckets
                    WHERE id = ANY(%s)
                    """,
                    (["cae-media", "cae-artifacts"],),
                )
                buckets = {row[0]: bool(row[1]) for row in cursor.fetchall()}

            missing_tables = sorted(REQUIRED_TABLES - tables)
            print(f"required_tables={'PASS' if not missing_tables else 'FAIL'}")
            print(
                "private_buckets="
                f"{'PASS' if buckets == {'cae-media': False, 'cae-artifacts': False} else 'FAIL'}"
            )

            with connection.transaction(force_rollback=True):
                with connection.cursor() as cursor:
                    try:
                        cursor.execute(
                            """
                            INSERT INTO cae.evidence_span(
                                evidence_span_id, evidence_id, media_asset_id, quoted_text
                            )
                            VALUES (
                                'proof:orphan-span', 'proof:missing-evidence',
                                'proof:missing-media', 'must fail'
                            )
                            """
                        )
                    except psycopg.errors.ForeignKeyViolation:
                        print("orphan_evidence_span_rejected=PASS")
                    else:
                        print("orphan_evidence_span_rejected=FAIL")
                        return 1
    except (OSError, psycopg.Error, RuntimeError) as error:
        print("foundation_structure=FAILED")
        print(f"failure_type={type(error).__name__}")
        return 1

    return 0 if not missing_tables and buckets == {"cae-media": False, "cae-artifacts": False} else 1


if __name__ == "__main__":
    raise SystemExit(main())
