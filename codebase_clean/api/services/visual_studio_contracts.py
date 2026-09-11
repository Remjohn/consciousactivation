from __future__ import annotations
from fastapi import HTTPException


def assert_operator(actor: dict[str, str]) -> None:
    if actor.get("actor_type") != "human" or actor.get("workflow_role") != "operator":
        raise HTTPException(
            status_code=403,
            detail={
                "error_code": "OPERATOR_AUTHORIZATION_REQUIRED",
                "message": "visual studio actions require a human operator actor",
            },
        )


def build_visual_validation(selected_layer: dict | None, item_count: int) -> dict[str, str]:
    """Deterministic inspection gate: absence of lineage blocks visual editing even when geometry renders plausibly."""
    return {
        "source_lineage": "PASS" if selected_layer and selected_layer.get("source_ref") else "BLOCKED",
        "source_quality": "NOT_OBSERVED",
        "geometry": "NOT_OBSERVED",
        "keyframes": "NOT_OBSERVED" if not item_count else "NOT_RECORDED_IN_CANONICAL_PROJECTION",
        "semantic_correctness": "OPERATOR_REVIEW_REQUIRED",
    }
