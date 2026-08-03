# Conscious Activations — Master Sequencing Plan
**Companion to `docs/PRD/CURRENT.md` §1.14. Version 1.0, 2026-08-01.**

**What this file is for:** `CURRENT.md` is the canonical PRD — status, doctrine, gaps. This file is the operational layer on top of it: which agent works on what, in what order, and what to paste into a fresh agent session to start each workstream safely. Every brief below assumes the agent is starting cold in the `consciousactivation-main` repo with `docs/PRD/CURRENT.md` available, and ends with the same instruction: update `CURRENT.md`'s relevant section before finishing, per its own maintenance rule (§1.12).

---

## 1. The ordering principle, in one paragraph

Don't choose PRD-first or build-first globally — decide it *per item*. An item is safe to build now if nothing left to verify in the PRD could change its correct shape. Mechanical gaps already fully traced (a stale registry field, a missing UI filter, an un-built TypeScript output, a schema field that structurally doesn't exist yet) are safe now — more doctrine reading won't change what "fixed" looks like. Anything touching the missing agentic/learned execution layer (§1.3a) or the four doctrine-protecting AIR features (F17/F28/F29/F30) is **not** safe yet — building a stand-in for those before the doctrine work lands is how you get the "wrapper slop" outcome this whole PRD rewrite exists to prevent. That's the entire filter. Everything below is that filter applied to the current gap list.

---

## 2. Phase map

```
PHASE 0  (now, parallel)                    PHASE 1  (after 0-D lands)          PHASE 2                    PHASE 3
─────────────────────────                   ─────────────────────────          ─────────────              ────────
0-A  registry fix          ─┐                                                                              
0-B  workspace_id UI        │                                                                              
0-C  studio dist/ build    ─┼─ independent → 1-B  apps/web ⇄ studio wiring  ┐                              
0-D  PRD deep dives (~70    │   of each                                     │                              
     specs, F03/F13/F22,    │   other                                       ├─→  2-A  F17/F28/F29/F30  ┐   
     doc03 TS-CAS-AUT gap) ─┘                                                │        generation logic  │   
0-E  harness authoring     ─── pilot, then  ── (independent thread) ─────────┤                           ├─→ 3  first real
     (pilot harness first)     wait on 0-F/G                                 ├─→  2-B  VAE pixel path    │    Entry-Point-B
0-F  Blocker 5 + capability_                                                 │        wiring             │    campaign
     metadata decision      ── decision only ──→ 1-C  export schema + ──────┘                             │
0-G  GAP-007 posture             (fast)             campaigns.py wiring                                   │
     decision                                                                                              │
                                                     1-A  one real DSPy/agent-backed
                                                          reasoning module bound via
                                                          ProgrammedModelRegistry
                                                          (§1.3a — highest leverage)
```

Phase 0 items run concurrently — they touch disjoint files. Phase 1 needs Phase 0's decisions (0-F/0-G) and enough of 0-D to trust the execution-engine shape. Phase 2 needs Phase 1-A to exist (same missing layer, five places). Phase 3 only needs 1-C and one harness from 0-E — it does not need Phase 2, on the current (unconfirmed, §1.13#3) belief that conversational campaigns don't route through VAE.

---

## 3. Workstream table

| ID | Workstream | Depends on | Touches (files/services) | Output |
|---|---|---|---|---|
| 0-A | Fix `interview_expression` registry status | operator label decision (§1.10#4) | `governance/.../PRD_ALIGNMENT_REGISTRY.yaml` | code + `CURRENT.md` §1.3 update |
| 0-B | Wire `workspace_id` into `CampaignFilters.tsx` | none | `apps/web/src/components/campaign-list/CampaignFilters.tsx` | code + `CURRENT.md` §1.4 update |
| 0-C | Build `services/studio/dist/` | none | `services/studio/` build config | code + `CURRENT.md` §1.3a/§1.4 update |
| 0-D | Read remaining ~70 service tech-specs, F03/F13/F22, doc-03's `TS-CAS-AUT-*` gap | none | `services/*/docs/tech-specs/`, `archive/specs/prd-v1-2/` | `CURRENT.md` §1.4a rows resolved |
| 0-E | Author harness definitions from operator's reference zip | operator zip upload | `services/builder` CLI, `CA_HARNESS_LIBRARY_ROOT` | harness `.zip` packages + `CURRENT.md` §1.4/§1.7 update. **Use the companion Skill for this one.** |
| 0-F | Blocker 5 + capability_metadata decision | operator | decision only (§1.10#1) | `CURRENT.md` §1.10 resolved |
| 0-G | GAP-007 posture confirmation | operator | decision only (§1.10#2) | `CURRENT.md` §1.10 resolved |
| 1-A | One real agent/DSPy reasoning module via `ProgrammedModelRegistry` | 0-D (execution-engine doctrine settled) | `services/pipeline/.../programmed_model_engine.py`, new module | `CURRENT.md` §1.3a + new spec section |
| 1-B | `apps/web` consumes `services/studio` domain layer, retires duplicates in `CampaignHeader.tsx`/`RunGraph.tsx`/`nodeState.ts` | 0-C | `apps/web/src/components/control-tower/*`, `apps/web/src/lib/nodeState.ts`, `services/studio/src/*` | `CURRENT.md` §1.4 Studio + F19/F27 rows updated |
| 1-C | Extend `portable_export.py` with a workflow field (per 0-F decision), wire real `capability_metadata` + `workflow` in `campaigns.py`, fix the error handler to report `exc.field`/`exc.reason` instead of a hardcoded string | 0-F | `services/builder/.../portable_export.py`, `api/routers/campaigns.py`, `services/pipeline/.../harness_compiler.py` (if the field lives there instead) | `CURRENT.md` §1.7 gap ledger, both blocker rows closed |
| 2-A | F17/F28/F29/F30 real generation logic behind the existing `store_*`/`capture_*` services | 1-A | `services/air/services/{archetype,coalition,primitive,brand,learning}_service.py` + new reasoning module | `CURRENT.md` §1.4a rows F17/F28/F29/F30 |
| 2-B | VAE pixel path: wire `ComfyUIHttpAdapter`, add a real `/api/vae` route, activate `configure_visual_delegation()` | 1-A (or independently, if scoped as deterministic-only for v1) | `services/vae/src/cmf_vae/comfyui.py`, `api/main.py`, `services/pipeline/.../delegation/service.py` | `CURRENT.md` §1.4 VAE/Pipeline updated |
| 3 | First real Entry-Point-B campaign, end to end | 1-C, one harness from 0-E | integration only | `CURRENT.md` new "first campaign" record, feeds §1.13#3 confirmation |

---

## 4. Per-workstream agent briefs

Each block is meant to be pasted as the opening message of a fresh agent session (Claude Code or equivalent) working in a clean checkout of the repo. Swap in the operator's actual decisions where a brief says "per operator decision."

### 0-A — Registry status fix
```
Read docs/PRD/CURRENT.md §1.3 and §1.10#4. Fix the stale
`interview_expression: status: planned_next` entry in
governance/program-control/00_CONSTITUTION/current-v1.1/governance/PRD_ALIGNMENT_REGISTRY.yaml
to read `status: [operator's chosen label]`. Re-verify services/interview and
services/interview-composer are still mounted at /api/interviews and
/api/interviews/compose in api/main.py before committing. Update CURRENT.md
§1.3 and §1.10#4 to mark this resolved, per §1.12's maintenance rule.
```

### 0-B — workspace_id UI filter
```
Read docs/PRD/CURRENT.md §1.4 (App layer) and §1.6. workspace_id already
exists end-to-end in api/schemas/campaigns.py and apps/web/src/api/campaigns.ts.
Add a workspace filter to apps/web/src/components/campaign-list/CampaignFilters.tsx
alongside the existing CampaignLifecycleState filter. Confirm the one-workspace-
per-coach / stable-slug convention with the operator if not already settled
(§1.10#3) before finalizing the UI copy. Update CURRENT.md §1.4 and §1.6 when done.
```

### 0-C — Build services/studio
```
Read docs/PRD/CURRENT.md §1.3a (fourth finding) and §1.4 (Studio). 
api/services/studio_bridge.py spawns `node services/studio/dist/rpc.js`, which
does not exist because services/studio's TypeScript was never compiled. Run
the real build for services/studio, confirm services/studio/dist/rpc.js exists
and api/routers/revisions.py::compile_revision no longer raises StudioBridgeCrash
on a real call. Do not change compileNaturalLanguageRevision's regex-matcher
logic — that's real, working, and in scope for a later pass (F26 in §1.4a is
otherwise correct as "Built, Runtime-Broken"; this closes the "Runtime-Broken"
half). Update CURRENT.md §1.3a and the F26 row in §1.4a.
```

### 0-D — Remaining PRD deep-dives
```
Read docs/PRD/CURRENT.md in full, then §1.12's "not yet done" list and §1.14.
Continue Phase 2 of the original PRD rewrite: open the ~70 located-but-unread
docs/tech-specs/ folders under services/{builder,delegation,pipeline,studio,
vae,interview,air}/, plus archive/specs/{air-v2-1-bundle,spec-builder-library,
workflow-v3-3}. Resolve the "Not Independently Verified"/"Built, Thin" rows in
§1.4a — specifically F03 (role taxonomy), F13 (Remotion claim), F22 (Expression
Moment/keyframe depth). Also read
archive/specs/prd-v1-2/.../sources/STUDIO_ARCHITECTURE_AMENDMENT_V2_1/ for
whether TS-CAS-AUT-001..004 (named in doc 03, confirmed not to exist anywhere)
should be newly authored or descoped. Verify every claim against source before
writing it down — do not carry forward a spec's claim without checking the
code. Update CURRENT.md inline as you go, per §1.12, not in one batch at the end.
```

### 0-E — Harness authoring (use the companion Skill)
```
Read docs/PRD/CURRENT.md §1.14 and the companion Skill file
(HARNESS_GAP_ANALYSIS_AND_BUILD_SKILL.md). The operator has a reference zip of
harness source material. Follow the Skill exactly: do gap analysis first
(what harnesses/categories are needed vs. what's in CA_HARNESS_LIBRARY_ROOT,
currently empty), author ONE pilot harness first via the real Builder CLI
(cmf-builder ingest → build → export), verify it drops correctly into the
library and is visible via GET /api/harnesses, and stop there to report back
before authoring the rest of the batch — per the Skill's sequencing note,
mass-authoring before the Blocker 5 / capability_metadata decision (§1.10#1)
risks rework if workflow ends up needing to live inside the harness
definition itself. Update CURRENT.md §1.4 (Builder) and §1.7 with what
the library now contains.
```

### 0-F / 0-G — Decisions
```
These are not agent workstreams — they're operator decisions blocking 1-C.
See docs/PRD/CURRENT.md §1.10#1 and §1.10#2 for the exact questions and the
evidence behind each option. Recommend resolving both before Phase 1 starts,
since 1-C is small once decided and unblocks the first real campaign (Phase 3).
```

### 1-A — Execution-layer module
```
Read docs/PRD/CURRENT.md §1.3a in full — this is the highest-leverage single
fix in the document. Confirm 0-D has closed enough of the open threads
(the ~70 service specs, doc 03/06 already read) that the shape of this module
is settled, not still moving. Bind one real DSPy or agent-backed reasoning
module through the existing services/pipeline/.../programmed_model_engine.py::
ProgrammedModelRegistry (currently a real, empty registry). Do not build five
bespoke stand-ins per subsystem — this is meant to be the one shared layer
that F17/F28/F29/F30, VAE pixel generation, and Builder's uncertified Skill
all plug into. Update CURRENT.md §1.3a and add a new implementation-spec
subsection once real.
```

### 1-B — Studio de-duplication
```
Read docs/PRD/CURRENT.md §1.4 (Studio) and §1.4a (F19, F27). Confirm 0-C has
landed (services/studio/dist/ builds). apps/web/src/components/control-tower/
CampaignHeader.tsx and RunGraph.tsx, plus apps/web/src/lib/nodeState.ts,
independently reimplement Studio-domain concepts instead of importing
services/studio (CampaignHeader.tsx even has a function named
getStudioSurfaceTitle() with a comment admitting it's a stand-in). Replace
the duplicated logic with real imports from services/studio's domain layer.
Update CURRENT.md §1.4 and the F19/F27 rows in §1.4a.
```

### 1-C — Blocker 5 + capability_metadata implementation
```
Read docs/PRD/CURRENT.md §1.10#1 for the operator's decision and §1.1
(eighth pass) for the full trace. Extend
services/builder/src/cmf_builder/domain/portable_export.py's content schema
per the decision (either derive workflow from the Builder task object inside
Pipeline's harness_compiler.py, or add a new authored field to
PortableAtomicHarnessDefinition — whichever the operator chose). Separately,
wire real capability_metadata sourcing at api/routers/campaigns.py's
_try_compile_harness() call site instead of the hardcoded {}. While there,
fix the exception handler (~line 285) to report exc.field/exc.reason instead
of the hardcoded "Blocker 5" string, so future failures are accurately
labeled. Re-run tests/pipeline/test_harness_compiler.py (17/17 must still
pass) plus a real create_campaign() call against a 0-E-authored harness.
Update CURRENT.md §1.7 (both blocker rows) and §1.10#1.
```

### 2-A / 2-B — Generation-layer work
```
Do not start until 1-A is real and merged. Read docs/PRD/CURRENT.md §1.3a,
§1.4a (F17/F28/F29/F30 for 2-A; F15 for 2-B), and whatever new implementation-
spec section 1-A added. [2-A] Build the actual generation logic that
ArchetypeService/CoalitionService/PrimitiveService/BrandService/LearningService
are currently missing — every method on all five is store_*/capture_*
persistence only. [2-B] Wire services/vae/src/cmf_vae/comfyui.py::
ComfyUIHttpAdapter to a real ComfyUI endpoint, add a real /api/vae route to
api/main.py, and call PipelineApplication.configure_visual_delegation()
somewhere real in api/. Both should consume 1-A's execution engine rather
than hardcoding provider calls independently. Update CURRENT.md §1.4a rows
and §1.4 (AIR, VAE, Pipeline) as each lands.
```

### 3 — First real campaign
```
Read docs/PRD/CURRENT.md §1.5 (Entry Point B) and §1.13#3. Confirm 1-C is
merged and at least one harness exists from 0-E. Run one real
Entry-Point-B campaign end to end: upload video + transcript, select the
harness, create the campaign, confirm ingestion_status reaches
BRIDGE_SUCCEEDED (not BRIDGE_BLOCKED). Confirm or refute §1.13#3's
still-unverified claim that a conversational/Format02-category campaign
never touches VAE. Record the result — including anything that broke and
had to be patched live — in a new "first campaign" note in CURRENT.md,
per the maintenance rule.
```

---

## 5. What NOT to parallelize

- **Anything in Phase 2 against anything else in Phase 2 without 1-A landing first.** Building F17/F28/F29/F30's generation logic and VAE's pixel path independently, each inventing its own ad-hoc model-calling code, is exactly how this becomes five wrapper-slop implementations instead of one governed execution layer.
- **0-E's full harness batch against 0-F/0-G still open.** One pilot harness is fine (validates the CLI path); the rest should wait for the decision so they're not rebuilt.
- **Editing `docs/PRD/CURRENT.md` sections outside your own workstream.** If a finding in your workstream changes another section (it will, sometimes), append a note rather than rewriting the other workstream's section — let that workstream's own pass reconcile it, per §1.14's coordination rule.
