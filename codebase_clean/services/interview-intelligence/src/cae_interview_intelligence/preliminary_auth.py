"""Fail-closed preliminary authorization for non-production CAE executions.

Mandate: CA-M024 / FR-024

This module is the local pre-flight boundary for exploratory, drafting, and other
non-production pipeline executions. It validates two independent classes of
preconditions before work is dispatched:

* the caller has the permission required by the requested execution class; and
* the requested resources fit the applicable hard quotas.

Policy and requests are immutable, evaluation is deterministic, and a denial
returns a structured gap report. No downstream execution is invoked by this
module.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from typing import Any, Callable, Mapping, Optional, Sequence

MANDATE_ID = "CA-M024"
REQUIREMENT_ID = "FR-024"
POLICY_VERSION = "CA-M024-PRELIMINARY-AUTH-V1"


class PreliminaryAuthError(ValueError):
    """Base error for malformed policy or request input."""


class InvalidPolicyError(PreliminaryAuthError):
    """Raised when a preliminary authorization policy is malformed."""


class InvalidRequestError(PreliminaryAuthError):
    """Raised when a preliminary authorization request is malformed."""


class ExecutionKind(str, Enum):
    EXPLORATORY = "EXPLORATORY"
    DRAFTING = "DRAFTING"
    NON_PRODUCTION = "NON_PRODUCTION"


class PolicyMode(str, Enum):
    YOLO = "YOLO"
    CHECKPOINT = "CHECKPOINT"
    STRICT = "STRICT"
    CUSTOM = "CUSTOM"


class AuthorizationDecision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"


class GapCode(str, Enum):
    UNAUTHENTICATED = "UNAUTHENTICATED"
    INVALID_EXECUTION_KIND = "INVALID_EXECUTION_KIND"
    PERMISSION_MISSING = "PERMISSION_MISSING"
    PRODUCTION_EXECUTION_FORBIDDEN = "PRODUCTION_EXECUTION_FORBIDDEN"
    TOKEN_QUOTA_EXCEEDED = "TOKEN_QUOTA_EXCEEDED"
    TIME_QUOTA_EXCEEDED = "TIME_QUOTA_EXCEEDED"
    COST_QUOTA_EXCEEDED = "COST_QUOTA_EXCEEDED"
    CONCURRENCY_QUOTA_EXCEEDED = "CONCURRENCY_QUOTA_EXCEEDED"


DEFAULT_PERMISSIONS: Mapping[ExecutionKind, frozenset[str]] = {
    ExecutionKind.EXPLORATORY: frozenset({"INTERVIEW_EXPLORE"}),
    ExecutionKind.DRAFTING: frozenset({"INTERVIEW_DRAFT"}),
    ExecutionKind.NON_PRODUCTION: frozenset({"PIPELINE_NON_PRODUCTION"}),
}


@dataclass(frozen=True, slots=True)
class ResourceQuota:
    """Hard upper bounds for one execution and its already-consumed allowance."""

    max_tokens: Optional[int] = None
    max_wall_seconds: Optional[float] = None
    max_cost_units: Optional[int] = None
    max_concurrent_runs: Optional[int] = None
    tokens_used: int = 0
    wall_seconds_used: float = 0.0
    cost_units_used: int = 0
    concurrent_runs: int = 0

    def __post_init__(self) -> None:
        for name in ("max_tokens", "max_cost_units", "max_concurrent_runs"):
            value = getattr(self, name)
            if value is not None and int(value) < 0:
                raise InvalidPolicyError(f"{name} must be >= 0 or None")
        if self.max_wall_seconds is not None and float(self.max_wall_seconds) < 0:
            raise InvalidPolicyError("max_wall_seconds must be >= 0 or None")
        for name in ("tokens_used", "cost_units_used", "concurrent_runs"):
            if int(getattr(self, name)) < 0:
                raise InvalidPolicyError(f"{name} must be >= 0")
        if float(self.wall_seconds_used) < 0:
            raise InvalidPolicyError("wall_seconds_used must be >= 0")


@dataclass(frozen=True, slots=True)
class PreliminaryAuthPolicy:
    """Immutable policy governing preliminary non-production execution."""

    policy_id: str
    policy_version: str = POLICY_VERSION
    mode: PolicyMode = PolicyMode.CHECKPOINT
    allowed_permissions: frozenset[str] = frozenset()
    quotas: ResourceQuota = ResourceQuota(
        max_tokens=100_000,
        max_wall_seconds=3_600,
        max_cost_units=10_000,
        max_concurrent_runs=4,
    )
    allow_production: bool = False

    def __post_init__(self) -> None:
        policy_id = str(self.policy_id).strip()
        policy_version = str(self.policy_version).strip()
        try:
            mode = self.mode if isinstance(self.mode, PolicyMode) else PolicyMode(str(self.mode).upper())
        except ValueError as exc:
            raise InvalidPolicyError(f"unsupported policy mode: {self.mode!r}") from exc
        permissions = frozenset(str(p).strip().upper() for p in self.allowed_permissions if str(p).strip())
        if not policy_id:
            raise InvalidPolicyError("policy_id is required")
        if not policy_version:
            raise InvalidPolicyError("policy_version is required")
        if self.allow_production:
            raise InvalidPolicyError("preliminary authorization cannot enable production execution")
        object.__setattr__(self, "policy_id", policy_id)
        object.__setattr__(self, "policy_version", policy_version)
        object.__setattr__(self, "mode", mode)
        object.__setattr__(self, "allowed_permissions", permissions)

    @classmethod
    def default(cls, *, policy_id: str = "ca-m024-default", mode: PolicyMode = PolicyMode.CHECKPOINT) -> "PreliminaryAuthPolicy":
        return cls(
            policy_id=policy_id,
            mode=mode,
            allowed_permissions=frozenset({
                "INTERVIEW_EXPLORE",
                "INTERVIEW_DRAFT",
                "PIPELINE_NON_PRODUCTION",
            }),
        )

    @property
    def policy_sha256(self) -> str:
        return _sha256(self.canonical_payload())

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "mode": self.mode.value,
            "allowed_permissions": sorted(self.allowed_permissions),
            "quotas": {
                "max_tokens": self.quotas.max_tokens,
                "max_wall_seconds": self.quotas.max_wall_seconds,
                "max_cost_units": self.quotas.max_cost_units,
                "max_concurrent_runs": self.quotas.max_concurrent_runs,
            },
            "allow_production": self.allow_production,
        }


@dataclass(frozen=True, slots=True)
class PreliminaryExecutionRequest:
    """Immutable caller and resource declaration evaluated before dispatch."""

    execution_id: str
    actor_id: str
    authenticated: bool
    execution_kind: ExecutionKind | str
    permission: str
    production: bool = False
    requested_tokens: int = 0
    requested_wall_seconds: float = 0.0
    requested_cost_units: int = 0
    request_concurrent_runs: int = 1

    def __post_init__(self) -> None:
        if not str(self.execution_id).strip():
            raise InvalidRequestError("execution_id is required")
        if not str(self.actor_id).strip():
            raise InvalidRequestError("actor_id is required")
        if int(self.requested_tokens) < 0:
            raise InvalidRequestError("requested_tokens must be >= 0")
        if float(self.requested_wall_seconds) < 0:
            raise InvalidRequestError("requested_wall_seconds must be >= 0")
        if int(self.requested_cost_units) < 0:
            raise InvalidRequestError("requested_cost_units must be >= 0")
        if int(self.request_concurrent_runs) < 1:
            raise InvalidRequestError("request_concurrent_runs must be >= 1")
        try:
            kind = self.execution_kind if isinstance(self.execution_kind, ExecutionKind) else ExecutionKind(str(self.execution_kind).upper())
        except ValueError as exc:
            raise InvalidRequestError(f"unsupported execution_kind: {self.execution_kind!r}") from exc
        permission = str(self.permission).strip().upper()
        if not permission:
            raise InvalidRequestError("permission is required")
        object.__setattr__(self, "execution_kind", kind)
        object.__setattr__(self, "permission", permission)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "PreliminaryExecutionRequest":
        return cls(**dict(value))


@dataclass(frozen=True, slots=True)
class AuthorizationGap:
    code: str
    control: str
    message: str
    observed: Any
    required: Any

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "control": self.control,
            "message": self.message,
            "observed": self.observed,
            "required": self.required,
        }


@dataclass(frozen=True, slots=True)
class PreliminaryAuthReport:
    """Structured evidence for an authorization decision."""

    decision: AuthorizationDecision
    mandate_id: str
    requirement_id: str
    policy_id: str
    policy_version: str
    policy_sha256: str
    mode: str
    execution_id: str
    actor_id: str
    execution_kind: str
    gaps: tuple[AuthorizationGap, ...]
    quota_snapshot: Mapping[str, Any]
    receipt_sha256: str

    @property
    def allowed(self) -> bool:
        return self.decision is AuthorizationDecision.ALLOW

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision.value,
            "mandate_id": self.mandate_id,
            "requirement_id": self.requirement_id,
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "policy_sha256": self.policy_sha256,
            "mode": self.mode,
            "execution_id": self.execution_id,
            "actor_id": self.actor_id,
            "execution_kind": self.execution_kind,
            "gaps": [gap.to_dict() for gap in self.gaps],
            "quota_snapshot": dict(self.quota_snapshot),
            "receipt_sha256": self.receipt_sha256,
        }


@dataclass(frozen=True, slots=True)
class PreliminaryAuthDecision:
    """Canonical result of the preliminary authorization boundary."""

    allowed: bool
    report: PreliminaryAuthReport

    def require_allowed(self) -> None:
        if not self.allowed:
            raise PreliminaryAuthorizationBlocked(self.report)


class PreliminaryAuthorizationBlocked(RuntimeError):
    """Raised by ``require_allowed`` when pre-flight authorization fails."""

    def __init__(self, report: PreliminaryAuthReport) -> None:
        self.report = report
        codes = ", ".join(gap.code for gap in report.gaps)
        super().__init__(f"{REQUIREMENT_ID} blocked execution {report.execution_id}: {codes}")


def _sha256(payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _gap(code: GapCode, control: str, message: str, observed: Any, required: Any) -> AuthorizationGap:
    return AuthorizationGap(code.value, control, message, observed, required)


def evaluate_preliminary_auth(
    request: PreliminaryExecutionRequest | Mapping[str, Any],
    policy: PreliminaryAuthPolicy,
) -> PreliminaryAuthDecision:
    """Evaluate authentication, permission, environment and hard quota checks."""
    req = request if isinstance(request, PreliminaryExecutionRequest) else PreliminaryExecutionRequest.from_mapping(request)
    gaps: list[AuthorizationGap] = []

    if not req.authenticated:
        gaps.append(_gap(GapCode.UNAUTHENTICATED, "AUTHENTICATED_ACTOR", "actor is not authenticated", False, True))

    required_permission = {
        ExecutionKind.EXPLORATORY: "INTERVIEW_EXPLORE",
        ExecutionKind.DRAFTING: "INTERVIEW_DRAFT",
        ExecutionKind.NON_PRODUCTION: "PIPELINE_NON_PRODUCTION",
    }.get(req.execution_kind)
    if required_permission is None:
        gaps.append(_gap(GapCode.INVALID_EXECUTION_KIND, "EXECUTION_KIND", "execution kind is not supported", req.execution_kind.value, [k.value for k in ExecutionKind]))
    else:
        if req.permission != required_permission or required_permission not in policy.allowed_permissions:
            gaps.append(
                _gap(
                    GapCode.PERMISSION_MISSING,
                    "EXECUTION_PERMISSION",
                    f"required permission {required_permission} is not granted",
                    req.permission,
                    required_permission,
                )
            )

    if req.production or req.execution_kind is ExecutionKind.NON_PRODUCTION and req.production:
        gaps.append(_gap(GapCode.PRODUCTION_EXECUTION_FORBIDDEN, "PRODUCTION_BOUNDARY", "preliminary authorization cannot authorize production execution", True, False))

    q = policy.quotas
    projected_tokens = q.tokens_used + req.requested_tokens
    if q.max_tokens is not None and projected_tokens > q.max_tokens:
        gaps.append(_gap(GapCode.TOKEN_QUOTA_EXCEEDED, "TOKEN_QUOTA", "requested token budget exceeds the hard quota", projected_tokens, q.max_tokens))

    projected_time = q.wall_seconds_used + req.requested_wall_seconds
    if q.max_wall_seconds is not None and projected_time > q.max_wall_seconds:
        gaps.append(_gap(GapCode.TIME_QUOTA_EXCEEDED, "WALL_TIME_QUOTA", "requested wall time exceeds the hard quota", projected_time, q.max_wall_seconds))

    projected_cost = q.cost_units_used + req.requested_cost_units
    if q.max_cost_units is not None and projected_cost > q.max_cost_units:
        gaps.append(_gap(GapCode.COST_QUOTA_EXCEEDED, "COST_QUOTA", "requested cost exceeds the hard quota", projected_cost, q.max_cost_units))

    projected_concurrency = q.concurrent_runs + req.request_concurrent_runs
    if q.max_concurrent_runs is not None and projected_concurrency > q.max_concurrent_runs:
        gaps.append(_gap(GapCode.CONCURRENCY_QUOTA_EXCEEDED, "CONCURRENCY_QUOTA", "requested concurrency exceeds the hard quota", projected_concurrency, q.max_concurrent_runs))

    snapshot = {
        "max_tokens": q.max_tokens,
        "projected_tokens": projected_tokens,
        "max_wall_seconds": q.max_wall_seconds,
        "projected_wall_seconds": projected_time,
        "max_cost_units": q.max_cost_units,
        "projected_cost_units": projected_cost,
        "max_concurrent_runs": q.max_concurrent_runs,
        "projected_concurrent_runs": projected_concurrency,
    }
    decision = AuthorizationDecision.DENY if gaps else AuthorizationDecision.ALLOW
    body = {
        "decision": decision.value,
        "mandate_id": MANDATE_ID,
        "requirement_id": REQUIREMENT_ID,
        "policy_id": policy.policy_id,
        "policy_version": policy.policy_version,
        "policy_sha256": policy.policy_sha256,
        "mode": policy.mode.value,
        "execution_id": req.execution_id,
        "actor_id": req.actor_id,
        "execution_kind": req.execution_kind.value,
        "gaps": [gap.to_dict() for gap in gaps],
        "quota_snapshot": snapshot,
    }
    report = PreliminaryAuthReport(
        decision=decision,
        mandate_id=MANDATE_ID,
        requirement_id=REQUIREMENT_ID,
        policy_id=policy.policy_id,
        policy_version=policy.policy_version,
        policy_sha256=policy.policy_sha256,
        mode=policy.mode.value,
        execution_id=req.execution_id,
        actor_id=req.actor_id,
        execution_kind=req.execution_kind.value,
        gaps=tuple(gaps),
        quota_snapshot=snapshot,
        receipt_sha256=_sha256(body),
    )
    return PreliminaryAuthDecision(allowed=report.allowed, report=report)


def authorize_preliminary_execution(
    request: PreliminaryExecutionRequest | Mapping[str, Any],
    policy: PreliminaryAuthPolicy,
) -> PreliminaryAuthReport:
    """Convenience API returning the structured report."""
    return evaluate_preliminary_auth(request, policy).report


def gate_preliminary_execution(
    request: PreliminaryExecutionRequest | Mapping[str, Any],
    policy: PreliminaryAuthPolicy,
    execute: Optional[Callable[[], Any]] = None,
) -> Any:
    """Authorize before optional downstream execution; fail closed on denial."""
    decision = evaluate_preliminary_auth(request, policy)
    decision.require_allowed()
    return execute() if execute is not None else decision.report


# Compatibility aliases for callers that prefer "pre-flight" naming.
PreflightAuthPolicy = PreliminaryAuthPolicy
PreflightExecutionRequest = PreliminaryExecutionRequest
PreflightAuthDecision = PreliminaryAuthDecision
PreflightAuthorizationBlocked = PreliminaryAuthorizationBlocked

authorize_preflight = authorize_preliminary_execution


__all__ = [
    "MANDATE_ID",
    "REQUIREMENT_ID",
    "POLICY_VERSION",
    "ExecutionKind",
    "PolicyMode",
    "AuthorizationDecision",
    "GapCode",
    "ResourceQuota",
    "PreliminaryAuthPolicy",
    "PreliminaryExecutionRequest",
    "AuthorizationGap",
    "PreliminaryAuthReport",
    "PreliminaryAuthDecision",
    "PreliminaryAuthorizationBlocked",
    "PreliminaryAuthError",
    "InvalidPolicyError",
    "InvalidRequestError",
    "evaluate_preliminary_auth",
    "authorize_preliminary_execution",
    "gate_preliminary_execution",
    "PreflightAuthPolicy",
    "PreflightExecutionRequest",
    "PreflightAuthDecision",
    "PreflightAuthorizationBlocked",
    "authorize_preflight",
]
