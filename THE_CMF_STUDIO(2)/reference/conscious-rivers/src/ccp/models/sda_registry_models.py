"""
CCP FR-ERA3-20 - SDA Ontology and Registry models.

Canonical typed contracts for the Semantic Discernment Architecture
ontology, structural grammar, crosswalk bundles, manifest health, and
audit outputs.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


SDA_ROOT_DIRNAME = "sda"

INV_PREFIX = "SDA-INV-"
RPG_PREFIX = "SDA-RPG-"
ARG_PREFIX = "SDA-ARG-"
SCG_PREFIX = "SDA-SCG-"
XW_PI_PREFIX = "SDA-XW-PI-"
XW_AG_PREFIX = "SDA-XW-AG-"

PROHIBITED_CANONICAL_CLASSES: set[str] = {
    "content_species",
    "edge_product",
    "recursive_pattern",
    "emergent_contextual_invariant",
    "feedback_loop",
    "directional_integrity_policy",
    "hard_negative",
    "mutation_stress_suite",
}

RETAINED_PRD02_CONTENT_ARCHETYPES: frozenset[str] = frozenset(
    {
        "Achievement Story",
        "Transformation Story",
        "Witness Story",
        "Backstory Reveal",
        "Confessional Turn",
        "Case Study Breakdown",
        "Comparison Breakdown",
        "Before vs After Contrast",
        "Wrong Way / Right Way Contrast",
        "Myth Debunk",
        "Scam Exposure",
        "Fear / Anxiety Listicle",
        "Shocking Listicle",
        "Stepwise Teaching Listicle",
        "Mistakes Listicle",
        "Tier List Authority",
        "Ranked Take / Ranked Claims",
        "Core Educator / Explainer",
        "Challenger / Frame Breaker",
        "Authority Proof Stack",
        "Observational Humor",
        "Meme Observation",
        "Tribal Absurdity",
        "Benign Violation Reframe",
        "Pain-to-Relief Contrast",
        "Status Satire",
        "Industry Hypocrisy Exposure",
        "Solo Reaction",
        "Vote Then React",
        "Debate with Jury Mode",
        "Supervisor Pairing",
        "Redemption Round",
        "Reaction Duel",
        "Audience Mirror Quiz",
        "Blind Rank Reveal / Blind Rank Defense",
        "Alphabet Challenge",
        "Last One Standing",
        "Authority Quiz / Pressure Ladder",
        "Tierlist Authority",
        "Compilation",
    }
)

SDA_REGISTRY_AUDIT_SQL = """
CREATE TABLE IF NOT EXISTS sda_registry_audit (
    audit_id TEXT PRIMARY KEY,
    stage_name TEXT NOT NULL,
    artifact_path TEXT NOT NULL,
    artifact_id TEXT,
    registry_kind TEXT,
    status TEXT NOT NULL,
    error_code TEXT,
    message TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_sda_registry_audit_stage
    ON sda_registry_audit(stage_name);
CREATE INDEX IF NOT EXISTS idx_sda_registry_audit_created_at
    ON sda_registry_audit(created_at DESC);
"""


class SDAArtifactClass(str, Enum):
    CANONICAL_ONTOLOGY = "canonical_ontology"
    CANONICAL_STRUCTURAL_GRAMMAR = "canonical_structural_grammar"
    CROSSWALK_MAPPING = "crosswalk_mapping"


class SDARegistryKind(str, Enum):
    EXISTENTIAL_INVARIANT = "existential_invariant"
    REPRESENTATION_GEOMETRY = "representation_geometry"
    ARCHETYPAL_GEOMETRY = "archetypal_geometry"
    SPECIES_COMPOSITION_GRAMMAR = "species_composition_grammar"
    PRIMITIVE_TO_INVARIANT_CROSSWALK = "primitive_to_invariant_crosswalk"
    ARCHETYPE_TO_GEOMETRY_CROSSWALK = "archetype_to_geometry_crosswalk"


class SDAAuditStatus(str, Enum):
    READY = "READY"
    NOT_READY = "NOT_READY"


class TensionAxis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    primary_pole: str
    counter_pole: str


class SignalIndicators(BaseModel):
    model_config = ConfigDict(extra="forbid")

    linguistic: list[str] = Field(default_factory=list)
    symbolic: list[str] = Field(default_factory=list)


class DistortionProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    healthy: list[str] = Field(default_factory=list)
    distorted: list[str] = Field(default_factory=list)
    trajectory_risks: list[str] = Field(default_factory=list)


class CrosswalkWeight(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target_id: str
    weight: float = Field(ge=0.0, le=1.0)
    rationale: str


class SDARegistryBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str
    artifact_class: SDAArtifactClass
    registry_kind: SDARegistryKind
    canonical_name: str
    version: str = "1.0"
    definition: str
    source_documents: list[str] = Field(min_length=1)
    notes: Optional[str] = None


class ExistentialInvariantRecord(SDARegistryBase):
    artifact_class: Literal[SDAArtifactClass.CANONICAL_ONTOLOGY]
    registry_kind: Literal[SDARegistryKind.EXISTENTIAL_INVARIANT]
    invariant_gravity: float = Field(ge=0.0, le=1.0)
    semantic_axis: TensionAxis
    human_questions: list[str] = Field(min_length=1)
    pressure_modes: DistortionProfile
    adjacent_invariants: list[str] = Field(default_factory=list)
    conflict_relations: list[str] = Field(default_factory=list)
    signal_indicators: SignalIndicators

    @field_validator("artifact_id")
    @classmethod
    def enforce_prefix(cls, value: str) -> str:
        if not value.startswith(INV_PREFIX):
            raise ValueError("ExistentialInvariantRecord IDs must start with SDA-INV-")
        return value

    @model_validator(mode="before")
    @classmethod
    def ban_runtime_scalars(cls, data: Any) -> Any:
        if isinstance(data, dict):
            forbidden = {"invariant_activation_intensity", "invariant_resonance_multiplier"}
            present = forbidden.intersection(data.keys())
            if present:
                present_list = ", ".join(sorted(present))
                raise ValueError(f"Runtime-only scalar(s) forbidden on canonical invariant: {present_list}")
        return data


class RepresentationGeometryRecord(SDARegistryBase):
    artifact_class: Literal[SDAArtifactClass.CANONICAL_ONTOLOGY]
    registry_kind: Literal[SDARegistryKind.REPRESENTATION_GEOMETRY]
    authority_source: str
    fear_weight: float = Field(ge=0.0, le=1.0)
    status_distribution: str
    identity_framing: str
    belonging_mode: str
    transcendence_mode: str
    moral_load_distribution: dict[str, float] = Field(default_factory=dict)
    trajectory_risks: list[str] = Field(default_factory=list)

    @field_validator("artifact_id")
    @classmethod
    def enforce_prefix(cls, value: str) -> str:
        if not value.startswith(RPG_PREFIX):
            raise ValueError("RepresentationGeometryRecord IDs must start with SDA-RPG-")
        return value


class ArchetypalGeometryRecord(SDARegistryBase):
    artifact_class: Literal[SDAArtifactClass.CANONICAL_STRUCTURAL_GRAMMAR]
    registry_kind: Literal[SDARegistryKind.ARCHETYPAL_GEOMETRY]
    invariant_bindings_primary: list[str] = Field(min_length=1)
    invariant_bindings_secondary: list[str] = Field(default_factory=list)
    authority_flow: str
    agency_distribution: str
    transformation_pattern: str
    sacrifice_pattern: str
    shadow_inversion: list[str] = Field(default_factory=list)
    compatible_content_archetypes: list[str] = Field(default_factory=list)
    incompatible_distortions: list[str] = Field(default_factory=list)

    @field_validator("artifact_id")
    @classmethod
    def enforce_prefix(cls, value: str) -> str:
        if not value.startswith(ARG_PREFIX):
            raise ValueError("ArchetypalGeometryRecord IDs must start with SDA-ARG-")
        return value


class SpeciesCompositionRule(SDARegistryBase):
    artifact_class: Literal[SDAArtifactClass.CANONICAL_STRUCTURAL_GRAMMAR]
    registry_kind: Literal[SDARegistryKind.SPECIES_COMPOSITION_GRAMMAR]
    admissible_invariants: list[str] = Field(default_factory=list)
    admissible_geometries: list[str] = Field(default_factory=list)
    admissible_representation_geometries: list[str] = Field(default_factory=list)
    forbidden_pairings: list[str] = Field(default_factory=list)
    instability_thresholds: dict[str, float] = Field(default_factory=dict)
    shadow_drift_triggers: list[str] = Field(default_factory=list)

    @field_validator("artifact_id")
    @classmethod
    def enforce_prefix(cls, value: str) -> str:
        if not value.startswith(SCG_PREFIX):
            raise ValueError("SpeciesCompositionRule IDs must start with SDA-SCG-")
        return value


class PrimitiveToInvariantCrosswalkEntry(SDARegistryBase):
    artifact_class: Literal[SDAArtifactClass.CROSSWALK_MAPPING]
    registry_kind: Literal[SDARegistryKind.PRIMITIVE_TO_INVARIANT_CROSSWALK]
    primitive_id: str
    linked_invariants: list[CrosswalkWeight] = Field(min_length=1)

    @field_validator("artifact_id")
    @classmethod
    def enforce_prefix(cls, value: str) -> str:
        if not value.startswith(XW_PI_PREFIX):
            raise ValueError("PrimitiveToInvariantCrosswalk IDs must start with SDA-XW-PI-")
        return value


class ArchetypeToGeometryCrosswalkEntry(SDARegistryBase):
    artifact_class: Literal[SDAArtifactClass.CROSSWALK_MAPPING]
    registry_kind: Literal[SDARegistryKind.ARCHETYPE_TO_GEOMETRY_CROSSWALK]
    content_archetype: str
    linked_geometries: list[CrosswalkWeight] = Field(min_length=1)

    @field_validator("artifact_id")
    @classmethod
    def enforce_prefix(cls, value: str) -> str:
        if not value.startswith(XW_AG_PREFIX):
            raise ValueError("ArchetypeToGeometryCrosswalk IDs must start with SDA-XW-AG-")
        return value


SDARegistryRecord = (
    ExistentialInvariantRecord
    | RepresentationGeometryRecord
    | ArchetypalGeometryRecord
    | SpeciesCompositionRule
    | PrimitiveToInvariantCrosswalkEntry
    | ArchetypeToGeometryCrosswalkEntry
)


class SDARegistryManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    manifest_version: str = "1.0"
    ontology_paths: dict[str, str]
    grammar_paths: dict[str, str]
    crosswalk_paths: dict[str, str]
    expected_counts: dict[str, int]
    source_documents: list[str] = Field(min_length=4)
    version_hash_fields: list[str] = Field(default_factory=list)


class SDAManifestHealth(BaseModel):
    model_config = ConfigDict(extra="forbid")

    manifest_path: str
    manifest_hash: str
    ontology_paths: dict[str, str]
    grammar_paths: dict[str, str]
    crosswalk_paths: dict[str, str]
    expected_counts: dict[str, int]
    path_exists: dict[str, bool] = Field(default_factory=dict)
    counts_matched: bool = False


class SDARegistryIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_path: str
    error_code: str
    message: str
    artifact_id: Optional[str] = None
    registry_kind: Optional[str] = None

    def issue_hash(self) -> str:
        payload = f"{self.artifact_path}:{self.error_code}:{self.message}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


class SDARegistryAuditReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    last_load_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    manifest_hash: str = ""
    registry_hash: str = ""
    existential_invariant_count: int = Field(ge=0, default=0)
    representation_geometry_count: int = Field(ge=0, default=0)
    archetypal_geometry_count: int = Field(ge=0, default=0)
    species_composition_rule_count: int = Field(ge=0, default=0)
    primitive_to_invariant_crosswalk_count: int = Field(ge=0, default=0)
    archetype_to_geometry_crosswalk_count: int = Field(ge=0, default=0)
    rejected_artifacts: list[str] = Field(default_factory=list)
    issues: list[SDARegistryIssue] = Field(default_factory=list)
    manifest_health: Optional[SDAManifestHealth] = None
    ready: bool = False
    status: SDAAuditStatus = SDAAuditStatus.NOT_READY

    @model_validator(mode="after")
    def align_status(self) -> "SDARegistryAuditReport":
        self.status = SDAAuditStatus.READY if self.ready else SDAAuditStatus.NOT_READY
        self.rejected_artifacts = [issue.artifact_path for issue in self.issues]
        return self


class SDAArtifactReloadResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_path: str
    artifact_id: Optional[str] = None
    success: bool
    error_code: Optional[str] = None
    message: str
    affected_crosswalks: list[str] = Field(default_factory=list)
    report: Optional[SDARegistryAuditReport] = None

