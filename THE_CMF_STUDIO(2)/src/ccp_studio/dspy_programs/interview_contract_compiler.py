"""DSPy-style Interview Asset Contract compiler for TS-CMF-027."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from ccp_studio.contracts.interview_contracts import (
    ContractRouteTarget,
    ExpressionState,
    FirstLineAnchorSet,
    InterviewAssetContract,
    InterviewContractStatus,
    InterviewDeck,
    InterviewPlanEvaluationScores,
    RepairFollowups,
)
from ccp_studio.contracts.matrix import MatrixOfEdgingBrief
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.pre_induction import PreInductionPlan


EXPRESSION_STATE_VALUES = {item.value for item in ExpressionState}


@dataclass(frozen=True)
class InterviewAssetContractCompiler:
    compiler_version: str = "interview-asset-contract-v1"

    def compile_contracts(
        self,
        *,
        organization_id,
        brand_id,
        guest_id,
        pre_induction_plan: PreInductionPlan,
        matrix_brief: MatrixOfEdgingBrief,
        force_confusion: bool = False,
        force_generic: bool = False,
    ) -> list[InterviewAssetContract]:
        now = utc_now()
        contracts: list[InterviewAssetContract] = []
        edge = matrix_brief.edge_products[0]
        for question in pre_induction_plan.planned_questions:
            route_target = ContractRouteTarget(
                schema_version="cmf.contract_route_target.v1",
                core_archetype_ref="vulnerability" if force_confusion else "archetype.conceptual_contrast.v1",
                asset_derivative_refs=[] if force_generic else ["derivative.identity_mirror.v1", "derivative.quote_to_question.v1"],
                meme_mechanism_refs=[],
                reaction_archetype_refs=["reaction.validation_reaction.v1"],
                cmf_render_mode_refs=[] if force_generic else ["cmf_route.personal_brand_commentary.v1", "cmf_route.paper_cutout_explainer.v1"],
                guest_asset_pack_potential=["video", "carousel", "poll_visual"],
            )
            contracts.append(
                InterviewAssetContract(
                    schema_version="cmf.interview_asset_contract.v1",
                    contract_id=uuid4(),
                    organization_id=organization_id,
                    brand_id=brand_id,
                    guest_id=guest_id,
                    operator_id=pre_induction_plan.operator_id,
                    pre_induction_plan_id=pre_induction_plan.pre_induction_plan_id,
                    question_id=question.question_id,
                    main_question="Tell me about your journey." if force_generic else question.natural_question,
                    target_expression_states=[
                        ExpressionState.cinematic,
                        ExpressionState.vulnerability,
                        ExpressionState.meaning,
                    ],
                    route_target=route_target,
                    edge_product_id=edge.edge_product_id,
                    first_line_anchors=FirstLineAnchorSet(
                        schema_version="cmf.first_line_anchor_set.v1",
                        cinematic=question.first_line_anchor_options[0] if question.first_line_anchor_options else None,
                        emotional=question.first_line_anchor_options[1] if len(question.first_line_anchor_options) > 1 else None,
                        reels_hook=question.first_line_anchor_options[2] if len(question.first_line_anchor_options) > 2 else None,
                    ),
                    depth_anchor=question.depth_anchor or "What did it cost before it became something you could teach?",
                    expected_source_material=["source scene", "emotional cost", "specific contradiction"],
                    clip_start_rule="start_at_selected_first_line_anchor",
                    depth_eval_rule="answer_must_contain_specific_cost_or_tension",
                    landing_eval_targets=[
                        "principle_landing",
                        "emotional_recognition_landing",
                        "question_landing",
                    ],
                    repair_followups=RepairFollowups(
                        schema_version="cmf.repair_followups.v1",
                        too_historical="Before the history, what did that moment do to you?",
                        too_abstract="Give me one image or scene, not the idea yet.",
                        too_flat="Where is the cost or contradiction in that answer?",
                        not_clip_ready="Restart from the first-line anchor and keep the same truth.",
                    ),
                    evidence_ids=[] if force_generic else question.evidence_ids,
                    matrix_brief_id=matrix_brief.matrix_brief_id,
                    induction_rationale_ids=[question.rationale_id] if question.rationale_id else [],
                    status=InterviewContractStatus.draft,
                    created_at=now,
                    updated_at=now,
                )
            )
        return contracts

    def compile_deck(
        self,
        *,
        organization_id,
        brand_id,
        guest_id,
        pre_induction_plan: PreInductionPlan,
        matrix_brief: MatrixOfEdgingBrief,
        contracts: list[InterviewAssetContract],
    ) -> InterviewDeck:
        now = utc_now()
        return InterviewDeck(
            schema_version="cmf.interview_deck.v1",
            interview_deck_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            guest_id=guest_id,
            pre_induction_plan_id=pre_induction_plan.pre_induction_plan_id,
            matrix_brief_id=matrix_brief.matrix_brief_id,
            contract_ids=[contract.contract_id for contract in contracts],
            status=InterviewContractStatus.draft,
            created_at=now,
            updated_at=now,
        )


@dataclass(frozen=True)
class InterviewPlanQualityGate:
    valid_core_archetypes: frozenset[str] = frozenset(
        {
            "archetype.conceptual_contrast.v1",
            "archetype.transformation_story.v1",
            "archetype.witness_story.v1",
            "archetype.core_educator_explainer.v1",
            "archetype.audience_mirror_quiz.v1",
        }
    )
    valid_derivatives: frozenset[str] = frozenset(
        {
            "derivative.identity_mirror.v1",
            "derivative.quote_to_question.v1",
            "derivative.tension_poll.v1",
            "derivative.scene_to_principle.v1",
        }
    )
    valid_cmf_routes: frozenset[str] = frozenset(
        {
            "cmf_route.personal_brand_commentary.v1",
            "cmf_route.paper_cutout_explainer.v1",
            "cmf_route.carousel_static_motion.v1",
            "cmf_route.cinematic_story_commentary.v1",
        }
    )

    def evaluate(self, contracts: list[InterviewAssetContract]) -> tuple[InterviewPlanEvaluationScores, list[str], bool]:
        failures: list[str] = []
        total = len(contracts) or 1
        evidence_complete = sum(1 for contract in contracts if contract.evidence_ids) / total
        routeable = sum(1 for contract in contracts if self._routeable(contract)) / total
        specific = sum(1 for contract in contracts if not self._generic(contract)) / total
        separated = sum(1 for contract in contracts if self._separated(contract)) / total
        collision = sum(1 for contract in contracts if contract.edge_product_id and contract.depth_anchor) / total
        if evidence_complete < 1:
            failures.append("CONTRACT_SATURATION_REQUIRED")
        if collision < 1:
            failures.append("CONTRACT_COLLISION_REQUIRED")
        if specific < 1:
            failures.append("CONTRACT_SPECIFICITY_FAILED")
        if routeable < 1:
            failures.append("CONTRACT_ROUTEABILITY_FAILED")
        if separated < 1:
            failures.append("EXPRESSION_ARCHETYPE_CONFUSION")
        if any("newsletter" in item.lower() for contract in contracts for item in contract.route_target.guest_asset_pack_potential):
            failures.append("UNSUPPORTED_CONTENT_FORMAT")
        scores = InterviewPlanEvaluationScores(
            schema_version="cmf.interview_plan_evaluation_scores.v1",
            saturation_score=evidence_complete,
            collision_strength_score=collision,
            specificity_score=specific,
            routeability_score=routeable,
            expression_archetype_separation_score=separated,
        )
        return scores, list(dict.fromkeys(failures)), not failures

    def _routeable(self, contract: InterviewAssetContract) -> bool:
        return (
            contract.route_target.core_archetype_ref in self.valid_core_archetypes
            and bool(set(contract.route_target.asset_derivative_refs).intersection(self.valid_derivatives))
            and bool(set(contract.route_target.cmf_render_mode_refs).intersection(self.valid_cmf_routes))
        )

    @staticmethod
    def _generic(contract: InterviewAssetContract) -> bool:
        lowered = contract.main_question.lower()
        return any(term in lowered for term in ["tell me about your journey", "share your thoughts", "content pillars"])

    @staticmethod
    def _separated(contract: InterviewAssetContract) -> bool:
        return contract.route_target.core_archetype_ref not in EXPRESSION_STATE_VALUES
