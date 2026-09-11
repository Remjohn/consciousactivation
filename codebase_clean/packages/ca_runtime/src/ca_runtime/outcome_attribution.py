"""Release-scoped outcome telemetry attribution for CA-M032b / FR-OUT-001.

The module owns the narrow boundary between post-distribution observations and
release/campaign lineage. It intentionally distinguishes an *attributed
observation* from a causal claim: exact release/lineage linkage is verified and
measured, while statistical correlation is reported as correlation, never as
causal proof.

No campaign-name or "latest release" lookup is performed. Every accepted event
must carry an explicit release identity and an exact, distributed receipt whose
release manifest digest matches. Tension collision anchors and creative
components are also explicit references and must exist in the sealed release's
lineage. Historical records are append-only, duplicate event IDs are idempotent
when their content is identical, and conflicting re-use is rejected.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import math
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Callable, Iterable, Mapping, Protocol, Sequence
from uuid import uuid4

try:
    from ca_contracts import canonical_json_bytes, canonical_sha256
except Exception:  # pragma: no cover - fallback for isolated source loading
    def canonical_json_bytes(value: Any) -> bytes:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

    def canonical_sha256(value: Any) -> str:
        return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


SCHEMA_VERSION = "ca-outcome-attribution/v1"
SHA256_HEX_LENGTH = 64
DELIVERED_STATUS = "DELIVERED"


def _digest_payload(value: Any) -> Any:
    """Convert measurement floats to deterministic decimal strings before canonical hashing."""
    if isinstance(value, Mapping):
        return {str(key): _digest_payload(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_digest_payload(item) for item in value]
    if isinstance(value, float):
        return format(value, ".12g")
    return value


def _payload_digest(value: Any) -> str:
    return canonical_sha256(_digest_payload(value))



class OutcomeAttributionError(RuntimeError):
    """Base class for fail-closed outcome attribution errors."""


class OutcomeValidationError(OutcomeAttributionError, ValueError):
    """Raised for malformed or semantically incomplete telemetry."""


class OutcomeIntegrityError(OutcomeAttributionError):
    """Raised when an outcome cannot be proven to refer to the released artifact."""


class OutcomeAttributionConflictError(OutcomeAttributionError):
    """Raised when an event identity is reused for different telemetry."""


class UnknownReleaseError(OutcomeIntegrityError):
    """Raised when an event points to a release absent from the supplied manifest."""


class UnresolvedAttributionError(OutcomeIntegrityError):
    """Raised when causal references cannot be traced to release lineage."""


class DistributionReceiptProtocol(Protocol):
    """Minimum repository-native contract exposed by CA-M031 delivery receipts."""

    release_id: str
    release_manifest_sha256: str
    delivery_status: Any
    receipt_id: str

    def to_dict(self) -> Mapping[str, Any]: ...

    def verify(self, signing_secret: bytes | str) -> None: ...



def _require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise OutcomeValidationError(f"{field} must be a non-empty string")
    return value.strip()



def _require_sha256(value: Any, field: str) -> str:
    value = _require_text(value, field).lower()
    if len(value) != SHA256_HEX_LENGTH or any(ch not in "0123456789abcdef" for ch in value):
        raise OutcomeValidationError(f"{field} must be a lowercase SHA-256 hex digest")
    return value



def _require_nonnegative_finite(value: Any, field: str) -> float:
    if isinstance(value, bool):
        raise OutcomeValidationError(f"{field} must be a finite non-negative number")
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise OutcomeValidationError(f"{field} must be a finite non-negative number") from exc
    if not math.isfinite(numeric) or numeric < 0.0:
        raise OutcomeValidationError(f"{field} must be a finite non-negative number")
    return numeric



def _normalize_refs(refs: Sequence[Mapping[str, Any]], field: str) -> tuple["CausalReference", ...]:
    if not isinstance(refs, Sequence) or isinstance(refs, (str, bytes, bytearray)):
        raise OutcomeValidationError(f"{field} must be a sequence")
    normalized = tuple(CausalReference.from_mapping(item, field=f"{field}[{index}]") for index, item in enumerate(refs))
    if not normalized:
        raise OutcomeValidationError(f"{field} must contain at least one reference")
    ids = [(item.object_id, item.revision, item.sha256) for item in normalized]
    if len(ids) != len(set(ids)):
        raise OutcomeValidationError(f"{field} contains duplicate references")
    return tuple(sorted(normalized, key=lambda item: (item.object_id, item.revision, item.sha256)))



def _mapping(value: Any, field: str) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    if hasattr(value, "to_dict"):
        mapped = value.to_dict()
        if isinstance(mapped, Mapping):
            return mapped
    raise OutcomeValidationError(f"{field} must be a mapping or expose to_dict()")



def _manifest_identity(manifest: Any) -> tuple[str, str, Mapping[str, Any]]:
    payload = _mapping(manifest, "release_manifest")
    release_id = _require_text(payload.get("release_id"), "release_manifest.release_id")
    manifest_sha = _require_sha256(payload.get("manifest_sha256"), "release_manifest.manifest_sha256")
    return release_id, manifest_sha, payload



def _receipt_payload(receipt: Any) -> Mapping[str, Any]:
    payload = _mapping(receipt, "distribution_receipt")
    if payload.get("receipt_id") is None:
        raise OutcomeValidationError("distribution_receipt.receipt_id is required")
    return payload



def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True, slots=True)
class CausalReference:
    """Revision-specific reference to a released upstream object."""

    object_id: str
    revision: str
    sha256: str

    def __post_init__(self) -> None:
        _require_text(self.object_id, "object_id")
        _require_text(self.revision, "revision")
        _require_sha256(self.sha256, "sha256")

    def to_dict(self) -> dict[str, str]:
        return {
            "object_id": self.object_id,
            "revision": self.revision,
            "sha256": self.sha256,
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any], *, field: str) -> "CausalReference":
        if not isinstance(value, Mapping):
            raise OutcomeValidationError(f"{field} must be a mapping")
        try:
            return cls(
                object_id=_require_text(value.get("object_id"), f"{field}.object_id"),
                revision=_require_text(value.get("revision"), f"{field}.revision"),
                sha256=_require_sha256(value.get("sha256"), f"{field}.sha256"),
            )
        except OutcomeValidationError:
            raise
        except Exception as exc:  # pragma: no cover
            raise OutcomeValidationError(f"invalid {field}") from exc


@dataclass(frozen=True, slots=True)
class OutcomeMetrics:
    """Normalized post-distribution performance and conversion observations.

    All supplied values are normalized to [0, 1]. A metric's provenance remains
    the raw telemetry event; this class only validates and aggregates it.
    """

    performance: Mapping[str, float]
    conversions: Mapping[str, float]

    def __post_init__(self) -> None:
        if not isinstance(self.performance, Mapping) or not self.performance:
            raise OutcomeValidationError("performance metrics must be a non-empty mapping")
        if not isinstance(self.conversions, Mapping) or not self.conversions:
            raise OutcomeValidationError("conversion metrics must be a non-empty mapping")
        for group_name, group in (("performance", self.performance), ("conversions", self.conversions)):
            for key, value in group.items():
                _require_text(key, f"{group_name} metric name")
                numeric = _require_nonnegative_finite(value, f"{group_name}.{key}")
                if numeric > 1.0:
                    raise OutcomeValidationError(
                        f"{group_name}.{key} must be normalized to [0, 1]; got {numeric}"
                    )
        object.__setattr__(self, "performance", dict(self.performance))
        object.__setattr__(self, "conversions", dict(self.conversions))

    @property
    def performance_yield(self) -> float:
        return mean(float(v) for v in self.performance.values())

    @property
    def conversion_yield(self) -> float:
        return mean(float(v) for v in self.conversions.values())

    def outcome_yield(self, *, performance_weight: float = 0.5, conversion_weight: float = 0.5) -> float:
        performance_weight = _require_nonnegative_finite(performance_weight, "performance_weight")
        conversion_weight = _require_nonnegative_finite(conversion_weight, "conversion_weight")
        total = performance_weight + conversion_weight
        if total <= 0.0:
            raise OutcomeValidationError("performance and conversion weights must have positive total")
        return (
            self.performance_yield * performance_weight
            + self.conversion_yield * conversion_weight
        ) / total

    def to_dict(self) -> dict[str, Any]:
        return {
            "performance": dict(self.performance),
            "conversions": dict(self.conversions),
        }


@dataclass(frozen=True, slots=True)
class OutcomeEvent:
    """Immutable raw observation admitted from the post-distribution boundary."""

    event_id: str
    release_id: str
    release_manifest_sha256: str
    distribution_receipt_id: str
    campaign_id: str | None
    tension_collision_anchor_refs: tuple[CausalReference, ...]
    creative_component_refs: tuple[CausalReference, ...]
    audience_hypothesis_refs: tuple[CausalReference, ...]
    metrics: OutcomeMetrics
    observed_at: str
    source: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.event_id, "event_id")
        _require_text(self.release_id, "release_id")
        _require_sha256(self.release_manifest_sha256, "release_manifest_sha256")
        _require_text(self.distribution_receipt_id, "distribution_receipt_id")
        if self.campaign_id is not None:
            _require_text(self.campaign_id, "campaign_id")
        if not self.tension_collision_anchor_refs:
            raise OutcomeValidationError("at least one tension collision anchor reference is required")
        if not self.creative_component_refs:
            raise OutcomeValidationError("at least one creative component reference is required")
        if not isinstance(self.metrics, OutcomeMetrics):
            raise OutcomeValidationError("metrics must be an OutcomeMetrics instance")
        _require_text(self.observed_at, "observed_at")
        _require_text(self.source, "source")
        if not isinstance(self.metadata, Mapping):
            raise OutcomeValidationError("metadata must be a mapping")
        object.__setattr__(self, "tension_collision_anchor_refs", tuple(self.tension_collision_anchor_refs))
        object.__setattr__(self, "creative_component_refs", tuple(self.creative_component_refs))
        object.__setattr__(self, "audience_hypothesis_refs", tuple(self.audience_hypothesis_refs))
        object.__setattr__(self, "metadata", dict(self.metadata))

    @property
    def payload(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "event_id": self.event_id,
            "release_id": self.release_id,
            "release_manifest_sha256": self.release_manifest_sha256,
            "distribution_receipt_id": self.distribution_receipt_id,
            "campaign_id": self.campaign_id,
            "tension_collision_anchor_refs": [ref.to_dict() for ref in self.tension_collision_anchor_refs],
            "creative_component_refs": [ref.to_dict() for ref in self.creative_component_refs],
            "audience_hypothesis_refs": [ref.to_dict() for ref in self.audience_hypothesis_refs],
            "metrics": self.metrics.to_dict(),
            "observed_at": self.observed_at,
            "source": self.source,
            "metadata": dict(self.metadata),
        }

    @property
    def event_sha256(self) -> str:
        return _payload_digest(self.payload)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "OutcomeEvent":
        if not isinstance(value, Mapping):
            raise OutcomeValidationError("outcome event must be a mapping")
        metrics_value = value.get("metrics")
        if not isinstance(metrics_value, Mapping):
            raise OutcomeValidationError("outcome event.metrics must be a mapping")
        return cls(
            event_id=_require_text(value.get("event_id"), "event_id"),
            release_id=_require_text(value.get("release_id"), "release_id"),
            release_manifest_sha256=_require_sha256(value.get("release_manifest_sha256"), "release_manifest_sha256"),
            distribution_receipt_id=_require_text(value.get("distribution_receipt_id"), "distribution_receipt_id"),
            campaign_id=(None if value.get("campaign_id") is None else _require_text(value.get("campaign_id"), "campaign_id")),
            tension_collision_anchor_refs=_normalize_refs(
                value.get("tension_collision_anchor_refs", []), "tension_collision_anchor_refs"
            ),
            creative_component_refs=_normalize_refs(
                value.get("creative_component_refs", []), "creative_component_refs"
            ),
            audience_hypothesis_refs=_normalize_refs(
                value.get("audience_hypothesis_refs", []), "audience_hypothesis_refs"
            ) if value.get("audience_hypothesis_refs") else (),
            metrics=OutcomeMetrics(
                performance=metrics_value.get("performance", {}),
                conversions=metrics_value.get("conversions", {}),
            ),
            observed_at=_require_text(value.get("observed_at"), "observed_at"),
            source=_require_text(value.get("source"), "source"),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True, slots=True)
class AttributedOutcome:
    """Verified observation linked to exact release and upstream causal references."""

    outcome_id: str
    event_id: str
    event_sha256: str
    release_id: str
    release_manifest_sha256: str
    distribution_receipt_id: str
    distribution_receipt_sha256: str
    campaign_id: str | None
    tension_collision_anchor_refs: tuple[CausalReference, ...]
    creative_component_refs: tuple[CausalReference, ...]
    audience_hypothesis_refs: tuple[CausalReference, ...]
    performance_yield: float
    conversion_yield: float
    outcome_yield: float
    observed_at: str
    source: str
    causal_interpretation_allowed: bool = False
    created_at: str = field(default_factory=_utc_now)
    record_sha256: str = ""

    def unsigned_payload(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "outcome_id": self.outcome_id,
            "event_id": self.event_id,
            "event_sha256": self.event_sha256,
            "release_id": self.release_id,
            "release_manifest_sha256": self.release_manifest_sha256,
            "distribution_receipt_id": self.distribution_receipt_id,
            "distribution_receipt_sha256": self.distribution_receipt_sha256,
            "campaign_id": self.campaign_id,
            "tension_collision_anchor_refs": [ref.to_dict() for ref in self.tension_collision_anchor_refs],
            "creative_component_refs": [ref.to_dict() for ref in self.creative_component_refs],
            "audience_hypothesis_refs": [ref.to_dict() for ref in self.audience_hypothesis_refs],
            "performance_yield": self.performance_yield,
            "conversion_yield": self.conversion_yield,
            "outcome_yield": self.outcome_yield,
            "observed_at": self.observed_at,
            "source": self.source,
            "causal_interpretation_allowed": self.causal_interpretation_allowed,
            "created_at": self.created_at,
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self.unsigned_payload(), "record_sha256": self.record_sha256}

    def verify(self) -> None:
        expected = _payload_digest(self.unsigned_payload())
        if not hmac.compare_digest(expected, self.record_sha256):
            raise OutcomeIntegrityError("attributed outcome record digest mismatch")
        if self.causal_interpretation_allowed:
            raise OutcomeIntegrityError("raw outcome attribution cannot authorize a causal interpretation")


@dataclass(frozen=True, slots=True)
class AttributionAggregate:
    """Aggregate yield for one explicit causal reference across attributed observations."""

    reference: CausalReference
    observation_count: int
    attributed_weight: float
    weighted_outcome_yield: float
    mean_outcome_yield: float
    yield_per_observation: float
    correlation_with_outcome_yield: float | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "reference": self.reference.to_dict(),
            "observation_count": self.observation_count,
            "attributed_weight": self.attributed_weight,
            "weighted_outcome_yield": self.weighted_outcome_yield,
            "mean_outcome_yield": self.mean_outcome_yield,
            "yield_per_observation": self.yield_per_observation,
            "correlation_with_outcome_yield": self.correlation_with_outcome_yield,
        }



def _pearson(xs: Sequence[float], ys: Sequence[float]) -> float | None:
    if len(xs) != len(ys) or len(xs) < 2:
        return None
    x_bar = mean(xs)
    y_bar = mean(ys)
    numerator = sum((x - x_bar) * (y - y_bar) for x, y in zip(xs, ys))
    denom_x = math.sqrt(sum((x - x_bar) ** 2 for x in xs))
    denom_y = math.sqrt(sum((y - y_bar) ** 2 for y in ys))
    if denom_x == 0.0 or denom_y == 0.0:
        return None
    return numerator / (denom_x * denom_y)



def _walk_lineage(node: Any) -> Iterable[Mapping[str, Any]]:
    if not isinstance(node, Mapping):
        return
    yield node
    children = node.get("children", [])
    if isinstance(children, Sequence) and not isinstance(children, (str, bytes, bytearray)):
        for child in children:
            yield from _walk_lineage(child)



def _manifest_lineage_keys(manifest_payload: Mapping[str, Any]) -> set[tuple[str, str, str]]:
    keys: set[tuple[str, str, str]] = set()
    for ref_field in ("source_refs", "semantic_refs", "authorization_refs"):
        refs = manifest_payload.get(ref_field, [])
        if isinstance(refs, Sequence) and not isinstance(refs, (str, bytes, bytearray)):
            for ref in refs:
                if isinstance(ref, Mapping) and ref.get("object_id") and ref.get("revision") and ref.get("sha256"):
                    keys.add((str(ref["object_id"]), str(ref["revision"]), str(ref["sha256"]).lower()))
    composition_ref = manifest_payload.get("composition_ref")
    if isinstance(composition_ref, Mapping) and composition_ref.get("object_id") and composition_ref.get("revision") and composition_ref.get("sha256"):
        keys.add((str(composition_ref["object_id"]), str(composition_ref["revision"]), str(composition_ref["sha256"]).lower()))
    provenance = manifest_payload.get("provenance_tree")
    for node in _walk_lineage(provenance):
        if node.get("node_id") and node.get("revision") and node.get("sha256"):
            keys.add((str(node["node_id"]), str(node["revision"]), str(node["sha256"]).lower()))
    return keys


class OutcomeAttributionEngine:
    """Canonical event admission, exact-release attribution, and read/query boundary."""

    def __init__(
        self,
        *,
        performance_weight: float = 0.5,
        conversion_weight: float = 0.5,
        clock: Callable[[], str] | None = None,
    ) -> None:
        self.performance_weight = _require_nonnegative_finite(performance_weight, "performance_weight")
        self.conversion_weight = _require_nonnegative_finite(conversion_weight, "conversion_weight")
        if self.performance_weight + self.conversion_weight <= 0.0:
            raise OutcomeValidationError("performance_weight + conversion_weight must be positive")
        self.clock = clock or _utc_now

    def ingest(
        self,
        event: OutcomeEvent | Mapping[str, Any],
        *,
        release_manifest: Any,
        distribution_receipt: Any,
        distribution_receipt_signing_secret: bytes | str | None = None,
    ) -> AttributedOutcome:
        """Admit and attribute one raw post-distribution event.

        The distribution receipt is authoritative for the delivered release. The
        event may include a campaign id, but the campaign is informational only;
        it is never used to resolve release identity.
        """

        normalized_event = event if isinstance(event, OutcomeEvent) else OutcomeEvent.from_mapping(event)
        release_id, manifest_sha, manifest_payload = _manifest_identity(release_manifest)
        receipt_payload = _receipt_payload(distribution_receipt)
        receipt_id = _require_text(receipt_payload.get("receipt_id"), "distribution_receipt.receipt_id")
        receipt_release_id = _require_text(receipt_payload.get("release_id"), "distribution_receipt.release_id")
        receipt_manifest_sha = _require_sha256(
            receipt_payload.get("release_manifest_sha256"),
            "distribution_receipt.release_manifest_sha256",
        )
        receipt_status = receipt_payload.get("delivery_status")
        if hasattr(receipt_status, "value"):
            receipt_status = receipt_status.value
        if str(receipt_status) != DELIVERED_STATUS:
            raise OutcomeIntegrityError("outcome events require a successful DISTRIBUTED/DELIVERED receipt")

        if distribution_receipt_signing_secret is not None and hasattr(distribution_receipt, "verify"):
            distribution_receipt.verify(distribution_receipt_signing_secret)

        if normalized_event.release_id != release_id or normalized_event.release_id != receipt_release_id:
            raise UnknownReleaseError("outcome release_id does not exactly match the sealed release and delivery receipt")
        if normalized_event.release_manifest_sha256 != manifest_sha or normalized_event.release_manifest_sha256 != receipt_manifest_sha:
            raise OutcomeIntegrityError("outcome release manifest digest does not exactly match the sealed release and delivery receipt")
        if normalized_event.distribution_receipt_id != receipt_id:
            raise OutcomeIntegrityError("outcome distribution receipt id does not match the supplied delivery receipt")

        lineage_keys = _manifest_lineage_keys(manifest_payload)
        all_refs = (
            *normalized_event.tension_collision_anchor_refs,
            *normalized_event.creative_component_refs,
            *normalized_event.audience_hypothesis_refs,
        )
        unresolved = [
            ref for ref in all_refs
            if (ref.object_id, ref.revision, ref.sha256.lower()) not in lineage_keys
        ]
        if unresolved:
            raise UnresolvedAttributionError(
                "one or more explicit causal references are absent from the sealed release lineage"
            )

        distribution_receipt_sha = _payload_digest(receipt_payload)
        metrics = normalized_event.metrics
        attributed = AttributedOutcome(
            outcome_id=f"OUTA-{uuid4().hex[:12]}",
            event_id=normalized_event.event_id,
            event_sha256=normalized_event.event_sha256,
            release_id=release_id,
            release_manifest_sha256=manifest_sha,
            distribution_receipt_id=receipt_id,
            distribution_receipt_sha256=distribution_receipt_sha,
            campaign_id=normalized_event.campaign_id,
            tension_collision_anchor_refs=normalized_event.tension_collision_anchor_refs,
            creative_component_refs=normalized_event.creative_component_refs,
            audience_hypothesis_refs=normalized_event.audience_hypothesis_refs,
            performance_yield=metrics.performance_yield,
            conversion_yield=metrics.conversion_yield,
            outcome_yield=metrics.outcome_yield(
                performance_weight=self.performance_weight,
                conversion_weight=self.conversion_weight,
            ),
            observed_at=normalized_event.observed_at,
            source=normalized_event.source,
            causal_interpretation_allowed=False,
            created_at=self.clock(),
        )
        object.__setattr__(attributed, "record_sha256", _payload_digest(attributed.unsigned_payload()))
        attributed.verify()
        return attributed


class OutcomeAttributionStore:
    """Append-only local store for attributed observations with deterministic queries."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._records_by_event_id: dict[str, AttributedOutcome] = {}

    def append(self, record: AttributedOutcome) -> AttributedOutcome:
        record.verify()
        with self._lock:
            existing = self._records_by_event_id.get(record.event_id)
            if existing is not None:
                if not hmac.compare_digest(existing.event_sha256, record.event_sha256):
                    raise OutcomeAttributionConflictError(
                        "event_id has already been admitted with different telemetry content"
                    )
                return existing
            self._records_by_event_id[record.event_id] = record
            return record

    def get(self, event_id: str) -> AttributedOutcome | None:
        with self._lock:
            return self._records_by_event_id.get(event_id)

    def all(self) -> tuple[AttributedOutcome, ...]:
        with self._lock:
            return tuple(self._records_by_event_id.values())

    def query_by_release(self, release_id: str) -> tuple[AttributedOutcome, ...]:
        release_id = _require_text(release_id, "release_id")
        return tuple(record for record in self.all() if record.release_id == release_id)

    def query_by_anchor(self, reference: CausalReference) -> tuple[AttributedOutcome, ...]:
        return tuple(
            record for record in self.all()
            if reference in record.tension_collision_anchor_refs
        )

    def query_by_component(self, reference: CausalReference) -> tuple[AttributedOutcome, ...]:
        return tuple(
            record for record in self.all()
            if reference in record.creative_component_refs
        )

    def aggregate_for_reference(
        self,
        reference: CausalReference,
        *,
        reference_kind: str,
    ) -> AttributionAggregate:
        normalized_kind = _require_text(reference_kind, "reference_kind").upper()
        if normalized_kind == "ANCHOR":
            records = self.query_by_anchor(reference)
        elif normalized_kind == "COMPONENT":
            records = self.query_by_component(reference)
        else:
            raise OutcomeValidationError("reference_kind must be ANCHOR or COMPONENT")
        if not records:
            return AttributionAggregate(
                reference=reference,
                observation_count=0,
                attributed_weight=0.0,
                weighted_outcome_yield=0.0,
                mean_outcome_yield=0.0,
                yield_per_observation=0.0,
                correlation_with_outcome_yield=None,
            )
        # Equal attribution weight across every explicitly named reference in the
        # relevant event preserves direct linkage without inventing winner/loser
        # semantics that the telemetry does not contain.
        weights: list[float] = []
        yields: list[float] = []
        for record in records:
            refs = record.tension_collision_anchor_refs if normalized_kind == "ANCHOR" else record.creative_component_refs
            weight = 1.0 / len(refs)
            weights.append(weight)
            yields.append(record.outcome_yield)
        total_weight = sum(weights)
        weighted_yield = sum(weight * outcome for weight, outcome in zip(weights, yields)) / total_weight
        return AttributionAggregate(
            reference=reference,
            observation_count=len(records),
            attributed_weight=total_weight,
            weighted_outcome_yield=weighted_yield,
            mean_outcome_yield=mean(yields),
            yield_per_observation=weighted_yield,
            correlation_with_outcome_yield=_pearson(weights, yields),
        )

    def trace(self, event_id: str) -> dict[str, Any]:
        record = self.get(_require_text(event_id, "event_id"))
        if record is None:
            raise UnknownReleaseError(f"no attributed outcome exists for event_id={event_id!r}")
        record.verify()
        return {
            "outcome_id": record.outcome_id,
            "event_id": record.event_id,
            "release": {
                "release_id": record.release_id,
                "release_manifest_sha256": record.release_manifest_sha256,
            },
            "distribution": {
                "receipt_id": record.distribution_receipt_id,
                "receipt_sha256": record.distribution_receipt_sha256,
            },
            "causal_lineage": {
                "tension_collision_anchors": [ref.to_dict() for ref in record.tension_collision_anchor_refs],
                "creative_components": [ref.to_dict() for ref in record.creative_component_refs],
                "audience_hypotheses": [ref.to_dict() for ref in record.audience_hypothesis_refs],
            },
            "observed_metrics": {
                "performance_yield": record.performance_yield,
                "conversion_yield": record.conversion_yield,
                "outcome_yield": record.outcome_yield,
                "causal_interpretation_allowed": False,
            },
        }

    def to_json_bytes(self) -> bytes:
        payload = {
            "schema_version": SCHEMA_VERSION,
            "records": [record.to_dict() for record in self.all()],
        }
        return json.dumps(
            payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode("utf-8")

    def save(self, path: str | Path) -> Path:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(self.to_json_bytes() + b"\n")
        return destination

    @classmethod
    def from_json_bytes(cls, raw: bytes) -> "OutcomeAttributionStore":
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise OutcomeValidationError("invalid outcome attribution store JSON") from exc
        if payload.get("schema_version") != SCHEMA_VERSION:
            raise OutcomeValidationError("unsupported outcome attribution schema version")
        store = cls()
        for item in payload.get("records", []):
            refs_anchor = _normalize_refs(item.get("tension_collision_anchor_refs", []), "tension_collision_anchor_refs")
            refs_component = _normalize_refs(item.get("creative_component_refs", []), "creative_component_refs")
            refs_audience = _normalize_refs(item.get("audience_hypothesis_refs", []), "audience_hypothesis_refs") if item.get("audience_hypothesis_refs") else ()
            record = AttributedOutcome(
                outcome_id=_require_text(item.get("outcome_id"), "outcome_id"),
                event_id=_require_text(item.get("event_id"), "event_id"),
                event_sha256=_require_sha256(item.get("event_sha256"), "event_sha256"),
                release_id=_require_text(item.get("release_id"), "release_id"),
                release_manifest_sha256=_require_sha256(item.get("release_manifest_sha256"), "release_manifest_sha256"),
                distribution_receipt_id=_require_text(item.get("distribution_receipt_id"), "distribution_receipt_id"),
                distribution_receipt_sha256=_require_sha256(item.get("distribution_receipt_sha256"), "distribution_receipt_sha256"),
                campaign_id=item.get("campaign_id"),
                tension_collision_anchor_refs=refs_anchor,
                creative_component_refs=refs_component,
                audience_hypothesis_refs=refs_audience,
                performance_yield=_require_nonnegative_finite(item.get("performance_yield"), "performance_yield"),
                conversion_yield=_require_nonnegative_finite(item.get("conversion_yield"), "conversion_yield"),
                outcome_yield=_require_nonnegative_finite(item.get("outcome_yield"), "outcome_yield"),
                observed_at=_require_text(item.get("observed_at"), "observed_at"),
                source=_require_text(item.get("source"), "source"),
                causal_interpretation_allowed=bool(item.get("causal_interpretation_allowed", False)),
                created_at=_require_text(item.get("created_at"), "created_at"),
                record_sha256=_require_sha256(item.get("record_sha256"), "record_sha256"),
            )
            record.verify()
            store.append(record)
        return store

    @classmethod
    def load(cls, path: str | Path) -> "OutcomeAttributionStore":
        try:
            raw = Path(path).read_bytes()
        except OSError as exc:
            raise OutcomeIntegrityError(f"unable to read outcome attribution store: {path}") from exc
        return cls.from_json_bytes(raw)
