from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from ca_contracts import canonical_sha256, utc_now_rfc3339, validate_payload

from .database import ProductDatabase
from .paths import default_database_path


def candidate_authority_ref() -> dict[str, str]:
    return {
        "authority_id": "ca-program-control-v2.1-candidate",
        "authority_version": "2.1.0-candidate",
        "authority_sha256": "cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39",
        "authority_state": "candidate_not_current",
    }


def bootstrap_transition(product_id: str, product_version: str, *, now: str | None = None) -> tuple[dict[str, Any], ...]:
    timestamp = now or utc_now_rfc3339()
    authority = candidate_authority_ref()
    actor = {
        "actor_id": f"{product_id}-phase01-bootstrap",
        "actor_type": "deterministic_module",
        "product_id": product_id,
        "workflow_role": "commander",
    }
    command_payload = {
        "product_id": product_id,
        "product_version": product_version,
        "phase": "phase_01_foundation",
        "development_authorized": True,
        "production_authorized": False,
        "certified": False,
    }
    payload_sha = canonical_sha256(command_payload)
    idempotency_key = canonical_sha256(
        {
            "command_type": "ca.phase01.initialize_product",
            "product_id": product_id,
            "payload_sha256": payload_sha,
            "authority": authority,
        }
    )
    command_id = f"{product_id}:phase01:init"
    correlation_id = f"{product_id}:phase01"
    command = {
        "command_id": command_id,
        "command_type": "ca.phase01.initialize_product",
        "idempotency_key": idempotency_key,
        "actor": actor,
        "authority": authority,
        "payload_schema": "ca.phase01.product-foundation",
        "payload_version": "0.1.0",
        "payload_sha256": payload_sha,
        "submitted_at_utc": timestamp,
        "correlation_id": correlation_id,
    }

    event_payload = {
        "product_id": product_id,
        "product_version": product_version,
        "lifecycle_state": "development_foundation_initialized",
    }
    event = {
        "event_id": f"{product_id}:phase01:initialized:v1",
        "event_type": "ca.phase01.product_foundation_initialized",
        "aggregate_id": product_id,
        "aggregate_version": 1,
        "actor": actor,
        "authority": authority,
        "payload_schema": "ca.phase01.product-foundation-initialized",
        "payload_version": "0.1.0",
        "payload_sha256": canonical_sha256(event_payload),
        "occurred_at_utc": timestamp,
        "causation_id": command_id,
        "correlation_id": correlation_id,
    }
    command_ref = {
        "object_id": command_id,
        "version": "0.1.0",
        "sha256": canonical_sha256({"envelope": command, "payload": command_payload}),
    }
    event_ref = {
        "object_id": event["event_id"],
        "version": "0.1.0",
        "sha256": canonical_sha256({"envelope": event, "payload": event_payload}),
    }
    receipt_without_hash = {
        "receipt_id": f"{product_id}:phase01:init:receipt",
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


def product_status(product_id: str, product_version: str, *, now: str | None = None) -> dict[str, Any]:
    status = {
        "product_id": product_id,
        "product_version": product_version,
        "lifecycle_state": "phase_01_development_foundation",
        "development_authorized": True,
        "production_authorized": False,
        "certified": False,
        "authority": candidate_authority_ref(),
        "updated_at_utc": now or utc_now_rfc3339(),
    }
    validate_payload("product-status-envelope", status)
    return status


def _database(args: argparse.Namespace, product_id: str, product_version: str) -> ProductDatabase:
    path = Path(args.database) if args.database else default_database_path(product_id)
    return ProductDatabase(
        path,
        product_id=product_id,
        product_version=product_version,
        authority_state="candidate_not_current",
        development_authorized=True,
        production_authorized=False,
        certified=False,
    )


def run_product_cli(product_id: str, product_version: str, argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=product_id)
    parser.add_argument("--database", help="SQLite development database path")
    sub = parser.add_subparsers(dest="command", required=True)

    health = sub.add_parser("health")
    health.add_argument("--json", action="store_true")

    init_db = sub.add_parser("init-db")
    init_db.add_argument("--json", action="store_true")

    bootstrap = sub.add_parser("bootstrap")
    bootstrap.add_argument("--json", action="store_true")

    status = sub.add_parser("status")
    status.add_argument("--json", action="store_true")

    args = parser.parse_args(argv)
    database = _database(args, product_id, product_version)

    if args.command == "health":
        result = database.health().to_dict()
    elif args.command == "init-db":
        result = database.initialize().to_dict()
    elif args.command == "bootstrap":
        database.initialize()
        command, command_payload, event, event_payload, receipt = bootstrap_transition(product_id, product_version)
        result = database.record_transition(
            command_envelope=command,
            command_payload=command_payload,
            event_envelope=event,
            event_payload=event_payload,
            receipt_envelope=receipt,
        )
    elif args.command == "status":
        result = product_status(product_id, product_version)
    else:
        parser.error(f"unsupported command: {args.command}")

    if getattr(args, "json", False):
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for key, value in result.items():
            print(f"{key}: {value}")
    return 0
