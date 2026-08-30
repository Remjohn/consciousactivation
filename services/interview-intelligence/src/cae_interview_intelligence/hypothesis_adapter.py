"""
hypothesis_adapter.py
---------------------
Derived hypothesis candidate adapter and diversity-aware working selection (CAE-M02).

This module implements the non-canonical candidate adapter that bridges upstream
AIR hypothesis/portfolio authority into the Interview Program candidate field (~96 -> 16-24).
It enforces strict provenance and evidence lineage, provides multidimensional diversity-aware
clustering and portfolio selection, and operates in read-only accordance with existing AIR authority.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field, field_validator


class CandidateState(str, Enum):
    DISCOVERED = "DISCOVERED"
    EVALUATED = "EVALUATED"
    SELECTED = "SELECTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    DEFERRED = "DEFERRED"
    LOCKED = "LOCKED"



class SemanticRef(BaseModel):
    """
    Validated cryptographic/URI reference structure for upstream authoritative objects.
    Ensures that references pointing to AIR objects, world signals, or registries are well-formed.
    """
    object_id: str = Field(..., min_length=3, description="Canonical or semantic object identifier")
    version: Optional[str] = Field(None, description="Object version string or semver")
    sha256: Optional[str] = Field(None, min_length=8, description="Cryptographic hash digest for integrity")
    object_type: Optional[str] = Field(None, description="Authoritative object type name")
    uri: Optional[str] = Field(None, description="Logical URI or resource path")

    @field_validator("object_id")
    @classmethod
    def validate_object_id(cls, v: str) -> str:
        s = v.strip()
        if not s or s.lower() in ("null", "none", "undefined", "invalid"):
            raise ValueError(f"SemanticRef object_id cannot be blank or invalid placeholder: {v!r}")
        return s

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SemanticRef:
        return cls(
            object_id=str(data.get("object_id") or data.get("id") or ""),
            version=data.get("version"),
            sha256=data.get("sha256"),
            object_type=data.get("object_type"),
            uri=data.get("uri"),
        )


class Provenance(BaseModel):
    """Immutable audit trail for candidate derivation."""
    source_refs: List[SemanticRef] = Field(default_factory=list, description="Upstream source object refs")
    audit_refs: List[SemanticRef] = Field(default_factory=list, description="Linked audit or evaluation receipts")
    generated_by: str = Field("cae-interview-intelligence:hypothesis-adapter:v3", description="Derivation engine version")
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Generation timestamp")


class SelectionDiagnostics(BaseModel):
    """
    Advisory, non-compensable scoring diagnostics.
    Used for diversity sorting and cluster ranking, never as sole proof of truth.
    """
    relevance: float = Field(0.5, ge=0.0, le=1.0)
    evidence_potential: float = Field(0.5, ge=0.0, le=1.0)
    guest_authority: float = Field(0.5, ge=0.0, le=1.0)
    audience_alignment: float = Field(0.5, ge=0.0, le=1.0)
    collision_strength: float = Field(0.5, ge=0.0, le=1.0)
    novelty: float = Field(0.5, ge=0.0, le=1.0)
    downstream_compatibility: float = Field(0.5, ge=0.0, le=1.0)
    research_grounding: float = Field(0.5, ge=0.0, le=1.0)
    distinctiveness: float = Field(0.5, ge=0.0, le=1.0)
    risk: float = Field(0.0, ge=0.0, le=1.0)
    portfolio_overlap: float = Field(0.0, ge=0.0, le=1.0)

    @property
    def composite_quality_score(self) -> float:
        """Advisory composite score penalizing risk and duplicate overlap."""
        positive_weight = (
            self.relevance * 0.15 +
            self.evidence_potential * 0.20 +
            self.guest_authority * 0.15 +
            self.audience_alignment * 0.10 +
            self.collision_strength * 0.15 +
            self.novelty * 0.10 +
            self.research_grounding * 0.15
        )
        penalty = (self.risk * 0.25) + (self.portfolio_overlap * 0.35)
        return max(0.0, min(1.0, positive_weight - penalty))


class CoordinateBasis(BaseModel):
    """
    The 12-Dimensional coordinate basis per CAE Hypothesis Coordinate Spec.
    Represents semantic vectors without creating a redundant database ontology.
    """
    d01_audience_tension: Optional[str] = Field(None, description="Active pressure or unresolved audience condition")
    d02_audience_belief: Optional[str] = Field(None, description="Organizing cognitive island or mental schema")
    d03_audience_desired_state: Optional[str] = Field(None, description="Desired relief, shift, or capability")
    d04_guest_lived_authority: Optional[str] = Field(None, description="Lived territory backing guest legitimacy")
    d05_guest_contradiction: Optional[str] = Field(None, description="Tension in guest past/present stance or behavior")
    d06_guest_transformation: Optional[str] = Field(None, description="Meaningful transformation across time")
    d07_cultural_world_signal: Optional[str] = Field(None, description="External macro signal, event, or discourse")
    d08_target_enemy_status_quo: Optional[str] = Field(None, description="Default paradigm or assumption under pressure")
    d09_oblique_lens: Optional[str] = Field(None, description="Cross-domain mental model or structural invariant")
    d10_archetype_opportunity: Optional[str] = Field(None, description="Candidate downstream content archetype")
    d11_distribution_condition: Optional[str] = Field(None, description="Syntax or distribution context")
    d12_evidence_opportunity: Optional[str] = Field(None, description="Concrete proof or receipt that could resolve collision")


class HypothesisCandidate(BaseModel):
    """
    Derived, non-canonical candidate representation combining coordinate collision data,
    upstream AIR references, selection diagnostics, and lineage.
    """
    candidate_id: str = Field(default_factory=lambda: f"hc:{uuid.uuid4().hex[:12]}")
    collision_statement: str = Field(..., min_length=10, description="The testable thesis uniting guest authority and audience tension")
    
    # Upstream Authority Linkage
    upstream_hypothesis_refs: List[SemanticRef] = Field(
        default_factory=list,
        description="References to authoritative AIR activation_hypothesis or portfolio objects",
    )
    coordinate_refs: List[SemanticRef] = Field(default_factory=list, description="Explicit coordinate object/registry refs")
    coordinates: CoordinateBasis = Field(default_factory=CoordinateBasis, description="12-D coordinate values")
    
    # Semantic Anchors
    audience_cognitive_island_ref: Optional[SemanticRef] = None
    guest_territory_ref: Optional[SemanticRef] = None
    world_signal_refs: List[SemanticRef] = Field(default_factory=list)
    edge_ref: Optional[SemanticRef] = None
    target_paradigm: Optional[str] = None
    expected_discrepancy: Optional[str] = None
    desired_evidence: List[str] = Field(default_factory=list)
    
    # Downstream Compatibility
    question_objective_ref: Optional[SemanticRef] = None
    mechanism_refs: List[SemanticRef] = Field(default_factory=list)
    archetype_refs: List[SemanticRef] = Field(default_factory=list)
    format_refs: List[SemanticRef] = Field(default_factory=list)
    narrative_role_refs: List[SemanticRef] = Field(default_factory=list)
    distribution_condition: Optional[str] = None
    
    # Scoring & Lineage
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    selection_diagnostics: SelectionDiagnostics = Field(default_factory=SelectionDiagnostics)
    provenance: Provenance = Field(default_factory=Provenance)
    state: CandidateState = Field(default=CandidateState.DISCOVERED)
    operator_notes: Optional[str] = None

    def validate_upstream_refs(self) -> bool:
        """Validates that candidate has at least one valid, non-blank upstream reference or source reference."""
        has_upstream = any(bool(r.object_id.strip()) for r in self.upstream_hypothesis_refs)
        has_source = any(bool(r.object_id.strip()) for r in self.provenance.source_refs)
        return has_upstream or has_source

    def get_diversity_signature(self) -> Dict[str, str]:
        """Extracts categorical diversity coordinates for cluster and diversity selection."""
        return {
            "audience_island": (
                self.audience_cognitive_island_ref.object_id
                if self.audience_cognitive_island_ref
                else (self.coordinates.d02_audience_belief or "general_audience")
            ),
            "tension": (
                self.edge_ref.object_id
                if self.edge_ref
                else (self.coordinates.d01_audience_tension or "core_tension")
            ),
            "guest_territory": (
                self.guest_territory_ref.object_id
                if self.guest_territory_ref
                else (self.coordinates.d04_guest_lived_authority or "general_authority")
            ),
            "target_paradigm": self.target_paradigm or self.coordinates.d08_target_enemy_status_quo or "status_quo",
            "archetype": (
                self.archetype_refs[0].object_id
                if self.archetype_refs
                else (self.coordinates.d10_archetype_opportunity or "general_archetype")
            ),
        }

    def compute_semantic_hash(self) -> str:
        """Deterministic fingerprint of core semantic coordinates for duplicate detection."""
        sig = self.get_diversity_signature()
        norm_text = " ".join(self.collision_statement.strip().lower().split())
        data = f"{sig['audience_island']}|{sig['tension']}|{sig['guest_territory']}|{sig['target_paradigm']}|{norm_text}"
        return hashlib.sha256(data.encode("utf-8")).hexdigest()[:16]


class CandidateCluster(BaseModel):
    """Grouping of semantically overlapping or duplicate candidates."""
    cluster_id: str = Field(default_factory=lambda: f"cl:{uuid.uuid4().hex[:8]}")
    cluster_key: str = Field(..., description="Semantic cluster key / signature")
    primary_candidate_id: str = Field(..., description="Representative candidate with highest quality score")
    candidate_ids: List[str] = Field(default_factory=list, description="All candidates grouped in this cluster")
    overlap_score: float = Field(0.0, ge=0.0, le=1.0, description="Average pairwise coordinate overlap")
    diversity_signature: Dict[str, str] = Field(default_factory=dict)


class PortfolioSelectionResult(BaseModel):
    """Result of diversity-aware working portfolio selection (~96 -> 16-24)."""
    selected_candidates: List[HypothesisCandidate] = Field(default_factory=list)
    rejected_candidates: List[HypothesisCandidate] = Field(default_factory=list)
    deferred_candidates: List[HypothesisCandidate] = Field(default_factory=list)
    clusters: List[CandidateCluster] = Field(default_factory=list)
    
    total_pool_evaluated: int = 0
    selected_count: int = 0
    diversity_coverage: Dict[str, int] = Field(
        default_factory=dict,
        description="Counts of unique dimensions covered (e.g. distinct cognitive islands, tensions, territories)",
    )
    evidence_insufficiency_warning: Optional[str] = None
    selection_rationale: Dict[str, Any] = Field(default_factory=dict)


class HypothesisPortfolioAdapter:
    """
    Adapter and evaluation engine for candidate hypothesis portfolios.
    Enforces reference integrity, performs semantic clustering, and executes
    diversity-maximizing selection targeting 16-24 candidates without artificial quotas.
    """

    def __init__(self, cluster_similarity_threshold: float = 0.75):
        self.cluster_similarity_threshold = cluster_similarity_threshold

    def validate_candidate(self, candidate: HypothesisCandidate) -> List[str]:
        """
        Validates candidate structural integrity.
        Returns a list of validation failure reasons (empty if valid).
        """
        errors: List[str] = []
        if not candidate.collision_statement or len(candidate.collision_statement.strip()) < 10:
            errors.append("collision_statement is missing or shorter than 10 characters")
        if not candidate.validate_upstream_refs():
            errors.append("candidate has no valid upstream_hypothesis_refs or provenance.source_refs")
        return errors

    def cluster_candidates(self, candidates: List[HypothesisCandidate]) -> List[CandidateCluster]:
        """
        Groups candidates by semantic coordinates and collision thesis overlap.
        Detects near-duplicates and calculates intra-cluster overlap scores.
        """
        cluster_map: Dict[str, List[HypothesisCandidate]] = {}
        
        for cand in candidates:
            sig = cand.get_diversity_signature()
            # Primary grouping by core tension + audience cognitive island + guest territory
            key = f"{sig['audience_island']}:::{sig['tension']}:::{sig['guest_territory']}"
            cluster_map.setdefault(key, []).append(cand)
            
        clusters: List[CandidateCluster] = []
        for key, group in cluster_map.items():
            # Sort within cluster by composite quality score descending
            sorted_group = sorted(
                group,
                key=lambda c: c.selection_diagnostics.composite_quality_score,
                reverse=True,
            )
            primary = sorted_group[0]
            
            # Update portfolio overlap penalty for non-primary members
            overlap_val = 0.0 if len(group) == 1 else min(1.0, 0.35 + (len(group) - 1) * 0.15)
            for idx, c in enumerate(sorted_group):
                if idx > 0:
                    c.selection_diagnostics.portfolio_overlap = overlap_val
            
            cluster = CandidateCluster(
                cluster_key=key,
                primary_candidate_id=primary.candidate_id,
                candidate_ids=[c.candidate_id for c in sorted_group],
                overlap_score=overlap_val,
                diversity_signature=primary.get_diversity_signature(),
            )
            clusters.append(cluster)
            
        return clusters

    def select_working_portfolio(
        self,
        candidates: List[HypothesisCandidate],
        target_min: int = 16,
        target_max: int = 24,
        force_strict_quota: bool = False,
    ) -> PortfolioSelectionResult:
        """
        Selects a working hypothesis portfolio maximizing multidimensional diversity.
        
        Rules:
        - Validates all candidates; rejects structurally invalid ones.
        - Clusters duplicates/near-duplicates and penalizes redundant selection.
        - Prioritizes covering all distinct cognitive islands, tensions, and guest territories.
        - Targets 16-24 candidates, but accepts smaller portfolios (<16) when evidence is sparse,
          reporting an evidence insufficiency warning instead of throwing arbitrary errors.
        - Never mutates AIR-owned upstream objects.
        """
        total_pool = len(candidates)
        valid_candidates: List[HypothesisCandidate] = []
        rejected_candidates: List[HypothesisCandidate] = []
        
        # 1. Validation phase
        for c in candidates:
            val_errors = self.validate_candidate(c)
            if val_errors:
                c.state = CandidateState.REJECTED
                c.operator_notes = f"Validation failed: {'; '.join(val_errors)}"
                rejected_candidates.append(c)
            else:
                valid_candidates.append(c)
                
        # 2. Clustering phase
        clusters = self.cluster_candidates(valid_candidates)
        
        # 3. Diversity-aware selection algorithm
        # Iteratively selects candidates maximizing marginal diversity across coordinates
        selected: List[HypothesisCandidate] = []
        deferred: List[HypothesisCandidate] = []
        
        covered_islands: Set[str] = set()
        covered_tensions: Set[str] = set()
        covered_territories: Set[str] = set()
        covered_archetypes: Set[str] = set()
        
        available_cands = list(valid_candidates)
        
        while available_cands and len(selected) < target_max:
            best_cand: Optional[HypothesisCandidate] = None
            best_score = -9999.0
            
            for cand in available_cands:
                sig = cand.get_diversity_signature()
                
                # Marginal diversity bonus for uncovered dimensions
                div_bonus = 0.0
                if sig["audience_island"] not in covered_islands:
                    div_bonus += 1.5
                if sig["tension"] not in covered_tensions:
                    div_bonus += 1.2
                if sig["guest_territory"] not in covered_territories:
                    div_bonus += 1.0
                if sig["archetype"] not in covered_archetypes:
                    div_bonus += 0.8
                
                quality = cand.selection_diagnostics.composite_quality_score
                
                # Overlap penalty if tension + island are already covered in selected set
                overlap_penalty = 0.0
                if sig["audience_island"] in covered_islands and sig["tension"] in covered_tensions:
                    overlap_penalty = 0.5
                    
                total_cand_score = div_bonus + (quality * 0.5) - overlap_penalty
                
                if total_cand_score > best_score:
                    best_score = total_cand_score
                    best_cand = cand
                    
            if best_cand is None:
                break
                
            available_cands.remove(best_cand)
            best_cand.state = CandidateState.SELECTED
            selected.append(best_cand)
            
            sig = best_cand.get_diversity_signature()
            covered_islands.add(sig["audience_island"])
            covered_tensions.add(sig["tension"])
            covered_territories.add(sig["guest_territory"])
            covered_archetypes.add(sig["archetype"])
            
        for rem in available_cands:
            rem.state = CandidateState.DEFERRED
            deferred.append(rem)

                    
        # Check for evidence insufficiency
        insufficiency_warning: Optional[str] = None
        if len(selected) < target_min:
            msg = (
                f"Candidate pool density insufficient: selected {len(selected)} candidates "
                f"(target range: {target_min}-{target_max}). Proceeding with available evidence without artificial padding."
            )
            if force_strict_quota:
                raise ValueError(msg)
            insufficiency_warning = msg
            
        coverage_metrics = {
            "unique_audience_islands": len(covered_islands),
            "unique_tensions": len(covered_tensions),
            "unique_guest_territories": len(covered_territories),
            "unique_archetypes": len(covered_archetypes),
            "total_clusters": len(clusters),
        }
        
        return PortfolioSelectionResult(
            selected_candidates=selected,
            rejected_candidates=rejected_candidates,
            deferred_candidates=deferred,
            clusters=clusters,
            total_pool_evaluated=total_pool,
            selected_count=len(selected),
            diversity_coverage=coverage_metrics,
            evidence_insufficiency_warning=insufficiency_warning,
            selection_rationale={
                "algorithm": "multidimensional_diversity_greedy",
                "target_range": f"{target_min}-{target_max}",
                "clusters_formed": len(clusters),
                "cluster_overlap_penalties_applied": sum(1 for cl in clusters if len(cl.candidate_ids) > 1),
            },
        )
