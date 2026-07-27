"""Legacy migration ledger contracts for TS-CMF-013."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class LegacyAssetStatus(str, Enum):
    proposed = "proposed"
    mapped = "mapped"
    approved = "approved"
    blocked = "blocked"
    deprecated = "deprecated"
    needs_hash_review = "needs_hash_review"


class LegacyDisposition(str, Enum):
    doctrine = "doctrine"
    registry = "registry"
    fixture = "fixture"
    eval_target = "eval_target"
    reference_implementation = "reference_implementation"
    worker_asset = "worker_asset"
    deprecated_runtime = "deprecated_runtime"


class MigrationTargetMap(BaseModel):
    schema_version: Literal["cmf.migration_target_map.v1"]
    target_python_package: str | None = None
    pydantic_contract_target: str | None = None
    dspy_program_target: str | None = None
    typescript_leaf_target: str | None = None
    fixture_target: str | None = None
    eval_target: str | None = None
    reviewer_actor_id: UUID | None = None


class LegacyAssetInventoryItem(BaseModel):
    schema_version: Literal["cmf.legacy_asset_inventory_item.v1"]
    legacy_asset_inventory_item_id: UUID
    source_path: str = Field(min_length=1)
    legacy_type: str = Field(min_length=1)
    registry_family: str | None = None
    canonicality_confidence: float = Field(ge=0, le=1)
    source_owner: str = Field(min_length=1)
    runtime_language: str | None = None
    valuable_mechanics: list[str] = Field(min_length=1)
    known_defects: list[str] = Field(default_factory=list)
    content_hash: str = Field(min_length=1)
    created_at: datetime


class HashReviewFlag(BaseModel):
    schema_version: Literal["cmf.hash_review_flag.v1"]
    hash_review_flag_id: UUID
    migration_ledger_entry_id: UUID
    source_path: str
    prior_content_hash: str
    observed_content_hash: str
    decision_code: Literal["LEGACY_HASH_REVIEW_REQUIRED"]
    created_at: datetime


class MigrationLedgerEntry(BaseModel):
    schema_version: Literal["cmf.migration_ledger_entry.v1"]
    migration_ledger_entry_id: UUID
    source_path: str
    legacy_type: str
    registry_family: str | None = None
    canonicality_confidence: float = Field(ge=0, le=1)
    source_owner: str
    runtime_language: str | None = None
    valuable_mechanics: list[str] = Field(min_length=1)
    known_defects: list[str] = Field(default_factory=list)
    content_hash: str
    disposition: LegacyDisposition
    target_map: MigrationTargetMap
    status: LegacyAssetStatus
    block_reason: str | None = None
    replacement_target: str | None = None
    created_at: datetime
    updated_at: datetime


class MigrationReceipt(BaseModel):
    schema_version: Literal["cmf.migration_receipt.v1"]
    migration_receipt_id: UUID
    migration_ledger_entry_id: UUID
    source_path: str
    action: str
    decision_code: str
    actor_id: UUID | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime


class BlockedReferenceResolution(BaseModel):
    schema_version: Literal["cmf.blocked_reference_resolution.v1"]
    source_path: str
    allowed: bool
    decision_code: str
    reason: str | None = None
    replacement_target: str | None = None
    migration_ledger_entry_id: UUID | None = None


def new_target_map(
    *,
    target_python_package: str | None = None,
    pydantic_contract_target: str | None = None,
    dspy_program_target: str | None = None,
    typescript_leaf_target: str | None = None,
    fixture_target: str | None = None,
    eval_target: str | None = None,
    reviewer_actor_id: UUID | None = None,
) -> MigrationTargetMap:
    return MigrationTargetMap(
        schema_version="cmf.migration_target_map.v1",
        target_python_package=target_python_package,
        pydantic_contract_target=pydantic_contract_target,
        dspy_program_target=dspy_program_target,
        typescript_leaf_target=typescript_leaf_target,
        fixture_target=fixture_target,
        eval_target=eval_target,
        reviewer_actor_id=reviewer_actor_id,
    )


def new_migration_receipt(
    *,
    migration_ledger_entry_id: UUID,
    source_path: str,
    action: str,
    decision_code: str,
    actor_id: UUID | None,
    evidence_refs: list[str],
) -> MigrationReceipt:
    return MigrationReceipt(
        schema_version="cmf.migration_receipt.v1",
        migration_receipt_id=uuid4(),
        migration_ledger_entry_id=migration_ledger_entry_id,
        source_path=source_path,
        action=action,
        decision_code=decision_code,
        actor_id=actor_id,
        evidence_refs=evidence_refs,
        written_at=utc_now(),
    )
