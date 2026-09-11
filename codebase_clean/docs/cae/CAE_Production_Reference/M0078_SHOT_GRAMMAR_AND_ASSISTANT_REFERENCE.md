# M0078 — Shot Grammar and Assistant Extraction Reference

**Status:** `REFERENCE_ONLY`  
**Mandate:** `M0078`  
**Decision boundary:** adopt bounded behavior; do not create a second semantic authority.

## 1. Brownfield decision

The existing CAE path already owns the semantic-program/state boundary. This reference therefore does **not** add runtime classes or state transitions. It maps the external vocabulary onto existing CAE objects:

- `SemanticSceneSpec` owns scene timing and spoken text.
- `AssetDemandSpec` / `AssetAnnotationItem` own typed asset demand, rights/source lineage and evidence.
- `VisualRequirement` / `VisualPromptSpec` own visual requirement, framing and provider-neutral prompt annotations.
- `ContentCandidateRecord` / `EditorialStoryboardRecord` retain version, predecessor, evidence links and operator decision references.
- Existing editorial coordinator and production-program gates remain the validator/state authority.

**Claim class:** `SCHEMA` for the mapping above; `TEST` for enforcement; `REGISTRY_SOURCE` for external behavior; `DOCUMENT` for repository doctrine.

## 2. Upstream-to-CAE mapping

### Seedance2 → CAE

**Exact source:** `engines/video/openchatcut/upstream/src/agent/skills/video-gen/references/seedance2.md`  
**Source repository:** `https://github.com/0xsline/OpenChatCut`  
**Local license evidence:** `engines/video/openchatcut/upstream/package.json` → `AGPL-3.0-or-later`  
**Source commit:** not preserved in the uploaded archive; recorded as `UNVERIFIED_FROM_ARCHIVE`.

Adopted language:
- shot size: `Close-up`, `MCU`, `Medium`, `Full`, `Long`, `Extreme long`
- angle: `Eye-level`, `Low`, `High`, `OTS`, `Top-down`
- move: `Push-in`, `Pull-out`, `Pan`, `Tilt`, `Dolly/Track`, `Orbit`, `Handheld`
- lens/effect: `Shallow DOF`, `Slow-mo`, `Time-lapse`, `Hitchcock zoom`
- timestamped multi-shot segmentation; segment windows must reconcile to the parent duration
- one primary camera move per sub-shot
- typed `@ImageN` / `@VideoN` / `@AudioN` references with role explanation
- edit/extend/bridge produces a new downstream result rather than mutating the source timeline item

Excluded:
- Seedance provider/API parameter names and queueing
- Kling-only `shotType`, `multiPrompts`, or `mode`
- provider reachability and generation success

**Claim class:** `REGISTRY_SOURCE`.

### Toonflow → CAE

**Exact sources:**
- `data/modelPrompt/video/universalMulti-parameterMode.md`
- `data/modelPrompt/video/universalFirstAndLastFrameMode.md`
- `data/modelPrompt/video/wan2.6Single-imageFirstFrameMode.md`
- `src/routes/assetsGenerate/generateAssets.ts`

**Source repository:** `https://github.com/HBAI-Ltd/Toonflow-app`  
**Observed source ref:** `master`, commit `640861b` (full SHA not reproduced by the available GitHub evidence view)  
**License:** Apache-2.0 plus HBAI-Ltd supplemental commercial terms.

Adopted field grammar:
`scene`, `related assets`, `duration`, `shot size`, `camera`, `character action`, `emotion`, `lighting`, `dialogue`, `sound effect`, `related asset IDs`.

Asset references remain typed and ordered; CAE does not infer semantic authority from an ordinal `@N`.

Excluded:
- Toonflow prompt strings as normative semantics
- model-specific formatting/XML
- provider execution and generation UI behavior
- direct source-code extraction

**Claim class:** `REGISTRY_SOURCE`.

### WaooWaoo → CAE

**Exact sources:**
- `src/features/project-workspace/ProjectWorkspace.tsx`
- `src/features/project-workspace/workspace-assistant-focus.ts`
- `src/features/project-workspace/canvas/lifecycle/workspace-canvas-lifecycle.ts`
- `src/features/project-workspace/canvas/lifecycle/resource-lifecycle.ts`

**Source repository:** `https://github.com/waooAI/waoowaoo`  
**Source ref:** `main`, commit `6cbbe22cc6492159e0f649d507e4e21a9aec3074`  
**License:** CC BY-NC-SA 4.0.

Adopted behavior:
- explicit assistant discussion/refinement action
- assistant turn identity + source message identity + explicit resource targets
- canvas selection alone does not retarget assistant context
- refinement preserves prior result and establishes new-version lineage

Excluded:
- WaooWaoo UI/state implementation
- source-code copying
- automatic CAE promotion
- any implicit mutation from selection

**Claim class:** `REGISTRY_SOURCE`.

## 3. CAE reference vocabulary

The full machine-readable vocabulary is in `M0078_shot_grammar_reference.yaml`.

| Reference field | CAE owner | Boundary |
|---|---|---|
| `scene_id` | `SemanticSceneSpec` | canonical scene/program state |
| `shot_id` | reference grouping | no new runtime authority |
| `start_seconds`, `end_seconds`, `duration_seconds` | `SemanticSceneSpec` | deterministic timing validation |
| `scene`, `visual_action`, `emotion` | `VisualRequirement` + semantic scene | CAE meaning remains upstream |
| `asset_refs` | `AssetAnnotationItem` / `AssetDemandSpec` | preserve evidence/source lineage |
| `shot_size`, `camera_angle`, `camera_move`, `lens_fx` | `VisualPromptSpec` metadata; downstream TransformationRecipe as applicable | model may propose; deterministic code bounds execution |
| `dialogue` | `SemanticSceneSpec.spoken_text` | preserve type/language |
| `audio_intent` | `SemanticProgram.visual_audio_specs` | provider-neutral intent |
| `continuity` | candidate/storyboard/asset lineage | prior results retained |
| `assistant_action`, `assistant_target_ids`, `base_revision` | existing editorial/candidate lineage | explicit target + revision only |
| `operator_decision` | gate/receipt infrastructure | operator-owned |

## 4. Motion/Transformation boundary

When Motion/Transformation is actually invoked, keep the existing chain:

`Editorial Intent → Narrative Editing Grammar → Editorial Expression Calculus → TransformationIntent → TransformationRecipe → primitives/keyframes`

The M0078 reference vocabulary supplies camera/timing words only. It does not authorize model-written geometry, automatic camera execution, or provider-specific motion control.

## 5. Assistant refinement contract

An assistant turn may **propose** a revision, but a governed transition requires:

1. explicit actor and target resource IDs;
2. an existing canonical CAE object or candidate lineage;
3. deterministic validation;
4. immutable preservation of the prior candidate/revision;
5. explicit operator decision where promotion is required;
6. receipt/evidence reference for the governed transition.

`canvas selection → assistant action` is explicitly **not** a valid state transition.

## 6. Evidence-first and external-runtime limits

The production order remains:

`RETRIEVE → TRANSFORM → COMPOSE → GENERATE`

This artifact is reference material only. It does **not** prove:
- external model/runtime availability,
- native generation fidelity,
- perceptual quality,
- semantic correctness of a generated preview,
- final creative acceptance.

Those require the existing runtime reachability evidence and operator gate.

## 7. Verification vectors

The focused test file proves:
- a well-formed shot passes;
- a plausible good-looking-but-wrong shot is rejected when declared duration disagrees with its time window;
- external/model authority cannot be used as CAE semantic authority;
- malformed source metadata is rejected;
- the YAML round-trips deterministically.

**Claim class:** `TEST`.

## 8. Mandatory-source path note

The uploaded repository did not contain these exact root paths from the mandate:
- `docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md`
- `governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`
- `AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/00_REPOSITORY_TO_PRODUCT_BUILD_PLAN.md`

Equivalent current brownfield documents were found under:
- `governance/program-control/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md`
- `governance/program-control/00_CONSTITUTION/current-v1.1/governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`
- `governance/program-control/00_CONSTITUTION/current-v1.1/docs/implementation/01_PI_CODING_AGENT_BUILD_PLAN.md`

The exact M0078 mandate file itself was not present in the archive; this execution used the user-supplied mandate text as the controlling mandate.

## 9. Scope

Added only:
- a reference registry/schema;
- its explanatory documentation;
- a focused CAE test;
- an evidence receipt;
- `AGENT_HANDOFF.md`.

No runtime service, canonical semantic model, prompt executor, retrieval service, UI, database migration, or external runtime integration was changed.
