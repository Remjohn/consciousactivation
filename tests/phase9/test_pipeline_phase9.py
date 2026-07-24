from __future__ import annotations

import pytest

from ca_contracts import canonical_sha256
from cmf_pipeline.application import PipelineApplication
from cmf_pipeline.domain.errors import PipelineAuthorityError, PipelineBudgetError, PipelineValidationError


def r(identifier: str, fill: str = "a") -> dict[str, str]:
    return {"object_id": identifier, "version": "1.0.0", "sha256": fill * 64}


def obj_ref(result: dict) -> dict[str, str]:
    obj = result["object"]
    return {"object_id": obj["object_id"], "version": obj["semantic_version"], "sha256": obj["canonical_sha256"]}


def test_skills_recipes_transformation_contract_and_resolution(tmp_path):
    app = PipelineApplication(tmp_path / "pipeline.sqlite3"); app.initialize()
    contract = app.skills.register_transformation_contract({
        "contract_id": "transform:source-led-short", "version": "1.0.0",
        "input_contract_ids": ["canonical_interview_source_package", "approved_final_script"],
        "output_contract_ids": ["video_edit_program"],
        "required_invariants": ["source_truth", "speaker_identity", "reaction_tail"],
        "allowed_transformation_classes": ["trim", "caption", "overlay"],
        "forbidden_transformations": ["invented_quote", "voice_replacement"],
        "evaluation_profile_refs": [r("evaluation")], "source_refs": [r("source")],
    }, idempotency_key="contract")
    skill = app.skills.register_skill({
        "skill_id": "skill:source-led-short", "version": "1.0.0", "title": "Source-led short",
        "purpose": "Preserve source expression while creating a bounded short.",
        "authority_owner": "atomic-harness-pipeline", "lifecycle_state": "VALIDATED",
        "category_ids": ["short_form_edited_video"], "format_profile_ids": ["format07_direct_coaching_a_roll"],
        "entry_condition_ids": ["source_package_ready", "final_script_approved"],
        "output_contract_ids": ["video_edit_program"], "allowed_tool_ids": ["ffmpeg", "remotion"],
        "forbidden_action_ids": ["semantic_rewrite", "source_voice_replacement"],
        "invariant_locks": ["source_truth", "reaction_tail"], "recipe_family_ids": ["source-led-short"],
        "source_refs": [r("source")], "evaluation_profile_refs": [r("evaluation")],
    }, idempotency_key="skill")
    recipe = app.skills.register_recipe({
        "recipe_id": "recipe:preserve-tail", "version": "1.0.0", "skill_id": skill["object"]["object_id"],
        "recipe_family_id": "source-led-short", "lifecycle_state": "VALIDATED",
        "primitive_coalition_ref": r("coalition"), "coalition_signature_ref": r("signature"),
        "edge_product_ref": r("edge"), "category_ids": ["short_form_edited_video"],
        "format_profile_ids": ["format07_direct_coaching_a_roll"], "failure_codes": ["REACTION_TAIL_LOST"],
        "applicability_tags": ["talking-head", "source-first"], "protected_properties": ["reaction_tail"],
        "operations": [{"tool_id": "ffmpeg", "tool_version": "development", "arguments": {"padding_ms": 120}, "preconditions": ["word_boundaries_available"], "expected_effect": "Preserve the reaction tail after the source phrase."}],
        "evidence_refs": [r("human-resolution")], "control_comparison_refs": [r("comparison")],
        "regression_case_refs": [r("regression")], "limitations": ["development evidence only"],
    }, idempotency_key="recipe")
    resolution = app.skills.resolve(
        skill_id=skill["object"]["object_id"], category_id="short_form_edited_video",
        format_profile_id="format07_direct_coaching_a_roll", failure_codes=["REACTION_TAIL_LOST"],
        applicability_tags=["talking-head", "source-first"], idempotency_key="resolve",
    )
    assert resolution["object"]["payload"]["selected_recipe_ids"] == [recipe["object"]["object_id"]]
    with pytest.raises(PipelineAuthorityError):
        app.skills.register_recipe({**recipe["object"]["payload"], "recipe_id": "recipe:bad", "lifecycle_state": "PRODUCTION"}, idempotency_key="bad")
    assert contract["object"]["payload"]["forbidden_transformations"] == ["invented_quote", "voice_replacement"]


def projection(identifier: str, *, source_kind: str, title: str, summary: str, category: str, contradicts=(), failed=False):
    return {
        "projection_id": identifier, "object_ref": r(f"object:{identifier}"), "source_kind": source_kind,
        "authority_state": "current", "lifecycle_state": "VALIDATED", "title": title, "summary": summary,
        "category_ids": [category], "format_profile_ids": ["format07_direct_coaching_a_roll"],
        "role_ids": ["composer"], "tags": ["source-fidelity", "reaction-tail"],
        "relationship_edges": [], "evidence_refs": [r(f"evidence:{identifier}")],
        "reaction_receipt_refs": [], "expression_moment_refs": [],
        "contradicts_ids": list(contradicts), "supersedes_ids": [], "failed_alternative": failed,
        "evidence_quality_micros": 800_000, "permitted_action_ids": ["compile_edl", "evaluate_render"],
        "content_sha256": canonical_sha256({"title": title, "summary": summary}),
    }


def test_authority_first_retrieval_includes_contradiction_and_failed_alternative(tmp_path):
    app = PipelineApplication(tmp_path / "pipeline.sqlite3"); app.initialize()
    app.retrieval.register_projection(projection("knowledge:skill", source_kind="skill", title="Source fidelity skill", summary="Preserve the source reaction tail.", category="short_form_edited_video", contradicts=["knowledge:contradiction"]), idempotency_key="k1")
    app.retrieval.register_projection(projection("knowledge:contradiction", source_kind="failure_precedent", title="Speed is not fidelity", summary="Faster pacing can destroy the expression moment.", category="short_form_edited_video"), idempotency_key="k2")
    app.retrieval.register_projection(projection("knowledge:failed", source_kind="failure_precedent", title="Overcompressed edit", summary="The reaction tail was removed.", category="short_form_edited_video", failed=True), idempotency_key="k3")
    app.retrieval.register_projection(projection("knowledge:other", source_kind="skill", title="Other category", summary="Irrelevant.", category="other"), idempotency_key="k4")
    result = app.retrieval.compile_capsule({
        "request_id": "request:1", "query_text": "preserve source reaction tail", "role_id": "composer",
        "category_id": "short_form_edited_video", "format_profile_id": "format07_direct_coaching_a_roll",
        "required_source_kinds": ["skill", "steering_recipe", "failure_precedent"], "required_tags": ["source-fidelity"],
        "required_action_ids": ["compile_edl"], "required_projection_ids": ["knowledge:skill"],
        "include_contradictions": True, "include_failed_alternatives": True, "budget_bytes": 20_000,
        "allowed_tool_ids": ["ffmpeg"], "forbidden_action_ids": ["semantic_rewrite"],
        "stopping_law_id": "minimum-complete-context", "source_package_ref": r("source"),
    }, idempotency_key="retrieve")
    assert result.capsule["authority_first"] is True
    assert {"knowledge:skill", "knowledge:contradiction", "knowledge:failed"}.issubset(set(result.receipt["selected_projection_ids"]))
    assert any(item["projection_id"] == "knowledge:other" for item in result.receipt["exclusions"])
    with pytest.raises(PipelineBudgetError):
        app.retrieval.compile_capsule({
            **result.receipt["request"], "request_id": "request:tiny", "budget_bytes": 1,
        }, idempotency_key="tiny")


def test_programmed_model_shadow_resolution_and_fallback(tmp_path):
    app = PipelineApplication(tmp_path / "pipeline.sqlite3"); app.initialize()
    artifact = app.programmed_models.register_artifact({
        "model_artifact_id": "model:tool-router", "version": "1.0.0", "artifact_ref": r("weights", "b"),
        "model_family": "small-tool-router", "architecture": "decoder-only", "parameter_count": 1_000_000_000,
        "quantization": "int8", "runtime_ids": ["local-cpu-reference"], "tokenizer_ref": r("tokenizer"),
        "training_dataset_refs": [r("training-data")], "evaluation_dataset_refs": [r("evaluation-data")],
        "applicability_envelope": {"category_ids": ["short_form_edited_video"], "format_profile_ids": ["format07_direct_coaching_a_roll"], "role_ids": ["composer"], "task_types": ["bounded_tool_routing"]},
        "lifecycle_state": "SHADOW", "limitations": ["no production promotion"], "source_authority_refs": [r("program-control")],
    }, idempotency_key="artifact")
    claim = app.programmed_models.register_claim({
        "claim_id": "claim:tool-router", "model_artifact_ref": obj_ref(artifact), "claim_type": "bounded_tool_routing",
        "lifecycle_state": "SHADOW", "applicability_envelope": artifact["object"]["payload"]["applicability_envelope"],
        "benchmark_ref": r("benchmark"), "evaluator_ref": r("evaluator"), "metric_name": "task_accuracy_micros",
        "threshold_micros": 800_000, "observed_micros": 900_000, "failure_limit_micros": 200_000,
        "fallback_mode": "DETERMINISTIC_OR_HUMAN", "limitations": ["shadow only"], "evidence_refs": [r("evidence")],
    }, idempotency_key="claim")
    program = app.programmed_models.register_program({
        "model_program_id": "program:tool-router", "version": "1.0.0", "claim_ref": obj_ref(claim),
        "input_contract_id": "tool-routing-request", "output_contract_id": "typed-tool-call",
        "skill_refs": [r("skill")], "steering_recipe_refs": [r("recipe")], "allowed_tool_ids": ["ffmpeg"],
        "forbidden_action_ids": ["semantic_rewrite"], "fallback_mode": "DETERMINISTIC_OR_HUMAN",
        "escalation_conditions": ["ambiguity", "hard_gate_failure"], "runtime_requirements": {"runtime_ids": ["local-cpu-reference"]},
        "lifecycle_state": "SHADOW",
    }, idempotency_key="program")
    resolved = app.programmed_models.resolve({
        "request_id": "resolve:1", "claim_type": "bounded_tool_routing", "category_id": "short_form_edited_video",
        "format_profile_id": "format07_direct_coaching_a_roll", "role_id": "composer", "task_type": "bounded_tool_routing",
        "available_runtime_ids": ["local-cpu-reference"], "maximum_parameter_count": 2_000_000_000,
        "required_tool_ids": ["ffmpeg"], "allowed_lifecycle_states": ["SHADOW"],
    }, idempotency_key="resolve")
    assert resolved["object"]["payload"]["decision"] == "RESOLVED_SHADOW_OR_VALIDATED"
    fallback = app.programmed_models.resolve({
        "request_id": "resolve:2", "claim_type": "bounded_tool_routing", "category_id": "other",
        "format_profile_id": "other", "role_id": "composer", "task_type": "bounded_tool_routing",
        "available_runtime_ids": ["local-cpu-reference"], "maximum_parameter_count": 2_000_000_000,
        "required_tool_ids": ["ffmpeg"], "allowed_lifecycle_states": ["SHADOW"],
    }, idempotency_key="fallback")
    assert fallback["object"]["payload"]["decision"] == "FALLBACK_REQUIRED"


def test_cross_derivative_continuity_and_backup_restore(tmp_path):
    app = PipelineApplication(tmp_path / "pipeline.sqlite3"); app.initialize()
    source = r("source")
    continuity = app.continuity.compile(
        source_package_ref=source, semantic_production_package_ref=r("semantic"), final_script_ref=r("script"),
        activation_transfer_contract_ref=r("transfer"),
        derivatives=[{
            "derivative_id": "short", "derivative_type": "SOURCE_LED_SHORT", "artifact_ref": r("video"),
            "source_package_ref": source,
            "source_span_refs": [{"source_ref": source, "start_ms": 0, "end_ms": 1000, "speaker_id": "speaker:1", "transcript_sha256": "c" * 64}],
            "semantic_program_ref": r("program"), "final_script_ref": r("script"), "transfer_contract_ref": r("transfer"),
            "evaluation_refs": [r("evaluation")], "consumption_state": "ACKNOWLEDGED",
        }], usage_records=[], evaluation_refs=[r("evaluation")], idempotency_key="continuity",
    )
    assert continuity["object"]["payload"]["result"] == "PASS"
    backup = app.operations.backup(tmp_path / "backup.sqlite3")
    restore = app.operations.restore_rehearsal(tmp_path / "backup.sqlite3", tmp_path / "restored.sqlite3")
    assert backup["integrity"] == "ok" and restore["result"] == "PASS"
