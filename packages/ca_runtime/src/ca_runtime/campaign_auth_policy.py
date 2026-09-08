"""Campaign authorization policy for production execution.

Mandate: CA-M025 / FR-POL-001
Stage: 12 Human Authorization

This module is the bounded runtime policy boundary for production-tier
campaign execution. It enforces three independent requirements:

1. authentication and role-based authorization;
2. production-tier constraints; and
3. spend-budget thresholds.

Every evaluation returns an immutable, evidence-bearing decision receipt. Denials
are explicit and descriptive; no policy failure silently downgrades to a less
restrictive execution mode.

The module intentionally does not persist receipts or bind policy revisions to
execution leases. Those concerns belong to later mandates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
from typing import Any, Mapping, Optional, Sequence, Tuple


MANDATE_ID = "CA-M025"
REQUIREMENT_ID = "FR-POL-001"
POLICY_SCHEMA_VERSION = "1.0.0"

# Canonical production roles already used by CAE campaign/operator surfaces.
CANONICAL_CAMPAIGN_ROLES: Tuple[str, ...] = (
    "HUNTER",
    "ANALYST",
    "COMPOSER",
    "COMMANDER",
    "OPERATOR",
    "EVALUATOR",
)

# The production policy is intentionally conservative: only the human control
# roles may authorize a production-tier campaign execution.
DEFAULT_PRODUCTION_AUTHORIZED_ROLES = frozenset({"COMMANDER", "OPERATOR"})

# The module is specifically a production policy boundary. A production policy
# cannot be used to authorize a non-production execution request.
PRODUCTION_TIER = "PRODUCTION"


class CampaignAuthPolicyError(ValueError):
    """Base error for invalid policy or execution inputs."""


class InvalidPolicyError(CampaignAuthPolicyError):
    """Raised when a policy contains an invalid role or threshold."""


class InvalidExecutionRequestError(CampaignAuthPolicyError):
    """Raised when an execution request is structurally invalid."""


class CampaignRole(str, Enum):
    HUNTER = "HUNTER"
    ANALYST = "ANALYST"
    COMPOSER = "COMPOSER"
    COMMANDER = "COMMANDER"
    OPERATOR = "OPERATOR"
    EVALUATOR = "EVALUATOR"


class CampaignTier(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"


class AuthorizationDecision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"


class DenialReasonCode(str, Enum):
    UNAUTHENTICATED_EXECUTION = "UNAUTHENTICATED_EXECUTION"
    ROLE_NOT_AUTHORIZED = "ROLE_NOT_AUTHORIZED"
    TIER_NOT_ALLOWED = "TIER_NOT_ALLOWED"
    INVALID_SPEND_AMOUNT = "INVALID_SPEND_AMOUNT"
    SPEND_BUDGET_EXCEEDED = "SPEND_BUDGET_EXCEEDED"
    INVALID_REQUEST = "INVALID_REQUEST"


@dataclass(frozen=True, slots=True)
class CampaignAuthorizationPolicy:
    """Validated, immutable policy governing a production campaign run.

    ``budget_limit_units`` is the campaign's total spend ceiling and
    ``max_run_spend_units`` is an optional per-run ceiling. A request must
    satisfy both ceilings after accounting for ``spend_to_date_units``.
    """

    policy_id: str = "ca-m025-production-default"
    policy_version: str = POLICY_SCHEMA_VERSION
    production_tier: str = PRODUCTION_TIER
    authorized_roles: frozenset[str] = DEFAULT_PRODUCTION_AUTHORIZED_ROLES
    budget_limit_units: int = 0
    max_run_spend_units: Optional[int] = None

    def __post_init__(self) -> None:
        policy_id = str(self.policy_id).strip()
        policy_version = str(self.policy_version).strip()
        tier = _normalize_token(self.production_tier)
        roles = frozenset(_normalize_role(role) for role in self.authorized_roles)

        if not policy_id:
            raise InvalidPolicyError("policy_id must be non-empty")
        if not policy_version:
            raise InvalidPolicyError("policy_version must be non-empty")
        if tier != PRODUCTION_TIER:
            raise InvalidPolicyError(
                f"production policy tier must be {PRODUCTION_TIER}, got {tier!r}"
            )
        unknown_roles = roles.difference(CANONICAL_CAMPAIGN_ROLES)
        if unknown_roles:
            raise InvalidPolicyError(
                "authorized_roles contains unknown role(s): "
                + ", ".join(sorted(unknown_roles))
            )
        if not roles:
            raise InvalidPolicyError("authorized_roles must contain at least one role")
        if int(self.budget_limit_units) < 0:
            raise InvalidPolicyError("budget_limit_units must be >= 0")
        if self.max_run_spend_units is not None and int(self.max_run_spend_units) < 0:
            raise InvalidPolicyError("max_run_spend_units must be >= 0")

        object.__setattr__(self, "policy_id", policy_id)
        object.__setattr__(self, "policy_version", policy_version)
        object.__setattr__(self, "production_tier", tier)
        object.__setattr__(self, "authorized_roles", roles)
        object.__setattr__(self, "budget_limit_units", int(self.budget_limit_units))
        if self.max_run_spend_units is not None:
            object.__setattr__(self, "max_run_spend_units", int(self.max_run_spend_units))

    @classmethod
    def production_default(
        cls,
        *,
        budget_limit_units: int,
        max_run_spend_units: Optional[int] = None,
        authorized_roles: Optional[Sequence[str]] = None,
        policy_id: str = "ca-m025-production-default",
        policy_version: str = POLICY_SCHEMA_VERSION,
    ) -> "CampaignAuthorizationPolicy":
        """Build the canonical production policy with explicit budget thresholds."""
        return cls(
            policy_id=policy_id,
            policy_version=policy_version,
            budget_limit_units=budget_limit_units,
            max_run_spend_units=max_run_spend_units,
            authorized_roles=(
                frozenset(authorized_roles)
                if authorized_roles is not None
                else DEFAULT_PRODUCTION_AUTHORIZED_ROLES
            ),
        )

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "CampaignAuthorizationPolicy":
        """Parse a runtime/API mapping without accepting silent aliases."""
        required = {"budget_limit_units"}
        missing = sorted(required.difference(data.keys()))
        if missing:
            raise InvalidPolicyError(
                f"missing required policy field(s): {', '.join(missing)}"
            )
        return cls(
            policy_id=str(data.get("policy_id", "ca-m025-production-default")),
            policy_version=str(data.get("policy_version", POLICY_SCHEMA_VERSION)),
            production_tier=str(data.get("production_tier", PRODUCTION_TIER)),
            authorized_roles=frozenset(
                data.get(
                    "authorized_roles",
                    DEFAULT_PRODUCTION_AUTHORIZED_ROLES,
                )
            ),
            budget_limit_units=int(data["budget_limit_units"]),
            max_run_spend_units=(
                None
                if data.get("max_run_spend_units") is None
                else int(data["max_run_spend_units"])
            ),
        )

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "production_tier": self.production_tier,
            "authorized_roles": sorted(self.authorized_roles),
            "budget_limit_units": self.budget_limit_units,
            "max_run_spend_units": self.max_run_spend_units,
        }

    @property
    def policy_sha256(self) -> str:
        return _sha256(self.canonical_dict())


@dataclass(frozen=True, slots=True)
class CampaignExecutionRequest:
    """Authoritative request presented to the production policy evaluator."""

    campaign_id: str
    actor_id: str
    actor_role: str
    authenticated: bool
    campaign_tier: str
    estimated_spend_units: int
    spend_to_date_units: int = 0
    requested_operation: str = "EXECUTE"

    def __post_init__(self) -> None:
        campaign_id = str(self.campaign_id).strip()
        actor_id = str(self.actor_id).strip()
        actor_role = _normalize_role(self.actor_role)
        campaign_tier = _normalize_token(self.campaign_tier)
        requested_operation = str(self.requested_operation).strip().upper() or "EXECUTE"

        if not campaign_id:
            raise InvalidExecutionRequestError("campaign_id must be non-empty")
        if not actor_id:
            raise InvalidExecutionRequestError("actor_id must be non-empty")
        if campaign_tier not in {tier.value for tier in CampaignTier}:
            raise InvalidExecutionRequestError(
                f"campaign_tier must be one of "
                f"{sorted(tier.value for tier in CampaignTier)}, got {campaign_tier!r}"
            )
        if actor_role not in CANONICAL_CAMPAIGN_ROLES:
            raise InvalidExecutionRequestError(
                f"actor_role must be one of {list(CANONICAL_CAMPAIGN_ROLES)}, got {actor_role!r}"
            )
        if not requested_operation:
            raise InvalidExecutionRequestError("requested_operation must be non-empty")

        object.__setattr__(self, "campaign_id", campaign_id)
        object.__setattr__(self, "actor_id", actor_id)
        object.__setattr__(self, "actor_role", actor_role)
        object.__setattr__(self, "campaign_tier", campaign_tier)
        object.__setattr__(self, "requested_operation", requested_operation)
        object.__setattr__(self, "estimated_spend_units", int(self.estimated_spend_units))
        object.__setattr__(self, "spend_to_date_units", int(self.spend_to_date_units))


@dataclass(frozen=True, slots=True)
class CampaignAuthorizationReceipt:
    """Immutable decision evidence returned by the policy evaluator.

    ``receipt_id`` is derived from the canonical receipt body and therefore
    remains deterministic for the same request/policy/timestamp tuple.
    """

    decision: AuthorizationDecision
    reason_code: str
    message: str
    mandate_id: str
    requirement_id: str
    campaign_id: str
    actor_id: str
    actor_role: str
    authenticated: bool
    campaign_tier: str
    requested_operation: str
    estimated_spend_units: int
    spend_to_date_units: int
    budget_limit_units: int
    remaining_budget_units: int
    max_run_spend_units: Optional[int]
    policy_id: str
    policy_version: str
    policy_sha256: str
    non_waivable_controls: Tuple[str, ...]
    created_at_utc: str
    receipt_id: str
    details: Mapping[str, Any] = field(default_factory=dict)

    @property
    def allowed(self) -> bool:
        return self.decision is AuthorizationDecision.ALLOW

    @property
    def denied(self) -> bool:
        return not self.allowed

    @property
    def denial_reason(self) -> Optional[str]:
        return None if self.allowed else self.reason_code

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision.value,
            "reason_code": self.reason_code,
            "message": self.message,
            "mandate_id": self.mandate_id,
            "requirement_id": self.requirement_id,
            "campaign_id": self.campaign_id,
            "actor_id": self.actor_id,
            "actor_role": self.actor_role,
            "authenticated": self.authenticated,
            "campaign_tier": self.campaign_tier,
            "requested_operation": self.requested_operation,
            "estimated_spend_units": self.estimated_spend_units,
            "spend_to_date_units": self.spend_to_date_units,
            "budget_limit_units": self.budget_limit_units,
            "remaining_budget_units": self.remaining_budget_units,
            "max_run_spend_units": self.max_run_spend_units,
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "policy_sha256": self.policy_sha256,
            "non_waivable_controls": list(self.non_waivable_controls),
            "created_at_utc": self.created_at_utc,
            "receipt_id": self.receipt_id,
            "details": dict(self.details),
        }

    def to_dict(self) -> dict[str, Any]:
        return self.canonical_dict()


class CampaignAuthorizationPolicyEngine:
    """Canonical, stateless production policy evaluator."""

    NON_WAIVABLE_CONTROLS: Tuple[str, ...] = (
        "AUTHENTICATED_ACTOR",
        "AUTHORIZED_ROLE",
        "PRODUCTION_TIER",
        "SPEND_WITHIN_BUDGET",
    )

    def __init__(self, policy: CampaignAuthorizationPolicy):
        self._policy = policy

    @property
    def policy(self) -> CampaignAuthorizationPolicy:
        return self._policy

    def evaluate(
        self,
        request: CampaignExecutionRequest | Mapping[str, Any],
        *,
        now_utc: Optional[str] = None,
    ) -> CampaignAuthorizationReceipt:
        """Evaluate a request and return a descriptive allow/deny receipt.

        ``Mapping`` input is normalized through the same typed request boundary,
        so callers cannot bypass validation by avoiding the dataclass.
        """
        try:
            normalized_request = (
                request
                if isinstance(request, CampaignExecutionRequest)
                else CampaignExecutionRequest(**dict(request))
            )
        except (TypeError, ValueError) as exc:
            return self._invalid_request_receipt(
                request,
                str(exc),
                now_utc=now_utc,
            )

        return self._evaluate_valid_request(normalized_request, now_utc=now_utc)

    def authorize(
        self,
        request: CampaignExecutionRequest | Mapping[str, Any],
        *,
        now_utc: Optional[str] = None,
    ) -> CampaignAuthorizationReceipt:
        """Alias for ``evaluate`` at the canonical runtime boundary."""
        return self.evaluate(request, now_utc=now_utc)

    def _evaluate_valid_request(
        self,
        request: CampaignExecutionRequest,
        *,
        now_utc: Optional[str],
    ) -> CampaignAuthorizationReceipt:
        timestamp = _normalize_timestamp(now_utc)

        if not request.authenticated:
            return self._receipt(
                decision=AuthorizationDecision.DENY,
                reason_code=DenialReasonCode.UNAUTHENTICATED_EXECUTION.value,
                message=(
                    f"Production execution denied for campaign {request.campaign_id!r}: "
                    f"actor {request.actor_id!r} is not authenticated."
                ),
                request=request,
                timestamp=timestamp,
                details={
                    "requirement": REQUIREMENT_ID,
                    "control": "AUTHENTICATED_ACTOR",
                },
            )

        if request.campaign_tier != self._policy.production_tier:
            return self._receipt(
                decision=AuthorizationDecision.DENY,
                reason_code=DenialReasonCode.TIER_NOT_ALLOWED.value,
                message=(
                    f"Production execution denied for campaign {request.campaign_id!r}: "
                    f"campaign tier {request.campaign_tier!r} is not the required "
                    f"{self._policy.production_tier!r} tier."
                ),
                request=request,
                timestamp=timestamp,
                details={
                    "required_tier": self._policy.production_tier,
                    "actual_tier": request.campaign_tier,
                    "control": "PRODUCTION_TIER",
                },
            )

        if request.actor_role not in self._policy.authorized_roles:
            return self._receipt(
                decision=AuthorizationDecision.DENY,
                reason_code=DenialReasonCode.ROLE_NOT_AUTHORIZED.value,
                message=(
                    f"Production execution denied for campaign {request.campaign_id!r}: "
                    f"role {request.actor_role!r} is not authorized by policy "
                    f"{self._policy.policy_id!r}."
                ),
                request=request,
                timestamp=timestamp,
                details={
                    "authorized_roles": sorted(self._policy.authorized_roles),
                    "actual_role": request.actor_role,
                    "control": "AUTHORIZED_ROLE",
                },
            )

        if request.estimated_spend_units < 0 or request.spend_to_date_units < 0:
            return self._receipt(
                decision=AuthorizationDecision.DENY,
                reason_code=DenialReasonCode.INVALID_SPEND_AMOUNT.value,
                message=(
                    f"Production execution denied for campaign {request.campaign_id!r}: "
                    "spend amounts cannot be negative."
                ),
                request=request,
                timestamp=timestamp,
                details={
                    "estimated_spend_units": request.estimated_spend_units,
                    "spend_to_date_units": request.spend_to_date_units,
                    "control": "SPEND_WITHIN_BUDGET",
                },
            )

        remaining_budget = self._policy.budget_limit_units - request.spend_to_date_units
        if request.estimated_spend_units > remaining_budget:
            return self._receipt(
                decision=AuthorizationDecision.DENY,
                reason_code=DenialReasonCode.SPEND_BUDGET_EXCEEDED.value,
                message=(
                    f"Production execution denied for campaign {request.campaign_id!r}: "
                    f"estimated spend {request.estimated_spend_units} exceeds the "
                    f"remaining campaign budget {max(remaining_budget, 0)} units."
                ),
                request=request,
                timestamp=timestamp,
                details={
                    "budget_limit_units": self._policy.budget_limit_units,
                    "spend_to_date_units": request.spend_to_date_units,
                    "remaining_budget_units": remaining_budget,
                    "estimated_spend_units": request.estimated_spend_units,
                    "control": "SPEND_WITHIN_BUDGET",
                },
            )

        if (
            self._policy.max_run_spend_units is not None
            and request.estimated_spend_units > self._policy.max_run_spend_units
        ):
            return self._receipt(
                decision=AuthorizationDecision.DENY,
                reason_code=DenialReasonCode.SPEND_BUDGET_EXCEEDED.value,
                message=(
                    f"Production execution denied for campaign {request.campaign_id!r}: "
                    f"estimated spend {request.estimated_spend_units} exceeds the "
                    f"per-run spend threshold {self._policy.max_run_spend_units} units."
                ),
                request=request,
                timestamp=timestamp,
                details={
                    "max_run_spend_units": self._policy.max_run_spend_units,
                    "estimated_spend_units": request.estimated_spend_units,
                    "control": "SPEND_WITHIN_BUDGET",
                },
            )

        return self._receipt(
            decision=AuthorizationDecision.ALLOW,
            reason_code="AUTHORIZED",
            message=(
                f"Production execution authorized for campaign {request.campaign_id!r}: "
                f"authenticated role {request.actor_role!r} satisfies policy and "
                f"estimated spend {request.estimated_spend_units} is within budget."
            ),
            request=request,
            timestamp=timestamp,
            details={
                "remaining_budget_units": remaining_budget,
                "required_tier": self._policy.production_tier,
            },
        )

    def _invalid_request_receipt(
        self,
        raw_request: CampaignExecutionRequest | Mapping[str, Any],
        error: str,
        *,
        now_utc: Optional[str],
    ) -> CampaignAuthorizationReceipt:
        timestamp = _normalize_timestamp(now_utc)
        raw = dict(raw_request) if isinstance(raw_request, Mapping) else {}

        campaign_id = str(raw.get("campaign_id", "")).strip() or "UNKNOWN"
        actor_id = str(raw.get("actor_id", "")).strip() or "UNKNOWN"
        actor_role = _safe_normalize_role(raw.get("actor_role")) or "UNKNOWN"
        authenticated = bool(raw.get("authenticated", False))
        campaign_tier = _safe_normalize_token(raw.get("campaign_tier")) or "UNKNOWN"
        requested_operation = (
            str(raw.get("requested_operation", "EXECUTE")).strip().upper() or "EXECUTE"
        )
        estimated_spend = _safe_int(raw.get("estimated_spend_units"))
        spend_to_date = _safe_int(raw.get("spend_to_date_units"))

        synthetic_request = CampaignExecutionRequest(
            campaign_id=campaign_id,
            actor_id=actor_id,
            actor_role=actor_role if actor_role in CANONICAL_CAMPAIGN_ROLES else "HUNTER",
            authenticated=authenticated,
            campaign_tier=(
                campaign_tier
                if campaign_tier in {tier.value for tier in CampaignTier}
                else CampaignTier.DEVELOPMENT.value
            ),
            estimated_spend_units=estimated_spend,
            spend_to_date_units=spend_to_date,
            requested_operation=requested_operation,
        )

        return self._receipt(
            decision=AuthorizationDecision.DENY,
            reason_code=DenialReasonCode.INVALID_REQUEST.value,
            message=(
                f"Production execution denied for campaign {campaign_id!r}: "
                f"request validation failed: {error}"
            ),
            request=synthetic_request,
            timestamp=timestamp,
            details={
                "error": error,
                "control": "REQUEST_VALIDATION",
            },
        )

    def _receipt(
        self,
        *,
        decision: AuthorizationDecision,
        reason_code: str,
        message: str,
        request: CampaignExecutionRequest,
        timestamp: str,
        details: Mapping[str, Any],
    ) -> CampaignAuthorizationReceipt:
        remaining_budget = self._policy.budget_limit_units - request.spend_to_date_units
        body = {
            "decision": decision.value,
            "reason_code": reason_code,
            "message": message,
            "mandate_id": MANDATE_ID,
            "requirement_id": REQUIREMENT_ID,
            "campaign_id": request.campaign_id,
            "actor_id": request.actor_id,
            "actor_role": request.actor_role,
            "authenticated": request.authenticated,
            "campaign_tier": request.campaign_tier,
            "requested_operation": request.requested_operation,
            "estimated_spend_units": request.estimated_spend_units,
            "spend_to_date_units": request.spend_to_date_units,
            "budget_limit_units": self._policy.budget_limit_units,
            "remaining_budget_units": remaining_budget,
            "max_run_spend_units": self._policy.max_run_spend_units,
            "policy_id": self._policy.policy_id,
            "policy_version": self._policy.policy_version,
            "policy_sha256": self._policy.policy_sha256,
            "non_waivable_controls": list(self.NON_WAIVABLE_CONTROLS),
            "created_at_utc": timestamp,
            "details": dict(details),
        }
        receipt_id = _sha256(body)
        return CampaignAuthorizationReceipt(
            decision=decision,
            reason_code=reason_code,
            message=message,
            mandate_id=MANDATE_ID,
            requirement_id=REQUIREMENT_ID,
            campaign_id=request.campaign_id,
            actor_id=request.actor_id,
            actor_role=request.actor_role,
            authenticated=request.authenticated,
            campaign_tier=request.campaign_tier,
            requested_operation=request.requested_operation,
            estimated_spend_units=request.estimated_spend_units,
            spend_to_date_units=request.spend_to_date_units,
            budget_limit_units=self._policy.budget_limit_units,
            remaining_budget_units=remaining_budget,
            max_run_spend_units=self._policy.max_run_spend_units,
            policy_id=self._policy.policy_id,
            policy_version=self._policy.policy_version,
            policy_sha256=self._policy.policy_sha256,
            non_waivable_controls=self.NON_WAIVABLE_CONTROLS,
            created_at_utc=timestamp,
            receipt_id=receipt_id,
            details=dict(details),
        )


def authorize_campaign_execution(
    request: CampaignExecutionRequest | Mapping[str, Any],
    policy: CampaignAuthorizationPolicy,
    *,
    now_utc: Optional[str] = None,
) -> CampaignAuthorizationReceipt:
    """Canonical functional entrypoint for production execution authorization."""
    return CampaignAuthorizationPolicyEngine(policy).evaluate(
        request,
        now_utc=now_utc,
    )


# Descriptive aliases for callers that use shorter names.
CampaignAuthPolicy = CampaignAuthorizationPolicy
CampaignAuthPolicyEngine = CampaignAuthorizationPolicyEngine
ExecutionRequest = CampaignExecutionRequest
AuthorizationReceipt = CampaignAuthorizationReceipt
authorize = authorize_campaign_execution


def _normalize_role(value: Any) -> str:
    return str(value).strip().upper()


def _safe_normalize_role(value: Any) -> Optional[str]:
    try:
        normalized = _normalize_role(value)
    except Exception:
        return None
    return normalized or None


def _normalize_token(value: Any) -> str:
    return str(value).strip().upper()


def _safe_normalize_token(value: Any) -> Optional[str]:
    try:
        normalized = _normalize_token(value)
    except Exception:
        return None
    return normalized or None


def _safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _normalize_timestamp(value: Optional[str]) -> str:
    if value is not None:
        parsed = str(value).strip()
        if not parsed:
            raise InvalidExecutionRequestError("now_utc must be non-empty when provided")
        return parsed
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha256(value: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
