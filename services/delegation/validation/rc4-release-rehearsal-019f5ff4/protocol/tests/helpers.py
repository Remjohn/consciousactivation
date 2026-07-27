from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from cmf_delegation_protocol import (
    Ed25519KeyRegistry,
    FrozenClock,
    InMemoryProtocolStore,
    ProtocolEngine,
    sign_envelope,
)
from cmf_delegation_validators.canonical import canonical_hash
from cmf_delegation_validators.contracts import registry_entry
from cmf_delegation_validators.paths import COMPATIBILITY_ROOT, CONTRACTS_ROOT, ROOT


EXAMPLES = CONTRACTS_ROOT / "examples"
NOW = datetime(2026, 7, 14, 10, 0, tzinfo=timezone.utc)
PRINCIPAL_IDS = {
    "CONTENT_HARNESS": "content-harness",
    "DELEGATION_PROTOCOL": "delegation-protocol",
    "VISUAL_ASSET_EDITOR": "visual-asset-editor",
    "CONTROL_TOWER": "control-tower",
}


def payload(message_type: str) -> dict[str, Any]:
    return json.loads((EXAMPLES / f"{message_type}.example.json").read_text(encoding="utf-8"))


def rewrite_identity(value: Any, identity: dict[str, Any], kind: str = "demand") -> Any:
    marker = "request_id" if kind == "demand" else "result_id"
    if isinstance(value, dict):
        if marker in value and {"version", "payload_hash", "canonical_ref"}.issubset(value):
            value.clear()
            value.update(deepcopy(identity))
            return value
        for child in value.values():
            rewrite_identity(child, identity, kind)
    elif isinstance(value, list):
        for child in value:
            rewrite_identity(child, identity, kind)
    return value


class Harness:
    def __init__(self) -> None:
        self.registry = Ed25519KeyRegistry()
        self.keys: dict[str, Ed25519PrivateKey] = {}
        for principal_type, principal_id in PRINCIPAL_IDS.items():
            private = Ed25519PrivateKey.generate()
            key_id = f"cmf-key://{principal_id}/test"
            self.keys[principal_type] = private
            self.registry.register(key_id, private.public_key())
        self.store = InMemoryProtocolStore()
        self.clock = FrozenClock(NOW)
        self.engine = ProtocolEngine(
            signature_verifier=self.registry, store=self.store, clock=self.clock
        )
        self.sequence = 0

    def principal(self, principal_type: str) -> dict[str, str]:
        return {
            "principal_id": PRINCIPAL_IDS[principal_type],
            "principal_type": principal_type,
            "product_version": "1.0",
        }

    def message(
        self,
        message_type: str,
        body: dict[str, Any],
        principal_type: str,
        correlation_id: str,
        *,
        message_id: str | None = None,
        nonce: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        self.sequence += 1
        sender = self.principal(principal_type)
        principal_id = sender["principal_id"]
        message_id = message_id or f"msg-{self.sequence}"
        envelope = {
            "protocol_version": "1.0",
            "message_type": message_type,
            "message_version": registry_entry(message_type)["message_version"],
            "message_id": message_id,
            "correlation_id": correlation_id,
            "causation_id": None,
            "sender": sender,
            "recipient": self.principal("DELEGATION_PROTOCOL"),
            "authority": {
                "action": f"produce_{message_type.replace('-', '_')}",
                "principal": sender,
                "field_scopes": [""],
            },
            "occurred_at": "2026-07-14T10:00:00Z",
            "idempotency_key": idempotency_key or f"idem-{self.sequence}",
            "payload_hash": canonical_hash(body),
            "payload_ref": f"cmf-contract://messages/{message_type}/{message_id}",
            "integrity": {
                "algorithm": "Ed25519",
                "key_id": f"cmf-key://{principal_id}/test",
                "signer": sender,
                "issued_at": "2026-07-14T09:59:00Z",
                "expires_at": "2026-07-14T11:00:00Z",
                "nonce": nonce or f"nonce-{self.sequence}",
            },
        }
        return sign_envelope(self.keys[principal_type], envelope, body)

    def send(
        self,
        message_type: str,
        body: dict[str, Any],
        principal_type: str,
        correlation_id: str,
        **kwargs: Any,
    ):
        envelope = self.message(
            message_type, body, principal_type, correlation_id, **kwargs
        )
        return self.engine.process(envelope, body), envelope

    def pin(self, correlation_id: str) -> dict[str, Any]:
        requester = json.loads(
            (COMPATIBILITY_ROOT / "manifest.json").read_text(
                encoding="utf-8"
            )
        )
        return self.engine.pin_compatibility(correlation_id, requester, deepcopy(requester))

    def record_demand(self, correlation_id: str):
        body = payload("visual-asset-demand")
        result, envelope = self.send(
            "visual-asset-demand", body, "CONTENT_HARNESS", correlation_id
        )
        identity = {
            "request_id": body["request_id"],
            "version": body["version"],
            "payload_hash": canonical_hash(body),
            "canonical_ref": f"cmf-contract://demands/{body['request_id']}/{body['version']}",
        }
        return result, envelope, body, identity

    def to_accepted(self, correlation_id: str):
        _, _, demand_body, demand_identity = self.record_demand(correlation_id)
        self.pin(correlation_id)
        submission = rewrite_identity(payload("visual-asset-submission"), demand_identity)
        assert self.send(
            "visual-asset-submission", submission, "CONTENT_HARNESS", correlation_id
        )[0].accepted
        validation = rewrite_identity(payload("submission-validation-receipt"), demand_identity)
        assert self.send(
            "submission-validation-receipt",
            validation,
            "DELEGATION_PROTOCOL",
            correlation_id,
        )[0].state == "SUBMITTED"
        admission = rewrite_identity(payload("admission-receipt"), demand_identity)
        assert self.send(
            "admission-receipt", admission, "VISUAL_ASSET_EDITOR", correlation_id
        )[0].state == "ACCEPTED"
        return demand_body, demand_identity, admission["execution"]

    def to_in_progress(self, correlation_id: str):
        demand_body, demand_identity, execution = self.to_accepted(correlation_id)
        event = rewrite_identity(payload("visual-asset-event"), demand_identity)
        result, _ = self.send(
            "visual-asset-event", event, "VISUAL_ASSET_EDITOR", correlation_id
        )
        assert result.state == "IN_PROGRESS"
        return demand_body, demand_identity, execution

    def to_completed(self, correlation_id: str):
        demand_body, demand_identity, execution = self.to_in_progress(correlation_id)
        contract = rewrite_identity(payload("asset-result-contract"), demand_identity)
        result, _ = self.send(
            "asset-result-contract", contract, "VISUAL_ASSET_EDITOR", correlation_id
        )
        assert result.state == "RESULT_READY"
        result_identity = {
            "result_id": contract["result_id"],
            "version": contract["version"],
            "payload_hash": canonical_hash(contract),
            "canonical_ref": f"cmf-contract://results/{contract['result_id']}/{contract['version']}",
        }
        acknowledgement = rewrite_identity(
            rewrite_identity(payload("result-acknowledgement"), demand_identity),
            result_identity,
            "result",
        )
        completed, _ = self.send(
            "result-acknowledgement",
            acknowledgement,
            "CONTENT_HARNESS",
            correlation_id,
        )
        assert completed.state == "COMPLETED"
        return demand_body, demand_identity, result_identity
