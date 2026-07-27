from __future__ import annotations

import json
import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.doctrine_evals import DoctrineEvalDecision, DoctrineEvalTargetInput
from ccp_studio.contracts.evaluation_receipts import EvaluationCategory, EvaluationDecision, EvaluationObjectType
from ccp_studio.services.doctrine_evaluation_service import (
    DoctrineEvaluationService,
    canonical_acting_library_doctrine_eval_definition,
    canonical_brand_genesis_doctrine_eval_definition,
    canonical_doctrine_eval_definitions,
    canonical_interview_brief_doctrine_eval_definition,
    canonical_papercut_rig_doctrine_eval_definition,
)


def _target(**overrides) -> DoctrineEvalTargetInput:
    definition = canonical_interview_brief_doctrine_eval_definition()
    values = {
        "organization_id": uuid4(),
        "brand_id": uuid4(),
        "object_type": EvaluationObjectType.interview_brief,
        "object_id": uuid4(),
        "object_hash": "sha256-conscious-interview-brief",
        "actor_id": uuid4(),
        "pipeline_stage": "conscious_interview_brief",
        "route_refs": ["archetype.conceptual_contrast", "cmf.personal_brand_commentary"],
        "doctrine_refs": list(definition.source_doctrine_refs),
        "evidence_routes": {
            "cral_scre_signal": ["cral:M1-relevant", "cral:M4-resonant"],
            "audience_conversation": ["audience-comments:identity-resistance"],
            "context_premise": ["context-premise:approved"],
            "audience_deep_trigger_map": ["trigger-map:approved"],
            "interviewer_resonance": ["interviewer-resonance:operator-bridge"],
            "matrix_of_edging": ["matrix:edge-product:recognition-exposure"],
            "primitive_registry": [
                "registries/primitives/meaning_plane/narrative_structure/PRM-STR-001.yaml",
                "registries/primitives/experience_plane/trigger_timing/EXP-TRG-001.yaml",
            ],
            "first_line_anchors": ["anchors:first-line:cinematic-emotional-reels"],
            "depth_anchor": ["anchors:depth:cost-and-tension"],
            "landing_eval_targets": ["landing:emotional-recognition", "landing:principle"],
            "repair_followups": ["repair:too-historical", "repair:too-abstract"],
            "route_target": ["route:archetype-derivative-cmf-render"],
            "hard_negative": ["failure:topic-first-question"],
        },
        "primitive_families": ["STR", "TRG", "PSY", "PRS", "FBK"],
        "primitive_refs": [
            "PRM-STR-001",
            "EXP-TRG-001",
            "PRM-PSY-001",
            "PRM-PRS-001",
            "EXP-FBK-001",
        ],
        "expected_coalition_refs": ["coalition:recognition-exposure-edge"],
        "expected_edge_product_refs": ["edge-product:question-that-causes-lived-scene"],
        "hard_negative_refs": ["failure:generic-biographical-question"],
    }
    values.update(overrides)
    return DoctrineEvalTargetInput(**values)


def _target_for_definition(definition, object_type, pipeline_stage, primitive_families) -> DoctrineEvalTargetInput:
    return DoctrineEvalTargetInput(
        organization_id=uuid4(),
        brand_id=uuid4(),
        object_type=object_type,
        object_id=uuid4(),
        object_hash=f"sha256-{definition.eval_definition_id.lower()}",
        actor_id=uuid4(),
        pipeline_stage=pipeline_stage,
        doctrine_refs=list(definition.source_doctrine_refs),
        evidence_routes={requirement.route: [f"{requirement.route}:approved"] for requirement in definition.evidence_requirements},
        primitive_families=list(primitive_families),
        primitive_refs=[f"PRM-{family}-001" for family in primitive_families],
    )


def test_canonical_interview_brief_eval_definition_carries_doctrine_and_primitive_obligations():
    definition = canonical_interview_brief_doctrine_eval_definition()

    assert "THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md" in definition.source_doctrine_refs
    assert "THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md" in definition.source_doctrine_refs
    assert "THE CMF STUDIO/Claude Ntahuga Interview Deck — V4.docx.md" in definition.source_doctrine_refs
    assert "THE CMF STUDIO/reference/conscious-rivers/docs/prd/modules/PRD_08_Conscious_Primitives.md" in definition.source_doctrine_refs
    assert EvaluationCategory.doctrine_alignment in definition.required_categories
    assert EvaluationCategory.primitive_registry_fidelity in definition.required_categories
    assert EvaluationCategory.anchor_contract_integrity in definition.required_categories
    assert {item.primitive_family for item in definition.primitive_obligations} == {"STR", "TRG", "PSY", "PRS", "FBK"}
    assert {item.route for item in definition.evidence_requirements} >= {
        "cral_scre_signal",
        "context_premise",
        "interviewer_resonance",
        "matrix_of_edging",
        "first_line_anchors",
        "depth_anchor",
        "hard_negative",
    }


def test_doctrine_eval_registry_includes_brand_genesis_acting_and_papercut_gates():
    definitions = {definition.eval_definition_id: definition for definition in canonical_doctrine_eval_definitions()}

    assert set(definitions) == {
        "EVL-DOCTRINE-IAC-001",
        "EVL-DOCTRINE-BGN-001",
        "EVL-DOCTRINE-ACT-064-001",
        "EVL-DOCTRINE-PPR-RIG-001",
    }
    assert EvaluationCategory.brand_genesis_completeness in definitions["EVL-DOCTRINE-BGN-001"].required_categories
    assert EvaluationCategory.acting_library_coverage in definitions["EVL-DOCTRINE-ACT-064-001"].required_categories
    assert EvaluationCategory.papercut_rig_integrity in definitions["EVL-DOCTRINE-PPR-RIG-001"].required_categories
    assert EvaluationCategory.animation_readiness in definitions["EVL-DOCTRINE-PPR-RIG-001"].required_categories
    assert EvaluationCategory.micro_semiotic_integrity in definitions["EVL-DOCTRINE-BGN-001"].required_categories


def test_doctrine_eval_registry_json_files_match_runtime_definitions():
    registry_dir = Path(__file__).resolve().parents[2] / "registries" / "evals" / "doctrine"
    files = sorted(registry_dir.glob("*.json"))
    runtime_definitions = {definition.eval_definition_id: definition for definition in canonical_doctrine_eval_definitions()}

    assert {json.loads(path.read_text(encoding="utf-8"))["eval_definition_id"] for path in files} == set(runtime_definitions)
    for path in files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        definition = runtime_definitions[payload["eval_definition_id"]]
        assert payload["required_categories"] == [category.value for category in definition.required_categories]
        assert payload["object_types"] == [object_type.value for object_type in definition.object_types]
        assert payload["pipeline_stages"] == definition.pipeline_stages
        assert payload["source_doctrine_refs"] == definition.source_doctrine_refs
        assert payload["evidence_routes"] == [requirement.route for requirement in definition.evidence_requirements]
        assert [item["primitive_family"] for item in payload["primitive_obligations"]] == [
            obligation.primitive_family for obligation in definition.primitive_obligations
        ]


def test_complete_doctrine_and_primitive_evidence_passes_evaluation_receipt():
    service = DoctrineEvaluationService()
    target = _target()

    selection = service.select_definition(target)
    receipt = service.evaluate_interview_brief_doctrine(target)

    assert selection.decision == DoctrineEvalDecision.selected
    assert receipt.object_type == EvaluationObjectType.interview_brief
    assert receipt.decision == EvaluationDecision.passes_for_human_review
    assert {score.category for score in receipt.scores} == set(EvaluationCategory)
    assert not receipt.hard_failures
    assert any(score.category == EvaluationCategory.doctrine_alignment for score in receipt.scores)
    assert any(score.category == EvaluationCategory.primitive_registry_fidelity for score in receipt.scores)


def test_complete_brand_genesis_doctrine_evidence_passes_evaluation_receipt():
    definition = canonical_brand_genesis_doctrine_eval_definition()
    service = DoctrineEvaluationService()
    target = _target_for_definition(
        definition,
        EvaluationObjectType.brand_genesis_session,
        "brand_genesis",
        ["IDN", "AUD", "VOI", "VSG", "SAF"],
    )

    selection = service.select_definition(target)
    receipt = service.evaluate_doctrine(target)

    assert selection.decision == DoctrineEvalDecision.selected
    assert receipt.decision == EvaluationDecision.passes_for_human_review
    assert receipt.object_type == EvaluationObjectType.brand_genesis_session


def test_missing_brand_genesis_substrate_blocks_context_lock():
    definition = canonical_brand_genesis_doctrine_eval_definition()
    service = DoctrineEvaluationService()
    target = _target_for_definition(
        definition,
        EvaluationObjectType.brand_context_version,
        "brand_context_lock",
        ["IDN"],
    ).model_copy(
        update={
            "evidence_routes": {
                "client_intake": ["client-intake:typed"],
                "consent_record": ["consent:valid"],
                "identity_pack": ["identity-pack:v1"],
            },
            "primitive_families": ["IDN"],
            "primitive_refs": ["PRM-IDN-001"],
        }
    )

    selection = service.select_definition(target)
    receipt = service.evaluate_doctrine(target)

    assert selection.decision == DoctrineEvalDecision.blocked
    assert "acting_library_plan" in selection.missing_evidence_routes
    assert "papercut_rig_plan" in selection.missing_evidence_routes
    assert "micro_semiotic_anchor_library" in selection.missing_evidence_routes
    assert {"AUD", "VOI", "VSG", "SAF"} <= set(selection.missing_primitive_families)
    assert receipt.decision == EvaluationDecision.blocked
    assert {failure.category for failure in receipt.hard_failures} >= {
        EvaluationCategory.acting_library_coverage,
        EvaluationCategory.papercut_rig_integrity,
        EvaluationCategory.micro_semiotic_integrity,
        EvaluationCategory.primitive_registry_fidelity,
    }


def test_incomplete_64_state_acting_library_blocks_lock():
    definition = canonical_acting_library_doctrine_eval_definition()
    service = DoctrineEvaluationService()
    target = _target_for_definition(
        definition,
        EvaluationObjectType.acting_library,
        "acting_library_review",
        ["ACT", "IDN", "NEG", "VSG", "SAF"],
    ).model_copy(
        update={
            "evidence_routes": {
                "identity_pack": ["identity-pack:v1"],
                "human_approval_before_generation": ["approval:identity-summary"],
                "cell_metadata": ["cell-metadata:partial"],
            }
        }
    )

    selection = service.select_definition(target)
    receipt = service.evaluate_doctrine(target)

    assert selection.decision == DoctrineEvalDecision.blocked
    assert "acting_state_matrix_64" in selection.missing_evidence_routes
    assert "provider_receipts_64" in selection.missing_evidence_routes
    assert "library_lock_receipt" in selection.missing_evidence_routes
    assert receipt.decision == EvaluationDecision.blocked
    assert {failure.category for failure in receipt.hard_failures} >= {
        EvaluationCategory.acting_library_coverage,
        EvaluationCategory.asset_generation_policy,
        EvaluationCategory.evaluation_target_coverage,
    }


def test_papercut_rig_missing_manifest_preview_and_editor_independence_blocks_approval():
    definition = canonical_papercut_rig_doctrine_eval_definition()
    service = DoctrineEvaluationService()
    target = _target_for_definition(
        definition,
        EvaluationObjectType.rig_manifest,
        "rig_review",
        ["RIG", "MOT", "VSG", "MSA", "SAF"],
    ).model_copy(
        update={
            "evidence_routes": {
                "approved_acting_library_version": ["acting-library:v1"],
                "required_avatar_asset_set": ["avatar-assets:partial"],
                "papercut_style_constitution": ["style:editorial-2-5d"],
                "composition_json_structure": ["composition-json:ideogram4"],
            }
        }
    )

    selection = service.select_definition(target)
    receipt = service.evaluate_doctrine(target)

    assert selection.decision == DoctrineEvalDecision.blocked
    assert "rig_manifest" in selection.missing_evidence_routes
    assert "editor_independence" in selection.missing_evidence_routes
    assert "preview_tests" in selection.missing_evidence_routes
    assert "micro_semiotic_anchor_refs" in selection.missing_evidence_routes
    assert receipt.decision == EvaluationDecision.blocked
    assert {failure.category for failure in receipt.hard_failures} >= {
        EvaluationCategory.papercut_rig_integrity,
        EvaluationCategory.animation_readiness,
        EvaluationCategory.micro_semiotic_integrity,
    }


def test_missing_doctrine_sources_and_primitive_evidence_block_interview_brief_approval():
    service = DoctrineEvaluationService()
    target = _target(
        doctrine_refs=["THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md"],
        evidence_routes={
            "context_premise": ["context-premise:approved"],
            "route_target": ["route:archetype-derivative-cmf-render"],
        },
        primitive_families=["STR"],
        primitive_refs=["PRM-STR-001"],
    )

    selection = service.select_definition(target)
    receipt = service.evaluate_interview_brief_doctrine(target)
    read_model = service.evaluation_service.build_review_read_model(receipt.evaluation_receipt_id)

    assert selection.decision == DoctrineEvalDecision.blocked
    assert "cral_scre_signal" in selection.missing_evidence_routes
    assert "first_line_anchors" in selection.missing_evidence_routes
    assert "depth_anchor" in selection.missing_evidence_routes
    assert {"TRG", "PSY", "PRS", "FBK"} <= set(selection.missing_primitive_families)
    assert "THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md" in selection.missing_source_doctrine_refs
    assert receipt.decision == EvaluationDecision.blocked
    assert {failure.category for failure in receipt.hard_failures} >= {
        EvaluationCategory.doctrine_alignment,
        EvaluationCategory.primitive_registry_fidelity,
        EvaluationCategory.anchor_contract_integrity,
        EvaluationCategory.ccf_orchestration_lineage,
    }
    assert read_model.approval_blocker_ids
    assert any("first_line_anchors" in failure.message for failure in receipt.hard_failures)
