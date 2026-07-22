# CCP Format 02 Golden Path Orchestrator V1 Integration Bundle

This bundle proves the whole backend compiler chain end-to-end for one deterministic Format 02 fixture.

## Purpose

```text
health myth source truth
→ Narrative Story Doctor / Extraction Intelligence
→ Format Intelligence
→ Composition Intelligence / Format 02 Pack
→ Avatar Performance Layer
→ Video Editing Engine V1
→ fake proxy render
→ eval
→ fake final render
→ approval
→ export pack
```

## Core doctrine

```text
This is not a new harness.
This is a golden-path recipe that must later be wired into the existing OrchestrationRun / StageExecutionPlan / ValidationContract / StageExecutionReceipt spine.
```

## Apply after

Required:

```text
Narrative Story Doctor + Content Extraction Intelligence V1
Format Intelligence V1
Narrative → Format Bridge V1
Composition Intelligence Core + Format 02 Pack V1
Avatar Performance Layer V1
Video Editing Engine V1
```

## Do not

```text
Do not call providers.
Do not call Ideogram.
Do not call Flux.
Do not call Remotion.
Do not call FFmpeg.
Do not render real media.
Do not add UI/API endpoints in this branch.
Do not create a second orchestration harness.
Do not duplicate upstream compiler logic.
```

## What this bundle adds

```text
GoldenPathRecipeSpec
GoldenPathRun
GoldenPathStageResult
Format02GoldenPathInput
Format02GoldenPathSceneSeed
Format02GoldenPathOutput
GoldenPathObjectSpineMap
GoldenPathReceipt
GoldenPathBlocker

Format02GoldenPathOrchestratorService
fixtures/golden_path/*
tests/cmf_studio/test_format02_golden_path_orchestrator_v1.py
```

## Milestones

### Milestone 1 — Docs, registries, contracts, fixtures

Copy/add:

```text
docs/architecture/golden-path-orchestrator/
fixtures/golden_path/
registries/canonical/golden_path_orchestrator/
src/ccp_studio/contracts/golden_path_orchestrator.py
FORMAT02_GOLDEN_PATH_ORCHESTRATOR_V1_BUNDLE_MANIFEST.json
FORMAT02_GOLDEN_PATH_ORCHESTRATOR_V1_LOCAL_VERIFICATION.json
APPLY_FORMAT02_GOLDEN_PATH_ORCHESTRATOR_V1_PATCH.md
```

Commit:

```bash
git add .
git commit -m "feat(golden-path): add Format 02 orchestrator contracts and fixtures"
```

### Milestone 2 — Repository, service, skills

Copy/add:

```text
src/ccp_studio/repositories/golden_path_orchestrator.py
src/ccp_studio/services/format02_golden_path_orchestrator_service.py
registries/canonical/skills/shared/golden_path_orchestrator/
```

Commit:

```bash
git add .
git commit -m "feat(golden-path): orchestrate Format 02 backend chain"
```

### Milestone 3 — Tests

Copy/add:

```text
tests/cmf_studio/test_format02_golden_path_orchestrator_v1.py
```

Run:

```bash
PYTHONPATH=src python -m compileall -q src
PYTHONPATH=src python -m pytest -q tests/cmf_studio
```

Commit:

```bash
git add .
git commit -m "test(golden-path): verify Format 02 source-to-fake-export"
```

## Core test

```text
test_health_myth_format02_golden_path_runs_source_to_fake_export
```

It proves:

```text
brand_context_version_id persists
source_span_refs persist
8 scene programs compile
8 composition decisions lock
8 avatar plans compile
8 audience proxy plans compile
no lip sync appears
audience proxies have SFL functions
video timeline compiles
Remotion props include timeline_program_id
OTIO audit timeline compiles
fake proxy render emits hash
eval passes
final timeline locks
fake final render emits hash
approval packet is produced
export pack requires approval
```

## Existing orchestration spine integration

If the repo contains:

```text
src/ccp_studio/contracts/orchestration.py
src/ccp_studio/services/orchestration.py
```

then the coding agent should wire:

```text
GoldenPathRun → OrchestrationRun
GoldenPathStageResult → StageExecutionReceipt
Golden path gate codes → ValidationContract
```

Do not create a second harness.
