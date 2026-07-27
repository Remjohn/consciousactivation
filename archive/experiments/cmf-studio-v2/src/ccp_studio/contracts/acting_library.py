"""64-state acting library contracts for TS-CMF-019."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class ActingEmotionalFamily(str, Enum):
    confident = "confident"
    warm = "warm"
    reflective = "reflective"
    serious = "serious"
    challenging = "challenging"
    playful = "playful"
    urgent = "urgent"
    celebratory = "celebratory"


class ActingGestureFamily(str, Enum):
    open_hands_explaining = "open_hands_explaining"
    pointing_directing = "pointing_directing"
    inviting_open_palms = "inviting_open_palms"
    grounded_authority = "grounded_authority"
    thinking_hand_to_face = "thinking_hand_to_face"
    emphasis_gesture = "emphasis_gesture"
    uncertainty_shrug = "uncertainty_shrug"
    dynamic_uplift = "dynamic_uplift"


class ActingReferenceStatus(str, Enum):
    generated = "generated"
    repair_requested = "repair_requested"
    replaced = "replaced"
    rejected = "rejected"
    approved = "approved"
    locked = "locked"


class ActingLibraryAction(str, Enum):
    generated = "generated"
    evaluated = "evaluated"
    repair_requested = "repair_requested"
    rejected = "rejected"
    replaced = "replaced"
    approved = "approved"
    locked = "locked"


class ActingStateCell(BaseModel):
    schema_version: Literal["cmf.acting_state_cell.v1"]
    emotional_family: ActingEmotionalFamily
    gesture_family: ActingGestureFamily
    matrix_row: int = Field(ge=1, le=8)
    matrix_column: int = Field(ge=1, le=8)
    state_key: str = Field(min_length=1)


class ActingProviderReceipt(BaseModel):
    schema_version: Literal["cmf.acting_provider_receipt.v1"]
    provider_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    brand_genesis_session_id: UUID
    provider_name: str = Field(min_length=1)
    request_hash: str = Field(min_length=1)
    artifact_uri: str = Field(min_length=1)
    source_artifact_ids: list[UUID] = Field(min_length=1)
    written_at: datetime


class ActingReferenceEvaluation(BaseModel):
    schema_version: Literal["cmf.acting_reference_evaluation.v1"]
    evaluation_receipt_id: UUID
    acting_reference_id: UUID
    likeness_score: float = Field(ge=0, le=1)
    gesture_clarity_score: float = Field(ge=0, le=1)
    hand_quality_score: float = Field(ge=0, le=1)
    paper_texture_score: float = Field(ge=0, le=1)
    style_adherence_score: float = Field(ge=0, le=1)
    negative_space_score: float = Field(ge=0, le=1)
    production_usability_score: float = Field(ge=0, le=1)
    failure_notes: list[str] = Field(default_factory=list)
    evaluated_at: datetime

    def passed(self, threshold: float = 0.8) -> bool:
        scores = [
            self.likeness_score,
            self.gesture_clarity_score,
            self.hand_quality_score,
            self.paper_texture_score,
            self.style_adherence_score,
            self.negative_space_score,
            self.production_usability_score,
        ]
        return all(score >= threshold for score in scores) and not self.failure_notes


class ActingReference(BaseModel):
    schema_version: Literal["cmf.acting_reference.v1"]
    acting_reference_id: UUID
    organization_id: UUID
    brand_id: UUID
    brand_genesis_session_id: UUID
    acting_library_version_id: UUID | None = None
    state_cell: ActingStateCell
    source_artifact_ids: list[UUID] = Field(min_length=1)
    provider_receipt_id: UUID
    artifact_uri: str = Field(min_length=1)
    content_hash: str = Field(min_length=1)
    body_language: str = Field(min_length=1)
    facial_expression: str = Field(min_length=1)
    energy_level: str = Field(min_length=1)
    framing: str = Field(min_length=1)
    orientation: str = Field(min_length=1)
    layout_bias: str = Field(min_length=1)
    status: ActingReferenceStatus
    latest_evaluation: ActingReferenceEvaluation | None = None
    replaces_reference_id: UUID | None = None
    created_at: datetime
    updated_at: datetime


class ActingLibraryVersion(BaseModel):
    schema_version: Literal["cmf.acting_library_version.v1"]
    acting_library_version_id: UUID
    organization_id: UUID
    brand_id: UUID
    brand_genesis_session_id: UUID
    version_hash: str
    acting_reference_ids: list[UUID] = Field(default_factory=list)
    locked: bool = False
    locked_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class ActingLibraryReceipt(BaseModel):
    schema_version: Literal["cmf.acting_library_receipt.v1"]
    acting_library_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    brand_genesis_session_id: UUID
    acting_library_version_id: UUID | None = None
    acting_reference_id: UUID | None = None
    action: ActingLibraryAction
    decision_code: str
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime


EMOTIONAL_FAMILIES: tuple[ActingEmotionalFamily, ...] = tuple(ActingEmotionalFamily)
GESTURE_FAMILIES: tuple[ActingGestureFamily, ...] = tuple(ActingGestureFamily)


def acting_state_matrix() -> list[ActingStateCell]:
    cells: list[ActingStateCell] = []
    for row, emotional_family in enumerate(EMOTIONAL_FAMILIES, start=1):
        for column, gesture_family in enumerate(GESTURE_FAMILIES, start=1):
            cells.append(
                ActingStateCell(
                    schema_version="cmf.acting_state_cell.v1",
                    emotional_family=emotional_family,
                    gesture_family=gesture_family,
                    matrix_row=row,
                    matrix_column=column,
                    state_key=f"{emotional_family.value}_{_gesture_short_key(gesture_family)}",
                )
            )
    return cells


def new_acting_library_version(
    *,
    organization_id: UUID,
    brand_id: UUID,
    brand_genesis_session_id: UUID,
) -> ActingLibraryVersion:
    now = utc_now()
    return ActingLibraryVersion(
        schema_version="cmf.acting_library_version.v1",
        acting_library_version_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        brand_genesis_session_id=brand_genesis_session_id,
        version_hash="draft",
        acting_reference_ids=[],
        created_at=now,
        updated_at=now,
    )


def acting_reference_content_hash(parts: list[str]) -> str:
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


def acting_library_version_hash(references: list[ActingReference]) -> str:
    payload = [
        {
            "acting_reference_id": str(reference.acting_reference_id),
            "state_key": reference.state_cell.state_key,
            "content_hash": reference.content_hash,
            "provider_receipt_id": str(reference.provider_receipt_id),
            "status": reference.status.value,
        }
        for reference in sorted(references, key=lambda item: item.state_cell.state_key)
    ]
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def new_acting_library_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    brand_genesis_session_id: UUID,
    action: ActingLibraryAction,
    decision_code: str,
    evidence_refs: list[str],
    acting_library_version_id: UUID | None = None,
    acting_reference_id: UUID | None = None,
) -> ActingLibraryReceipt:
    return ActingLibraryReceipt(
        schema_version="cmf.acting_library_receipt.v1",
        acting_library_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        brand_genesis_session_id=brand_genesis_session_id,
        acting_library_version_id=acting_library_version_id,
        acting_reference_id=acting_reference_id,
        action=action,
        decision_code=decision_code,
        evidence_refs=evidence_refs,
        written_at=utc_now(),
    )


def _gesture_short_key(gesture_family: ActingGestureFamily) -> str:
    return {
        ActingGestureFamily.open_hands_explaining: "open_explain",
        ActingGestureFamily.pointing_directing: "point",
        ActingGestureFamily.inviting_open_palms: "invite",
        ActingGestureFamily.grounded_authority: "authority",
        ActingGestureFamily.thinking_hand_to_face: "think",
        ActingGestureFamily.emphasis_gesture: "emphasis",
        ActingGestureFamily.uncertainty_shrug: "shrug",
        ActingGestureFamily.dynamic_uplift: "uplift",
    }[gesture_family]
