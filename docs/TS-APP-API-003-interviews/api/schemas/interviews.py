from __future__ import annotations
from typing import Literal
from pydantic import BaseModel


class RefModel(BaseModel):
    object_id: str
    version: str
    sha256: str


class MediaAssetSummary(BaseModel):
    asset_id: str
    sha256: str
    bytes: int
    media_type: str


class ComponentSlotSummary(BaseModel):
    state: Literal["PENDING_REQUIRED_COMPONENT", "BOUND", "NOT_APPLICABLE", "INVALIDATED"]
    ref: RefModel | None = None
    reason: str | None = None


class ImportInterviewResponse(BaseModel):
    package_id: str
    revision: int
    lifecycle_state: str
    admission_mode: Literal["IMPORTED", "BRIEF_LED"]
    derivative_eligible: bool
    planning_lineage: dict
    transcript_alignment_ref: RefModel
    packed_phrase_transcript_ref: RefModel
    visual_structure_index_ref: RefModel
    word_count: int
    phrase_count: int
    shot_count: int
    keyframe_count: int
    idempotent_replay: bool


class InterviewStatusResponse(BaseModel):
    package_id: str
    revision: int
    workspace_id: str
    project_id: str
    admission_mode: Literal["IMPORTED", "BRIEF_LED"]
    source_kind: Literal["INTERVIEW_EXPRESSION", "NON_INTERVIEW"]
    lifecycle_state: str
    derivative_eligible: bool
    planning_lineage: dict
    components: dict[str, ComponentSlotSummary]
    media_assets: list[MediaAssetSummary]
