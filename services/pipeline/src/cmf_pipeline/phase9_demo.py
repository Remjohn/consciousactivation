from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from ca_contracts import canonical_json_text, canonical_sha256
from conscious_activations_interview_expression.demo import run_demo as run_interview_demo
from cmf_activative_intelligence.application import AirApplication
from cmf_activative_intelligence.production_demo import run_production_demo
from cmf_pipeline.application import PipelineApplication
from cmf_pipeline.phase6_demo import run_phase6_demo
from cmf_vae.phase8_demo import run_phase8_demo


def ref(value: Mapping[str, Any], *, fallback_id: str = "ref") -> dict[str, str]:
    current: Mapping[str, Any] = value.get("object", value) if isinstance(value, Mapping) else {}
    return {
        "object_id": str(current.get("object_id", current.get("id", fallback_id))),
        "version": str(current.get("semantic_version", current.get("version", "1.0.0"))),
        "sha256": str(current.get("canonical_sha256", current.get("sha256", canonical_sha256(current)))),
    }


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json_text(value) + "\n", encoding="utf-8")


def _artifact_ref(identifier: str, version: str, sha256: str) -> dict[str, str]:
    return {"object_id": identifier, "version": version, "sha256": sha256}


def _knowledge_projection(
    identifier: str,
    *,
    source_kind: str,
    title: str,
    summary: str,
    source_ref: Mapping[str, Any],
    contradiction_ids: list[str] | None = None,
    failed_alternative: bool = False,
) -> dict[str, Any]:
    return {
        "projection_id": identifier,
        "object_ref": {"object_id": f"object:{identifier}", "version": "1.0.0", "sha256": canonical_sha256({"object": identifier})},
        "source_kind": source_kind,
        "authority_state": "current",
        "lifecycle_state": "VALIDATED",
        "title": title,
        "summary": summary,
        "category_ids": ["short_form_edited_video"],
        "format_profile_ids": ["format07_direct_coaching_a_roll"],
        "role_ids": ["composer"],
        "tags": ["source-fidelity", "reaction-tail"],
        "relationship_edges": [],
        "evidence_refs": [dict(source_ref)],
        "reaction_receipt_refs": [],
        "expression_moment_refs": [],
        "contradicts_ids": list(contradiction_ids or []),
        "supersedes_ids": [],
        "failed_alternative": failed_alternative,
        "evidence_quality_micros": 850_000,
        "permitted_action_ids": ["compile_edl", "evaluate_render"],
        "content_sha256": canonical_sha256({"title": title, "summary": summary}),
    }


def run_phase9_demo(output_dir: str | Path, repo_root: str | Path) -> dict[str, Any]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    repo = Path(repo_root)

    interview = run_interview_demo(output / "interview.sqlite3")
    semantic = run_production_demo(output / "air.sqlite3", output / "interview-semantic.sqlite3")
    source_ref = {
        "object_id": interview["source_package"]["object_id"],
        "version": interview["source_package"]["version"],
        "sha256": interview["source_package"]["sha256"],
    }

    air = AirApplication(output / "air.sqlite3")
    air.initialize()
    air.load_registries()

    iac = air.phase9.compile_interview_asset_contract(
        program_id="phase9:iac",
        planned_pack_ref=semantic["planned_pack_ref"],
        source_context_ref=source_ref,
        evidence_refs=[interview["expression_moment_ref"], interview["reaction_receipt_ref"]],
        parent_lock_refs=[{"object_id": "lock:source-truth", "version": "1.0.0", "sha256": "c" * 64}],
        evaluation_profile_ref=semantic["comparison_ref"],
        idempotency_key="phase9:iac",
    )
    iac_ref = ref(iac)
    arm = air.phase9.arm_contract(
        receipt_id="phase9:iac-arm",
        contract_ref=iac_ref,
        session_context_ref=source_ref,
        compiler_actor_id="phase9:iac-compiler",
        evaluator_actor_id="phase9:independent-evaluator",
        human_actor_id="operator:emilio",
        idempotency_key="phase9:iac-arm",
    )
    live = air.phase9.compile_live_policy(
        proposal_id="phase9:live-policy",
        contract_ref=iac_ref,
        live_state_ref=interview["observed_evidence_pack_ref"],
        evidence_refs=[interview["reaction_receipt_ref"], interview["expression_moment_ref"]],
        current_dose=1,
        ceiling=3,
        overload=False,
        producer_actor_id="phase9:policy-compiler",
        evaluator_actor_id="phase9:policy-evaluator",
        idempotency_key="phase9:live-policy",
    )
    observed = air.phase9.compile_observed_pack(
        pack_id="phase9:observed-pack",
        source_package_refs=[source_ref],
        reaction_refs=[interview["reaction_receipt_ref"]],
        expression_refs=[interview["expression_moment_ref"]],
        input_manifest_ref=interview["observed_evidence_pack_ref"],
        candidate_portfolio_ref=semantic["portfolio_ref"],
        independent_evaluation_ref=semantic["comparison_ref"],
        human_resolution_ref={"object_id": "human-resolution:phase9-observed", "version": "1.0.0", "sha256": "d" * 64},
        planned_pack_ref=semantic["planned_pack_ref"],
        idempotency_key="phase9:observed-pack",
    )
    observed_ref = ref(observed)

    relationship_state, relationship_program = air.phase9.compile_relationship_program(
        state_id="phase9:relationship",
        subject_ref={"object_id": "person:guest", "version": "1.0.0", "sha256": "1" * 64},
        evidence_refs=[interview["expression_moment_ref"]],
        coalition_ref={"object_id": "primitive-coalition:phase9", "version": "1.0.0", "sha256": "2" * 64},
        evaluation_ref=semantic["comparison_ref"],
        idempotency_key="phase9:relationship",
    )
    visual_handoff = air.phase9.compile_visual_handoff(
        handoff_id="phase9:visual-handoff",
        source_refs=[source_ref, interview["expression_moment_ref"]],
        semantic_package_ref=semantic["semantic_production_package_ref"],
        final_script_ref=semantic["approved_final_script_ref"],
        transfer_ref=semantic["activation_transfer_contract_ref"],
        wrong_reading_locks=[{"object_id": "lock:source-truth", "version": "1.0.0", "sha256": "c" * 64}],
        producer_actor_id="phase9:visual-semantic-compiler",
        evaluator_actor_id="phase9:visual-semantic-evaluator",
        idempotency_key="phase9:visual-handoff",
    )
    visual_evaluation = air.phase9.evaluate_activation(
        receipt_id="phase9:visual-evaluation",
        target_ref=ref(visual_handoff),
        profile_ref=semantic["comparison_ref"],
        producer_actor_id="phase9:visual-semantic-compiler",
        evaluator_actor_id="phase9:visual-semantic-evaluator",
        checks=[
            {"check_id": "source-lineage", "hard_gate": True, "result": "PASS", "evidence_refs": [source_ref]},
            {"check_id": "wrong-reading-locks", "hard_gate": True, "result": "PASS", "evidence_refs": [ref(visual_handoff)]},
        ],
        judgments=[{"dimension": "role-inside-tension", "score_micros": 900_000, "limitations": ["development evaluator"]}],
        idempotency_key="phase9:visual-evaluation",
    )

    media = run_phase6_demo(output / "pipeline.sqlite3", output / "media")
    vae = run_phase8_demo(output / "vae", repo / "03_DELEGATION_PROTOCOL/delegation-contracts/1.1.0-rc.4")

    campaign_payload = {
        "campaign_program_id": "phase9:campaign",
        "version": "1.0.0",
        "audience_context_ref": {"object_id": "audience:operators", "version": "1.0.0", "sha256": "e" * 64},
        "source_package_refs": [source_ref],
        "entry_program_refs": list(semantic["derivative_program_refs"].values()),
        "freshness_policy_ref": {"object_id": "freshness-policy:phase9", "version": "1.0.0", "sha256": "f" * 64},
        "activation_axes": [
            {
                "entry_program_ref": program_ref,
                "psychological_role": role,
                "tension": "Control protects agency while creating distance.",
                "edge_product_ref": {"object_id": "edge-product:phase9", "version": "1.0.0", "sha256": "3" * 64},
                "primitive_coalition_ref": {"object_id": "primitive-coalition:phase9", "version": "1.0.0", "sha256": "2" * 64},
                "archetype_coalition_ref": semantic["archetype_coalition_ref"],
                "relief_state": relief,
            }
            for program_ref, role, relief in zip(
                list(semantic["derivative_program_refs"].values()),
                ["self-recognizing witness", "accountable chooser", "protective skeptic", "participant"],
                ["NONE", "PARTIAL", "FULL", "AFFINITY_RESET"],
                strict=True,
            )
        ],
        "sequence_constraints": ["preserve source-first lineage", "do not repeat the same viewer role consecutively"],
        "relief_requirements": ["every pressure sequence must provide a truthful release or participation route"],
        "lifecycle_state": "VALIDATED",
        "authority": {"authority_id": "ca-program-control-v2.1-candidate", "authority_version": "2.1.0-candidate", "authority_sha256": "a" * 64, "authority_state": "candidate_not_current"},
    }
    campaign = air.campaigns.store_program(campaign_payload, idempotency_key="phase9:campaign")
    campaign_ref = ref(campaign)
    freshness = air.campaigns.compile_freshness_profile(
        campaign_program_ref=campaign_ref,
        audience_context_ref=campaign_payload["audience_context_ref"],
        platform_id="development-export",
        window_id="phase9-reference-window",
        exposures=[
            {
                "asset_ref": _artifact_ref(media["video_artifact"]["artifact_id"], media["video_artifact"]["artifact_version"], media["video_artifact"]["sha256"]),
                "pattern_ids": ["viewer-role:self-recognizing-witness"],
                "impressions": 100,
                "engagements": 12,
                "shares": 4,
                "cohort_id": "cohort:reference",
                "paid_or_organic": "organic",
                "metric_definition_ref": {"object_id": "metric:reference", "version": "1.0.0", "sha256": "4" * 64},
            }
        ],
        policy={"repeated_pattern_threshold": 3, "minimum_share_rate_micros": 1000},
        idempotency_key="phase9:freshness",
    )
    audience_reaction = air.campaigns.record_audience_reaction(
        campaign_program_ref=campaign_ref,
        asset_ref=_artifact_ref(media["video_artifact"]["artifact_id"], media["video_artifact"]["artifact_version"], media["video_artifact"]["sha256"]),
        audience_context_ref=campaign_payload["audience_context_ref"],
        observations=[
            {"observation_id": "phase9:operator-review", "metric_name": "operator_acceptance", "value": 1, "denominator": 1, "epistemic_state": "observed", "limitations": ["development operator review; not platform telemetry"], "metric_definition_ref": {"object_id": "metric:operator-review", "version": "1.0.0", "sha256": "5" * 64}}
        ],
        evaluator_id="phase9:audience-evaluator",
        producer_id="phase9:publishing-adapter",
        idempotency_key="phase9:audience-reaction",
    )
    campaign_revision = air.campaigns.propose_revision(
        campaign_program_ref=campaign_ref,
        freshness_profile_ref=ref(freshness),
        affected_entry_refs=[semantic["derivative_program_refs"]["source_short"]],
        reason_codes=["DEVELOPMENT_REVIEW_ONLY"],
        owner_product="activative-intelligence-runtime",
        idempotency_key="phase9:campaign-revision",
    )

    pipeline = PipelineApplication(output / "pipeline.sqlite3")
    pipeline.initialize()

    transformation = pipeline.skills.register_transformation_contract(
        {
            "contract_id": "transform:source-led-short", "version": "1.0.0",
            "input_contract_ids": ["canonical_interview_source_package", "approved_final_script", "activation_transfer_contract"],
            "output_contract_ids": ["video_edit_program"],
            "required_invariants": ["source_truth", "speaker_identity", "reaction_tail"],
            "allowed_transformation_classes": ["trim", "caption", "overlay", "reframe"],
            "forbidden_transformations": ["invented_quote", "voice_replacement", "semantic_rewrite"],
            "evaluation_profile_refs": [semantic["transfer_evaluation_ref"]],
            "source_refs": [source_ref],
        },
        idempotency_key="phase9:transformation-contract",
    )
    transformation_ref = ref(transformation)
    skill = pipeline.skills.register_skill(
        {
            "skill_id": "skill:phase9:source-led-short", "version": "1.0.0", "title": "Source-led short composition",
            "purpose": "Preserve source A-roll, exact word boundaries, and the reaction tail while compiling a category-native short.",
            "authority_owner": "atomic-harness-pipeline", "lifecycle_state": "VALIDATED",
            "category_ids": ["short_form_edited_video"], "format_profile_ids": ["format07_direct_coaching_a_roll"],
            "entry_condition_ids": ["source_package_ready", "final_script_approved", "transfer_contract_ready"],
            "output_contract_ids": ["video_edit_program"], "allowed_tool_ids": ["ffmpeg", "remotion", "hyperframes"],
            "forbidden_action_ids": ["semantic_rewrite", "source_voice_replacement"],
            "invariant_locks": ["source_truth", "speaker_identity", "reaction_tail"],
            "recipe_family_ids": ["source-led-short"], "source_refs": [source_ref],
            "evaluation_profile_refs": [semantic["transfer_evaluation_ref"]],
        },
        idempotency_key="phase9:skill",
    )
    skill_ref = ref(skill)
    recipe = pipeline.skills.register_recipe(
        {
            "recipe_id": "recipe:phase9:preserve-reaction-tail", "version": "1.0.0", "skill_id": skill_ref["object_id"],
            "recipe_family_id": "source-led-short", "lifecycle_state": "VALIDATED",
            "primitive_coalition_ref": {"object_id": "primitive-coalition:phase9", "version": "1.0.0", "sha256": "2" * 64},
            "coalition_signature_ref": {"object_id": "coalition-signature:phase9", "version": "1.0.0", "sha256": "6" * 64},
            "edge_product_ref": {"object_id": "edge-product:phase9", "version": "1.0.0", "sha256": "3" * 64},
            "category_ids": ["short_form_edited_video"], "format_profile_ids": ["format07_direct_coaching_a_roll"],
            "failure_codes": ["REACTION_TAIL_LOST"], "applicability_tags": ["talking-head", "source-first"],
            "protected_properties": ["source_truth", "reaction_tail"],
            "operations": [
                {"tool_id": "ffmpeg", "tool_version": "development", "arguments": {"padding_ms": 120}, "preconditions": ["word_boundaries_available"], "expected_effect": "Preserve the bounded reaction tail."}
            ],
            "evidence_refs": [{"object_id": "human-resolution:phase9", "version": "1.0.0", "sha256": "7" * 64}],
            "control_comparison_refs": [semantic["comparison_ref"]], "regression_case_refs": [{"object_id": "regression:reaction-tail", "version": "1.0.0", "sha256": "8" * 64}],
            "limitations": ["development evidence only"],
        },
        idempotency_key="phase9:recipe",
    )
    skill_resolution = pipeline.skills.resolve(
        skill_id=skill_ref["object_id"], category_id="short_form_edited_video",
        format_profile_id="format07_direct_coaching_a_roll", failure_codes=["REACTION_TAIL_LOST"],
        applicability_tags=["talking-head", "source-first"], idempotency_key="phase9:skill-resolution",
    )

    projections = [
        _knowledge_projection("knowledge:phase9:skill", source_kind="skill", title="Source fidelity skill", summary="Preserve source A-roll, word boundaries, and reaction tail.", source_ref=skill_ref, contradiction_ids=["knowledge:phase9:contradiction"]),
        _knowledge_projection("knowledge:phase9:recipe", source_kind="steering_recipe", title="Preserve reaction tail", summary="Keep the bounded tail after the source phrase when expression continues.", source_ref=ref(recipe)),
        _knowledge_projection("knowledge:phase9:failed", source_kind="failure_precedent", title="Overcompressed source edit", summary="The previous edit removed hesitation and changed the human reading.", source_ref=source_ref, failed_alternative=True),
        _knowledge_projection("knowledge:phase9:contradiction", source_kind="failure_precedent", title="Speed is not source fidelity", summary="Faster pacing can destroy the original expression moment.", source_ref=source_ref),
    ]
    for index, projection in enumerate(projections):
        pipeline.retrieval.register_projection(projection, idempotency_key=f"phase9:knowledge:{index}")
    retrieval_result = pipeline.retrieval.compile_capsule(
        {
            "request_id": "retrieval:phase9:source-led-short", "query_text": "preserve source reaction tail",
            "role_id": "composer", "category_id": "short_form_edited_video",
            "format_profile_id": "format07_direct_coaching_a_roll", "required_source_kinds": ["skill", "steering_recipe", "failure_precedent"],
            "required_tags": ["source-fidelity"], "required_action_ids": ["compile_edl"],
            "required_projection_ids": ["knowledge:phase9:skill"], "include_contradictions": True,
            "include_failed_alternatives": True, "budget_bytes": 30_000,
            "allowed_tool_ids": ["ffmpeg", "remotion", "hyperframes"],
            "forbidden_action_ids": ["semantic_rewrite", "source_voice_replacement"],
            "stopping_law_id": "minimum-complete-context", "source_package_ref": source_ref,
        },
        idempotency_key="phase9:retrieval",
    )

    model_artifact = pipeline.programmed_models.register_artifact(
        {
            "model_artifact_id": "model-artifact:phase9:tool-router", "version": "1.0.0",
            "artifact_ref": {"object_id": "weights:phase9:tool-router", "version": "1.0.0", "sha256": "9" * 64},
            "model_family": "bounded-small-tool-router", "architecture": "decoder-only", "parameter_count": 1_000_000_000,
            "quantization": "int8", "runtime_ids": ["local-cpu-reference"],
            "tokenizer_ref": {"object_id": "tokenizer:phase9", "version": "1.0.0", "sha256": "a" * 64},
            "training_dataset_refs": [{"object_id": "dataset:human-resolutions", "version": "1.0.0", "sha256": "b" * 64}],
            "evaluation_dataset_refs": [{"object_id": "dataset:shadow-evaluation", "version": "1.0.0", "sha256": "c" * 64}],
            "applicability_envelope": {"category_ids": ["short_form_edited_video"], "format_profile_ids": ["format07_direct_coaching_a_roll"], "role_ids": ["composer"], "task_types": ["bounded_tool_routing"]},
            "lifecycle_state": "SHADOW", "limitations": ["shadow only", "no visual judgment"],
            "source_authority_refs": [{"object_id": "program-control:v2.1-candidate", "version": "2.1.0-candidate", "sha256": "d" * 64}],
        },
        idempotency_key="phase9:model-artifact",
    )
    model_claim = pipeline.programmed_models.register_claim(
        {
            "claim_id": "model-claim:phase9:tool-router", "model_artifact_ref": ref(model_artifact),
            "claim_type": "bounded_tool_routing", "lifecycle_state": "SHADOW",
            "applicability_envelope": model_artifact["object"]["payload"]["applicability_envelope"],
            "benchmark_ref": {"object_id": "benchmark:phase9:tool-router", "version": "1.0.0", "sha256": "e" * 64},
            "evaluator_ref": {"object_id": "evaluator:phase9:independent", "version": "1.0.0", "sha256": "f" * 64},
            "metric_name": "task_accuracy_micros", "threshold_micros": 800_000, "observed_micros": 900_000,
            "failure_limit_micros": 200_000, "fallback_mode": "DETERMINISTIC_OR_HUMAN",
            "limitations": ["synthetic shadow evidence"], "evidence_refs": [ref(visual_evaluation)],
        },
        idempotency_key="phase9:model-claim",
    )
    model_program = pipeline.programmed_models.register_program(
        {
            "model_program_id": "model-program:phase9:tool-router", "version": "1.0.0", "claim_ref": ref(model_claim),
            "input_contract_id": "tool-routing-request", "output_contract_id": "typed-tool-call",
            "skill_refs": [skill_ref], "steering_recipe_refs": [ref(recipe)],
            "allowed_tool_ids": ["ffmpeg", "remotion", "hyperframes"],
            "forbidden_action_ids": ["semantic_rewrite", "source_voice_replacement"],
            "fallback_mode": "DETERMINISTIC_OR_HUMAN", "escalation_conditions": ["ambiguity", "hard_gate_failure"],
            "runtime_requirements": {"runtime_ids": ["local-cpu-reference"]}, "lifecycle_state": "SHADOW",
        },
        idempotency_key="phase9:model-program",
    )
    model_resolution = pipeline.programmed_models.resolve(
        {
            "request_id": "model-resolution:phase9", "claim_type": "bounded_tool_routing",
            "category_id": "short_form_edited_video", "format_profile_id": "format07_direct_coaching_a_roll",
            "role_id": "composer", "task_type": "bounded_tool_routing",
            "available_runtime_ids": ["local-cpu-reference"], "maximum_parameter_count": 2_000_000_000,
            "required_tool_ids": ["ffmpeg"], "allowed_lifecycle_states": ["SHADOW"],
        },
        idempotency_key="phase9:model-resolution",
    )
    model_evidence = air.programmed_model_evidence.register_claim_candidate(
        model_claim_ref=ref(model_claim), model_program_ref=ref(model_program),
        semantic_scope_refs=[semantic["semantic_production_package_ref"]],
        human_resolution_refs=[{"object_id": "human-resolution:phase9", "version": "1.0.0", "sha256": "7" * 64}],
        benchmark_ref={"object_id": "benchmark:phase9:tool-router", "version": "1.0.0", "sha256": "e" * 64},
        independent_evaluator_ref={"object_id": "evaluator:phase9:independent", "version": "1.0.0", "sha256": "f" * 64},
        producer_actor_id="phase9:model-trainer", evaluator_actor_id="phase9:model-evaluator",
        idempotency_key="phase9:model-evidence",
    )

    video_ref = _artifact_ref(media["video_artifact"]["artifact_id"], media["video_artifact"]["artifact_version"], media["video_artifact"]["sha256"])
    supervisual_ref = _artifact_ref(media["supervisual_artifact"]["artifact_id"], media["supervisual_artifact"]["artifact_version"], media["supervisual_artifact"]["sha256"])
    carousel_ref = _artifact_ref(media["carousel_artifact"]["carousel_artifact_id"], media["carousel_artifact"]["carousel_artifact_version"], media["carousel_artifact"]["pdf_artifact"]["sha256"])
    animation_ref = _artifact_ref(media["animation_artifact"]["animation_artifact_id"], media["animation_artifact"]["animation_artifact_version"], media["animation_artifact"]["sha256"])
    vae_ref = _artifact_ref(vae["result_id"], "1.0.0", vae["artifact_sha256"])
    expression_span = {"source_ref": source_ref, "start_ms": 0, "end_ms": 1000, "speaker_id": "speaker:guest", "transcript_sha256": interview["phrase_pack_ref"]["sha256"]}
    derivatives = [
        {"derivative_id": "source-led-short", "derivative_type": "SOURCE_LED_SHORT", "artifact_ref": video_ref, "source_package_ref": source_ref, "source_span_refs": [expression_span], "semantic_program_ref": semantic["derivative_program_refs"]["source_short"], "final_script_ref": semantic["approved_final_script_ref"], "transfer_contract_ref": semantic["activation_transfer_contract_ref"], "evaluation_refs": [ref({"id": media["video_evaluation"]["evaluation_id"], "version": media["video_evaluation"]["evaluation_version"], "sha256": canonical_sha256(media["video_evaluation"])})], "consumption_state": "ACKNOWLEDGED"},
        {"derivative_id": "supervisual", "derivative_type": "SUPERVISUAL", "artifact_ref": supervisual_ref, "source_package_ref": source_ref, "source_span_refs": [expression_span], "semantic_program_ref": semantic["derivative_program_refs"]["supervisual"], "final_script_ref": semantic["approved_final_script_ref"], "transfer_contract_ref": semantic["activation_transfer_contract_ref"], "evaluation_refs": [ref(visual_evaluation)], "consumption_state": "ACKNOWLEDGED"},
        {"derivative_id": "carousel", "derivative_type": "CAROUSEL", "artifact_ref": carousel_ref, "source_package_ref": source_ref, "source_span_refs": [expression_span], "semantic_program_ref": semantic["derivative_program_refs"]["carousel"], "final_script_ref": semantic["approved_final_script_ref"], "transfer_contract_ref": semantic["activation_transfer_contract_ref"], "evaluation_refs": [ref(visual_evaluation)], "consumption_state": "ACKNOWLEDGED"},
        {"derivative_id": "animation", "derivative_type": "ANIMATION_SCENE_PACKAGE", "artifact_ref": animation_ref, "source_package_ref": source_ref, "source_span_refs": [expression_span], "semantic_program_ref": semantic["derivative_program_refs"]["animation"], "final_script_ref": semantic["approved_final_script_ref"], "transfer_contract_ref": semantic["activation_transfer_contract_ref"], "evaluation_refs": [ref(visual_evaluation)], "consumption_state": "ACKNOWLEDGED"},
        {"derivative_id": "vae-reference-asset", "derivative_type": "VISUAL_ASSET", "artifact_ref": vae_ref, "source_package_ref": source_ref, "source_span_refs": [expression_span], "semantic_program_ref": semantic["derivative_program_refs"]["supervisual"], "final_script_ref": semantic["approved_final_script_ref"], "transfer_contract_ref": semantic["activation_transfer_contract_ref"], "evaluation_refs": [ref(visual_evaluation)], "consumption_state": "ACKNOWLEDGED"},
    ]
    continuity = pipeline.continuity.compile(
        source_package_ref=source_ref,
        semantic_production_package_ref=semantic["semantic_production_package_ref"],
        final_script_ref=semantic["approved_final_script_ref"],
        activation_transfer_contract_ref=semantic["activation_transfer_contract_ref"],
        derivatives=derivatives,
        usage_records=[
            {"usage_id": "usage:animation-as-broll", "source_artifact_ref": animation_ref, "consumer_derivative_id": "source-led-short", "usage_role": "BROLL", "time_or_page_locator": {"start_ms": 600, "end_ms": 1000}, "acknowledgement_ref": {"object_id": vae["acknowledgement_id"], "version": "1.0.0", "sha256": canonical_sha256({"ack": vae["acknowledgement_id"]})}}
        ],
        evaluation_refs=[ref(visual_evaluation), semantic["transfer_evaluation_ref"]],
        idempotency_key="phase9:continuity",
    )

    records = {
        "interview": interview,
        "semantic": semantic,
        "interview_asset_contract": iac["object"],
        "arm_receipt": arm["object"],
        "live_policy": live["object"],
        "observed_pack": observed["object"],
        "relationship_state": relationship_state["object"],
        "relationship_program": relationship_program["object"],
        "visual_handoff": visual_handoff["object"],
        "visual_evaluation": visual_evaluation["object"],
        "campaign": campaign["object"],
        "freshness": freshness["object"],
        "audience_reaction": audience_reaction["object"],
        "campaign_revision": campaign_revision["object"],
        "transformation_contract": transformation["object"],
        "skill": skill["object"],
        "recipe": recipe["object"],
        "skill_resolution": skill_resolution["object"],
        "jit_capsule": retrieval_result.capsule,
        "retrieval_receipt": retrieval_result.receipt,
        "model_artifact": model_artifact["object"],
        "model_claim": model_claim["object"],
        "model_program": model_program["object"],
        "model_resolution": model_resolution["object"],
        "model_evidence": model_evidence["object"],
        "continuity": continuity["object"],
        "media": media,
        "vae": vae,
    }
    for name, value in records.items():
        write_json(output / f"{name}.json", value)

    receipt = {
        "pilot_core_id": "phase9-integrated-core",
        "source_package_ref": source_ref,
        "semantic_production_package_ref": semantic["semantic_production_package_ref"],
        "continuity_ref": ref(continuity),
        "artifact_refs": [video_ref, supervisual_ref, carousel_ref, animation_ref, vae_ref],
        "artifact_count": 5,
        "skill_resolution_ref": ref(skill_resolution),
        "retrieval_capsule_ref": {"object_id": retrieval_result.capsule["capsule_id"], "version": retrieval_result.capsule["capsule_version"], "sha256": retrieval_result.capsule["capsule_sha256"]},
        "model_resolution_ref": ref(model_resolution),
        "campaign_ref": campaign_ref,
        "production_authorized": False,
        "certified": False,
        "format02_activated": False,
        "vae_stage5_authorized": False,
        "real_platform_pilot_executed": False,
        "claim_ceiling": "PHASE_09_FINAL_INTEGRATED_DEVELOPMENT_CANDIDATE",
    }
    receipt["pilot_core_sha256"] = canonical_sha256(receipt)
    write_json(output / "phase9-core-receipt.json", receipt)
    write_json(output / "release_evidence.json", {"release_state": "DEVELOPMENT_REFERENCE_CANDIDATE", "pilot_core_ref": {"object_id": receipt["pilot_core_id"], "version": "0.9.0-dev.1", "sha256": receipt["pilot_core_sha256"]}, "artifact_count": receipt["artifact_count"], "production_authorized": False, "certified": False, "format02_activated": False})
    return {**receipt, "output_dir": str(output), "media_output_dir": str(output / "media"), "vae_output_dir": str(output / "vae"), "pipeline_database": str(output / "pipeline.sqlite3"), "air_database": str(output / "air.sqlite3")}
