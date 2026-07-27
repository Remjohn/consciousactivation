"""Migrated registry contracts for TS-CMF-014."""

from __future__ import annotations

import hashlib
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class RegistryFamily(str, Enum):
    archetype = "archetype"
    cognitive_primitive = "cognitive_primitive"
    sda = "sda"
    sfl = "sfl"
    cbar_gate = "cbar_gate"
    ttt_profile = "ttt_profile"
    voice_dna = "voice_dna"
    creative_subsystem = "creative_subsystem"
    cmf_reference_behavior = "cmf_reference_behavior"


class RegistryStatus(str, Enum):
    draft = "draft"
    active = "active"
    blocked = "blocked"
    deprecated = "deprecated"


class FixtureSet(BaseModel):
    schema_version: Literal["cmf.fixture_set.v1"]
    fixture_set_id: UUID
    migration_ledger_entry_id: UUID
    fixture_path: str
    golden_examples: list[str] = Field(default_factory=list)
    counterexamples: list[str] = Field(default_factory=list)
    failure_cases: list[str] = Field(default_factory=list)
    content_hash: str


class EvaluationTarget(BaseModel):
    schema_version: Literal["cmf.evaluation_target.v1"]
    evaluation_target_id: UUID
    target_path: str
    threshold: float | None = Field(default=None, ge=0, le=1)
    required: bool = True


class RegistryEntry(BaseModel):
    schema_version: Literal["cmf.registry_entry.v1"]
    registry_entry_id: UUID
    registry_family: RegistryFamily
    migration_ledger_entry_id: UUID
    source_hash: str
    payload: dict[str, Any]
    fixture_set_ids: list[UUID] = Field(default_factory=list)
    evaluation_target_ids: list[UUID] = Field(default_factory=list)
    known_defects: list[str] = Field(default_factory=list)
    reviewer_actor_id: UUID
    status: RegistryStatus
    created_at: datetime
    updated_at: datetime


class RegistryConflict(BaseModel):
    schema_version: Literal["cmf.registry_conflict.v1"]
    registry_conflict_id: UUID
    registry_family: RegistryFamily
    existing_registry_entry_id: UUID
    proposed_registry_entry_id: UUID
    conflict_key: str
    resolved: bool = False
    created_at: datetime


class RegistryActivationReceipt(BaseModel):
    schema_version: Literal["cmf.registry_activation_receipt.v1"]
    registry_activation_receipt_id: UUID
    registry_entry_id: UUID
    migration_ledger_entry_id: UUID
    decision_code: str
    evidence_refs: list[str] = Field(default_factory=list)
    reviewer_actor_id: UUID
    written_at: datetime


def content_hash_for_fixture_parts(parts: list[str]) -> str:
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


def new_fixture_set(
    *,
    migration_ledger_entry_id: UUID,
    fixture_path: str,
    golden_examples: list[str],
    counterexamples: list[str],
    failure_cases: list[str],
) -> FixtureSet:
    return FixtureSet(
        schema_version="cmf.fixture_set.v1",
        fixture_set_id=uuid4(),
        migration_ledger_entry_id=migration_ledger_entry_id,
        fixture_path=fixture_path,
        golden_examples=golden_examples,
        counterexamples=counterexamples,
        failure_cases=failure_cases,
        content_hash=content_hash_for_fixture_parts(golden_examples + counterexamples + failure_cases),
    )


def new_evaluation_target(*, target_path: str, threshold: float | None = None, required: bool = True) -> EvaluationTarget:
    return EvaluationTarget(
        schema_version="cmf.evaluation_target.v1",
        evaluation_target_id=uuid4(),
        target_path=target_path,
        threshold=threshold,
        required=required,
    )


def new_registry_activation_receipt(
    *,
    registry_entry: RegistryEntry,
    decision_code: str,
    evidence_refs: list[str],
) -> RegistryActivationReceipt:
    return RegistryActivationReceipt(
        schema_version="cmf.registry_activation_receipt.v1",
        registry_activation_receipt_id=uuid4(),
        registry_entry_id=registry_entry.registry_entry_id,
        migration_ledger_entry_id=registry_entry.migration_ledger_entry_id,
        decision_code=decision_code,
        evidence_refs=evidence_refs,
        reviewer_actor_id=registry_entry.reviewer_actor_id,
        written_at=utc_now(),
    )
