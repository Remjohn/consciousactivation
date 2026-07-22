"""DSPy-style pre-induction compiler and evaluator for TS-CMF-026."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from ccp_studio.contracts.context import ContextPremise, InterviewerResonanceContext
from ccp_studio.contracts.matrix import MatrixOfEdgingBrief
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.pre_induction import (
    InductionBridge,
    InductionRiskLevel,
    PreInductionPlan,
    PreInductionPlanStatus,
    PreInductionQuestion,
    QuestionAvoidanceRule,
)


@dataclass(frozen=True)
class PreInductionPlanCompiler:
    compiler_version: str = "pre-induction-plan-v1"

    def predict(
        self,
        *,
        organization_id,
        brand_id,
        guest_id,
        operator_id,
        context_premise: ContextPremise,
        resonance_context: InterviewerResonanceContext | None,
        matrix_brief: MatrixOfEdgingBrief,
    ) -> PreInductionPlan:
        now = utc_now()
        first_edge = matrix_brief.edge_products[0]
        evidence_ids = list(dict.fromkeys([*context_premise.evidence_ids, *matrix_brief.tension_sites[0].evidence_ids]))
        curiosity = (
            resonance_context.authentic_curiosity[0]
            if resonance_context and resonance_context.authentic_curiosity
            else "Which sourced scene still feels alive enough to ask about?"
        )
        opening_state = resonance_context.opening_state if resonance_context else "curious, grounded, source-led"
        question = PreInductionQuestion(
            schema_version="cmf.pre_induction_question.v1",
            question_id=uuid4(),
            natural_question="When did this pressure become real enough that advice was no longer enough?",
            authentic_curiosity=curiosity,
            first_line_anchor_options=[
                "The first time I felt that pressure, I remember...",
                "What people do not see about this is...",
                "The real cost was not the method, it was...",
            ],
            depth_anchor="What did that moment cost before it became something you could teach?",
            centroid_risk=InductionRiskLevel.low,
            manipulation_risk=InductionRiskLevel.low,
            rationale_id=None,
            evidence_ids=evidence_ids,
            matrix_edge_product_id=first_edge.edge_product_id,
        )
        bridges = [
            InductionBridge(
                schema_version="cmf.induction_bridge.v1",
                bridge_id=uuid4(),
                emotional_bridge=(
                    resonance_context.emotional_bridges[0]
                    if resonance_context and resonance_context.emotional_bridges
                    else "Share only a small reflection that is true for the Operator."
                ),
                guest_specific_resonance=context_premise.guest_implication,
                matrix_edge_product_id=first_edge.edge_product_id,
                evidence_ids=evidence_ids,
            )
        ]
        avoid_rules = [
            QuestionAvoidanceRule(
                schema_version="cmf.question_avoidance_rule.v1",
                rule_id=uuid4(),
                reason=(
                    resonance_context.questions_to_avoid[0]
                    if resonance_context and resonance_context.questions_to_avoid
                    else "Do not assert unverified psychology."
                ),
                evidence_ids=evidence_ids,
                safer_route="Ask what the guest remembers, not what the system believes they felt.",
            ),
            QuestionAvoidanceRule(
                schema_version="cmf.question_avoidance_rule.v1",
                rule_id=uuid4(),
                reason="Do not script the landing; landing remains open and is evaluated later.",
                evidence_ids=evidence_ids,
                safer_route="Offer a first-line anchor and depth constraint, then let the guest complete it.",
            ),
        ]
        return PreInductionPlan(
            schema_version="cmf.pre_induction_plan.v1",
            pre_induction_plan_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            guest_id=guest_id,
            operator_id=operator_id,
            context_premise_id=context_premise.context_premise_id,
            matrix_brief_id=matrix_brief.matrix_brief_id,
            resonance_context_id=resonance_context.resonance_context_id if resonance_context else None,
            opening_state=opening_state,
            bridges=bridges,
            questions_to_avoid=avoid_rules,
            planned_questions=[question],
            status=PreInductionPlanStatus.draft,
            created_at=now,
            updated_at=now,
        )


@dataclass(frozen=True)
class PreInductionEvaluator:
    generic_markers: tuple[str, ...] = (
        "tell me about your journey",
        "what is your story",
        "share your thoughts",
        "how do you feel about content",
    )
    manipulation_markers: tuple[str, ...] = (
        "say that",
        "end by saying",
        "make the guest feel",
        "make them cry",
        "admit that",
        "perform",
        "pretend",
    )

    def evaluate_question(self, question: PreInductionQuestion) -> tuple[InductionRiskLevel, InductionRiskLevel]:
        lowered = question.natural_question.lower()
        centroid = (
            InductionRiskLevel.review
            if any(marker in lowered for marker in self.generic_markers)
            else InductionRiskLevel.low
        )
        manipulation = (
            InductionRiskLevel.blocked
            if any(marker in lowered for marker in self.manipulation_markers)
            else InductionRiskLevel.low
        )
        if not question.evidence_ids:
            centroid = InductionRiskLevel.review
        return centroid, manipulation

    def risk_scores(self, plan: PreInductionPlan) -> dict[str, float]:
        centroid_review = sum(1 for item in plan.planned_questions if item.centroid_risk == InductionRiskLevel.review)
        manipulation_blocked = sum(1 for item in plan.planned_questions if item.manipulation_risk == InductionRiskLevel.blocked)
        total = len(plan.planned_questions) or 1
        return {
            "centroid_risk": centroid_review / total,
            "manipulation_risk": manipulation_blocked / total,
            "evidence_coverage": 1.0 if all(item.evidence_ids for item in plan.planned_questions) else 0.0,
            "operator_edit_count": float(len(plan.operator_edit_ids)),
        }
