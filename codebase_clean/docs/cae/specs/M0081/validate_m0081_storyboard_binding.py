"""Environment-isolated M0081 storyboard binding probe.

This loads the actual M0081 and M0079 source modules directly, avoiding the
repository package aggregator which imports optional monorepo services absent
from the supplied environment. It does not stub the tested modules or mutate
production configuration.
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
import types
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
RUNTIME = REPO / "packages/ca_runtime/src/ca_runtime"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    package = types.ModuleType("ca_runtime")
    package.__path__ = [str(RUNTIME)]
    sys.modules["ca_runtime"] = package

    load_module("ca_runtime.narrative_editing_grammar", RUNTIME / "narrative_editing_grammar.py")
    load_module("ca_runtime.editorial_discovery_store", RUNTIME / "editorial_discovery_store.py")
    load_module("ca_runtime.preparation_graph_store", RUNTIME / "preparation_graph_store.py")
    storyboard = load_module("ca_runtime.storyboard_session", RUNTIME / "storyboard_session.py")

    discovery = sys.modules["ca_runtime.editorial_discovery_store"]
    grammar = sys.modules["ca_runtime.narrative_editing_grammar"]

    workspace = "ws-m0081-probe"
    text = "The line lost time to false alarms."
    editorial = discovery.EditorialDiscoveryStore(":memory:")
    editorial.insert_evidence_segment(
        discovery.EvidenceSegmentRecord(
            workspace_id=workspace,
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
    editorial.insert_content_candidate(
        discovery.ContentCandidateRecord(
            workspace_id=workspace,
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
    editorial.insert_editorial_storyboard(
        discovery.EditorialStoryboardRecord(
            workspace_id=workspace,
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

    store = storyboard.StoryboardSessionStore(editorial_store=editorial)
    session = store.create_session(
        workspace_id=workspace,
        editorial_storyboard_id="STB-M0081-01",
        created_by="operator-chief",
        semantic_program_id="PRG-M0081-01",
        harness_id="HARNESS-VIDEO-01",
    )

    def make_binding(scene_id: str, mode: str, context: str, index: int):
        return grammar.NarrativeGrammarBinding(
            binding_id=f"binding-{scene_id}",
            scene_id=scene_id,
            grammar_mode=mode,
            grammar_version=grammar.NarrativeEditingGrammarRegistry.VERSION,
            archetype_id="F01_CINEMATIC_STORY",
            harness_id="HARNESS-VIDEO-01",
            activative_meaning="Expose lived tension without inventing a new claim.",
            editorial_intent="Change understanding through source-grounded sequence.",
            scene_context=context,
            sequence_index=index,
            evidence_refs=["seg-01"],
            wrong_reading_locks=["Do not imply unsupported facts."],
        )

    bindings = [
        make_binding("scene-00", "WITHHOLD", "SETUP", 0),
        make_binding("scene-01", "REVEAL", "EVIDENCE", 1),
        make_binding("scene-02", "RESOLVE", "RESOLUTION", 2),
    ]

    scenes = [
        storyboard.StoryboardScene(
            scene_id=binding.scene_id,
            scene_order=binding.sequence_index,
            semantic_purpose="Ground the narrative beat in source evidence.",
            source_evidence_refs=["seg-01"],
            narrative_grammar=binding,
            shots=[
                storyboard.StoryboardShot(
                    shot_id=f"{binding.scene_id}-shot",
                    start_ms=binding.sequence_index * 1000,
                    end_ms=(binding.sequence_index + 1) * 1000,
                    semantic_purpose="Carry the bounded narrative beat.",
                    elements=[
                        storyboard.StoryboardElement(
                            element_id=f"{binding.scene_id}-element",
                            kind="SOURCE_FRAME",
                            semantic_purpose="Evidence-bearing visual element.",
                            source_evidence_refs=["seg-01"],
                        )
                    ],
                )
            ],
        )
        for binding in bindings
    ]

    revision = store.save_revision(
        workspace_id=workspace,
        session_id=session.session_id,
        author_id="operator-chief",
        scenes=scenes,
        source_evidence_refs=["seg-01"],
        base_revision_id=None,
    )
    report = store.validate_revision(
        workspace_id=workspace,
        session_id=session.session_id,
        revision_id=revision.revision_id,
    )

    if not report.passed:
        raise AssertionError(report.errors)
    if report.checks.get("narrative_editing_grammar") != "PASS":
        raise AssertionError(report.checks)

    print("M0081 storyboard binding probe: PASS")
    print("narrative_editing_grammar=PASS")
    print(f"revision={revision.revision_id}")


if __name__ == "__main__":
    main()


