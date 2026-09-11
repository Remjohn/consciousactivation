from __future__ import annotations

import hashlib

import pytest

from ca_runtime.editorial_discovery_store import (
    ContentCandidateRecord,
    EditorialDiscoveryStore,
    EditorialStoryboardRecord,
    EvidenceSegmentRecord,
)
from ca_runtime.narrative_editing_grammar import (
    NarrativeEditingGrammarRegistry,
    NarrativeGrammarBinding,
    NarrativeGrammarBindingError,
    NarrativeGrammarMode,
    NarrativeSceneContext,
)
from ca_runtime.storyboard_session import (
    StoryboardElement,
    StoryboardRevisionValidationError,
    StoryboardScene,
    StoryboardSessionStore,
    StoryboardShot,
)


def _binding(
    *,
    scene_id: str,
    mode: str,
    index: int,
    context: str,
    evidence_refs: list[str] | None = None,
    relation_scene_ids: list[str] | None = None,
    harness_id: str = "HARNESS-VIDEO-01",
) -> NarrativeGrammarBinding:
    return NarrativeGrammarBinding(
        binding_id=f"binding-{scene_id}",
        scene_id=scene_id,
        grammar_mode=mode,
        grammar_version=NarrativeEditingGrammarRegistry.VERSION,
        archetype_id="F01_CINEMATIC_STORY",
        harness_id=harness_id,
        activative_meaning="Expose the lived tension without inventing a new claim.",
        editorial_intent="Change the viewer's understanding through source-grounded sequence.",
        scene_context=context,
        sequence_index=index,
        evidence_refs=evidence_refs or ["seg-01"],
        relation_scene_ids=relation_scene_ids or [],
        wrong_reading_locks=["Do not imply a fact absent from source evidence."],
    )


def _editorial_store() -> EditorialDiscoveryStore:
    store = EditorialDiscoveryStore(":memory:")
    ws = "ws-m0081"
    text = "The line lost time to false alarms."
    store.insert_evidence_segment(
        EvidenceSegmentRecord(
            workspace_id=ws,
            segment_id="seg-01",
            session_id="interview-01",
            speaker="Operator",
            start_time_ms=0,
            end_time_ms=1600,
            verbatim_text=text,
            boundary_type="SYNTACTIC_SENTENCE",
            text_sha256=hashlib.sha256(text.encode()).hexdigest(),
        )
    )
    store.insert_content_candidate(
        ContentCandidateRecord(
            workspace_id=ws,
            candidate_id="candidate-01",
            candidate_type="PROBLEM_SOLUTION_ARC",
            title="False Alarm",
            hook_statement=text,
            narrative_completeness="COMPLETE_ARC",
            evidence_links=[{"segment_id": "seg-01"}],
            production_status="SELECTED_FOR_PRODUCTION",
            archetypal_container="F01_CINEMATIC_STORY",
        )
    )
    store.insert_editorial_storyboard(
        EditorialStoryboardRecord(
            workspace_id=ws,
            storyboard_id="STB-M0081-01",
            candidate_id="candidate-01",
            title="False Alarm",
            hook_statement=text,
            priority_rank=1,
            evidence_links=[{"segment_id": "seg-01"}],
            narrative_structure=[{"segment_id": "seg-01"}],
            approved_by="operator-chief",
        )
    )
    return store


def _scene(
    *,
    scene_id: str,
    order: int,
    binding: NarrativeGrammarBinding | None = None,
) -> StoryboardScene:
    return StoryboardScene(
        scene_id=scene_id,
        scene_order=order,
        semantic_purpose="Ground the sequence in source evidence.",
        source_evidence_refs=["seg-01"],
        narrative_grammar=binding,
        shots=[
            StoryboardShot(
                shot_id=f"{scene_id}-shot",
                start_ms=order * 1000,
                end_ms=(order + 1) * 1000,
                semantic_purpose="Carry the bounded narrative beat.",
                elements=[
                    StoryboardElement(
                        element_id=f"{scene_id}-element",
                        kind="SOURCE_FRAME",
                        semantic_purpose="Evidence-bearing visual element.",
                        source_evidence_refs=["seg-01"],
                    )
                ],
            )
        ],
    )


def test_registry_contains_all_required_modes_and_no_effect_recipes():
    modes = NarrativeEditingGrammarRegistry.modes()
    assert modes == (
        "WITHHOLD",
        "REVEAL",
        "FOCUS",
        "CONTRAST",
        "PROVE",
        "EXPLAIN",
        "CONNECT",
        "ESCALATE",
        "INTERRUPT",
        "RESOLVE",
    )
    for entry in NarrativeEditingGrammarRegistry.all_entries():
        assert "effect" not in entry.relational_pattern.lower()
        assert "geometry" not in entry.relational_pattern.lower()
        assert entry.false_proof_conditions


def test_happy_path_sequence_validates_and_is_deterministic():
    bindings = [
        _binding(
            scene_id="scene-00",
            mode=NarrativeGrammarMode.WITHHOLD,
            index=0,
            context=NarrativeSceneContext.SETUP,
        ),
        _binding(
            scene_id="scene-01",
            mode=NarrativeGrammarMode.REVEAL,
            index=1,
            context=NarrativeSceneContext.EVIDENCE,
        ),
        _binding(
            scene_id="scene-02",
            mode=NarrativeGrammarMode.RESOLVE,
            index=2,
            context=NarrativeSceneContext.RESOLUTION,
        ),
    ]
    first = NarrativeEditingGrammarRegistry.validate_sequence(
        bindings,
        expected_harness_id="HARNESS-VIDEO-01",
        expected_scene_ids=["scene-00", "scene-01", "scene-02"],
    )
    second = NarrativeEditingGrammarRegistry.validate_sequence(
        bindings,
        expected_harness_id="HARNESS-VIDEO-01",
        expected_scene_ids=["scene-00", "scene-01", "scene-02"],
    )

    assert first.passed is True
    assert first.errors == []
    assert first.report_sha256 == second.report_sha256


def test_good_looking_but_wrong_reveal_without_withhold_is_rejected():
    binding = _binding(
        scene_id="scene-00",
        mode=NarrativeGrammarMode.REVEAL,
        index=0,
        context=NarrativeSceneContext.TURN,
    )
    report = NarrativeEditingGrammarRegistry.validate_sequence(
        [binding],
        expected_harness_id="HARNESS-VIDEO-01",
        expected_scene_ids=["scene-00"],
    )
    assert report.passed is False
    assert any("requires prior mode" in error for error in report.errors)


def test_contrast_requires_a_distinct_relation_target():
    binding = _binding(
        scene_id="scene-00",
        mode=NarrativeGrammarMode.CONTRAST,
        index=0,
        context=NarrativeSceneContext.CONTRAST,
    )
    with pytest.raises(NarrativeGrammarBindingError, match="relation target"):
        NarrativeEditingGrammarRegistry.validate_binding(
            binding,
            expected_harness_id="HARNESS-VIDEO-01",
        )


def test_harness_mismatch_is_authorization_failure():
    binding = _binding(
        scene_id="scene-00",
        mode=NarrativeGrammarMode.FOCUS,
        index=0,
        context=NarrativeSceneContext.EVIDENCE,
        harness_id="HARNESS-WRONG",
    )
    with pytest.raises(NarrativeGrammarBindingError, match="harness"):
        NarrativeEditingGrammarRegistry.validate_binding(
            binding,
            expected_harness_id="HARNESS-VIDEO-01",
        )


def test_storyboard_revision_rejects_grammar_bound_scene_without_harness():
    editorial = _editorial_store()
    store = StoryboardSessionStore(editorial_store=editorial)
    session = store.create_session(
        workspace_id="ws-m0081",
        editorial_storyboard_id="STB-M0081-01",
        created_by="operator-chief",
    )
    scene = _scene(
        scene_id="scene-00",
        order=0,
        binding=_binding(
            scene_id="scene-00",
            mode=NarrativeGrammarMode.PROVE,
            index=0,
            context=NarrativeSceneContext.EVIDENCE,
        ),
    )
    with pytest.raises(StoryboardRevisionValidationError, match="canonical session harness_id"):
        store.save_revision(
            workspace_id="ws-m0081",
            session_id=session.session_id,
            author_id="operator-chief",
            scenes=[scene],
            source_evidence_refs=["seg-01"],
            base_revision_id=None,
        )


def test_storyboard_revision_accepts_grammar_binding_and_reports_grammar_check():
    editorial = _editorial_store()
    store = StoryboardSessionStore(editorial_store=editorial)
    session = store.create_session(
        workspace_id="ws-m0081",
        editorial_storyboard_id="STB-M0081-01",
        created_by="operator-chief",
        harness_id="HARNESS-VIDEO-01",
        semantic_program_id="PRG-M0081-01",
    )
    scenes = [
        _scene(
            scene_id="scene-00",
            order=0,
            binding=_binding(
                scene_id="scene-00",
                mode=NarrativeGrammarMode.WITHHOLD,
                index=0,
                context=NarrativeSceneContext.SETUP,
            ),
        ),
        _scene(
            scene_id="scene-01",
            order=1,
            binding=_binding(
                scene_id="scene-01",
                mode=NarrativeGrammarMode.REVEAL,
                index=1,
                context=NarrativeSceneContext.EVIDENCE,
            ),
        ),
        _scene(
            scene_id="scene-02",
            order=2,
            binding=_binding(
                scene_id="scene-02",
                mode=NarrativeGrammarMode.RESOLVE,
                index=2,
                context=NarrativeSceneContext.RESOLUTION,
            ),
        ),
    ]
    revision = store.save_revision(
        workspace_id="ws-m0081",
        session_id=session.session_id,
        author_id="operator-chief",
        scenes=scenes,
        source_evidence_refs=["seg-01"],
        base_revision_id=None,
    )
    report = store.validate_revision(
        workspace_id="ws-m0081",
        session_id=session.session_id,
        revision_id=revision.revision_id,
    )
    assert report.passed is True
    assert report.checks["narrative_editing_grammar"] == "PASS"


