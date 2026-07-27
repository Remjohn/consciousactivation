import pytest

from cmf_builder.application.skill_runtime_inspection import (
    ActivationState,
    RuntimeObjectClass,
    SkillRuntimeInspection,
    SkillRuntimeInspectionError,
    SkillRuntimeObject,
    query_runtime_objects,
    trace_runtime_lineage,
)


def obj(object_id="skill:1", object_class=RuntimeObjectClass.SKILL_VERSION, **overrides):
    values = {
        "object_id": object_id,
        "object_class": object_class,
        "version": "1.0.0",
        "source_registry": "registry:skills",
        "capability_requirement": "capability:activative_pack",
        "necessity_decision": "decision:required",
        "behavioral_anchors": ("anchor:wrong-reading",),
        "recipe_components": ("recipe:1",),
        "phase_applicability": ("phase:compile",),
        "minimum_context_refs": ("context:min",),
        "pin_identity": "pin:1",
        "load_identity": "load:1",
        "activation_state": ActivationState.ACTIVE,
        "predecessor_identities": (),
        "descendant_identities": (),
        "receipt_refs": ("receipt:skill",),
        "provenance": "provenance:skill",
        "maturity": "development_validated",
        "limitations": ("not certification",),
        "source_lineage": "lineage:skill",
    }
    values.update(overrides)
    return SkillRuntimeObject(**values)


def test_complete_lineage_and_query_are_deterministic():
    skill = obj("skill")
    recipe = obj("recipe", RuntimeObjectClass.RECIPE, predecessor_identities=("skill",), descendant_identities=("jit",))
    jit = obj("jit", RuntimeObjectClass.JIT_CAPSULE, predecessor_identities=("recipe",), descendant_identities=("runtime",))
    runtime = obj("runtime", RuntimeObjectClass.PINNED_RUNTIME_CAPSULE, predecessor_identities=("jit",))
    inspection = SkillRuntimeInspection("harness:1", (skill, recipe, jit, runtime), "rev:1")

    assert inspection.inspection_identity
    assert trace_runtime_lineage((recipe, jit, runtime), "recipe") == ("recipe", "jit", "runtime")
    assert query_runtime_objects((skill, recipe, jit, runtime), phase="phase:compile")


def test_empty_skill_path_is_explicit_not_missing():
    empty = obj(
        "empty-skill-decision",
        RuntimeObjectClass.SKILL_DECISION,
        capability_requirement="NOT_APPLICABLE",
        necessity_decision="zero_external_skill_required",
        behavioral_anchors=(),
    )
    assert empty.capability_requirement == "NOT_APPLICABLE"


def test_runtime_failures_reject_unpinned_invalidated_disposed_and_excess_context():
    with pytest.raises(SkillRuntimeInspectionError) as unpinned:
        obj("runtime", RuntimeObjectClass.PINNED_RUNTIME_CAPSULE, pin_identity="UNPINNED")
    assert unpinned.value.code == "UNPINNED_RUNTIME_SKILL_USE"

    with pytest.raises(SkillRuntimeInspectionError) as invalid:
        obj("invalid", RuntimeObjectClass.INVALIDATED_CAPSULE, activation_state=ActivationState.ACTIVE)
    assert invalid.value.code == "INVALIDATED_CAPSULE_DISPLAYED_ACTIVE"

    with pytest.raises(SkillRuntimeInspectionError) as disposed:
        obj("disposed", RuntimeObjectClass.DISPOSED_CAPSULE, activation_state=ActivationState.LOADED)
    assert disposed.value.code == "DISPOSED_CAPSULE_DISPLAYED_LOADED"

    with pytest.raises(SkillRuntimeInspectionError) as excess:
        obj("jit", RuntimeObjectClass.JIT_CAPSULE, excess_context_included=True)
    assert excess.value.code == "EXCESS_CONTEXT_INCLUDED"


def test_missing_anchors_missing_decision_and_certification_claim_fail():
    with pytest.raises(SkillRuntimeInspectionError) as anchors:
        obj(behavioral_anchors=())
    assert anchors.value.code == "MISSING_BEHAVIORAL_ANCHORS"

    with pytest.raises(SkillRuntimeInspectionError) as cert:
        obj(certified=True)
    assert cert.value.code == "DEVELOPMENT_DISPLAYED_AS_CERTIFICATION"
