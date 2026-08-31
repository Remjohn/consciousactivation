"""Script Program Runtime Coordinator and Domain Models.

Governed by:
- Phase 4 Mandate M40 (04_PHASE_4_PRODUCTION_AND_ACCEPTANCE/M40_script_program_runtime.md)
- 00_CONTROL/30_PHASE4_PRODUCTION_CONTRACT.md
- 00_CONTROL/31_PHASE4_ASSET_LINEAGE_GRAPH.md
- 00_CONTROL/32_PHASE4_SEMANTIC_VS_RENDER_QA.md
- 00_CONTROL/34_PHASE4_OPERATOR_SUPERVISION_MATRIX.md
- FR-APP-032 Script Approval and Transfer Contract Invariants

Operating Model:
- Consumes verified SemanticProgram and EvidenceSegments with cryptographic fidelity.
- Strict 4-Lane Authority: HUNTER (JIT request / context admission), ANALYST (Semantic QA evaluation),
  COMPOSER (Script proposal authoring & compilation), COMMANDER (Authoritative operator approval & transfer contracts).
- Passive and Flat Skills: reasoning only for generation, typed operations for mutations.
- Backend-Authoritative Operator Gate: transfer is strictly blocked without operator approval receipt.
- Governed Revision: revisions produce new versions with explicit parent SHA-256 lineage and reset approval status.
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
    IProgramStateStore,
    InMemoryProgramStateStore,
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
    get_canonical_script_state_machine,
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

logger = logging.getLogger("ca_runtime.script_program")

PROGRAM_ID = "script_program"
PROGRAM_VERSION = "1.0.0"


# ============================================================================
# 1. Typed Error Hierarchy
# ============================================================================

class ScriptProgramError(ProgramStateRuntimeError):
    """Base exception for Script Program Runtime operations."""
    pass


class ScriptNotApprovedError(ScriptProgramError):
    """Raised when transfer contract creation is attempted on an unapproved script."""

    def __init__(self, script_id: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            f"Script '{script_id}' is not approved by an operator. Transfer contract creation is strictly blocked.",
            reason_code="SCRIPT_NOT_APPROVED",
            details={"script_id": script_id, **(details or {})},
        )
        self.script_id = script_id


class ScriptAlreadyApprovedError(ScriptProgramError):
    """Raised when approval is attempted on an already approved script revision."""

    def __init__(self, script_id: str):
        super().__init__(
            f"Script '{script_id}' is already approved.",
            reason_code="SCRIPT_ALREADY_APPROVED",
            details={"script_id": script_id},
        )
        self.script_id = script_id


class ScriptNotFoundError(ScriptProgramError):
    """Raised when a requested Script Package does not exist."""

    def __init__(self, script_id: str):
        super().__init__(
            f"Script Package '{script_id}' not found.",
            reason_code="SCRIPT_NOT_FOUND",
            details={"script_id": script_id},
        )
        self.script_id = script_id


class ScriptProposalNotFoundError(ScriptProgramError):
    """Raised when a requested Script Proposal does not exist."""

    def __init__(self, proposal_id: str):
        super().__init__(
            f"Script Proposal '{proposal_id}' not found.",
            reason_code="SCRIPT_PROPOSAL_NOT_FOUND",
            details={"proposal_id": proposal_id},
        )
        self.proposal_id = proposal_id


class JITAuthoringRequestNotFoundError(ScriptProgramError):
    """Raised when a requested JIT Authoring Request does not exist."""

    def __init__(self, request_id: str):
        super().__init__(
            f"JIT Authoring Request '{request_id}' not found.",
            reason_code="JIT_REQUEST_NOT_FOUND",
            details={"request_id": request_id},
        )
        self.request_id = request_id


class ScriptIntegrityError(ScriptProgramError):
    """Raised when script SHA-256 or segment quote checksum check fails."""

    def __init__(self, message: str, *, script_id: Optional[str] = None, expected_sha256: Optional[str] = None, actual_sha256: Optional[str] = None):
        super().__init__(
            message,
            reason_code="SCRIPT_INTEGRITY_VIOLATION",
            details={"script_id": script_id, "expected_sha256": expected_sha256, "actual_sha256": actual_sha256},
        )
        self.script_id = script_id
        self.expected_sha256 = expected_sha256
        self.actual_sha256 = actual_sha256


class SemanticQAFailureError(ScriptProgramError):
    """Raised when Semantic QA evaluation fails verification checks."""

    def __init__(self, message: str, *, proposal_id: Optional[str] = None, violations: Optional[List[str]] = None):
        super().__init__(
            message,
            reason_code="SEMANTIC_QA_FAILED",
            details={"proposal_id": proposal_id, "violations": violations or []},
        )
        self.proposal_id = proposal_id
        self.violations = violations or []


class EvidenceQuoteMismatchError(ScriptProgramError):
    """Raised when spoken dialogue text or hash diverges from verbatim EvidenceSegment."""

    def __init__(self, message: str, *, turn_id: Optional[str] = None, expected_sha256: Optional[str] = None, actual_sha256: Optional[str] = None):
        super().__init__(
            message,
            reason_code="EVIDENCE_QUOTE_MISMATCH",
            details={"turn_id": turn_id, "expected_sha256": expected_sha256, "actual_sha256": actual_sha256},
        )
        self.turn_id = turn_id
        self.expected_sha256 = expected_sha256
        self.actual_sha256 = actual_sha256


# ============================================================================
# 2. Typed Domain Models
# ============================================================================

@dataclass
class JITAuthoringRequest:
    """Authoritative context bundle authorizing script authoring."""
    request_id: str
    workspace_id: str
    program_ref: Dict[str, str]
    voice_dna_ref: Dict[str, str]
    role_tension_ref: Dict[str, str]
    primitive_coalition_ref: Dict[str, str]
    archetype_coalition_ref: Dict[str, str]
    approved_ingredient_refs: List[Dict[str, str]] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now_rfc3339)
    request_sha256: str = ""

    def __post_init__(self) -> None:
        if not self.request_sha256:
            self.request_sha256 = canonical_sha256({
                "request_id": self.request_id,
                "workspace_id": self.workspace_id,
                "program_ref": self.program_ref,
                "voice_dna_ref": self.voice_dna_ref,
                "role_tension_ref": self.role_tension_ref,
                "primitive_coalition_ref": self.primitive_coalition_ref,
                "archetype_coalition_ref": self.archetype_coalition_ref,
                "approved_ingredient_refs": self.approved_ingredient_refs,
            })

    def immutable_ref(self) -> Dict[str, str]:
        return {"object_id": self.request_id, "version": "1.0.0", "sha256": self.request_sha256}


@dataclass
class ScriptProposal:
    """Candidate script proposal generated by COMPOSER lane reasoning."""
    proposal_id: str
    workspace_id: str
    authoring_request_ref: Dict[str, str]
    program_ref: Dict[str, str]
    title: str
    scenes: List[Dict[str, Any]] = field(default_factory=list)
    rejected_alternative_refs: List[Dict[str, str]] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now_rfc3339)
    proposal_sha256: str = ""

    def __post_init__(self) -> None:
        if not self.proposal_sha256:
            self.proposal_sha256 = canonical_sha256({
                "proposal_id": self.proposal_id,
                "workspace_id": self.workspace_id,
                "authoring_request_ref": self.authoring_request_ref,
                "program_ref": self.program_ref,
                "title": self.title,
                "scenes": self.scenes,
                "rejected_alternative_refs": self.rejected_alternative_refs,
            })

    def immutable_ref(self) -> Dict[str, str]:
        return {"object_id": self.proposal_id, "version": "1.0.0", "sha256": self.proposal_sha256}


@dataclass
class SemanticQAReceipt:
    """Receipt documenting Semantic QA verification results."""
    receipt_id: str
    workspace_id: str
    proposal_ref: Dict[str, str]
    evaluator_id: str
    voice_dna_adherence: bool = True
    forbidden_centroids_avoided: bool = True
    wrong_reading_locks_preserved: bool = True
    quote_integrity_verified: bool = True
    verdict: str = "PASS"
    evaluation_notes: str = "Semantic QA verified successfully."
    created_at: str = field(default_factory=utc_now_rfc3339)
    receipt_sha256: str = ""

    def __post_init__(self) -> None:
        if not self.receipt_sha256:
            self.receipt_sha256 = canonical_sha256({
                "receipt_id": self.receipt_id,
                "workspace_id": self.workspace_id,
                "proposal_ref": self.proposal_ref,
                "evaluator_id": self.evaluator_id,
                "voice_dna_adherence": self.voice_dna_adherence,
                "forbidden_centroids_avoided": self.forbidden_centroids_avoided,
                "wrong_reading_locks_preserved": self.wrong_reading_locks_preserved,
                "quote_integrity_verified": self.quote_integrity_verified,
                "verdict": self.verdict,
            })

    def immutable_ref(self) -> Dict[str, str]:
        return {"object_id": self.receipt_id, "version": "1.0.0", "sha256": self.receipt_sha256}


@dataclass
class ScriptSegment:
    """Individual spoken turn or scene segment within a FinalScriptPackage."""
    segment_id: str
    scene_number: int
    speaker: str
    spoken_text: str
    start_time_ms: int
    end_time_ms: int
    source_evidence_ref: Optional[Dict[str, str]] = None
    quote_sha256: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "segment_id": self.segment_id,
            "scene_number": self.scene_number,
            "speaker": self.speaker,
            "spoken_text": self.spoken_text,
            "start_time_ms": self.start_time_ms,
            "end_time_ms": self.end_time_ms,
        }
        if self.source_evidence_ref:
            d["source_evidence_ref"] = self.source_evidence_ref
        if self.quote_sha256:
            d["quote_sha256"] = self.quote_sha256
        return d


@dataclass
class FinalScriptPackage:
    """Canonical final script package governed under CAE Phase 4."""
    script_id: str
    workspace_id: str
    version: str = "1.0.0"
    revision: int = 1
    title: str = ""
    program_ref: Dict[str, str] = field(default_factory=dict)
    proposal_ref: Dict[str, str] = field(default_factory=dict)
    role_tension_ref: Dict[str, str] = field(default_factory=dict)
    primitive_coalition_ref: Dict[str, str] = field(default_factory=dict)
    archetype_coalition_ref: Dict[str, str] = field(default_factory=dict)
    brand_context_ref: Dict[str, str] = field(default_factory=dict)
    voice_dna_ref: Dict[str, str] = field(default_factory=dict)
    segments: List[Dict[str, Any]] = field(default_factory=list)
    script_sha256: str = ""
    source_lineage_refs: List[Dict[str, str]] = field(default_factory=list)
    distillation_receipt_refs: List[Dict[str, str]] = field(default_factory=list)
    evaluation_receipt_refs: List[Dict[str, str]] = field(default_factory=list)
    wrong_reading_lock_refs: List[Dict[str, str]] = field(default_factory=list)
    operator_approved: bool = False
    composition_eligible: bool = False
    approval_receipt_ref: Optional[Dict[str, str]] = None
    supersedes_ref: Optional[Dict[str, str]] = None
    lifecycle_state: str = "draft"
    epistemic_state: str = "proposed"
    created_at: str = field(default_factory=utc_now_rfc3339)

    def __post_init__(self) -> None:
        if not self.script_sha256:
            self.script_sha256 = canonical_sha256(self.segments)

    def immutable_ref(self) -> Dict[str, str]:
        return {"object_id": self.script_id, "version": self.version, "sha256": self.script_sha256}


@dataclass
class FinalScriptApprovalReceipt:
    """Backend-authoritative operator gate approval receipt."""
    receipt_id: str
    workspace_id: str
    candidate_script_ref: Dict[str, str]
    approved_script_sha256: str
    operator_id: str
    operator_decision_ref: Dict[str, str]
    decision: str = "APPROVE"
    exact_bytes_approved: bool = True
    evaluation_refs: List[Dict[str, str]] = field(default_factory=list)
    resulting_script_ref: Dict[str, str] = field(default_factory=dict)
    rationale: str = "Approved by human operator."
    created_at: str = field(default_factory=utc_now_rfc3339)
    receipt_sha256: str = ""

    def __post_init__(self) -> None:
        if not self.receipt_sha256:
            self.receipt_sha256 = canonical_sha256({
                "receipt_id": self.receipt_id,
                "workspace_id": self.workspace_id,
                "candidate_script_ref": self.candidate_script_ref,
                "approved_script_sha256": self.approved_script_sha256,
                "operator_id": self.operator_id,
                "operator_decision_ref": self.operator_decision_ref,
                "decision": self.decision,
                "exact_bytes_approved": self.exact_bytes_approved,
                "evaluation_refs": self.evaluation_refs,
                "resulting_script_ref": self.resulting_script_ref,
                "rationale": self.rationale,
            })

    def immutable_ref(self) -> Dict[str, str]:
        return {"object_id": self.receipt_id, "version": "1.0.0", "sha256": self.receipt_sha256}


@dataclass
class ActivationTransferContract:
    """Governed contract authorizing transfer of approved script to CompositionIR / VAE."""
    contract_id: str
    workspace_id: str
    final_script_ref: Dict[str, str]
    selected_hypothesis_ref: Dict[str, str]
    role_tension_ref: Dict[str, str]
    primitive_coalition_ref: Dict[str, str]
    archetype_coalition_ref: Dict[str, str]
    source_expression_refs: List[Dict[str, str]] = field(default_factory=list)
    source_package_refs: List[Dict[str, str]] = field(default_factory=list)
    expression_moment_refs: List[Dict[str, str]] = field(default_factory=list)
    reaction_receipt_refs: List[Dict[str, str]] = field(default_factory=list)
    must_survive_properties: List[str] = field(default_factory=list)
    transformation_rules: List[str] = field(default_factory=list)
    required_changes: List[str] = field(default_factory=list)
    wrong_reading_lock_refs: List[Dict[str, str]] = field(default_factory=list)
    evaluation_profile_ref: Dict[str, str] = field(default_factory=dict)
    limitations: List[str] = field(default_factory=list)
    lifecycle_state: str = "approved"
    epistemic_state: str = "operator_confirmed"
    created_at: str = field(default_factory=utc_now_rfc3339)
    contract_sha256: str = ""

    def __post_init__(self) -> None:
        if not self.contract_sha256:
            self.contract_sha256 = canonical_sha256({
                "contract_id": self.contract_id,
                "workspace_id": self.workspace_id,
                "final_script_ref": self.final_script_ref,
                "selected_hypothesis_ref": self.selected_hypothesis_ref,
                "role_tension_ref": self.role_tension_ref,
                "primitive_coalition_ref": self.primitive_coalition_ref,
                "archetype_coalition_ref": self.archetype_coalition_ref,
                "must_survive_properties": self.must_survive_properties,
                "transformation_rules": self.transformation_rules,
                "required_changes": self.required_changes,
                "wrong_reading_lock_refs": self.wrong_reading_lock_refs,
                "lifecycle_state": self.lifecycle_state,
                "epistemic_state": self.epistemic_state,
            })

    def immutable_ref(self) -> Dict[str, str]:
        return {"object_id": self.contract_id, "version": "1.0.0", "sha256": self.contract_sha256}


# ============================================================================
# 3. Script Program Coordinator
# ============================================================================

class ScriptProgramCoordinator:
    """Governed Program Coordinator for script generation, semantic QA, operator approval, and transfer.

    Enforces:
    1. Four Authority Lanes (HUNTER, ANALYST, COMPOSER, COMMANDER).
    2. Passive and flat Skills.
    3. Backend-authoritative Operator Gate approval before transfer contract generation.
    4. Cryptographic Causal Trace Ledger chaining.
    5. Script revision lineage with explicit supersedes_ref.
    6. Multi-tenant cross-workspace isolation.
    """

    def __init__(
        self,
        runtime: Optional[UniversalProgramStateRuntime] = None,
        ledger: Optional[CausalTraceLedger] = None,
        operator_gate: Optional[OperatorGateRuntimeEngine] = None,
        store: Optional[IProgramStateStore] = None,
    ) -> None:
        self.store = store or InMemoryProgramStateStore()
        self.runtime = runtime or UniversalProgramStateRuntime(store=self.store)
        self.ledger = ledger or CausalTraceLedger()
        self.operator_gate = operator_gate or OperatorGateRuntimeEngine()

        # In-memory storage maps indexed by (workspace_id, object_id)
        self._jit_requests: Dict[Tuple[str, str], JITAuthoringRequest] = {}
        self._proposals: Dict[Tuple[str, str], ScriptProposal] = {}
        self._qa_receipts: Dict[Tuple[str, str], SemanticQAReceipt] = {}
        self._scripts: Dict[Tuple[str, str], FinalScriptPackage] = {}
        self._approval_receipts: Dict[Tuple[str, str], FinalScriptApprovalReceipt] = {}
        self._transfer_contracts: Dict[Tuple[str, str], ActivationTransferContract] = {}

    def _require_lane(self, actual: AuthorityLane, required: AuthorityLane, operation: str, aggregate_id: str = "") -> None:
        if actual != required:
            raise ProgramAuthorityLaneViolationError(
                aggregate_id=aggregate_id or f"prog:{PROGRAM_ID}",
                transition_name=operation,
                actor_lane=actual,
                required_lane=required,
            )

    def _require_tenant_workspace(self, workspace_id: str) -> None:
        tenant = require_current_tenant_context()
        if str(tenant.workspace_id) != str(workspace_id):
            raise CrossWorkspaceLeakError(
                f"Tenant workspace '{tenant.workspace_id}' cannot operate on workspace '{workspace_id}'"
            )

    def _get_aggregate_id(self, workspace_id: str, script_id: str) -> str:
        return f"prog:{PROGRAM_ID}:{workspace_id}:{script_id}"

    def _record_trace(
        self,
        *,
        aggregate_id: str,
        workspace_id: str,
        cae_run_id: str,
        lane: AuthorityLane,
        actor_id: str,
        event_type: CausalTraceEventType,
        payload: Mapping[str, Any],
        receipt_id: Optional[str] = None,
    ) -> CausalTraceRecord:
        prev_hash = self.ledger.get_latest_trace_hash(aggregate_id)
        record = CausalTraceRecord.create(
            cae_run_id=cae_run_id,
            program_id=PROGRAM_ID,
            aggregate_id=aggregate_id,
            workspace_id=workspace_id,
            lane=lane,
            actor_id=actor_id,
            event_type=event_type,
            payload=payload,
            receipt_id=receipt_id,
            previous_trace_sha256=prev_hash,
        )
        self.ledger.append(record)
        return record

    # ------------------------------------------------------------------------
    # State Lifecycle & Initialization
    # ------------------------------------------------------------------------

    def initialize_script_session(
        self,
        *,
        workspace_id: str,
        script_id: str,
    ) -> ProgramStateAggregate:
        """Initializes a new governed Script Program state aggregate in INITIAL state."""
        self._require_tenant_workspace(workspace_id)

        aggregate_id = self._get_aggregate_id(workspace_id, script_id)
        existing = self.store.get_aggregate(aggregate_id)
        if existing:
            return existing

        state_machine = self.runtime.get_state_machine(PROGRAM_ID)
        initial_payload: Dict[str, Any] = {
            "workspace_id": workspace_id,
            "script_id": script_id,
            "program_id": PROGRAM_ID,
            "lifecycle_state": "INITIAL",
            "version": 1,
        }
        state_hash = _compute_state_hash(
            aggregate_id=aggregate_id,
            program_id=PROGRAM_ID,
            program_version=PROGRAM_VERSION,
            current_state=state_machine.initial_state,
            version=1,
            state_data=initial_payload,
        )

        aggregate = ProgramStateAggregate(
            aggregate_id=aggregate_id,
            workspace_id=workspace_id,
            cae_run_id=f"run_script_{uuid4().hex[:16]}",
            program_id=PROGRAM_ID,
            program_version=PROGRAM_VERSION,
            current_state="INITIAL",
            state_data=initial_payload,
            version=1,
            state_hash=state_hash,
            lifecycle=ProgramStateLifecycle.INITIALIZED,
            last_receipt_id=None,
            created_at=utc_now_rfc3339(),
            updated_at=utc_now_rfc3339(),
        )
        self.store.save_aggregate(aggregate)

        self._record_trace(
            aggregate_id=aggregate_id,
            workspace_id=workspace_id,
            cae_run_id=aggregate.cae_run_id,
            lane=AuthorityLane.COMMANDER,
            actor_id="system",
            event_type=CausalTraceEventType.STATE_ENTERED,
            payload={"workspace_id": workspace_id, "script_id": script_id},
        )
        return aggregate

    # ------------------------------------------------------------------------
    # 1. HUNTER Lane: JIT Authoring Request
    # ------------------------------------------------------------------------

    def request_jit_authoring(
        self,
        *,
        workspace_id: str,
        script_id: str,
        request_id: str,
        program_ref: Dict[str, str],
        voice_dna_ref: Dict[str, str],
        role_tension_ref: Dict[str, str],
        primitive_coalition_ref: Dict[str, str],
        archetype_coalition_ref: Dict[str, str],
        approved_ingredient_refs: Optional[List[Dict[str, str]]] = None,
        actor_id: str = "hunter-001",
        lane: AuthorityLane = AuthorityLane.HUNTER,
    ) -> JITAuthoringRequest:
        """Admit context and request JIT authoring under the HUNTER lane."""
        self._require_tenant_workspace(workspace_id)
        self._require_lane(lane, AuthorityLane.HUNTER, "request_jit_authoring")

        aggregate_id = self._get_aggregate_id(workspace_id, script_id)
        aggregate = self.store.get_aggregate(aggregate_id)
        if not aggregate:
            aggregate = self.initialize_script_session(workspace_id=workspace_id, script_id=script_id)

        req = JITAuthoringRequest(
            request_id=request_id,
            workspace_id=workspace_id,
            program_ref=program_ref,
            voice_dna_ref=voice_dna_ref,
            role_tension_ref=role_tension_ref,
            primitive_coalition_ref=primitive_coalition_ref,
            archetype_coalition_ref=archetype_coalition_ref,
            approved_ingredient_refs=approved_ingredient_refs or [],
        )
        self._jit_requests[(workspace_id, request_id)] = req

        # Transition state aggregate
        transition_result = self.runtime.execute_transition(
            aggregate_id=aggregate_id,
            transition_name="request_jit_authoring",
            actor_id=actor_id,
            actor_lane=lane,
            payload={"request_id": request_id, "request_sha256": req.request_sha256},
            context_claims=["workspace_active", "semantic_program_verified"],
        )

        self._record_trace(
            aggregate_id=aggregate_id,
            workspace_id=workspace_id,
            cae_run_id=transition_result.aggregate.cae_run_id,
            lane=lane,
            actor_id=actor_id,
            event_type=CausalTraceEventType.STATE_ENTERED,
            payload={"request_id": request_id, "request_sha256": req.request_sha256},
        )
        return req

    # ------------------------------------------------------------------------
    # 2. COMPOSER Lane: Propose Script
    # ------------------------------------------------------------------------

    def propose_script(
        self,
        *,
        workspace_id: str,
        script_id: str,
        proposal_id: str,
        request_id: str,
        title: str,
        scenes: List[Dict[str, Any]],
        rejected_alternative_refs: Optional[List[Dict[str, str]]] = None,
        actor_id: str = "composer-001",
        lane: AuthorityLane = AuthorityLane.COMPOSER,
    ) -> ScriptProposal:
        """Author and propose script candidate under the COMPOSER lane."""
        self._require_tenant_workspace(workspace_id)
        self._require_lane(lane, AuthorityLane.COMPOSER, "propose_script")

        jit_req = self._jit_requests.get((workspace_id, request_id))
        if not jit_req:
            raise JITAuthoringRequestNotFoundError(request_id)

        aggregate_id = self._get_aggregate_id(workspace_id, script_id)
        proposal = ScriptProposal(
            proposal_id=proposal_id,
            workspace_id=workspace_id,
            authoring_request_ref=jit_req.immutable_ref(),
            program_ref=jit_req.program_ref,
            title=title,
            scenes=scenes,
            rejected_alternative_refs=rejected_alternative_refs or [],
        )
        self._proposals[(workspace_id, proposal_id)] = proposal

        transition_result = self.runtime.execute_transition(
            aggregate_id=aggregate_id,
            transition_name="propose_script",
            actor_id=actor_id,
            actor_lane=lane,
            payload={"proposal_id": proposal_id, "proposal_sha256": proposal.proposal_sha256},
            context_claims=["workspace_active", "jit_authorized"],
        )

        self._record_trace(
            aggregate_id=aggregate_id,
            workspace_id=workspace_id,
            cae_run_id=transition_result.aggregate.cae_run_id,
            lane=lane,
            actor_id=actor_id,
            event_type=CausalTraceEventType.STATE_ENTERED,
            payload={"proposal_id": proposal_id, "proposal_sha256": proposal.proposal_sha256},
        )
        return proposal

    # ------------------------------------------------------------------------
    # 3. ANALYST Lane: Semantic QA Evaluation
    # ------------------------------------------------------------------------

    def evaluate_semantic_qa(
        self,
        *,
        workspace_id: str,
        script_id: str,
        receipt_id: str,
        proposal_id: str,
        evaluator_id: str,
        voice_dna_adherence: bool = True,
        forbidden_centroids_avoided: bool = True,
        wrong_reading_locks_preserved: bool = True,
        quote_integrity_verified: bool = True,
        evaluation_notes: str = "Semantic QA verified successfully.",
        actor_id: str = "analyst-001",
        lane: AuthorityLane = AuthorityLane.ANALYST,
    ) -> SemanticQAReceipt:
        """Evaluate candidate script proposal under the ANALYST lane."""
        self._require_tenant_workspace(workspace_id)
        self._require_lane(lane, AuthorityLane.ANALYST, "evaluate_semantic_qa")

        proposal = self._proposals.get((workspace_id, proposal_id))
        if not proposal:
            raise ScriptProposalNotFoundError(proposal_id)

        violations: List[str] = []
        if not voice_dna_adherence:
            violations.append("VOICE_DNA_DRIFT_DETECTED")
        if not forbidden_centroids_avoided:
            violations.append("FORBIDDEN_CENTROID_COLLISION")
        if not wrong_reading_locks_preserved:
            violations.append("WRONG_READING_LOCK_MUTATION")
        if not quote_integrity_verified:
            violations.append("VERBATIM_QUOTE_INTEGRITY_MISMATCH")

        verdict = "PASS" if not violations else "FAIL"

        receipt = SemanticQAReceipt(
            receipt_id=receipt_id,
            workspace_id=workspace_id,
            proposal_ref=proposal.immutable_ref(),
            evaluator_id=evaluator_id,
            voice_dna_adherence=voice_dna_adherence,
            forbidden_centroids_avoided=forbidden_centroids_avoided,
            wrong_reading_locks_preserved=wrong_reading_locks_preserved,
            quote_integrity_verified=quote_integrity_verified,
            verdict=verdict,
            evaluation_notes=evaluation_notes if not violations else f"Violations: {', '.join(violations)}",
        )
        self._qa_receipts[(workspace_id, receipt_id)] = receipt

        if verdict == "FAIL":
            raise SemanticQAFailureError(
                f"Semantic QA evaluation failed for proposal '{proposal_id}': {violations}",
                proposal_id=proposal_id,
                violations=violations,
            )

        aggregate_id = self._get_aggregate_id(workspace_id, script_id)
        transition_result = self.runtime.execute_transition(
            aggregate_id=aggregate_id,
            transition_name="evaluate_semantic_qa",
            actor_id=actor_id,
            actor_lane=lane,
            payload={"receipt_id": receipt_id, "verdict": verdict},
            context_claims=["workspace_active", "script_proposal_present"],
        )

        self._record_trace(
            aggregate_id=aggregate_id,
            workspace_id=workspace_id,
            cae_run_id=transition_result.aggregate.cae_run_id,
            lane=lane,
            actor_id=actor_id,
            event_type=CausalTraceEventType.STATE_ENTERED,
            payload={"receipt_id": receipt_id, "verdict": verdict},
            receipt_id=receipt_id,
        )
        return receipt

    # ------------------------------------------------------------------------
    # 4. COMPOSER Lane: Compile Final Script Package
    # ------------------------------------------------------------------------

    def compile_final_script(
        self,
        *,
        workspace_id: str,
        script_id: str,
        proposal_id: str,
        qa_receipt_id: str,
        version: str = "1.0.0",
        revision: int = 1,
        title: str = "",
        segments: Optional[List[Dict[str, Any]]] = None,
        source_lineage_refs: Optional[List[Dict[str, str]]] = None,
        distillation_receipt_refs: Optional[List[Dict[str, str]]] = None,
        wrong_reading_lock_refs: Optional[List[Dict[str, str]]] = None,
        brand_context_ref: Optional[Dict[str, str]] = None,
        supersedes_ref: Optional[Dict[str, str]] = None,
        actor_id: str = "composer-001",
        lane: AuthorityLane = AuthorityLane.COMPOSER,
    ) -> FinalScriptPackage:
        """Compile and assemble final script package under the COMPOSER lane."""
        self._require_tenant_workspace(workspace_id)
        self._require_lane(lane, AuthorityLane.COMPOSER, "compile_final_script")

        proposal = self._proposals.get((workspace_id, proposal_id))
        if not proposal:
            raise ScriptProposalNotFoundError(proposal_id)

        qa_receipt = self._qa_receipts.get((workspace_id, qa_receipt_id))
        if not qa_receipt or qa_receipt.verdict != "PASS":
            raise SemanticQAFailureError(f"Valid passed Semantic QA receipt '{qa_receipt_id}' is required.")

        jit_req = self._jit_requests.get((workspace_id, proposal.authoring_request_ref["object_id"]))
        if not jit_req:
            raise JITAuthoringRequestNotFoundError(proposal.authoring_request_ref["object_id"])

        segs = segments or []
        # Verify quote hashes if provided
        for seg in segs:
            if "quote_sha256" in seg and "spoken_text" in seg:
                expected = hashlib.sha256(seg["spoken_text"].encode("utf-8")).hexdigest()
                if seg["quote_sha256"] != expected:
                    raise EvidenceQuoteMismatchError(
                        f"Spoken text hash mismatch in segment {seg.get('segment_id')}",
                        turn_id=seg.get("segment_id"),
                        expected_sha256=expected,
                        actual_sha256=seg["quote_sha256"],
                    )

        script = FinalScriptPackage(
            script_id=script_id,
            workspace_id=workspace_id,
            version=version,
            revision=revision,
            title=title or proposal.title,
            program_ref=proposal.program_ref,
            proposal_ref=proposal.immutable_ref(),
            role_tension_ref=jit_req.role_tension_ref,
            primitive_coalition_ref=jit_req.primitive_coalition_ref,
            archetype_coalition_ref=jit_req.archetype_coalition_ref,
            brand_context_ref=brand_context_ref or {"object_id": f"brand-ctx-{workspace_id}", "version": "1.0.0", "sha256": "bc0001"},
            voice_dna_ref=jit_req.voice_dna_ref,
            segments=segs,
            source_lineage_refs=source_lineage_refs or [],
            distillation_receipt_refs=distillation_receipt_refs or [],
            evaluation_receipt_refs=[qa_receipt.immutable_ref()],
            wrong_reading_lock_refs=wrong_reading_lock_refs or [],
            operator_approved=False,
            composition_eligible=False,
            supersedes_ref=supersedes_ref,
            lifecycle_state="draft",
            epistemic_state="proposed",
        )
        self._scripts[(workspace_id, script_id)] = script

        aggregate_id = self._get_aggregate_id(workspace_id, script_id)
        transition_result = self.runtime.execute_transition(
            aggregate_id=aggregate_id,
            transition_name="compile_final_script",
            actor_id=actor_id,
            actor_lane=lane,
            payload={"script_id": script_id, "script_sha256": script.script_sha256, "version": version},
            context_claims=["workspace_active", "semantic_qa_passed"],
        )

        self._record_trace(
            aggregate_id=aggregate_id,
            workspace_id=workspace_id,
            cae_run_id=transition_result.aggregate.cae_run_id,
            lane=lane,
            actor_id=actor_id,
            event_type=CausalTraceEventType.STATE_ENTERED,
            payload={"script_id": script_id, "script_sha256": script.script_sha256},
        )
        return script

    # ------------------------------------------------------------------------
    # 5. COMMANDER Lane: Authoritative Operator Gate Approval
    # ------------------------------------------------------------------------

    def approve_script(
        self,
        *,
        workspace_id: str,
        script_id: str,
        receipt_id: str,
        operator_id: str,
        operator_decision_ref: Dict[str, str],
        rationale: str = "Approved by human operator.",
        evaluation_refs: Optional[List[Dict[str, str]]] = None,
        actor_id: str = "commander-operator",
        lane: AuthorityLane = AuthorityLane.COMMANDER,
        requester_id: Optional[str] = None,
    ) -> Tuple[FinalScriptApprovalReceipt, FinalScriptPackage]:
        """Operator approval gate under COMMANDER lane. Enforces anti-self-approval."""
        self._require_tenant_workspace(workspace_id)
        self._require_lane(lane, AuthorityLane.COMMANDER, "approve_script")

        # Anti-Self-Approval Check
        if requester_id and requester_id == operator_id:
            raise SelfApprovalProhibitedError(
                actor_id=requester_id,
                gate_id=script_id,
            )

        script = self._scripts.get((workspace_id, script_id))
        if not script:
            raise ScriptNotFoundError(script_id)
        if script.operator_approved:
            raise ScriptAlreadyApprovedError(script_id)

        candidate_ref = script.immutable_ref()
        receipt = FinalScriptApprovalReceipt(
            receipt_id=receipt_id,
            workspace_id=workspace_id,
            candidate_script_ref=candidate_ref,
            approved_script_sha256=script.script_sha256,
            operator_id=operator_id,
            operator_decision_ref=operator_decision_ref,
            decision="APPROVE",
            exact_bytes_approved=True,
            evaluation_refs=evaluation_refs or list(script.evaluation_receipt_refs),
            resulting_script_ref=candidate_ref,
            rationale=rationale,
        )
        self._approval_receipts[(workspace_id, receipt_id)] = receipt

        # Mutate script with authoritative approval
        script.operator_approved = True
        script.composition_eligible = True
        script.lifecycle_state = "approved"
        script.epistemic_state = "operator_confirmed"
        script.approval_receipt_ref = receipt.immutable_ref()

        aggregate_id = self._get_aggregate_id(workspace_id, script_id)
        transition_result = self.runtime.execute_transition(
            aggregate_id=aggregate_id,
            transition_name="approve_script",
            actor_id=actor_id,
            actor_lane=lane,
            payload={"receipt_id": receipt_id, "operator_id": operator_id},
            context_claims=["workspace_active", "operator_gate_approved"],
        )

        self._record_trace(
            aggregate_id=aggregate_id,
            workspace_id=workspace_id,
            cae_run_id=transition_result.aggregate.cae_run_id,
            lane=lane,
            actor_id=operator_id,
            event_type=CausalTraceEventType.RECEIPT_COMMITTED,
            payload={"receipt_id": receipt_id, "decision": "APPROVE"},
            receipt_id=receipt_id,
        )
        return receipt, script

    # ------------------------------------------------------------------------
    # 6. COMMANDER Lane: Activation Transfer Contract
    # ------------------------------------------------------------------------

    def create_transfer_contract(
        self,
        *,
        workspace_id: str,
        script_id: str,
        contract_id: str,
        selected_hypothesis_ref: Dict[str, str],
        source_expression_refs: Optional[List[Dict[str, str]]] = None,
        source_package_refs: Optional[List[Dict[str, str]]] = None,
        expression_moment_refs: Optional[List[Dict[str, str]]] = None,
        reaction_receipt_refs: Optional[List[Dict[str, str]]] = None,
        must_survive_properties: Optional[List[str]] = None,
        transformation_rules: Optional[List[str]] = None,
        required_changes: Optional[List[str]] = None,
        wrong_reading_lock_refs: Optional[List[Dict[str, str]]] = None,
        evaluation_profile_ref: Optional[Dict[str, str]] = None,
        limitations: Optional[List[str]] = None,
        actor_id: str = "commander-transfer",
        lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> ActivationTransferContract:
        """Create governed transfer contract. FAILS CLOSED if script is not operator-approved."""
        self._require_tenant_workspace(workspace_id)
        self._require_lane(lane, AuthorityLane.COMMANDER, "create_transfer_contract")

        script = self._scripts.get((workspace_id, script_id))
        if not script:
            raise ScriptNotFoundError(script_id)

        # STRICT INVARIANT: Must be operator approved
        if not script.operator_approved:
            raise ScriptNotApprovedError(
                script_id,
                details={"reason": "Transfer is prohibited for unapproved script.", "workspace_id": workspace_id},
            )

        contract = ActivationTransferContract(
            contract_id=contract_id,
            workspace_id=workspace_id,
            final_script_ref=script.immutable_ref(),
            selected_hypothesis_ref=selected_hypothesis_ref,
            role_tension_ref=script.role_tension_ref,
            primitive_coalition_ref=script.primitive_coalition_ref,
            archetype_coalition_ref=script.archetype_coalition_ref,
            source_expression_refs=source_expression_refs or [],
            source_package_refs=source_package_refs or [],
            expression_moment_refs=expression_moment_refs or [],
            reaction_receipt_refs=reaction_receipt_refs or [],
            must_survive_properties=must_survive_properties or ["speaker_authenticity", "verbatim_quotes"],
            transformation_rules=transformation_rules or ["preserve_sfl_register"],
            required_changes=required_changes or [],
            wrong_reading_lock_refs=wrong_reading_lock_refs or list(script.wrong_reading_lock_refs),
            evaluation_profile_ref=evaluation_profile_ref or {"object_id": "eval-prof-default", "version": "1.0.0", "sha256": "ep0001"},
            limitations=limitations or ["supervised production"],
            lifecycle_state="approved",
            epistemic_state="operator_confirmed",
        )
        self._transfer_contracts[(workspace_id, contract_id)] = contract

        aggregate_id = self._get_aggregate_id(workspace_id, script_id)
        transition_result = self.runtime.execute_transition(
            aggregate_id=aggregate_id,
            transition_name="create_transfer_contract",
            actor_id=actor_id,
            actor_lane=lane,
            payload={"contract_id": contract_id, "contract_sha256": contract.contract_sha256},
            context_claims=["workspace_active", "operator_approved_enforced"],
        )

        self._record_trace(
            aggregate_id=aggregate_id,
            workspace_id=workspace_id,
            cae_run_id=transition_result.aggregate.cae_run_id,
            lane=lane,
            actor_id=actor_id,
            event_type=CausalTraceEventType.TRANSFERRED,
            payload={"contract_id": contract_id, "contract_sha256": contract.contract_sha256},
        )
        return contract

    # ------------------------------------------------------------------------
    # 7. Governed Revision & Version Supersession
    # ------------------------------------------------------------------------

    def revise_script(
        self,
        *,
        workspace_id: str,
        script_id: str,
        new_proposal_id: str,
        new_title: str,
        new_scenes: List[Dict[str, Any]],
        rationale: str = "Script revision requested by editorial.",
        actor_id: str = "composer-001",
        lane: AuthorityLane = AuthorityLane.COMPOSER,
    ) -> ScriptProposal:
        """Create a new governed revision proposal from an approved script."""
        self._require_tenant_workspace(workspace_id)
        self._require_lane(lane, AuthorityLane.COMPOSER, "revise_script")

        parent_script = self._scripts.get((workspace_id, script_id))
        if not parent_script:
            raise ScriptNotFoundError(script_id)

        aggregate_id = self._get_aggregate_id(workspace_id, script_id)

        # Transition back to SCRIPT_PROPOSED
        transition_result = self.runtime.execute_transition(
            aggregate_id=aggregate_id,
            transition_name="revise_script",
            actor_id=actor_id,
            actor_lane=lane,
            payload={
                "parent_script_ref": parent_script.immutable_ref(),
                "new_proposal_id": new_proposal_id,
                "rationale": rationale,
            },
            context_claims=["workspace_active", "revision_authorized"],
        )

        parent_proposal = self._proposals.get((workspace_id, parent_script.proposal_ref["object_id"]))
        authoring_request_ref = parent_proposal.authoring_request_ref if parent_proposal else parent_script.proposal_ref

        new_proposal = ScriptProposal(
            proposal_id=new_proposal_id,
            workspace_id=workspace_id,
            authoring_request_ref=authoring_request_ref,
            program_ref=parent_script.program_ref,
            title=new_title,
            scenes=new_scenes,
            rejected_alternative_refs=[parent_script.immutable_ref()],
        )
        self._proposals[(workspace_id, new_proposal_id)] = new_proposal

        self._record_trace(
            aggregate_id=aggregate_id,
            workspace_id=workspace_id,
            cae_run_id=transition_result.aggregate.cae_run_id,
            lane=lane,
            actor_id=actor_id,
            event_type=CausalTraceEventType.STATE_ENTERED,
            payload={
                "supersedes_script_sha256": parent_script.script_sha256,
                "new_proposal_id": new_proposal_id,
            },
        )
        return new_proposal

    # ------------------------------------------------------------------------
    # 8. Recovery & State Repair
    # ------------------------------------------------------------------------

    def recover_to_repairing(
        self,
        *,
        workspace_id: str,
        script_id: str,
        reason: str,
        actor_id: str = "commander-001",
        lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> ProgramStateAggregate:
        """Route script state aggregate into REPAIRING state under COMMANDER supervision."""
        self._require_tenant_workspace(workspace_id)
        self._require_lane(lane, AuthorityLane.COMMANDER, "recover_to_repairing")

        aggregate_id = self._get_aggregate_id(workspace_id, script_id)
        aggregate = self.store.get_aggregate(aggregate_id)
        if not aggregate:
            raise ScriptNotFoundError(script_id)

        repair_result = self.runtime.repair_state(
            aggregate_id=aggregate_id,
            repair_action="enter_repairing",
            repair_payload={"reason": reason},
            actor_id=actor_id,
            actor_lane=lane,
            target_state="REPAIRING",
        )
        aggregate = repair_result.aggregate

        self._record_trace(
            aggregate_id=aggregate_id,
            workspace_id=workspace_id,
            cae_run_id=aggregate.cae_run_id,
            lane=lane,
            actor_id=actor_id,
            event_type=CausalTraceEventType.BLOCKED,
            payload={"reason": reason},
        )
        return aggregate

    def repair_script(
        self,
        *,
        workspace_id: str,
        script_id: str,
        repair_action: str = "Reset to JIT_REQUESTED",
        actor_id: str = "commander-001",
        lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> ProgramStateAggregate:
        """Repair script aggregate back to JIT_REQUESTED from REPAIRING state."""
        self._require_tenant_workspace(workspace_id)
        self._require_lane(lane, AuthorityLane.COMMANDER, "repair_script")

        aggregate_id = self._get_aggregate_id(workspace_id, script_id)
        repair_result = self.runtime.repair_state(
            aggregate_id=aggregate_id,
            repair_action=repair_action,
            repair_payload={"repair_action": repair_action},
            actor_id=actor_id,
            actor_lane=lane,
            target_state="JIT_REQUESTED",
        )

        self._record_trace(
            aggregate_id=aggregate_id,
            workspace_id=workspace_id,
            cae_run_id=repair_result.aggregate.cae_run_id,
            lane=lane,
            actor_id=actor_id,
            event_type=CausalTraceEventType.REPAIRED,
            payload={"repair_action": repair_action},
        )
        aggregate = self.store.get_aggregate(aggregate_id)
        assert aggregate is not None
        return aggregate

    # ------------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------------

    def get_script(self, workspace_id: str, script_id: str) -> Optional[FinalScriptPackage]:
        return self._scripts.get((workspace_id, script_id))

    def get_proposal(self, workspace_id: str, proposal_id: str) -> Optional[ScriptProposal]:
        return self._proposals.get((workspace_id, proposal_id))

    def get_transfer_contract(self, workspace_id: str, contract_id: str) -> Optional[ActivationTransferContract]:
        return self._transfer_contracts.get((workspace_id, contract_id))
