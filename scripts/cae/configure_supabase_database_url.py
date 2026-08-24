"""Safely encode the local CAE Supabase database password for a URL.

Run this only in your trusted local terminal. Password input is hidden and the
script never prints the password, encoded value, or complete connection URL.
"""

from __future__ import annotations

from getpass import getpass
from pathlib import Path
from urllib.parse import quote, urlsplit


ENV_PATH = Path(".env")
ENVIRONMENT_VARIABLE = "CAE_SUPABASE_DATABASE_URL"


def main() -> int:
    lines = ENV_PATH.read_text(encoding="utf-8-sig").splitlines()
    index = next(
        (
            position
            for position, line in enumerate(lines)
            if line.startswith(f"{ENVIRONMENT_VARIABLE}=")
        ),
        None,
    )
    if index is None:
        print(f"{ENVIRONMENT_VARIABLE} is missing from .env")
        return 2

    current_url = lines[index].partition("=")[2]
    parsed = urlsplit(current_url)
    if not parsed.scheme.startswith("postgres") or not parsed.hostname:
        print("The existing CAE_SUPABASE_DATABASE_URL is not a PostgreSQL URL.")
        return 2

    raw_userinfo = parsed.netloc.rsplit("@", maxsplit=1)[0]
    username = raw_userinfo.partition(":")[0]
    if not username:
        print("The existing CAE_SUPABASE_DATABASE_URL has no database user.")
        return 2

    password = getpass("Supabase database password (hidden): ")
    if not password:
        print("No password entered; .env was not changed.")
        return 2

    host_port = parsed.netloc.rsplit("@", maxsplit=1)[1]
    encoded_password = quote(password, safe="")
    query = f"?{parsed.query}" if parsed.query else ""
    fragment = f"#{parsed.fragment}" if parsed.fragment else ""
    lines[index] = (
        f"{ENVIRONMENT_VARIABLE}={parsed.scheme}://{username}:"
        f"{encoded_password}@{host_port}{parsed.path}{query}{fragment}"
    )
    ENV_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("CAE_SUPABASE_DATABASE_URL updated with URL-encoded password.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
