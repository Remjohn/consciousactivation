"""
knowledge_cluster_signal_store.py
---------------------------------
Database persistence and projection store for Knowledge Clusters, Research Signals,
and Context Projections (CAE Phase 3 Mandate M31).

Supports multi-tenant workspace isolation, SQLite/PostgreSQL DDL execution,
integer basis points/micros scoring, and structured relational queries.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Data Models for Persistence & Retrieval
# ---------------------------------------------------------------------------

class KnowledgeClusterRecord(BaseModel):
    """Cluster of related canonical knowledge nodes."""
    cluster_id: str
    cluster_label: str
    theme: str
    cluster_type: str = "thematic"  # thematic, domain, emergent, structural
    coherence_score_micros: int = Field(..., ge=0, le=1000000)
    member_node_ids: List[str] = Field(default_factory=list)
    lineage_hashes: List[str] = Field(default_factory=list)
    status: str = "ACTIVE"  # ACTIVE, SUPERSEDED, RETRACTED, QUARANTINED
    rebuild_count: int = 0
    created_at_utc: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at_utc: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ProvenanceEntry(BaseModel):
    """Source-level provenance item."""
    origin_url: str
    root_domain: str
    platform: str
    observed_at_utc: str
    content_hash_sha256: str
    author_outlet: Optional[str] = None
    is_syndicated_copy: bool = False


class SourceMultiplicityInfo(BaseModel):
    """Tracks independent root domain corroboration."""
    raw_mention_count: int = Field(..., ge=1)
    unique_root_domain_count: int = Field(..., ge=1)
    independent_source_count: int = Field(..., ge=1)
    syndication_ratio_bps: int = Field(0, ge=0, le=10000)


class ResearchSignalRecord(BaseModel):
    """Temporal and contextual research signal grounded in knowledge clusters."""
    signal_id: str
    cluster_id: str
    topic: str
    entities: List[str] = Field(default_factory=list)
    status: str = "ACTIVE"  # ACTIVE, SUPERSEDED, RETRACTED, EXPIRED, QUARANTINED
    temporal_window_start_utc: str
    temporal_window_end_utc: str
    velocity_micros: int = Field(..., ge=0, le=1000000)
    acceleration_micros: int = Field(0, ge=0, le=1000000)
    novelty_micros: int = Field(500000, ge=0, le=1000000)
    divergence_micros: int = Field(0, ge=0, le=1000000)
    confidence_micros: int = Field(..., ge=0, le=1000000)
    evidence_excerpt: str
    source_multiplicity: SourceMultiplicityInfo
    primary_provenance: ProvenanceEntry
    corroborating_provenance: List[ProvenanceEntry] = Field(default_factory=list)
    created_at_utc: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at_utc: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ContextProjectionRecord(BaseModel):
    """Signal projected onto Guest DNA & Audience cognitive tension."""
    projection_id: str
    signal_id: str
    cluster_id: str
    guest_id: str
    audience_state_id: str
    activation_potential_micros: int = Field(..., ge=0, le=1000000)
    distribution_potential_micros: int = Field(..., ge=0, le=1000000)
    evidence_confidence_micros: int = Field(..., ge=0, le=1000000)
    composite_opportunity_score_micros: int = Field(..., ge=0, le=1000000)
    trigger_vector_refs: List[str] = Field(default_factory=list)
    audience_tension_refs: List[str] = Field(default_factory=list)
    hypothesis_readiness: bool = True
    created_at_utc: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at_utc: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Storage Engine
# ---------------------------------------------------------------------------

class KnowledgeClusterSignalStore:
    """Multi-tenant projection store for knowledge clusters, signals, and context projections."""

    def __init__(self, connection: Optional[sqlite3.Connection] = None):
        self._conn = connection or sqlite3.connect(":memory:", check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        with self._conn:
            self._conn.executescript("""
                CREATE TABLE IF NOT EXISTS knowledge_cluster (
                    workspace_id TEXT NOT NULL,
                    cluster_id TEXT NOT NULL,
                    cluster_label TEXT NOT NULL,
                    theme TEXT NOT NULL,
                    cluster_type TEXT NOT NULL,
                    coherence_score_micros INTEGER NOT NULL,
                    member_node_ids_json TEXT NOT NULL,
                    cluster_json TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'ACTIVE',
                    rebuild_count INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, cluster_id)
                );

                CREATE INDEX IF NOT EXISTS idx_kcluster_type
                    ON knowledge_cluster (workspace_id, cluster_type, status);

                CREATE TABLE IF NOT EXISTS research_signal (
                    workspace_id TEXT NOT NULL,
                    signal_id TEXT NOT NULL,
                    cluster_id TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'ACTIVE',
                    temporal_window_start TEXT NOT NULL,
                    temporal_window_end TEXT NOT NULL,
                    velocity_micros INTEGER NOT NULL,
                    acceleration_micros INTEGER NOT NULL,
                    novelty_micros INTEGER NOT NULL,
                    divergence_micros INTEGER NOT NULL,
                    confidence_micros INTEGER NOT NULL,
                    signal_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, signal_id)
                );

                CREATE INDEX IF NOT EXISTS idx_rsignal_cluster
                    ON research_signal (workspace_id, cluster_id, status);

                CREATE INDEX IF NOT EXISTS idx_rsignal_velocity
                    ON research_signal (workspace_id, velocity_micros DESC);

                CREATE TABLE IF NOT EXISTS context_projection (
                    workspace_id TEXT NOT NULL,
                    projection_id TEXT NOT NULL,
                    signal_id TEXT NOT NULL,
                    cluster_id TEXT NOT NULL,
                    guest_id TEXT NOT NULL,
                    audience_state_id TEXT NOT NULL,
                    activation_potential_micros INTEGER NOT NULL,
                    distribution_potential_micros INTEGER NOT NULL,
                    evidence_confidence_micros INTEGER NOT NULL,
                    composite_opportunity_score_micros INTEGER NOT NULL,
                    hypothesis_readiness INTEGER NOT NULL DEFAULT 1,
                    projection_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, projection_id)
                );

                CREATE INDEX IF NOT EXISTS idx_cproj_guest
                    ON context_projection (workspace_id, guest_id, composite_opportunity_score_micros DESC);

                CREATE INDEX IF NOT EXISTS idx_cproj_signal
                    ON context_projection (workspace_id, signal_id);
            """)

    # -----------------------------------------------------------------------
    # Cluster Operations
    # -----------------------------------------------------------------------

    def store_clusters(self, workspace_id: str, clusters: List[KnowledgeClusterRecord]) -> int:
        """Stores or updates knowledge clusters for a given workspace."""
        if not workspace_id:
            raise ValueError("workspace_id cannot be empty")
        now = datetime.now(timezone.utc).isoformat()
        count = 0
        with self._conn:
            for cl in clusters:
                # check existing
                cur = self._conn.execute(
                    "SELECT rebuild_count, created_at FROM knowledge_cluster WHERE workspace_id = ? AND cluster_id = ?",
                    (workspace_id, cl.cluster_id),
                )
                row = cur.fetchone()
                rebuild_count = (row["rebuild_count"] + 1) if row else cl.rebuild_count
                created_at = row["created_at"] if row else (cl.created_at_utc or now)

                cl_dict = cl.model_dump()
                cl_dict["rebuild_count"] = rebuild_count
                cl_dict["created_at_utc"] = created_at
                cl_dict["updated_at_utc"] = now

                self._conn.execute("""
                    INSERT INTO knowledge_cluster (
                        workspace_id, cluster_id, cluster_label, theme, cluster_type,
                        coherence_score_micros, member_node_ids_json, cluster_json,
                        status, rebuild_count, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT (workspace_id, cluster_id) DO UPDATE SET
                        cluster_label = excluded.cluster_label,
                        theme = excluded.theme,
                        cluster_type = excluded.cluster_type,
                        coherence_score_micros = excluded.coherence_score_micros,
                        member_node_ids_json = excluded.member_node_ids_json,
                        cluster_json = excluded.cluster_json,
                        status = excluded.status,
                        rebuild_count = excluded.rebuild_count,
                        updated_at = excluded.updated_at
                """, (
                    workspace_id,
                    cl.cluster_id,
                    cl.cluster_label,
                    cl.theme,
                    cl.cluster_type,
                    cl.coherence_score_micros,
                    json.dumps(cl.member_node_ids),
                    json.dumps(cl_dict),
                    cl.status,
                    rebuild_count,
                    created_at,
                    now,
                ))
                count += 1
        return count

    def get_cluster(self, workspace_id: str, cluster_id: str) -> Optional[KnowledgeClusterRecord]:
        """Retrieves a single cluster by ID with workspace isolation."""
        cur = self._conn.execute(
            "SELECT cluster_json FROM knowledge_cluster WHERE workspace_id = ? AND cluster_id = ?",
            (workspace_id, cluster_id),
        )
        row = cur.fetchone()
        if not row:
            return None
        return KnowledgeClusterRecord.model_validate_json(row["cluster_json"])

    def list_clusters(
        self,
        workspace_id: str,
        cluster_type: Optional[str] = None,
        status: str = "ACTIVE",
    ) -> List[KnowledgeClusterRecord]:
        """Lists clusters within a workspace filtered by type and status."""
        query = "SELECT cluster_json FROM knowledge_cluster WHERE workspace_id = ? AND status = ?"
        params: List[Any] = [workspace_id, status]
        if cluster_type:
            query += " AND cluster_type = ?"
            params.append(cluster_type)
        query += " ORDER BY coherence_score_micros DESC"
        cur = self._conn.execute(query, tuple(params))
        return [KnowledgeClusterRecord.model_validate_json(r["cluster_json"]) for r in cur.fetchall()]

    def get_clusters_for_node(self, workspace_id: str, node_id: str) -> List[KnowledgeClusterRecord]:
        """Finds all active clusters containing a given node ID."""
        cur = self._conn.execute(
            "SELECT cluster_json, member_node_ids_json FROM knowledge_cluster WHERE workspace_id = ? AND status = 'ACTIVE'",
            (workspace_id,),
        )
        results: List[KnowledgeClusterRecord] = []
        for row in cur.fetchall():
            member_ids = json.loads(row["member_node_ids_json"])
            if node_id in member_ids:
                results.append(KnowledgeClusterRecord.model_validate_json(row["cluster_json"]))
        return results

    def retract_cluster(self, workspace_id: str, cluster_id: str) -> bool:
        """Retracts a cluster and cascades retraction to related signals and projections."""
        now = datetime.now(timezone.utc).isoformat()
        with self._conn:
            cur = self._conn.execute(
                "UPDATE knowledge_cluster SET status = 'RETRACTED', updated_at = ? WHERE workspace_id = ? AND cluster_id = ?",
                (now, workspace_id, cluster_id),
            )
            if cur.rowcount == 0:
                return False
            # Cascade retraction to active signals
            self._conn.execute(
                "UPDATE research_signal SET status = 'RETRACTED', updated_at = ? WHERE workspace_id = ? AND cluster_id = ? AND status = 'ACTIVE'",
                (now, workspace_id, cluster_id),
            )
            return True

    # -----------------------------------------------------------------------
    # Signal Operations
    # -----------------------------------------------------------------------

    def store_signals(self, workspace_id: str, signals: List[ResearchSignalRecord]) -> int:
        """Stores or updates temporal research signals."""
        if not workspace_id:
            raise ValueError("workspace_id cannot be empty")
        now = datetime.now(timezone.utc).isoformat()
        count = 0
        with self._conn:
            for sig in signals:
                cur = self._conn.execute(
                    "SELECT created_at FROM research_signal WHERE workspace_id = ? AND signal_id = ?",
                    (workspace_id, sig.signal_id),
                )
                row = cur.fetchone()
                created_at = row["created_at"] if row else (sig.created_at_utc or now)

                sig_dict = sig.model_dump()
                sig_dict["created_at_utc"] = created_at
                sig_dict["updated_at_utc"] = now

                self._conn.execute("""
                    INSERT INTO research_signal (
                        workspace_id, signal_id, cluster_id, topic, status,
                        temporal_window_start, temporal_window_end, velocity_micros,
                        acceleration_micros, novelty_micros, divergence_micros,
                        confidence_micros, signal_json, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT (workspace_id, signal_id) DO UPDATE SET
                        cluster_id = excluded.cluster_id,
                        topic = excluded.topic,
                        status = excluded.status,
                        temporal_window_start = excluded.temporal_window_start,
                        temporal_window_end = excluded.temporal_window_end,
                        velocity_micros = excluded.velocity_micros,
                        acceleration_micros = excluded.acceleration_micros,
                        novelty_micros = excluded.novelty_micros,
                        divergence_micros = excluded.divergence_micros,
                        confidence_micros = excluded.confidence_micros,
                        signal_json = excluded.signal_json,
                        updated_at = excluded.updated_at
                """, (
                    workspace_id,
                    sig.signal_id,
                    sig.cluster_id,
                    sig.topic,
                    sig.status,
                    sig.temporal_window_start_utc,
                    sig.temporal_window_end_utc,
                    sig.velocity_micros,
                    sig.acceleration_micros,
                    sig.novelty_micros,
                    sig.divergence_micros,
                    sig.confidence_micros,
                    json.dumps(sig_dict),
                    created_at,
                    now,
                ))
                count += 1
        return count

    def get_signal(self, workspace_id: str, signal_id: str) -> Optional[ResearchSignalRecord]:
        """Retrieves a research signal by ID."""
        cur = self._conn.execute(
            "SELECT signal_json FROM research_signal WHERE workspace_id = ? AND signal_id = ?",
            (workspace_id, signal_id),
        )
        row = cur.fetchone()
        if not row:
            return None
        return ResearchSignalRecord.model_validate_json(row["signal_json"])

    def list_signals(
        self,
        workspace_id: str,
        cluster_id: Optional[str] = None,
        status: str = "ACTIVE",
        min_velocity_micros: int = 0,
    ) -> List[ResearchSignalRecord]:
        """Lists signals within a workspace matching criteria."""
        query = "SELECT signal_json FROM research_signal WHERE workspace_id = ? AND status = ? AND velocity_micros >= ?"
        params: List[Any] = [workspace_id, status, min_velocity_micros]
        if cluster_id:
            query += " AND cluster_id = ?"
            params.append(cluster_id)
        query += " ORDER BY velocity_micros DESC, confidence_micros DESC"
        cur = self._conn.execute(query, tuple(params))
        return [ResearchSignalRecord.model_validate_json(r["signal_json"]) for r in cur.fetchall()]

    def retract_signal(self, workspace_id: str, signal_id: str) -> bool:
        """Retracts an active research signal."""
        now = datetime.now(timezone.utc).isoformat()
        with self._conn:
            cur = self._conn.execute(
                "UPDATE research_signal SET status = 'RETRACTED', updated_at = ? WHERE workspace_id = ? AND signal_id = ?",
                (now, workspace_id, signal_id),
            )
            return cur.rowcount > 0

    # -----------------------------------------------------------------------
    # Context Projection Operations
    # -----------------------------------------------------------------------

    def store_context_projections(self, workspace_id: str, projections: List[ContextProjectionRecord]) -> int:
        """Stores or updates context projections."""
        if not workspace_id:
            raise ValueError("workspace_id cannot be empty")
        now = datetime.now(timezone.utc).isoformat()
        count = 0
        with self._conn:
            for cp in projections:
                cur = self._conn.execute(
                    "SELECT created_at FROM context_projection WHERE workspace_id = ? AND projection_id = ?",
                    (workspace_id, cp.projection_id),
                )
                row = cur.fetchone()
                created_at = row["created_at"] if row else (cp.created_at_utc or now)

                cp_dict = cp.model_dump()
                cp_dict["created_at_utc"] = created_at
                cp_dict["updated_at_utc"] = now

                self._conn.execute("""
                    INSERT INTO context_projection (
                        workspace_id, projection_id, signal_id, cluster_id,
                        guest_id, audience_state_id, activation_potential_micros,
                        distribution_potential_micros, evidence_confidence_micros,
                        composite_opportunity_score_micros, hypothesis_readiness,
                        projection_json, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT (workspace_id, projection_id) DO UPDATE SET
                        signal_id = excluded.signal_id,
                        cluster_id = excluded.cluster_id,
                        guest_id = excluded.guest_id,
                        audience_state_id = excluded.audience_state_id,
                        activation_potential_micros = excluded.activation_potential_micros,
                        distribution_potential_micros = excluded.distribution_potential_micros,
                        evidence_confidence_micros = excluded.evidence_confidence_micros,
                        composite_opportunity_score_micros = excluded.composite_opportunity_score_micros,
                        hypothesis_readiness = excluded.hypothesis_readiness,
                        projection_json = excluded.projection_json,
                        updated_at = excluded.updated_at
                """, (
                    workspace_id,
                    cp.projection_id,
                    cp.signal_id,
                    cp.cluster_id,
                    cp.guest_id,
                    cp.audience_state_id,
                    cp.activation_potential_micros,
                    cp.distribution_potential_micros,
                    cp.evidence_confidence_micros,
                    cp.composite_opportunity_score_micros,
                    1 if cp.hypothesis_readiness else 0,
                    json.dumps(cp_dict),
                    created_at,
                    now,
                ))
                count += 1
        return count

    def get_context_projection(self, workspace_id: str, projection_id: str) -> Optional[ContextProjectionRecord]:
        """Retrieves a context projection by ID."""
        cur = self._conn.execute(
            "SELECT projection_json FROM context_projection WHERE workspace_id = ? AND projection_id = ?",
            (workspace_id, projection_id),
        )
        row = cur.fetchone()
        if not row:
            return None
        return ContextProjectionRecord.model_validate_json(row["projection_json"])

    def list_context_projections(
        self,
        workspace_id: str,
        guest_id: Optional[str] = None,
        audience_state_id: Optional[str] = None,
        min_opportunity_score_micros: int = 0,
    ) -> List[ContextProjectionRecord]:
        """Lists context projections matching criteria."""
        query = "SELECT projection_json FROM context_projection WHERE workspace_id = ? AND composite_opportunity_score_micros >= ?"
        params: List[Any] = [workspace_id, min_opportunity_score_micros]
        if guest_id:
            query += " AND guest_id = ?"
            params.append(guest_id)
        if audience_state_id:
            query += " AND audience_state_id = ?"
            params.append(audience_state_id)
        query += " ORDER BY composite_opportunity_score_micros DESC"
        cur = self._conn.execute(query, tuple(params))
        return [ContextProjectionRecord.model_validate_json(r["projection_json"]) for r in cur.fetchall()]

    def list_top_content_opportunities(
        self,
        workspace_id: str,
        guest_id: str,
        limit: int = 10,
    ) -> List[ContextProjectionRecord]:
        """Retrieves top content opportunities for a guest above hard-gate threshold."""
        cur = self._conn.execute("""
            SELECT cp.projection_json
            FROM context_projection cp
            JOIN research_signal rs ON cp.workspace_id = rs.workspace_id AND cp.signal_id = rs.signal_id
            WHERE cp.workspace_id = ?
              AND cp.guest_id = ?
              AND cp.hypothesis_readiness = 1
              AND rs.status = 'ACTIVE'
            ORDER BY cp.composite_opportunity_score_micros DESC
            LIMIT ?
        """, (workspace_id, guest_id, limit))
        return [ContextProjectionRecord.model_validate_json(r["projection_json"]) for r in cur.fetchall()]
