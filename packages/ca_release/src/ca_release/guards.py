from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from ca_contracts import canonical_sha256


def evaluate_format02_gate(evidence_refs: Sequence[Mapping[str, Any]] = ()) -> dict[str, Any]:
    """Keep historical Format 02 evidence isolated until a new complete gate exists."""
    record = {
        "gate_id": "format02-current-harness-activation",
        "decision": "DENIED_DEFERRED",
        "required_evidence_classes": [
            "current_builder_atomic_harness_definition",
            "independent_harness_validation",
            "runtime_compatibility_receipt",
            "composition_consumer_proof",
            "operator_activation_decision",
        ],
        "supplied_evidence_refs": [dict(ref) for ref in evidence_refs],
        "historical_evidence_is_current_authority": False,
        "format02_activated": False,
        "production_authorized": False,
        "reason_codes": ["CURRENT_COMPLETE_HARNESS_NOT_PROVEN", "SEPARATE_OPERATOR_ACTIVATION_REQUIRED"],
    }
    record["gate_sha256"] = canonical_sha256(record)
    return record
