"""
interview_semantic_store.py
----------------------------
Authoritative SQLite / PostgreSQL Relational Storage Adapter for Activative Interview
Briefs, Interview Sessions, and Semantic Audit Receipts (CAE M33).
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class InterviewBriefRecord(BaseModel):
    """Authoritative representation of an Activative Interview Brief entity."""
    workspace_id: str
    brief_id: str
    hypothesis_id: str
    guest_name: str
    research_package_ref: Dict[str, Any]
    brand_context_ref: Optional[Dict[str, Any]] = None
    voice_dna_ref: Optional[Dict[str, Any]] = None
    tension_hypothesis: str
    matrix_of_edging_seed: Dict[str, Any]
    planned_questions: List[Dict[str, Any]] = Field(default_factory=list)
    expression_targets: List[str] = Field(default_factory=list)
    composer_authority: Dict[str, str]
    canonical_sha256: str
    lifecycle_state: str = "SEALED"  # DRAFT, COMPILED, SEALED, ARCHIVED
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class InterviewSessionRecord(BaseModel):
    """Authoritative representation of an Interview Elicitation Session entity."""
    workspace_id: str
    session_id: str
    brief_id: str
    status: str = "INITIALIZED"  # INITIALIZED, QUESTIONING, TRANSCRIBING, COMPLETED, CANCELLED
    turns_count: int = 0
    evidence_package_ref: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class InterviewSemanticReceiptRecord(BaseModel):
    """Authoritative audit receipt for Interview Brief compilation & sealing."""
    workspace_id: str
    receipt_id: str
    brief_id: str
    hypothesis_id: str
    evaluator_lane: str
    decision: str  # SEALED, REJECTED, QUARANTINED, AUTHENTICATED
    score_breakdown_micros: Dict[str, int] = Field(default_factory=dict)
    gate_checks: List[Dict[str, Any]] = Field(default_factory=list)
    signature: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class InterviewTurnRecord(BaseModel):
    """Authoritative representation of an Interview Turn entity (CA-EVT-003)."""
    workspace_id: str
    turn_id: str
    session_id: str
    turn_index: int
    speaker: str  # CONDUCTOR, GUEST
    question_id: str
    stage: str
    prompt_text: str
    transcript_text: str
    transcript_sha256: str
    is_authenticated: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class InterviewObservationRecord(BaseModel):
    """Authoritative representation of a semantic acquisition observation (CAE-M07)."""
    workspace_id: str
    observation_id: str
    turn_id: str
    session_id: str
    kind: str  # guest_stated_evidence, system_inference, guest_validated_interpretation
    statement_text: str
    evidence_mode: str
    temporal_orientation: str
    information_completeness: str
    specificity_micros: int
    authenticity_micros: int
    is_authenticated: bool = False
    discrepancy_refs: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EvidencePackageRecord(BaseModel):
    """Authoritative representation of an Authenticated Evidence Package (CAE-M09)."""
    workspace_id: str
    package_id: str
    session_id: str
    brief_id: str
    guest_id: str
    canonical_sha256: str
    accepted_evidence_records: List[Dict[str, Any]] = Field(default_factory=list)
    downstream_candidates: List[Dict[str, Any]] = Field(default_factory=list)
    is_authenticated: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EvidenceAuthenticationRecord(BaseModel):
    """Authoritative evaluation receipt for Evidence Authentication (CA-REC-003)."""
    workspace_id: str
    auth_id: str
    session_id: str
    evidence_package_id: str
    evaluator_lane: str
    evaluator_actor_id: str
    verdict: str  # AUTHENTICATED, REJECTED, NEEDS_REPAIR
    rationale: str
    signature: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class InterviewSemanticStore:
    """Relational store adapter supporting dual SQLite and PostgreSQL execution."""

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self._init_schema()

    def _init_schema(self) -> None:
        """Create required tables if they do not exist."""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS interview_briefs (
                    workspace_id TEXT NOT NULL,
                    brief_id TEXT NOT NULL,
                    hypothesis_id TEXT NOT NULL,
                    guest_name TEXT NOT NULL,
                    research_package_ref TEXT NOT NULL,
                    brand_context_ref TEXT,
                    voice_dna_ref TEXT,
                    tension_hypothesis TEXT NOT NULL,
                    matrix_of_edging_seed TEXT NOT NULL,
                    planned_questions TEXT NOT NULL,
                    expression_targets TEXT NOT NULL,
                    composer_authority TEXT NOT NULL,
                    canonical_sha256 TEXT NOT NULL,
                    lifecycle_state TEXT NOT NULL DEFAULT 'SEALED',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, brief_id)
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS interview_sessions (
                    workspace_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    brief_id TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'INITIALIZED',
                    turns_count INTEGER NOT NULL DEFAULT 0,
                    evidence_package_ref TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, session_id)
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS interview_semantic_receipts (
                    workspace_id TEXT NOT NULL,
                    receipt_id TEXT NOT NULL,
                    brief_id TEXT NOT NULL,
                    hypothesis_id TEXT NOT NULL,
                    evaluator_lane TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    score_breakdown_micros TEXT NOT NULL,
                    gate_checks TEXT NOT NULL,
                    signature TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, receipt_id)
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS interview_turns (
                    workspace_id TEXT NOT NULL,
                    turn_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    turn_index INTEGER NOT NULL,
                    speaker TEXT NOT NULL,
                    question_id TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    prompt_text TEXT NOT NULL,
                    transcript_text TEXT NOT NULL,
                    transcript_sha256 TEXT NOT NULL,
                    is_authenticated INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, turn_id)
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS interview_observations (
                    workspace_id TEXT NOT NULL,
                    observation_id TEXT NOT NULL,
                    turn_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    kind TEXT NOT NULL,
                    statement_text TEXT NOT NULL,
                    evidence_mode TEXT NOT NULL,
                    temporal_orientation TEXT NOT NULL,
                    information_completeness TEXT NOT NULL,
                    specificity_micros INTEGER NOT NULL,
                    authenticity_micros INTEGER NOT NULL,
                    is_authenticated INTEGER NOT NULL DEFAULT 0,
                    discrepancy_refs TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, observation_id)
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS interview_evidence_packages (
                    workspace_id TEXT NOT NULL,
                    package_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    brief_id TEXT NOT NULL,
                    guest_id TEXT NOT NULL,
                    canonical_sha256 TEXT NOT NULL,
                    accepted_evidence_records TEXT NOT NULL,
                    downstream_candidates TEXT NOT NULL,
                    is_authenticated INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, package_id)
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS evidence_authentications (
                    workspace_id TEXT NOT NULL,
                    auth_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    evidence_package_id TEXT NOT NULL,
                    evaluator_lane TEXT NOT NULL,
                    evaluator_actor_id TEXT NOT NULL,
                    verdict TEXT NOT NULL,
                    rationale TEXT NOT NULL,
                    signature TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, auth_id)
                );
            """)

    # --- Brief Operations ---

    def store_brief(self, record: InterviewBriefRecord) -> None:
        """Stores or updates an interview brief."""
        with self.conn:
            self.conn.execute("""
                INSERT INTO interview_briefs (
                    workspace_id, brief_id, hypothesis_id, guest_name,
                    research_package_ref, brand_context_ref, voice_dna_ref,
                    tension_hypothesis, matrix_of_edging_seed, planned_questions,
                    expression_targets, composer_authority, canonical_sha256,
                    lifecycle_state, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (workspace_id, brief_id) DO UPDATE SET
                    hypothesis_id = excluded.hypothesis_id,
                    guest_name = excluded.guest_name,
                    research_package_ref = excluded.research_package_ref,
                    brand_context_ref = excluded.brand_context_ref,
                    voice_dna_ref = excluded.voice_dna_ref,
                    tension_hypothesis = excluded.tension_hypothesis,
                    matrix_of_edging_seed = excluded.matrix_of_edging_seed,
                    planned_questions = excluded.planned_questions,
                    expression_targets = excluded.expression_targets,
                    composer_authority = excluded.composer_authority,
                    canonical_sha256 = excluded.canonical_sha256,
                    lifecycle_state = excluded.lifecycle_state,
                    updated_at = excluded.updated_at
            """, (
                record.workspace_id,
                record.brief_id,
                record.hypothesis_id,
                record.guest_name,
                json.dumps(record.research_package_ref, sort_keys=True),
                json.dumps(record.brand_context_ref, sort_keys=True) if record.brand_context_ref else None,
                json.dumps(record.voice_dna_ref, sort_keys=True) if record.voice_dna_ref else None,
                record.tension_hypothesis,
                json.dumps(record.matrix_of_edging_seed, sort_keys=True),
                json.dumps(record.planned_questions, sort_keys=True),
                json.dumps(record.expression_targets, sort_keys=True),
                json.dumps(record.composer_authority, sort_keys=True),
                record.canonical_sha256,
                record.lifecycle_state,
                record.created_at.isoformat(),
                record.updated_at.isoformat(),
            ))

    def get_brief(self, workspace_id: str, brief_id: str) -> Optional[InterviewBriefRecord]:
        """Retrieves an interview brief by workspace and brief ID."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT workspace_id, brief_id, hypothesis_id, guest_name,
                   research_package_ref, brand_context_ref, voice_dna_ref,
                   tension_hypothesis, matrix_of_edging_seed, planned_questions,
                   expression_targets, composer_authority, canonical_sha256,
                   lifecycle_state, created_at, updated_at
            FROM interview_briefs
            WHERE workspace_id = ? AND brief_id = ?
        """, (workspace_id, brief_id))
        row = cursor.fetchone()
        if not row:
            return None
        return InterviewBriefRecord(
            workspace_id=row[0],
            brief_id=row[1],
            hypothesis_id=row[2],
            guest_name=row[3],
            research_package_ref=json.loads(row[4]),
            brand_context_ref=json.loads(row[5]) if row[5] else None,
            voice_dna_ref=json.loads(row[6]) if row[6] else None,
            tension_hypothesis=row[7],
            matrix_of_edging_seed=json.loads(row[8]),
            planned_questions=json.loads(row[9]),
            expression_targets=json.loads(row[10]),
            composer_authority=json.loads(row[11]),
            canonical_sha256=row[12],
            lifecycle_state=row[13],
            created_at=datetime.fromisoformat(row[14]),
            updated_at=datetime.fromisoformat(row[15]),
        )

    def list_briefs(self, workspace_id: str, hypothesis_id: Optional[str] = None) -> List[InterviewBriefRecord]:
        """Lists interview briefs in a workspace."""
        cursor = self.conn.cursor()
        if hypothesis_id:
            cursor.execute("""
                SELECT workspace_id, brief_id, hypothesis_id, guest_name,
                       research_package_ref, brand_context_ref, voice_dna_ref,
                       tension_hypothesis, matrix_of_edging_seed, planned_questions,
                       expression_targets, composer_authority, canonical_sha256,
                       lifecycle_state, created_at, updated_at
                FROM interview_briefs
                WHERE workspace_id = ? AND hypothesis_id = ?
                ORDER BY created_at DESC
            """, (workspace_id, hypothesis_id))
        else:
            cursor.execute("""
                SELECT workspace_id, brief_id, hypothesis_id, guest_name,
                       research_package_ref, brand_context_ref, voice_dna_ref,
                       tension_hypothesis, matrix_of_edging_seed, planned_questions,
                       expression_targets, composer_authority, canonical_sha256,
                       lifecycle_state, created_at, updated_at
                FROM interview_briefs
                WHERE workspace_id = ?
                ORDER BY created_at DESC
            """, (workspace_id,))
        results = []
        for row in cursor.fetchall():
            results.append(InterviewBriefRecord(
                workspace_id=row[0],
                brief_id=row[1],
                hypothesis_id=row[2],
                guest_name=row[3],
                research_package_ref=json.loads(row[4]),
                brand_context_ref=json.loads(row[5]) if row[5] else None,
                voice_dna_ref=json.loads(row[6]) if row[6] else None,
                tension_hypothesis=row[7],
                matrix_of_edging_seed=json.loads(row[8]),
                planned_questions=json.loads(row[9]),
                expression_targets=json.loads(row[10]),
                composer_authority=json.loads(row[11]),
                canonical_sha256=row[12],
                lifecycle_state=row[13],
                created_at=datetime.fromisoformat(row[14]),
                updated_at=datetime.fromisoformat(row[15]),
            ))
        return results

    # --- Session Operations ---

    def store_session(self, record: InterviewSessionRecord) -> None:
        """Stores or updates an interview session."""
        with self.conn:
            self.conn.execute("""
                INSERT INTO interview_sessions (
                    workspace_id, session_id, brief_id, status,
                    turns_count, evidence_package_ref, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (workspace_id, session_id) DO UPDATE SET
                    brief_id = excluded.brief_id,
                    status = excluded.status,
                    turns_count = excluded.turns_count,
                    evidence_package_ref = excluded.evidence_package_ref,
                    updated_at = excluded.updated_at
            """, (
                record.workspace_id,
                record.session_id,
                record.brief_id,
                record.status,
                record.turns_count,
                json.dumps(record.evidence_package_ref, sort_keys=True) if record.evidence_package_ref else None,
                record.created_at.isoformat(),
                record.updated_at.isoformat(),
            ))

    def get_session(self, workspace_id: str, session_id: str) -> Optional[InterviewSessionRecord]:
        """Retrieves an interview session by workspace and session ID."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT workspace_id, session_id, brief_id, status,
                   turns_count, evidence_package_ref, created_at, updated_at
            FROM interview_sessions
            WHERE workspace_id = ? AND session_id = ?
        """, (workspace_id, session_id))
        row = cursor.fetchone()
        if not row:
            return None
        return InterviewSessionRecord(
            workspace_id=row[0],
            session_id=row[1],
            brief_id=row[2],
            status=row[3],
            turns_count=row[4],
            evidence_package_ref=json.loads(row[5]) if row[5] else None,
            created_at=datetime.fromisoformat(row[6]),
            updated_at=datetime.fromisoformat(row[7]),
        )

    # --- Receipt Operations ---

    def store_receipt(self, record: InterviewSemanticReceiptRecord) -> None:
        """Stores an interview semantic execution receipt."""
        with self.conn:
            self.conn.execute("""
                INSERT INTO interview_semantic_receipts (
                    workspace_id, receipt_id, brief_id, hypothesis_id,
                    evaluator_lane, decision, score_breakdown_micros,
                    gate_checks, signature, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (workspace_id, receipt_id) DO NOTHING
            """, (
                record.workspace_id,
                record.receipt_id,
                record.brief_id,
                record.hypothesis_id,
                record.evaluator_lane,
                record.decision,
                json.dumps(record.score_breakdown_micros, sort_keys=True),
                json.dumps(record.gate_checks, sort_keys=True),
                record.signature,
                record.created_at.isoformat(),
            ))

    def get_receipt(self, workspace_id: str, receipt_id: str) -> Optional[InterviewSemanticReceiptRecord]:
        """Retrieves an execution receipt."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT workspace_id, receipt_id, brief_id, hypothesis_id,
                   evaluator_lane, decision, score_breakdown_micros,
                   gate_checks, signature, created_at
            FROM interview_semantic_receipts
            WHERE workspace_id = ? AND receipt_id = ?
        """, (workspace_id, receipt_id))
        row = cursor.fetchone()
        if not row:
            return None
        return InterviewSemanticReceiptRecord(
            workspace_id=row[0],
            receipt_id=row[1],
            brief_id=row[2],
            hypothesis_id=row[3],
            evaluator_lane=row[4],
            decision=row[5],
            score_breakdown_micros=json.loads(row[6]),
            gate_checks=json.loads(row[7]),
            signature=row[8],
            created_at=datetime.fromisoformat(row[9]),
        )

    # --- Turn Operations ---

    def store_turn(self, record: InterviewTurnRecord) -> None:
        """Stores or updates an interview turn."""
        with self.conn:
            self.conn.execute("""
                INSERT INTO interview_turns (
                    workspace_id, turn_id, session_id, turn_index,
                    speaker, question_id, stage, prompt_text,
                    transcript_text, transcript_sha256, is_authenticated,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (workspace_id, turn_id) DO UPDATE SET
                    transcript_text = excluded.transcript_text,
                    transcript_sha256 = excluded.transcript_sha256,
                    is_authenticated = excluded.is_authenticated
            """, (
                record.workspace_id,
                record.turn_id,
                record.session_id,
                record.turn_index,
                record.speaker,
                record.question_id,
                record.stage,
                record.prompt_text,
                record.transcript_text,
                record.transcript_sha256,
                1 if record.is_authenticated else 0,
                record.created_at.isoformat(),
            ))

    def get_turn(self, workspace_id: str, turn_id: str) -> Optional[InterviewTurnRecord]:
        """Retrieves a single interview turn by workspace and turn ID."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT workspace_id, turn_id, session_id, turn_index,
                   speaker, question_id, stage, prompt_text,
                   transcript_text, transcript_sha256, is_authenticated,
                   created_at
            FROM interview_turns
            WHERE workspace_id = ? AND turn_id = ?
        """, (workspace_id, turn_id))
        row = cursor.fetchone()
        if not row:
            return None
        return InterviewTurnRecord(
            workspace_id=row[0],
            turn_id=row[1],
            session_id=row[2],
            turn_index=row[3],
            speaker=row[4],
            question_id=row[5],
            stage=row[6],
            prompt_text=row[7],
            transcript_text=row[8],
            transcript_sha256=row[9],
            is_authenticated=bool(row[10]),
            created_at=datetime.fromisoformat(row[11]),
        )

    def list_turns(self, workspace_id: str, session_id: str) -> List[InterviewTurnRecord]:
        """Lists all interview turns for a given session ordered by turn_index."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT workspace_id, turn_id, session_id, turn_index,
                   speaker, question_id, stage, prompt_text,
                   transcript_text, transcript_sha256, is_authenticated,
                   created_at
            FROM interview_turns
            WHERE workspace_id = ? AND session_id = ?
            ORDER BY turn_index ASC
        """, (workspace_id, session_id))
        results = []
        for row in cursor.fetchall():
            results.append(InterviewTurnRecord(
                workspace_id=row[0],
                turn_id=row[1],
                session_id=row[2],
                turn_index=row[3],
                speaker=row[4],
                question_id=row[5],
                stage=row[6],
                prompt_text=row[7],
                transcript_text=row[8],
                transcript_sha256=row[9],
                is_authenticated=bool(row[10]),
                created_at=datetime.fromisoformat(row[11]),
            ))
        return results

    # --- Observation Operations ---

    def store_observation(self, record: InterviewObservationRecord) -> None:
        """Stores a semantic acquisition observation."""
        with self.conn:
            self.conn.execute("""
                INSERT INTO interview_observations (
                    workspace_id, observation_id, turn_id, session_id,
                    kind, statement_text, evidence_mode,
                    temporal_orientation, information_completeness,
                    specificity_micros, authenticity_micros,
                    is_authenticated, discrepancy_refs, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (workspace_id, observation_id) DO NOTHING
            """, (
                record.workspace_id,
                record.observation_id,
                record.turn_id,
                record.session_id,
                record.kind,
                record.statement_text,
                record.evidence_mode,
                record.temporal_orientation,
                record.information_completeness,
                record.specificity_micros,
                record.authenticity_micros,
                1 if record.is_authenticated else 0,
                json.dumps(record.discrepancy_refs, sort_keys=True),
                record.created_at.isoformat(),
            ))

    def list_observations(
        self,
        workspace_id: str,
        session_id: Optional[str] = None,
        turn_id: Optional[str] = None,
    ) -> List[InterviewObservationRecord]:
        """Lists observations matching the specified workspace and optional filters."""
        cursor = self.conn.cursor()
        query = """
            SELECT workspace_id, observation_id, turn_id, session_id,
                   kind, statement_text, evidence_mode,
                   temporal_orientation, information_completeness,
                   specificity_micros, authenticity_micros,
                   is_authenticated, discrepancy_refs, created_at
            FROM interview_observations
            WHERE workspace_id = ?
        """
        params: List[Any] = [workspace_id]
        if session_id:
            query += " AND session_id = ?"
            params.append(session_id)
        if turn_id:
            query += " AND turn_id = ?"
            params.append(turn_id)
        query += " ORDER BY created_at ASC"

        cursor.execute(query, tuple(params))
        results = []
        for row in cursor.fetchall():
            results.append(InterviewObservationRecord(
                workspace_id=row[0],
                observation_id=row[1],
                turn_id=row[2],
                session_id=row[3],
                kind=row[4],
                statement_text=row[5],
                evidence_mode=row[6],
                temporal_orientation=row[7],
                information_completeness=row[8],
                specificity_micros=row[9],
                authenticity_micros=row[10],
                is_authenticated=bool(row[11]),
                discrepancy_refs=json.loads(row[12]),
                created_at=datetime.fromisoformat(row[13]),
            ))
        return results

    # --- Evidence Package Operations ---

    def store_evidence_package(self, record: EvidencePackageRecord) -> None:
        """Stores an authenticated evidence package."""
        with self.conn:
            self.conn.execute("""
                INSERT INTO interview_evidence_packages (
                    workspace_id, package_id, session_id, brief_id,
                    guest_id, canonical_sha256, accepted_evidence_records,
                    downstream_candidates, is_authenticated, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (workspace_id, package_id) DO UPDATE SET
                    canonical_sha256 = excluded.canonical_sha256,
                    accepted_evidence_records = excluded.accepted_evidence_records,
                    downstream_candidates = excluded.downstream_candidates,
                    is_authenticated = excluded.is_authenticated
            """, (
                record.workspace_id,
                record.package_id,
                record.session_id,
                record.brief_id,
                record.guest_id,
                record.canonical_sha256,
                json.dumps(record.accepted_evidence_records, sort_keys=True),
                json.dumps(record.downstream_candidates, sort_keys=True),
                1 if record.is_authenticated else 0,
                record.created_at.isoformat(),
            ))

    def get_evidence_package(self, workspace_id: str, package_id: str) -> Optional[EvidencePackageRecord]:
        """Retrieves an evidence package by workspace and package ID."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT workspace_id, package_id, session_id, brief_id,
                   guest_id, canonical_sha256, accepted_evidence_records,
                   downstream_candidates, is_authenticated, created_at
            FROM interview_evidence_packages
            WHERE workspace_id = ? AND package_id = ?
        """, (workspace_id, package_id))
        row = cursor.fetchone()
        if not row:
            return None
        return EvidencePackageRecord(
            workspace_id=row[0],
            package_id=row[1],
            session_id=row[2],
            brief_id=row[3],
            guest_id=row[4],
            canonical_sha256=row[5],
            accepted_evidence_records=json.loads(row[6]),
            downstream_candidates=json.loads(row[7]),
            is_authenticated=bool(row[8]),
            created_at=datetime.fromisoformat(row[9]),
        )

    def get_evidence_package_by_session(self, workspace_id: str, session_id: str) -> Optional[EvidencePackageRecord]:
        """Retrieves an evidence package for a given session."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT workspace_id, package_id, session_id, brief_id,
                   guest_id, canonical_sha256, accepted_evidence_records,
                   downstream_candidates, is_authenticated, created_at
            FROM interview_evidence_packages
            WHERE workspace_id = ? AND session_id = ?
            ORDER BY created_at DESC
            LIMIT 1
        """, (workspace_id, session_id))
        row = cursor.fetchone()
        if not row:
            return None
        return EvidencePackageRecord(
            workspace_id=row[0],
            package_id=row[1],
            session_id=row[2],
            brief_id=row[3],
            guest_id=row[4],
            canonical_sha256=row[5],
            accepted_evidence_records=json.loads(row[6]),
            downstream_candidates=json.loads(row[7]),
            is_authenticated=bool(row[8]),
            created_at=datetime.fromisoformat(row[9]),
        )

    # --- Evidence Authentication Operations ---

    def store_evidence_authentication(self, record: EvidenceAuthenticationRecord) -> None:
        """Stores an evidence authentication record."""
        with self.conn:
            self.conn.execute("""
                INSERT INTO evidence_authentications (
                    workspace_id, auth_id, session_id, evidence_package_id,
                    evaluator_lane, evaluator_actor_id, verdict,
                    rationale, signature, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (workspace_id, auth_id) DO NOTHING
            """, (
                record.workspace_id,
                record.auth_id,
                record.session_id,
                record.evidence_package_id,
                record.evaluator_lane,
                record.evaluator_actor_id,
                record.verdict,
                record.rationale,
                record.signature,
                record.created_at.isoformat(),
            ))

    def list_evidence_authentications(
        self,
        workspace_id: str,
        session_id: Optional[str] = None,
    ) -> List[EvidenceAuthenticationRecord]:
        """Lists evidence authentications for a workspace and optional session."""
        cursor = self.conn.cursor()
        if session_id:
            cursor.execute("""
                SELECT workspace_id, auth_id, session_id, evidence_package_id,
                       evaluator_lane, evaluator_actor_id, verdict,
                       rationale, signature, created_at
                FROM evidence_authentications
                WHERE workspace_id = ? AND session_id = ?
                ORDER BY created_at ASC
            """, (workspace_id, session_id))
        else:
            cursor.execute("""
                SELECT workspace_id, auth_id, session_id, evidence_package_id,
                       evaluator_lane, evaluator_actor_id, verdict,
                       rationale, signature, created_at
                FROM evidence_authentications
                WHERE workspace_id = ?
                ORDER BY created_at ASC
            """, (workspace_id,))
        results = []
        for row in cursor.fetchall():
            results.append(EvidenceAuthenticationRecord(
                workspace_id=row[0],
                auth_id=row[1],
                session_id=row[2],
                evidence_package_id=row[3],
                evaluator_lane=row[4],
                evaluator_actor_id=row[5],
                verdict=row[6],
                rationale=row[7],
                signature=row[8],
                created_at=datetime.fromisoformat(row[9]),
            ))
        return results

