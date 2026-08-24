"""Read-only CAE staging PostgreSQL connectivity probe.

The script intentionally emits no connection string, credentials, query text,
or database rows. It establishes the environment identity needed before a CAE
migration package can be applied.
"""

from __future__ import annotations

import os
import socket
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import psycopg


ENVIRONMENT_VARIABLE = "CAE_SUPABASE_DATABASE_URL"
PROJECT_REF = "evnxdssbxxrsesftdvgx"
DIRECT_HOST = f"db.{PROJECT_REF}.supabase.co"
POOLER_HOST_SUFFIX = ".pooler.supabase.com"


def load_local_environment() -> None:
    """Load missing keys from the workspace-local, gitignored .env file."""
    for line in Path(".env").read_text(encoding="utf-8-sig").splitlines():
        key, separator, value = line.partition("=")
        if separator and key and not key.lstrip().startswith("#"):
            os.environ.setdefault(key.strip(), value.strip())


def main() -> int:
    port_override: int | None = None
    if len(sys.argv) == 3 and sys.argv[1] == "--port":
        try:
            port_override = int(sys.argv[2])
        except ValueError:
            print("usage: verify_supabase_connection.py [--port 5432|6543]")
            return 2
    elif len(sys.argv) != 1:
        print("usage: verify_supabase_connection.py [--port 5432|6543]")
        return 2

    load_local_environment()
    connection_url = os.environ.get(ENVIRONMENT_VARIABLE, "")
    if not connection_url or ":***@" in connection_url:
        print("connection=NOT_CONFIGURED")
        return 2
    parsed = urlsplit(connection_url)
    raw_userinfo = parsed.netloc.rsplit("@", maxsplit=1)[0]
    raw_password = raw_userinfo.partition(":")[2]
    has_unencoded_reserved_password_character = any(
        character in raw_password for character in "@:/?#[]"
    )
    print(
        "password_url_encoding="
        f"{'NEEDS_ATTENTION' if has_unencoded_reserved_password_character else 'VALIDATED'}"
    )
    if has_unencoded_reserved_password_character:
        print("connection=FAILED")
        print("failure_class=CONNECTION_STRING_FORMAT")
        return 2
    if port_override is not None:
        raw_userinfo, separator, _host_port = parsed.netloc.rpartition("@")
        if not separator or not parsed.hostname:
            print("connection=FAILED")
            print("failure_class=CONNECTION_STRING_FORMAT")
            return 2
        connection_url = urlunsplit(
            (
                parsed.scheme,
                f"{raw_userinfo}@{parsed.hostname}:{port_override}",
                parsed.path,
                parsed.query,
                parsed.fragment,
            )
        )
        parsed = urlsplit(connection_url)
    is_direct = parsed.hostname == DIRECT_HOST and parsed.username == "postgres"
    is_session_pooler = (
        bool(parsed.hostname)
        and parsed.hostname.endswith(POOLER_HOST_SUFFIX)
        and parsed.port in {5432, 6543}
        and parsed.username == f"postgres.{PROJECT_REF}"
    )
    if not (is_direct or is_session_pooler):
        print("connection=FAILED")
        print("failure_class=CONNECTION_STRING_FORMAT")
        return 2
    endpoint_mode = "DIRECT" if is_direct else (
        "SESSION_POOLER" if parsed.port == 5432 else "TRANSACTION_POOLER"
    )
    print(f"endpoint_mode={endpoint_mode}")
    print(f"endpoint_host={parsed.hostname}")
    print(f"endpoint_port={parsed.port}")
    try:
        socket.getaddrinfo(parsed.hostname, parsed.port, type=socket.SOCK_STREAM)
    except socket.gaierror:
        print("dns_resolution=FAILED")
        return 1
    print("dns_resolution=VERIFIED")

    try:
        with psycopg.connect(connection_url, connect_timeout=10) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT current_database(), current_user, current_setting('server_version'),
                           (now() AT TIME ZONE 'UTC')
                    """
                )
                database, user, server_version, server_time = cursor.fetchone()
                cursor.execute(
                    "SELECT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'cae')"
                )
                cae_schema_exists = cursor.fetchone()[0]
    except psycopg.Error as error:
        print("connection=FAILED")
        detail = str(error).lower()
        indicators = {
            "AUTHENTICATION_REJECTED": "password authentication failed",
            "POOLER_TENANT_OR_USER": "tenant or user not found",
            "DATABASE_UNAVAILABLE": "database \"postgres\" does not exist",
            "CONNECTION_LIMIT": "too many connections",
            "TLS_NEGOTIATION": "ssl",
            "NETWORK_EGRESS_BLOCKED": "permission denied (0x0000271d/10013)",
        }
        observed = [name for name, phrase in indicators.items() if phrase in detail]
        if observed:
            print("failure_indicators=" + ",".join(observed))
        if "password authentication failed" in detail:
            print("failure_class=AUTHENTICATION_REJECTED")
        elif "permission denied (0x0000271d/10013)" in detail:
            print("failure_class=NETWORK_EGRESS_BLOCKED")
        elif any(
            phrase in detail
            for phrase in (
                "could not translate host name",
                "name or service not known",
                "no such host is known",
                "getaddrinfo failed",
            )
        ):
            print("failure_class=DNS_RESOLUTION")
        elif any(
            phrase in detail
            for phrase in (
                "network is unreachable",
                "connection timed out",
                "timeout expired",
                "no route to host",
            )
        ):
            print("failure_class=NETWORK_OR_IPV6_REACHABILITY")
        elif "connection refused" in detail:
            print("failure_class=CONNECTION_REFUSED")
        elif any(phrase in detail for phrase in ("invalid connection option", "missing '='")):
            print("failure_class=CONNECTION_STRING_FORMAT")
        elif "ssl" in detail or "tls" in detail:
            print("failure_class=TLS_NEGOTIATION")
        else:
            print("failure_class=UNCLASSIFIED_CONNECT_ERROR")
        return 1

    timestamp = datetime.fromisoformat(str(server_time)).isoformat()
    print("connection=VERIFIED")
    print(f"database={database}")
    print(f"database_user={user}")
    print(f"postgres_version={server_version}")
    print(f"server_time_utc={timestamp}")
    print(f"cae_schema_exists={str(cae_schema_exists).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
