"""M0084 focused tests for source-quality-aware transformation bounds."""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "packages/ca_runtime/src/ca_runtime/storyboard_session.py"


def _load_storyboard_module():
    """Load the scoped module without importing the DB-backed ca_runtime package."""
    package = types.ModuleType("ca_runtime")
    package.__path__ = [str(MODULE_PATH.parent)]
    sys.modules.setdefault("ca_runtime", package)

    editorial = types.ModuleType("ca_runtime.editorial_discovery_store")

    class EditorialDiscoveryStore:  # pragma: no cover - import-only stub
        pass

    editorial.EditorialDiscoveryStore = EditorialDiscoveryStore
    sys.modules.setdefault("ca_runtime.editorial_discovery_store", editorial)

    preparation = types.ModuleType("ca_runtime.preparation_graph_store")

    class GraphRevisionRecord:  # pragma: no cover - import-only stub
        pass

    class PreparationGraphStore:  # pragma: no cover - import-only stub
        pass

    class StaleBaseRevisionError(Exception):  # pragma: no cover - import-only stub
        pass

    preparation.GraphRevisionRecord = GraphRevisionRecord
    preparation.PreparationGraphStore = PreparationGraphStore
    preparation.StaleBaseRevisionError = StaleBaseRevisionError
    sys.modules.setdefault("ca_runtime.preparation_graph_store", preparation)

    spec = importlib.util.spec_from_file_location("ca_runtime.storyboard_session", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


m0084 = _load_storyboard_module()


@pytest.fixture
def high_profile():
    return m0084.SourceQualityProfile(
        profile_id="sq-high-01",
        source_ref="asset-01",
        width_px=3840,
        height_px=2160,
        frame_rate_milli_fps=30000,
        crop_count=0,
        crop_retention_bps=10000,
        compression_loss_bps=500,
        sharpness_bps=9000,
        prior_degradation_bps=0,
        evidence_refs=["seg-01"],
    )


def test_high_quality_source_allows_subtle_zoom_and_reframe(high_profile):
    recipe = m0084.TransformationRecipe(
        recipe_id="recipe-high",
        intent_id="intent-01",
        primitives=[
            {"op": "ZOOM", "amount_bps": 1200},
            {"op": "REFRAME", "reframe_bps": 1200},
            {"op": "COLOR", "treatment": "SUBTLE_LUT"},
        ],
    )
    result = m0084.validate_transformation_for_source_quality(high_profile, recipe)
    assert result.allowed is True
    assert result.source_quality_level == "HIGH"
    assert result.max_scale_delta_bps == 1200


def test_low_quality_aggressive_zoom_is_rejected_even_when_it_looks_clean():
    profile = m0084.SourceQualityProfile(
        profile_id="sq-low-01",
        source_ref="asset-02",
        width_px=854,
        height_px=480,
        frame_rate_milli_fps=24000,
        crop_count=2,
        crop_retention_bps=6000,
        compression_loss_bps=4000,
        sharpness_bps=5000,
        prior_degradation_bps=2500,
        evidence_refs=["seg-02"],
    )
    recipe = m0084.TransformationRecipe(
        recipe_id="recipe-wrong",
        intent_id="intent-02",
        primitives=[{"op": "ZOOM", "amount_bps": 5000}],
    )
    result = m0084.validate_transformation_for_source_quality(profile, recipe)
    assert result.allowed is False
    assert any("scale_delta_bps" in violation for violation in result.violations)
    assert "INSET" in result.recommended_presentation_strategies


def test_degraded_source_adaptation_is_deterministic_and_preserves_intent():
    profile = m0084.SourceQualityProfile(
        profile_id="sq-degraded-01",
        source_ref="asset-03",
        width_px=640,
        height_px=360,
        frame_rate_milli_fps=15000,
        crop_count=3,
        crop_retention_bps=4500,
        compression_loss_bps=6500,
        sharpness_bps=3000,
        prior_degradation_bps=6000,
        evidence_refs=["seg-03"],
    )
    recipe = m0084.TransformationRecipe(
        recipe_id="recipe-degraded",
        intent_id="intent-03",
        primitives=[
            {"op": "ZOOM", "amount_bps": 4000},
            {"op": "REFRAME", "reframe_bps": 1800},
            {"op": "COLOR", "treatment": "SUBTLE_LUT"},
            {"op": "MOTION", "motion_amplitude_bps": 2200},
        ],
        constraints={"semantic_lock": "keep_source_evidence"},
    )
    original = recipe.model_dump()
    adapted_a = m0084.adapt_transformation_recipe_for_source_quality(profile, recipe)
    adapted_b = m0084.adapt_transformation_recipe_for_source_quality(profile, recipe)
    assert recipe.model_dump() == original
    assert adapted_a.model_dump() == adapted_b.model_dump()
    assert adapted_a.intent_id == recipe.intent_id
    assert adapted_a.constraints["source_quality_level"] == "DEGRADED"
    assert adapted_a.constraints["source_quality_profile_id"] == profile.profile_id
    assert adapted_a.constraints["source_quality_evidence_refs"] == profile.evidence_refs
    assert adapted_a.constraints["presentation_strategy"] == "CONTAINERIZED"
    assert adapted_a.primitives[0]["amount_bps"] == 150
    assert adapted_a.primitives[2]["treatment"] == "NONE"
    assert adapted_a.primitives[3]["motion_amplitude_bps"] == 0


def test_profile_requires_valid_measured_metadata_and_evidence():
    with pytest.raises(ValueError, match="source dimensions must be positive"):
        m0084.SourceQualityProfile(
            profile_id="sq-invalid",
            source_ref="asset-invalid",
            width_px=0,
            height_px=1080,
            frame_rate_milli_fps=24000,
            evidence_refs=["seg-invalid"],
        )

    with pytest.raises(ValueError, match="between 0 and 10000"):
        m0084.SourceQualityProfile(
            profile_id="sq-invalid-2",
            source_ref="asset-invalid",
            width_px=1920,
            height_px=1080,
            frame_rate_milli_fps=24000,
            compression_loss_bps=10001,
            evidence_refs=["seg-invalid"],
        )

    with pytest.raises(ValueError, match="evidence_refs"):
        m0084.SourceQualityProfile(
            profile_id="sq-invalid-3",
            source_ref="asset-invalid",
            width_px=1920,
            height_px=1080,
            frame_rate_milli_fps=24000,
        )


def test_asset_quality_profile_cannot_be_rebound_to_another_source():
    profile = m0084.SourceQualityProfile(
        profile_id="sq-lineage-01",
        source_ref="asset-authorized",
        width_px=1920,
        height_px=1080,
        frame_rate_milli_fps=30000,
        evidence_refs=["seg-01"],
    )
    asset = m0084.VisualAssetReference(
        reference_id="ref-01",
        asset_id="asset-other",
        evidence_refs=["seg-01"],
        source_quality_profile=profile,
    )
    with pytest.raises(m0084.StoryboardRevisionValidationError, match="another source"):
        store = object.__new__(m0084.StoryboardSessionStore)
        store._validate_revision_input(
            session=m0084.StoryboardSession(
                workspace_id="ws-01",
                session_id="session-01",
                editorial_storyboard_id="storyboard-01",
                graph_id="graph-01",
                created_by="operator",
            ),
            scenes=[
                m0084.StoryboardScene(
                    scene_id="scene-01",
                    scene_order=0,
                    semantic_purpose="Preserve evidence.",
                    source_evidence_refs=["seg-01"],
                    shots=[
                        m0084.StoryboardShot(
                            shot_id="shot-01",
                            start_ms=0,
                            end_ms=1000,
                            semantic_purpose="Show source.",
                            elements=[
                                m0084.StoryboardElement(
                                    element_id="element-01",
                                    kind="SOURCE_FRAME",
                                    semantic_purpose="Show source.",
                                    source_evidence_refs=["seg-01"],
                                    asset_references=[asset],
                                )
                            ],
                        )
                    ],
                )
            ],
            source_evidence_refs=["seg-01"],
        )


def test_clean_1080p_profile_is_high_and_can_use_the_subtle_path():
    profile = m0084.SourceQualityProfile(
        profile_id="sq-1080-01",
        source_ref="asset-1080",
        width_px=1920,
        height_px=1080,
        frame_rate_milli_fps=30000,
        crop_count=0,
        crop_retention_bps=10000,
        compression_loss_bps=300,
        sharpness_bps=9200,
        prior_degradation_bps=0,
        evidence_refs=["seg-1080"],
    )
    assert profile.quality_level == "HIGH"
    assert "SUBTLE_REFRAME" in profile.presentation_strategies


def test_storyboard_revision_gate_rejects_quality_damaging_recipe():
    profile = m0084.SourceQualityProfile(
        profile_id="sq-gate-01",
        source_ref="asset-gate",
        width_px=854,
        height_px=480,
        frame_rate_milli_fps=24000,
        crop_count=1,
        crop_retention_bps=6200,
        compression_loss_bps=3500,
        sharpness_bps=5000,
        prior_degradation_bps=2000,
        evidence_refs=["seg-gate"],
    )
    element = m0084.StoryboardElement(
        element_id="element-gate",
        kind="SOURCE_FRAME",
        semantic_purpose="Make the evidence visible.",
        source_evidence_refs=["seg-gate"],
        asset_references=[
            m0084.VisualAssetReference(
                reference_id="ref-gate",
                asset_id="asset-gate",
                evidence_refs=["seg-gate"],
                source_quality_profile=profile,
            )
        ],
        transformation_intent=m0084.TransformationIntent(
            intent_id="intent-gate",
            source_element_id="element-gate",
            semantic_target="Evidence region",
            mode="FOCUS",
        ),
        transformation_recipe=m0084.TransformationRecipe(
            recipe_id="recipe-gate",
            intent_id="intent-gate",
            primitives=[{"op": "ZOOM", "amount_bps": 1800}],
        ),
    )
    store = object.__new__(m0084.StoryboardSessionStore)
    with pytest.raises(m0084.StoryboardRevisionValidationError, match="source-quality limits"):
        store._validate_revision_input(
            session=m0084.StoryboardSession(
                workspace_id="ws-gate",
                session_id="session-gate",
                editorial_storyboard_id="storyboard-gate",
                graph_id="graph-gate",
                created_by="operator",
            ),
            scenes=[
                m0084.StoryboardScene(
                    scene_id="scene-gate",
                    scene_order=0,
                    semantic_purpose="Preserve source evidence.",
                    source_evidence_refs=["seg-gate"],
                    shots=[
                        m0084.StoryboardShot(
                            shot_id="shot-gate",
                            start_ms=0,
                            end_ms=1000,
                            semantic_purpose="Reveal the evidence.",
                            elements=[element],
                        )
                    ],
                )
            ],
            source_evidence_refs=["seg-gate"],
        )


def test_quality_measurements_materially_change_quality_band():
    clean = m0084.SourceQualityProfile(
        profile_id="sq-clean", source_ref="asset-quality", width_px=1920, height_px=1080,
        frame_rate_milli_fps=30000, crop_count=0, crop_retention_bps=10000,
        compression_loss_bps=0, sharpness_bps=10000, prior_degradation_bps=0, evidence_refs=["seg-quality"],
    )
    degraded = clean.model_copy(update={
        "crop_count": 3, "crop_retention_bps": 4500, "compression_loss_bps": 5000,
        "sharpness_bps": 3500, "frame_rate_milli_fps": 15000, "prior_degradation_bps": 5000,
    })
    assert clean.quality_score_bps > degraded.quality_score_bps
    assert clean.quality_level == "HIGH"
    assert degraded.quality_level in {"LOW", "DEGRADED"}


def test_sensitive_primitive_without_declared_intensity_is_rejected():
    profile = m0084.SourceQualityProfile(
        profile_id="sq-undeclared", source_ref="asset-undeclared", width_px=1920, height_px=1080,
        frame_rate_milli_fps=30000, evidence_refs=["seg-undeclared"],
    )
    recipe = m0084.TransformationRecipe(
        recipe_id="recipe-undeclared", intent_id="intent-undeclared", primitives=[{"op": "ZOOM"}],
    )
    result = m0084.validate_transformation_for_source_quality(profile, recipe)
    assert result.allowed is False
    assert any("must declare amount_bps" in violation for violation in result.violations)


