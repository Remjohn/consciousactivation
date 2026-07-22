# Tech-Spec: FR-ERA3-20 - SDA Ontology and Registry
**Created:** 2026-05-12  
**Status:** Ready for Development  
**Version:** 1.0 (ERA3 Architecture - SDA Foundation)  
**Phase:** 6 - Semantic Discernment Foundation  
**Architecture Reference:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`

---

## Pre-Work Log

```text
1. PROTOCOL LOADED:   ERA3_Tech_Spec_Writing_Protocol.md. Confirmed 10-section spec structure, architecture traceability requirement, typed model expectation, receipt-chain logging patterns, and file-read log requirement.
2. PRD LOADED:        PRD-01 Â§3.4 + Brownfield Â§1.5. Confirmed platform-level SDA adoption, scalar separation law (`Invariant Gravity`, `Invariant Activation Intensity`, `Invariant Resonance Multiplier`), and the rule that Existential Invariants are deepest pressure fields while Perceptual Primitives are operators over that field.
3. PRD LOADED:        PRD-02 Â§3.1/Â§3.2/Â§3.4A. Confirmed new SDA packet expectations (`InvariantFieldPacket`, `ArchetypalGeometryPacket`, `RepresentationGeometryPacket`, `SpeciesHypothesisPacket`, `DirectionalIntegrityReport`, `HardNegativeEvaluationReport`) and updated compiler law: `signal -> coach reaction -> invariant field -> primitive coalition -> edge product -> archetypal geometry check -> archetype container -> directional integrity validation -> JIT script contract -> render blueprint`.
4. PRD LOADED:        PRD-08 Â§3.2/Â§3.6/Â§4. Confirmed primitives are transformation operators, not deep ontology; SDA artifacts are sibling intelligence structures, not new primitive families; and `primitives are not edges`.
5. SDA CORE DOC LOADED: lab/semantic_discernment_architecture_content_engine_v_1.md. Confirmed the motivating problem is deceptively close failure and the canonical concepts are existential invariants, archetypes, content species, representation geometry, hard negatives, recursive discernment, and directional integrity.
6. SDA TAXONOMY LOADED: lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md. Confirmed artifact-class split:
   - Canonical Ontology: Existential Invariant, Representation Geometry
   - Canonical Structural Grammar: Archetypal Geometry, Species Composition Grammar
   - Runtime-Derived Semantic Form: Content Species, Edge Product
   - Runtime Dynamics: Recursive Pattern, Emergent Contextual Invariant, Feedback Loop
   - Validation / Adversarial: Directional Integrity Policy, Hard Negative, Mutation Stress Suite
   Also confirmed `Role-before-schema`, `No false registry`, `Canonical/derived separation`, and `Scalar separation` rules.
7. PPA / EDGING DOCS LOADED:
   - Perceptual_Primitives_Architecture.md: `CRAL evidence -> primitive spaces -> candidate survival -> coalition signature -> edge product -> CCF routing`
   - Matrix of Edging.md: edging is the force-selection layer; experience primitives are the force-delivery layer.
   These documents confirm that FR-ERA3-20 must NOT collapse edge products into primitive ontology and must keep broad-signal selection separate from canonical SDA registries.
8. PRIMITIVE YAMLs VERIFIED:
   - EXP-TRS-003 = "Reflective Social Proof (The Status Share)"
   - EXP-PRG-002 = "Discover -> On-board -> Immerse -> Master -> Replay"
   - PRM-HUM-001 = "Dual-Processor Cognitive Engine"
   - PRM-BUS-001 = "Perception and Guidance Stack"
   Verified current repository convention: canonical IDs, aliases, source audits, book_reference, summary/core_move/why_it_works, fit matrices, activation conditions, suppression conditions, conflicts/synergies, and optional `crosswalk_id`.
9. BACKEND FILES READ:
   - src/ccp/services/visual_format_constraint_adapter.py - deterministic registry loader, sealed envelope, staged receipts, tamper detection pattern
   - src/ccp/services/known_persons_registry_adapter.py - multi-stage resolution pipeline, registry query, hard prohibition guard, receipt-chain logging
   - src/ccp/services/tiar_adapter.py - fresh/stale registry query, active-vs-blocked partitioning, downstream revalidation pattern
   - src/ccp/services/semantic_affinity_guard.py - deterministic scalar-threshold gate, fallback states, fail-closed / operator-review pattern
   - src/ccp/services/research_synthesis_protocol.py - deterministic conflict classes, auto-resolve vs operator-flag vs terminal-block pattern
10. MODEL / TEST PATTERNS READ:
   - src/ccp/models/visual_engine_models.py contains `FormatRegistryEntry`, `FormatConstraintEnvelope`, `TIARNounEntry`, `TIARInjectionResult`, `TIARValidationResult`, `KnownPersonRegistryEntry`
   - tests/integration/test_vis07_format_constraint.py asserts registry completeness, hash sealing, staged receipts, and safety failures
   - tests/integration/test_vis12_known_persons.py asserts context matrix, repetition rules, and hard prohibitions
   - tests/integration/test_vis02_tiar_integration.py asserts active/blocked partitioning, stale-cache fallback, downstream revalidation, and audit completeness
11. WAVE-0 DOCTRINE CHECK: No dedicated Phase 6 epic file exists yet. This spec therefore uses the Wave-0 PRD updates plus the four SDA source documents as the authoritative traceability base.
```

---

## 1. Files Read

| # | File | Date/Version | Purpose |
|---|------|--------------|---------|
| 1 | `docs/architecture/april_updates/spec_prompts/P6_S35_FR-ERA3-20_SDA_Ontology_And_Registry.md` | 2026-05-12 | Prompt source, scope boundary, mandatory reading set |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | 2026-05-08 | Spec-writing protocol and architecture format |
| 3 | `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md` | v6.0, 2026-05-06 | Platform-level SDA doctrine and Brownfield Wave-0 update |
| 4 | `reference/conscious-rivers/docs/prd/modules/PRD_02_CCF_Content_Factory.md` | v6.0, 2026-05-06 | SDA packet dependencies and updated compiler runtime law |
| 5 | `reference/conscious-rivers/docs/prd/modules/PRD_08_Conscious_Primitives.md` | v6.0, 2026-05-06 | Primitive/SDA boundary and plane separation |
| 6 | `lab/semantic_discernment_architecture_content_engine_v_1.md` | 2026-05-12 source-of-truth lab doc | Meaning problem statement and SDA conceptual stack |
| 7 | `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md` | 2026-05-12 proposed source of truth | Formal SDA artifact taxonomy and governance rules |
| 8 | `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md` | 2026-05-02 | Primitive spaces, candidate survival, coalition, edge product sequence |
| 9 | `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md` | 2026-05-03 | Broad signal vs edge-product distinction and force-selection doctrine |
| 10 | `primitives/experience/trust_branding/EXP-TRS-003.yaml` | Current repo artifact | Existing YAML registry shape and crosswalk precedent |
| 11 | `primitives/experience/progression_replay/EXP-PRG-002.yaml` | Current repo artifact | Existing lifecycle-scaffold registry shape |
| 12 | `primitives/meaning/humor_distortion/PRM-HUM-001.yaml` | Current repo artifact | Existing meaning-plane canonical YAML pattern |
| 13 | `primitives/meaning/design_business/PRM-BUS-001.yaml` | Current repo artifact | Existing crosswalk and fit-matrix pattern |
| 14 | `src/ccp/services/visual_format_constraint_adapter.py` | Current code | Deterministic registry-gate pattern with seal hash |
| 15 | `src/ccp/services/known_persons_registry_adapter.py` | Current code | Multi-stage registry resolution and hard prohibition pattern |
| 16 | `src/ccp/services/tiar_adapter.py` | Current code | Registry query, partition, stale-cache fallback, downstream revalidation |
| 17 | `src/ccp/services/semantic_affinity_guard.py` | Current code | Deterministic threshold gate and fallback states |
| 18 | `src/ccp/services/research_synthesis_protocol.py` | Current code | Deterministic conflict-resolution precedent |
| 19 | `src/ccp/models/visual_engine_models.py` | Current code | Existing registry-entry and audit-result Pydantic style |
| 20 | `tests/integration/test_vis07_format_constraint.py` | Current tests | Registry completeness, sealing, receipts, safety-test pattern |
| 21 | `tests/integration/test_vis12_known_persons.py` | Current tests | Matrix-style acceptance criteria and hard prohibition tests |
| 22 | `tests/integration/test_vis02_tiar_integration.py` | Current tests | Active/blocked partition, stale fallback, audit-completeness test pattern |

---

## 2. Overview

### 2.1 Problem Statement - What breaks without this spec?

SDA doctrine now exists in the PRDs and lab architecture, but the codebase still has no canonical machine-readable substrate for SDA itself. Without FR-ERA3-20:

- **SDA remains prose-only.** `PRD-01`, `PRD-02`, and `PRD-08` now reference `Existential Invariants`, `Representation Geometries`, and `Archetypal Geometries`, but no typed registry exists for loaders or validators to consume.
- **Downstream specs would build on undefined objects.** `FR-ERA3-21` (query/crosswalk), `FR-ERA3-22` (Directional Integrity), `FR-ERA3-23` (Recursive Semantic Dynamics), and `FR-ERA3-24` (Hard Negative Harness) all need canonical IDs, storage layout, and field contracts first.
- **The architecture can drift into false registries.** The taxonomy explicitly warns that not all SDA artifacts are registries. Without this spec, implementers could incorrectly store derived `Content Species`, `Hard Negatives`, or runtime `Feedback Loops` as canonical ontology.
- **Scalar meaning collapses.** The Wave-0 PRD updates made `Invariant Gravity`, `Invariant Activation Intensity`, and `Invariant Resonance Multiplier` distinct architectural measurements. Without a canonical ontology spec, future code will likely flatten them into one generic â€œstrengthâ€ field.
- **Primitive/SDA confusion becomes likely.** `PRD-08` now explicitly says SDA artifacts are not primitive families. Without an actual registry boundary, future implementations will be tempted to put invariants or geometries into `primitives/` and break the architecture.

### 2.2 Solution

This spec establishes the canonical SDA ontology and grammar layer as a **repo-backed, typed, deterministic registry system** with:

- canonical registries for:
  - `Existential Invariants`
  - `Representation Geometries`
  - `Archetypal Geometries`
  - `Species Composition Grammar`
- maintained crosswalk registries for:
  - `Primitive-to-Invariant`
  - `Archetype-to-Geometry`
- a registry manifest and loader service that validates every artifact at startup
- strict governance rules that reject false registry entries such as `Content Species`, `Hard Negatives`, or `Feedback Loops`
- first-class scalar separation:
  - `invariant_gravity` on canonical invariant objects
  - runtime-only scalar placeholders for packet interoperability, but not canonical storage of activation/resonance on registry entries

This is a **foundation spec**, not a query-API or evaluation-engine spec. It defines what the canonical SDA objects are, how they are stored, how they are validated, and how the rest of the architecture can safely depend on them.

### 2.3 Scope

**In scope:**

- canonical storage layout for SDA ontology and structural grammar
- typed Pydantic models for canonical SDA artifact classes
- registry manifest, validation rules, and boot-time loader
- crosswalk registry structures required by future query services
- explicit rejection rules for non-canonical / derived / adversarial artifacts
- registry health and audit outputs
- startup validation and targeted artifact reload support

**Out of scope:**

- public HTTP query API (`FR-ERA3-21`)
- Directional Integrity evaluation logic (`FR-ERA3-22`)
- Recursive Pattern / Emergent Contextual Invariant / Feedback Loop runtime engine (`FR-ERA3-23`)
- Hard Negative corpus and mutation harness (`FR-ERA3-24`)
- canonical `Content Species` registry (taxonomy says species are derived, not canonical)
- embedding, vector search, or inference-time branching policy

---

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source | What It Does |
|--------|-----------|--------|--------------|
| `DEP-SDA-001` | `ExistentialInvariantRecord` | FR-ERA3-20 | Canonical typed record for an existential invariant |
| `DEP-SDA-002` | `RepresentationGeometryRecord` | FR-ERA3-20 | Canonical typed record for representation geometry |
| `DEP-SDA-003` | `ArchetypalGeometryRecord` | FR-ERA3-20 | Canonical typed record for archetypal geometry |
| `DEP-SDA-004` | `SpeciesCompositionRule` | FR-ERA3-20 | Canonical typed record for structural species grammar |
| `DEP-SDA-005` | `SDARegistryManifest` | FR-ERA3-20 | Canonical manifest for directories, versions, counts, and validation state |
| `DEP-SDA-006` | `SDARegistryAuditReport` | FR-ERA3-20 | Structured health/audit result for startup, reload, and CI validation |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|------|------|------------------------|
| `visual_format_constraint_adapter.py` | `src/ccp/services/visual_format_constraint_adapter.py` | **Primary implementation precedent.** This spec follows its deterministic registry load, typed entry model, staged validation, receipt writes, and â€œsealed contract before downstream useâ€ pattern. |
| `known_persons_registry_adapter.py` | `src/ccp/services/known_persons_registry_adapter.py` | **Multi-stage registry precedent.** This spec copies the pattern of query/validate/resolve with explicit hard prohibitions, but replaces person-specific routing with ontology-class validation. |
| `tiar_adapter.py` | `src/ccp/services/tiar_adapter.py` | **Partition and revalidation precedent.** This spec borrows the idea of fresh/stale registry states and downstream revalidation, but uses it for ontology manifests and crosswalk bundles instead of nouns. |
| `semantic_affinity_guard.py` | `src/ccp/services/semantic_affinity_guard.py` | **Deterministic scalar-gate precedent.** This spec follows the explicit threshold, fallback, and fail-closed/operator-review pattern for registry validation errors. |
| `research_synthesis_protocol.py` | `src/ccp/services/research_synthesis_protocol.py` | **Deterministic conflict-pass precedent.** This spec uses the same style of classifying validation failures as auto-resolvable, operator-flag, or terminal-block instead of vague schema warnings. |
| `visual_engine_models.py` | `src/ccp/models/visual_engine_models.py` | **Pydantic style precedent.** `FormatRegistryEntry`, `FormatConstraintEnvelope`, `TIARNounEntry`, and `KnownPersonRegistryEntry` define the repositoryâ€™s current registry-model style. |

### 3.3 SDA Source Doctrine Anchors

| Source | Anchor | Constraint This Spec Must Preserve |
|--------|--------|------------------------------------|
| `semantic_discernment_architecture_content_engine_v_1.md` | Â§Â§3, 4, 6, 7, 9, 11 | Canonical ontology must serve deeper semantic direction, not just style or coherence |
| `semantic_discernment_architecture_artifact_taxonomy_v_1.md` | Â§Â§4, 5, 8 | Artifact classes are distinct; schema follows role; no false registry objects |
| `Perceptual_Primitives_Architecture.md` | Â§Â§2, 3, 8, 15 | Primitives are not edges; edge products are derived and must stay out of canonical ontology |
| `Matrix of Edging.md` | Â§Â§3, 4, 5, 13 | Edging selects force; experience primitives deliver force; ontology must not absorb either responsibility |

### 3.4 SDA Governance Constraints

Because there is no dedicated Phase 6 epic file yet, this section serves as the authoritative governance map for FR-ERA3-20.

| Governance Rule | Source | Enforcement in This Spec |
|-----------------|--------|--------------------------|
| **Role-before-schema** | Taxonomy Â§8.1 | Every artifact type gets a declared class before any field schema is accepted. |
| **No false registry** | Taxonomy Â§8.2 | `Content Species`, `Hard Negatives`, `Recursive Patterns`, `Emergent Contextual Invariants`, and `Feedback Loops` are explicitly rejected from canonical registry directories. |
| **Canonical / derived separation** | Taxonomy Â§8.3 | Only `Existential Invariants`, `Representation Geometries`, `Archetypal Geometries`, and `Species Composition Grammar` may live in the canonical ontology/grammar folders. |
| **Scalar separation** | PRD-01 Â§3.4, Taxonomy Â§8.3A | `invariant_gravity` is stored only on invariant records; `invariant_activation_intensity` and `invariant_resonance_multiplier` are prohibited as canonical registry fields. |
| **Primitive/SDA separation** | PRD-08 Â§3.6 | No SDA artifacts may be stored under `primitives/`; no primitive schemas are extended to â€œbecomeâ€ invariants or geometries. |
| **Slow ontology / fast inference** | Taxonomy Â§8.6 | This spec versions slow-changing ontology/grammar only. Runtime semantic dynamics are deferred to `FR-ERA3-23`. |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|----------|-----------|----------------------|--------------|
| Use repo-backed YAML artifacts under a dedicated `sda/` root | Matches current primitive-registry practice while preserving a hard boundary from `primitives/` | Store SDA inside `primitives/` | Violates PRD-08 Â§3.6 and collapses ontology into operators |
| Build canonical `Species Composition Grammar`, not canonical `Content Species` | Taxonomy explicitly says species are derived semantic forms | Create `content_species/*.yaml` as primary registry | Violates the `No false registry` and `Canonical/derived separation` rules |
| Treat crosswalks as maintained registry artifacts | Future query/crosswalk and DI specs need explicit machine-readable mappings | Derive crosswalks on the fly from prose notes | Too brittle; no deterministic IDs or validation |
| Make the registry internal-only in this spec | Query API belongs to `FR-ERA3-21`; keep this foundation narrow and stable | Expose FastAPI routes now | Blurs responsibility with the next spec and forces unstable public contracts |
| Fail closed on artifact-class violations | Better to block boot/CI than silently accept false ontology objects | Lenient validation with warnings only | Risks doctrinal drift and invalid downstream engine behavior |

---

## 4. Implementation Plan

### Phase A: Canonical Storage Layout and Models (Tasks 1-4)

- [ ] **Task 1:** Create canonical SDA root layout:
  - `sda/registry_manifest.yaml`
  - `sda/ontology/existential_invariants/`
  - `sda/ontology/representation_geometries/`
  - `sda/grammar/archetypal_geometries/`
  - `sda/grammar/species_composition/`
  - `sda/crosswalks/`
- [ ] **Task 2:** Create `src/ccp/models/sda_registry_models.py` with core enums and Pydantic models for all canonical FR-ERA3-20 artifacts.
- [ ] **Task 3:** Add `SDA_ARTIFACT_CLASS`, `SDA_REGISTRY_KIND`, `SCALAR_FIELD_GUARD`, and canonical ID-prefix constants.
- [ ] **Task 4:** Add `SDA_REGISTRY_AUDIT_SQL` and `SDAManifestHealth` / `SDARegistryAuditReport` models for CI and startup health checks.

### Phase B: Loader and Validation Engine (Tasks 5-8)

- [ ] **Task 5:** Create `src/ccp/services/sda_registry_service.py` with `SDARegistryService` and `SDAOntologyValidator`.
- [ ] **Task 6:** Implement manifest-driven recursive loading of ontology, grammar, and crosswalk files into typed Pydantic records.
- [ ] **Task 7:** Enforce artifact-class validation rules:
  - reject unknown `artifact_class`
  - reject misplaced files
  - reject prohibited scalar fields on canonical records
  - reject canonical `ContentSpecies`, `HardNegative`, `RecursivePattern`, `FeedbackLoop` entries
- [ ] **Task 8:** Implement targeted `reload_artifact(path)` support for CI or local authoring flows without requiring full process restart.

### Phase C: Crosswalk and Registry Health Layer (Tasks 9-12)

- [ ] **Task 9:** Implement `SDACrosswalkCompiler` that validates:
  - referenced primitive IDs exist under `primitives/`
  - referenced content archetype names belong to retained PRD-02 inventories
  - referenced invariant/geometry IDs exist in canonical SDA registries
- [ ] **Task 10:** Implement `SDARegistryService.health()` returning counts, version hashes, last load time, rejected artifact list, and manifest consistency.
- [ ] **Task 11:** Implement receipt-chain logging for:
  - startup warm
  - manifest load
  - artifact rejection
  - reload success/failure
  - crosswalk integrity errors
- [ ] **Task 12:** Add developer-safe helper methods:
  - `get_invariant(id)`
  - `get_representation_geometry(id)`
  - `get_archetypal_geometry(id)`
  - `get_species_grammar(rule_id)`
  - `get_crosswalk_bundle(name)`

### Phase D: Verification and Interop Hardening (Tasks 13-16)

- [ ] **Task 13:** Create `tests/integration/test_era3_fr20_sda_registry.py` covering boot load, manifest counts, path discipline, and scalar separation.
- [ ] **Task 14:** Create `tests/integration/test_era3_fr20_sda_crosswalks.py` covering primitive/invariant and archetype/geometry crosswalk integrity.
- [ ] **Task 15:** Add CI-style fixture registries with at least:
  - 3 existential invariants
  - 3 representation geometries
  - 3 archetypal geometries
  - 2 species-composition grammar rules
  - 2 crosswalk bundles
- [ ] **Task 16:** Verify `FR-ERA3-21`, `FR-ERA3-22`, `FR-ERA3-23`, and `FR-ERA3-24` can import these models without redefining the ontology layer.

---

## 5. Primary Output Schema

```python
# src/ccp/models/sda_registry_models.py
from __future__ import annotations

from enum import Enum
from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator


SDA_ROOT = "sda"

INV_PREFIX = "SDA-INV-"
RPG_PREFIX = "SDA-RPG-"
ARG_PREFIX = "SDA-ARG-"
SCG_PREFIX = "SDA-SCG-"
XW_PI_PREFIX = "SDA-XW-PI-"
XW_AG_PREFIX = "SDA-XW-AG-"

PROHIBITED_CANONICAL_CLASSES = {
    "content_species",
    "edge_product",
    "recursive_pattern",
    "emergent_contextual_invariant",
    "feedback_loop",
    "directional_integrity_policy",
    "hard_negative",
    "mutation_stress_suite",
}


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


class TensionAxis(BaseModel):
    primary_pole: str
    counter_pole: str


class SignalIndicators(BaseModel):
    linguistic: list[str] = Field(default_factory=list)
    symbolic: list[str] = Field(default_factory=list)


class DistortionProfile(BaseModel):
    healthy: list[str] = Field(default_factory=list)
    distorted: list[str] = Field(default_factory=list)
    trajectory_risks: list[str] = Field(default_factory=list)


class InvariantReference(BaseModel):
    invariant_id: str
    weight: float = Field(ge=0.0, le=1.0)


class CrosswalkWeight(BaseModel):
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
    def ban_runtime_scalars(cls, data: any) -> any:
        if isinstance(data, dict):
            forbidden = {"invariant_activation_intensity", "invariant_resonance_multiplier"}
            present = forbidden.intersection(data.keys())
            if present:
                raise ValueError(f"Runtime-only scalar(s) forbidden on canonical invariant: {sorted(present)}")
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
    notes: Optional[str] = None

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
    notes: Optional[str] = None

    @field_validator("artifact_id")
    @classmethod
    def enforce_prefix(cls, value: str) -> str:
        if not value.startswith(XW_AG_PREFIX):
            raise ValueError("ArchetypeToGeometryCrosswalk IDs must start with SDA-XW-AG-")
        return value


class SDARegistryManifest(BaseModel):
    manifest_version: str = "1.0"
    ontology_paths: dict[str, str]
    grammar_paths: dict[str, str]
    crosswalk_paths: dict[str, str]
    expected_counts: dict[str, int]
    source_documents: list[str] = Field(min_length=4)


class SDARegistryAuditReport(BaseModel):
    last_load_at: str
    manifest_hash: str
    existential_invariant_count: int = Field(ge=0)
    representation_geometry_count: int = Field(ge=0)
    archetypal_geometry_count: int = Field(ge=0)
    species_composition_rule_count: int = Field(ge=0)
    primitive_to_invariant_crosswalk_count: int = Field(ge=0)
    archetype_to_geometry_crosswalk_count: int = Field(ge=0)
    rejected_artifacts: list[str] = Field(default_factory=list)
    ready: bool = False


SDA_REGISTRY_AUDIT_SQL = '''
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
'''
```

### Canonical Repository Layout

```text
sda/
  registry_manifest.yaml
  ontology/
    existential_invariants/
      SDA-INV-001.yaml
      SDA-INV-002.yaml
    representation_geometries/
      SDA-RPG-001.yaml
      SDA-RPG-002.yaml
  grammar/
    archetypal_geometries/
      SDA-ARG-001.yaml
      SDA-ARG-002.yaml
    species_composition/
      SDA-SCG-001.yaml
      SDA-SCG-002.yaml
  crosswalks/
    primitive_to_invariant/
      SDA-XW-PI-001.yaml
    archetype_to_geometry/
      SDA-XW-AG-001.yaml
```

### Explicit Non-Ownership

The following directories are **forbidden** in `FR-ERA3-20`:

```text
sda/species/                  # rejected - species are derived, not canonical
sda/hard_negatives/           # rejected - owned by FR-ERA3-24
sda/recursive_patterns/       # rejected - owned by FR-ERA3-23
sda/contextual_invariants/    # rejected - owned by FR-ERA3-23
sda/feedback_loops/           # rejected - owned by FR-ERA3-23
```

---

## 6. Backward Compatibility Fallback

This spec is foundational, so its fallback behavior must preserve doctrine before convenience.

1. **Manifest missing but directories present**
   - Behavior: `SDARegistryService` enters `NOT_READY` state and emits `SDA_MANIFEST_MISSING`.
   - Result: boot continues only in explicitly degraded developer mode; production startup fails closed.
   - Rationale: future specs need deterministic manifest-driven counts and paths.

2. **Single artifact malformed**
   - Behavior: artifact is rejected, added to `rejected_artifacts`, and startup fails if the artifact belongs to canonical ontology/grammar and would drop a required count below manifest minimum.
   - Result: no silent partial ontology in production.
   - Rationale: malformed canonical ontology is more dangerous than temporary unavailability.

3. **False registry artifact found**
   - Example: `sda/ontology/content_species/SDA-SPC-001.yaml`
   - Behavior: immediate terminal validation failure with `FALSE_REGISTRY_VIOLATION`.
   - Result: build / boot blocked.
   - Rationale: this is an architectural, not cosmetic, error.

4. **Runtime scalar leaked into canonical artifact**
   - Example: invariant YAML includes `invariant_resonance_multiplier`
   - Behavior: reject artifact with `SCALAR_LAYER_VIOLATION`.
   - Result: no boot readiness.
   - Rationale: protects the Wave-0 scalar distinction adopted in `PRD-01`.

5. **Crosswalk references unknown primitive or unknown geometry**
   - Behavior: reject the crosswalk file, keep canonical ontology loaded, and mark registry `ready = false` until fixed.
   - Result: ontology can still be inspected in dev, but downstream query/DI specs are blocked from promotion.
   - Rationale: crosswalk integrity is mandatory for the next wave.

---

## 7. Tasks

### Sprint 1: Canonical Structures

- [ ] Create `sda/registry_manifest.yaml` with paths, required counts, source-doc references, and version hash fields.
- [ ] Create `src/ccp/models/sda_registry_models.py` with canonical ontology, grammar, and crosswalk models.
- [ ] Define canonical ID-prefix constants and prohibited-class sets.
- [ ] Add `SDA_REGISTRY_AUDIT_SQL` and `SDARegistryAuditReport`.

### Sprint 2: Loader and Validation

- [ ] Create `src/ccp/services/sda_registry_service.py`.
- [ ] Implement manifest-driven startup warm.
- [ ] Implement directory-to-class validation so each folder only accepts its allowed artifact kind.
- [ ] Implement scalar-layer validation so only `invariant_gravity` appears on invariant ontology objects.

### Sprint 3: Crosswalk and Readiness

- [ ] Implement primitive-to-invariant crosswalk validation against `primitives/`.
- [ ] Implement archetype-to-geometry crosswalk validation against the retained PRD-02 archetype inventory.
- [ ] Implement `health()` and `reload_artifact(path)` methods.
- [ ] Implement receipt-chain logs for startup, reject, reload, and health scan actions.

### Sprint 4: Verification

- [ ] Create `tests/integration/test_era3_fr20_sda_registry.py`.
- [ ] Create `tests/integration/test_era3_fr20_sda_crosswalks.py`.
- [ ] Add fixture YAMLs for canonical ontology/grammar and failing-path cases.
- [ ] Validate that upcoming FR-ERA3-21/22/23/24 specs can depend on these models without redefining them.

---

## 8. Acceptance Criteria

### AC-20.1: Canonical Registry Boot and Manifest Integrity

**Given** the repository contains a valid `sda/registry_manifest.yaml` and all required SDA canonical artifact files,  
**When** `SDARegistryService.warm()` runs at startup,  
**Then** it loads every canonical ontology, grammar, and crosswalk file into typed Pydantic models,  
**And** the resulting `SDARegistryAuditReport.ready` is `true`,  
**And** the loaded counts match or exceed the manifestâ€™s required counts.

**FAILURE EXAMPLE:** The service starts with two existential invariants and one archetypal geometry loaded, but the manifest expects three of each and still reports healthy. Downstream engines now operate on an incomplete ontology and silently misclassify meaning. This is a spec violation.

**Measurable pass condition:** warm-start report exposes exact loaded counts, zero terminal manifest mismatches, and `ready == true`.

---

### AC-20.2: No False Registry Objects in Canonical SDA Directories

**Given** a developer adds a YAML file representing a derived or adversarial artifact such as `ContentSpecies`, `HardNegative`, or `FeedbackLoop` under the canonical SDA directories,  
**When** startup validation runs,  
**Then** `SDAOntologyValidator` rejects the file with a deterministic error code,  
**And** the registry does not enter a ready state,  
**And** the receipt chain records the exact path and rejected artifact class.

**FAILURE EXAMPLE:** `sda/ontology/content_species/SDA-SPC-001.yaml` is accepted because its YAML looks well-formed. A later engine now mistakes a derived species snapshot for canonical ontology and hardcodes unstable semantics into production logic. This is a spec violation.

**Measurable pass condition:** every forbidden class in `PROHIBITED_CANONICAL_CLASSES` is rejected at validation time with `FALSE_REGISTRY_VIOLATION`.

---

### AC-20.3: Scalar Separation Is Enforced

**Given** the Wave-0 PRD doctrine distinguishes `Invariant Gravity` from runtime `Invariant Activation Intensity` and `Invariant Resonance Multiplier`,  
**When** an `ExistentialInvariantRecord` is loaded,  
**Then** `invariant_gravity` is accepted as a canonical ontology field,  
**And** runtime-only scalar fields are rejected if present on the canonical record,  
**And** the failure is classified as `SCALAR_LAYER_VIOLATION`.

**FAILURE EXAMPLE:** An invariant YAML stores all three scalar values directly on the canonical object because a developer wanted a shortcut. Future runtime evaluators now cannot distinguish what the invariant is from how active it is in a specific artifact. This is a spec violation.

**Measurable pass condition:** canonical invariants accept `invariant_gravity` only; attempts to add runtime-only scalar keys fail validation.

---

### AC-20.4: Crosswalk References Must Resolve Deterministically

**Given** a primitive-to-invariant or archetype-to-geometry crosswalk file is present,  
**When** the crosswalk compiler validates the bundle,  
**Then** every referenced primitive ID, invariant ID, geometry ID, and content-archetype carrier must resolve against the loaded canonical registries or retained PRD-02 archetype inventory,  
**And** unresolved references produce a deterministic validation failure with the exact missing target listed.

**FAILURE EXAMPLE:** `SDA-XW-PI-001` references `PRM-HUM-999` and `SDA-INV-999`, but the compiler silently drops those edges and loads the rest. Query and DI services later operate on incomplete crosswalks and produce inconsistent lineage. This is a spec violation.

**Measurable pass condition:** every crosswalk entry resolves all targets, and any missing target blocks readiness with a named error.

---

### AC-20.5: Targeted Artifact Reload Preserves Registry Stability

**Given** a single canonical SDA artifact is edited during local development or CI refresh,  
**When** `reload_artifact(path)` is called,  
**Then** only the targeted artifact and any directly affected crosswalk bundle are revalidated and replaced in memory,  
**And** unrelated ontology/grammar records remain intact,  
**And** the audit report records both the old and new manifest hash inputs.

**FAILURE EXAMPLE:** Updating `SDA-RPG-002.yaml` triggers a full registry teardown, wiping unrelated invariants and forcing all downstream services to rebuild the entire ontology from scratch. This is a spec violation.

**Measurable pass condition:** a single-file reload updates one artifact deterministically without reducing ready-state coverage for unaffected registries.

---

## 9. Dependencies

### Internal

| Service/Spec | Dependency Type | What This Spec Needs From It |
|-------------|-----------------|------------------------------|
| `PRD_01_CCP_Platform_Strategy.md` | Source doctrine | Scalar separation, platform-level SDA adoption, and meaning-force architecture |
| `PRD_02_CCF_Content_Factory.md` | Source doctrine | SDA packet dependency set and runtime compiler sequence |
| `PRD_08_Conscious_Primitives.md` | Source doctrine | Primitive/SDA boundary and plane separation |
| `lab/semantic_discernment_architecture_content_engine_v_1.md` | Concept source | Deep semantic concepts and deceptively-close-failure framing |
| `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md` | Artifact taxonomy | Canonical vs derived class boundaries and governance rules |
| `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md` | Operator boundary | Confirms edge products are derived and primitives are basis/operators |
| `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md` | Force-selection boundary | Keeps broad-signal and edge-product responsibilities outside canonical ontology |
| `src/ccp/models/visual_engine_models.py` | Model precedent | Existing Pydantic registry-entry style |
| `src/ccp/services/visual_format_constraint_adapter.py` | Service precedent | Deterministic registry loading and validation pattern |
| `src/ccp/services/known_persons_registry_adapter.py` | Service precedent | Multi-stage registry resolution and hard prohibition pattern |
| `src/ccp/services/tiar_adapter.py` | Service precedent | Active/blocked partition and stale-cache fallback pattern |
| `src/ccp/core/receipt_chain.py` | Runtime dependency | Audit logging for warm/load/reject/reload lifecycle |

### External

| API/Library | Version | Purpose |
|------------|---------|---------|
| `pydantic` | `>=2.6.0` | Canonical typed SDA models |
| `PyYAML` | `>=6.0.1` | YAML parsing for ontology/grammar/crosswalk artifacts |
| PostgreSQL | Existing platform dependency | Optional persistence of registry audit records if promoted beyond file receipts |

---

## 10. Testing Strategy

### Unit / Integration Tests

**File:** `tests/integration/test_era3_fr20_sda_registry.py`

```python
class TestManifestBoot:
    def test_ac201_warm_loads_all_required_classes(self)
    def test_manifest_counts_must_match_loaded_counts(self)
    def test_registry_ready_false_when_manifest_missing(self)


class TestArtifactClassGuards:
    def test_false_registry_content_species_rejected(self)
    def test_false_registry_hard_negative_rejected(self)
    def test_runtime_scalar_fields_rejected_on_invariant(self)
    def test_wrong_prefix_rejected_for_artifact_kind(self)


class TestReloadBehavior:
    def test_single_artifact_reload_updates_only_target(self)
    def test_failed_reload_preserves_previous_good_state(self)
```

**File:** `tests/integration/test_era3_fr20_sda_crosswalks.py`

```python
class TestPrimitiveInvariantCrosswalks:
    def test_ac204_primitive_reference_must_exist(self)
    def test_invariant_reference_must_exist(self)
    def test_crosswalk_weights_within_zero_to_one(self)


class TestArchetypeGeometryCrosswalks:
    def test_content_archetype_must_belong_to_retained_prd02_inventory(self)
    def test_geometry_reference_must_exist(self)
```

### Test Pattern Requirements

Follow the repoâ€™s existing registry-spec style seen in:

- `tests/integration/test_vis07_format_constraint.py`
  - registry completeness assertions
  - explicit failure examples
  - staged receipt verification
- `tests/integration/test_vis12_known_persons.py`
  - matrix-style acceptance-criteria grouping
  - hard prohibition checks
- `tests/integration/test_vis02_tiar_integration.py`
  - active/blocked partition tests
  - stale/fresh state behavior
  - downstream revalidation audit checks

### Manual Verification

1. Create a minimal valid `sda/` fixture set and run `SDARegistryService.warm()`.
2. Confirm `SDARegistryAuditReport.ready == true` and counts match the manifest.
3. Add a malformed invariant file with `invariant_resonance_multiplier` and confirm boot fails with `SCALAR_LAYER_VIOLATION`.
4. Add a fake `content_species` YAML under `sda/ontology/` and confirm boot fails with `FALSE_REGISTRY_VIOLATION`.
5. Add a crosswalk that references a missing primitive ID and confirm readiness is blocked with the exact missing target named.
6. Edit one representation-geometry file and call `reload_artifact(path)`; confirm unrelated invariants and grammars remain loaded.
7. Review receipt-chain output and verify startup, reject, and reload events are each logged with deterministic stage names.

---

*This spec is the canonical foundation for Wave 1 SDA implementation. It intentionally stops at ontology, grammar, and crosswalk registries so that `FR-ERA3-21` through `FR-ERA3-24` can build on a stable, doctrine-correct substrate instead of improvising their own semantic object model.*

