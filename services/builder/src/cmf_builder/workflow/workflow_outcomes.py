"""Workflow outcome visibility and anti-monolith checks for OD-AM-002 / ST-09.08."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
from typing import Any


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha256_of(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


class WorkflowOutcomeError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class OutcomeStatus(str, Enum):
    PASS_ = "PASS"
    FAIL = "FAIL"
    PENDING = "PENDING"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class OutcomeDimension(str, Enum):
    COMPLETION = "completion"
    CORRECTNESS = "correctness"
    AUTHORITY = "authority"
    SEMANTIC_PRESERVATION = "semantic_preservation"
    CATEGORY_PRESERVATION = "category_preservation"
    NODE_VALIDATION = "node_validation"
    CHECKPOINT_RECOVERY = "checkpoint_recovery"
    RETRY = "retry"
    CANCELLATION = "cancellation"
    ELAPSED_DURATION = "elapsed_duration"
    SIMULATED_RESOURCE_USAGE = "simulated_resource_usage"
    CONTEXT_USAGE = "context_usage"
    FAILURE_CONTAINMENT = "failure_containment"
    HUMAN_INTERVENTION = "human_intervention"
    EXTERNAL_BOUNDARY = "external_boundary"


REQUIRED_DIMENSIONS = frozenset(dimension for dimension in OutcomeDimension)


class AntiMonolithViolation(str, Enum):
    INCOMPATIBLE_ACTOR_ROLES = "incompatible_actor_roles"
    HIDDEN_HUMAN_DECISIONS = "hidden_human_decisions"
    UNTYPED_INTERMEDIATE_STATE = "untyped_intermediate_state"
    HIDDEN_EXTERNAL_EXECUTION = "hidden_external_execution"
    MISSING_CHECKPOINTS = "missing_checkpoints"
    GLOBAL_FAILURE_HANDLER = "global_failure_handler"
    UNBOUNDED_RETRY = "unbounded_retry"
    UNBOUNDED_CONTEXT = "unbounded_context"
    ORCHESTRATION_BLOB_BYPASSES_NODE_CONTRACTS = "orchestration_blob_bypasses_node_contracts"
    UNTRACEABLE_OUTCOMES = "untraceable_outcomes"


def _text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise WorkflowOutcomeError("MISSING_GOVERNED_FIELD", f"{name} is required")


@dataclass(frozen=True)
class DimensionOutcome:
    dimension: OutcomeDimension
    status: OutcomeStatus
    evidence_refs: tuple[str, ...]
    authority_ref: str
    notes: str
    simulated: bool = False

    def __post_init__(self) -> None:
        _text(self.authority_ref, "authority_ref")
        _text(self.notes, "notes")
        if self.dimension is OutcomeDimension.SIMULATED_RESOURCE_USAGE and not self.simulated:
            raise WorkflowOutcomeError("RESOURCE_USAGE_MUST_BE_SIMULATED", "OD-AM-002 permits only simulated resource evidence")
        if self.status is OutcomeStatus.NOT_APPLICABLE and "NOT_APPLICABLE" not in self.notes:
            raise WorkflowOutcomeError("NOT_APPLICABLE_BASIS_REQUIRED", "not-applicable outcomes require explicit basis")
        if self.status is not OutcomeStatus.NOT_APPLICABLE and not self.evidence_refs:
            raise WorkflowOutcomeError("OUTCOME_EVIDENCE_REQUIRED", f"{self.dimension.value} requires evidence")

    def as_dict(self) -> dict[str, Any]:
        return {
            "dimension": self.dimension.value,
            "status": self.status.value,
            "evidence_refs": list(self.evidence_refs),
            "authority_ref": self.authority_ref,
            "notes": self.notes,
            "simulated": self.simulated,
        }


@dataclass(frozen=True)
class WorkflowOutcomeVector:
    workflow_identity: str
    workflow_profile_identity: str
    node_identities: tuple[str, ...]
    dimensions: tuple[DimensionOutcome, ...]
    aggregate_status: str
    provider_validation: str
    production_ready: bool = False
    certified: bool = False
    _anchor: str = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        _text(self.workflow_identity, "workflow_identity")
        _text(self.workflow_profile_identity, "workflow_profile_identity")
        if not self.node_identities:
            raise WorkflowOutcomeError("MISSING_NODE_COVERAGE", "workflow outcome must reference node coverage")
        present = {item.dimension for item in self.dimensions}
        if present != REQUIRED_DIMENSIONS:
            missing = sorted(d.value for d in REQUIRED_DIMENSIONS - present)
            extra = sorted(d.value for d in present - REQUIRED_DIMENSIONS)
            raise WorkflowOutcomeError("INCOMPLETE_OUTCOME_DIMENSIONS", "all dimensions must be represented independently", missing=missing, extra=extra)
        if len(self.dimensions) != len(present):
            raise WorkflowOutcomeError("DUPLICATE_OUTCOME_DIMENSION", "each outcome dimension must appear once")
        if self.aggregate_status.lower() in {"pass", "green", "complete"}:
            raise WorkflowOutcomeError("AGGREGATE_STATUS_HIDES_OPEN_GATES", "aggregate pass cannot hide independent outcome dimensions")
        if self.provider_validation != "pending":
            raise WorkflowOutcomeError("PROVIDER_VALIDATION_REQUIRES_PROVIDER_EVIDENCE", "provider validation remains pending offline")
        if self.production_ready or self.certified:
            raise WorkflowOutcomeError("FALSE_PRODUCTION_OR_CERTIFICATION_CLAIM", "workflow outcome cannot claim production or certification")
        object.__setattr__(self, "_anchor", sha256_of(self._payload()))

    def _payload(self) -> dict[str, Any]:
        return {
            "workflow_identity": self.workflow_identity,
            "workflow_profile_identity": self.workflow_profile_identity,
            "node_identities": list(self.node_identities),
            "dimensions": [dimension.as_dict() for dimension in sorted(self.dimensions, key=lambda item: item.dimension.value)],
            "aggregate_status": self.aggregate_status,
            "provider_validation": self.provider_validation,
            "production_ready": False,
            "certified": False,
        }

    @property
    def outcome_identity(self) -> str:
        return sha256_of(self._payload())

    def as_dict(self) -> dict[str, Any]:
        payload = self._payload()
        if sha256_of(payload) != self._anchor:
            raise WorkflowOutcomeError("MUTATED_GOVERNED_OBJECT", "workflow outcome changed after creation")
        payload["outcome_identity"] = sha256_of(payload)
        return payload


@dataclass(frozen=True)
class WorkflowStructureDeclaration:
    workflow_identity: str
    actor_roles: tuple[str, ...]
    typed_intermediate_states: bool
    human_decisions_visible: bool
    external_nodes_visible: bool
    checkpoint_refs: tuple[str, ...]
    failure_handlers_by_node: bool
    retry_policy: str
    context_policy: str
    node_contract_refs: tuple[str, ...]
    trace_refs: tuple[str, ...]


def analyze_anti_monolith_structure(declaration: WorkflowStructureDeclaration) -> tuple[AntiMonolithViolation, ...]:
    violations: list[AntiMonolithViolation] = []
    if any("+" in role or "," in role for role in declaration.actor_roles):
        violations.append(AntiMonolithViolation.INCOMPATIBLE_ACTOR_ROLES)
    if not declaration.human_decisions_visible:
        violations.append(AntiMonolithViolation.HIDDEN_HUMAN_DECISIONS)
    if not declaration.typed_intermediate_states:
        violations.append(AntiMonolithViolation.UNTYPED_INTERMEDIATE_STATE)
    if not declaration.external_nodes_visible:
        violations.append(AntiMonolithViolation.HIDDEN_EXTERNAL_EXECUTION)
    if not declaration.checkpoint_refs:
        violations.append(AntiMonolithViolation.MISSING_CHECKPOINTS)
    if not declaration.failure_handlers_by_node:
        violations.append(AntiMonolithViolation.GLOBAL_FAILURE_HANDLER)
    if declaration.retry_policy == "unbounded":
        violations.append(AntiMonolithViolation.UNBOUNDED_RETRY)
    if declaration.context_policy == "load_everything":
        violations.append(AntiMonolithViolation.UNBOUNDED_CONTEXT)
    if not declaration.node_contract_refs:
        violations.append(AntiMonolithViolation.ORCHESTRATION_BLOB_BYPASSES_NODE_CONTRACTS)
    if not declaration.trace_refs:
        violations.append(AntiMonolithViolation.UNTRACEABLE_OUTCOMES)
    return tuple(violations)
