# AGENT_HANDOFF — M0078

## Status

`COMPLETE_WITH_OPERATOR_DECISION_REQUIRED`

The bounded M0078 artifact is implemented as a reference-only registry/schema, explanatory documentation, focused tests, and an evidence receipt. No runtime service, canonical semantic program, prompt executor, retrieval system, UI, database migration, or external runtime integration was changed.

## Changed/new repository paths

- `docs/cae/CAE_Production_Reference/M0078_shot_grammar_reference.yaml`
- `docs/cae/CAE_Production_Reference/M0078_SHOT_GRAMMAR_AND_ASSISTANT_REFERENCE.md`
- `tests/cae/test_m0078_shot_grammar_reference.py`
- `docs/cae/CAE_Production_Reference/M0078_EVIDENCE_RECEIPT.json`
- `AGENT_HANDOFF.md`

## Rationale

The brownfield already contains canonical CAE objects for semantic scenes, asset demand/annotation, visual requirements, visual prompt specifications, candidate/storyboard lineage, operator decisions, and production-program state. Creating a second runtime shot or assistant state model would violate M0078. The smallest compatible change is therefore a source-attributed reference vocabulary that maps to those existing authorities.

Seedance2 contributes bounded shot/camera/timing language and explicit reference-role hygiene. Toonflow contributes explicit scene/shot/asset fields. WaooWaoo contributes explicit assistant-turn/resource targeting and revision interaction. Provider-specific generation logic and external UI/state are excluded.

## Exact commands and results

1. `python -m pytest -q tests/cae/test_m0078_shot_grammar_reference.py`
   - Exit: `0`
   - Observed: `7 passed in 0.15s`
   - Note: the environment emitted an `artifact_tool` spreadsheet warmup RemoteError to stderr during Python startup. The focused pytest process still completed successfully with exit code 0.

2. `git rev-parse HEAD`
   - Exit: non-zero
   - Observed: `fatal: not a git repository (or any of the parent directories): .git`
   - This prevents honest reporting of an exact CAE commit SHA from the uploaded archive.

## External source records

### OpenChatCut / Seedance2 adapter

Repository: `https://github.com/0xsline/OpenChatCut`  
Exact local source: `engines/video/openchatcut/upstream/src/agent/skills/video-gen/references/seedance2.md`  
License evidence: `engines/video/openchatcut/upstream/package.json` → `AGPL-3.0-or-later`  
Upstream commit: `UNVERIFIED_FROM_ARCHIVE` (Git metadata absent)

### Toonflow

Repository: `https://github.com/HBAI-Ltd/Toonflow-app`  
Exact sources:
- `data/modelPrompt/video/universalMulti-parameterMode.md`
- `data/modelPrompt/video/universalFirstAndLastFrameMode.md`
- `data/modelPrompt/video/wan2.6Single-imageFirstFrameMode.md`
- `src/routes/assetsGenerate/generateAssets.ts`

Observed ref: `master`, short commit `640861b`; full SHA was not exposed by the available evidence view.  
License: Apache-2.0 plus HBAI-Ltd supplemental commercial terms.

### WaooWaoo

Repository: `https://github.com/waooAI/waoowaoo`  
Exact sources:
- `src/features/project-workspace/ProjectWorkspace.tsx`
- `src/features/project-workspace/workspace-assistant-focus.ts`
- `src/features/project-workspace/canvas/lifecycle/workspace-canvas-lifecycle.ts`
- `src/features/project-workspace/canvas/lifecycle/resource-lifecycle.ts`

Source commit: `6cbbe22cc6492159e0f649d507e4e21a9aec3074`  
License: `CC BY-NC-SA 4.0`

No external source code was copied.

## Evidence classes

- `DOCUMENT`: mandatory CAE constitutional/PRD/convergence sources and the implementation-direction equivalent paths found in the brownfield.
- `SCHEMA`: M0078 reference vocabulary and canonical CAE mapping.
- `REGISTRY_SOURCE`: exact upstream files/symbols and their stated licenses/source refs.
- `TEST`: seven focused properties, including a good-looking-but-wrong timing counterexample and deterministic round-trip.
- `OPERATOR_DECISION_REQUIRED`: exact CAE Git commit SHA unavailable from archive; native external runtime/visual inspection not performed.

## Limitations

1. The uploaded archive is not a Git worktree; no `.git` metadata is present. Therefore the exact CAE commit SHA cannot be established without inventing it.
2. The OpenChatCut/Seedance2 adapter source exists exactly in the archive, but the upstream commit is not preserved.
3. Toonflow's current `master` was observed at short commit `640861b`; the full SHA could not be captured from the available GitHub evidence rendering.
4. No native external runtime reachability was proved.
5. No real visual preview was generated or operator-reviewed; semantic/perceptual/creative acceptance remains a human gate.

## Mandatory-source path substitutions

The archive did not contain the mandate's three requested paths at their exact root locations. Equivalent current brownfield documents were located at:

- `governance/program-control/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md`
- `governance/program-control/00_CONSTITUTION/current-v1.1/governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`
- `governance/program-control/00_CONSTITUTION/current-v1.1/docs/implementation/01_PI_CODING_AGENT_BUILD_PLAN.md`

The exact M0078 mandate file itself was not present in the archive; this execution used the user-supplied mandate text as the controlling mandate.

## Rollback

Rollback consists only of removing the five new M0078 artifacts listed above. No pre-existing CAE state or source evidence was modified.

## Operator decision requested

Select exactly one:

- `APPROVE`
- `APPROVE-WITH-LIMITATIONS`
- `REJECT`

Recommended decision: `APPROVE-WITH-LIMITATIONS` pending confirmation of the CAE commit identity and any desired operator review of external source licensing/provenance.
