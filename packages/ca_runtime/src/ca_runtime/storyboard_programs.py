"""Format-specific storyboard program contracts (CAE-M0080).

The four programs in this module are deterministic projections of the
M0079 ``StoryboardRevision``.  They define format grammar and constraints;
they do not create semantic meaning, retrieve evidence, approve assets, or
replace the existing EditorialStoryboard authority.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Mapping, Sequence, Type

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ca_contracts import CanonicalizationError, canonical_sha256
from ca_runtime.storyboard_session import (
    StoryboardElement,
    StoryboardRevision,
    StoryboardScene,
    StoryboardShot,
)


class StoryboardProgramError(Exception):
    """Base error for format-specific storyboard contract compilation."""


class StoryboardProgramAuthorityError(StoryboardProgramError):
    """The input is not a canonical, evidence-linked storyboard revision."""


class StoryboardProgramValidationError(StoryboardProgramError):
    """The revision does not satisfy the selected format grammar."""


class StoryboardProgramCanonicalizationError(StoryboardProgramError):
    """The proposed expression contains values outside CAE canonical JSON."""


class StoryboardFormat(str):
    VIDEO = "VIDEO"
    CAROUSEL = "CAROUSEL"
    SUPERVISUAL = "SUPERVISUAL"
    PRESENTATION = "PRESENTATION"


class StoryboardExpression(BaseModel):
    """Common governed expression emitted by every format program."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    format_id: str
    program_id: str
    session_id: str
    revision_id: str
    editorial_storyboard_id: str
    semantic_program_id: str | None = None
    harness_id: str | None = None
    grammar_profile: str
    format_constraints: Dict[str, Any] = Field(default_factory=dict)
    source_evidence_refs: List[str] = Field(default_factory=list)
    scenes: List[Dict[str, Any]] = Field(default_factory=list)
    status: str = "COMPILED"
    canonical_sha256: str

    @field_validator("format_id", "program_id", "session_id", "revision_id", "editorial_storyboard_id")
    @classmethod
    def non_empty_identity(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("storyboard expression identity values cannot be empty")
        return value


class StoryboardProgramContract(BaseModel):
    """Inspection-friendly contract metadata shared by the four programs."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    program_id: str
    format_id: str
    grammar_profile: str
    constraints: Dict[str, Any]
    authority: str = (
        "EditorialStoryboardRecord and StoryboardRevision remain semantic and revision authority"
    )


def _dump(model: BaseModel) -> Dict[str, Any]:
    return model.model_dump(exclude_none=True)


def _scene_elements(scene: StoryboardScene) -> List[StoryboardElement]:
    return [element for shot in scene.shots for element in shot.elements]


def _validate_shared_revision(revision: StoryboardRevision) -> None:
    """Enforce the common evidence-first and authority boundary."""

    if not revision.editorial_storyboard_id:
        raise StoryboardProgramAuthorityError(
            "format compilation requires an existing EditorialStoryboard identity"
        )
    if not revision.source_evidence_refs:
        raise StoryboardProgramAuthorityError(
            "format compilation requires source_evidence_refs"
        )
    evidence = set(revision.source_evidence_refs)
    if len(evidence) != len(revision.source_evidence_refs):
        raise StoryboardProgramValidationError("source_evidence_refs must be deterministic and unique")
    if not revision.scenes:
        raise StoryboardProgramValidationError("format compilation requires at least one scene")
    scene_ids = [scene.scene_id for scene in revision.scenes]
    if len(scene_ids) != len(set(scene_ids)):
        raise StoryboardProgramValidationError("scene_id values must be unique")
    for scene in revision.scenes:
        if not set(scene.source_evidence_refs).issubset(evidence):
            raise StoryboardProgramAuthorityError(
                f"scene '{scene.scene_id}' references evidence outside the revision lineage"
            )
        for element in _scene_elements(scene):
            if not element.source_evidence_refs:
                raise StoryboardProgramAuthorityError(
                    f"element '{element.element_id}' has no evidence lineage"
                )
            if not set(element.source_evidence_refs).issubset(evidence):
                raise StoryboardProgramAuthorityError(
                    f"element '{element.element_id}' references evidence outside the revision lineage"
                )
            for asset in element.asset_references:
                if not asset.approved:
                    raise StoryboardProgramAuthorityError(
                        f"asset '{asset.asset_id}' is not operator-approved"
                    )
                if not asset.evidence_refs or not set(asset.evidence_refs).issubset(evidence):
                    raise StoryboardProgramAuthorityError(
                        f"asset '{asset.asset_id}' is not evidence-grounded"
                    )


def _require_contiguous_scene_order(scenes: Sequence[StoryboardScene], label: str) -> None:
    orders = [scene.scene_order for scene in scenes]
    if sorted(orders) != list(range(len(scenes))):
        raise StoryboardProgramValidationError(
            f"{label} scene order must be contiguous from zero"
        )


class BaseStoryboardProgram(ABC):
    """Shared compiler with format-specific validation hooks."""

    contract: StoryboardProgramContract

    def compile(self, revision: StoryboardRevision) -> StoryboardExpression:
        _validate_shared_revision(revision)
        self.validate(revision)
        payload = {
            "format_id": self.contract.format_id,
            "program_id": self.contract.program_id,
            "session_id": revision.session_id,
            "revision_id": revision.revision_id,
            "editorial_storyboard_id": revision.editorial_storyboard_id,
            "semantic_program_id": revision.semantic_program_id,
            "harness_id": revision.harness_id,
            "grammar_profile": self.contract.grammar_profile,
            "format_constraints": self.contract.constraints,
            "source_evidence_refs": list(revision.source_evidence_refs),
            "scenes": self.project_scenes(revision.scenes),
            "status": "COMPILED",
        }
        try:
            digest = canonical_sha256(payload)
        except CanonicalizationError as exc:
            raise StoryboardProgramCanonicalizationError(str(exc)) from exc
        return StoryboardExpression(canonical_sha256=digest, **payload)

    compile_revision = compile

    @abstractmethod
    def validate(self, revision: StoryboardRevision) -> None:
        raise NotImplementedError

    def project_scenes(self, scenes: Sequence[StoryboardScene]) -> List[Dict[str, Any]]:
        return [_dump(scene) for scene in sorted(scenes, key=lambda item: item.scene_order)]


class VideoStoryboardProgram(BaseStoryboardProgram):
    """Temporal storyboard grammar for source-grounded video expression."""

    contract = StoryboardProgramContract(
        program_id="video_storyboard_program",
        format_id=StoryboardFormat.VIDEO,
        grammar_profile="VIDEO_TEMPORAL_SEQUENCE_V1",
        constraints={
            "requires_temporal_structure": True,
            "shot_order": "non_overlapping_by_scene",
            "runtime_surface": "video_edit_program_or_openchatcut",
        },
    )

    def validate(self, revision: StoryboardRevision) -> None:
        for scene in revision.scenes:
            if not scene.shots:
                raise StoryboardProgramValidationError(
                    f"video scene '{scene.scene_id}' requires at least one shot"
                )
            previous_end = -1
            for shot in sorted(scene.shots, key=lambda item: item.start_ms):
                if shot.start_ms < previous_end:
                    raise StoryboardProgramValidationError(
                        f"video scene '{scene.scene_id}' contains overlapping shots"
                    )
                previous_end = shot.end_ms


class CarouselStoryboardProgram(BaseStoryboardProgram):
    """Slide progression grammar for source-grounded carousel composition."""

    contract = StoryboardProgramContract(
        program_id="carousel_storyboard_program",
        format_id=StoryboardFormat.CAROUSEL,
        grammar_profile="CAROUSEL_SLIDE_PROGRESSION_V1",
        constraints={
            "requires_slide_progression": True,
            "slide_order": "contiguous_from_zero",
            "one_scene_per_slide": True,
        },
    )

    def validate(self, revision: StoryboardRevision) -> None:
        _require_contiguous_scene_order(revision.scenes, "carousel")
        for scene in revision.scenes:
            if not _scene_elements(scene):
                raise StoryboardProgramValidationError(
                    f"carousel slide '{scene.scene_id}' requires at least one element"
                )

    def project_scenes(self, scenes: Sequence[StoryboardScene]) -> List[Dict[str, Any]]:
        return [
            {
                "slide_index": scene.scene_order,
                "scene_id": scene.scene_id,
                "semantic_purpose": scene.semantic_purpose,
                "source_evidence_refs": list(scene.source_evidence_refs),
                "elements": [_dump(element) for element in _scene_elements(scene)],
            }
            for scene in sorted(scenes, key=lambda item: item.scene_order)
        ]


class SuperVisualStoryboardProgram(BaseStoryboardProgram):
    """Bounded spatial composition grammar for a single visual expression."""

    contract = StoryboardProgramContract(
        program_id="supervisual_storyboard_program",
        format_id=StoryboardFormat.SUPERVISUAL,
        grammar_profile="SUPERVISUAL_SPATIAL_COMPOSITION_V1",
        constraints={
            "requires_spatial_composition": True,
            "coordinate_system": "basis_points_0_to_10000",
            "geometry_keys": ["x_bps", "y_bps", "width_bps", "height_bps"],
        },
    )

    def validate(self, revision: StoryboardRevision) -> None:
        for scene in revision.scenes:
            for element in _scene_elements(scene):
                geometry = element.properties.get("geometry")
                if not isinstance(geometry, Mapping):
                    raise StoryboardProgramValidationError(
                        f"supervisual element '{element.element_id}' requires geometry"
                    )
                required = ("x_bps", "y_bps", "width_bps", "height_bps")
                if any(key not in geometry for key in required):
                    raise StoryboardProgramValidationError(
                        f"supervisual element '{element.element_id}' has incomplete geometry"
                    )
                values = [geometry[key] for key in required]
                if any(not isinstance(value, int) for value in values):
                    raise StoryboardProgramValidationError(
                        f"supervisual element '{element.element_id}' geometry must use integer basis points"
                    )
                if any(value < 0 or value > 10000 for value in values):
                    raise StoryboardProgramValidationError(
                        f"supervisual element '{element.element_id}' geometry is outside safe bounds"
                    )
                if geometry["width_bps"] == 0 or geometry["height_bps"] == 0:
                    raise StoryboardProgramValidationError(
                        f"supervisual element '{element.element_id}' geometry must be visible"
                    )
                if geometry["x_bps"] + geometry["width_bps"] > 10000 or geometry["y_bps"] + geometry["height_bps"] > 10000:
                    raise StoryboardProgramValidationError(
                        f"supervisual element '{element.element_id}' geometry exceeds canvas bounds"
                    )


class PresentationStoryboardProgram(BaseStoryboardProgram):
    """Slide/build grammar for presentation runtime projections."""

    contract = StoryboardProgramContract(
        program_id="presentation_storyboard_program",
        format_id=StoryboardFormat.PRESENTATION,
        grammar_profile="PRESENTATION_SLIDE_BUILD_V1",
        constraints={
            "requires_slide_progression": True,
            "requires_build_semantics": True,
            "slide_order": "contiguous_from_zero",
            "build_step": "positive_integer_per_element",
        },
    )

    def validate(self, revision: StoryboardRevision) -> None:
        _require_contiguous_scene_order(revision.scenes, "presentation")
        for scene in revision.scenes:
            elements = _scene_elements(scene)
            if not elements:
                raise StoryboardProgramValidationError(
                    f"presentation slide '{scene.scene_id}' requires buildable elements"
                )
            build_steps: List[int] = []
            for element in elements:
                build_step = element.properties.get("build_step")
                if not isinstance(build_step, int) or build_step < 1:
                    raise StoryboardProgramValidationError(
                        f"presentation element '{element.element_id}' requires a positive build_step"
                    )
                build_steps.append(build_step)
            if len(build_steps) != len(set(build_steps)):
                raise StoryboardProgramValidationError(
                    f"presentation slide '{scene.scene_id}' has duplicate build_step values"
                )

    def project_scenes(self, scenes: Sequence[StoryboardScene]) -> List[Dict[str, Any]]:
        projected = super().project_scenes(scenes)
        for scene in projected:
            elements = [
                element
                for shot in scene.get("shots", [])
                for element in shot.get("elements", [])
            ]
            scene["build_order"] = sorted(
                [
                    {"element_id": element["element_id"], "build_step": element["properties"]["build_step"]}
                    for element in elements
                ],
                key=lambda item: item["build_step"],
            )
        return projected


STORYBOARD_PROGRAM_TYPES: Dict[str, Type[BaseStoryboardProgram]] = {
    StoryboardFormat.VIDEO: VideoStoryboardProgram,
    StoryboardFormat.CAROUSEL: CarouselStoryboardProgram,
    StoryboardFormat.SUPERVISUAL: SuperVisualStoryboardProgram,
    StoryboardFormat.PRESENTATION: PresentationStoryboardProgram,
}


def get_storyboard_program(format_id: str) -> BaseStoryboardProgram:
    """Return a deterministic format compiler or fail closed."""

    try:
        return STORYBOARD_PROGRAM_TYPES[format_id.upper()]()
    except KeyError as exc:
        raise StoryboardProgramValidationError(
            f"unsupported storyboard format '{format_id}'"
        ) from exc


__all__ = [
    "BaseStoryboardProgram",
    "CarouselStoryboardProgram",
    "PresentationStoryboardProgram",
    "STORYBOARD_PROGRAM_TYPES",
    "StoryboardExpression",
    "StoryboardFormat",
    "StoryboardProgramAuthorityError",
    "StoryboardProgramCanonicalizationError",
    "StoryboardProgramContract",
    "StoryboardProgramError",
    "StoryboardProgramValidationError",
    "SuperVisualStoryboardProgram",
    "VideoStoryboardProgram",
    "get_storyboard_program",
]
