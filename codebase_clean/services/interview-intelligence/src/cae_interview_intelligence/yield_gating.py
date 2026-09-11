"""
Deterministic portfolio yield gating for CAE Mandate CA-M023.

The gate is intentionally contract-driven: the frozen Content Portfolio Contract is
the source of thresholds. This module does not invent or persist portfolio policy.
It evaluates acquired narrative yield and diversity against the supplied frozen
contract, emits a deterministic structured receipt, and only invokes downstream
media assembly on a passing receipt.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence

MANDATE_ID = "CA-M023"
INVARIANT_ID = "FR-023"
POLICY_VERSION = "CA-M023-PORTFOLIO-YIELD-V1"

_REQUIRED_DIVERSITY_DIMENSIONS = (
    "unique_audience_islands",
    "unique_tensions",
    "unique_guest_territories",
    "unique_archetypes",
)


class YieldGateConfigurationError(ValueError):
    """Raised when the frozen portfolio contract is missing or invalid."""


class YieldGateBlockedError(RuntimeError):
    """Raised when insufficient yield blocks downstream media assembly."""

    def __init__(self, report: "YieldGapReport") -> None:
        self.report = report
        super().__init__(
            f"{INVARIANT_ID} blocked downstream media assembly: "
            + "; ".join(g["code"] for g in report.gaps)
        )


@dataclass(frozen=True)
class FrozenContentPortfolioContract:
    """
    Explicit, frozen portfolio requirements consumed by the gate.

    The gate never assigns defaults to these thresholds: they must come from the
    already-frozen Content Portfolio Contract at the authoritative call site.
    ``contract_sha256`` binds the evaluation receipt to the exact contract inputs.
    """

    contract_id: str
    contract_version: str
    min_viable_candidates: int
    min_evidence_backed_ratio: float
    min_unique_audience_islands: int
    min_unique_tensions: int
    min_unique_guest_territories: int
    min_unique_archetypes: int
    contract_sha256: str

    def __post_init__(self) -> None:
        if not self.contract_id.strip():
            raise YieldGateConfigurationError("contract_id is required")
        if not self.contract_version.strip():
            raise YieldGateConfigurationError("contract_version is required")
        if self.min_viable_candidates < 1:
            raise YieldGateConfigurationError("min_viable_candidates must be >= 1")
        if not 0.0 <= self.min_evidence_backed_ratio <= 1.0:
            raise YieldGateConfigurationError(
                "min_evidence_backed_ratio must be between 0 and 1"
            )
        for name in _REQUIRED_DIVERSITY_DIMENSIONS:
            if getattr(self, _contract_field(name)) < 1:
                raise YieldGateConfigurationError(f"{name} must be >= 1")
        if len(self.contract_sha256) != 64 or any(
            c not in "0123456789abcdef" for c in self.contract_sha256.lower()
        ):
            raise YieldGateConfigurationError(
                "contract_sha256 must be a 64-character hexadecimal digest"
            )
        if self.contract_sha256 != _sha256(self.canonical_payload()):
            raise YieldGateConfigurationError(
                "contract_sha256 does not match the frozen contract payload"
            )

    def canonical_payload(self) -> dict[str, Any]:
        """Return the policy payload without the self-referential hash."""
        return {
            "contract_id": self.contract_id,
            "contract_version": self.contract_version,
            "min_viable_candidates": self.min_viable_candidates,
            "min_evidence_backed_ratio": self.min_evidence_backed_ratio,
            "min_unique_audience_islands": self.min_unique_audience_islands,
            "min_unique_tensions": self.min_unique_tensions,
            "min_unique_guest_territories": self.min_unique_guest_territories,
            "min_unique_archetypes": self.min_unique_archetypes,
        }

    @classmethod
    def from_payload(
        cls,
        *,
        contract_id: str,
        contract_version: str,
        min_viable_candidates: int,
        min_evidence_backed_ratio: float,
        min_unique_audience_islands: int,
        min_unique_tensions: int,
        min_unique_guest_territories: int,
        min_unique_archetypes: int,
    ) -> "FrozenContentPortfolioContract":
        payload = {
            "contract_id": contract_id,
            "contract_version": contract_version,
            "min_viable_candidates": min_viable_candidates,
            "min_evidence_backed_ratio": min_evidence_backed_ratio,
            "min_unique_audience_islands": min_unique_audience_islands,
            "min_unique_tensions": min_unique_tensions,
            "min_unique_guest_territories": min_unique_guest_territories,
            "min_unique_archetypes": min_unique_archetypes,
        }
        digest = _sha256(payload)
        return cls(**payload, contract_sha256=digest)


@dataclass(frozen=True)
class NarrativeYieldMetrics:
    """
    Acquired-evidence yield observed immediately before downstream assembly.

    ``viable_candidates`` are narrative candidates that survived upstream evidence
    and compatibility validation. ``evidence_backed_candidates`` is the subset with
    retained evidence lineage. Diversity counts are the same categories surfaced by
    the existing portfolio selector.
    """

    viable_candidates: int
    evidence_backed_candidates: int
    unique_audience_islands: int
    unique_tensions: int
    unique_guest_territories: int
    unique_archetypes: int

    @property
    def evidence_backed_ratio(self) -> float:
        if self.viable_candidates <= 0:
            return 0.0
        return self.evidence_backed_candidates / self.viable_candidates

    def __post_init__(self) -> None:
        for field_name in (
            "viable_candidates",
            "evidence_backed_candidates",
            *_REQUIRED_DIVERSITY_DIMENSIONS,
        ):
            value = getattr(self, field_name)
            if value < 0:
                raise ValueError(f"{field_name} must be >= 0")
        if self.evidence_backed_candidates > self.viable_candidates:
            raise ValueError(
                "evidence_backed_candidates cannot exceed viable_candidates"
            )


@dataclass(frozen=True)
class YieldGapReport:
    """Structured fail-closed diagnostics for a portfolio yield evaluation."""

    gate: str
    mandate_id: str
    invariant_id: str
    policy_version: str
    contract_id: str
    contract_version: str
    contract_sha256: str
    passed: bool
    gaps: tuple[dict[str, Any], ...]
    metrics: dict[str, Any]
    receipt_sha256: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate": self.gate,
            "mandate_id": self.mandate_id,
            "invariant_id": self.invariant_id,
            "policy_version": self.policy_version,
            "contract_id": self.contract_id,
            "contract_version": self.contract_version,
            "contract_sha256": self.contract_sha256,
            "passed": self.passed,
            "gaps": [dict(g) for g in self.gaps],
            "metrics": dict(self.metrics),
            "receipt_sha256": self.receipt_sha256,
        }


@dataclass(frozen=True)
class YieldGateDecision:
    """Auditable gate result returned to callers."""

    allowed: bool
    report: YieldGapReport

    def require_allowed(self) -> None:
        if not self.allowed:
            raise YieldGateBlockedError(self.report)


def _contract_field(dimension_name: str) -> str:
    return dimension_name if dimension_name.startswith("min_") else f"min_{dimension_name}"


def _sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _gap(
    *,
    code: str,
    metric: str,
    observed: int | float,
    required: int | float,
) -> dict[str, Any]:
    deficit: int | float
    if isinstance(observed, float) or isinstance(required, float):
        deficit = round(max(0.0, float(required) - float(observed)), 12)
    else:
        deficit = max(0, int(required) - int(observed))
    return {
        "code": code,
        "metric": metric,
        "observed": observed,
        "required": required,
        "deficit": deficit,
    }


def evaluate_yield(
    metrics: NarrativeYieldMetrics,
    contract: FrozenContentPortfolioContract,
) -> YieldGateDecision:
    """
    Deterministically compare observed yield against the frozen portfolio contract.

    The overall decision is the conjunction of all required gates. No aggregate
    score, average, ranking score, or single "yield percentage" can compensate
    for a failed diversity or evidence-backed threshold.
    """
    gaps: list[dict[str, Any]] = []
    if metrics.viable_candidates < contract.min_viable_candidates:
        gaps.append(
            _gap(
                code="YIELD_MIN_VIABLE_CANDIDATES",
                metric="viable_candidates",
                observed=metrics.viable_candidates,
                required=contract.min_viable_candidates,
            )
        )

    ratio = metrics.evidence_backed_ratio
    if ratio < contract.min_evidence_backed_ratio:
        gaps.append(
            _gap(
                code="YIELD_EVIDENCE_BACKED_RATIO",
                metric="evidence_backed_ratio",
                observed=ratio,
                required=contract.min_evidence_backed_ratio,
            )
        )

    diversity_specs = (
        (
            "unique_audience_islands",
            contract.min_unique_audience_islands,
            "YIELD_DIVERSITY_AUDIENCE_ISLANDS",
        ),
        (
            "unique_tensions",
            contract.min_unique_tensions,
            "YIELD_DIVERSITY_TENSIONS",
        ),
        (
            "unique_guest_territories",
            contract.min_unique_guest_territories,
            "YIELD_DIVERSITY_GUEST_TERRITORIES",
        ),
        (
            "unique_archetypes",
            contract.min_unique_archetypes,
            "YIELD_DIVERSITY_ARCHETYPES",
        ),
    )
    for metric_name, required, code in diversity_specs:
        observed = getattr(metrics, metric_name)
        if observed < required:
            gaps.append(
                _gap(
                    code=code,
                    metric=metric_name,
                    observed=observed,
                    required=required,
                )
            )

    metrics_payload = {
        "viable_candidates": metrics.viable_candidates,
        "evidence_backed_candidates": metrics.evidence_backed_candidates,
        "evidence_backed_ratio": ratio,
        "unique_audience_islands": metrics.unique_audience_islands,
        "unique_tensions": metrics.unique_tensions,
        "unique_guest_territories": metrics.unique_guest_territories,
        "unique_archetypes": metrics.unique_archetypes,
    }
    base_payload = {
        "gate": "downstream_media_assembly",
        "mandate_id": MANDATE_ID,
        "invariant_id": INVARIANT_ID,
        "policy_version": POLICY_VERSION,
        "contract_id": contract.contract_id,
        "contract_version": contract.contract_version,
        "contract_sha256": contract.contract_sha256,
        "passed": not gaps,
        "gaps": tuple(gaps),
        "metrics": metrics_payload,
    }
    receipt_hash = _sha256(base_payload)
    report = YieldGapReport(
        **base_payload,
        receipt_sha256=receipt_hash,
    )
    return YieldGateDecision(allowed=report.passed, report=report)


def gate_downstream_media_assembly(
    metrics: NarrativeYieldMetrics,
    contract: FrozenContentPortfolioContract,
    assemble: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> Any:
    """
    Fail-closed boundary around a costly downstream media assembly program.

    ``assemble`` is never touched when the deterministic contract check fails.
    The callback may be sync or async; the gate performs no work before it has
    accepted the portfolio.
    """
    decision = evaluate_yield(metrics, contract)
    decision.require_allowed()
    return assemble(*args, **kwargs)


def metrics_from_candidates(
    candidates: Sequence[Any],
    *,
    evidence_backed_predicate: Callable[[Any], bool],
) -> NarrativeYieldMetrics:
    """
    Derive gate metrics from candidate objects without scoring them.

    Candidates must expose ``get_diversity_signature()``. Evidence-backed status is
    deliberately delegated to an explicit predicate because upstream hypothesis
    lineage is not itself proof that acquired narrative evidence was retained.
    """
    viable = list(candidates)
    evidence_backed = sum(1 for candidate in viable if evidence_backed_predicate(candidate))

    signatures = [candidate.get_diversity_signature() for candidate in viable]
    return NarrativeYieldMetrics(
        viable_candidates=len(viable),
        evidence_backed_candidates=evidence_backed,
        unique_audience_islands=len(
            {signature["audience_island"] for signature in signatures}
        ),
        unique_tensions=len({signature["tension"] for signature in signatures}),
        unique_guest_territories=len(
            {signature["guest_territory"] for signature in signatures}
        ),
        unique_archetypes=len({signature["archetype"] for signature in signatures}),
    )
