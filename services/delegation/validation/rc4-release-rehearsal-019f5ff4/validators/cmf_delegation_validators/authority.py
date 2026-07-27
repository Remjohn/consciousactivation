"""Producer and forbidden-field authority enforcement."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from .paths import CONTRACTS_ROOT


class AuthorityError(ValueError):
    """Raised when a principal attempts an unauthorized contract action."""


@lru_cache(maxsize=1)
def load_authority_registry() -> dict[str, Any]:
    return json.loads((CONTRACTS_ROOT / "authority-registry.json").read_text(encoding="utf-8"))


def _entry(message_type: str) -> dict[str, Any]:
    matches = [
        item
        for item in load_authority_registry()["messages"]
        if item["message_type"] == message_type
    ]
    if len(matches) != 1:
        raise AuthorityError(f"Unknown authority policy for {message_type!r}")
    return matches[0]


def _path_exists(value: Any, pointer: str) -> bool:
    current = value
    for token in pointer.lstrip("/").split("/"):
        if token == "":
            continue
        token = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict) or token not in current:
            return False
        current = current[token]
    return True


def _template_matches(template: str, pointer: str) -> bool:
    template_tokens = template.lstrip("/").split("/") if template else []
    pointer_tokens = pointer.lstrip("/").split("/") if pointer else []
    if len(template_tokens) != len(pointer_tokens):
        return False
    return all(
        pointer_token.isdigit() if template_token == "{index}" else template_token == pointer_token
        for template_token, pointer_token in zip(template_tokens, pointer_tokens)
    )


def resolve_value_owner(message_type: str, pointer: str) -> str:
    owners = {
        owner
        for template, owner in _entry(message_type)["value_owner_by_path"].items()
        if _template_matches(template, pointer)
    }
    if len(owners) != 1:
        raise AuthorityError(
            f"Expected exactly one value owner for {message_type}{pointer}, found {sorted(owners)}"
        )
    return next(iter(owners))


def _value_paths(value: Any, pointer: str = "") -> list[str]:
    paths: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            token = key.replace("~", "~0").replace("/", "~1")
            child_pointer = f"{pointer}/{token}"
            paths.append(child_pointer)
            paths.extend(_value_paths(child, child_pointer))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_pointer = f"{pointer}/{index}"
            paths.append(child_pointer)
            paths.extend(_value_paths(child, child_pointer))
    return paths


def validate_authority(message_type: str, principal_type: str, payload: Any | None = None) -> None:
    entry = _entry(message_type)
    if principal_type not in entry["allowed_producers"]:
        raise AuthorityError(f"{principal_type} may not produce {message_type}")
    if payload is not None:
        for forbidden_path in entry["forbidden_paths"]:
            if _path_exists(payload, forbidden_path):
                raise AuthorityError(f"Forbidden authority path present: {forbidden_path}")
        for pointer in _value_paths(payload):
            owner = resolve_value_owner(message_type, pointer)
            expected_owner = principal_type if owner == "SIGNING_PRINCIPAL" else owner
            if expected_owner != principal_type:
                raise AuthorityError(
                    f"{principal_type} may not author {message_type}{pointer}; owner is {owner}"
                )
        if message_type == "delegation-envelope":
            sender_type = payload.get("sender", {}).get("principal_type")
            authority_type = payload.get("authority", {}).get("principal", {}).get("principal_type")
            signer_type = payload.get("integrity", {}).get("signer", {}).get("principal_type")
            if {sender_type, authority_type, signer_type} != {principal_type}:
                raise AuthorityError("Envelope sender, authority principal, and signer must be identical")
        if message_type == "delegation-failure":
            detecting_type = payload.get("detecting_principal", {}).get("principal_type")
            if detecting_type != principal_type:
                raise AuthorityError("Failure producer must match detecting_principal")
