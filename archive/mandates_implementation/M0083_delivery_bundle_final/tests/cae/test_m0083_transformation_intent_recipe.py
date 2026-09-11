"""M0083 acceptance tests for the bounded transformation projection layer."""

from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path

import pytest


# The supplied snapshot is missing the optional psycopg runtime dependency.
# M0083 is a pure contract/compiler layer, so load only CAE runtime submodules
# required by the canonical storyboard models and bypass package __init__.
ROOT = Path(__file__).resolve().parents[2]
RUNTIME_SRC = ROOT / "packages" / "ca_runtime" / "src" / "ca_runtime"
CONTRACTS_SRC = ROOT / "packages" / "ca_contracts" / "src"
if str(CONTRACTS_SRC) not in sys.path:
    sys.path.insert(0, str(CONTRACTS_SRC))
if "ca_runtime" not in sys.modules or not hasattr(sys.modules["ca_runtime"], "__path__"):
    pkg = types.ModuleType("ca_runtime")
    pkg.__path__ = [str(RUNTIME_SRC)]
    pkg.__package__ = "ca_runtime"
    sys.modules["ca_runtime"] = pkg

storyboard_session = importlib.import_module("ca_runtime.storyboard_session")
transformation_recipe = importlib.import_module("ca_runtime.transformation_recipe")

TransformationIntent = storyboard_session.TransformationIntent
TransformationRecipeCompiler = transformation_recipe.TransformationRecipeCompiler
TransformationRecipeRegistry = transformation_recipe.TransformationRecipeRegistry
TRANSFORMATION_RECIPE_REGISTRY_VERSION = transformation_recipe.TRANSFORMATION_RECIPE_REGISTRY_VERSION
TransformationAuthorizationError = transformation_recipe.TransformationAuthorizationError
TransformationConstraintError = transformation_recipe.TransformationConstraintError
TransformationModeMismatchError = transformation_recipe.TransformationModeMismatchError
SourceQualityRequiredError = transformation_recipe.SourceQualityRequiredError
StaleTransformationRecipeRegistryError = transformation_recipe.StaleTransformationRecipeRegistryError


BASE_INTENT = dict(
    intent_id="intent-01",
    source_element_id="element-01",
    intent="FOCUS",
    semantic_target="show the false alarm mechanism",
    mode="REFRAME",
    emphasis="MECHANISM",
    motion="SUBTLE_ZOOM",
    constraints={"source_quality": "HIGH"},
)


def _intent(**overrides):
    payload = {**BASE_INTENT, **overrides}
    return TransformationIntent(**payload)


def test_registry_covers_all_declared_intents_with_approved_primitives():
    registry = TransformationRecipeRegistry()
    declared = set(storyboard_session.TRANSFORMATION_INTENTS)
    resolved = {registry.resolve(intent).template_id for intent in declared}
    assert len(resolved) == 8
    for intent in declared:
        template = registry.resolve(intent)
        assert template.intents
        assert set(template.primitive_ops).issubset(
            {
                "EXTRACT_REGION",
                "REFRAME",
                "HIGHLIGHT",
                "SIDE_BY_SIDE",
                "ANNOTATE",
                "INSET",
                "CONNECTOR",
                "MASK_REGION",
                "CUT",
                "RETURN",
                "HOLD",
            }
        )


def test_every_declared_intent_compiles_to_a_registered_recipe():
    compiler = TransformationRecipeCompiler()
    for intent_name in sorted(storyboard_session.TRANSFORMATION_INTENTS):
        intent = TransformationIntent(
            intent_id=f"{intent_name.lower()}-01",
            source_element_id="element-01",
            intent=intent_name,
            semantic_target=f"target for {intent_name.lower()}",
            mode="AUTO",
            emphasis="MEANING",
            motion="STATIC",
            constraints={"source_quality": "HIGH"},
        )
        recipe = compiler.compile(intent)
        assert recipe.governed is True
        assert recipe.template_id
        assert recipe.recipe_sha256


def test_focus_intent_compiles_to_governed_recipe_and_deterministic_keyframes():
    compiler = TransformationRecipeCompiler()
    recipe = compiler.compile(_intent())

    assert recipe.governed is True
    assert recipe.registry_version == TRANSFORMATION_RECIPE_REGISTRY_VERSION
    assert recipe.template_id == "FOCUS_TARGET_V1"
    assert [primitive["op"] for primitive in recipe.primitives] == ["REFRAME", "HIGHLIGHT"]
    assert recipe.keyframes == [
        {"at_bps": 0, "template": "SCALE", "scale_bps": 10000},
        {"at_bps": 10000, "template": "SCALE", "scale_bps": 10700},
    ]
    assert recipe.recipe_sha256

    replay = compiler.compile(_intent())
    assert replay.model_dump() == recipe.model_dump()


def test_legacy_m0079_mode_shape_is_normalized_without_new_authority():
    intent = TransformationIntent(
        intent_id="legacy-01",
        source_element_id="element-01",
        semantic_target="show the mechanism",
        mode="FOCUS",
        emphasis="MECHANISM",
    )
    assert intent.intent == "FOCUS"
    assert intent.mode == "AUTO"
    assert intent.source == "element-01"


def test_good_looking_but_wrong_mode_is_rejected_fail_closed():
    # A comparison can be visually polished but is not an approved projection
    # of FOCUS.  The recipe compiler must not infer its way around the mismatch.
    with pytest.raises(TransformationModeMismatchError):
        TransformationRecipeCompiler().compile(
            _intent(intent="FOCUS", mode="COMPARE")
        )


def test_unauthorized_recipe_is_rejected_before_compilation_output():
    with pytest.raises(TransformationAuthorizationError):
        TransformationRecipeCompiler().compile(
            _intent(),
            authorized_recipe_ids=["CONTRAST_SOURCES_V1"],
        )


def test_stale_registry_is_rejected():
    with pytest.raises(StaleTransformationRecipeRegistryError):
        TransformationRecipeCompiler().compile(
            _intent(),
            expected_registry_version="M0079-legacy",
        )


def test_motion_requires_explicit_source_quality():
    with pytest.raises(SourceQualityRequiredError):
        TransformationRecipeCompiler().compile(
            _intent(constraints={}),
        )


def test_low_quality_source_suppresses_zoom_deterministically():
    recipe = TransformationRecipeCompiler().compile(
        _intent(constraints={"source_quality": "LOW"}),
    )
    assert recipe.motion_template == "STATIC_HOLD"
    assert recipe.constraints["effective_motion"] == "STATIC"
    assert recipe.keyframes[0]["template"] == "HOLD"
    assert recipe.keyframes[1]["template"] == "HOLD"


def test_explicit_scale_limit_clamps_medium_quality_motion():
    recipe = TransformationRecipeCompiler().compile(
        _intent(
            constraints={
                "source_quality": "MEDIUM",
                "max_scale_change_bps": 150,
            }
        )
    )
    assert recipe.keyframes[-1]["scale_bps"] == 10150
    assert recipe.constraints["effective_motion"] == "SUBTLE_ZOOM"


def test_invalid_constraint_key_is_rejected():
    with pytest.raises(TransformationConstraintError):
        TransformationRecipeCompiler().compile(
            _intent(constraints={"freeform_effect": "glow"}),
        )
