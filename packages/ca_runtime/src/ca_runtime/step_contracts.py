"""
Workflow Step Contracts, Validator & Registry Architecture.

Governed by:
- Mandate CAE-M60 (Phase 07 - Workflow Engineering)
- Object Constitution CA-CAN-04 (docs/cae/constitutions/CA-CAN-04_WORKFLOW_PRIMITIVES.yaml)
- StateM Alignment Contract (docs/cae/CAE_Next_16_Mandate_Bundle/00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md)

Core Doctrine:
- Code owns deterministic control flow; Agents own bounded reasoning;
- Every workflow node has an explicit Step Contract distinguishing Agent from Code;
- Side effects, postconditions, failure routing, and validators are explicit;
- Mutation steps strictly require postconditions and validators;
- Internal Agent reasoning is never mistaken for a state transition; only host control commits state.
"""

from __future__ import annotations

import collections
import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from ca_contracts import canonical_json_text

from .pi_adapter import AuthorityLane
from .workflow_ir import ExecutableWorkflowIR, WorkflowIRNode
from .workflow_primitives import (
    RetryPolicyDefinition,
    WorkflowPrimitiveError,
    WorkflowPrimitiveKind,
    WorkUnitKind,
)


# ============================================================================
# 1. Error Taxonomy
# ============================================================================


class StepContractError(WorkflowPrimitiveError):
    """Base error for all Step Contract validation and execution failures."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "STEP_CONTRACT_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, reason_code=reason_code, details=details)


class StepContractValidationError(StepContractError):
    """Raised when a Step Contract fails structural or invariant validation."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, reason_code="ERR_STEP_CONTRACT_VALIDATION", details=details)


class EmptyOutputContractsError(StepContractValidationError):
    """Raised when a Step Contract declares no output contracts."""

    def __init__(self, step_id: str) -> None:
        super().__init__(
            f"Step Contract '{step_id}' declares no output contracts; non-empty outputs are mandatory",
            details={"step_id": step_id},
        )
        self.reason_code = "ERR_EMPTY_OUTPUT_CONTRACTS"


class MissingMutationValidatorError(StepContractValidationError):
    """Raised when a MUTATION_OPERATION step lacks postconditions or validators."""

    def __init__(self, step_id: str, missing_field: str) -> None:
        super().__init__(
            f"Step Contract '{step_id}' has side_effect_class='MUTATION_OPERATION' but lacks required '{missing_field}'",
            details={"step_id": step_id, "missing_field": missing_field},
        )
        self.reason_code = "ERR_MISSING_MUTATION_VALIDATOR"


class HiddenModelDependenceError(StepContractValidationError):
    """Raised when a CODE_FUNCTION step attempts to hide model inference or agent calls."""

    def __init__(self, step_id: str, hidden_ref: str) -> None:
        super().__init__(
            f"Step Contract '{step_id}' declared as CODE_FUNCTION but contains hidden model reference '{hidden_ref}'",
            details={"step_id": step_id, "hidden_ref": hidden_ref},
        )
        self.reason_code = "ERR_HIDDEN_MODEL_DEPENDENCE"


class SideEffectDeclarationMismatchError(StepContractValidationError):
    """Raised when an operation's declared side effect contradicts its execution requirements."""

    def __init__(self, step_id: str, declared_effect: str, required_effect: str) -> None:
        super().__init__(
            f"Step Contract '{step_id}' declared side_effect_class='{declared_effect}' but operation requires '{required_effect}'",
            details={"step_id": step_id, "declared_effect": declared_effect, "required_effect": required_effect},
        )
        self.reason_code = "ERR_SIDE_EFFECT_MISMATCH"


class StepContractNotFoundError(StepContractError):
    """Raised when resolving an unregistered or missing Step Contract."""

    def __init__(self, step_id: str) -> None:
        super().__init__(
            f"Step Contract '{step_id}' not found in registry",
            reason_code="ERR_STEP_CONTRACT_NOT_FOUND",
            details={"step_id": step_id},
        )


class UnregisteredStepContractError(StepContractError):
    """Raised when a workflow node references an unregistered Step Contract."""

    def __init__(self, node_id: str, contract_ref: str) -> None:
        super().__init__(
            f"Workflow node '{node_id}' references unregistered Step Contract '{contract_ref}'",
            reason_code="ERR_UNREGISTERED_STEP_CONTRACT",
            details={"node_id": node_id, "contract_ref": contract_ref},
        )


# ============================================================================
# 2. Domain Models
# ============================================================================


@dataclass(frozen=True, slots=True)
class StepContract:
    """
    Formal, hash-addressed Step Contract for an individual workflow execution node.
    """

    step_id: str
    name: str
    purpose: str
    work_unit_kind: WorkUnitKind
    target_ref: str  # Agent package ID/name or Python function path
    authority_lane: AuthorityLane
    product_boundary: str  # AHP, AIR, STUDIO, INTERVIEW, VAE, DELEGATION, BUILDER
    side_effect_class: str  # NONE, READ_ONLY, MUTATION_OPERATION
    input_contracts: Tuple[str, ...]
    output_contracts: Tuple[str, ...]
    version: str = "1.0.0"
    preconditions: Tuple[str, ...] = ()
    postconditions: Tuple[str, ...] = ()
    timeout_seconds: Optional[int] = None
    retry_policy: Optional[RetryPolicyDefinition] = None
    failure_routing: Optional[Dict[str, str]] = None  # e.g. {"ON_FAILURE": "REPAIR_STEP", "ON_TIMEOUT": "TIMEOUT_STEP"}
    validators: Tuple[str, ...] = ()  # Mandatory for MUTATION_OPERATION
    state_boundary: Optional[str] = None  # Bound StateAggregate state ID
    state_entry_context_requirements: Tuple[str, ...] = ()
    blocking_exit_checks: Tuple[str, ...] = ()
    evidence_required_to_transition: Tuple[str, ...] = ()
    contract_sha256: str = field(default="")

    def __post_init__(self) -> None:
        if not self.step_id or not self.step_id.strip():
            raise StepContractValidationError("step_id cannot be empty")
        if not self.name or not self.name.strip():
            raise StepContractValidationError("name cannot be empty")
        if not self.purpose or not self.purpose.strip():
            raise StepContractValidationError("purpose cannot be empty")
        if not self.target_ref or not self.target_ref.strip():
            raise StepContractValidationError("target_ref cannot be empty")

        if not self.output_contracts:
            raise EmptyOutputContractsError(self.step_id)

        if self.side_effect_class not in {"NONE", "READ_ONLY", "MUTATION_OPERATION"}:
            raise StepContractValidationError(
                f"Invalid side_effect_class '{self.side_effect_class}'; must be NONE, READ_ONLY, or MUTATION_OPERATION"
            )

        if self.side_effect_class == "MUTATION_OPERATION":
            if not self.postconditions:
                raise MissingMutationValidatorError(self.step_id, "postconditions")
            if not self.validators:
                raise MissingMutationValidatorError(self.step_id, "validators")

        if self.work_unit_kind == WorkUnitKind.CODE_FUNCTION:
            lowered = self.target_ref.lower()
            if any(term in lowered for term in ["agent", "model_prompt", "llm_", "gpt_", "claude_"]):
                raise HiddenModelDependenceError(self.step_id, self.target_ref)
        elif self.work_unit_kind == WorkUnitKind.AGENT_CALL:
            if self.authority_lane not in {
                AuthorityLane.HUNTER,
                AuthorityLane.ANALYST,
                AuthorityLane.COMPOSER,
                AuthorityLane.COMMANDER,
            }:
                raise StepContractValidationError(
                    f"AGENT_CALL step '{self.step_id}' must belong to an authorized AuthorityLane"
                )

        if not self.contract_sha256:
            digest = self._compute_sha256()
            object.__setattr__(self, "contract_sha256", digest)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "name": self.name,
            "version": self.version,
            "purpose": self.purpose,
            "work_unit_kind": self.work_unit_kind.value,
            "target_ref": self.target_ref,
            "authority_lane": self.authority_lane.value,
            "product_boundary": self.product_boundary,
            "side_effect_class": self.side_effect_class,
            "input_contracts": sorted(list(self.input_contracts)),
            "output_contracts": sorted(list(self.output_contracts)),
            "preconditions": sorted(list(self.preconditions)),
            "postconditions": sorted(list(self.postconditions)),
            "timeout_seconds": self.timeout_seconds,
            "retry_policy": self.retry_policy.canonical_dict() if self.retry_policy else None,
            "failure_routing": {k: self.failure_routing[k] for k in sorted(self.failure_routing)} if self.failure_routing else None,
            "validators": sorted(list(self.validators)),
            "state_boundary": self.state_boundary,
            "state_entry_context_requirements": sorted(list(self.state_entry_context_requirements)),
            "blocking_exit_checks": sorted(list(self.blocking_exit_checks)),
            "evidence_required_to_transition": sorted(list(self.evidence_required_to_transition)),
        }

    def _compute_sha256(self) -> str:
        data = self.canonical_dict()
        data["contract_sha256"] = ""
        raw = canonical_json_text(data)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def verify_integrity(self) -> bool:
        return self._compute_sha256() == self.contract_sha256


@dataclass(frozen=True, slots=True)
class StepContractCoverageReport:
    """Audit report measuring step contract coverage across a workflow."""

    workflow_id: str
    total_steps_count: int
    contracted_steps_count: int
    agent_steps_count: int
    code_steps_count: int
    mutation_steps_count: int
    coverage_percentage: int
    coverage_basis_points: int = 10000
    uncontracted_step_ids: Tuple[str, ...] = ()
    report_sha256: str = field(default="")

    def __post_init__(self) -> None:
        if not self.report_sha256:
            digest = self._compute_sha256()
            object.__setattr__(self, "report_sha256", digest)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "total_steps_count": self.total_steps_count,
            "contracted_steps_count": self.contracted_steps_count,
            "agent_steps_count": self.agent_steps_count,
            "code_steps_count": self.code_steps_count,
            "mutation_steps_count": self.mutation_steps_count,
            "coverage_percentage": self.coverage_percentage,
            "coverage_basis_points": self.coverage_basis_points,
            "uncontracted_step_ids": sorted(list(self.uncontracted_step_ids)),
        }

    def _compute_sha256(self) -> str:
        data = self.canonical_dict()
        data["report_sha256"] = ""
        raw = canonical_json_text(data)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class StepExecutionVerificationReport:
    """Verification record confirming that a step execution adhered to its Step Contract."""

    step_id: str
    run_id: str
    contract_sha256: str
    work_unit_kind: WorkUnitKind
    inputs_valid: bool
    outputs_valid: bool
    postconditions_satisfied: bool
    validators_passed: bool
    state_transition_authorized: bool
    verified_at_utc: str
    receipt_sha256: str = field(default="")

    def __post_init__(self) -> None:
        if not self.receipt_sha256:
            digest = self._compute_sha256()
            object.__setattr__(self, "receipt_sha256", digest)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "run_id": self.run_id,
            "contract_sha256": self.contract_sha256,
            "work_unit_kind": self.work_unit_kind.value,
            "inputs_valid": self.inputs_valid,
            "outputs_valid": self.outputs_valid,
            "postconditions_satisfied": self.postconditions_satisfied,
            "validators_passed": self.validators_passed,
            "state_transition_authorized": self.state_transition_authorized,
            "verified_at_utc": self.verified_at_utc,
        }

    def _compute_sha256(self) -> str:
        data = self.canonical_dict()
        data["receipt_sha256"] = ""
        raw = canonical_json_text(data)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# ============================================================================
# 3. Step Contract Validator
# ============================================================================


class StepContractValidator:
    """Validates structural and semantic invariants of Step Contracts."""

    @classmethod
    def validate_contract(cls, contract: StepContract) -> None:
        """Enforces all 7 acceptance invariants on a StepContract."""
        # 1. Required core string fields
        if not contract.step_id or not contract.step_id.strip():
            raise StepContractValidationError("step_id cannot be empty")
        if not contract.name or not contract.name.strip():
            raise StepContractValidationError("name cannot be empty")
        if not contract.purpose or not contract.purpose.strip():
            raise StepContractValidationError("purpose cannot be empty")
        if not contract.target_ref or not contract.target_ref.strip():
            raise StepContractValidationError("target_ref cannot be empty")

        # 2. Output contracts mandatory (False-proof defense 1)
        if not contract.output_contracts:
            raise EmptyOutputContractsError(contract.step_id)

        # 3. Side-effect class validity
        if contract.side_effect_class not in {"NONE", "READ_ONLY", "MUTATION_OPERATION"}:
            raise StepContractValidationError(
                f"Invalid side_effect_class '{contract.side_effect_class}'; must be NONE, READ_ONLY, or MUTATION_OPERATION"
            )

        # 4. Mutation step rigor (Gate 5 & False-proof defense 4)
        if contract.side_effect_class == "MUTATION_OPERATION":
            if not contract.postconditions:
                raise MissingMutationValidatorError(contract.step_id, "postconditions")
            if not contract.validators:
                raise MissingMutationValidatorError(contract.step_id, "validators")

        # 5. Work unit typing & hidden dependence checks (Gate 2 & False-proof defense 2)
        if contract.work_unit_kind == WorkUnitKind.CODE_FUNCTION:
            # Check target_ref does not claim model dependence
            lowered = contract.target_ref.lower()
            if any(term in lowered for term in ["agent", "model_prompt", "llm_", "gpt_", "claude_"]):
                raise HiddenModelDependenceError(contract.step_id, contract.target_ref)
        elif contract.work_unit_kind == WorkUnitKind.AGENT_CALL:
            # Must have valid authority lane
            if contract.authority_lane not in {
                AuthorityLane.HUNTER,
                AuthorityLane.ANALYST,
                AuthorityLane.COMPOSER,
                AuthorityLane.COMMANDER,
            }:
                raise StepContractValidationError(
                    f"AGENT_CALL step '{contract.step_id}' must belong to an authorized AuthorityLane"
                )

        # 6. Integrity check
        if not contract.verify_integrity():
            raise StepContractValidationError(
                f"Step Contract '{contract.step_id}' integrity hash mismatch; contract tampering detected"
            )


# ============================================================================
# 4. Step Contract Registry
# ============================================================================


class StepContractRegistry:
    """Central registry for discovering, registering, and verifying Step Contracts."""

    def __init__(self) -> None:
        self._contracts: Dict[str, StepContract] = {}

    def register(self, contract: StepContract) -> None:
        """Register a validated Step Contract."""
        StepContractValidator.validate_contract(contract)
        self._contracts[contract.step_id] = contract

    def get(self, step_id: str) -> StepContract:
        """Retrieve a registered Step Contract by ID."""
        if step_id not in self._contracts:
            raise StepContractNotFoundError(step_id)
        return self._contracts[step_id]

    def list_all(self) -> List[StepContract]:
        """Return all registered Step Contracts sorted by step_id."""
        return [self._contracts[k] for k in sorted(self._contracts)]

    def generate_coverage_report(self, ir: ExecutableWorkflowIR) -> StepContractCoverageReport:
        """
        Audit an ExecutableWorkflowIR against this registry and generate a coverage report.
        """
        total_steps = len(ir.nodes)
        contracted_steps = 0
        agent_steps = 0
        code_steps = 0
        mutation_steps = 0
        uncontracted: List[str] = []

        for node in ir.nodes:
            if node.node_id in self._contracts:
                contract = self._contracts[node.node_id]
                contracted_steps += 1
                if contract.work_unit_kind == WorkUnitKind.AGENT_CALL:
                    agent_steps += 1
                elif contract.work_unit_kind == WorkUnitKind.CODE_FUNCTION:
                    code_steps += 1
                if contract.side_effect_class == "MUTATION_OPERATION":
                    mutation_steps += 1
            else:
                uncontracted.append(node.node_id)

        coverage_pct = int(round(contracted_steps / total_steps * 100.0)) if total_steps > 0 else 100
        coverage_basis_points = int(round(contracted_steps / total_steps * 10000.0)) if total_steps > 0 else 10000

        return StepContractCoverageReport(
            workflow_id=ir.workflow_ir_id,
            total_steps_count=total_steps,
            contracted_steps_count=contracted_steps,
            agent_steps_count=agent_steps,
            code_steps_count=code_steps,
            mutation_steps_count=mutation_steps,
            coverage_percentage=coverage_pct,
            coverage_basis_points=coverage_basis_points,
            uncontracted_step_ids=tuple(uncontracted),
        )


# ============================================================================
# 5. Program Migration Helpers (Research & Collision Programs)
# ============================================================================


def create_research_canonicalization_step_contracts() -> List[StepContract]:
    """
    Complete Step Contracts migration for research_canonicalization_program.
    Migrates 4 nodes: Signal Extraction, Entity Canonicalization, OKF Synthesis, Release Gate.
    """
    c1 = StepContract(
        step_id="RESEARCH_SIGNAL_EXTRACTION",
        name="Research Signal Extraction",
        purpose="Extract grounded signals from verified research streams",
        work_unit_kind=WorkUnitKind.CODE_FUNCTION,
        target_ref="cmf_pipeline.extractors.signal_extractor",
        authority_lane=AuthorityLane.HUNTER,
        product_boundary="ATOMIC_HARNESS_PIPELINE",
        side_effect_class="READ_ONLY",
        input_contracts=("RAW_EVIDENCE_STREAM",),
        output_contracts=("RESEARCH_SIGNALS_CONTRACT",),
        preconditions=("VERIFIED_SOURCE_REFS",),
        postconditions=("GROUNDED_SIGNALS_PRESENT",),
        state_boundary="STATE_EXTRACTION",
        state_entry_context_requirements=("RAW_EVIDENCE_STREAM",),
        blocking_exit_checks=("NON_EMPTY_SIGNALS",),
        evidence_required_to_transition=("EXTRACTION_RECEIPT",),
    )

    c2 = StepContract(
        step_id="RELATIONSHIP_CANONICALIZATION",
        name="Relationship Canonicalization",
        purpose="Reason entity relationships and resolve aliases",
        work_unit_kind=WorkUnitKind.AGENT_CALL,
        target_ref="RelationshipCanonicalizationAnalystAgent",
        authority_lane=AuthorityLane.ANALYST,
        product_boundary="ACTIVATIVE_INTELLIGENCE_RUNTIME",
        side_effect_class="READ_ONLY",
        input_contracts=("RESEARCH_SIGNALS_CONTRACT",),
        output_contracts=("CANONICAL_RELATIONSHIPS_CONTRACT",),
        preconditions=("GROUNDED_SIGNALS_PRESENT",),
        postconditions=("CONTRADICTIONS_ADJUDICATED",),
        timeout_seconds=300,
        retry_policy=RetryPolicyDefinition(max_attempts=3),
        failure_routing={"ON_FAILURE": "BOUNDED_REPAIR_STEP", "ON_TIMEOUT": "FALLBACK_RELATIONSHIP_STEP"},
        state_boundary="STATE_CANONICALIZATION",
        state_entry_context_requirements=("RESEARCH_SIGNALS_CONTRACT", "ONTOLOGY_TAXONOMY"),
        blocking_exit_checks=("NO_UNRESOLVED_CONTRADICTIONS",),
        evidence_required_to_transition=("CANONICALIZATION_RECEIPT",),
    )

    c3 = StepContract(
        step_id="OKF_BUNDLE_SYNTHESIS",
        name="OKF Knowledge Bundle Synthesis",
        purpose="Compose verified Ontology Knowledge Framework bundle",
        work_unit_kind=WorkUnitKind.AGENT_CALL,
        target_ref="OKFBundleComposerAgent",
        authority_lane=AuthorityLane.COMPOSER,
        product_boundary="ACTIVATIVE_INTELLIGENCE_RUNTIME",
        side_effect_class="READ_ONLY",
        input_contracts=("CANONICAL_RELATIONSHIPS_CONTRACT",),
        output_contracts=("OKF_BUNDLE_CONTRACT",),
        preconditions=("CANONICAL_RELATIONSHIPS_CONTRACT",),
        postconditions=("OKF_SCHEMA_VALIDATED",),
        state_boundary="STATE_SYNTHESIS",
        state_entry_context_requirements=("CANONICAL_RELATIONSHIPS_CONTRACT",),
        blocking_exit_checks=("OKF_SCHEMA_VALID",),
        evidence_required_to_transition=("SYNTHESIS_RECEIPT",),
    )

    c4 = StepContract(
        step_id="OPERATOR_RELEASE_GATE",
        name="Operator Release Gate",
        purpose="Commander lane operator adjudication and production release commit",
        work_unit_kind=WorkUnitKind.CODE_FUNCTION,
        target_ref="cmf_pipeline.gates.operator_release_gate",
        authority_lane=AuthorityLane.COMMANDER,
        product_boundary="CONSCIOUS_ACTIVATIONS_STUDIO",
        side_effect_class="MUTATION_OPERATION",
        input_contracts=("OKF_BUNDLE_CONTRACT",),
        output_contracts=("RATIFIED_RELEASE_RECEIPT_CONTRACT",),
        preconditions=("OKF_SCHEMA_VALIDATED", "COMMANDER_AUTHORIZATION"),
        postconditions=("RELEASE_RECEIPT_PERSISTED", "STATE_COMMITTED"),
        validators=("VALIDATOR_RELEASE_SIGNATURE", "VALIDATOR_AUDIT_LINEAGE"),
        state_boundary="STATE_RELEASE",
        state_entry_context_requirements=("OKF_BUNDLE_CONTRACT", "OPERATOR_DECISION_RECORD"),
        blocking_exit_checks=("OPERATOR_SIGNATURE_VERIFIED",),
        evidence_required_to_transition=("RATIFIED_RELEASE_RECEIPT",),
    )

    return [c1, c2, c3, c4]


def create_collision_program_step_contracts() -> List[StepContract]:
    """
    Complete Step Contracts migration for collision_program.
    Migrates 4 nodes: Collision Hunting, Matrix of Edging, Hypothesis Composition, Commander Adjudication.
    """
    c1 = StepContract(
        step_id="COLLISION_HUNTING",
        name="Collision Candidate Hunting",
        purpose="Discover high-friction conceptual collision points",
        work_unit_kind=WorkUnitKind.AGENT_CALL,
        target_ref="CollisionHuntingAgent",
        authority_lane=AuthorityLane.HUNTER,
        product_boundary="ACTIVATIVE_INTELLIGENCE_RUNTIME",
        side_effect_class="READ_ONLY",
        input_contracts=("VERIFIED_CORPUS_REFS",),
        output_contracts=("COLLISION_CANDIDATES_CONTRACT",),
        preconditions=("CORPUS_INDEX_READY",),
        postconditions=("CANDIDATES_SCORED",),
        state_boundary="STATE_COLLISION_DISCOVERY",
        state_entry_context_requirements=("VERIFIED_CORPUS_REFS",),
        blocking_exit_checks=("CANDIDATE_SCORE_THRESHOLD",),
        evidence_required_to_transition=("HUNTING_RECEIPT",),
    )

    c2 = StepContract(
        step_id="MATRIX_OF_EDGING_ANALYSIS",
        name="Matrix of Edging Analysis",
        purpose="Analyze tension gradients across dialectical edges",
        work_unit_kind=WorkUnitKind.AGENT_CALL,
        target_ref="MatrixOfEdgingAnalystAgent",
        authority_lane=AuthorityLane.ANALYST,
        product_boundary="ACTIVATIVE_INTELLIGENCE_RUNTIME",
        side_effect_class="READ_ONLY",
        input_contracts=("COLLISION_CANDIDATES_CONTRACT",),
        output_contracts=("EDGING_MATRIX_CONTRACT",),
        preconditions=("CANDIDATES_SCORED",),
        postconditions=("GRADIENTS_CALCULATED",),
        state_boundary="STATE_EDGING_ANALYSIS",
        state_entry_context_requirements=("COLLISION_CANDIDATES_CONTRACT",),
        blocking_exit_checks=("MINIMUM_TENSION_CONFIRMED",),
        evidence_required_to_transition=("EDGING_RECEIPT",),
    )

    c3 = StepContract(
        step_id="HYPOTHESIS_COMPOSITION",
        name="Collision Hypothesis Composition",
        purpose="Compose dialectical activation hypothesis",
        work_unit_kind=WorkUnitKind.AGENT_CALL,
        target_ref="CollisionHypothesisComposerAgent",
        authority_lane=AuthorityLane.COMPOSER,
        product_boundary="ACTIVATIVE_INTELLIGENCE_RUNTIME",
        side_effect_class="READ_ONLY",
        input_contracts=("EDGING_MATRIX_CONTRACT",),
        output_contracts=("COLLISION_HYPOTHESIS_CONTRACT",),
        preconditions=("GRADIENTS_CALCULATED",),
        postconditions=("HYPOTHESIS_FORMULATED",),
        state_boundary="STATE_HYPOTHESIS_COMPOSITION",
        state_entry_context_requirements=("EDGING_MATRIX_CONTRACT",),
        blocking_exit_checks=("HYPOTHESIS_STRUCTURE_VALID",),
        evidence_required_to_transition=("COMPOSITION_RECEIPT",),
    )

    c4 = StepContract(
        step_id="COLLISION_COMMANDER_ADJUDICATION",
        name="Collision Commander Adjudication",
        purpose="Adjudicate and commit hypothesis to activation registry",
        work_unit_kind=WorkUnitKind.CODE_FUNCTION,
        target_ref="cmf_pipeline.gates.collision_adjudicator",
        authority_lane=AuthorityLane.COMMANDER,
        product_boundary="CONSCIOUS_ACTIVATIONS_STUDIO",
        side_effect_class="MUTATION_OPERATION",
        input_contracts=("COLLISION_HYPOTHESIS_CONTRACT",),
        output_contracts=("RATIFIED_COLLISION_RECORD_CONTRACT",),
        preconditions=("HYPOTHESIS_FORMULATED", "COMMANDER_AUTHORIZATION"),
        postconditions=("COLLISION_RECORD_COMMITTED", "STATE_PERSISTED"),
        validators=("VALIDATOR_COLLISION_PROOF", "VALIDATOR_AUDIT_TRAIL"),
        state_boundary="STATE_COLLISION_COMMITTED",
        state_entry_context_requirements=("COLLISION_HYPOTHESIS_CONTRACT", "COMMANDER_ADJUDICATION_RECORD"),
        blocking_exit_checks=("ADJUDICATION_SIGNATURE_VALID",),
        evidence_required_to_transition=("RATIFIED_COLLISION_RECEIPT",),
    )

    return [c1, c2, c3, c4]
