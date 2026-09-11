"""M0092 acceptance tests for final-hit storyboard validation and motion compilation."""

from __future__ import annotations

import copy
import sqlite3
import importlib
import sys
import types
from pathlib import Path

import pytest

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

session = importlib.import_module("ca_runtime.storyboard_session")
final_hit = importlib.import_module("ca_runtime.storyboard_final_hit")
grammar = importlib.import_module("ca_runtime.narrative_editing_grammar")

Keyframe = session.Keyframe
MotionPlan = session.MotionPlan
NarrativeGrammarBinding = session.NarrativeGrammarBinding
SourceQualityProfile = session.SourceQualityProfile
StoryboardElement = session.StoryboardElement
StoryboardRevision = session.StoryboardRevision
StoryboardSessionStore = session.StoryboardSessionStore
StoryboardScene = session.StoryboardScene
StoryboardShot = session.StoryboardShot
TransformationIntent = session.TransformationIntent
TransformationRecipe = session.TransformationRecipe
VisualAssetReference = session.VisualAssetReference
validate_final_hit = final_hit.validate_final_hit
FinalHitValidationError = final_hit.FinalHitValidationError

DS_REF = {"object_id": "design-system:cae-default", "version": "1.0.0", "sha256": "d" * 64}
HARNESS = {
    "max_motion_intensity_bps": 1200,
    "max_attention_cost_bps": 1600,
    "max_keyframes": 4,
    "min_legibility_bps": 6000,
    "safe_area": {"x_bps": 500, "y_bps": 500, "width_bps": 9000, "height_bps": 9000},
    "require_design_system": True,
    "require_wrong_reading_locks": True,
}


def _profile(level: str = "HIGH") -> SourceQualityProfile:
    dimensions = {
        "HIGH": (3840, 2160),
        "MEDIUM": (1920, 1080),
        "LOW": (640, 360),
    }[level]
    return SourceQualityProfile(
        profile_id=f"quality:{level.lower()}",
        source_ref="asset:source",
        width_px=dimensions[0],
        height_px=dimensions[1],
        frame_rate_milli_fps=30000,
        evidence_refs=["evidence:source"],
        sharpness_bps=9000,
        compression_loss_bps=500,
    )


def _binding(mode: str = "FOCUS") -> NarrativeGrammarBinding:
    return NarrativeGrammarBinding(
        binding_id="grammar-binding:scene-1",
        scene_id="scene:1",
        grammar_mode=mode,
        grammar_version="1.0.0",
        archetype_id="evidence_focus",
        harness_id="supervisual-harness-v1",
        activative_meaning="make the false alarm mechanism legible",
        editorial_intent="focus the evidence-backed mechanism",
        scene_context="EVIDENCE",
        sequence_index=0,
        evidence_refs=["evidence:source"],
        relation_scene_ids=[],
        wrong_reading_locks=["preserve source claim", "do not replace source evidence"],
    )


def _revision(
    *,
    quality_level: str = "HIGH",
    geometry: dict | None = None,
    element_overrides: dict | None = None,
    motion_plan: MotionPlan | None = None,
    intent: TransformationIntent | None = None,
) -> StoryboardRevision:
    asset = VisualAssetReference(
        reference_id="visual-ref:source",
        asset_id="asset:source",
        source_evidence_refs=["evidence:source"],
        evidence_refs=["evidence:source"],
        rights_status="CLEARED",
        source_quality=quality_level,
        source_quality_profile=_profile(quality_level),
        approved=True,
    )
    base_properties = {
        "geometry": geometry or {"x_bps": 1800, "y_bps": 1600, "width_bps": 5600, "height_bps": 4800},
        "evidence_legibility_bps": 8200,
        "design_system_ref": DS_REF,
    }
    if element_overrides:
        base_properties.update(element_overrides)
    element = StoryboardElement(
        element_id="element:mechanism",
        kind="SCREENSHOT",
        semantic_purpose="show the false alarm mechanism clearly",
        source_evidence_refs=["evidence:source"],
        asset_references=[asset],
        transformation_intent=intent
        or TransformationIntent(
            intent_id="intent:focus-mechanism",
            source_element_id="element:mechanism",
            intent="FOCUS",
            semantic_target="false alarm mechanism",
            mode="REFRAME",
            emphasis="MEANING",
            motion="SUBTLE_ZOOM",
            constraints={"source_quality": quality_level},
        ),
        motion_plan=motion_plan,
        properties=base_properties,
    )
    scene = StoryboardScene(
        scene_id="scene:1",
        scene_order=0,
        semantic_purpose="make the false alarm mechanism legible",
        source_evidence_refs=["evidence:source"],
        narrative_grammar=_binding(),
        shots=[
            StoryboardShot(
                shot_id="shot:1",
                start_ms=0,
                end_ms=1000,
                semantic_purpose="focus the mechanism without changing the source claim",
                elements=[element],
            )
        ],
    )
    return StoryboardRevision(
        workspace_id="workspace:test",
        session_id="session:test",
        revision_id="revision:test",
        revision_seq=1,
        base_revision_id=None,
        editorial_storyboard_id="storyboard:test",
        semantic_program_id="semantic:test",
        harness_id="supervisual-harness-v1",
        scenes=[scene],
        source_evidence_refs=["evidence:source"],
        status="IN_REVIEW",
        author_id="operator:test",
        canonical_sha256="c" * 64,
        created_at="2026-09-11T00:00:00Z",
    )


def test_m0092_success_validates_and_compiles_deterministic_motion_plan():
    revision = _revision()
    result = validate_final_hit(
        revision,
        format_id="SUPERVISUAL",
        design_system_ref=DS_REF,
        harness_constraints=HARNESS,
        wrong_reading_locks=["preserve source claim", "do not replace source evidence"],
    )
    assert result.passed is True
    assert result.operator_judgment_required is True
    assert all(status == "PASS" for status in result.checks.values())
    assert len(result.motion_plan_compilations) == 1
    plan = result.motion_plan_compilations[0].motion_plan
    assert plan.duration_ms == 1000
    assert [frame.at_ms for frame in plan.keyframes] == [0, 1000]
    assert [frame.scale_bps for frame in plan.keyframes] == [10000, 10700]
    assert plan.intensity_bps == 700
    assert plan.attention_cost_bps == 700
    assert plan.compiled_from_recipe_id is not None


def test_m0092_good_looking_but_wrong_visual_without_evidence_lineage_is_blocked():
    revision = _revision(element_overrides={"design_system_ref": DS_REF}, geometry={"x_bps": 1800, "y_bps": 1600, "width_bps": 5600, "height_bps": 4800})
    broken = copy.deepcopy(revision)
    broken.scenes[0].shots[0].elements[0].source_evidence_refs = []
    result = validate_final_hit(
        broken,
        format_id="SUPERVISUAL",
        design_system_ref=DS_REF,
        harness_constraints=HARNESS,
        wrong_reading_locks=["preserve source claim"],
    )
    assert result.passed is False
    assert result.checks["source_evidence"] == "PASS"
    assert any("source evidence lineage" in error for error in result.errors)
    assert result.operator_judgment_required is True


def test_m0092_low_quality_source_rejects_aggressive_compiled_motion():
    aggressive = TransformationRecipe(
        recipe_id="recipe:aggressive",
        intent_id="intent:focus-mechanism",
        primitives=[{"op": "ZOOM", "target": "intent_target", "amount_bps": 900}],
        keyframes=[
            {"at_bps": 0, "template": "HOLD"},
            {"at_bps": 10000, "template": "SCALE", "scale_bps": 10900},
        ],
        constraints={"effective_motion": "SUBTLE_ZOOM", "source_quality": "HIGH"},
        template_id="focus",
        registry_version="M0083-1",
        motion_template="SUBTLE_ZOOM_IN",
        governed=True,
        recipe_sha256="e" * 64,
    )
    revision = _revision(quality_level="LOW")
    revision.scenes[0].shots[0].elements[0].transformation_recipe = aggressive
    result = validate_final_hit(
        revision,
        format_id="SUPERVISUAL",
        design_system_ref=DS_REF,
        harness_constraints=HARNESS,
        wrong_reading_locks=["preserve source claim"],
    )
    assert result.passed is False
    assert result.checks["source_quality"] == "FAIL"
    assert any("source-quality limits" in error for error in result.errors)


def test_m0092_safe_area_violation_is_blocked_even_when_canvas_geometry_is_valid():
    revision = _revision(geometry={"x_bps": 0, "y_bps": 0, "width_bps": 4000, "height_bps": 4000})
    result = validate_final_hit(
        revision,
        format_id="SUPERVISUAL",
        design_system_ref=DS_REF,
        harness_constraints=HARNESS,
        wrong_reading_locks=["preserve source claim"],
    )
    assert result.passed is False
    assert result.checks["geometry_safe_area"] == "FAIL"
    assert any("safe area" in error for error in result.errors)


def test_m0092_missing_design_system_and_locks_fail_closed():
    revision = _revision()
    result = validate_final_hit(
        revision,
        format_id="SUPERVISUAL",
        design_system_ref=None,
        harness_constraints=HARNESS,
        wrong_reading_locks=[],
    )
    assert result.passed is False
    assert result.checks["design_system"] == "FAIL"
    assert result.checks["wrong_reading_locks"] == "FAIL"


def test_m0092_malformed_harness_is_rejected_before_projection():
    revision = _revision()
    with pytest.raises(final_hit.HarnessConstraintValidationError):
        validate_final_hit(
            revision,
            format_id="SUPERVISUAL",
            design_system_ref=DS_REF,
            harness_constraints={"max_attention_cost_bps": 1000, "safe_area": HARNESS["safe_area"]},
            wrong_reading_locks=["preserve source claim"],
        )


def test_m0092_manual_motion_plan_validates_keyframe_continuity_and_budget():
    bad_plan = MotionPlan(
        motion_plan_id="motion:manual",
        duration_ms=1000,
        keyframes=[
            Keyframe(at_ms=0, template="HOLD", purpose="HOLD"),
            Keyframe(at_ms=100, template="SCALE", scale_bps=11500, purpose="FOCUS"),
            Keyframe(at_ms=1000, template="RETURN", scale_bps=10000, purpose="RETURN_TO_SOURCE"),
        ],
        intensity_bps=1100,
        attention_cost_bps=1601,
    )
    revision = _revision(motion_plan=bad_plan)
    revision.scenes[0].shots[0].elements[0].transformation_intent = None
    revision.scenes[0].shots[0].elements[0].transformation_recipe = None
    result = validate_final_hit(
        revision,
        format_id="SUPERVISUAL",
        design_system_ref=DS_REF,
        harness_constraints=HARNESS,
        wrong_reading_locks=["preserve source claim"],
    )
    assert result.passed is False
    assert any("attention cost" in error for error in result.errors)


def test_m0092_replay_is_deterministic_and_idempotent():
    revision = _revision()
    kwargs = dict(
        format_id="SUPERVISUAL",
        design_system_ref=DS_REF,
        harness_constraints=HARNESS,
        wrong_reading_locks=["preserve source claim", "do not replace source evidence"],
    )
    first = validate_final_hit(revision, **kwargs)
    second = validate_final_hit(revision, **kwargs)
    assert first.validation_sha256 == second.validation_sha256
    assert first.motion_plan_compilations[0].motion_plan.motion_plan_id == second.motion_plan_compilations[0].motion_plan.motion_plan_id
    assert first.motion_plan_compilations[0].compilation_sha256 == second.motion_plan_compilations[0].compilation_sha256


def test_m0092_compile_final_hit_is_pure_and_content_addressed():
    compilation = final_hit.compile_final_hit(
        _revision(),
        format_id="SUPERVISUAL",
        design_system_ref=DS_REF,
        harness_constraints=HARNESS,
        wrong_reading_locks=["preserve source claim"],
    )
    assert compilation.format_id == "SUPERVISUAL"
    assert compilation.motion_plan_compilations
    assert compilation.compilation_sha256


class _SemanticProgramStub:
    wrong_reading_locks = ["preserve source claim", "do not replace source evidence"]

    @staticmethod
    def get(workspace_id: str, program_id: str):
        assert workspace_id == "workspace:test"
        assert program_id == "semantic:test"
        return _SemanticProgramStub()


def test_m0092_store_facade_resolves_canonical_semantic_program_locks_and_does_not_mutate_state():
    revision = _revision()
    conn = sqlite3.connect(":memory:")
    store = StoryboardSessionStore(connection=conn)

    class EditorialStoreStub:
        _conn = conn

        def get_semantic_program(self, workspace_id: str, program_id: str):
            return _SemanticProgramStub.get(workspace_id, program_id)

    store.editorial_store = EditorialStoreStub()
    store.get_revision = lambda workspace_id, session_id, revision_id: revision

    before = conn.execute("SELECT COUNT(*) FROM storyboard_validation_report").fetchone()[0]
    result = store.validate_final_hit(
        workspace_id="workspace:test",
        session_id="session:test",
        revision_id="revision:test",
        format_id="SUPERVISUAL",
        design_system_ref=DS_REF,
        harness_constraints=HARNESS,
    )
    after = conn.execute("SELECT COUNT(*) FROM storyboard_validation_report").fetchone()[0]

    assert result.passed is True
    assert after == before
    compilation = store.compile_final_hit(
        workspace_id="workspace:test",
        session_id="session:test",
        revision_id="revision:test",
        format_id="SUPERVISUAL",
        design_system_ref=DS_REF,
        harness_constraints=HARNESS,
    )
    assert compilation.motion_plan_compilations


def test_m0092_strict_visual_hit_requires_explicit_legibility_observation():
    revision = _revision(element_overrides={"evidence_legibility_bps": None})
    result = validate_final_hit(
        revision,
        format_id="SUPERVISUAL",
        design_system_ref=DS_REF,
        harness_constraints=HARNESS,
        wrong_reading_locks=["preserve source claim"],
    )
    assert result.passed is False
    assert result.checks["evidence_legibility"] == "FAIL"
    assert any("pixel-level legibility is unproven" in error for error in result.errors)
