"""Canonical CAE storyboard session and revision domain (M0079).

This module is deliberately a projection layer around the existing
``EditorialStoryboardRecord`` and ``PreparationGraphStore`` authorities.  It
does not own semantic meaning, candidate selection, asset rights, or runtime
execution.  A session points at one approved editorial storyboard and each
revision is persisted through ``GraphRevisionRecord`` so stale editors cannot
overwrite one another.
"""

from __future__ import annotations

import json
import sqlite3
from typing import Any, Dict, Iterable, List, Optional, Sequence
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator, root_validator, validator

from ca_contracts import CanonicalizationError, canonical_sha256, utc_now_rfc3339
from ca_runtime.editorial_discovery_store import EditorialDiscoveryStore
from ca_runtime.narrative_editing_grammar import (
    NarrativeEditingGrammarRegistry,
    NarrativeGrammarBinding,
    NarrativeGrammarBindingError,
)
from ca_runtime.preparation_graph_store import (
    GraphRevisionRecord,
    PreparationGraphStore,
    StaleBaseRevisionError,
)


class StoryboardDomainError(Exception):
    """Base error for fail-closed storyboard domain operations."""


class StoryboardAuthorityError(StoryboardDomainError):
    """The requested storyboard or source lineage is not authoritative."""


class StoryboardRevisionValidationError(StoryboardDomainError):
    """A revision is malformed, ungrounded, or internally inconsistent."""


class StoryboardRevisionNotFoundError(StoryboardDomainError):
    """A revision is not visible in the requested workspace/session."""


class StoryboardFeedbackError(StoryboardDomainError):
    """Feedback is invalid or attempts to mutate an immutable record."""


class FeedbackDecision(str):
    GOOD = "GOOD"
    NEEDS_EDIT = "NEEDS_EDIT"
    REJECT = "REJECT"


class StoryboardSessionStatus(str):
    DRAFT = "DRAFT"
    IN_REVIEW = "IN_REVIEW"
    COMPILED = "COMPILED"
    BLOCKED = "BLOCKED"


class SourceQualityProfile(BaseModel):
    """Measured source-condition profile used to bound transformations."""

    profile_id: str
    source_ref: str
    width_px: int
    height_px: int
    frame_rate_milli_fps: int
    crop_count: int = 0
    crop_retention_bps: int = 10000
    compression_loss_bps: int = 0
    sharpness_bps: int = 10000
    prior_degradation_bps: int = 0
    evidence_refs: List[str] = Field(..., min_length=1)

    @field_validator("width_px", "height_px")
    @classmethod
    def positive_dimensions(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("source dimensions must be positive")
        return value

    @field_validator("frame_rate_milli_fps")
    @classmethod
    def positive_frame_rate(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("frame_rate_milli_fps must be positive")
        return value

    @field_validator("crop_count")
    @classmethod
    def non_negative_crop_count(cls, value: int) -> int:
        if value < 0:
            raise ValueError("crop_count must be non-negative")
        return value

    @field_validator("crop_retention_bps", "compression_loss_bps", "sharpness_bps", "prior_degradation_bps")
    @classmethod
    def bounded_quality_measurement(cls, value: int) -> int:
        if not 0 <= value <= 10000:
            raise ValueError("quality measurements must be between 0 and 10000 bps")
        return value

    @property
    def resolution_bps(self) -> int:
        minimum_dimension = min(self.width_px, self.height_px)
        if minimum_dimension >= 2160:
            return 10000
        if minimum_dimension >= 1080:
            return 8000
        if minimum_dimension >= 720:
            return 5500
        if minimum_dimension >= 480:
            return 3500
        return 2000

    @property
    def frame_rate_quality_bps(self) -> int:
        if self.frame_rate_milli_fps >= 30000:
            return 10000
        if self.frame_rate_milli_fps >= 24000:
            return 8500
        if self.frame_rate_milli_fps >= 20000:
            return 6500
        if self.frame_rate_milli_fps >= 15000:
            return 4500
        return 2500

    @property
    def quality_score_bps(self) -> int:
        score = (
            self.resolution_bps * 30
            + self.crop_retention_bps * 15
            + (10000 - self.compression_loss_bps) * 20
            + self.sharpness_bps * 20
            + self.frame_rate_quality_bps * 10
            + (10000 - self.prior_degradation_bps) * 5
        ) // 100
        return max(0, min(10000, score))

    @property
    def quality_level(self) -> str:
        if self.quality_score_bps >= 8000:
            return "HIGH"
        if self.quality_score_bps >= 6500:
            return "MEDIUM"
        if self.quality_score_bps >= 4500:
            return "LOW"
        return "DEGRADED"

    @property
    def presentation_strategies(self) -> List[str]:
        return {
            "HIGH": ["STANDARD", "SUBTLE_REFRAME", "SUBTLE_COLOR"],
            "MEDIUM": ["STANDARD", "REDUCED_SCALE", "SELECTIVE_FRAMING"],
            "LOW": ["REDUCED_SCALE", "INSET", "CONTEXTUAL", "GRAYSCALE"],
            "DEGRADED": ["CONTAINERIZED", "INSET", "CONTEXTUAL", "GRAYSCALE"],
        }[self.quality_level]


class VisualAssetReference(BaseModel):
    """A governed reference to an asset; it is not an asset authority."""

    reference_id: str
    asset_id: str
    source_type: str = "EVIDENCE"
    source_uri: Optional[str] = None
    evidence_refs: List[str] = Field(default_factory=list)
    rights_status: str = "UNVERIFIED"
    source_quality: str = "UNKNOWN"
    source_quality_profile: Optional[SourceQualityProfile] = None
    approved: bool = False


TRANSFORMATION_INTENTS = frozenset({
    "WITHHOLD", "REVEAL", "FOCUS", "CONTRAST", "PROVE",
    "EXPLAIN", "CONNECT", "ESCALATE", "INTERRUPT", "RESOLVE",
})
TRANSFORMATION_MODES = frozenset({
    "AUTO", "EXTRACT_REGION", "REFRAME", "COMPARE", "ANNOTATE", "INSET",
    "PROTECT", "HOLD", "RETURN", "CUT",
})
TRANSFORMATION_MOTIONS = frozenset({"STATIC", "SUBTLE_ZOOM", "SUBTLE_PAN", "RETURN"})
TRANSFORMATION_SOURCE_QUALITIES = frozenset({"HIGH", "MEDIUM", "LOW", "DEGRADED", "UNKNOWN"})
TRANSFORMATION_SOURCE_ROLES = frozenset({"A_ROLL", "B_ROLL", "E_ROLL", "DOCUMENT", "PATTERN_INTERRUPT"})


class TransformationIntent(BaseModel):
    """Typed reason for changing a source, distinct from executable detail."""

    intent_id: str
    source_element_id: str
    intent: str
    semantic_target: str
    mode: str = "AUTO"
    emphasis: str = "BALANCED"
    motion: str = "STATIC"
    constraints: Dict[str, Any] = Field(default_factory=dict)

    @root_validator(pre=True)
    def normalize_legacy_shape(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        payload = dict(values or {})
        legacy_mode = str(payload.get("mode", "")).upper()
        if "intent" not in payload and legacy_mode in TRANSFORMATION_INTENTS:
            payload["intent"] = legacy_mode
            payload["mode"] = "AUTO"
        if "source_element_id" not in payload and payload.get("source"):
            payload["source_element_id"] = payload["source"]
        return payload

    @validator("intent")
    def intent_is_bounded(cls, value: str) -> str:
        normalized = value.upper()
        if normalized not in TRANSFORMATION_INTENTS:
            raise ValueError(f"unsupported transformation intent: {value}")
        return normalized

    @validator("mode")
    def mode_is_bounded(cls, value: str) -> str:
        normalized = value.upper()
        if normalized not in TRANSFORMATION_MODES:
            raise ValueError(f"unsupported transformation mode: {value}")
        return normalized

    @validator("motion")
    def motion_is_bounded(cls, value: str) -> str:
        normalized = value.upper()
        if normalized not in TRANSFORMATION_MOTIONS:
            raise ValueError(f"unsupported transformation motion: {value}")
        return normalized

    @validator("emphasis")
    def emphasis_is_present(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("transformation emphasis must be non-empty")
        return normalized

    @validator("semantic_target", "source_element_id")
    def required_reference_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("transformation source and semantic target are required")
        return value

    @property
    def source(self) -> str:
        return self.source_element_id

    def compile(self, *, authorized_recipe_ids: Optional[Sequence[str]] = None,
                expected_registry_version: Optional[str] = None) -> "TransformationRecipe":
        from ca_runtime.transformation_recipe import TransformationRecipeCompiler
        return TransformationRecipeCompiler().compile(
            self, authorized_recipe_ids=authorized_recipe_ids,
            expected_registry_version=expected_registry_version,
        )


class TransformationRecipe(BaseModel):
    """Governed primitive/keyframe projection of a ``TransformationIntent``."""

    recipe_id: str
    intent_id: str
    primitives: List[Dict[str, Any]] = Field(default_factory=list)
    keyframes: List[Dict[str, Any]] = Field(default_factory=list)
    constraints: Dict[str, Any] = Field(default_factory=dict)
    template_id: Optional[str] = None
    registry_version: str = "LEGACY"
    motion_template: str = "STATIC_HOLD"
    governed: bool = False
    recipe_sha256: Optional[str] = None


class TransformationValidationResult(BaseModel):
    allowed: bool
    source_quality_level: str
    max_scale_delta_bps: int
    max_reframe_bps: int
    max_motion_amplitude_bps: int
    allowed_color_treatments: List[str]
    recommended_presentation_strategies: List[str]
    violations: List[str] = Field(default_factory=list)


_TRANSFORMATION_QUALITY_LIMITS = {
    "HIGH": {"scale": 1200, "reframe": 1200, "motion": 1200, "color": ["NONE", "CONTROLLED", "SUBTLE_LUT"]},
    "MEDIUM": {"scale": 800, "reframe": 800, "motion": 700, "color": ["NONE", "CONTROLLED"]},
    "LOW": {"scale": 400, "reframe": 400, "motion": 300, "color": ["NONE", "GRAYSCALE", "CONTROLLED"]},
    "DEGRADED": {"scale": 150, "reframe": 200, "motion": 0, "color": ["NONE", "GRAYSCALE"]},
}


def _declared_transform_intensity(recipe: TransformationRecipe) -> Dict[str, Any]:
    scales: List[int] = []
    reframes: List[int] = []
    motions: List[int] = []
    colors: List[str] = []
    undeclared: List[str] = []
    for primitive in recipe.primitives:
        op = str(primitive.get("op", "")).upper()
        if op in {"ZOOM", "SCALE"} and "scale_delta_bps" not in primitive and "amount_bps" not in primitive:
            undeclared.append(f"{op} must declare amount_bps or scale_delta_bps")
        if op == "REFRAME" and "reframe_bps" not in primitive:
            undeclared.append("REFRAME must declare reframe_bps")
        if op == "MOTION" and "motion_amplitude_bps" not in primitive:
            undeclared.append("MOTION must declare motion_amplitude_bps")
        if "scale_delta_bps" in primitive:
            scales.append(abs(int(primitive["scale_delta_bps"])))
        if op in {"ZOOM", "SCALE"} and "amount_bps" in primitive:
            scales.append(abs(int(primitive["amount_bps"])))
        if "reframe_bps" in primitive:
            reframes.append(abs(int(primitive["reframe_bps"])))
        if "motion_amplitude_bps" in primitive:
            motions.append(abs(int(primitive["motion_amplitude_bps"])))
        if op in {"COLOR", "LUT", "COLOR_TREATMENT"}:
            colors.append(str(primitive.get("treatment", "CONTROLLED")).upper())
    for keyframe in recipe.keyframes:
        if "scale_delta_bps" in keyframe:
            scales.append(abs(int(keyframe["scale_delta_bps"])))
        if "motion_amplitude_bps" in keyframe:
            motions.append(abs(int(keyframe["motion_amplitude_bps"])))
    return {
        "scale_delta_bps": max(scales, default=0),
        "reframe_bps": max(reframes, default=0),
        "motion_amplitude_bps": max(motions, default=0),
        "color_treatments": colors or ["NONE"],
        "undeclared_intensity": undeclared,
    }


def validate_transformation_for_source_quality(
    profile: SourceQualityProfile, recipe: TransformationRecipe
) -> TransformationValidationResult:
    limits = _TRANSFORMATION_QUALITY_LIMITS[profile.quality_level]
    declared = _declared_transform_intensity(recipe)
    violations = list(declared["undeclared_intensity"])
    if declared["scale_delta_bps"] > limits["scale"]:
        violations.append(f"scale_delta_bps={declared['scale_delta_bps']} exceeds {limits['scale']} for {profile.quality_level}")
    if declared["reframe_bps"] > limits["reframe"]:
        violations.append(f"reframe_bps={declared['reframe_bps']} exceeds {limits['reframe']} for {profile.quality_level}")
    if declared["motion_amplitude_bps"] > limits["motion"]:
        violations.append(f"motion_amplitude_bps={declared['motion_amplitude_bps']} exceeds {limits['motion']} for {profile.quality_level}")
    for treatment in declared["color_treatments"]:
        if treatment not in limits["color"]:
            violations.append(f"color treatment '{treatment}' is not allowed for {profile.quality_level}")
    return TransformationValidationResult(
        allowed=not violations,
        source_quality_level=profile.quality_level,
        max_scale_delta_bps=limits["scale"],
        max_reframe_bps=limits["reframe"],
        max_motion_amplitude_bps=limits["motion"],
        allowed_color_treatments=list(limits["color"]),
        recommended_presentation_strategies=profile.presentation_strategies,
        violations=violations,
    )


def adapt_transformation_recipe_for_source_quality(
    profile: SourceQualityProfile, recipe: TransformationRecipe
) -> TransformationRecipe:
    limits = _TRANSFORMATION_QUALITY_LIMITS[profile.quality_level]
    primitives: List[Dict[str, Any]] = []
    for primitive in recipe.primitives:
        copy = dict(primitive)
        if "scale_delta_bps" in copy:
            copy["scale_delta_bps"] = min(abs(int(copy["scale_delta_bps"])), limits["scale"])
        if str(copy.get("op", "")).upper() in {"ZOOM", "SCALE"} and "amount_bps" in copy:
            copy["amount_bps"] = min(abs(int(copy["amount_bps"])), limits["scale"])
        if "reframe_bps" in copy:
            copy["reframe_bps"] = min(abs(int(copy["reframe_bps"])), limits["reframe"])
        if "motion_amplitude_bps" in copy:
            copy["motion_amplitude_bps"] = min(abs(int(copy["motion_amplitude_bps"])), limits["motion"])
        if str(copy.get("op", "")).upper() in {"COLOR", "LUT", "COLOR_TREATMENT"}:
            treatment = str(copy.get("treatment", "CONTROLLED")).upper()
            if treatment not in limits["color"]:
                copy["treatment"] = limits["color"][0]
        primitives.append(copy)
    keyframes: List[Dict[str, Any]] = []
    for keyframe in recipe.keyframes:
        copy = dict(keyframe)
        if "scale_delta_bps" in copy:
            copy["scale_delta_bps"] = min(abs(int(copy["scale_delta_bps"])), limits["scale"])
        if "motion_amplitude_bps" in copy:
            copy["motion_amplitude_bps"] = min(abs(int(copy["motion_amplitude_bps"])), limits["motion"])
        keyframes.append(copy)
    constraints = dict(recipe.constraints)
    constraints.update({
        "source_quality_level": profile.quality_level,
        "source_quality_profile_id": profile.profile_id,
        "source_quality_evidence_refs": list(profile.evidence_refs),
        "presentation_strategy": profile.presentation_strategies[0],
    })
    return recipe.model_copy(update={"primitives": primitives, "keyframes": keyframes, "constraints": constraints})


class Keyframe(BaseModel):
    """Canonical fixed-point keyframe emitted by the final-hit compiler."""

    at_ms: int
    template: str = "HOLD"
    scale_bps: Optional[int] = None
    x_bps: Optional[int] = None
    y_bps: Optional[int] = None
    purpose: str = "HOLD"

    @validator("at_ms")
    def at_ms_non_negative(cls, value: int) -> int:
        if isinstance(value, bool) or value < 0:
            raise ValueError("keyframe at_ms must be a non-negative integer")
        return value

    @validator("template", "purpose")
    def keyframe_text_non_empty(cls, value: str) -> str:
        normalized = value.strip().upper()
        if not normalized:
            raise ValueError("keyframe template and purpose must be non-empty")
        return normalized

    @validator("scale_bps")
    def scale_is_bounded(cls, value: Optional[int]) -> Optional[int]:
        if value is None:
            return value
        if isinstance(value, bool) or value < 0 or value > 20000:
            raise ValueError("keyframe scale_bps must be an integer in [0, 20000]")
        return value

    @validator("x_bps", "y_bps")
    def position_is_bounded(cls, value: Optional[int]) -> Optional[int]:
        if value is None:
            return value
        if isinstance(value, bool) or value < 0 or value > 10000:
            raise ValueError("keyframe positions must be integers in [0, 10000]")
        return value


class MotionPlan(BaseModel):
    """Deterministic motion/keyframe plan, downstream of semantic intent."""

    motion_plan_id: str
    duration_ms: int = 0
    keyframes: List[Keyframe] = Field(default_factory=list)
    intensity_bps: int = 0
    attention_cost_bps: int = 0
    compiled_from_recipe_id: Optional[str] = None
    source_quality_level: Optional[str] = None

    @validator("duration_ms", "intensity_bps", "attention_cost_bps")
    def non_negative(cls, value: int) -> int:
        if isinstance(value, bool) or value < 0:
            raise ValueError("motion values must be non-negative")
        return value

    @validator("intensity_bps")
    def intensity_is_bounded(cls, value: int) -> int:
        if value > 10000:
            raise ValueError("motion intensity must be in [0, 10000] bps")
        return value

    @validator("attention_cost_bps")
    def attention_cost_is_bounded(cls, value: int) -> int:
        if value > 10000:
            raise ValueError("motion attention cost must be in [0, 10000] bps")
        return value


class StoryboardElement(BaseModel):
    element_id: str
    kind: str
    semantic_purpose: str
    source_evidence_refs: List[str] = Field(default_factory=list)
    asset_references: List[VisualAssetReference] = Field(default_factory=list)
    transformation_intent: Optional[TransformationIntent] = None
    transformation_recipe: Optional[TransformationRecipe] = None
    motion_plan: Optional[MotionPlan] = None
    properties: Dict[str, Any] = Field(default_factory=dict)


class StoryboardShot(BaseModel):
    shot_id: str
    start_ms: int
    end_ms: int
    semantic_purpose: str
    shot_language: Dict[str, Any] = Field(default_factory=dict)
    elements: List[StoryboardElement] = Field(default_factory=list)

    @validator("end_ms")
    def end_after_start(cls, value: int, values: Dict[str, Any]) -> int:
        if "start_ms" in values and value <= values["start_ms"]:
            raise ValueError("shot end_ms must be greater than start_ms")
        return value


class StoryboardScene(BaseModel):
    scene_id: str
    scene_order: int
    semantic_purpose: str
    source_evidence_refs: List[str] = Field(default_factory=list)
    narrative_grammar: Optional[NarrativeGrammarBinding] = None
    shots: List[StoryboardShot] = Field(default_factory=list)

    @validator("scene_order")
    def scene_order_is_non_negative(cls, value: int) -> int:
        if value < 0:
            raise ValueError("scene_order must be non-negative")
        return value


class StoryboardSession(BaseModel):
    """Editable workspace identity around one canonical EditorialStoryboard."""

    workspace_id: str
    session_id: str
    editorial_storyboard_id: str
    graph_id: str
    semantic_program_id: Optional[str] = None
    harness_id: Optional[str] = None
    status: str = StoryboardSessionStatus.DRAFT
    created_by: str
    created_at: str = Field(default_factory=utc_now_rfc3339)
    latest_revision_id: Optional[str] = None


class StoryboardRevision(BaseModel):
    """Immutable editable storyboard snapshot backed by ``GraphRevisionRecord``."""

    workspace_id: str
    session_id: str
    revision_id: str
    revision_seq: int
    base_revision_id: Optional[str]
    editorial_storyboard_id: str
    semantic_program_id: Optional[str] = None
    harness_id: Optional[str] = None
    scenes: List[StoryboardScene] = Field(default_factory=list)
    source_evidence_refs: List[str] = Field(default_factory=list)
    status: str = StoryboardSessionStatus.DRAFT
    author_id: str
    canonical_sha256: str
    created_at: str


class OperatorVisualFeedback(BaseModel):
    feedback_id: str
    workspace_id: str
    session_id: str
    revision_id: str
    operator_id: str
    decision: str
    note: Optional[str] = None
    reason_category: Optional[str] = None
    created_at: str = Field(default_factory=utc_now_rfc3339)
    feedback_sha256: str

    @validator("decision")
    def decision_is_bounded(cls, value: str) -> str:
        normalized = value.upper()
        if normalized not in {
            FeedbackDecision.GOOD,
            FeedbackDecision.NEEDS_EDIT,
            FeedbackDecision.REJECT,
        }:
            raise ValueError(f"unsupported feedback decision: {value}")
        return normalized


class StoryboardValidationReport(BaseModel):
    report_id: str
    workspace_id: str
    session_id: str
    revision_id: str
    passed: bool
    checks: Dict[str, str] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    report_sha256: str
    created_at: str = Field(default_factory=utc_now_rfc3339)


class StoryboardCompileReceipt(BaseModel):
    receipt_id: str
    workspace_id: str
    session_id: str
    revision_id: str
    editorial_storyboard_id: str
    semantic_program_id: Optional[str]
    harness_id: Optional[str]
    validation_report_id: str
    status: str
    lineage_sha256: str
    created_at: str = Field(default_factory=utc_now_rfc3339)


def _model_payload(model: BaseModel) -> Dict[str, Any]:
    return model.dict(exclude_none=True)


class StoryboardSessionStore:
    """SQLite persistence adapter for the canonical editable storyboard layer."""

    def __init__(
        self,
        connection: Optional[sqlite3.Connection] = None,
        *,
        editorial_store: Optional[EditorialDiscoveryStore] = None,
    ) -> None:
        if editorial_store is not None:
            connection = editorial_store._conn  # shared authoritative connection
        self.conn = connection or sqlite3.connect(":memory:", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.editorial_store = editorial_store
        self.graph_store = PreparationGraphStore(self.conn)
        self._init_schema()

    def _init_schema(self) -> None:
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS storyboard_session (
                    workspace_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    editorial_storyboard_id TEXT NOT NULL,
                    graph_id TEXT NOT NULL,
                    semantic_program_id TEXT,
                    harness_id TEXT,
                    status TEXT NOT NULL,
                    created_by TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    latest_revision_id TEXT,
                    PRIMARY KEY (workspace_id, session_id),
                    UNIQUE (workspace_id, editorial_storyboard_id)
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS storyboard_operator_feedback (
                    workspace_id TEXT NOT NULL,
                    feedback_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    revision_id TEXT NOT NULL,
                    operator_id TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    note TEXT,
                    reason_category TEXT,
                    created_at TEXT NOT NULL,
                    feedback_sha256 TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, feedback_id),
                    UNIQUE (workspace_id, revision_id, operator_id)
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS storyboard_validation_report (
                    workspace_id TEXT NOT NULL,
                    report_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    revision_id TEXT NOT NULL,
                    passed INTEGER NOT NULL,
                    checks_json TEXT NOT NULL,
                    errors_json TEXT NOT NULL,
                    warnings_json TEXT NOT NULL,
                    report_sha256 TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, report_id),
                    UNIQUE (workspace_id, revision_id)
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS storyboard_compile_receipt (
                    workspace_id TEXT NOT NULL,
                    receipt_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    revision_id TEXT NOT NULL,
                    editorial_storyboard_id TEXT NOT NULL,
                    semantic_program_id TEXT,
                    harness_id TEXT,
                    validation_report_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    lineage_sha256 TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, receipt_id),
                    UNIQUE (workspace_id, revision_id)
                )
                """
            )

    def _require_editorial_storyboard(self, workspace_id: str, storyboard_id: str) -> None:
        if self.editorial_store is not None:
            if self.editorial_store.get_editorial_storyboard(workspace_id, storyboard_id) is None:
                raise StoryboardAuthorityError(
                    f"EditorialStoryboard '{storyboard_id}' not found in workspace '{workspace_id}'"
                )
            return
        row = self.conn.execute(
            "SELECT storyboard_id FROM cae_editorial_storyboards "
            "WHERE workspace_id = ? AND storyboard_id = ?",
            (workspace_id, storyboard_id),
        ).fetchone()
        if row is None:
            raise StoryboardAuthorityError(
                f"EditorialStoryboard '{storyboard_id}' not found in workspace '{workspace_id}'"
            )

    def create_session(
        self,
        *,
        workspace_id: str,
        editorial_storyboard_id: str,
        created_by: str,
        session_id: Optional[str] = None,
        semantic_program_id: Optional[str] = None,
        harness_id: Optional[str] = None,
    ) -> StoryboardSession:
        self._require_editorial_storyboard(workspace_id, editorial_storyboard_id)
        sid = session_id or f"storyboard_session_{uuid4().hex[:16]}"
        existing = self.get_session(workspace_id, sid)
        if existing is not None:
            if existing.editorial_storyboard_id != editorial_storyboard_id:
                raise StoryboardAuthorityError(
                    f"StoryboardSession '{sid}' is already bound to another EditorialStoryboard"
                )
            return existing
        existing_storyboard = self.conn.execute(
            "SELECT session_id FROM storyboard_session "
            "WHERE workspace_id = ? AND editorial_storyboard_id = ?",
            (workspace_id, editorial_storyboard_id),
        ).fetchone()
        if existing_storyboard is not None:
            existing_session = self.get_session(workspace_id, existing_storyboard[0])
            assert existing_session is not None
            return existing_session
        graph_id = f"storyboard_graph_{sid}"
        now = utc_now_rfc3339()
        session = StoryboardSession(
            workspace_id=workspace_id,
            session_id=sid,
            editorial_storyboard_id=editorial_storyboard_id,
            graph_id=graph_id,
            semantic_program_id=semantic_program_id,
            harness_id=harness_id,
            created_by=created_by,
            created_at=now,
        )
        graph = self.graph_store.create_graph(
            workspace_id=workspace_id,
            graph_id=graph_id,
            campaign_id=editorial_storyboard_id,
            name=f"Storyboard session {sid}",
        )
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO storyboard_session
                (workspace_id, session_id, editorial_storyboard_id, graph_id,
                 semantic_program_id, harness_id, status, created_by, created_at,
                 latest_revision_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session.workspace_id,
                    session.session_id,
                    session.editorial_storyboard_id,
                    session.graph_id,
                    session.semantic_program_id,
                    session.harness_id,
                    session.status,
                    session.created_by,
                    session.created_at,
                    session.latest_revision_id,
                ),
            )
        return session

    def get_session(self, workspace_id: str, session_id: str) -> Optional[StoryboardSession]:
        row = self.conn.execute(
            """
            SELECT workspace_id, session_id, editorial_storyboard_id, graph_id,
                   semantic_program_id, harness_id, status, created_by, created_at,
                   latest_revision_id
            FROM storyboard_session
            WHERE workspace_id = ? AND session_id = ?
            """,
            (workspace_id, session_id),
        ).fetchone()
        if row is None:
            return None
        return StoryboardSession(**dict(row))

    def _revision_from_graph(self, session: StoryboardSession, graph: GraphRevisionRecord) -> StoryboardRevision:
        try:
            payload = json.loads(graph.parameter_payload_json)
            return StoryboardRevision(
                workspace_id=graph.workspace_id,
                session_id=session.session_id,
                revision_id=graph.revision_id,
                revision_seq=graph.revision_seq,
                base_revision_id=graph.base_revision_id,
                editorial_storyboard_id=payload["editorial_storyboard_id"],
                semantic_program_id=payload.get("semantic_program_id"),
                harness_id=payload.get("harness_id"),
                scenes=[StoryboardScene(**scene) for scene in payload.get("scenes", [])],
                source_evidence_refs=payload.get("source_evidence_refs", []),
                status=payload.get("status", StoryboardSessionStatus.DRAFT),
                author_id=graph.author_id,
                canonical_sha256=graph.canonical_sha256,
                created_at=graph.created_at,
            )
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise StoryboardRevisionValidationError(
                f"malformed persisted storyboard revision '{graph.revision_id}': {exc}"
            ) from exc

    def get_revision(self, workspace_id: str, session_id: str, revision_id: str) -> StoryboardRevision:
        session = self.get_session(workspace_id, session_id)
        if session is None:
            raise StoryboardRevisionNotFoundError(
                f"StoryboardSession '{session_id}' not found in workspace '{workspace_id}'"
            )
        try:
            graph = self.graph_store.get_revision(workspace_id, revision_id)
        except Exception as exc:
            raise StoryboardRevisionNotFoundError(revision_id) from exc
        if graph.graph_id != session.graph_id:
            raise StoryboardRevisionNotFoundError(revision_id)
        return self._revision_from_graph(session, graph)

    def latest_revision(self, workspace_id: str, session_id: str) -> Optional[StoryboardRevision]:
        session = self.get_session(workspace_id, session_id)
        if session is None or session.latest_revision_id is None:
            return None
        return self.get_revision(workspace_id, session_id, session.latest_revision_id)

    def list_revisions(self, workspace_id: str, session_id: str) -> List[StoryboardRevision]:
        session = self.get_session(workspace_id, session_id)
        if session is None:
            raise StoryboardRevisionNotFoundError(session_id)
        return [
            self._revision_from_graph(session, graph)
            for graph in self.graph_store.list_revisions(workspace_id, session.graph_id)
        ]

    def _validate_revision_input(
        self,
        *,
        session: StoryboardSession,
        scenes: Sequence[StoryboardScene],
        source_evidence_refs: Sequence[str],
    ) -> None:
        if not source_evidence_refs:
            raise StoryboardRevisionValidationError(
                "storyboard revision requires source_evidence_refs"
            )
        scene_ids = [scene.scene_id for scene in scenes]
        if len(scene_ids) != len(set(scene_ids)):
            raise StoryboardRevisionValidationError("scene_id values must be unique")
        evidence_refs = set(source_evidence_refs)
        for scene in scenes:
            if not scene.source_evidence_refs:
                raise StoryboardRevisionValidationError(
                    f"scene '{scene.scene_id}' has no source evidence lineage"
                )
            if not set(scene.source_evidence_refs).issubset(evidence_refs):
                raise StoryboardRevisionValidationError(
                    f"scene '{scene.scene_id}' references evidence outside revision lineage"
                )
            shot_ids = [shot.shot_id for shot in scene.shots]
            if len(shot_ids) != len(set(shot_ids)):
                raise StoryboardRevisionValidationError("shot_id values must be unique within a scene")
            for shot in scene.shots:
                for element in shot.elements:
                    if not element.source_evidence_refs:
                        raise StoryboardRevisionValidationError(
                            f"element '{element.element_id}' has no source evidence lineage"
                        )
                    if not set(element.source_evidence_refs).issubset(evidence_refs):
                        raise StoryboardRevisionValidationError(
                            f"element '{element.element_id}' references evidence outside revision lineage"
                        )
                    for asset in element.asset_references:
                        if not asset.evidence_refs:
                            raise StoryboardRevisionValidationError(
                                f"asset '{asset.asset_id}' is not evidence-grounded"
                            )
                        if not set(asset.evidence_refs).issubset(evidence_refs):
                            raise StoryboardRevisionValidationError(
                                f"asset '{asset.asset_id}' references evidence outside revision lineage"
                            )
                        if asset.source_quality_profile is not None:
                            profile = asset.source_quality_profile
                            if profile.source_ref != asset.asset_id:
                                raise StoryboardRevisionValidationError(
                                    f"asset '{asset.asset_id}' quality profile is bound to another source"
                                )
                            if not set(profile.evidence_refs).issubset(evidence_refs):
                                raise StoryboardRevisionValidationError(
                                    f"asset '{asset.asset_id}' quality profile references evidence outside revision lineage"
                                )
                    intent = element.transformation_intent
                    recipe = element.transformation_recipe
                    if recipe is not None and (intent is None or recipe.intent_id != intent.intent_id):
                        raise StoryboardRevisionValidationError(
                            f"element '{element.element_id}' has a recipe detached from its intent"
                        )
                    if intent is not None and intent.source_element_id != element.element_id:
                        raise StoryboardRevisionValidationError(
                            f"transformation intent for '{element.element_id}' points at another element"
                        )
                    if recipe is not None:
                        for asset in element.asset_references:
                            profile = asset.source_quality_profile
                            if profile is None:
                                continue
                            quality_result = validate_transformation_for_source_quality(profile, recipe)
                            if not quality_result.allowed:
                                raise StoryboardRevisionValidationError(
                                    f"element '{element.element_id}' transformation exceeds source-quality limits: "
                                    + "; ".join(quality_result.violations)
                                )

        grammar_bindings = [
            scene.narrative_grammar for scene in scenes if scene.narrative_grammar is not None
        ]
        if grammar_bindings:
            if not session.harness_id:
                raise StoryboardRevisionValidationError(
                    "narrative grammar bindings require a canonical session harness_id"
                )
            try:
                report = NarrativeEditingGrammarRegistry.validate_sequence(
                    grammar_bindings,
                    expected_harness_id=session.harness_id,
                    expected_scene_ids=(scene.scene_id for scene in scenes),
                )
            except NarrativeGrammarBindingError as exc:
                raise StoryboardRevisionValidationError(str(exc)) from exc
            if not report.passed:
                raise StoryboardRevisionValidationError(
                    "narrative editing grammar validation failed: "
                    + "; ".join(report.errors)
                )

    def save_revision(
        self,
        *,
        workspace_id: str,
        session_id: str,
        author_id: str,
        scenes: Sequence[StoryboardScene],
        source_evidence_refs: Sequence[str],
        base_revision_id: Optional[str],
        semantic_program_id: Optional[str] = None,
        harness_id: Optional[str] = None,
        status: str = StoryboardSessionStatus.DRAFT,
    ) -> StoryboardRevision:
        session = self.get_session(workspace_id, session_id)
        if session is None:
            raise StoryboardAuthorityError(
                f"StoryboardSession '{session_id}' not found in workspace '{workspace_id}'"
            )
        self._require_editorial_storyboard(workspace_id, session.editorial_storyboard_id)
        self._validate_revision_input(
            session=session,
            scenes=scenes,
            source_evidence_refs=source_evidence_refs,
        )
        payload = {
            "editorial_storyboard_id": session.editorial_storyboard_id,
            "semantic_program_id": semantic_program_id or session.semantic_program_id,
            "harness_id": harness_id or session.harness_id,
            "scenes": [_model_payload(scene) for scene in scenes],
            "source_evidence_refs": list(source_evidence_refs),
            "status": status,
        }
        try:
            graph_revision = self.graph_store.save_graph_revision(
                workspace_id=workspace_id,
                graph_id=session.graph_id,
                base_revision_id=base_revision_id,
                parameters=payload,
                author_id=author_id,
            )
        except CanonicalizationError as exc:
            raise StoryboardRevisionValidationError(
                f"revision payload is not canonicalizable: {exc}"
            ) from exc
        with self.conn:
            self.conn.execute(
                "UPDATE storyboard_session SET latest_revision_id = ?, status = ? "
                "WHERE workspace_id = ? AND session_id = ?",
                (graph_revision.revision_id, StoryboardSessionStatus.IN_REVIEW, workspace_id, session_id),
            )
        return self._revision_from_graph(session, graph_revision)

    def validate_revision(
        self, *, workspace_id: str, session_id: str, revision_id: str
    ) -> StoryboardValidationReport:
        revision = self.get_revision(workspace_id, session_id, revision_id)
        checks: Dict[str, str] = {
            "editorial_storyboard_lineage": "PASS",
            "source_evidence_lineage": "PASS",
            "scene_shot_timing": "PASS",
            "transformation_chain": "PASS",
        }
        grammar_bindings = [
            scene.narrative_grammar for scene in revision.scenes
            if scene.narrative_grammar is not None
        ]
        if grammar_bindings:
            report = NarrativeEditingGrammarRegistry.validate_sequence(
                grammar_bindings,
                expected_harness_id=revision.harness_id,
                expected_scene_ids=(scene.scene_id for scene in revision.scenes),
            )
            checks["narrative_editing_grammar"] = "PASS" if report.passed else "FAIL"
            if not report.passed:
                report_payload = {
                    "workspace_id": workspace_id,
                    "session_id": session_id,
                    "revision_id": revision_id,
                    "passed": False,
                    "checks": checks,
                    "errors": list(report.errors),
                    "warnings": [],
                }
                report_model = StoryboardValidationReport(
                    report_id=f"validation_{revision_id}",
                    report_sha256=canonical_sha256(report_payload),
                    **report_payload,
                )
                with self.conn:
                    self.conn.execute(
                        """
                        INSERT INTO storyboard_validation_report
                        (workspace_id, report_id, session_id, revision_id, passed,
                         checks_json, errors_json, warnings_json, report_sha256, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(workspace_id, revision_id) DO NOTHING
                        """,
                        (
                            report_model.workspace_id, report_model.report_id, report_model.session_id,
                            report_model.revision_id, 0,
                            json.dumps(report_model.checks, sort_keys=True),
                            json.dumps(report_model.errors, sort_keys=True),
                            "[]", report_model.report_sha256, report_model.created_at,
                        ),
                    )
                return report_model
        report_payload = {
            "workspace_id": workspace_id,
            "session_id": session_id,
            "revision_id": revision_id,
            "passed": True,
            "checks": checks,
            "errors": [],
            "warnings": [],
        }
        report = StoryboardValidationReport(
            report_id=f"validation_{revision_id}",
            report_sha256=canonical_sha256(report_payload),
            **report_payload,
        )
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO storyboard_validation_report
                (workspace_id, report_id, session_id, revision_id, passed,
                 checks_json, errors_json, warnings_json, report_sha256, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(workspace_id, revision_id) DO NOTHING
                """,
                (
                    report.workspace_id,
                    report.report_id,
                    report.session_id,
                    report.revision_id,
                    1,
                    json.dumps(report.checks, sort_keys=True),
                    "[]",
                    "[]",
                    report.report_sha256,
                    report.created_at,
                ),
            )
        return self.get_validation_report(workspace_id, revision_id) or report

    def get_validation_report(
        self, workspace_id: str, revision_id: str
    ) -> Optional[StoryboardValidationReport]:
        row = self.conn.execute(
            """
            SELECT report_id, workspace_id, session_id, revision_id, passed,
                   checks_json, errors_json, warnings_json, report_sha256, created_at
            FROM storyboard_validation_report
            WHERE workspace_id = ? AND revision_id = ?
            """,
            (workspace_id, revision_id),
        ).fetchone()
        if row is None:
            return None
        return StoryboardValidationReport(
            report_id=row[0], workspace_id=row[1], session_id=row[2],
            revision_id=row[3], passed=bool(row[4]), checks=json.loads(row[5]),
            errors=json.loads(row[6]), warnings=json.loads(row[7]),
            report_sha256=row[8], created_at=row[9],
        )

    def record_feedback(
        self,
        *,
        workspace_id: str,
        session_id: str,
        revision_id: str,
        operator_id: str,
        decision: str,
        note: Optional[str] = None,
        reason_category: Optional[str] = None,
        feedback_id: Optional[str] = None,
    ) -> OperatorVisualFeedback:
        self.get_revision(workspace_id, session_id, revision_id)
        payload = {
            "workspace_id": workspace_id,
            "session_id": session_id,
            "revision_id": revision_id,
            "operator_id": operator_id,
            "decision": decision.upper(),
            "note": note,
            "reason_category": reason_category,
        }
        feedback = OperatorVisualFeedback(
            feedback_id=feedback_id or f"feedback_{uuid4().hex[:16]}",
            feedback_sha256=canonical_sha256(payload),
            **payload,
        )
        try:
            with self.conn:
                self.conn.execute(
                    """
                    INSERT INTO storyboard_operator_feedback
                    (workspace_id, feedback_id, session_id, revision_id, operator_id,
                     decision, note, reason_category, created_at, feedback_sha256)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        feedback.workspace_id, feedback.feedback_id, feedback.session_id,
                        feedback.revision_id, feedback.operator_id, feedback.decision,
                        feedback.note, feedback.reason_category, feedback.created_at,
                        feedback.feedback_sha256,
                    ),
                )
        except sqlite3.IntegrityError as exc:
            raise StoryboardFeedbackError(
                "feedback for an operator/revision is immutable; create a new revision"
            ) from exc
        return feedback

    def _resolve_final_hit_wrong_reading_locks(
        self,
        *,
        workspace_id: str,
        revision: StoryboardRevision,
        wrong_reading_locks: Optional[Sequence[str]],
    ) -> Optional[Sequence[str]]:
        if wrong_reading_locks is not None:
            return wrong_reading_locks
        if self.editorial_store is not None and revision.semantic_program_id:
            semantic_program = self.editorial_store.get_semantic_program(
                workspace_id, revision.semantic_program_id
            )
            if semantic_program is not None:
                return semantic_program.wrong_reading_locks
        return None

    def validate_final_hit(
        self,
        *,
        workspace_id: str,
        session_id: str,
        revision_id: str,
        format_id: str,
        design_system_ref: Optional[Dict[str, Any]] = None,
        harness_constraints: Optional[Dict[str, Any]] = None,
        wrong_reading_locks: Optional[Sequence[str]] = None,
        strict: bool = True,
    ):
        """Validate an existing canonical revision without mutating persisted state."""
        from ca_runtime.storyboard_final_hit import validate_final_hit as _validate_final_hit

        revision = self.get_revision(workspace_id, session_id, revision_id)
        locks = self._resolve_final_hit_wrong_reading_locks(
            workspace_id=workspace_id,
            revision=revision,
            wrong_reading_locks=wrong_reading_locks,
        )
        return _validate_final_hit(
            revision,
            format_id=format_id,
            design_system_ref=design_system_ref,
            harness_constraints=harness_constraints,
            wrong_reading_locks=locks,
            strict=strict,
        )

    def compile_final_hit(
        self,
        *,
        workspace_id: str,
        session_id: str,
        revision_id: str,
        format_id: str,
        design_system_ref: Optional[Dict[str, Any]] = None,
        harness_constraints: Optional[Dict[str, Any]] = None,
        wrong_reading_locks: Optional[Sequence[str]] = None,
        strict: bool = True,
    ):
        """Compile final-hit projections after deterministic validation; no state mutation."""
        from ca_runtime.storyboard_final_hit import compile_final_hit as _compile_final_hit

        revision = self.get_revision(workspace_id, session_id, revision_id)
        locks = self._resolve_final_hit_wrong_reading_locks(
            workspace_id=workspace_id,
            revision=revision,
            wrong_reading_locks=wrong_reading_locks,
        )
        return _compile_final_hit(
            revision,
            format_id=format_id,
            design_system_ref=design_system_ref,
            harness_constraints=harness_constraints,
            wrong_reading_locks=locks,
            strict=strict,
        )

    def compile_revision(
        self, *, workspace_id: str, session_id: str, revision_id: str
    ) -> StoryboardCompileReceipt:
        revision = self.get_revision(workspace_id, session_id, revision_id)
        report = self.get_validation_report(workspace_id, revision_id)
        if report is None or not report.passed:
            raise StoryboardRevisionValidationError(
                f"revision '{revision_id}' must have a passing validation report before compile"
            )
        feedback = self.conn.execute(
            """
            SELECT decision FROM storyboard_operator_feedback
            WHERE workspace_id = ? AND revision_id = ?
            ORDER BY created_at DESC LIMIT 1
            """,
            (workspace_id, revision_id),
        ).fetchone()
        if feedback is None or feedback[0] != FeedbackDecision.GOOD:
            raise StoryboardFeedbackError(
                "compile requires immutable operator feedback decision GOOD"
            )
        session = self.get_session(workspace_id, session_id)
        assert session is not None
        receipt_payload = {
            "workspace_id": workspace_id,
            "session_id": session_id,
            "revision_id": revision_id,
            "editorial_storyboard_id": session.editorial_storyboard_id,
            "semantic_program_id": revision.semantic_program_id,
            "harness_id": revision.harness_id,
            "validation_report_id": report.report_id,
            "status": "COMPILE_READY",
        }
        receipt = StoryboardCompileReceipt(
            receipt_id=f"compile_{revision_id}",
            lineage_sha256=canonical_sha256(
                {**receipt_payload, "revision_sha256": revision.canonical_sha256}
            ),
            **receipt_payload,
        )
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO storyboard_compile_receipt
                (workspace_id, receipt_id, session_id, revision_id,
                 editorial_storyboard_id, semantic_program_id, harness_id,
                 validation_report_id, status, lineage_sha256, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(workspace_id, revision_id) DO NOTHING
                """,
                (
                    receipt.workspace_id, receipt.receipt_id, receipt.session_id,
                    receipt.revision_id, receipt.editorial_storyboard_id,
                    receipt.semantic_program_id, receipt.harness_id,
                    receipt.validation_report_id, receipt.status,
                    receipt.lineage_sha256, receipt.created_at,
                ),
            )
            self.conn.execute(
                "UPDATE storyboard_session SET status = ? WHERE workspace_id = ? AND session_id = ?",
                (StoryboardSessionStatus.COMPILED, workspace_id, session_id),
            )
        return receipt


__all__ = [
    "FeedbackDecision",
    "MotionPlan",
    "NarrativeGrammarBinding",
    "OperatorVisualFeedback",
    "StoryboardAuthorityError",
    "StoryboardCompileReceipt",
    "StoryboardDomainError",
    "StoryboardElement",
    "StoryboardRevision",
    "StoryboardRevisionNotFoundError",
    "StoryboardRevisionValidationError",
    "StoryboardScene",
    "StoryboardSession",
    "StoryboardSessionStatus",
    "StoryboardSessionStore",
    "StoryboardShot",
    "StoryboardValidationReport",
    "SourceQualityProfile",
    "TransformationIntent",
    "TransformationRecipe",
    "TransformationValidationResult",
    "adapt_transformation_recipe_for_source_quality",
    "validate_transformation_for_source_quality",
    "VisualAssetReference",
]
