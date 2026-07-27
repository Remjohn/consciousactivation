from ccp_studio.contracts.provider_adapters import ProviderCapabilityId, ProviderExecutionStatus, ProviderId
from ccp_studio.services.supervisual_provider_materialization_service import SuperVisualProviderMaterializationService


def test_supervisual_provider_materialization_uses_fake_provider_blueprint():
    service = SuperVisualProviderMaterializationService()
    receipt = service.materialize_from_blueprint(
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
        prompt="source-grounded editorial plate",
        negative_prompt="generic cinematic gloss",
        allow_fake_without_approval=True,
    )
    assert receipt.status == ProviderExecutionStatus.SUCCEEDED
    assert receipt.provider_job_blueprint_id == "blueprint_1"
    assert receipt.output_assets
    assert receipt.output_assets[0].sha256


def test_supervisual_real_provider_materialization_requires_approval():
    service = SuperVisualProviderMaterializationService()
    try:
        service.materialize_from_blueprint(
            brand_id="brand_1",
            brand_context_version_id="bcv_1",
            provider_id=ProviderId.OPENAI_IMAGE,
            provider_capability_id=ProviderCapabilityId.IMAGE_GENERATE,
            provider_job_blueprint_id="blueprint_1",
            route_production_spec_id="route_spec_1",
            primary_style_route_id="CAC_CONSCIOUS_AMBIENT_CINEMA",
            source_references=["source_ref_1"],
            frame_profile="1:1_SOFT_ROUNDED_EDITORIAL",
            composition_role="hero_visual",
            prompt="source-grounded editorial plate",
            negative_prompt="generic cinematic gloss",
        )
    except Exception as exc:
        assert "operator_approval_ref" in str(exc) or "trusted_auto_approval_policy_id" in str(exc)
    else:
        raise AssertionError("Expected real provider call without approval to fail")
