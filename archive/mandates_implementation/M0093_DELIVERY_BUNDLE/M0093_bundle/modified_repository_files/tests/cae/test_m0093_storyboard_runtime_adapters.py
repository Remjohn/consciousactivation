"""Focused M0093 tests for downstream storyboard runtime adapters.

The uploaded repository snapshot does not contain all installed runtime-package dependencies, so
this test module loads the ca_runtime package as a namespace package to isolate the canonical
storyboard modules without changing application code. This is test-environment plumbing only.
"""

from __future__ import annotations

import sys
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_SRC = ROOT / "packages" / "ca_runtime" / "src" / "ca_runtime"


def _bootstrap_canonical_runtime_namespace() -> None:
    if "ca_runtime" not in sys.modules:
        package = types.ModuleType("ca_runtime")
        package.__path__ = [str(RUNTIME_SRC)]
        sys.modules["ca_runtime"] = package


_bootstrap_canonical_runtime_namespace()

from ca_contracts import canonical_sha256
from ca_runtime.storyboard_programs import get_storyboard_program
from ca_runtime.storyboard_session import (
    StoryboardCompileReceipt,
    StoryboardElement,
    StoryboardRevision,
    StoryboardScene,
    StoryboardShot,
    StoryboardValidationReport,
    VisualAssetReference,
)
from adapters.storyboard_runtime import (
    GovernedStoryboardRuntimeInput,
    StoryboardRuntimeAuthorizationError,
    StoryboardRuntimeStaleError,
    StoryboardRuntimeValidationError,
)
from engines.carousel import CarouselStoryboardRuntimeAdapter
from engines.presentation import PresentationStoryboardRuntimeAdapter


@pytest.fixture
def approved_handoff() -> GovernedStoryboardRuntimeInput:
    asset = VisualAssetReference(
        reference_id="ref-a1",
        asset_id="asset-a1",
        source_uri="https://cdn.example.test/a1.png",
        evidence_refs=["ev-1"],
        rights_status="CLEARED",
        source_quality="HIGH",
        approved=True,
    )
    carousel_element = StoryboardElement(
        element_id="el-1",
        kind="image",
        semantic_purpose="establish the source-backed contrast",
        source_evidence_refs=["ev-1"],
        asset_references=[asset],
    )
    presentation_element = carousel_element.model_copy(update={"properties": {"build_step": 1}})
    scene = StoryboardScene(
        scene_id="scene-0",
        scene_order=0,
        semantic_purpose="establish the source-backed contrast",
        source_evidence_refs=["ev-1"],
        shots=[StoryboardShot(
            shot_id="shot-0",
            start_ms=0,
            end_ms=1000,
            semantic_purpose="hold the evidence",
            elements=[presentation_element],
        )],
    )
    revision = StoryboardRevision(
        workspace_id="ws-1",
        session_id="session-1",
        revision_id="rev-1",
        revision_seq=1,
        base_revision_id=None,
        editorial_storyboard_id="storyboard-1",
        semantic_program_id="semantic-1",
        harness_id="harness-1",
        scenes=[scene],
        source_evidence_refs=["ev-1"],
        status="IN_REVIEW",
        author_id="operator-1",
        canonical_sha256="a" * 64,
        created_at="2026-09-11T00:00:00Z",
    )

    # Build the presentation expression so the same handoff can be swapped to the carousel fixture.
    expression = get_storyboard_program("PRESENTATION").compile(revision)
    report_payload = {
        "workspace_id": revision.workspace_id,
        "session_id": revision.session_id,
        "revision_id": revision.revision_id,
        "passed": True,
        "checks": {
            "editorial_storyboard_lineage": "PASS",
            "source_evidence_lineage": "PASS",
            "scene_shot_timing": "PASS",
            "transformation_chain": "PASS",
        },
        "errors": [],
        "warnings": [],
    }
    report = StoryboardValidationReport(
        report_id="validation_rev-1",
        **report_payload,
        report_sha256=canonical_sha256(report_payload),
        created_at="2026-09-11T00:01:00Z",
    )
    receipt_payload = {
        "workspace_id": revision.workspace_id,
        "session_id": revision.session_id,
        "revision_id": revision.revision_id,
        "editorial_storyboard_id": revision.editorial_storyboard_id,
        "semantic_program_id": revision.semantic_program_id,
        "harness_id": revision.harness_id,
        "validation_report_id": report.report_id,
        "status": "COMPILE_READY",
    }
    receipt = StoryboardCompileReceipt(
        receipt_id="compile_rev-1",
        **receipt_payload,
        lineage_sha256=canonical_sha256({**receipt_payload, "revision_sha256": revision.canonical_sha256}),
        created_at="2026-09-11T00:02:00Z",
    )
    return GovernedStoryboardRuntimeInput(
        revision=revision,
        expression=expression,
        validation_report=report,
        compile_receipt=receipt,
    )


def _carousel_handoff(handoff: GovernedStoryboardRuntimeInput) -> GovernedStoryboardRuntimeInput:
    expression = get_storyboard_program("CAROUSEL").compile(handoff.revision)
    return handoff.__class__(
        revision=handoff.revision,
        expression=expression,
        validation_report=handoff.validation_report,
        compile_receipt=handoff.compile_receipt,
    )


def test_carousel_adapter_compiles_open_carrusel_compatible_preview_and_is_idempotent(approved_handoff):
    handoff = _carousel_handoff(approved_handoff)
    adapter = CarouselStoryboardRuntimeAdapter(aspect_ratio="4:5")
    before = handoff.revision.model_dump(mode="json")

    first = adapter.compile(handoff)
    second = adapter.compile(handoff)

    assert first.payload == second.payload
    assert first.lineage_sha256 == second.lineage_sha256
    assert first.native_reachability_proven is False
    carousel = first.payload["carousels"][0]
    assert carousel["aspectRatio"] == "4:5"
    assert carousel["slides"][0]["order"] == 0
    assert "width: 1080px; height: 1350px" in carousel["slides"][0]["html"]
    assert first.payload["cae_lineage"]["compile_receipt_id"] == "compile_rev-1"
    assert handoff.revision.model_dump(mode="json") == before


def test_presentation_adapter_preserves_build_order_for_slidev_and_reveal(approved_handoff):
    slidev = PresentationStoryboardRuntimeAdapter(runtime="slidev").compile(approved_handoff)
    reveal = PresentationStoryboardRuntimeAdapter(runtime="revealjs").compile(approved_handoff)

    slides_md = slidev.payload["slides_md"]
    index_html = reveal.payload["index_html"]
    assert slides_md.startswith("---\ntitle:")
    assert "v-click=\"1\"" in slides_md
    assert "<!-- cae-scene-id: scene-0 -->" in slides_md
    assert "compile_rev-1" in slides_md
    assert '<div class="reveal"><div class="slides">' in index_html
    assert 'class="fragment" data-fragment-index="1"' in index_html
    assert 'data-cae-element-id="el-1"' in index_html
    assert '<script src="dist/reveal.js"></script>' in index_html
    assert "compile_rev-1" in index_html
    assert slidev.native_reachability_proven is False
    assert reveal.native_reachability_proven is False


def test_good_looking_but_wrong_expression_is_rejected(approved_handoff):
    wrong_scene = approved_handoff.expression.scenes[0].copy()
    wrong_scene["semantic_purpose"] = "sell an unrelated conclusion"
    tampered = approved_handoff.expression.model_copy(update={"scenes": [wrong_scene]})
    tampered_handoff = approved_handoff.__class__(
        revision=approved_handoff.revision,
        expression=tampered,
        validation_report=approved_handoff.validation_report,
        compile_receipt=approved_handoff.compile_receipt,
    )

    with pytest.raises(StoryboardRuntimeStaleError, match="canonical program projection"):
        PresentationStoryboardRuntimeAdapter().compile(tampered_handoff)


def test_missing_operator_authorization_is_rejected(approved_handoff):
    bad_report_payload = approved_handoff.validation_report.model_copy(update={"passed": False, "errors": ["operator gate failed"]})
    bad_report = bad_report_payload.model_copy(
        update={
            "report_sha256": canonical_sha256({
                "workspace_id": bad_report_payload.workspace_id,
                "session_id": bad_report_payload.session_id,
                "revision_id": bad_report_payload.revision_id,
                "passed": False,
                "checks": bad_report_payload.checks,
                "errors": bad_report_payload.errors,
                "warnings": bad_report_payload.warnings,
            })
        }
    )
    bad_handoff = approved_handoff.__class__(
        revision=approved_handoff.revision,
        expression=approved_handoff.expression,
        validation_report=bad_report,
        compile_receipt=approved_handoff.compile_receipt,
    )
    with pytest.raises(StoryboardRuntimeAuthorizationError, match="passing validation report"):
        PresentationStoryboardRuntimeAdapter().compile(bad_handoff)


def test_stale_receipt_is_rejected(approved_handoff):
    stale_receipt = approved_handoff.compile_receipt.model_copy(update={"revision_id": "rev-old"})
    stale_handoff = approved_handoff.__class__(
        revision=approved_handoff.revision,
        expression=approved_handoff.expression,
        validation_report=approved_handoff.validation_report,
        compile_receipt=stale_receipt,
    )
    with pytest.raises(StoryboardRuntimeStaleError, match="revision_id"):
        PresentationStoryboardRuntimeAdapter().compile(stale_handoff)


def test_malformed_source_uri_fails_closed(approved_handoff):
    bad_asset = VisualAssetReference(
        reference_id="ref-a1",
        asset_id="asset-a1",
        source_uri="javascript:alert(1)",
        evidence_refs=["ev-1"],
        rights_status="CLEARED",
        source_quality="HIGH",
        approved=True,
    )
    scene = approved_handoff.revision.scenes[0].model_copy(
        update={
            "shots": [approved_handoff.revision.scenes[0].shots[0].model_copy(
                update={
                    "elements": [approved_handoff.revision.scenes[0].shots[0].elements[0].model_copy(
                        update={"asset_references": [bad_asset]}
                    )]
                }
            )]
        }
    )
    bad_revision = approved_handoff.revision.model_copy(update={"scenes": [scene]})
    expression = get_storyboard_program("CAROUSEL").compile(bad_revision)
    bad_handoff = approved_handoff.__class__(
        revision=bad_revision,
        expression=expression,
        validation_report=approved_handoff.validation_report.model_copy(update={"revision_id": "rev-1"}),
        compile_receipt=approved_handoff.compile_receipt,
    )
    with pytest.raises(StoryboardRuntimeValidationError, match="source_uri"):
        CarouselStoryboardRuntimeAdapter().compile(bad_handoff)
