"""Read-only precondition check before the WP-03 evidence-contract amendment."""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlsplit

import psycopg


ENVIRONMENT_VARIABLE = "CAE_SUPABASE_DATABASE_URL"
PROJECT_REF = "evnxdssbxxrsesftdvgx"


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
                    SELECT
                      (SELECT count(*) FROM cae.command),
                      (SELECT count(*) FROM cae.event),
                      (SELECT count(*) FROM cae.receipt),
                      EXISTS (
                        SELECT 1 FROM pg_extension WHERE extname = 'pgcrypto'
                      )
                    """
                )
                command_count, event_count, receipt_count, pgcrypto_available = cursor.fetchone()
    except (OSError, psycopg.Error, RuntimeError) as error:
        print("wp03_preconditions=FAILED")
        print(f"failure_type={type(error).__name__}")
        return 1
    print(f"command_count={command_count}")
    print(f"event_count={event_count}")
    print(f"receipt_count={receipt_count}")
    print(f"pgcrypto_available={str(bool(pgcrypto_available)).lower()}")
    empty = command_count == event_count == receipt_count == 0
    print(f"evidence_tables_empty={'PASS' if empty else 'FAIL'}")
    return 0 if empty and pgcrypto_available else 1


if __name__ == "__main__":
    raise SystemExit(main())
