from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.generative_adapters import GenerativeEvaluationState  # noqa: E402
from ccp_studio.providers.generative import GPTImage2Adapter  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.generative_provider_service import (  # noqa: E402
    GenerativeProviderError,
    GenerativeProviderService,
    register_generative_provider_command_handlers,
)
from ccp_studio.services.provider_operations_service import ProviderOperationsService  # noqa: E402
from ccp_studio.workflows.provider_job_workflow import ProviderJobWorkflow  # noqa: E402


def _service() -> GenerativeProviderService:
    provider_operations = ProviderOperationsService()
    provider_operations.seed_current_cmf_capabilities()
    return GenerativeProviderService(provider_operations)


def _submit_kwargs(service: GenerativeProviderService, capability_id: str = "gpt_image_2.image_generation.v1"):
    org_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    capability = service.provider_operations.repository.capabilities[capability_id]
    return {
        "provider_capability_id": capability.provider_capability_id,
        "organization_id": org_id,
        "brand_id": brand_id,
        "actor_id": actor_id,
        "purpose": "identity_preserving_visual_refinement",
        "input_artifact_hashes": ["sha256-source-frame", "sha256-locked-brand-layer"],
        "input_types": capability.allowed_input_types[:1],
        "prompt_hash": "sha256-prompt",
        "parameters": {
            "estimated_cost_amount": 1.5,
            "prompt": "source-backed visual refinement",
            "seed": "seed-044",
            "config_values": {"identity_strength": 0.72},
        },
        "consent_record_version_ids": [uuid4()],
        "requires_consent_compatibility": True,
        "evaluation_target_id": uuid4(),
        "idempotency_key": f"generative:{capability_id}",
    }


def test_approved_provider_job_passes_through_adapter_and_capability_record():
    service = _service()
    kwargs = _submit_kwargs(service)

    output = service.submit_generative_provider_job(**kwargs)
    provider_receipt = service.provider_operations.repository.receipts[output.provider_receipt_id]

    assert output.metadata.provider_name == "gpt_image_2"
    assert output.metadata.model_or_workflow_version == "gpt_image_2"
    assert output.metadata.seed == "seed-044"
    assert provider_receipt.provider_capability_id == "gpt_image_2.image_generation.v1"
    assert provider_receipt.provider_name == "gpt_image_2"


def test_source_inputs_store_artifact_hashes_and_consent_compatibility():
    service = _service()
    kwargs = _submit_kwargs(service)

    output = service.submit_generative_provider_job(**kwargs)
    request = service.repository.requests[output.generative_provider_request_id]

    assert request.input_artifact_hashes == ["sha256-source-frame", "sha256-locked-brand-layer"]
    assert request.requires_consent_compatibility is True
    assert request.consent_record_version_ids == kwargs["consent_record_version_ids"]
    assert output.consent_record_version_ids == kwargs["consent_record_version_ids"]


def test_raw_output_is_stored_under_provider_raw_with_hash_and_receipt():
    service = _service()
    kwargs = _submit_kwargs(service)

    output = service.submit_generative_provider_job(**kwargs)

    assert output.raw_output_uri.startswith(f"brands/{kwargs['brand_id']}/provider-raw/gpt_image_2/")
    assert output.raw_output_uri.endswith(".png")
    assert output.output_hash
    assert output.provider_receipt_id in service.provider_operations.repository.receipts
    receipt = next(item for item in service.repository.receipts.values() if item.provider_output_id == output.provider_output_id)
    assert receipt.decision_code == "GENERATIVE_PROVIDER_OUTPUT_NORMALIZED"


def test_failed_evaluation_output_cannot_be_promoted_to_approved_render_asset():
    service = _service()
    kwargs = _submit_kwargs(service)
    output = service.submit_generative_provider_job(**kwargs)
    failed = service.evaluate_generated_asset(
        provider_output_id=output.provider_output_id,
        actor_id=kwargs["actor_id"],
        passed=False,
        notes=["identity drift exceeded threshold"],
    )

    with pytest.raises(GenerativeProviderError) as exc:
        service.promote_generated_asset(provider_output_id=failed.provider_output_id, actor_id=kwargs["actor_id"])

    blocked = service.repository.outputs[failed.provider_output_id]
    assert exc.value.code == "GENERATED_ASSET_EVALUATION_NOT_PASSED"
    assert blocked.promoted_asset_id is None
    assert blocked.evaluation_state == GenerativeEvaluationState.promotion_blocked


def test_missing_model_metadata_fails_receipt_validation():
    service = _service()
    service.provider_operations.adapters["gpt_image_2"] = GPTImage2Adapter(include_metadata=False)
    kwargs = _submit_kwargs(service)

    with pytest.raises(GenerativeProviderError) as exc:
        service.submit_generative_provider_job(**kwargs)

    assert exc.value.code == "PROVIDER_METADATA_REQUIRED"
    assert list(service.repository.receipts.values())[-1].decision_code == "GENERATIVE_PROVIDER_RECEIPT_VALIDATION_FAILED"


def test_all_approved_generative_adapters_normalize_metadata_and_raw_outputs():
    service = _service()
    capabilities = [
        ("gpt_image_2.image_generation.v1", ["scene_spec"]),
        ("flux_2_klein_9b.image_generation.v1", ["scene_spec"]),
        ("qwen_image_layered.layer_generation.v1", ["layer_manifest"]),
        ("sam3.segmentation_mask.v1", ["visual_candidate"]),
        ("lavasr.audio_restoration.v1", ["source_audio"]),
        ("moss_tts.synthetic_bridge_voice.v1", ["approved_bridge_text"]),
    ]

    outputs = []
    for capability_id, input_types in capabilities:
        kwargs = _submit_kwargs(service, capability_id)
        kwargs["input_types"] = input_types
        kwargs["parameters"] = {"estimated_cost_amount": 0.5, "seed": "seed-loop", "config_values": {"fixture": capability_id}}
        if capability_id.startswith(("gpt_image_2", "flux_2")):
            kwargs["parameters"]["prompt"] = "visual prompt"
        outputs.append(service.submit_generative_provider_job(**kwargs))

    assert {output.metadata.provider_name for output in outputs} == {
        "gpt_image_2",
        "flux_2_klein_9b",
        "qwen_image_layered",
        "sam3",
        "lavasr",
        "moss_tts",
    }
    assert all("/provider-raw/" in output.raw_output_uri for output in outputs)


def test_workflow_and_command_bus_submit_generative_provider_job():
    service = _service()
    kwargs = _submit_kwargs(service)
    workflow = ProviderJobWorkflow(service.provider_operations, generative_provider_service=service)

    output = workflow.stage11_generative_provider_adapter(**kwargs)

    assert output.provider_output_id in service.repository.outputs

    bus = create_in_memory_command_bus()
    bus.brands.add_scope(kwargs["organization_id"], kwargs["brand_id"])
    register_generative_provider_command_handlers(bus, service)
    actor = ActorContext(actor_id=kwargs["actor_id"], actor_type=ActorType.human, role_ids=["production_steward"])
    envelope = new_command_envelope(
        command_type="EvaluateGeneratedAssetCommand",
        organization_id=kwargs["organization_id"],
        brand_id=kwargs["brand_id"],
        actor=actor,
        payload={
            "provider_output_id": str(output.provider_output_id),
            "passed": True,
            "notes": ["identity and layerability accepted"],
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["evaluation_state"] == "passed"
    assert bus.event_outbox.events[-1].event_type == "EvaluateGeneratedAssetCommand.succeeded"
