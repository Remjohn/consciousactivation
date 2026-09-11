# M0083 Agent Handoff

## Status

`IMPLEMENTED — FOCUSED TESTS PASS — OPERATOR REVIEW REQUIRED`

The bounded TransformationIntent / TransformationRecipe projection layer has
been implemented by extending the existing M0079 storyboard objects. No new
semantic-program, storyboard, retrieval, VAE, Design System, or runtime
authority was created.

## Objective completed

Implemented a compact taxonomy and deterministic compiler for:

`Editorial Intent → Narrative Editing Grammar → Editorial Expression Calculus → TransformationIntent → TransformationRecipe → primitives/keyframes`

The implementation supports the required TransformationIntent fields (`intent`,
`source`, `semantic_target`, `mode`, `emphasis`, `motion`, `constraints`),
registered recipes, bounded primitives/keyframe templates, source-quality-aware
motion reduction, authorization/stale-registry checks, and deterministic replay.

## Brownfield audit and reuse

Primary reusable objects and tests inspected:

- `packages/ca_runtime/src/ca_runtime/storyboard_session.py`
  - `TransformationIntent`
  - `TransformationRecipe`
  - `MotionPlan`
  - `StoryboardElement`
  - `StoryboardSessionStore._validate_revision_input`
  - `StoryboardSessionStore.compile_revision`
- `tests/cae/test_m0079_storyboard_session_revision.py`
- `docs/cae/CAE_Production_Reference/M0078_SHOT_GRAMMAR_AND_ASSISTANT_REFERENCE.md`
- `docs/cae/CAE_Production_Reference/M0078_shot_grammar_reference.yaml`
- existing `services/pipeline/contracts/schemas/transformation_contract.schema.json`
  was inspected and deliberately not duplicated or replaced.

The smallest compatible change was therefore to extend M0079's canonical
TransformationIntent/TransformationRecipe objects and add the missing bounded
compiler as a sibling runtime module.

## Authority mapping

| Evidence class | Exact source | Result |
|---|---|---|
| DOCUMENT / REGISTRY_SOURCE | `https://github.com/Remjohn/consciousactivation/blob/main/docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/00_REPOSITORY_TO_PRODUCT_BUILD_PLAN.md` | Establishes the native transformation projection, compact grammar, evidence-first order, and source-quality-aware editing. |
| DOCUMENT / REGISTRY_SOURCE | `https://github.com/Remjohn/consciousactivation/blob/main/docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/01_CAE_Product_Update_Visual_Asset_Editor.md` | Establishes the seven-field TransformationIntent contract and reusable TransformationRecipe concept. |
| DOCUMENT / SCHEMA | `https://github.com/Remjohn/consciousactivation/blob/main/docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/02_CAE_PRD_Update_Visual_Asset_Studio.md` | FR-VAE-003/004/007 require typed intents, registered recipes/fail-closed resolution, and source-quality governance. |
| DOCUMENT / REGISTRY_SOURCE | `https://github.com/Remjohn/consciousactivation/blob/main/docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/03_CONSCIOUS_E_MOTION_EDITING_STANDARDS_v2.md` | Requires evidence-first transformation, quality-aware reduction, justified motion, and intent-expressive keyframes. |
| DOCUMENT | `https://github.com/Remjohn/consciousactivation/blob/main/docs/cae/CAE_Production_Convergence_M65_M72_v1/07_PRODUCTION_OPERATOR_GATES/M72_final_production_gate_current_sync.md` | Confirms no automatic promotion and explicit operator gate. |
| DOCUMENT / SCHEMA | Local governed equivalents under `governance/program-control/00_CONSTITUTION/current-v1.1/` | Confirms the constitutional precedence and fail-closed operating context. |
| REGISTRY_SOURCE / DOCUMENT | `docs/cae/CAE_Production_Reference/M0078_SHOT_GRAMMAR_AND_ASSISTANT_REFERENCE.md` | Confirms the existing transformation chain and that camera/motion vocabulary does not authorize model-written execution. |

Authority source commit for the dated pack:
`de202244eb5b8e436685bf4e9ed02f93b6f5faa4`.

No external implementation repository was adopted. Therefore external commit and
license fields are `N/A` for this mandate.

## Implementation paths

### Modified

- `packages/ca_runtime/src/ca_runtime/storyboard_session.py`
  - added bounded intent/mode/motion/source-quality/source-role vocabularies;
  - added explicit `intent` to `TransformationIntent`;
  - added `source` compatibility alias;
  - normalized legacy M0079 intent-in-mode payloads;
  - added bounded intent/mode/motion/emphasis/reference validation;
  - added `.compile()` handoff to the deterministic compiler;
  - added governed-registry metadata fields to `TransformationRecipe` while
    preserving legacy storage shape.
- `packages/ca_runtime/src/ca_runtime/__init__.py`
  - exported M0083 vocabularies and compiler symbols.

### Added

- `packages/ca_runtime/src/ca_runtime/transformation_recipe.py`
  - registry version `M0083-1`;
  - eight compact templates covering all ten intents;
  - approved primitive vocabulary;
  - stale/authorization/mode/constraint/source-quality guards;
  - deterministic primitive/keyframe projection and recipe digest.
- `tests/cae/test_m0083_transformation_intent_recipe.py`
  - eleven focused acceptance tests.
- `docs/cae/specs/M0083/TRANSFORMATION_INTENT_RECIPE_SPEC.md`
  - implementation/reference artifact.
- `docs/cae/specs/M0083/AGENT_HANDOFF.md`
- `docs/cae/specs/M0083/M0083_EVIDENCE_RECEIPT.json`

## Test evidence

### Focused M0083 suite

Command:

`python scratch/run_single_test.py tests/cae/test_m0083_transformation_intent_recipe.py`

Observed result: **11 passed**.

Direct equivalent command:

`pytest -q -p no:asyncio tests/cae/test_m0083_transformation_intent_recipe.py`

Observed result: **11 passed, 10 Pydantic deprecation warnings**.

The warnings originate from the pre-existing repository's Pydantic v1-style
validators in `storyboard_session.py`; no Pydantic migration was attempted in
this bounded mandate.

### Syntax verification

Command:

`python -m py_compile packages/ca_runtime/src/ca_runtime/storyboard_session.py packages/ca_runtime/src/ca_runtime/transformation_recipe.py tests/cae/test_m0083_transformation_intent_recipe.py`

Observed result: **PASS**.

### Existing M0079 focused suite

Command:

`python scratch/run_single_test.py tests/cae/test_m0079_storyboard_session_revision.py`

Observed result: **collection error: `ModuleNotFoundError: No module named 'psycopg'`**.

This is an environment limitation in the supplied snapshot, not evidence of an
M0083 regression. The M0083 test module uses a test-only submodule import path to
avoid importing the package `__init__` dependency on the unavailable database
driver; production imports were not altered to hide or replace the dependency.

## Required verification properties covered

- normal success compilation;
- every declared intent resolves to a registered recipe;
- deterministic replay/idempotence of the compiled model payload;
- legacy M0079 normalization;
- good-looking-but-wrong `FOCUS + COMPARE` rejection;
- negative authorization check;
- stale registry rejection;
- missing source quality rejection for motion;
- low/degraded-quality motion reduction behavior;
- deterministic bounded scale clamping;
- malformed/free-form constraint rejection.

## What the tests do not prove

The focused suite does not prove final geometry correctness, safe-area validity,
source crop-history quality, renderer fidelity, external runtime availability,
actual playback, perceptual quality, semantic correctness of the upstream
intent, or operator approval. Those remain downstream validation/review gates.

The `SUBTLE_PAN` token is registered but exact geometry solving is intentionally
out of M0083 scope. `max_motion_amplitude_bps` is validated and carried as a
constraint for downstream motion calculus; this mandate does not implement a
second motion calculus authority.

## Evidence / receipt requirements

`docs/cae/specs/M0083/M0083_EVIDENCE_RECEIPT.json` records:

- supplied archive hash;
- authority-pack source and commit;
- changed/new paths;
- exact verification commands and observed results;
- evidence classes;
- external-source status;
- limitations;
- operator decision request.

## Scope control

All repository changes are inside the mandate boundary:

`packages/, services/, docs/cae/specs/, tests`

Only `packages/` and `docs/cae/specs/` plus `tests/cae/` were changed for M0083.
No `services/` files were modified.

## Rollback / recovery

Rollback should remove only the M0083 files and revert only the M0083 changes in
the two modified package files. Pre-existing M0079 storyboard/state behavior and
source evidence must be preserved. No database migration or external runtime
state was introduced.

## Exact Git commit SHA

`UNAVAILABLE — the supplied repository snapshot has no .git metadata.`

This is a release-evidence limitation, not a fabricated commit. The dated
authority-pack source commit is known and recorded separately:
`de202244eb5b8e436685bf4e9ed02f93b6f5faa4`.

## Operator decision requested

`APPROVE-WITH-LIMITATIONS` is requested for this implementation bundle, with the
following explicit limitations accepted:

1. The supplied snapshot does not contain Git metadata, so an exact implementation
   commit SHA cannot be truthfully reported.
2. The repository's existing M0079 suite cannot be collected in the supplied
   environment because `psycopg` is unavailable.
3. No external runtime reachability or perceptual visual acceptance is claimed.
4. Operator must review any real preview before promotion and confirm that the
   transformation serves meaning, preserves source lineage, and does not create
gratuitous attention.

Final decision vocabulary remains `APPROVE`, `APPROVE-WITH-LIMITATIONS`, or
`REJECT`. No self-promotion has occurred.
