import os
import pytest

from ccp_studio.contracts.provider_adapters import (
    ProviderAssetInput,
    ProviderCapabilityId,
    ProviderExecutionRequest,
    ProviderExecutionStatus,
    ProviderId,
    ProviderPromptContract,
    ProviderTransportMode,
    ProviderAdapterConfig,
    ProviderErrorCode,
    RetryDecision,
)
from ccp_studio.providers.bfl_flux_adapter import BFLFluxAdapter
from ccp_studio.providers.fake_image_adapter import FakeImageAdapter
from ccp_studio.providers.ideogram_adapter import IdeogramAdapter
from ccp_studio.providers.openai_image_adapter import OpenAIImageAdapter
from ccp_studio.providers.provider_errors import normalize_provider_error
from ccp_studio.providers.provider_storage import ProviderOutputStorage
from ccp_studio.providers.segment_anything_adapter import SegmentAnythingAdapter


def _request(provider_id=ProviderId.FAKE_IMAGE, capability=ProviderCapabilityId.IMAGE_GENERATE, approval=True):
    return ProviderExecutionRequest(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        provider_id=provider_id,
        provider_capability_id=capability,
        provider_job_blueprint_id="blueprint_1",
        route_production_spec_id="route_spec_1",
        primary_style_route_id="CAC_CONSCIOUS_AMBIENT_CINEMA",
        source_references=["source_ref_1"],
        frame_profile="1:1_SOFT_ROUNDED_EDITORIAL",
        composition_role="hero_visual",
        prompt_contract=ProviderPromptContract(
            primary_prompt="source-grounded editorial visual",
            route_id="CAC_CONSCIOUS_AMBIENT_CINEMA",
            frame_profile="1:1_SOFT_ROUNDED_EDITORIAL",
            composition_role="hero_visual",
            source_reference_ids=["source_ref_1"],
        ),
        idempotency_key="idem_1",
        operator_approval_ref="approval_1" if approval else None,
        allow_fake_without_approval=provider_id == ProviderId.FAKE_IMAGE,
    )


def test_provider_request_requires_idempotency_key():
    with pytest.raises(Exception):
        ProviderExecutionRequest(
            brand_id="brand_1",
            brand_context_version_id="bcv_1",
            provider_id=ProviderId.FAKE_IMAGE,
            provider_capability_id=ProviderCapabilityId.IMAGE_GENERATE,
            provider_job_blueprint_id="blueprint_1",
            route_production_spec_id="route_spec_1",
            primary_style_route_id="CAC_CONSCIOUS_AMBIENT_CINEMA",
            source_references=["source_ref_1"],
            frame_profile="1:1_SOFT_ROUNDED_EDITORIAL",
            composition_role="hero_visual",
            prompt_contract=ProviderPromptContract(
                primary_prompt="test",
                route_id="CAC_CONSCIOUS_AMBIENT_CINEMA",
                frame_profile="1:1_SOFT_ROUNDED_EDITORIAL",
                composition_role="hero_visual",
            ),
            idempotency_key="",
            allow_fake_without_approval=True,
        )


def test_real_provider_request_requires_operator_approval():
    with pytest.raises(Exception):
        _request(provider_id=ProviderId.OPENAI_IMAGE, approval=False)


def test_fake_adapter_completes_and_stores_output(tmp_path):
    adapter = FakeImageAdapter(storage=ProviderOutputStorage(tmp_path))
    request = _request(provider_id=ProviderId.FAKE_IMAGE, approval=False)
    preflight = adapter.validate(request)
    assert preflight.pass_status
    submission = adapter.submit(request)
    poll = adapter.poll(request, submission)
    outputs = adapter.download_outputs(request, poll)
    receipt = adapter.normalize(request, submission, poll, outputs)
    assert receipt.status == ProviderExecutionStatus.SUCCEEDED
    assert outputs[0].sha256
    assert os.path.exists(outputs[0].uri)


def test_openai_adapter_builds_generate_payload():
    adapter = OpenAIImageAdapter()
    request = _request(provider_id=ProviderId.OPENAI_IMAGE)
    payload = adapter.build_payload(request)
    assert payload["prompt"] == "source-grounded editorial visual"
    assert payload["size"] == "1024x1024"


def test_ideogram_adapter_maps_frame_profile_to_aspect_ratio():
    adapter = IdeogramAdapter()
    assert adapter.map_frame_profile_to_aspect_ratio("9:16_FULL_VERTICAL") == "ASPECT_9_16"
    assert adapter.map_frame_profile_to_aspect_ratio("4:5_FEED_POSTER") == "ASPECT_4_5"
    assert adapter.map_frame_profile_to_aspect_ratio("1:1_SOFT_ROUNDED_EDITORIAL") == "ASPECT_1_1"


def test_bfl_adapter_rejects_too_many_reference_images():
    adapter = BFLFluxAdapter()
    request = ProviderExecutionRequest(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        provider_id=ProviderId.BFL_FLUX,
        provider_capability_id=ProviderCapabilityId.IMAGE_REFERENCE_EDIT,
        provider_job_blueprint_id="blueprint_1",
        route_production_spec_id="route_spec_1",
        primary_style_route_id="CAC_CONSCIOUS_AMBIENT_CINEMA",
        source_references=["source_ref_1"],
        reference_assets=[ProviderAssetInput(asset_id=f"asset_{i}", uri=f"file://asset_{i}.png") for i in range(11)],
        frame_profile="1:1_SOFT_ROUNDED_EDITORIAL",
        composition_role="hero_visual",
        prompt_contract=ProviderPromptContract(
            primary_prompt="test",
            route_id="CAC_CONSCIOUS_AMBIENT_CINEMA",
            frame_profile="1:1_SOFT_ROUNDED_EDITORIAL",
            composition_role="hero_visual",
        ),
        idempotency_key="idem_bfl",
        operator_approval_ref="approval_1",
    )
    report = adapter.validate(request)
    assert not report.pass_status
    assert ProviderErrorCode.UNSUPPORTED_INPUT_ASSET in report.blocker_codes


def test_segment_anything_outputs_mask_and_cutout(tmp_path):
    adapter = SegmentAnythingAdapter(
        config=ProviderAdapterConfig(
            provider_id=ProviderId.SEGMENT_ANYTHING,
            enabled=True,
            transport_mode=ProviderTransportMode.LOCAL,
            model_name="sam-local-test",
        ),
        storage=ProviderOutputStorage(tmp_path),
    )
    request = _request(provider_id=ProviderId.SEGMENT_ANYTHING, capability=ProviderCapabilityId.MASK_GENERATE)
    submission = adapter.submit(request)
    poll = adapter.poll(request, submission)
    outputs = adapter.download_outputs(request, poll)
    assert {output.output_type.value for output in outputs} == {"mask", "cutout"}


def test_provider_error_normalization():
    receipt = normalize_provider_error(
        provider_id=ProviderId.OPENAI_IMAGE,
        message="rate limit exceeded",
        status_code=429,
    )
    assert receipt.normalized_error_code == ProviderErrorCode.RATE_LIMITED
    assert receipt.retry_decision == RetryDecision.RETRY
    assert receipt.safe_to_retry
