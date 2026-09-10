"""M0077 bounded ArcReel review/regeneration behavior adapter.

This module is deliberately provider-neutral. It extracts interaction contracts from
ArcReel without importing its runtime, provider/model routing, or state authority.
CAE canonical storyboard/revision/state systems remain authoritative.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Any, Mapping


class ArcReelObservedAction(str, Enum):
    REVIEW = "REVIEW"
    APPROVE = "APPROVE"
    EDIT = "EDIT"
    REGENERATE = "REGENERATE"
    INSPECT_TIMELINE = "INSPECT_TIMELINE"


class CAETarget(str, Enum):
    STORYBOARD_REVISION = "STORYBOARD_REVISION"
    VISUAL_DERIVATIVE_REVISION = "VISUAL_DERIVATIVE_REVISION"
    TIMELINE_PROJECTION = "TIMELINE_PROJECTION"
    OPERATOR_GATE = "OPERATOR_GATE"


class AdapterContractError(ValueError):
    """Raised when an extracted interaction cannot be safely mapped to CAE."""


@dataclass(frozen=True)
class ArcReelReviewEvent:
    """A behavior observation, not an ArcReel runtime/state object."""

    interaction_id: str
    action: ArcReelObservedAction
    project_ref: str
    stage: str
    actor_id: str
    actor_type: str
    storyboard_id: str
    source_evidence_refs: tuple[str, ...]
    source_artifact_ref: str | None
    expected_state_version: int
    observed_state_version: int
    operator_approved: bool
    semantic_revision_requested: bool = False
    generation_requested: bool = False
    rejected_candidate_ids: tuple[str, ...] = ()
    canvas_projection_ref: str | None = None
    timeline_edit_requested: bool = False


@dataclass(frozen=True)
class CAEInteractionMapping:
    """Deterministic translation of one external behavior into a CAE contract."""

    interaction_id: str
    target: CAETarget
    canonical_operation: str
    required_lane: str
    requires_operator_gate: bool
    preserve_provenance: bool
    retain_rejected_candidates: bool
    evidence_first_required: bool
    state_version: int
    notes: tuple[str, ...]
    mapping_sha256: str


def map_arcreel_review_event(event: ArcReelReviewEvent) -> CAEInteractionMapping:
    """Map ArcReel-like review behavior to existing CAE authority, fail-closed."""
    _validate(event)

    if event.action is ArcReelObservedAction.INSPECT_TIMELINE:
        target = CAETarget.TIMELINE_PROJECTION
        operation = "observe_existing_timeline_projection"
        lane = "OPERATOR"
        gate = False
        evidence_first = True
        notes = (
            "Use TimelineProjectionModel; do not persist a second canvas/timeline authority.",
            "Edits must route through existing revision compilation/execution contracts.",
        )
    elif event.action is ArcReelObservedAction.EDIT:
        target = CAETarget.STORYBOARD_REVISION if event.semantic_revision_requested else CAETarget.VISUAL_DERIVATIVE_REVISION
        operation = "compile_existing_revision_program"
        lane = "COMMANDER"
        gate = True
        evidence_first = True
        notes = (
            "Use canonical CAE revision program and existing human-resolution path.",
            "Do not mutate semantic meaning in the adapter.",
        )
    elif event.action is ArcReelObservedAction.REGENERATE:
        target = CAETarget.STORYBOARD_REVISION
        operation = "request_operator_constrained_regeneration"
        lane = "COMMANDER"
        gate = True
        evidence_first = True
        notes = (
            "Delegate candidate regeneration to existing operator_request_regeneration lineage.",
            "Keep predecessor/rejected candidates and decision receipts immutable.",
        )
    elif event.action is ArcReelObservedAction.APPROVE:
        target = CAETarget.OPERATOR_GATE
        operation = "approve_existing_canonical_gate"
        lane = "COMMANDER"
        gate = True
        evidence_first = True
        notes = (
            "Approval advances an existing CAE state machine; it does not create external authority.",
        )
    else:
        target = CAETarget.STORYBOARD_REVISION
        operation = "observe_existing_review_checkpoint"
        lane = "OPERATOR"
        gate = True
        evidence_first = True
        notes = (
            "Review remains a checkpoint over canonical CAE state.",
        )

    canonical = {
        "interaction_id": event.interaction_id,
        "target": target.value,
        "canonical_operation": operation,
        "required_lane": lane,
        "requires_operator_gate": gate,
        "preserve_provenance": True,
        "retain_rejected_candidates": event.action is ArcReelObservedAction.REGENERATE or bool(event.rejected_candidate_ids),
        "evidence_first_required": evidence_first,
        "state_version": event.observed_state_version,
        "notes": list(notes),
    }
    digest = _sha256_json(canonical)
    return CAEInteractionMapping(
        interaction_id=event.interaction_id,
        target=target,
        canonical_operation=operation,
        required_lane=lane,
        requires_operator_gate=gate,
        preserve_provenance=True,
        retain_rejected_candidates=canonical["retain_rejected_candidates"],
        evidence_first_required=evidence_first,
        state_version=event.observed_state_version,
        notes=notes,
        mapping_sha256=digest,
    )


def replay_fingerprint(event: ArcReelReviewEvent) -> str:
    """Stable fingerprint proving deterministic mapping/replay input identity."""
    return _sha256_json(asdict(event))


def _validate(event: ArcReelReviewEvent) -> None:
    if not event.interaction_id.strip():
        raise AdapterContractError("interaction_id is required")
    if not event.project_ref.strip() or not event.project_ref.startswith("ref:"):
        raise AdapterContractError("project_ref must be a canonical ref: value")
    if not event.storyboard_id.strip():
        raise AdapterContractError("storyboard_id is required")
    if not event.actor_id.strip():
        raise AdapterContractError("actor_id is required")
    if event.actor_type != "human":
        raise AdapterContractError("operator-controlled actions require actor_type=human")
    if event.expected_state_version != event.observed_state_version:
        raise AdapterContractError("stale state: expected_state_version does not match observed_state_version")
    if event.observed_state_version < 1:
        raise AdapterContractError("observed_state_version must be >= 1")

    mutating = event.action in {
        ArcReelObservedAction.APPROVE,
        ArcReelObservedAction.EDIT,
        ArcReelObservedAction.REGENERATE,
    }
    if mutating and not event.operator_approved:
        raise AdapterContractError("mutating production progression requires operator approval")

    if event.action in {ArcReelObservedAction.REVIEW, ArcReelObservedAction.APPROVE, ArcReelObservedAction.REGENERATE, ArcReelObservedAction.EDIT}:
        if not event.source_evidence_refs:
            raise AdapterContractError("evidence lineage is required for review/production actions")
        if event.source_artifact_ref is None:
            raise AdapterContractError("source artifact provenance is required for review/production actions")

    if event.action is ArcReelObservedAction.REGENERATE and not event.generation_requested:
        raise AdapterContractError("regeneration mapping requires generation_requested=true")

    if event.action is ArcReelObservedAction.EDIT and event.generation_requested:
        raise AdapterContractError("edit and generation requests must remain distinct")

    if event.action is ArcReelObservedAction.INSPECT_TIMELINE and not event.canvas_projection_ref:
        raise AdapterContractError("timeline inspection requires an existing canonical projection ref")


def _sha256_json(value: Mapping[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(encoded).hexdigest()
