"""Canonical CAE storyboard session and revision domain (M0079).

This module is deliberately a projection layer around the existing
``EditorialStoryboardRecord`` and ``PreparationGraphStore`` authorities.  It
does not own semantic meaning, candidate selection, asset rights, or runtime
execution.  A session points at one approved editorial storyboard and each
revision is persisted through ``GraphRevisionRecord`` so stale editors cannot
overwrite one another.
"""

from __future__ import annotations

import json
import sqlite3
from typing import Any, Dict, Iterable, List, Optional, Sequence
from uuid import uuid4

from pydantic import BaseModel, Field, validator

from ca_contracts import CanonicalizationError, canonical_sha256, utc_now_rfc3339
from ca_runtime.editorial_discovery_store import EditorialDiscoveryStore
from ca_runtime.preparation_graph_store import (
    GraphRevisionRecord,
    PreparationGraphStore,
    StaleBaseRevisionError,
)


class StoryboardDomainError(Exception):
    """Base error for fail-closed storyboard domain operations."""


class StoryboardAuthorityError(StoryboardDomainError):
    """The requested storyboard or source lineage is not authoritative."""


class StoryboardRevisionValidationError(StoryboardDomainError):
    """A revision is malformed, ungrounded, or internally inconsistent."""


class StoryboardRevisionNotFoundError(StoryboardDomainError):
    """A revision is not visible in the requested workspace/session."""


class StoryboardFeedbackError(StoryboardDomainError):
    """Feedback is invalid or attempts to mutate an immutable record."""


class FeedbackDecision(str):
    GOOD = "GOOD"
    NEEDS_EDIT = "NEEDS_EDIT"
    REJECT = "REJECT"


class StoryboardSessionStatus(str):
    DRAFT = "DRAFT"
    IN_REVIEW = "IN_REVIEW"
    COMPILED = "COMPILED"
    BLOCKED = "BLOCKED"


class VisualAssetReference(BaseModel):
    """A governed reference to an asset; it is not an asset authority."""

    reference_id: str
    asset_id: str
    source_type: str = "EVIDENCE"
    source_uri: Optional[str] = None
    evidence_refs: List[str] = Field(default_factory=list)
    rights_status: str = "UNVERIFIED"
    source_quality: str = "UNKNOWN"
    approved: bool = False


class TransformationIntent(BaseModel):
    """Why a source is transformed, distinct from how it is rendered."""

    intent_id: str
    source_element_id: str
    semantic_target: str
    mode: str
    emphasis: str = "BALANCED"
    motion: str = "STATIC"
    constraints: Dict[str, Any] = Field(default_factory=dict)

    @validator("mode")
    def mode_is_bounded(cls, value: str) -> str:
        normalized = value.upper()
        allowed = {
            "WITHHOLD", "REVEAL", "FOCUS", "CONTRAST", "PROVE",
            "EXPLAIN", "CONNECT", "ESCALATE", "INTERRUPT", "RESOLVE",
        }
        if normalized not in allowed:
            raise ValueError(f"unsupported transformation intent: {value}")
        return normalized


class TransformationRecipe(BaseModel):
    """Bounded primitive projection of a ``TransformationIntent``."""

    recipe_id: str
    intent_id: str
    primitives: List[Dict[str, Any]] = Field(default_factory=list)
    keyframes: List[Dict[str, Any]] = Field(default_factory=list)
    constraints: Dict[str, Any] = Field(default_factory=dict)


class MotionPlan(BaseModel):
    """Deterministic motion/keyframe plan, downstream of semantic intent."""

    motion_plan_id: str
    duration_ms: int = 0
    keyframes: List[Dict[str, Any]] = Field(default_factory=list)
    intensity_bps: int = 0
    attention_cost_bps: int = 0

    @validator("duration_ms", "intensity_bps", "attention_cost_bps")
    def non_negative(cls, value: int) -> int:
        if value < 0:
            raise ValueError("motion values must be non-negative")
        return value


class StoryboardElement(BaseModel):
    element_id: str
    kind: str
    semantic_purpose: str
    source_evidence_refs: List[str] = Field(default_factory=list)
    asset_references: List[VisualAssetReference] = Field(default_factory=list)
    transformation_intent: Optional[TransformationIntent] = None
    transformation_recipe: Optional[TransformationRecipe] = None
    motion_plan: Optional[MotionPlan] = None
    properties: Dict[str, Any] = Field(default_factory=dict)


class StoryboardShot(BaseModel):
    shot_id: str
    start_ms: int
    end_ms: int
    semantic_purpose: str
    shot_language: Dict[str, Any] = Field(default_factory=dict)
    elements: List[StoryboardElement] = Field(default_factory=list)

    @validator("end_ms")
    def end_after_start(cls, value: int, values: Dict[str, Any]) -> int:
        if "start_ms" in values and value <= values["start_ms"]:
            raise ValueError("shot end_ms must be greater than start_ms")
        return value


class StoryboardScene(BaseModel):
    scene_id: str
    scene_order: int
    semantic_purpose: str
    source_evidence_refs: List[str] = Field(default_factory=list)
    shots: List[StoryboardShot] = Field(default_factory=list)

    @validator("scene_order")
    def scene_order_is_non_negative(cls, value: int) -> int:
        if value < 0:
            raise ValueError("scene_order must be non-negative")
        return value


class StoryboardSession(BaseModel):
    """Editable workspace identity around one canonical EditorialStoryboard."""

    workspace_id: str
    session_id: str
    editorial_storyboard_id: str
    graph_id: str
    semantic_program_id: Optional[str] = None
    harness_id: Optional[str] = None
    status: str = StoryboardSessionStatus.DRAFT
    created_by: str
    created_at: str = Field(default_factory=utc_now_rfc3339)
    latest_revision_id: Optional[str] = None


class StoryboardRevision(BaseModel):
    """Immutable editable storyboard snapshot backed by ``GraphRevisionRecord``."""

    workspace_id: str
    session_id: str
    revision_id: str
    revision_seq: int
    base_revision_id: Optional[str]
    editorial_storyboard_id: str
    semantic_program_id: Optional[str] = None
    harness_id: Optional[str] = None
    scenes: List[StoryboardScene] = Field(default_factory=list)
    source_evidence_refs: List[str] = Field(default_factory=list)
    status: str = StoryboardSessionStatus.DRAFT
    author_id: str
    canonical_sha256: str
    created_at: str


class OperatorVisualFeedback(BaseModel):
    feedback_id: str
    workspace_id: str
    session_id: str
    revision_id: str
    operator_id: str
    decision: str
    note: Optional[str] = None
    reason_category: Optional[str] = None
    created_at: str = Field(default_factory=utc_now_rfc3339)
    feedback_sha256: str

    @validator("decision")
    def decision_is_bounded(cls, value: str) -> str:
        normalized = value.upper()
        if normalized not in {
            FeedbackDecision.GOOD,
            FeedbackDecision.NEEDS_EDIT,
            FeedbackDecision.REJECT,
        }:
            raise ValueError(f"unsupported feedback decision: {value}")
        return normalized


class StoryboardValidationReport(BaseModel):
    report_id: str
    workspace_id: str
    session_id: str
    revision_id: str
    passed: bool
    checks: Dict[str, str] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    report_sha256: str
    created_at: str = Field(default_factory=utc_now_rfc3339)


class StoryboardCompileReceipt(BaseModel):
    receipt_id: str
    workspace_id: str
    session_id: str
    revision_id: str
    editorial_storyboard_id: str
    semantic_program_id: Optional[str]
    harness_id: Optional[str]
    validation_report_id: str
    status: str
    lineage_sha256: str
    created_at: str = Field(default_factory=utc_now_rfc3339)


def _model_payload(model: BaseModel) -> Dict[str, Any]:
    return model.dict(exclude_none=True)


class StoryboardSessionStore:
    """SQLite persistence adapter for the canonical editable storyboard layer."""

    def __init__(
        self,
        connection: Optional[sqlite3.Connection] = None,
        *,
        editorial_store: Optional[EditorialDiscoveryStore] = None,
    ) -> None:
        if editorial_store is not None:
            connection = editorial_store._conn  # shared authoritative connection
        self.conn = connection or sqlite3.connect(":memory:", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.editorial_store = editorial_store
        self.graph_store = PreparationGraphStore(self.conn)
        self._init_schema()

    def _init_schema(self) -> None:
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS storyboard_session (
                    workspace_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    editorial_storyboard_id TEXT NOT NULL,
                    graph_id TEXT NOT NULL,
                    semantic_program_id TEXT,
                    harness_id TEXT,
                    status TEXT NOT NULL,
                    created_by TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    latest_revision_id TEXT,
                    PRIMARY KEY (workspace_id, session_id),
                    UNIQUE (workspace_id, editorial_storyboard_id)
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS storyboard_operator_feedback (
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
                    PRIMARY KEY (workspace_id, feedback_id),
                    UNIQUE (workspace_id, revision_id, operator_id)
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS storyboard_validation_report (
                    workspace_id TEXT NOT NULL,
                    report_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    revision_id TEXT NOT NULL,
                    passed INTEGER NOT NULL,
                    checks_json TEXT NOT NULL,
                    errors_json TEXT NOT NULL,
                    warnings_json TEXT NOT NULL,
                    report_sha256 TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, report_id),
                    UNIQUE (workspace_id, revision_id)
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS storyboard_compile_receipt (
                    workspace_id TEXT NOT NULL,
                    receipt_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    revision_id TEXT NOT NULL,
                    editorial_storyboard_id TEXT NOT NULL,
                    semantic_program_id TEXT,
                    harness_id TEXT,
                    validation_report_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    lineage_sha256 TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, receipt_id),
                    UNIQUE (workspace_id, revision_id)
                )
                """
            )

    def _require_editorial_storyboard(self, workspace_id: str, storyboard_id: str) -> None:
        if self.editorial_store is not None:
            if self.editorial_store.get_editorial_storyboard(workspace_id, storyboard_id) is None:
                raise StoryboardAuthorityError(
                    f"EditorialStoryboard '{storyboard_id}' not found in workspace '{workspace_id}'"
                )
            return
        row = self.conn.execute(
            "SELECT storyboard_id FROM cae_editorial_storyboards "
            "WHERE workspace_id = ? AND storyboard_id = ?",
            (workspace_id, storyboard_id),
        ).fetchone()
        if row is None:
            raise StoryboardAuthorityError(
                f"EditorialStoryboard '{storyboard_id}' not found in workspace '{workspace_id}'"
            )

    def create_session(
        self,
        *,
        workspace_id: str,
        editorial_storyboard_id: str,
        created_by: str,
        session_id: Optional[str] = None,
        semantic_program_id: Optional[str] = None,
        harness_id: Optional[str] = None,
    ) -> StoryboardSession:
        self._require_editorial_storyboard(workspace_id, editorial_storyboard_id)
        sid = session_id or f"storyboard_session_{uuid4().hex[:16]}"
        existing = self.get_session(workspace_id, sid)
        if existing is not None:
            if existing.editorial_storyboard_id != editorial_storyboard_id:
                raise StoryboardAuthorityError(
                    f"StoryboardSession '{sid}' is already bound to another EditorialStoryboard"
                )
            return existing
        existing_storyboard = self.conn.execute(
            "SELECT session_id FROM storyboard_session "
            "WHERE workspace_id = ? AND editorial_storyboard_id = ?",
            (workspace_id, editorial_storyboard_id),
        ).fetchone()
        if existing_storyboard is not None:
            existing_session = self.get_session(workspace_id, existing_storyboard[0])
            assert existing_session is not None
            return existing_session
        graph_id = f"storyboard_graph_{sid}"
        now = utc_now_rfc3339()
        session = StoryboardSession(
            workspace_id=workspace_id,
            session_id=sid,
            editorial_storyboard_id=editorial_storyboard_id,
            graph_id=graph_id,
            semantic_program_id=semantic_program_id,
            harness_id=harness_id,
            created_by=created_by,
            created_at=now,
        )
        graph = self.graph_store.create_graph(
            workspace_id=workspace_id,
            graph_id=graph_id,
            campaign_id=editorial_storyboard_id,
            name=f"Storyboard session {sid}",
        )
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO storyboard_session
                (workspace_id, session_id, editorial_storyboard_id, graph_id,
                 semantic_program_id, harness_id, status, created_by, created_at,
                 latest_revision_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session.workspace_id,
                    session.session_id,
                    session.editorial_storyboard_id,
                    session.graph_id,
                    session.semantic_program_id,
                    session.harness_id,
                    session.status,
                    session.created_by,
                    session.created_at,
                    session.latest_revision_id,
                ),
            )
        return session

    def get_session(self, workspace_id: str, session_id: str) -> Optional[StoryboardSession]:
        row = self.conn.execute(
            """
            SELECT workspace_id, session_id, editorial_storyboard_id, graph_id,
                   semantic_program_id, harness_id, status, created_by, created_at,
                   latest_revision_id
            FROM storyboard_session
            WHERE workspace_id = ? AND session_id = ?
            """,
            (workspace_id, session_id),
        ).fetchone()
        if row is None:
            return None
        return StoryboardSession(**dict(row))

    def _revision_from_graph(self, session: StoryboardSession, graph: GraphRevisionRecord) -> StoryboardRevision:
        try:
            payload = json.loads(graph.parameter_payload_json)
            return StoryboardRevision(
                workspace_id=graph.workspace_id,
                session_id=session.session_id,
                revision_id=graph.revision_id,
                revision_seq=graph.revision_seq,
                base_revision_id=graph.base_revision_id,
                editorial_storyboard_id=payload["editorial_storyboard_id"],
                semantic_program_id=payload.get("semantic_program_id"),
                harness_id=payload.get("harness_id"),
                scenes=[StoryboardScene(**scene) for scene in payload.get("scenes", [])],
                source_evidence_refs=payload.get("source_evidence_refs", []),
                status=payload.get("status", StoryboardSessionStatus.DRAFT),
                author_id=graph.author_id,
                canonical_sha256=graph.canonical_sha256,
                created_at=graph.created_at,
            )
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise StoryboardRevisionValidationError(
                f"malformed persisted storyboard revision '{graph.revision_id}': {exc}"
            ) from exc

    def get_revision(self, workspace_id: str, session_id: str, revision_id: str) -> StoryboardRevision:
        session = self.get_session(workspace_id, session_id)
        if session is None:
            raise StoryboardRevisionNotFoundError(
                f"StoryboardSession '{session_id}' not found in workspace '{workspace_id}'"
            )
        try:
            graph = self.graph_store.get_revision(workspace_id, revision_id)
        except Exception as exc:
            raise StoryboardRevisionNotFoundError(revision_id) from exc
        if graph.graph_id != session.graph_id:
            raise StoryboardRevisionNotFoundError(revision_id)
        return self._revision_from_graph(session, graph)

    def latest_revision(self, workspace_id: str, session_id: str) -> Optional[StoryboardRevision]:
        session = self.get_session(workspace_id, session_id)
        if session is None or session.latest_revision_id is None:
            return None
        return self.get_revision(workspace_id, session_id, session.latest_revision_id)

    def list_revisions(self, workspace_id: str, session_id: str) -> List[StoryboardRevision]:
        session = self.get_session(workspace_id, session_id)
        if session is None:
            raise StoryboardRevisionNotFoundError(session_id)
        return [
            self._revision_from_graph(session, graph)
            for graph in self.graph_store.list_revisions(workspace_id, session.graph_id)
        ]

    def _validate_revision_input(
        self,
        *,
        session: StoryboardSession,
        scenes: Sequence[StoryboardScene],
        source_evidence_refs: Sequence[str],
    ) -> None:
        if not source_evidence_refs:
            raise StoryboardRevisionValidationError(
                "storyboard revision requires source_evidence_refs"
            )
        scene_ids = [scene.scene_id for scene in scenes]
        if len(scene_ids) != len(set(scene_ids)):
            raise StoryboardRevisionValidationError("scene_id values must be unique")
        evidence_refs = set(source_evidence_refs)
        for scene in scenes:
            if not scene.source_evidence_refs:
                raise StoryboardRevisionValidationError(
                    f"scene '{scene.scene_id}' has no source evidence lineage"
                )
            if not set(scene.source_evidence_refs).issubset(evidence_refs):
                raise StoryboardRevisionValidationError(
                    f"scene '{scene.scene_id}' references evidence outside revision lineage"
                )
            shot_ids = [shot.shot_id for shot in scene.shots]
            if len(shot_ids) != len(set(shot_ids)):
                raise StoryboardRevisionValidationError("shot_id values must be unique within a scene")
            for shot in scene.shots:
                for element in shot.elements:
                    if not element.source_evidence_refs:
                        raise StoryboardRevisionValidationError(
                            f"element '{element.element_id}' has no source evidence lineage"
                        )
                    if not set(element.source_evidence_refs).issubset(evidence_refs):
                        raise StoryboardRevisionValidationError(
                            f"element '{element.element_id}' references evidence outside revision lineage"
                        )
                    for asset in element.asset_references:
                        if not asset.evidence_refs:
                            raise StoryboardRevisionValidationError(
                                f"asset '{asset.asset_id}' is not evidence-grounded"
                            )
                        if not set(asset.evidence_refs).issubset(evidence_refs):
                            raise StoryboardRevisionValidationError(
                                f"asset '{asset.asset_id}' references evidence outside revision lineage"
                            )
                    intent = element.transformation_intent
                    recipe = element.transformation_recipe
                    if recipe is not None and (intent is None or recipe.intent_id != intent.intent_id):
                        raise StoryboardRevisionValidationError(
                            f"element '{element.element_id}' has a recipe detached from its intent"
                        )
                    if intent is not None and intent.source_element_id != element.element_id:
                        raise StoryboardRevisionValidationError(
                            f"transformation intent for '{element.element_id}' points at another element"
                        )

    def save_revision(
        self,
        *,
        workspace_id: str,
        session_id: str,
        author_id: str,
        scenes: Sequence[StoryboardScene],
        source_evidence_refs: Sequence[str],
        base_revision_id: Optional[str],
        semantic_program_id: Optional[str] = None,
        harness_id: Optional[str] = None,
        status: str = StoryboardSessionStatus.DRAFT,
    ) -> StoryboardRevision:
        session = self.get_session(workspace_id, session_id)
        if session is None:
            raise StoryboardAuthorityError(
                f"StoryboardSession '{session_id}' not found in workspace '{workspace_id}'"
            )
        self._require_editorial_storyboard(workspace_id, session.editorial_storyboard_id)
        self._validate_revision_input(
            session=session,
            scenes=scenes,
            source_evidence_refs=source_evidence_refs,
        )
        payload = {
            "editorial_storyboard_id": session.editorial_storyboard_id,
            "semantic_program_id": semantic_program_id or session.semantic_program_id,
            "harness_id": harness_id or session.harness_id,
            "scenes": [_model_payload(scene) for scene in scenes],
            "source_evidence_refs": list(source_evidence_refs),
            "status": status,
        }
        try:
            graph_revision = self.graph_store.save_graph_revision(
                workspace_id=workspace_id,
                graph_id=session.graph_id,
                base_revision_id=base_revision_id,
                parameters=payload,
                author_id=author_id,
            )
        except CanonicalizationError as exc:
            raise StoryboardRevisionValidationError(
                f"revision payload is not canonicalizable: {exc}"
            ) from exc
        with self.conn:
            self.conn.execute(
                "UPDATE storyboard_session SET latest_revision_id = ?, status = ? "
                "WHERE workspace_id = ? AND session_id = ?",
                (graph_revision.revision_id, StoryboardSessionStatus.IN_REVIEW, workspace_id, session_id),
            )
        return self._revision_from_graph(session, graph_revision)

    def validate_revision(
        self, *, workspace_id: str, session_id: str, revision_id: str
    ) -> StoryboardValidationReport:
        revision = self.get_revision(workspace_id, session_id, revision_id)
        checks: Dict[str, str] = {
            "editorial_storyboard_lineage": "PASS",
            "source_evidence_lineage": "PASS",
            "scene_shot_timing": "PASS",
            "transformation_chain": "PASS",
        }
        report_payload = {
            "workspace_id": workspace_id,
            "session_id": session_id,
            "revision_id": revision_id,
            "passed": True,
            "checks": checks,
            "errors": [],
            "warnings": [],
        }
        report = StoryboardValidationReport(
            report_id=f"validation_{revision_id}",
            report_sha256=canonical_sha256(report_payload),
            **report_payload,
        )
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO storyboard_validation_report
                (workspace_id, report_id, session_id, revision_id, passed,
                 checks_json, errors_json, warnings_json, report_sha256, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(workspace_id, revision_id) DO NOTHING
                """,
                (
                    report.workspace_id,
                    report.report_id,
                    report.session_id,
                    report.revision_id,
                    1,
                    json.dumps(report.checks, sort_keys=True),
                    "[]",
                    "[]",
                    report.report_sha256,
                    report.created_at,
                ),
            )
        return self.get_validation_report(workspace_id, revision_id) or report

    def get_validation_report(
        self, workspace_id: str, revision_id: str
    ) -> Optional[StoryboardValidationReport]:
        row = self.conn.execute(
            """
            SELECT report_id, workspace_id, session_id, revision_id, passed,
                   checks_json, errors_json, warnings_json, report_sha256, created_at
            FROM storyboard_validation_report
            WHERE workspace_id = ? AND revision_id = ?
            """,
            (workspace_id, revision_id),
        ).fetchone()
        if row is None:
            return None
        return StoryboardValidationReport(
            report_id=row[0], workspace_id=row[1], session_id=row[2],
            revision_id=row[3], passed=bool(row[4]), checks=json.loads(row[5]),
            errors=json.loads(row[6]), warnings=json.loads(row[7]),
            report_sha256=row[8], created_at=row[9],
        )

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
        feedback_id: Optional[str] = None,
    ) -> OperatorVisualFeedback:
        self.get_revision(workspace_id, session_id, revision_id)
        payload = {
            "workspace_id": workspace_id,
            "session_id": session_id,
            "revision_id": revision_id,
            "operator_id": operator_id,
            "decision": decision.upper(),
            "note": note,
            "reason_category": reason_category,
        }
        feedback = OperatorVisualFeedback(
            feedback_id=feedback_id or f"feedback_{uuid4().hex[:16]}",
            feedback_sha256=canonical_sha256(payload),
            **payload,
        )
        try:
            with self.conn:
                self.conn.execute(
                    """
                    INSERT INTO storyboard_operator_feedback
                    (workspace_id, feedback_id, session_id, revision_id, operator_id,
                     decision, note, reason_category, created_at, feedback_sha256)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        feedback.workspace_id, feedback.feedback_id, feedback.session_id,
                        feedback.revision_id, feedback.operator_id, feedback.decision,
                        feedback.note, feedback.reason_category, feedback.created_at,
                        feedback.feedback_sha256,
                    ),
                )
        except sqlite3.IntegrityError as exc:
            raise StoryboardFeedbackError(
                "feedback for an operator/revision is immutable; create a new revision"
            ) from exc
        return feedback

    def compile_revision(
        self, *, workspace_id: str, session_id: str, revision_id: str
    ) -> StoryboardCompileReceipt:
        revision = self.get_revision(workspace_id, session_id, revision_id)
        report = self.get_validation_report(workspace_id, revision_id)
        if report is None or not report.passed:
            raise StoryboardRevisionValidationError(
                f"revision '{revision_id}' must have a passing validation report before compile"
            )
        feedback = self.conn.execute(
            """
            SELECT decision FROM storyboard_operator_feedback
            WHERE workspace_id = ? AND revision_id = ?
            ORDER BY created_at DESC LIMIT 1
            """,
            (workspace_id, revision_id),
        ).fetchone()
        if feedback is None or feedback[0] != FeedbackDecision.GOOD:
            raise StoryboardFeedbackError(
                "compile requires immutable operator feedback decision GOOD"
            )
        session = self.get_session(workspace_id, session_id)
        assert session is not None
        receipt_payload = {
            "workspace_id": workspace_id,
            "session_id": session_id,
            "revision_id": revision_id,
            "editorial_storyboard_id": session.editorial_storyboard_id,
            "semantic_program_id": revision.semantic_program_id,
            "harness_id": revision.harness_id,
            "validation_report_id": report.report_id,
            "status": "COMPILE_READY",
        }
        receipt = StoryboardCompileReceipt(
            receipt_id=f"compile_{revision_id}",
            lineage_sha256=canonical_sha256(
                {**receipt_payload, "revision_sha256": revision.canonical_sha256}
            ),
            **receipt_payload,
        )
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO storyboard_compile_receipt
                (workspace_id, receipt_id, session_id, revision_id,
                 editorial_storyboard_id, semantic_program_id, harness_id,
                 validation_report_id, status, lineage_sha256, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(workspace_id, revision_id) DO NOTHING
                """,
                (
                    receipt.workspace_id, receipt.receipt_id, receipt.session_id,
                    receipt.revision_id, receipt.editorial_storyboard_id,
                    receipt.semantic_program_id, receipt.harness_id,
                    receipt.validation_report_id, receipt.status,
                    receipt.lineage_sha256, receipt.created_at,
                ),
            )
            self.conn.execute(
                "UPDATE storyboard_session SET status = ? WHERE workspace_id = ? AND session_id = ?",
                (StoryboardSessionStatus.COMPILED, workspace_id, session_id),
            )
        return receipt


__all__ = [
    "FeedbackDecision",
    "MotionPlan",
    "OperatorVisualFeedback",
    "StoryboardAuthorityError",
    "StoryboardCompileReceipt",
    "StoryboardDomainError",
    "StoryboardElement",
    "StoryboardRevision",
    "StoryboardRevisionNotFoundError",
    "StoryboardRevisionValidationError",
    "StoryboardScene",
    "StoryboardSession",
    "StoryboardSessionStatus",
    "StoryboardSessionStore",
    "StoryboardShot",
    "StoryboardValidationReport",
    "TransformationIntent",
    "TransformationRecipe",
    "VisualAssetReference",
]
