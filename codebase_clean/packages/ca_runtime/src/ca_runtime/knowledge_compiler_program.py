"""Phase 3 Mandate M30: Canonical Knowledge Compiler + Supabase Projection Program Coordinator.

Governed by:
- 03_PHASE_3_INTELLIGENCE_AND_PROGRAMS/M30_canonical_knowledge_compiler_supabase_projection.md
- 00_CONTROL/20_PHASE3_CANONICALIZATION_MODEL.md
- 00_CONTROL/21_PHASE3_KNOWLEDGE_RUNTIME_CONTRACT.md
- 00_CONTROL/22_PHASE3_RESEARCH_RETRIEVAL_MATRIX.md
- 00_CONTROL/24_PHASE3_PROGRAM_STATE_HOOKS_MATRIX.md

Coordinates compilation of curated canonical knowledge nodes and OKF bundles into authoritative
Supabase / PostgreSQL runtime structures while enforcing:
- Four distinct Authority Lanes (HUNTER, ANALYST, COMPOSER, COMMANDER).
- Idempotent projection rebuilds preserving source identity and cryptographic lineage.
- Strict multi-tenant Workspace boundary isolation.
- Float-free integer basis points scoring.
- Zero Redis dependency for canonical operational state.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.knowledge_projection_store import (
    KnowledgeProjectionStore,
    ScoredKnowledgeMatch,
    _normalize_workspace_id,
    _tokenize,
)
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_state_runtime import (
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
    ProgramStateMachineDefinition,
    ProgramTransitionBlockedError,
    UniversalProgramStateRuntime,
    get_canonical_knowledge_compiler_state_machine,
)
from ca_runtime.research_canonicalization_program import (
    CanonicalKnowledgeNode,
    CanonicalRelationship,
    CanonicalRelationshipType,
    OKFDocument,
    OKFKnowledgeBundle,
)
from ca_runtime.tenancy import (
    CrossWorkspaceLeakError,
    TenancyError,
    require_current_tenant_context,
)


# ----------------------------------------------------------------------------
# Typed Error Taxonomy
# ----------------------------------------------------------------------------

class KnowledgeCompilerProgramError(TenancyError):
    """Base error for knowledge compiler operations."""
    pass


class InvalidKnowledgeNodeError(KnowledgeCompilerProgramError):
    """Raised when a knowledge node fails structural or authority validation."""
    pass


class ProjectionCompilationError(KnowledgeCompilerProgramError):
    """Raised when knowledge projection compilation fails contract validation."""
    pass


class ProvenanceLineageBrokenError(KnowledgeCompilerProgramError):
    """Raised when knowledge projection fails to preserve source provenance hashes."""
    pass


class CrossWorkspaceProjectionError(KnowledgeCompilerProgramError):
    """Raised when projection or query violates workspace tenancy boundaries."""
    pass


class UnauthorizedKnowledgeCompilerLaneError(KnowledgeCompilerProgramError):
    """Raised when an operation is executed on an unauthorized authority lane."""
    pass


# ----------------------------------------------------------------------------
# Domain Models (Pydantic V2)
# ----------------------------------------------------------------------------

class CompiledKnowledgeProjection(BaseModel):
    """Authoritative projection record conforming to knowledge_projection.schema.json."""
    projection_id: str = Field(..., min_length=1)
    object_ref: Dict[str, str] = Field(..., description="Canonical reference: object_id, version, sha256")
    source_kind: str = Field(default="research_knowledge", min_length=1)
    authority_state: str = Field(default="current", min_length=1)
    lifecycle_state: str = Field(default="ACTIVE", min_length=1)
    title: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=1)
    category_ids: List[str] = Field(default_factory=list)
    format_profile_ids: List[str] = Field(default_factory=list)
    role_ids: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    relationship_edges: List[Dict[str, str]] = Field(default_factory=list)
    evidence_refs: List[Dict[str, str]] = Field(default_factory=list)
    reaction_receipt_refs: List[Dict[str, str]] = Field(default_factory=list)
    expression_moment_refs: List[Dict[str, str]] = Field(default_factory=list)
    contradicts_ids: List[str] = Field(default_factory=list)
    supersedes_ids: List[str] = Field(default_factory=list)
    failed_alternative: bool = Field(default=False)
    evidence_quality_micros: int = Field(default=1_000_000, ge=0)
    permitted_action_ids: List[str] = Field(default_factory=list)
    content_sha256: str = Field(..., min_length=64, max_length=64)


class CompiledSearchIndex(BaseModel):
    """Search index payload for lexical and exact multi-predicate retrieval."""
    index_id: str = Field(..., min_length=1)
    node_id: str = Field(..., min_length=1)
    tokens_text: str = Field(...)
    exact_terms_text: str = Field(...)
    category: str = Field(default="concept")


class KnowledgeCompilationReceipt(BaseModel):
    """Cryptographic audit receipt for knowledge compiler projection operations."""
    receipt_id: str = Field(..., min_length=1)
    workspace_id: UUID
    program_id: str = Field(default="knowledge_compiler_program")
    program_version: str = Field(default="1.0.0")
    operation: str = Field(..., min_length=1)
    nodes_count: int = Field(default=0, ge=0)
    projections_count: int = Field(default=0, ge=0)
    edges_count: int = Field(default=0, ge=0)
    rebuild_count: int = Field(default=0, ge=0)
    timestamp_utc: str = Field(..., min_length=1)
    receipt_sha256: str = Field(..., min_length=64, max_length=64)


class KnowledgeCompilerSnapshot(BaseModel):
    """Strongly-typed snapshot of the knowledge compiler program state."""
    workspace_id: UUID
    status: str
    current_state: str
    nodes_count: int
    projections_count: int
    indices_count: int
    last_rebuild_at_utc: Optional[str] = None
    receipt_count: int


# ----------------------------------------------------------------------------
# Knowledge Compiler Coordinator
# ----------------------------------------------------------------------------

class KnowledgeCompilerProgramCoordinator:
    """Orchestrates ingestion, compilation, indexing, and Supabase projection of canonical knowledge."""

    PROGRAM_ID = "knowledge_compiler_program"
    PROGRAM_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        runtime: UniversalProgramStateRuntime,
        store: Optional[KnowledgeProjectionStore] = None,
    ):
        self.runtime = runtime
        self.store = store or KnowledgeProjectionStore(":memory:")
        self._ensure_state_machine_registered()
        self._aggregate_ids: Dict[str, str] = {}
        self._in_memory_nodes: Dict[str, Dict[str, Dict[str, Any]]] = {}
        self._in_memory_projections: Dict[str, Dict[str, CompiledKnowledgeProjection]] = {}
        self._in_memory_indices: Dict[str, Dict[str, CompiledSearchIndex]] = {}
        self._in_memory_receipts: Dict[str, List[KnowledgeCompilationReceipt]] = {}
        self._rebuild_counters: Dict[str, int] = {}

    def _ensure_state_machine_registered(self) -> None:
        try:
            self.runtime.register_state_machine(get_canonical_knowledge_compiler_state_machine())
        except Exception:
            pass

    def _get_or_create_aggregate(self, workspace_id: UUID, actor_id: str = "usr_lead_commander") -> ProgramStateAggregate:
        ws_key = _normalize_workspace_id(workspace_id)
        agg_id = self._aggregate_ids.get(ws_key)
        if agg_id:
            try:
                return self.runtime.get_aggregate(agg_id)
            except Exception:
                pass

        agg = self.runtime.initialize_program_state(
            program_id=self.PROGRAM_ID,
            workspace_id=workspace_id,
            actor_id=actor_id,
            initial_data={
                "nodes": {},
                "projections": {},
                "indices": {},
                "receipts": [],
            },
            context_claims=[
                "workspace_active",
                "nodes_verified",
                "nodes_ingested",
                "projections_compiled",
                "search_index_built",
                "rebuild_authorized",
                "operator_authorized",
            ],
        )
        self._aggregate_ids[ws_key] = agg.aggregate_id
        return agg

    # ------------------------------------------------------------------------
    # Multi-Lane Operations
    # ------------------------------------------------------------------------

    def initialize_session(
        self,
        workspace_id: Union[str, UUID],
        *,
        actor_id: str = "usr_lead_commander",
    ) -> KnowledgeCompilerSnapshot:
        """Initializes a new knowledge compiler program session."""
        ws_uuid = UUID(str(workspace_id))
        ws_key = _normalize_workspace_id(ws_uuid)
        agg = self._get_or_create_aggregate(ws_uuid, actor_id=actor_id)
        self._in_memory_nodes.setdefault(ws_key, {})
        self._in_memory_projections.setdefault(ws_key, {})
        self._in_memory_indices.setdefault(ws_key, {})
        self._in_memory_receipts.setdefault(ws_key, [])
        self._rebuild_counters.setdefault(ws_key, 0)
        return self.get_snapshot(ws_uuid)

    def ingest_nodes(
        self,
        workspace_id: Union[str, UUID],
        nodes: Sequence[Union[CanonicalKnowledgeNode, Dict[str, Any]]],
        *,
        actor_id: str = "usr_hunter_lead",
        caller_lane: AuthorityLane = AuthorityLane.HUNTER,
    ) -> KnowledgeCompilerSnapshot:
        """Ingests validated canonical knowledge nodes into the compiler session (HUNTER lane)."""
        if caller_lane != AuthorityLane.HUNTER:
            raise UnauthorizedKnowledgeCompilerLaneError(
                f"ingest_nodes must execute on HUNTER lane, observed {caller_lane.name}"
            )

        ws_uuid = UUID(str(workspace_id))
        ws_key = _normalize_workspace_id(ws_uuid)
        agg = self._get_or_create_aggregate(ws_uuid, actor_id=actor_id)

        if not nodes:
            raise InvalidKnowledgeNodeError("Cannot ingest empty node sequence")

        nodes_dict: Dict[str, Dict[str, Any]] = {}
        for item in nodes:
            if isinstance(item, CanonicalKnowledgeNode):
                node_data = item.model_dump(mode="json")
            elif isinstance(item, dict):
                node_data = dict(item)
            else:
                raise InvalidKnowledgeNodeError(f"Unsupported node type: {type(item)}")

            node_id = node_data.get("node_id")
            if not node_id:
                raise InvalidKnowledgeNodeError("Knowledge node missing node_id")
            if not node_data.get("lineage_sha256"):
                raise ProvenanceLineageBrokenError(f"Node {node_id} missing lineage_sha256")
            if not node_data.get("source_evidence_hashes") and not node_data.get("source_record_refs"):
                raise ProvenanceLineageBrokenError(f"Node {node_id} has zero source provenance references")

            nodes_dict[node_id] = node_data

        trans_name = "ingest_nodes" if agg.current_state == "INITIAL" else "reingest_nodes"
        self.runtime.execute_transition(
            aggregate_id=agg.aggregate_id,
            transition_name=trans_name,
            actor_id=actor_id,
            actor_lane=caller_lane,
            context_claims=["workspace_active", "nodes_verified"],
            state_updates={
                "nodes_count": len(nodes_dict),
                "node_ids": list(nodes_dict.keys()),
            },
        )

        self._in_memory_nodes[ws_key] = nodes_dict
        return self.get_snapshot(ws_uuid)

    def compile_projections(
        self,
        workspace_id: Union[str, UUID],
        *,
        actor_id: str = "usr_composer_lead",
        caller_lane: AuthorityLane = AuthorityLane.COMPOSER,
    ) -> KnowledgeCompilerSnapshot:
        """Compiles canonical knowledge nodes into structured query projections (COMPOSER lane)."""
        if caller_lane != AuthorityLane.COMPOSER:
            raise UnauthorizedKnowledgeCompilerLaneError(
                f"compile_projections must execute on COMPOSER lane, observed {caller_lane.name}"
            )

        ws_uuid = UUID(str(workspace_id))
        ws_key = _normalize_workspace_id(ws_uuid)
        agg = self._get_or_create_aggregate(ws_uuid, actor_id=actor_id)
        nodes = self._in_memory_nodes.get(ws_key, {})

        if not nodes:
            raise ProjectionCompilationError("No ingested nodes found to compile")

        projections: Dict[str, CompiledKnowledgeProjection] = {}
        for node_id, node in nodes.items():
            canonical_label = node.get("canonical_label", "")
            definition = node.get("definition", "")
            category = node.get("category", "concept")
            lifecycle_status = node.get("lifecycle_status", "active")
            version = str(node.get("version", "1"))
            lineage_sha = node.get("lineage_sha256", "")

            # Map typed relationships
            edges = []
            contradicts_ids = []
            supersedes_ids = []
            if node.get("supersedes_node_id"):
                supersedes_ids.append(node["supersedes_node_id"])

            typed_edges_raw = node.get("typed_edges", {})
            if isinstance(typed_edges_raw, dict):
                for rel_type, targets in typed_edges_raw.items():
                    rel_type_str = str(rel_type.value) if hasattr(rel_type, "value") else str(rel_type)
                    for tgt in targets:
                        edges.append({"relation_type": rel_type_str, "target_id": str(tgt)})
                        if rel_type_str in ("CONTRADICTORY", "CONTRADICTS"):
                            contradicts_ids.append(str(tgt))
                        elif rel_type_str == "SUPERSEDES":
                            supersedes_ids.append(str(tgt))
            elif isinstance(typed_edges_raw, list):
                for edge in typed_edges_raw:
                    if isinstance(edge, dict):
                        rel_type = edge.get("rel_type") or edge.get("relation_type", "RELATED")
                        tgt = edge.get("target_id") or edge.get("target_node_id", "")
                        rel_type_str = str(rel_type.value) if hasattr(rel_type, "value") else str(rel_type)
                        edges.append({"relation_type": rel_type_str, "target_id": str(tgt)})
                        if rel_type_str in ("CONTRADICTORY", "CONTRADICTS"):
                            contradicts_ids.append(str(tgt))
                        elif rel_type_str == "SUPERSEDES":
                            supersedes_ids.append(str(tgt))

            # Map evidence refs
            evidence_refs = []
            srefs = node.get("source_record_refs", [])
            shashes = node.get("source_evidence_hashes", [])
            for i, sref in enumerate(srefs):
                if isinstance(shashes, list) and i < len(shashes):
                    sha = shashes[i]
                elif isinstance(shashes, dict):
                    sha = shashes.get(str(sref), lineage_sha)
                else:
                    sha = lineage_sha
                evidence_refs.append({
                    "object_id": str(sref),
                    "version": "1",
                    "sha256": sha,
                })

            # Tags compilation
            tags = [category, f"status:{lifecycle_status}"]
            for alias in node.get("aliases", []):
                tags.append(alias.lower())

            # Deterministic projection payload for SHA computation
            proj_dict = {
                "projection_id": f"proj_{node_id}",
                "object_ref": {
                    "object_id": node_id,
                    "version": version,
                    "sha256": lineage_sha,
                },
                "source_kind": "research_knowledge",
                "authority_state": "current",
                "lifecycle_state": "ACTIVE" if lifecycle_status == "active" else lifecycle_status.upper(),
                "title": canonical_label,
                "summary": definition,
                "category_ids": [category],
                "format_profile_ids": ["portable_activative_v1"],
                "role_ids": ["curated_knowledge_projection"],
                "tags": sorted(list(set(tags))),
                "relationship_edges": edges,
                "evidence_refs": evidence_refs,
                "reaction_receipt_refs": [],
                "expression_moment_refs": [],
                "contradicts_ids": sorted(list(set(contradicts_ids))),
                "supersedes_ids": sorted(list(set(supersedes_ids))),
                "failed_alternative": False,
                "evidence_quality_micros": 1_000_000,
                "permitted_action_ids": ["read", "retrieve", "link"],
            }
            content_sha = canonical_sha256(proj_dict)
            proj_dict["content_sha256"] = content_sha

            projections[node_id] = CompiledKnowledgeProjection(**proj_dict)

        trans_name = "compile_projections" if agg.current_state == "KNOWLEDGE_INGESTED" else "rebuild_projections"
        self.runtime.execute_transition(
            aggregate_id=agg.aggregate_id,
            transition_name=trans_name,
            actor_id=actor_id,
            actor_lane=caller_lane,
            context_claims=["workspace_active", "nodes_ingested", "rebuild_authorized"],
            state_updates={
                "projections_count": len(projections),
                "compiled_node_ids": list(projections.keys()),
            },
        )

        self._in_memory_projections[ws_key] = projections
        return self.get_snapshot(ws_uuid)

    def build_search_index(
        self,
        workspace_id: Union[str, UUID],
        *,
        actor_id: str = "usr_analyst_lead",
        caller_lane: AuthorityLane = AuthorityLane.ANALYST,
    ) -> KnowledgeCompilerSnapshot:
        """Builds lexical and exact match search index payloads (ANALYST lane)."""
        if caller_lane != AuthorityLane.ANALYST:
            raise UnauthorizedKnowledgeCompilerLaneError(
                f"build_search_index must execute on ANALYST lane, observed {caller_lane.name}"
            )

        ws_uuid = UUID(str(workspace_id))
        ws_key = _normalize_workspace_id(ws_uuid)
        agg = self._get_or_create_aggregate(ws_uuid, actor_id=actor_id)
        nodes = self._in_memory_nodes.get(ws_key, {})
        projections = self._in_memory_projections.get(ws_key, {})

        if not projections:
            raise ProjectionCompilationError("Cannot build search index before projections are compiled")

        indices: Dict[str, CompiledSearchIndex] = {}
        for node_id, proj in projections.items():
            node = nodes.get(node_id, {})
            tokens: Set[str] = set()
            tokens.update(_tokenize(proj.title))
            tokens.update(_tokenize(proj.summary))
            for t in proj.tags:
                tokens.update(_tokenize(t))
            for alias in node.get("aliases", []):
                tokens.update(_tokenize(alias))

            exact_terms = [proj.title.lower()]
            for alias in node.get("aliases", []):
                exact_terms.append(alias.lower())

            idx = CompiledSearchIndex(
                index_id=f"idx_{node_id}",
                node_id=node_id,
                tokens_text=" ".join(sorted(tokens)),
                exact_terms_text="|".join(sorted(list(set(exact_terms)))),
                category=node.get("category", "concept"),
            )
            indices[node_id] = idx

        trans_name = "build_search_index" if agg.current_state == "PROJECTIONS_COMPILED" else "rebuild_index"
        self.runtime.execute_transition(
            aggregate_id=agg.aggregate_id,
            transition_name=trans_name,
            actor_id=actor_id,
            actor_lane=caller_lane,
            context_claims=["workspace_active", "projections_compiled", "rebuild_authorized"],
            state_updates={
                "indices_count": len(indices),
                "indexed_node_ids": list(indices.keys()),
            },
        )

        self._in_memory_indices[ws_key] = indices
        return self.get_snapshot(ws_uuid)

    def project_to_database(
        self,
        workspace_id: Union[str, UUID],
        *,
        actor_id: str = "usr_lead_commander",
        caller_lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> KnowledgeCompilationReceipt:
        """Projects compiled knowledge structures to the operational database store (COMMANDER lane)."""
        if caller_lane != AuthorityLane.COMMANDER:
            raise UnauthorizedKnowledgeCompilerLaneError(
                f"project_to_database must execute on COMMANDER lane, observed {caller_lane.name}"
            )

        ws_uuid = UUID(str(workspace_id))
        ws_key = _normalize_workspace_id(ws_uuid)
        agg = self._get_or_create_aggregate(ws_uuid, actor_id=actor_id)

        nodes = self._in_memory_nodes.get(ws_key, {})
        projections = self._in_memory_projections.get(ws_key, {})
        indices = self._in_memory_indices.get(ws_key, {})

        if not projections or not indices:
            raise ProjectionCompilationError("Projections and search indices must be compiled before projection to database")

        # 1. Store nodes
        node_records = list(nodes.values())
        self.store.store_nodes(ws_uuid, node_records)

        # 2. Store edges
        edge_records = []
        for node in node_records:
            src = node["node_id"]
            typed_edges_raw = node.get("typed_edges", {})
            if isinstance(typed_edges_raw, dict):
                for rel_type, targets in typed_edges_raw.items():
                    rel_type_str = str(rel_type.value) if hasattr(rel_type, "value") else str(rel_type)
                    for tgt in targets:
                        edge_id = f"edge_{src}_{tgt}_{rel_type_str}".lower()
                        edge_records.append({
                            "edge_id": edge_id,
                            "source_node_id": src,
                            "target_node_id": str(tgt),
                            "relation_type": rel_type_str,
                            "confidence_score": 100,
                            "adjudicated": True,
                        })
            elif isinstance(typed_edges_raw, list):
                for edge in typed_edges_raw:
                    if isinstance(edge, dict):
                        tgt = edge.get("target_id") or edge.get("target_node_id", "")
                        rel = edge.get("rel_type") or edge.get("relation_type", "RELATED")
                        rel_str = str(rel.value) if hasattr(rel, "value") else str(rel)
                        edge_id = f"edge_{src}_{tgt}_{rel_str}".lower()
                        edge_records.append({
                            "edge_id": edge_id,
                            "source_node_id": src,
                            "target_node_id": str(tgt),
                            "relation_type": rel_str,
                            "confidence_score": edge.get("confidence_score", 100),
                            "adjudicated": edge.get("adjudicated", False),
                        })
        if edge_records:
            self.store.store_edges(ws_uuid, edge_records)

        # 3. Store projections
        proj_records = [p.model_dump(mode="json") for p in projections.values()]
        self.store.store_projections(ws_uuid, proj_records)

        # 4. Store provenance links
        prov_records = []
        for node in node_records:
            nid = node["node_id"]
            srefs = node.get("source_record_refs", [])
            shashes = node.get("source_evidence_hashes", [])
            for i, sref in enumerate(srefs):
                if isinstance(shashes, list) and i < len(shashes):
                    shash = shashes[i]
                elif isinstance(shashes, dict):
                    shash = shashes.get(str(sref), node.get("lineage_sha256", ""))
                else:
                    shash = node.get("lineage_sha256", "")
                link_id = f"link_{nid}_{sref}".lower()
                prov_records.append({
                    "link_id": link_id,
                    "node_id": nid,
                    "source_id": str(sref),
                    "source_sha256": shash,
                })
        if prov_records:
            self.store.store_provenance_links(ws_uuid, prov_records)

        # 5. Store search indices
        idx_records = [idx.model_dump(mode="json") for idx in indices.values()]
        self.store.store_search_indexes(ws_uuid, idx_records)

        # State transition
        self.runtime.execute_transition(
            aggregate_id=agg.aggregate_id,
            transition_name="project_supabase",
            actor_id=actor_id,
            actor_lane=caller_lane,
            context_claims=["workspace_active", "search_index_built"],
            state_updates={
                "nodes_stored": len(node_records),
                "projections_stored": len(proj_records),
                "edges_stored": len(edge_records),
                "indices_stored": len(idx_records),
            },
        )

        now = utc_now_rfc3339()
        receipt_raw = {
            "receipt_id": f"rcpt_kcp_{uuid4().hex[:12]}",
            "workspace_id": str(ws_uuid),
            "program_id": self.PROGRAM_ID,
            "program_version": self.PROGRAM_VERSION,
            "operation": "project_to_database",
            "nodes_count": len(node_records),
            "projections_count": len(proj_records),
            "edges_count": len(edge_records),
            "rebuild_count": self._rebuild_counters.get(ws_key, 0),
            "timestamp_utc": now,
        }
        receipt_sha = canonical_sha256(receipt_raw)
        receipt = KnowledgeCompilationReceipt(
            receipt_id=receipt_raw["receipt_id"],
            workspace_id=ws_uuid,
            program_id=self.PROGRAM_ID,
            program_version=self.PROGRAM_VERSION,
            operation=receipt_raw["operation"],
            nodes_count=receipt_raw["nodes_count"],
            projections_count=receipt_raw["projections_count"],
            edges_count=receipt_raw["edges_count"],
            rebuild_count=receipt_raw["rebuild_count"],
            timestamp_utc=now,
            receipt_sha256=receipt_sha,
        )

        self._in_memory_receipts.setdefault(ws_key, []).append(receipt)
        return receipt

    def rebuild_projections(
        self,
        workspace_id: Union[str, UUID],
        *,
        actor_id: str = "usr_lead_commander",
        caller_lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> KnowledgeCompilationReceipt:
        """Idempotently rebuilds projections and search indexes without mutating source identity (COMMANDER lane)."""
        if caller_lane != AuthorityLane.COMMANDER:
            raise UnauthorizedKnowledgeCompilerLaneError(
                f"rebuild_projections must execute on COMMANDER lane, observed {caller_lane.name}"
            )

        ws_uuid = UUID(str(workspace_id))
        ws_key = _normalize_workspace_id(ws_uuid)

        # Execute rebuild pipeline
        self.compile_projections(ws_uuid, actor_id=actor_id, caller_lane=AuthorityLane.COMPOSER)
        self.build_search_index(ws_uuid, actor_id=actor_id, caller_lane=AuthorityLane.ANALYST)

        self._rebuild_counters[ws_key] = self._rebuild_counters.get(ws_key, 0) + 1

        receipt = self.project_to_database(ws_uuid, actor_id=actor_id, caller_lane=AuthorityLane.COMMANDER)
        return receipt

    def sync_retraction(
        self,
        workspace_id: Union[str, UUID],
        node_id: str,
        reason: str,
        *,
        actor_id: str = "usr_lead_commander",
        caller_lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> KnowledgeCompilationReceipt:
        """Synchronizes node retraction into projections and search indexes (COMMANDER lane)."""
        if caller_lane != AuthorityLane.COMMANDER:
            raise UnauthorizedKnowledgeCompilerLaneError(
                f"sync_retraction must execute on COMMANDER lane, observed {caller_lane.name}"
            )

        ws_uuid = UUID(str(workspace_id))
        ws_key = _normalize_workspace_id(ws_uuid)
        nodes = self._in_memory_nodes.get(ws_key, {})

        if node_id not in nodes:
            raise InvalidKnowledgeNodeError(f"Node {node_id} not found in compiler session")

        nodes[node_id]["lifecycle_status"] = "retracted"
        nodes[node_id]["retraction_reason"] = reason

        return self.rebuild_projections(ws_uuid, actor_id=actor_id, caller_lane=caller_lane)

    def recover_to_repairing(
        self,
        workspace_id: Union[str, UUID],
        reason: str,
        *,
        actor_id: str = "usr_lead_commander",
        caller_lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> KnowledgeCompilerSnapshot:
        """Puts the compiler session into REPAIRING state (COMMANDER lane)."""
        if caller_lane != AuthorityLane.COMMANDER:
            raise UnauthorizedKnowledgeCompilerLaneError(
                f"recover_to_repairing must execute on COMMANDER lane, observed {caller_lane.name}"
            )

        ws_uuid = UUID(str(workspace_id))
        agg = self._get_or_create_aggregate(ws_uuid, actor_id=actor_id)

        self.runtime.repair_state(
            aggregate_id=agg.aggregate_id,
            repair_action="recover_to_repairing",
            repair_payload={"reason": reason},
            actor_id=actor_id,
            actor_lane=caller_lane,
            target_state="REPAIRING",
            state_updates={"repair_reason": reason},
        )
        return self.get_snapshot(ws_uuid)

    def repair_compiler_state(
        self,
        workspace_id: Union[str, UUID],
        *,
        actor_id: str = "usr_lead_commander",
        caller_lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> KnowledgeCompilerSnapshot:
        """Repairs and restores the compiler session from REPAIRING back to KNOWLEDGE_INGESTED (COMMANDER lane)."""
        if caller_lane != AuthorityLane.COMMANDER:
            raise UnauthorizedKnowledgeCompilerLaneError(
                f"repair_compiler_state must execute on COMMANDER lane, observed {caller_lane.name}"
            )

        ws_uuid = UUID(str(workspace_id))
        agg = self._get_or_create_aggregate(ws_uuid, actor_id=actor_id)

        self.runtime.repair_state(
            aggregate_id=agg.aggregate_id,
            repair_action="repair_compiler",
            repair_payload={"action": "restore_to_knowledge_ingested"},
            actor_id=actor_id,
            actor_lane=caller_lane,
            target_state="KNOWLEDGE_INGESTED",
            state_updates={"repaired_at_utc": utc_now_rfc3339()},
        )
        return self.get_snapshot(ws_uuid)

    def quarantine_compiler_state(
        self,
        workspace_id: Union[str, UUID],
        reason: str,
        *,
        actor_id: str = "usr_lead_commander",
        caller_lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> KnowledgeCompilerSnapshot:
        """Quarantines the compiler session on critical authority violation (COMMANDER lane)."""
        if caller_lane != AuthorityLane.COMMANDER:
            raise UnauthorizedKnowledgeCompilerLaneError(
                f"quarantine_compiler_state must execute on COMMANDER lane, observed {caller_lane.name}"
            )

        ws_uuid = UUID(str(workspace_id))
        agg = self._get_or_create_aggregate(ws_uuid, actor_id=actor_id)

        self.runtime.repair_state(
            aggregate_id=agg.aggregate_id,
            repair_action="quarantine_compiler",
            repair_payload={"reason": reason},
            actor_id=actor_id,
            actor_lane=caller_lane,
            target_state="QUARANTINED",
            state_updates={"quarantine_reason": reason},
        )
        return self.get_snapshot(ws_uuid)

    # ------------------------------------------------------------------------
    # State & Query Accessors
    # ------------------------------------------------------------------------

    def get_snapshot(self, workspace_id: Union[str, UUID]) -> KnowledgeCompilerSnapshot:
        """Returns the current state snapshot of the knowledge compiler."""
        ws_uuid = UUID(str(workspace_id))
        ws_key = _normalize_workspace_id(ws_uuid)
        agg = self._get_or_create_aggregate(ws_uuid)

        nodes = self._in_memory_nodes.get(ws_key, {})
        projections = self._in_memory_projections.get(ws_key, {})
        indices = self._in_memory_indices.get(ws_key, {})
        receipts = self._in_memory_receipts.get(ws_key, [])

        return KnowledgeCompilerSnapshot(
            workspace_id=ws_uuid,
            status=agg.lifecycle.value,
            current_state=agg.current_state,
            nodes_count=len(nodes),
            projections_count=len(projections),
            indices_count=len(indices),
            last_rebuild_at_utc=receipts[-1].timestamp_utc if receipts else None,
            receipt_count=len(receipts),
        )

    def query_structured_nodes(
        self,
        workspace_id: Union[str, UUID],
        *,
        category: Optional[str] = None,
        lifecycle_status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Queries authoritative knowledge nodes with structured SQL filters."""
        return self.store.list_nodes(
            workspace_id=workspace_id,
            category=category,
            lifecycle_status=lifecycle_status,
        )

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
        """Multi-predicate search over knowledge projections with integer basis points scoring."""
        return self.store.search_knowledge(
            workspace_id=workspace_id,
            query=query,
            category=category,
            tags=tags,
            lifecycle_state=lifecycle_state,
            dense_adapter_cb=dense_adapter_cb,
            limit=limit,
        )
