# CMF Studio Predecessor Migration Audit V1

## Verdict

`THE_CMF_STUDIO(2).zip` is not totally outdated.

It is a predecessor implementation containing a substantial prototype of the future
Atomic Harness Pipeline, Composition Runtime, category-native editing engines, render
adapters, evaluation, repair, artifact storage, and operator surfaces.

It is superseded as constitutional and product authority. It must not be restored as
one monolithic product or treated as the canonical source of current semantics.

## Evidence from the archive

- 4,743 files after extraction.
- 564 Python source files under `src/ccp_studio`.
- 129 primary test files under `tests/cmf_studio`.
- 994/994 legacy tests passed in a clean local run with `PYTHONPATH=src`.
- 88 repository modules are explicitly in-memory implementations.
- The archive contains a React operator UI with timeline and SuperVisual workbenches.
- It contains contracts and services for composition runtime, video editing, reaction
  templates, pipeline recipes, deterministic rendering, Remotion/FFmpeg adapters,
  render QA, local workers, provider preflight, artifacts, and Format 02 orchestration.
- Real execution remains mostly fake, dry-run, synthetic, or contract-only.
- The archive contains no canonical packaged Python application at the root, no
  production database implementation, and no verified active Remotion component project.
- Its own handoff and audits explicitly classify real execution as incomplete.

## Correct authority treatment

```text
Current Constitution and approved PRDs
    ↓
Current Builder / VAE / Delegation contracts and receipts
    ↓
New Atomic Harness Pipeline authority
    ↓
Selected migrated CMF Studio implementations
    ↓
Archived CMF Studio material
```

The old Studio may contribute code and evidence. It cannot override current product
boundaries, current format ontology, human authority, wrong-reading locks, or claim ceilings.

## What the attached chat got right

The chat correctly distinguishes:

- editing taste from mere tool calling;
- visual policy learning from command routing;
- deterministic validation from model judgment;
- large teacher models from smaller specialist executors;
- Needle as a possible late compression target;
- composition runtime from visual-asset production.

It also correctly emphasizes Composition IR, Visual Syntax, recipes, preference data,
renderer validation, and human corrections.

## What the chat missed

The chat states that the composition/editing runtime is not implemented as a dedicated
current product. That is correct for the current canonical product split, but incomplete
historically.

The old CMF Studio already contains a prototype composition and editing runtime:

- `contracts/composition_runtime.py`
- `services/composition_runtime_service.py`
- `contracts/video_editing_engine.py`
- `services/video_editing_engine_service.py`
- `contracts/studio_pipeline_recipe_harness.py`
- pipeline recipe/run/step services
- deterministic rendering contracts and services
- Remotion/FFmpeg adapter contracts and services
- render QA
- reaction-editing templates
- Format 02 golden-path orchestration
- timeline and SuperVisual operator UI

Therefore the next product should be extracted from this predecessor rather than designed
from a blank page.

## Migration classes

### RETAIN DIRECTLY

Retain only after namespace, dependency, and authority review:

- canonical hashing and immutable receipt patterns;
- deterministic validators and pure geometry/timeline helpers;
- test fixtures and rejection cases;
- renderer metadata, ffprobe, frame-sampling, caption, audio and QA contracts;
- local artifact references and path-safety logic;
- undo, rollback and idempotency patterns;
- operator read-model ideas and selected UI primitives.

### EXTRACT AND ADAPT

These are the highest-value assets.

1. **Pipeline Recipe Harness**
   - Becomes the Atomic Harness Pipeline execution profile.
   - Recipe steps become phase/node execution records.
   - Approval gates become explicit human gates.
   - Artifacts and receipts remain typed.
   - Must consume `AtomicHarnessDefinition` rather than define its own meaning.

2. **Composition Runtime**
   - Becomes category-owned composition capabilities inside Atomic Harness runtime.
   - Preserve BBOX, layers, beat maps, template bindings, renderer props and evaluation.
   - Replace old route IDs with Category → Master → Subformat → Atomic Unit lineage.

3. **Video Editing Engine**
   - Becomes Short-Form Edited Video runtime modules.
   - Preserve timeline, tracks, captions, motion, transitions, source references, audio
     plans and export contracts.
   - Add current Activative Sequence, wrong-reading and source-truth locks.

4. **Format 02 Golden Path**
   - Becomes the first compatibility vertical slice for the new Pipeline.
   - Preserve object-spine and test-fixture lessons.
   - Remove fake approval and fake-render success implications.

5. **2D Character Engine**
   - Preserve typed program, rig, performance, compatibility, eval and repair schemas.
   - Reconcile with the current 13 character-performance registry requirements.

6. **Carousel and Single-Image Composition Atlases**
   - Use as candidate Visual Syntax registries, synthetic-data seeds and benchmark cases.
   - Do not treat old compositions as current Master/Subformat authority automatically.

7. **Remotion/FFmpeg and Local Worker Contracts**
   - Preserve as external runtime adapter contracts.
   - Real execution must remain outside Builder and behind pipeline capability gates.

8. **Render QA**
   - Preserve technical checks and composite receipts.
   - Add rendered-output Visual Syntax re-parsing and current evaluation ownership.

9. **Template Preview Atlas**
   - Preserve deterministic previews as pre-spend inspection tools.

10. **Operator UI**
    - Migrate selected timeline, project, evidence, candidate and QA panels.
    - Replace embedded semantics with API-provided current contracts.

### REWRITE AROUND CURRENT AUTHORITY

- Pi/DSPy orchestration as universal runtime authority;
- agent factory and hidden persona selection;
- generic role prompts that collapse explicit actors;
- old doctrine hierarchy centered on primitives/archetypes rather than the current
  Constitution and Activative Intelligence;
- old format IDs and the “four formats” worldview;
- old Content Harness/CMF Studio boundaries;
- old direct provider assumptions;
- old skill architecture where skills, programs, tools and models are blurred;
- legacy memory admission rules not aligned to current evidence and authority states.

### ARCHIVE OR REMOVE FROM ACTIVE CODE

- nested ZIP bundles and duplicate integration patches;
- `.pyc` and cache artifacts;
- reference copies of older repositories mixed with active source;
- hard-coded commercial pricing and Publer-specific product flows from the core runtime;
- fake provider results presented as completed production objects;
- synthetic object URIs presented as actual rendered assets;
- obsolete provider/model pins;
- historical planning prompts treated as executable authority.

## Current-to-new product map

| Old CMF Studio area | New owner |
|---|---|
| Visual Syntax discovery and format formalization | Atomic Harness Builder |
| Pipeline Recipe Harness and orchestration spine | Atomic Harness Pipeline |
| Composition Runtime and Video Editing Engine | Atomic Harness Pipeline, category-owned |
| Model/DSPy programs | Pipeline Model Program Registry |
| Provider image generation and visual repair | Visual Asset Editor |
| Cross-product envelopes and lifecycle | Delegation Protocol |
| Remotion/HyperFrames/animation rendering | External runtime adapters |
| Interview preparation and expression capture | Interview Expression product |
| Operator workbenches | Product-specific Control Tower projections |
| Program-wide authority and compatibility | Program Control |

## Model Program migration

The old DSPy programs are useful task decompositions and possible data generators, but
they are not yet the current Model Program architecture.

A new Model Program must bind:

- exact capability;
- owning module and phase;
- base model and adapter identity;
- allowed tools;
- phase-local context;
- input and output contracts;
- validation;
- evaluator;
- escalation;
- training/evaluation receipts;
- invalidation and rollback.

The old code can supply:

- task names;
- structured inputs and outputs;
- deterministic examples;
- fixtures;
- failure cases;
- operator corrections;
- golden-path traces.

It cannot supply final current labels without constitutional and Visual Syntax review.

## Recommended extraction sequence

### Wave 0 — Freeze and inventory

- Hash the original archive.
- Exclude caches, nested bundles and reference copies from the active candidate set.
- Produce file-level dispositions.

### Wave 1 — Create `04_ATOMIC_HARNESS_PIPELINE`

Define it as the runtime consumer of `AtomicHarnessDefinition`.

Initial kernel:

1. definition loader and integrity verification;
2. phase scheduler;
3. Minimum Complete Context loader;
4. capability resolver;
5. Model Program resolver;
6. deterministic tool executor;
7. typed handoff engine;
8. event and receipt store;
9. evaluator and repair controller;
10. external runtime and VAE boundary.

### Wave 2 — Port the old generic runtime spine

Port and adapt:

- pipeline recipes/runs/steps/gates;
- artifact references;
- command/idempotency patterns;
- QA receipts;
- rollback/recovery;
- operator inspection.

### Wave 3 — Format 02 compatibility slice

Use fixed assets and a dry-run renderer first.

```text
AtomicHarnessDefinition
→ Pipeline phase execution
→ Format 02 performance/composition program
→ Remotion request
→ deterministic fake adapter
→ QA and Visual Syntax comparison
→ human gate
```

### Wave 4 — real renderer proof

Add a real renderer adapter only after deterministic contracts and rollback pass.

### Wave 5 — Model Programs

Run base models in shadow mode, record traces, generate synthetic legal/illegal cases,
render and reparse outputs, then fine-tune specialists.

### Wave 6 — VAE and Delegation integration

The Pipeline emits a Visual Asset Demand only when required ingredients are missing,
invalid, or require external production/repair.

## Two different first pilots

- **First Pipeline migration slice:** Format 02, because the predecessor and current
  program both have the strongest structural support there.
- **First editing-policy model benchmark:** Carousel or SuperVisual composition, because
  static BBOX and reading-order conformance are easier to isolate and measure.

## Final disposition

```yaml
totally_outdated: false
current_authority: false
production_ready: false
directly_restartable_as_monolith: false
valuable_predecessor_runtime: true
extract_into_atomic_harness_pipeline: true
use_as_training_and_benchmark_source: true
```
