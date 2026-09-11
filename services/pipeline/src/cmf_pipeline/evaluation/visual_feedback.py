"""CAE operator visual-feedback contract and evaluation-only projection (M0089).

This module extends the existing ``studio_visual_feedback`` object stream. It does
not create a new storyboard, asset, Design System, or production-rule authority.
Feedback is immutable by construction: every distinct feedback payload receives
its own content-addressed object id, while replaying the same payload through the
same idempotency key returns the existing object.

Evaluation projection is deliberately downstream and read-only. Its labels are
training/benchmark features, not production acceptance rules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from copy import deepcopy
from typing import Any, Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ca_contracts import canonical_sha256, utc_now_rfc3339

from ..domain.errors import PipelineValidationError
from ..domain.validation import reject_noncanonical, require_ref, require_string


FeedbackDecision = Literal["GOOD", "NEEDS_EDIT", "REJECT"]
FeedbackReasonCode = Literal[
    "SOURCE_MISMATCH",
    "WRONG_READING",
    "COMPOSITION",
    "TRANSFORMATION",
    "SOURCE_QUALITY",
    "OTHER",
]
CoordinateSpace = Literal["NORMALIZED_BPS"]


class CanonicalRef(BaseModel):
    """Stable CAE object reference; no mutable payload is embedded."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    object_id: str
    version: str
    sha256: str

    @model_validator(mode="after")
    def validate_reference(self) -> "CanonicalRef":
        try:
            normalized = require_ref(self.model_dump(), "reference")
        except PipelineValidationError as exc:
            raise ValueError(str(exc)) from exc
        if normalized != self.model_dump():
            raise ValueError("reference must use normalized canonical values")
        return self


class FeedbackReason(BaseModel):
    """Optional structured reason, bounded to the existing VAE reason vocabulary."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    code: FeedbackReasonCode
    detail: str | None = Field(default=None, max_length=2000)


class FeedbackRegion(BaseModel):
    """Optional normalized region using integer basis points (0..10000)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    coordinate_space: CoordinateSpace = "NORMALIZED_BPS"
    x_bps: int = Field(ge=0, le=10000)
    y_bps: int = Field(ge=0, le=10000)
    width_bps: int = Field(gt=0, le=10000)
    height_bps: int = Field(gt=0, le=10000)

    @model_validator(mode="after")
    def fit_inside_canvas(self) -> "FeedbackRegion":
        if self.x_bps + self.width_bps > 10000:
            raise ValueError("region x_bps + width_bps must be <= 10000")
        if self.y_bps + self.height_bps > 10000:
            raise ValueError("region y_bps + height_bps must be <= 10000")
        return self


class OperatorActor(BaseModel):
    """Operator identity required for human visual judgment."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    actor_id: str = Field(min_length=1)
    actor_type: Literal["human"]
    product_id: str = Field(min_length=1)
    workflow_role: Literal["operator"]


class VisualFeedbackRecord(BaseModel):
    """Immutable, evidence-linked operator judgment for a storyboard revision."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    feedback_id: str = Field(min_length=1)
    feedback_version: str = "1.0.0"
    workspace_id: str = Field(min_length=1)
    session_id: str = Field(min_length=1)
    campaign_ref: CanonicalRef
    storyboard_revision_ref: CanonicalRef
    element_revision_ref: CanonicalRef | None = None
    affected_scene_ref: CanonicalRef | None = None
    affected_element_ref: CanonicalRef | None = None
    asset_source_ref: CanonicalRef | None = None
    harness_ref: CanonicalRef
    design_system_ref: CanonicalRef
    decision: FeedbackDecision
    reason: FeedbackReason | None = None
    note: str | None = Field(default=None, max_length=4000)
    region: FeedbackRegion | None = None
    operator_actor: OperatorActor
    created_at: str
    feedback_sha256: str

    @model_validator(mode="after")
    def validate_immutable_identity(self) -> "VisualFeedbackRecord":
        core = self.model_dump(mode="json", exclude={"feedback_id", "feedback_sha256"})
        expected_sha = canonical_sha256(core)
        expected_id = f"visual-feedback:{expected_sha}"
        if self.feedback_sha256 != expected_sha:
            raise ValueError("feedback_sha256 does not match immutable feedback payload")
        if self.feedback_id != expected_id:
            raise ValueError("feedback_id must be content-addressed from the immutable feedback payload")
        return self

    @classmethod
    def build(
        cls,
        *,
        workspace_id: str,
        session_id: str,
        campaign_ref: Mapping[str, Any],
        storyboard_revision_ref: Mapping[str, Any],
        harness_ref: Mapping[str, Any],
        design_system_ref: Mapping[str, Any],
        operator_actor: Mapping[str, Any],
        decision: FeedbackDecision,
        element_revision_ref: Mapping[str, Any] | None = None,
        affected_scene_ref: Mapping[str, Any] | None = None,
        affected_element_ref: Mapping[str, Any] | None = None,
        asset_source_ref: Mapping[str, Any] | None = None,
        reason: Mapping[str, Any] | None = None,
        note: str | None = None,
        region: Mapping[str, Any] | None = None,
        created_at: str | None = None,
    ) -> "VisualFeedbackRecord":
        actor_type = operator_actor.get("actor_type")
        workflow_role = operator_actor.get("workflow_role")
        if actor_type != "human" or workflow_role != "operator":
            raise PipelineValidationError(
                "visual feedback requires a human operator actor"
            )
        core = {
            "feedback_version": "1.0.0",
            "workspace_id": require_string(workspace_id, "workspace_id"),
            "session_id": require_string(session_id, "session_id"),
            "campaign_ref": dict(require_ref(campaign_ref, "campaign_ref")),
            "storyboard_revision_ref": dict(
                require_ref(storyboard_revision_ref, "storyboard_revision_ref")
            ),
            "element_revision_ref": (
                dict(require_ref(element_revision_ref, "element_revision_ref"))
                if element_revision_ref is not None
                else None
            ),
            "affected_scene_ref": (
                dict(require_ref(affected_scene_ref, "affected_scene_ref"))
                if affected_scene_ref is not None
                else None
            ),
            "affected_element_ref": (
                dict(require_ref(affected_element_ref, "affected_element_ref"))
                if affected_element_ref is not None
                else None
            ),
            "asset_source_ref": (
                dict(require_ref(asset_source_ref, "asset_source_ref"))
                if asset_source_ref is not None
                else None
            ),
            "harness_ref": dict(require_ref(harness_ref, "harness_ref")),
            "design_system_ref": dict(
                require_ref(design_system_ref, "design_system_ref")
            ),
            "decision": decision,
            "reason": deepcopy(dict(reason)) if reason is not None else None,
            "note": note,
            "region": deepcopy(dict(region)) if region is not None else None,
            "operator_actor": dict(operator_actor),
            "created_at": created_at or utc_now_rfc3339(),
        }
        reject_noncanonical(core)
        semantic_id = canonical_sha256(core)
        record_id = f"visual-feedback:{semantic_id}"
        payload = {"feedback_id": record_id, **core}
        payload["feedback_sha256"] = canonical_sha256(core)
        return cls.model_validate(payload)


class VisualFeedbackRepository(Protocol):
    def store_object(
        self,
        object_type: str,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        object_id: str,
        semantic_version: str = "1.0.0",
        lifecycle_state: str = "ACTIVE",
        authority_state: str = "candidate_not_current",
        expected_revision: int | None = None,
        now: str | None = None,
    ) -> dict[str, Any]: ...

    def list_objects(self, *, object_type: str | None = None) -> list[dict[str, Any]]: ...

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        relation_type: str,
        *,
        evidence: Mapping[str, Any] | None = None,
        now: str | None = None,
    ) -> dict[str, Any]: ...


_DECISION_LABELS: dict[str, tuple[str, int]] = {
    "GOOD": ("POSITIVE", 10000),
    "NEEDS_EDIT": ("REVISION_NEEDED", 5000),
    "REJECT": ("NEGATIVE", 0),
}


CONTRASTIVE_EXAMPLES: tuple[dict[str, Any], ...] = (
    {
        "example_id": "m0089-good-looking-but-wrong-source",
        "decision": "REJECT",
        "reason": {
            "code": "WRONG_READING",
            "detail": "A polished zoom and highlight makes the frame look premium but changes the source claim being evidenced.",
        },
        "presentation": "A high-contrast crop enlarges a secondary phrase while the actual evidence remains outside the crop.",
        "why_good_looking_is_wrong": "Visual polish cannot override source lineage or semantic reading.",
        "invariant_violated": "source_truth_and_wrong_reading_locks",
    },
    {
        "example_id": "m0089-good-looking-but-damaging-source",
        "decision": "NEEDS_EDIT",
        "reason": {
            "code": "SOURCE_QUALITY",
            "detail": "A smooth cinematic push-in looks intentional but magnifies compression artifacts in already-cropped footage.",
        },
        "presentation": "A strong animated reframe fills the canvas and reads as visually sophisticated.",
        "why_good_looking_is_wrong": "The treatment makes source degradation more salient and should be reduced or replaced.",
        "invariant_violated": "source_quality_governs_treatment",
    },
)


def _evaluation_record_from_object(item: Mapping[str, Any]) -> dict[str, Any]:
    object_id = require_string(item.get("object_id"), "feedback_object.object_id")
    payload = item.get("payload")
    if not isinstance(payload, Mapping):
        raise PipelineValidationError("feedback object payload must be an object")
    decision = str(payload.get("decision", "")).upper()
    if decision not in _DECISION_LABELS:
        raise PipelineValidationError(
            f"feedback object '{object_id}' has unsupported decision '{decision}'"
        )
    label, score = _DECISION_LABELS[decision]
    revision_ref = payload.get("storyboard_revision_ref") or payload.get("revision_ref")
    if revision_ref is None:
        revision_ref = None
    normalized: dict[str, Any] = {
        "evaluation_record_id": f"visual-feedback-eval:{object_id}",
        "feedback_object_ref": {
            "object_id": object_id,
            "version": str(item.get("semantic_version", "1.0.0")),
            "sha256": str(item.get("canonical_sha256", "")),
        },
        "decision": decision,
        "evaluation_label": label,
        "evaluation_rank_score_bps": score,
        "campaign_ref": payload.get("campaign_ref"),
        "storyboard_revision_ref": revision_ref,
        "element_revision_ref": payload.get("element_revision_ref"),
        "affected_scene_ref": payload.get("affected_scene_ref"),
        "affected_element_ref": payload.get("affected_element_ref"),
        "asset_source_ref": payload.get("asset_source_ref") or payload.get("target_ref"),
        "harness_ref": payload.get("harness_ref"),
        "design_system_ref": payload.get("design_system_ref"),
        "reason": payload.get("reason"),
        "reason_code": (
            payload.get("reason", {}).get("code")
            if isinstance(payload.get("reason"), Mapping)
            else payload.get("reason") or payload.get("reason_category")
        ),
        "note": payload.get("note"),
        "region": payload.get("region"),
        "operator_actor": payload.get("operator_actor"),
        "created_at": payload.get("created_at"),
        "production_rule_effect": "NONE",
        "operator_judgment_required": True,
    }
    reject_noncanonical(normalized)
    return normalized


def build_visual_feedback_evaluation_dataset(
    feedback_objects: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    """Project immutable feedback objects into an evaluation-only dataset."""

    records = [
        _evaluation_record_from_object(item)
        for item in feedback_objects
    ]
    records.sort(key=lambda item: (str(item.get("created_at") or ""), item["evaluation_record_id"]))
    dataset_core = {
        "dataset_id": "visual-operator-feedback",
        "dataset_version": "1.0.0",
        "source_object_type": "studio_visual_feedback",
        "record_count": len(records),
        "records": records,
        "contrastive_examples": [deepcopy(item) for item in CONTRASTIVE_EXAMPLES],
        "production_rules_mutated": False,
    }
    dataset_sha256 = canonical_sha256(dataset_core)
    return {**dataset_core, "dataset_sha256": dataset_sha256}


class VisualFeedbackService:
    """Canonical writer + evaluation projection for the existing feedback stream."""

    OBJECT_TYPE = "studio_visual_feedback"

    def __init__(self, repository: VisualFeedbackRepository):
        self.repository = repository

    def record(self, record: VisualFeedbackRecord, *, idempotency_key: str | None = None) -> dict[str, Any]:
        payload = record.model_dump(mode="json")
        stored = self.repository.store_object(
            self.OBJECT_TYPE,
            payload,
            idempotency_key=idempotency_key or record.feedback_id,
            object_id=record.feedback_id,
            semantic_version=record.feedback_version,
            lifecycle_state=record.decision,
        )
        self.repository.add_edge(
            record.storyboard_revision_ref.object_id,
            record.feedback_id,
            "visual_operator_feedback",
            evidence={"feedback_sha256": record.feedback_sha256},
        )
        if record.asset_source_ref is not None:
            self.repository.add_edge(
                record.asset_source_ref.object_id,
                record.feedback_id,
                "visual_feedback_source",
                evidence={"feedback_sha256": record.feedback_sha256},
            )
        return stored

    def project_evaluation_dataset(self) -> dict[str, Any]:
        objects = self.repository.list_objects(object_type=self.OBJECT_TYPE)
        return build_visual_feedback_evaluation_dataset(objects)
