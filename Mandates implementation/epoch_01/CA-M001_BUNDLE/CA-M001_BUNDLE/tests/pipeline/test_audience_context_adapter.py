"""CA-M001 / Q01 tests for the immutable three-layer Audience Context boundary."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from cmf_pipeline.adapters import (
    AudienceContext,
    AudienceContextAdapter,
    AudienceContextAdmissionError,
    AudienceContextMutationError,
    LiveAudienceTensions,
    MarketMacroSignals,
    SegmentCulturalArchetypes,
    SyntheticDeterministicAdapter,
)
from cmf_pipeline.workflow.infrastructure.repository import PipelineRepository


def _layer_triplet(*, version: int = 1):
    market = MarketMacroSignals.create(
        workspace_id="workspace-test",
        audience_id="audience-test",
        version=version,
        payload={
            "economic_cycle": "tightening",
            "industry_trend": "measured_growth",
            "signal_strength": 7,
        },
        provenance_refs=("src:macro:001",),
    )
    archetypes = SegmentCulturalArchetypes.create(
        workspace_id="workspace-test",
        audience_id="audience-test",
        version=version,
        payload={
            "dominant_values": ["craft", "agency"],
            "decision_style": "deliberate",
        },
        provenance_refs=("src:segment:001",),
    )
    tensions = LiveAudienceTensions.create(
        workspace_id="workspace-test",
        audience_id="audience-test",
        version=version,
        payload={
            "unresolved_friction": "trust_gap",
            "urgency": 8,
        },
        provenance_refs=("src:tension:001",),
    )
    return market, archetypes, tensions


def _context(*, version: int = 1) -> AudienceContext:
    market, archetypes, tensions = _layer_triplet(version=version)
    return AudienceContext.create(
        workspace_id="workspace-test",
        audience_id="audience-test",
        version=version,
        market_macro_signals=market,
        segment_cultural_archetypes=archetypes,
        live_audience_tensions=tensions,
    )


def test_positive_path_creates_three_independent_digest_pinned_layers() -> None:
    context = _context()

    assert context.market_macro_signals.KIND == "MARKET_MACRO_SIGNALS"
    assert context.segment_cultural_archetypes.KIND == "SEGMENT_CULTURAL_ARCHETYPES"
    assert context.live_audience_tensions.KIND == "LIVE_AUDIENCE_TENSIONS"

    digests = {
        context.market_macro_signals.layer_sha256,
        context.segment_cultural_archetypes.layer_sha256,
        context.live_audience_tensions.layer_sha256,
    }
    assert len(digests) == 3
    assert len({layer.layer_id for layer in (
        context.market_macro_signals,
        context.segment_cultural_archetypes,
        context.live_audience_tensions,
    )}) == 3

    canonical = context.to_dict()
    assert set(canonical["layers"]) == {
        "market_macro_signals",
        "segment_cultural_archetypes",
        "live_audience_tensions",
    }
    for reference in canonical["layers"].values():
        assert set(reference) == {
            "object_id",
            "revision",
            "version",
            "semantic_version",
            "sha256",
        }
        assert "payload" not in reference


def test_operator_projection_exposes_layers_separately_with_provenance() -> None:
    projection = _context().operator_projection()

    assert set(projection["layers"]) == {
        "market_macro_signals",
        "segment_cultural_archetypes",
        "live_audience_tensions",
    }
    for layer in projection["layers"].values():
        assert layer["revision"] == 1
        assert len(layer["sha256"]) == 64
        assert len(layer["payload_sha256"]) == 64
        assert layer["provenance_refs"]


def test_immutable_revision_rejects_in_place_mutation_and_returns_fresh_payload_views() -> None:
    context = _context()

    with pytest.raises(FrozenInstanceError):
        context.market_macro_signals = context.market_macro_signals.revise(payload={"changed": True})  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        context.market_macro_signals.payload_json = "{}"  # type: ignore[misc]

    view = context.market_macro_signals.to_dict()
    view["payload"]["economic_cycle"] = "mutated-outside"
    assert context.market_macro_signals.to_dict()["payload"]["economic_cycle"] == "tightening"

    revised = context.market_macro_signals.revise(
        payload={
            "economic_cycle": "easing",
            "industry_trend": "measured_growth",
            "signal_strength": 7,
        }
    )
    assert revised is not context.market_macro_signals
    assert revised.layer_id == context.market_macro_signals.layer_id
    assert revised.version == 2
    assert revised.layer_sha256 != context.market_macro_signals.layer_sha256
    assert context.market_macro_signals.version == 1


def test_conflicting_layer_identity_is_rejected() -> None:
    market, _, tensions = _layer_triplet()
    with pytest.raises(AudienceContextAdmissionError, match="three explicit layer types"):
        AudienceContext.create(
            workspace_id="workspace-test",
            audience_id="audience-test",
            market_macro_signals=market,
            segment_cultural_archetypes=market,  # type: ignore[arg-type]
            live_audience_tensions=tensions,
        )


def test_blended_or_missing_layer_representation_fails_closed() -> None:
    context = _context()
    payload = context.to_dict()

    blended = dict(payload)
    blended["layers"] = dict(payload["layers"])
    blended["layers"]["market_macro_signals"] = {
        **blended["layers"]["market_macro_signals"],
        "payload": context.market_macro_signals.to_dict()["payload"],
    }
    with pytest.raises(AudienceContextAdmissionError, match="embedded audience content"):
        AudienceContext.from_reference_payload(
            blended,
            market_macro_signals=context.market_macro_signals,
            segment_cultural_archetypes=context.segment_cultural_archetypes,
            live_audience_tensions=context.live_audience_tensions,
        )

    missing = dict(payload)
    missing["layers"] = dict(payload["layers"])
    missing["layers"].pop("live_audience_tensions")
    with pytest.raises(AudienceContextAdmissionError, match="exactly the three governed layers"):
        AudienceContext.from_reference_payload(
            missing,
            market_macro_signals=context.market_macro_signals,
            segment_cultural_archetypes=context.segment_cultural_archetypes,
            live_audience_tensions=context.live_audience_tensions,
        )


def test_tampered_layer_digest_is_rejected() -> None:
    payload = _context().market_macro_signals.to_dict()
    payload["payload"]["economic_cycle"] = "tampered"

    with pytest.raises(
        AudienceContextMutationError,
        match="payload digest mismatch|layer digest mismatch",
    ):
        MarketMacroSignals.from_dict(payload)


def test_persistence_and_reload_preserve_exact_layer_revisions_and_digests(tmp_path) -> None:
    repository = PipelineRepository(tmp_path / "pipeline.sqlite3")
    context_v1 = _context(version=1)

    first = AudienceContextAdapter.persist(
        context_v1,
        repository,
        idempotency_key="ca-m001:audience-test:v1",
    )
    assert first["context"]["created"] is True
    assert repository.get_object(context_v1.context_id, revision=1)["revision"] == 1

    repository_after_reload = PipelineRepository(tmp_path / "pipeline.sqlite3")
    context_v1_reloaded = AudienceContextAdapter.read(
        repository_after_reload,
        workspace_id="workspace-test",
        audience_id="audience-test",
        version=1,
    )
    assert context_v1_reloaded.to_dict() == context_v1.to_dict()
    assert context_v1_reloaded.market_macro_signals.layer_sha256 == context_v1.market_macro_signals.layer_sha256
    assert context_v1_reloaded.segment_cultural_archetypes.layer_sha256 == context_v1.segment_cultural_archetypes.layer_sha256
    assert context_v1_reloaded.live_audience_tensions.layer_sha256 == context_v1.live_audience_tensions.layer_sha256

    market_v2 = context_v1.market_macro_signals.revise(
        payload={
            "economic_cycle": "easing",
            "industry_trend": "measured_growth",
            "signal_strength": 8,
        }
    )
    context_v2 = context_v1.revise(market_macro_signals=market_v2)

    second = AudienceContextAdapter.persist(
        context_v2,
        repository,
        idempotency_key="ca-m001:audience-test:v2",
    )
    assert second["context"]["created"] is True

    historical_market = repository.get_object(
        context_v1.market_macro_signals.layer_id,
        revision=1,
    )
    current_market = repository.get_object(
        context_v2.market_macro_signals.layer_id,
        revision=2,
    )
    assert historical_market["payload"] == context_v1.market_macro_signals.to_dict()
    assert current_market["payload"] == context_v2.market_macro_signals.to_dict()
    assert historical_market["canonical_sha256"] != current_market["canonical_sha256"]

    repository_after_revision = PipelineRepository(tmp_path / "pipeline.sqlite3")
    reloaded_v2 = AudienceContextAdapter.read(
        repository_after_revision,
        workspace_id="workspace-test",
        audience_id="audience-test",
    )
    assert reloaded_v2.version == 2
    assert reloaded_v2.market_macro_signals.version == 2
    assert reloaded_v2.market_macro_signals.layer_sha256 == context_v2.market_macro_signals.layer_sha256
    assert reloaded_v2.segment_cultural_archetypes.version == 1
    assert reloaded_v2.live_audience_tensions.version == 1



def test_persist_rejects_changed_payload_reusing_an_existing_revision(tmp_path) -> None:
    repository = PipelineRepository(tmp_path / "pipeline.sqlite3")
    context_v1 = _context(version=1)
    AudienceContextAdapter.persist(
        context_v1,
        repository,
        idempotency_key="ca-m001:audience-test:stable-v1",
    )

    tampered_market = MarketMacroSignals.create(
        workspace_id="workspace-test",
        audience_id="audience-test",
        version=1,
        payload={
            "economic_cycle": "easing",
            "industry_trend": "measured_growth",
            "signal_strength": 99,
        },
        provenance_refs=("src:macro:001",),
    )
    tampered_context = context_v1.revise(
        market_macro_signals=tampered_market,
    )
    tampered_context_same_version = AudienceContext.create(
        workspace_id=tampered_context.workspace_id,
        audience_id=tampered_context.audience_id,
        version=1,
        market_macro_signals=tampered_market,
        segment_cultural_archetypes=context_v1.segment_cultural_archetypes,
        live_audience_tensions=context_v1.live_audience_tensions,
    )

    with pytest.raises(AudienceContextMutationError):
        AudienceContextAdapter.persist(
            tampered_context_same_version,
            repository,
            idempotency_key="ca-m001:audience-test:stable-v1-tampered",
        )


def test_adjacent_synthetic_adapter_behavior_remains_compatible() -> None:
    result = SyntheticDeterministicAdapter().execute(
        node_id="node-1",
        input_refs=[{"object_id": "z-ref"}, {"object_id": "a-ref"}],
    )

    assert result["node_id"] == "node-1"
    assert result["input_ref_ids"] == ["a-ref", "z-ref"]
    assert result["classification"] == "SYNTHETIC_DEVELOPMENT_EVIDENCE"
    assert result["real_artifact"] is False
    assert result["synthetic_result_id"].startswith("synthetic:")
    assert len(result["payload_sha256"]) == 64
