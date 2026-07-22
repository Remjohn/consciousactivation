"""Canonical ontology and convergence contracts for CCP Studio.

These contracts are the bridge between docs, bundles, registries, and runtime code.
They are intentionally small, strict, and portable: the glossary is not a prose
document; it is a machine-readable planning artifact used to converge contracts.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.orchestration import utc_now


class OntologyLayer(str, Enum):
    doctrine = "doctrine"
    brand_workspace = "brand_workspace"
    primitive_system = "primitive_system"
    reasoning_methodology = "reasoning_methodology"
    research = "research"
    interview_intelligence = "interview_intelligence"
    content_strategy = "content_strategy"
    sequencing = "sequencing"
    creative_ingredients = "creative_ingredients"
    asset_intelligence = "asset_intelligence"
    visual_style_motion = "visual_style_motion"
    visual_preproduction = "visual_preproduction"
    composition = "composition"
    component_engines = "component_engines"
    providers_tools = "providers_tools"
    render_timeline = "render_timeline"
    evaluation_review = "evaluation_review"
    publishing_memory = "publishing_memory"


class OntologyTermType(str, Enum):
    doctrine = "doctrine"
    primitive = "primitive"
    methodology = "methodology"
    contract = "contract"
    registry = "registry"
    component = "component"
    engine = "engine"
    agent = "agent"
    skill = "skill"
    provider = "provider"
    model = "model"
    asset = "asset"
    library = "library"
    composition = "composition"
    format = "format"
    style = "style"
    workflow = "workflow"
    eval = "eval"
    receipt = "receipt"
    ui_surface = "ui_surface"
    storage_object = "storage_object"


class OntologyStatus(str, Enum):
    canonical = "canonical"
    canonical_to_create = "canonical_to_create"
    partial_existing = "partial_existing"
    legacy_alias = "legacy_alias"
    deprecated = "deprecated"
    candidate = "candidate"


class MigrationAction(str, Enum):
    keep = "keep"
    extend = "extend"
    wrap = "wrap"
    merge = "merge"
    split = "split"
    rename = "rename"
    replace = "replace"
    deprecate = "deprecate"
    create = "create"


class OntologyTerm(BaseModel):
    schema_version: Literal["cmf.ontology_term.v1"] = "cmf.ontology_term.v1"
    term_id: str = Field(min_length=1)
    canonical_name: str = Field(min_length=1)
    aliases: list[str] = Field(default_factory=list)
    term_type: OntologyTermType
    layer: OntologyLayer
    definition: str = Field(min_length=1)
    source_of_truth: str | None = None
    existing_code_refs: list[str] = Field(default_factory=list)
    existing_doc_refs: list[str] = Field(default_factory=list)
    bundle_refs: list[str] = Field(default_factory=list)
    owner_component: str = Field(min_length=1)
    used_by: list[str] = Field(default_factory=list)
    depends_on: list[str] = Field(default_factory=list)
    produces: list[str] = Field(default_factory=list)
    invariants: list[str] = Field(default_factory=list)
    failure_modes: list[str] = Field(default_factory=list)
    status: OntologyStatus
    migration_action: MigrationAction

    @model_validator(mode="after")
    def canonical_terms_need_source_or_action(self):
        if self.status == OntologyStatus.canonical and not self.source_of_truth:
            raise ValueError("canonical ontology terms require source_of_truth")
        if self.migration_action in {MigrationAction.replace, MigrationAction.deprecate} and not (
            self.existing_code_refs or self.existing_doc_refs or self.bundle_refs
        ):
            raise ValueError("replacement/deprecation actions require at least one referenced source")
        return self


class OntologyGlossaryManifest(BaseModel):
    schema_version: Literal["cmf.ontology_glossary_manifest.v1"] = "cmf.ontology_glossary_manifest.v1"
    ontology_glossary_manifest_id: UUID = Field(default_factory=uuid4)
    generated_at: datetime = Field(default_factory=utc_now)
    source_refs: list[str] = Field(min_length=1)
    terms: list[OntologyTerm] = Field(default_factory=list)
    content_hash: str = Field(min_length=1)

    @model_validator(mode="after")
    def hash_matches_terms(self):
        canonical = json.dumps(
            [term.model_dump(mode="json") for term in self.terms],
            sort_keys=True,
            separators=(",", ":"),
        )
        expected = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        if self.content_hash != expected:
            raise ValueError("content_hash must equal sha256 of canonical term payload")
        return self


class IntegrationMatrixDecision(BaseModel):
    schema_version: Literal["cmf.integration_matrix_decision.v1"] = "cmf.integration_matrix_decision.v1"
    integration_matrix_decision_id: UUID = Field(default_factory=uuid4)
    concept_id: str = Field(min_length=1)
    canonical_name: str = Field(min_length=1)
    ontology_term_id: str | None = None
    existing_code_refs: list[str] = Field(default_factory=list)
    existing_doc_refs: list[str] = Field(default_factory=list)
    bundle_refs: list[str] = Field(default_factory=list)
    canonical_target_refs: list[str] = Field(default_factory=list)
    action: MigrationAction
    rationale: str = Field(min_length=1)
    risk_level: Literal["low", "medium", "high"] = "medium"
    owner_component: str = Field(min_length=1)
    implementation_status: Literal["planned", "in_progress", "implemented", "blocked", "deprecated"] = "planned"


class IntegrationMatrixRow(BaseModel):
    schema_version: Literal["cmf.integration_matrix_row.v1"] = "cmf.integration_matrix_row.v1"
    concept_id: str = Field(min_length=1)
    canonical_name: str = Field(min_length=1)
    ontology_layer: OntologyLayer
    term_type: OntologyTermType
    current_contract_path: str | None = None
    canonical_contract_path: str | None = None
    current_registry_path: str | None = None
    canonical_registry_namespace: str | None = None
    migration_action: MigrationAction
    owner_component: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    status: Literal["planned", "in_progress", "implemented", "blocked"] = "planned"


class CanonicalContractPath(BaseModel):
    schema_version: Literal["cmf.canonical_contract_path.v1"] = "cmf.canonical_contract_path.v1"
    path: str = Field(min_length=1)
    module_name: str = Field(min_length=1)
    canonical_since: Literal["v1"] = "v1"
    frozen: bool = True
    migration_adr_required: bool = True
    owner_component: str = "contract_convergence"
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def frozen_paths_require_migration_adr(self):
        if self.frozen and not self.migration_adr_required:
            raise ValueError("frozen canonical contract paths require a migration ADR before moving")
        if not self.path.startswith("src/ccp_studio/contracts/"):
            raise ValueError("canonical contract paths must live under src/ccp_studio/contracts/")
        return self


class ContractConvergenceReceipt(BaseModel):
    schema_version: Literal["cmf.contract_convergence_receipt.v1"] = "cmf.contract_convergence_receipt.v1"
    contract_convergence_receipt_id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=utc_now)
    source_contract_refs: list[str] = Field(min_length=1)
    canonical_contract_ref: str = Field(min_length=1)
    decision: MigrationAction
    adapter_required: bool = True
    compatibility_notes: list[str] = Field(default_factory=list)
    test_refs: list[str] = Field(default_factory=list)
    receipt_hash: str = Field(min_length=1)

    @model_validator(mode="after")
    def convergence_hash_matches(self):
        payload = {
            "source_contract_refs": self.source_contract_refs,
            "canonical_contract_ref": self.canonical_contract_ref,
            "decision": self.decision.value,
            "adapter_required": self.adapter_required,
            "compatibility_notes": self.compatibility_notes,
            "test_refs": self.test_refs,
        }
        expected = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
        if self.receipt_hash != expected:
            raise ValueError("receipt_hash must equal sha256 of convergence decision payload")
        return self


def ontology_terms_hash(terms: list[OntologyTerm]) -> str:
    canonical = json.dumps([term.model_dump(mode="json") for term in terms], sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def convergence_receipt_hash(
    *,
    source_contract_refs: list[str],
    canonical_contract_ref: str,
    decision: MigrationAction,
    adapter_required: bool,
    compatibility_notes: list[str] | None = None,
    test_refs: list[str] | None = None,
) -> str:
    payload = {
        "source_contract_refs": source_contract_refs,
        "canonical_contract_ref": canonical_contract_ref,
        "decision": decision.value,
        "adapter_required": adapter_required,
        "compatibility_notes": compatibility_notes or [],
        "test_refs": test_refs or [],
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
