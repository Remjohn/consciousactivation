"""Apply the guarded CAE WP-02a workspace RLS scaffolding migration."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from urllib.parse import urlsplit

import psycopg


ENVIRONMENT_VARIABLE = "CAE_SUPABASE_DATABASE_URL"
PROJECT_REF = "evnxdssbxxrsesftdvgx"
MIGRATION_VERSION = "0002_cae_workspace_rls"
MIGRATION_PATH = Path("docs/cae/implementation/sql/0002_cae_workspace_rls.sql")
MIGRATION_ACTOR = "cae-wp02a-rls-runner"


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
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    arguments = parser.parse_args()
    load_local_environment()
    sql = MIGRATION_PATH.read_text(encoding="utf-8")
    checksum = hashlib.sha256(sql.encode("utf-8")).hexdigest()
    try:
        with psycopg.connect(connection_url(), connect_timeout=10) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT checksum_sha256 FROM cae.schema_migrations WHERE version = %s",
                    (MIGRATION_VERSION,),
                )
                existing = cursor.fetchone()
            if arguments.check:
                status = "NOT_APPLIED" if existing is None else (
                    "APPLIED" if existing[0] == checksum else "CHECKSUM_MISMATCH"
                )
                print(f"migration_status={status}")
                return 0
            if existing is not None:
                print(
                    "migration_status=ALREADY_APPLIED"
                    if existing[0] == checksum
                    else "migration_status=REFUSED_CHECKSUM_MISMATCH"
                )
                return 0 if existing[0] == checksum else 2
            with connection.transaction():
                with connection.cursor() as cursor:
                    cursor.execute("SELECT pg_advisory_xact_lock(hashtext(%s))", (MIGRATION_VERSION,))
                    cursor.execute(sql)
                    cursor.execute(
                        "INSERT INTO cae.schema_migrations(version, checksum_sha256, applied_by) VALUES (%s, %s, %s)",
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
