"""Doctrine-driven test harness contracts for TS-CMF-077."""

from __future__ import annotations

import json
from datetime import datetime
from hashlib import sha256
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.orchestration import utc_now


class DoctrineTestDecision(str, Enum):
    passed = "passed"
    needs_revision = "needs_revision"
    blocked = "blocked"


class DoctrineTestTarget(BaseModel):
    schema_version: Literal["cmf.doctrine_test_target.v1"]
    target_type: str = Field(min_length=1)
    target_id: UUID
    object_hash: str | None = None
    spec_id: str | None = None
    pipeline_stage: str | None = None
    lineage_refs: list[str] = Field(default_factory=list)


class DoctrineInvariant(BaseModel):
    schema_version: Literal["cmf.doctrine_invariant.v1"]
    invariant_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    statement: str = Field(min_length=1)
    source_doctrine_refs: list[str] = Field(min_length=1)
    applies_to_target_types: list[str] = Field(default_factory=lambda: ["*"])
    required_evidence_types: list[str] = Field(default_factory=list)
    hard_failure_code: str = Field(min_length=1)
    approval_blocker_code: str = Field(min_length=1)

    @model_validator(mode="after")
    def require_evidence_or_target_scope(self) -> "DoctrineInvariant":
        if not self.required_evidence_types and "*" not in self.applies_to_target_types:
            raise ValueError("target-scoped invariants must declare at least one required evidence type")
        return self


class DoctrinePrimitiveTestObligation(BaseModel):
    schema_version: Literal["cmf.doctrine_primitive_test_obligation.v1"]
    primitive_ref: str = Field(min_length=1)
    primitive_family: str = Field(min_length=1)
    doctrine_binding: str = Field(min_length=1)
    required_evidence_types: list[str] = Field(min_length=1)
    hard_failure_code: str = Field(min_length=1)
    approval_blocker_code: str = Field(min_length=1)


class DoctrineNegativeFixture(BaseModel):
    schema_version: Literal["cmf.doctrine_negative_fixture.v1"]
    fixture_id: str = Field(min_length=1)
    forbidden_shortcut: str = Field(min_length=1)
    description: str = Field(min_length=1)
    required_absent_terms: list[str] = Field(default_factory=list)
    required_evidence_types: list[str] = Field(default_factory=list)
    hard_failure_code: str = Field(min_length=1)
    approval_blocker_code: str = Field(min_length=1)

    @model_validator(mode="after")
    def require_detection_condition(self) -> "DoctrineNegativeFixture":
        if not self.required_absent_terms and not self.required_evidence_types:
            raise ValueError("negative fixtures need forbidden terms or evidence requirements")
        return self


class DoctrineInvariantResult(BaseModel):
    invariant_id: str = Field(min_length=1)
    passed: bool
    evidence_refs: list[str] = Field(default_factory=list)
    missing_evidence_types: list[str] = Field(default_factory=list)
    hard_failure_code: str | None = None
    approval_blocker_code: str | None = None

    @model_validator(mode="after")
    def require_blocker_for_failure(self) -> "DoctrineInvariantResult":
        if not self.passed and (not self.hard_failure_code or not self.approval_blocker_code):
            raise ValueError("failed invariant results require hard failure and approval blocker codes")
        return self


class DoctrinePrimitiveResult(BaseModel):
    primitive_ref: str = Field(min_length=1)
    primitive_family: str = Field(min_length=1)
    passed: bool
    evidence_refs: list[str] = Field(default_factory=list)
    missing_evidence_types: list[str] = Field(default_factory=list)
    hard_failure_code: str | None = None
    approval_blocker_code: str | None = None

    @model_validator(mode="after")
    def require_blocker_for_failure(self) -> "DoctrinePrimitiveResult":
        if not self.passed and (not self.hard_failure_code or not self.approval_blocker_code):
            raise ValueError("failed primitive results require hard failure and approval blocker codes")
        return self


class DoctrineNegativeFixtureResult(BaseModel):
    fixture_id: str = Field(min_length=1)
    forbidden_shortcut: str = Field(min_length=1)
    passed: bool
    evidence_refs: list[str] = Field(default_factory=list)
    triggered_terms: list[str] = Field(default_factory=list)
    missing_evidence_types: list[str] = Field(default_factory=list)
    hard_failure_code: str | None = None
    approval_blocker_code: str | None = None

    @model_validator(mode="after")
    def require_blocker_for_failure(self) -> "DoctrineNegativeFixtureResult":
        if not self.passed and (not self.hard_failure_code or not self.approval_blocker_code):
            raise ValueError("failed negative fixture results require hard failure and approval blocker codes")
        return self


class DoctrineTestRunReceipt(BaseModel):
    schema_version: Literal["cmf.doctrine_test_run_receipt.v1"]
    doctrine_test_run_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    target: DoctrineTestTarget
    invariant_results: list[DoctrineInvariantResult] = Field(default_factory=list)
    primitive_results: list[DoctrinePrimitiveResult] = Field(default_factory=list)
    negative_fixture_results: list[DoctrineNegativeFixtureResult] = Field(default_factory=list)
    decision: DoctrineTestDecision
    hard_failures: list[str] = Field(default_factory=list)
    approval_blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    actor_id: UUID
    command_id: UUID | None = None
    receipt_hash: str = Field(min_length=1)
    created_at: datetime

    @model_validator(mode="after")
    def require_blocked_decision_for_hard_failures(self) -> "DoctrineTestRunReceipt":
        if self.hard_failures and self.decision != DoctrineTestDecision.blocked:
            raise ValueError("hard failures require blocked decision")
        if self.decision == DoctrineTestDecision.blocked and not self.hard_failures:
            raise ValueError("blocked decision requires hard failures")
        if self.approval_blocker_codes and not self.hard_failures:
            raise ValueError("approval blockers require hard failures")
        return self


def doctrine_test_receipt_hash(receipt: DoctrineTestRunReceipt) -> str:
    payload = receipt.model_dump(mode="json", exclude={"receipt_hash"})
    return sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def new_doctrine_test_target(
    *,
    target_type: str,
    target_id: UUID,
    object_hash: str | None = None,
    spec_id: str | None = None,
    pipeline_stage: str | None = None,
    lineage_refs: list[str] | None = None,
) -> DoctrineTestTarget:
    return DoctrineTestTarget(
        schema_version="cmf.doctrine_test_target.v1",
        target_type=target_type,
        target_id=target_id,
        object_hash=object_hash,
        spec_id=spec_id,
        pipeline_stage=pipeline_stage,
        lineage_refs=lineage_refs or [],
    )


def new_doctrine_test_run_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    target: DoctrineTestTarget,
    invariant_results: list[DoctrineInvariantResult],
    primitive_results: list[DoctrinePrimitiveResult],
    negative_fixture_results: list[DoctrineNegativeFixtureResult],
    actor_id: UUID,
    command_id: UUID | None = None,
) -> DoctrineTestRunReceipt:
    hard_failures = _unique(
        [
            code
            for result in [*invariant_results, *primitive_results, *negative_fixture_results]
            for code in [result.hard_failure_code]
            if code
        ]
    )
    approval_blocker_codes = _unique(
        [
            code
            for result in [*invariant_results, *primitive_results, *negative_fixture_results]
            for code in [result.approval_blocker_code]
            if code
        ]
    )
    evidence_refs = _unique(
        [
            ref
            for result in [*invariant_results, *primitive_results, *negative_fixture_results]
            for ref in result.evidence_refs
        ]
    )
    decision = DoctrineTestDecision.blocked if hard_failures else DoctrineTestDecision.passed
    receipt = DoctrineTestRunReceipt(
        schema_version="cmf.doctrine_test_run_receipt.v1",
        doctrine_test_run_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        target=target,
        invariant_results=invariant_results,
        primitive_results=primitive_results,
        negative_fixture_results=negative_fixture_results,
        decision=decision,
        hard_failures=hard_failures,
        approval_blocker_codes=approval_blocker_codes,
        evidence_refs=evidence_refs,
        actor_id=actor_id,
        command_id=command_id,
        receipt_hash="pending",
        created_at=utc_now(),
    )
    return receipt.model_copy(update={"receipt_hash": doctrine_test_receipt_hash(receipt)})


def _unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    values: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            values.append(item)
    return values
