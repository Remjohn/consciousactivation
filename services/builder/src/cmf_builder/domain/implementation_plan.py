from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha256
import json
from typing import Mapping

from cmf_builder.domain.development_capsule import (
    CAPSULE_MODE,
    VersionedTraceableDevelopmentCapsule,
)


PLAN_INPUT_PATH = (
    "development-capsules/ST-11.02/"
    "SYNTHETIC_VERTICAL_IMPLEMENTATION_PLAN_INPUT.json"
)
PLAN_INPUT_SHA256 = "672c2e6d8b7f6b3951d679c0721a93169cc122ccc6c2babc1c72539fc7f8647b"
PLAN_MODE = "SYNTHETIC_BUILDER_PROOF_HANDOFF_ONLY"
PLAN_PROFILE_ID = "synthetic_text_normalization_v1"
PLAN_OUTCOME = "DEPENDENCY_ORDERED_VERTICAL_IMPLEMENTATION_PLAN_COMPILED"
OWNED_OBLIGATIONS = ("FR-156", "FR-157")
DIRECT_DEPENDENCIES = ("ST-11.01",)
EXTERNAL_TARGET_COMPATIBILITY = "NOT_EVALUATED_EXTERNAL_TARGET_BRANCH"
HORIZONTAL_LAYER_TITLES = frozenset(
    {"database", "api", "frontend", "schema", "infrastructure"}
)


class ImplementationPlanError(Exception):
    code = "ImplementationPlanError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class ImplementationPlanInputInvalid(ImplementationPlanError):
    code = "ImplementationPlanInputInvalid"


class ImplementationPlanTraceInvalid(ImplementationPlanError):
    code = "ImplementationPlanTraceInvalid"


class ImplementationPlanScopeInvalid(ImplementationPlanError):
    code = "ImplementationPlanScopeInvalid"


class ImplementationPlanAuthorityInvalid(ImplementationPlanError):
    code = "ImplementationPlanAuthorityInvalid"


class ImplementationPlanInvalidatedError(ImplementationPlanError):
    code = "ImplementationPlanInvalidated"


@dataclass(frozen=True, slots=True)
class VerticalIncrement:
    increment_id: str
    outcome: str
    depends_on: tuple[str, ...]
    requirement_ids: tuple[str, ...]
    acceptance_evidence: tuple[str, ...]
    test_ids: tuple[str, ...]
    observability_evidence: tuple[str, ...]
    rollback_requirements: tuple[str, ...]
    file_scope: tuple[str, ...]
    prohibited_scope: tuple[str, ...]
    one_focused_context: bool
    user_observable: bool

    @classmethod
    def from_mapping(cls, value: Mapping[str, object]) -> "VerticalIncrement":
        return cls(
            increment_id=_text(value, "increment_id"),
            outcome=_text(value, "outcome"),
            depends_on=_text_sequence(value, "depends_on", allow_empty=True),
            requirement_ids=_text_sequence(value, "requirement_ids"),
            acceptance_evidence=_text_sequence(value, "acceptance_evidence"),
            test_ids=_text_sequence(value, "test_ids"),
            observability_evidence=_text_sequence(value, "observability_evidence"),
            rollback_requirements=_text_sequence(value, "rollback_requirements"),
            file_scope=_text_sequence(value, "file_scope"),
            prohibited_scope=_text_sequence(value, "prohibited_scope"),
            one_focused_context=value.get("one_focused_context") is True,
            user_observable=value.get("user_observable") is True,
        )

    def validate(self, earlier_increment_ids: tuple[str, ...]) -> None:
        if (
            not self.increment_id.startswith("VI-")
            or not self.outcome.strip()
            or not self.one_focused_context
            or not self.user_observable
            or not self.requirement_ids
            or not self.acceptance_evidence
            or not self.test_ids
            or not self.observability_evidence
            or not self.rollback_requirements
            or not self.file_scope
            or not self.prohibited_scope
        ):
            raise ImplementationPlanInputInvalid(
                "Every increment must be focused, observable and independently verifiable.",
                increment_id=self.increment_id,
            )
        if tuple(dict.fromkeys(self.depends_on)) != self.depends_on or any(
            dependency not in earlier_increment_ids for dependency in self.depends_on
        ):
            raise ImplementationPlanInputInvalid(
                "Increment dependencies must reference earlier increments only.",
                increment_id=self.increment_id,
                depends_on=self.depends_on,
            )
        lowered = self.outcome.strip().lower()
        if lowered in HORIZONTAL_LAYER_TITLES:
            raise ImplementationPlanScopeInvalid(
                "A horizontal technical layer is not a vertical outcome.",
                increment_id=self.increment_id,
            )
        if any(_is_absolute_path(path) for path in self.file_scope):
            raise ImplementationPlanScopeInvalid(
                "Portable plan scope cannot contain absolute paths.",
                increment_id=self.increment_id,
            )
        if any(item not in OWNED_OBLIGATIONS for item in self.requirement_ids):
            raise ImplementationPlanTraceInvalid(
                "An increment claims an obligation outside ST-11.02 ownership.",
                increment_id=self.increment_id,
            )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "increment_id": self.increment_id,
            "outcome": self.outcome,
            "depends_on": list(self.depends_on),
            "requirement_ids": list(self.requirement_ids),
            "acceptance_evidence": list(self.acceptance_evidence),
            "test_ids": list(self.test_ids),
            "observability_evidence": list(self.observability_evidence),
            "rollback_requirements": list(self.rollback_requirements),
            "file_scope": list(self.file_scope),
            "prohibited_scope": list(self.prohibited_scope),
            "one_focused_context": self.one_focused_context,
            "user_observable": self.user_observable,
        }


@dataclass(frozen=True, slots=True)
class VerticalImplementationPlan:
    plan_id: str
    plan_hash: str
    schema_id: str
    schema_version: str
    plan_version: str
    active_mode: str
    profile_id: str
    run_id: str
    capsule_id: str
    capsule_hash: str
    capsule_version: str
    capsule_authority_identity: str
    plan_input_path: str
    plan_input_hash: str
    obligation_ids: tuple[str, ...]
    dependency_order: tuple[str, ...]
    first_working_increment_id: str
    increments: tuple[VerticalIncrement, ...]
    authority_identity: str
    lineage: tuple[str, ...]
    implementation_authorized: bool
    production_eligible: bool
    certified: bool
    external_target_compatibility: str
    completion_receipt_contract: str
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        capsule: VersionedTraceableDevelopmentCapsule,
        plan_input: Mapping[str, object],
        authority_identity: str,
    ) -> "VerticalImplementationPlan":
        _validate_input_contract(plan_input)
        increments = tuple(
            VerticalIncrement.from_mapping(item)
            for item in _mapping_sequence(plan_input, "increments")
        )
        candidate = cls(
            plan_id="pending",
            plan_hash="pending",
            schema_id="cmf-builder-vertical-implementation-plan/v1",
            schema_version="1.0.0",
            plan_version=_text(plan_input, "plan_version"),
            active_mode=_text(plan_input, "active_mode"),
            profile_id=_text(plan_input, "profile_id"),
            run_id=capsule.run_id,
            capsule_id=capsule.capsule_id,
            capsule_hash=capsule.capsule_hash,
            capsule_version=capsule.capsule_version,
            capsule_authority_identity=capsule.authority_identity,
            plan_input_path=PLAN_INPUT_PATH,
            plan_input_hash=f"sha256:{PLAN_INPUT_SHA256}",
            obligation_ids=OWNED_OBLIGATIONS,
            dependency_order=DIRECT_DEPENDENCIES,
            first_working_increment_id=_text(
                plan_input, "first_working_increment_id"
            ),
            increments=increments,
            authority_identity=authority_identity,
            lineage=(
                capsule.capsule_hash,
                capsule.definition_hash,
                capsule.validation_hash,
                f"sha256:{PLAN_INPUT_SHA256}",
            ),
            implementation_authorized=False,
            production_eligible=False,
            certified=False,
            external_target_compatibility=EXTERNAL_TARGET_COMPATIBILITY,
            completion_receipt_contract=_text(
                plan_input, "completion_receipt_contract"
            ),
            outcome=PLAN_OUTCOME,
        )
        candidate.validate(capsule)
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            plan_id=f"vertical-plan_{digest}",
            plan_hash=f"sha256:{digest}",
        )
        result.validate(capsule)
        return result

    def validate(self, capsule: VersionedTraceableDevelopmentCapsule) -> None:
        if (
            self.schema_id != "cmf-builder-vertical-implementation-plan/v1"
            or self.schema_version != "1.0.0"
            or self.active_mode != PLAN_MODE
            or self.profile_id != PLAN_PROFILE_ID
            or self.run_id != capsule.run_id
            or self.capsule_id != capsule.capsule_id
            or self.capsule_hash != capsule.capsule_hash
            or self.capsule_version != capsule.capsule_version
            or self.capsule_authority_identity != capsule.authority_identity
            or self.plan_input_path != PLAN_INPUT_PATH
            or self.plan_input_hash != f"sha256:{PLAN_INPUT_SHA256}"
            or self.obligation_ids != OWNED_OBLIGATIONS
            or self.dependency_order != DIRECT_DEPENDENCIES
            or len(self.increments) < 2
            or self.implementation_authorized
            or self.production_eligible
            or self.certified
            or self.external_target_compatibility != EXTERNAL_TARGET_COMPATIBILITY
            or self.outcome != PLAN_OUTCOME
            or capsule.active_mode != CAPSULE_MODE
            or capsule.profile_id != PLAN_PROFILE_ID
            or capsule.generated_product_implementation
            or capsule.production_eligible
            or capsule.certified
        ):
            raise ImplementationPlanTraceInvalid(
                "The plan does not preserve its exact synthetic Development Capsule authority."
            )
        ids: list[str] = []
        for increment in self.increments:
            increment.validate(tuple(ids))
            ids.append(increment.increment_id)
        if (
            len(ids) != len(set(ids))
            or self.first_working_increment_id != ids[0]
            or frozenset(
                requirement
                for increment in self.increments
                for requirement in increment.requirement_ids
            )
            != frozenset(OWNED_OBLIGATIONS)
        ):
            raise ImplementationPlanTraceInvalid(
                "The plan must cover every owned obligation and identify its first increment."
            )
        if self.lineage != (
            capsule.capsule_hash,
            capsule.definition_hash,
            capsule.validation_hash,
            f"sha256:{PLAN_INPUT_SHA256}",
        ):
            raise ImplementationPlanTraceInvalid("Plan lineage is incomplete or altered.")
        if self.plan_id != "pending" or self.plan_hash != "pending":
            digest = sha256(
                replace(self, plan_id="pending", plan_hash="pending").canonical_bytes()
            ).hexdigest()
            if self.plan_id != f"vertical-plan_{digest}" or self.plan_hash != f"sha256:{digest}":
                raise ImplementationPlanTraceInvalid("Plan identity is not deterministic.")

    def canonical_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "plan_version": self.plan_version,
            "active_mode": self.active_mode,
            "profile_id": self.profile_id,
            "run_id": self.run_id,
            "capsule_id": self.capsule_id,
            "capsule_hash": self.capsule_hash,
            "capsule_version": self.capsule_version,
            "capsule_authority_identity": self.capsule_authority_identity,
            "plan_input_path": self.plan_input_path,
            "plan_input_hash": self.plan_input_hash,
            "obligation_ids": list(self.obligation_ids),
            "dependency_order": list(self.dependency_order),
            "first_working_increment_id": self.first_working_increment_id,
            "increments": [item.canonical_dict() for item in self.increments],
            "authority_identity": self.authority_identity,
            "lineage": list(self.lineage),
            "implementation_authorized": self.implementation_authorized,
            "production_eligible": self.production_eligible,
            "certified": self.certified,
            "external_target_compatibility": self.external_target_compatibility,
            "completion_receipt_contract": self.completion_receipt_contract,
            "outcome": self.outcome,
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(self.canonical_dict())


@dataclass(frozen=True, slots=True)
class ImplementationPlanReceipt:
    receipt_id: str
    receipt_hash: str
    schema_id: str
    command_id: str
    run_id: str
    plan_id: str
    plan_hash: str
    capsule_id: str
    capsule_hash: str
    authority_identity: str
    stream_version: int
    increment_count: int
    obligation_count: int
    implementation_authorized: bool
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        plan: VerticalImplementationPlan,
        stream_version: int,
    ) -> "ImplementationPlanReceipt":
        candidate = cls(
            receipt_id="pending",
            receipt_hash="pending",
            schema_id="cmf-builder-vertical-implementation-plan-receipt/v1",
            command_id=command_id,
            run_id=plan.run_id,
            plan_id=plan.plan_id,
            plan_hash=plan.plan_hash,
            capsule_id=plan.capsule_id,
            capsule_hash=plan.capsule_hash,
            authority_identity=plan.authority_identity,
            stream_version=stream_version,
            increment_count=len(plan.increments),
            obligation_count=len(plan.obligation_ids),
            implementation_authorized=False,
            outcome=PLAN_OUTCOME,
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            receipt_id=f"vertical-plan-receipt_{digest}",
            receipt_hash=f"sha256:{digest}",
        )
        result.validate(plan)
        return result

    def validate(self, plan: VerticalImplementationPlan) -> None:
        if (
            self.schema_id != "cmf-builder-vertical-implementation-plan-receipt/v1"
            or self.run_id != plan.run_id
            or self.plan_id != plan.plan_id
            or self.plan_hash != plan.plan_hash
            or self.capsule_id != plan.capsule_id
            or self.capsule_hash != plan.capsule_hash
            or self.authority_identity != plan.authority_identity
            or self.stream_version < 1
            or self.increment_count != len(plan.increments)
            or self.obligation_count != len(plan.obligation_ids)
            or self.implementation_authorized
            or self.outcome != PLAN_OUTCOME
        ):
            raise ImplementationPlanTraceInvalid("Implementation plan receipt is invalid.")
        if self.receipt_id != "pending" or self.receipt_hash != "pending":
            digest = sha256(
                replace(self, receipt_id="pending", receipt_hash="pending").canonical_bytes()
            ).hexdigest()
            if self.receipt_id != f"vertical-plan-receipt_{digest}" or self.receipt_hash != f"sha256:{digest}":
                raise ImplementationPlanTraceInvalid("Receipt identity is not deterministic.")

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "schema_id": self.schema_id,
                "command_id": self.command_id,
                "run_id": self.run_id,
                "plan_id": self.plan_id,
                "plan_hash": self.plan_hash,
                "capsule_id": self.capsule_id,
                "capsule_hash": self.capsule_hash,
                "authority_identity": self.authority_identity,
                "stream_version": self.stream_version,
                "increment_count": self.increment_count,
                "obligation_count": self.obligation_count,
                "implementation_authorized": self.implementation_authorized,
                "outcome": self.outcome,
            }
        )


def _validate_input_contract(value: Mapping[str, object]) -> None:
    if (
        value.get("schema_version") != "cmf-builder-synthetic-vertical-plan-input/v1"
        or value.get("story_id") != "ST-11.02"
        or value.get("active_mode") != PLAN_MODE
        or value.get("profile_id") != PLAN_PROFILE_ID
        or tuple(value.get("owned_obligations", ())) != OWNED_OBLIGATIONS
        or tuple(value.get("direct_dependencies", ())) != DIRECT_DEPENDENCIES
        or value.get("implementation_authorized") is not False
        or value.get("production_eligible") is not False
        or value.get("certified") is not False
        or value.get("external_target_compatibility") != EXTERNAL_TARGET_COMPATIBILITY
        or value.get("expected_outcome") != PLAN_OUTCOME
    ):
        raise ImplementationPlanInputInvalid("Vertical plan input contract is invalid.")


def _mapping_sequence(value: Mapping[str, object], key: str) -> tuple[Mapping[str, object], ...]:
    raw = value.get(key)
    if not isinstance(raw, list) or not raw or any(not isinstance(item, Mapping) for item in raw):
        raise ImplementationPlanInputInvalid(f"{key} must contain governed mappings.")
    return tuple(raw)  # type: ignore[return-value]


def _text(value: Mapping[str, object], key: str) -> str:
    raw = value.get(key)
    if not isinstance(raw, str) or not raw.strip():
        raise ImplementationPlanInputInvalid(f"{key} must be non-empty text.")
    return raw


def _text_sequence(
    value: Mapping[str, object], key: str, *, allow_empty: bool = False
) -> tuple[str, ...]:
    raw = value.get(key)
    if not isinstance(raw, list) or any(
        not isinstance(item, str) or not item.strip() for item in raw
    ) or (not raw and not allow_empty):
        raise ImplementationPlanInputInvalid(f"{key} must contain governed text.")
    return tuple(raw)


def _is_absolute_path(value: str) -> bool:
    normalized = value.replace("\\", "/")
    return normalized.startswith("/") or ":/" in normalized


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
