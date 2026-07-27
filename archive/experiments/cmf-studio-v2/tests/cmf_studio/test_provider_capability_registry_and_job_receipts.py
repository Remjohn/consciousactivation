from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.orchestration import utc_now  # noqa: E402
from ccp_studio.contracts.provider_jobs import ProviderCapabilityRecord, ProviderJobStatus, ProviderWebhookEnvelope  # noqa: E402
from ccp_studio.providers.fake_provider import FakeProviderAdapter  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.provider_operations_service import (  # noqa: E402
    ProviderOperationsError,
    ProviderOperationsService,
    register_provider_operations_command_handlers,
)
from ccp_studio.workflows.provider_job_workflow import ProviderJobWorkflow  # noqa: E402


def _service() -> ProviderOperationsService:
    service = ProviderOperationsService()
    service.seed_current_cmf_capabilities()
    return service


def _request_kwargs(service: ProviderOperationsService, capability_id: str = "ideogram_4.composition_plate.v1"):
    org_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    capability = service.repository.capabilities[capability_id]
    return {
        "provider_capability_id": capability.provider_capability_id,
        "organization_id": org_id,
        "brand_id": brand_id,
        "requested_by_actor_id": actor_id,
        "complete_editing_session_id": uuid4(),
        "scene_spec_id": uuid4(),
        "input_artifact_hashes": ["sha256-source", "sha256-render-contract"],
        "input_types": capability.allowed_input_types[:1],
        "prompt_hash": "sha256-prompt",
        "parameters": {"estimated_cost_amount": 1.25, "compiled_prompt": "source-backed scene prompt"},
        "idempotency_key": "provider-job:one",
    }


def test_current_provider_capability_seed_uses_cmf_provider_names_and_self_hosted_comfyui():
    service = _service()

    names = {item.provider_name for item in service.repository.capabilities.values()}
    comfy = service.repository.capabilities["comfyui_docker_gpu.render_worker.v1"]

    assert {"ideogram_4", "gpt_image_2", "flux_2_klein_9b", "qwen_image_layered", "sam3"} <= names
    assert {"lavasr", "moss_tts", "remotion", "motion_canvas", "comfyui_docker_gpu"} <= names
    assert "24gb_32gb_vram" in comfy.execution_environment
    assert "RunningHub" not in " ".join(comfy.governance_notes)
    assert comfy.output_contract == "cmf.render_output.v1"


def test_submitted_provider_request_stores_hashes_prompt_params_brand_scene_and_correlation():
    service = _service()
    kwargs = _request_kwargs(service)

    job = service.submit_provider_job(**kwargs)
    request = service.repository.requests[job.provider_request_id]

    assert job.status == ProviderJobStatus.submitted
    assert request.input_artifact_hashes == ["sha256-source", "sha256-render-contract"]
    assert request.prompt_hash == "sha256-prompt"
    assert request.parameters["compiled_prompt"] == "source-backed scene prompt"
    assert request.brand_id == kwargs["brand_id"]
    assert request.scene_spec_id == kwargs["scene_spec_id"]
    assert request.correlation_id
    assert job.provider_correlation_id.startswith("ideogram_4:")


def test_provider_response_normalization_writes_receipt_cost_retries_outputs_and_events():
    service = _service()
    job = service.submit_provider_job(**_request_kwargs(service))
    response = service.repository.latest_response_for_job(job.provider_job_id)

    receipt = service.normalize_provider_response(response=response)

    assert receipt.output_artifact_hashes
    assert receipt.cost_amount == 1.25
    assert receipt.retry_count == 0
    assert receipt.status == ProviderJobStatus.succeeded
    assert receipt.created_domain_event_type == "ProviderReceiptValidated"
    assert [event.event_type for event in service.repository.domain_events][-2:] == [
        "ProviderReceiptValidated",
        "ProviderJobCompleted",
    ]


def test_unavailable_capability_fails_with_provider_capability_unavailable():
    service = _service()
    capability = service.repository.capabilities["ideogram_4.composition_plate.v1"]
    service.repository.capabilities[capability.provider_capability_id] = capability.model_copy(update={"active": False})

    with pytest.raises(ProviderOperationsError) as exc:
        service.submit_provider_job(**_request_kwargs(service))

    assert exc.value.code == "PROVIDER_CAPABILITY_UNAVAILABLE"


def test_cost_policy_blocks_duplicate_spend_before_submission():
    service = _service()
    kwargs = _request_kwargs(service)
    kwargs["parameters"] = {"estimated_cost_amount": 999.0, "compiled_prompt": "too expensive"}

    with pytest.raises(ProviderOperationsError) as exc:
        service.submit_provider_job(**kwargs)

    assert exc.value.code == "COST_POLICY_EXCEEDED"
    assert service.repository.jobs == {}


def test_webhook_processing_uses_command_path_shape_and_is_idempotent():
    service = _service()
    job = service.submit_provider_job(**_request_kwargs(service))
    envelope = ProviderWebhookEnvelope(
        schema_version="cmf.provider_webhook_envelope.v1",
        provider_webhook_id=uuid4(),
        provider_name=job.provider_name,
        provider_correlation_id=job.provider_correlation_id,
        payload={
            "status": "succeeded",
            "output_artifact_hashes": ["sha256-webhook-output"],
            "cost_amount": 2.0,
            "response_metadata": {"retry_count": 1},
        },
        idempotency_key="webhook:one",
        received_at=utc_now(),
    )

    receipt = service.process_provider_webhook(envelope)
    duplicate = service.process_provider_webhook(envelope)

    assert duplicate.provider_receipt_id == receipt.provider_receipt_id
    assert receipt.retry_count == 1
    assert receipt.output_artifact_hashes == ["sha256-webhook-output"]
    assert len([item for item in service.repository.domain_events if item.event_type == "ProviderWebhookProcessed"]) == 1


def test_workflow_and_command_bus_emit_provider_receipt_event_after_validation():
    service = _service()
    workflow = ProviderJobWorkflow(service)
    kwargs = _request_kwargs(service, "comfyui_docker_gpu.render_worker.v1")
    kwargs["input_types"] = ["workflow_json"]
    kwargs["parameters"] = {"estimated_cost_amount": 22.0}

    receipt = workflow.stage11_provider_execution(
        provider_capability_id=kwargs["provider_capability_id"],
        organization_id=kwargs["organization_id"],
        brand_id=kwargs["brand_id"],
        actor_id=kwargs["requested_by_actor_id"],
        input_artifact_hashes=kwargs["input_artifact_hashes"],
        input_types=kwargs["input_types"],
        parameters=kwargs["parameters"],
        idempotency_key=kwargs["idempotency_key"],
    )

    assert receipt.provider_name == "comfyui_docker_gpu"
    assert receipt.status == ProviderJobStatus.succeeded

    bus = create_in_memory_command_bus()
    bus.brands.add_scope(kwargs["organization_id"], kwargs["brand_id"])
    register_provider_operations_command_handlers(bus, service)
    actor = ActorContext(actor_id=kwargs["requested_by_actor_id"], actor_type=ActorType.human, role_ids=["production_steward"])
    envelope = new_command_envelope(
        command_type="ValidateProviderReceiptCommand",
        organization_id=kwargs["organization_id"],
        brand_id=kwargs["brand_id"],
        actor=actor,
        payload={"provider_receipt_id": str(receipt.provider_receipt_id)},
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["provider_receipt_id"] == str(receipt.provider_receipt_id)
    assert bus.event_outbox.events[-1].event_type == "ValidateProviderReceiptCommand.succeeded"


def test_inactive_custom_capability_cannot_be_used_even_when_registered():
    service = _service()
    inactive = ProviderCapabilityRecord(
        schema_version="cmf.provider_capability_record.v1",
        provider_capability_id="custom.disabled.v1",
        provider_name="custom_disabled",
        capability_name="disabled_test",
        model_or_workflow_version="disabled",
        allowed_input_types=["scene_spec"],
        output_contract="cmf.test_output.v1",
        cost_policy_id="cmf.provider.cost.standard",
        retry_policy_id="cmf.provider.retry.standard",
        evaluation_requirement_ids=["cmf.eval.disabled.v1"],
        execution_environment="test",
        governance_notes=[],
        active=False,
        activated_at=utc_now(),
    )
    service.activate_provider_capability(inactive)
    service.adapters["custom_disabled"] = FakeProviderAdapter(provider_name="custom_disabled")
    kwargs = _request_kwargs(service, "ideogram_4.composition_plate.v1")
    kwargs["provider_capability_id"] = "custom.disabled.v1"
    kwargs["input_types"] = ["scene_spec"]

    with pytest.raises(ProviderOperationsError) as exc:
        service.submit_provider_job(**kwargs)

    assert exc.value.code == "PROVIDER_CAPABILITY_UNAVAILABLE"
