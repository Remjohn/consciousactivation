from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_interviewer_pre_induction import _session_plan  # noqa: E402

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.context import ContextArtifactKind, TriggerDepthMode  # noqa: E402
from ccp_studio.contracts.induction import CRALMoment, RationaleMode, new_supported_claim  # noqa: E402
from ccp_studio.contracts.research import SourceRole  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.induction_rationale_service import (  # noqa: E402
    InductionRationaleService,
    register_induction_rationale_command_handlers,
)
from ccp_studio.services.interview_contract_service import InterviewContractService  # noqa: E402
from ccp_studio.workflows.interview_preparation import InterviewPreparationWorkflow  # noqa: E402


def _approved_plan_and_induction_service():
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
    induction_service = InductionRationaleService(
        context_service=pre_service.context_service,
        matrix_service=pre_service.matrix_service,
        pre_induction_service=pre_service,
        interview_contract_service=contract_service,
    )
    return induction_service, contract_service, org_id, brand_id, actor_id, guest_id, context_receipt, matrix, plan


def test_cral_roles_are_preserved_when_evidence_is_promoted():
    service, _contract_service, org_id, brand_id, actor_id, _guest_id, context_receipt, _matrix, _plan = _approved_plan_and_induction_service()
    premise = service.context_service.repository.context_premises[
        context_receipt.output_ids[ContextArtifactKind.context_premise]
    ]

    receipt = service.compile_cral_findings(
        organization_id=org_id,
        brand_id=brand_id,
        research_field_id=premise.research_field_id,
        evidence_ids=premise.evidence_ids,
        actor_id=actor_id,
    )
    moments = {service.repository.cral_findings[item].moment for item in receipt.cral_finding_ids}

    assert moments == set(CRALMoment)
    assert all(service.repository.cral_findings[item].evidence_ids for item in receipt.cral_finding_ids)


def test_audience_deep_trigger_map_exposes_depth_vectors_confidence_focus_and_gaps():
    service, _contract_service, org_id, brand_id, actor_id, _guest_id, context_receipt, _matrix, _plan = _approved_plan_and_induction_service()

    trigger_map = service.compile_audience_deep_trigger_map(
        organization_id=org_id,
        brand_id=brand_id,
        trigger_map_id=context_receipt.output_ids[ContextArtifactKind.audience_deep_trigger_map],
        actor_id=actor_id,
    )

    assert trigger_map.depth_mode == TriggerDepthMode.saturated
    assert trigger_map.hermeneutical_gaps
    assert trigger_map.moral_emotional_vectors
    assert trigger_map.coping_trajectory
    assert trigger_map.regulatory_focus == "prevention"
    assert trigger_map.confidence > 0
    assert trigger_map.gaps == []


def test_emotional_and_voice_dna_distinguish_root_belief_construction_path_and_negative_space():
    service, _contract_service, org_id, brand_id, actor_id, _guest_id, context_receipt, _matrix, _plan = _approved_plan_and_induction_service()
    premise_id = context_receipt.output_ids[ContextArtifactKind.context_premise]
    trigger_map_id = context_receipt.output_ids[ContextArtifactKind.audience_deep_trigger_map]

    emotional_receipt = service.extract_emotional_dna(
        organization_id=org_id,
        brand_id=brand_id,
        context_premise_id=premise_id,
        trigger_map_id=trigger_map_id,
        actor_id=actor_id,
    )
    voice_receipt = service.compile_voice_dna_profile(
        organization_id=org_id,
        brand_id=brand_id,
        context_premise_id=premise_id,
        emotional_dna_profile_id=emotional_receipt.emotional_dna_profile_id,
        actor_id=actor_id,
    )
    emotional = service.repository.emotional_dna_profiles[emotional_receipt.emotional_dna_profile_id]
    voice = service.repository.voice_dna_profiles[voice_receipt.voice_dna_profile_id]

    assert emotional.belief_content
    assert emotional.emotional_path
    assert emotional.suppression_markers
    assert emotional.escalation_triggers
    assert voice.emotional_dna_profile_id == emotional.emotional_dna_profile_id
    assert voice.construction_mechanics
    assert voice.negative_space
    assert voice.normative_expression_targets


def test_operator_can_inspect_rationale_for_each_move_and_contract_binding():
    service, contract_service, org_id, brand_id, actor_id, _guest_id, _context_receipt, matrix, plan = _approved_plan_and_induction_service()
    deck = contract_service.compile_interview_deck(
        organization_id=org_id,
        brand_id=brand_id,
        pre_induction_plan_id=plan.pre_induction_plan_id,
        matrix_brief_id=matrix.matrix_brief_id,
        compiled_by_actor_id=actor_id,
    )

    receipt = service.compile_induction_rationales(
        organization_id=org_id,
        brand_id=brand_id,
        pre_induction_plan_id=plan.pre_induction_plan_id,
        matrix_brief_id=matrix.matrix_brief_id,
        interview_deck_id=deck.interview_deck_id,
        actor_id=actor_id,
    )
    updated_plan = service.pre_induction_service.repository.plans[plan.pre_induction_plan_id]
    first_question = updated_plan.planned_questions[0]
    inspection = service.inspect_rationale_for_move(
        organization_id=org_id,
        brand_id=brand_id,
        planned_move_id=first_question.question_id,
    )
    contract = contract_service.repository.contracts[deck.contract_ids[0]]

    assert receipt.decision_code == "INDUCTION_RATIONALE_COMPILED"
    assert first_question.rationale_id in receipt.rationale_ids
    assert inspection.cral_signals
    assert inspection.context_premise_id == updated_plan.context_premise_id
    assert inspection.emotional_dna_profile_id
    assert inspection.voice_dna_profile_id
    assert contract.induction_rationale_ids == [first_question.rationale_id]


def test_insufficient_dna_evidence_creates_partial_mode_and_blocks_certainty_language():
    service, _contract_service, org_id, brand_id, actor_id, _guest_id, _context_receipt, matrix, plan = _approved_plan_and_induction_service()

    receipt = service.compile_induction_rationales(
        organization_id=org_id,
        brand_id=brand_id,
        pre_induction_plan_id=plan.pre_induction_plan_id,
        matrix_brief_id=matrix.matrix_brief_id,
        include_emotional_dna=False,
        include_voice_dna=False,
        actor_id=actor_id,
    )
    rationale = service.repository.rationales[receipt.rationale_ids[0]]

    assert receipt.rationale_mode == RationaleMode.partial
    assert rationale.rationale_mode == RationaleMode.partial
    assert rationale.emotional_dna_profile_id is None
    assert rationale.voice_dna_profile_id is None
    assert any("absent" in item.lower() for item in rationale.support_limitations)


def test_unsupported_psychology_claim_is_blocked():
    service, _contract_service, org_id, brand_id, actor_id, _guest_id, _context_receipt, _matrix, _plan = _approved_plan_and_induction_service()
    evidence_id = next(iter(service.context_service.research_service.repository.evidence))
    claim = new_supported_claim(
        statement="The guest has a deep trauma pattern that explains all recording resistance.",
        claim_type="unsupported_certainty",
        evidence_ids=[evidence_id],
        source_roles=[SourceRole.inference],
        confidence=0.95,
        limitation="This claim overstates the evidence and must be blocked.",
        rationale_mode=RationaleMode.full_depth,
    )

    receipt = service.block_unsupported_psychology(
        organization_id=org_id,
        brand_id=brand_id,
        claims=[claim],
        actor_id=actor_id,
    )

    assert receipt.decision_code == "UNSUPPORTED_PSYCHOLOGY_BLOCKED"
    assert any(item.startswith("UNSUPPORTED_PSYCHOLOGICAL_CERTAINTY") for item in receipt.blocked_claims)


def test_workflow_stage3_4_compile_induction_rationale():
    service, contract_service, org_id, brand_id, actor_id, _guest_id, _context_receipt, matrix, plan = _approved_plan_and_induction_service()
    workflow = InterviewPreparationWorkflow(
        service.context_service.research_service,
        context_service=service.context_service,
        matrix_service=service.matrix_service,
        pre_induction_service=service.pre_induction_service,
        interview_contract_service=contract_service,
        induction_rationale_service=service,
    )

    receipt = workflow.stage3_4_compile_induction_rationale(
        organization_id=org_id,
        brand_id=brand_id,
        pre_induction_plan_id=plan.pre_induction_plan_id,
        matrix_brief_id=matrix.matrix_brief_id,
        actor_id=actor_id,
    )

    assert receipt.rationale_ids
    assert receipt.decision_code == "INDUCTION_RATIONALE_COMPILED"


def test_induction_rationale_command_bus_emits_receipt_event():
    service, _contract_service, org_id, brand_id, actor_id, _guest_id, _context_receipt, matrix, plan = _approved_plan_and_induction_service()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_induction_rationale_command_handlers(bus, service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["operator"])
    envelope = new_command_envelope(
        command_type="CompileInductionRationaleCommand",
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
    assert result.result_payload["decision_code"] == "INDUCTION_RATIONALE_COMPILED"
    assert bus.event_outbox.events[-1].event_type == "CompileInductionRationaleCommand.succeeded"
