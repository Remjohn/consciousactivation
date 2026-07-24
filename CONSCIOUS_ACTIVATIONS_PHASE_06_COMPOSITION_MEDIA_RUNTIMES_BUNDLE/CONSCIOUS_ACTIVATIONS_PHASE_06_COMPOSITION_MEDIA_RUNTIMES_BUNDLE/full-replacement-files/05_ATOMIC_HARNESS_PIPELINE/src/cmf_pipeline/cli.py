from __future__ import annotations

import argparse
import json
from pathlib import Path

from .application import PipelineApplication
from .demo import run_demo
from ca_runtime.cli import bootstrap_transition
from ca_runtime.database import ProductDatabase
from . import PRODUCT_ID, PRODUCT_VERSION


def _print(value: object, as_json: bool) -> None:
    if as_json:
        print(json.dumps(value, indent=2, sort_keys=True))
    elif isinstance(value, dict):
        for key, item in value.items():
            print(f"{key}: {item}")
    else:
        print(value)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="cmf-pipeline")
    parser.add_argument("--database", type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("health", "init-db", "bootstrap", "status", "load-development-candidates", "demo", "phase6-demo"):
        command = sub.add_parser(name)
        command.add_argument("--json", action="store_true")
    export = sub.add_parser("export-schemas")
    export.add_argument("destination", type=Path)
    export.add_argument("--json", action="store_true")
    replay = sub.add_parser("replay-run")
    replay.add_argument("run_id")
    replay.add_argument("--json", action="store_true")
    inspect = sub.add_parser("inspect-run")
    inspect.add_argument("run_id")
    inspect.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    app = PipelineApplication(args.database)
    if args.command == "health":
        result = app.repository.health()
    elif args.command == "init-db":
        result = app.initialize()
    elif args.command == "bootstrap":
        app.initialize()
        database = ProductDatabase(
            app.repository.path,
            product_id=PRODUCT_ID,
            product_version=PRODUCT_VERSION,
            authority_state="candidate_not_current",
            development_authorized=True,
            production_authorized=False,
            certified=False,
        )
        command, command_payload, event, event_payload, receipt = bootstrap_transition(PRODUCT_ID, PRODUCT_VERSION)
        result = database.record_transition(
            command_envelope=command,
            command_payload=command_payload,
            event_envelope=event,
            event_payload=event_payload,
            receipt_envelope=receipt,
        )
    elif args.command == "status":
        result = app.status()
    elif args.command == "load-development-candidates":
        result = {"candidates": app.load_default_development_candidates()}
    elif args.command == "demo":
        result = run_demo(args.database)
    elif args.command == "phase6-demo":
        from .phase6_demo import run_phase6_demo
        result = run_phase6_demo(args.database)
    elif args.command == "export-schemas":
        from .schema_export import export_schemas
        result = export_schemas(args.destination)
    elif args.command == "replay-run":
        result = app.runs.replay(args.run_id)
    elif args.command == "inspect-run":
        result = app.runs.status(args.run_id)
    else:
        parser.error(f"unsupported command: {args.command}")
    _print(result, getattr(args, "json", False))
    return 0
