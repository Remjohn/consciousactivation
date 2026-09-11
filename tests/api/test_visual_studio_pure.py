from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.services.visual_studio_contracts import assert_operator, build_visual_validation


def test_visual_studio_rejects_non_operator_actor() -> None:
    from fastapi import HTTPException
    try:
        assert_operator({"actor_type": "model_program", "workflow_role": "composer"})
    except HTTPException as exc:
        assert exc.status_code == 403
        assert exc.detail["error_code"] == "OPERATOR_AUTHORIZATION_REQUIRED"
    else:
        raise AssertionError("non-operator actor was accepted")


def test_good_looking_but_unproven_layer_is_blocked_without_source_lineage() -> None:
    report = build_visual_validation({"layer_id": "layer:1", "source_ref": None}, 1)
    assert report["source_lineage"] == "BLOCKED"
    assert report["semantic_correctness"] == "OPERATOR_REVIEW_REQUIRED"
