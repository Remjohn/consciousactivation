"""Audience Context + Cognitive Island State Program Coordinator.

Governed by:
- Phase 3 Mandate M26 (03_PHASE_3_INTELLIGENCE_AND_PROGRAMS/M26_audience_context_program.md)
- 00_CONTROL/20_PHASE3_CANONICALIZATION_MODEL.md
- 00_CONTROL/21_PHASE3_KNOWLEDGE_RUNTIME_CONTRACT.md
- 00_CONTROL/24_PHASE3_PROGRAM_STATE_HOOKS_MATRIX.md
- 00_CONTROL/17_PHASE1_AGENT_SKILL_OPERATION_OWNERSHIP_GRAPH.md (AUD-001, AUD-002, AUD-003)
- Live PostgreSQL/RLS Tenancy Authority (TS-CAE-TEN-001)

Operating Model:
- Protected Cognitive Islands: Source-bearing cognitive topology (mental models, resistance
  patterns, friction points) that CANNOT be silently rewritten by downstream repair or recompilation.
- Mutable Current-State Projections: Derived context expressions (activation coordinates,
  viewer-state sequences) that may be dynamically recompiled/versioned with cryptographic
  lineage back to source Cognitive Islands.
- Four Authority Lanes: HUNTER (tension hunting), ANALYST (island mapping), COMPOSER (state projection),
  COMMANDER (lifecycle & operator gate supervision).
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple
from uuid import UUID, uuid4

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.hook_runtime import (
    HookExtensionManager,
    OperatorGateReceipt,
    OperatorGateRuntimeEngine,
    SelfApprovalProhibitedError,
)
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_state_runtime import (
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
    ProgramStateAggregateNotFoundError,
    ProgramStateLifecycle,
    ProgramStateMachineDefinition,
    ProgramStateRuntimeError,
    ProgramStateVersionConflictError,
    ProgramTransitionResult,
    UniversalProgramStateRuntime,
    _compute_state_hash,
    get_canonical_audience_context_state_machine,
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
    UnauthorizedOperatorAccessError,
    require_current_tenant_context,
)

logger = logging.getLogger("ca_runtime.audience_context_program")

PROGRAM_ID = "audience_context_program"
PROGRAM_VERSION = "1.0.0"


# ============================================================================
# 1. Typed Error Hierarchy
# ============================================================================

class AudienceProgramError(ProgramStateRuntimeError):
    """Base exception for Audience Context Program execution."""
    pass


class ProtectedCognitiveIslandMutationError(AudienceProgramError):
    """Raised when an attempt is made to silently modify or rewrite a protected Cognitive Island."""

    def __init__(self, message: str, *, island_id: Optional[str] = None, expected_sha256: Optional[str] = None, actual_sha256: Optional[str] = None):
        super().__init__(
            message,
            reason_code="PROTECTED_COGNITIVE_ISLAND_MUTATION_PROHIBITED",
            details={
                "island_id": island_id,
                "expected_sha256": expected_sha256,
                "actual_sha256": actual_sha256,
            },
        )
        self.island_id = island_id
        self.expected_sha256 = expected_sha256
        self.actual_sha256 = actual_sha256


class CognitiveIslandNotFoundError(AudienceProgramError):
    """Raised when a requested Cognitive Island does not exist."""

    def __init__(self, message: str, *, island_id: str):
        super().__init__(
            message,
            reason_code="COGNITIVE_ISLAND_NOT_FOUND",
            details={"island_id": island_id},
        )
        self.island_id = island_id


class AudienceLineageMissingError(AudienceProgramError):
    """Raised when derived audience projection lacks cryptographic lineage to active Cognitive Islands."""

    def __init__(self, message: str, *, missing_island_ids: Sequence[str] = ()):
        super().__init__(
            message,
            reason_code="AUDIENCE_LINEAGE_MISSING",
            details={"missing_island_ids": list(missing_island_ids)},
        )
        self.missing_island_ids = list(missing_island_ids)


class AudienceIntegrityError(AudienceProgramError):
    """Raised when audience data fails cryptographic verification or schema assertions."""

    def __init__(self, message: str, *, item_id: Optional[str] = None, reason: Optional[str] = None):
        super().__init__(
            message,
            reason_code="AUDIENCE_INTEGRITY_ERROR",
            details={"item_id": item_id, "reason": reason},
        )
        self.item_id = item_id


class AudienceWorkspaceScopeViolationError(AudienceProgramError):
    """Raised when cross-workspace tenant leak is detected."""

    def __init__(self, message: str, *, expected_workspace_id: str, actual_workspace_id: str):
        super().__init__(
            message,
            reason_code="WORKSPACE_SCOPE_VIOLATION",
            details={"expected_workspace_id": expected_workspace_id, "actual_workspace_id": actual_workspace_id},
        )


class AudienceProfileNotInitializedError(AudienceProgramError):
    """Raised when operation requires an initialized audience profile but none exists."""

    def __init__(self, message: str, *, aggregate_id: str):
        super().__init__(
            message,
            reason_code="AUDIENCE_PROFILE_NOT_INITIALIZED",
            details={"aggregate_id": aggregate_id},
        )


# ============================================================================
# 2. Strongly Typed Data Models
# ============================================================================

@dataclass(frozen=True, slots=True)
class AudienceProfile:
    """Canonical Audience Profile setup."""
    audience_id: str
    workspace_id: str
    target_segment: str
    core_demographics: Dict[str, Any]
    psychographic_baseline: Dict[str, Any]
    status: str = "ACTIVE"
    created_at: str = field(default_factory=utc_now_rfc3339)

    def __post_init__(self) -> None:
        if not self.audience_id or not self.audience_id.strip():
            raise AudienceIntegrityError("audience_id cannot be empty")
        if not self.workspace_id or not self.workspace_id.strip():
            raise AudienceIntegrityError("workspace_id cannot be empty")
        if not self.target_segment or not self.target_segment.strip():
            raise AudienceIntegrityError("target_segment cannot be empty")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audience_id": self.audience_id,
            "workspace_id": self.workspace_id,
            "target_segment": self.target_segment,
            "core_demographics": self.core_demographics,
            "psychographic_baseline": self.psychographic_baseline,
            "status": self.status,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> AudienceProfile:
        return cls(
            audience_id=data["audience_id"],
            workspace_id=data["workspace_id"],
            target_segment=data["target_segment"],
            core_demographics=dict(data.get("core_demographics", {})),
            psychographic_baseline=dict(data.get("psychographic_baseline", {})),
            status=data.get("status", "ACTIVE"),
            created_at=data.get("created_at", utc_now_rfc3339()),
        )


@dataclass(frozen=True, slots=True)
class CognitiveIsland:
    """Protected source-bearing Cognitive Island structure.
    
    Represents entrenched mental models, resistance patterns, and friction points.
    Cannot be silently rewritten or modified in-place.
    """
    island_id: str
    workspace_id: str
    audience_id: str
    name: str
    mental_model: str
    resistance_patterns: Tuple[str, ...]
    friction_points: Tuple[str, ...]
    source_evidence_hashes: Tuple[str, ...]
    content_sha256: str
    is_protected: bool = True
    version: int = 1
    parent_island_sha256: Optional[str] = None
    created_at: str = field(default_factory=utc_now_rfc3339)

    def __post_init__(self) -> None:
        if not self.island_id or not self.island_id.strip():
            raise AudienceIntegrityError("island_id cannot be empty")
        if not self.name or not self.name.strip():
            raise AudienceIntegrityError("name cannot be empty")
        for h in self.source_evidence_hashes:
            if not h or len(h) != 64:
                raise AudienceIntegrityError(f"Invalid source evidence hash '{h}': must be 64-char hex string")
        computed = self.compute_content_hash(
            island_id=self.island_id,
            workspace_id=self.workspace_id,
            audience_id=self.audience_id,
            name=self.name,
            mental_model=self.mental_model,
            resistance_patterns=self.resistance_patterns,
            friction_points=self.friction_points,
            source_evidence_hashes=self.source_evidence_hashes,
            version=self.version,
            parent_island_sha256=self.parent_island_sha256,
        )
        if self.content_sha256 != computed:
            raise ProtectedCognitiveIslandMutationError(
                f"CognitiveIsland '{self.island_id}' content_sha256 mismatch: expected {computed}, got {self.content_sha256}",
                island_id=self.island_id,
                expected_sha256=computed,
                actual_sha256=self.content_sha256,
            )

    @staticmethod
    def compute_content_hash(
        *,
        island_id: str,
        workspace_id: str | UUID,
        audience_id: str,
        name: str,
        mental_model: str,
        resistance_patterns: Sequence[str],
        friction_points: Sequence[str],
        source_evidence_hashes: Sequence[str],
        version: int = 1,
        parent_island_sha256: Optional[str] = None,
    ) -> str:
        payload = {
            "island_id": island_id,
            "workspace_id": str(workspace_id),
            "audience_id": audience_id,
            "name": name,
            "mental_model": mental_model,
            "resistance_patterns": sorted(list(resistance_patterns)),
            "friction_points": sorted(list(friction_points)),
            "source_evidence_hashes": sorted(list(source_evidence_hashes)),
            "version": version,
            "parent_island_sha256": parent_island_sha256 or "",
        }
        return canonical_sha256(payload)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "island_id": self.island_id,
            "workspace_id": self.workspace_id,
            "audience_id": self.audience_id,
            "name": self.name,
            "mental_model": self.mental_model,
            "resistance_patterns": list(self.resistance_patterns),
            "friction_points": list(self.friction_points),
            "source_evidence_hashes": list(self.source_evidence_hashes),
            "content_sha256": self.content_sha256,
            "is_protected": self.is_protected,
            "version": self.version,
            "parent_island_sha256": self.parent_island_sha256,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CognitiveIsland:
        return cls(
            island_id=data["island_id"],
            workspace_id=data["workspace_id"],
            audience_id=data["audience_id"],
            name=data["name"],
            mental_model=data["mental_model"],
            resistance_patterns=tuple(data.get("resistance_patterns", ())),
            friction_points=tuple(data.get("friction_points", ())),
            source_evidence_hashes=tuple(data.get("source_evidence_hashes", ())),
            content_sha256=data["content_sha256"],
            is_protected=data.get("is_protected", True),
            version=data.get("version", 1),
            parent_island_sha256=data.get("parent_island_sha256"),
            created_at=data.get("created_at", utc_now_rfc3339()),
        )


@dataclass(frozen=True, slots=True)
class AudienceStateProjection:
    """Mutable derived context expression projected from protected Cognitive Islands."""
    projection_id: str
    workspace_id: str
    audience_id: str
    source_island_ids: Tuple[str, ...]
    source_island_hashes: Tuple[str, ...]
    activation_coordinates_bps: Dict[str, int]
    viewer_state_sequence: Tuple[str, ...]
    tension_summary: str
    projection_sha256: str
    derived_at: str = field(default_factory=utc_now_rfc3339)

    def __post_init__(self) -> None:
        if not self.projection_id or not self.projection_id.strip():
            raise AudienceIntegrityError("projection_id cannot be empty")
        if not self.source_island_ids:
            raise AudienceLineageMissingError("AudienceStateProjection must reference at least one source_island_id")
        # Validate integer basis points (no floats)
        for k, v in self.activation_coordinates_bps.items():
            if not isinstance(v, int):
                raise AudienceIntegrityError(f"Activation coordinate '{k}' must be integer basis points [0..10000], got {type(v).__name__}")
            if not (0 <= v <= 10000):
                raise AudienceIntegrityError(f"Activation coordinate '{k}'={v} out of bounds [0..10000] bps")

    @staticmethod
    def compute_projection_hash(
        *,
        projection_id: str,
        workspace_id: str | UUID,
        audience_id: str,
        source_island_ids: Sequence[str],
        source_island_hashes: Sequence[str],
        activation_coordinates_bps: Mapping[str, int],
        viewer_state_sequence: Sequence[str],
        tension_summary: str,
    ) -> str:
        payload = {
            "projection_id": projection_id,
            "workspace_id": str(workspace_id),
            "audience_id": audience_id,
            "source_island_ids": sorted(list(source_island_ids)),
            "source_island_hashes": sorted(list(source_island_hashes)),
            "activation_coordinates_bps": dict(sorted(activation_coordinates_bps.items())),
            "viewer_state_sequence": list(viewer_state_sequence),
            "tension_summary": tension_summary,
        }
        return canonical_sha256(payload)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "projection_id": self.projection_id,
            "workspace_id": self.workspace_id,
            "audience_id": self.audience_id,
            "source_island_ids": list(self.source_island_ids),
            "source_island_hashes": list(self.source_island_hashes),
            "activation_coordinates_bps": self.activation_coordinates_bps,
            "viewer_state_sequence": list(self.viewer_state_sequence),
            "tension_summary": self.tension_summary,
            "projection_sha256": self.projection_sha256,
            "derived_at": self.derived_at,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> AudienceStateProjection:
        return cls(
            projection_id=data["projection_id"],
            workspace_id=data["workspace_id"],
            audience_id=data["audience_id"],
            source_island_ids=tuple(data.get("source_island_ids", ())),
            source_island_hashes=tuple(data.get("source_island_hashes", ())),
            activation_coordinates_bps=dict(data.get("activation_coordinates_bps", {})),
            viewer_state_sequence=tuple(data.get("viewer_state_sequence", ())),
            tension_summary=data.get("tension_summary", ""),
            projection_sha256=data["projection_sha256"],
            derived_at=data.get("derived_at", utc_now_rfc3339()),
        )


@dataclass(frozen=True, slots=True)
class AudienceContextSnapshot:
    """Operator-facing immutable snapshot of active Audience Context and Cognitive Islands."""
    aggregate_id: str
    workspace_id: str
    current_state: str
    audience_profile: Optional[AudienceProfile]
    cognitive_islands: Tuple[CognitiveIsland, ...]
    current_projection: Optional[AudienceStateProjection]
    version: int
    state_hash: str
    last_receipt_id: Optional[str]


# ============================================================================
# 3. Audience Context Program Coordinator
# ============================================================================

class AudienceContextProgramCoordinator:
    """Governed Coordinator for Audience Context + Cognitive Island Program.
    
    Orchestrates the lifecycle:
      INITIAL -> AUDIENCE_INITIALIZED -> TENSIONS_HUNTED -> ISLANDS_MAPPED -> CONTEXT_PROJECTED -> AUDIENCE_ACTIVE
      (with REPAIRING recovery route)
    
    Enforces:
    - Root tenant boundary at Workspace level.
    - Protection of Cognitive Islands: Invariant enforcement against silent in-place modifications.
    - Derived context projections versioned and recomputed with cryptographic lineage.
    - Strict Four Authority Lanes: COMMANDER, HUNTER, ANALYST, COMPOSER.
    - Cryptographic CausalTraceLedger forward linking.
    """

    def __init__(
        self,
        *,
        runtime: UniversalProgramStateRuntime,
        coordinator: StateLifecycleCoordinator,
        trace_ledger: CausalTraceLedger,
        operator_gate_engine: Optional[OperatorGateRuntimeEngine] = None,
        hook_manager: Optional[HookExtensionManager] = None,
    ) -> None:
        self._runtime = runtime
        self._coordinator = coordinator
        self._trace_ledger = trace_ledger
        self._operator_gate_engine = operator_gate_engine or OperatorGateRuntimeEngine(
            trace_ledger=trace_ledger
        )
        self._hook_manager = hook_manager

    # ------------------------------------------------------------------------
    # Phase 1: Initialize Audience Profile (COMMANDER)
    # ------------------------------------------------------------------------
    def initialize_audience(
        self,
        *,
        workspace_id: str | UUID,
        audience_id: str,
        target_segment: str,
        core_demographics: Optional[Dict[str, Any]] = None,
        psychographic_baseline: Optional[Dict[str, Any]] = None,
        context: TenantContext,
        actor_id: str = "audience_commander",
        idempotency_key: Optional[str] = None,
    ) -> ProgramTransitionResult:
        """Initializes Audience Profile setup for the workspace."""
        ws_str = str(workspace_id)
        if str(context.workspace_id) != ws_str:
            raise CrossWorkspaceLeakError(
                f"Context workspace '{context.workspace_id}' does not match target workspace '{ws_str}'"
            )

        profile = AudienceProfile(
            audience_id=audience_id,
            workspace_id=ws_str,
            target_segment=target_segment,
            core_demographics=core_demographics or {},
            psychographic_baseline=psychographic_baseline or {},
            status="INITIALIZED",
        )

        # Initialize aggregate in runtime
        aggregate = self._runtime.initialize_program_state(
            program_id=PROGRAM_ID,
            workspace_id=ws_str,
            actor_id=actor_id,
            context_claims=["workspace_active", "operator_authorized"],
        )

        def work_fn(agg: ProgramStateAggregate) -> Dict[str, Any]:
            current = dict(agg.state_data)
            current["audience_profile"] = profile.to_dict()
            current["cognitive_islands"] = []
            current["tensions"] = []
            current["projections"] = []
            current["current_projection"] = None
            return current

        return self._coordinator.execute_state_phase(
            aggregate_id=aggregate.aggregate_id,
            transition_name="initialize_audience",
            actor_id=actor_id,
            actor_lane=AuthorityLane.COMMANDER,
            work_fn=work_fn,
            context=context,
            context_claims=["workspace_active", "operator_authorized"],
            idempotency_key=idempotency_key or f"init_{ws_str}_{audience_id}",
        )

    # ------------------------------------------------------------------------
    # Phase 2: Hunt Audience Tensions (HUNTER)
    # ------------------------------------------------------------------------
    def hunt_tensions(
        self,
        *,
        aggregate_id: str,
        tension_observations: Sequence[Dict[str, Any]],
        context: TenantContext,
        actor_id: str = "audience_tension_hunter",
        idempotency_key: Optional[str] = None,
    ) -> ProgramTransitionResult:
        """Hunts audience tensions and acute cognitive resistances (AUD-001)."""
        aggregate = self._runtime.get_aggregate(aggregate_id)
        if not aggregate:
            raise ProgramStateAggregateNotFoundError(f"Aggregate '{aggregate_id}' not found")
        if aggregate.workspace_id != str(context.workspace_id):
            raise CrossWorkspaceLeakError("Tenant workspace mismatch")
        if "audience_profile" not in aggregate.state_data:
            raise AudienceProfileNotInitializedError(f"Audience profile not initialized in {aggregate_id}", aggregate_id=aggregate_id)

        def work_fn(agg: ProgramStateAggregate) -> Dict[str, Any]:
            current = dict(agg.state_data)
            current["tensions"] = list(tension_observations)
            current["tensions_hunted_at"] = utc_now_rfc3339()
            return current

        return self._coordinator.execute_state_phase(
            aggregate_id=aggregate_id,
            transition_name="hunt_tensions",
            actor_id=actor_id,
            actor_lane=AuthorityLane.HUNTER,
            work_fn=work_fn,
            context=context,
            context_claims=["workspace_active", "audience_profile_active"],
            idempotency_key=idempotency_key or f"hunt_{aggregate_id}_{len(tension_observations)}",
        )

    # ------------------------------------------------------------------------
    # Phase 3: Map Cognitive Islands (ANALYST)
    # ------------------------------------------------------------------------
    def map_cognitive_islands(
        self,
        *,
        aggregate_id: str,
        islands_data: Sequence[Dict[str, Any]],
        context: TenantContext,
        actor_id: str = "cognitive_island_mapper",
        idempotency_key: Optional[str] = None,
    ) -> ProgramTransitionResult:
        """Maps and establishes protected Cognitive Islands with content hash verification (AUD-002)."""
        aggregate = self._runtime.get_aggregate(aggregate_id)
        if not aggregate:
            raise ProgramStateAggregateNotFoundError(f"Aggregate '{aggregate_id}' not found")
        if aggregate.workspace_id != str(context.workspace_id):
            raise CrossWorkspaceLeakError("Tenant workspace mismatch")
        if "audience_profile" not in aggregate.state_data:
            raise AudienceProfileNotInitializedError(f"Audience profile not initialized in {aggregate_id}", aggregate_id=aggregate_id)

        audience_id = aggregate.state_data["audience_profile"]["audience_id"]

        built_islands: List[CognitiveIsland] = []
        for raw in islands_data:
            raw_dict = dict(raw)
            island_id = raw_dict["island_id"]
            name = raw_dict["name"]
            mental_model = raw_dict.get("mental_model", "")
            resistance_patterns = tuple(raw_dict.get("resistance_patterns", ()))
            friction_points = tuple(raw_dict.get("friction_points", ()))
            source_evidence_hashes = tuple(raw_dict.get("source_evidence_hashes", ()))
            version = raw_dict.get("version", 1)
            parent_sha = raw_dict.get("parent_island_sha256")

            computed_sha = CognitiveIsland.compute_content_hash(
                island_id=island_id,
                workspace_id=str(context.workspace_id),
                audience_id=audience_id,
                name=name,
                mental_model=mental_model,
                resistance_patterns=resistance_patterns,
                friction_points=friction_points,
                source_evidence_hashes=source_evidence_hashes,
                version=version,
                parent_island_sha256=parent_sha,
            )

            island = CognitiveIsland(
                island_id=island_id,
                workspace_id=str(context.workspace_id),
                audience_id=audience_id,
                name=name,
                mental_model=mental_model,
                resistance_patterns=resistance_patterns,
                friction_points=friction_points,
                source_evidence_hashes=source_evidence_hashes,
                content_sha256=computed_sha,
                is_protected=True,
                version=version,
                parent_island_sha256=parent_sha,
            )
            built_islands.append(island)

        def work_fn(agg: ProgramStateAggregate) -> Dict[str, Any]:
            current = dict(agg.state_data)
            current["cognitive_islands"] = [isl.to_dict() for isl in built_islands]
            current["islands_mapped_at"] = utc_now_rfc3339()
            return current

        return self._coordinator.execute_state_phase(
            aggregate_id=aggregate_id,
            transition_name="map_cognitive_islands",
            actor_id=actor_id,
            actor_lane=AuthorityLane.ANALYST,
            work_fn=work_fn,
            context=context,
            context_claims=["workspace_active", "tensions_available", "protected_islands_verified"],
            idempotency_key=idempotency_key or f"map_{aggregate_id}_{len(built_islands)}",
        )

    # ------------------------------------------------------------------------
    # Phase 4: Project Current State (COMPOSER)
    # ------------------------------------------------------------------------
    def project_current_state(
        self,
        *,
        aggregate_id: str,
        activation_coordinates_bps: Dict[str, int],
        viewer_state_sequence: Sequence[str],
        tension_summary: str,
        context: TenantContext,
        actor_id: str = "viewer_state_composer",
        projection_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> ProgramTransitionResult:
        """Projects mutable current-state context expression from active Cognitive Islands (AUD-003)."""
        aggregate = self._runtime.get_aggregate(aggregate_id)
        if not aggregate:
            raise ProgramStateAggregateNotFoundError(f"Aggregate '{aggregate_id}' not found")
        if aggregate.workspace_id != str(context.workspace_id):
            raise CrossWorkspaceLeakError("Tenant workspace mismatch")
        if "audience_profile" not in aggregate.state_data:
            raise AudienceProfileNotInitializedError(f"Audience profile not initialized in {aggregate_id}", aggregate_id=aggregate_id)

        raw_islands = aggregate.state_data.get("cognitive_islands", [])
        if not raw_islands:
            raise AudienceLineageMissingError("Cannot project current state: zero Cognitive Islands present in aggregate")

        islands = [CognitiveIsland.from_dict(raw) for raw in raw_islands]
        island_ids = tuple(isl.island_id for isl in islands)
        island_hashes = tuple(isl.content_sha256 for isl in islands)
        audience_id = aggregate.state_data["audience_profile"]["audience_id"]
        pid = projection_id or f"proj_{uuid4().hex[:12]}"

        proj_sha = AudienceStateProjection.compute_projection_hash(
            projection_id=pid,
            workspace_id=str(context.workspace_id),
            audience_id=audience_id,
            source_island_ids=island_ids,
            source_island_hashes=island_hashes,
            activation_coordinates_bps=activation_coordinates_bps,
            viewer_state_sequence=viewer_state_sequence,
            tension_summary=tension_summary,
        )

        projection = AudienceStateProjection(
            projection_id=pid,
            workspace_id=str(context.workspace_id),
            audience_id=audience_id,
            source_island_ids=island_ids,
            source_island_hashes=island_hashes,
            activation_coordinates_bps=dict(activation_coordinates_bps),
            viewer_state_sequence=tuple(viewer_state_sequence),
            tension_summary=tension_summary,
            projection_sha256=proj_sha,
        )

        def work_fn(agg: ProgramStateAggregate) -> Dict[str, Any]:
            current = dict(agg.state_data)
            projections = list(current.get("projections", []))
            projections.append(projection.to_dict())
            current["projections"] = projections
            current["current_projection"] = projection.to_dict()
            return current

        return self._coordinator.execute_state_phase(
            aggregate_id=aggregate_id,
            transition_name="project_current_state",
            actor_id=actor_id,
            actor_lane=AuthorityLane.COMPOSER,
            work_fn=work_fn,
            context=context,
            context_claims=["workspace_active", "protected_islands_present", "lineage_provenance_verified"],
            idempotency_key=idempotency_key or f"proj_{aggregate_id}_{pid}",
        )

    # ------------------------------------------------------------------------
    # Phase 5: Approve Audience Context (COMMANDER & Operator Gate)
    # ------------------------------------------------------------------------
    def approve_audience_context(
        self,
        *,
        aggregate_id: str,
        operator_context: TenantContext,
        approver_id: str,
        approval_decision: str = "APPROVED",
        reason: Optional[str] = None,
        requester_id: str = "audience_commander",
        idempotency_key: Optional[str] = None,
    ) -> ProgramTransitionResult:
        """Approves and activates the Audience Context via verified Operator Gate."""
        aggregate = self._runtime.get_aggregate(aggregate_id)
        if not aggregate:
            raise ProgramStateAggregateNotFoundError(f"Aggregate '{aggregate_id}' not found")
        if aggregate.workspace_id != str(operator_context.workspace_id):
            raise CrossWorkspaceLeakError("Operator context workspace mismatch")

        # 1. Anti-Self-Approval and Operator Gate verification
        gate = self._operator_gate_engine.create_operator_gate(
            workspace_id=operator_context.workspace_id,
            state_aggregate_id=aggregate_id,
            operation_id="cae.audience.approve_context@1.0.0",
            decision_context={"target_state": "AUDIENCE_ACTIVE", "reason": reason or "Audience context verified by human operator"},
            requester_id=requester_id,
        )

        receipt = self._operator_gate_engine.submit_operator_decision(
            gate_id=gate.gate_id,
            decision=approval_decision,
            context=operator_context,
            decision_notes=reason or "Audience context verified by human operator",
        )

        def work_fn(agg: ProgramStateAggregate) -> Dict[str, Any]:
            current = dict(agg.state_data)
            current["operator_approval_receipt"] = {
                "receipt_id": receipt.receipt_id,
                "gate_id": receipt.gate_id,
                "workspace_id": str(receipt.workspace_id),
                "state_aggregate_id": receipt.state_aggregate_id,
                "decision": receipt.decision,
                "decided_by": receipt.decided_by,
                "decided_at": receipt.decided_at,
                "receipt_sha256": receipt.receipt_sha256,
            }
            current["approved_at"] = utc_now_rfc3339()
            return current

        return self._coordinator.execute_state_phase(
            aggregate_id=aggregate_id,
            transition_name="approve_audience_context",
            actor_id=approver_id,
            actor_lane=AuthorityLane.COMMANDER,
            work_fn=work_fn,
            context=operator_context,
            context_claims=["workspace_active", "operator_gate_approved"],
            idempotency_key=idempotency_key or f"approve_{aggregate_id}_{receipt.receipt_id}",
        )

    # ------------------------------------------------------------------------
    # Evolutionary & Recompilation Operations
    # ------------------------------------------------------------------------
    def supersede_cognitive_island(
        self,
        *,
        aggregate_id: str,
        island_id: str,
        updated_name: str,
        updated_mental_model: str,
        updated_resistance_patterns: Sequence[str],
        updated_friction_points: Sequence[str],
        updated_source_evidence_hashes: Sequence[str],
        context: TenantContext,
        actor_id: str = "cognitive_island_mapper",
    ) -> CognitiveIsland:
        """Explicitly supersedes an existing Cognitive Island with version increment and ancestor hash link."""
        aggregate = self._runtime.get_aggregate(aggregate_id)
        if not aggregate:
            raise ProgramStateAggregateNotFoundError(f"Aggregate '{aggregate_id}' not found")
        if aggregate.workspace_id != str(context.workspace_id):
            raise CrossWorkspaceLeakError("Tenant workspace mismatch")

        raw_islands = aggregate.state_data.get("cognitive_islands", [])
        existing_idx = -1
        existing_island: Optional[CognitiveIsland] = None
        for i, raw in enumerate(raw_islands):
            isl = CognitiveIsland.from_dict(raw)
            if isl.island_id == island_id:
                existing_idx = i
                existing_island = isl
                break

        if existing_island is None:
            raise CognitiveIslandNotFoundError(f"CognitiveIsland '{island_id}' not found in aggregate", island_id=island_id)

        new_version = existing_island.version + 1
        parent_sha = existing_island.content_sha256
        audience_id = existing_island.audience_id

        computed_sha = CognitiveIsland.compute_content_hash(
            island_id=island_id,
            workspace_id=str(context.workspace_id),
            audience_id=audience_id,
            name=updated_name,
            mental_model=updated_mental_model,
            resistance_patterns=updated_resistance_patterns,
            friction_points=updated_friction_points,
            source_evidence_hashes=updated_source_evidence_hashes,
            version=new_version,
            parent_island_sha256=parent_sha,
        )

        superseding_island = CognitiveIsland(
            island_id=island_id,
            workspace_id=str(context.workspace_id),
            audience_id=audience_id,
            name=updated_name,
            mental_model=updated_mental_model,
            resistance_patterns=tuple(updated_resistance_patterns),
            friction_points=tuple(updated_friction_points),
            source_evidence_hashes=tuple(updated_source_evidence_hashes),
            content_sha256=computed_sha,
            is_protected=True,
            version=new_version,
            parent_island_sha256=parent_sha,
        )

        # Update aggregate in place without mutating prior versions
        current_data = dict(aggregate.state_data)
        updated_islands = list(raw_islands)
        updated_islands[existing_idx] = superseding_island.to_dict()
        current_data["cognitive_islands"] = updated_islands

        new_version_num = aggregate.version + 1
        now = utc_now_rfc3339()
        new_state_hash = _compute_state_hash(
            aggregate_id=aggregate.aggregate_id,
            program_id=aggregate.program_id,
            program_version=aggregate.program_version,
            current_state=aggregate.current_state,
            version=new_version_num,
            state_data=current_data,
        )

        updated_aggregate = ProgramStateAggregate(
            aggregate_id=aggregate.aggregate_id,
            workspace_id=aggregate.workspace_id,
            cae_run_id=aggregate.cae_run_id,
            program_id=aggregate.program_id,
            program_version=aggregate.program_version,
            current_state=aggregate.current_state,
            state_data=current_data,
            version=new_version_num,
            state_hash=new_state_hash,
            lifecycle=aggregate.lifecycle,
            last_receipt_id=aggregate.last_receipt_id,
            created_at=aggregate.created_at,
            updated_at=now,
        )
        self._runtime.store.save_aggregate(updated_aggregate, expected_version=aggregate.version)

        # Record causal trace
        prev_hash = self._trace_ledger.get_latest_trace_hash(aggregate_id)
        trace_rec = CausalTraceRecord.create(
            cae_run_id=aggregate.cae_run_id,
            program_id=aggregate.program_id,
            aggregate_id=aggregate.aggregate_id,
            workspace_id=aggregate.workspace_id,
            lane=AuthorityLane.ANALYST,
            actor_id=actor_id,
            event_type=CausalTraceEventType.ARTIFACT_CHANGED,
            payload={
                "event": "COGNITIVE_ISLAND_SUPERSEDED",
                "island_id": island_id,
                "parent_sha256": parent_sha,
                "new_sha256": computed_sha,
                "new_version": new_version,
            },
            previous_trace_sha256=prev_hash,
        )
        self._trace_ledger.append(trace_rec)

        return superseding_island

    def recompile_projections(
        self,
        *,
        aggregate_id: str,
        activation_coordinates_bps: Dict[str, int],
        viewer_state_sequence: Sequence[str],
        tension_summary: str,
        context: TenantContext,
        actor_id: str = "viewer_state_composer",
    ) -> AudienceStateProjection:
        """Dynamically recompiles derived context expressions against active Cognitive Islands."""
        aggregate = self._runtime.get_aggregate(aggregate_id)
        if not aggregate:
            raise ProgramStateAggregateNotFoundError(f"Aggregate '{aggregate_id}' not found")
        if aggregate.workspace_id != str(context.workspace_id):
            raise CrossWorkspaceLeakError("Tenant workspace mismatch")

        raw_islands = aggregate.state_data.get("cognitive_islands", [])
        if not raw_islands:
            raise AudienceLineageMissingError("Cannot recompile projections: zero active Cognitive Islands")

        islands = [CognitiveIsland.from_dict(raw) for raw in raw_islands]
        island_ids = tuple(isl.island_id for isl in islands)
        island_hashes = tuple(isl.content_sha256 for isl in islands)
        audience_id = aggregate.state_data["audience_profile"]["audience_id"]
        pid = f"proj_rec_{uuid4().hex[:12]}"

        proj_sha = AudienceStateProjection.compute_projection_hash(
            projection_id=pid,
            workspace_id=str(context.workspace_id),
            audience_id=audience_id,
            source_island_ids=island_ids,
            source_island_hashes=island_hashes,
            activation_coordinates_bps=activation_coordinates_bps,
            viewer_state_sequence=viewer_state_sequence,
            tension_summary=tension_summary,
        )

        new_projection = AudienceStateProjection(
            projection_id=pid,
            workspace_id=str(context.workspace_id),
            audience_id=audience_id,
            source_island_ids=island_ids,
            source_island_hashes=island_hashes,
            activation_coordinates_bps=dict(activation_coordinates_bps),
            viewer_state_sequence=tuple(viewer_state_sequence),
            tension_summary=tension_summary,
            projection_sha256=proj_sha,
        )

        current_data = dict(aggregate.state_data)
        projections = list(current_data.get("projections", []))
        projections.append(new_projection.to_dict())
        current_data["projections"] = projections
        current_data["current_projection"] = new_projection.to_dict()

        new_version_num = aggregate.version + 1
        now = utc_now_rfc3339()
        new_state_hash = _compute_state_hash(
            aggregate_id=aggregate.aggregate_id,
            program_id=aggregate.program_id,
            program_version=aggregate.program_version,
            current_state=aggregate.current_state,
            version=new_version_num,
            state_data=current_data,
        )

        updated_aggregate = ProgramStateAggregate(
            aggregate_id=aggregate.aggregate_id,
            workspace_id=aggregate.workspace_id,
            cae_run_id=aggregate.cae_run_id,
            program_id=aggregate.program_id,
            program_version=aggregate.program_version,
            current_state=aggregate.current_state,
            state_data=current_data,
            version=new_version_num,
            state_hash=new_state_hash,
            lifecycle=aggregate.lifecycle,
            last_receipt_id=aggregate.last_receipt_id,
            created_at=aggregate.created_at,
            updated_at=now,
        )
        self._runtime.store.save_aggregate(updated_aggregate, expected_version=aggregate.version)

        prev_hash = self._trace_ledger.get_latest_trace_hash(aggregate_id)
        trace_rec = CausalTraceRecord.create(
            cae_run_id=aggregate.cae_run_id,
            program_id=aggregate.program_id,
            aggregate_id=aggregate.aggregate_id,
            workspace_id=aggregate.workspace_id,
            lane=AuthorityLane.COMPOSER,
            actor_id=actor_id,
            event_type=CausalTraceEventType.ARTIFACT_CHANGED,
            payload={
                "event": "PROJECTIONS_RECOMPILED",
                "projection_id": pid,
                "projection_sha256": proj_sha,
                "source_island_hashes": list(island_hashes),
            },
            previous_trace_sha256=prev_hash,
        )
        self._trace_ledger.append(trace_rec)

        return new_projection

    # ------------------------------------------------------------------------
    # Snapshot & Recovery
    # ------------------------------------------------------------------------
    def get_snapshot(
        self,
        aggregate_id: str,
        context: TenantContext,
    ) -> AudienceContextSnapshot:
        """Returns an immutable snapshot of Audience Context state."""
        aggregate = self._runtime.get_aggregate(aggregate_id)
        if not aggregate:
            raise ProgramStateAggregateNotFoundError(f"Aggregate '{aggregate_id}' not found")
        if aggregate.workspace_id != str(context.workspace_id):
            raise CrossWorkspaceLeakError("Tenant workspace mismatch")

        data = aggregate.state_data
        profile = AudienceProfile.from_dict(data["audience_profile"]) if "audience_profile" in data else None
        islands = tuple(CognitiveIsland.from_dict(raw) for raw in data.get("cognitive_islands", []))
        proj = AudienceStateProjection.from_dict(data["current_projection"]) if data.get("current_projection") else None

        return AudienceContextSnapshot(
            aggregate_id=aggregate.aggregate_id,
            workspace_id=aggregate.workspace_id,
            current_state=aggregate.current_state,
            audience_profile=profile,
            cognitive_islands=islands,
            current_projection=proj,
            version=aggregate.version,
            state_hash=aggregate.state_hash,
            last_receipt_id=aggregate.last_receipt_id,
        )

    def recover_to_repairing(
        self,
        *,
        aggregate_id: str,
        failure_reason: str,
        context: TenantContext,
        actor_id: str = "audience_commander",
    ) -> ProgramStateAggregate:
        """Transitions aggregate to REPAIRING lifecycle on invariant violation or fault."""
        aggregate = self._runtime.get_aggregate(aggregate_id)
        if not aggregate:
            raise ProgramStateAggregateNotFoundError(f"Aggregate '{aggregate_id}' not found")
        if aggregate.workspace_id != str(context.workspace_id):
            raise CrossWorkspaceLeakError("Tenant workspace mismatch")

        current_data = dict(aggregate.state_data)
        current_data["repair_reason"] = failure_reason
        current_data["entered_repair_at"] = utc_now_rfc3339()

        new_version_num = aggregate.version + 1
        now = utc_now_rfc3339()
        new_state_hash = _compute_state_hash(
            aggregate_id=aggregate.aggregate_id,
            program_id=aggregate.program_id,
            program_version=aggregate.program_version,
            current_state="REPAIRING",
            version=new_version_num,
            state_data=current_data,
        )

        repairing_aggregate = ProgramStateAggregate(
            aggregate_id=aggregate.aggregate_id,
            workspace_id=aggregate.workspace_id,
            cae_run_id=aggregate.cae_run_id,
            program_id=aggregate.program_id,
            program_version=aggregate.program_version,
            current_state="REPAIRING",
            state_data=current_data,
            version=new_version_num,
            state_hash=new_state_hash,
            lifecycle=ProgramStateLifecycle.REPAIRING,
            last_receipt_id=aggregate.last_receipt_id,
            created_at=aggregate.created_at,
            updated_at=now,
        )
        self._runtime.store.save_aggregate(repairing_aggregate, expected_version=aggregate.version)

        prev_hash = self._trace_ledger.get_latest_trace_hash(aggregate_id)
        record = CausalTraceRecord.create(
            cae_run_id=aggregate.cae_run_id,
            program_id=aggregate.program_id,
            aggregate_id=aggregate.aggregate_id,
            workspace_id=aggregate.workspace_id,
            lane=AuthorityLane.COMMANDER,
            actor_id=actor_id,
            event_type=CausalTraceEventType.REPAIRED,
            payload={"reason": failure_reason, "status": "REPAIRING"},
            recovery_status="REPAIRING",
            previous_trace_sha256=prev_hash,
        )
        self._trace_ledger.append(record)

        return repairing_aggregate
