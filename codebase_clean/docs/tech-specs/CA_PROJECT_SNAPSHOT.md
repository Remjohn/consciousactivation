# Conscious Activations — Project Snapshot v2
**Date:** 2026-07-25
**Purpose:** Complete, accurate briefing for any model or developer picking up this project.
Read this entire document before writing a single line of code.

---

## 1. What This Product Is

Conscious Activations is **one product** — an AI-powered content production platform for coaches and personal brands. It takes a real human interview and turns it into a batch of production-ready content: short-form videos, Carousels, SuperVisuals, and animation scenes.

The central doctrine:

> **Content activates when it gives the viewer a psychological role inside a tension.**

Everything in the system exists to serve that doctrine. Every module, every data type, every workflow decision traces back to it.

---

## 2. The Complete Product Flow (End to End)

This is the canonical flow. Every module maps to a stage in this chain.

```
[WORKSPACE SETUP]
Brand Genesis Session
  → Coach personal branding DNA, Voice DNA, Visual DNA
  → Stored as Brand Context Version

[ENTRY POINT A — Engineered Interview]
Interview Composer
  → Research the guest (existing content, brand, positioning)
  → Pull Coach's Voice DNA + Brand Context
  → Engineer the Activative Interview Brief (questions, tension hypothesis, Matrix of Edging seed)
  → Conduct or schedule the interview session
  → Record + transcribe
  → Produce Canonical Interview Source Package

[ENTRY POINT B — Imported Interview]
Upload existing interview video + transcript
  → No fabricated Brief history
  → Same output: Canonical Interview Source Package

[BOTH PATHS CONVERGE HERE]
Canonical Interview Source Package
  → Word-aligned transcript, speaker segments
  → Shot map, keyframes
  → Proposed tags, Anchor Hits
  → Approved Expression Moments (Hunters propose, operator approves)
  → Asset Package Spec

[ACTIVATIVE INTELLIGENCE]
Matrix of Edging
  → Find the live psychological tension
  → Primitive Coalition Contract (the creative recipe)
  → Coalition Signature + Edge Product
  → Archetype Coalition (viewer's role inside the tension)
  → Activation Hypothesis Portfolio
  → Operator selects and approves one Planned Pack

[FINAL SCRIPT]
JIT Writer + Composer
  → Guest Voice DNA Final Script
  → Every word traceable to source or declared transformation
  → Operator approval gate
  → Reusable 2D Animation Scene Package compiled automatically

[PIPELINE EXECUTION]
Operator creates Campaign Order
  → Select Atomic Harness (the job template — see section 5)
  → Choose outputs: short video, Carousel, SuperVisual, animation
  → Set autonomy mode: Autopilot / Review Before Ship / Checkpointed / Shadow
  → Pipeline executes:
      - FFmpeg source-led video editing (A-roll = original interview footage)
      - Composition IR → SuperVisual / Carousel / Animation
      - VAE visual asset jobs (ComfyUI, SAM3, Lucida, GNM)
      - Skills + Steering Recipes retrieved from knowledge base
      - Programmed Models invoked where eligible

[STUDIO SUPERVISION]
Operator reviews in Control Tower
  → Timeline projection, artifact viewer, run graph
  → Exception queue for blocked jobs
  → Natural language revision ("move the B-roll earlier")
  → Direct manipulation (drag BBOX, trim source span)
  → Both compile to typed ChangeRequestProgram
  → Human Resolution Episodes recorded as programming material

[EVALUATION + REPAIR]
Deterministic checks + independent evaluation
  → Source Fidelity, Primitive Coalition, Archetype Fulfillment
  → Voice/Visual DNA, Negative Space, Edge Integrity
  → Bounded local repair (only the responsible layer reruns)

[SHIP]
Ship gate in Studio
  → Audit export: source → tension → recipe → script → render → evaluation
  → Publish decision
```

---

## 3. Module Map — One Product, Many Features

These are not separate products. They are **modules of one application** that communicate through well-defined contracts.

| Module | What it does | Python package | Status |
|---|---|---|---|
| **Interview Composer** | Research guest, engineer Brief, create interview session | Built internally (not in this repo yet) | Needs integration |
| **Interview Expression** | Ingest interview, align transcript, index shots, discover Expression Moments | `conscious_activations_interview_expression` | ✅ Built |
| **Activative Intelligence (AIR)** | Find tension, build Primitive Coalition, Archetype, Final Script | `cmf_activative_intelligence` | ✅ Built |
| **Atomic Harness Builder** | Define and govern Harness templates (Pi Coding Agent uses this) | `cmf_builder` | ✅ Built, CLI operational |
| **Pipeline** | Execute production jobs, schedule workflow, evaluate, repair | `cmf_pipeline` | ✅ Built |
| **Studio** | Operator supervision UI — Control Tower, revisions, ship | TypeScript domain (18 files), no React yet | ⚠️ Domain only, no UI |
| **Visual Asset Editor (VAE)** | Visual asset generation via ComfyUI, SAM3, Lucida, GNM | `cmf_vae` | ✅ Built (reference providers) |
| **Delegation** | Transport lifecycle contracts between modules | `ca_delegation_rc4` | ✅ Built (RC4 release) |
| **Brand Genesis / DNA** | Coach branding, Voice DNA, Visual DNA, Brand Context Version | Lives inside AIR + Builder | ✅ Built |

---

## 4. What Actually Exists in the Repo

### Live applied Python (in product directories, confirmed)

| Directory | Package | Files | Key capability |
|---|---|---|---|
| `services/builder/src/cmf_builder/` | cmf_builder | ~91 files | Harness IR, constitutional validation, category binding, Development Capsule, JIT capsules, export to portable AtomicHarnessDefinition ZIP |
| `services/air/src/cmf_activative_intelligence/` | cmf_activative_intelligence | ~34 files | Primitive registry (243 primitives), coalitions, archetypes, hypothesis portfolios, Final Scripts, campaign activation, Programmed Model evidence |
| `services/pipeline/src/cmf_pipeline/` | cmf_pipeline | ~76 files | Workflow execution, FFmpeg editing, Composition IR, SuperVisual/Carousel/Animation rendering, retrieval engine, skill registry, Delegation integration |
| `services/interview/src/` | conscious_activations_interview_expression | ~23 files | Source package lifecycle, transcript alignment, shot maps, Expression Moments, Reaction Receipts, live session state |
| `services/vae/src/cmf_vae/` | cmf_vae | ~18 files | Visual Production Plans, provider routing, ComfyUI graph compiler, SAM3/Lucida/GNM adapters, content-addressed storage, job queue |
| `services/delegation/` | ca_delegation_rc4 | RC4 release | Contract validation, transport lifecycle |
| `packages/ca_contracts/` | ca_contracts | 5 files | Shared schemas, canonical JSON serialization |
| `packages/ca_runtime/` | ca_runtime | 5 files | SQLite migrations, command/event/receipt persistence, idempotency |
| `packages/ca_release/` | ca_release | 7 files | SBOM, backup/restore, release guards, pilot orchestration |

### Live TypeScript (Studio domain layer)

`services/studio/src/` — 18 files, ~2,026 lines. Contains ALL the right domain types:
- `domain.ts` — AutonomyMode, CampaignLifecycleState, CampaignOrder, OutputTarget
- `campaign.ts` — CampaignState machine
- `controlTower.ts` — ControlTowerProjection
- `timeline.ts` — TimelineProjection, track structure
- `revision.ts` — ChangeRequestProgram, RevisionCompilationStatus
- `ship.ts` — ShipDecision, ShipRequest
- `store.ts` — State management foundation
- `resolutions.ts` — HumanResolutionEpisode
- `rerun.ts` — SelectiveRerunRequest
- `auditExport.ts` — AuditExportManifest

**These types are correct and complete. The React app is built on top of them — not redesigned.**

---

## 5. Atomic Harnesses — How They Work in the Ecosystem

This is critical to understand. An **Atomic Harness** is the operating template for a production job. It defines:
- Which content category (short video, Carousel, SuperVisual, animation)
- Which format profile
- Which capabilities are required
- Which phases of work must happen in sequence
- Which evaluation gates apply
- Which Skills and Steering Recipes are eligible

**The Builder (`cmf_builder`) is the tool that creates Harnesses.** The Pi Coding Agent uses the Builder's CLI to define and export Harnesses as portable `AtomicHarnessDefinition` ZIP packages.

**The Pipeline (`cmf_pipeline`) loads and executes Harnesses.** When an operator creates a Campaign Order and selects a Harness, the Pipeline:
1. Ingests the Harness ZIP via `intake/definition_intake.py`
2. Validates it against the constitutional authority
3. Compiles the execution bindings (`bindings/compiler.py`)
4. Schedules the workflow nodes (`workflow/application/scheduler.py`)
5. Executes each node using the right worker/provider

**In the app UI (Studio), Harnesses appear as selectable "job templates"** when creating a Campaign. The operator picks "Short Video Harness v2" or "Carousel Harness v1" and the Pipeline knows exactly how to execute it.

**Pi Coding Agent integration:** The Builder CLI (`cmf-builder ingest`, `cmf-builder build`, `cmf-builder export`) is already operational for development-level Harness creation. For production, the Pi Coding Agent sends commands to the Builder API (to be built) to define and export new Harnesses without human coding.

---

## 6. What Is Missing (The Real Gaps)

### Gap 1 — No HTTP API (MOST CRITICAL)
Every Python module has a CLI but zero HTTP endpoints. Nothing can talk to anything else over the network. No frontend can call the backend.

**Fix:** FastAPI gateway. ~3-5 days of focused work.

### Gap 2 — No React UI (MOST CRITICAL)
The Studio TypeScript domain types exist and are correct. There is no React component tree, no pages, no routing. The reference HTML Control Tower is a static demo, not a UI.

**Fix:** React app using Vite + TanStack Router + TanStack Query + Tailwind. ~1-2 weeks for MVP.

### Gap 3 — Interview Composer not integrated
The Interview Composer was built internally. It needs to be connected to this repo as the first step of the workspace flow — research the guest, pull Brand Context + Voice DNA, engineer the Brief, produce the session structure that flows into Interview Expression.

**Fix:** Add `services/interview-composer/` or integrate the existing internal build. Expose via API.

### Gap 4 — Real providers not wired
- FFmpeg: ✅ already real
- ComfyUI: graph compiler works, no real worker execution
- SAM3 / Lucida: adapters exist, point to fake commands
- Remotion / HyperFrames: binding manifests compiled, no execution
- Model inference: resolver exists, no actual inference calls

**Fix:** Wire ComfyUI first (easiest). Then SAM3. Remotion last.

### Gap 5 — No real interview pilot
All tests use synthetic fixtures. A real `.mp4` + transcript has never been ingested end to end.

**Fix:** After the API is running, run a real interview through it. This is Gate B.

---

## 7. Target Application Structure

```
conscious-activations/
  apps/
    web/                          ← React frontend (BUILD THIS)
      src/
        pages/
          WorkspaceSetup.tsx      ← Brand Genesis, Voice DNA, Visual DNA
          InterviewComposer.tsx   ← Research guest, engineer Brief, create session
          CampaignList.tsx        ← All campaigns in a workspace
          CampaignNew.tsx         ← Upload interview OR start from Brief
          CampaignDetail.tsx      ← Control Tower (main working view)
          HarnessLibrary.tsx      ← Browse and select Atomic Harnesses
        components/
          ControlTower.tsx        ← uses controlTower.ts types
          Timeline.tsx            ← uses timeline.ts types
          ArtifactViewer.tsx
          RunGraph.tsx
          RevisionComposer.tsx    ← natural language + direct manipulation
          ExceptionQueue.tsx
          HarnessCard.tsx
        hooks/
          useCampaign.ts
          useControlTower.ts      ← polls or WebSocket
          useRevision.ts
          useHarnesses.ts
        api/
          client.ts               ← typed against existing domain.ts types

  api/                            ← FastAPI gateway (BUILD THIS)
    main.py
    routers/
      workspaces.py               ← Brand Context, Voice DNA, Visual DNA
      interviews.py               ← admit source package (both entry points)
      campaigns.py                ← CRUD + state transitions
      harnesses.py                ← list available, select, load
      artifacts.py                ← download outputs
      revisions.py                ← ChangeRequestProgram submission
      ship.py                     ← ship decision
      pipeline_status.py          ← WebSocket for live updates

  services/                       ← renamed from numbered dirs, code unchanged
    builder/                      ← was 01_ATOMIC_HARNESS_BUILDER
    vae/                          ← was 02_VISUAL_ASSET_EDITOR
    delegation/                   ← was 03_DELEGATION_PROTOCOL
    air/                          ← was 04_ACTIVATIVE_INTELLIGENCE_RUNTIME
    pipeline/                     ← was 05_ATOMIC_HARNESS_PIPELINE
    interview/                    ← was 06_INTERVIEW_EXPRESSION
    studio/                       ← was 07_CONSCIOUS_ACTIVATIONS_STUDIO (TS domain only)
    interview-composer/           ← integrate from internal build

  packages/                       ← unchanged
    ca_contracts/
    ca_runtime/
    ca_delegation_rc4/
    ca_release/

  infra/
    docker/
      docker-compose.yml          ← long-running services, not one-shot CLI
      dockerfile.api
      dockerfile.web
      dockerfile.worker
    nginx/
      nginx.conf

  docs/
    specs/
      current/                    ← governing specs only
      archive/                    ← all historical specs
      spec-index.yaml             ← one file classifying all 60 specs

  archive/
    bundles/                      ← all PHASE_*_BUNDLE dirs moved here
    experiments/                  ← _PARALLEL, THE_CMF_STUDIO(2)
    specs/                        ← old spec library folders
```

---

## 8. Quickest Path to Production

Brutally honest priority order. Each step makes the next one possible.

### Week 1 — Make it runnable as one app

**Day 1-2: Restructure the repo**
Run this to rename directories (no code changes, just moves):
```bash
# rename services
mv 01_ATOMIC_HARNESS_BUILDER services/builder
mv 02_VISUAL_ASSET_EDITOR services/vae
mv 03_DELEGATION_PROTOCOL services/delegation
mv 04_ACTIVATIVE_INTELLIGENCE_RUNTIME services/air
mv 05_ATOMIC_HARNESS_PIPELINE services/pipeline
mv 06_INTERVIEW_EXPRESSION services/interview
mv 07_CONSCIOUS_ACTIVATIONS_STUDIO services/studio

# archive bundles
mkdir -p archive/bundles
mv CONSCIOUS_ACTIVATIONS_PHASE_*_BUNDLE archive/bundles/
mv CONSCIOUS_ACTIVATIONS_PHASE_*_BUNDLE.zip archive/bundles/

# archive old spec folders
mkdir -p archive/specs archive/experiments
mv CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED archive/specs/
mv CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3 archive/specs/
mv Specs_Builder_Library_CA_V2_1_3 archive/specs/
mv CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE archive/specs/
mv _PARALLEL archive/experiments/
mv "_PARALLEL_REPORTS" archive/experiments/
mv "THE_CMF_STUDIO(2)" archive/experiments/
mv 05_FUTURE_PRODUCTS archive/experiments/

# update pyproject.toml paths in each service (just change the path references)
```
Update each service's `pyproject.toml` to reflect the new path. Run tests to confirm nothing broke.

**Day 3-4: Build the FastAPI gateway**
```python
# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Conscious Activations", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
```

Start with just these routes to prove the plumbing works:
- `GET /api/health` — import each service package, call `.status()`, return JSON
- `POST /api/campaigns/demo` — run the existing Phase 9 demo flow, return artifact paths
- `GET /api/harnesses` — list available AtomicHarnessDefinition packages

Once those work: add campaign CRUD, interview admission, revision submission, ship.

**Day 5: Replace docker-compose**
```yaml
services:
  api:
    build: { context: ., dockerfile: infra/docker/dockerfile.api }
    ports: ["8000:8000"]
    command: uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
    volumes: [ca-state:/state, ca-media:/media]

  worker:
    build: { context: ., dockerfile: infra/docker/dockerfile.api }
    command: python -m cmf_pipeline worker --poll-interval 5
    volumes: [ca-state:/state, ca-media:/media]

  web:
    build: { context: ./apps/web }
    ports: ["3000:3000"]

volumes:
  ca-state: {}
  ca-media: {}
```

### Week 2 — Build the React MVP

**Priority pages (in order):**

1. `CampaignList` — show all campaigns with status badge
2. `CampaignNew` — two cards: "Start from Interview Brief" | "Upload Existing Interview"
3. `CampaignDetail` — the Control Tower. This is the main screen. Build it first as a polling status view (no WebSocket needed initially)
4. `WorkspaceSetup` — Brand Context, Voice DNA inputs (simple form)

**The React app imports the existing TypeScript types directly:**
```typescript
// apps/web/src/api/client.ts
import type { CampaignOrder, ControlTowerProjection, ChangeRequestProgram }
  from "../../services/studio/src/domain.js"

export async function getCampaign(id: string): Promise<CampaignState> {
  const res = await fetch(`/api/campaigns/${id}`)
  return res.json()
}
```

No type redesign. No new contracts. The domain is already modeled correctly.

### Week 3 — Wire the Interview Composer

Integrate the internally built Interview Composer. It should call into:
- Brand Context Version (from AIR) to pull the coach's DNA
- Interview Expression service to create the Activative Interview Brief
- Output: a structured session plan that becomes the Brief when the interview is admitted

### Week 4 — Wire one real provider + run a real interview

1. Point the ComfyUI adapter at a real local ComfyUI instance
2. Upload a real `.mp4` + transcript through the `/api/interviews` endpoint
3. Run it through the full Pipeline
4. Review output in the Studio UI

This is the moment the product becomes real.

---

## 9. How Atomic Harnesses Work Inside the App (For Pi Coding Agent)

```
Pi Coding Agent
  ↓ calls Builder API
  POST /api/harnesses/build
    { category: "short_video", profile: "talking_head_v2", ... }
  ↓
Builder service (cmf_builder)
  → validates against constitutional authority
  → builds HarnessIR
  → exports portable AtomicHarnessDefinition ZIP
  → stores in harness library
  ↓
Harness appears in UI
  HarnessLibrary.tsx shows it as selectable
  ↓
Operator selects it in CampaignNew
  POST /api/campaigns { harness_id: "talking_head_v2", ... }
  ↓
Pipeline service (cmf_pipeline)
  → ingests the Harness ZIP
  → compiles execution bindings
  → schedules workflow nodes
  → executes using available workers/providers
  → reports status back via WebSocket
```

The Harness is the OS for the job. The Pipeline is the machine that runs it. The Studio is the cockpit where the operator watches and steers.

---

## 10. What NOT to Do

- **Do not rewrite the Python backend.** All the business logic is working. Add HTTP on top.
- **Do not create more phase bundles.** That system served its purpose. Archive it.
- **Do not run the spec traceability pass.** The app needs to work first. Tests follow a working app.
- **Do not treat the Phase documents as the architecture.** They described build order, not product structure. The product structure is this document.
- **Do not use capital letters in new directory or file names.** Use `kebab-case` for directories, `snake_case` for Python files, `PascalCase` for React components, `camelCase` for TypeScript utilities.

---

## 11. One-Paragraph Summary

Conscious Activations is one AI-powered content production platform. It has a complete, tested Python backend (~865 lines of shared infrastructure, ~300+ files of business logic) covering interview ingestion, activative intelligence, pipeline execution, video/static/animation production, VAE visual asset generation, Studio supervision logic, and Delegation contracts. It also has an internally built Interview Composer (not yet in this repo) that engineers interview sessions from guest research and coach Brand DNA. What does not yet exist is the HTTP API layer connecting these Python modules to each other and to a frontend, and the React application that operators would actually use. The Interview Composer needs to be integrated. The path to production is: restructure directory names to lowercase, build the FastAPI gateway, scaffold the React app on top of the existing TypeScript domain types, wire ComfyUI as the first real provider, and run a real interview end to end. The Atomic Harness Builder is operational as a CLI and needs an HTTP API so the Pi Coding Agent can build new Harnesses programmatically — those Harnesses then appear as selectable templates in the Studio when operators create Campaign Orders.
