from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_interviewer_pre_induction import _session_plan  # noqa: E402

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.consent import ConsentScope  # noqa: E402
from ccp_studio.contracts.expression_session import ExpressionSessionStatus  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.consent_service import ConsentService  # noqa: E402
from ccp_studio.services.expression_session_service import (  # noqa: E402
    CompleteExpressionSessionService,
    CompleteExpressionSessionServiceError,
    register_complete_expression_session_command_handlers,
)
from ccp_studio.services.interview_contract_service import InterviewContractService  # noqa: E402
from ccp_studio.services.source_ingestion import SourceIngestionService  # noqa: E402
from ccp_studio.workflows.complete_expression_session import CompleteExpressionSessionWorkflow  # noqa: E402


def _scope(**overrides):
    values = {
        "recording_allowed": True,
        "source_storage_allowed": True,
        "likeness_use_allowed": True,
        "derivative_generation_allowed": True,
        "provider_processing_allowed": True,
        "synthetic_voice_eligible": False,
        "reuse_allowed": True,
        "retention_allowed": True,
        "publication_allowed": True,
    }
    values.update(overrides)
    return ConsentScope(**values)


def _approved_deck_fixture(scope=None, quality_gate_passed=True):
    pre_service, org_id, brand_id, actor_id, guest_id, _context_receipt, matrix, plan = _session_plan()
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
    deck = contract_service.compile_interview_deck(
        organization_id=org_id,
        brand_id=brand_id,
        pre_induction_plan_id=plan.pre_induction_plan_id,
        matrix_brief_id=matrix.matrix_brief_id,
        compiled_by_actor_id=actor_id,
    )
    contract_service.evaluate_interview_plan(
        organization_id=org_id,
        brand_id=brand_id,
        interview_deck_id=deck.interview_deck_id,
        evaluator_actor_id=actor_id,
    )
    deck = contract_service.approve_interview_deck(
        organization_id=org_id,
        brand_id=brand_id,
        interview_deck_id=deck.interview_deck_id,
        reviewer_actor_id=actor_id,
    )
    consent_service = ConsentService()
    consent = consent_service.grant_consent(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=guest_id,
        scope=scope or _scope(),
        actor_id=actor_id,
        evidence_refs=["consent:complete-expression-session"],
    )
    source_service = SourceIngestionService()
    session_service = CompleteExpressionSessionService(
        consent_service=consent_service,
        source_service=source_service,
        interview_contract_service=contract_service,
    )
    session = session_service.create_session(
        organization_id=org_id,
        brand_id=brand_id,
        guest_id=guest_id,
        operator_id=actor_id,
        interview_deck_id=deck.interview_deck_id,
        consent_record_version_id=consent.consent_record_version_id,
        conversation_language="en",
        created_by_actor_id=actor_id,
        expected_master_source="local wav master",
        backup_route="secondary recorder",
        platform_source="zoom",
        upload_method="operator_upload",
        file_safety_expectations=["no platform compression as canonical"],
        quality_requirements=["master wav", "guest/interviewer separation", "timestamp alignment"],
        quality_gate_passed=quality_gate_passed,
    )
    return session_service, org_id, brand_id, actor_id, guest_id, consent, deck, session


def test_session_binds_brand_guest_consent_config_contracts_and_status():
    service, org_id, brand_id, actor_id, guest_id, consent, deck, session = _approved_deck_fixture()

    assert session.organization_id == org_id
    assert session.brand_id == brand_id
    assert session.guest_id == guest_id
    assert session.operator_id == actor_id
    assert session.consent_record_version_id == consent.consent_record_version_id
    assert session.interview_deck_id == deck.interview_deck_id
    assert session.interview_asset_contract_ids == deck.contract_ids
    assert session.recording_configuration.master_recording_source == "local wav master"
    assert session.status == ExpressionSessionStatus.ready_for_recording


def test_incomplete_consent_or_setup_blocks_start_and_writes_blocked_receipt():
    service, org_id, brand_id, actor_id, _guest_id, _consent, _deck, session = _approved_deck_fixture(
        scope=_scope(recording_allowed=False),
        quality_gate_passed=False,
    )

    with pytest.raises(CompleteExpressionSessionServiceError) as exc:
        service.start_session(
            organization_id=org_id,
            brand_id=brand_id,
            expression_session_id=session.expression_session_id,
            actor_id=actor_id,
        )
    blocked = list(service.repository.receipts.values())[-1]

    assert exc.value.code == "SESSION_NOT_READY_FOR_RECORDING"
    assert blocked.decision_code == "SESSION_READINESS_BLOCKED"
    assert "SESSION_NOT_READY_FOR_RECORDING" in blocked.missing_requirements


def test_brand_scope_filters_session_queries():
    service, org_id, brand_id, _actor_id, _guest_id, _consent, _deck, session = _approved_deck_fixture()

    assert service.list_sessions_for_brand(organization_id=org_id, brand_id=brand_id) == [session]
    assert service.list_sessions_for_brand(organization_id=org_id, brand_id=uuid4()) == []
    with pytest.raises(CompleteExpressionSessionServiceError) as exc:
        service.get_session(
            organization_id=org_id,
            brand_id=uuid4(),
            expression_session_id=session.expression_session_id,
        )
    assert exc.value.code == "BRAND_SCOPE_VIOLATION"


def test_start_writes_event_receipt_and_binds_deck_to_expression_session():
    service, org_id, brand_id, actor_id, guest_id, _consent, deck, session = _approved_deck_fixture()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_complete_expression_session_command_handlers(bus, service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["operator"])
    envelope = new_command_envelope(
        command_type="StartCompleteExpressionSessionCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "guest_or_client_id": str(guest_id),
            "expression_session_id": str(session.expression_session_id),
        },
    )

    result = bus.submit(envelope)
    started = service.repository.sessions[session.expression_session_id]
    receipt = list(service.repository.receipts.values())[-1]

    assert result.status == CommandStatus.succeeded
    assert started.status == ExpressionSessionStatus.in_progress
    assert receipt.decision_code == "COMPLETE_EXPRESSION_SESSION_STARTED"
    assert service.interview_contract_service.repository.decks[deck.interview_deck_id].status.value == "bound_to_session"
    assert bus.event_outbox.events[-1].event_type == "StartCompleteExpressionSessionCommand.succeeded"


def test_pause_fail_and_close_transitions_use_explicit_statuses():
    service, org_id, brand_id, actor_id, _guest_id, _consent, _deck, session = _approved_deck_fixture()
    started = service.start_session(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        actor_id=actor_id,
    )
    paused = service.pause_session(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=started.expression_session_id,
        actor_id=actor_id,
        reason="Operator pause.",
    )
    resumed = service.resume_session(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=started.expression_session_id,
        actor_id=actor_id,
    )
    closed = service.close_session(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=started.expression_session_id,
        actor_id=actor_id,
    )

    assert paused.status == ExpressionSessionStatus.paused
    assert resumed.status == ExpressionSessionStatus.in_progress
    assert closed.status == ExpressionSessionStatus.closed
    failed_service, fail_org, fail_brand, fail_actor, _guest, _consent2, _deck2, fail_session = _approved_deck_fixture()
    failed = failed_service.fail_session(
        organization_id=fail_org,
        brand_id=fail_brand,
        expression_session_id=fail_session.expression_session_id,
        actor_id=fail_actor,
        reason="Guest source setup failed.",
    )
    assert failed.status == ExpressionSessionStatus.failed


def test_workflow_stage5_start_session_requires_receipt_backed_readiness():
    service, org_id, brand_id, actor_id, _guest_id, _consent, _deck, session = _approved_deck_fixture()
    workflow = CompleteExpressionSessionWorkflow(service)

    started = workflow.stage5_start_session(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        actor_id=actor_id,
    )

    assert started.status == ExpressionSessionStatus.in_progress
    assert any(receipt.decision_code == "COMPLETE_EXPRESSION_SESSION_STARTED" for receipt in service.repository.receipts.values())
