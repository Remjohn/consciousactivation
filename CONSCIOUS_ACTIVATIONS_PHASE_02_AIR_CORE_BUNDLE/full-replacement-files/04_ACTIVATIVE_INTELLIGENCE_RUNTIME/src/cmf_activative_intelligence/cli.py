from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .application import AirApplication
from .domain import (
    require_epistemic_transition,
    supported_object_types,
)
from .schema_export import export_schemas
from .demo import run_demo
from ca_runtime.cli import bootstrap_transition


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object in {path}")
    return value


def _emit(value: Any, *, compact: bool = False) -> None:
    if compact:
        print(json.dumps(value, sort_keys=True, separators=(",", ":")))
    else:
        print(json.dumps(value, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cmf-air")
    parser.add_argument("--database", type=Path)
    parser.add_argument("--compact", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    def command_parser(name: str) -> argparse.ArgumentParser:
        child = sub.add_parser(name)
        child.add_argument("--json", action="store_true", help=argparse.SUPPRESS)
        return child

    command_parser("status")
    command_parser("health")
    command_parser("init-db")
    command_parser("bootstrap")
    command_parser("load-registries")
    command_parser("registry-status")
    command_parser("supported-types")
    command_parser("demo")

    query_p = command_parser("query-primitives")
    query_p.add_argument("query")
    query_p.add_argument("--family")
    query_p.add_argument("--plane")
    query_p.add_argument("--feature")
    query_p.add_argument("--limit", type=int, default=10)

    query_a = command_parser("query-archetypes")
    query_a.add_argument("query")
    query_a.add_argument("--family")
    query_a.add_argument("--limit", type=int, default=10)

    get_o = command_parser("get-object")
    get_o.add_argument("object_id")
    get_o.add_argument("--revision", type=int)

    history = command_parser("history")
    history.add_argument("object_id")

    validate = command_parser("validate-object")
    validate.add_argument("object_type", choices=supported_object_types())
    validate.add_argument("file", type=Path)

    store = command_parser("store-object")
    store.add_argument("object_type", choices=supported_object_types())
    store.add_argument("file", type=Path)
    store.add_argument("--idempotency-key", required=True)
    store.add_argument("--expected-revision", type=int)

    schemas = command_parser("export-schemas")
    schemas.add_argument("output", type=Path)

    transition = command_parser("check-epistemic-transition")
    transition.add_argument("current")
    transition.add_argument("target")
    transition.add_argument("--evidence-ref", action="append", default=[])
    transition.add_argument("--operator-decision-ref")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    app = AirApplication(args.database)

    if args.command == "status":
        result = app.status()
    elif args.command == "health":
        result = app.repository.health()
    elif args.command == "init-db":
        result = app.initialize()
    elif args.command == "bootstrap":
        app.initialize()
        command, command_payload, event, event_payload, receipt = bootstrap_transition(
            "activative-intelligence-runtime", "0.2.0-dev.1"
        )
        result = app.repository.record_foundation_transition(
            command_envelope=command,
            command_payload=command_payload,
            event_envelope=event,
            event_payload=event_payload,
            receipt_envelope=receipt,
        )
    elif args.command == "load-registries":
        result = app.load_registries()
    elif args.command == "registry-status":
        result = app.registries.status()
    elif args.command == "supported-types":
        result = {"object_types": list(supported_object_types())}
    elif args.command == "demo":
        result = run_demo(app.repository.path)
    elif args.command == "query-primitives":
        result = {
            "results": [
                item.to_dict()
                for item in app.registries.query_primitives(
                    args.query,
                    family=args.family,
                    plane=args.plane,
                    active_feature_id=args.feature,
                    limit=args.limit,
                )
            ]
        }
    elif args.command == "query-archetypes":
        result = {
            "results": [
                item.to_dict()
                for item in app.registries.query_archetypes(
                    args.query,
                    family=args.family,
                    limit=args.limit,
                )
            ]
        }
    elif args.command == "get-object":
        result = app.repository.get_object(
            args.object_id,
            revision=args.revision,
        ).to_dict()
    elif args.command == "history":
        result = {
            "history": [
                item.to_dict() for item in app.repository.history(args.object_id)
            ]
        }
    elif args.command == "validate-object":
        result = {
            "object_type": args.object_type,
            "object": app.validate(args.object_type, _read_json(args.file)),
            "valid": True,
        }
    elif args.command == "store-object":
        result = app.store(
            args.object_type,
            _read_json(args.file),
            idempotency_key=args.idempotency_key,
            expected_revision=args.expected_revision,
        )
    elif args.command == "export-schemas":
        result = export_schemas(args.output)
    elif args.command == "check-epistemic-transition":
        evidence_refs = [
            {"object_id": value, "version": "operator-supplied", "sha256": "0" * 64}
            for value in args.evidence_ref
        ]
        operator_ref = (
            {
                "object_id": args.operator_decision_ref,
                "version": "operator-supplied",
                "sha256": "0" * 64,
            }
            if args.operator_decision_ref
            else None
        )
        require_epistemic_transition(
            args.current,
            args.target,
            evidence_refs=evidence_refs,
            operator_decision_ref=operator_ref,
        )
        result = {
            "current": args.current,
            "target": args.target,
            "allowed": True,
        }
    else:
        parser.error(f"unknown command: {args.command}")
        raise AssertionError

    _emit(result, compact=args.compact)
    return 0
