from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_sha256

from ..bindings.eligibility_registry import ImplementationEligibilityRegistry
from ..domain.validation import require_string


def register_default_synthetic_candidates(registry: ImplementationEligibilityRegistry) -> list[dict[str, Any]]:
    candidates = [
        {
            "implementation_id": "cmf-pipeline.synthetic.inspect",
            "implementation_version": "1.0.0",
            "owner_product": "ATOMIC_HARNESS_PIPELINE",
            "implementation_kind": "DETERMINISTIC_MODULE",
            "capability_ids": ["inspect_source"],
            "features": ["canonical_hash", "read_only"],
            "side_effect_class": "READ_ONLY",
            "authority_boundary": "may inspect typed refs; cannot infer semantic truth",
            "development_eligible": True,
            "production_authorized": False,
            "evidence_refs": ["phase3:synthetic-adapter"],
        },
        {
            "implementation_id": "cmf-pipeline.synthetic.compose",
            "implementation_version": "1.0.0",
            "owner_product": "ATOMIC_HARNESS_PIPELINE",
            "implementation_kind": "DETERMINISTIC_MODULE",
            "capability_ids": ["compile_program"],
            "features": ["canonical_hash", "typed_output"],
            "side_effect_class": "LOCAL_STATE_WRITE",
            "authority_boundary": "may compile typed execution program; cannot change AIR meaning",
            "development_eligible": True,
            "production_authorized": False,
            "evidence_refs": ["phase3:synthetic-adapter"],
        },
        {
            "implementation_id": "cmf-pipeline.synthetic.review",
            "implementation_version": "1.0.0",
            "owner_product": "CONSCIOUS_ACTIVATIONS_STUDIO",
            "implementation_kind": "HUMAN_GATE",
            "capability_ids": ["operator_review"],
            "features": ["attributable_decision", "typed_handoff"],
            "side_effect_class": "HUMAN_DECISION",
            "authority_boundary": "human gate may approve bounded transition only",
            "development_eligible": True,
            "production_authorized": False,
            "evidence_refs": ["phase3:synthetic-adapter"],
        },
    ]
    return [registry.register(item) for item in candidates]


class SyntheticDeterministicAdapter:
    """Produces typed synthetic evidence, never a real artifact reference."""

    def execute(self, *, node_id: str, input_refs: list[Mapping[str, Any]]) -> dict[str, Any]:
        node_id = require_string(node_id, "node_id")
        core = {
            "node_id": node_id,
            "input_ref_ids": sorted(str(item["object_id"]) for item in input_refs),
            "classification": "SYNTHETIC_DEVELOPMENT_EVIDENCE",
            "real_artifact": False,
        }
        return {
            "synthetic_result_id": f"synthetic:{canonical_sha256(core)}",
            **core,
            "payload_sha256": canonical_sha256(core),
        }
