from __future__ import annotations

import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen


class ProviderHttpClient:
    def post_json(
        self,
        *,
        url: str,
        payload: dict,
        headers: dict | None = None,
        timeout: int = 120,
    ) -> dict:
        body = json.dumps(payload).encode("utf-8")
        request = Request(
            url,
            data=body,
            headers={"Content-Type": "application/json", **(headers or {})},
            method="POST",
        )
        try:
            with urlopen(request, timeout=timeout) as response:
                data = response.read().decode("utf-8")
                return json.loads(data) if data else {}
        except HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {exc.code}: {raw}") from exc

    def get_json(self, *, url: str, headers: dict | None = None, timeout: int = 120) -> dict:
        request = Request(url, headers=headers or {}, method="GET")
        try:
            with urlopen(request, timeout=timeout) as response:
                data = response.read().decode("utf-8")
                return json.loads(data) if data else {}
        except HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {exc.code}: {raw}") from exc
