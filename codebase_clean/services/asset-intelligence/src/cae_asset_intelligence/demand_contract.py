"""
demand_contract.py
------------------
Provider-neutral production asset demand and resolution contracts (CAE-M061).

The contract carries declared physical-media constraints and preserves the
upstream semantic obligation as data. Resolution may validate a candidate
against those declarations but does not create or reinterpret meaning.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Iterable, Mapping, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .domain import AssetAnnotation, AssetCatalog, MediaType, RightsStatus


class AssetResolutionState(str, Enum):
    PROGRAM_NEEDS_ASSET = "PROGRAM_NEEDS_ASSET"
    DEMAND_EMITTED = "DEMAND_EMITTED"
    RESOLUTION_PENDING = "RESOLUTION_PENDING"
    SATISFIED = "SATISFIED"
    BLOCKED = "BLOCKED"


class AssetResolutionError(ValueError):
    """Base error for demand/resolution contract validation."""


class AssetDemandValidationError(AssetResolutionError):
    """Raised when a demand violates its declared contract."""


class AssetResolutionBlockedError(AssetResolutionError):
    """Raised when a candidate cannot satisfy a declared demand."""


class AssetRef(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    object_id: str = Field(..., min_length=1)
    version: str = Field(..., min_length=1)
    sha256: str = Field(..., min_length=64, max_length=64)


class AssetDurationConstraint(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    minimum_seconds: float = Field(..., gt=0.0)
    maximum_seconds: float = Field(..., gt=0.0)
    preferred_seconds: Optional[float] = Field(None, gt=0.0)

    @model_validator(mode="after")
    def validate_range(self) -> "AssetDurationConstraint":
        if self.minimum_seconds > self.maximum_seconds:
            raise ValueError("minimum_seconds cannot exceed maximum_seconds")
        if self.preferred_seconds is not None and not (
            self.minimum_seconds <= self.preferred_seconds <= self.maximum_seconds
        ):
            raise ValueError("preferred_seconds must be inside the duration range")
        return self


class AssetRightsConstraint(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    acceptable_statuses: tuple[str, ...] = Field(..., min_length=1)
    allowed_territories: tuple[str, ...] = Field(default=("GLOBAL",), min_length=1)
    license_required: bool = False

    @field_validator("acceptable_statuses", "allowed_territories")
    @classmethod
    def unique_nonempty(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        if any(not value.strip() for value in values):
            raise ValueError("rights constraint values must be non-empty")
        return tuple(dict.fromkeys(value.strip() for value in values))


class AssetSemanticObligation(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    scene_role: str = Field(..., min_length=3)
    semantic_role: str = Field(..., min_length=3)
    obligation: str = Field(..., min_length=10)
    evidence_ref: str = Field(..., min_length=1)
    evidence_sha256: str = Field(..., min_length=64, max_length=64)
    wrong_reading_locks: tuple[str, ...] = ()


class PhysicalMediaRequirement(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    media_type: MediaType
    source_type: str = Field(..., min_length=3)
    insert_role: str = Field(..., min_length=3)
    duration: AssetDurationConstraint


class ProductionAssetDemand(BaseModel):
    """One exact physical-media request derived from an existing Program."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    demand_id: str = Field(..., min_length=1)
    candidate_id: str = Field(..., min_length=1)
    workspace_id: str = Field(..., min_length=1)
    scene_index: int = Field(..., ge=1)
    segment_id: str = Field(..., min_length=1)
    program_ref: AssetRef
    semantic_obligation: AssetSemanticObligation
    media: PhysicalMediaRequirement
    rights: AssetRightsConstraint
    provenance_ref: AssetRef


class AssetResolutionOutcome(BaseModel):
    """Declarative resolution result; it never changes the demand's semantics."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    demand_id: str = Field(..., min_length=1)
    state: AssetResolutionState
    asset_ref: Optional[AssetRef] = None
    matched_duration_seconds: Optional[float] = Field(None, gt=0.0)
    resolved_rights_status: Optional[str] = None
    reason_code: Optional[str] = None
    reason_detail: Optional[str] = None

    @model_validator(mode="after")
    def validate_state(self) -> "AssetResolutionOutcome":
        if self.state == AssetResolutionState.SATISFIED and self.asset_ref is None:
            raise ValueError("SATISFIED resolution requires asset_ref")
        if self.state == AssetResolutionState.BLOCKED and not self.reason_code:
            raise ValueError("BLOCKED resolution requires reason_code")
        if self.state in {
            AssetResolutionState.DEMAND_EMITTED,
            AssetResolutionState.RESOLUTION_PENDING,
        } and self.asset_ref is not None:
            raise ValueError(f"{self.state.value} cannot carry an asset_ref")
        return self


class AssetDemandResolutionContract(BaseModel):
    """Typed boundary between Program semantics and provider-neutral asset resolution."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    contract_version: str = "1.0.0"
    contract_id: str = Field(..., min_length=1)
    state: AssetResolutionState
    program_ref: AssetRef
    candidate_id: str = Field(..., min_length=1)
    workspace_id: str = Field(..., min_length=1)
    demands: tuple[ProductionAssetDemand, ...] = Field(..., min_length=1)
    resolutions: tuple[AssetResolutionOutcome, ...] = ()
    emitted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Mapping[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_contract(self) -> "AssetDemandResolutionContract":
        if any(d.workspace_id != self.workspace_id for d in self.demands):
            raise AssetDemandValidationError("All demands must remain in the contract workspace")
        if any(d.candidate_id != self.candidate_id for d in self.demands):
            raise AssetDemandValidationError("All demands must remain in the contract candidate")
        if any(d.program_ref != self.program_ref for d in self.demands):
            raise AssetDemandValidationError("All demands must retain the source program reference")
        demand_ids = {d.demand_id for d in self.demands}
        resolution_ids = [r.demand_id for r in self.resolutions]
        if len(resolution_ids) != len(set(resolution_ids)):
            raise AssetDemandValidationError("Resolution demand IDs must be unique")
        if not set(resolution_ids).issubset(demand_ids):
            raise AssetDemandValidationError("Resolution references an unknown demand")
        return self

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def _canonical_sha256(payload: Mapping[str, Any]) -> str:
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def _program_ref(program: Mapping[str, Any]) -> AssetRef:
    version = str(program.get("program_version") or "1.0.0")
    program_id = str(program["program_id"])
    return AssetRef(
        object_id=program_id,
        version=version,
        sha256=_canonical_sha256(dict(program)),
    )


def _as_mapping(program: Any) -> Mapping[str, Any]:
    if isinstance(program, Mapping):
        return program
    if hasattr(program, "model_dump"):
        return program.model_dump(mode="python")
    raise TypeError("program must be a mapping or a Pydantic model with model_dump()")


def compile_production_asset_demand(
    program: Any,
    *,
    demand_prefix: str = "AD",
) -> AssetDemandResolutionContract:
    """Translate an existing SemanticProgram into declared physical-media demands.

    The translator only copies already-declared requirements. It does not infer
    semantic meaning, select assets, call retrieval, or inspect media bytes.
    """

    raw = _as_mapping(program)
    program_ref = _program_ref(raw)
    workspace_id = str(raw["workspace_id"])
    candidate_id = str(raw["candidate_id"])
    scenes = raw.get("scenes") or []
    demands: list[ProductionAssetDemand] = []

    for scene in scenes:
        scene_index = int(scene["scene_index"])
        segment_id = str(scene["segment_id"])
        scene_role = getattr(scene["scene_role"], "value", str(scene["scene_role"]))
        scene_sha = str(scene["text_sha256"])
        for demand_index, raw_demand in enumerate(scene.get("asset_demands") or [], start=1):
            demand = raw_demand if isinstance(raw_demand, Mapping) else raw_demand.model_dump(mode="python")
            if str(demand["evidence_ref"]) != segment_id:
                raise AssetDemandValidationError(
                    f"Demand {demand['demand_key']} evidence_ref must match scene segment_id"
                )
            if str(demand["evidence_sha256"]) != scene_sha:
                raise AssetDemandValidationError(
                    f"Demand {demand['demand_key']} evidence_sha256 must match scene text_sha256"
                )

            demand_id = f"{demand_prefix}-{program_ref.object_id}-{scene_index:03d}-{demand_index:02d}"
            source_type = str(demand["source_type"])
            media_type = MediaType(str(demand["media_type"]))
            physical = PhysicalMediaRequirement(
                media_type=media_type,
                source_type=source_type,
                insert_role=str(demand["insert_role"]),
                duration=AssetDurationConstraint(
                    minimum_seconds=float(demand["min_duration_seconds"]),
                    maximum_seconds=float(demand["max_duration_seconds"]),
                    preferred_seconds=(
                        float(demand["preferred_duration_seconds"])
                        if demand.get("preferred_duration_seconds") is not None
                        else None
                    ),
                ),
            )
            semantic = AssetSemanticObligation(
                scene_role=scene_role,
                semantic_role=str(demand["semantic_role"]),
                obligation=str(demand["semantic_obligation"]),
                evidence_ref=segment_id,
                evidence_sha256=scene_sha,
                wrong_reading_locks=tuple(str(lock) for lock in scene.get("wrong_reading_locks", [])),
            )
            rights = AssetRightsConstraint(
                acceptable_statuses=tuple(str(status) for status in demand["rights_statuses"]),
                allowed_territories=tuple(str(t) for t in demand.get("allowed_territories", ["GLOBAL"])),
                license_required=bool(demand.get("license_required", False)),
            )
            provenance = AssetRef(
                object_id=segment_id,
                version="1.0.0",
                sha256=scene_sha,
            )
            demands.append(
                ProductionAssetDemand(
                    demand_id=demand_id,
                    candidate_id=candidate_id,
                    workspace_id=workspace_id,
                    scene_index=scene_index,
                    segment_id=segment_id,
                    program_ref=program_ref,
                    semantic_obligation=semantic,
                    media=physical,
                    rights=rights,
                    provenance_ref=provenance,
                )
            )

    if not demands:
        raise AssetDemandValidationError("SemanticProgram does not declare any asset demands")

    payload = {
        "program_ref": program_ref.model_dump(mode="json"),
        "candidate_id": candidate_id,
        "workspace_id": workspace_id,
        "demands": [d.model_dump(mode="json") for d in demands],
    }
    contract_id = f"ADR-{_canonical_sha256(payload)[:20]}"
    return AssetDemandResolutionContract(
        contract_id=contract_id,
        state=AssetResolutionState.DEMAND_EMITTED,
        program_ref=program_ref,
        candidate_id=candidate_id,
        workspace_id=workspace_id,
        demands=tuple(demands),
    )


class AssetDemandResolver:
    """Validates AssetAnnotation candidates against declared demand constraints."""

    @staticmethod
    def _rights_match(annotation: AssetAnnotation, demand: ProductionAssetDemand) -> bool:
        status = annotation.rights.status.value
        allowed = set(demand.rights.acceptable_statuses)
        if status not in allowed:
            return False
        if demand.rights.license_required and not (
            annotation.rights.license_id or annotation.rights.proof_url
        ):
            return False
        requested_territories = set(demand.rights.allowed_territories)
        actual_territories = set(annotation.rights.allowed_territories)
        return "GLOBAL" in requested_territories or bool(requested_territories & actual_territories)

    @staticmethod
    def _duration_match(annotation: AssetAnnotation, demand: ProductionAssetDemand) -> bool:
        return (
            demand.media.duration.minimum_seconds
            <= annotation.duration
            <= demand.media.duration.maximum_seconds
        )

    @staticmethod
    def _semantic_match(annotation: AssetAnnotation, demand: ProductionAssetDemand) -> bool:
        # Equality is validation of the Program-declared obligation, not semantic inference.
        return (
            annotation.semantic_role == demand.semantic_obligation.semantic_role
            and annotation.insert_role.value == demand.media.insert_role
        )

    @classmethod
    def resolve_candidate(
        cls,
        *,
        demand_contract: AssetDemandResolutionContract,
        demand_id: str,
        annotation: AssetAnnotation,
    ) -> AssetResolutionOutcome:
        demand = next((item for item in demand_contract.demands if item.demand_id == demand_id), None)
        if demand is None:
            raise AssetResolutionBlockedError(f"Unknown demand_id '{demand_id}'")
        if annotation.workspace_id != demand.workspace_id:
            return AssetResolutionOutcome(
                demand_id=demand_id,
                state=AssetResolutionState.BLOCKED,
                reason_code="WORKSPACE_SCOPE_VIOLATION",
                reason_detail="Asset workspace does not match demand workspace",
            )
        if annotation.media_type != demand.media.media_type:
            return AssetResolutionOutcome(
                demand_id=demand_id,
                state=AssetResolutionState.BLOCKED,
                reason_code="MEDIA_TYPE_MISMATCH",
                reason_detail="Asset media_type does not match the declared physical-media requirement",
            )
        if annotation.source_type.value != demand.media.source_type:
            return AssetResolutionOutcome(
                demand_id=demand_id,
                state=AssetResolutionState.BLOCKED,
                reason_code="SOURCE_TYPE_MISMATCH",
                reason_detail="Asset source_type does not match the declared source requirement",
            )
        if not cls._duration_match(annotation, demand):
            return AssetResolutionOutcome(
                demand_id=demand_id,
                state=AssetResolutionState.BLOCKED,
                reason_code="DURATION_CONSTRAINT_VIOLATION",
                reason_detail="Asset duration is outside the declared demand range",
            )
        if not cls._semantic_match(annotation, demand):
            return AssetResolutionOutcome(
                demand_id=demand_id,
                state=AssetResolutionState.BLOCKED,
                reason_code="SEMANTIC_OBLIGATION_MISMATCH",
                reason_detail="Asset does not preserve the exact Program-declared role/obligation",
            )
        if not cls._rights_match(annotation, demand):
            return AssetResolutionOutcome(
                demand_id=demand_id,
                state=AssetResolutionState.BLOCKED,
                reason_code="RIGHTS_CONSTRAINT_VIOLATION",
                reason_detail="Asset rights do not satisfy the declared demand",
            )
        asset_ref = AssetRef(
            object_id=annotation.asset_id,
            version="1.0.0",
            sha256=annotation.source_sha256,
        )
        return AssetResolutionOutcome(
            demand_id=demand_id,
            state=AssetResolutionState.SATISFIED,
            asset_ref=asset_ref,
            matched_duration_seconds=annotation.duration,
            resolved_rights_status=annotation.rights.status.value,
        )

    @classmethod
    def resolve_catalog(
        cls,
        *,
        demand_contract: AssetDemandResolutionContract,
        catalog: AssetCatalog,
    ) -> AssetDemandResolutionContract:
        if catalog.workspace_id != demand_contract.workspace_id or catalog.candidate_id != demand_contract.candidate_id:
            raise AssetResolutionBlockedError(
                "Asset catalog scope does not match the demand contract"
            )
        outcomes: list[AssetResolutionOutcome] = []
        for demand in demand_contract.demands:
            candidate = next(
                (
                    asset
                    for asset in catalog.assets
                    if cls._duration_match(asset, demand)
                    and asset.media_type == demand.media.media_type
                    and asset.source_type.value == demand.media.source_type
                    and cls._semantic_match(asset, demand)
                    and cls._rights_match(asset, demand)
                ),
                None,
            )
            if candidate is None:
                outcomes.append(
                    AssetResolutionOutcome(
                        demand_id=demand.demand_id,
                        state=AssetResolutionState.BLOCKED,
                        reason_code="NO_MATCHING_ASSET",
                        reason_detail="Catalog contains no asset satisfying every declared constraint",
                    )
                )
            else:
                outcomes.append(
                    cls.resolve_candidate(
                        demand_contract=demand_contract,
                        demand_id=demand.demand_id,
                        annotation=candidate,
                    )
                )
        final_state = (
            AssetResolutionState.SATISFIED
            if all(item.state == AssetResolutionState.SATISFIED for item in outcomes)
            else AssetResolutionState.BLOCKED
        )
        return demand_contract.model_copy(
            update={"state": final_state, "resolutions": tuple(outcomes)}
        )
