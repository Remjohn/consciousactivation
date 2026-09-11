from __future__ import annotations

from typing import Any

from cmf_activative_intelligence.application import AirApplication
from cmf_activative_intelligence.demo import run_demo as run_air_core_demo

AUTHORITY = {
    "authority_id": "ca-program-control-v2.1-candidate",
    "authority_version": "2.1.0-candidate",
    "authority_sha256": "a" * 64,
    "authority_state": "candidate_not_current",
}


def _ref(object_id: str, sha256: str | None = None, version: str = "1.0.0") -> dict[str, str]:
    return {"object_id": object_id, "version": version, "sha256": sha256 or "b" * 64}


def _stored_ref(value: dict[str, Any]) -> dict[str, str]:
    obj = value["object"] if "object" in value else value
    return {
        "object_id": str(obj["object_id"]),
        "version": str(obj.get("semantic_version", obj.get("version", "1.0.0"))),
        "sha256": str(obj.get("canonical_sha256", obj.get("sha256"))),
    }


def _budget(*, consumed_candidates: int = 3, consumed_rounds: int = 1) -> dict[str, int]:
    return {
        "maximum_candidate_count": 5,
        "maximum_round_count": 3,
        "maximum_model_tokens": 0,
        "maximum_provider_cost_micros": 0,
        "consumed_candidate_count": consumed_candidates,
        "consumed_round_count": consumed_rounds,
        "consumed_model_tokens": 0,
        "consumed_provider_cost_micros": 0,
    }


_CANDIDATE_SPECS = [
    {
        "role": "self-recognizing witness",
        "tension": "keep control as proof of competence or recognize what it prevents",
        "pressure_path": "concealed protection to visible relational cost",
        "stance": "name the protective logic before offering movement",
        "smallest_commitment": "notice one moment when control prevents listening",
        "direction": "MIRROR",
        "strategy": "preserve the hesitation and belief revision before any instruction",
    },
    {
        "role": "accountable chooser",
        "tension": "retain control or choose a more exposed listening stance",
        "pressure_path": "consequence to deliberate relational choice",
        "stance": "hold the cost of control until the viewer locates themselves",
        "smallest_commitment": "name the cost of one controlling reflex",
        "direction": "TARGET",
        "strategy": "make agency explicit so listening is not mistaken for softness",
    },
    {
        "role": "protective skeptic",
        "tension": "defend agency through control or test stronger presence",
        "pressure_path": "anticipated rejection to bounded experiment",
        "stance": "surface the predictable rejection and answer it with source evidence",
        "smallest_commitment": "test listening in one bounded decision",
        "direction": "CONTRADICTION",
        "strategy": "use the guest source to distinguish listening from passivity",
    },
]


def _make_hypothesis(
    air: AirApplication,
    *,
    prefix: str,
    index: int,
    source_package_ref: dict[str, str],
    observed_ref: dict[str, str],
    moment_ref: dict[str, str],
    reaction_ref: dict[str, str],
    matrix_ref: dict[str, str],
    binding_refs: list[dict[str, str]],
    role: str,
    tension: str,
    pressure_path: str,
    stance: str,
    smallest_commitment: str,
    direction: str,
    strategy: str,
) -> dict[str, Any]:
    axes = {
        "psychological_role": role,
        "tension": tension,
        "activation_direction_set": direction,
        "pressure_path": pressure_path,
        "stance": stance,
        "counteractivation_strategy": strategy,
        "smallest_commitment": smallest_commitment,
    }
    payload = {
        "hypothesis_id": f"{prefix}:hypothesis:{index}",
        "version": "1.0.0",
        "authority": dict(AUTHORITY),
        "lifecycle_state": "proposed",
        "epistemic_state": "inferred",
        "activation_domain": "source",
        "source_kind": "interview_expression",
        "source_refs": [dict(moment_ref), dict(reaction_ref), dict(observed_ref)],
        "canonical_interview_source_package_refs": [dict(source_package_ref)],
        "identity_dna_ref": _ref(f"{prefix}:identity-dna"),
        "context_premise_ref": _ref(f"{prefix}:context-premise"),
        "matrix_of_edging_ref": dict(matrix_ref),
        "edge_product_candidate_ref": _ref(f"{prefix}:edge-product-candidate:{index}"),
        "objective_ref": _ref(f"{prefix}:objective:source-expression-batch"),
        "psychological_role": role,
        "tension": tension,
        "activation_directions": [direction],
        "pressure_path": pressure_path,
        "stance": stance,
        "stakes": ["preserve human source truth", "avoid generic advice"],
        "pressure_dose": 2,
        "participation_design": "locate the viewer inside the source tension before offering movement",
        "smallest_useful_commitment": smallest_commitment,
        "counteractivation_hypotheses": [
            {
                "risk": "the viewer hears the source as generic empathy advice",
                "trigger": "the source tension is compressed before identity pressure is visible",
                "mitigation": strategy,
                "evidence_refs": [dict(moment_ref), dict(reaction_ref)],
            }
        ],
        "inherited_wrong_reading_locks": [_ref(f"{prefix}:wrong-reading-lock:source-truth")],
        "additional_wrong_reading_locks": ["listening must not be framed as passivity"],
        "primitive_application_refs": [dict(ref) for ref in binding_refs],
        "diversity_signature": {
            "signature_id": f"{prefix}:diversity:{index}",
            "axes": axes,
            "proof_sha256": air.hypotheses.diversity_proof(axes),
            "compared_candidate_refs": [],
        },
        "proposal_binding_ref": _ref(f"{prefix}:hypothesis-binding:{index}"),
        "proposal_attempt_ref": _ref(f"{prefix}:hypothesis-attempt:{index}"),
        "interview_provenance": {
            "reaction_receipt_refs": [dict(reaction_ref)],
            "expression_moment_refs": [dict(moment_ref)],
        },
    }
    return air.hypotheses.store_hypothesis(
        payload,
        idempotency_key=f"{prefix}:hypothesis:{index}",
    )["object"]


def build_portfolio_fixture(air: AirApplication, *, prefix: str) -> dict[str, Any]:
    """Builds a fresh, OPEN, 3-candidate activation_hypothesis_portfolio
    directly against `air`, mirroring production_demo.py's
    run_production_demo hypothesis/portfolio construction (lines ~148-243)
    without also running the Interview/VAE demo. `prefix` must be unique per
    portfolio within a shared database so object ids don't collide across
    fixtures built in the same test.

    Returns a dict with: portfolio_id, hypothesis_ids (in candidate order),
    matrix_of_edging_ref, role_tension_ref, and the other refs a caller needs
    to drive POST /hypotheses/{portfolio_id}/select.
    """
    air.initialize()
    core = run_air_core_demo(air.repository.path)
    matrix_ref = dict(core["matrix_ref"])
    role_ref = dict(core["role_tension_ref"])
    binding_refs = [dict(item) for item in core["primitive_binding_refs"]]

    source_package_ref = _ref(f"{prefix}:source-package")
    observed_ref = _ref(f"{prefix}:observed-evidence-pack")
    moment_ref = _ref(f"{prefix}:expression-moment")
    reaction_ref = _ref(f"{prefix}:reaction-receipt")

    hypotheses = [
        _make_hypothesis(
            air,
            prefix=prefix,
            index=index,
            source_package_ref=source_package_ref,
            observed_ref=observed_ref,
            moment_ref=moment_ref,
            reaction_ref=reaction_ref,
            matrix_ref=matrix_ref,
            binding_refs=binding_refs,
            **spec,
        )
        for index, spec in enumerate(_CANDIDATE_SPECS, 1)
    ]
    hypothesis_refs = [_stored_ref(item) for item in hypotheses]

    portfolio_payload = {
        "portfolio_id": f"{prefix}:hypothesis-portfolio",
        "version": "1.0.0",
        "authority": dict(AUTHORITY),
        "search_policy_ref": _ref(f"{prefix}:hypothesis-search-policy"),
        "search_budget": _budget(),
        "upstream_snapshot_refs": [source_package_ref, observed_ref, matrix_ref, role_ref],
        "candidate_refs": hypothesis_refs,
        "candidate_state_records": [
            {"candidate_ref": ref, "state": "PROPOSED", "reason_codes": ["INITIAL_PORTFOLIO"]}
            for ref in hypothesis_refs
        ],
        "gate_result_refs": [],
        "comparative_evaluation_refs": [],
        "portfolio_state": "OPEN",
    }
    portfolio = air.hypotheses.store_portfolio(
        portfolio_payload,
        idempotency_key=f"{prefix}:portfolio",
    )["object"]

    return {
        "portfolio_id": portfolio["object_id"],
        "hypothesis_ids": [ref["object_id"] for ref in hypothesis_refs],
        "hypothesis_refs": hypothesis_refs,
        "matrix_of_edging_ref": matrix_ref,
        "role_tension_ref": role_ref,
        "search_budget": portfolio_payload["search_budget"],
        "gate_profile_ref": _ref(f"{prefix}:gate-profile"),
        "evaluation_profile_ref": _ref(f"{prefix}:evaluation-profile"),
        "evidence_refs": [dict(moment_ref), dict(reaction_ref)],
        "source_refs": [dict(moment_ref), dict(reaction_ref), dict(observed_ref)],
        "authority_decision_ref": _ref(f"{prefix}:authority-decision"),
    }
