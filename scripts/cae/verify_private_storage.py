"""Real private-bucket upload/read/denied-read/hash proof for CAE staging.

Requires the server-only CAE_SUPABASE_SECRET_KEY in local .env. The proof
uploads a temporary object, verifies downloaded bytes by SHA-256, confirms an
unauthenticated read is denied, and deletes the proof object on completion.
"""

from __future__ import annotations

import hashlib
import os
import uuid
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


PROJECT_URL = "https://evnxdssbxxrsesftdvgx.supabase.co"
SECRET_VARIABLE = "CAE_SUPABASE_SECRET_KEY"
BUCKET = "cae-media"


def load_local_environment() -> None:
    for line in Path(".env").read_text(encoding="utf-8-sig").splitlines():
        key, separator, value = line.partition("=")
        if separator and key and not key.lstrip().startswith("#"):
            os.environ.setdefault(key.strip(), value.strip())


def request(url: str, *, method: str, headers: dict[str, str] | None = None, body: bytes | None = None) -> tuple[int, bytes]:
    with urlopen(Request(url, method=method, headers=headers or {}, data=body), timeout=20) as response:
        return int(response.status), response.read()


def main() -> int:
    load_local_environment()
    secret = os.environ.get(SECRET_VARIABLE, "")
    if not secret or secret == "***":
        print("storage_proof=NOT_CONFIGURED")
        print(f"required_environment_variable={SECRET_VARIABLE}")
        return 2
    key = f"proof/wp02a/{uuid.uuid4()}.txt"
    payload = b"CAE WP-02a private storage proof\n"
    payload_sha256 = hashlib.sha256(payload).hexdigest()
    object_url = f"{PROJECT_URL}/storage/v1/object/{BUCKET}/{key}"
    headers = {
        "apikey": secret,
        "Authorization": f"Bearer {secret}",
        "Content-Type": "text/plain",
        "x-upsert": "false",
    }
    uploaded = False
    try:
        status, _ = request(object_url, method="POST", headers=headers, body=payload)
        uploaded = status in {200, 201}
        print(f"private_upload={'PASS' if uploaded else 'FAIL'}")
        _, downloaded = request(object_url, method="GET", headers=headers)
        print(
            "private_authorized_hash_read="
            f"{'PASS' if hashlib.sha256(downloaded).hexdigest() == payload_sha256 else 'FAIL'}"
        )
        try:
            request(object_url, method="GET")
        except HTTPError as error:
            denied = error.code in {400, 401, 403}
        else:
            denied = False
        print(f"private_unauthenticated_read_denied={'PASS' if denied else 'FAIL'}")
        return 0 if uploaded and hashlib.sha256(downloaded).hexdigest() == payload_sha256 and denied else 1
    except (HTTPError, OSError):
        print("storage_proof=FAILED")
        return 1
    finally:
        if uploaded:
            try:
                request(object_url, method="DELETE", headers=headers)
                print("temporary_proof_object_deleted=PASS")
            except (HTTPError, OSError):
                print("temporary_proof_object_deleted=FAIL")


if __name__ == "__main__":
    raise SystemExit(main())
