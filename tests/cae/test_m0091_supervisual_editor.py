from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENGINE_ROOT = ROOT / "engines" / "visual"
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from supervisual.editor import CanonicalGeometryPort, Layer, Rect, SuperVisualEditor, SuperVisualValidationError


class TestGeometryPort(CanonicalGeometryPort):
    def validate(self, layers: list[Layer]) -> None:
        for index, left in enumerate(layers):
            for right in layers[index + 1 :]:
                if left.bbox.intersects(right.bbox) and not (left.overlap_allowed and right.overlap_allowed):
                    raise SuperVisualValidationError(f"BBOX_COLLISION:{left.layer_id}:{right.layer_id}")


def projection(*, bbox: dict[str, int] | None = None, annotations: list[dict] | None = None) -> dict:
    return {
        "format": "SUPERVISUAL",
        "composition_id": "composition:test",
        "state": "CANONICAL_PROJECTION",
        "renderer": {"kind": "SKIA_STATIC_RENDERER", "proof": "PROJECTION_ONLY"},
        "layers": [
            {
                "layer_id": "layer:quote",
                "kind": "TEXT",
                "role": "PRIMARY_CLAIM",
                "source_ref": {"object_id": "source:1", "version": "1.0.0", "sha256": "a" * 64},
                "bbox": bbox or {"x": 100000, "y": 100000, "width": 300000, "height": 200000},
                "text": "Source-backed claim",
                "annotations": annotations or [],
            }
        ],
    }


def test_m0091_success_exposes_all_distinct_primitive_roles() -> None:
    result = SuperVisualEditor(TestGeometryPort()).project(projection())
    assert result.primitive_roles == ("BBOX", "PRETEXT", "SKIA", "ROUGH_NOTATION")
    assert result.layers[0]["primitive_role"] == "BBOX"
    assert result.renderer["proof"] == "PROJECTION_ONLY"


def test_m0091_good_looking_but_wrong_layer_without_bbox_is_blocked() -> None:
    bad = projection()
    del bad["layers"][0]["bbox"]
    try:
        SuperVisualEditor(TestGeometryPort()).project(bad)
    except SuperVisualValidationError as exc:
        assert "no authoritative bbox" in str(exc)
    else:
        raise AssertionError("layer without authoritative BBOX was accepted")


def test_m0091_operator_annotation_proposal_is_typed_and_non_mutating() -> None:
    original = projection()
    before = copy.deepcopy(original)
    proposal = SuperVisualEditor(TestGeometryPort()).prepare_annotation(
        projection=original,
        target_layer_id="layer:quote",
        annotation_type="underline",
    )
    assert proposal.status == "PROPOSED"
    assert proposal.config["type"] == "underline"
    assert proposal.config["animate"] is False
    assert proposal.canonical_state_changed is False
    assert original == before


def test_m0091_unauthorized_revision_is_rejected() -> None:
    try:
        SuperVisualEditor(TestGeometryPort()).prepare_revision(
            parent_revision_ref={"object_id": "rev:1", "version": "1", "sha256": "b" * 64},
            operation={"type": "ANNOTATE", "target": "layer:quote"},
            proposed_by={"actor_type": "model", "workflow_role": "composer"},
        )
    except SuperVisualValidationError as exc:
        assert str(exc) == "operator actor required"
    else:
        raise AssertionError("unauthorized model actor was accepted")


def test_m0091_revision_identity_is_deterministic_for_replay() -> None:
    editor = SuperVisualEditor(TestGeometryPort())
    args = {
        "parent_revision_ref": {"object_id": "rev:1", "version": "1", "sha256": "b" * 64},
        "operation": {"type": "ANNOTATE", "target": "layer:quote", "annotation": "underline"},
        "proposed_by": {"actor_id": "operator:1", "actor_type": "human", "workflow_role": "operator"},
    }
    first = editor.prepare_revision(**args)
    second = editor.prepare_revision(**args)
    assert first.revision_id == second.revision_id
    assert first.canonical_state_changed is False


def test_m0091_geometry_operation_is_deterministic_and_fail_closed_on_collision() -> None:
    editor = SuperVisualEditor(TestGeometryPort())
    result = editor.apply_geometry_operation_for_review(
        projection(), layer_id="layer:quote", operation="MOVE_X", amount=50000
    )
    assert result["status"] == "PROPOSED"
    assert result["canonical_state_changed"] is False
    assert result["bbox"]["x"] == 150000

    collision = projection()
    collision["layers"].append(
        {
            "layer_id": "layer:second",
            "kind": "IMAGE",
            "role": "SUPPORT",
            "source_ref": {"object_id": "source:2", "version": "1.0.0", "sha256": "c" * 64},
            "bbox": {"x": 350000, "y": 100000, "width": 250000, "height": 200000},
            "text": None,
            "annotations": [],
        }
    )
    try:
        editor.project(collision)
    except SuperVisualValidationError as exc:
        assert str(exc).startswith("BBOX_COLLISION:")
    else:
        raise AssertionError("colliding composition was accepted")
