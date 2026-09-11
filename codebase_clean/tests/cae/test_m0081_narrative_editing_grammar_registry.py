from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
import yaml


REPO = Path(__file__).resolve().parents[2]
MODULE = REPO / "packages/ca_runtime/src/ca_runtime/narrative_editing_grammar.py"


def load_module():
    name = "_m0081_narrative_editing_grammar_under_test"
    spec = importlib.util.spec_from_file_location(name, MODULE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def binding(module, *, mode, scene_id, index, context, evidence=None, relations=None, harness="H"):
    return module.NarrativeGrammarBinding(
        binding_id=f"binding-{scene_id}",
        scene_id=scene_id,
        grammar_mode=mode,
        grammar_version=module.NarrativeEditingGrammarRegistry.VERSION,
        archetype_id="F01_CINEMATIC_STORY",
        harness_id=harness,
        activative_meaning="Source-grounded activative meaning.",
        editorial_intent="Change interpretation through a declared relation.",
        scene_context=context,
        sequence_index=index,
        evidence_refs=evidence or ["seg-01"],
        relation_scene_ids=relations or [],
        wrong_reading_locks=["Do not create unsupported facts."],
    )


def test_registry_has_required_vocabulary_and_is_not_an_effect_catalog():
    module = load_module()
    registry = module.NarrativeEditingGrammarRegistry
    assert registry.modes() == (
        "WITHHOLD", "REVEAL", "FOCUS", "CONTRAST", "PROVE",
        "EXPLAIN", "CONNECT", "ESCALATE", "INTERRUPT", "RESOLVE",
    )
    assert len(registry.all_entries()) == 10
    for entry in registry.all_entries():
        assert entry.relational_pattern
        assert entry.allowed_scene_contexts
        assert entry.required_meaning_fields
        assert entry.false_proof_conditions
        assert "geometry" not in entry.relational_pattern.lower()
        assert "keyframe" not in entry.relational_pattern.lower()
        assert "provider" not in entry.relational_pattern.lower()


def test_valid_withhold_reveal_resolve_sequence_passes_and_replays_identically():
    module = load_module()
    b = [
        binding(module, mode="WITHHOLD", scene_id="s0", index=0, context="SETUP"),
        binding(module, mode="REVEAL", scene_id="s1", index=1, context="EVIDENCE"),
        binding(module, mode="RESOLVE", scene_id="s2", index=2, context="RESOLUTION"),
    ]
    first = module.NarrativeEditingGrammarRegistry.validate_sequence(
        b, expected_harness_id="H", expected_scene_ids=["s0", "s1", "s2"]
    )
    second = module.NarrativeEditingGrammarRegistry.validate_sequence(
        b, expected_harness_id="H", expected_scene_ids=["s0", "s1", "s2"]
    )
    assert first.passed is True
    assert first.errors == []
    assert first.report_sha256 == second.report_sha256


def test_good_looking_but_wrong_reveal_without_withhold_is_rejected():
    module = load_module()
    reveal = binding(module, mode="REVEAL", scene_id="s0", index=0, context="EVIDENCE")
    report = module.NarrativeEditingGrammarRegistry.validate_sequence(
        [reveal], expected_harness_id="H", expected_scene_ids=["s0"]
    )
    assert report.passed is False
    assert any("requires a prior mode" in error for error in report.errors)


def test_contrastive_relation_and_harness_failures_are_closed():
    module = load_module()
    contrast = binding(module, mode="CONTRAST", scene_id="s0", index=0, context="CONTRAST")
    with pytest.raises(module.NarrativeGrammarBindingError, match="relation target"):
        module.NarrativeEditingGrammarRegistry.validate_binding(
            contrast, expected_harness_id="H"
        )

    wrong_harness = binding(
        module, mode="FOCUS", scene_id="s0", index=0, context="EVIDENCE", harness="OTHER"
    )
    with pytest.raises(module.NarrativeGrammarBindingError, match="harness"):
        module.NarrativeEditingGrammarRegistry.validate_binding(
            wrong_harness, expected_harness_id="H"
        )


def test_allowed_scene_context_and_meaning_inputs_are_fail_closed():
    module = load_module()
    wrong_context = binding(
        module, mode="REVEAL", scene_id="s0", index=0, context="OPENING"
    )
    with pytest.raises(module.NarrativeGrammarBindingError, match="not allowed"):
        module.NarrativeEditingGrammarRegistry.validate_binding(wrong_context)

    missing_intent = binding(
        module, mode="FOCUS", scene_id="s0", index=0, context="EVIDENCE"
    ).model_copy(update={"editorial_intent": ""})
    with pytest.raises(module.NarrativeGrammarBindingError, match="editorial_intent"):
        module.NarrativeEditingGrammarRegistry.validate_binding(missing_intent)


def test_registry_payload_round_trip_is_canonicalizable():
    module = load_module()
    payload = module.narrative_grammar_registry_payload()
    assert payload["grammar_id"] == module.NarrativeEditingGrammarRegistry.GRAMMAR_ID
    assert payload["version"] == module.NarrativeEditingGrammarRegistry.VERSION
    assert [entry["mode"] for entry in payload["entries"]] == list(
        module.NarrativeEditingGrammarRegistry.modes()
    )
    digest = module.canonical_sha256(payload)
    assert isinstance(digest, str) and len(digest) == 64

def test_yaml_registry_matches_executable_registry():
    module = load_module()
    yaml_path = REPO / "docs/cae/specs/M0081/narrative_editing_grammar_registry.yaml"
    payload = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    assert payload["grammar_id"] == module.NarrativeEditingGrammarRegistry.GRAMMAR_ID
    assert payload["version"] == module.NarrativeEditingGrammarRegistry.VERSION
    assert [item["mode"] for item in payload["entries"]] == list(
        module.NarrativeEditingGrammarRegistry.modes()
    )


