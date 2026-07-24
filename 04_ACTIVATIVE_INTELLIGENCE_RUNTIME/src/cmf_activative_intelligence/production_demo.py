from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from ca_contracts import canonical_sha256
from conscious_activations_interview_expression.demo import run_demo as run_interview_demo

from .application import AirApplication
from .demo import run_demo as run_air_core_demo
from .production_domain import EVALUATION_DIMENSIONS, HYPOTHESIS_GATES

_AUTHORITY = {
    "authority_id": "ca-program-control-v2.1-candidate",
    "authority_version": "2.1.0-candidate",
    "authority_sha256": "a" * 64,
    "authority_state": "candidate_not_current",
}


def _ref(object_id: str, sha256: str | None = None, version: str = "1.0.0") -> dict[str, str]:
    return {"object_id": object_id, "version": version, "sha256": sha256 or "b" * 64}


def _stored_ref(value: Mapping[str, Any]) -> dict[str, str]:
    obj = value["object"] if "object" in value else value
    return {
        "object_id": str(obj["object_id"]),
        "version": str(obj.get("semantic_version", obj.get("version", "1.0.0"))),
        "sha256": str(obj.get("canonical_sha256", obj.get("sha256"))),
    }


def _base(
    id_field: str,
    object_id: str,
    *,
    lifecycle: str | None = "validated",
    epistemic: str | None = "inferred",
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        id_field: object_id,
        "version": "1.0.0",
        "authority": dict(_AUTHORITY),
    }
    if lifecycle is not None:
        payload["lifecycle_state"] = lifecycle
    if epistemic is not None:
        payload["epistemic_state"] = epistemic
    return payload


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


def _make_hypothesis(
    app: AirApplication,
    *,
    index: int,
    source_package_ref: Mapping[str, Any],
    observed_ref: Mapping[str, Any],
    moment_ref: Mapping[str, Any],
    reaction_ref: Mapping[str, Any],
    matrix_ref: Mapping[str, Any],
    binding_refs: list[Mapping[str, Any]],
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
        **_base(
            "hypothesis_id",
            f"demo:hypothesis:{index}",
            lifecycle="proposed",
            epistemic="inferred",
        ),
        "activation_domain": "source",
        "source_kind": "interview_expression",
        "source_refs": [dict(moment_ref), dict(reaction_ref), dict(observed_ref)],
        "canonical_interview_source_package_refs": [dict(source_package_ref)],
        "identity_dna_ref": _ref("demo:identity-dna"),
        "context_premise_ref": _ref("demo:context-premise"),
        "matrix_of_edging_ref": dict(matrix_ref),
        "edge_product_candidate_ref": _ref(f"demo:edge-product-candidate:{index}"),
        "objective_ref": _ref("demo:objective:source-expression-batch"),
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
        "inherited_wrong_reading_locks": [_ref("demo:wrong-reading-lock:source-truth")],
        "additional_wrong_reading_locks": ["listening must not be framed as passivity"],
        "primitive_application_refs": [dict(ref) for ref in binding_refs],
        "diversity_signature": {
            "signature_id": f"demo:diversity:{index}",
            "axes": axes,
            "proof_sha256": app.hypotheses.diversity_proof(axes),
            "compared_candidate_refs": [],
        },
        "proposal_binding_ref": _ref(f"demo:hypothesis-binding:{index}"),
        "proposal_attempt_ref": _ref(f"demo:hypothesis-attempt:{index}"),
        "interview_provenance": {
            "reaction_receipt_refs": [dict(reaction_ref)],
            "expression_moment_refs": [dict(moment_ref)],
        },
    }
    return app.hypotheses.store_hypothesis(
        payload,
        idempotency_key=f"phase5-demo:hypothesis:{index}",
    )["object"]


def run_production_demo(
    database_path: str | Path,
    interview_database_path: str | Path,
) -> dict[str, Any]:
    """Run one deterministic, source-backed semantic-production compiler path.

    All media and human inputs are development fixtures. The demonstration proves
    contract enforcement, semantic ownership, lineage, approvals, and persistence;
    it does not prove real human activation or production readiness.
    """

    interview = run_interview_demo(interview_database_path)
    core = run_air_core_demo(database_path)
    app = AirApplication(database_path)
    app.initialize()
    app.load_registries()

    source_package_ref = {
        "object_id": str(interview["source_package"]["object_id"]),
        "version": str(interview["source_package"]["version"]),
        "sha256": str(interview["source_package"]["sha256"]),
    }
    observed_ref = dict(interview["observed_evidence_pack_ref"])
    moment_ref = dict(interview["expression_moment_ref"])
    reaction_ref = dict(interview["reaction_receipt_ref"])
    visual_index_ref = dict(interview["visual_index_ref"])
    matrix_ref = dict(core["matrix_ref"])
    context_ref = dict(core["context_ref"])
    role_ref = dict(core["role_tension_ref"])
    coalition_ref = dict(core["primitive_coalition_ref"])
    binding_refs = [dict(item) for item in core["primitive_binding_refs"]]

    candidate_specs = [
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
    hypotheses = [
        _make_hypothesis(
            app,
            index=index,
            source_package_ref=source_package_ref,
            observed_ref=observed_ref,
            moment_ref=moment_ref,
            reaction_ref=reaction_ref,
            matrix_ref=matrix_ref,
            binding_refs=binding_refs,
            **spec,
        )
        for index, spec in enumerate(candidate_specs, 1)
    ]
    hypothesis_refs = [_stored_ref(item) for item in hypotheses]

    portfolio_payload = {
        **_base("portfolio_id", "demo:hypothesis-portfolio", lifecycle=None, epistemic=None),
        "search_policy_ref": _ref("demo:hypothesis-search-policy"),
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
    portfolio = app.hypotheses.store_portfolio(
        portfolio_payload,
        idempotency_key="phase5-demo:portfolio",
    )["object"]
    portfolio_ref = _stored_ref(portfolio)

    gate_refs: list[dict[str, str]] = []
    for index, hypothesis_ref in enumerate(hypothesis_refs, 1):
        gate = app.hypotheses.gate_hypothesis(
            receipt_id=f"demo:hypothesis-gate:{index}",
            version="1.0.0",
            authority=_AUTHORITY,
            portfolio_ref=portfolio_ref,
            hypothesis_ref=hypothesis_ref,
            gate_profile_ref=_ref("demo:hypothesis-gate-profile"),
            evaluator_actor_id="demo:independent-hypothesis-gate-evaluator",
            producer_actor_id=f"demo:hypothesis-producer:{index}",
            outcomes={gate_name: True for gate_name in HYPOTHESIS_GATES},
            evidence_refs=[moment_ref, matrix_ref],
            idempotency_key=f"phase5-demo:gate:{index}",
        )["object"]
        gate_refs.append(_stored_ref(gate))

    score_bases = [930_000, 720_000, 670_000]
    candidate_scores = {
        ref["object_id"]: {
            dimension: score_bases[index] - offset * 4_000
            for offset, dimension in enumerate(EVALUATION_DIMENSIONS)
        }
        for index, ref in enumerate(hypothesis_refs)
    }
    comparison = app.hypotheses.compare_portfolio(
        receipt_id="demo:hypothesis-comparison",
        version="1.0.0",
        authority=_AUTHORITY,
        portfolio_ref=portfolio_ref,
        evaluation_profile_ref=_ref("demo:hypothesis-evaluation-profile"),
        evaluator_actor_id="demo:independent-hypothesis-comparator",
        producer_actor_ids=[f"demo:hypothesis-producer:{i}" for i in range(1, 4)],
        gate_receipt_refs=gate_refs,
        candidate_scores=candidate_scores,
        decisive_margin_micros=100_000,
        idempotency_key="phase5-demo:comparison",
    )["object"]
    comparison_ref = _stored_ref(comparison)
    selected_ref = dict(comparison["payload"]["selected_hypothesis_ref"])

    stopping = app.hypotheses.stop_search(
        receipt_id="demo:hypothesis-stop",
        version="1.0.0",
        authority=_AUTHORITY,
        portfolio_ref=portfolio_ref,
        evaluation_ref=comparison_ref,
        remaining_budget=_budget(),
        diversity_exhausted=False,
        idempotency_key="phase5-demo:stop",
    )["object"]
    stopping_ref = _stored_ref(stopping)

    planned_pack_payload = {
        **_base(
            "pack_id",
            "demo:planned-activative-pack",
            lifecycle="approved",
            epistemic="planned",
        ),
        "portfolio_ref": portfolio_ref,
        "selected_hypothesis_ref": selected_ref,
        "matrix_of_edging_ref": matrix_ref,
        "role_tension_ref": role_ref,
        "source_refs": [source_package_ref, moment_ref, reaction_ref],
        "limitations": ["development fixture; no real-human activation claim"],
    }
    planned_pack = app.hypotheses.store_planned_pack(
        planned_pack_payload,
        idempotency_key="phase5-demo:planned-pack",
    )["object"]
    planned_pack_ref = _stored_ref(planned_pack)

    promotion_payload = {
        **_base("receipt_id", "demo:hypothesis-promotion", lifecycle=None, epistemic=None),
        "portfolio_ref": portfolio_ref,
        "selected_hypothesis_ref": selected_ref,
        "stopping_receipt_ref": stopping_ref,
        "planned_pack_ref": planned_pack_ref,
        "authority_decision_ref": _ref("demo:operator-hypothesis-selection"),
    }
    promotion = app.hypotheses.promote(
        promotion_payload,
        idempotency_key="phase5-demo:promotion",
    )["object"]
    promotion_ref = _stored_ref(promotion)

    promoted_portfolio_payload = {
        **portfolio_payload,
        "supersedes_ref": portfolio_ref,
        "gate_result_refs": gate_refs,
        "comparative_evaluation_refs": [comparison_ref],
        "portfolio_state": "PROMOTED",
        "stopping_receipt_ref": stopping_ref,
        "selected_hypothesis_ref": selected_ref,
        "promotion_ref": promotion_ref,
        "candidate_state_records": [
            {
                "candidate_ref": ref,
                "state": "PROMOTED" if ref == selected_ref else "ELIGIBLE",
                "reason_codes": ["SELECTED_BY_DECISIVE_COMPARISON" if ref == selected_ref else "NOT_SELECTED"],
                "caused_by_receipt_ref": promotion_ref if ref == selected_ref else comparison_ref,
            }
            for ref in hypothesis_refs
        ],
    }
    promoted_portfolio = app.hypotheses.store_portfolio(
        promoted_portfolio_payload,
        idempotency_key="phase5-demo:portfolio-promoted",
        expected_revision=1,
    )["object"]

    archetype = app.registries.query_archetypes("", limit=1)[0]
    archetype_payload = {
        **_base("program_id", "demo:archetype-coalition", lifecycle="approved", epistemic=None),
        "role_tension_contract_ref": role_ref,
        "primitive_coalition_ref": coalition_ref,
        "primary_archetype": {
            "binding_id": "demo:archetype-binding:primary",
            "archetype_ref": archetype.immutable_ref(),
            "current_validation_ref": _ref("demo:archetype-current-validation"),
            "local_function": "let source expression become recognition before instruction",
            "source_fit": "the guest names a lived belief revision",
            "category_geometry": "source-led short with reusable visual explanation",
            "primitive_binding_ids": [ref["object_id"] for ref in binding_refs],
            "rejection_conditions": ["generic quote card", "advice without source tension"],
        },
        "supporting_archetypes": [],
        "source_expression_refs": [moment_ref, reaction_ref],
        "category_target": "source_led_short",
        "sequence_or_reading_logic": "source expression then viewer recognition then bounded movement",
        "anti_centroid_locks": ["do not flatten the guest into generic listening advice"],
        "wrong_reading_locks": ["listening is not passivity"],
        "rejected_alternatives": ["motivational quote montage"],
    }
    archetype_program = app.store(
        "archetype_coalition_program",
        archetype_payload,
        idempotency_key="phase5-demo:archetype-coalition",
    )["object"]
    archetype_ref = _stored_ref(archetype_program)

    brand_payload = {
        **_base("brand_context_id", "demo:brand-context", lifecycle="approved", epistemic="operator_confirmed"),
        "brand_genesis_session_ref": _ref("demo:brand-genesis"),
        "identity_truths": ["human truth before content performance"],
        "audience_relationship": "credible challenger who protects agency",
        "positioning_tension": "real expression versus generic inspiration",
        "source_refs": [moment_ref],
    }
    brand = app.store("brand_context_version", brand_payload, idempotency_key="phase5-demo:brand")["object"]
    brand_ref = _stored_ref(brand)

    voice_payload = {
        **_base("voice_dna_id", "demo:voice-dna", lifecycle="approved", epistemic="operator_confirmed"),
        "brand_context_ref": brand_ref,
        "vocabulary_patterns": ["concrete pressure language"],
        "rhythm_patterns": ["short recognition then consequence"],
        "sentence_pressure_patterns": ["name the concealed tradeoff"],
        "stance_patterns": ["direct without theatrical certainty"],
        "specificity_patterns": ["keep exact source behavior visible"],
        "metaphor_range": ["bounded lived metaphor"],
        "emotional_distance": "close and source-grounded",
        "prohibited_centroid_patterns": ["generic inspiration", "empty empathy"],
        "source_evidence_refs": [moment_ref, reaction_ref],
    }
    voice = app.store("voice_dna", voice_payload, idempotency_key="phase5-demo:voice")["object"]
    voice_ref = _stored_ref(voice)

    visual_payload = {
        **_base("visual_dna_id", "demo:visual-dna", lifecycle="approved", epistemic="operator_confirmed"),
        "brand_context_ref": brand_ref,
        "real_life_reference_refs": [visual_index_ref],
        "subject_treatment": ["guest remains the identity anchor"],
        "visual_temperature": ["restrained unresolved tension"],
        "materiality": ["documentary source texture"],
        "composition_tendencies": ["asymmetric source-first hierarchy"],
        "negative_space_functions": ["hold the gap between control and listening"],
        "edge_behaviors": ["protect source contradiction"],
        "typographic_posture": ["quiet exact claims"],
        "motion_character": ["bounded explanatory movement"],
        "prohibited_centroid_defaults": ["centered generic quote card"],
    }
    visual = app.store("visual_dna", visual_payload, idempotency_key="phase5-demo:visual")["object"]
    visual_ref = _stored_ref(visual)

    wrong_lock_ref = _ref("demo:wrong-reading-lock:listening-not-passivity")
    input_manifest_payload = {
        **_base("manifest_id", "demo:derivative-input-manifest", lifecycle="approved", epistemic="operator_confirmed"),
        "source_kind": "interview_expression",
        "source_package_refs": [source_package_ref],
        "expression_moment_refs": [moment_ref],
        "reaction_receipt_refs": [reaction_ref],
        "observed_activative_pack_ref": observed_ref,
        "selected_hypothesis_ref": selected_ref,
        "matrix_of_edging_ref": matrix_ref,
        "role_tension_ref": role_ref,
        "primitive_coalition_ref": coalition_ref,
        "archetype_coalition_ref": archetype_ref,
        "brand_context_ref": brand_ref,
        "voice_dna_ref": voice_ref,
        "visual_dna_ref": visual_ref,
        "objective_ref": _ref("demo:objective:source-expression-batch"),
        "campaign_role": "source expression anchor",
        "category_id": "short_form_edited_video",
        "profile_id": "format07_direct_coaching_a_roll",
        "format_harness_ref": _ref("demo:harness:format07"),
        "wrong_reading_lock_refs": [wrong_lock_ref],
        "limitations": ["development fixture"],
    }
    input_manifest = app.derivatives.store_input_manifest(
        input_manifest_payload,
        idempotency_key="phase5-demo:input-manifest",
    )["object"]
    input_manifest_ref = _stored_ref(input_manifest)

    derivative_types = {
        "source_short": ("SOURCE_LED_SHORT", "format07_direct_coaching_a_roll"),
        "carousel": ("CAROUSEL", "carousel_source_expression_sequence"),
        "supervisual": ("SUPERVISUAL", "supervisual_source_argument"),
        "animation": ("ANIMATION_SCENE_PACKAGE", "animation_scene_package_non_character_performance"),
    }
    program_refs: dict[str, dict[str, str]] = {}
    for key, (dtype, profile) in derivative_types.items():
        payload = {
            **_base("program_id", f"demo:derivative-program:{key}", lifecycle="approved", epistemic="operator_confirmed"),
            "input_manifest_ref": input_manifest_ref,
            "derivative_type": dtype,
            "category_id": "short_form_edited_video" if key == "source_short" else "static_or_animation_derivative",
            "profile_id": profile,
            "source_ingredient_refs": [moment_ref, reaction_ref, source_package_ref],
            "role_tension_ref": role_ref,
            "matrix_of_edging_ref": matrix_ref,
            "primitive_coalition_ref": coalition_ref,
            "archetype_coalition_ref": archetype_ref,
            "brand_context_ref": brand_ref,
            "voice_dna_ref": voice_ref,
            "visual_dna_ref": visual_ref,
            "allowed_transformation_classes": ["VERBATIM", "CONDENSATION", "BRIDGE", "VOICE_DNA_REWRITE"],
            "maximum_claim": "SOURCE_GROUNDED_DERIVATIVE_DEVELOPMENT_EVIDENCE",
            "wrong_reading_lock_refs": [wrong_lock_ref],
            "evaluation_profile_ref": _ref(f"demo:evaluation-profile:{key}"),
            "allowed_tools": ["source-lineage-reader", "guest-voice-writer", "primitive-coalition-composer"],
            "denied_tools": ["format02-runtime", "unbounded-autonomous-publisher"],
            "composition_authorized": False,
            "limitations": ["composition waits for exact operator-approved Final Script"],
        }
        stored = app.derivatives.store_program(payload, idempotency_key=f"phase5-demo:program:{key}")["object"]
        program_refs[key] = _stored_ref(stored)

    primary_program_ref = program_refs["source_short"]
    context_sha = canonical_sha256(
        {
            "program_ref": primary_program_ref,
            "voice_dna_ref": voice_ref,
            "primitive_coalition_ref": coalition_ref,
            "archetype_coalition_ref": archetype_ref,
            "source_refs": [moment_ref, reaction_ref],
        }
    )
    jit_payload = {
        **_base("request_id", "demo:jit-authoring-request", lifecycle=None, epistemic=None),
        "program_ref": primary_program_ref,
        "authoring_role": "WRITER",
        "approved_ingredient_refs": [moment_ref, reaction_ref, source_package_ref],
        "voice_dna_ref": voice_ref,
        "primitive_coalition_ref": coalition_ref,
        "archetype_coalition_ref": archetype_ref,
        "category_id": "short_form_edited_video",
        "profile_id": "format07_direct_coaching_a_roll",
        "allowed_transformation_classes": ["VERBATIM", "CONDENSATION", "BRIDGE", "VOICE_DNA_REWRITE"],
        "maximum_claim": "SOURCE_GROUNDED_DERIVATIVE_DEVELOPMENT_EVIDENCE",
        "wrong_reading_lock_refs": [wrong_lock_ref],
        "allowed_tools": ["source-lineage-reader", "guest-voice-writer"],
        "denied_tools": ["fabricate-source-quote"],
        "context_sha256": context_sha,
    }
    jit = app.derivatives.store_jit_request(jit_payload, idempotency_key="phase5-demo:jit")["object"]
    jit_ref = _stored_ref(jit)

    source_span_ref = _ref("demo:source-span:1500-3500", source_package_ref["sha256"])
    segments = [
        {
            "segment_id": "demo:segment:0",
            "order": 0,
            "final_text": "I thought success meant control.",
            "transformation_class": "VERBATIM",
            "source_text": "I thought success meant control.",
            "source_span_refs": [source_span_ref],
            "transformation_operations": [],
            "voice_dna_applied": False,
            "claim_state": "DIRECT_QUOTE",
            "epistemic_state": "observed",
            "sequence_role": "source confession",
        },
        {
            "segment_id": "demo:segment:1",
            "order": 1,
            "final_text": "Then I learned that control was keeping me from listening.",
            "transformation_class": "VOICE_DNA_REWRITE",
            "source_text": "Then I learned to listen.",
            "source_span_refs": [source_span_ref],
            "transformation_operations": ["make the source consequence explicit without changing the belief revision"],
            "voice_dna_applied": True,
            "claim_state": "SOURCE_GROUNDED_CONDENSATION",
            "epistemic_state": "inferred",
            "sequence_role": "recognition turn",
        },
    ]
    proposal_payload = {
        **_base("proposal_id", "demo:script-proposal", lifecycle="validated", epistemic="inferred"),
        "authoring_request_ref": jit_ref,
        "program_ref": primary_program_ref,
        "producer_actor_id": "demo:guest-voice-script-writer",
        "segments": segments,
        "rejected_alternative_refs": [_ref("demo:rejected-script:generic-advice")],
        "limitations": ["development fixture"],
    }
    proposal = app.derivatives.store_proposal(proposal_payload, idempotency_key="phase5-demo:proposal")["object"]
    proposal_ref = _stored_ref(proposal)

    lineage_refs: list[dict[str, str]] = []
    lineage_specs = [
        ("VERBATIM", segments[0], None, True, "DIRECT_QUOTE"),
        ("VOICE_DNA_REWRITE", segments[1], voice_ref, False, "SOURCE_GROUNDED"),
    ]
    for index, (transform, segment, voice, exact, claim) in enumerate(lineage_specs):
        payload = {
            **_base("lineage_id", f"demo:source-lineage:{index}", lifecycle=None, epistemic="observed" if index == 0 else "inferred"),
            "source_refs": [moment_ref, source_package_ref],
            "target_ref": _ref(segment["segment_id"], canonical_sha256(segment)),
            "transformation_class": transform,
            "operations": list(segment["transformation_operations"]),
            "source_text": segment["source_text"],
            "target_text": segment["final_text"],
            "source_span_refs": list(segment["source_span_refs"]),
            "claim_state": claim,
            "exact_quote_match": exact,
            "limitations": ["development source lineage"],
        }
        if voice is not None:
            payload["voice_dna_ref"] = voice
        stored = app.transfer.store_lineage(payload, idempotency_key=f"phase5-demo:lineage:{index}")["object"]
        lineage_refs.append(_stored_ref(stored))

    distillation_payload = {
        **_base("receipt_id", "demo:distillation:source-fidelity", lifecycle=None, epistemic=None),
        "layer": "compression",
        "input_refs": [proposal_ref, *lineage_refs],
        "output_refs": [_ref("demo:final-script-candidate")],
        "decisions": ["retain exact source confession", "make the source consequence explicit", "reject generic empathy language"],
        "edge_product_preserved": True,
        "role_tension_preserved": True,
        "voice_dna_preserved": True,
        "visual_dna_preserved": True,
        "rejection_refs": [_ref("demo:rejected-script:generic-advice")],
    }
    distillation = app.store(
        "distillation_layer_receipt",
        distillation_payload,
        idempotency_key="phase5-demo:distillation",
    )["object"]
    distillation_ref = _stored_ref(distillation)

    script_payload = {
        **_base("script_id", "demo:final-script", lifecycle="validated", epistemic="inferred"),
        "program_ref": primary_program_ref,
        "proposal_ref": proposal_ref,
        "segments": segments,
        "script_sha256": canonical_sha256(segments),
        "evaluation_receipt_refs": [_ref("demo:independent-script-evaluation")],
        "operator_approved": False,
        "source_lineage_refs": lineage_refs,
        "role_tension_ref": role_ref,
        "primitive_coalition_ref": coalition_ref,
        "archetype_coalition_ref": archetype_ref,
        "brand_context_ref": brand_ref,
        "voice_dna_ref": voice_ref,
        "distillation_receipt_refs": [distillation_ref],
        "ccv_axes": {
            "source_fidelity": "locked",
            "edge_integrity": "locked",
            "voice_specificity": "bounded variation",
        },
        "wrong_reading_lock_refs": [wrong_lock_ref],
        "maximum_claim": "SOURCE_GROUNDED_FINAL_SCRIPT_DEVELOPMENT_EVIDENCE",
        "composition_eligible": False,
        "limitations": ["operator approval required before composition"],
    }
    candidate_script = app.derivatives.store_script(
        script_payload,
        idempotency_key="phase5-demo:final-script-candidate",
    )["object"]
    candidate_script_ref = _stored_ref(candidate_script)

    approval_result = app.derivatives.approve_script(
        candidate_script_ref=candidate_script_ref,
        operator_id="demo-operator",
        operator_decision_ref=_ref("demo:operator-final-script-decision"),
        evaluation_refs=[_ref("demo:independent-script-evaluation")],
        rationale="Exact source-grounded bytes preserve the guest's belief revision and viewer role.",
        approval_idempotency_key="phase5-demo:script-approval",
        script_revision_idempotency_key="phase5-demo:approved-script",
    )
    approval_ref = _stored_ref(approval_result["approval"]["object"])
    approved_script_ref = _stored_ref(approval_result["script"]["object"])

    composition_intent_ref = _ref("demo:composition-intent:identity-before-claim")
    animation_payload = {
        **_base("package_id", "demo:animation-scene-package", lifecycle="approved", epistemic="operator_confirmed"),
        "final_script_ref": approved_script_ref,
        "scenes": [
            {
                "scene_id": "demo:animation-scene:control-listening",
                "segment_refs": [_ref(segment["segment_id"], canonical_sha256(segment)) for segment in segments],
                "source_refs": [moment_ref, source_package_ref],
                "role_tension_movement": "move from self-recognizing witness to accountable chooser",
                "sequence_role": "explain the hidden consequence of control",
                "timing_intent": "preserve the source pause before revealing the listening consequence",
                "bbox_intents": [
                    {
                        "intent_id": "demo:bbox-intent:identity-anchor",
                        "semantic_target_ref": moment_ref,
                        "attention_function": "keep the human source as the identity anchor",
                        "why": "the explanatory scene must remain attached to the guest expression",
                        "allowed_variation": ["bounded scale", "bounded horizontal shift"],
                        "forbidden_outcomes": ["generic faceless quote graphic"],
                    }
                ],
                "composition_intent": "use negative space to hold the unresolved choice between control and listening",
                "identity_continuity_refs": [visual_index_ref],
                "visual_requirement_intents": [
                    {
                        "intent_id": "demo:visual-intent:explanatory-broll",
                        "asset_family": "2d_animation_scene",
                        "semantic_role": "externalize the control-versus-listening tension",
                        "sequence_role": "bounded explanatory b-roll",
                        "composition_intent_ref": composition_intent_ref,
                        "feature_contract_refs": [_ref("demo:feature-contract:animation-scene")],
                        "identity_continuity_refs": [visual_index_ref],
                        "geometry_need": "one subject anchor and one negative-space claim region",
                        "permitted_variation": "style and pose may vary while source identity and role remain stable",
                        "preservation_lock_refs": [wrong_lock_ref],
                        "source_reference_refs": [moment_ref, visual_index_ref],
                        "evaluation_profile_ref": _ref("demo:evaluation-profile:animation-scene"),
                        "priority": 1,
                        "limitations": ["VAE chooses production strategy later"],
                        "authority_class": "NONAUTHORITATIVE_REQUIREMENT_INTENT",
                    }
                ],
                "wrong_reading_lock_refs": [wrong_lock_ref],
                "reuse_roles": ["SHORT_BROLL", "CAROUSEL_SLIDE", "SUPERVISUAL_ELEMENT", "ANIMATION_SHORT"],
            }
        ],
        "render_disposition": "DEFER_RENDER_PRESERVE_PACKAGE",
        "format02_activated": False,
        "limitations": ["scene package is composition-ready but not rendered in Phase 5"],
    }
    animation_package = app.derivatives.store_animation_package(
        animation_payload,
        idempotency_key="phase5-demo:animation-package",
    )["object"]
    animation_package_ref = _stored_ref(animation_package)

    transfer_payload = {
        **_base("contract_id", "demo:activation-transfer-contract", lifecycle="approved", epistemic="operator_confirmed"),
        "source_expression_refs": [moment_ref, reaction_ref],
        "source_package_refs": [source_package_ref],
        "expression_moment_refs": [moment_ref],
        "reaction_receipt_refs": [reaction_ref],
        "selected_hypothesis_ref": selected_ref,
        "role_tension_ref": role_ref,
        "primitive_coalition_ref": coalition_ref,
        "archetype_coalition_ref": archetype_ref,
        "final_script_ref": approved_script_ref,
        "must_survive_properties": [
            {
                "property_id": "source-belief-revision",
                "property_kind": "SOURCE_MEANING",
                "statement": "the guest moved from control toward listening",
                "evidence_refs": [moment_ref, lineage_refs[0], lineage_refs[1]],
                "hard_gate": True,
            },
            {
                "property_id": "viewer-role-tension",
                "property_kind": "ROLE_TENSION",
                "statement": "the viewer remains located between protective control and relational presence",
                "evidence_refs": [role_ref, selected_ref],
                "hard_gate": True,
            },
            {
                "property_id": "anti-passivity-lock",
                "property_kind": "WRONG_READING_LOCK",
                "statement": "listening must not be interpreted as passivity",
                "evidence_refs": [wrong_lock_ref],
                "hard_gate": True,
            },
        ],
        "transformation_rules": [
            {"operation_class": "VERBATIM", "allowed": True, "constraints": ["source words remain exact"]},
            {"operation_class": "CONDENSATION", "allowed": True, "constraints": ["preserve the belief revision and disclose transformation"]},
            {"operation_class": "REWRITE", "allowed": True, "constraints": ["apply Guest Voice DNA and preserve source lineage"]},
            {"operation_class": "VISUAL_TRANSLATION", "allowed": True, "constraints": ["preserve viewer role, tension, and wrong-reading locks"]},
            {"operation_class": "ANIMATION_TRANSLATION", "allowed": True, "constraints": ["remain reusable without activating Format 02"]},
        ],
        "required_changes": [
            {
                "change_id": "make-hidden-consequence-visible",
                "reason": "the derivative must expose what control prevents",
                "target_property_ids": ["source-belief-revision", "viewer-role-tension"],
                "required_operations": ["CONDENSATION", "VISUAL_TRANSLATION"],
            }
        ],
        "wrong_reading_lock_refs": [wrong_lock_ref],
        "evaluation_profile_ref": _ref("demo:evaluation-profile:activation-transfer"),
        "limitations": ["Phase 5 evaluates script and scene contracts, not final rendered media"],
    }
    transfer_contract = app.transfer.store_contract(
        transfer_payload,
        idempotency_key="phase5-demo:transfer-contract",
    )["object"]
    transfer_contract_ref = _stored_ref(transfer_contract)

    checkpoint_payload = {
        **_base("receipt_id", "demo:transfer-checkpoint:script", lifecycle=None, epistemic=None),
        "contract_ref": transfer_contract_ref,
        "checkpoint": "SCRIPT",
        "target_ref": approved_script_ref,
        "property_results": [
            {"property_id": "source-belief-revision", "result": "PASS", "evidence_refs": lineage_refs, "reason": "source and rewritten consequence retain explicit lineage"},
            {"property_id": "viewer-role-tension", "result": "PASS", "evidence_refs": [role_ref, selected_ref], "reason": "approved script preserves the role and unresolved choice"},
        ],
        "wrong_reading_results": [
            {"property_id": "anti-passivity-lock", "result": "PASS", "evidence_refs": [wrong_lock_ref, approved_script_ref], "reason": "script distinguishes listening from passivity"}
        ],
        "deterministic_pass": True,
        "independent_evaluator_ref": _ref("demo:independent-transfer-evaluator"),
        "limitations": ["development-only deterministic checkpoint"],
    }
    checkpoint = app.transfer.store_checkpoint(
        checkpoint_payload,
        idempotency_key="phase5-demo:transfer-checkpoint",
    )["object"]
    checkpoint_ref = _stored_ref(checkpoint)

    transfer_evaluation_payload = {
        **_base("receipt_id", "demo:transfer-evaluation", lifecycle=None, epistemic=None),
        "contract_ref": transfer_contract_ref,
        "checkpoint_refs": [checkpoint_ref],
        "deterministic_gate_passed": True,
        "independent_evaluation_ref": _ref("demo:independent-transfer-evaluation"),
        "verdict": "PASS",
        "failed_property_ids": [],
        "limitations": ["rendered composition remains a later-phase checkpoint"],
    }
    transfer_evaluation = app.transfer.store_evaluation(
        transfer_evaluation_payload,
        idempotency_key="phase5-demo:transfer-evaluation",
    )["object"]

    semantic_package_payload = {
        **_base("package_id", "demo:semantic-production-package", lifecycle="approved", epistemic="operator_confirmed"),
        "derivative_program_ref": primary_program_ref,
        "approved_final_script_ref": approved_script_ref,
        "animation_scene_package_ref": animation_package_ref,
        "activation_transfer_contract_ref": transfer_contract_ref,
        "source_lineage_refs": lineage_refs,
        "observed_activative_pack_ref": observed_ref,
        "matrix_of_edging_ref": matrix_ref,
        "role_tension_ref": role_ref,
        "primitive_coalition_ref": coalition_ref,
        "archetype_coalition_ref": archetype_ref,
        "brand_context_ref": brand_ref,
        "voice_dna_ref": voice_ref,
        "visual_dna_ref": visual_ref,
        "distillation_receipt_refs": [distillation_ref],
        "approval_receipt_ref": approval_ref,
        "rejected_candidate_refs": [hypothesis_refs[1], hypothesis_refs[2], _ref("demo:rejected-script:generic-advice")],
        "wrong_reading_lock_refs": [wrong_lock_ref],
        "evaluation_profile_ref": _ref("demo:evaluation-profile:semantic-production-package"),
        "claim_ceiling": "PHASE_05_SEMANTIC_PRODUCTION_COMPILER_DEVELOPMENT_EVIDENCE",
        "downstream_consumers": ["atomic-harness-pipeline", "conscious-activations-studio", "visual-asset-editor"],
        "limitations": ["no media composition or rendering occurs in Phase 5"],
    }
    semantic_package = app.derivatives.store_semantic_package(
        semantic_package_payload,
        idempotency_key="phase5-demo:semantic-package",
    )["object"]

    return {
        "demo_id": "phase5-semantic-production-compiler-demo",
        "synthetic_fixture_only": True,
        "source_package_ref": source_package_ref,
        "expression_moment_ref": moment_ref,
        "reaction_receipt_ref": reaction_ref,
        "portfolio_ref": _stored_ref(promoted_portfolio),
        "hypothesis_refs": hypothesis_refs,
        "gate_receipt_refs": gate_refs,
        "comparison_ref": comparison_ref,
        "stopping_receipt_ref": stopping_ref,
        "planned_pack_ref": planned_pack_ref,
        "promotion_ref": promotion_ref,
        "selected_hypothesis_ref": selected_ref,
        "archetype_coalition_ref": archetype_ref,
        "brand_context_ref": brand_ref,
        "voice_dna_ref": voice_ref,
        "visual_dna_ref": visual_ref,
        "derivative_program_refs": program_refs,
        "approved_final_script_ref": approved_script_ref,
        "final_script_approval_ref": approval_ref,
        "animation_scene_package_ref": animation_package_ref,
        "activation_transfer_contract_ref": transfer_contract_ref,
        "transfer_checkpoint_ref": checkpoint_ref,
        "transfer_evaluation_ref": _stored_ref(transfer_evaluation),
        "semantic_production_package_ref": _stored_ref(semantic_package),
        "health": app.repository.health(),
        "claim_ceiling": "PHASE_05_SEMANTIC_PRODUCTION_COMPILER_DEVELOPMENT_EVIDENCE",
        "external_model_calls": 0,
        "real_human_evidence_claimed": False,
        "composition_rendered": False,
        "format02_activated": False,
        "vae_stage5_authorized": False,
        "production_authorized": False,
        "certified": False,
    }
