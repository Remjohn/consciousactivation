from __future__ import annotations

from pathlib import Path
from typing import Any

from .application import AirApplication

_AUTHORITY = {
    "authority_id": "ca-program-control-v2.1-candidate",
    "authority_version": "2.1.0-candidate",
    "authority_sha256": "a" * 64,
    "authority_state": "candidate_not_current",
}


def _ref(object_id: str, sha256: str | None = None, version: str = "1.0.0") -> dict[str, str]:
    return {"object_id": object_id, "version": version, "sha256": sha256 or "b" * 64}


def _base(id_field: str, object_id: str, *, epistemic: bool = True) -> dict[str, Any]:
    value: dict[str, Any] = {
        id_field: object_id,
        "version": "1.0.0",
        "authority": dict(_AUTHORITY),
        "lifecycle_state": "approved",
    }
    if epistemic:
        value["epistemic_state"] = "operator_confirmed"
    return value


def run_demo(database_path: str | Path) -> dict[str, Any]:
    """Execute one deterministic, development-only AIR semantic path.

    The demonstration uses synthetic references only. It proves structure,
    persistence, ownership, and replay mechanics; it is not human evidence.
    """
    app = AirApplication(database_path)
    app.initialize()
    registry_result = app.load_registries()

    matrix_payload = {
        **_base("matrix_id", "demo:matrix"),
        "broad_signal": "The audience asks for confidence.",
        "hidden_pressure": "They avoid being seen choosing.",
        "surviving_edge": "Confidence follows a visible committed move.",
        "identity_gap": "observer to accountable chooser",
        "audience_reality": "They know the options but avoid exposure.",
        "desired_recognition": "I am protecting myself from being seen choosing.",
        "smallest_useful_movement": "Name one choice and its cost.",
        "counteractivation_risks": ["shame", "premature certainty"],
        "source_refs": [_ref("demo:source-expression")],
    }
    matrix = app.store("matrix_of_edging", matrix_payload, idempotency_key="demo-matrix")["object"]
    matrix_ref = _ref(matrix["object_id"], matrix["canonical_sha256"])

    context_payload = {
        **_base("context_id", "demo:context"),
        "identity_dna_ref": _ref("demo:identity-dna"),
        "audience_context_ref": _ref("demo:audience-context"),
        "live_premise": "The person is avoiding exposure rather than lacking information.",
        "matrix_of_edging_ref": matrix_ref,
        "evidence_refs": [_ref("demo:source-expression")],
    }
    context = app.store("activative_context", context_payload, idempotency_key="demo-context")["object"]

    role_payload = {
        **_base("contract_id", "demo:role-tension", epistemic=False),
        "activation_domain": "audience",
        "psychological_role": "accountable chooser",
        "tension": "remain protected or become visible through a choice",
        "recognition_path": "recognize avoidance as an active choice",
        "stance": "stand inside the cost of non-choice",
        "participation_threshold": "name one choice",
        "counteractivation_roles": ["judged failure"],
        "transfer_invariants": ["preserve agency", "preserve unresolved cost"],
        "evidence_refs": [_ref("demo:source-expression")],
    }
    role = app.store(
        "psychological_role_tension_contract",
        role_payload,
        idempotency_key="demo-role",
    )["object"]
    role_ref = _ref(role["object_id"], role["canonical_sha256"])

    primitives = [
        item
        for item in app.registries.query_primitives("", limit=20)
        if item.primitive_id != "EXP-TRG-001"
    ][:2]
    bindings: list[dict[str, Any]] = []
    for index, primitive in enumerate(primitives, 1):
        binding_payload = {
            **_base("binding_id", f"demo:binding:{index}"),
            "primitive_ref": primitive.immutable_ref(),
            "target_ref": _ref("demo:derivative"),
            "role_tension_ref": role_ref,
            "governed_role": "primary" if index == 1 else "support",
            "local_function": "surface the concealed choice" if index == 1 else "hold the consequence",
            "intended_effect": "viewer recognizes their current position",
            "execution_surface": "semantic production program",
            "evidence_refs": [_ref("demo:source-expression")],
            "allowed_adaptations": ["compress wording"],
            "suppression_conditions": [],
            "relation_set": [],
            "misuse_risk_refs": [],
        }
        bindings.append(
            app.store(
                "primitive_binding",
                binding_payload,
                idempotency_key=f"demo-binding-{index}",
            )["object"]
        )

    signature = {
        "signature_id": "demo:signature",
        "dominant_pressure_path": "avoidance to visible choice",
        "recognition_move": "name the protection strategy",
        "tension_release_pattern": "release only through a committed move",
        "psychological_role_transition": "observer to accountable chooser",
        "participation_threshold": "one named choice",
        "visual_attention_logic": "hold negative space around the choice",
        "experiential_progression": "recognition then commitment",
        "canonical_fingerprint": "0" * 64,
    }
    signature["canonical_fingerprint"] = app.coalitions.signature_fingerprint(signature)
    coalition_payload = {
        **_base("coalition_id", "demo:coalition", epistemic=False),
        "source_context_refs": [_ref(context["object_id"], context["canonical_sha256"])],
        "binding_refs": [_ref(item["object_id"], item["canonical_sha256"]) for item in bindings],
        "execution_order": [item["object_id"] for item in bindings],
        "compatibility_explanation": "The recognition move and consequence share one role/tension contract.",
        "conflict_resolutions": [],
        "suppressed_binding_ids": [],
        "signature": signature,
        "edge_product": {
            "edge_product_id": "demo:edge-product",
            "broad_signal_ref": _ref("demo:signal"),
            "matrix_of_edging_ref": matrix_ref,
            "hidden_pressure": matrix_payload["hidden_pressure"],
            "surviving_edge": matrix_payload["surviving_edge"],
            "stance": role_payload["stance"],
            "psychological_role": role_payload["psychological_role"],
            "tension": role_payload["tension"],
            "consequence": "non-choice remains a visible choice",
            "counteractivation_risks": ["shame"],
            "evidence_refs": [_ref("demo:source-expression")],
            "epistemic_state": "operator_confirmed",
        },
        "misuse_risk_refs": [],
        "evaluation_profile_ref": _ref("demo:primitive-evaluation-profile"),
    }
    coalition = app.store(
        "primitive_coalition_contract",
        coalition_payload,
        idempotency_key="demo-coalition",
    )["object"]

    return {
        "demo_id": "air-phase02-deterministic-semantic-demo",
        "synthetic_only": True,
        "registry_result": registry_result,
        "matrix_ref": matrix_ref,
        "context_ref": _ref(context["object_id"], context["canonical_sha256"]),
        "role_tension_ref": role_ref,
        "primitive_binding_refs": [_ref(item["object_id"], item["canonical_sha256"]) for item in bindings],
        "primitive_coalition_ref": _ref(coalition["object_id"], coalition["canonical_sha256"]),
        "health": app.repository.health(),
        "claim_ceiling": "AIR_PHASE_02_CORE_IMPLEMENTED_DEVELOPMENT_PASS",
        "real_human_evidence_claimed": False,
        "production_authorized": False,
        "certified": False,
    }
