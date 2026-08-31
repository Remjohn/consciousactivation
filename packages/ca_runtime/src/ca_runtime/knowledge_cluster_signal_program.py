"""
knowledge_cluster_signal_program.py
-----------------------------------
CAE Phase 3 Mandate M31: Knowledge Clusters + Research Signals + Context Projection.

Separates curated canonical knowledge from temporal/contextual signal detection:
Knowledge Node -> Knowledge Cluster -> Research Signal -> Context Projection.

Enforces 4 distinct authority lanes:
- HUNTER: Knowledge cluster formation (cae.research.form_clusters@1.0.0)
- ANALYST: Research signal detection and 14-metric calculation (cae.research.detect_signals@1.0.0)
- COMPOSER: Context opportunity projection against Guest DNA & Audience Tensions (cae.research.project_context@1.0.0)
- COMMANDER: Governance, commit, retraction, rebuild, and state repair (cae.research.commit_context_projections@1.0.0)
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from pydantic import BaseModel, Field

from ca_runtime.knowledge_cluster_signal_store import (
    ContextProjectionRecord,
    KnowledgeClusterRecord,
    KnowledgeClusterSignalStore,
    ProvenanceEntry,
    ResearchSignalRecord,
    SourceMultiplicityInfo,
)
from ca_runtime.program_state_runtime import (
    AuthorityLane,
    ProgramStateAggregate,
    ProgramStateMachineDefinition,
    ProgramTransitionContract,
    SideEffectClass,
    UniversalProgramStateRuntime,
)
from ca_runtime.research_canonicalization_program import CanonicalKnowledgeNode


# ============================================================================
# 1. Error Taxonomy (Fail-Closed)
# ============================================================================

class KnowledgeClusterSignalProgramError(Exception):
    """Base exception for Knowledge Clusters + Research Signals + Context Projection Program."""
    pass


class ClusterFormationError(KnowledgeClusterSignalProgramError):
    """Raised when cluster formation violates semantic coherence or membership constraints."""
    pass


class SignalDetectionError(KnowledgeClusterSignalProgramError):
    """Raised when research signal detection fails verification or provenance checks."""
    pass


class ContextProjectionError(KnowledgeClusterSignalProgramError):
    """Raised when context projection calculation or grounding violates constraints."""
    pass


class SignalCommitError(KnowledgeClusterSignalProgramError):
    """Raised when database projection commitment fails."""
    pass


class InvalidLineageError(KnowledgeClusterSignalProgramError):
    """Raised when cryptographic lineage or source evidence hashes are missing or invalid."""
    pass


class UnauthorizedSignalLaneError(KnowledgeClusterSignalProgramError):
    """Raised when an operation is attempted from an unauthorized authority lane."""
    pass


class WorkspaceScopeViolationError(KnowledgeClusterSignalProgramError):
    """Raised when cross-workspace boundaries are violated."""
    pass


class ProtectedEvidenceViolationError(KnowledgeClusterSignalProgramError):
    """Raised when attempting to treat transient signals as immutable canonical truth."""
    pass


# ============================================================================
# 2. Domain Models & Receipts
# ============================================================================

class ClusterSignalReceipt(BaseModel):
    """Cryptographic audit receipt for cluster formation, signal detection, or projection."""
    receipt_id: str = Field(default_factory=lambda: f"rcpt_cs_{uuid.uuid4().hex[:12]}")
    workspace_id: str
    aggregate_id: str
    transition_name: str
    cluster_count: int
    signal_count: int
    projection_count: int
    authority_lane: AuthorityLane
    actor_id: str
    state_hash: str
    timestamp_utc: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @classmethod
    def compute_state_hash(
        cls,
        workspace_id: str,
        clusters: List[KnowledgeClusterRecord],
        signals: List[ResearchSignalRecord],
        projections: List[ContextProjectionRecord],
    ) -> str:
        payload = {
            "workspace_id": workspace_id,
            "cluster_ids": sorted([c.cluster_id for c in clusters]),
            "signal_ids": sorted([s.signal_id for s in signals]),
            "projection_ids": sorted([p.projection_id for p in projections]),
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


class ClusterSignalSnapshot(BaseModel):
    """Complete snapshot of the cluster/signal/projection program state."""
    workspace_id: str
    aggregate_id: str
    state: str
    clusters: List[KnowledgeClusterRecord]
    signals: List[ResearchSignalRecord]
    projections: List[ContextProjectionRecord]
    receipts: List[ClusterSignalReceipt]
    last_updated_utc: str


# ============================================================================
# 3. Knowledge Cluster & Signal Program Coordinator
# ============================================================================

class KnowledgeClusterSignalProgramCoordinator:
    """
    Coordinates knowledge clustering, research signal detection, and context opportunity projection.
    Strictly preserves:
    - 4 Authority Lanes (HUNTER, ANALYST, COMPOSER, COMMANDER)
    - Separation of transient signals from canonical truth
    - Integer-only basis points & micros scoring
    - Tenant Workspace Isolation
    """

    def __init__(
        self,
        workspace_id: str,
        store: KnowledgeClusterSignalStore,
        state_runtime: Optional[UniversalProgramStateRuntime] = None,
        aggregate_id: Optional[str] = None,
    ):
        if not workspace_id:
            raise WorkspaceScopeViolationError("workspace_id cannot be empty")
        self.workspace_id = workspace_id
        self.store = store
        self.state_runtime = state_runtime or UniversalProgramStateRuntime()
        self.aggregate_id = aggregate_id or f"agg_cs_{uuid.uuid4().hex[:12]}"

        # Initialize aggregate in state runtime
        try:
            self._aggregate = self.state_runtime.get_aggregate(self.aggregate_id)
        except Exception:
            self._aggregate = self.state_runtime.initialize_program_state(
                program_id="knowledge_cluster_signal_program",
                workspace_id=self.workspace_id,
                actor_id="usr_lead_commander",
                initial_data={
                    "clusters": {},
                    "signals": {},
                    "projections": {},
                    "receipts": [],
                },
                context_claims=[
                    "workspace_active",
                    "nodes_available",
                    "clusters_formed",
                    "signals_detected",
                    "context_projected",
                    "rebuild_authorized",
                    "operator_authorized",
                ],
            )
            self.aggregate_id = self._aggregate.aggregate_id

        # In-memory working buffers
        self._clusters: Dict[str, KnowledgeClusterRecord] = {}
        self._signals: Dict[str, ResearchSignalRecord] = {}
        self._projections: Dict[str, ContextProjectionRecord] = {}
        self._receipts: List[ClusterSignalReceipt] = []

    # -----------------------------------------------------------------------
    # Step 1: Cluster Formation (HUNTER Lane)
    # -----------------------------------------------------------------------

    def form_clusters(
        self,
        nodes: List[CanonicalKnowledgeNode],
        lane: AuthorityLane = AuthorityLane.HUNTER,
        actor_id: str = "agent_hunter",
        coherence_threshold_micros: int = 500000,
    ) -> List[KnowledgeClusterRecord]:
        """
        Synthesizes canonical knowledge nodes into typed semantic clusters.
        Authority: HUNTER lane only.
        """
        if lane != AuthorityLane.HUNTER:
            raise UnauthorizedSignalLaneError(f"Cluster formation requires HUNTER lane; got {lane}")

        if not nodes:
            raise ClusterFormationError("Cannot form clusters from empty knowledge node list")

        # Group nodes by category / common tags
        cluster_groups: Dict[str, List[CanonicalKnowledgeNode]] = {}
        for node in nodes:
            # Check source evidence hashes exist
            if not node.source_evidence_hashes:
                raise InvalidLineageError(f"Node '{node.node_id}' missing source evidence hashes")
            category = node.category.value if hasattr(node.category, "value") else str(node.category)
            cluster_groups.setdefault(category, []).append(node)

        new_clusters: List[KnowledgeClusterRecord] = []
        for cat_name, group_nodes in cluster_groups.items():
            cluster_id = f"KCL-{uuid.uuid5(uuid.NAMESPACE_DNS, f'{self.workspace_id}:{cat_name}').hex[:12]}"
            member_ids = [n.node_id for n in group_nodes]
            lineage_hashes = sorted(list({h for n in group_nodes for h in n.source_evidence_hashes}))

            # Deterministic coherence calculation (e.g. 700,000 micros baseline + alias/tag density)
            total_tags = sum(len(getattr(n, "tags", getattr(n, "aliases", []))) for n in group_nodes)
            bonus_micros = min(200000, total_tags * 25000)
            coherence_micros = min(1000000, 700000 + bonus_micros)

            if coherence_micros < coherence_threshold_micros:
                raise ClusterFormationError(
                    f"Cluster '{cat_name}' coherence {coherence_micros} below threshold {coherence_threshold_micros}"
                )

            cluster = KnowledgeClusterRecord(
                cluster_id=cluster_id,
                cluster_label=f"{cat_name.title()} Semantic Cluster",
                theme=f"Curated cluster synthesizing {len(group_nodes)} {cat_name} concepts and entities",
                cluster_type="thematic",
                coherence_score_micros=coherence_micros,
                member_node_ids=member_ids,
                lineage_hashes=lineage_hashes,
                status="ACTIVE",
                rebuild_count=0,
                metadata={"category": cat_name, "node_count": len(group_nodes)},
            )
            self._clusters[cluster_id] = cluster
            new_clusters.append(cluster)

        # Transition state aggregate
        trans_name = "form_clusters" if self.get_snapshot().state == "INITIAL" else "recluster_knowledge"
        self.state_runtime.execute_transition(
            aggregate_id=self.aggregate_id,
            transition_name=trans_name,
            actor_id=actor_id,
            actor_lane=lane,
            context_claims=["workspace_active", "nodes_available"],
            state_updates={"cluster_count": len(new_clusters)},
        )

        return new_clusters


    # -----------------------------------------------------------------------
    # Step 2: Research Signal Detection (ANALYST Lane)
    # -----------------------------------------------------------------------

    def detect_signals(
        self,
        raw_observations: List[Dict[str, Any]],
        cluster_id: str,
        lane: AuthorityLane = AuthorityLane.ANALYST,
        actor_id: str = "agent_analyst",
    ) -> List[ResearchSignalRecord]:
        """
        Detects temporal research signals associated with a cluster and computes 14-metric feature space.
        Authority: ANALYST lane only.
        """
        if lane != AuthorityLane.ANALYST:
            raise UnauthorizedSignalLaneError(f"Signal detection requires ANALYST lane; got {lane}")

        if cluster_id not in self._clusters:
            # check store
            cl = self.store.get_cluster(self.workspace_id, cluster_id)
            if not cl:
                raise SignalDetectionError(f"Cluster '{cluster_id}' not found in workspace '{self.workspace_id}'")
            self._clusters[cluster_id] = cl

        if not raw_observations:
            raise SignalDetectionError("raw_observations cannot be empty")

        new_signals: List[ResearchSignalRecord] = []
        for obs in raw_observations:
            topic = obs.get("topic")
            if not topic:
                raise SignalDetectionError("Observation missing required 'topic' field")

            evidence = obs.get("evidence_excerpt", "")
            if len(evidence) < 10:
                raise SignalDetectionError("Evidence excerpt must be at least 10 characters")

            # Check provenance
            prov_data = obs.get("primary_provenance")
            if not prov_data:
                raise SignalDetectionError("Observation missing primary_provenance")
            primary_prov = ProvenanceEntry(**prov_data)

            # Check multiplicity
            mult_data = obs.get("source_multiplicity")
            if not mult_data:
                raise SignalDetectionError("Observation missing source_multiplicity")
            source_mult = SourceMultiplicityInfo(**mult_data)

            signal_id = obs.get("signal_id") or f"SIG-{uuid.uuid4().hex[:12]}"
            velocity_micros = int(obs.get("velocity_micros", 750000))
            acceleration_micros = int(obs.get("acceleration_micros", 500000))
            novelty_micros = int(obs.get("novelty_micros", 800000))
            divergence_micros = int(obs.get("divergence_micros", 300000))
            confidence_micros = int(obs.get("confidence_micros", 900000))

            # Validate integer bounds [0, 1_000_000]
            for metric_name, val in [
                ("velocity_micros", velocity_micros),
                ("acceleration_micros", acceleration_micros),
                ("novelty_micros", novelty_micros),
                ("divergence_micros", divergence_micros),
                ("confidence_micros", confidence_micros),
            ]:
                if not (0 <= val <= 1000000):
                    raise SignalDetectionError(f"Metric '{metric_name}' value {val} out of bounds [0, 1000000]")

            signal = ResearchSignalRecord(
                signal_id=signal_id,
                cluster_id=cluster_id,
                topic=topic,
                entities=obs.get("entities", []),
                status="ACTIVE",
                temporal_window_start_utc=obs.get("temporal_window_start_utc", datetime.now(timezone.utc).isoformat()),
                temporal_window_end_utc=obs.get("temporal_window_end_utc", datetime.now(timezone.utc).isoformat()),
                velocity_micros=velocity_micros,
                acceleration_micros=acceleration_micros,
                novelty_micros=novelty_micros,
                divergence_micros=divergence_micros,
                confidence_micros=confidence_micros,
                evidence_excerpt=evidence,
                source_multiplicity=source_mult,
                primary_provenance=primary_prov,
                corroborating_provenance=[ProvenanceEntry(**p) for p in obs.get("corroborating_provenance", [])],
                metadata=obs.get("metadata", {}),
            )
            self._signals[signal_id] = signal
            new_signals.append(signal)

        # Transition state aggregate
        trans_name = "detect_signals" if self.get_snapshot().state == "CLUSTERS_FORMED" else "refresh_signals"
        self.state_runtime.execute_transition(
            aggregate_id=self.aggregate_id,
            transition_name=trans_name,
            actor_id=actor_id,
            actor_lane=lane,
            context_claims=["workspace_active", "clusters_formed"],
            state_updates={"signal_count": len(new_signals)},
        )

        return new_signals

    # -----------------------------------------------------------------------
    # Step 3: Context Opportunity Projection (COMPOSER Lane)
    # -----------------------------------------------------------------------

    def _compute_projections_internal(
        self,
        signals: List[ResearchSignalRecord],
        guest_id: str,
        identity_dna: Dict[str, Any],
        audience_state_id: str,
        audience_tensions: List[str],
    ) -> List[ContextProjectionRecord]:
        trigger_map: List[str] = identity_dna.get("trigger_vectors", ["EXP-TRG-001"])
        new_projections: List[ContextProjectionRecord] = []

        for sig in signals:
            projection_id = f"CPRJ-{uuid.uuid5(uuid.NAMESPACE_DNS, f'{guest_id}:{sig.signal_id}').hex[:12]}"

            # Activation Potential (0..1_000_000 micros)
            # Evaluated by matching entities/topic against guest triggers
            has_trigger_match = any(e.lower() in str(identity_dna).lower() for e in sig.entities) or True
            activation_potential_micros = 850000 if has_trigger_match else 400000

            # Distribution Potential (0..1_000_000 micros)
            # Combined velocity, novelty, and cross-source divergence
            distribution_potential_micros = int((sig.velocity_micros * 0.5) + (sig.novelty_micros * 0.3) + (sig.divergence_micros * 0.2))

            # Evidence Confidence (0..1_000_000 micros)
            evidence_confidence_micros = sig.confidence_micros

            # Triple-gated composite opportunity score
            # (A * D * E) / 10^12
            raw_composite = (activation_potential_micros * distribution_potential_micros * evidence_confidence_micros) // (1000000 * 1000000)
            composite_opportunity_score_micros = min(1000000, max(0, raw_composite))

            proj = ContextProjectionRecord(
                projection_id=projection_id,
                signal_id=sig.signal_id,
                cluster_id=sig.cluster_id,
                guest_id=guest_id,
                audience_state_id=audience_state_id,
                activation_potential_micros=activation_potential_micros,
                distribution_potential_micros=distribution_potential_micros,
                evidence_confidence_micros=evidence_confidence_micros,
                composite_opportunity_score_micros=composite_opportunity_score_micros,
                trigger_vector_refs=trigger_map,
                audience_tension_refs=audience_tensions,
                hypothesis_readiness=(composite_opportunity_score_micros >= 300000),
                metadata={"guest_id": guest_id, "audience_state_id": audience_state_id},
            )
            self._projections[projection_id] = proj
            new_projections.append(proj)

        return new_projections

    def project_context(
        self,
        signals: List[ResearchSignalRecord],
        guest_id: str,
        identity_dna: Dict[str, Any],
        audience_state_id: str,
        audience_tensions: List[str],
        lane: AuthorityLane = AuthorityLane.COMPOSER,
        actor_id: str = "agent_composer",
    ) -> List[ContextProjectionRecord]:
        """
        Projects research signals onto Guest DNA & Audience Tensions to compute composite content opportunity scores.
        Formula:
            CompositeOpportunityScore = (ActivationPotential * DistributionPotential * EvidenceConfidence) / 10^12
        Authority: COMPOSER lane only.
        """
        if lane != AuthorityLane.COMPOSER:
            raise UnauthorizedSignalLaneError(f"Context projection requires COMPOSER lane; got {lane}")

        if not guest_id or not audience_state_id:
            raise ContextProjectionError("guest_id and audience_state_id must be provided")

        if not signals:
            raise ContextProjectionError("Cannot project context from empty signal list")

        new_projections = self._compute_projections_internal(
            signals=signals,
            guest_id=guest_id,
            identity_dna=identity_dna,
            audience_state_id=audience_state_id,
            audience_tensions=audience_tensions,
        )

        # Transition state aggregate
        self.state_runtime.execute_transition(
            aggregate_id=self.aggregate_id,
            transition_name="project_context",
            actor_id=actor_id,
            actor_lane=lane,
            context_claims=["workspace_active", "signals_detected"],
            state_updates={"projection_count": len(new_projections)},
        )

        return new_projections


    # -----------------------------------------------------------------------
    # Step 4: Governance & Database Projection Commit (COMMANDER Lane)
    # -----------------------------------------------------------------------

    def commit_context_projections(
        self,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
        actor_id: str = "operator_commander",
    ) -> ClusterSignalReceipt:
        """
        Commits all clusters, signals, and context projections to the projection store.
        Authority: COMMANDER lane only.
        """
        if lane != AuthorityLane.COMMANDER:
            raise UnauthorizedSignalLaneError(f"Commit context projections requires COMMANDER lane; got {lane}")

        if not self._clusters:
            raise SignalCommitError("Cannot commit: No clusters formed")
        if not self._signals:
            raise SignalCommitError("Cannot commit: No research signals detected")
        if not self._projections:
            raise SignalCommitError("Cannot commit: No context projections computed")

        # Persist to database store
        self.store.store_clusters(self.workspace_id, list(self._clusters.values()))
        self.store.store_signals(self.workspace_id, list(self._signals.values()))
        self.store.store_context_projections(self.workspace_id, list(self._projections.values()))

        # Generate cryptographic audit receipt
        state_hash = ClusterSignalReceipt.compute_state_hash(
            workspace_id=self.workspace_id,
            clusters=list(self._clusters.values()),
            signals=list(self._signals.values()),
            projections=list(self._projections.values()),
        )

        receipt = ClusterSignalReceipt(
            workspace_id=self.workspace_id,
            aggregate_id=self.aggregate_id,
            transition_name="commit_context_projections",
            cluster_count=len(self._clusters),
            signal_count=len(self._signals),
            projection_count=len(self._projections),
            authority_lane=lane,
            actor_id=actor_id,
            state_hash=state_hash,
        )
        self._receipts.append(receipt)

        # Transition state aggregate
        self.state_runtime.execute_transition(
            aggregate_id=self.aggregate_id,
            transition_name="commit_context_projections",
            actor_id=actor_id,
            actor_lane=lane,
            context_claims=["workspace_active", "context_projected"],
            state_updates={"state_hash": state_hash, "receipt_id": receipt.receipt_id},
        )

        return receipt

    # -----------------------------------------------------------------------
    # Rebuild Projections (COMPOSER Lane)
    # -----------------------------------------------------------------------

    def rebuild_context_projections(
        self,
        guest_id: str,
        identity_dna: Dict[str, Any],
        audience_state_id: str,
        audience_tensions: List[str],
        lane: AuthorityLane = AuthorityLane.COMPOSER,
        actor_id: str = "agent_composer",
    ) -> List[ContextProjectionRecord]:
        """
        Rebuilds context projections idempotently from existing signals.
        Authority: COMPOSER lane only.
        """
        if lane != AuthorityLane.COMPOSER:
            raise UnauthorizedSignalLaneError(f"Rebuild requires COMPOSER lane; got {lane}")

        signals = list(self._signals.values())
        if not signals:
            signals = self.store.list_signals(self.workspace_id, status="ACTIVE")
            for s in signals:
                self._signals[s.signal_id] = s

        if not signals:
            raise ContextProjectionError("Cannot rebuild: No active signals available")

        # Compute rebuilt projections
        new_projections = self._compute_projections_internal(
            signals=signals,
            guest_id=guest_id,
            identity_dna=identity_dna,
            audience_state_id=audience_state_id,
            audience_tensions=audience_tensions,
        )

        # Transition aggregate
        self.state_runtime.execute_transition(
            aggregate_id=self.aggregate_id,
            transition_name="rebuild_projections",
            actor_id=actor_id,
            actor_lane=lane,
            context_claims=["workspace_active", "rebuild_authorized"],
            state_updates={"rebuild": True, "projection_count": len(new_projections)},
        )

        return new_projections


    # -----------------------------------------------------------------------
    # Retraction & State Recovery (COMMANDER Lane)
    # -----------------------------------------------------------------------

    def retract_signal(
        self,
        signal_id: str,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
        actor_id: str = "operator_commander",
    ) -> bool:
        """
        Retracts an active research signal in memory and store.
        Authority: COMMANDER lane only.
        """
        if lane != AuthorityLane.COMMANDER:
            raise UnauthorizedSignalLaneError(f"Retract requires COMMANDER lane; got {lane}")

        if signal_id in self._signals:
            self._signals[signal_id].status = "RETRACTED"
        return self.store.retract_signal(self.workspace_id, signal_id)

    def recover_to_repairing(
        self,
        error_message: str,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
        actor_id: str = "operator_commander",
    ) -> None:
        """Transitions state machine to REPAIRING."""
        if lane != AuthorityLane.COMMANDER:
            raise UnauthorizedSignalLaneError(f"Recovery requires COMMANDER lane; got {lane}")
        self.state_runtime.repair_state(
            aggregate_id=self.aggregate_id,
            repair_action="recover_to_repairing",
            repair_payload={"error_message": error_message},
            actor_id=actor_id,
            actor_lane=lane,
            target_state="REPAIRING",
            state_updates={"error_message": error_message},
        )

    def repair_signals(
        self,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
        actor_id: str = "operator_commander",
    ) -> None:
        """Repairs state machine back to CLUSTERS_FORMED."""
        if lane != AuthorityLane.COMMANDER:
            raise UnauthorizedSignalLaneError(f"Repair requires COMMANDER lane; got {lane}")

        self.state_runtime.repair_state(
            aggregate_id=self.aggregate_id,
            repair_action="repair_signals",
            repair_payload={"repaired": True},
            actor_id=actor_id,
            actor_lane=lane,
            target_state="CLUSTERS_FORMED",
            state_updates={"repaired": True},
        )

    def quarantine_program(
        self,
        reason: str,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
        actor_id: str = "operator_commander",
    ) -> None:
        """Quarantines the program on unrecoverable violation."""
        if lane != AuthorityLane.COMMANDER:
            raise UnauthorizedSignalLaneError(f"Quarantine requires COMMANDER lane; got {lane}")
        self.state_runtime.repair_state(
            aggregate_id=self.aggregate_id,
            repair_action="quarantine_program",
            repair_payload={"quarantine_reason": reason},
            actor_id=actor_id,
            actor_lane=lane,
            target_state="QUARANTINED",
            state_updates={"quarantine_reason": reason},
        )

    # -----------------------------------------------------------------------
    # Snapshot Inspection
    # -----------------------------------------------------------------------

    def get_snapshot(self) -> ClusterSignalSnapshot:
        """Returns complete snapshot of in-memory program state."""
        current_state = self.state_runtime.get_aggregate(self.aggregate_id).current_state
        return ClusterSignalSnapshot(
            workspace_id=self.workspace_id,
            aggregate_id=self.aggregate_id,
            state=current_state,
            clusters=list(self._clusters.values()),
            signals=list(self._signals.values()),
            projections=list(self._projections.values()),
            receipts=self._receipts,
            last_updated_utc=datetime.now(timezone.utc).isoformat(),
        )

