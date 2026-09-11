"""Research Knowledge Extraction + Canonicalization + OKF Program Coordinator.

Governed by:
- Phase 3 Mandate M29 (03_PHASE_3_INTELLIGENCE_AND_PROGRAMS/M29_research_knowledge_extraction_canonicalization_okf.md)
- 00_CONTROL/20_PHASE3_CANONICALIZATION_MODEL.md
- 00_CONTROL/21_PHASE3_KNOWLEDGE_RUNTIME_CONTRACT.md
- 00_CONTROL/22_PHASE3_RESEARCH_RETRIEVAL_MATRIX.md
- 00_CONTROL/24_PHASE3_PROGRAM_STATE_HOOKS_MATRIX.md
- 00_CONTROL/26_PHASE3_EXTERNAL_REFERENCE_READS.md
- Live PostgreSQL/RLS Tenancy Authority (TS-CAE-TEN-001)

Operating Model:
- Protected Research Sources: Protected source-bearing records cannot be silently rewritten.
- Canonicalization as Intelligence Program: Semantic chain from Source -> Extraction -> Candidate -> Canonicalization -> OKF Projection.
- Canonical Taxonomy: SAME (alias merge), RELATED (associative edge), SUBTYPE/SUPERTYPE (hierarchy), CONTRADICTORY (contradiction edge), DISTINCT (separate node).
- False-Merge Rejection: Homonyms, context collisions, and distinct entities are preserved as distinct canonical nodes.
- Open Knowledge Format (OKF): Curated Markdown + YAML frontmatter representation with deterministic SHA-256 hashes.
- Four Authority Lanes:
  - HUNTER: Knowledge candidate extraction from raw research sources.
  - ANALYST: Relationship classification (SAME/RELATED/SUBTYPE/CONTRADICTORY/DISTINCT) and anti-false-merge validation.
  - COMPOSER: Canonical knowledge node composition and OKF Markdown bundle projection.
  - COMMANDER: Operator adjudication, contradiction resolution, canonical node commitment, retraction, and recovery.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
import logging
from pathlib import Path
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_state_runtime import (
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
    ProgramStateAggregateNotFoundError,
    ProgramStateLifecycle,
    ProgramStateMachineDefinition,
    ProgramStateRuntimeError,
    ProgramStateVersionConflictError,
    ProgramTransitionContract,
    ProgramTransitionResult,
    SideEffectClass,
    UniversalProgramStateRuntime,
    _compute_state_hash,
    get_canonical_research_canonicalization_state_machine,
)
from ca_runtime.state_lifecycle import (
    CausalTraceEventType,
    CausalTraceLedger,
    CausalTraceRecord,
    StateLifecycleCoordinator,
)
from ca_runtime.tenancy import (
    CrossWorkspaceLeakError,
    TenantContext,
    TenancyError,
    TenancyViolationError,
    require_current_tenant_context,
)

logger = logging.getLogger("ca_runtime.research_canonicalization_program")

PROGRAM_ID = "research_canonicalization_program"
PROGRAM_VERSION = "1.0.0"
OKF_VERSION = "0.1"
OKF_PROFILE = "cmf-okf-research-knowledge-1.0"


# ============================================================================
# 1. Typed Error Hierarchy
# ============================================================================

class ResearchCanonicalizationProgramError(ProgramStateRuntimeError):
    """Base exception for Research Canonicalization Program execution."""
    pass


class FalseMergeViolationError(ResearchCanonicalizationProgramError):
    """Raised when distinct concepts or homonyms are falsely merged without identity proof."""

    def __init__(self, message: str, *, candidate_labels: Sequence[str], details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message,
            reason_code="FALSE_MERGE_VIOLATION",
            details={"candidate_labels": list(candidate_labels), **(details or {})},
        )
        self.candidate_labels = list(candidate_labels)


class ContradictionAdjudicationRequiredError(ResearchCanonicalizationProgramError):
    """Raised when unadjudicated contradiction edges block state promotion to KNOWLEDGE_COMMITTED."""

    def __init__(self, message: str, *, contradiction_ids: Sequence[str], details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message,
            reason_code="CONTRADICTION_ADJUDICATION_REQUIRED",
            details={"contradiction_ids": list(contradiction_ids), **(details or {})},
        )
        self.contradiction_ids = list(contradiction_ids)


class SourceProvenanceMissingError(ResearchCanonicalizationProgramError):
    """Raised when extracted candidate or canonical node lacks valid source provenance."""

    def __init__(self, message: str, *, item_id: str, missing_fields: Sequence[str]):
        super().__init__(
            message,
            reason_code="SOURCE_PROVENANCE_MISSING",
            details={"item_id": item_id, "missing_fields": list(missing_fields)},
        )
        self.item_id = item_id
        self.missing_fields = list(missing_fields)


class NodeRetractedError(ResearchCanonicalizationProgramError):
    """Raised when an operation targets a canonical node that has been retracted."""

    def __init__(self, message: str, *, node_id: str, retraction_reason: Optional[str] = None):
        super().__init__(
            message,
            reason_code="NODE_RETRACTED",
            details={"node_id": node_id, "retraction_reason": retraction_reason},
        )
        self.node_id = node_id
        self.retraction_reason = retraction_reason


class OKFValidationError(ResearchCanonicalizationProgramError):
    """Raised when OKF Markdown or frontmatter generation violates specification."""

    def __init__(self, message: str, *, document_id: str, validation_errors: Sequence[str]):
        super().__init__(
            message,
            reason_code="OKF_VALIDATION_ERROR",
            details={"document_id": document_id, "validation_errors": list(validation_errors)},
        )
        self.document_id = document_id
        self.validation_errors = list(validation_errors)


class SourceImmutabilityViolationError(ResearchCanonicalizationProgramError):
    """Raised when an attempt is made to mutate protected source records."""

    def __init__(self, message: str, *, source_id: str):
        super().__init__(
            message,
            reason_code="SOURCE_IMMUTABILITY_VIOLATION",
            details={"source_id": source_id},
        )
        self.source_id = source_id


class WorkspaceScopeViolationError(ResearchCanonicalizationProgramError):
    """Raised when an operation crosses tenant workspace isolation boundaries."""

    def __init__(self, message: str, *, expected_workspace_id: str, actual_workspace_id: str):
        super().__init__(
            message,
            reason_code="WORKSPACE_SCOPE_VIOLATION",
            details={"expected_workspace_id": expected_workspace_id, "actual_workspace_id": actual_workspace_id},
        )


# ============================================================================
# 2. Domain Data Models
# ============================================================================

class CanonicalRelationshipType(str, Enum):
    """Canonical relationship taxonomy per 20_PHASE3_CANONICALIZATION_MODEL.md."""
    SAME = "SAME"                       # Alias / synonym -> merge into canonical node
    RELATED = "RELATED"                 # Associative edge -> related_to
    SUBTYPE = "SUBTYPE"                 # Taxonomic child -> subtype_of
    SUPERTYPE = "SUPERTYPE"             # Taxonomic parent -> supertype_of
    CONTRADICTORY = "CONTRADICTORY"     # Contradiction / counter-claim -> contradicts
    DISTINCT = "DISTINCT"               # Explicitly distinct concept (anti-false-merge)


class KnowledgeCandidate(BaseModel):
    """Structured knowledge candidate extracted from an immutable research source."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    candidate_id: str = Field(default_factory=lambda: f"cand_{uuid4().hex[:12]}")
    label: str = Field(..., min_length=1, description="Primary candidate label or phrase")
    candidate_type: str = Field("concept", description="concept, entity, claim, methodology, signal")
    extracted_text: str = Field(..., min_length=1, description="Verbatim extracted text or definition")
    source_id: str = Field(..., min_length=1, description="Reference to protected ResearchSourceRecord")
    source_sha256: str = Field(..., min_length=64, max_length=64, description="SHA-256 of source content")
    confidence_score: int = Field(90, ge=0, le=100)
    attributes: Dict[str, Any] = Field(default_factory=dict)
    extracted_at: str = Field(default_factory=utc_now_rfc3339)


class CanonicalRelationship(BaseModel):
    """Semantic relationship connecting candidates or canonical nodes."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    rel_id: str = Field(default_factory=lambda: f"rel_{uuid4().hex[:12]}")
    source_id: str = Field(..., min_length=1, description="Source candidate or node ID")
    target_id: str = Field(..., min_length=1, description="Target candidate or node ID")
    rel_type: CanonicalRelationshipType
    confidence_score: int = Field(100, ge=0, le=100)
    rationale: str = Field(..., min_length=1)
    adjudicated: bool = Field(False)
    adjudicated_by: Optional[str] = None
    created_at: str = Field(default_factory=utc_now_rfc3339)


class CanonicalKnowledgeNode(BaseModel):
    """Curated canonical knowledge entity with full provenance back-pointers."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    node_id: str = Field(default_factory=lambda: f"kn_{uuid4().hex[:12]}")
    canonical_label: str = Field(..., min_length=1)
    category: str = Field("concept", description="concept, entity, claim, methodology, signal")
    aliases: List[str] = Field(default_factory=list)
    definition: str = Field(..., min_length=1)
    lifecycle_status: str = Field("active", description="active, experimental, superseded, retracted")
    authority_class: str = Field("derived_validated_knowledge", description="authority classification")
    source_record_refs: List[str] = Field(..., min_length=1, description="Immutable source record IDs")
    source_evidence_hashes: List[str] = Field(..., min_length=1, description="SHA-256 digests of source evidence")
    lineage_sha256: str = Field(..., min_length=64, max_length=64, description="Cryptographic lineage hash")
    version: int = Field(1, ge=1)
    supersedes_node_id: Optional[str] = None
    retraction_reason: Optional[str] = None
    typed_edges: Dict[str, List[str]] = Field(default_factory=dict)
    created_at: str = Field(default_factory=utc_now_rfc3339)
    updated_at: str = Field(default_factory=utc_now_rfc3339)

    @classmethod
    def compute_lineage_hash(
        cls,
        *,
        canonical_label: str,
        category: str,
        aliases: Sequence[str],
        definition: str,
        source_record_refs: Sequence[str],
        source_evidence_hashes: Sequence[str],
        version: int,
        supersedes_node_id: Optional[str] = None,
    ) -> str:
        payload = {
            "canonical_label": canonical_label.strip(),
            "category": category.strip(),
            "aliases": sorted(list(set(aliases))),
            "definition": definition.strip(),
            "source_record_refs": sorted(list(source_record_refs)),
            "source_evidence_hashes": sorted(list(source_evidence_hashes)),
            "version": version,
            "supersedes_node_id": supersedes_node_id,
        }
        return canonical_sha256(payload)


class OKFDocument(BaseModel):
    """Open Knowledge Format (OKF) Markdown projection of a canonical knowledge node."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    document_id: str
    relative_path: str
    frontmatter: Dict[str, Any]
    markdown: str
    markdown_sha256: str
    canonical_state: bool = True
    rebuildable: bool = True


class OKFKnowledgeBundle(BaseModel):
    """Complete exportable OKF knowledge bundle conforming to OKF specification."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    bundle_id: str = Field(default_factory=lambda: f"okf_bundle_{uuid4().hex[:12]}")
    bundle_sha256: str
    index_markdown: str
    documents: List[OKFDocument]
    node_count: int
    edge_count: int
    created_at: str = Field(default_factory=utc_now_rfc3339)


class AdjudicationDecision(BaseModel):
    """Operator adjudication decision for resolving contradictions or false merges."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    decision_id: str = Field(default_factory=lambda: f"adj_{uuid4().hex[:12]}")
    target_id: str = Field(..., min_length=1, description="Node ID or Relationship ID")
    action: str = Field(..., description="APPROVE_MERGE, FORCE_DISTINCT, RESOLVE_CONTRADICTION, RETRACT_NODE, RECLASSIFY_NODE")
    operator_actor_id: str = Field(..., min_length=1)
    rationale: str = Field(..., min_length=1)
    timestamp: str = Field(default_factory=utc_now_rfc3339)


class ResearchCanonicalizationSnapshot(BaseModel):
    """Immutable point-in-time state aggregate snapshot."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    aggregate_id: str
    workspace_id: str
    program_id: str
    program_version: str
    state: str
    version: int
    source_records: List[Dict[str, Any]]
    candidates: List[KnowledgeCandidate]
    relationships: List[CanonicalRelationship]
    canonical_nodes: List[CanonicalKnowledgeNode]
    okf_bundle: Optional[OKFKnowledgeBundle]
    adjudications: List[AdjudicationDecision]
    state_hash: str
    updated_at: str


# ============================================================================
# 3. Canonicalization & OKF Rendering Helpers
# ============================================================================

def _slugify(text: str) -> str:
    """Converts a label into a filesystem-safe slug."""
    s = text.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    return s.strip("-") or "item"


def _render_okf_markdown(node: CanonicalKnowledgeNode) -> Tuple[str, Dict[str, Any], str]:
    """Renders a CanonicalKnowledgeNode into OKF YAML frontmatter and structured Markdown."""
    frontmatter = {
        "okf_version": OKF_VERSION,
        "cmf_profile": OKF_PROFILE,
        "type": node.category.capitalize(),
        "id": node.node_id,
        "version": f"{node.version}.0.0",
        "lifecycle_status": node.lifecycle_status,
        "authority_class": node.authority_class,
        "title": node.canonical_label,
        "description": node.definition[:160] + ("..." if len(node.definition) > 160 else ""),
        "aliases": node.aliases,
        "source_record_refs": node.source_record_refs,
        "source_evidence_hashes": node.source_evidence_hashes,
        "typed_edges": node.typed_edges,
        "lineage_sha256": node.lineage_sha256,
    }

    yaml_lines = ["---"]
    for key, val in frontmatter.items():
        if isinstance(val, list):
            if not val:
                yaml_lines.append(f"{key}: []")
            else:
                yaml_lines.append(f"{key}:")
                for item in val:
                    yaml_lines.append(f"  - {json.dumps(item)}")
        elif isinstance(val, dict):
            if not val:
                yaml_lines.append(f"{key}: {{}}")
            else:
                yaml_lines.append(f"{key}:")
                for sub_k, sub_v in val.items():
                    yaml_lines.append(f"  {sub_k}:")
                    for edge_target in sub_v:
                        yaml_lines.append(f"    - {json.dumps(edge_target)}")
        else:
            yaml_lines.append(f"{key}: {json.dumps(val)}")
    yaml_lines.append("---")
    yaml_header = "\n".join(yaml_lines)

    body_lines = [
        f"# {node.canonical_label}",
        "",
        "## Definition",
        "",
        node.definition,
        "",
        "## Aliases & Synonyms",
        "",
    ]
    if node.aliases:
        for alias in node.aliases:
            body_lines.append(f"- {alias}")
    else:
        body_lines.append("*None*")

    body_lines.extend([
        "",
        "## Provenance & Lineage",
        "",
        f"- **Authority Class:** `{node.authority_class}`",
        f"- **Lifecycle Status:** `{node.lifecycle_status}`",
        f"- **Lineage SHA-256:** `{node.lineage_sha256}`",
        "- **Source Records:**",
    ])
    for sref in node.source_record_refs:
        body_lines.append(f"  - `{sref}`")

    body_lines.extend([
        "",
        "## Typed Relationships",
        "",
    ])
    if node.typed_edges:
        for edge_name, targets in node.typed_edges.items():
            body_lines.append(f"### {edge_name.replace('_', ' ').capitalize()}")
            for target in targets:
                body_lines.append(f"- `{target}`")
            body_lines.append("")
    else:
        body_lines.append("*No outgoing relationships defined.*")
        body_lines.append("")

    full_markdown = f"{yaml_header}\n\n" + "\n".join(body_lines)
    full_markdown_sha256 = hashlib.sha256(full_markdown.encode("utf-8")).hexdigest()

    category_slug = _slugify(node.category) + "s"
    relative_path = f"{category_slug}/{_slugify(node.canonical_label)}.md"

    return full_markdown, frontmatter, relative_path


def _render_okf_index(nodes: Sequence[CanonicalKnowledgeNode], bundle_id: str) -> str:
    """Renders the top-level index.md catalog for the OKF bundle."""
    lines = [
        f"# Research Knowledge Catalog (OKF)",
        "",
        f"**Bundle ID:** `{bundle_id}`  ",
        f"**Generated At:** `{utc_now_rfc3339()}`  ",
        f"**Profile:** `{OKF_PROFILE}`  ",
        f"**Total Canonical Nodes:** `{len(nodes)}`",
        "",
        "---",
        "",
        "## Knowledge Index by Category",
        "",
    ]

    by_category: Dict[str, List[CanonicalKnowledgeNode]] = {}
    for node in nodes:
        cat = node.category.capitalize()
        by_category.setdefault(cat, []).append(node)

    for cat, cat_nodes in sorted(by_category.items()):
        lines.append(f"### {cat} ({len(cat_nodes)})")
        lines.append("")
        for n in sorted(cat_nodes, key=lambda x: x.canonical_label.lower()):
            category_slug = _slugify(n.category) + "s"
            rel_link = f"{category_slug}/{_slugify(n.canonical_label)}.md"
            status_tag = f" `[{n.lifecycle_status}]`" if n.lifecycle_status != "active" else ""
            lines.append(f"- [{n.canonical_label}]({rel_link}){status_tag} — {n.definition[:100]}...")
        lines.append("")

    return "\n".join(lines)


# ============================================================================
# 4. Coordinator Implementation
# ============================================================================

class ResearchCanonicalizationProgramCoordinator:
    """Coordinator for the Research Knowledge Extraction + Canonicalization + OKF Program."""

    def __init__(
        self,
        runtime: Optional[UniversalProgramStateRuntime] = None,
        lifecycle_coordinator: Optional[StateLifecycleCoordinator] = None,
        trace_ledger: Optional[CausalTraceLedger] = None,
    ) -> None:
        self.runtime = runtime or UniversalProgramStateRuntime()
        self.state_runtime = self.runtime
        self.state_machine = get_canonical_research_canonicalization_state_machine()
        self.runtime.register_state_machine(self.state_machine)
        self.trace_ledger = trace_ledger or CausalTraceLedger()
        self.lifecycle_coordinator = lifecycle_coordinator or StateLifecycleCoordinator(
            state_runtime=self.runtime,
            trace_ledger=self.trace_ledger,
        )

    def _get_aggregate_state_data(self, aggregate_id: str) -> Tuple[ProgramStateAggregate, Dict[str, Any]]:
        agg = self.runtime.get_aggregate(aggregate_id)
        if agg is None:
            raise ProgramStateAggregateNotFoundError(f"Aggregate '{aggregate_id}' not found")
        return agg, agg.state_data

    # ------------------------------------------------------------------------
    # State Operations
    # ------------------------------------------------------------------------

    def initialize_program(
        self,
        workspace_id: UUID | str,
        actor_id: str,
        cae_run_id: Optional[str] = None,
        context_claims: Optional[Sequence[str]] = None,
    ) -> str:
        """Initializes a new Research Canonicalization Program state aggregate in INITIAL state."""
        ws_str = str(workspace_id)
        agg = self.runtime.initialize_program_state(
            program_id=PROGRAM_ID,
            workspace_id=ws_str,
            actor_id=actor_id,
            cae_run_id=cae_run_id,
            initial_data={
                "source_records": [],
                "candidates": [],
                "relationships": [],
                "canonical_nodes": [],
                "okf_bundle": None,
                "adjudications": [],
            },
            context_claims=context_claims or ["workspace_active", "sources_verified", "false_merge_verified"],
        )
        return agg.aggregate_id

    def attach_sources(
        self,
        aggregate_id: str,
        sources: Sequence[Any],
        context: Optional[TenantContext] = None,
        idempotency_key: Optional[str] = None,
    ) -> ProgramTransitionResult:
        """Attaches validated immutable research sources (COMMANDER lane)."""
        ctx = context or require_current_tenant_context()
        agg = self.runtime.get_aggregate(aggregate_id)
        if str(ctx.workspace_id) != agg.workspace_id:
            raise WorkspaceScopeViolationError(
                f"Workspace isolation violation: aggregate belongs to '{agg.workspace_id}', context has '{ctx.workspace_id}'",
                expected_workspace_id=agg.workspace_id,
                actual_workspace_id=str(ctx.workspace_id),
            )

        if not sources:
            raise SourceProvenanceMissingError(
                "Cannot attach empty research sources",
                item_id=aggregate_id,
                missing_fields=["sources"],
            )

        serialized_sources: List[Dict[str, Any]] = []
        for s in sources:
            if hasattr(s, "model_dump"):
                d = s.model_dump()
            elif hasattr(s, "__dict__"):
                d = dict(s.__dict__)
            elif isinstance(s, dict):
                d = dict(s)
            else:
                raise ResearchCanonicalizationProgramError(f"Unsupported source record type: {type(s)}")

            s_id = d.get("source_id") or d.get("observation_id") or d.get("signal_id")
            s_hash = d.get("content_hash_sha256") or d.get("sha256") or d.get("content_hash")
            if not s_id or not s_hash:
                raise SourceProvenanceMissingError(
                    f"Source missing source_id or content_hash: {d}",
                    item_id=str(s_id or "unknown"),
                    missing_fields=["source_id", "content_hash"],
                )
            d["source_id"] = s_id
            d["content_hash_sha256"] = s_hash
            serialized_sources.append(d)

        def _work(current_agg: ProgramStateAggregate) -> Dict[str, Any]:
            new_state = dict(current_agg.state_data)
            new_state["source_records"] = serialized_sources
            return new_state

        return self.lifecycle_coordinator.execute_state_phase(
            aggregate_id=aggregate_id,
            transition_name="attach_sources",
            actor_id=ctx.actor_id,
            actor_lane=AuthorityLane.COMMANDER,
            work_fn=_work,
            context=ctx,
            context_claims=["workspace_active", "sources_verified"],
            idempotency_key=idempotency_key,
        )

    def extract_candidates(
        self,
        aggregate_id: str,
        custom_candidates: Optional[Sequence[KnowledgeCandidate]] = None,
        context: Optional[TenantContext] = None,
        idempotency_key: Optional[str] = None,
    ) -> ProgramTransitionResult:
        """Extracts knowledge candidates from attached sources (HUNTER lane)."""
        ctx = context or require_current_tenant_context()
        agg = self.runtime.get_aggregate(aggregate_id)
        if str(ctx.workspace_id) != agg.workspace_id:
            raise WorkspaceScopeViolationError(
                f"Workspace isolation violation: aggregate belongs to '{agg.workspace_id}', context has '{ctx.workspace_id}'",
                expected_workspace_id=agg.workspace_id,
                actual_workspace_id=str(ctx.workspace_id),
            )

        sources = agg.state_data.get("source_records", [])
        if not sources:
            raise SourceProvenanceMissingError(
                "No attached sources found on aggregate",
                item_id=aggregate_id,
                missing_fields=["source_records"],
            )

        source_id_to_hash = {s["source_id"]: s["content_hash_sha256"] for s in sources}

        extracted_candidates: List[KnowledgeCandidate] = []
        if custom_candidates:
            for cand in custom_candidates:
                if cand.source_id not in source_id_to_hash:
                    raise SourceProvenanceMissingError(
                        f"Candidate '{cand.label}' references unknown source '{cand.source_id}'",
                        item_id=cand.candidate_id,
                        missing_fields=["source_id"],
                    )
                if cand.source_sha256 != source_id_to_hash[cand.source_id]:
                    raise SourceProvenanceMissingError(
                        f"Candidate '{cand.label}' source hash mismatch",
                        item_id=cand.candidate_id,
                        missing_fields=["source_sha256"],
                    )
                extracted_candidates.append(cand)
        else:
            for s in sources:
                s_id = s["source_id"]
                s_hash = s["content_hash_sha256"]
                topic = s.get("topic") or s.get("query_context") or s.get("title") or "Unknown Topic"
                excerpt = s.get("evidence_excerpt") or s.get("raw_text_snippet") or s.get("content") or topic

                cand = KnowledgeCandidate(
                    candidate_id=f"cand_{uuid4().hex[:12]}",
                    label=topic,
                    candidate_type="concept",
                    extracted_text=excerpt,
                    source_id=s_id,
                    source_sha256=s_hash,
                    confidence_score=95,
                )
                extracted_candidates.append(cand)

        def _work(current_agg: ProgramStateAggregate) -> Dict[str, Any]:
            new_state = dict(current_agg.state_data)
            new_state["candidates"] = [c.model_dump() for c in extracted_candidates]
            return new_state

        return self.lifecycle_coordinator.execute_state_phase(
            aggregate_id=aggregate_id,
            transition_name="extract_candidates",
            actor_id=ctx.actor_id,
            actor_lane=AuthorityLane.HUNTER,
            work_fn=_work,
            context=ctx,
            context_claims=["workspace_active", "sources_attached"],
            idempotency_key=idempotency_key,
        )

    def canonicalize_candidates(
        self,
        aggregate_id: str,
        custom_relationships: Optional[Sequence[CanonicalRelationship]] = None,
        similarity_threshold_pct: int = 85,
        homonym_blacklist: Optional[Mapping[str, Set[str]]] = None,
        context: Optional[TenantContext] = None,
        idempotency_key: Optional[str] = None,
    ) -> ProgramTransitionResult:
        """Classifies relationships, resolves aliases/merges, and guards against false merges (ANALYST lane)."""
        ctx = context or require_current_tenant_context()
        agg = self.runtime.get_aggregate(aggregate_id)
        if str(ctx.workspace_id) != agg.workspace_id:
            raise WorkspaceScopeViolationError(
                f"Workspace isolation violation: aggregate belongs to '{agg.workspace_id}', context has '{ctx.workspace_id}'",
                expected_workspace_id=agg.workspace_id,
                actual_workspace_id=str(ctx.workspace_id),
            )

        candidates_raw = agg.state_data.get("candidates", [])
        if not candidates_raw:
            raise ResearchCanonicalizationProgramError("No candidates available for canonicalization")

        candidates = [KnowledgeCandidate(**c) for c in candidates_raw]
        blacklist = homonym_blacklist or {}

        canonical_nodes: List[CanonicalKnowledgeNode] = []
        relationships: List[CanonicalRelationship] = []

        if custom_relationships:
            relationships.extend(custom_relationships)

        clusters: List[Dict[str, Any]] = []

        for cand in candidates:
            cand_norm = cand.label.strip().lower()
            placed = False

            for cluster in clusters:
                cluster_label = cluster["canonical_label"]
                cluster_norm = cluster_label.lower()

                if cluster_norm in blacklist and cand_norm in blacklist[cluster_norm]:
                    continue
                if cand_norm in blacklist and cluster_norm in blacklist[cand_norm]:
                    continue

                is_same = (
                    cand_norm == cluster_norm
                    or cand.label in cluster["aliases"]
                    or cluster_label in cand.attributes.get("aliases", [])
                )

                if not is_same:
                    cand_words = cand.label.split()
                    cluster_words = cluster_label.split()
                    cand_acronym = "".join(w[0] for w in cand_words if w).upper()
                    cluster_acronym = "".join(w[0] for w in cluster_words if w).upper()
                    if len(cand_acronym) >= 2 and cand_acronym == cluster_label.upper():
                        is_same = True
                    elif len(cluster_acronym) >= 2 and cluster_acronym == cand.label.upper():
                        is_same = True

                if is_same:
                    cluster["candidates"].append(cand)
                    if cand.label != cluster_label and cand.label not in cluster["aliases"]:
                        cluster["aliases"].append(cand.label)
                    for a in cand.attributes.get("aliases", []):
                        if a not in cluster["aliases"] and a != cluster_label:
                            cluster["aliases"].append(a)
                    placed = True
                    break

            if not placed:
                aliases = list(cand.attributes.get("aliases", []))
                clusters.append({
                    "canonical_label": cand.label,
                    "category": cand.candidate_type,
                    "definition": cand.extracted_text,
                    "candidates": [cand],
                    "aliases": aliases,
                })

        for cluster in clusters:
            cluster_cands: List[KnowledgeCandidate] = cluster["candidates"]
            source_refs = sorted(list(set(c.source_id for c in cluster_cands)))
            source_hashes = sorted(list(set(c.source_sha256 for c in cluster_cands)))

            lineage_sha = CanonicalKnowledgeNode.compute_lineage_hash(
                canonical_label=cluster["canonical_label"],
                category=cluster["category"],
                aliases=cluster["aliases"],
                definition=cluster["definition"],
                source_record_refs=source_refs,
                source_evidence_hashes=source_hashes,
                version=1,
            )

            typed_edges: Dict[str, List[str]] = {}
            if cluster["aliases"]:
                typed_edges["same_as"] = sorted(cluster["aliases"])

            node = CanonicalKnowledgeNode(
                node_id=f"kn_{_slugify(cluster['canonical_label'])}",
                canonical_label=cluster["canonical_label"],
                category=cluster["category"],
                aliases=cluster["aliases"],
                definition=cluster["definition"],
                lifecycle_status="active",
                authority_class="derived_validated_knowledge",
                source_record_refs=source_refs,
                source_evidence_hashes=source_hashes,
                lineage_sha256=lineage_sha,
                version=1,
                typed_edges=typed_edges,
            )
            canonical_nodes.append(node)

        for rel in relationships:
            if rel.rel_type == CanonicalRelationshipType.SAME:
                pass
            elif rel.rel_type == CanonicalRelationshipType.CONTRADICTORY:
                for idx, n in enumerate(canonical_nodes):
                    if n.node_id == rel.source_id or n.canonical_label == rel.source_id:
                        edges = dict(n.typed_edges)
                        edges.setdefault("contradicts", []).append(rel.target_id)
                        new_lineage = CanonicalKnowledgeNode.compute_lineage_hash(
                            canonical_label=n.canonical_label,
                            category=n.category,
                            aliases=n.aliases,
                            definition=n.definition,
                            source_record_refs=n.source_record_refs,
                            source_evidence_hashes=n.source_evidence_hashes,
                            version=n.version,
                        )
                        canonical_nodes[idx] = n.model_copy(
                            update={"typed_edges": edges, "lineage_sha256": new_lineage}
                        )

        def _work(current_agg: ProgramStateAggregate) -> Dict[str, Any]:
            new_state = dict(current_agg.state_data)
            new_state["canonical_nodes"] = [n.model_dump() for n in canonical_nodes]
            new_state["relationships"] = [r.model_dump() for r in relationships]
            return new_state

        return self.lifecycle_coordinator.execute_state_phase(
            aggregate_id=aggregate_id,
            transition_name="canonicalize_candidates",
            actor_id=ctx.actor_id,
            actor_lane=AuthorityLane.ANALYST,
            work_fn=_work,
            context=ctx,
            context_claims=["workspace_active", "candidates_extracted", "false_merge_verified"],
            idempotency_key=idempotency_key,
        )

    def project_okf_bundle(
        self,
        aggregate_id: str,
        context: Optional[TenantContext] = None,
        idempotency_key: Optional[str] = None,
    ) -> ProgramTransitionResult:
        """Projects canonical knowledge nodes into Open Knowledge Format (OKF) bundle (COMPOSER lane)."""
        ctx = context or require_current_tenant_context()
        agg = self.runtime.get_aggregate(aggregate_id)
        if str(ctx.workspace_id) != agg.workspace_id:
            raise WorkspaceScopeViolationError(
                f"Workspace isolation violation: aggregate belongs to '{agg.workspace_id}', context has '{ctx.workspace_id}'",
                expected_workspace_id=agg.workspace_id,
                actual_workspace_id=str(ctx.workspace_id),
            )

        nodes_raw = agg.state_data.get("canonical_nodes", [])
        if not nodes_raw:
            raise ResearchCanonicalizationProgramError("No canonical nodes available for OKF projection")

        nodes = [CanonicalKnowledgeNode(**n) for n in nodes_raw]
        bundle_id = f"okf_{agg.aggregate_id}_{agg.version}"

        documents: List[OKFDocument] = []
        doc_hashes: List[str] = []
        edge_count = 0

        for node in nodes:
            md_content, frontmatter, rel_path = _render_okf_markdown(node)
            md_sha = hashlib.sha256(md_content.encode("utf-8")).hexdigest()

            doc = OKFDocument(
                document_id=node.node_id,
                relative_path=rel_path,
                frontmatter=frontmatter,
                markdown=md_content,
                markdown_sha256=md_sha,
                canonical_state=True,
                rebuildable=True,
            )
            documents.append(doc)
            doc_hashes.append(f"{rel_path}:{md_sha}")
            for targets in node.typed_edges.values():
                edge_count += len(targets)

        index_md = _render_okf_index(nodes, bundle_id)
        index_sha = hashlib.sha256(index_md.encode("utf-8")).hexdigest()
        doc_hashes.append(f"index.md:{index_sha}")

        composite_seed = "\n".join(sorted(doc_hashes))
        bundle_sha = hashlib.sha256(composite_seed.encode("utf-8")).hexdigest()

        bundle = OKFKnowledgeBundle(
            bundle_id=bundle_id,
            bundle_sha256=bundle_sha,
            index_markdown=index_md,
            documents=documents,
            node_count=len(nodes),
            edge_count=edge_count,
        )

        def _work(current_agg: ProgramStateAggregate) -> Dict[str, Any]:
            new_state = dict(current_agg.state_data)
            new_state["okf_bundle"] = bundle.model_dump()
            return new_state

        return self.lifecycle_coordinator.execute_state_phase(
            aggregate_id=aggregate_id,
            transition_name="project_okf_bundle",
            actor_id=ctx.actor_id,
            actor_lane=AuthorityLane.COMPOSER,
            work_fn=_work,
            context=ctx,
            context_claims=["workspace_active", "canonical_nodes_resolved"],
            idempotency_key=idempotency_key,
        )

    def adjudicate_contradiction(
        self,
        aggregate_id: str,
        decision: AdjudicationDecision,
        context: Optional[TenantContext] = None,
    ) -> None:
        """Records an operator adjudication decision (COMMANDER lane)."""
        ctx = context or require_current_tenant_context()
        agg = self.runtime.get_aggregate(aggregate_id)
        if str(ctx.workspace_id) != agg.workspace_id:
            raise WorkspaceScopeViolationError(
                f"Workspace isolation violation: aggregate belongs to '{agg.workspace_id}', context has '{ctx.workspace_id}'",
                expected_workspace_id=agg.workspace_id,
                actual_workspace_id=str(ctx.workspace_id),
            )

        new_state_data = dict(agg.state_data)
        adjudications = list(new_state_data.get("adjudications", []))
        adjudications.append(decision.model_dump())
        new_state_data["adjudications"] = adjudications

        relationships = list(new_state_data.get("relationships", []))
        for r in relationships:
            if r.get("rel_id") == decision.target_id or r.get("source_id") == decision.target_id or r.get("target_id") == decision.target_id:
                r["adjudicated"] = True
                r["adjudicated_by"] = decision.operator_actor_id
        new_state_data["relationships"] = relationships

        new_state_hash = _compute_state_hash(
            aggregate_id=agg.aggregate_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            current_state=agg.current_state,
            version=agg.version + 1,
            state_data=new_state_data,
        )
        updated_agg = ProgramStateAggregate(
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            cae_run_id=agg.cae_run_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            current_state=agg.current_state,
            state_data=new_state_data,
            version=agg.version + 1,
            state_hash=new_state_hash,
            lifecycle=agg.lifecycle,
            last_receipt_id=f"rcpt_adj_{decision.decision_id}",
            created_at=agg.created_at,
            updated_at=utc_now_rfc3339(),
        )
        self.runtime.store.save_aggregate(updated_agg)

        prev_trace_hash = self.trace_ledger.get_latest_trace_hash(aggregate_id)
        trace = CausalTraceRecord.create(
            cae_run_id=agg.cae_run_id or "run_default",
            program_id=PROGRAM_ID,
            aggregate_id=aggregate_id,
            workspace_id=agg.workspace_id,
            lane=AuthorityLane.COMMANDER,
            actor_id=decision.operator_actor_id,
            event_type=CausalTraceEventType.RECEIPT_COMMITTED,
            payload={"action": decision.action, "rationale": decision.rationale, "target_id": decision.target_id},
            receipt_id=f"rec_adj_{decision.decision_id}",
            previous_trace_sha256=prev_trace_hash,
        )
        self.trace_ledger.append(trace)

    def commit_canonical_knowledge(
        self,
        aggregate_id: str,
        allow_unadjudicated_contradictions: bool = False,
        context: Optional[TenantContext] = None,
        idempotency_key: Optional[str] = None,
    ) -> ProgramTransitionResult:
        """Commits and activates canonical knowledge in aggregate store (COMMANDER lane)."""
        ctx = context or require_current_tenant_context()
        agg = self.runtime.get_aggregate(aggregate_id)
        if str(ctx.workspace_id) != agg.workspace_id:
            raise WorkspaceScopeViolationError(
                f"Workspace isolation violation: aggregate belongs to '{agg.workspace_id}', context has '{ctx.workspace_id}'",
                expected_workspace_id=agg.workspace_id,
                actual_workspace_id=str(ctx.workspace_id),
            )

        bundle_raw = agg.state_data.get("okf_bundle")
        if not bundle_raw:
            raise OKFValidationError("No OKF bundle found to commit", document_id="bundle", validation_errors=["bundle_missing"])

        relationships = [CanonicalRelationship(**r) for r in agg.state_data.get("relationships", [])]
        unadjudicated_contradictions = [
            r.rel_id for r in relationships if r.rel_type == CanonicalRelationshipType.CONTRADICTORY and not r.adjudicated
        ]

        if unadjudicated_contradictions and not allow_unadjudicated_contradictions:
            raise ContradictionAdjudicationRequiredError(
                f"Cannot commit knowledge with unadjudicated contradiction edges: {unadjudicated_contradictions}",
                contradiction_ids=unadjudicated_contradictions,
            )

        def _work(current_agg: ProgramStateAggregate) -> Dict[str, Any]:
            return dict(current_agg.state_data)

        return self.lifecycle_coordinator.execute_state_phase(
            aggregate_id=aggregate_id,
            transition_name="commit_canonical_knowledge",
            actor_id=ctx.actor_id,
            actor_lane=AuthorityLane.COMMANDER,
            work_fn=_work,
            context=ctx,
            context_claims=["workspace_active", "okf_bundle_valid", "operator_adjudicated"],
            idempotency_key=idempotency_key,
        )

    def retract_canonical_node(
        self,
        aggregate_id: str,
        node_id: str,
        retraction_reason: str,
        context: Optional[TenantContext] = None,
    ) -> CanonicalKnowledgeNode:
        """Retracts an invalid or refuted canonical node (COMMANDER lane)."""
        ctx = context or require_current_tenant_context()
        agg = self.runtime.get_aggregate(aggregate_id)
        if str(ctx.workspace_id) != agg.workspace_id:
            raise WorkspaceScopeViolationError(
                f"Workspace isolation violation: aggregate belongs to '{agg.workspace_id}', context has '{ctx.workspace_id}'",
                expected_workspace_id=agg.workspace_id,
                actual_workspace_id=str(ctx.workspace_id),
            )

        if not retraction_reason or not retraction_reason.strip():
            raise ResearchCanonicalizationProgramError("Retraction reason cannot be empty")

        canonical_nodes = [CanonicalKnowledgeNode(**n) for n in agg.state_data.get("canonical_nodes", [])]
        target_node: Optional[CanonicalKnowledgeNode] = None
        target_idx = -1

        for idx, n in enumerate(canonical_nodes):
            if n.node_id == node_id:
                target_node = n
                target_idx = idx
                break

        if target_node is None:
            raise ResearchCanonicalizationProgramError(f"Canonical node '{node_id}' not found")

        updated_node = target_node.model_copy(
            update={
                "lifecycle_status": "retracted",
                "retraction_reason": retraction_reason,
                "updated_at": utc_now_rfc3339(),
            }
        )
        canonical_nodes[target_idx] = updated_node

        new_state_data = dict(agg.state_data)
        new_state_data["canonical_nodes"] = [n.model_dump() for n in canonical_nodes]
        new_state_hash = _compute_state_hash(
            aggregate_id=agg.aggregate_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            current_state=agg.current_state,
            version=agg.version + 1,
            state_data=new_state_data,
        )
        updated_agg = ProgramStateAggregate(
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            cae_run_id=agg.cae_run_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            current_state=agg.current_state,
            state_data=new_state_data,
            version=agg.version + 1,
            state_hash=new_state_hash,
            lifecycle=agg.lifecycle,
            last_receipt_id=f"rcpt_retract_{node_id}",
            created_at=agg.created_at,
            updated_at=utc_now_rfc3339(),
        )
        self.runtime.store.save_aggregate(updated_agg)

        prev_trace_hash = self.trace_ledger.get_latest_trace_hash(aggregate_id)
        trace = CausalTraceRecord.create(
            cae_run_id=agg.cae_run_id or "run_default",
            program_id=PROGRAM_ID,
            aggregate_id=aggregate_id,
            workspace_id=agg.workspace_id,
            lane=AuthorityLane.COMMANDER,
            actor_id=ctx.actor_id,
            event_type=CausalTraceEventType.RECEIPT_COMMITTED,
            payload={"node_id": node_id, "retraction_reason": retraction_reason},
            receipt_id=f"rec_retract_{node_id}",
            previous_trace_sha256=prev_trace_hash,
        )
        self.trace_ledger.append(trace)

        return updated_node

    def reexpress_canonical_node(
        self,
        aggregate_id: str,
        node_id: str,
        new_definition: str,
        new_label: Optional[str] = None,
        context: Optional[TenantContext] = None,
    ) -> CanonicalKnowledgeNode:
        """Produces a new versioned expression of an existing canonical node with lineage preservation."""
        ctx = context or require_current_tenant_context()
        agg = self.runtime.get_aggregate(aggregate_id)
        if str(ctx.workspace_id) != agg.workspace_id:
            raise WorkspaceScopeViolationError(
                f"Workspace isolation violation: aggregate belongs to '{agg.workspace_id}', context has '{ctx.workspace_id}'",
                expected_workspace_id=agg.workspace_id,
                actual_workspace_id=str(ctx.workspace_id),
            )

        canonical_nodes = [CanonicalKnowledgeNode(**n) for n in agg.state_data.get("canonical_nodes", [])]
        prior_node: Optional[CanonicalKnowledgeNode] = None

        for n in canonical_nodes:
            if n.node_id == node_id:
                prior_node = n
                break

        if prior_node is None:
            raise ResearchCanonicalizationProgramError(f"Node '{node_id}' not found for re-expression")

        if prior_node.lifecycle_status == "retracted":
            raise NodeRetractedError(f"Cannot re-express retracted node '{node_id}'", node_id=node_id)

        new_v = prior_node.version + 1
        resolved_label = new_label or prior_node.canonical_label

        new_lineage = CanonicalKnowledgeNode.compute_lineage_hash(
            canonical_label=resolved_label,
            category=prior_node.category,
            aliases=prior_node.aliases,
            definition=new_definition,
            source_record_refs=prior_node.source_record_refs,
            source_evidence_hashes=prior_node.source_evidence_hashes,
            version=new_v,
            supersedes_node_id=prior_node.node_id,
        )

        idx = canonical_nodes.index(prior_node)
        canonical_nodes[idx] = prior_node.model_copy(update={"lifecycle_status": "superseded"})

        new_node = CanonicalKnowledgeNode(
            node_id=f"{prior_node.node_id}_v{new_v}",
            canonical_label=resolved_label,
            category=prior_node.category,
            aliases=prior_node.aliases,
            definition=new_definition,
            lifecycle_status="active",
            authority_class=prior_node.authority_class,
            source_record_refs=prior_node.source_record_refs,
            source_evidence_hashes=prior_node.source_evidence_hashes,
            lineage_sha256=new_lineage,
            version=new_v,
            supersedes_node_id=prior_node.node_id,
            typed_edges={**prior_node.typed_edges, "supersedes": [prior_node.node_id]},
        )
        canonical_nodes.append(new_node)

        new_state_data = dict(agg.state_data)
        new_state_data["canonical_nodes"] = [n.model_dump() for n in canonical_nodes]
        new_state_hash = _compute_state_hash(
            aggregate_id=agg.aggregate_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            current_state=agg.current_state,
            version=agg.version + 1,
            state_data=new_state_data,
        )
        updated_agg = ProgramStateAggregate(
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            cae_run_id=agg.cae_run_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            current_state=agg.current_state,
            state_data=new_state_data,
            version=agg.version + 1,
            state_hash=new_state_hash,
            lifecycle=agg.lifecycle,
            last_receipt_id=f"rcpt_reexpr_{new_node.node_id}",
            created_at=agg.created_at,
            updated_at=utc_now_rfc3339(),
        )
        self.runtime.store.save_aggregate(updated_agg)

        return new_node

    def repair_canonicalization(
        self,
        aggregate_id: str,
        repair_reason: str,
        context: Optional[TenantContext] = None,
    ) -> ProgramTransitionResult:
        """Recovers from REPAIRING to SOURCES_ATTACHED (COMMANDER lane)."""
        ctx = context or require_current_tenant_context()
        agg = self.runtime.get_aggregate(aggregate_id)
        if str(ctx.workspace_id) != agg.workspace_id:
            raise WorkspaceScopeViolationError(
                f"Workspace isolation violation: aggregate belongs to '{agg.workspace_id}', context has '{ctx.workspace_id}'",
                expected_workspace_id=agg.workspace_id,
                actual_workspace_id=str(ctx.workspace_id),
            )

        def _work(current_agg: ProgramStateAggregate) -> Dict[str, Any]:
            return dict(current_agg.state_data)

        return self.lifecycle_coordinator.execute_state_phase(
            aggregate_id=aggregate_id,
            transition_name="repair_canonicalization",
            actor_id=ctx.actor_id,
            actor_lane=AuthorityLane.COMMANDER,
            work_fn=_work,
            context=ctx,
            context_claims=["workspace_active", "operator_authorized"],
        )

    def export_okf_bundle_to_directory(
        self,
        aggregate_id: str,
        target_dir: str | Path,
    ) -> Path:
        """Exports the full OKF markdown bundle to a target filesystem directory."""
        snapshot = self.get_snapshot(aggregate_id)
        if not snapshot.okf_bundle:
            raise OKFValidationError("No OKF bundle present to export", document_id="bundle", validation_errors=["bundle_none"])

        out_path = Path(target_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        index_file = out_path / "index.md"
        index_file.write_text(snapshot.okf_bundle.index_markdown, encoding="utf-8")

        for doc in snapshot.okf_bundle.documents:
            doc_file = out_path / doc.relative_path
            doc_file.parent.mkdir(parents=True, exist_ok=True)
            doc_file.write_text(doc.markdown, encoding="utf-8")

        return out_path

    def get_snapshot(self, aggregate_id: str) -> ResearchCanonicalizationSnapshot:
        """Returns typed aggregate snapshot."""
        agg = self.runtime.get_aggregate(aggregate_id)
        state_data = agg.state_data

        candidates = [KnowledgeCandidate(**c) for c in state_data.get("candidates", [])]
        relationships = [CanonicalRelationship(**r) for r in state_data.get("relationships", [])]
        canonical_nodes = [CanonicalKnowledgeNode(**n) for n in state_data.get("canonical_nodes", [])]
        bundle_raw = state_data.get("okf_bundle")
        okf_bundle = OKFKnowledgeBundle(**bundle_raw) if bundle_raw else None
        adjudications = [AdjudicationDecision(**a) for a in state_data.get("adjudications", [])]

        return ResearchCanonicalizationSnapshot(
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            state=agg.current_state,
            version=agg.version,
            source_records=state_data.get("source_records", []),
            candidates=candidates,
            relationships=relationships,
            canonical_nodes=canonical_nodes,
            okf_bundle=okf_bundle,
            adjudications=adjudications,
            state_hash=agg.state_hash,
            updated_at=agg.updated_at,
        )
