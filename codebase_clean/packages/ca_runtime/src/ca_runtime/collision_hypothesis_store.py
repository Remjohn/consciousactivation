"""
collision_hypothesis_store.py
-----------------------------
Authoritative SQLite / PostgreSQL Relational Storage Adapter for Matrix of Edging,
Collision Hypotheses, Hypothesis Portfolios, and Evaluation Receipts (CAE M32).
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class MatrixOfEdgingRecord(BaseModel):
    """Authoritative representation of a Matrix of Edging entity."""
    workspace_id: str
    matrix_id: str
    broad_signal: str
    hidden_pressure: str
    surviving_edge: str
    identity_gap: str
    audience_reality: str
    desired_recognition: str
    smallest_useful_movement: str
    counteractivation_risks: List[str] = Field(default_factory=list)
    source_refs: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CollisionHypothesisRecord(BaseModel):
    """Authoritative representation of a Collision Hypothesis entity."""
    workspace_id: str
    hypothesis_id: str
    title: str
    relation_type: str  # ANALOGY, INVERSION, PARADOX, SYSTEMS_LENS, COUNTER_POSITION
    audience_id: str
    audience_tension_ref: str
    guest_id: str
    guest_lived_proof_citation: str
    research_signal_id: str
    sda_invariant: str = "SDA-INV-001_ACTIVE_TENSION"
    oblique_lens: Optional[Dict[str, Any]] = None
    bridge_statement: str
    evidence_references: List[str] = Field(default_factory=list)
    novelty_assessment: Dict[str, Any]
    falsification_condition: Dict[str, Any]
    heritage_eval: Dict[str, Any]
    status: str = "PENDING"  # PENDING, APPROVED, REJECTED, QUARANTINED
    approval_notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CollisionHypothesisPortfolioRecord(BaseModel):
    """Authoritative representation of a Collision Hypothesis Portfolio entity."""
    workspace_id: str
    portfolio_id: str
    candidate_hypothesis_ids: List[str] = Field(default_factory=list)
    diversity_signature: Dict[str, Any]
    status: str = "DRAFT"  # DRAFT, EVALUATED, DECIDED
    selected_hypothesis_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class HypothesisEvaluationReceiptRecord(BaseModel):
    """Authoritative audit receipt for comparative portfolio & gate evaluation."""
    workspace_id: str
    receipt_id: str
    portfolio_id: str
    hypothesis_id: str
    evaluator_lane: str
    decision: str  # APPROVED, REJECTED, QUARANTINED
    score_breakdown_micros: Dict[str, int] = Field(default_factory=dict)
    gate_checks: List[Dict[str, Any]] = Field(default_factory=list)
    signature: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CollisionHypothesisStore:
    """Relational store adapter supporting dual SQLite and PostgreSQL execution."""

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self._init_schema()

    def _init_schema(self) -> None:
        """Create required tables if they do not exist."""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS matrix_of_edging (
                    workspace_id TEXT NOT NULL,
                    matrix_id TEXT NOT NULL,
                    broad_signal TEXT NOT NULL,
                    hidden_pressure TEXT NOT NULL,
                    surviving_edge TEXT NOT NULL,
                    identity_gap TEXT NOT NULL,
                    audience_reality TEXT NOT NULL,
                    desired_recognition TEXT NOT NULL,
                    smallest_useful_movement TEXT NOT NULL,
                    counteractivation_risks TEXT NOT NULL DEFAULT '[]',
                    source_refs TEXT NOT NULL DEFAULT '[]',
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, matrix_id)
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS collision_hypothesis (
                    workspace_id TEXT NOT NULL,
                    hypothesis_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    relation_type TEXT NOT NULL,
                    audience_id TEXT NOT NULL,
                    audience_tension_ref TEXT NOT NULL,
                    guest_id TEXT NOT NULL,
                    guest_lived_proof_citation TEXT NOT NULL,
                    research_signal_id TEXT NOT NULL,
                    sda_invariant TEXT NOT NULL DEFAULT 'SDA-INV-001_ACTIVE_TENSION',
                    oblique_lens TEXT,
                    bridge_statement TEXT NOT NULL,
                    evidence_references TEXT NOT NULL DEFAULT '[]',
                    novelty_assessment TEXT NOT NULL,
                    falsification_condition TEXT NOT NULL,
                    heritage_eval TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'PENDING',
                    approval_notes TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, hypothesis_id)
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS collision_hypothesis_portfolio (
                    workspace_id TEXT NOT NULL,
                    portfolio_id TEXT NOT NULL,
                    candidate_hypothesis_ids TEXT NOT NULL DEFAULT '[]',
                    diversity_signature TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'DRAFT',
                    selected_hypothesis_id TEXT,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, portfolio_id)
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS hypothesis_evaluation_receipt (
                    workspace_id TEXT NOT NULL,
                    receipt_id TEXT NOT NULL,
                    portfolio_id TEXT NOT NULL,
                    hypothesis_id TEXT NOT NULL,
                    evaluator_lane TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    score_breakdown_micros TEXT NOT NULL DEFAULT '{}',
                    gate_checks TEXT NOT NULL DEFAULT '[]',
                    signature TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, receipt_id)
                );
            """)
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_hyp_status ON collision_hypothesis (workspace_id, status);")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_hyp_rel ON collision_hypothesis (workspace_id, relation_type);")

    def store_matrix(self, matrix: MatrixOfEdgingRecord) -> MatrixOfEdgingRecord:
        """Upsert a Matrix of Edging record."""
        with self.conn:
            self.conn.execute("""
                INSERT INTO matrix_of_edging (
                    workspace_id, matrix_id, broad_signal, hidden_pressure,
                    surviving_edge, identity_gap, audience_reality, desired_recognition,
                    smallest_useful_movement, counteractivation_risks, source_refs, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(workspace_id, matrix_id) DO UPDATE SET
                    broad_signal=excluded.broad_signal,
                    hidden_pressure=excluded.hidden_pressure,
                    surviving_edge=excluded.surviving_edge,
                    identity_gap=excluded.identity_gap,
                    audience_reality=excluded.audience_reality,
                    desired_recognition=excluded.desired_recognition,
                    smallest_useful_movement=excluded.smallest_useful_movement,
                    counteractivation_risks=excluded.counteractivation_risks,
                    source_refs=excluded.source_refs,
                    created_at=excluded.created_at;
            """, (
                matrix.workspace_id,
                matrix.matrix_id,
                matrix.broad_signal,
                matrix.hidden_pressure,
                matrix.surviving_edge,
                matrix.identity_gap,
                matrix.audience_reality,
                matrix.desired_recognition,
                matrix.smallest_useful_movement,
                json.dumps(matrix.counteractivation_risks),
                json.dumps(matrix.source_refs),
                matrix.created_at.isoformat(),
            ))
        return matrix

    def get_matrix(self, workspace_id: str, matrix_id: str) -> Optional[MatrixOfEdgingRecord]:
        """Fetch a Matrix of Edging record by ID."""
        cursor = self.conn.execute("""
            SELECT workspace_id, matrix_id, broad_signal, hidden_pressure,
                   surviving_edge, identity_gap, audience_reality, desired_recognition,
                   smallest_useful_movement, counteractivation_risks, source_refs, created_at
            FROM matrix_of_edging
            WHERE workspace_id = ? AND matrix_id = ?;
        """, (workspace_id, matrix_id))
        row = cursor.fetchone()
        if not row:
            return None
        return MatrixOfEdgingRecord(
            workspace_id=row[0],
            matrix_id=row[1],
            broad_signal=row[2],
            hidden_pressure=row[3],
            surviving_edge=row[4],
            identity_gap=row[5],
            audience_reality=row[6],
            desired_recognition=row[7],
            smallest_useful_movement=row[8],
            counteractivation_risks=json.loads(row[9]),
            source_refs=json.loads(row[10]),
            created_at=datetime.fromisoformat(row[11]),
        )

    def list_matrices(self, workspace_id: str) -> List[MatrixOfEdgingRecord]:
        """List all Matrix of Edging records for a workspace."""
        cursor = self.conn.execute("""
            SELECT workspace_id, matrix_id, broad_signal, hidden_pressure,
                   surviving_edge, identity_gap, audience_reality, desired_recognition,
                   smallest_useful_movement, counteractivation_risks, source_refs, created_at
            FROM matrix_of_edging
            WHERE workspace_id = ?
            ORDER BY created_at DESC;
        """, (workspace_id,))
        results = []
        for row in cursor.fetchall():
            results.append(MatrixOfEdgingRecord(
                workspace_id=row[0],
                matrix_id=row[1],
                broad_signal=row[2],
                hidden_pressure=row[3],
                surviving_edge=row[4],
                identity_gap=row[5],
                audience_reality=row[6],
                desired_recognition=row[7],
                smallest_useful_movement=row[8],
                counteractivation_risks=json.loads(row[9]),
                source_refs=json.loads(row[10]),
                created_at=datetime.fromisoformat(row[11]),
            ))
        return results

    def store_hypothesis(self, hypothesis: CollisionHypothesisRecord) -> CollisionHypothesisRecord:
        """Upsert a Collision Hypothesis record."""
        with self.conn:
            self.conn.execute("""
                INSERT INTO collision_hypothesis (
                    workspace_id, hypothesis_id, title, relation_type, audience_id,
                    audience_tension_ref, guest_id, guest_lived_proof_citation,
                    research_signal_id, sda_invariant, oblique_lens, bridge_statement,
                    evidence_references, novelty_assessment, falsification_condition,
                    heritage_eval, status, approval_notes, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(workspace_id, hypothesis_id) DO UPDATE SET
                    title=excluded.title,
                    relation_type=excluded.relation_type,
                    audience_id=excluded.audience_id,
                    audience_tension_ref=excluded.audience_tension_ref,
                    guest_id=excluded.guest_id,
                    guest_lived_proof_citation=excluded.guest_lived_proof_citation,
                    research_signal_id=excluded.research_signal_id,
                    sda_invariant=excluded.sda_invariant,
                    oblique_lens=excluded.oblique_lens,
                    bridge_statement=excluded.bridge_statement,
                    evidence_references=excluded.evidence_references,
                    novelty_assessment=excluded.novelty_assessment,
                    falsification_condition=excluded.falsification_condition,
                    heritage_eval=excluded.heritage_eval,
                    status=excluded.status,
                    approval_notes=excluded.approval_notes,
                    updated_at=excluded.updated_at;
            """, (
                hypothesis.workspace_id,
                hypothesis.hypothesis_id,
                hypothesis.title,
                hypothesis.relation_type,
                hypothesis.audience_id,
                hypothesis.audience_tension_ref,
                hypothesis.guest_id,
                hypothesis.guest_lived_proof_citation,
                hypothesis.research_signal_id,
                hypothesis.sda_invariant,
                json.dumps(hypothesis.oblique_lens) if hypothesis.oblique_lens else None,
                hypothesis.bridge_statement,
                json.dumps(hypothesis.evidence_references),
                json.dumps(hypothesis.novelty_assessment),
                json.dumps(hypothesis.falsification_condition),
                json.dumps(hypothesis.heritage_eval),
                hypothesis.status,
                hypothesis.approval_notes,
                hypothesis.created_at.isoformat(),
                hypothesis.updated_at.isoformat(),
            ))
        return hypothesis

    def get_hypothesis(self, workspace_id: str, hypothesis_id: str) -> Optional[CollisionHypothesisRecord]:
        """Fetch a Collision Hypothesis by ID."""
        cursor = self.conn.execute("""
            SELECT workspace_id, hypothesis_id, title, relation_type, audience_id,
                   audience_tension_ref, guest_id, guest_lived_proof_citation,
                   research_signal_id, sda_invariant, oblique_lens, bridge_statement,
                   evidence_references, novelty_assessment, falsification_condition,
                   heritage_eval, status, approval_notes, created_at, updated_at
            FROM collision_hypothesis
            WHERE workspace_id = ? AND hypothesis_id = ?;
        """, (workspace_id, hypothesis_id))
        row = cursor.fetchone()
        if not row:
            return None
        return CollisionHypothesisRecord(
            workspace_id=row[0],
            hypothesis_id=row[1],
            title=row[2],
            relation_type=row[3],
            audience_id=row[4],
            audience_tension_ref=row[5],
            guest_id=row[6],
            guest_lived_proof_citation=row[7],
            research_signal_id=row[8],
            sda_invariant=row[9],
            oblique_lens=json.loads(row[10]) if row[10] else None,
            bridge_statement=row[11],
            evidence_references=json.loads(row[12]),
            novelty_assessment=json.loads(row[13]),
            falsification_condition=json.loads(row[14]),
            heritage_eval=json.loads(row[15]),
            status=row[16],
            approval_notes=row[17],
            created_at=datetime.fromisoformat(row[18]),
            updated_at=datetime.fromisoformat(row[19]),
        )

    def list_hypotheses(
        self,
        workspace_id: str,
        relation_type: Optional[str] = None,
        status: Optional[str] = None,
        guest_id: Optional[str] = None,
        audience_id: Optional[str] = None,
    ) -> List[CollisionHypothesisRecord]:
        """Query Collision Hypotheses with optional filters."""
        query = """
            SELECT workspace_id, hypothesis_id, title, relation_type, audience_id,
                   audience_tension_ref, guest_id, guest_lived_proof_citation,
                   research_signal_id, sda_invariant, oblique_lens, bridge_statement,
                   evidence_references, novelty_assessment, falsification_condition,
                   heritage_eval, status, approval_notes, created_at, updated_at
            FROM collision_hypothesis
            WHERE workspace_id = ?
        """
        params: List[Any] = [workspace_id]
        if relation_type:
            query += " AND relation_type = ?"
            params.append(relation_type)
        if status:
            query += " AND status = ?"
            params.append(status)
        if guest_id:
            query += " AND guest_id = ?"
            params.append(guest_id)
        if audience_id:
            query += " AND audience_id = ?"
            params.append(audience_id)

        query += " ORDER BY created_at DESC;"
        cursor = self.conn.execute(query, params)
        results = []
        for row in cursor.fetchall():
            results.append(CollisionHypothesisRecord(
                workspace_id=row[0],
                hypothesis_id=row[1],
                title=row[2],
                relation_type=row[3],
                audience_id=row[4],
                audience_tension_ref=row[5],
                guest_id=row[6],
                guest_lived_proof_citation=row[7],
                research_signal_id=row[8],
                sda_invariant=row[9],
                oblique_lens=json.loads(row[10]) if row[10] else None,
                bridge_statement=row[11],
                evidence_references=json.loads(row[12]),
                novelty_assessment=json.loads(row[13]),
                falsification_condition=json.loads(row[14]),
                heritage_eval=json.loads(row[15]),
                status=row[16],
                approval_notes=row[17],
                created_at=datetime.fromisoformat(row[18]),
                updated_at=datetime.fromisoformat(row[19]),
            ))
        return results

    def update_hypothesis_status(
        self,
        workspace_id: str,
        hypothesis_id: str,
        status: str,
        approval_notes: Optional[str] = None,
    ) -> Optional[CollisionHypothesisRecord]:
        """Update approval/rejection status of a hypothesis without mutating underlying content."""
        now = datetime.now(timezone.utc)
        with self.conn:
            self.conn.execute("""
                UPDATE collision_hypothesis
                SET status = ?, approval_notes = ?, updated_at = ?
                WHERE workspace_id = ? AND hypothesis_id = ?;
            """, (status, approval_notes, now.isoformat(), workspace_id, hypothesis_id))
        return self.get_hypothesis(workspace_id, hypothesis_id)

    def store_portfolio(self, portfolio: CollisionHypothesisPortfolioRecord) -> CollisionHypothesisPortfolioRecord:
        """Upsert a Collision Hypothesis Portfolio record."""
        with self.conn:
            self.conn.execute("""
                INSERT INTO collision_hypothesis_portfolio (
                    workspace_id, portfolio_id, candidate_hypothesis_ids,
                    diversity_signature, status, selected_hypothesis_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(workspace_id, portfolio_id) DO UPDATE SET
                    candidate_hypothesis_ids=excluded.candidate_hypothesis_ids,
                    diversity_signature=excluded.diversity_signature,
                    status=excluded.status,
                    selected_hypothesis_id=excluded.selected_hypothesis_id;
            """, (
                portfolio.workspace_id,
                portfolio.portfolio_id,
                json.dumps(portfolio.candidate_hypothesis_ids),
                json.dumps(portfolio.diversity_signature),
                portfolio.status,
                portfolio.selected_hypothesis_id,
                portfolio.created_at.isoformat(),
            ))
        return portfolio

    def get_portfolio(self, workspace_id: str, portfolio_id: str) -> Optional[CollisionHypothesisPortfolioRecord]:
        """Fetch a portfolio by ID."""
        cursor = self.conn.execute("""
            SELECT workspace_id, portfolio_id, candidate_hypothesis_ids,
                   diversity_signature, status, selected_hypothesis_id, created_at
            FROM collision_hypothesis_portfolio
            WHERE workspace_id = ? AND portfolio_id = ?;
        """, (workspace_id, portfolio_id))
        row = cursor.fetchone()
        if not row:
            return None
        return CollisionHypothesisPortfolioRecord(
            workspace_id=row[0],
            portfolio_id=row[1],
            candidate_hypothesis_ids=json.loads(row[2]),
            diversity_signature=json.loads(row[3]),
            status=row[4],
            selected_hypothesis_id=row[5],
            created_at=datetime.fromisoformat(row[6]),
        )

    def list_portfolios(self, workspace_id: str) -> List[CollisionHypothesisPortfolioRecord]:
        """List all portfolios for a workspace."""
        cursor = self.conn.execute("""
            SELECT workspace_id, portfolio_id, candidate_hypothesis_ids,
                   diversity_signature, status, selected_hypothesis_id, created_at
            FROM collision_hypothesis_portfolio
            WHERE workspace_id = ?
            ORDER BY created_at DESC;
        """, (workspace_id,))
        results = []
        for row in cursor.fetchall():
            results.append(CollisionHypothesisPortfolioRecord(
                workspace_id=row[0],
                portfolio_id=row[1],
                candidate_hypothesis_ids=json.loads(row[2]),
                diversity_signature=json.loads(row[3]),
                status=row[4],
                selected_hypothesis_id=row[5],
                created_at=datetime.fromisoformat(row[6]),
            ))
        return results

    def update_portfolio_selection(
        self,
        workspace_id: str,
        portfolio_id: str,
        status: str,
        selected_hypothesis_id: Optional[str],
    ) -> Optional[CollisionHypothesisPortfolioRecord]:
        """Update status and selected hypothesis for a portfolio."""
        with self.conn:
            self.conn.execute("""
                UPDATE collision_hypothesis_portfolio
                SET status = ?, selected_hypothesis_id = ?
                WHERE workspace_id = ? AND portfolio_id = ?;
            """, (status, selected_hypothesis_id, workspace_id, portfolio_id))
        return self.get_portfolio(workspace_id, portfolio_id)

    def store_evaluation_receipt(self, receipt: HypothesisEvaluationReceiptRecord) -> HypothesisEvaluationReceiptRecord:
        """Store an immutable evaluation receipt."""
        with self.conn:
            self.conn.execute("""
                INSERT INTO hypothesis_evaluation_receipt (
                    workspace_id, receipt_id, portfolio_id, hypothesis_id,
                    evaluator_lane, decision, score_breakdown_micros,
                    gate_checks, signature, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(workspace_id, receipt_id) DO UPDATE SET
                    decision=excluded.decision,
                    score_breakdown_micros=excluded.score_breakdown_micros,
                    gate_checks=excluded.gate_checks,
                    signature=excluded.signature;
            """, (
                receipt.workspace_id,
                receipt.receipt_id,
                receipt.portfolio_id,
                receipt.hypothesis_id,
                receipt.evaluator_lane,
                receipt.decision,
                json.dumps(receipt.score_breakdown_micros),
                json.dumps(receipt.gate_checks),
                receipt.signature,
                receipt.created_at.isoformat(),
            ))
        return receipt

    def list_evaluation_receipts(
        self,
        workspace_id: str,
        portfolio_id: Optional[str] = None,
        hypothesis_id: Optional[str] = None,
    ) -> List[HypothesisEvaluationReceiptRecord]:
        """List evaluation receipts with optional filters."""
        query = """
            SELECT workspace_id, receipt_id, portfolio_id, hypothesis_id,
                   evaluator_lane, decision, score_breakdown_micros,
                   gate_checks, signature, created_at
            FROM hypothesis_evaluation_receipt
            WHERE workspace_id = ?
        """
        params: List[Any] = [workspace_id]
        if portfolio_id:
            query += " AND portfolio_id = ?"
            params.append(portfolio_id)
        if hypothesis_id:
            query += " AND hypothesis_id = ?"
            params.append(hypothesis_id)

        query += " ORDER BY created_at DESC;"
        cursor = self.conn.execute(query, params)
        results = []
        for row in cursor.fetchall():
            results.append(HypothesisEvaluationReceiptRecord(
                workspace_id=row[0],
                receipt_id=row[1],
                portfolio_id=row[2],
                hypothesis_id=row[3],
                evaluator_lane=row[4],
                decision=row[5],
                score_breakdown_micros=json.loads(row[6]),
                gate_checks=json.loads(row[7]),
                signature=row[8],
                created_at=datetime.fromisoformat(row[9]),
            ))
        return results
