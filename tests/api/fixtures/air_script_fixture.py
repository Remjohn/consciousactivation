from __future__ import annotations

from typing import Any

from ca_contracts import canonical_sha256
from cmf_activative_intelligence.application import AirApplication
from cmf_activative_intelligence.demo import run_demo as run_air_core_demo

from .air_portfolio_fixture import AUTHORITY, _ref, _stored_ref, build_portfolio_fixture


def _base(id_field: str, object_id: str, *, lifecycle: str | None = "validated", epistemic: str | None = "inferred") -> dict[str, Any]:
    payload: dict[str, Any] = {id_field: object_id, "version": "1.0.0", "authority": dict(AUTHORITY)}
    if lifecycle is not None:
        payload["lifecycle_state"] = lifecycle
    if epistemic is not None:
        payload["epistemic_state"] = epistemic
    return payload


def build_script_fixture(air: AirApplication, *, prefix: str) -> dict[str, Any]:
    """Builds a fresh, un-approved (operator_approved=False) final_script_package
    directly against `air`, mirroring production_demo.py's construction of the
    same object (archetype coalition, brand context, voice DNA, visual DNA,
    input manifest, program, JIT request, proposal, source lineage,
    distillation receipt, then the script itself). `prefix` must be unique per
    script within a shared database.

    Returns a dict with `script_id` plus ready-to-send request bodies for
    POST /scripts/{id}/approve (`approve_request`) and
    POST /scripts/{id}/transfer-contract (`transfer_contract_request`).
    """
    air.initialize()
    core = run_air_core_demo(air.repository.path)
    matrix_ref = dict(core["matrix_ref"])
    role_ref = dict(core["role_tension_ref"])
    binding_refs = [dict(item) for item in core["primitive_binding_refs"]]
    coalition_ref = dict(core["primitive_coalition_ref"])

    # A real, existing activation_hypothesis is required (store_input_manifest
    # existence-checks selected_hypothesis_ref) -- reuse the portfolio fixture
    # for a minimal one rather than duplicating hypothesis-construction here.
    portfolio_fx = build_portfolio_fixture(air, prefix=f"{prefix}:src")
    selected_ref = portfolio_fx["hypothesis_refs"][0]

    source_package_ref = _ref(f"{prefix}:source-package")
    moment_ref = _ref(f"{prefix}:expression-moment")
    reaction_ref = _ref(f"{prefix}:reaction-receipt")
    observed_ref = _ref(f"{prefix}:observed-evidence-pack")

    archetype = air.registries.query_archetypes("", limit=1)[0]
    archetype_payload = {
        **_base("program_id", f"{prefix}:archetype-coalition", lifecycle="approved", epistemic=None),
        "role_tension_contract_ref": role_ref,
        "primitive_coalition_ref": coalition_ref,
        "primary_archetype": {
            "binding_id": f"{prefix}:archetype-binding:primary",
            "archetype_ref": archetype.immutable_ref(),
            "current_validation_ref": _ref(f"{prefix}:archetype-current-validation"),
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
    archetype_program = air.store("archetype_coalition_program", archetype_payload, idempotency_key=f"{prefix}:archetype-coalition")["object"]
    archetype_ref = _stored_ref(archetype_program)

    brand_payload = {
        **_base("brand_context_id", f"{prefix}:brand-context", lifecycle="approved", epistemic="operator_confirmed"),
        "brand_genesis_session_ref": _ref(f"{prefix}:brand-genesis"),
        "identity_truths": ["human truth before content performance"],
        "audience_relationship": "credible challenger who protects agency",
        "positioning_tension": "real expression versus generic inspiration",
        "source_refs": [moment_ref],
    }
    brand = air.store("brand_context_version", brand_payload, idempotency_key=f"{prefix}:brand")["object"]
    brand_ref = _stored_ref(brand)

    voice_payload = {
        **_base("voice_dna_id", f"{prefix}:voice-dna", lifecycle="approved", epistemic="operator_confirmed"),
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
    voice = air.store("voice_dna", voice_payload, idempotency_key=f"{prefix}:voice")["object"]
    voice_ref = _stored_ref(voice)

    visual_payload = {
        **_base("visual_dna_id", f"{prefix}:visual-dna", lifecycle="approved", epistemic="operator_confirmed"),
        "brand_context_ref": brand_ref,
        "real_life_reference_refs": [_ref(f"{prefix}:visual-index")],
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
    visual = air.store("visual_dna", visual_payload, idempotency_key=f"{prefix}:visual")["object"]
    visual_ref = _stored_ref(visual)

    wrong_lock_ref = _ref(f"{prefix}:wrong-reading-lock:listening-not-passivity")
    input_manifest_payload = {
        **_base("manifest_id", f"{prefix}:derivative-input-manifest", lifecycle="approved", epistemic="operator_confirmed"),
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
        "objective_ref": _ref(f"{prefix}:objective:source-expression-batch"),
        "campaign_role": "source expression anchor",
        "category_id": "short_form_edited_video",
        "profile_id": "format07_direct_coaching_a_roll",
        "format_harness_ref": _ref(f"{prefix}:harness:format07"),
        "wrong_reading_lock_refs": [wrong_lock_ref],
        "limitations": ["development fixture"],
    }
    input_manifest = air.derivatives.store_input_manifest(input_manifest_payload, idempotency_key=f"{prefix}:input-manifest")["object"]
    input_manifest_ref = _stored_ref(input_manifest)

    program_payload = {
        **_base("program_id", f"{prefix}:derivative-program", lifecycle="approved", epistemic="operator_confirmed"),
        "input_manifest_ref": input_manifest_ref,
        "derivative_type": "SOURCE_LED_SHORT",
        "category_id": "short_form_edited_video",
        "profile_id": "format07_direct_coaching_a_roll",
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
        "evaluation_profile_ref": _ref(f"{prefix}:evaluation-profile"),
        "allowed_tools": ["source-lineage-reader", "guest-voice-writer", "primitive-coalition-composer"],
        "denied_tools": ["format02-runtime", "unbounded-autonomous-publisher"],
        "composition_authorized": False,
        "limitations": ["composition waits for exact operator-approved Final Script"],
    }
    program = air.derivatives.store_program(program_payload, idempotency_key=f"{prefix}:program")["object"]
    program_ref = _stored_ref(program)

    context_sha = canonical_sha256({
        "program_ref": program_ref, "voice_dna_ref": voice_ref, "primitive_coalition_ref": coalition_ref,
        "archetype_coalition_ref": archetype_ref, "source_refs": [moment_ref, reaction_ref],
    })
    jit_payload = {
        **_base("request_id", f"{prefix}:jit-authoring-request", lifecycle=None, epistemic=None),
        "program_ref": program_ref,
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
    jit = air.derivatives.store_jit_request(jit_payload, idempotency_key=f"{prefix}:jit")["object"]
    jit_ref = _stored_ref(jit)

    source_span_ref = _ref(f"{prefix}:source-span:1500-3500", source_package_ref["sha256"])
    segments = [
        {
            "segment_id": f"{prefix}:segment:0", "order": 0,
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
            "segment_id": f"{prefix}:segment:1", "order": 1,
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
        **_base("proposal_id", f"{prefix}:script-proposal", lifecycle="validated", epistemic="inferred"),
        "authoring_request_ref": jit_ref,
        "program_ref": program_ref,
        "producer_actor_id": f"{prefix}:guest-voice-script-writer",
        "segments": segments,
        "rejected_alternative_refs": [_ref(f"{prefix}:rejected-script:generic-advice")],
        "limitations": ["development fixture"],
    }
    proposal = air.derivatives.store_proposal(proposal_payload, idempotency_key=f"{prefix}:proposal")["object"]
    proposal_ref = _stored_ref(proposal)

    lineage_refs: list[dict[str, str]] = []
    lineage_specs = [
        ("VERBATIM", segments[0], None, True, "DIRECT_QUOTE"),
        ("VOICE_DNA_REWRITE", segments[1], voice_ref, False, "SOURCE_GROUNDED"),
    ]
    for index, (transform, segment, voice, exact, claim) in enumerate(lineage_specs):
        payload = {
            **_base("lineage_id", f"{prefix}:source-lineage:{index}", lifecycle=None, epistemic="observed" if index == 0 else "inferred"),
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
        stored = air.transfer.store_lineage(payload, idempotency_key=f"{prefix}:lineage:{index}")["object"]
        lineage_refs.append(_stored_ref(stored))

    distillation_payload = {
        **_base("receipt_id", f"{prefix}:distillation:source-fidelity", lifecycle=None, epistemic=None),
        "layer": "compression",
        "input_refs": [proposal_ref, *lineage_refs],
        "output_refs": [_ref(f"{prefix}:final-script-candidate")],
        "decisions": ["retain exact source confession", "make the source consequence explicit", "reject generic empathy language"],
        "edge_product_preserved": True,
        "role_tension_preserved": True,
        "voice_dna_preserved": True,
        "visual_dna_preserved": True,
        "rejection_refs": [_ref(f"{prefix}:rejected-script:generic-advice")],
    }
    distillation = air.store("distillation_layer_receipt", distillation_payload, idempotency_key=f"{prefix}:distillation")["object"]
    distillation_ref = _stored_ref(distillation)

    evaluation_receipt_ref = _ref(f"{prefix}:independent-script-evaluation")
    script_payload = {
        **_base("script_id", f"{prefix}:final-script", lifecycle="validated", epistemic="inferred"),
        "program_ref": program_ref,
        "proposal_ref": proposal_ref,
        "segments": segments,
        "script_sha256": canonical_sha256(segments),
        "evaluation_receipt_refs": [evaluation_receipt_ref],
        "operator_approved": False,
        "source_lineage_refs": lineage_refs,
        "role_tension_ref": role_ref,
        "primitive_coalition_ref": coalition_ref,
        "archetype_coalition_ref": archetype_ref,
        "brand_context_ref": brand_ref,
        "voice_dna_ref": voice_ref,
        "distillation_receipt_refs": [distillation_ref],
        "ccv_axes": {"source_fidelity": "locked", "edge_integrity": "locked", "voice_specificity": "bounded variation"},
        "wrong_reading_lock_refs": [wrong_lock_ref],
        "maximum_claim": "SOURCE_GROUNDED_FINAL_SCRIPT_DEVELOPMENT_EVIDENCE",
        "composition_eligible": False,
        "limitations": ["operator approval required before composition"],
    }
    candidate_script = air.derivatives.store_script(script_payload, idempotency_key=f"{prefix}:final-script-candidate")["object"]
    script_id = candidate_script["object_id"]

    return {
        "script_id": script_id,
        "selected_hypothesis_ref": selected_ref,
        "approve_request": {
            "idempotency_key": f"{prefix}:script-approval",
            "operator_id": f"{prefix}:operator",
            "operator_decision_ref": _ref(f"{prefix}:operator-final-script-decision"),
            "rationale": "Exact source-grounded bytes preserve the guest's belief revision and viewer role.",
            "evaluation_refs": [evaluation_receipt_ref],
        },
        "transfer_contract_request": {
            "idempotency_key": f"{prefix}:transfer-contract",
            "authority": dict(AUTHORITY),
            "source_expression_refs": [moment_ref, reaction_ref],
            "source_package_refs": [source_package_ref],
            "expression_moment_refs": [moment_ref],
            "reaction_receipt_refs": [reaction_ref],
            "selected_hypothesis_ref": selected_ref,
            "must_survive_properties": [
                {
                    "property_id": f"{prefix}:msp:source-confession",
                    "property_kind": "SOURCE_MEANING",
                    "statement": "the guest's exact belief revision about control must remain intact",
                    "evidence_refs": [moment_ref],
                    "hard_gate": True,
                }
            ],
            "transformation_rules": [
                {"operation_class": "VERBATIM", "allowed": True, "constraints": ["no paraphrase of the source confession line"]},
                {"operation_class": "VISUAL_TRANSLATION", "allowed": True, "constraints": ["keep the guest as the identity anchor"]},
            ],
            "required_changes": [
                {
                    "change_id": f"{prefix}:req-change:aspect-ratio",
                    "reason": "downstream formats require vertical framing",
                    "target_property_ids": [f"{prefix}:msp:source-confession"],
                    "required_operations": ["reframe to 9:16 without cropping the guest's face"],
                }
            ],
            "evaluation_profile_ref": _ref(f"{prefix}:evaluation-profile"),
            "limitations": ["development fixture"],
        },
    }
