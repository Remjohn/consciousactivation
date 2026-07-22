"""Doctrine and primitive evaluation registry contracts."""

from __future__ import annotations

from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.evaluation_receipts import EvaluationCategory, EvaluationObjectType


class DoctrineEvalDecision(str, Enum):
    selected = "selected"
    not_applicable = "not_applicable"
    blocked = "blocked"


class DoctrineEvidenceRequirement(BaseModel):
    schema_version: Literal["cmf.doctrine_evidence_requirement.v1"] = "cmf.doctrine_evidence_requirement.v1"
    route: str = Field(min_length=1)
    description: str = Field(min_length=1)
    blocking: bool = True
    maps_to_category: EvaluationCategory


class PrimitiveEvalObligation(BaseModel):
    schema_version: Literal["cmf.primitive_eval_obligation.v1"] = "cmf.primitive_eval_obligation.v1"
    primitive_family: str = Field(min_length=1)
    registry_ref: str | None = None
    obligation: str = Field(min_length=1)
    evidence_route: str = Field(min_length=1)
    blocking: bool = True


class DoctrineEvalDefinition(BaseModel):
    schema_version: Literal["cmf.doctrine_eval_definition.v1"] = "cmf.doctrine_eval_definition.v1"
    eval_definition_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    object_types: list[EvaluationObjectType] = Field(min_length=1)
    pipeline_stages: list[str] = Field(min_length=1)
    required_categories: list[EvaluationCategory] = Field(min_length=1)
    source_doctrine_refs: list[str] = Field(min_length=1)
    evidence_requirements: list[DoctrineEvidenceRequirement] = Field(min_length=1)
    primitive_obligations: list[PrimitiveEvalObligation] = Field(min_length=1)
    threshold: float = Field(ge=0, le=1)
    hard_failure_codes: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def required_categories_cover_requirements(self):
        mapped = {requirement.maps_to_category for requirement in self.evidence_requirements}
        missing = [category.value for category in mapped if category not in self.required_categories]
        if missing:
            raise ValueError(f"required_categories missing mapped evidence categories: {', '.join(missing)}")
        return self


class DoctrineEvalTargetInput(BaseModel):
    schema_version: Literal["cmf.doctrine_eval_target_input.v1"] = "cmf.doctrine_eval_target_input.v1"
    organization_id: UUID
    brand_id: UUID
    object_type: EvaluationObjectType
    object_id: UUID
    object_hash: str = Field(min_length=1)
    actor_id: UUID
    pipeline_stage: str = Field(min_length=1)
    route_refs: list[str] = Field(default_factory=list)
    doctrine_refs: list[str] = Field(default_factory=list)
    evidence_routes: dict[str, list[str]] = Field(default_factory=dict)
    primitive_families: list[str] = Field(default_factory=list)
    primitive_refs: list[str] = Field(default_factory=list)
    expected_coalition_refs: list[str] = Field(default_factory=list)
    expected_edge_product_refs: list[str] = Field(default_factory=list)
    hard_negative_refs: list[str] = Field(default_factory=list)


class DoctrineEvalSelection(BaseModel):
    schema_version: Literal["cmf.doctrine_eval_selection.v1"] = "cmf.doctrine_eval_selection.v1"
    doctrine_eval_selection_id: UUID
    eval_definition_id: str
    decision: DoctrineEvalDecision
    missing_evidence_routes: list[str] = Field(default_factory=list)
    missing_primitive_families: list[str] = Field(default_factory=list)
    missing_source_doctrine_refs: list[str] = Field(default_factory=list)
    selected_categories: list[EvaluationCategory] = Field(default_factory=list)


def new_doctrine_eval_selection(
    *,
    definition: DoctrineEvalDefinition,
    decision: DoctrineEvalDecision,
    missing_evidence_routes: list[str],
    missing_primitive_families: list[str],
    missing_source_doctrine_refs: list[str],
) -> DoctrineEvalSelection:
    return DoctrineEvalSelection(
        doctrine_eval_selection_id=uuid4(),
        eval_definition_id=definition.eval_definition_id,
        decision=decision,
        missing_evidence_routes=missing_evidence_routes,
        missing_primitive_families=missing_primitive_families,
        missing_source_doctrine_refs=missing_source_doctrine_refs,
        selected_categories=definition.required_categories,
    )
