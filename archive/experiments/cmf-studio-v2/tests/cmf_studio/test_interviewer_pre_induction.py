from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.context import ContextArtifactKind  # noqa: E402
from ccp_studio.contracts.orchestration import utc_now  # noqa: E402
from ccp_studio.contracts.pre_induction import InductionRiskLevel, PreInductionPlanStatus  # noqa: E402
from ccp_studio.contracts.research import EvidenceCitation, SourceRole, TemporalSensitivity  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.context_compilation_service import ContextCompilationService  # noqa: E402
from ccp_studio.services.matrix_service import MatrixService  # noqa: E402
from ccp_studio.services.pre_induction_service import (  # noqa: E402
    PreInductionService,
    PreInductionServiceError,
    register_pre_induction_command_handlers,
)
from ccp_studio.services.research_service import ResearchService  # noqa: E402
from ccp_studio.workflows.interview_preparation import InterviewPreparationWorkflow  # noqa: E402


def _citation(title="Pre-induction source", source_hash="sha256-pre-induction"):
    return EvidenceCitation(
        schema_version="cmf.evidence_citation.v1",
        citation_id=uuid4(),
        uri="https://example.com/pre-induction-source",
        title=title,
        retrieved_at=utc_now(),
        quoted_span_ref="p3",
        source_hash=source_hash,
    )


def _session_plan():
    research = ResearchService()
    organization_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    guest_id = uuid4()
    field = research.create_field(
        organization_id=organization_id,
        brand_id=brand_id,
        guest_id=guest_id,
        objective="Prepare pre-induction for exposure risk interview.",
        source_scope=["primary source", "audience reality", "CRAL"],
        created_by_actor_id=actor_id,
    )
    evidence = [
        research.attach_evidence(
            organization_id=organization_id,
            brand_id=brand_id,
            research_field_id=field.research_field_id,
            claim="The guest frames recording resistance as exposure risk rather than laziness.",
            source_role=SourceRole.primary_source,
            citations=[_citation("Guest source", "sha256-guest")],
            confidence=0.91,
            temporal_sensitivity=TemporalSensitivity.low,
            provenance_summary="Primary source.",
            contradiction_notes=["laziness frame vs exposure risk"],
            primitive_family_hints=["vulnerable-specificity"],
            created_by_actor_id=actor_id,
        ),
        research.attach_evidence(
            organization_id=organization_id,
            brand_id=brand_id,
            research_field_id=field.research_field_id,
            claim="Audience comments show founders need practical language before mindset claims.",
            source_role=SourceRole.audience_signal,
            citations=[_citation("Audience source", "sha256-audience")],
            confidence=0.87,
            temporal_sensitivity=TemporalSensitivity.medium,
            freshness_due_at=utc_now().replace(year=utc_now().year + 1),
            provenance_summary="Audience source.",
            contradiction_notes=["practical need vs abstract phrasing"],
            primitive_family_hints=["what-is-what-could-be"],
            created_by_actor_id=actor_id,
        ),
        research.attach_evidence(
            organization_id=organization_id,
            brand_id=brand_id,
            research_field_id=field.research_field_id,
            claim="CRAL pressure identifies competence versus visibility avoidance.",
            source_role=SourceRole.cral_signal,
            citations=[_citation("CRAL source", "sha256-cral")],
            confidence=0.86,
            temporal_sensitivity=TemporalSensitivity.low,
            provenance_summary="CRAL source.",
            contradiction_notes=["competence vs visibility avoidance"],
            primitive_family_hints=["edge-pressure"],
            created_by_actor_id=actor_id,
        ),
    ]
    for item in evidence:
        research.validate_evidence_provenance(
            organization_id=organization_id,
            brand_id=brand_id,
            evidence_id=item.evidence_id,
            validator_actor_id=actor_id,
        )
        research.approve_evidence(
            organization_id=organization_id,
            brand_id=brand_id,
            evidence_id=item.evidence_id,
            validator_actor_id=actor_id,
        )
    context_service = ContextCompilationService(research_service=research)
    context_receipt = context_service.compile_context_artifacts(
        organization_id=organization_id,
        brand_id=brand_id,
        research_field_id=field.research_field_id,
        evidence_ids=[item.evidence_id for item in evidence],
        operator_id=actor_id,
        audience_scope="Expression-latent founders",
        compiler_actor_id=actor_id,
        guest_id=guest_id,
        operator_notes=["The exposure-risk contradiction feels alive."],
    )
    for kind in [
        ContextArtifactKind.guest_dossier,
        ContextArtifactKind.audience_reality_brief,
        ContextArtifactKind.audience_deep_trigger_map,
        ContextArtifactKind.context_premise,
        ContextArtifactKind.interviewer_resonance_context,
    ]:
        context_service.approve_context_artifact(
            organization_id=organization_id,
            brand_id=brand_id,
            artifact_kind=kind,
            artifact_id=context_receipt.output_ids[kind],
            reviewer_actor_id=actor_id,
        )
    matrix_service = MatrixService(context_service=context_service)
    matrix = matrix_service.compile_matrix_brief(
        organization_id=organization_id,
        brand_id=brand_id,
        guest_dossier_id=context_receipt.output_ids[ContextArtifactKind.guest_dossier],
        audience_reality_brief_id=context_receipt.output_ids[ContextArtifactKind.audience_reality_brief],
        context_premise_id=context_receipt.output_ids[ContextArtifactKind.context_premise],
        trigger_map_id=context_receipt.output_ids[ContextArtifactKind.audience_deep_trigger_map],
        compiled_by_actor_id=actor_id,
    )
    matrix_service.evaluate_matrix_collision(
        organization_id=organization_id,
        brand_id=brand_id,
        matrix_brief_id=matrix.matrix_brief_id,
        evaluator_actor_id=actor_id,
    )
    matrix = matrix_service.approve_matrix_brief(
        organization_id=organization_id,
        brand_id=brand_id,
        matrix_brief_id=matrix.matrix_brief_id,
        reviewer_actor_id=actor_id,
    )
    service = PreInductionService(context_service=context_service, matrix_service=matrix_service)
    plan = service.compile_pre_induction_plan(
        organization_id=organization_id,
        brand_id=brand_id,
        guest_id=guest_id,
        operator_id=actor_id,
        context_premise_id=context_receipt.output_ids[ContextArtifactKind.context_premise],
        matrix_brief_id=matrix.matrix_brief_id,
        resonance_context_id=context_receipt.output_ids[ContextArtifactKind.interviewer_resonance_context],
        compiled_by_actor_id=actor_id,
    )
    return service, organization_id, brand_id, actor_id, guest_id, context_receipt, matrix, plan


def test_operator_sees_curiosity_bridges_avoid_list_resonance_and_opening_state():
    service, _org_id, _brand_id, _actor_id, _guest_id, _context_receipt, _matrix, plan = _session_plan()

    assert plan.opening_state == "curious, grounded, source-led"
    assert plan.bridges[0].emotional_bridge
    assert plan.bridges[0].guest_specific_resonance
    assert plan.questions_to_avoid
    assert plan.planned_questions[0].authentic_curiosity == "The exposure-risk contradiction feels alive."
    assert next(iter(service.repository.receipts.values())).decision_code == "PRE_INDUCTION_PLAN_COMPILED"


def test_centroid_safe_question_is_flagged_with_collision_bearing_route():
    service, org_id, brand_id, actor_id, _guest_id, _context_receipt, _matrix, plan = _session_plan()
    question = plan.planned_questions[0].model_copy(
        update={"natural_question": "Tell me about your journey and share your thoughts."}
    )
    service.repository.put_plan(plan.model_copy(update={"planned_questions": [question]}))

    receipt = service.evaluate_pre_induction_plan(
        organization_id=org_id,
        brand_id=brand_id,
        pre_induction_plan_id=plan.pre_induction_plan_id,
        evaluator_actor_id=actor_id,
    )
    evaluated = service.repository.plans[plan.pre_induction_plan_id]

    assert evaluated.planned_questions[0].centroid_risk == InductionRiskLevel.review
    assert evaluated.questions_to_avoid[0].safer_route.startswith("Ask what the guest remembers")
    assert receipt.risk_scores["centroid_risk"] == 1.0


def test_operator_edits_preserve_evidence_and_induction_rationale():
    service, org_id, brand_id, actor_id, _guest_id, _context_receipt, _matrix, plan = _session_plan()
    question = plan.planned_questions[0]

    edit = service.edit_pre_induction_question(
        organization_id=org_id,
        brand_id=brand_id,
        pre_induction_plan_id=plan.pre_induction_plan_id,
        question_id=question.question_id,
        revised_question="When did visibility stop feeling like marketing and start feeling like exposure?",
        evidence_ids=question.evidence_ids,
        rationale="Operator chose the question that preserves the Matrix pressure without scripting the landing.",
        edited_by_actor_id=actor_id,
    )
    updated = service.repository.plans[plan.pre_induction_plan_id]

    assert edit.evidence_ids == question.evidence_ids
    assert edit.rationale.startswith("Operator chose")
    assert edit.operator_edit_id in updated.operator_edit_ids
    assert updated.planned_questions[0].natural_question.startswith("When did visibility")


def test_manipulative_or_scripted_prompt_is_blocked_or_marked_for_rewrite():
    service, org_id, brand_id, actor_id, _guest_id, _context_receipt, _matrix, plan = _session_plan()
    question = plan.planned_questions[0].model_copy(
        update={"natural_question": "End by saying that your audience must admit they are afraid."}
    )
    service.repository.put_plan(plan.model_copy(update={"planned_questions": [question]}))

    receipt = service.evaluate_pre_induction_plan(
        organization_id=org_id,
        brand_id=brand_id,
        pre_induction_plan_id=plan.pre_induction_plan_id,
        evaluator_actor_id=actor_id,
    )
    blocked = service.repository.plans[plan.pre_induction_plan_id]

    assert blocked.status == PreInductionPlanStatus.blocked
    assert blocked.planned_questions[0].manipulation_risk == InductionRiskLevel.blocked
    assert receipt.decision_code == "PRE_INDUCTION_PLAN_BLOCKED"


def test_approved_plan_feeds_live_mode_without_replacing_operator_judgment():
    service, org_id, brand_id, actor_id, _guest_id, _context_receipt, _matrix, plan = _session_plan()
    service.evaluate_pre_induction_plan(
        organization_id=org_id,
        brand_id=brand_id,
        pre_induction_plan_id=plan.pre_induction_plan_id,
        evaluator_actor_id=actor_id,
    )
    approved = service.approve_pre_induction_plan(
        organization_id=org_id,
        brand_id=brand_id,
        pre_induction_plan_id=plan.pre_induction_plan_id,
        reviewer_actor_id=actor_id,
    )
    binding = service.get_live_interview_mode_binding(
        organization_id=org_id,
        brand_id=brand_id,
        pre_induction_plan_id=plan.pre_induction_plan_id,
    )

    assert approved.status == PreInductionPlanStatus.approved
    assert binding.read_only is True
    assert binding.operator_judgment_required is True
    with pytest.raises(PreInductionServiceError) as exc:
        service.edit_pre_induction_question(
            organization_id=org_id,
            brand_id=brand_id,
            pre_induction_plan_id=plan.pre_induction_plan_id,
            question_id=plan.planned_questions[0].question_id,
            revised_question="Try this late edit.",
            evidence_ids=plan.planned_questions[0].evidence_ids,
            rationale="late edit",
            edited_by_actor_id=actor_id,
        )
    assert exc.value.code == "PRE_INDUCTION_PLAN_IMMUTABLE"


def test_workflow_stage4_pre_induction_compiles_plan():
    service, org_id, brand_id, actor_id, guest_id, context_receipt, matrix, _plan = _session_plan()
    workflow = InterviewPreparationWorkflow(
        service.context_service.research_service,
        context_service=service.context_service,
        matrix_service=service.matrix_service,
        pre_induction_service=service,
    )

    plan = workflow.stage4_pre_induction(
        organization_id=org_id,
        brand_id=brand_id,
        guest_id=guest_id,
        operator_id=actor_id,
        context_premise_id=context_receipt.output_ids[ContextArtifactKind.context_premise],
        matrix_brief_id=matrix.matrix_brief_id,
        resonance_context_id=context_receipt.output_ids[ContextArtifactKind.interviewer_resonance_context],
        actor_id=actor_id,
    )

    assert plan.status == PreInductionPlanStatus.draft
    assert plan.matrix_brief_id == matrix.matrix_brief_id


def test_pre_induction_command_bus_emits_receipt_and_event():
    service, org_id, brand_id, actor_id, guest_id, context_receipt, matrix, _plan = _session_plan()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_pre_induction_command_handlers(bus, service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["operator"])
    envelope = new_command_envelope(
        command_type="CompilePreInductionPlanCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "guest_id": str(guest_id),
            "operator_id": str(actor_id),
            "context_premise_id": str(context_receipt.output_ids[ContextArtifactKind.context_premise]),
            "matrix_brief_id": str(matrix.matrix_brief_id),
            "resonance_context_id": str(context_receipt.output_ids[ContextArtifactKind.interviewer_resonance_context]),
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["schema_version"] == "cmf.pre_induction_plan.v1"
    assert bus.event_outbox.events[-1].event_type == "CompilePreInductionPlanCommand.succeeded"
