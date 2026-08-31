"""Authoritative Supabase / PostgreSQL & SQLite Storage Projection for Curated Knowledge.

Governed by:
- 03_PHASE_3_INTELLIGENCE_AND_PROGRAMS/M30_canonical_knowledge_compiler_supabase_projection.md
- 00_CONTROL/20_PHASE3_CANONICALIZATION_MODEL.md
- 00_CONTROL/21_PHASE3_KNOWLEDGE_RUNTIME_CONTRACT.md
- 00_CONTROL/22_PHASE3_RESEARCH_RETRIEVAL_MATRIX.md

Implements typed persistence and retrieval over:
- knowledge_node
- knowledge_edge
- knowledge_projection
- knowledge_provenance_link
- knowledge_search_index

Ensures strict multi-tenant Workspace scoping, integer basis points scoring, and zero Redis dependency.
"""

from __future__ import annotations

from contextlib import closing
from dataclasses import dataclass, field
import json
from pathlib import Path
import re
import sqlite3
from typing import Any, Callable, Dict, List, Optional, Sequence, Union
from uuid import UUID

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.tenancy import CrossWorkspaceLeakError, TenancyError


def _normalize_workspace_id(workspace_id: Union[str, UUID]) -> str:
    return str(workspace_id).strip().lower()


def _tokenize(text: str) -> List[str]:
    return [tok for tok in re.split(r"[^\w]+", text.lower()) if tok]


class KnowledgeStorageError(RuntimeError):
    """Base error for knowledge projection storage."""
    pass


@dataclass(frozen=True, slots=True)
class ScoredKnowledgeMatch:
    node_id: str
    projection_id: str
    title: str
    summary: str
    category: str
    lifecycle_state: str
    authority_state: str
    total_score_micros: int
    exact_score_micros: int
    lexical_score_micros: int
    tag_score_micros: int
    graph_score_micros: int
    dense_score_micros: int
    content_sha256: str
    provenance_refs: List[Dict[str, str]] = field(default_factory=list)
    relationship_edges: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "projection_id": self.projection_id,
            "title": self.title,
            "summary": self.summary,
            "category": self.category,
            "lifecycle_state": self.lifecycle_state,
            "authority_state": self.authority_state,
            "total_score_micros": self.total_score_micros,
            "exact_score_micros": self.exact_score_micros,
            "lexical_score_micros": self.lexical_score_micros,
            "tag_score_micros": self.tag_score_micros,
            "graph_score_micros": self.graph_score_micros,
            "dense_score_micros": self.dense_score_micros,
            "content_sha256": self.content_sha256,
            "provenance_refs": self.provenance_refs,
            "relationship_edges": self.relationship_edges,
        }


class KnowledgeProjectionStore:
    """Authoritative storage adapter for knowledge nodes, edges, projections, and indices."""

    def __init__(self, db_path: Union[str, Path, None] = None, *, connection: Optional[sqlite3.Connection] = None):
        self._db_path = Path(db_path) if db_path and db_path != ":memory:" else None
        self._in_memory = (db_path == ":memory:" or db_path is None)
        self._shared_connection = connection
        if self._shared_connection is None and self._in_memory:
            self._shared_connection = sqlite3.connect(":memory:", check_same_thread=False)
            self._shared_connection.row_factory = sqlite3.Row
            self._init_schema(self._shared_connection)
        elif self._shared_connection is not None:
            self._shared_connection.row_factory = sqlite3.Row
            self._init_schema(self._shared_connection)
        elif self._db_path is not None:
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
            with closing(self._connect()) as conn:
                self._init_schema(conn)

    def _connect(self) -> sqlite3.Connection:
        if self._shared_connection is not None:
            return self._shared_connection
        conn = sqlite3.connect(self._db_path or ":memory:")
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_schema(self, conn: sqlite3.Connection) -> None:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS knowledge_nodes (
                workspace_id TEXT NOT NULL,
                node_id TEXT NOT NULL,
                canonical_label TEXT NOT NULL,
                category TEXT NOT NULL,
                definition TEXT NOT NULL,
                lifecycle_status TEXT NOT NULL,
                authority_class TEXT NOT NULL,
                lineage_sha256 TEXT NOT NULL,
                version INTEGER NOT NULL DEFAULT 1,
                supersedes_node_id TEXT,
                retraction_reason TEXT,
                node_payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (workspace_id, node_id)
            );

            CREATE TABLE IF NOT EXISTS knowledge_edges (
                workspace_id TEXT NOT NULL,
                edge_id TEXT NOT NULL,
                source_node_id TEXT NOT NULL,
                target_node_id TEXT NOT NULL,
                relation_type TEXT NOT NULL,
                confidence_score INTEGER NOT NULL DEFAULT 100,
                adjudicated INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                PRIMARY KEY (workspace_id, edge_id)
            );

            CREATE TABLE IF NOT EXISTS knowledge_projections (
                workspace_id TEXT NOT NULL,
                projection_id TEXT NOT NULL,
                node_id TEXT NOT NULL,
                source_kind TEXT NOT NULL,
                authority_state TEXT NOT NULL,
                lifecycle_state TEXT NOT NULL,
                title TEXT NOT NULL,
                summary TEXT NOT NULL,
                content_sha256 TEXT NOT NULL,
                projection_json TEXT NOT NULL,
                rebuild_count INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (workspace_id, projection_id)
            );

            CREATE TABLE IF NOT EXISTS knowledge_provenance_links (
                workspace_id TEXT NOT NULL,
                link_id TEXT NOT NULL,
                node_id TEXT NOT NULL,
                source_id TEXT NOT NULL,
                source_sha256 TEXT NOT NULL,
                created_at TEXT NOT NULL,
                PRIMARY KEY (workspace_id, link_id)
            );

            CREATE TABLE IF NOT EXISTS knowledge_search_indexes (
                workspace_id TEXT NOT NULL,
                index_id TEXT NOT NULL,
                node_id TEXT NOT NULL,
                tokens_text TEXT NOT NULL,
                exact_terms_text TEXT NOT NULL,
                category TEXT NOT NULL,
                created_at TEXT NOT NULL,
                PRIMARY KEY (workspace_id, index_id)
            );

            CREATE INDEX IF NOT EXISTS idx_kn_cat ON knowledge_nodes(workspace_id, category);
            CREATE INDEX IF NOT EXISTS idx_kn_status ON knowledge_nodes(workspace_id, lifecycle_status);
            CREATE INDEX IF NOT EXISTS idx_ke_src ON knowledge_edges(workspace_id, source_node_id);
            CREATE INDEX IF NOT EXISTS idx_ke_tgt ON knowledge_edges(workspace_id, target_node_id);
            CREATE INDEX IF NOT EXISTS idx_kp_node ON knowledge_projections(workspace_id, node_id);
            CREATE INDEX IF NOT EXISTS idx_kp_status ON knowledge_projections(workspace_id, lifecycle_state);
        """)

    # ------------------------------------------------------------------------
    # Persistence Operations
    # ------------------------------------------------------------------------

    def store_nodes(self, workspace_id: Union[str, UUID], nodes: Sequence[Dict[str, Any]]) -> int:
        ws_id = _normalize_workspace_id(workspace_id)
        now = utc_now_rfc3339()
        stored = 0
        conn = self._connect()
        try:
            with conn:
                for node in nodes:
                    node_id = str(node["node_id"])
                    canonical_label = str(node["canonical_label"])
                    category = str(node.get("category", "concept"))
                    definition = str(node.get("definition", ""))
                    lifecycle_status = str(node.get("lifecycle_status", "active"))
                    authority_class = str(node.get("authority_class", "derived_validated_knowledge"))
                    lineage_sha256 = str(node["lineage_sha256"])
                    version = int(node.get("version", 1))
                    supersedes_node_id = node.get("supersedes_node_id")
                    retraction_reason = node.get("retraction_reason")
                    payload_json = canonical_json_text(node)

                    conn.execute("""
                        INSERT INTO knowledge_nodes (
                            workspace_id, node_id, canonical_label, category, definition,
                            lifecycle_status, authority_class, lineage_sha256, version,
                            supersedes_node_id, retraction_reason, node_payload_json,
                            created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(workspace_id, node_id) DO UPDATE SET
                            canonical_label = excluded.canonical_label,
                            category = excluded.category,
                            definition = excluded.definition,
                            lifecycle_status = excluded.lifecycle_status,
                            authority_class = excluded.authority_class,
                            lineage_sha256 = excluded.lineage_sha256,
                            version = excluded.version,
                            supersedes_node_id = excluded.supersedes_node_id,
                            retraction_reason = excluded.retraction_reason,
                            node_payload_json = excluded.node_payload_json,
                            updated_at = excluded.updated_at
                    """, (
                        ws_id, node_id, canonical_label, category, definition,
                        lifecycle_status, authority_class, lineage_sha256, version,
                        supersedes_node_id, retraction_reason, payload_json,
                        now, now
                    ))
                    stored += 1
        finally:
            if self._shared_connection is None:
                conn.close()
        return stored

    def store_edges(self, workspace_id: Union[str, UUID], edges: Sequence[Dict[str, Any]]) -> int:
        ws_id = _normalize_workspace_id(workspace_id)
        now = utc_now_rfc3339()
        stored = 0
        conn = self._connect()
        try:
            with conn:
                for edge in edges:
                    edge_id = str(edge["edge_id"])
                    source_node_id = str(edge["source_node_id"])
                    target_node_id = str(edge["target_node_id"])
                    relation_type = str(edge["relation_type"])
                    confidence_score = int(edge.get("confidence_score", 100))
                    adjudicated = 1 if edge.get("adjudicated", False) else 0

                    conn.execute("""
                        INSERT INTO knowledge_edges (
                            workspace_id, edge_id, source_node_id, target_node_id,
                            relation_type, confidence_score, adjudicated, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(workspace_id, edge_id) DO UPDATE SET
                            relation_type = excluded.relation_type,
                            confidence_score = excluded.confidence_score,
                            adjudicated = excluded.adjudicated
                    """, (
                        ws_id, edge_id, source_node_id, target_node_id,
                        relation_type, confidence_score, adjudicated, now
                    ))
                    stored += 1
        finally:
            if self._shared_connection is None:
                conn.close()
        return stored

    def store_projections(self, workspace_id: Union[str, UUID], projections: Sequence[Dict[str, Any]]) -> int:
        ws_id = _normalize_workspace_id(workspace_id)
        now = utc_now_rfc3339()
        stored = 0
        conn = self._connect()
        try:
            with conn:
                for proj in projections:
                    proj_id = str(proj["projection_id"])
                    node_id = str(proj.get("node_id") or proj.get("object_ref", {}).get("object_id", ""))
                    source_kind = str(proj.get("source_kind", "research_knowledge"))
                    authority_state = str(proj.get("authority_state", "current"))
                    lifecycle_state = str(proj.get("lifecycle_state", "ACTIVE"))
                    title = str(proj["title"])
                    summary = str(proj["summary"])
                    content_sha256 = str(proj["content_sha256"])
                    proj_json = canonical_json_text(proj)

                    conn.execute("""
                        INSERT INTO knowledge_projections (
                            workspace_id, projection_id, node_id, source_kind,
                            authority_state, lifecycle_state, title, summary,
                            content_sha256, projection_json, rebuild_count,
                            created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?)
                        ON CONFLICT(workspace_id, projection_id) DO UPDATE SET
                            node_id = excluded.node_id,
                            source_kind = excluded.source_kind,
                            authority_state = excluded.authority_state,
                            lifecycle_state = excluded.lifecycle_state,
                            title = excluded.title,
                            summary = excluded.summary,
                            content_sha256 = excluded.content_sha256,
                            projection_json = excluded.projection_json,
                            rebuild_count = knowledge_projections.rebuild_count + 1,
                            updated_at = excluded.updated_at
                    """, (
                        ws_id, proj_id, node_id, source_kind,
                        authority_state, lifecycle_state, title, summary,
                        content_sha256, proj_json, now, now
                    ))
                    stored += 1
        finally:
            if self._shared_connection is None:
                conn.close()
        return stored

    def store_provenance_links(self, workspace_id: Union[str, UUID], links: Sequence[Dict[str, Any]]) -> int:
        ws_id = _normalize_workspace_id(workspace_id)
        now = utc_now_rfc3339()
        stored = 0
        conn = self._connect()
        try:
            with conn:
                for link in links:
                    link_id = str(link["link_id"])
                    node_id = str(link["node_id"])
                    source_id = str(link["source_id"])
                    source_sha256 = str(link["source_sha256"])

                    conn.execute("""
                        INSERT INTO knowledge_provenance_links (
                            workspace_id, link_id, node_id, source_id, source_sha256, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?)
                        ON CONFLICT(workspace_id, link_id) DO NOTHING
                    """, (ws_id, link_id, node_id, source_id, source_sha256, now))
                    stored += 1
        finally:
            if self._shared_connection is None:
                conn.close()
        return stored

    def store_search_indexes(self, workspace_id: Union[str, UUID], indexes: Sequence[Dict[str, Any]]) -> int:
        ws_id = _normalize_workspace_id(workspace_id)
        now = utc_now_rfc3339()
        stored = 0
        conn = self._connect()
        try:
            with conn:
                for idx in indexes:
                    index_id = str(idx["index_id"])
                    node_id = str(idx["node_id"])
                    tokens_text = str(idx["tokens_text"])
                    exact_terms_text = str(idx["exact_terms_text"])
                    category = str(idx.get("category", "concept"))

                    conn.execute("""
                        INSERT INTO knowledge_search_indexes (
                            workspace_id, index_id, node_id, tokens_text, exact_terms_text, category, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(workspace_id, index_id) DO UPDATE SET
                            tokens_text = excluded.tokens_text,
                            exact_terms_text = excluded.exact_terms_text,
                            category = excluded.category
                    """, (ws_id, index_id, node_id, tokens_text, exact_terms_text, category, now))
                    stored += 1
        finally:
            if self._shared_connection is None:
                conn.close()
        return stored

    # ------------------------------------------------------------------------
    # Structured SQL Queries
    # ------------------------------------------------------------------------

    def get_node(self, workspace_id: Union[str, UUID], node_id: str) -> Optional[Dict[str, Any]]:
        ws_id = _normalize_workspace_id(workspace_id)
        conn = self._connect()
        try:
            row = conn.execute(
                "SELECT node_payload_json FROM knowledge_nodes WHERE workspace_id = ? AND node_id = ?",
                (ws_id, str(node_id)),
            ).fetchone()
            if row is None:
                return None
            return json.loads(row["node_payload_json"])
        finally:
            if self._shared_connection is None:
                conn.close()

    def list_nodes(
        self,
        workspace_id: Union[str, UUID],
        *,
        category: Optional[str] = None,
        lifecycle_status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        ws_id = _normalize_workspace_id(workspace_id)
        query = "SELECT node_payload_json FROM knowledge_nodes WHERE workspace_id = ?"
        params: List[Any] = [ws_id]
        if category:
            query += " AND category = ?"
            params.append(category)
        if lifecycle_status:
            query += " AND lifecycle_status = ?"
            params.append(lifecycle_status)
        query += " ORDER BY canonical_label ASC"

        conn = self._connect()
        try:
            rows = conn.execute(query, params).fetchall()
            return [json.loads(r["node_payload_json"]) for r in rows]
        finally:
            if self._shared_connection is None:
                conn.close()

    def get_projection(self, workspace_id: Union[str, UUID], projection_id: str) -> Optional[Dict[str, Any]]:
        ws_id = _normalize_workspace_id(workspace_id)
        conn = self._connect()
        try:
            row = conn.execute(
                "SELECT projection_json, rebuild_count FROM knowledge_projections WHERE workspace_id = ? AND projection_id = ?",
                (ws_id, str(projection_id)),
            ).fetchone()
            if row is None:
                return None
            data = json.loads(row["projection_json"])
            data["rebuild_count"] = row["rebuild_count"]
            return data
        finally:
            if self._shared_connection is None:
                conn.close()

    def get_projection_by_node(self, workspace_id: Union[str, UUID], node_id: str) -> Optional[Dict[str, Any]]:
        ws_id = _normalize_workspace_id(workspace_id)
        conn = self._connect()
        try:
            row = conn.execute(
                "SELECT projection_json, rebuild_count FROM knowledge_projections WHERE workspace_id = ? AND node_id = ?",
                (ws_id, str(node_id)),
            ).fetchone()
            if row is None:
                return None
            data = json.loads(row["projection_json"])
            data["rebuild_count"] = row["rebuild_count"]
            return data
        finally:
            if self._shared_connection is None:
                conn.close()

    def list_projections(
        self,
        workspace_id: Union[str, UUID],
        *,
        lifecycle_state: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        ws_id = _normalize_workspace_id(workspace_id)
        query = "SELECT projection_json FROM knowledge_projections WHERE workspace_id = ?"
        params: List[Any] = [ws_id]
        if lifecycle_state:
            query += " AND lifecycle_state = ?"
            params.append(lifecycle_state)
        query += " ORDER BY title ASC"

        conn = self._connect()
        try:
            rows = conn.execute(query, params).fetchall()
            return [json.loads(r["projection_json"]) for r in rows]
        finally:
            if self._shared_connection is None:
                conn.close()

    def get_edges_for_node(
        self,
        workspace_id: Union[str, UUID],
        node_id: str,
        *,
        relation_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        ws_id = _normalize_workspace_id(workspace_id)
        query = "SELECT * FROM knowledge_edges WHERE workspace_id = ? AND (source_node_id = ? OR target_node_id = ?)"
        params: List[Any] = [ws_id, str(node_id), str(node_id)]
        if relation_type:
            query += " AND relation_type = ?"
            params.append(relation_type)

        conn = self._connect()
        try:
            rows = conn.execute(query, params).fetchall()
            return [dict(r) for r in rows]
        finally:
            if self._shared_connection is None:
                conn.close()

    def get_provenance_for_node(self, workspace_id: Union[str, UUID], node_id: str) -> List[Dict[str, Any]]:
        ws_id = _normalize_workspace_id(workspace_id)
        conn = self._connect()
        try:
            rows = conn.execute(
                "SELECT source_id, source_sha256, created_at FROM knowledge_provenance_links WHERE workspace_id = ? AND node_id = ?",
                (ws_id, str(node_id)),
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            if self._shared_connection is None:
                conn.close()

    # ------------------------------------------------------------------------
    # Multi-Modal Knowledge Retrieval (SQL + Lexical + Graph + Dense Adapter)
    # ------------------------------------------------------------------------

    def search_knowledge(
        self,
        workspace_id: Union[str, UUID],
        query: str,
        *,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        lifecycle_state: str = "ACTIVE",
        dense_adapter_cb: Optional[Callable[[List[str], str], Dict[str, int]]] = None,
        limit: int = 10,
    ) -> List[ScoredKnowledgeMatch]:
        ws_id = _normalize_workspace_id(workspace_id)
        query_text = (query or "").strip().lower()
        query_tokens = set(_tokenize(query_text))

        conn = self._connect()
        try:
            sql = """
                SELECT p.projection_json, p.content_sha256, i.tokens_text, i.exact_terms_text, i.category
                FROM knowledge_projections p
                JOIN knowledge_search_indexes i ON p.workspace_id = i.workspace_id AND p.node_id = i.node_id
                WHERE p.workspace_id = ? AND p.lifecycle_state = ?
            """
            params: List[Any] = [ws_id, lifecycle_state]
            if category:
                sql += " AND i.category = ?"
                params.append(category)

            rows = conn.execute(sql, params).fetchall()
            if not rows:
                return []

            candidate_records = []
            candidate_node_ids = []
            for row in rows:
                proj = json.loads(row["projection_json"])
                node_id = proj.get("node_id") or proj.get("object_ref", {}).get("object_id", "")
                tokens = set(_tokenize(row["tokens_text"]))
                exact_terms = row["exact_terms_text"].lower().split("|")
                candidate_records.append({
                    "proj": proj,
                    "node_id": node_id,
                    "content_sha256": row["content_sha256"],
                    "tokens": tokens,
                    "exact_terms": exact_terms,
                    "category": row["category"],
                })
                candidate_node_ids.append(node_id)

            # Optional Dense Adapter scoring
            dense_scores_micros: Dict[str, int] = {}
            if dense_adapter_cb is not None and candidate_node_ids:
                try:
                    dense_scores_micros = dense_adapter_cb(candidate_node_ids, query)
                except Exception:
                    dense_scores_micros = {}

            matches: List[ScoredKnowledgeMatch] = []
            for cand in candidate_records:
                proj = cand["proj"]
                node_id = cand["node_id"]
                title = proj.get("title", "")
                summary = proj.get("summary", "")
                cand_tags = set(proj.get("tags", []))

                # Exact Match Scoring (up to 400,000 micros)
                exact_score_micros = 0
                title_lower = title.lower()
                if query_text and query_text == title_lower:
                    exact_score_micros = 400_000
                elif query_text and query_text in title_lower:
                    exact_score_micros = 250_000
                elif any(query_text == term for term in cand["exact_terms"] if term):
                    exact_score_micros = 300_000

                # Lexical Token Overlap Scoring (up to 300,000 micros)
                lexical_score_micros = 0
                if query_tokens:
                    token_intersection = query_tokens.intersection(cand["tokens"])
                    if token_intersection:
                        lexical_score_micros = int((len(token_intersection) / len(query_tokens)) * 300_000)

                # Tag Overlap Scoring (up to 150,000 micros)
                tag_score_micros = 0
                if tags and cand_tags:
                    tag_query_set = {t.lower() for t in tags}
                    tag_overlap = tag_query_set.intersection({t.lower() for t in cand_tags})
                    if tag_overlap:
                        tag_score_micros = int((len(tag_overlap) / len(tag_query_set)) * 150_000)

                # Graph relationship boost (up to 50,000 micros if connected)
                rel_edges = proj.get("relationship_edges", [])
                graph_score_micros = min(50_000, len(rel_edges) * 10_000)

                # Dense adapter score (up to 100,000 micros)
                dense_score_micros = dense_scores_micros.get(node_id, 0)
                dense_score_micros = max(0, min(100_000, dense_score_micros))

                total_score_micros = (
                    exact_score_micros
                    + lexical_score_micros
                    + tag_score_micros
                    + graph_score_micros
                    + dense_score_micros
                )

                # Only include if there is some positive signal or empty query was passed
                if total_score_micros > 0 or not query_text:
                    evidence_refs = proj.get("evidence_refs", [])
                    matches.append(
                        ScoredKnowledgeMatch(
                            node_id=node_id,
                            projection_id=proj.get("projection_id", f"proj_{node_id}"),
                            title=title,
                            summary=summary,
                            category=cand["category"],
                            lifecycle_state=proj.get("lifecycle_state", "ACTIVE"),
                            authority_state=proj.get("authority_state", "current"),
                            total_score_micros=total_score_micros,
                            exact_score_micros=exact_score_micros,
                            lexical_score_micros=lexical_score_micros,
                            tag_score_micros=tag_score_micros,
                            graph_score_micros=graph_score_micros,
                            dense_score_micros=dense_score_micros,
                            content_sha256=cand["content_sha256"],
                            provenance_refs=[{"source_id": r.get("object_id", ""), "sha256": r.get("sha256", "")} for r in evidence_refs],
                            relationship_edges=rel_edges,
                        )
                    )

            matches.sort(key=lambda m: (-m.total_score_micros, m.title))
            return matches[:limit]
        finally:
            if self._shared_connection is None:
                conn.close()
