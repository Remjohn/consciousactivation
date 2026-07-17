"""Dual compile and governed migration framework for OD-AM-005 / ST-12.02."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from typing import Any


def sha256_of(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


class MigrationError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class CompatibilityResult(str, Enum):
    COMPATIBLE = "COMPATIBLE"
    COMPATIBLE_WITH_ACCEPTED_DIFFERENCES = "COMPATIBLE_WITH_ACCEPTED_DIFFERENCES"
    INCOMPATIBLE = "INCOMPATIBLE"
    MISSING_SOURCE_EVIDENCE = "MISSING_SOURCE_EVIDENCE"


@dataclass(frozen=True)
class DualCompileMigration:
    source_artifact: str
    source_version: str
    source_hash: str
    destination_schema: str
    source_compilation_hash: str
    destination_compilation_hash: str
    semantic_differences: tuple[str, ...]
    structural_differences: tuple[str, ...]
    authority_differences: tuple[str, ...]
    evidence_differences: tuple[str, ...]
    accepted_differences: tuple[str, ...]
    prohibited_differences: tuple[str, ...]
    compatibility_result: CompatibilityResult
    rollback_identity: str
    regression_receipt: str
    production_cutover: bool = False

    def __post_init__(self) -> None:
        if self.production_cutover:
            raise MigrationError("PRODUCTION_CUTOVER_PROHIBITED", "bounded migration cannot perform production cutover")
        if self.source_hash == "MISSING" and self.compatibility_result is not CompatibilityResult.MISSING_SOURCE_EVIDENCE:
            raise MigrationError("MISSING_SOURCE_EVIDENCE_MUST_REMAIN_MISSING", "missing evidence cannot be treated as compatible")
        if set(self.prohibited_differences) & set(self.accepted_differences):
            raise MigrationError("PROHIBITED_DIFFERENCE_ACCEPTED", "prohibited differences cannot be accepted")
        if "semantic_flattening" in self.semantic_differences and "semantic_flattening" in self.accepted_differences:
            raise MigrationError("SEMANTIC_FLATTENING_REJECTED", "semantic flattening cannot be accepted")
        if self.authority_differences and self.compatibility_result is CompatibilityResult.COMPATIBLE:
            raise MigrationError("AUTHORITY_DIFFERENCE_NOT_COMPATIBLE", "authority differences prevent full compatibility")

    @property
    def migration_identity(self) -> str:
        return sha256_of(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {
            "mode": "DUAL_COMPILE_MIGRATION_DEVELOPMENT",
            "source_artifact": self.source_artifact,
            "source_version": self.source_version,
            "source_hash": self.source_hash,
            "destination_schema": self.destination_schema,
            "source_compilation_hash": self.source_compilation_hash,
            "destination_compilation_hash": self.destination_compilation_hash,
            "semantic_differences": list(self.semantic_differences),
            "structural_differences": list(self.structural_differences),
            "authority_differences": list(self.authority_differences),
            "evidence_differences": list(self.evidence_differences),
            "accepted_differences": list(self.accepted_differences),
            "prohibited_differences": list(self.prohibited_differences),
            "compatibility_result": self.compatibility_result.value,
            "rollback_identity": self.rollback_identity,
            "regression_receipt": self.regression_receipt,
            "production_cutover": False,
        }


class MigrationLedger:
    def __init__(self) -> None:
        self._records: dict[str, DualCompileMigration] = {}

    def commit(self, migration: DualCompileMigration) -> DualCompileMigration:
        existing = self._records.get(migration.migration_identity)
        if existing is not None:
            return existing
        self._records[migration.migration_identity] = migration
        return migration

    def rollback(self, migration_identity: str) -> str:
        migration = self._records[migration_identity]
        return migration.rollback_identity
