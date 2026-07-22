"""Telegram authentication service for TS-CMF-007."""

from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass
from time import time
from urllib.parse import parse_qsl


class TelegramAuthError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class TelegramAuthService:
    bot_token: str
    max_age_seconds: int = 300

    def verify_init_data(self, init_data: str, now_seconds: int | None = None) -> dict[str, str]:
        fields = dict(parse_qsl(init_data, keep_blank_values=True))
        received_hash = fields.pop("hash", None)
        if not received_hash:
            raise TelegramAuthError("TELEGRAM_AUTH_INVALID", "Missing Telegram hash.")
        auth_date = int(fields.get("auth_date", "0"))
        now = now_seconds if now_seconds is not None else int(time())
        if now - auth_date > self.max_age_seconds:
            raise TelegramAuthError("TELEGRAM_AUTH_STALE", "Telegram initData is stale.")
        data_check_string = "\n".join(f"{key}={fields[key]}" for key in sorted(fields))
        secret_key = hmac.new(
            b"WebAppData",
            self.bot_token.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        calculated = hmac.new(
            secret_key,
            data_check_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(calculated, received_hash):
            raise TelegramAuthError("TELEGRAM_AUTH_INVALID", "Telegram hash mismatch.")
        return fields
