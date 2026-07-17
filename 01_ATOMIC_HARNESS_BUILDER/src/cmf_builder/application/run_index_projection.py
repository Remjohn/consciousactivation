"""Evidence-derived run index projection for OD-AM-002 / ST-10.01."""

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


class RunIndexError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class GateState(str, Enum):
    PASS_ = "PASS"
    PENDING = "PENDING"
    BLOCKED = "BLOCKED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class RunLifecycleState(str, Enum):
    ACTIVE = "ACTIVE"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    INVALIDATED = "INVALIDATED"
    STALE = "STALE"


def _text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise RunIndexError("MISSING_GOVERNED_FIELD", f"{name} is required")


@dataclass(frozen=True)
class RunEvidenceRecord:
    run_identity: str
    workflow_profile_identity: str
    harness_identity: str
    category_identity: str
    target_identity: str
    maturity_state: str
    implementation_status: GateState
    evidence_status: GateState
    authority_status: GateState
    production_status: GateState
    certification_status: GateState
    current_phase: str
    current_node: str
    lifecycle_state: RunLifecycleState
    latest_checkpoint_ref: str
    receipt_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    updated_at_utc: str
    freshness_ref: str
    partial: bool = False
    redacted_fields: tuple[str, ...] = ()
    source_receipt_hash: str = ""

    def __post_init__(self) -> None:
        for value, name in (
            (self.run_identity, "run_identity"),
            (self.workflow_profile_identity, "workflow_profile_identity"),
            (self.harness_identity, "harness_identity"),
            (self.category_identity, "category_identity"),
            (self.target_identity, "target_identity"),
            (self.maturity_state, "maturity_state"),
            (self.current_phase, "current_phase"),
            (self.current_node, "current_node"),
            (self.latest_checkpoint_ref, "latest_checkpoint_ref"),
            (self.updated_at_utc, "updated_at_utc"),
            (self.freshness_ref, "freshness_ref"),
            (self.source_receipt_hash, "source_receipt_hash"),
        ):
            _text(value, name)
        if self.production_status is GateState.PASS_ or self.certification_status is GateState.PASS_:
            raise RunIndexError("FALSE_PRODUCTION_OR_CERTIFICATION_CLAIM", "run index entry cannot imply production or certification")
        if not self.receipt_refs:
            raise RunIndexError("RUN_INDEX_REQUIRES_RECEIPT_TRACE", "run index entries must trace to receipts")

    def as_dict(self) -> dict[str, Any]:
        return {
            "run_identity": self.run_identity,
            "workflow_profile_identity": self.workflow_profile_identity,
            "harness_identity": self.harness_identity,
            "category_identity": self.category_identity,
            "target_identity": self.target_identity,
            "maturity_state": self.maturity_state,
            "implementation_status": self.implementation_status.value,
            "evidence_status": self.evidence_status.value,
            "authority_status": self.authority_status.value,
            "production_status": self.production_status.value,
            "certification_status": self.certification_status.value,
            "current_phase": self.current_phase,
            "current_node": self.current_node,
            "lifecycle_state": self.lifecycle_state.value,
            "latest_checkpoint_ref": self.latest_checkpoint_ref,
            "receipt_refs": list(self.receipt_refs),
            "evidence_refs": list(self.evidence_refs),
            "updated_at_utc": self.updated_at_utc,
            "freshness_ref": self.freshness_ref,
            "partial": self.partial,
            "redacted_fields": list(self.redacted_fields),
            "source_receipt_hash": self.source_receipt_hash,
        }

    @property
    def record_identity(self) -> str:
        return sha256_of(self.as_dict())


@dataclass(frozen=True)
class RunIndexProjection:
    records: tuple[RunEvidenceRecord, ...]
    sort_key: str
    filters: dict[str, str]
    page: int
    page_size: int
    total_records: int
    _anchor: str = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self.page < 1 or self.page_size < 1:
            raise RunIndexError("INVALID_PAGINATION", "page and page_size must be positive")
        object.__setattr__(self, "_anchor", sha256_of(self._payload()))

    def _payload(self) -> dict[str, Any]:
        return {
            "records": [record.as_dict() | {"record_identity": record.record_identity} for record in self.records],
            "sort_key": self.sort_key,
            "filters": self.filters,
            "page": self.page,
            "page_size": self.page_size,
            "total_records": self.total_records,
        }

    @property
    def projection_identity(self) -> str:
        return sha256_of(self._payload())

    def as_dict(self) -> dict[str, Any]:
        payload = self._payload()
        if sha256_of(payload) != self._anchor:
            raise RunIndexError("MUTATED_GOVERNED_OBJECT", "run index projection changed")
        payload["projection_identity"] = sha256_of(payload)
        return payload


def build_run_index(
    records: tuple[RunEvidenceRecord, ...],
    *,
    filters: dict[str, str] | None = None,
    sort_key: str = "run_identity",
    page: int = 1,
    page_size: int = 50,
) -> RunIndexProjection:
    filters = dict(filters or {})
    supported = {"maturity_state", "implementation_status", "evidence_status", "lifecycle_state", "category_identity", "target_identity"}
    unsupported = set(filters) - supported
    if unsupported:
        raise RunIndexError("UNSUPPORTED_RUN_INDEX_FILTER", "unsupported run index filter", filters=sorted(unsupported))
    filtered = list(records)
    for key, expected in filters.items():
        filtered = [record for record in filtered if str(getattr(record, key).value if hasattr(getattr(record, key), "value") else getattr(record, key)) == expected]
    if sort_key not in {"run_identity", "updated_at_utc", "maturity_state", "lifecycle_state"}:
        raise RunIndexError("UNSUPPORTED_RUN_INDEX_SORT", "unsupported run index sort")
    ordered = sorted(filtered, key=lambda record: str(getattr(record, sort_key).value if hasattr(getattr(record, sort_key), "value") else getattr(record, sort_key)))
    start = (page - 1) * page_size
    return RunIndexProjection(tuple(ordered[start : start + page_size]), sort_key, filters, page, page_size, len(filtered))


def detect_stale_records(records: tuple[RunEvidenceRecord, ...], active_receipt_hashes: set[str]) -> tuple[str, ...]:
    stale: list[str] = []
    for record in records:
        if record.source_receipt_hash not in active_receipt_hashes or record.lifecycle_state is RunLifecycleState.STALE:
            stale.append(record.record_identity)
    return tuple(sorted(stale))
