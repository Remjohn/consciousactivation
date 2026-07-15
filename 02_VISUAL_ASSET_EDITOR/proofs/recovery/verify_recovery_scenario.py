"""non_production_readiness_proof: verify recovery/rollback event invariants only."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

CLASSIFICATION = "non_production_readiness_proof"
path = Path(__file__).with_name("RECOVERY_ROLLBACK_SCENARIO.yaml")
scenario = yaml.safe_load(path.read_text(encoding="utf-8"))
events = scenario["events"]
types = [event["type"] for event in events]
errors = []
if scenario["classification"] != CLASSIFICATION:
    errors.append("classification")
if types.index("worker_interrupted") >= types.index("checkpoint_restored"):
    errors.append("checkpoint_order")
if {event["quality_round"] for event in events} != {scenario["quality_round_at_start"]}:
    errors.append("quality_round_consumed")
if "provider_fallback_selected" not in types:
    errors.append("provider_fallback_missing")
if types.index("runtime_promotion_failed") >= types.index("rollback_applied"):
    errors.append("rollback_order")
verified = next(event for event in events if event["type"] == "accepted_asset_verified")
if verified["asset_hash"] != scenario["accepted_evidence"]["asset_hash"] or verified["receipt_hash"] != scenario["accepted_evidence"]["receipt_hash"]:
    errors.append("accepted_evidence_changed")
print(json.dumps({
    "classification": CLASSIFICATION,
    "simulation_verdict": "PASS" if not errors else "FAIL",
    "runtime_recovery_proof": "FAIL_not_executed",
    "events_verified": len(events),
    "quality_repair_rounds_consumed_by_infrastructure_retry": 0,
    "errors": errors,
}, indent=2))
raise SystemExit(0 if not errors else 1)
