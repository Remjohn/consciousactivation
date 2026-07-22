from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_scene_containers_creative_subsystems_and_asset_roll_orchestration import _scene_intelligence_fixture  # noqa: E402

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.visual_research import CandidateUseMode, LicenseTier  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.provider_operations_service import ProviderOperationsService  # noqa: E402
from ccp_studio.services.visual_research_service import (  # noqa: E402
    LEGACY_ADAPTER_ROUTE,
    VisualResearchError,
    VisualResearchService,
    register_visual_research_command_handlers,
)
from ccp_studio.workflows.provider_job_workflow import ProviderJobWorkflow  # noqa: E402


def _provider_ops():
    service = ProviderOperationsService()
    service.seed_current_cmf_capabilities()
    return service


def _query(service: VisualResearchService, scene_spec_id):
    return service.create_visual_research_query(
        scene_spec_id=scene_spec_id,
        asset_roll_role="b_roll",
        emotional_state="contained conviction",
        symbolic_role="threshold mirror",
        contradiction_value="polished expert authority versus exposure risk",
        brand_alignment_constraints=["paper-cut texture", "no stock atmosphere", "source truth stays primary"],
        source_constraints=["searxng:image-category:public-context", "source_win_rate:min:0.7", "no_old_execution_service"],
        licensing_requirements=["direct_use_license_or_reference_only", "provenance_required"],
        query_terms=["founder exposure risk visual metaphor", "paper cut threshold"],
        known_person_name="Claude Ntahuga",
        actor_id=uuid4(),
    )


def _score(**overrides):
    values = {
        "emotional_mode_match": 0.91,
        "tribal_cultural_proximity": 0.84,
        "symbolic_role_fit": 0.89,
        "visual_congruence": 0.88,
        "authenticity": 0.86,
        "source_quality": 0.92,
        "brand_alignment": 0.9,
        "known_person_validity": 0.93,
        "source_win_rate": 0.87,
        "scoring_rationale": "SVRE/Aurore fixture balances emotional mode, cultural proximity, symbolic fit, authenticity, source quality, brand alignment, known-person validity, and source win rate.",
    }
    values.update(overrides)
    return values


def _candidate_payloads():
    return [
        {
            "source_url_or_ref": "https://example.com/licensed-threshold-image",
            "candidate_uri": "object://visual-research/licensed-threshold.png",
            "license_tier": LicenseTier.royalty_free.value,
            "provenance_summary": "Royalty-free image with source page, author, and retrieved hash.",
            "direct_use_requested": True,
            "evidence_refs": ["source:url:licensed-threshold", "license:royalty-free"],
            "provider_route": "gpt_image_2.image_generation.v1",
            "score_fields": _score(),
        },
        {
            "source_url_or_ref": "https://example.com/reference-only-board",
            "candidate_uri": "object://visual-research/reference-board.png",
            "license_tier": LicenseTier.unknown.value,
            "provenance_summary": "Pinterest/source-search reference has provenance but no direct-use license.",
            "direct_use_requested": True,
            "evidence_refs": ["source:url:reference-board"],
            "provider_route": "ideogram_4.composition_plate.v1",
            "score_fields": _score(emotional_mode_match=0.87, known_person_validity=0.9, source_win_rate=0.72),
        },
        {
            "source_url_or_ref": "https://example.com/restricted-person-image",
            "candidate_uri": "object://visual-research/restricted-person.png",
            "license_tier": LicenseTier.restricted.value,
            "provenance_summary": "Known-person image is restricted for final render.",
            "direct_use_requested": True,
            "evidence_refs": ["source:url:restricted-person", "license:restricted"],
            "provider_route": "qwen_image_layered.layer_generation.v1",
            "score_fields": _score(known_person_validity=0.4, source_quality=0.44),
        },
    ]


def test_visual_research_query_contains_scene_asset_roll_emotion_symbolic_contradiction_brand_source_and_license_fields():
    service = VisualResearchService(_provider_ops())
    scene_spec_id = uuid4()

    query = _query(service, scene_spec_id)

    assert query.scene_spec_id == scene_spec_id
    assert query.asset_roll_role == "b_roll"
    assert query.emotional_state == "contained conviction"
    assert query.symbolic_role == "threshold mirror"
    assert query.contradiction_value == "polished expert authority versus exposure risk"
    assert "source truth stays primary" in query.brand_alignment_constraints
    assert "searxng:image-category:public-context" in query.source_constraints
    assert "direct_use_license_or_reference_only" in query.licensing_requirements
    assert query.legacy_adapter_route == LEGACY_ADAPTER_ROUTE


def test_visual_candidates_are_scored_across_svre_aurore_dimensions():
    service = VisualResearchService(_provider_ops())
    query = _query(service, uuid4())
    license_decision = service.record_licensing_decision(
        visual_research_query_id=query.visual_research_query_id,
        source_url_or_ref="https://example.com/licensed-threshold-image",
        license_tier=LicenseTier.owned,
        provenance_summary="Owned asset with internal source hash.",
        evidence_refs=["asset:owned", "source_hash:sha256-owned"],
        actor_id=uuid4(),
    )

    candidate = service.score_visual_candidate(
        visual_research_query_id=query.visual_research_query_id,
        source_url_or_ref="https://example.com/licensed-threshold-image",
        candidate_uri="object://visual-research/licensed-threshold.png",
        provenance_summary="Owned asset with internal source hash.",
        licensing_decision_id=license_decision.licensing_decision_id,
        provider_route="gpt_image_2.image_generation.v1",
        score_fields=_score(),
        actor_id=uuid4(),
    )
    score = service.repository.scores[candidate.score_id]

    assert candidate.use_mode == CandidateUseMode.direct_use
    assert score.emotional_mode_match == 0.91
    assert score.tribal_cultural_proximity == 0.84
    assert score.symbolic_role_fit == 0.89
    assert score.visual_congruence == 0.88
    assert score.authenticity == 0.86
    assert score.source_quality == 0.92
    assert score.brand_alignment == 0.9
    assert score.known_person_validity == 0.93
    assert score.total_score > 0.85


def test_unlicensed_candidate_cannot_be_routed_as_direct_use():
    service = VisualResearchService(_provider_ops())
    query = _query(service, uuid4())
    receipt = service.run_asset_research(
        visual_research_query_id=query.visual_research_query_id,
        candidates=[_candidate_payloads()[1]],
        actor_id=uuid4(),
        downstream_render_route="composition_reference_to_ideogram_4",
    )

    manifest = service.repository.manifests[receipt.asset_research_manifest_id]
    image_map = service.repository.image_resolution_maps[receipt.image_resolution_map_id]
    selected = service.repository.candidates[manifest.selected_candidate_id]
    license_decision = service.repository.licensing_decisions[selected.license_decision_id]

    assert selected.use_mode == CandidateUseMode.composition_reference_only
    assert license_decision.direct_use_allowed is False
    assert "DIRECT_USE_LICENSE_NOT_AVAILABLE" in license_decision.blocker_codes
    assert image_map.direct_use_asset_uri is None
    assert image_map.composition_reference_uri == selected.candidate_uri


def test_legacy_svre_aurore_execution_routes_are_blocked_while_current_provider_routes_are_allowed():
    service = VisualResearchService(_provider_ops())
    query = _query(service, uuid4())
    license_decision = service.record_licensing_decision(
        visual_research_query_id=query.visual_research_query_id,
        source_url_or_ref="https://example.com/licensed",
        license_tier=LicenseTier.owned,
        provenance_summary="Owned source.",
        evidence_refs=["asset:owned"],
        actor_id=uuid4(),
    )

    with pytest.raises(VisualResearchError) as exc:
        service.score_visual_candidate(
            visual_research_query_id=query.visual_research_query_id,
            source_url_or_ref="https://example.com/licensed",
            candidate_uri="object://visual-research/licensed.png",
            provenance_summary="Owned source.",
            licensing_decision_id=license_decision.licensing_decision_id,
            provider_route="svre_legacy_executor",
            score_fields=_score(),
            actor_id=uuid4(),
        )

    assert exc.value.code == "LEGACY_EXECUTION_ROUTE_BLOCKED"

    candidate = service.score_visual_candidate(
        visual_research_query_id=query.visual_research_query_id,
        source_url_or_ref="https://example.com/licensed",
        candidate_uri="object://visual-research/licensed.png",
        provenance_summary="Owned source.",
        licensing_decision_id=license_decision.licensing_decision_id,
        provider_route="gpt_image_2.image_generation.v1",
        score_fields=_score(),
        actor_id=uuid4(),
    )
    assert "svre:t-score" in candidate.superseded_legacy_logic_refs


def test_manifest_image_resolution_map_and_render_contract_link_selected_alternatives_scores_license_source_and_route():
    _scene_service, _planner, compiler, _org_id, _brand_id, actor_id, scene_spec = _scene_intelligence_fixture()
    service = VisualResearchService(_provider_ops(), scene_spec_compiler=compiler)
    query = _query(service, scene_spec.scene_spec_id)

    receipt = service.run_asset_research(
        visual_research_query_id=query.visual_research_query_id,
        candidates=_candidate_payloads(),
        actor_id=actor_id,
        downstream_render_route="asset_research_to_render_contract",
    )

    manifest = service.repository.manifests[receipt.asset_research_manifest_id]
    image_map = service.repository.image_resolution_maps[receipt.image_resolution_map_id]
    contract = compiler.render_contract_for_scene(scene_spec.scene_spec_id)

    assert manifest.selected_candidate_id == receipt.selected_candidate_id
    assert manifest.alternative_candidate_ids
    assert manifest.rejected_candidate_reasons
    assert manifest.scoring_receipt_refs == receipt.score_ids
    assert manifest.license_decision_refs == receipt.license_decision_ids
    assert image_map.source_url_or_ref == "https://example.com/licensed-threshold-image"
    assert image_map.downstream_render_route == "asset_research_to_render_contract"
    assert contract.renderer_props["asset_research_manifest_id"] == str(manifest.asset_research_manifest_id)
    assert contract.renderer_props["image_resolution_map_id"] == str(image_map.image_resolution_map_id)


def test_provider_job_workflow_stage11_asset_research_runs_query_to_receipt():
    provider_ops = _provider_ops()
    service = VisualResearchService(provider_ops)
    query = _query(service, uuid4())
    workflow = ProviderJobWorkflow(provider_ops, visual_research_service=service)

    receipt = workflow.stage11_asset_research(
        visual_research_query_id=query.visual_research_query_id,
        candidates=_candidate_payloads(),
        actor_id=uuid4(),
        downstream_render_route="asset_research_to_render_contract",
    )

    assert receipt.decision_code == "ASSET_RESEARCH_MANIFEST_WRITTEN"
    assert receipt.legacy_adapter_route == LEGACY_ADAPTER_ROUTE
    assert "gpt_image_2.image_generation.v1" in receipt.provider_routes


def test_visual_research_command_bus_emits_asset_research_receipt_event():
    provider_ops = _provider_ops()
    service = VisualResearchService(provider_ops)
    org_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    query = _query(service, uuid4())
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_visual_research_command_handlers(bus, service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["production_steward"])
    envelope = new_command_envelope(
        command_type="RunAssetResearchCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "visual_research_query_id": str(query.visual_research_query_id),
            "candidates": _candidate_payloads(),
            "downstream_render_route": "asset_research_to_render_contract",
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["asset_research_manifest_id"]
    assert result.result_payload["image_resolution_map_id"]
    assert bus.event_outbox.events[-1].event_type == "RunAssetResearchCommand.succeeded"
