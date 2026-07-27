"""Ed25519 verification and deterministic signing material."""

from __future__ import annotations

import base64
from copy import deepcopy
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from cmf_delegation_validators.canonical import canonical_bytes


def signature_material(envelope: dict[str, Any], payload: Any) -> bytes:
    unsigned = deepcopy(envelope)
    unsigned["integrity"].pop("signature", None)
    return canonical_bytes({"envelope": unsigned, "payload": payload})


def encode_signature(signature: bytes) -> str:
    return base64.urlsafe_b64encode(signature).decode("ascii").rstrip("=")


def decode_signature(signature: str) -> bytes:
    padding = "=" * ((4 - len(signature) % 4) % 4)
    return base64.urlsafe_b64decode(signature + padding)


class Ed25519KeyRegistry:
    def __init__(self) -> None:
        self._keys: dict[str, Ed25519PublicKey] = {}

    def register(self, key_id: str, public_key: Ed25519PublicKey) -> None:
        self._keys[key_id] = public_key

    def verify(self, envelope: dict[str, Any], payload: Any) -> bool:
        integrity = envelope.get("integrity", {})
        public_key = self._keys.get(integrity.get("key_id"))
        if public_key is None:
            return False
        try:
            public_key.verify(
                decode_signature(integrity["signature"]),
                signature_material(envelope, payload),
            )
        except (InvalidSignature, KeyError, ValueError):
            return False
        return True


def sign_envelope(
    private_key: Ed25519PrivateKey,
    envelope: dict[str, Any],
    payload: Any,
) -> dict[str, Any]:
    signed = deepcopy(envelope)
    signed["integrity"]["signature"] = encode_signature(
        private_key.sign(signature_material(signed, payload))
    )
    return signed

