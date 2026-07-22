"""
CCP FR-ERA3-25 - Subliminal Function Library and Taxonomy models.

Canonical typed contracts for the Subliminal Function Layer registry,
its maintained crosswalks, validation issues, manifest health, and
reload/audit reports.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


SFL_ROOT_DIRNAME = "sfl"

SFL_FAMILY_PREFIX = "SFL-FAM-"
SFL_FUNCTION_PREFIX = "SFL-FN-"
SFL_COMPRESSION_PREFIX = "SFL-CR-"
SFL_XW_PF_PREFIX = "SFL-XW-PF-"
SFL_XW_RG_PREFIX = "SFL-XW-RG-"
SFL_XW_AR_PREFIX = "SFL-XW-AR-"
SFL_XW_SF_PREFIX = "SFL-XW-SF-"

FORBIDDEN_METRIC_KEYS: frozenset[str] = frozenset(
    {
        "cognitive_imprint_score",
        "symbolic_density_score",
        "atmospheric_coherence_score",
        "identity_signal_strength",
        "memorability_pressure",
        "human_congruence_score",
        "contrast_clarity_score",
        "suggestive_load_score",
        "overexplanation_risk_score",
        "synthetic_smoothness_score",
    }
)

FORBIDDEN_SDA_OWNERSHIP_KEYS: frozenset[str] = frozenset(
    {
        "invariant_gravity",
        "representation_geometry_type",
        "directional_integrity_policy",
        "invariant_activation_intensity",
        "invariant_resonance_multiplier",
    }
)

RECOMMENDED_FUNCTION_FAMILY_COUNT = 12


class SFLArtifactClass(str, Enum):
    CANONICAL_FUNCTION_FAMILY = "canonical_function_family"
    FUNCTION_DEFINITION = "function_definition"
    COMPRESSION_RULE = "compression_rule"
    CROSSWALK = "crosswalk"


class FunctionPolarity(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    DUAL_USE = "dual_use"


class SurfaceKind(str, Enum):
    TELEGRAM = "telegram"
    CAROUSEL = "carousel"
    SHORT_FORM_VIDEO = "short_form_video"
    LONG_FORM_VIDEO = "long_form_video"
    WEBINAR = "webinar"
    COMMERCIAL = "commercial"
    AUDIT = "audit"


class FamilyKind(str, Enum):
    FRAMING_AND_CONTRAST = "framing_and_contrast"
    REPETITION_AND_IMPRINT = "repetition_and_imprint"
    SYMBOLIC_COMPRESSION = "symbolic_compression"
    SUGGESTIVE_GUIDANCE = "suggestive_guidance"
    ATMOSPHERE_AND_FIELD_SHAPING = "atmosphere_and_field_shaping"
    IDENTITY_SIGNALING = "identity_signaling"
    EMOTIONAL_PRIMING = "emotional_priming"
    NARRATIVE_TENSION_PRESERVATION = "narrative_tension_preservation"
    TRUST_AND_PROOF_REINFORCEMENT = "trust_and_proof_reinforcement"
    MEMETIC_AND_RECALL_HOOKS = "memetic_and_recall_hooks"
    PERCEPTUAL_THRESHOLD_MODULATION = "perceptual_threshold_modulation"
    ADAPTIVE_AMBIGUITY_AND_PARADOX = "adaptive_ambiguity_and_paradox"


class SourceDocumentRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=3)
    note: str = Field(min_length=3)


class FunctionEffectRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    effect_key: str = Field(pattern=r"^[a-z0-9_]+$")
    description: str = Field(min_length=3)


class ConstraintRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    constraint_key: str = Field(pattern=r"^[a-z0-9_]+$")
    description: str = Field(min_length=3)


class PrimitiveLinkRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    primitive_id: str = Field(pattern=r"^(EXP|PRM)-[A-Z]{3}-\d{3}$")
    rationale: str = Field(min_length=3)


class GeometryLinkRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    geometry_id: str = Field(pattern=r"^SDA-(RPG|ARG)-\d{3}$")
    rationale: str = Field(min_length=3)


class ArchetypeLinkRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    archetype_name: str = Field(min_length=3)
    rationale: str = Field(min_length=3)


class AssociationAliasRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    raw_term: str = Field(min_length=2)
    normalization_note: str = Field(min_length=3)


class FunctionBoundaryRule(BaseModel):
    model_config = ConfigDict(extra="forbid")

    allowed_when: str = Field(min_length=3)
    disallowed_when: str = Field(min_length=3)
    downgrade_behavior: str = Field(min_length=3)


class SubliminalFunctionFamilyRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(pattern=r"^SFL-FAM-\d{3}$")
    artifact_class: Literal["canonical_function_family"] = "canonical_function_family"
    canonical_name: str = Field(min_length=3)
    family_kind: FamilyKind
    definition: str = Field(min_length=20)
    purpose: str = Field(min_length=20)
    positive_space_role: str = Field(min_length=20)
    negative_space_boundary: str = Field(min_length=20)
    anti_bloat_guidance: str = Field(min_length=20)
    related_raw_terms: list[AssociationAliasRef] = Field(min_length=1)
    source_documents: list[SourceDocumentRef] = Field(min_length=1)


class SubliminalFunctionDefinitionRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(pattern=r"^SFL-FN-\d{3}$")
    artifact_class: Literal["function_definition"] = "function_definition"
    canonical_name: str = Field(min_length=3)
    family_id: str = Field(pattern=r"^SFL-FAM-\d{3}$")
    polarity: FunctionPolarity
    definition: str = Field(min_length=20)
    positive_operation: str = Field(min_length=20)
    negative_operation: str = Field(min_length=20)
    intended_effects: list[FunctionEffectRef] = Field(min_length=1)
    alignment_rules: list[FunctionBoundaryRule] = Field(min_length=1)
    primitive_links: list[PrimitiveLinkRef] = Field(default_factory=list)
    geometry_links: list[GeometryLinkRef] = Field(default_factory=list)
    archetype_links: list[ArchetypeLinkRef] = Field(default_factory=list)
    source_documents: list[SourceDocumentRef] = Field(min_length=1)


class FunctionFamilyCompressionRuleRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(pattern=r"^SFL-CR-\d{3}$")
    artifact_class: Literal["compression_rule"] = "compression_rule"
    canonical_family_id: str = Field(pattern=r"^SFL-FAM-\d{3}$")
    raw_terms: list[AssociationAliasRef] = Field(min_length=1)
    compression_rationale: str = Field(min_length=20)
    duplicate_rejection_terms: list[str] = Field(default_factory=list)
    source_documents: list[SourceDocumentRef] = Field(min_length=1)


class PrimitiveToFunctionFamilyCrosswalkRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(pattern=r"^SFL-XW-PF-\d{3}$")
    artifact_class: Literal["crosswalk"] = "crosswalk"
    primitive_links: list[PrimitiveLinkRef] = Field(min_length=1)
    target_family_ids: list[str] = Field(min_length=1)
    mapping_rationale: str = Field(min_length=20)
    source_documents: list[SourceDocumentRef] = Field(min_length=1)


class RepresentationGeometryToFunctionProfileRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(pattern=r"^SFL-XW-RG-\d{3}$")
    artifact_class: Literal["crosswalk"] = "crosswalk"
    geometry_links: list[GeometryLinkRef] = Field(min_length=1)
    preferred_function_ids: list[str] = Field(min_length=1)
    discouraged_function_ids: list[str] = Field(default_factory=list)
    mapping_rationale: str = Field(min_length=20)
    source_documents: list[SourceDocumentRef] = Field(min_length=1)


class ArchetypeToFunctionProfileRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(pattern=r"^SFL-XW-AR-\d{3}$")
    artifact_class: Literal["crosswalk"] = "crosswalk"
    archetype_links: list[ArchetypeLinkRef] = Field(min_length=1)
    preferred_function_ids: list[str] = Field(min_length=1)
    required_family_ids: list[str] = Field(default_factory=list)
    discouraged_family_ids: list[str] = Field(default_factory=list)
    mapping_rationale: str = Field(min_length=20)
    source_documents: list[SourceDocumentRef] = Field(min_length=1)


class SurfaceConstraintProfileRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(pattern=r"^SFL-XW-SF-\d{3}$")
    artifact_class: Literal["crosswalk"] = "crosswalk"
    surface: SurfaceKind
    preferred_family_ids: list[str] = Field(default_factory=list)
    discouraged_family_ids: list[str] = Field(default_factory=list)
    hard_constraints: list[ConstraintRef] = Field(default_factory=list)
    rationale: str = Field(min_length=20)
    source_documents: list[SourceDocumentRef] = Field(min_length=1)


SFLRegistryRecord = (
    SubliminalFunctionFamilyRecord
    | SubliminalFunctionDefinitionRecord
    | FunctionFamilyCompressionRuleRecord
    | PrimitiveToFunctionFamilyCrosswalkRecord
    | RepresentationGeometryToFunctionProfileRecord
    | ArchetypeToFunctionProfileRecord
    | SurfaceConstraintProfileRecord
)


class SFLManifestExpectedCounts(BaseModel):
    model_config = ConfigDict(extra="forbid")

    families: int = Field(ge=1)
    functions: int = Field(ge=1)
    compression_rules: int = Field(ge=1)
    primitive_to_function_family_crosswalks: int = Field(ge=0)
    representation_geometry_crosswalks: int = Field(ge=0)
    archetype_profile_crosswalks: int = Field(ge=0)
    surface_constraint_profiles: int = Field(ge=0)


class SFLRegistryManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: str = Field(min_length=1)
    artifact_root: str = Field(min_length=1)
    family_path: str = Field(min_length=1)
    function_path: str = Field(min_length=1)
    compression_rule_path: str = Field(min_length=1)
    crosswalk_paths: list[str] = Field(min_length=1)
    expected_counts: SFLManifestExpectedCounts


class SFLManifestHealth(BaseModel):
    model_config = ConfigDict(extra="forbid")

    manifest_path: str
    artifact_root: str
    manifest_hash: str
    family_path: str
    function_path: str
    compression_rule_path: str
    crosswalk_paths: list[str]
    resolved_crosswalk_paths: dict[str, str] = Field(default_factory=dict)
    expected_counts: SFLManifestExpectedCounts
    path_exists: dict[str, bool] = Field(default_factory=dict)
    counts_matched: bool = False


class SFLRegistryIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    error_code: str = Field(min_length=3)
    artifact_path: str = Field(min_length=3)
    artifact_id: str | None = None
    message: str = Field(min_length=3)
    severity: Literal["warning", "error"] = "error"

    def issue_hash(self) -> str:
        payload = f"{self.artifact_path}:{self.error_code}:{self.message}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


class SFLRegistryAuditReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ready: bool
    family_count: int = Field(ge=0)
    function_count: int = Field(ge=0)
    compression_rule_count: int = Field(ge=0)
    primitive_to_function_family_crosswalk_count: int = Field(ge=0)
    representation_geometry_crosswalk_count: int = Field(ge=0)
    archetype_profile_crosswalk_count: int = Field(ge=0)
    surface_constraint_profile_count: int = Field(ge=0)
    issues: list[SFLRegistryIssue] = Field(default_factory=list)
    rejected_artifacts: list[str] = Field(default_factory=list)
    manifest_health: SFLManifestHealth | None = None
    last_load_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @model_validator(mode="after")
    def align_rejections(self) -> "SFLRegistryAuditReport":
        self.rejected_artifacts = [issue.artifact_path for issue in self.issues]
        return self


class SFLArtifactReloadResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_path: str = Field(min_length=3)
    artifact_id: str | None = None
    success: bool
    error_code: str | None = None
    message: str = Field(min_length=3)
    previous_state_restored: bool = False
    report: SFLRegistryAuditReport
