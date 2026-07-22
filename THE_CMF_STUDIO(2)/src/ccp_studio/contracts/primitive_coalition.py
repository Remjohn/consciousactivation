"""Primitive-first contract convergence layer.

The old `PrimitiveTriadContract` remains useful as a simple projection, but the
canonical runtime object is the richer `PrimitiveCoalitionContract`.
"""

from __future__ import annotations

import hashlib
import json
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator


class PrimitivePlane(str, Enum):
    meaning = "meaning"
    experience = "experience"


class PrimitiveBindingRole(str, Enum):
    meaning_transform = "meaning_transform"
    diagnostic_pressure = "diagnostic_pressure"
    narrative_structure = "narrative_structure"
    persuasion_force = "persuasion_force"
    visual_sonic_guidance = "visual_sonic_guidance"
    performance_delivery = "performance_delivery"
    voice_intimacy = "voice_intimacy"
    experience_entry = "experience_entry"
    friction_management = "friction_management"
    feedback_loop = "feedback_loop"
    progression_replay = "progression_replay"
    trust_transfer = "trust_transfer"
    safety_boundary = "safety_boundary"
    format_material = "format_material"
    suppression = "suppression"


class PrimitiveBinding(BaseModel):
    schema_version: Literal["cmf.primitive_binding.v1"] = "cmf.primitive_binding.v1"
    primitive_binding_id: UUID = Field(default_factory=uuid4)
    primitive_id: str = Field(min_length=1)
    primitive_plane: PrimitivePlane
    family: str = Field(min_length=1)
    role: PrimitiveBindingRole
    activation_reason: str = Field(min_length=1)
    required: bool = True
    evidence_refs: list[str] = Field(default_factory=list)
    suppression_conditions: list[str] = Field(default_factory=list)
    misuse_risks: list[str] = Field(default_factory=list)
    eval_targets: dict[str, float] = Field(default_factory=dict)

    @model_validator(mode="after")
    def required_bindings_need_evidence_or_reason(self):
        if self.required and not self.activation_reason:
            raise ValueError("required primitive bindings need activation_reason")
        for value in self.eval_targets.values():
            if value < 0 or value > 1:
                raise ValueError("eval target values must be between 0 and 1")
        return self


class PrimitiveEvaluationTarget(BaseModel):
    schema_version: Literal["cmf.primitive_evaluation_target.v1"] = "cmf.primitive_evaluation_target.v1"
    primitive_evaluation_target_id: UUID = Field(default_factory=uuid4)
    target_ref: str = Field(min_length=1)
    target_kind: Literal["copy", "composition", "provider_job", "render", "asset", "sequence", "interview_brief"]
    required_primitive_ids: list[str] = Field(min_length=1)
    minimum_coverage_score: float = Field(default=0.86, ge=0, le=1)
    max_misuse_risk: float = Field(default=0.18, ge=0, le=1)
    eval_requirements: dict[str, float] = Field(default_factory=dict)

    @model_validator(mode="after")
    def eval_requirements_are_scores(self):
        for value in self.eval_requirements.values():
            if value < 0 or value > 1:
                raise ValueError("primitive evaluation target scores must be between 0 and 1")
        return self


class PrimitiveConflictRule(BaseModel):
    schema_version: Literal["cmf.primitive_conflict_rule.v1"] = "cmf.primitive_conflict_rule.v1"
    conflict_rule_id: UUID = Field(default_factory=uuid4)
    primitive_id: str = Field(min_length=1)
    conflicting_primitive_id: str = Field(min_length=1)
    conflict_reason: str = Field(min_length=1)
    resolution_policy: Literal["suppress_conflicting", "lower_intensity", "route_to_operator", "block"] = "route_to_operator"


class PrimitiveCoalitionContract(BaseModel):
    schema_version: Literal["cmf.primitive_coalition_contract.v1"] = "cmf.primitive_coalition_contract.v1"
    primitive_coalition_contract_id: UUID = Field(default_factory=uuid4)
    brand_id: UUID | None = None
    brand_context_version_id: str | None = None
    source_context_refs: dict[str, str] = Field(default_factory=dict)
    coalition_intent: str = Field(min_length=1)
    primary_bindings: list[PrimitiveBinding] = Field(min_length=1)
    support_bindings: list[PrimitiveBinding] = Field(default_factory=list)
    suppression_bindings: list[PrimitiveBinding] = Field(default_factory=list)
    conflict_rules: list[PrimitiveConflictRule] = Field(default_factory=list)
    coalition_signature: str = Field(min_length=1)
    minimum_coverage_score: float = Field(default=0.86, ge=0, le=1)
    max_misuse_risk: float = Field(default=0.18, ge=0, le=1)
    content_hash: str = Field(min_length=1)

    @model_validator(mode="after")
    def hash_matches_payload(self):
        payload = self.model_dump(mode="json", exclude={"content_hash"}, exclude_none=True)
        expected = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
        if self.content_hash != expected:
            raise ValueError("content_hash must equal sha256 of primitive coalition payload")
        return self


class PrimitiveCoverageResult(BaseModel):
    schema_version: Literal["cmf.primitive_coverage_result.v1"] = "cmf.primitive_coverage_result.v1"
    primitive_id: str = Field(min_length=1)
    coverage_score: float = Field(ge=0, le=1)
    misuse_risk: float = Field(ge=0, le=1)
    evidence: list[str] = Field(default_factory=list)
    failure_flags: list[str] = Field(default_factory=list)


class PrimitiveEvaluationReceipt(BaseModel):
    schema_version: Literal["cmf.primitive_evaluation_receipt.v1"] = "cmf.primitive_evaluation_receipt.v1"
    primitive_evaluation_receipt_id: UUID = Field(default_factory=uuid4)
    primitive_coalition_contract_id: UUID
    evaluated_object_ref: str = Field(min_length=1)
    coverage_results: list[PrimitiveCoverageResult] = Field(default_factory=list)
    overall_coverage_score: float = Field(ge=0, le=1)
    overall_misuse_risk: float = Field(ge=0, le=1)
    decision: Literal["pass", "repair_required", "blocked"]

    @model_validator(mode="after")
    def decision_matches_scores(self):
        if self.decision == "pass" and self.overall_coverage_score < 0.5:
            raise ValueError("pass decision cannot have extremely low coverage")
        return self


def primitive_coalition_hash(contract: PrimitiveCoalitionContract | dict) -> str:
    if isinstance(contract, PrimitiveCoalitionContract):
        payload = contract.model_dump(mode="json", exclude={"content_hash"}, exclude_none=True)
    else:
        payload = {k: v for k, v in contract.items() if k != "content_hash" and v is not None}
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def simple_triad_to_coalition(
    *,
    meaning_transform: str,
    delivery_shape: str,
    format_material: str,
    coalition_intent: str,
    source_context_refs: dict[str, str] | None = None,
) -> PrimitiveCoalitionContract:
    """Compatibility adapter for the legacy PrimitiveTriadContract shape."""
    bindings = [
        PrimitiveBinding(
            primitive_id=meaning_transform,
            primitive_plane=PrimitivePlane.meaning,
            family="legacy_triad",
            role=PrimitiveBindingRole.meaning_transform,
            activation_reason="Projected from legacy PrimitiveTriadContract.meaning_transform.",
        ),
        PrimitiveBinding(
            primitive_id=delivery_shape,
            primitive_plane=PrimitivePlane.meaning,
            family="legacy_triad",
            role=PrimitiveBindingRole.visual_sonic_guidance,
            activation_reason="Projected from legacy PrimitiveTriadContract.delivery_shape.",
        ),
        PrimitiveBinding(
            primitive_id=format_material,
            primitive_plane=PrimitivePlane.experience,
            family="legacy_triad",
            role=PrimitiveBindingRole.format_material,
            activation_reason="Projected from legacy PrimitiveTriadContract.format_material.",
        ),
    ]
    payload = {
        "schema_version": "cmf.primitive_coalition_contract.v1",
        "primitive_coalition_contract_id": str(uuid4()),
        "source_context_refs": source_context_refs or {},
        "coalition_intent": coalition_intent,
        "primary_bindings": [binding.model_dump(mode="json") for binding in bindings],
        "support_bindings": [],
        "suppression_bindings": [],
        "conflict_rules": [],
        "coalition_signature": f"legacy:{meaning_transform}|{delivery_shape}|{format_material}",
        "minimum_coverage_score": 0.86,
        "max_misuse_risk": 0.18,
    }
    payload["content_hash"] = primitive_coalition_hash(payload)
    return PrimitiveCoalitionContract.model_validate(payload)
