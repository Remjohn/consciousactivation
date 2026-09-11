from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha256
from typing import Any, Mapping, Sequence

SCALE = 1_000_000
ANNOTATION_TYPES = frozenset(
    {"underline", "box", "circle", "highlight", "strike-through", "crossed-off", "bracket"}
)


class SuperVisualValidationError(ValueError):
    """Raised when an editor operation cannot be proven safe and deterministic."""


class SuperVisualDependencyError(RuntimeError):
    """Raised when the canonical CAE primitive services are unavailable."""


class PrimitiveRole:
    BBOX = "BBOX"
    PRETEXT = "PRETEXT"
    SKIA = "SKIA"
    ROUGH_NOTATION = "ROUGH_NOTATION"


@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    width: int
    height: int

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any], field: str = "bbox") -> "Rect":
        if set(value) != {"x", "y", "width", "height"}:
            raise SuperVisualValidationError(f"{field} invalid shape")
        values = []
        for key in ("x", "y", "width", "height"):
            raw = value[key]
            if not isinstance(raw, int) or isinstance(raw, bool):
                raise SuperVisualValidationError(f"{field}.{key} must be an integer")
            values.append(raw)
        rect = cls(*values)
        if rect.width <= 0 or rect.height <= 0:
            raise SuperVisualValidationError(f"{field} must be visible")
        if rect.x < 0 or rect.y < 0 or rect.x + rect.width > SCALE or rect.y + rect.height > SCALE:
            raise SuperVisualValidationError(f"{field} outside normalized canvas")
        return rect

    def to_dict(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y, "width": self.width, "height": self.height}

    def intersects(self, other: "Rect") -> bool:
        return (
            self.x < other.x + other.width
            and other.x < self.x + self.width
            and self.y < other.y + other.height
            and other.y < self.y + self.height
        )


@dataclass(frozen=True)
class Layer:
    layer_id: str
    bbox: Rect
    kind: str
    role: str
    source_ref: Mapping[str, Any] | None
    text: str | None
    annotations: tuple[Mapping[str, Any], ...]
    overlap_allowed: bool = False


@dataclass(frozen=True)
class AnnotationProposal:
    proposal_id: str
    target_layer_id: str
    annotation_type: str
    config: Mapping[str, Any]
    status: str = "PROPOSED"
    canonical_state_changed: bool = False


@dataclass(frozen=True)
class EditorRevision:
    revision_id: str
    parent_revision_ref: Mapping[str, Any]
    operation: Mapping[str, Any]
    proposed_by: Mapping[str, Any]
    canonical_state_changed: bool = False


@dataclass(frozen=True)
class SuperVisualProjection:
    composition_id: str | None
    state: str
    primitive_roles: tuple[str, ...]
    layers: tuple[Mapping[str, Any], ...]
    annotations: tuple[Mapping[str, Any], ...]
    evidence_path: tuple[str, ...]
    renderer: Mapping[str, Any]
    authority: str = "CAE_CANONICAL_SEMANTIC_AUTHORITY"

    def to_dict(self) -> dict[str, Any]:
        return {
            "composition_id": self.composition_id,
            "state": self.state,
            "primitive_roles": list(self.primitive_roles),
            "layers": list(self.layers),
            "annotations": list(self.annotations),
            "evidence_path": list(self.evidence_path),
            "renderer": dict(self.renderer),
            "authority": self.authority,
        }


def _digest(payload: Mapping[str, Any]) -> str:
    import json

    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return sha256(canonical.encode("utf-8")).hexdigest()


def _layer_from_projection(raw: Mapping[str, Any], index: int) -> Layer:
    layer_id = str(raw.get("layer_id") or raw.get("item_id") or f"layer:{index}")
    bbox_value = raw.get("bbox")
    if bbox_value is None:
        raise SuperVisualValidationError(f"layer {layer_id} has no authoritative bbox")
    return Layer(
        layer_id=layer_id,
        bbox=Rect.from_mapping(bbox_value, f"layers[{index}].bbox"),
        kind=str(raw.get("kind", "UNKNOWN")),
        role=str(raw.get("role", "UNKNOWN")),
        source_ref=raw.get("source_ref"),
        text=raw.get("text"),
        annotations=tuple(raw.get("annotations", ()) or ()),
        overlap_allowed=raw.get("overlap_allowed") is True,
    )


class CanonicalGeometryPort:
    """Small adapter around CAE's existing BBOX/geometry authority."""

    def validate(self, layers: Sequence[Layer]) -> None:
        raise NotImplementedError


class CaeCompositionServices(CanonicalGeometryPort):
    """Use the existing CAE BBox and GeometryValidator implementations."""

    def __init__(self) -> None:
        try:
            from cmf_pipeline.composition.geometry import BBox, GeometryValidator
            from cmf_pipeline.composition.pretext import PretextEngine
            from cmf_pipeline.composition.skia_renderer import SkiaStaticRenderer
        except Exception as exc:  # pragma: no cover - environment-dependent import
            raise SuperVisualDependencyError(
                "canonical CAE composition services are unavailable; "
                "install the pipeline runtime dependencies before using the production editor"
            ) from exc
        self.bbox_type = BBox
        self.geometry = GeometryValidator()
        self.pretext = PretextEngine()
        self.renderer = SkiaStaticRenderer()

    def validate(self, layers: Sequence[Layer]) -> None:
        elements = [
            {
                "element_id": layer.layer_id,
                "bbox": layer.bbox.to_dict(),
                "overlap_allowed": layer.overlap_allowed,
            }
            for layer in layers
        ]
        result = self.geometry.validate_elements(elements)
        if result["result"] != "PASS":
            violation = result["violations"][0]
            raise SuperVisualValidationError(
                f"BBOX_COLLISION:{violation['a']}:{violation['b']}"
            )

    def text_fit(self, text: str, width_px: int, height_px: int, font_size_px: int) -> Mapping[str, Any]:
        return self.pretext.fit(text, width_px, height_px, font_size_px).to_dict()


class SuperVisualEditor:
    """Deterministic composition/editor facade over the four primitive roles.

    The editor accepts already-resolved CAE projection data. It can prepare typed
    revisions but never mutates canonical state or promotes a proposal.
    """

    def __init__(self, services: CanonicalGeometryPort | None = None) -> None:
        self.services = services

    @classmethod
    def from_cae(cls) -> "SuperVisualEditor":
        return cls(CaeCompositionServices())

    primitive_owners = {
        PrimitiveRole.BBOX: "geometry + spatial validation",
        PrimitiveRole.PRETEXT: "text measurement + fit",
        PrimitiveRole.SKIA: "rendering substrate + display list",
        PrimitiveRole.ROUGH_NOTATION: "annotation primitive configuration",
    }

    def project(self, projection: Mapping[str, Any]) -> SuperVisualProjection:
        if projection.get("format") not in (None, "SUPERVISUAL"):
            raise SuperVisualValidationError("projection must be SuperVisual")
        raw_layers = projection.get("layers", ())
        layers = tuple(_layer_from_projection(raw, i) for i, raw in enumerate(raw_layers))
        self._validate_geometry(layers)
        annotations = tuple(
            annotation
            for layer in layers
            for annotation in layer.annotations
        )
        renderer = dict(projection.get("renderer", {"kind": "SKIA_STATIC_RENDERER", "proof": "PROJECTION_ONLY"}))
        renderer.setdefault("proof", "PROJECTION_ONLY")
        return SuperVisualProjection(
            composition_id=projection.get("composition_id"),
            state=str(projection.get("state", "CANONICAL_PROJECTION")),
            primitive_roles=(
                PrimitiveRole.BBOX,
                PrimitiveRole.PRETEXT,
                PrimitiveRole.SKIA,
                PrimitiveRole.ROUGH_NOTATION,
            ),
            layers=tuple(
                {
                    "layer_id": layer.layer_id,
                    "primitive_role": PrimitiveRole.BBOX,
                    "geometry": layer.bbox.to_dict(),
                    "source_ref": layer.source_ref,
                    "role": layer.role,
                    "kind": layer.kind,
                }
                for layer in layers
            ),
            annotations=annotations,
            evidence_path=("RETRIEVE", "TRANSFORM", "COMPOSE", "GENERATE"),
            renderer=renderer,
        )

    def prepare_annotation(
        self,
        *,
        projection: Mapping[str, Any],
        target_layer_id: str,
        annotation_type: str,
        config: Mapping[str, Any] | None = None,
    ) -> AnnotationProposal:
        view = self.project(projection)
        if target_layer_id not in {str(layer["layer_id"]) for layer in view.layers}:
            raise SuperVisualValidationError(f"unknown annotation target: {target_layer_id}")
        if annotation_type not in ANNOTATION_TYPES:
            raise SuperVisualValidationError(f"unsupported annotation type: {annotation_type}")
        clean_config = dict(config or {})
        clean_config.setdefault("type", annotation_type)
        clean_config.setdefault("animate", False)
        clean_config.setdefault("source", "ROUGH_NOTATION_PRIMITIVE")
        identity = _digest(
            {
                "composition_id": view.composition_id,
                "target_layer_id": target_layer_id,
                "annotation_type": annotation_type,
                "config": clean_config,
            }
        )
        return AnnotationProposal(
            proposal_id=f"visual-annotation:{identity[:24]}",
            target_layer_id=target_layer_id,
            annotation_type=annotation_type,
            config=clean_config,
        )

    def prepare_revision(
        self,
        *,
        parent_revision_ref: Mapping[str, Any],
        operation: Mapping[str, Any],
        proposed_by: Mapping[str, Any],
    ) -> EditorRevision:
        if proposed_by.get("actor_type") != "human" or proposed_by.get("workflow_role") != "operator":
            raise SuperVisualValidationError("operator actor required")
        payload = {
            "parent_revision_ref": dict(parent_revision_ref),
            "operation": dict(operation),
            "proposed_by": dict(proposed_by),
        }
        return EditorRevision(
            revision_id=f"visual-revision:{_digest(payload)[:24]}",
            parent_revision_ref=dict(parent_revision_ref),
            operation=dict(operation),
            proposed_by=dict(proposed_by),
        )

    def apply_geometry_operation_for_review(
        self,
        projection: Mapping[str, Any],
        *,
        layer_id: str,
        operation: str,
        amount: int,
    ) -> dict[str, Any]:
        """Return a deterministic draft; never persist or promote it."""
        layers = [_layer_from_projection(raw, i) for i, raw in enumerate(projection.get("layers", ()))]
        by_id = {layer.layer_id: layer for layer in layers}
        if layer_id not in by_id:
            raise SuperVisualValidationError(f"unknown layer: {layer_id}")
        target = by_id[layer_id]
        if operation == "MOVE_X":
            next_box = replace(target.bbox, x=target.bbox.x + amount)
        elif operation == "MOVE_Y":
            next_box = replace(target.bbox, y=target.bbox.y + amount)
        elif operation == "RESIZE":
            next_width = target.bbox.width + amount
            next_height = target.bbox.height + amount
            next_box = replace(target.bbox, width=next_width, height=next_height)
        else:
            raise SuperVisualValidationError(f"unsupported geometry operation: {operation}")
        next_box = Rect.from_mapping(next_box.to_dict())
        updated = replace(target, bbox=next_box)
        next_layers = tuple(updated if layer.layer_id == layer_id else layer for layer in layers)
        self._validate_geometry(next_layers)
        return {
            "status": "PROPOSED",
            "canonical_state_changed": False,
            "target_layer_id": layer_id,
            "operation": operation,
            "amount": amount,
            "bbox": next_box.to_dict(),
            "geometry_validation": "PASS",
        }

    def _validate_geometry(self, layers: Sequence[Layer]) -> None:
        if self.services is not None:
            self.services.validate(layers)
            return
        for index, left in enumerate(layers):
            for right in layers[index + 1 :]:
                if left.bbox.intersects(right.bbox) and not (left.overlap_allowed and right.overlap_allowed):
                    raise SuperVisualValidationError(
                        f"BBOX_COLLISION:{left.layer_id}:{right.layer_id}"
                    )
