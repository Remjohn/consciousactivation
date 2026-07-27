from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_interviewer_pre_induction import _session_plan  # noqa: E402

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.interview_contracts import ExpressionState, InterviewContractStatus  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.interview_contract_service import (  # noqa: E402
    InterviewContractService,
    InterviewContractServiceError,
    register_interview_contract_command_handlers,
)
from ccp_studio.workflows.interview_preparation import InterviewPreparationWorkflow  # noqa: E402


def _approved_preparation():
    pre_service, org_id, brand_id, actor_id, guest_id, context_receipt, matrix, plan = _session_plan()
    pre_service.evaluate_pre_induction_plan(
        organization_id=org_id,
        brand_id=brand_id,
        pre_induction_plan_id=plan.pre_induction_plan_id,
        evaluator_actor_id=actor_id,
    )
    plan = pre_service.approve_pre_induction_plan(
        organization_id=org_id,
        brand_id=brand_id,
        pre_induction_plan_id=plan.pre_induction_plan_id,
        reviewer_actor_id=actor_id,
    )
    contract_service = InterviewContractService(
        pre_induction_service=pre_service,
        matrix_service=pre_service.matrix_service,
    )
    return contract_service, org_id, brand_id, actor_id, guest_id, context_receipt, matrix, plan


def test_contract_includes_expression_route_derivative_edge_anchors_followups_cmf_route_and_eval_logic():
    service, org_id, brand_id, actor_id, _guest_id, _context_receipt, matrix, plan = _approved_preparation()

    deck = service.compile_interview_deck(
        organization_id=org_id,
        brand_id=brand_id,
        pre_induction_plan_id=plan.pre_induction_plan_id,
        matrix_brief_id=matrix.matrix_brief_id,
        compiled_by_actor_id=actor_id,
    )
    contract = service.repository.contracts[deck.contract_ids[0]]

    assert ExpressionState.vulnerability in contract.target_expression_states
    assert contract.route_target.core_archetype_ref == "archetype.conceptual_contrast.v1"
    assert contract.route_target.asset_derivative_refs
    assert contract.route_target.cmf_render_mode_refs
    assert contract.edge_product_id == matrix.edge_products[0].edge_product_id
    assert contract.first_line_anchors.complete is True
    assert contract.depth_anchor
    assert contract.repair_followups.too_abstract
    assert contract.depth_eval_rule == "answer_must_contain_specific_cost_or_tension"


def test_expression_state_confused_with_output_archetype_is_rejected_with_correction_note():
    service, org_id, brand_id, actor_id, _guest_id, _context_receipt, matrix, plan = _approved_preparation()
    deck = service.compile_interview_deck(
        organization_id=org_id,
        brand_id=brand_id,
        pre_induction_plan_id=plan.pre_induction_plan_id,
        matrix_brief_id=matrix.matrix_brief_id,
        compiled_by_actor_id=actor_id,
        force_confusion=True,
    )

    receipt = service.evaluate_interview_plan(
        organization_id=org_id,
        brand_id=brand_id,
        interview_deck_id=deck.interview_deck_id,
        evaluator_actor_id=actor_id,
    )
    rejected = service.reject_expression_archetype_confusion(
        organization_id=org_id,
        brand_id=brand_id,
        interview_deck_id=deck.interview_deck_id,
        reviewer_actor_id=actor_id,
        correction_note="Use vulnerability as expression state and a migrated archetype as output route.",
    )

    assert receipt.decision_code == "INTERVIEW_PLAN_EVALUATION_FAILED"
    assert "EXPRESSION_ARCHETYPE_CONFUSION" in receipt.failure_reasons
    assert rejected.status == InterviewContractStatus.rejected


def test_weak_saturation_collision_specificity_or_routeability_blocks_approval():
    service, org_id, brand_id, actor_id, _guest_id, _context_receipt, matrix, plan = _approved_preparation()
    deck = service.compile_interview_deck(
        organization_id=org_id,
        brand_id=brand_id,
        pre_induction_plan_id=plan.pre_induction_plan_id,
        matrix_brief_id=matrix.matrix_brief_id,
        compiled_by_actor_id=actor_id,
        force_generic=True,
    )
    receipt = service.evaluate_interview_plan(
        organization_id=org_id,
        brand_id=brand_id,
        interview_deck_id=deck.interview_deck_id,
        evaluator_actor_id=actor_id,
    )

    assert receipt.decision_code == "INTERVIEW_PLAN_EVALUATION_FAILED"
    assert "CONTRACT_SATURATION_REQUIRED" in receipt.failure_reasons
    assert "CONTRACT_ROUTEABILITY_FAILED" in receipt.failure_reasons
    with pytest.raises(InterviewContractServiceError) as exc:
        service.approve_interview_deck(
            organization_id=org_id,
            brand_id=brand_id,
            interview_deck_id=deck.interview_deck_id,
            reviewer_actor_id=actor_id,
        )
    assert exc.value.code == "INTERVIEW_PLAN_EVALUATION_REQUIRED"


def test_approved_contract_binds_to_complete_expression_session():
    service, org_id, brand_id, actor_id, _guest_id, _context_receipt, matrix, plan = _approved_preparation()
    deck = service.compile_interview_deck(
        organization_id=org_id,
        brand_id=brand_id,
        pre_induction_plan_id=plan.pre_induction_plan_id,
        matrix_brief_id=matrix.matrix_brief_id,
        compiled_by_actor_id=actor_id,
    )
    service.evaluate_interview_plan(
        organization_id=org_id,
        brand_id=brand_id,
        interview_deck_id=deck.interview_deck_id,
        evaluator_actor_id=actor_id,
    )
    approved = service.approve_interview_deck(
        organization_id=org_id,
        brand_id=brand_id,
        interview_deck_id=deck.interview_deck_id,
        reviewer_actor_id=actor_id,
    )
    expression_session_id = uuid4()
    binding = service.bind_deck_to_expression_session(
        organization_id=org_id,
        brand_id=brand_id,
        interview_deck_id=deck.interview_deck_id,
        expression_session_id=expression_session_id,
        actor_id=actor_id,
    )

    assert approved.approved_for_session is True
    assert binding.expression_session_id == expression_session_id
    assert binding.contract_ids == deck.contract_ids
    assert service.repository.decks[deck.interview_deck_id].status == InterviewContractStatus.bound_to_session


def test_extraction_review_can_show_originating_induction_context():
    service, org_id, brand_id, actor_id, _guest_id, _context_receipt, matrix, plan = _approved_preparation()
    deck = service.compile_interview_deck(
        organization_id=org_id,
        brand_id=brand_id,
        pre_induction_plan_id=plan.pre_induction_plan_id,
        matrix_brief_id=matrix.matrix_brief_id,
        compiled_by_actor_id=actor_id,
    )
    contract = service.repository.contracts[deck.contract_ids[0]]

    context = service.induction_context_for_extraction(
        organization_id=org_id,
        brand_id=brand_id,
        contract_id=contract.contract_id,
    )

    assert context.contract_id == contract.contract_id
    assert context.pre_induction_plan_id == plan.pre_induction_plan_id
    assert context.matrix_brief_id == matrix.matrix_brief_id
    assert context.evidence_ids == contract.evidence_ids


def test_workflow_stage4_compile_asset_contracts_creates_deck():
    service, org_id, brand_id, actor_id, _guest_id, _context_receipt, matrix, plan = _approved_preparation()
    workflow = InterviewPreparationWorkflow(
        service.pre_induction_service.context_service.research_service,
        context_service=service.pre_induction_service.context_service,
        matrix_service=service.matrix_service,
        pre_induction_service=service.pre_induction_service,
        interview_contract_service=service,
    )

    deck = workflow.stage4_compile_asset_contracts(
        organization_id=org_id,
        brand_id=brand_id,
        pre_induction_plan_id=plan.pre_induction_plan_id,
        matrix_brief_id=matrix.matrix_brief_id,
        actor_id=actor_id,
    )

    assert deck.contract_ids
    assert deck.status == InterviewContractStatus.draft


def test_interview_contract_command_bus_emits_deck_event():
    service, org_id, brand_id, actor_id, _guest_id, _context_receipt, matrix, plan = _approved_preparation()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_interview_contract_command_handlers(bus, service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["operator"])
    envelope = new_command_envelope(
        command_type="CompileInterviewDeckCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "pre_induction_plan_id": str(plan.pre_induction_plan_id),
            "matrix_brief_id": str(matrix.matrix_brief_id),
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["schema_version"] == "cmf.interview_deck.v1"
    assert bus.event_outbox.events[-1].event_type == "CompileInterviewDeckCommand.succeeded"
