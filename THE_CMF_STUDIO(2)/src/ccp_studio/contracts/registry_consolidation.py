"""Canonical registry consolidation contracts."""

from __future__ import annotations

import hashlib
import json
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator


class CanonicalRegistryNamespace(str, Enum):
    primitive_meaning = "registry.primitive.meaning"
    primitive_experience = "registry.primitive.experience"
    methodology = "registry.methodology"
    content_archetype = "registry.content.archetype"
    content_asset_derivative = "registry.content.asset_derivative"
    content_meme_mechanism = "registry.content.meme_mechanism"
    content_reaction_archetype = "registry.content.reaction_archetype"
    sequence_pattern = "registry.sequence.pattern"
    composition_template = "registry.composition.template"
    composition_frame_profile = "registry.composition.frame_profile"
    visual_style_route = "registry.visual.style_route"
    visual_motion_skill = "registry.visual.motion_skill"
    asset_class = "registry.asset.class"
    asset_role = "registry.asset.role"
    provider_capability = "registry.provider.capability"
    eval_rubric = "registry.eval.rubric"
    agent_role = "registry.agent.role"
    skill_binding = "registry.skill.binding"
    ontology = "registry.ontology"


RegistryNamespace = CanonicalRegistryNamespace


class CanonicalRegistryStatus(str, Enum):
    draft = "draft"
    active = "active"
    blocked = "blocked"
    deprecated = "deprecated"
    reference_only = "reference_only"


class CanonicalRegistryEntry(BaseModel):
    schema_version: Literal["cmf.canonical_registry_entry.v1"] = "cmf.canonical_registry_entry.v1"
    canonical_registry_entry_id: UUID = Field(default_factory=uuid4)
    namespace: CanonicalRegistryNamespace
    entry_id: str = Field(min_length=1)
    version: str = Field(default="1.0.0", min_length=1)
    status: CanonicalRegistryStatus = CanonicalRegistryStatus.draft
    display_name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)
    required_inputs: list[str] = Field(default_factory=list)
    compatible_frame_profiles: list[str] = Field(default_factory=list)
    compatible_content_archetypes: list[str] = Field(default_factory=list)
    primitive_affinities: list[str] = Field(default_factory=list)
    eval_rubric_refs: list[str] = Field(default_factory=list)
    provider_capability_refs: list[str] = Field(default_factory=list)
    source_docs: list[str] = Field(default_factory=list)
    owner_component: str = Field(min_length=1)
    content_hash: str = Field(min_length=1)

    @model_validator(mode="after")
    def hash_matches_payload(self):
        payload = self.model_dump(mode="json", exclude={"content_hash"})
        expected = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
        if self.content_hash != expected:
            raise ValueError("content_hash must equal sha256 of canonical registry entry payload")
        return self


class RegistryCrosswalkEntry(BaseModel):
    schema_version: Literal["cmf.registry_crosswalk_entry.v1"] = "cmf.registry_crosswalk_entry.v1"
    source_path: str = Field(min_length=1)
    source_family: str | None = None
    canonical_namespace: CanonicalRegistryNamespace
    canonical_entry_id: str = Field(min_length=1)
    action: Literal["keep", "move", "merge", "split", "wrap", "deprecate", "manual_review"]
    rationale: str = Field(min_length=1)


class RegistryConsolidationManifest(BaseModel):
    schema_version: Literal["cmf.registry_consolidation_manifest.v1"] = "cmf.registry_consolidation_manifest.v1"
    registry_consolidation_manifest_id: UUID = Field(default_factory=uuid4)
    source_registry_root: str = Field(min_length=1)
    canonical_registry_root: str = Field(min_length=1)
    crosswalk: list[RegistryCrosswalkEntry] = Field(default_factory=list)
    canonical_entries: list[CanonicalRegistryEntry] = Field(default_factory=list)
    blocked_sources: list[str] = Field(default_factory=list)
    content_hash: str = Field(min_length=1)

    @model_validator(mode="after")
    def hash_matches(self):
        payload = self.model_dump(mode="json", exclude={"content_hash"})
        expected = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
        if self.content_hash != expected:
            raise ValueError("content_hash must equal sha256 of registry consolidation manifest payload")
        return self


def canonical_registry_entry_hash(entry: CanonicalRegistryEntry | dict) -> str:
    if isinstance(entry, CanonicalRegistryEntry):
        payload = entry.model_dump(mode="json", exclude={"content_hash"})
    else:
        payload = {k: v for k, v in entry.items() if k != "content_hash"}
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def registry_consolidation_manifest_hash(manifest: RegistryConsolidationManifest | dict) -> str:
    if isinstance(manifest, RegistryConsolidationManifest):
        payload = manifest.model_dump(mode="json", exclude={"content_hash"})
    else:
        payload = {k: v for k, v in manifest.items() if k != "content_hash"}
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
