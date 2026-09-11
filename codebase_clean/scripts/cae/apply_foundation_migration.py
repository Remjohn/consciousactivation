"""Apply or inspect the guarded WP-02a CAE foundation migration.

This runner is deliberately restricted to the approved staging project and
records the DDL checksum in the CAE migration ledger. It never displays a
connection URL, password, or table contents.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path
from urllib.parse import urlsplit

import psycopg


ENVIRONMENT_VARIABLE = "CAE_SUPABASE_DATABASE_URL"
PROJECT_REF = "evnxdssbxxrsesftdvgx"
MIGRATION_VERSION = "0001_cae_foundation"
MIGRATION_PATH = Path("docs/cae/implementation/sql/0001_cae_foundation_draft.sql")
MIGRATION_ACTOR = "cae-wp02a-foundation-runner"


def load_local_environment() -> None:
    for line in Path(".env").read_text(encoding="utf-8-sig").splitlines():
        key, separator, value = line.partition("=")
        if separator and key and not key.lstrip().startswith("#"):
            os.environ.setdefault(key.strip(), value.strip())


def connection_url() -> str:
    url = os.environ.get(ENVIRONMENT_VARIABLE, "")
    if not url or ":***@" in url:
        raise RuntimeError(f"{ENVIRONMENT_VARIABLE} is not configured")
    parsed = urlsplit(url)
    valid_session_pooler = (
        parsed.hostname is not None
        and parsed.hostname.endswith(".pooler.supabase.com")
        and parsed.port == 5432
        and parsed.username == f"postgres.{PROJECT_REF}"
    )
    valid_direct = (
        parsed.hostname == f"db.{PROJECT_REF}.supabase.co"
        and parsed.port == 5432
        and parsed.username == "postgres"
    )
    if not (valid_session_pooler or valid_direct):
        raise RuntimeError("connection is not the approved CAE staging project")
    return url


def migration_sql_and_checksum() -> tuple[str, str]:
    sql = MIGRATION_PATH.read_text(encoding="utf-8")
    return sql, hashlib.sha256(sql.encode("utf-8")).hexdigest()


def read_status(connection: psycopg.Connection[object], checksum: str) -> str:
    with connection.cursor() as cursor:
        cursor.execute("SELECT to_regclass('cae.schema_migrations')")
        if cursor.fetchone()[0] is None:
            return "NOT_APPLIED"
        cursor.execute(
            "SELECT checksum_sha256 FROM cae.schema_migrations WHERE version = %s",
            (MIGRATION_VERSION,),
        )
        row = cursor.fetchone()
    if row is None:
        return "SCHEMA_EXISTS_MIGRATION_NOT_RECORDED"
    if row[0] != checksum:
        return "CHECKSUM_MISMATCH"
    return "APPLIED"


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    arguments = parser.parse_args()

    load_local_environment()
    sql, checksum = migration_sql_and_checksum()
    try:
        with psycopg.connect(connection_url(), connect_timeout=10) as connection:
            if arguments.check:
                print(f"migration_status={read_status(connection, checksum)}")
                return 0

            with connection.transaction():
                with connection.cursor() as cursor:
                    cursor.execute("SELECT pg_advisory_xact_lock(hashtext(%s))", (MIGRATION_VERSION,))
                status = read_status(connection, checksum)
                if status == "APPLIED":
                    print("migration_status=ALREADY_APPLIED")
                    return 0
                if status != "NOT_APPLIED":
                    print(f"migration_status=REFUSED_{status}")
                    return 2
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    cursor.execute(
                        """
                        INSERT INTO cae.schema_migrations(version, checksum_sha256, applied_by)
                        VALUES (%s, %s, %s)
                        """,
                        (MIGRATION_VERSION, checksum, MIGRATION_ACTOR),
                    )
            print("migration_status=APPLIED")
            print(f"migration_checksum_sha256={checksum}")
            return 0
    except (OSError, psycopg.Error, RuntimeError) as error:
        print("migration_status=FAILED")
        print(f"failure_type={type(error).__name__}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
