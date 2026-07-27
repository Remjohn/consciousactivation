from __future__ import annotations

from typing import Any, Mapping

from ca_contracts import canonical_sha256, utc_now_rfc3339, validate_payload
from ca_runtime.cli import candidate_authority_ref


def semantic_actor() -> dict[str, str]:
    return {
        "actor_id": "air-phase02-deterministic-semantic-core",
        "actor_type": "deterministic_module",
        "product_id": "activative-intelligence-runtime",
        "workflow_role": "composer",
    }


def make_transition(
    *,
    object_type: str,
    object_id: str,
    revision: int,
    object_payload: Mapping[str, Any],
    idempotency_key: str,
    command_type: str = "ca.air.store_semantic_object",
    event_type: str = "ca.air.semantic_object_stored",
    now: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    timestamp = now or utc_now_rfc3339()
    authority = candidate_authority_ref()
    actor = semantic_actor()
    object_sha = canonical_sha256(object_payload)
    command_payload = {
        "object_type": object_type,
        "object_id": object_id,
        "object_revision": revision,
        "object_sha256": object_sha,
        "object": dict(object_payload),
    }
    command_payload_sha = canonical_sha256(command_payload)
    correlation_id = f"air:{object_id}"
    token = canonical_sha256(
        {
            "idempotency_key": idempotency_key,
            "object_id": object_id,
            "object_revision": revision,
            "object_sha256": object_sha,
        }
    )
    command_id = f"air:command:{token[:32]}"
    event_id = f"air:event:{token[:32]}:v{revision}"
    command = {
        "command_id": command_id,
        "command_type": command_type,
        "idempotency_key": idempotency_key,
        "actor": actor,
        "authority": authority,
        "payload_schema": f"ca.air.{object_type}",
        "payload_version": "0.2.0-dev.1",
        "payload_sha256": command_payload_sha,
        "submitted_at_utc": timestamp,
        "correlation_id": correlation_id,
    }
    event_payload = {
        "object_type": object_type,
        "object_id": object_id,
        "object_revision": revision,
        "object_sha256": object_sha,
    }
    event = {
        "event_id": event_id,
        "event_type": event_type,
        "aggregate_id": object_id,
        "aggregate_version": revision,
        "actor": actor,
        "authority": authority,
        "payload_schema": "ca.air.semantic-object-event",
        "payload_version": "0.2.0-dev.1",
        "payload_sha256": canonical_sha256(event_payload),
        "occurred_at_utc": timestamp,
        "causation_id": command_id,
        "correlation_id": correlation_id,
    }
    command_ref = {
        "object_id": command_id,
        "version": "0.2.0-dev.1",
        "sha256": canonical_sha256({"envelope": command, "payload": command_payload}),
    }
    event_ref = {
        "object_id": event_id,
        "version": "0.2.0-dev.1",
        "sha256": canonical_sha256({"envelope": event, "payload": event_payload}),
    }
    receipt_without_hash = {
        "receipt_id": f"air:receipt:{token[:32]}",
        "command_ref": command_ref,
        "outcome": "accepted",
        "result_refs": [event_ref],
        "failure": None,
        "authority": authority,
        "evaluator": None,
        "recorded_at_utc": timestamp,
    }
    receipt = {
        **receipt_without_hash,
        "receipt_sha256": canonical_sha256(receipt_without_hash),
    }
    validate_payload("command-envelope", command)
    validate_payload("event-envelope", event)
    validate_payload("receipt-envelope", receipt)
    return command, command_payload, event, event_payload, receipt
