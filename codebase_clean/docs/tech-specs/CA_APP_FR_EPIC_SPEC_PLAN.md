---
document_class: APP_REBUILD_FUNCTIONAL_REQUIREMENTS_AND_SPEC_PLAN
product: Conscious Activations
version: 1.0
status: READY_FOR_SPEC_WRITING
prepared: 2026-07-25
authority: CA_PROJECT_SNAPSHOT_V2 + PRD_CA_AHP_V1.2 + Specs_Builder_Library_CA_V2_1_3
purpose: >
  Provide the next agent with a complete, grounded, sequenced plan to turn the
  existing Phase-09 Python backend into a composable, debuggable, shippable
  React + FastAPI application. This document is the input to the CA Spec
  Lifecycle Controller (CA_SPEC_LIFECYCLE_CONTROLLER_SKILL.md). It produces
  Functional Requirements → Epics → Stories → Tech Specs in that order.
---

# Conscious Activations — App Rebuild: FR → Epic → Story → Spec Plan

## READ THIS FIRST — Context for the Next Agent

### What already exists (do not rewrite)
The Phase-09 branch of `github.com/Remjohn/consciousactivation` contains a complete,
tested Python backend across six packages:

| Package | Path | What it does |
|---|---|---|
| `cmf_builder` | `services/builder/src/` | Atomic Harness definition, validation, export |
| `cmf_activative_intelligence` | `services/air/src/` | Primitive coalitions, archetypes, Final Scripts, campaign |
| `cmf_pipeline` | `services/pipeline/src/` | Workflow execution, FFmpeg, Composition IR, retrieval, skills |
| `conscious_activations_interview_expression` | `services/interview/src/` | Interview ingestion, transcript, Expression Moments |
| `cmf_vae` | `services/vae/src/` | Visual asset planning, ComfyUI, SAM3/Lucida/GNM adapters |
| `ca_delegation_rc4` | `packages/ca_delegation_rc4/` | Delegation contract validation (RC4 release) |
| `ca_contracts` | `packages/ca_contracts/` | Shared schemas, canonical JSON |
| `ca_runtime` | `packages/ca_runtime/` | SQLite migrations, idempotency, receipts |
| `ca_release` | `packages/ca_release/` | SBOM, backup, release guards |

The Studio TypeScript domain layer exists at `services/studio/src/` (18 files, ~2,026 lines)
with correct types for CampaignOrder, ControlTowerProjection, TimelineProjection,
ChangeRequestProgram, ShipDecision, HumanResolutionEpisode.

### What does NOT exist (build this)
1. HTTP API layer (FastAPI) — zero HTTP endpoints exist today
2. React application — no UI exists beyond a reference HTML demo
3. Interview Composer integration — built internally, not in this repo
4. Real provider wiring (ComfyUI, SAM3, Remotion) beyond FFmpeg
5. Auth / workspace isolation / multi-tenancy

### The single product flow (never lose sight of this)
```
Brand Genesis (Voice DNA, Visual DNA, Brand Context)
  ↓
Interview Composer (research guest → engineer Brief → session plan)
  ↓  OR  ↓
Activative Interview Session    Imported Interview Upload
  ↓              ↓
Canonical Interview Source Package
  ↓
Expression Discovery (tags, Anchor Hits, Expression Moments)
  ↓
Activative Intelligence (tension, Primitive Coalition, Archetype, Final Script)
  ↓
Campaign Order (select Harness, choose outputs, set autonomy)
  ↓
Pipeline Execution (video, Carousel, SuperVisual, animation, VAE assets)
  ↓
Studio Supervision (Control Tower, revisions, evaluation, repair)
  ↓
Ship + Audit Export
```

### Naming conventions
- Directories: `kebab-case`
- Python files: `snake_case`
- React components: `PascalCase`
- TypeScript utilities: `camelCase`
- No capital-letter directory names anywhere in new code

---

## PART 1 — FUNCTIONAL REQUIREMENTS

These FRs describe what the application must do from a user and system perspective.
They reference existing code where it already exists. Each FR will anchor one or
more Stories and eventually one Tech Spec.

### Module A — Workspace and Brand Foundation

**FR-APP-001 — Workspace creation**
A user can create a named workspace tied to one coach identity. The workspace holds
all Brand Context Versions, Voice DNA records, Visual DNA records, Harness library,
and campaign history.
- Existing code: partial in `cmf_activative_intelligence` (brand_service.py)
- Missing: HTTP endpoint, React page, persistence to shared store

**FR-APP-002 — Brand Genesis session**
Within a workspace, the operator can run a Brand Genesis session to establish the
coach's Brand Context Version: Voice DNA (cadence, syntax, compression, pressure,
metaphor, anti-draft boundaries), Visual DNA (identity geometry, typography, color,
motion, Negative Space), and acting/identity references.
- Existing code: `cmf_activative_intelligence/services/brand_service.py`
- Missing: HTTP endpoint, React form, file upload for reference media

**FR-APP-003 — Brand Context Version management**
The operator can view, version, and select the active Brand Context Version. A new
version does not overwrite history; prior campaigns reference their exact version.
- Existing code: brand domain objects in AIR
- Missing: API + UI list/detail view

### Module B — Interview Composer

**FR-APP-010 — Guest research ingestion**
The operator can input a guest's name and provide URLs or upload documents (LinkedIn,
articles, podcast transcripts, social content). The system indexes this into a guest
research package.
- Existing code: Interview Composer built internally (not in repo yet)
- Action: integrate from internal build into `services/interview-composer/`

**FR-APP-011 — Activative Interview Brief generation**
Using the guest research package + active Brand Context Version + active Voice DNA,
the system generates an Activative Interview Brief: tension hypothesis, Matrix of
Edging seed, planned question sequence, expression targets.
- Existing code: internally built Interview Composer
- Missing in repo: API exposure, connection to AIR brief objects

**FR-APP-012 — Interview session scheduling and linking**
The operator can attach a recording date, link a recorded `.mp4` or audio file,
and transition the Brief into a live Canonical Interview Source Package upon upload.
- Existing code: `conscious_activations_interview_expression/source_package.py`
- Missing: HTTP POST endpoint, React upload UI

### Module C — Interview Admission (Both Entry Points)

**FR-APP-020 — Admit a Brief-led interview (Entry Point A)**
Given an accepted Activative Interview Brief and a recording upload, the system
creates a Canonical Interview Source Package preserving the planned/observed
distinction. Planned anchors are labeled; no planned tags are fabricated as observed.
- Existing code: `interview_expression/source_package.py`, `canonical.py`
- Missing: HTTP endpoint, React upload + status page

**FR-APP-021 — Admit an imported interview (Entry Point B)**
Given only a video/audio file and transcript (no Brief history), the system creates
a Canonical Interview Source Package with `planning_lineage: ABSENT_NOT_CREATED`.
No fabricated Brief, anchors, or Matrix paths.
- Existing code: `interview_expression/source_package.py` (imported path)
- Missing: HTTP endpoint, React upload UI (simpler form than FR-APP-020)

**FR-APP-022 — Transcript alignment and phrase packing**
The system aligns the transcript to the media, assigns word-level timestamps,
identifies speakers, creates packed phrase segments, and preserves hesitations.
- Existing code: `interview_expression/transcript.py`
- Missing: HTTP status endpoint, UI progress view

**FR-APP-023 — Shot map and keyframe indexing**
The system builds a visual index from the media: shot boundaries, transitions,
representative keyframes, without confusing visual change with semantic importance.
- Existing code: `interview_expression/visual.py`
- Missing: HTTP status endpoint

**FR-APP-024 — Expression Moment discovery and approval**
Hunters propose tags and Expression Moment candidates from the phrase transcript.
Analysts verify. The operator approves or rejects each candidate in the UI. Rejected
candidates are preserved as negative evidence.
- Existing code: `interview_expression/expression.py`
- Missing: HTTP endpoints for proposal list + approval action, React approval UI

### Module D — Activative Intelligence

**FR-APP-030 — Matrix of Edging and Edge Product formation**
Given an approved set of Expression Moments and the active Brand Context, the AIR
service computes the Matrix of Edging, surviving Primitive candidates, and the
Edge Product (the emergent tension object).
- Existing code: `cmf_activative_intelligence/services/primitive_service.py`,
  `coalition_service.py`
- Missing: HTTP trigger endpoint, React display of Edge Product

**FR-APP-031 — Activation Hypothesis Portfolio**
AIR generates a portfolio of meaningfully different Activation Hypotheses each with
a distinct psychological role inside the tension. Hard eligibility gates filter
disqualified candidates. The operator reviews and selects one.
- Existing code: `cmf_activative_intelligence/services/hypothesis_service.py`
- Missing: HTTP endpoint, React hypothesis comparison UI

**FR-APP-032 — Final Script compilation and approval**
Given a selected Planned Pack, JIT Writer and Composer compile a Guest Voice DNA
Final Script. Every segment preserves transformation class and source lineage.
The operator approves before composition begins.
- Existing code: `cmf_activative_intelligence/services/derivative_service.py`
- Missing: HTTP endpoint, React script review and approval UI

### Module E — Atomic Harness Library

**FR-APP-040 — Harness library browsing**
The operator can browse available AtomicHarnessDefinition packages in the workspace
library: category, format profile, version, capability requirements.
- Existing code: `cmf_builder` exports portable Harness ZIPs via CLI
- Missing: HTTP list endpoint, React Harness library page

**FR-APP-041 — Harness selection for campaign**
When creating a Campaign Order, the operator selects a Harness from the library.
The system validates that the Harness is compatible with the source package category.
- Existing code: `cmf_pipeline/bindings/eligibility_registry.py`
- Missing: HTTP validation endpoint, React selection UI in campaign creation flow

**FR-APP-042 — Harness creation via Pi Coding Agent**
The Pi Coding Agent can POST a Harness definition to the Builder API. The Builder
validates it against constitutional authority, builds the HarnessIR, and exports
a portable AtomicHarnessDefinition ZIP into the library.
- Existing code: `cmf_builder` CLI (`ingest`, `build`, `export` commands)
- Missing: HTTP POST endpoint wrapping the existing CLI commands

### Module F — Campaign Execution

**FR-APP-050 — Campaign Order creation**
The operator creates a Campaign Order by selecting: source package, Harness, output
targets (short video, Carousel, SuperVisual, animation), autonomy mode, budget,
deadline.
- Existing code: `cmf_pipeline/batch/service.py`, Studio `domain.ts` CampaignOrder type
- Missing: HTTP POST /campaigns endpoint, React CampaignNew page

**FR-APP-051 — Pipeline execution and progress reporting**
On Campaign Order creation, the Pipeline compiles execution bindings, schedules
workflow nodes, and begins executing. Status is reported in real time.
- Existing code: `cmf_pipeline/workflow/application/run_service.py`, `scheduler.py`
- Missing: WebSocket or SSE endpoint for live status, React RunGraph component

**FR-APP-052 — FFmpeg source-led video production**
The Pipeline produces a source-led short video where the original interview footage
is the A-roll spine. Word-boundary EDL cuts, captions, B-roll slots, and audio
fades are applied.
- Existing code: `cmf_pipeline/media/ffmpeg_adapter.py`, `edl.py`, `program.py`
- Status: FFmpeg execution is REAL and working. This needs API exposure only.

**FR-APP-053 — Carousel, SuperVisual, and Animation production**
The Pipeline renders Carousel slides, SuperVisual PNGs, and Animation Scene MP4s
from the approved Composition IR.
- Existing code: `cmf_pipeline/composition/` (skia_renderer, products, animation, pdf)
- Status: Reference rendering works. Needs real Skia-python for production quality.

**FR-APP-054 — VAE visual asset job execution**
When a job requires a generated visual asset, the Pipeline sends a demand across
Delegation to VAE. VAE plans the production, routes to provider, executes, evaluates,
and returns an Asset Result.
- Existing code: `cmf_vae/` full stack, `cmf_pipeline/delegation/service.py`
- Missing: ComfyUI worker must be wired to a real instance

### Module G — Studio Supervision

**FR-APP-060 — Control Tower**
The operator sees one unified view of the active campaign: source package, semantic
programs, Final Script, workflow node graph with statuses, artifacts, evaluations,
exception queue, and available actions.
- Existing code: Studio `controlTower.ts` ControlTowerProjection type, Python
  backend projections
- Missing: React ControlTower component, HTTP GET /campaigns/:id/tower endpoint

**FR-APP-061 — Timeline projection**
The operator sees a read-only timeline of the VideoEditProgram: A-roll source spans,
output-time positions, captions, overlays, motion slots.
- Existing code: Studio `timeline.ts` TimelineProjection type
- Missing: React Timeline component, HTTP GET /campaigns/:id/timeline endpoint

**FR-APP-062 — Natural language revision**
The operator types a revision request in plain language ("move the B-roll earlier",
"trim the intro by 3 seconds"). The Studio compiles it into a typed ChangeRequestProgram.
Unknown requests return NEEDS_CLARIFICATION.
- Existing code: Studio `revision.ts`, Python revision compiler in cmf_pipeline
- Missing: HTTP POST /campaigns/:id/revisions endpoint, React RevisionComposer component

**FR-APP-063 — Exception review and resolution**
Blocked jobs appear in an exception queue. The operator reviews, resolves, or
escalates. Resolution is recorded as a HumanResolutionEpisode.
- Existing code: Studio `resolutions.ts`, `cmf_pipeline` error handling
- Missing: HTTP GET /campaigns/:id/exceptions, React ExceptionQueue component

**FR-APP-064 — Ship gate**
The operator reviews final artifacts and requests shipment. The system evaluates
ship eligibility: campaign state, autonomy mode, artifact presence, evaluation
evidence, unresolved exceptions. Decision is recorded with full audit trail.
- Existing code: Studio `ship.ts` ShipDecision type, Python ship logic
- Missing: HTTP POST /campaigns/:id/ship endpoint, React ShipGate page

---

## PART 2 — EPICS (Value-Based, Not Technical Layer)

Following ERA3 Epic Design Doctrine: Epics deliver user value, not technical capability.

### Epic 1 — Establish the Coach's Creative Identity
**Value:** An operator can define the coach's brand DNA once and have it govern every
piece of content produced forever.
**FRs covered:** FR-APP-001, FR-APP-002, FR-APP-003
**Stories:** ST-APP-01.01, ST-APP-01.02, ST-APP-01.03
**Existing backend:** brand_service.py, AIR brand domain — needs API + UI
**Primitive context:** Identity DNA, Voice DNA, Visual DNA

### Epic 2 — Engineer and Conduct a Powerful Interview
**Value:** An operator can research a guest, engineer a psychologically loaded
interview Brief, conduct the session, and have the recording automatically indexed
as trusted production source material.
**FRs covered:** FR-APP-010, FR-APP-011, FR-APP-012, FR-APP-020, FR-APP-022,
FR-APP-023
**Stories:** ST-APP-02.01 through ST-APP-02.05
**Existing backend:** Interview Composer (internal), interview_expression package
**Note:** This is Entry Point A. Entry Point B (FR-APP-021) is covered in Epic 3.

### Epic 3 — Unlock Existing Interviews for Production
**Value:** An operator can upload any existing interview recording and transcript
and immediately access the full production pipeline without needing a retroactive
Brief.
**FRs covered:** FR-APP-021, FR-APP-022, FR-APP-023
**Stories:** ST-APP-03.01, ST-APP-03.02
**Existing backend:** interview_expression imported path — needs API + UI
**Note:** Equal peer to Epic 2. Same downstream from the Source Package onward.

### Epic 4 — Discover and Approve the Source Expression
**Value:** An operator can review what the interview actually contains — the charged
moments, the exact quotes, the expression candidates — and approve only the ones
that carry real activation force.
**FRs covered:** FR-APP-024
**Stories:** ST-APP-04.01, ST-APP-04.02
**Existing backend:** expression.py, reaction.py — needs API + approval UI
**Primitive context:** Hunters propose, operator approves, rejected = negative evidence

### Epic 5 — Build the Creative Recipe and Final Script
**Value:** An operator can see the psychological tension extracted from the interview,
review the Primitive Coalition that structures it, compare strategic hypotheses,
and approve one Guest Voice DNA Final Script before any production begins.
**FRs covered:** FR-APP-030, FR-APP-031, FR-APP-032
**Stories:** ST-APP-05.01 through ST-APP-05.04
**Existing backend:** primitive_service, coalition_service, hypothesis_service,
derivative_service — needs API + review UI
**Primitive context:** Matrix of Edging → Coalition → Archetype → Script

### Epic 6 — Manage the Harness Library
**Value:** An operator (or Pi Coding Agent) can create, browse, and select Atomic
Harnesses that encode production operating instructions for each content category.
**FRs covered:** FR-APP-040, FR-APP-041, FR-APP-042
**Stories:** ST-APP-06.01, ST-APP-06.02, ST-APP-06.03
**Existing backend:** cmf_builder full CLI — needs HTTP API wrapper
**Pi Coding Agent integration:** FR-APP-042 is specifically for the agent path

### Epic 7 — Launch and Monitor a Production Campaign
**Value:** An operator can fire off a full content batch and watch it run in real
time, with the original interview footage preserved as the video spine and all
derivatives traceable to approved source material.
**FRs covered:** FR-APP-050, FR-APP-051, FR-APP-052, FR-APP-053, FR-APP-054
**Stories:** ST-APP-07.01 through ST-APP-07.05
**Existing backend:** cmf_pipeline full stack — needs HTTP API + WebSocket + React RunGraph

### Epic 8 — Supervise, Correct, and Ship
**Value:** An operator can inspect every artifact in a unified Control Tower, request
precise corrections in plain language, resolve exceptions, and ship the batch with
a complete audit trail from interview to publication.
**FRs covered:** FR-APP-060 through FR-APP-064
**Stories:** ST-APP-08.01 through ST-APP-08.05
**Existing backend:** Studio TypeScript domain layer (complete), Python supervision
logic — needs HTTP API + React Control Tower UI

---

## PART 3 — STORIES (Selected Critical Path)

These are the stories that unlock everything else. An agent writing Tech Specs
must implement these first — each one must work end to end before the next begins.

### ST-APP-06.01 — Browse available Harnesses
As an operator, I want to see the Harness library so I know what production templates
are available before I create a campaign.
- **API:** GET /api/harnesses → list of AtomicHarnessDefinition summaries
- **Backend:** scan Harness library directory, parse each ZIP manifest
- **React:** HarnessLibrary.tsx — card grid with category, profile, version
- **Acceptance:** operator sees at least one Harness; clicking shows capability list

### ST-APP-07.01 — Create a Campaign Order
As an operator, I want to select a source package, choose a Harness, pick output
types, and launch a campaign so the Pipeline starts producing content.
- **API:** POST /api/campaigns { source_package_id, harness_id, output_targets,
  autonomy_mode }
- **Backend:** validates source + harness compatibility, creates CampaignOrder,
  triggers Pipeline workflow
- **React:** CampaignNew.tsx — two-step form: (1) select source, (2) select harness
  + outputs + autonomy
- **Acceptance:** Campaign appears in list with LAUNCHED status; Pipeline nodes visible

### ST-APP-07.02 — Watch Pipeline status in real time
As an operator, I want to see each Pipeline node's status update live so I know
what the system is doing and when it's blocked.
- **API:** WebSocket ws://api/campaigns/:id/status or GET /api/campaigns/:id/status
  (polling fallback)
- **Backend:** cmf_pipeline run_service emits status events; API streams them
- **React:** RunGraph.tsx — node graph using campaign workflow structure
- **Acceptance:** node transitions from PENDING → RUNNING → COMPLETE visible within
  2 seconds of state change

### ST-APP-08.01 — View Control Tower for a campaign
As an operator, I want one screen that shows me everything about an active campaign
so I never have to go to a command line.
- **API:** GET /api/campaigns/:id/tower → ControlTowerProjection JSON
- **Backend:** assemble projection from Pipeline + AIR + VAE state
- **React:** CampaignDetail.tsx with ControlTower.tsx, Timeline.tsx,
  ArtifactViewer.tsx, ExceptionQueue.tsx
- **Acceptance:** operator can see source package, Final Script, workflow nodes,
  artifacts, and exceptions from one page

### ST-APP-08.04 — Submit a natural language revision
As an operator, I want to type "trim the intro by 3 seconds" and have the system
compile and execute the correct operation without me touching a timeline editor.
- **API:** POST /api/campaigns/:id/revisions { request_text: string }
  → ChangeRequestProgram or NEEDS_CLARIFICATION
- **Backend:** Studio revision compiler in cmf_pipeline
- **React:** RevisionComposer.tsx — text input + confirmation display of compiled
  ChangeRequestProgram before execution
- **Acceptance:** request compiles to typed operations; NEEDS_CLARIFICATION returned
  for unknown requests; HumanResolutionEpisode created on execution

### ST-APP-03.01 — Upload an existing interview
As an operator with a legacy interview, I want to upload my video and transcript
and get the same downstream production capability as a Brief-led session.
- **API:** POST /api/interviews/import { video: File, transcript: File }
  → source_package_id
- **Backend:** `interview_expression` imported path
- **React:** CampaignNew.tsx import tab — file dropzone for video + transcript
- **Acceptance:** source package created with planning_lineage: ABSENT_NOT_CREATED;
  appears in campaign creation source selector

---

## PART 4 — TECH SPEC QUEUE

Following CA_SPEC_LIFECYCLE_CONTROLLER_SKILL.md, these specs must be written in
wave order. Each spec covers one bounded implementation unit. An agent works on
exactly one spec per execution.

### Wave 1 — Foundation API (no upstream spec dependencies)

**TS-APP-API-001 — FastAPI Gateway Bootstrap**
- FRs: all FR-APP-* (gateway entry point for all)
- Stories: all ST-APP-* (blocking dependency for all UI work)
- Scope: api/main.py, CORS, health endpoint, error contract, OpenAPI schema
- Existing code to wrap: all six Python packages
- Output: running FastAPI server, GET /api/health returns status from all services
- Build prerequisite for: every other API spec

**TS-APP-API-002 — Harness Library API**
- FRs: FR-APP-040, FR-APP-041, FR-APP-042
- Stories: ST-APP-06.01, ST-APP-06.02, ST-APP-06.03
- Scope: api/routers/harnesses.py
- Existing code: cmf_builder CLI commands → wrap as HTTP
- Output: GET /api/harnesses, GET /api/harnesses/:id, POST /api/harnesses/build
- Build prerequisite for: TS-APP-API-005 (campaign creation needs harness selection)

**TS-APP-API-003 — Interview Admission API**
- FRs: FR-APP-020, FR-APP-021, FR-APP-022, FR-APP-023
- Stories: ST-APP-02.01, ST-APP-03.01
- Scope: api/routers/interviews.py
- Existing code: interview_expression package — POST wraps source_package creation
- Output: POST /api/interviews/import, POST /api/interviews/brief-led,
  GET /api/interviews/:id/status

### Wave 2 — Campaign and Execution API (depends on Wave 1)

**TS-APP-API-004 — Campaign CRUD API**
- FRs: FR-APP-050
- Stories: ST-APP-07.01
- Scope: api/routers/campaigns.py
- Existing code: cmf_pipeline batch service
- Output: POST /api/campaigns, GET /api/campaigns, GET /api/campaigns/:id
- Depends on: TS-APP-API-001 (gateway), TS-APP-API-002 (harness), TS-APP-API-003 (interview)

**TS-APP-API-005 — Pipeline Status WebSocket**
- FRs: FR-APP-051
- Stories: ST-APP-07.02
- Scope: api/websockets/pipeline_status.py
- Existing code: cmf_pipeline run_service status events
- Output: ws://api/campaigns/:id/status — streams node state transitions
- Depends on: TS-APP-API-004

**TS-APP-API-006 — Control Tower and Supervision API**
- FRs: FR-APP-060, FR-APP-061, FR-APP-062, FR-APP-063, FR-APP-064
- Stories: ST-APP-08.01 through ST-APP-08.05
- Scope: api/routers/campaigns.py (supervision routes), api/routers/revisions.py,
  api/routers/ship.py
- Existing code: Studio Python backend projections, revision compiler
- Output: GET /tower, GET /timeline, POST /revisions, GET /exceptions,
  POST /ship endpoints
- Depends on: TS-APP-API-004, TS-APP-API-005

### Wave 3 — React Application (depends on Wave 1 + 2 APIs)

**TS-APP-UI-001 — React App Scaffold**
- FRs: all FR-APP-* (UI layer)
- Scope: apps/web/ — Vite + React + TypeScript + TanStack Router + TanStack Query
  + Tailwind
- Imports: existing services/studio/src/domain.ts types directly
- Output: running dev server, routing structure, API client, auth scaffold
- Build prerequisite for: all UI component specs

**TS-APP-UI-002 — Campaign List and Creation UI**
- FRs: FR-APP-050
- Stories: ST-APP-07.01, ST-APP-03.01
- Scope: apps/web/src/pages/CampaignList.tsx, CampaignNew.tsx
- Depends on: TS-APP-UI-001, TS-APP-API-003, TS-APP-API-004

**TS-APP-UI-003 — Control Tower UI**
- FRs: FR-APP-060, FR-APP-061, FR-APP-062, FR-APP-063
- Stories: ST-APP-08.01, ST-APP-07.02, ST-APP-08.04
- Scope: apps/web/src/pages/CampaignDetail.tsx, components/ControlTower.tsx,
  Timeline.tsx, RunGraph.tsx, RevisionComposer.tsx, ExceptionQueue.tsx
- Key: imports ControlTowerProjection, TimelineProjection from existing domain.ts
- Depends on: TS-APP-UI-001, TS-APP-API-005, TS-APP-API-006

**TS-APP-UI-004 — Harness Library UI**
- FRs: FR-APP-040, FR-APP-041
- Stories: ST-APP-06.01
- Scope: apps/web/src/pages/HarnessLibrary.tsx, components/HarnessCard.tsx
- Depends on: TS-APP-UI-001, TS-APP-API-002

### Wave 4 — Interview Composer Integration (depends on internal build)

**TS-APP-COMPOSER-001 — Interview Composer Service Integration**
- FRs: FR-APP-010, FR-APP-011, FR-APP-012
- Stories: ST-APP-02.01 through ST-APP-02.04
- Scope: services/interview-composer/ (integrate from internal build),
  api/routers/interviews.py (composer routes)
- Prerequisite: internal Interview Composer codebase must be provided
- Output: POST /api/interviews/compose/research, POST /api/interviews/compose/brief,
  React InterviewComposer.tsx page

---

## PART 5 — REPOSITORY RESTRUCTURE (DO FIRST, BEFORE ANY SPEC WORK)

An agent cannot write clean specs against messy paths. Do this mechanical work first.

### Step 1 — Rename directories (no code changes)
```bash
# Rename numbered service dirs to kebab-case
mv 01_ATOMIC_HARNESS_BUILDER services/builder
mv 02_VISUAL_ASSET_EDITOR services/vae
mv 03_DELEGATION_PROTOCOL services/delegation
mv 04_ACTIVATIVE_INTELLIGENCE_RUNTIME services/air
mv 05_ATOMIC_HARNESS_PIPELINE services/pipeline
mv 06_INTERVIEW_EXPRESSION services/interview
mv 07_CONSCIOUS_ACTIVATIONS_STUDIO services/studio

# Create new app directories
mkdir -p apps/web/src/{pages,components,hooks,api}
mkdir -p api/{routers,websockets}
mkdir -p infra/{docker,nginx}
mkdir -p docs/specs/{current,archive}

# Archive all phase bundle directories
mkdir -p archive/bundles
mv CONSCIOUS_ACTIVATIONS_PHASE_*_BUNDLE archive/bundles/
mv CONSCIOUS_ACTIVATIONS_PHASE_*_BUNDLE.zip archive/bundles/
mv CONSCIOUS_ACTIVATIONS_PHASE_01_03_TRACEABILITY_AND_GAP_CLOSURE_BUNDLE archive/bundles/

# Archive spec libraries
mkdir -p archive/specs archive/experiments
mv CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED archive/specs/prd-v1-2
mv CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3 archive/specs/workflow-v3-3
mv Specs_Builder_Library_CA_V2_1_3 archive/specs/spec-builder-library
mv CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE archive/specs/air-v2-1-bundle

# Archive noise
mv _PARALLEL archive/experiments/parallel
mv _PARALLEL_REPORTS archive/experiments/parallel-reports
mv "THE_CMF_STUDIO(2)" archive/experiments/cmf-studio-v2
mv 05_FUTURE_PRODUCTS archive/experiments/future-products
```

### Step 2 — Update pyproject.toml paths
Each service directory has a `pyproject.toml`. After the rename, the paths in
`tool.setuptools.packages.find` change from `01_ATOMIC_HARNESS_BUILDER/src` to
`services/builder/src`. Update all six.

### Step 3 — Verify tests still pass
```bash
pip install -e packages/ca_contracts -e packages/ca_runtime \
  -e services/builder -e services/air -e services/pipeline \
  -e services/interview -e services/vae --break-system-packages
python -m pytest tests/ -q
```
All 60 existing test files must pass before any new spec work begins.

### Step 4 — Create api/ and apps/web/ skeletons
```
api/
  __init__.py
  main.py          ← FastAPI app creation, CORS, router includes
  dependencies.py  ← shared FastAPI dependencies (DB session, auth)
  routers/
    __init__.py
    health.py      ← GET /api/health (WRITE THIS FIRST)

apps/web/
  package.json     ← React 18, Vite, TypeScript, TanStack Router/Query, Tailwind
  tsconfig.json
  vite.config.ts
  src/
    main.tsx
    App.tsx
    api/client.ts  ← base fetch wrapper
```

---

## PART 6 — SPEC WRITING INSTRUCTIONS FOR NEXT AGENT

When you (the next agent) pick up a Tech Spec from the queue in Part 4:

1. **Read first:** `archive/specs/spec-builder-library/Specs_Builder_Library/`
   - `Protocols_and_Skills/Conscious_Activations_V2_1/CA_SPEC_LIFECYCLE_CONTROLLER_SKILL.md`
   - `Protocols_and_Skills/Conscious_Activations_V2_1/CA_TECH_SPEC_WRITE_SKILL.md`
   - `Protocols_and_Skills/ERA3_Tech_Spec_Writing_Protocol.md`
   - `Examples/FR29_Context_Premise_Extraction_Tech_Spec.md` (example format)

2. **Read the existing code** for the module the spec covers — listed in Part 4
   under each spec. Do not invent what already exists.

3. **Write to:** `docs/specs/current/TS-APP-{module}-{number}.md`

4. **Each spec must include:**
   - Files read (with paths relative to repo root)
   - Problem + user outcome + solution scope
   - Governing FRs and Stories (from Part 1 and 3 above)
   - Existing code referenced (what already exists, what it does)
   - What this spec adds (HTTP routes, React components, new Python)
   - Data contracts (request/response schemas, TypeScript interfaces)
   - Acceptance criteria (BDD: Given/When/Then)
   - Test obligations
   - What is explicitly OUT OF SCOPE

5. **One spec per execution.** Do not batch.

6. **Start with TS-APP-API-001** (FastAPI gateway). Nothing else can be tested
   until the gateway exists.

---

## PART 7 — PRODUCTION READINESS GATES (for reference)

The application is production-ready when these gates pass:

| Gate | Description | Blocking spec |
|---|---|---|
| A | GET /api/health returns real status from all services | TS-APP-API-001 |
| B | A real .mp4 + transcript can be imported end to end | TS-APP-API-003 |
| C | A campaign runs and produces a real FFmpeg-cut MP4 | TS-APP-API-004 |
| D | Control Tower page shows live campaign status | TS-APP-UI-003 |
| E | A natural language revision compiles and executes | TS-APP-API-006 |
| F | Ship gate produces signed audit export | TS-APP-API-006 |
| G | ComfyUI wired to real instance, VAE job completes | TS-APP-API-004 |
| H | Pi Coding Agent can POST a new Harness via API | TS-APP-API-002 |

**Minimum viable product = Gates A through D.**

---
document_end: true
next_action: >
  Assign to an agent. Agent reads Part 6 instructions. Agent begins with
  repository restructure (Part 5). Then writes TS-APP-API-001. One spec
  per execution. Do not skip ahead.
