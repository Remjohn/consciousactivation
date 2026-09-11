"""
CAE Interview Program — Content Menu Readiness (Mandate M10)

Produces an Operator-reviewable content candidate menu from authenticated evidence
without quota forcing (FR-IP-010).

Each candidate preserves:
  - source hypothesis;
  - supporting evidence refs;
  - semantic role;
  - response structure;
  - archetype/format compatibility;
  - confidence/diagnostics;
  - provenance;
  - any missing evidence required before production.

Quantity rule:
  ~32 is a planning aspiration, not a quota. One hypothesis can yield multiple
  viable pieces; another may yield none.

Operator role:
  The system may rank and cluster. The Operator selects production-worthy candidates.
  Distribution performance must not compensate for semantic failure.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set

from pydantic import BaseModel, Field

try:
    from ca_contracts import canonical_sha256
except ImportError:
    def canonical_sha256(payload: Any) -> str:
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

from conscious_activations_interview_composer.errors import ConflictError, NotFoundError, ValidationError

from .composition_compatibility import (
    KNOWN_ARCHETYPES,
    KNOWN_FORMATS,
    KNOWN_NARRATIVE_ROLES,
    CompositionCompatibilityEvaluator,
)
from .evidence_handoff import (
    AcceptedEvidenceRecord,
    AuthenticatedEvidencePackage,
    DownstreamContentCandidate,
    LineageTraceNode,
    SourceReference,
)
from .hypothesis_adapter import CoordinateBasis, HypothesisCandidate, Provenance, SemanticRef
from .question_resolver import (
    AnswerResolution,
    CompositionCompatibility,
    EvidenceMode,
    QuestionCandidate,
    SocialReferenceFrame,
    TemporalOrientation,
)
from .semantic_acquisition import (
    AcquisitionEvidenceRecord,
    DiscrepancyRecord,
    EvidenceLineageKind,
    SemanticAcquisitionObservation,
)


# -----------------------------------------------------------------------------
# 1. Menu Status & Diagnostics
# -----------------------------------------------------------------------------

class ContentCandidateMenuStatus(str, Enum):
    """
    Lifecycle status of a content candidate item within the Operator Content Menu.
    """
    DISCOVERED = "discovered"
    EVALUATED = "evaluated"
    OPERATOR_SELECTED = "operator_selected"
    REJECTED = "rejected"
    DEFICIENT_EVIDENCE = "deficient_evidence"


class MenuCandidateDiagnostics(BaseModel):
    """
    Diagnostic analysis evaluating semantic grounding, authenticity, and readiness.
    """
    semantic_grounding_score: float = Field(default=0.8, ge=0.0, le=1.0)
    authenticity_score: float = Field(default=0.8, ge=0.0, le=1.0)
    is_generic_slop: bool = Field(default=False)
    evidence_count: int = Field(default=1, ge=0)
    archetype_compatible: bool = Field(default=True)
    format_compatible: bool = Field(default=True)
    missing_evidence_required: List[str] = Field(default_factory=list)
    rejection_reasons: List[str] = Field(default_factory=list)
    compatibility_notes: List[str] = Field(default_factory=list)


# -----------------------------------------------------------------------------
# 2. Menu Item & Cluster
# -----------------------------------------------------------------------------

class MenuCandidateItem(BaseModel):
    """
    Individual reviewable content candidate entry in the Operator Content Menu.
    """
    menu_item_id: str = Field(default_factory=lambda: f"cmi:{uuid.uuid4().hex[:10]}")
    downstream_candidate_ref: SemanticRef = Field(...)
    title: str = Field(..., min_length=5)
    core_narrative_claim: str = Field(..., min_length=10)
    source_hypothesis_ref: SemanticRef = Field(...)
    supporting_evidence_refs: List[SemanticRef] = Field(..., min_length=1)
    target_archetype: str = Field(...)
    target_format: str = Field(...)
    target_narrative_role: str = Field(...)
    observed_response_structure: List[str] = Field(default_factory=list)
    required_response_structure: List[str] = Field(default_factory=list)
    diagnostics: MenuCandidateDiagnostics = Field(default_factory=MenuCandidateDiagnostics)
    status: ContentCandidateMenuStatus = Field(default=ContentCandidateMenuStatus.EVALUATED)
    operator_selection_notes: Optional[str] = Field(None)
    operator_decision_timestamp_utc: Optional[datetime] = Field(None)
    workspace_id: str = Field(..., min_length=3)
    project_id: str = Field(..., min_length=3)
    provenance: Provenance = Field(default_factory=Provenance)


class ContentMenuCluster(BaseModel):
    """
    Logical grouping of content candidates around a shared hypothesis root or narrative theme.
    """
    cluster_id: str = Field(default_factory=lambda: f"cmc:{uuid.uuid4().hex[:10]}")
    hypothesis_ref: SemanticRef = Field(...)
    cluster_theme: str = Field(..., min_length=3)
    candidates: List[MenuCandidateItem] = Field(default_factory=list)

    @property
    def viable_count(self) -> int:
        return sum(1 for c in self.candidates if c.status != ContentCandidateMenuStatus.DEFICIENT_EVIDENCE and not c.diagnostics.is_generic_slop)


# -----------------------------------------------------------------------------
# 3. Content Candidate Menu
# -----------------------------------------------------------------------------

class ContentCandidateMenu(BaseModel):
    """
    Top-level Operator-reviewable Content Candidate Menu.
    Preserves all candidates, clusters, diagnostics, and cryptographic manifest SHA-256.
    """
    menu_id: str = Field(default_factory=lambda: f"menu:{uuid.uuid4().hex[:10]}")
    session_ref: SemanticRef = Field(...)
    brief_ref: SemanticRef = Field(...)
    workspace_id: str = Field(..., min_length=3)
    project_id: str = Field(..., min_length=3)
    total_candidates: int = Field(0)
    viable_candidates_count: int = Field(0)
    selected_candidates_count: int = Field(0)
    rejected_candidates_count: int = Field(0)
    clusters: List[ContentMenuCluster] = Field(default_factory=list)
    unclustered_candidates: List[MenuCandidateItem] = Field(default_factory=list)
    menu_manifest_sha256: str = Field("")
    created_at_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def compute_manifest_hash(self) -> str:
        """Computes deterministic SHA256 across all menu candidates and clusters."""
        all_items: List[Dict[str, Any]] = []
        for cl in self.clusters:
            for item in cl.candidates:
                all_items.append({
                    "menu_item_id": item.menu_item_id,
                    "candidate_id": item.downstream_candidate_ref.object_id,
                    "status": item.status.value,
                    "archetype": item.target_archetype,
                    "format": item.target_format,
                })
        for item in self.unclustered_candidates:
            all_items.append({
                "menu_item_id": item.menu_item_id,
                "candidate_id": item.downstream_candidate_ref.object_id,
                "status": item.status.value,
                "archetype": item.target_archetype,
                "format": item.target_format,
            })
        payload = {
            "menu_id": self.menu_id,
            "session_ref": self.session_ref.model_dump(),
            "brief_ref": self.brief_ref.model_dump(),
            "workspace_id": self.workspace_id,
            "project_id": self.project_id,
            "items": sorted(all_items, key=lambda x: x["menu_item_id"]),
        }
        return canonical_sha256(payload)


# -----------------------------------------------------------------------------
# 4. Content Menu Readiness Engine
# -----------------------------------------------------------------------------

class ContentMenuReadinessEngine:
    """
    Processes authenticated evidence packages into an Operator-reviewable Content Candidate Menu.
    Enforces anti-fabrication rules, rejects ungrounded generic material, flags unsupported
    archetypes, and allows multi-format generation without quota forcing.
    """

    def __init__(self, evaluator: Optional[CompositionCompatibilityEvaluator] = None):
        self.evaluator = evaluator or CompositionCompatibilityEvaluator()

    def generate_menu(
        self,
        evidence_package: AuthenticatedEvidencePackage,
        min_grounding_score: float = 0.6,
    ) -> ContentCandidateMenu:
        """
        Builds the ContentCandidateMenu from an AuthenticatedEvidencePackage.
        Does NOT force quotas: heterogeneous hypotheses can yield 0 or multiple viable candidates.
        """
        # Map evidence records by ID for fast lookup
        evidence_map: Dict[str, AcceptedEvidenceRecord] = {
            ev.evidence_id: ev for ev in evidence_package.accepted_evidence
        }

        # Group candidates by upstream hypothesis ID
        hypothesis_candidate_map: Dict[str, List[MenuCandidateItem]] = {}
        unclustered: List[MenuCandidateItem] = []

        total_candidates = len(evidence_package.content_candidates)
        viable_count = 0

        for cand in evidence_package.content_candidates:
            # Gather associated evidence records
            matched_evidence: List[AcceptedEvidenceRecord] = []
            for ev_ref in cand.source_evidence_refs:
                if ev_ref.object_id in evidence_map:
                    matched_evidence.append(evidence_map[ev_ref.object_id])

            # Invariant: No candidate without evidence lineage
            if not matched_evidence:
                raise ValidationError(
                    f"no production candidate appears without evidence lineage: candidate '{cand.candidate_id}' has no matching evidence records."
                )

            # Extract observed response structures
            observed_structure: Set[str] = set()
            for ev in matched_evidence:
                for s in ev.response_structure_present:
                    observed_structure.add(s.strip().lower())

            # Evaluate archetype compatibility
            archetype_key = cand.target_archetype_ref.object_id.upper()
            archetype_spec = KNOWN_ARCHETYPES.get(archetype_key)
            required_structure: List[str] = archetype_spec.required_response_shape if archetype_spec else []

            missing_reqs = [
                req for req in required_structure if req.strip().lower() not in observed_structure
            ]

            # Check for generic/slop characteristics
            is_generic = False
            rejection_reasons: List[str] = []
            compatibility_notes: List[str] = list(cand.readiness_notes)

            # If evidence has empty extracted statements or short vague claims, flag as generic slop
            total_statement_len = sum(len(ev.extracted_statement) for ev in matched_evidence)
            if total_statement_len < 20 or any("generic" in ev.extracted_statement.lower() for ev in matched_evidence):
                is_generic = True
                rejection_reasons.append("Flagged as generic fluent material with insufficient empirical grounding.")

            if missing_reqs:
                compatibility_notes.append(
                    f"Unsupported archetype structure: missing required elements {missing_reqs} for '{archetype_key}'"
                )

            # Determine status
            if is_generic:
                status = ContentCandidateMenuStatus.DEFICIENT_EVIDENCE
            elif missing_reqs:
                status = ContentCandidateMenuStatus.DEFICIENT_EVIDENCE
            else:
                status = ContentCandidateMenuStatus.EVALUATED
                viable_count += 1

            diagnostics = MenuCandidateDiagnostics(
                semantic_grounding_score=0.4 if is_generic else (0.7 if missing_reqs else 0.9),
                authenticity_score=0.3 if is_generic else 0.85,
                is_generic_slop=is_generic,
                evidence_count=len(matched_evidence),
                archetype_compatible=len(missing_reqs) == 0,
                format_compatible=True,
                missing_evidence_required=missing_reqs,
                rejection_reasons=rejection_reasons,
                compatibility_notes=compatibility_notes,
            )

            primary_hyp_ref = cand.upstream_hypothesis_refs[0] if cand.upstream_hypothesis_refs else SemanticRef(object_id="unknown_hyp", object_type="hypothesis")

            menu_item = MenuCandidateItem(
                menu_item_id=f"cmi:{uuid.uuid4().hex[:10]}",
                downstream_candidate_ref=SemanticRef(object_id=cand.candidate_id, object_type="downstream_content_candidate"),
                title=cand.title,
                core_narrative_claim=cand.core_narrative_claim,
                source_hypothesis_ref=primary_hyp_ref,
                supporting_evidence_refs=cand.source_evidence_refs,
                target_archetype=archetype_key,
                target_format=cand.target_format_ref.object_id,
                target_narrative_role=cand.target_narrative_role_ref.object_id,
                observed_response_structure=sorted(list(observed_structure)),
                required_response_structure=required_structure,
                diagnostics=diagnostics,
                status=status,
                workspace_id=evidence_package.workspace_id,
                project_id=evidence_package.project_id,
                provenance=cand.provenance,
            )

            hyp_id = primary_hyp_ref.object_id
            if hyp_id not in hypothesis_candidate_map:
                hypothesis_candidate_map[hyp_id] = []
            hypothesis_candidate_map[hyp_id].append(menu_item)

        # Build clusters
        clusters: List[ContentMenuCluster] = []
        for hyp_id, items in hypothesis_candidate_map.items():
            first_item = items[0]
            clusters.append(ContentMenuCluster(
                cluster_id=f"cmc:{uuid.uuid4().hex[:10]}",
                hypothesis_ref=first_item.source_hypothesis_ref,
                cluster_theme=f"Hypothesis Cluster: {hyp_id}",
                candidates=items,
            ))

        menu = ContentCandidateMenu(
            session_ref=evidence_package.session_ref,
            brief_ref=evidence_package.brief_ref,
            workspace_id=evidence_package.workspace_id,
            project_id=evidence_package.project_id,
            total_candidates=total_candidates,
            viable_candidates_count=viable_count,
            selected_candidates_count=0,
            rejected_candidates_count=0,
            clusters=clusters,
            unclustered_candidates=unclustered,
        )
        menu.menu_manifest_sha256 = menu.compute_manifest_hash()
        return menu

    def operator_select_candidate(
        self,
        menu: ContentCandidateMenu,
        menu_item_id: str,
        operator_id: str,
        notes: Optional[str] = None,
    ) -> ContentCandidateMenu:
        """
        Authoritative Operator selection of a production-worthy candidate.
        Rejects selecting candidates with deficient evidence or missing lineage.
        """
        if not operator_id or not operator_id.strip():
            raise ValidationError("Operator authorization required for candidate selection.")

        target_item: Optional[MenuCandidateItem] = None
        for cl in menu.clusters:
            for item in cl.candidates:
                if item.menu_item_id == menu_item_id:
                    target_item = item
                    break

        if not target_item:
            for item in menu.unclustered_candidates:
                if item.menu_item_id == menu_item_id:
                    target_item = item
                    break

        if not target_item:
            raise NotFoundError(f"Menu item '{menu_item_id}' not found in ContentCandidateMenu.")

        # Invariant: Distribution performance must not compensate for semantic failure
        if target_item.diagnostics.is_generic_slop:
            raise ValidationError(
                f"Cannot select candidate '{menu_item_id}': flagged as generic fluent material with insufficient evidence grounding."
            )
        if not target_item.diagnostics.archetype_compatible:
            raise ValidationError(
                f"Cannot select candidate '{menu_item_id}': unsupported archetype missing {target_item.diagnostics.missing_evidence_required}."
            )
        if not target_item.supporting_evidence_refs:
            raise ValidationError(f"Cannot select candidate '{menu_item_id}': missing supporting evidence lineage.")

        target_item.status = ContentCandidateMenuStatus.OPERATOR_SELECTED
        target_item.operator_selection_notes = notes
        target_item.operator_decision_timestamp_utc = datetime.now(timezone.utc)
        target_item.provenance.source_refs.append(
            SemanticRef(object_id=f"op:{operator_id.strip()}", object_type="operator_authorization")
        )

        menu.selected_candidates_count = sum(
            1 for cl in menu.clusters for c in cl.candidates if c.status == ContentCandidateMenuStatus.OPERATOR_SELECTED
        ) + sum(1 for c in menu.unclustered_candidates if c.status == ContentCandidateMenuStatus.OPERATOR_SELECTED)

        menu.menu_manifest_sha256 = menu.compute_manifest_hash()
        return menu

    def operator_reject_candidate(
        self,
        menu: ContentCandidateMenu,
        menu_item_id: str,
        operator_id: str,
        reason: str,
    ) -> ContentCandidateMenu:
        """
        Authoritative Operator rejection of a candidate with mandatory rejection reason.
        """
        if not operator_id or not operator_id.strip():
            raise ValidationError("Operator authorization required for candidate rejection.")
        if not reason or not reason.strip():
            raise ValidationError("Rejection reason required for candidate rejection.")

        target_item: Optional[MenuCandidateItem] = None
        for cl in menu.clusters:
            for item in cl.candidates:
                if item.menu_item_id == menu_item_id:
                    target_item = item
                    break

        if not target_item:
            for item in menu.unclustered_candidates:
                if item.menu_item_id == menu_item_id:
                    target_item = item
                    break

        if not target_item:
            raise NotFoundError(f"Menu item '{menu_item_id}' not found in ContentCandidateMenu.")

        target_item.status = ContentCandidateMenuStatus.REJECTED
        target_item.diagnostics.rejection_reasons.append(reason.strip())
        target_item.operator_selection_notes = reason.strip()
        target_item.operator_decision_timestamp_utc = datetime.now(timezone.utc)

        menu.rejected_candidates_count = sum(
            1 for cl in menu.clusters for c in cl.candidates if c.status == ContentCandidateMenuStatus.REJECTED
        ) + sum(1 for c in menu.unclustered_candidates if c.status == ContentCandidateMenuStatus.REJECTED)

        menu.menu_manifest_sha256 = menu.compute_manifest_hash()
        return menu

    def _sanitize_for_canonical(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: self._sanitize_for_canonical(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._sanitize_for_canonical(item) for item in obj]
        elif isinstance(obj, float):
            return f"{obj:.4f}"
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Enum):
            return obj.value
        return obj

    def export_production_manifest(self, menu: ContentCandidateMenu) -> Dict[str, Any]:
        """
        Exports the verified downstream production manifest containing only OPERATOR_SELECTED candidates.
        Preserves full provenance and cryptographic manifest hash.
        """
        selected_candidates: List[Dict[str, Any]] = []
        for cl in menu.clusters:
            for item in cl.candidates:
                if item.status == ContentCandidateMenuStatus.OPERATOR_SELECTED:
                    selected_candidates.append({
                        "menu_item_id": item.menu_item_id,
                        "downstream_candidate_id": item.downstream_candidate_ref.object_id,
                        "title": item.title,
                        "core_narrative_claim": item.core_narrative_claim,
                        "source_hypothesis": item.source_hypothesis_ref.model_dump(),
                        "supporting_evidence_refs": [ref.model_dump() for ref in item.supporting_evidence_refs],
                        "target_archetype": item.target_archetype,
                        "target_format": item.target_format,
                        "target_narrative_role": item.target_narrative_role,
                        "observed_response_structure": item.observed_response_structure,
                        "diagnostics": item.diagnostics.model_dump(),
                        "operator_notes": item.operator_selection_notes,
                        "provenance": item.provenance.model_dump(),
                    })

        manifest = {
            "menu_id": menu.menu_id,
            "session_ref": menu.session_ref.model_dump(),
            "brief_ref": menu.brief_ref.model_dump(),
            "workspace_id": menu.workspace_id,
            "project_id": menu.project_id,
            "selected_count": len(selected_candidates),
            "selected_production_candidates": selected_candidates,
            "exported_at_utc": datetime.now(timezone.utc).isoformat(),
            "menu_manifest_sha256": menu.menu_manifest_sha256,
        }
        sanitized_manifest = self._sanitize_for_canonical(manifest)
        manifest["production_manifest_sha256"] = canonical_sha256(sanitized_manifest)
        return manifest
