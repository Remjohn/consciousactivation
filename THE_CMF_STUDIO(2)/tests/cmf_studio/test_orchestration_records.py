from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
except ModuleNotFoundError:
    FastAPI = None
    TestClient = None

from ccp_studio.contracts.agent_gateway import AgentActionRequest, AgentGatewayDecisionStatus
from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus
from ccp_studio.contracts.orchestration import (
    ActiveObjectRef,
    StageRunStatus,
    new_stage_execution_receipt,
)
from ccp_studio.services.agent_gateway import PiAgentGateway
from ccp_studio.services.command_bus import create_in_memory_command_bus
from ccp_studio.services.orchestration import OrchestrationService, OrchestrationValidationError
from ccp_studio.workflows.orchestration_run import OrchestrationRunWorkflow


def _prepare_stage(service: OrchestrationService | None = None):
    service = service or OrchestrationService()
    workflow = OrchestrationRunWorkflow(service)
    org_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    prepared = workflow.prepare_stage(
        organization_id=org_id,
        brand_id=brand_id,
        actor_id=actor_id,
        active_object=ActiveObjectRef(object_type="transcript", object_id=uuid4()),
        requested_outcome="extract expression moments",
        pipeline_stage="6 / Post-session extraction",
        expected_exit_object_type="ExpressionMoment",
        allowed_actor_or_service="Post-Session Extraction Agent",
        required_inputs=["transcript", "source_artifact_manifest"],
        allowed_actions=["run_jit_skill", "submit_stage_command"],
        blocked_actions=[
            "skip_stage",
            "direct_canonical_mutation",
            "self_approve",
            "publish_public",
            "neo4j_authorize_transition",
        ],
        downstream_proof_obligation="stage_execution_receipt with transcript and source evidence",
        success_criteria=["expression moments preserve source wording"],
        failure_criteria=["generic rewrite", "missing source boundary"],
        required_receipt_types=["stage_execution_receipt"],
        required_evidence_refs=["transcript:1", "source:video:1"],
        source_evidence_refs=["transcript:1", "source:video:1"],
        upstream_receipt_ids=[uuid4()],
    )
    return service, prepared, org_id, brand_id, actor_id


def test_prepare_stage_records_run_plan_validation_and_handoff():
    service, prepared, _org_id, _brand_id, _actor_id = _prepare_stage()

    assert prepared.run.status == StageRunStatus.executing
    assert prepared.plan.pipeline_stage == "6 / Post-session extraction"
    assert prepared.validation_contract.required_receipt_types == ["stage_execution_receipt"]
    assert prepared.handoff_packet.required_downstream_receipt == "stage_execution_receipt"
    assert prepared.run.orchestration_run_id in service.repository.runs
    assert prepared.plan.stage_execution_plan_id in service.repository.plans
    assert prepared.handoff_packet.handoff_packet_id in service.repository.handoff_packets


def test_missing_validation_contract_blocks_agent_handoff():
    service = OrchestrationService()
    run = service.open_or_resume_run(
        organization_id=uuid4(),
        brand_id=uuid4(),
        actor_id=uuid4(),
        active_object=ActiveObjectRef(object_type="asset_package_spec", object_id=uuid4()),
        requested_outcome="render approved asset package",
    )
    plan = service.create_stage_execution_plan(
        orchestration_run_id=run.orchestration_run_id,
        pipeline_stage="11 / Assembly and rendering",
        expected_exit_object_type="RenderOutput",
        allowed_actor_or_service="Renderer Router",
        required_inputs=["SceneSpec", "RenderContract"],
        allowed_actions=["submit_render_job"],
        blocked_actions=["skip_stage"],
        downstream_proof_obligation="render execution receipt",
    )

    with pytest.raises(OrchestrationValidationError) as exc:
        service.create_agent_handoff_packet(
            orchestration_run_id=run.orchestration_run_id,
            stage_execution_plan_id=plan.stage_execution_plan_id,
            recipient_type="renderer",
            recipient_name="Renderer Router",
            source_evidence_refs=[],
            upstream_receipt_ids=[],
        )

    assert exc.value.code == "VALIDATION_CONTRACT_REQUIRED"


def test_pi_gateway_blocks_forbidden_autonomy_actions():
    service, prepared, org_id, brand_id, actor_id = _prepare_stage()
    gateway = PiAgentGateway(service)

    blocked = gateway.request_action(
        AgentActionRequest(
            schema_version="cmf.agent_action_request.v1",
            organization_id=org_id,
            brand_id=brand_id,
            actor_id=actor_id,
            orchestration_run_id=prepared.run.orchestration_run_id,
            stage_execution_plan_id=prepared.plan.stage_execution_plan_id,
            actor_or_service="Pi",
            requested_action="direct_canonical_mutation",
            requested_target="expression_moments",
        )
    )

    assert blocked.status == AgentGatewayDecisionStatus.blocked
    assert blocked.code == "DIRECT_CANONICAL_MUTATION_FORBIDDEN"

    projection_blocked = gateway.request_action(
        AgentActionRequest(
            schema_version="cmf.agent_action_request.v1",
            organization_id=org_id,
            brand_id=brand_id,
            actor_id=actor_id,
            orchestration_run_id=prepared.run.orchestration_run_id,
            stage_execution_plan_id=prepared.plan.stage_execution_plan_id,
            actor_or_service="Pi",
            requested_action="neo4j_authorize_transition",
            requested_target="stage_transition",
        )
    )

    assert projection_blocked.status == AgentGatewayDecisionStatus.blocked
    assert projection_blocked.code == "PROJECTION_NOT_CANONICAL"


def test_jit_skill_invocation_record_preserves_compiler_context():
    service, prepared, _org_id, _brand_id, _actor_id = _prepare_stage()

    record = service.record_skill_invocation(
        orchestration_run_id=prepared.run.orchestration_run_id,
        stage_execution_plan_id=prepared.plan.stage_execution_plan_id,
        skill_key="legacy.expression_extraction.contrastive_v1",
        registry_snapshot_id=uuid4(),
        compiler_fingerprint="sha256:compiler-fingerprint",
        source_context_refs=["transcript:1", "guest:dossier:1"],
        contrastive_prompt_layer_refs=["prompt:anti_draft", "prompt:hard_negative"],
        critic_result_ref="critic:expression-boundary:1",
        synthesis_result_ref="synthesis:moment-candidates:1",
        eval_state="passed_source_truth_eval",
    )

    assert record.skill_key == "legacy.expression_extraction.contrastive_v1"
    assert "prompt:anti_draft" in record.contrastive_prompt_layer_refs
    assert record.skill_invocation_id in service.repository.skill_invocations


def test_stage_closure_requires_receipt_type_and_evidence_refs():
    service, prepared, _org_id, _brand_id, _actor_id = _prepare_stage()
    missing_evidence = new_stage_execution_receipt(
        orchestration_run_id=prepared.run.orchestration_run_id,
        stage_execution_plan_id=prepared.plan.stage_execution_plan_id,
        receipt_type="stage_execution_receipt",
        status=StageRunStatus.succeeded,
        decision="advance",
        evidence_refs=["transcript:1"],
        correlation_id=prepared.run.correlation_id,
    )

    with pytest.raises(OrchestrationValidationError) as exc:
        service.close_stage_execution(missing_evidence)
    assert exc.value.code == "REQUIRED_EVIDENCE_MISSING"

    wrong_type = new_stage_execution_receipt(
        orchestration_run_id=prepared.run.orchestration_run_id,
        stage_execution_plan_id=prepared.plan.stage_execution_plan_id,
        receipt_type="provider_receipt",
        status=StageRunStatus.succeeded,
        decision="advance",
        evidence_refs=["transcript:1", "source:video:1"],
        correlation_id=prepared.run.correlation_id,
    )

    with pytest.raises(OrchestrationValidationError) as exc:
        service.close_stage_execution(wrong_type)
    assert exc.value.code == "REQUIRED_RECEIPT_MISSING"

    valid = new_stage_execution_receipt(
        orchestration_run_id=prepared.run.orchestration_run_id,
        stage_execution_plan_id=prepared.plan.stage_execution_plan_id,
        receipt_type="stage_execution_receipt",
        status=StageRunStatus.succeeded,
        decision="advance",
        evidence_refs=["transcript:1", "source:video:1"],
        correlation_id=prepared.run.correlation_id,
    )

    receipt = service.close_stage_execution(valid)

    assert receipt.receipt_id in service.repository.stage_receipts
    assert service.repository.get_run(prepared.run.orchestration_run_id).status == StageRunStatus.succeeded


def test_orchestration_submits_mutations_through_command_bus():
    service, prepared, org_id, brand_id, actor_id = _prepare_stage()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)

    result = service.submit_stage_command(
        command_bus=bus,
        orchestration_run_id=prepared.run.orchestration_run_id,
        stage_execution_plan_id=prepared.plan.stage_execution_plan_id,
        command_type="SubmitCommand",
        actor=ActorContext(
            actor_id=actor_id,
            actor_type=ActorType.pi,
            role_ids=["owner"],
        ),
        payload={"aggregate_id": str(brand_id), "purpose": "record stage checkpoint"},
        idempotency_key="orchestration-checkpoint",
    )

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["payload"]["pipeline_stage"] == "6 / Post-session extraction"
    assert len(bus.command_log.records) == 1
    assert len(bus.audit_receipts.receipts) == 1


def test_fastapi_orchestration_prepare_stage_route_smoke():
    if FastAPI is None or TestClient is None:
        pytest.skip("FastAPI adapter dependency set is incomplete in this local environment.")

    from ccp_studio.api.v1.orchestration import router, set_orchestration_service

    service = OrchestrationService()
    set_orchestration_service(service)
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)
    org_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    object_id = uuid4()

    response = client.post(
        "/api/v1/orchestration/prepare-stage",
        json={
            "organization_id": str(org_id),
            "brand_id": str(brand_id),
            "actor_id": str(actor_id),
            "active_object": {"object_type": "transcript", "object_id": str(object_id)},
            "requested_outcome": "extract expression moments",
            "pipeline_stage": "6 / Post-session extraction",
            "expected_exit_object_type": "ExpressionMoment",
            "allowed_actor_or_service": "Post-Session Extraction Agent",
            "required_inputs": ["transcript"],
            "allowed_actions": ["run_jit_skill"],
            "blocked_actions": ["skip_stage"],
            "downstream_proof_obligation": "stage execution receipt",
            "success_criteria": ["source-backed extraction"],
            "failure_criteria": ["generic rewrite"],
            "required_receipt_types": ["stage_execution_receipt"],
            "required_evidence_refs": ["transcript:1"],
            "source_evidence_refs": ["transcript:1"],
            "upstream_receipt_ids": [],
        },
    )

    assert response.status_code == 200
    assert response.json()["handoff_packet"]["required_downstream_receipt"] == "stage_execution_receipt"


def test_failure_friction_human_and_quarantine_receipts_are_recorded():
    service, prepared, _org_id, _brand_id, _actor_id = _prepare_stage()

    failure = service.record_failure_receipt(
        orchestration_run_id=prepared.run.orchestration_run_id,
        stage_execution_plan_id=prepared.plan.stage_execution_plan_id,
        failed_gate="source_truth_eval",
        root_cause="candidate detached from transcript wording",
        retry_policy="retry_with_hard_negative",
        next_action="repair_extraction",
        evidence_refs=["eval:source_truth:failed"],
    )
    friction = service.record_friction_receipt(
        orchestration_run_id=prepared.run.orchestration_run_id,
        stage_execution_plan_id=prepared.plan.stage_execution_plan_id,
        friction_type="reviewer_uncertainty",
        description="Two candidates passed but reviewer requested taste judgment.",
    )
    handoff = service.request_human_handoff(
        orchestration_run_id=prepared.run.orchestration_run_id,
        stage_execution_plan_id=prepared.plan.stage_execution_plan_id,
        reason="taste ambiguity",
        required_decision="choose expression candidate",
        allowed_responses=["candidate_a", "candidate_b", "reject_both"],
    )
    quarantine = service.record_quarantine_receipt(
        orchestration_run_id=prepared.run.orchestration_run_id,
        stage_execution_plan_id=prepared.plan.stage_execution_plan_id,
        quarantine_reason="ambiguous provenance",
        recovery_action="request source artifact review",
        blocked_output_refs=["candidate:unsafe"],
    )

    assert failure.receipt_id in service.repository.failure_receipts
    assert friction.receipt_id in service.repository.friction_receipts
    assert handoff.handoff_request_id in service.repository.human_handoffs
    assert quarantine.receipt_id in service.repository.quarantine_receipts
    assert service.repository.get_run(prepared.run.orchestration_run_id).status == StageRunStatus.quarantined
