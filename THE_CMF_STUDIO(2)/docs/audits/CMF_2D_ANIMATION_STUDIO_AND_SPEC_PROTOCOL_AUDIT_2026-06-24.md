# CMF 2D Animation Studio and Spec Protocol Audit

Date: 2026-06-24  
Auditor: Codex / John PM support  
Scope: Current CMF Studio 2D avatar, Paper-Cut animation, deterministic rendering, legacy Animation Studio evidence, and spec-writing protocol compliance.

## 1. Executive Finding

The 2D Animation Studio is not operational end-to-end inside `THE CMF STUDIO`.

CMF Studio currently has working Python-side contracts, services, repositories, and tests for paper-cut rig validation, creative libraries, deterministic renderer props, receipts, synthetic render jobs, and object URI outputs. Those layers pass targeted tests.

However, the actual operator-facing 2D Animation Studio, Paper-Cut/2D avatar editor, Pixi/DragonBones canvas runtime, Remotion/Motion Canvas component library, frame renderer worker, and transcript-timed final video rendering path are not present as operational implementation inside `THE CMF STUDIO`.

The legacy implementation at `D:\Work\The Conscious Coaching Factory\apps\animation-studio` is important and should be migrated or adapted. It contains a Next.js editor shell, Zustand state, schemas, scene presets, two-character layout logic, Gate O checks, BPM/lip-sync services, clip import conversion helpers, and frame export job descriptors. It does not appear to include the actual Node/Pixi/DragonBones headless renderer subprocess it describes.

## 2. Sources Read

| Source | What Was Checked |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory 10-section spec protocol, pre-flight requirements, backend integration, primitives, CBAR mandates. |
| `THE CMF STUDIO/docs/architecture/april_updates/PROMPT_Spec_Audit.md` | Five-lens audit protocol: FR coverage, DEP/primitive integrity, boundary precision, gate/CBAR completeness, cross-spec consistency. |
| `THE CMF STUDIO/docs/architecture/april_updates/PROMPT_Spec_Revision.md` | Revision format: one flagged spec at a time, exact copy-pasteable fixes, no broad summary replacements. |
| `THE CMF STUDIO/docs/architecture/april_updates/PROMPT_Spec_Build.md` | Build protocol: one spec at a time, spec is law, no partial completions, proof before progress. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Paper-Cut Avatar System, 2.5D paper-cut reel animation, layer taxonomy, motion recipes, Remotion/Motion Canvas routing, rig manifest, preview tests. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md` | Python-first authority, TypeScript as leaf runtime, Remotion/Motion Canvas as execution targets, paper-cut actor, renderer contract boundaries. |
| `D:\Work\The Conscious Coaching Factory\apps\animation-studio` | Legacy Next/Pixi-oriented animation editor and API/service evidence. |
| `THE CMF STUDIO/src/ccp_studio/contracts/rig_manifest.py` | Current rig manifest contracts. |
| `THE CMF STUDIO/src/ccp_studio/services/rig_validation_service.py` | Current rig blocker validation. |
| `THE CMF STUDIO/src/ccp_studio/contracts/deterministic_rendering.py` | Current deterministic renderer props, jobs, output, and receipts. |
| `THE CMF STUDIO/src/ccp_studio/services/deterministic_rendering_service.py` | Current props bundle compilation and synthetic deterministic render output. |
| `THE CMF STUDIO/tests/cmf_studio/test_paper_cut_rig_and_creative_libraries.py` | Current rig and creative library tests. |
| `THE CMF STUDIO/tests/cmf_studio/test_deterministic_remotion_and_motion_canvas_rendering.py` | Current deterministic rendering contract tests. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-020-paper-cut-rig-and-creative-libraries.md` | Full earlier paper-cut rig spec structure. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-080...TS-CMF-092` | Current composition/runtime companion specs and protocol compliance gaps. |

## 3. Current State Matrix

| Capability | Documented | Specified | Implemented in CMF Studio | Tested | Operational End-to-End |
|---|---:|---:|---:|---:|---:|
| Paper-Cut avatar doctrine and style constraints | Yes | Partial | Partial | Partial | No |
| 64-state acting library | Yes | Yes | Yes, backend | Yes | Partial |
| Rig manifest with layers, pivots, mouth, eyes/brows, gestures, body layers | Yes | Yes | Yes, backend | Yes | Partial |
| Rig preview validation | Yes | Yes | Metadata/blocker validation | Yes | No visual preview runtime verified |
| Creative libraries: props, anchors, motion recipes, SFX, platform profiles | Yes | Yes | Yes, backend | Yes | Partial |
| Paper-Cut runtime manifest | Yes | Thin spec only | No dedicated implementation found | No dedicated tests found | No |
| Paper materiality/motion constitution eval | Yes | Thin spec only | No dedicated implementation found | No dedicated tests found | No |
| Operator-facing 2D Animation Studio UI | Legacy app exists outside CMF | Not migrated as CMF spec | Not present in CMF folder | Not tested in CMF | No |
| Pixi/DragonBones canvas runtime | Legacy app references it | Not migrated | Not found in CMF | No | No |
| Headless frame export worker | Legacy service creates job descriptors | Not migrated | Not found in CMF | No real frame render test | No |
| BPM/lip-sync services | Legacy app has Python services | Not migrated into CMF | Not found in CMF | Not tested in CMF | No |
| Clip import Spine/Lottie/BVH to DragonBones | Legacy app has converter helpers | Not migrated into CMF | Not found in CMF | Not tested in CMF | No |
| Remotion renderer project | Documented as default execution target | Specified | No component project found | Props contract tests only | No |
| Motion Canvas renderer project | Documented for explainers/frameworks | Specified | No component project found | Props contract tests only | No |
| Renderer props compiler | Yes | Yes | Yes, backend | Yes | Partial |
| Actual video export from transcript-timed composition | Yes | Thin spec only | Synthetic object URI only | Contract tests only | No |
| Operator approval workbench for composition evals | Yes | Thin spec only | No UI found | No | No |

## 4. What Works Now

The following is working at the Python contract/service level:

- Rig manifests can represent layers, pivot points, mouth shapes, eye/brow variants, gestures, body layers, preview tests, status, and version hashes.
- Rig validation blocks missing layers, missing pivots, missing body layers, insufficient mouth/eye/gesture variants, missing preview tests, failed preview tests, and missing version hashes.
- Creative library services can approve/repair/reject rig and library items and enforce brand-scoped creative assets.
- Deterministic renderer props can be built from Python-owned contracts.
- Deterministic renderer output records stable hashes, renderer versions, receipts, provider receipts, and synthetic object URIs.
- Targeted tests pass:
  - `test_paper_cut_rig_and_creative_libraries.py`
  - `test_deterministic_remotion_and_motion_canvas_rendering.py`
  - Result: 13 passed.

## 5. What Does Not Work Yet

The following is not operational inside `THE CMF STUDIO`:

- No migrated `apps/animation-studio` web app.
- No verified Next/Pixi/DragonBones editor under the CMF project folder.
- No actual Pixi canvas mount implementation found in CMF.
- No actual headless Node/Pixi/DragonBones renderer worker found in CMF.
- No actual Remotion project with video components found in CMF.
- No actual Motion Canvas project with Paper-Cut explainer scenes found in CMF.
- No command that takes transcript beat map + Brand Context + Paper-Cut rig + template JSON and outputs a real rendered video file.
- No visual eval harness that compares Paper-Cut outputs against doctrine-specific fixtures.
- No UI surface for the operator to preview animation, inspect beats, patch bone overrides, approve eval receipts, and export final video.
- No migrated BPM/lip-sync/clip-import services from the legacy Animation Studio into the CMF Python package.

## 6. Legacy Animation Studio Findings

Legacy path:

`D:\Work\The Conscious Coaching Factory\apps\animation-studio`

Useful assets found:

- `package.json`: Next 14, React, PixiJS, `@pixi/react`, Zustand, WaveSurfer, Tailwind.
- `app/page.tsx`: 6-panel editor shell with Clip Library, Beat Timeline, Bone Inspector, Layer Manager, Audio Panel, Transport Controls, Gate O on boot, and export patch action.
- `app/types.ts`: Character package, clip library, manifest patch, BPM analysis, studio state, scene presets, character overlay, Remotion manifest, lip-sync keyframe, frame export job contracts.
- `app/scene-presets.ts`: SC-01 through SC-08 scene/format matrix.
- `app/two-character.ts`: two-character layouts for primary/secondary actor interactions.
- `app/gate-o.ts`: executable pre-session validation questions.
- `services/bpm_service.py`: BPM detection.
- `services/lip_sync_service.py`: amplitude-to-jaw keyframe generation.
- `services/clip_import_service.py`: Spine/Lottie/BVH conversion helpers into DragonBones-like animation data.
- `services/frame_export_service.py`: frame/pose export job descriptors and safety checks.
- `api/main.py`: FastAPI endpoints for BPM, lip sync, frame export, pose export, clip import, and package safety validation.

Critical limitation:

The legacy app describes production frame rendering as a Node.js service using `@pixi/node` and DragonBonesJS delegated through a subprocess, but no such renderer worker file was found in the app folder during this audit. The UI also includes a placeholder canvas region rather than a verified mounted Pixi/DragonBones runtime in the inspected `page.tsx`.

## 7. Spec Protocol Compliance Finding

The spec protocol requires the following minimum structure:

1. Files Read.
2. Overview.
3. Context for Development, including architecture traceability, existing backend integration, ADR-05 primitives, CBAR mandate enforcement, and technical decisions.
4. Implementation Plan.
5. Primary Output Schema.
6. Backward Compatibility Fallback.
7. Tasks.
8. Acceptance Criteria with failure examples and CBAR references.
9. Dependencies.
10. Testing Strategy.

The protocol also requires:

- Full PRD/module loading before writing.
- Existing code/service/model/database/API mapping.
- Relevant primitive YAML IDs and constraints.
- CBAR mandate enforcement in Section 3.
- One spec at a time during audit and build.
- No implementation against ambiguous or thin specs.

## 8. Recent Spec Compliance Status

| Spec Range | Finding |
|---|---|
| TS-CMF-020 | Much closer to the required protocol. It includes files read, overview, traceability, legacy mapping, implementation plan, schema, commands/events/receipts, migration fallback, CBAR, tasks, ACs, dependencies, and tests. It still should be revised to explicit 10-section protocol if being used as strict build law. |
| TS-CMF-080 | Broad and useful as a synthesis spec. It is closer to protocol than TS-CMF-081 through TS-CMF-092, but it owns too much surface area and should be decomposed only through fully compliant companion specs. |
| TS-CMF-081 through TS-CMF-092 | Not protocol-compliant as build specs. They are thin decomposition notes with purpose, inputs, contracts, blockers, ACs, and tests, but they lack mandatory Files Read, full existing backend integration, exact primitive IDs, CBAR mandate enforcement, architecture component maps, detailed implementation plans, dependency chains, backward compatibility fallbacks, protocol-grade tasks, and full acceptance criteria mapped to gates/receipts. |

## 9. Why This Happened

The immediate cause is that TS-CMF-081 through TS-CMF-092 were written as fast functional decomposition companions to repair an identified composition-runtime gap, not as full Era 3 / CMF canonical build specs.

That shortcut violates the writing protocol because the protocol is not just formatting. It exists to prevent exactly this failure mode: documents that sound architecturally correct but do not give a coding agent enough exact authority to implement safely.

## 10. Consequences

If the current thin specs are treated as build-ready, the consequences are serious:

- Build agents will improvise missing behavior because required implementation detail is absent.
- Paper-Cut could collapse into flat generated images instead of deterministic layered animation.
- Remotion/Motion Canvas could be treated as vague renderer names instead of actual typed execution boundaries.
- Transcript timing may not bind frame-accurately to avatar state, motion cues, captions, SFX, and scene transitions.
- Operator UI requirements will remain ambiguous, producing dashboards rather than a true animation workbench.
- Eval gates will be non-executable because primitives and doctrine checks are not fully mapped to tests.
- Receipts will lack enough reconstruction evidence to prove why a scene was approved.
- Legacy Animation Studio assets will be forgotten or duplicated incorrectly.
- Open-source integrations will become inspiration only, not controlled adapters.
- The build ledger cannot honestly mark specs as built because the spec law is incomplete.

## 11. Required Repair Plan

### Repair 1: Create a CMF Animation Studio Migration Spec

Write a full canonical spec for migrating/adapting `D:\Work\The Conscious Coaching Factory\apps\animation-studio` into `THE CMF STUDIO`.

This spec must cover:

- Next/Pixi operator editor.
- Character package loading.
- Beat timeline.
- Bone inspector and manifest patching.
- Layer manager.
- Audio panel.
- Transport controls.
- Gate O adaptation into CMF doctrine gates.
- Two-character interaction layouts.
- Export patch receipts.
- Integration with CMF brand, guest workspace, asset code, beat map, and render contracts.

### Repair 2: Create a Headless 2D Frame Renderer Spec

Write a full canonical spec for the missing Node/Pixi/DragonBones or alternative deterministic renderer worker.

This spec must cover:

- Rig manifest ingestion.
- Layer compositing.
- Bone transform application.
- Clip playback.
- Lip sync jaw keyframes.
- Scene preset placement.
- Frame export naming.
- Transparent PNG sequence output.
- Golden-frame tests.
- Safety limits.
- Failure receipts.

### Repair 3: Revise TS-CMF-086

TS-CMF-086 must be rewritten from a thin Paper-Cut runtime note into a full build spec.

Mandatory additions:

- Files Read.
- Existing backend integration.
- Legacy Animation Studio integration.
- Exact source sections from Brand Genesis V3 and Greenfield context.
- Primitive IDs and doctrine constraints.
- Motion recipe schema.
- Materiality eval schema.
- SFX binding schema.
- Preview renderer requirements.
- Acceptance criteria with failure examples and receipt/eval references.

### Repair 4: Revise TS-CMF-090

TS-CMF-090 must be rewritten to include actual renderer component architecture, not only prop rules.

Mandatory additions:

- Component registry.
- Remotion project boundary.
- Motion Canvas project boundary.
- Generated TypeScript consumption.
- Preview/final render parity.
- Props hash reconstruction.
- Asset scope enforcement.
- Pixel/canvas nonblank tests.
- Golden output tests.

### Repair 5: Create a Transcript-to-Animation Timing Spec

TS-CMF-084 must be expanded or split to cover frame-accurate binding:

- Transcript segment to beat map.
- Beat map to avatar state.
- Beat map to motion cue.
- Beat map to caption cue.
- Beat map to SFX cue.
- Beat map to visual emphasis.
- Handling pauses, interruption, reaction, interviewer/guest alternation.

### Repair 6: Create a Doctrine/Primitive Visual Eval Harness Spec

A dedicated spec must define how every composition is validated by at least three primitives/doctrines before build or render approval.

This must include:

- Eval target selection.
- Eval run command.
- `EvaluationReceipt`.
- Approval blocker.
- Review read model.
- UI surfacing in the approval workbench.

### Repair 7: Run Protocol Audit One Spec at a Time

Per `TRIGGER_COMMAND_AUDIT.md`, each target spec must be audited one at a time against the five lenses. Do not batch-pass TS-CMF-080 through TS-CMF-092.

Priority order:

1. TS-CMF-086 Paper-Cut Runtime.
2. TS-CMF-090 Renderer Prop Compiler and Component Harness.
3. New CMF Animation Studio Migration Spec.
4. New Headless 2D Frame Renderer Spec.
5. TS-CMF-084 Transcript Beat Map.
6. TS-CMF-092 Operator Approval Workbench.
7. TS-CMF-080 Composition Runtime.

## 12. Build Readiness Verdict

The CMF 2D Animation Studio is not build-ready as a full product surface until the above spec repairs are complete.

Backend foundations are partially build-ready and tested. The actual animation studio, Paper-Cut runtime, and rendering stack are not operationally built inside `THE CMF STUDIO`.

Status:

- Backend rig/creative/render contracts: `PARTIAL PASS`.
- Legacy animation-studio reference: `USEFUL BUT NOT MIGRATED`.
- Paper-Cut runtime: `NOT BUILT`.
- 2D avatar editor: `NOT BUILT IN CMF`.
- Remotion/Motion Canvas production components: `NOT BUILT`.
- Actual video output from transcript-timed composition: `NOT VERIFIED / NOT OPERATIONAL`.
- Specs TS-CMF-081 through TS-CMF-092: `NOT BUILD-LAW COMPLIANT`.

