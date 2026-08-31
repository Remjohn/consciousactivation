"""
editorial_discovery_store.py
----------------------------
Authoritative SQLite / PostgreSQL Relational Storage Adapter for Evidence
Segmentation, Semantic Attribution, Content Candidates, Candidate Clusters,
Editorial Storyboards, and Synthetic-Proof Audit Receipts (CAE M35).
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from ca_contracts import canonical_sha256


class EvidenceSegmentRecord(BaseModel):
    """Authoritative representation of an EvidenceSegment entity (CAE-M05)."""
    workspace_id: str
    segment_id: str
    session_id: str
    speaker: str
    start_time_ms: int
    end_time_ms: int
    verbatim_text: str
    boundary_type: str
    text_sha256: str
    context_dependency: Dict[str, Any] = Field(default_factory=dict)
    is_authenticated: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SemanticAnnotationRecord(BaseModel):
    """Authoritative representation of a SemanticAnnotation entity (CAE-M06)."""
    workspace_id: str
    annotation_id: str
    segment_id: str
    semantic_role: str
    epistemic_status: str
    confidence_score_bps: int
    tension_ref: Optional[str] = None
    invariant_ref: Optional[str] = None
    emotional_register: str = "NEUTRAL"
    story_arc_geometry: str = "NONE"
    is_candidate_eligible: bool = True
    is_publishable: bool = False
    observable_evidence: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ContentCandidateRecord(BaseModel):
    """Authoritative representation of a ContentCandidate entity (CAE-M07)."""
    workspace_id: str
    candidate_id: str
    candidate_type: str
    title: str
    hook_statement: str
    narrative_completeness: str
    story_arc: Optional[str] = None
    tension_ref: Optional[str] = None
    invariant_ref: Optional[str] = None
    archetypal_container: Optional[str] = None
    evidence_links: List[Dict[str, Any]] = Field(default_factory=list)
    cmf_score_bps: Dict[str, int] = Field(default_factory=dict)
    production_status: str = "DRAFT_CANDIDATE"
    is_synthetic: bool = False
    standalone_context_notes: Optional[str] = None
    version: int = 1
    predecessor_candidate_id: Optional[str] = None
    lock_status: str = "UNLOCKED"
    operator_decision_ref: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CandidateClusterRecord(BaseModel):
    """Authoritative representation of a CandidateCluster entity (CAE-M08)."""
    workspace_id: str
    cluster_id: str
    theme: str
    candidate_ids: List[str] = Field(default_factory=list)
    redundancy_score_bps: int
    coverage_domain: str
    dominant_candidate_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EditorialStoryboardRecord(BaseModel):
    """Authoritative representation of an approved EditorialStoryboard entity (CAE-M09)."""
    workspace_id: str
    storyboard_id: str
    candidate_id: str
    title: str
    hook_statement: str
    priority_rank: int
    evidence_links: List[Dict[str, Any]] = Field(default_factory=list)
    narrative_structure: List[Dict[str, Any]] = Field(default_factory=list)
    planned_inserts: List[Dict[str, Any]] = Field(default_factory=list)
    approved_by: str
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SemanticProgramRecord(BaseModel):
    """Authoritative representation of a compiled SemanticProgram entity (CAE-M11)."""
    workspace_id: str
    program_id: str
    storyboard_id: str
    candidate_id: str
    title: str
    semantic_intent: str
    story_arc: str
    scenes: List[Dict[str, Any]] = Field(default_factory=list)
    total_duration: float
    visual_audio_specs: Dict[str, Any] = Field(default_factory=dict)
    wrong_reading_locks: List[str] = Field(default_factory=list)
    evidence_lineage_hashes: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CompositionHandoffRecord(BaseModel):
    """Authoritative representation of a CompositionHandoffReceipt entity (CAE-M11/M16)."""
    workspace_id: str
    receipt_id: str
    program_id: str
    candidate_id: str
    storyboard_id: str
    compiler_version: str = "1.0.0"
    evidence_sha256_list: List[str] = Field(default_factory=list)
    asset_id_list: List[str] = Field(default_factory=list)
    wrong_reading_locks: List[str] = Field(default_factory=list)
    composition_ir_ref: Optional[Dict[str, Any]] = None
    receipt_sha256: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EditorialDecisionReceiptRecord(BaseModel):
    """Authoritative audit receipt for operator selection, rejection, framing modification, or synthetic block."""
    workspace_id: str
    receipt_id: str
    operator_id: str
    candidate_id: str
    action_type: str  # SELECT, REJECT, MODIFY, LOCK, COMPARE, REGENERATE, SYNTHETIC_BLOCKED
    rationale: str
    taste_delta: Optional[str] = None
    is_synthetic_blocked: bool = False
    metadata_payload: Dict[str, Any] = Field(default_factory=dict)
    receipt_sha256: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EditorialDiscoveryStore:
    """Relational dual-backend storage adapter for Editorial Discovery and Synthetic-Proof blocks."""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self) -> None:
        cursor = self._conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cae_evidence_segments (
                segment_id TEXT PRIMARY KEY,
                workspace_id TEXT NOT NULL,
                session_id TEXT NOT NULL,
                speaker TEXT NOT NULL,
                start_time_ms INTEGER NOT NULL,
                end_time_ms INTEGER NOT NULL,
                verbatim_text TEXT NOT NULL,
                boundary_type TEXT NOT NULL,
                text_sha256 TEXT NOT NULL,
                context_dependency JSON NOT NULL,
                is_authenticated INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL
            );
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_cae_segments_ws_session
            ON cae_evidence_segments (workspace_id, session_id);
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cae_semantic_annotations (
                annotation_id TEXT PRIMARY KEY,
                workspace_id TEXT NOT NULL,
                segment_id TEXT NOT NULL,
                semantic_role TEXT NOT NULL,
                epistemic_status TEXT NOT NULL,
                confidence_score_bps INTEGER NOT NULL,
                tension_ref TEXT,
                invariant_ref TEXT,
                emotional_register TEXT NOT NULL,
                story_arc_geometry TEXT NOT NULL,
                is_candidate_eligible INTEGER NOT NULL DEFAULT 1,
                is_publishable INTEGER NOT NULL DEFAULT 0,
                observable_evidence JSON NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (segment_id) REFERENCES cae_evidence_segments(segment_id)
            );
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_cae_annotations_ws_segment
            ON cae_semantic_annotations (workspace_id, segment_id);
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cae_content_candidates (
                candidate_id TEXT PRIMARY KEY,
                workspace_id TEXT NOT NULL,
                candidate_type TEXT NOT NULL,
                title TEXT NOT NULL,
                hook_statement TEXT NOT NULL,
                narrative_completeness TEXT NOT NULL,
                story_arc TEXT,
                tension_ref TEXT,
                invariant_ref TEXT,
                archetypal_container TEXT,
                evidence_links JSON NOT NULL,
                cmf_score_bps JSON NOT NULL,
                production_status TEXT NOT NULL,
                is_synthetic INTEGER NOT NULL DEFAULT 0,
                standalone_context_notes TEXT,
                version INTEGER NOT NULL DEFAULT 1,
                predecessor_candidate_id TEXT,
                lock_status TEXT NOT NULL DEFAULT 'UNLOCKED',
                operator_decision_ref TEXT,
                created_at TEXT NOT NULL
            );
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_cae_candidates_ws
            ON cae_content_candidates (workspace_id, production_status);
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cae_candidate_clusters (
                cluster_id TEXT PRIMARY KEY,
                workspace_id TEXT NOT NULL,
                theme TEXT NOT NULL,
                candidate_ids JSON NOT NULL,
                redundancy_score_bps INTEGER NOT NULL,
                coverage_domain TEXT NOT NULL,
                dominant_candidate_id TEXT,
                created_at TEXT NOT NULL
            );
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_cae_clusters_ws
            ON cae_candidate_clusters (workspace_id);
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cae_editorial_storyboards (
                storyboard_id TEXT PRIMARY KEY,
                workspace_id TEXT NOT NULL,
                candidate_id TEXT NOT NULL,
                title TEXT NOT NULL,
                hook_statement TEXT NOT NULL,
                priority_rank INTEGER NOT NULL,
                evidence_links JSON NOT NULL,
                narrative_structure JSON NOT NULL DEFAULT '[]',
                planned_inserts JSON NOT NULL DEFAULT '[]',
                approved_by TEXT NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (candidate_id) REFERENCES cae_content_candidates(candidate_id)
            );
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_cae_storyboards_ws
            ON cae_editorial_storyboards (workspace_id, candidate_id);
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cae_semantic_programs (
                program_id TEXT PRIMARY KEY,
                workspace_id TEXT NOT NULL,
                storyboard_id TEXT NOT NULL,
                candidate_id TEXT NOT NULL,
                title TEXT NOT NULL,
                semantic_intent TEXT NOT NULL,
                story_arc TEXT NOT NULL,
                scenes JSON NOT NULL,
                total_duration REAL NOT NULL,
                visual_audio_specs JSON NOT NULL,
                wrong_reading_locks JSON NOT NULL,
                evidence_lineage_hashes JSON NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (storyboard_id) REFERENCES cae_editorial_storyboards(storyboard_id)
            );
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_cae_semantic_programs_ws
            ON cae_semantic_programs (workspace_id, candidate_id);
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cae_composition_handoff_receipts (
                receipt_id TEXT PRIMARY KEY,
                workspace_id TEXT NOT NULL,
                program_id TEXT NOT NULL,
                candidate_id TEXT NOT NULL,
                storyboard_id TEXT NOT NULL,
                compiler_version TEXT NOT NULL,
                evidence_sha256_list JSON NOT NULL,
                asset_id_list JSON NOT NULL,
                wrong_reading_locks JSON NOT NULL,
                composition_ir_ref JSON,
                receipt_sha256 TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (program_id) REFERENCES cae_semantic_programs(program_id)
            );
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_cae_composition_handoffs_ws
            ON cae_composition_handoff_receipts (workspace_id, program_id);
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cae_editorial_receipts (
                receipt_id TEXT PRIMARY KEY,
                workspace_id TEXT NOT NULL,
                operator_id TEXT NOT NULL,
                candidate_id TEXT NOT NULL,
                action_type TEXT NOT NULL,
                rationale TEXT NOT NULL,
                taste_delta TEXT,
                is_synthetic_blocked INTEGER NOT NULL DEFAULT 0,
                metadata_payload JSON NOT NULL,
                receipt_sha256 TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_cae_editorial_receipts_ws
            ON cae_editorial_receipts (workspace_id, candidate_id);
        """)
        self._conn.commit()

    # --- Evidence Segment Operations ---

    def insert_evidence_segment(self, segment: EvidenceSegmentRecord) -> None:
        cursor = self._conn.cursor()
        cursor.execute("""
            INSERT INTO cae_evidence_segments (
                segment_id, workspace_id, session_id, speaker, start_time_ms, end_time_ms,
                verbatim_text, boundary_type, text_sha256, context_dependency, is_authenticated, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            segment.segment_id,
            segment.workspace_id,
            segment.session_id,
            segment.speaker,
            segment.start_time_ms,
            segment.end_time_ms,
            segment.verbatim_text,
            segment.boundary_type,
            segment.text_sha256,
            json.dumps(segment.context_dependency, default=str),
            1 if segment.is_authenticated else 0,
            segment.created_at.isoformat(),
        ))
        self._conn.commit()

    def get_evidence_segment(self, workspace_id: str, segment_id: str) -> Optional[EvidenceSegmentRecord]:
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT * FROM cae_evidence_segments WHERE workspace_id = ? AND segment_id = ?
        """, (workspace_id, segment_id))
        row = cursor.fetchone()
        if not row:
            return None
        return EvidenceSegmentRecord(
            workspace_id=row["workspace_id"],
            segment_id=row["segment_id"],
            session_id=row["session_id"],
            speaker=row["speaker"],
            start_time_ms=row["start_time_ms"],
            end_time_ms=row["end_time_ms"],
            verbatim_text=row["verbatim_text"],
            boundary_type=row["boundary_type"],
            text_sha256=row["text_sha256"],
            context_dependency=json.loads(row["context_dependency"]),
            is_authenticated=bool(row["is_authenticated"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def list_evidence_segments(self, workspace_id: str, session_id: Optional[str] = None) -> List[EvidenceSegmentRecord]:
        cursor = self._conn.cursor()
        if session_id:
            cursor.execute("""
                SELECT * FROM cae_evidence_segments WHERE workspace_id = ? AND session_id = ? ORDER BY start_time_ms ASC
            """, (workspace_id, session_id))
        else:
            cursor.execute("""
                SELECT * FROM cae_evidence_segments WHERE workspace_id = ? ORDER BY start_time_ms ASC
            """, (workspace_id,))
        rows = cursor.fetchall()
        return [
            EvidenceSegmentRecord(
                workspace_id=row["workspace_id"],
                segment_id=row["segment_id"],
                session_id=row["session_id"],
                speaker=row["speaker"],
                start_time_ms=row["start_time_ms"],
                end_time_ms=row["end_time_ms"],
                verbatim_text=row["verbatim_text"],
                boundary_type=row["boundary_type"],
                text_sha256=row["text_sha256"],
                context_dependency=json.loads(row["context_dependency"]),
                is_authenticated=bool(row["is_authenticated"]),
                created_at=datetime.fromisoformat(row["created_at"]),
            )
            for row in rows
        ]

    # --- Semantic Annotation Operations ---

    def insert_semantic_annotation(self, annotation: SemanticAnnotationRecord) -> None:
        cursor = self._conn.cursor()
        cursor.execute("""
            INSERT INTO cae_semantic_annotations (
                annotation_id, workspace_id, segment_id, semantic_role, epistemic_status,
                confidence_score_bps, tension_ref, invariant_ref, emotional_register,
                story_arc_geometry, is_candidate_eligible, is_publishable, observable_evidence, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            annotation.annotation_id,
            annotation.workspace_id,
            annotation.segment_id,
            annotation.semantic_role,
            annotation.epistemic_status,
            annotation.confidence_score_bps,
            annotation.tension_ref,
            annotation.invariant_ref,
            annotation.emotional_register,
            annotation.story_arc_geometry,
            1 if annotation.is_candidate_eligible else 0,
            1 if annotation.is_publishable else 0,
            json.dumps(annotation.observable_evidence, default=str),
            annotation.created_at.isoformat(),
        ))
        self._conn.commit()

    def get_semantic_annotation(self, workspace_id: str, annotation_id: str) -> Optional[SemanticAnnotationRecord]:
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT * FROM cae_semantic_annotations WHERE workspace_id = ? AND annotation_id = ?
        """, (workspace_id, annotation_id))
        row = cursor.fetchone()
        if not row:
            return None
        return SemanticAnnotationRecord(
            workspace_id=row["workspace_id"],
            annotation_id=row["annotation_id"],
            segment_id=row["segment_id"],
            semantic_role=row["semantic_role"],
            epistemic_status=row["epistemic_status"],
            confidence_score_bps=row["confidence_score_bps"],
            tension_ref=row["tension_ref"],
            invariant_ref=row["invariant_ref"],
            emotional_register=row["emotional_register"],
            story_arc_geometry=row["story_arc_geometry"],
            is_candidate_eligible=bool(row["is_candidate_eligible"]),
            is_publishable=bool(row["is_publishable"]),
            observable_evidence=json.loads(row["observable_evidence"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def list_semantic_annotations(self, workspace_id: str, segment_id: Optional[str] = None) -> List[SemanticAnnotationRecord]:
        cursor = self._conn.cursor()
        if segment_id:
            cursor.execute("""
                SELECT * FROM cae_semantic_annotations WHERE workspace_id = ? AND segment_id = ? ORDER BY created_at ASC
            """, (workspace_id, segment_id))
        else:
            cursor.execute("""
                SELECT * FROM cae_semantic_annotations WHERE workspace_id = ? ORDER BY created_at ASC
            """, (workspace_id,))
        rows = cursor.fetchall()
        return [
            SemanticAnnotationRecord(
                workspace_id=row["workspace_id"],
                annotation_id=row["annotation_id"],
                segment_id=row["segment_id"],
                semantic_role=row["semantic_role"],
                epistemic_status=row["epistemic_status"],
                confidence_score_bps=row["confidence_score_bps"],
                tension_ref=row["tension_ref"],
                invariant_ref=row["invariant_ref"],
                emotional_register=row["emotional_register"],
                story_arc_geometry=row["story_arc_geometry"],
                is_candidate_eligible=bool(row["is_candidate_eligible"]),
                is_publishable=bool(row["is_publishable"]),
                observable_evidence=json.loads(row["observable_evidence"]),
                created_at=datetime.fromisoformat(row["created_at"]),
            )
            for row in rows
        ]

    # --- Content Candidate Operations ---

    def insert_content_candidate(self, candidate: ContentCandidateRecord) -> None:
        cursor = self._conn.cursor()
        cursor.execute("""
            INSERT INTO cae_content_candidates (
                candidate_id, workspace_id, candidate_type, title, hook_statement,
                narrative_completeness, story_arc, tension_ref, invariant_ref,
                archetypal_container, evidence_links, cmf_score_bps, production_status,
                is_synthetic, standalone_context_notes, version, predecessor_candidate_id,
                lock_status, operator_decision_ref, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            candidate.candidate_id,
            candidate.workspace_id,
            candidate.candidate_type,
            candidate.title,
            candidate.hook_statement,
            candidate.narrative_completeness,
            candidate.story_arc,
            candidate.tension_ref,
            candidate.invariant_ref,
            candidate.archetypal_container,
            json.dumps(candidate.evidence_links, default=str),
            json.dumps(candidate.cmf_score_bps, default=str),
            candidate.production_status,
            1 if candidate.is_synthetic else 0,
            candidate.standalone_context_notes,
            candidate.version,
            candidate.predecessor_candidate_id,
            candidate.lock_status,
            candidate.operator_decision_ref,
            candidate.created_at.isoformat(),
        ))
        self._conn.commit()

    def get_content_candidate(self, workspace_id: str, candidate_id: str) -> Optional[ContentCandidateRecord]:
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT * FROM cae_content_candidates WHERE workspace_id = ? AND candidate_id = ?
        """, (workspace_id, candidate_id))
        row = cursor.fetchone()
        if not row:
            return None
        return ContentCandidateRecord(
            workspace_id=row["workspace_id"],
            candidate_id=row["candidate_id"],
            candidate_type=row["candidate_type"],
            title=row["title"],
            hook_statement=row["hook_statement"],
            narrative_completeness=row["narrative_completeness"],
            story_arc=row["story_arc"],
            tension_ref=row["tension_ref"],
            invariant_ref=row["invariant_ref"],
            archetypal_container=row["archetypal_container"],
            evidence_links=json.loads(row["evidence_links"]),
            cmf_score_bps=json.loads(row["cmf_score_bps"]),
            production_status=row["production_status"],
            is_synthetic=bool(row["is_synthetic"]),
            standalone_context_notes=row["standalone_context_notes"],
            version=row["version"] if "version" in row.keys() else 1,
            predecessor_candidate_id=row["predecessor_candidate_id"] if "predecessor_candidate_id" in row.keys() else None,
            lock_status=row["lock_status"] if "lock_status" in row.keys() else "UNLOCKED",
            operator_decision_ref=row["operator_decision_ref"] if "operator_decision_ref" in row.keys() else None,
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def list_content_candidates(
        self,
        workspace_id: str,
        production_status: Optional[str] = None,
        is_synthetic: Optional[bool] = None,
    ) -> List[ContentCandidateRecord]:
        cursor = self._conn.cursor()
        query = "SELECT * FROM cae_content_candidates WHERE workspace_id = ?"
        params: List[Any] = [workspace_id]
        if production_status is not None:
            query += " AND production_status = ?"
            params.append(production_status)
        if is_synthetic is not None:
            query += " AND is_synthetic = ?"
            params.append(1 if is_synthetic else 0)
        query += " ORDER BY created_at ASC"

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        return [
            ContentCandidateRecord(
                workspace_id=row["workspace_id"],
                candidate_id=row["candidate_id"],
                candidate_type=row["candidate_type"],
                title=row["title"],
                hook_statement=row["hook_statement"],
                narrative_completeness=row["narrative_completeness"],
                story_arc=row["story_arc"],
                tension_ref=row["tension_ref"],
                invariant_ref=row["invariant_ref"],
                archetypal_container=row["archetypal_container"],
                evidence_links=json.loads(row["evidence_links"]),
                cmf_score_bps=json.loads(row["cmf_score_bps"]),
                production_status=row["production_status"],
                is_synthetic=bool(row["is_synthetic"]),
                standalone_context_notes=row["standalone_context_notes"],
                version=row["version"] if "version" in row.keys() else 1,
                predecessor_candidate_id=row["predecessor_candidate_id"] if "predecessor_candidate_id" in row.keys() else None,
                lock_status=row["lock_status"] if "lock_status" in row.keys() else "UNLOCKED",
                operator_decision_ref=row["operator_decision_ref"] if "operator_decision_ref" in row.keys() else None,
                created_at=datetime.fromisoformat(row["created_at"]),
            )
            for row in rows
        ]

    def update_candidate_status(
        self,
        workspace_id: str,
        candidate_id: str,
        production_status: str,
        operator_decision_ref: Optional[str] = None,
    ) -> None:
        """Authoritatively updates candidate production status and links decision receipt."""
        cursor = self._conn.cursor()
        if operator_decision_ref:
            cursor.execute("""
                UPDATE cae_content_candidates
                SET production_status = ?, operator_decision_ref = ?
                WHERE workspace_id = ? AND candidate_id = ?
            """, (production_status, operator_decision_ref, workspace_id, candidate_id))
        else:
            cursor.execute("""
                UPDATE cae_content_candidates
                SET production_status = ?
                WHERE workspace_id = ? AND candidate_id = ?
            """, (production_status, workspace_id, candidate_id))
        self._conn.commit()

    def lock_candidate(
        self,
        workspace_id: str,
        candidate_id: str,
        operator_decision_ref: Optional[str] = None,
    ) -> None:
        """Authoritatively marks a candidate as LOCKED against automated modification."""
        cursor = self._conn.cursor()
        cursor.execute("""
            UPDATE cae_content_candidates
            SET lock_status = 'LOCKED', operator_decision_ref = coalesce(?, operator_decision_ref)
            WHERE workspace_id = ? AND candidate_id = ?
        """, (operator_decision_ref, workspace_id, candidate_id))
        self._conn.commit()

    def list_candidate_lineage(
        self,
        workspace_id: str,
        candidate_id: str,
    ) -> List[ContentCandidateRecord]:
        """Traverses candidate lineage through predecessor links back to root candidate."""
        lineage: List[ContentCandidateRecord] = []
        current_id: Optional[str] = candidate_id

        while current_id:
            cand = self.get_content_candidate(workspace_id, current_id)
            if not cand:
                break
            lineage.append(cand)
            current_id = cand.predecessor_candidate_id

        return list(reversed(lineage))


    # --- Candidate Cluster Operations ---

    def insert_candidate_cluster(self, cluster: CandidateClusterRecord) -> None:
        cursor = self._conn.cursor()
        cursor.execute("""
            INSERT INTO cae_candidate_clusters (
                cluster_id, workspace_id, theme, candidate_ids, redundancy_score_bps,
                coverage_domain, dominant_candidate_id, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cluster.cluster_id,
            cluster.workspace_id,
            cluster.theme,
            json.dumps(cluster.candidate_ids, default=str),
            cluster.redundancy_score_bps,
            cluster.coverage_domain,
            cluster.dominant_candidate_id,
            cluster.created_at.isoformat(),
        ))
        self._conn.commit()

    def get_candidate_cluster(self, workspace_id: str, cluster_id: str) -> Optional[CandidateClusterRecord]:
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT * FROM cae_candidate_clusters WHERE workspace_id = ? AND cluster_id = ?
        """, (workspace_id, cluster_id))
        row = cursor.fetchone()
        if not row:
            return None
        return CandidateClusterRecord(
            workspace_id=row["workspace_id"],
            cluster_id=row["cluster_id"],
            theme=row["theme"],
            candidate_ids=json.loads(row["candidate_ids"]),
            redundancy_score_bps=row["redundancy_score_bps"],
            coverage_domain=row["coverage_domain"],
            dominant_candidate_id=row["dominant_candidate_id"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def list_candidate_clusters(self, workspace_id: str) -> List[CandidateClusterRecord]:
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT * FROM cae_candidate_clusters WHERE workspace_id = ? ORDER BY created_at ASC
        """, (workspace_id,))
        rows = cursor.fetchall()
        return [
            CandidateClusterRecord(
                workspace_id=row["workspace_id"],
                cluster_id=row["cluster_id"],
                theme=row["theme"],
                candidate_ids=json.loads(row["candidate_ids"]),
                redundancy_score_bps=row["redundancy_score_bps"],
                coverage_domain=row["coverage_domain"],
                dominant_candidate_id=row["dominant_candidate_id"],
                created_at=datetime.fromisoformat(row["created_at"]),
            )
            for row in rows
        ]

    # --- Editorial Storyboard Operations ---

    def insert_editorial_storyboard(self, storyboard: EditorialStoryboardRecord) -> None:
        cursor = self._conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO cae_editorial_storyboards (
                storyboard_id, workspace_id, candidate_id, title, hook_statement,
                priority_rank, evidence_links, narrative_structure, planned_inserts,
                approved_by, notes, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            storyboard.storyboard_id,
            storyboard.workspace_id,
            storyboard.candidate_id,
            storyboard.title,
            storyboard.hook_statement,
            storyboard.priority_rank,
            json.dumps(storyboard.evidence_links, default=str),
            json.dumps(storyboard.narrative_structure, default=str),
            json.dumps(storyboard.planned_inserts, default=str),
            storyboard.approved_by,
            storyboard.notes,
            storyboard.created_at.isoformat(),
        ))
        self._conn.commit()

    def get_editorial_storyboard(self, workspace_id: str, storyboard_id: str) -> Optional[EditorialStoryboardRecord]:
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT * FROM cae_editorial_storyboards WHERE workspace_id = ? AND storyboard_id = ?
        """, (workspace_id, storyboard_id))
        row = cursor.fetchone()
        if not row:
            return None
        return EditorialStoryboardRecord(
            workspace_id=row["workspace_id"],
            storyboard_id=row["storyboard_id"],
            candidate_id=row["candidate_id"],
            title=row["title"],
            hook_statement=row["hook_statement"],
            priority_rank=row["priority_rank"],
            evidence_links=json.loads(row["evidence_links"]),
            narrative_structure=json.loads(row["narrative_structure"]) if "narrative_structure" in row.keys() else [],
            planned_inserts=json.loads(row["planned_inserts"]) if "planned_inserts" in row.keys() else [],
            approved_by=row["approved_by"],
            notes=row["notes"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def list_editorial_storyboards(self, workspace_id: str, candidate_id: Optional[str] = None) -> List[EditorialStoryboardRecord]:
        cursor = self._conn.cursor()
        if candidate_id:
            cursor.execute("""
                SELECT * FROM cae_editorial_storyboards WHERE workspace_id = ? AND candidate_id = ? ORDER BY created_at ASC
            """, (workspace_id, candidate_id))
        else:
            cursor.execute("""
                SELECT * FROM cae_editorial_storyboards WHERE workspace_id = ? ORDER BY created_at ASC
            """, (workspace_id,))
        rows = cursor.fetchall()
        return [
            EditorialStoryboardRecord(
                workspace_id=row["workspace_id"],
                storyboard_id=row["storyboard_id"],
                candidate_id=row["candidate_id"],
                title=row["title"],
                hook_statement=row["hook_statement"],
                priority_rank=row["priority_rank"],
                evidence_links=json.loads(row["evidence_links"]),
                narrative_structure=json.loads(row["narrative_structure"]) if "narrative_structure" in row.keys() else [],
                planned_inserts=json.loads(row["planned_inserts"]) if "planned_inserts" in row.keys() else [],
                approved_by=row["approved_by"],
                notes=row["notes"],
                created_at=datetime.fromisoformat(row["created_at"]),
            )
            for row in rows
        ]

    # --- Semantic Program Operations ---

    def insert_semantic_program(self, program: SemanticProgramRecord) -> None:
        cursor = self._conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO cae_semantic_programs (
                program_id, workspace_id, storyboard_id, candidate_id, title,
                semantic_intent, story_arc, scenes, total_duration, visual_audio_specs,
                wrong_reading_locks, evidence_lineage_hashes, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            program.program_id,
            program.workspace_id,
            program.storyboard_id,
            program.candidate_id,
            program.title,
            program.semantic_intent,
            program.story_arc,
            json.dumps(program.scenes, default=str),
            program.total_duration,
            json.dumps(program.visual_audio_specs, default=str),
            json.dumps(program.wrong_reading_locks, default=str),
            json.dumps(program.evidence_lineage_hashes, default=str),
            program.created_at.isoformat(),
        ))
        self._conn.commit()

    def get_semantic_program(self, workspace_id: str, program_id: str) -> Optional[SemanticProgramRecord]:
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT * FROM cae_semantic_programs WHERE workspace_id = ? AND program_id = ?
        """, (workspace_id, program_id))
        row = cursor.fetchone()
        if not row:
            return None
        return SemanticProgramRecord(
            workspace_id=row["workspace_id"],
            program_id=row["program_id"],
            storyboard_id=row["storyboard_id"],
            candidate_id=row["candidate_id"],
            title=row["title"],
            semantic_intent=row["semantic_intent"],
            story_arc=row["story_arc"],
            scenes=json.loads(row["scenes"]),
            total_duration=row["total_duration"],
            visual_audio_specs=json.loads(row["visual_audio_specs"]),
            wrong_reading_locks=json.loads(row["wrong_reading_locks"]),
            evidence_lineage_hashes=json.loads(row["evidence_lineage_hashes"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def list_semantic_programs(self, workspace_id: str, candidate_id: Optional[str] = None) -> List[SemanticProgramRecord]:
        cursor = self._conn.cursor()
        if candidate_id:
            cursor.execute("""
                SELECT * FROM cae_semantic_programs WHERE workspace_id = ? AND candidate_id = ? ORDER BY created_at ASC
            """, (workspace_id, candidate_id))
        else:
            cursor.execute("""
                SELECT * FROM cae_semantic_programs WHERE workspace_id = ? ORDER BY created_at ASC
            """, (workspace_id,))
        rows = cursor.fetchall()
        return [
            SemanticProgramRecord(
                workspace_id=row["workspace_id"],
                program_id=row["program_id"],
                storyboard_id=row["storyboard_id"],
                candidate_id=row["candidate_id"],
                title=row["title"],
                semantic_intent=row["semantic_intent"],
                story_arc=row["story_arc"],
                scenes=json.loads(row["scenes"]),
                total_duration=row["total_duration"],
                visual_audio_specs=json.loads(row["visual_audio_specs"]),
                wrong_reading_locks=json.loads(row["wrong_reading_locks"]),
                evidence_lineage_hashes=json.loads(row["evidence_lineage_hashes"]),
                created_at=datetime.fromisoformat(row["created_at"]),
            )
            for row in rows
        ]

    # --- Composition Handoff Operations ---

    def insert_composition_handoff(self, handoff: CompositionHandoffRecord) -> None:
        cursor = self._conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO cae_composition_handoff_receipts (
                receipt_id, workspace_id, program_id, candidate_id, storyboard_id,
                compiler_version, evidence_sha256_list, asset_id_list, wrong_reading_locks,
                composition_ir_ref, receipt_sha256, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            handoff.receipt_id,
            handoff.workspace_id,
            handoff.program_id,
            handoff.candidate_id,
            handoff.storyboard_id,
            handoff.compiler_version,
            json.dumps(handoff.evidence_sha256_list, default=str),
            json.dumps(handoff.asset_id_list, default=str),
            json.dumps(handoff.wrong_reading_locks, default=str),
            json.dumps(handoff.composition_ir_ref, default=str) if handoff.composition_ir_ref else None,
            handoff.receipt_sha256,
            handoff.created_at.isoformat(),
        ))
        self._conn.commit()

    def get_composition_handoff(self, workspace_id: str, receipt_id: str) -> Optional[CompositionHandoffRecord]:

        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT * FROM cae_composition_handoff_receipts WHERE workspace_id = ? AND receipt_id = ?
        """, (workspace_id, receipt_id))
        row = cursor.fetchone()
        if not row:
            return None
        return CompositionHandoffRecord(
            workspace_id=row["workspace_id"],
            receipt_id=row["receipt_id"],
            program_id=row["program_id"],
            candidate_id=row["candidate_id"],
            storyboard_id=row["storyboard_id"],
            compiler_version=row["compiler_version"],
            evidence_sha256_list=json.loads(row["evidence_sha256_list"]),
            asset_id_list=json.loads(row["asset_id_list"]),
            wrong_reading_locks=json.loads(row["wrong_reading_locks"]),
            composition_ir_ref=json.loads(row["composition_ir_ref"]) if row["composition_ir_ref"] else None,
            receipt_sha256=row["receipt_sha256"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def list_composition_handoffs(self, workspace_id: str, program_id: Optional[str] = None) -> List[CompositionHandoffRecord]:
        cursor = self._conn.cursor()
        if program_id:
            cursor.execute("""
                SELECT * FROM cae_composition_handoff_receipts WHERE workspace_id = ? AND program_id = ? ORDER BY created_at ASC
            """, (workspace_id, program_id))
        else:
            cursor.execute("""
                SELECT * FROM cae_composition_handoff_receipts WHERE workspace_id = ? ORDER BY created_at ASC
            """, (workspace_id,))
        rows = cursor.fetchall()
        return [
            CompositionHandoffRecord(
                workspace_id=row["workspace_id"],
                receipt_id=row["receipt_id"],
                program_id=row["program_id"],
                candidate_id=row["candidate_id"],
                storyboard_id=row["storyboard_id"],
                compiler_version=row["compiler_version"],
                evidence_sha256_list=json.loads(row["evidence_sha256_list"]),
                asset_id_list=json.loads(row["asset_id_list"]),
                wrong_reading_locks=json.loads(row["wrong_reading_locks"]),
                composition_ir_ref=json.loads(row["composition_ir_ref"]) if row["composition_ir_ref"] else None,
                receipt_sha256=row["receipt_sha256"],
                created_at=datetime.fromisoformat(row["created_at"]),
            )
            for row in rows
        ]

    # --- Editorial Receipts Operations ---

    def insert_decision_receipt(self, receipt: EditorialDecisionReceiptRecord) -> None:
        cursor = self._conn.cursor()
        cursor.execute("""
            INSERT INTO cae_editorial_receipts (
                receipt_id, workspace_id, operator_id, candidate_id, action_type,
                rationale, taste_delta, is_synthetic_blocked, metadata_payload, receipt_sha256, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            receipt.receipt_id,
            receipt.workspace_id,
            receipt.operator_id,
            receipt.candidate_id,
            receipt.action_type,
            receipt.rationale,
            receipt.taste_delta,
            1 if receipt.is_synthetic_blocked else 0,
            json.dumps(receipt.metadata_payload, default=str),
            receipt.receipt_sha256,
            receipt.created_at.isoformat(),
        ))
        self._conn.commit()

    def get_decision_receipt(self, workspace_id: str, receipt_id: str) -> Optional[EditorialDecisionReceiptRecord]:
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT * FROM cae_editorial_receipts WHERE workspace_id = ? AND receipt_id = ?
        """, (workspace_id, receipt_id))
        row = cursor.fetchone()
        if not row:
            return None
        return EditorialDecisionReceiptRecord(
            workspace_id=row["workspace_id"],
            receipt_id=row["receipt_id"],
            operator_id=row["operator_id"],
            candidate_id=row["candidate_id"],
            action_type=row["action_type"],
            rationale=row["rationale"],
            taste_delta=row["taste_delta"],
            is_synthetic_blocked=bool(row["is_synthetic_blocked"]),
            metadata_payload=json.loads(row["metadata_payload"]),
            receipt_sha256=row["receipt_sha256"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def list_decision_receipts(self, workspace_id: str, candidate_id: Optional[str] = None) -> List[EditorialDecisionReceiptRecord]:
        cursor = self._conn.cursor()
        if candidate_id:
            cursor.execute("""
                SELECT * FROM cae_editorial_receipts WHERE workspace_id = ? AND candidate_id = ? ORDER BY created_at ASC
            """, (workspace_id, candidate_id))
        else:
            cursor.execute("""
                SELECT * FROM cae_editorial_receipts WHERE workspace_id = ? ORDER BY created_at ASC
            """, (workspace_id,))
        rows = cursor.fetchall()
        return [
            EditorialDecisionReceiptRecord(
                workspace_id=row["workspace_id"],
                receipt_id=row["receipt_id"],
                operator_id=row["operator_id"],
                candidate_id=row["candidate_id"],
                action_type=row["action_type"],
                rationale=row["rationale"],
                taste_delta=row["taste_delta"],
                is_synthetic_blocked=bool(row["is_synthetic_blocked"]),
                metadata_payload=json.loads(row["metadata_payload"]),
                receipt_sha256=row["receipt_sha256"],
                created_at=datetime.fromisoformat(row["created_at"]),
            )
            for row in rows
        ]

