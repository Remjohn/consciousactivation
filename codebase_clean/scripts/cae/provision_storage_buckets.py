"""Provision and inspect CAE private Supabase Storage buckets.

Bucket metadata is created through the staging project's PostgreSQL storage
catalog. This is an idempotent WP-02a provisioning step; it does not upload or
alter media objects.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from urllib.parse import urlsplit

import psycopg


ENVIRONMENT_VARIABLE = "CAE_SUPABASE_DATABASE_URL"
PROJECT_REF = "evnxdssbxxrsesftdvgx"
BUCKETS = ("cae-media", "cae-artifacts")


def load_local_environment() -> None:
    for line in Path(".env").read_text(encoding="utf-8-sig").splitlines():
        key, separator, value = line.partition("=")
        if separator and key and not key.lstrip().startswith("#"):
            os.environ.setdefault(key.strip(), value.strip())


def connection_url() -> str:
    url = os.environ.get(ENVIRONMENT_VARIABLE, "")
    parsed = urlsplit(url)
    allowed = (
        parsed.hostname is not None
        and parsed.hostname.endswith(".pooler.supabase.com")
        and parsed.port == 5432
        and parsed.username == f"postgres.{PROJECT_REF}"
    )
    if not allowed:
        raise RuntimeError("connection is not the approved CAE staging session pooler")
    return url


def bucket_rows(connection: psycopg.Connection[object]) -> list[tuple[str, bool]]:
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, public FROM storage.buckets WHERE id = ANY(%s) ORDER BY id",
            (list(BUCKETS),),
        )
        return [(str(bucket_id), bool(is_public)) for bucket_id, is_public in cursor.fetchall()]


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    arguments = parser.parse_args()

    load_local_environment()
    try:
        with psycopg.connect(connection_url(), connect_timeout=10) as connection:
            if arguments.apply:
                with connection.transaction():
                    with connection.cursor() as cursor:
                        for bucket_id in BUCKETS:
                            cursor.execute(
                                """
                                INSERT INTO storage.buckets (id, name, public)
                                VALUES (%s, %s, false)
                                ON CONFLICT (id) DO UPDATE SET public = false
                                """,
                                (bucket_id, bucket_id),
                            )
            rows = bucket_rows(connection)
    except (OSError, psycopg.Error, RuntimeError) as error:
        print("bucket_status=FAILED")
        print(f"failure_type={type(error).__name__}")
        return 1

    state = {bucket_id: is_public for bucket_id, is_public in rows}
    for bucket_id in BUCKETS:
        print(f"bucket_{bucket_id}={'PRIVATE' if state.get(bucket_id) is False else 'MISSING'}")
    return 0 if all(state.get(bucket_id) is False for bucket_id in BUCKETS) else 2


if __name__ == "__main__":
    raise SystemExit(main())
