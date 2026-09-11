"""Canonical CAE visual tracking session state for M0090.

SAM3 is a downstream vision runtime.  This module owns the governed CAE
objects, immutable revisions, operator authorization boundary, provenance,
state transitions, receipts, and consumer geometry projections.  It does not
own semantic identity or narrative meaning.
"""

from __future__ import annotations

import json
import re
import sqlite3
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator

from ca_contracts import canonical_sha256, utc_now_rfc3339

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_BPS_MAX = 10_000


class TrackingDomainError(Exception):
    """Base exception for fail-closed tracking-domain operations."""


class TrackingAuthorizationError(TrackingDomainError):
    """Actor is not authorized by the injected CAE operator authority."""


class TrackingAuthorityError(TrackingDomainError):
    """Tracking state is not properly linked to an existing CAE context."""


class TrackingRevisionValidationError(TrackingDomainError):
    """Revision, prompt, geometry, or provenance data is malformed."""


class TrackingStaleRevisionError(TrackingDomainError):
    """The caller attempted a mutation from a stale base revision."""


class TrackingRevisionNotFoundError(TrackingDomainError):
    """Revision is not visible in the requested workspace/session."""


class TrackingIdempotencyConflictError(TrackingDomainError):
    """An idempotency key was replayed with a different request payload."""


class TrackingPromotionError(TrackingDomainError):
    """A track cannot be exposed to downstream consumers yet."""


class TrackingPromptKind(str):
    FACE = "FACE"
    BOX = "BOX"
    POINT = "POINT"
    MASK = "MASK"


class TrackingSessionStatus(str):
    DRAFT = "DRAFT"
    TRACKING = "TRACKING"
    IN_REVIEW = "IN_REVIEW"
    NEEDS_REVISION = "NEEDS_REVISION"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    BLOCKED = "BLOCKED"


class TrackingRevisionStatus(str):
    PROPOSED = "PROPOSED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    NEEDS_REVISION = "NEEDS_REVISION"


class TrackingFeedbackDecision(str):
    GOOD = "GOOD"
    NEEDS_EDIT = "NEEDS_EDIT"
    REJECT = "REJECT"


class TrackGapReason(str):
    MODEL_NO_OUTPUT = "MODEL_NO_OUTPUT"
    SOURCE_UNAVAILABLE = "SOURCE_UNAVAILABLE"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"


class BBoxGeometry(BaseModel):
    """Normalized integer basis-point bounding box for deterministic consumers."""

    x_bps: int
    y_bps: int
    width_bps: int
    height_bps: int

    @model_validator(mode="after")
    def validate_geometry(self) -> "BBoxGeometry":
        values = (self.x_bps, self.y_bps, self.width_bps, self.height_bps)
        if any(v < 0 or v > _BPS_MAX for v in values):
            raise ValueError("bbox geometry must use 0..10000 basis-point values")
        if self.width_bps <= 0 or self.height_bps <= 0:
            raise ValueError("bbox width and height must be positive")
        if self.x_bps + self.width_bps > _BPS_MAX:
            raise ValueError("bbox exceeds normalized frame width")
        if self.y_bps + self.height_bps > _BPS_MAX:
            raise ValueError("bbox exceeds normalized frame height")
        return self


class PointGeometry(BaseModel):
    x_bps: int
    y_bps: int

    @model_validator(mode="after")
    def validate_geometry(self) -> "PointGeometry":
        if not (0 <= self.x_bps <= _BPS_MAX and 0 <= self.y_bps <= _BPS_MAX):
            raise ValueError("point geometry must use 0..10000 basis-point values")
        return self


class TrackingTarget(BaseModel):
    """An operator-selected visual target, not a semantic identity authority."""

    target_id: str
    target_ref: str
    operator_id: str
    label: Optional[str] = None
    created_at: str = Field(default_factory=utc_now_rfc3339)

    @model_validator(mode="after")
    def require_fields(self) -> "TrackingTarget":
        if not self.target_id.strip() or not self.target_ref.strip() or not self.operator_id.strip():
            raise ValueError("target_id, target_ref, and operator_id are required")
        return self


class TrackingPrompt(BaseModel):
    """Operator seed prompt retained as immutable evidence in a revision."""

    prompt_id: str
    target_id: str
    kind: str
    frame_index: int
    source_frame_sha256: str
    face_ref: Optional[str] = None
    box: Optional[BBoxGeometry] = None
    point: Optional[PointGeometry] = None
    mask_ref: Optional[str] = None
    note: Optional[str] = None

    @model_validator(mode="after")
    def validate_prompt(self) -> "TrackingPrompt":
        if self.frame_index < 0:
            raise ValueError("prompt frame_index must be non-negative")
        if not _SHA256_RE.fullmatch(self.source_frame_sha256):
            raise ValueError("source_frame_sha256 must be a lowercase SHA-256 digest")
        if self.kind not in {
            TrackingPromptKind.FACE,
            TrackingPromptKind.BOX,
            TrackingPromptKind.POINT,
            TrackingPromptKind.MASK,
        }:
            raise ValueError(f"unsupported tracking prompt kind: {self.kind}")
        if self.kind == TrackingPromptKind.FACE:
            if not self.face_ref or (self.box is None and self.point is None):
                raise ValueError("FACE prompt requires face_ref plus box or point geometry")
        elif self.kind == TrackingPromptKind.BOX:
            if self.box is None:
                raise ValueError("BOX prompt requires box geometry")
        elif self.kind == TrackingPromptKind.POINT:
            if self.point is None:
                raise ValueError("POINT prompt requires point geometry")
        elif self.kind == TrackingPromptKind.MASK:
            if not self.mask_ref:
                raise ValueError("MASK prompt requires an immutable mask artifact reference")
        return self


class TrackFrame(BaseModel):
    """One governed tracked frame with source-lineage hash and confidence."""

    frame_index: int
    source_frame_sha256: str
    confidence_bps: int
    bbox: BBoxGeometry
    mask_artifact_ref: Optional[str] = None

    @model_validator(mode="after")
    def validate_frame(self) -> "TrackFrame":
        if self.frame_index < 0:
            raise ValueError("track frame_index must be non-negative")
        if not _SHA256_RE.fullmatch(self.source_frame_sha256):
            raise ValueError("source_frame_sha256 must be a lowercase SHA-256 digest")
        if not 0 <= self.confidence_bps <= _BPS_MAX:
            raise ValueError("confidence_bps must be between 0 and 10000")
        return self


class TrackGap(BaseModel):
    start_frame: int
    end_frame: int
    reason: str

    @model_validator(mode="after")
    def validate_gap(self) -> "TrackGap":
        if self.start_frame < 0 or self.end_frame < self.start_frame:
            raise ValueError("track gap frame range is invalid")
        if self.reason not in {
            TrackGapReason.MODEL_NO_OUTPUT,
            TrackGapReason.SOURCE_UNAVAILABLE,
            TrackGapReason.LOW_CONFIDENCE,
        }:
            raise ValueError(f"unsupported track gap reason: {self.reason}")
        return self


class TrackSegment(BaseModel):
    segment_id: str
    target_id: str
    start_frame: int
    end_frame: int
    frames: List[TrackFrame] = Field(default_factory=list)
    gaps: List[TrackGap] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_segment(self) -> "TrackSegment":
        if self.start_frame < 0 or self.end_frame < self.start_frame:
            raise ValueError("track segment frame range is invalid")
        last = None
        for frame in self.frames:
            if frame.frame_index < self.start_frame or frame.frame_index > self.end_frame:
                raise ValueError("track frame falls outside segment range")
            if last is not None and frame.frame_index <= last:
                raise ValueError("track frames must be strictly increasing")
            last = frame.frame_index
        for gap in self.gaps:
            if gap.start_frame < self.start_frame or gap.end_frame > self.end_frame:
                raise ValueError("track gap falls outside segment range")
        return self

    @property
    def source_frame_hashes(self) -> Dict[int, str]:
        return {frame.frame_index: frame.source_frame_sha256 for frame in self.frames}


class TrackRevision(BaseModel):
    """Immutable revision of one operator-controlled tracking proposal."""

    workspace_id: str
    session_id: str
    revision_id: str
    revision_seq: int
    base_revision_id: Optional[str] = None
    source_media_sha256: str
    target: TrackingTarget
    prompts: List[TrackingPrompt] = Field(default_factory=list)
    segments: List[TrackSegment] = Field(default_factory=list)
    status: str = TrackingRevisionStatus.PROPOSED
    author_id: str
    reason: Optional[str] = None
    created_at: str = Field(default_factory=utc_now_rfc3339)
    canonical_sha256: str = ""

    @model_validator(mode="after")
    def validate_revision(self) -> "TrackRevision":
        if self.revision_seq < 1:
            raise ValueError("revision_seq must start at 1")
        if not self.workspace_id.strip() or not self.session_id.strip() or not self.author_id.strip():
            raise ValueError("workspace_id, session_id, and author_id are required")
        if not _SHA256_RE.fullmatch(self.source_media_sha256):
            raise ValueError("source_media_sha256 must be a lowercase SHA-256 digest")
        if self.status not in {
            TrackingRevisionStatus.PROPOSED,
            TrackingRevisionStatus.ACCEPTED,
            TrackingRevisionStatus.REJECTED,
            TrackingRevisionStatus.NEEDS_REVISION,
        }:
            raise ValueError(f"unsupported revision status: {self.status}")
        if not self.segments and self.status == TrackingRevisionStatus.ACCEPTED:
            raise ValueError("accepted tracking revision must contain track geometry")
        if self.canonical_sha256 and not _SHA256_RE.fullmatch(self.canonical_sha256):
            raise ValueError("canonical_sha256 must be a lowercase SHA-256 digest")
        return self


class TrackingSession(BaseModel):
    """Canonical session pointer to source, selected target, and latest revision."""

    workspace_id: str
    session_id: str
    canonical_context_ref: str
    source_uri: str
    source_media_sha256: str
    width_px: int
    height_px: int
    frame_count: int
    frame_rate_milli_fps: int
    target: TrackingTarget
    status: str = TrackingSessionStatus.DRAFT
    created_at: str = Field(default_factory=utc_now_rfc3339)
    latest_revision_id: Optional[str] = None

    @model_validator(mode="after")
    def validate_session(self) -> "TrackingSession":
        if not self.workspace_id.strip() or not self.session_id.strip() or not self.canonical_context_ref.strip():
            raise ValueError("workspace_id, session_id, and canonical_context_ref are required")
        if not self.source_uri.strip():
            raise ValueError("source_uri is required")
        if not _SHA256_RE.fullmatch(self.source_media_sha256):
            raise ValueError("source_media_sha256 must be a lowercase SHA-256 digest")
        if self.width_px <= 0 or self.height_px <= 0 or self.frame_count <= 0 or self.frame_rate_milli_fps <= 0:
            raise ValueError("source frame dimensions/count/frame rate must be positive")
        if self.status not in {
            TrackingSessionStatus.DRAFT,
            TrackingSessionStatus.TRACKING,
            TrackingSessionStatus.IN_REVIEW,
            TrackingSessionStatus.NEEDS_REVISION,
            TrackingSessionStatus.ACCEPTED,
            TrackingSessionStatus.REJECTED,
            TrackingSessionStatus.BLOCKED,
        }:
            raise ValueError(f"unsupported session status: {self.status}")
        return self


class TrackingFeedback(BaseModel):
    feedback_id: str
    workspace_id: str
    session_id: str
    revision_id: str
    operator_id: str
    decision: str
    note: Optional[str] = None
    reason_category: Optional[str] = None
    created_at: str = Field(default_factory=utc_now_rfc3339)
    feedback_sha256: str = ""

    @model_validator(mode="after")
    def validate_feedback(self) -> "TrackingFeedback":
        if self.decision not in {
            TrackingFeedbackDecision.GOOD,
            TrackingFeedbackDecision.NEEDS_EDIT,
            TrackingFeedbackDecision.REJECT,
        }:
            raise ValueError(f"unsupported tracking feedback decision: {self.decision}")
        if not self.operator_id.strip():
            raise ValueError("operator_id is required")
        if self.feedback_sha256 and not _SHA256_RE.fullmatch(self.feedback_sha256):
            raise ValueError("feedback_sha256 must be a lowercase SHA-256 digest")
        return self


class TrackingTransitionReceipt(BaseModel):
    receipt_id: str
    workspace_id: str
    session_id: str
    actor_id: str
    operation: str
    precondition_revision_id: Optional[str] = None
    postcondition_revision_id: Optional[str] = None
    postcondition_status: str
    validator_result: str
    error_route: str
    recovery_path: str
    receipt_sha256: str
    created_at: str = Field(default_factory=utc_now_rfc3339)


class StoryboardBBoxFrame(BaseModel):
    frame_index: int
    x_bps: int
    y_bps: int
    width_bps: int
    height_bps: int


class StoryboardBBoxTrack(BaseModel):
    track_revision_id: str
    target_ref: str
    frames: List[StoryboardBBoxFrame]
    source_media_sha256: str


class OpenChatCutTrackingRegion(BaseModel):
    frame_index: int
    x_px: int
    y_px: int
    width_px: int
    height_px: int
    confidence_bps: int
    source_frame_sha256: str


class OpenChatCutTrackingTrack(BaseModel):
    track_revision_id: str
    target_ref: str
    video_width_px: int
    video_height_px: int
    regions: List[OpenChatCutTrackingRegion]
    source_media_sha256: str


def _payload(model: BaseModel) -> Dict[str, Any]:
    return model.model_dump(mode="json", exclude_none=True)


def _hash_without(model: BaseModel, field_name: str) -> str:
    data = _payload(model)
    data.pop(field_name, None)
    return canonical_sha256(data)


def _round_div_bps(value_bps: int, pixels: int) -> int:
    return (value_bps * pixels + 5_000) // _BPS_MAX


def project_storyboard_bbox(revision: TrackRevision, *, source_media_sha256: Optional[str] = None) -> StoryboardBBoxTrack:
    if revision.status != TrackingRevisionStatus.ACCEPTED:
        raise TrackingPromotionError("only an accepted tracking revision can be exposed to Storyboard/BBOX")
    if source_media_sha256 is not None and source_media_sha256 != revision.source_media_sha256:
        raise TrackingPromotionError("source media hash does not match the accepted tracking revision")
    frames = [
        StoryboardBBoxFrame(
            frame_index=frame.frame_index,
            x_bps=frame.bbox.x_bps,
            y_bps=frame.bbox.y_bps,
            width_bps=frame.bbox.width_bps,
            height_bps=frame.bbox.height_bps,
        )
        for segment in revision.segments
        for frame in segment.frames
    ]
    return StoryboardBBoxTrack(
        track_revision_id=revision.revision_id,
        target_ref=revision.target.target_ref,
        frames=frames,
        source_media_sha256=revision.source_media_sha256,
    )


def project_openchatcut_tracking(
    revision: TrackRevision,
    *,
    source_media_sha256: Optional[str] = None,
    video_width_px: int,
    video_height_px: int,
) -> OpenChatCutTrackingTrack:
    if revision.status != TrackingRevisionStatus.ACCEPTED:
        raise TrackingPromotionError("only an accepted tracking revision can be exposed to OpenChatCut")
    if source_media_sha256 is not None and source_media_sha256 != revision.source_media_sha256:
        raise TrackingPromotionError("source media hash does not match the accepted tracking revision")
    regions: List[OpenChatCutTrackingRegion] = []
    for segment in revision.segments:
        for frame in segment.frames:
            x = _round_div_bps(frame.bbox.x_bps, video_width_px)
            y = _round_div_bps(frame.bbox.y_bps, video_height_px)
            right = _round_div_bps(frame.bbox.x_bps + frame.bbox.width_bps, video_width_px)
            bottom = _round_div_bps(frame.bbox.y_bps + frame.bbox.height_bps, video_height_px)
            regions.append(
                OpenChatCutTrackingRegion(
                    frame_index=frame.frame_index,
                    x_px=x,
                    y_px=y,
                    width_px=max(1, right - x),
                    height_px=max(1, bottom - y),
                    confidence_bps=frame.confidence_bps,
                    source_frame_sha256=frame.source_frame_sha256,
                )
            )
    return OpenChatCutTrackingTrack(
        track_revision_id=revision.revision_id,
        target_ref=revision.target.target_ref,
        video_width_px=video_width_px,
        video_height_px=video_height_px,
        regions=regions,
        source_media_sha256=revision.source_media_sha256,
    )


OperatorAuthorizer = Callable[[str, str], bool]


class TrackingSessionStore:
    """SQLite CAS-backed projection store for M0090 tracking state."""

    def __init__(
        self,
        connection: Optional[sqlite3.Connection] = None,
        *,
        operator_authorizer: Optional[OperatorAuthorizer] = None,
    ) -> None:
        self.conn = connection or sqlite3.connect(":memory:", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.operator_authorizer = operator_authorizer
        self._init_schema()

    def _init_schema(self) -> None:
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tracking_session (
                    workspace_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    canonical_context_ref TEXT NOT NULL,
                    source_uri TEXT NOT NULL,
                    source_media_sha256 TEXT NOT NULL,
                    width_px INTEGER NOT NULL,
                    height_px INTEGER NOT NULL,
                    frame_count INTEGER NOT NULL,
                    frame_rate_milli_fps INTEGER NOT NULL,
                    target_json TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    latest_revision_id TEXT,
                    PRIMARY KEY (workspace_id, session_id)
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tracking_revision (
                    workspace_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    revision_id TEXT NOT NULL,
                    revision_seq INTEGER NOT NULL,
                    base_revision_id TEXT,
                    revision_json TEXT NOT NULL,
                    canonical_sha256 TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    idempotency_key TEXT,
                    request_sha256 TEXT,
                    PRIMARY KEY (workspace_id, revision_id),
                    UNIQUE (workspace_id, session_id, revision_seq)
                )
                """
            )
            self.conn.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS tracking_revision_idempotency "
                "ON tracking_revision(workspace_id, session_id, idempotency_key) "
                "WHERE idempotency_key IS NOT NULL"
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tracking_feedback (
                    workspace_id TEXT NOT NULL,
                    feedback_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    revision_id TEXT NOT NULL,
                    operator_id TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    note TEXT,
                    reason_category TEXT,
                    created_at TEXT NOT NULL,
                    feedback_sha256 TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, feedback_id)
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tracking_receipt (
                    workspace_id TEXT NOT NULL,
                    receipt_id TEXT NOT NULL,
                    receipt_json TEXT NOT NULL,
                    receipt_sha256 TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, receipt_id)
                )
                """
            )

    def _authorize(self, workspace_id: str, actor_id: str) -> None:
        if self.operator_authorizer is None or not self.operator_authorizer(workspace_id, actor_id):
            raise TrackingAuthorizationError(
                f"operator authorization denied for actor '{actor_id}' in workspace '{workspace_id}'"
            )

    def _session_row(self, workspace_id: str, session_id: str) -> sqlite3.Row:
        row = self.conn.execute(
            "SELECT * FROM tracking_session WHERE workspace_id = ? AND session_id = ?",
            (workspace_id, session_id),
        ).fetchone()
        if row is None:
            raise TrackingAuthorityError(
                f"TrackingSession '{session_id}' not found in workspace '{workspace_id}'"
            )
        return row

    def create_session(
        self,
        *,
        workspace_id: str,
        canonical_context_ref: str,
        source_uri: str,
        source_media_sha256: str,
        width_px: int,
        height_px: int,
        frame_count: int,
        frame_rate_milli_fps: int,
        target: TrackingTarget,
        actor_id: str,
        session_id: Optional[str] = None,
    ) -> TrackingSession:
        self._authorize(workspace_id, actor_id)
        if actor_id != target.operator_id:
            raise TrackingAuthorizationError("session actor must match target selection operator")
        sid = session_id or f"tracking_session_{uuid4().hex[:16]}"
        existing = self.conn.execute(
            "SELECT * FROM tracking_session WHERE workspace_id = ? AND session_id = ?",
            (workspace_id, sid),
        ).fetchone()
        if existing is not None:
            current = self.get_session(workspace_id, sid)
            assert current is not None
            if current.source_media_sha256 != source_media_sha256 or current.canonical_context_ref != canonical_context_ref:
                raise TrackingAuthorityError("TrackingSession ID is already bound to different source/context")
            return current
        session = TrackingSession(
            workspace_id=workspace_id,
            session_id=sid,
            canonical_context_ref=canonical_context_ref,
            source_uri=source_uri,
            source_media_sha256=source_media_sha256,
            width_px=width_px,
            height_px=height_px,
            frame_count=frame_count,
            frame_rate_milli_fps=frame_rate_milli_fps,
            target=target,
        )
        receipt = self._make_receipt(
            workspace_id=workspace_id,
            session_id=sid,
            actor_id=actor_id,
            operation="CREATE_SESSION",
            precondition_revision_id=None,
            postcondition_revision_id=None,
            postcondition_status=TrackingSessionStatus.DRAFT,
        )
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO tracking_session
                (workspace_id, session_id, canonical_context_ref, source_uri, source_media_sha256,
                 width_px, height_px, frame_count, frame_rate_milli_fps, target_json, status,
                 created_at, latest_revision_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session.workspace_id,
                    session.session_id,
                    session.canonical_context_ref,
                    session.source_uri,
                    session.source_media_sha256,
                    session.width_px,
                    session.height_px,
                    session.frame_count,
                    session.frame_rate_milli_fps,
                    json.dumps(_payload(session.target), sort_keys=True, separators=(",", ":")),
                    session.status,
                    session.created_at,
                    None,
                ),
            )
            self._insert_receipt(receipt)
        return session

    def get_session(self, workspace_id: str, session_id: str) -> Optional[TrackingSession]:
        row = self.conn.execute(
            "SELECT * FROM tracking_session WHERE workspace_id = ? AND session_id = ?",
            (workspace_id, session_id),
        ).fetchone()
        if row is None:
            return None
        return TrackingSession(
            workspace_id=row["workspace_id"],
            session_id=row["session_id"],
            canonical_context_ref=row["canonical_context_ref"],
            source_uri=row["source_uri"],
            source_media_sha256=row["source_media_sha256"],
            width_px=row["width_px"],
            height_px=row["height_px"],
            frame_count=row["frame_count"],
            frame_rate_milli_fps=row["frame_rate_milli_fps"],
            target=TrackingTarget(**json.loads(row["target_json"])),
            status=row["status"],
            created_at=row["created_at"],
            latest_revision_id=row["latest_revision_id"],
        )

    def save_revision(
        self,
        *,
        workspace_id: str,
        session_id: str,
        target: TrackingTarget,
        prompts: Sequence[TrackingPrompt],
        segments: Sequence[TrackSegment],
        author_id: str,
        base_revision_id: Optional[str],
        reason: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        revision_id: Optional[str] = None,
        created_at: Optional[str] = None,
    ) -> TrackRevision:
        self._authorize(workspace_id, author_id)
        session = self._session_row(workspace_id, session_id)
        stored_target = TrackingTarget(**json.loads(session["target_json"]))
        if target.target_id != stored_target.target_id or target.target_ref != stored_target.target_ref:
            raise TrackingAuthorityError("revision target does not match operator-selected session target")
        if author_id != target.operator_id:
            raise TrackingAuthorizationError("revision author must match target-selection operator")
        current_revision_id = session["latest_revision_id"]

        request_payload = {
            "base_revision_id": base_revision_id,
            "target": _payload(target),
            "prompts": [_payload(item) for item in prompts],
            "segments": [_payload(item) for item in segments],
            "author_id": author_id,
            "reason": reason,
        }
        request_sha256 = canonical_sha256(request_payload)
        if idempotency_key:
            existing = self.conn.execute(
                "SELECT revision_json, request_sha256 FROM tracking_revision WHERE "
                "workspace_id = ? AND session_id = ? AND idempotency_key = ?",
                (workspace_id, session_id, idempotency_key),
            ).fetchone()
            if existing is not None:
                if existing["request_sha256"] != request_sha256:
                    raise TrackingIdempotencyConflictError("idempotency key replay payload differs")
                return TrackRevision(**json.loads(existing["revision_json"]))

        if base_revision_id != current_revision_id:
            if current_revision_id is None and base_revision_id is None:
                pass
            else:
                raise TrackingStaleRevisionError(
                    f"stale tracking base: expected {current_revision_id!r}, got {base_revision_id!r}"
                )

        next_seq_row = self.conn.execute(
            "SELECT COALESCE(MAX(revision_seq), 0) + 1 AS next_seq FROM tracking_revision "
            "WHERE workspace_id = ? AND session_id = ?",
            (workspace_id, session_id),
        ).fetchone()
        revision = TrackRevision(
            workspace_id=workspace_id,
            session_id=session_id,
            revision_id=revision_id or f"track_revision_{uuid4().hex[:16]}",
            revision_seq=int(next_seq_row["next_seq"]),
            base_revision_id=base_revision_id,
            source_media_sha256=session["source_media_sha256"],
            target=target,
            prompts=list(prompts),
            segments=list(segments),
            status=TrackingRevisionStatus.PROPOSED,
            author_id=author_id,
            reason=reason,
            created_at=created_at or utc_now_rfc3339(),
        )
        digest = _hash_without(revision, "canonical_sha256")
        revision = revision.model_copy(update={"canonical_sha256": digest})
        receipt = self._make_receipt(
            workspace_id=workspace_id,
            session_id=session_id,
            actor_id=author_id,
            operation="SAVE_REVISION",
            precondition_revision_id=base_revision_id,
            postcondition_revision_id=revision.revision_id,
            postcondition_status=TrackingSessionStatus.IN_REVIEW,
        )
        try:
            with self.conn:
                result = self.conn.execute(
                    """
                    UPDATE tracking_session
                    SET status = ?, latest_revision_id = ?
                    WHERE workspace_id = ? AND session_id = ? AND latest_revision_id IS ?
                    """,
                    (
                        TrackingSessionStatus.IN_REVIEW,
                        revision.revision_id,
                        workspace_id,
                        session_id,
                        current_revision_id,
                    ),
                )
                if result.rowcount != 1:
                    raise TrackingStaleRevisionError("tracking session changed during revision commit")
                self.conn.execute(
                    """
                    INSERT INTO tracking_revision
                    (workspace_id, session_id, revision_id, revision_seq, base_revision_id,
                     revision_json, canonical_sha256, created_at, idempotency_key, request_sha256)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        revision.workspace_id,
                        revision.session_id,
                        revision.revision_id,
                        revision.revision_seq,
                        revision.base_revision_id,
                        json.dumps(_payload(revision), sort_keys=True, separators=(",", ":")),
                        revision.canonical_sha256,
                        revision.created_at,
                        idempotency_key,
                        request_sha256,
                    ),
                )
                self._insert_receipt(receipt)
        except sqlite3.IntegrityError as exc:
            raise TrackingStaleRevisionError("tracking revision commit collided with another revision") from exc
        return revision

    def get_revision(self, workspace_id: str, session_id: str, revision_id: str) -> TrackRevision:
        row = self.conn.execute(
            "SELECT revision_json FROM tracking_revision WHERE workspace_id = ? AND session_id = ? AND revision_id = ?",
            (workspace_id, session_id, revision_id),
        ).fetchone()
        if row is None:
            raise TrackingRevisionNotFoundError(
                f"tracking revision '{revision_id}' not found in workspace/session"
            )
        return TrackRevision(**json.loads(row["revision_json"]))

    def list_revisions(self, workspace_id: str, session_id: str) -> List[TrackRevision]:
        rows = self.conn.execute(
            "SELECT revision_json FROM tracking_revision WHERE workspace_id = ? AND session_id = ? "
            "ORDER BY revision_seq",
            (workspace_id, session_id),
        ).fetchall()
        return [TrackRevision(**json.loads(row["revision_json"])) for row in rows]

    def record_feedback(
        self,
        *,
        workspace_id: str,
        session_id: str,
        revision_id: str,
        operator_id: str,
        decision: str,
        note: Optional[str] = None,
        reason_category: Optional[str] = None,
    ) -> TrackingFeedback:
        self._authorize(workspace_id, operator_id)
        session = self._session_row(workspace_id, session_id)
        if session["latest_revision_id"] != revision_id:
            raise TrackingStaleRevisionError("feedback can only operate on the current tracking revision")
        revision = self.get_revision(workspace_id, session_id, revision_id)
        if operator_id != revision.target.operator_id:
            raise TrackingAuthorizationError("feedback operator must match target-selection operator")
        feedback = TrackingFeedback(
            feedback_id=f"track_feedback_{uuid4().hex[:16]}",
            workspace_id=workspace_id,
            session_id=session_id,
            revision_id=revision_id,
            operator_id=operator_id,
            decision=decision,
            note=note,
            reason_category=reason_category,
        )
        feedback = feedback.model_copy(update={"feedback_sha256": _hash_without(feedback, "feedback_sha256")})
        if decision == TrackingFeedbackDecision.GOOD:
            next_session_status = TrackingSessionStatus.ACCEPTED
            promoted_revision_id = f"track_revision_{uuid4().hex[:16]}"
            next_seq = self.conn.execute(
                "SELECT COALESCE(MAX(revision_seq), 0) + 1 AS next_seq FROM tracking_revision "
                "WHERE workspace_id = ? AND session_id = ?",
                (workspace_id, session_id),
            ).fetchone()["next_seq"]
            promoted = TrackRevision(
                workspace_id=revision.workspace_id,
                session_id=revision.session_id,
                revision_id=promoted_revision_id,
                revision_seq=int(next_seq),
                base_revision_id=revision.revision_id,
                source_media_sha256=revision.source_media_sha256,
                target=revision.target,
                prompts=revision.prompts,
                segments=revision.segments,
                status=TrackingRevisionStatus.ACCEPTED,
                author_id=operator_id,
                reason="PROMOTED_BY_OPERATOR_GOOD",
                created_at=utc_now_rfc3339(),
            )
            promoted = promoted.model_copy(update={"canonical_sha256": _hash_without(promoted, "canonical_sha256")})
        elif decision == TrackingFeedbackDecision.NEEDS_EDIT:
            next_session_status = TrackingSessionStatus.NEEDS_REVISION
            promoted = None
        elif decision == TrackingFeedbackDecision.REJECT:
            next_session_status = TrackingSessionStatus.REJECTED
            promoted = None
        else:
            raise TrackingRevisionValidationError(f"unsupported feedback decision: {decision}")
        receipt = self._make_receipt(
            workspace_id=workspace_id,
            session_id=session_id,
            actor_id=operator_id,
            operation=f"FEEDBACK_{decision}",
            precondition_revision_id=revision_id,
            postcondition_revision_id=promoted.revision_id if promoted is not None else revision_id,
            postcondition_status=next_session_status,
        )
        with self.conn:
            self.conn.execute(
                "INSERT INTO tracking_feedback "
                "(workspace_id, feedback_id, session_id, revision_id, operator_id, decision, note, "
                "reason_category, created_at, feedback_sha256) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    feedback.workspace_id,
                    feedback.feedback_id,
                    feedback.session_id,
                    feedback.revision_id,
                    feedback.operator_id,
                    feedback.decision,
                    feedback.note,
                    feedback.reason_category,
                    feedback.created_at,
                    feedback.feedback_sha256,
                ),
            )
            if promoted is not None:
                self.conn.execute(
                    "INSERT INTO tracking_revision "
                    "(workspace_id, session_id, revision_id, revision_seq, base_revision_id, "
                    "revision_json, canonical_sha256, created_at, idempotency_key, request_sha256) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL)",
                    (
                        promoted.workspace_id,
                        promoted.session_id,
                        promoted.revision_id,
                        promoted.revision_seq,
                        promoted.base_revision_id,
                        json.dumps(_payload(promoted), sort_keys=True, separators=(",", ":")),
                        promoted.canonical_sha256,
                        promoted.created_at,
                    ),
                )
                result = self.conn.execute(
                    "UPDATE tracking_session SET status = ?, latest_revision_id = ? "
                    "WHERE workspace_id = ? AND session_id = ? AND latest_revision_id = ?",
                    (next_session_status, promoted.revision_id, workspace_id, session_id, revision_id),
                )
            else:
                result = self.conn.execute(
                    "UPDATE tracking_session SET status = ? WHERE workspace_id = ? AND session_id = ? "
                    "AND latest_revision_id = ?",
                    (next_session_status, workspace_id, session_id, revision_id),
                )
            if result.rowcount != 1:
                raise TrackingStaleRevisionError("tracking session changed while applying feedback")
            self._insert_receipt(receipt)
        return feedback

    def list_receipts(self, workspace_id: str, session_id: str) -> List[TrackingTransitionReceipt]:
        rows = self.conn.execute(
            "SELECT receipt_json FROM tracking_receipt WHERE workspace_id = ? "
            "ORDER BY created_at, receipt_id",
            (workspace_id,),
        ).fetchall()
        return [TrackingTransitionReceipt(**json.loads(row["receipt_json"])) for row in rows if json.loads(row["receipt_json"])["session_id"] == session_id]

    def feedback(self, workspace_id: str, session_id: str, revision_id: str) -> List[TrackingFeedback]:
        rows = self.conn.execute(
            "SELECT * FROM tracking_feedback WHERE workspace_id = ? AND session_id = ? AND revision_id = ? "
            "ORDER BY created_at, feedback_id",
            (workspace_id, session_id, revision_id),
        ).fetchall()
        return [
            TrackingFeedback(
                feedback_id=row["feedback_id"],
                workspace_id=row["workspace_id"],
                session_id=row["session_id"],
                revision_id=row["revision_id"],
                operator_id=row["operator_id"],
                decision=row["decision"],
                note=row["note"],
                reason_category=row["reason_category"],
                created_at=row["created_at"],
                feedback_sha256=row["feedback_sha256"],
            )
            for row in rows
        ]

    def _make_receipt(
        self,
        *,
        workspace_id: str,
        session_id: str,
        actor_id: str,
        operation: str,
        precondition_revision_id: Optional[str],
        postcondition_revision_id: Optional[str],
        postcondition_status: str,
    ) -> TrackingTransitionReceipt:
        receipt = TrackingTransitionReceipt(
            receipt_id=f"track_receipt_{uuid4().hex[:16]}",
            workspace_id=workspace_id,
            session_id=session_id,
            actor_id=actor_id,
            operation=operation,
            precondition_revision_id=precondition_revision_id,
            postcondition_revision_id=postcondition_revision_id,
            postcondition_status=postcondition_status,
            validator_result="PASS",
            error_route="FAIL_CLOSED",
            recovery_path="RETRY_FROM_LATEST_REVISION_OR_OPERATOR_REPAIR",
            receipt_sha256="",
        )
        return receipt.model_copy(update={"receipt_sha256": _hash_without(receipt, "receipt_sha256")})

    def _insert_receipt(self, receipt: TrackingTransitionReceipt) -> None:
        self.conn.execute(
            "INSERT INTO tracking_receipt "
            "(workspace_id, receipt_id, receipt_json, receipt_sha256, created_at) VALUES (?, ?, ?, ?, ?)",
            (
                receipt.workspace_id,
                receipt.receipt_id,
                json.dumps(_payload(receipt), sort_keys=True, separators=(",", ":")),
                receipt.receipt_sha256,
                receipt.created_at,
            ),
        )
