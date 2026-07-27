"""Brownfield V2.1 behavior inventory and mapping for OD-AM-005 / ST-12.01."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from typing import Any


def sha256_of(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


class BrownfieldMappingError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class ProvenBehaviorStatus(str, Enum):
    OBSERVED_AND_PROVEN = "OBSERVED_AND_PROVEN"
    OBSERVED_NOT_PROVEN = "OBSERVED_NOT_PROVEN"
    DOCUMENTED_NOT_OBSERVED = "DOCUMENTED_NOT_OBSERVED"
    SYNTHETIC_REFERENCE = "SYNTHETIC_REFERENCE"
    MISSING = "MISSING"
    EXCLUDED = "EXCLUDED"
    INCOMPATIBLE = "INCOMPATIBLE"


@dataclass(frozen=True)
class BrownfieldArtifactRecord:
    reference_artifact_identity: str
    source_location: str
    artifact_type: str
    version: str
    source_hash: str
    observed_behavior: tuple[str, ...]
    proven_behavior_status: ProvenBehaviorStatus
    evidence_class: str
    builder_capability: str
    mapped_story: str
    mapped_obligation: str
    compatibility: str
    gap: str
    conflict: str
    provenance: str
    limitations: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.proven_behavior_status is ProvenBehaviorStatus.OBSERVED_AND_PROVEN and not self.observed_behavior:
            raise BrownfieldMappingError("PROVEN_BEHAVIOR_REQUIRES_OBSERVATION", "proven behavior requires observed behavior")
        if self.proven_behavior_status is ProvenBehaviorStatus.MISSING and self.source_hash != "MISSING":
            raise BrownfieldMappingError("MISSING_ARTIFACT_CANNOT_HAVE_HASH", "missing artifact cannot carry a source hash")
        if self.proven_behavior_status is ProvenBehaviorStatus.SYNTHETIC_REFERENCE and self.evidence_class != "REPOSITORY_OWNED_FIXTURE":
            raise BrownfieldMappingError("SYNTHETIC_REFERENCE_MISLABELED", "synthetic references must be fixture-labeled")
        if self.proven_behavior_status is ProvenBehaviorStatus.EXCLUDED and not self.limitations:
            raise BrownfieldMappingError("EXCLUDED_REQUIRES_LIMITATION", "excluded artifacts require limitations")

    @property
    def mapping_identity(self) -> str:
        return sha256_of(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {
            "reference_artifact_identity": self.reference_artifact_identity,
            "source_location": self.source_location,
            "artifact_type": self.artifact_type,
            "version": self.version,
            "source_hash": self.source_hash,
            "observed_behavior": list(self.observed_behavior),
            "proven_behavior_status": self.proven_behavior_status.value,
            "evidence_class": self.evidence_class,
            "builder_capability": self.builder_capability,
            "mapped_story": self.mapped_story,
            "mapped_obligation": self.mapped_obligation,
            "compatibility": self.compatibility,
            "gap": self.gap,
            "conflict": self.conflict,
            "provenance": self.provenance,
            "limitations": list(self.limitations),
        }


def build_brownfield_inventory(records: tuple[BrownfieldArtifactRecord, ...]) -> dict[str, Any]:
    identities = [record.reference_artifact_identity for record in records]
    if len(identities) != len(set(identities)):
        raise BrownfieldMappingError("DUPLICATE_REFERENCE_ARTIFACT", "reference artifact identities must be unique")
    ordered = sorted(records, key=lambda item: item.reference_artifact_identity)
    return {
        "mode": "BROWNFIELD_MAPPING_DEVELOPMENT",
        "records": [record.as_dict() for record in ordered],
        "reference_evidence": "PENDING_OR_PARTIAL",
        "production_migration_authority": False,
        "inventory_identity": sha256_of([record.mapping_identity for record in ordered]),
    }
