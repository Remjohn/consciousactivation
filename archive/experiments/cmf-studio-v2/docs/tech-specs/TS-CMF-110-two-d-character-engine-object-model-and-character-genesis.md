---
tech_spec_id: "TS-CMF-110"
title: "2D Character Engine Object Model and Character Genesis"
story_id: "7.26"
story_title: "2D Character Animation Engine - Character Genesis"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-25"
source_story: "CCP 2D Character Animation Engine V1 bundle integration"
pipeline_stage: "4 / 7 / 8 / 10 / 11"
entry_object: "BrandContextVersion, CharacterIdentityReferences, ConsentRecord, VoiceVisualDNA, MicroSemioticAnchorLibrary, AssetPackageSpec"
exit_object: "CharacterIdentityPack, CharacterArtVersion, LayeredCharacterAssetVersion, CharacterRigVersion, PerformanceLibraryVersion, CharacterGenesisReceipt"
validation_contract: "identity continuity, rig-aware design, PaperCut materiality, layered asset integrity, rig release gates, performance library coverage, primitive triads, operator approval"
required_receipt: "CharacterGenesisReceipt"
runtime_target: "Python / Pydantic v2 / DSPy / Pi Command Bus / provider workers / object storage / Animation Studio"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-110: 2D Character Engine Object Model and Character Genesis

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory 10-section spec structure, backend integration, primitive, CBAR, acceptance, and test requirements. |
| `THE CMF STUDIO/docs/audits/CMF_2D_ANIMATION_STUDIO_AND_SPEC_PROTOCOL_AUDIT_2026-06-24.md` | Confirms the current 2D animation system is not operational end-to-end and identifies missing runtime, editor, and renderer pieces. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/00_START_HERE.md` | Defines the bundle purpose, structured inputs, Python-first rule, and `TwoDCharacterProgram` as canonical runtime artifact. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/01_MASTER_SPEC.md` | Defines Character Genesis, Performance Compilation, canonical immutable objects, structured inputs, and character design doctrine. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/03_RIGGING_AND_ASSET_CONTRACTS.md` | Defines PSD normalization, layer graph, bone graph, mesh bundle, masks, shape keys, hand/mouth/gaze libraries, skins, and rig release gate. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/models/two_d_character_models.py` | Provides canonical Pydantic model names and invariants for rig, performance library, and program objects. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/schemas/character_rig_manifest.schema.json` | JSON schema evidence for rig manifest shape. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/schemas/performance_library.schema.json` | JSON schema evidence for acting state and transition library. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Defines Brand Genesis, 64-state assets, micro-semiotic anchoring, and paper-cut asset obligations. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Provides creative pipeline stages for scene, asset, motion, review, and reproducibility. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-019-64-state-acting-library.md` | Upstream 64-state acting library dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-020-paper-cut-rig-and-creative-libraries.md` | Existing paper-cut rig and creative library foundation. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-044-generative-provider-adapters.md` | Provider adapter boundary for GPT Image 2, Flux 2 Klein, Qwen-Image-Layered, SAM3, and ComfyUI workers. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-085-64-state-acting-and-avatar-performance-selector.md` | Existing acting/avatar selection dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-086-papercut-rig-layer-motion-and-sfx-runtime.md` | Existing PaperCut runtime dependency that consumes rig and layer assets. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-093-animation-studio-migration-and-operator-rig-editor.md` | Operator-facing rig editor dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-094-headless-2d-frame-renderer-and-avatar-export-worker.md` | Downstream renderer worker dependency. |

## 2. Overview

The 2D Character Engine creates reusable, brand-owned digital actors for CMF educational, explainer, reaction, and avatar scenes. This spec owns the canonical object model and the Character Genesis lifecycle. It does not render final videos and it does not compile transcript-timed performances; those are downstream responsibilities in `TS-CMF-108` and `TS-CMF-109`.

Character Genesis transforms approved identity and brand material into locked, versioned character infrastructure:

```text
Brand Context + identity references + consent
-> CharacterIdentityPack
-> rig-aware master art candidates
-> CharacterArtVersion
-> layer decomposition and hidden-region repair
-> LayeredCharacterAssetVersion
-> rig authoring and runtime export
-> CharacterRigVersion
-> face / mouth / hand / gaze / prop / 64-state performance library
-> PerformanceLibraryVersion
-> CharacterGenesisReceipt
```

This is the missing character, rig, and performance foundation for the Educational / Explainer format. It also supports PaperCut inserts in Cinematic Story Commentary, character-led Living Commentary Reactions, and animated elements inside Conscious Reactions Editing.

This spec explicitly does not:

- allow loose prompts to create production characters;
- let a provider output become production truth without approval and version lock;
- import legacy runtime code directly from `D:\Work\The Conscious Coaching Factory`;
- treat a flat illustration as a production-ready rig;
- skip primitive triads, doctrine gates, or operator approval.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-106-001 | `BrandContextVersion` | Locks identity, visual DNA, typography, colors, approved motifs, banned motifs, rights, and negative space constraints. |
| DEP-CMF-106-002 | `ConsentRecord` | Defines whether the guest or brand can be represented by a stylized or animated character. |
| DEP-CMF-106-003 | `CharacterIdentityPack` | Immutable identity source for approved references, non-negotiable likeness traits, allowed stylizations, forbidden representations, and reference hashes. |
| DEP-CMF-106-004 | `CharacterArtVersion` | Approved rig-aware character design, expression sheet, eye-direction sheet, mouth-shape sheet, hand sheet, costume sheet, prop sheet, and material definitions. |
| DEP-CMF-106-005 | `LayeredCharacterAssetVersion` | Normalized PSD/layer package with semantic layer graph, hidden regions, masks, depth, draw order, alpha QC, and repair history. |
| DEP-CMF-106-006 | `CharacterRigVersion` | Locked bones, pivots, slots, attachments, meshes, weights, masks, shape keys, IK constraints, draw-order rules, material bindings, and runtime export refs. |
| DEP-CMF-106-007 | `PerformanceLibraryVersion` | Reusable base idles, postures, gestures, facial poses, gaze policies, viseme map, hand variants, prop actions, transition graph, and 64 semantic acting states. |
| DEP-CMF-106-008 | `MicroSemioticAnchorLibrary` | Supplies approved costume, prop, texture, object, or environmental anchors that may become character skins or attachments. |
| DEP-CMF-106-009 | `CharacterGenesisReceipt` | Immutable proof of source refs, provider jobs, QC results, primitive/doctrine gates, operator approval, object hashes, and version locks. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/two_d_character.py` | New Pydantic contracts for Section 5 objects and schema parity with bundle models. |
| `src/ccp_studio/services/character_genesis_service.py` | New service that validates inputs, coordinates providers, promotes approved assets, and locks versions. |
| `src/ccp_studio/workflows/character_genesis_workflow.py` | New durable workflow with resumable provider, QC, rig, and approval stages. |
| `src/ccp_studio/services/provider_operations_service.py` | Must register provider capabilities for rig-aware art, layered decomposition, masks, repair, rig authoring, and runtime export. |
| `src/ccp_studio/services/rig_validation_service.py` | Remains backend authority for rig release validation. |
| `src/ccp_studio/contracts/creative_libraries.py` | Supplies acting states, paper props, SFX families, costume skins, and performance library refs. |
| `src/ccp_studio/services/creative_library_service.py` | Resolves approved creative library assets per guest workspace and Brand Context. |
| `src/ccp_studio/services/doctrine_evaluation_service.py` | Runs identity, PaperCut materiality, primitive triad, and rig doctrine gates before lock. |
| Object storage | Stores references, master art, PSDs, masks, meshes, sidecars, runtime exports, previews, hashes, and receipt artifacts. |

### ADR-05 Primitives

Every Character Genesis request must validate at least three primitives across meaning, delivery, and material/format roles:

| Role | Required Use |
|---|---|
| Meaning transform | Prove why this character embodiment helps explain, witness, contrast, or teach the source idea. |
| Delivery shape | Prove that the character supports comprehension through gesture, gaze, pose, prop, or scene role. |
| Format material | Prove that PaperCut, 2D avatar, or mixed-media materiality is justified by the target format. |

Preferred primitive anchors include:

| Primitive | Use |
|---|---|
| `PRM-VSG-008` Character Coherence Beats Beauty | Blocks generic attractive avatars that lose guest identity. |
| `PRM-VSG-020` Perspective and Layering as Meaning | Requires layer depth and perspective to carry meaning, not decoration. |
| `PRM-VSG-001` Composition as Eye-Path Engineering | Requires rig and art to support readable eye path. |
| `PRM-BUS-012` Grid as Cognitive Relief | Requires reusable character assets to fit teaching and review layouts. |

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase4-M01 Intelligence-Gated Intercept | Character Genesis cannot start without locked Brand Context, consent, identity refs, and target use case. |
| Phase4-M02 Cinematic Meaning | Character creation must name the intended scene role and meaning operation before provider calls. |
| Phase4-M04 Frictionless Block | Missing consent, identity ambiguity, provider capability gaps, layer failures, or primitive gaps block before expensive downstream renders. |
| Phase4-M05 Actionable Rejection | Every blocker names the failed object, failed gate, evidence ref, and repair command family. |
| Phase5-M01 Verifiable Artifact | Every locked version is reconstructable from source refs, provider receipts, QC reports, hashes, and approval receipts. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Separate Character Genesis from Performance Compilation. | Character infrastructure is reusable and slow-changing; scene performance is per asset and transcript-timed. |
| Make approved objects immutable. | Final scenes must be reproducible and debuggable from exact version IDs. |
| Treat providers as candidate generators only. | See-Through, Qwen, SAM3, GPT Image 2, Flux 2 Klein, Stretchy Studio, and Spine-compatible tooling do not own semantic approval. |
| Require rig-aware art before decomposition. | Arbitrary final images tend to fuse arms, hands, hair, props, and clothing in ways that break animation. |
| Model `PerformanceLibraryVersion` separately from `CharacterRigVersion`. | The same rig can receive improved acting states without losing rig lineage. |
| Require operator approval before lock. | Identity and likeness cannot be fully delegated to automated gates. |

### Gate Thresholds and Verdicts

Character Genesis gates inherit the source bundle thresholds from `registries/eval_gates.json`.

| Gate ID | Threshold | Hard Fail | Downstream Consequence |
|---|---:|---|---|
| `identity_consistency` | 0.90 | Yes | Blocks `CharacterIdentityPack` lock. |
| `semantic_layer_correctness` | 0.92 | Yes | Blocks `LayeredCharacterAssetVersion` promotion. |
| `hidden_region_completeness` | 0.88 | Yes | Blocks rig authoring until repaired. |
| `pivot_quality` | 0.90 | Yes | Blocks `CharacterRigVersion` lock. |
| `mesh_integrity` | 0.95 | Yes | Blocks runtime export and rig lock. |
| `runtime_export_parity` | 0.94 | Yes | Blocks renderer handoff. |
| `paper_materiality` | 0.86 | No | Below threshold creates `PROVISIONAL_PAPER_MATERIALITY_REVIEW`; operator must approve or repair before lock. |

Verdict semantics are deterministic: hard-fail gates return `PASS` when `score >= threshold` and `FAIL` otherwise. Non-hard-fail gates return `PASS` when `score >= threshold`, `PROVISIONAL` when `threshold - 0.08 <= score < threshold`, and `FAIL` when below that provisional floor.

## 4. Implementation Plan

1. Add `contracts/two_d_character.py` with `CharacterIdentityPack`, `CharacterArtVersion`, `LayeredCharacterAssetVersion`, `CharacterRigVersion`, `PerformanceLibraryVersion`, and `CharacterGenesisReceipt`.
2. Import or translate bundle schemas into CMF schema generation tests without making the bundle folder a production import.
3. Add `services/character_genesis_service.py` with validation, provider planning, candidate promotion, version locking, and receipt emission.
4. Add `workflows/character_genesis_workflow.py` with states: `accepted`, `identity_pack_ready`, `art_candidates_ready`, `art_approved`, `layered_assets_ready`, `rig_candidate_ready`, `performance_library_ready`, `awaiting_operator_lock`, `locked`, `failed`.
5. Extend provider capability registry with required provider roles and capability IDs for art, decomposition, masks, repair, rig authoring, runtime export, and QC.
6. Add rig release gate enforcement through `rig_validation_service.py`.
7. Add primitive and doctrine eval targets for identity, rig-aware design, materiality, layer graph, and performance library coverage.
8. Add PWA review read model for identity pack, art candidates, layer QC, rig debug preview, performance library coverage, and lock blockers.
9. Add fixtures for one PaperCut educational character, one photo-paper-cut mixed-media character, and one simple avatar explainer character.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class CharacterIdentityPack(BaseModel):
    schema_version: Literal["cmf.character_identity_pack.v1"]
    identity_pack_id: UUID
    workspace_id: UUID
    brand_context_version_id: UUID
    consent_record_id: UUID
    approved_reference_asset_refs: list[str]
    non_negotiable_likeness_traits: list[str]
    allowed_stylizations: list[str]
    forbidden_representations: list[str]
    micro_semiotic_anchor_refs: list[UUID]
    reference_hashes: dict[str, str]


class CharacterArtVersion(BaseModel):
    schema_version: Literal["cmf.character_art_version.v1"]
    character_art_version_id: UUID
    identity_pack_id: UUID
    master_art_ref: str
    expression_sheet_ref: str
    eye_direction_sheet_ref: str
    mouth_shape_sheet_ref: str
    hand_gesture_sheet_ref: str
    costume_sheet_ref: str
    prop_sheet_ref: str
    material_profile_id: str
    provider_receipt_refs: list[str]
    approved_by_operator: bool


class LayeredCharacterAssetVersion(BaseModel):
    schema_version: Literal["cmf.layered_character_asset_version.v1"]
    layered_asset_version_id: UUID
    character_art_version_id: UUID
    psd_ref: str
    layer_graph_ref: str
    hidden_region_report_ref: str
    mask_bundle_ref: str
    alpha_quality_report_ref: str
    repair_history_refs: list[str]
    locked: bool


class CharacterRigVersion(BaseModel):
    schema_version: Literal["cmf.character_rig_version.v1"]
    rig_version_id: UUID
    layered_asset_version_id: UUID
    setup_pose_id: str
    bone_graph_ref: str
    mesh_bundle_ref: str
    shape_key_bundle_ref: str
    constraints_ref: str
    runtime_export_refs: list[str]
    rig_release_gate_receipt_ref: str
    locked: bool


class PerformanceLibraryVersion(BaseModel):
    schema_version: Literal["cmf.performance_library_version.v1"]
    performance_library_version_id: UUID
    rig_version_id: UUID
    acting_library_version_id: UUID
    viseme_map_id: str
    facial_pose_map_id: str
    gaze_map_id: str
    hand_pose_map_id: str
    prop_action_map_id: str
    transition_graph_ref: str
    acting_state_count: int = Field(ge=64)
    locked: bool


class CharacterGenesisReceipt(BaseModel):
    schema_version: Literal["cmf.character_genesis_receipt.v1"]
    receipt_id: UUID
    identity_pack_id: UUID
    character_art_version_id: UUID
    layered_asset_version_id: UUID
    rig_version_id: UUID
    performance_library_version_id: UUID
    provider_receipt_refs: list[str]
    eval_receipt_refs: list[str]
    operator_approval_ref: str
    locked_object_hashes: dict[str, str]
    blocker_codes: list[str]
```

## 6. Backward Compatibility Fallback

Legacy character concepts, PaperCut examples, and animation-studio references may be used as source intelligence only. They must be converted into CMF contracts and pass all gates before use.

| Condition | Fallback |
|---|---|
| Consent does not permit animated likeness | Block with `CHARACTER_CONSENT_SCOPE_MISSING`. |
| Identity refs are insufficient | Block with `CHARACTER_IDENTITY_REFERENCE_INSUFFICIENT`. |
| Rig-aware art cannot be approved | Permit concept preview only; block lock with `RIG_AWARE_ART_NOT_APPROVED`. |
| Layer decomposition fails | Route to repair provider or block with `LAYERED_CHARACTER_ASSET_INVALID`. |
| Rig release gate fails | Return actionable rig repair blockers; do not create `CharacterRigVersion`. |
| Performance library lacks 64-state coverage | Block with `PERFORMANCE_LIBRARY_COVERAGE_MISSING`. |

## 7. Tasks

| Task | Implementation Requirement |
|---|---|
| T106-01 | Add CMF Pydantic contracts for all Character Genesis objects. |
| T106-02 | Add schema parity tests against bundle schemas and examples. |
| T106-03 | Add character genesis workflow and state machine. |
| T106-04 | Add provider planning hooks for art, decomposition, mask, repair, rig authoring, and runtime export. |
| T106-05 | Add identity, likeness, materiality, layer, rig, and performance library eval gates. |
| T106-06 | Add operator review read model and approval command. |
| T106-07 | Add object storage layout for character source, candidates, sidecars, previews, exports, and receipts. |
| T106-08 | Add fixtures for PaperCut, mixed-media, and simple avatar characters. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | Mandate |
|---|---|---|---|
| AC106-01 | Character Genesis cannot start without Brand Context, consent, identity refs, and target use case. | A prompt creates an avatar from one uploaded photo and no consent record. | Phase4-M01 |
| AC106-02 | Provider outputs remain candidates until promoted into approved, versioned CMF objects. | A Qwen layer result is referenced directly by a render program. | Phase5-M01 |
| AC106-03 | Character art must pass rig-aware design checks before decomposition. | Hands are fused to props and the system still proceeds to rigging. | Phase4-M04 |
| AC106-04 | `CharacterRigVersion` locks only after rig release gate passes. | Extreme arm bend causes mesh inversion but rig is locked. | Phase4-M05 |
| AC106-05 | `PerformanceLibraryVersion` must include viseme, face, gaze, hand, prop, transition, and 64-state acting coverage. | The character can idle but has no gaze or mouth library. | Phase4-M02 |
| AC106-06 | Character approval receipt includes hashes, provider receipts, eval receipts, and operator approval. | A locked rig has no source hash or approval trail. | Phase5-M01 |

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `TS-CMF-019` | Internal | 64-state acting library. |
| `TS-CMF-020` | Internal | PaperCut rig and creative libraries. |
| `TS-CMF-042` | Internal | Provider capability registry and receipts. |
| `TS-CMF-044` | Internal | Generative provider adapters. |
| `TS-CMF-085` | Internal | Acting/avatar performance selector. |
| `TS-CMF-086` | Internal | PaperCut runtime. |
| `TS-CMF-093` | Internal | Operator rig editor. |
| `TS-CMF-094` | Internal | Headless 2D frame renderer. |
| See-Through | External/reference | Illustration decomposition candidate route. |
| Qwen-Image-Layered | External/provider | Mixed-media and semantic layer extraction. |
| SAM3 | External/provider | Mask refinement, edge cleanup, tracking. |
| GPT Image 2 / Flux 2 Klein | External/provider | Candidate art, identity edits, repair, harmonization. |
| Stretchy Studio | External/reference | Rig authoring adapter and export inspiration. |
| Spine-compatible runtime | External/runtime | Bone, slot, mesh, constraint, and animation export target. |

## 10. Testing Strategy

- Unit test every Pydantic model with valid and invalid fixtures.
- Validate generated JSON schemas against bundle examples.
- Run identity scope tests for missing consent, forbidden representation, weak references, and banned stylization.
- Run layer graph tests for cropped layers, missing semantic tags, invalid draw order, alpha bleed, and missing hidden regions.
- Run rig release tests for pivot failure, mesh inversion, mask leakage, eye clipping, mouth shape failure, costume switch failure, and deterministic export mismatch.
- Run performance library tests for missing 64-state coverage, illegal transitions, missing visemes, missing gaze policies, and missing hand variants.
- Run workflow recovery tests from each resumable state.
- Run review approval tests proving locked objects are immutable and repair creates a new version.
