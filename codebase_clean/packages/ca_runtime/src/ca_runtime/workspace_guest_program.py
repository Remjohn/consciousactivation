"""Workspace + Guest Operating Context Program Coordinator.

Governed by:
- Phase 3 Mandate M25 (03_PHASE_3_INTELLIGENCE_AND_PROGRAMS/M25_workspace_guest_operating_context_program.md)
- 00_CONTROL/24_PHASE3_PROGRAM_STATE_HOOKS_MATRIX.md
- CA-CAN-01A_WORKSPACE.yaml & CA-CAN-01B_GUEST.yaml
- SPEC-TWC-UI-001 & SPEC-GST-UI-001
- Live PostgreSQL/RLS Tenancy Authority (TS-CAE-TEN-001)

Operating Model:
- One-Workspace: The root customer tenant isolation boundary (CA-ENT-001).
- One-Active-Guest: Exactly one active Guest operating context per active Program session.
  No parallel guest-tenant layer is permitted.
- Persona/Brand Context: A subordinate derived dimension retaining cryptographic SHA-256
  lineage back to authenticated source evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
import logging
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
    ProgramTransitionResult,
    UniversalProgramStateRuntime,
    get_canonical_workspace_guest_state_machine,
)
from ca_runtime.state_lifecycle import (
    CausalTraceLedger,
    StateLifecycleCoordinator,
)
from ca_runtime.tenancy import (
    CrossWorkspaceLeakError,
    TenantContext,
    TenancyError,
    TenancyViolationError,
    require_current_tenant_context,
)

logger = logging.getLogger("ca_runtime.workspace_guest_program")

PROGRAM_ID = "workspace_guest_operating_context_program"
PROGRAM_VERSION = "1.0.0"


# ============================================================================
# 1. Typed Error Hierarchy
# ============================================================================

class WorkspaceGuestProgramError(ProgramStateRuntimeError):
    """Base exception for Workspace + Guest Program execution."""
    pass


class SingleActiveGuestViolationError(WorkspaceGuestProgramError):
    """Raised when an attempt is made to bind or activate multiple active Guests concurrently."""

    def __init__(self, message: str, *, active_guest_id: Optional[str] = None, candidate_guest_id: Optional[str] = None):
        super().__init__(
            message,
            reason_code="SINGLE_ACTIVE_GUEST_VIOLATION",
            details={"active_guest_id": active_guest_id, "candidate_guest_id": candidate_guest_id},
        )
        self.active_guest_id = active_guest_id
        self.candidate_guest_id = candidate_guest_id


class LineageMissingError(WorkspaceGuestProgramError):
    """Raised when derived Persona/Brand context lacks cryptographic lineage back to source evidence."""

    def __init__(self, message: str, *, guest_id: str, missing_hashes: Sequence[str] = ()):
        super().__init__(
            message,
            reason_code="EVIDENCE_LINEAGE_MISSING",
            details={"guest_id": guest_id, "missing_hashes": list(missing_hashes)},
        )
        self.guest_id = guest_id
        self.missing_hashes = list(missing_hashes)


class GuestEvidenceIntegrityError(WorkspaceGuestProgramError):
    """Raised when guest evidence fails cryptographic verification or schema assertions."""

    def __init__(self, message: str, *, evidence_id: Optional[str] = None, reason: Optional[str] = None):
        super().__init__(
            message,
            reason_code="GUEST_EVIDENCE_INTEGRITY_ERROR",
            details={"evidence_id": evidence_id, "reason": reason},
        )
        self.evidence_id = evidence_id


class WorkspaceScopeViolationError(WorkspaceGuestProgramError):
    """Raised when cross-workspace tenant leak is detected."""

    def __init__(self, message: str, *, expected_workspace_id: str, actual_workspace_id: str):
        super().__init__(
            message,
            reason_code="WORKSPACE_SCOPE_VIOLATION",
            details={"expected_workspace_id": expected_workspace_id, "actual_workspace_id": actual_workspace_id},
        )


class GuestNotRegisteredError(WorkspaceGuestProgramError):
    """Raised when operation requires a registered guest but none is registered."""

    def __init__(self, message: str, *, aggregate_id: str):
        super().__init__(
            message,
            reason_code="GUEST_NOT_REGISTERED",
            details={"aggregate_id": aggregate_id},
        )


# ============================================================================
# 2. Strongly Typed Data Models
# ============================================================================

@dataclass(frozen=True, slots=True)
class GuestEvidenceItem:
    """Authenticated source evidence bound to a Guest operating context."""
    evidence_id: str
    source_url: str
    content_type: str
    sha256_digest: str
    captured_at: str = field(default_factory=utc_now_rfc3339)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.evidence_id or not self.evidence_id.strip():
            raise GuestEvidenceIntegrityError("evidence_id cannot be empty")
        if not self.sha256_digest or len(self.sha256_digest) != 64:
            raise GuestEvidenceIntegrityError(
                f"Invalid sha256_digest for evidence '{self.evidence_id}': must be 64-char hex string",
                evidence_id=self.evidence_id,
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "source_url": self.source_url,
            "content_type": self.content_type,
            "sha256_digest": self.sha256_digest,
            "captured_at": self.captured_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> GuestEvidenceItem:
        return cls(
            evidence_id=data["evidence_id"],
            source_url=data["source_url"],
            content_type=data["content_type"],
            sha256_digest=data["sha256_digest"],
            captured_at=data.get("captured_at", utc_now_rfc3339()),
            metadata=dict(data.get("metadata", {})),
        )


@dataclass(frozen=True, slots=True)
class DerivedBrandContext:
    """Subordinate derived Persona/Brand dimension with cryptographic evidence lineage."""
    brand_id: str
    guest_id: str
    workspace_id: str
    tone_attributes: Tuple[str, ...]
    voice_archetype: str
    visual_theme: str
    source_evidence_hashes: Tuple[str, ...]
    derived_at: str
    lineage_sha256: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "brand_id": self.brand_id,
            "guest_id": self.guest_id,
            "workspace_id": self.workspace_id,
            "tone_attributes": list(self.tone_attributes),
            "voice_archetype": self.voice_archetype,
            "visual_theme": self.visual_theme,
            "source_evidence_hashes": list(self.source_evidence_hashes),
            "derived_at": self.derived_at,
            "lineage_sha256": self.lineage_sha256,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> DerivedBrandContext:
        return cls(
            brand_id=data["brand_id"],
            guest_id=data["guest_id"],
            workspace_id=data["workspace_id"],
            tone_attributes=tuple(data.get("tone_attributes", ())),
            voice_archetype=data["voice_archetype"],
            visual_theme=data["visual_theme"],
            source_evidence_hashes=tuple(data.get("source_evidence_hashes", ())),
            derived_at=data["derived_at"],
            lineage_sha256=data["lineage_sha256"],
        )


@dataclass(frozen=True, slots=True)
class WorkspaceGuestContextSnapshot:
    """Operator-facing snapshot of active Workspace and Guest operating context."""
    aggregate_id: str
    workspace_id: str
    current_state: str
    workspace_name: Optional[str]
    active_guest_id: Optional[str]
    active_guest_pseudonym: Optional[str]
    active_guest_consent: Optional[str]
    evidence_count: int
    derived_brand_context: Optional[DerivedBrandContext]
    version: int
    state_hash: str
    last_receipt_id: Optional[str]


# ============================================================================
# 3. Workspace + Guest Program Coordinator
# ============================================================================

class WorkspaceGuestProgramCoordinator:
    """Governed Coordinator for Workspace + Guest Operating Context Program.
    
    Orchestrates the lifecycle:
      INITIAL -> WORKSPACE_CONFIGURED -> GUEST_REGISTERED -> EVIDENCE_BOUND -> CONTEXT_ACTIVE
      (with REPAIRING recovery route)
    
    Enforces:
    - Root tenant boundary at Workspace level.
    - Exactly one active Guest context per aggregate.
    - Subordinate Persona/Brand context with strict SHA-256 evidence lineage.
    - Authority Lane separation (COMMANDER, HUNTER, ANALYST).
    - Deterministic receipt emission on every transition.
    """

    def __init__(
        self,
        state_runtime: Optional[UniversalProgramStateRuntime] = None,
        coordinator: Optional[StateLifecycleCoordinator] = None,
        trace_ledger: Optional[CausalTraceLedger] = None,
    ) -> None:
        self.state_runtime = state_runtime or UniversalProgramStateRuntime()
        # Ensure state machine is registered
        self.state_machine = get_canonical_workspace_guest_state_machine()
        self.state_runtime.register_state_machine(self.state_machine)
        self.trace_ledger = trace_ledger or CausalTraceLedger()
        self.lifecycle_coordinator = coordinator or StateLifecycleCoordinator(
            state_runtime=self.state_runtime,
            trace_ledger=self.trace_ledger,
        )

    # ------------------------------------------------------------------------
    # 3.1 Initialize Program Aggregate
    # ------------------------------------------------------------------------
    def initialize_program(
        self,
        *,
        workspace_id: UUID | str,
        actor_id: str,
        cae_run_id: Optional[str] = None,
        context_claims: Optional[Sequence[str]] = None,
    ) -> ProgramStateAggregate:
        """Initializes a new Workspace + Guest Program State Aggregate in INITIAL state."""
        ws_str = str(workspace_id)
        return self.state_runtime.initialize_program_state(
            program_id=PROGRAM_ID,
            workspace_id=ws_str,
            actor_id=actor_id,
            cae_run_id=cae_run_id,
            initial_data={
                "workspace_id": ws_str,
                "workspace_configured": False,
                "active_guest_id": None,
                "active_guest": None,
                "evidence_items": [],
                "derived_brand_context": None,
            },
            context_claims=context_claims or ["workspace_active"],
        )

    # ------------------------------------------------------------------------
    # 3.2 Transition 1: INITIAL -> WORKSPACE_CONFIGURED (COMMANDER)
    # ------------------------------------------------------------------------
    def configure_workspace(
        self,
        *,
        aggregate_id: str,
        display_name: str,
        config: Optional[Dict[str, Any]] = None,
        context: Optional[TenantContext] = None,
        idempotency_key: Optional[str] = None,
    ) -> ProgramTransitionResult:
        """Configures tenant workspace parameters and bounds. Requires COMMANDER lane."""
        ctx = context or require_current_tenant_context()
        agg = self.state_runtime.get_aggregate(aggregate_id)
        if str(ctx.workspace_id) != agg.workspace_id:
            raise CrossWorkspaceLeakError(
                f"Tenant context workspace {ctx.workspace_id} does not match aggregate {agg.workspace_id}"
            )

        def _work(current_agg: ProgramStateAggregate) -> Dict[str, Any]:
            new_state = dict(current_agg.state_data)
            new_state["workspace_configured"] = True
            new_state["display_name"] = display_name
            new_state["workspace_config"] = config or {}
            new_state["configured_at"] = utc_now_rfc3339()
            new_state["configured_by"] = ctx.actor_id
            return new_state

        return self.lifecycle_coordinator.execute_state_phase(
            aggregate_id=aggregate_id,
            transition_name="configure_workspace",
            actor_id=ctx.actor_id,
            actor_lane=AuthorityLane.COMMANDER,
            work_fn=_work,
            context=ctx,
            context_claims=["workspace_active", "operator_authorized"],
            idempotency_key=idempotency_key,
        )

    # ------------------------------------------------------------------------
    # 3.3 Transition 2: WORKSPACE_CONFIGURED -> GUEST_REGISTERED (HUNTER)
    # ------------------------------------------------------------------------
    def register_guest(
        self,
        *,
        aggregate_id: str,
        pseudonym: str,
        external_reference_id: Optional[str] = None,
        consent_status: str = "CONSENT_GRANTED",
        guest_id: Optional[str] = None,
        context: Optional[TenantContext] = None,
        idempotency_key: Optional[str] = None,
    ) -> ProgramTransitionResult:
        """Registers the single active Guest participant for this operating session. Requires HUNTER lane."""
        ctx = context or require_current_tenant_context()
        agg = self.state_runtime.get_aggregate(aggregate_id)
        if str(ctx.workspace_id) != agg.workspace_id:
            raise CrossWorkspaceLeakError(
                f"Tenant context workspace {ctx.workspace_id} does not match aggregate {agg.workspace_id}"
            )

        # Single active guest verification: Fail closed if another active guest is already bound
        existing_active_guest = agg.state_data.get("active_guest_id")
        assigned_guest_id = guest_id or f"gst_{uuid4().hex[:12]}"
        if existing_active_guest is not None and existing_active_guest != assigned_guest_id:
            raise SingleActiveGuestViolationError(
                f"Single active Guest violation: aggregate '{aggregate_id}' already has active guest '{existing_active_guest}'",
                active_guest_id=existing_active_guest,
                candidate_guest_id=assigned_guest_id,
            )

        def _work(current_agg: ProgramStateAggregate) -> Dict[str, Any]:
            new_state = dict(current_agg.state_data)
            guest_record = {
                "guest_id": assigned_guest_id,
                "workspace_id": current_agg.workspace_id,
                "pseudonym": pseudonym,
                "external_reference_id": external_reference_id,
                "consent_status": consent_status,
                "registered_at": utc_now_rfc3339(),
                "registered_by": ctx.actor_id,
            }
            new_state["active_guest_id"] = assigned_guest_id
            new_state["active_guest"] = guest_record
            return new_state

        return self.lifecycle_coordinator.execute_state_phase(
            aggregate_id=aggregate_id,
            transition_name="register_guest",
            actor_id=ctx.actor_id,
            actor_lane=AuthorityLane.HUNTER,
            work_fn=_work,
            context=ctx,
            context_claims=["workspace_active", "single_active_guest_enforced"],
            idempotency_key=idempotency_key,
        )

    # ------------------------------------------------------------------------
    # 3.4 Transition 3: GUEST_REGISTERED -> EVIDENCE_BOUND (ANALYST)
    # ------------------------------------------------------------------------
    def bind_guest_evidence(
        self,
        *,
        aggregate_id: str,
        guest_id: str,
        evidence_items: Sequence[GuestEvidenceItem],
        context: Optional[TenantContext] = None,
        idempotency_key: Optional[str] = None,
    ) -> ProgramTransitionResult:
        """Binds authenticated source evidence to the active Guest operating context. Requires ANALYST lane."""
        ctx = context or require_current_tenant_context()
        agg = self.state_runtime.get_aggregate(aggregate_id)
        if str(ctx.workspace_id) != agg.workspace_id:
            raise CrossWorkspaceLeakError(
                f"Tenant context workspace {ctx.workspace_id} does not match aggregate {agg.workspace_id}"
            )

        # Enforce that guest_id matches the active guest
        active_guest_id = agg.state_data.get("active_guest_id")
        if not active_guest_id:
            raise GuestNotRegisteredError(
                f"Cannot bind evidence: no guest registered on aggregate '{aggregate_id}'",
                aggregate_id=aggregate_id,
            )
        if active_guest_id != guest_id:
            raise SingleActiveGuestViolationError(
                f"Cannot bind evidence for guest '{guest_id}': active guest is '{active_guest_id}'",
                active_guest_id=active_guest_id,
                candidate_guest_id=guest_id,
            )

        if not evidence_items:
            raise GuestEvidenceIntegrityError("evidence_items sequence cannot be empty")

        def _work(current_agg: ProgramStateAggregate) -> Dict[str, Any]:
            new_state = dict(current_agg.state_data)
            existing_items = list(new_state.get("evidence_items", []))
            for item in evidence_items:
                existing_items.append(item.to_dict())
            new_state["evidence_items"] = existing_items
            new_state["evidence_bound_at"] = utc_now_rfc3339()
            new_state["evidence_bound_by"] = ctx.actor_id
            return new_state

        return self.lifecycle_coordinator.execute_state_phase(
            aggregate_id=aggregate_id,
            transition_name="bind_guest_evidence",
            actor_id=ctx.actor_id,
            actor_lane=AuthorityLane.ANALYST,
            work_fn=_work,
            context=ctx,
            context_claims=["workspace_active", "evidence_integrity_verified"],
            idempotency_key=idempotency_key,
        )

    # ------------------------------------------------------------------------
    # 3.5 Subordinate Persona / Brand Context Derivation with Lineage
    # ------------------------------------------------------------------------
    def derive_brand_context(
        self,
        *,
        aggregate_id: str,
        guest_id: str,
        tone_attributes: Sequence[str],
        voice_archetype: str,
        visual_theme: str,
        source_evidence_hashes: Sequence[str],
        brand_id: Optional[str] = None,
        context: Optional[TenantContext] = None,
    ) -> DerivedBrandContext:
        """Derives Persona/Brand Context as a subordinate dimension with strict SHA-256 lineage.
        
        Requires non-empty source_evidence_hashes that match evidence bound to the active guest.
        """
        ctx = context or require_current_tenant_context()
        agg = self.state_runtime.get_aggregate(aggregate_id)
        if str(ctx.workspace_id) != agg.workspace_id:
            raise CrossWorkspaceLeakError(
                f"Tenant context workspace {ctx.workspace_id} does not match aggregate {agg.workspace_id}"
            )

        active_guest_id = agg.state_data.get("active_guest_id")
        if active_guest_id != guest_id:
            raise SingleActiveGuestViolationError(
                f"Cannot derive brand context for guest '{guest_id}': active guest is '{active_guest_id}'",
                active_guest_id=active_guest_id,
                candidate_guest_id=guest_id,
            )

        if not source_evidence_hashes:
            raise LineageMissingError(
                f"Brand context derivation for guest '{guest_id}' rejected: source_evidence_hashes cannot be empty",
                guest_id=guest_id,
            )

        # Verify that all source_evidence_hashes exist in bound evidence
        bound_hashes: Set[str] = {
            item["sha256_digest"] for item in agg.state_data.get("evidence_items", [])
        }
        missing_hashes = [h for h in source_evidence_hashes if h not in bound_hashes]
        if missing_hashes:
            raise LineageMissingError(
                f"Brand context derivation rejected: hashes {missing_hashes} not found in bound evidence",
                guest_id=guest_id,
                missing_hashes=missing_hashes,
            )

        now = utc_now_rfc3339()
        assigned_brand_id = brand_id or f"brand_{uuid4().hex[:12]}"
        lineage_payload = {
            "brand_id": assigned_brand_id,
            "guest_id": guest_id,
            "workspace_id": agg.workspace_id,
            "source_evidence_hashes": sorted(list(source_evidence_hashes)),
            "tone_attributes": sorted(list(tone_attributes)),
            "voice_archetype": voice_archetype,
            "visual_theme": visual_theme,
        }
        lineage_sha256 = canonical_sha256(lineage_payload)

        brand_context = DerivedBrandContext(
            brand_id=assigned_brand_id,
            guest_id=guest_id,
            workspace_id=agg.workspace_id,
            tone_attributes=tuple(tone_attributes),
            voice_archetype=voice_archetype,
            visual_theme=visual_theme,
            source_evidence_hashes=tuple(source_evidence_hashes),
            derived_at=now,
            lineage_sha256=lineage_sha256,
        )

        # Update aggregate state data with the subordinate derived dimension
        current_state_data = dict(agg.state_data)
        current_state_data["derived_brand_context"] = brand_context.to_dict()
        new_state_hash = hashlib.sha256(
            canonical_json_text(current_state_data).encode("utf-8")
        ).hexdigest()

        updated_agg = ProgramStateAggregate(
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            cae_run_id=agg.cae_run_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            current_state=agg.current_state,
            state_data=current_state_data,
            version=agg.version,
            state_hash=new_state_hash,
            lifecycle=agg.lifecycle,
            last_receipt_id=agg.last_receipt_id,
            created_at=agg.created_at,
            updated_at=now,
        )
        self.state_runtime.store.save_aggregate(updated_agg, expected_version=agg.version)
        return brand_context

    # ------------------------------------------------------------------------
    # 3.6 Transition 4: EVIDENCE_BOUND -> CONTEXT_ACTIVE (COMMANDER)
    # ------------------------------------------------------------------------
    def activate_guest_context(
        self,
        *,
        aggregate_id: str,
        guest_id: str,
        context: Optional[TenantContext] = None,
        idempotency_key: Optional[str] = None,
    ) -> ProgramTransitionResult:
        """Activates the single active Guest operating context for downstream execution. Requires COMMANDER lane."""
        ctx = context or require_current_tenant_context()
        agg = self.state_runtime.get_aggregate(aggregate_id)
        if str(ctx.workspace_id) != agg.workspace_id:
            raise CrossWorkspaceLeakError(
                f"Tenant context workspace {ctx.workspace_id} does not match aggregate {agg.workspace_id}"
            )

        active_guest_id = agg.state_data.get("active_guest_id")
        if active_guest_id != guest_id:
            raise SingleActiveGuestViolationError(
                f"Cannot activate guest context for '{guest_id}': active guest is '{active_guest_id}'",
                active_guest_id=active_guest_id,
                candidate_guest_id=guest_id,
            )

        def _work(current_agg: ProgramStateAggregate) -> Dict[str, Any]:
            new_state = dict(current_agg.state_data)
            new_state["context_activated"] = True
            new_state["context_activated_at"] = utc_now_rfc3339()
            new_state["context_activated_by"] = ctx.actor_id
            return new_state

        return self.lifecycle_coordinator.execute_state_phase(
            aggregate_id=aggregate_id,
            transition_name="activate_guest_context",
            actor_id=ctx.actor_id,
            actor_lane=AuthorityLane.COMMANDER,
            work_fn=_work,
            context=ctx,
            context_claims=["workspace_active", "lineage_provenance_verified"],
            idempotency_key=idempotency_key,
        )

    # ------------------------------------------------------------------------
    # 3.7 Repair Transition: REPAIRING -> WORKSPACE_CONFIGURED (COMMANDER)
    # ------------------------------------------------------------------------
    def repair_context(
        self,
        *,
        aggregate_id: str,
        repair_reason: str,
        context: Optional[TenantContext] = None,
        idempotency_key: Optional[str] = None,
    ) -> ProgramTransitionResult:
        """Executes governed repair transition from REPAIRING back to WORKSPACE_CONFIGURED. Requires COMMANDER lane."""
        ctx = context or require_current_tenant_context()
        agg = self.state_runtime.get_aggregate(aggregate_id)
        if str(ctx.workspace_id) != agg.workspace_id:
            raise CrossWorkspaceLeakError(
                f"Tenant context workspace {ctx.workspace_id} does not match aggregate {agg.workspace_id}"
            )

        def _work(current_agg: ProgramStateAggregate) -> Dict[str, Any]:
            new_state = dict(current_agg.state_data)
            new_state["last_repair_reason"] = repair_reason
            new_state["repaired_at"] = utc_now_rfc3339()
            new_state["repaired_by"] = ctx.actor_id
            return new_state

        return self.lifecycle_coordinator.execute_state_phase(
            aggregate_id=aggregate_id,
            transition_name="repair_context",
            actor_id=ctx.actor_id,
            actor_lane=AuthorityLane.COMMANDER,
            work_fn=_work,
            context=ctx,
            context_claims=["workspace_active", "operator_authorized"],
            idempotency_key=idempotency_key,
        )

    # ------------------------------------------------------------------------
    # 3.8 Snapshot Inspection
    # ------------------------------------------------------------------------
    def get_context_snapshot(self, aggregate_id: str) -> WorkspaceGuestContextSnapshot:
        """Returns strongly-typed operator snapshot of active Workspace and Guest context."""
        agg = self.state_runtime.get_aggregate(aggregate_id)
        state_data = agg.state_data
        active_guest = state_data.get("active_guest") or {}
        derived_brand_raw = state_data.get("derived_brand_context")
        derived_brand = DerivedBrandContext.from_dict(derived_brand_raw) if derived_brand_raw else None

        return WorkspaceGuestContextSnapshot(
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            current_state=agg.current_state,
            workspace_name=state_data.get("display_name"),
            active_guest_id=state_data.get("active_guest_id"),
            active_guest_pseudonym=active_guest.get("pseudonym"),
            active_guest_consent=active_guest.get("consent_status"),
            evidence_count=len(state_data.get("evidence_items", [])),
            derived_brand_context=derived_brand,
            version=agg.version,
            state_hash=agg.state_hash,
            last_receipt_id=agg.last_receipt_id,
        )
