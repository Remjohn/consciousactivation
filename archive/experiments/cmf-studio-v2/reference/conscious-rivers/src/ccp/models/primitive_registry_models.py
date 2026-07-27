"""
CCP FR-ERA3-06 - Primitive Registry Query Service models.

Typed contracts for the primitive registry cache, conflict resolution, and API
surface. These models are intentionally permissive about extra YAML fields so
the registry can preserve forward-compatible primitive metadata.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


FAMILY_SORT_ORDER: dict[str, int] = {
    "TRG": 0,
    "FRC": 1,
    "TRS": 2,
    "FBK": 3,
    "PRG": 4,
    "SOC": 5,
    "SAF": 6,
    "PER": 7,
}

EXPERIENCE_PLANE = "experience_plane"
MEANING_PLANE = "meaning_plane"

CACHE_KEY_PREFIX_EXP = "prim:exp"
CACHE_KEY_PREFIX_MNG = "prim:mng"

REGISTRY_AGENT_NAME = "Athena"

PRIMITIVE_QUERY_AUDIT_SQL = """
CREATE TABLE IF NOT EXISTS primitive_query_audit (
    audit_id        TEXT PRIMARY KEY,
    query_type      TEXT NOT NULL,
    requested_ids   JSONB NOT NULL,
    resolved_ids    JSONB NOT NULL,
    conflicts_found JSONB NOT NULL DEFAULT '[]',
    resolution_log  JSONB NOT NULL DEFAULT '[]',
    latency_ms      REAL NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_primitive_query_audit_type
    ON primitive_query_audit(query_type);
CREATE INDEX IF NOT EXISTS idx_primitive_query_audit_created_at
    ON primitive_query_audit(created_at DESC);
"""


class PrimitivePlane(str, Enum):
    EXPERIENCE = EXPERIENCE_PLANE
    MEANING = MEANING_PLANE


class ConflictPrecedenceReason(str, Enum):
    SCORING_FIT = "higher_scoring_stage_fit"
    PRIMARY_INTENT = "primary_intent_priority"
    FAMILY_ORDER = "family_sort_order_tiebreak"


class PrimitiveRegistryBaseModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class ExperiencePrimitiveRecord(PrimitiveRegistryBaseModel):
    experience_primitive_id: str = Field(pattern=r"^EXP-[A-Z]{3}-\d{3}$")
    canonical_name: str = Field(min_length=1)
    aliases: list[str] = Field(default_factory=list)
    experience_family: str = Field(min_length=1)
    mechanic_role: str = Field(default="")
    moment_role: str = Field(default="")
    implementation_role: str = Field(default="")
    summary: str = Field(default="")
    core_move: str = Field(default="")
    why_it_works: str = Field(default="")
    synergizes_with: list[str] = Field(default_factory=list)
    conflicts_with: list[str] = Field(default_factory=list)
    experience_stage_fit: dict[str, float] = Field(default_factory=dict)
    surface_fit: dict[str, float] = Field(default_factory=dict)
    crosswalk_id: str = Field(default="")
    crosswalk_note: str = Field(default="")

    @field_validator("conflicts_with", "synergizes_with", mode="before")
    @classmethod
    def normalize_id_list(cls, value: Any) -> list[str]:
        if value in (None, "", "None"):
            return []
        if isinstance(value, str):
            value = [value]
        cleaned: list[str] = []
        for item in value:
            if not item:
                continue
            item_str = str(item).strip()
            if not item_str or item_str.lower() == "none":
                continue
            cleaned.append(item_str)
        return cleaned

    @field_validator("crosswalk_id", "crosswalk_note", mode="before")
    @classmethod
    def normalize_optional_strings(cls, value: Any) -> str:
        if value is None:
            return ""
        return str(value)


class MeaningPrimitiveRecord(PrimitiveRegistryBaseModel):
    primitive_id: str = Field(pattern=r"^PRM-[A-Z]{3}-\d{3}$")
    canonical_name: str = Field(min_length=1)
    aliases: list[str] = Field(default_factory=list)
    family: str = Field(min_length=1)
    implementation_role: str = Field(default="")
    summary: str = Field(default="")
    core_move: str = Field(default="")
    why_it_works: str = Field(default="")
    synergizes_with: list[str] = Field(default_factory=list)
    conflicts_with: list[str] = Field(default_factory=list)
    coalition_partners_synergistic: list[str] = Field(default_factory=list)
    coalition_partners_antagonistic: list[str] = Field(default_factory=list)
    phase_fit: dict[str, float] = Field(default_factory=dict)
    surface_fit: dict[str, float] = Field(default_factory=dict)
    goal_bias: dict[str, float] = Field(default_factory=dict)
    crosswalk_id: str = Field(default="")
    crosswalk_note: str = Field(default="")

    @field_validator(
        "conflicts_with",
        "synergizes_with",
        "coalition_partners_synergistic",
        "coalition_partners_antagonistic",
        mode="before",
    )
    @classmethod
    def normalize_relationship_lists(cls, value: Any) -> list[str]:
        if value in (None, "", "None"):
            return []
        if isinstance(value, str):
            value = [value]
        cleaned: list[str] = []
        for item in value:
            if not item:
                continue
            item_str = str(item).strip()
            if not item_str or item_str.lower() == "none":
                continue
            cleaned.append(item_str)
        return cleaned

    @field_validator("crosswalk_id", "crosswalk_note", mode="before")
    @classmethod
    def normalize_optional_strings(cls, value: Any) -> str:
        if value is None:
            return ""
        return str(value)


PrimitiveRecord = ExperiencePrimitiveRecord | MeaningPrimitiveRecord


class PrimitiveQueryRequest(BaseModel):
    requested_ids: list[str] = Field(min_length=1)
    primary_intent_ids: list[str] = Field(default_factory=list)
    context: str = Field(default="general")
    include_conflicts_log: bool = Field(default=True)

    @field_validator("requested_ids", "primary_intent_ids", mode="before")
    @classmethod
    def normalize_requested_ids(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            value = [value]
        normalized: list[str] = []
        seen: set[str] = set()
        for item in value:
            item_str = str(item).strip()
            if not item_str or item_str in seen:
                continue
            seen.add(item_str)
            normalized.append(item_str)
        return normalized


class ConflictEntry(BaseModel):
    primitive_a: str
    primitive_b: str
    winner: str
    loser: str
    reason: ConflictPrecedenceReason


class ConflictResolutionResult(BaseModel):
    clean_ids: list[str]
    removed_ids: list[str] = Field(default_factory=list)
    conflicts: list[ConflictEntry] = Field(default_factory=list)
    resolution_log: list[str] = Field(default_factory=list)
    resolution_applied: bool = Field(default=False)


class PrimitiveQueryResponse(BaseModel):
    query_id: str
    requested_ids: list[str]
    resolved_primitives: list[PrimitiveRecord]
    conflict_resolution: ConflictResolutionResult
    cache_hit: bool = Field(default=True)
    latency_ms: float = Field(ge=0.0)


class PrimitiveFamilyQueryResponse(BaseModel):
    family_code: str
    experience_records: list[ExperiencePrimitiveRecord] = Field(default_factory=list)
    meaning_records: list[MeaningPrimitiveRecord] = Field(default_factory=list)


class PrimitivePlaneQueryResponse(BaseModel):
    plane: PrimitivePlane
    primitives: list[PrimitiveRecord] = Field(default_factory=list)


class PrimitiveInvalidationRequest(BaseModel):
    primitive_id: str = Field(min_length=1)


class PrimitiveInvalidationResponse(BaseModel):
    primitive_id: str
    deleted_keys: int = Field(ge=0, default=0)
    broadcast_sent: bool = Field(default=False)
    redis_connected: bool = Field(default=False)


class CacheHealthStatus(BaseModel):
    experience_count: int = Field(ge=0)
    meaning_count: int = Field(ge=0)
    total_cached: int = Field(ge=0)
    redis_connected: bool
    last_warm_at: str
    stale_keys: int = Field(default=0, ge=0)
    yaml_reads: int = Field(default=0, ge=0)
    local_mirror_size: int = Field(default=0, ge=0)


class CacheWarmStats(BaseModel):
    experience_count: int = Field(default=0, ge=0)
    meaning_count: int = Field(default=0, ge=0)
    stale_keys: int = Field(default=0, ge=0)
    yaml_reads: int = Field(default=0, ge=0)
    warmed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def total_cached(self) -> int:
        return self.experience_count + self.meaning_count


class PrimitiveReloadResult(BaseModel):
    primitive_id: str
    found: bool
    reloaded: bool
    cache_hit: bool
    plane: PrimitivePlane | None = None


class PrimitiveLookupResult(BaseModel):
    primitive_id: str
    record: PrimitiveRecord | None = None
    plane: PrimitivePlane | None = None
    cache_hit: bool = Field(default=True)
    reloaded_from_disk: bool = Field(default=False)

    @model_validator(mode="after")
    def validate_plane_consistency(self) -> "PrimitiveLookupResult":
        if self.record is None:
            return self
        if isinstance(self.record, ExperiencePrimitiveRecord):
            self.plane = PrimitivePlane.EXPERIENCE
        elif isinstance(self.record, MeaningPrimitiveRecord):
            self.plane = PrimitivePlane.MEANING
        return self
