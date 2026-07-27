---
title: "CMF 2D Character Engine Spec Audit and Revision"
status: "revised"
created_at: "2026-06-25"
protocols:
  - "docs/architecture/april_updates/TRIGGER_COMMAND_AUDIT.md"
  - "docs/architecture/april_updates/PROMPT_Spec_Audit.md"
  - "docs/architecture/april_updates/TRIGGER_COMMAND_REVISION.md"
  - "docs/architecture/april_updates/PROMPT_Spec_Revision.md"
  - "THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md"
scope_before_revision:
  - "TS-CMF-106"
  - "TS-CMF-107"
  - "TS-CMF-108"
  - "TS-CMF-109"
scope_after_revision:
  - "TS-CMF-110"
  - "TS-CMF-111"
  - "TS-CMF-112"
  - "TS-CMF-113"
---

# CMF 2D Character Engine Spec Audit and Revision

## 1. Audit Scope

This audit reviews the newly integrated CCP 2D Character Animation Engine V1 specification chain. The purpose is to verify that the bundle was transformed into canonical CMF/ERA3 specs without colliding with existing video-editing reservations, losing provider boundaries, weakening primitive/doctrine gates, or leaving the `TwoDCharacterProgram` scene program underspecified.

The legacy audit protocol says to audit one spec at a time. For this subsystem pass, each target spec was evaluated independently under the five lenses, then revised as a connected chain because the highest-risk issue was cross-spec numbering and runtime handoff consistency.

## 2. Sources Read

| Source | Use |
|---|---|
| `docs/architecture/april_updates/PROMPT_Spec_Audit.md` | Five-lens audit structure. |
| `docs/architecture/april_updates/PROMPT_Spec_Revision.md` | Section-targeted revision discipline. |
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory 10-section spec shape, backend mapping, primitives, CBAR, gates, and tests. |
| `THE CMF STUDIO/docs/audits/CMF_CAROUSEL_AND_SUPERVISUAL_SPEC_AUDIT_REVISION_2026-06-24.md` | Existing audit/revision report pattern and cross-spec numbering context. |
| `THE CMF STUDIO/docs/audits/CMF_VIDEO_EDITING_ENGINE_MCDA_2026-06-24.md` | Confirms `TS-CMF-106` was already reserved for the future Video Edit Program compiler. |
| `THE CMF STUDIO/docs/audits/CMF_2D_ANIMATION_STUDIO_AND_SPEC_PROTOCOL_AUDIT_2026-06-24.md` | Confirms the 2D animation studio is not operational end-to-end and identifies renderer/editor gaps. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-04, FR-CMF-07, FR-CMF-08, FR-CMF-09, interview-first doctrine, Brand Genesis, rig, provider, render, eval, and approval requirements. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/00_START_HERE.md` | Defines Python-first boundary and `TwoDCharacterProgram` as canonical runtime artifact. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/01_MASTER_SPEC.md` | Defines Character Genesis, Performance Compilation, immutable objects, structured inputs, and character doctrine. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/02_PIPELINE_AND_PROVIDER_ROLES.md` | Provider boundary truth. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/03_RIGGING_AND_ASSET_CONTRACTS.md` | Rig, layer, shape key, hand, mouth, gaze, skin, and release gate truth. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/04_PERFORMANCE_COMPILER.md` | DSPy compiler stage, beat-to-state, gesture, gaze, viseme, prop, transition, and eval truth. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/05_RENDERING_AND_REPRODUCIBILITY.md` | Render modes, Motion Canvas, Remotion, FFmpeg, receipt, golden tests, and network isolation truth. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/06_EVALS_APPROVAL_AND_REPAIR.md` | Preview hierarchy, typed repairs, approval lifecycle, and receipt chain truth. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/registries/eval_gates.json` | Numeric gate threshold source. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/registries/provider_responsibilities.json` | Provider ownership and prohibited ownership source. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/registries/repair_commands.json` | Typed repair command versioning source. |

## 3. Decision Log

**Decision 1 - Reserve `TS-CMF-106` for Video Editing:**
`TS-CMF-106` remains reserved for the Video Edit Program compiler because `CMF_VIDEO_EDITING_ENGINE_MCDA_2026-06-24.md` and the carousel/supervisual audit already moved that future spec into the `TS-CMF-106` slot. The 2D Character Engine specs are renumbered to `TS-CMF-110` through `TS-CMF-113`.

**Decision 2 - Use Bundle Gate Thresholds as Canonical:**
Character and per-program gates must inherit thresholds from `registries/eval_gates.json`. Hard-fail gates return only `PASS` or `FAIL`. Non-hard-fail gates may return `PROVISIONAL` inside an explicit `threshold - 0.08` margin and require repair or operator rationale before lock/render approval.

**Decision 3 - Repair Commands Control Versioning:**
Repair command versioning is governed by `registries/repair_commands.json`. Rig-targeting repairs create a new rig version; program-level repairs create program revisions. Approved objects are never patched in place.

## 4. Audit Report

### PASS

No target spec passed with zero flags before revision because the batch contained cross-spec numbering and gate-completeness issues.

### FLAGS

**[TS-CMF-106] | LENS 5 | SEVERITY: CRITICAL**
- **Finding:** The spec occupied `TS-CMF-106`, which was already reserved by the video-editing MCDA and the carousel/supervisual audit for `TS-CMF-106-video-edit-program-compiler-otio-and-render-runtime.md`.
- **Location:** Frontmatter, filename, README dependency order, cross-spec audit references.
- **Required Action:** Renumber the 2D Character Engine spec family to non-colliding IDs and update all dependency references.
- **Revision Applied:** Yes. Character specs moved to `TS-CMF-110` through `TS-CMF-113`; README now preserves `TS-CMF-106` for the future video edit compiler.

**[TS-CMF-106] | LENS 4 | SEVERITY: WARNING**
- **Finding:** Character Genesis referenced identity, layer, rig, export, and paper materiality gates without exact numeric thresholds or provisional verdict behavior.
- **Location:** Section 3, ADR-05 Primitives and Technical Decisions.
- **Required Action:** Add Character Genesis gate thresholds from `eval_gates.json` and deterministic verdict semantics.
- **Revision Applied:** Yes in `TS-CMF-110`.

**[TS-CMF-107] | LENS 4 | SEVERITY: CRITICAL**
- **Finding:** Provider promotion gates referenced capability, license, hashes, semantic layer quality, alpha quality, and runtime parity without exact thresholds and downstream consequences.
- **Location:** Section 3, Technical Decisions; Section 8, Acceptance Criteria.
- **Required Action:** Add provider gate thresholds, hard-fail behavior, and promotion consequences.
- **Revision Applied:** Yes in `TS-CMF-111`.

**[TS-CMF-108] | LENS 4 | SEVERITY: CRITICAL**
- **Finding:** The `TwoDCharacterProgram` compiler declared `EvaluationSpec` but did not pin the exact thresholds for source alignment, lip sync, beat-performance match, primitive compliance, doctrine alignment, motion restraint, or technical render readiness.
- **Location:** Section 3, Architecture Traceability and Technical Decisions.
- **Required Action:** Add per-program gate thresholds from `eval_gates.json`, including provisional behavior for non-hard-fail gates.
- **Revision Applied:** Yes in `TS-CMF-112`.

**[TS-CMF-109] | LENS 4 | SEVERITY: CRITICAL**
- **Finding:** Render/eval/approval gates lacked exact numeric thresholds for final render approval, render package completeness, and reproducibility receipt completeness.
- **Location:** Section 3, Technical Decisions; Section 8, Acceptance Criteria.
- **Required Action:** Add runtime gate thresholds and hard-fail/provisional semantics.
- **Revision Applied:** Yes in `TS-CMF-113`.

**[TS-CMF-109] | LENS 5 | SEVERITY: WARNING**
- **Finding:** Typed repair commands were listed, but the spec did not expose which command families require a new rig version versus a program revision.
- **Location:** Section 3, Technical Decisions; Section 4, Implementation Plan; Section 5, schema.
- **Required Action:** Add repair command versioning rules from `repair_commands.json`.
- **Revision Applied:** Yes in `TS-CMF-113`.

## 5. Revision Log

| Target | Revision |
|---|---|
| `TS-CMF-106` | Moved to `TS-CMF-110-two-d-character-engine-object-model-and-character-genesis.md`. |
| `TS-CMF-107` | Moved to `TS-CMF-111-two-d-character-provider-adapters-rig-authoring-and-asset-promotion.md`. |
| `TS-CMF-108` | Moved to `TS-CMF-112-two-d-character-scene-program-and-performance-compiler.md`. |
| `TS-CMF-109` | Moved to `TS-CMF-113-two-d-character-render-runtime-evals-approval-and-repair.md`. |
| `TS-CMF-110` | Added Character Genesis gate thresholds and deterministic verdict semantics. |
| `TS-CMF-111` | Added provider gate thresholds, hard-fail behavior, and promotion consequences. |
| `TS-CMF-112` | Added per-program gate thresholds and provisional behavior for lip sync and motion restraint. |
| `TS-CMF-113` | Added runtime/render thresholds, reproducibility completeness gates, provisional behavior, and repair command versioning rules. |
| `docs/tech-specs/README.md` | Updated dependency order to `TS-CMF-110` through `TS-CMF-113` and preserved `TS-CMF-106` for video editing. |

## 6. Current System Shape After Revision

```text
TS-CMF-110
CharacterIdentityPack / CharacterArtVersion / LayeredCharacterAssetVersion
-> CharacterRigVersion / PerformanceLibraryVersion
-> CharacterGenesisReceipt

TS-CMF-111
CharacterProviderJobPlan
-> LayeredCharacterAssetCandidate / RigAuthoringProject / RigExportBundle
-> ProviderAdapterReceipt

TS-CMF-112
Interview context + TranscriptBeatMap + CharacterRigVersion + PerformanceLibraryVersion
-> TwoDCharacterProgram
-> CharacterPerformanceCompilerReceipt

TS-CMF-113
TwoDCharacterProgram
-> RigDebugPreview / PerformanceBlockingPreview / FinalCompositionPreview
-> CharacterRenderReceipt / CharacterRepairReceipt
-> ApprovedTwoDCharacterSceneProgram
```

## 7. Remaining Implementation Blockers

| Blocker | Why It Still Matters |
|---|---|
| Runtime code for `contracts/two_d_character.py` is not implemented yet. | The specs are now build-ready, but code must still be written. |
| Provider adapters are not executable yet. | See-Through, Qwen, SAM3, GPT Image 2 / Flux 2 Klein, Stretchy Studio, and Spine-compatible routes still need implementation and sandbox evaluation. |
| Animation Studio UI is still required. | `TS-CMF-093` remains the operator surface needed to inspect rig debug and performance blocking previews. |
| Headless 2D renderer is still required. | `TS-CMF-094` remains the worker path for actual frame rendering and avatar export. |
| Video Edit Program compiler remains unwritten. | `TS-CMF-106` is preserved for the future video-editing spec so 2D character scenes can become inputs to the broader video timeline. |

## 8. Summary Statistics

| Metric | Count |
|---|---:|
| Specs reviewed before revision | 4 |
| Specs moved by revision | 4 |
| Specs modified by revision | 4 |
| Critical findings | 4 |
| Warning findings | 2 |
| Notes | 0 |
| DEP-ID conflicts repaired | 1 |
| Gate threshold gaps repaired | 4 |
| Cross-spec consistency issues repaired | 2 |
