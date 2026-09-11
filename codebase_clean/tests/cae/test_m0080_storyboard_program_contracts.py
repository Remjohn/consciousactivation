"""M0080 contract tests for the four format-specific storyboard programs."""

from __future__ import annotations

import pytest

from ca_runtime.storyboard_programs import (
    CarouselStoryboardProgram,
    PresentationStoryboardProgram,
    StoryboardProgramAuthorityError,
    StoryboardProgramValidationError,
    SuperVisualStoryboardProgram,
    VideoStoryboardProgram,
    get_storyboard_program,
)
from ca_runtime.storyboard_session import (
    StoryboardElement,
    StoryboardRevision,
    StoryboardScene,
    StoryboardShot,
    VisualAssetReference,
)


def _element(*, geometry: dict[str, int] | None = None, build_step: int | None = None) -> StoryboardElement:
    properties: dict[str, object] = {}
    if geometry is not None:
        properties["geometry"] = geometry
    if build_step is not None:
        properties["build_step"] = build_step
    return StoryboardElement(
        element_id=f"element-{build_step or 'one'}",
        kind="SOURCE_FRAME",
        semantic_purpose="Make the approved evidence legible.",
        source_evidence_refs=["seg-01"],
        asset_references=[
            VisualAssetReference(
                reference_id="asset-ref-01",
                asset_id="asset-01",
                evidence_refs=["seg-01"],
                source_quality="HIGH",
                rights_status="CLEARED",
                approved=True,
            )
        ],
        properties=properties,
    )


def _scene(order: int, *, element: StoryboardElement | None = None, two_shots: bool = False) -> StoryboardScene:
    first = StoryboardShot(
        shot_id=f"shot-{order}-01",
        start_ms=order * 2000,
        end_ms=order * 2000 + 1000,
        semantic_purpose="Reveal the evidence.",
        elements=[element or _element()],
    )
    shots = [first]
    if two_shots:
        shots.append(
            StoryboardShot(
                shot_id=f"shot-{order}-02",
                start_ms=order * 2000 + 1000,
                end_ms=order * 2000 + 2000,
                semantic_purpose="Hold the evidence.",
                elements=[element or _element()],
            )
        )
    return StoryboardScene(
        scene_id=f"scene-{order}",
        scene_order=order,
        semantic_purpose="Ground the composition in source evidence.",
        source_evidence_refs=["seg-01"],
        shots=shots,
    )


def _revision(*scenes: StoryboardScene) -> StoryboardRevision:
    return StoryboardRevision(
        workspace_id="ws-m0080",
        session_id="storyboard-session-01",
        revision_id="rev-storyboard-01",
        revision_seq=1,
        base_revision_id=None,
        editorial_storyboard_id="STB-M0080-01",
        semantic_program_id="PRG-M0080-01",
        harness_id="HARNESS-VIDEO-01",
        scenes=list(scenes),
        source_evidence_refs=["seg-01"],
        author_id="operator-01",
        canonical_sha256="a" * 64,
        created_at="2026-09-11T00:00:00Z",
    )


def test_all_four_programs_compile_shared_revision_without_new_semantic_authority():
    revision = _revision(
        _scene(
            0,
            element=_element(geometry={"x_bps": 0, "y_bps": 0, "width_bps": 5000, "height_bps": 5000}, build_step=1),
            two_shots=True,
        ),
        _scene(
            1,
            element=_element(geometry={"x_bps": 5000, "y_bps": 0, "width_bps": 5000, "height_bps": 5000}, build_step=1),
        ),
    )
    revision.scenes[0].shots[1].elements[0] = _element(
        geometry={"x_bps": 1000, "y_bps": 1000, "width_bps": 3000, "height_bps": 3000},
        build_step=2,
    )
    revision.scenes[0].shots[1].elements[0].element_id = "element-two"

    video = VideoStoryboardProgram().compile(revision)
    carousel = CarouselStoryboardProgram().compile(revision)
    supervisual = SuperVisualStoryboardProgram().compile(revision)
    presentation = PresentationStoryboardProgram().compile(revision)

    assert video.format_id == "VIDEO"
    assert carousel.scenes[1]["slide_index"] == 1
    assert supervisual.format_id == "SUPERVISUAL"
    assert presentation.scenes[0]["build_order"][0]["build_step"] == 1
    for expression in (video, carousel, supervisual, presentation):
        assert expression.editorial_storyboard_id == revision.editorial_storyboard_id
        assert expression.source_evidence_refs == ["seg-01"]
        assert expression.canonical_sha256


def test_good_looking_but_wrong_format_projection_cannot_escape_evidence_authority():
    revision = _revision(_scene(0, element=_element(geometry={"x_bps": 0, "y_bps": 0, "width_bps": 5000, "height_bps": 5000})))
    revision.scenes[0].shots[0].elements[0].asset_references[0].approved = False
    with pytest.raises(StoryboardProgramAuthorityError, match="not operator-approved"):
        SuperVisualStoryboardProgram().compile(revision)


def test_format_specific_negative_cases_fail_closed():
    with pytest.raises(StoryboardProgramValidationError, match="unsupported storyboard format"):
        get_storyboard_program("UNKNOWN")

    no_geometry = _revision(_scene(0))
    with pytest.raises(StoryboardProgramValidationError, match="requires geometry"):
        SuperVisualStoryboardProgram().compile(no_geometry)

    duplicate_build = _revision(
        _scene(0, element=_element(build_step=1))
    )
    duplicate_build.scenes[0].shots[0].elements.append(_element(build_step=1))
    with pytest.raises(StoryboardProgramValidationError, match="duplicate build_step"):
        PresentationStoryboardProgram().compile(duplicate_build)

    non_contiguous = _revision(_scene(1, element=_element(geometry={"x_bps": 0, "y_bps": 0, "width_bps": 5000, "height_bps": 5000})))
    with pytest.raises(StoryboardProgramValidationError, match="contiguous"):
        CarouselStoryboardProgram().compile(non_contiguous)


def test_video_rejects_overlapping_temporal_structure():
    revision = _revision(_scene(0, two_shots=True))
    revision.scenes[0].shots[1].start_ms = 900
    with pytest.raises(StoryboardProgramValidationError, match="overlapping shots"):
        VideoStoryboardProgram().compile(revision)
