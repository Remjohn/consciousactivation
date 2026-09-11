"""Verify CAE workspace RLS with authorized and denied identities.

All fixture creation and role/session changes are force-rolled back.
"""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlsplit

import psycopg


ENVIRONMENT_VARIABLE = "CAE_SUPABASE_DATABASE_URL"
PROJECT_REF = "evnxdssbxxrsesftdvgx"
AUTHORIZED_SUBJECT = "00000000-0000-0000-0000-000000000201"
DENIED_SUBJECT = "00000000-0000-0000-0000-000000000202"
WORKSPACE_ID = "proof:rls-workspace"
ACTOR_ID = "proof:rls-actor"


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


def count_visible_workspace(cursor: psycopg.Cursor[object], subject: str) -> int:
    cursor.execute("SET LOCAL ROLE authenticated")
    cursor.execute("SELECT set_config('request.jwt.claim.sub', %s, true)", (subject,))
    cursor.execute("SELECT count(*) FROM cae.workspace WHERE workspace_id = %s", (WORKSPACE_ID,))
    return int(cursor.fetchone()[0])


def main() -> int:
    load_local_environment()
    try:
        with psycopg.connect(connection_url(), connect_timeout=10) as connection:
            with connection.transaction(force_rollback=True):
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO cae.workspace(workspace_id, display_name) VALUES (%s, %s)",
                        (WORKSPACE_ID, "RLS proof workspace"),
                    )
                    cursor.execute(
                        "INSERT INTO cae.actor(actor_id, workspace_id, actor_kind, external_subject) VALUES (%s, %s, 'HUMAN', %s)",
                        (ACTOR_ID, WORKSPACE_ID, AUTHORIZED_SUBJECT),
                    )
                    allowed_count = count_visible_workspace(cursor, AUTHORIZED_SUBJECT)
                    cursor.execute("RESET ROLE")
                    denied_count = count_visible_workspace(cursor, DENIED_SUBJECT)
            print(f"authorized_workspace_read={'PASS' if allowed_count == 1 else 'FAIL'}")
            print(f"denied_workspace_read={'PASS' if denied_count == 0 else 'FAIL'}")
            return 0 if allowed_count == 1 and denied_count == 0 else 1
    except (OSError, psycopg.Error, RuntimeError) as error:
        print("rls_proof=FAILED")
        print(f"failure_type={type(error).__name__}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
