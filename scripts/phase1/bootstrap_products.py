from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from _paths import add_phase1_python_paths, repo_root

ROOT = repo_root()
add_phase1_python_paths(ROOT)

from ca_runtime.cli import bootstrap_transition  # noqa: E402
from ca_runtime.database import ProductDatabase  # noqa: E402

PRODUCTS = (
    ("activative-intelligence-runtime", "0.1.0-dev.1"),
    ("atomic-harness-pipeline", "0.1.0-dev.1"),
    ("interview-expression", "0.1.0-dev.1"),
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, default=Path(".conscious-activations/dev"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    data_root = args.data_root if args.data_root.is_absolute() else ROOT / args.data_root
    results = []
    for product_id, version in PRODUCTS:
        database = ProductDatabase(
            data_root / product_id / "product.sqlite3",
            product_id=product_id,
            product_version=version,
            authority_state="candidate_not_current",
            development_authorized=True,
            production_authorized=False,
            certified=False,
        )
        database.initialize(initialized_at_utc="2026-07-23T12:00:00Z")
        command, command_payload, event, event_payload, receipt = bootstrap_transition(
            product_id,
            version,
            now="2026-07-23T12:00:00Z",
        )
        database.record_transition(
            command_envelope=command,
            command_payload=command_payload,
            event_envelope=event,
            event_payload=event_payload,
            receipt_envelope=receipt,
        )
        # Idempotent replay must return the same receipt.
        replay = database.record_transition(
            command_envelope=command,
            command_payload=command_payload,
            event_envelope=event,
            event_payload=event_payload,
            receipt_envelope=receipt,
        )
        if replay != receipt:
            raise RuntimeError(f"idempotent replay drift for {product_id}")
        results.append(database.health().to_dict())
    output = {"result": "PASS", "products": results, "data_root": str(data_root)}
    if args.json:
        print(json.dumps(output, indent=2, sort_keys=True))
    else:
        for product in results:
            print(f"{product['product_id']}: {product['integrity']} commands={product['command_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
