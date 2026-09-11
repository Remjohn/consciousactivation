"""Carousel runtime adapter for CAE-M0093.

The adapter compiles the canonical CarouselStoryboardProgram into an in-memory Open Carrusel-
compatible payload. It does not write to Open Carrusel storage, call its agents, or promote state.
"""

from __future__ import annotations

from typing import Any

from ca_contracts import canonical_sha256
from ca_runtime.storyboard_programs import StoryboardFormat
from adapters.storyboard_runtime import (
    GovernedStoryboardRuntimeInput,
    RuntimeArtifact,
    StoryboardRuntimeValidationError,
    expression_runtime_sha,
    open_carrusel_dimensions,
    render_slide_html,
    validate_runtime_input,
)

OPEN_CARRUSEL_UPSTREAM = {
    "repository": "https://github.com/Hainrixz/open-carrusel",
    "commit": "8ba717ba4d59c8a9a5f64d278f6e83cbea34efde",
    "license": "MIT",
}


class CarouselStoryboardRuntimeAdapter:
    """Project a compiled CarouselStoryboardProgram into downstream carousel syntax."""

    program_id = "carousel_storyboard_program"
    format_id = StoryboardFormat.CAROUSEL
    runtime_id = "open-carrusel-compatible-preview"

    def __init__(self, *, aspect_ratio: str = "4:5") -> None:
        width, height = open_carrusel_dimensions(aspect_ratio)
        self.aspect_ratio = aspect_ratio
        self.width = width
        self.height = height

    def compile(self, handoff: GovernedStoryboardRuntimeInput) -> RuntimeArtifact:
        expression = validate_runtime_input(
            handoff,
            expected_program_id=self.program_id,
            expected_format_id=self.format_id,
        )
        if len(expression.scenes) > 20:
            raise StoryboardRuntimeValidationError(
                "Open Carrusel preview/export contract permits at most 20 slides"
            )

        slides: list[dict[str, Any]] = []
        for scene in expression.scenes:
            elements = []
            for element_payload in scene["elements"]:
                # Reuse the exact canonical element projection rather than reinterpreting it.
                elements.append(element_payload)
            # The HTML projection is generated from the canonical scene dict without a second
            # semantic model; element metadata remains embedded in the downstream HTML.
            scene_html = render_slide_html(
                scene_id=scene["scene_id"],
                semantic_purpose=scene["semantic_purpose"],
                elements=[
                    _element_model_from_payload(payload)
                    for payload in elements
                ],
                width=self.width,
                height=self.height,
            )
            slides.append(
                {
                    "id": f"cae-{scene['scene_id']}",
                    "html": scene_html,
                    "previousVersions": [],
                    "order": scene["slide_index"],
                    "notes": _slide_notes(scene),
                }
            )

        carousel = {
            "id": f"cae-{handoff.revision.revision_id}",
            "name": f"CAE {handoff.revision.editorial_storyboard_id}",
            "aspectRatio": self.aspect_ratio,
            "slides": slides,
            "referenceImages": [],
            "chatSessionId": None,
            "isTemplate": False,
            "tags": ["cae", "storyboard"],
            "createdAt": handoff.revision.created_at,
            "updatedAt": handoff.revision.created_at,
        }
        payload = {
            "carousels": [carousel],
            "cae_lineage": {
                "workspace_id": handoff.revision.workspace_id,
                "session_id": handoff.revision.session_id,
                "revision_id": handoff.revision.revision_id,
                "editorial_storyboard_id": handoff.revision.editorial_storyboard_id,
                "expression_sha256": expression.canonical_sha256,
                "validation_report_id": handoff.validation_report.report_id,
                "compile_receipt_id": handoff.compile_receipt.receipt_id,
                "receipt_lineage_sha256": handoff.compile_receipt.lineage_sha256,
            },
        }
        artifact_sha = expression_runtime_sha(payload)
        return RuntimeArtifact(
            artifact_id=f"carousel-runtime-{handoff.revision.revision_id}",
            runtime=self.runtime_id,
            format_id=self.format_id,
            revision_id=handoff.revision.revision_id,
            expression_sha256=expression.canonical_sha256,
            artifact_sha256=artifact_sha,
            lineage_sha256=handoff.compile_receipt.lineage_sha256,
            payload=payload,
            native_reachability_proven=False,
            environment_requirements=(
                "Open Carrusel source tree/runtime at the pinned upstream commit",
                "Browser-capable preview surface",
                f"slide dimensions {self.width}x{self.height}px",
            ),
        )


def _slide_notes(scene: dict[str, Any]) -> str:
    return (
        f"CAE semantic purpose: {scene['semantic_purpose']}\n"
        f"Source evidence: {', '.join(scene['source_evidence_refs'])}"
    )


def _element_model_from_payload(payload: dict[str, Any]):
    """Rehydrate only the fields render_element_html consumes.

    The runtime projection is not a second storyboard model; this tiny local shape is deliberately
    structural and derives every value from the already-compiled expression.
    """
    from types import SimpleNamespace

    assets = []
    for asset_payload in payload.get("asset_references", []):
        assets.append(
            SimpleNamespace(
                asset_id=asset_payload["asset_id"],
                source_uri=asset_payload.get("source_uri"),
                rights_status=asset_payload.get("rights_status", "UNVERIFIED"),
                source_quality=asset_payload.get("source_quality", "UNKNOWN"),
            )
        )
    return SimpleNamespace(
        element_id=payload["element_id"],
        semantic_purpose=payload["semantic_purpose"],
        source_evidence_refs=payload.get("source_evidence_refs", []),
        asset_references=assets,
    )


__all__ = ["CarouselStoryboardRuntimeAdapter", "OPEN_CARRUSEL_UPSTREAM"]
