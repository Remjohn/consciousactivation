---
spec_id: TS-APP-UI-003
title: Control Tower UI
document_class: TECH_SPEC
product: Conscious Activations
module: web
quality_state: RECONCILED_PENDING_AUDIT
authority_state: CURRENT
build_authority: false
controlling_frs:
  - FR-APP-060 (Control Tower)
  - FR-APP-061 (Timeline projection)
  - FR-APP-062 (Natural language revision)
  - FR-APP-063 (Exception review and resolution)
controlling_stories:
  - ST-APP-08.01 (View Control Tower for a campaign)
  - ST-APP-07.02 (Watch Pipeline status in real time)
  - ST-APP-08.04 (Submit a natural language revision)
upstream_dependencies:
  - CA_PROJECT_SNAPSHOT_V2.md (authority — CURRENT)
  - CA_APP_FR_EPIC_SPEC_PLAN.md (authority — CURRENT)
  - TS-APP-UI-001.md — NOT YET WRITTEN. Per CA_APP_FR_EPIC_SPEC_PLAN.md Part 4, the React App
    Scaffold (Vite + TanStack Router + TanStack Query + Tailwind, `apps/web/src/api/client.ts`,
    routing, auth scaffold) is the stated "build prerequisite for all UI component specs." It has
    not been authored. This spec is being written out of Wave sequence at the user's explicit
    request — the same situation TS-APP-API-006 was in with respect to TS-APP-API-004, and this
    spec follows that precedent. Section 4 defines the minimal scaffold-shaped surface (route
    convention, fetch wrapper, query client, Tailwind entry point) this spec needs and marks it
    `ASSUMED_INTERFACE_PENDING_UI_001` — binding on TS-APP-UI-001's author, not a substitute for it.
  - TS-APP-UI-002.md — NOT YET WRITTEN. `CampaignList.tsx`/`CampaignNew.tsx` is where a
    `campaign_id` is first produced or selected. This spec assumes `CampaignDetail.tsx` is reached
    via a route param supplied by a link from that page and does not itself implement campaign
    creation, listing, or the source/harness selection flow.
  - TS-APP-API-005.md (quality_state: WRITTEN_PENDING_AUDIT — draft dependency) — this spec's
    `RunGraph.tsx` and its `usePipelineStatus` hook are direct, literal consumers of
    `ws://.../api/campaigns/{id}/status`, its REST polling fallback, and its close-code contract.
  - TS-APP-API-006.md (quality_state: WRITTEN_PENDING_AUDIT — draft dependency) — this spec's
    `ControlTower.tsx`, `Timeline.tsx`, `RevisionComposer.tsx`, and `ExceptionQueue.tsx` are direct,
    literal consumers of the tower/timeline/revision/exception endpoints and schemas it defines.
    This spec does **not** consume its `/ship` or `/audit-export` endpoints — see Section 2.
  - `services/studio/src/domain.ts`, `controlTower.ts`, `timeline.ts`, `revision.ts`, `surfaces.ts`,
    `generated/contracts.ts` (READ — CURRENT IMPLEMENTATION) — the authoritative TypeScript types
    this spec's data layer mirrors directly, per `CA_PROJECT_SNAPSHOT_V2.md` Section 8's stated
    pattern ("the React app imports the existing TypeScript types directly").
downstream_consumers:
  - Production readiness Gate D in CA_APP_FR_EPIC_SPEC_PLAN.md Part 7
    ("Control Tower page shows live campaign status") — this spec is Gate D's blocking spec.
  - A future Ship Gate UI spec (not in the current queue) — this spec leaves the
    `REQUEST_SHIP_DECISION` available-action as a visible, disabled stub; it does not build
    against `POST /api/campaigns/{id}/ship` or `GET /api/campaigns/{id}/audit-export`.
output_path: apps/web/src/pages/CampaignDetail.tsx (and supporting files listed in Section 8)
wave: 3
---

# TS-APP-UI-003 — Control Tower UI

## 1. Files and Authorities Read

| File | SHA-256 (first 8) | Status | Fact extracted |
|---|---|---|---|
| `CA_PROJECT_SNAPSHOT_V2.md` | `b568220d` | READ — CURRENT AUTHORITY | Section 7 names the exact target files this spec builds: `pages/CampaignDetail.tsx`, `components/ControlTower.tsx`, `Timeline.tsx`, `ArtifactViewer.tsx`, `RunGraph.tsx`, `RevisionComposer.tsx`, `ExceptionQueue.tsx`, `hooks/useCampaign.ts`, `useControlTower.ts`, `useRevision.ts`. Section 4 confirms Studio is "TypeScript domain, no React yet." |
| `CA_APP_FR_EPIC_SPEC_PLAN.md` | `8ea2646c` | READ — CURRENT AUTHORITY | Part 4 defines this spec's exact scope line, FR list, and story list; Part 7 lists this spec as Gate D's blocking spec |
| `services/studio/src/domain.ts` | `4fa1b8a5` | READ — CURRENT IMPLEMENTATION | Source of every projection/program type this spec's data layer imports: `ControlTowerProjection`, `TimelineProjection`, `RunNodeProjection`, `ExceptionReviewPackage`, `ChangeRequestProgram`, `OperatorRevisionRequest`, `CampaignLifecycleState`, `AutonomyMode` |
| `services/studio/src/controlTower.ts` | `1b46231f` | READ — CURRENT IMPLEMENTATION | `availableActions()` (lines 34–41) is the exact, exhaustive, sorted source of every string this spec's UI must be able to render an affordance for: `INSPECT_SOURCE`, `INSPECT_SEMANTIC_PROGRAM`, `EXPORT_AUDIT` always present; `OPEN_TIMELINE`/`REQUEST_REVISION`/`DIRECT_MANIPULATION` gated on `timeline != null`; `COMPARE_ARTIFACTS`/`REQUEST_REVISION` gated on `artifacts.length`; `RESOLVE_EXCEPTION` gated on `exception_packages.length`; `REQUEST_SHIP_DECISION` gated on `lifecycle_state === "READY_TO_SHIP"` |
| `services/studio/src/timeline.ts` | `2e64ba20` | READ — CURRENT IMPLEMENTATION | `projectVideoEditProgram` produces a `state: "READ_ONLY_CANONICAL_PROGRAM_PROJECTION"` literal — confirms the timeline this spec renders is read-only by construction, not by a UI-layer choice this spec is inventing |
| `services/studio/src/revision.ts` | `903449ed` | READ — CURRENT IMPLEMENTATION | `RevisionContext.target_layers_by_ref: Record<string,string>` maps a target's `object_id` to a target layer string; `DEFAULT_STUDIO_TOOLS` (lines 31–41) shows every tool's `allowed_target_layers` — `VIDEO_EDIT_PROGRAM` is the only target layer this spec's UI has a concrete, available ref for (`timeline.video_edit_program_ref`); `targetLayer()` throws `TARGET_REQUIRED` when `target_refs` is empty |
| `services/studio/src/surfaces.ts` | `1d9edb46` | READ — CURRENT IMPLEMENTATION | `STUDIO_MODULES` (lines 6–49) is a small, static, six-entry array giving each `StudioSurfaceId` a human `title`; `moduleById()` looks one up. Pure data, safe to import directly into the browser bundle |
| `services/studio/src/generated/contracts.ts` | `a38d316c` | READ — CURRENT IMPLEMENTATION | `ImmutableRef = {object_id, sha256, version}` is **not** the same shape as `ArtifactRef = {artifact_id, artifact_kind, bytes, media_type, sha256, uri}` — see Source gap notice 2 |
| `TS-APP-API-005.md` | `93d601aa` | READ — WRITTEN_PENDING_AUDIT (draft dependency) | Full WS message envelope (`snapshot`/`history`/`node_state_changed`/`run_state_changed`/`run_terminal`), REST fallback shapes, and close codes `4404`/`4409` — the exact contract `usePipelineStatus` implements against |
| `TS-APP-API-006.md` | `bfed8e44` | READ — WRITTEN_PENDING_AUDIT (draft dependency) | Full REST contract for tower/timeline/revisions/exceptions; its own Source gap notice 4 documents that `RunNodeProjectionModel.status` (8 values, Studio vocabulary) and `NodeStatus.state` on the WS/REST-status side of TS-APP-API-005 (9 values, raw Python `NodeState`) are **not the same enum** — see Source gap notice 1 below, which this spec must additionally resolve on the client |
| `TS-APP-API-001.md` | `7fe1b48f` | READ — WRITTEN_PENDING_AUDIT (draft dependency) | Confirms CORS is already enabled gateway-wide; this spec's fetch/WS clients need no CORS workaround |

### Source gap notices (read carefully — these govern this spec's design)

**Source gap notice 1 — the WebSocket layer and the tower layer speak different node-status vocabularies, and the WS payload cannot losslessly resolve the difference.** `TS-APP-API-006`'s `RunNodeProjectionModel.status` is `PENDING | READY | RUNNING | WAITING_HUMAN | SUCCEEDED | FAILED | CANCELLED | INVALIDATED` (8 values, Studio's node-kind-aware mapping). `TS-APP-API-005`'s `NodeStatus.state` is the raw Python `NodeState`: `BLOCKED | READY | DISPATCHED | RUNNING | SUCCEEDED | FAILED | CANCELLED | INVALIDATED | QUARANTINED` (9 values) and — critically — its schema carries no `node_type`/`NodeKind` field, so the client cannot tell a plain `READY` node from a `READY` `HUMAN_GATE` node the way `TS-APP-API-006`'s own server-side mapping table does. This spec does not attempt to re-derive `WAITING_HUMAN` on the client. Instead (Section 6) it defines two separate, explicitly-scoped mappings: a **coarse WS-driven visual class** (5 buckets: idle / active / done / failed / stopped) used only for `RunGraph.tsx`'s live pulse animation, and the **authoritative Studio status** (all 8 values, including `WAITING_HUMAN`) used for every label, badge, and available-action decision, sourced only from `GET .../tower`. The two are reconciled by invalidating the tower query on every `run_state_changed`/`run_terminal` WS message (Section 6) rather than by trying to make the WS stream itself authoritative for anything but "something changed, go refetch."

**Source gap notice 2 — `ArtifactRef` and `ImmutableRef` are different shapes, so a revision's `target_refs` cannot be built from a node's `artifact_refs`.** `OperatorRevisionRequest.target_refs: ImmutableRef[]` (`{object_id, sha256, version}`) per `domain.ts`. `RunNodeProjection.artifact_refs: ArtifactRef[]` (`{artifact_id, artifact_kind, bytes, media_type, sha256, uri}`) — a different object family entirely (rendered artifacts, not versioned program objects). The only `ImmutableRef`-shaped value this spec's data surface exposes that plausibly matches a `revision.ts`-recognized target layer (`VIDEO_EDIT_PROGRAM`, per `DEFAULT_STUDIO_TOOLS`) is `ControlTowerProjection.timeline.video_edit_program_ref`. Section 6 therefore scopes `RevisionComposer.tsx` to compiling revisions against exactly one target: the bound `video_edit_program_ref`. Any other target layer (`COMPOSITION`, `CAROUSEL_SEQUENCE`, `CANDIDATE_PORTFOLIO`, `AIR_REVISION_REQUEST`) has no `ImmutableRef` surfaced anywhere in `ControlTowerProjectionModel` today and is out of scope until a future spec surfaces one.

**Source gap notice 3 — `current_state_ref` on a revision request has no independently-confirmed source.** `NaturalLanguageRevisionInput.current_state_ref: RefModel` is a required field in `TS-APP-API-006`'s schema, but that spec's own workflow section (its Section 5, "Revision compile") does not show the client-supplied value being read or overridden server-side before the bridge call — it is forwarded as given. This spec sets `current_state_ref = timeline.video_edit_program_ref`, identical to `target_refs[0]`, as the only defensible choice available from data this UI actually holds (Source gap notice 2). This is flagged, not silently assumed, because a future audit of `TS-APP-API-006` may reveal `current_state_ref` was meant to reference something this spec does not have visibility into (e.g., a prior revision's resulting state rather than the program's own ref).

**Source gap notice 4 — TS-APP-UI-001 does not exist, so this spec states, rather than imports, its scaffold assumptions.** Section 4 lists the exact shape (`apps/web/src/api/client.ts` fetch wrapper signature, TanStack Router route-file convention, a `QueryClientProvider` at the app root, Tailwind configured with a `ca-` prefix-free custom token set) this spec's files are written against. If TS-APP-UI-001 lands with a materially different shape, the files in Section 8 need a mechanical adaptation pass, not a redesign — none of this spec's component logic depends on scaffold internals beyond "a fetch wrapper exists" and "a query client exists."

---

## 2. Problem, User Outcome, Solution, and Scope

### Problem without this spec
`TS-APP-API-005` and `TS-APP-API-006` expose a complete, typed HTTP and WebSocket surface for supervising a running campaign — but nothing renders it. The operator's only way to know what a campaign is doing is to `curl` an endpoint or read a database directly. There is no page where a human can look at one campaign and understand: what is it building, what has finished, what is stuck, and what can I do about it. `FR-APP-060` through `FR-APP-063` describe exactly this screen and are unimplemented on the frontend in every respect.

### User outcome
An operator opens `/campaigns/{campaignId}`, and within one page — no command line, no separate tool — sees: the source interview and Final Script this campaign is building from, every production node and whether it's blocked, running, done, or failed, the read-only edit timeline once one exists, a plain-English box to type a correction like "trim the intro by 3 seconds," and a queue of anything that needs a decision from them. Node states update within about a second of changing, without a page reload. If their revision request is ambiguous, the system says so instead of guessing. If a node fails, they see why and what they're allowed to do about it, not a stack trace.

### Solution
A `CampaignDetail.tsx` page built on five components — `ControlTower`, `RunGraph`, `Timeline`, `RevisionComposer`, `ExceptionQueue` — each thin over one of `TS-APP-API-005`/`006`'s endpoints, composed through a small set of typed hooks (`useControlTower`, `usePipelineStatus`, `useRevisionCompose`, `useExceptionResolve`) that own polling, WebSocket reconnection, and query invalidation so the five components never talk to `fetch`/`WebSocket` directly. A single client-side node-status normalization module (Source gap notice 1) is the one place either vocabulary is interpreted.

### In scope
- `apps/web/src/pages/CampaignDetail.tsx` — the route page, campaign header, tab strip, layout shell
- `apps/web/src/components/control-tower/ControlTower.tsx` — overview panel: source/script refs, knowledge, runtime health, available actions
- `apps/web/src/components/control-tower/RunGraph.tsx` — live node DAG, WS-driven
- `apps/web/src/components/control-tower/Timeline.tsx` — read-only track/item visualization
- `apps/web/src/components/control-tower/RevisionComposer.tsx` — natural-language revision compile + confirm + execute
- `apps/web/src/components/control-tower/ExceptionQueue.tsx` — exception list + resolve
- `apps/web/src/hooks/useControlTower.ts`, `usePipelineStatus.ts`, `useRevision.ts`, `useExceptions.ts`
- `apps/web/src/lib/nodeState.ts` — the Source gap notice 1 normalization module
- `apps/web/src/lib/actionRegistry.ts` — the `available_actions` → affordance mapping
- Design tokens: `apps/web/src/styles/tokens.css`, `apps/web/tailwind.config.ts` additions (Section 5)
- Component and hook tests (Section 11)

### Out of scope
- Ship gate UI (`POST /api/campaigns/{id}/ship`, `GET /api/campaigns/{id}/audit-export`) — `FR-APP-064` is not in this spec's controlling FR list (Part 4 of the plan scopes it to `FR-APP-060` through `063` only). `REQUEST_SHIP_DECISION` renders as a visible, disabled stub (Section 6).
- Direct manipulation editing (drag a bounding box, trim a segment by dragging a timeline edge). `Timeline.tsx` is read-only by construction (Source gap notice, `timeline.ts` fact above); `DIRECT_MANIPULATION` renders as a visible, disabled stub.
- Campaign creation, listing, source/harness selection — `TS-APP-UI-002`.
- `ArtifactViewer.tsx` as a rich media player/comparison tool — `artifacts` render as a linked, typed list inside `ControlTower.tsx` (uri + media_type + bytes) in this spec; a dedicated viewer with inline preview/compare is deferred.
- Authentication, multi-tenant workspace switching — not yet designed anywhere in the plan.
- Any change to `services/studio/`, `api/routers/`, or any Python package. This is a pure consumer of already-specified HTTP/WS contracts.

---

## 3. Governing Decisions and Constraints

**The tower projection is the single source of truth for labels; the WebSocket is only a "something changed" signal.** Per Source gap notice 1, no component renders a status string sourced directly from a WS message. `RunGraph.tsx` renders WS-derived coarse visual classes (pulse/idle/done/failed/stopped) as animation state only; every text label, badge, and count comes from the most recent `GET .../tower` response.

**`available_actions` drives affordances; the UI never hand-invents a button `controlTower.ts` didn't emit.** `actionRegistry.ts` (Section 6) is total over the nine known strings from `availableActions()`. An unrecognized action string (a future backend addition) renders as a disabled, labeled-with-its-raw-code chip and logs a `console.warn` — it is never silently dropped, matching the same "don't invent, don't drop" discipline `TS-APP-API-006` applies to its own Source gap notices.

**No component owns a raw `fetch` or `WebSocket` call.** All network access is behind the four hooks in Section 6. This is testable in isolation (Section 11) and keeps the Source gap notice 3 assumption (`current_state_ref`) in exactly one place (`useRevision.ts`) so a future correction touches one file.

**Query invalidation, not manual refetch calls, is how components stay in sync with each other.** Executing a revision, resolving an exception, or receiving a WS terminal message all call `queryClient.invalidateQueries({ queryKey: ['campaign', campaignId] })` — a single prefix invalidation that refreshes tower, timeline, and exceptions together. No component calls another component's refetch function directly.

**No `float` in any request body this spec constructs**, mirroring `ca_contracts`' convention already enforced server-side (`TS-APP-API-001` Section 3). `confidence_micros`, frame numbers, and byte counts are rendered client-side (e.g., `confidence_micros / 10000` → a percentage with one decimal) but never sent back to the server in a re-derived, lossy form — mutation payloads only ever echo values the server itself returned (e.g., `program_id`) or values the operator explicitly typed (the revision text).

**Claim ceiling: `SUPERVISION_UI_DEVELOPMENT_EVIDENCE`.** This spec does not claim production readiness, accessibility certification, or that every `RunNodeProjection.node_type` renders with a bespoke icon (Section 6 defines a small icon set with a generic fallback).

---

## 4. Current Brownfield Architecture

| Component | Path | Actual state | Disposition | Reason |
|---|---|---|---|---|
| `apps/web/` | — | Does not exist. `TS-APP-UI-001` (Section 1, Source gap notice 4) is the spec responsible for creating it | ASSUMED SCAFFOLD | This spec writes files as if the scaffold below already exists |
| `apps/web/src/api/http.ts` | **reconciled 2026-07-27** (was: ASSUMED — UI-001 not yet written) | Typed fetch wrapper `apiFetch<T>(path: string, init?: RequestInit): Promise<T>` throwing a typed `ApiError { error_code, message, service, timestamp }` on non-2xx, matching `TS-APP-API-001`'s `ErrorResponse` shape. **This spec's earlier `apiGet<T>`/`apiPost<T>` helper names have been replaced** — they were invented against an assumed scaffold and are withdrawn; `CampaignsApi` (§7) now calls `apiFetch` directly. UI-001 also owns `src/api/ws.ts` and `src/api/queryClient.ts`. | **RECONCILED** (Source Gap Notice 4 resolved) | Named in `CA_PROJECT_SNAPSHOT_V2.md` Section 7; verified by reading TS-APP-UI-001.md in full |
| TanStack Router route tree | **reconciled 2026-07-27** (was: ASSUMED — UI-001 not yet written) | File-based routes under `apps/web/src/routes/` generated by `@tanstack/router-plugin/vite`. `CampaignDetail.tsx` is reached via `routes/campaigns/$campaignId.tsx` (UI-001's own placeholder — this spec overwrites it). Route files use `createFileRoute("/path")({ component: ... })`, not an imperative `router.tsx` table. | **RECONCILED** (Source Gap Notice 4 resolved) | Named in `CA_PROJECT_SNAPSHOT_V2.md` Section 3; file path `apps/web/src/routes/campaigns/$campaignId.tsx` confirmed by reading TS-APP-UI-001.md |
| `QueryClientProvider` | assumed | Mounted once at the app root with `defaultOptions.queries.retry: false` in test, default elsewhere | ASSUMED_INTERFACE_PENDING_UI_001 | Standard TanStack Query setup; this spec's hooks assume a client is reachable via `useQueryClient()` |
| `services/studio/src/*.ts` (compiled to `dist/`) | confirmed, per Section 1 | Correct, complete, zero runtime dependencies (`package.json` fact from `TS-APP-API-006`'s file table: `"type": "module"`, no runtime deps) | REUSE — import types and the six pure functions/constants named in Section 1 directly from `services/studio/dist/` via a workspace path alias | `CA_PROJECT_SNAPSHOT_V2.md` Section 8: "No type redesign. No new contracts." |
| `TS-APP-API-005`/`006` routers | confirmed, per Section 1 | Fully specified, not yet implemented (both `quality_state: WRITTEN_PENDING_AUDIT`) | REUSE (as contract) | This spec's hooks are written against their documented shapes; if implementation diverges from spec, that is a defect in those specs' implementation, not this one |
| Reference HTML Control Tower | `CA_PROJECT_SNAPSHOT_V2.md` Section 6, Gap 2 | "a static demo, not a UI" | DO NOT REUSE | Explicitly called out as non-functional; this spec does not read or adapt it |

---

## 5. Design Direction

The brief includes a concrete visual identity reference (a dark, gold-accented operator console — "Fortress / CMF Studio Control Tower" — sharing this product's own working name for this exact screen) and a companion dark/gold marketing template. Both pin down a real direction rather than leaving one free, so per the frontend-design discipline this spec follows that direction exactly rather than defaulting to a generic dashboard look.

### Token system

**Color** (CSS custom properties, `apps/web/src/styles/tokens.css`):

| Token | Value | Use |
|---|---|---|
| `--ca-bg` | `#0B0B0D` | Page background |
| `--ca-surface` | `#16161B` | Card/panel background |
| `--ca-surface-raised` | `#1D1D24` | Hover/active card state |
| `--ca-border` | `rgba(255,255,255,0.08)` | Card and divider borders |
| `--ca-gold-300` | `#F8CE86` | Badge tint backgrounds, subtle highlight text |
| `--ca-gold-500` | `#F2A93C` | Primary accent — CTA fills, active tab, progress fill, focus ring |
| `--ca-gold-600` | `#D6912A` | Hover/pressed state on gold elements |
| `--ca-text-primary` | `#F5F5F7` | Headlines, primary values |
| `--ca-text-secondary` | `#9A9AA5` | Labels, captions, eyebrows |
| `--ca-text-tertiary` | `#6B6B74` | Disabled/inert text |
| `--ca-success` | `#34D399` | `SUCCEEDED` |
| `--ca-danger` | `#F0554C` | `FAILED`, exception badges |
| `--ca-waiting` | `#8B7CF6` | `WAITING_HUMAN` — the one deliberate departure from gold/gray/green/red. `WAITING_HUMAN` means "the system needs *you*, specifically," which is a different call to action than the gold CTA buttons the operator clicks constantly; reusing gold here would make every human gate visually indistinguishable from an ordinary button |
| `--ca-idle` | `#3A3A42` | `PENDING`, `CANCELLED`, `INVALIDATED` — desaturated, deliberately unremarkable |

**Type**: Display/headline — Space Grotesk, bold, used with restraint for the hero run-progress number and uppercase section eyebrows (tracked +0.04em). Body — Inter, regular/medium, for every label, description, and table cell. Utility/monospace — JetBrains Mono, for every `object_id`, `sha256`, and timestamp fragment this screen is full of; giving technical identifiers their own face keeps them from competing with the display type and signals "this is a copyable value, not prose."

**Layout**: A persistent left rail (240px) carries campaign identity — lifecycle-state badge, autonomy-mode badge, `studio_binding.primary_surface`'s human title via `moduleById()` — and the available-actions list, playing the role the Fortress reference gives its bottom tab bar, rotated for a desktop-first operator console rather than a mobile consumer app. The main column opens with the hero (below), then a tab strip (Overview / Run Graph / Timeline / Exceptions / Revise), each tab a card-sectioned panel matching the reference's card language: `rounded-2xl` (16px), 1px `--ca-border`, `--ca-surface` fill, an icon + uppercase eyebrow label as the card header.

**Signature**: The hero is a radial gauge — `SUCCEEDED` node count ÷ total node count as a circular progress ring with the percentage centered in Space Grotesk bold — directly continuing the reference's "Operator Readiness 94%" dial into this product's own most important number, "Run Progress." This is the one intentionally bold element; everything else on the page is quiet by comparison, per the restraint principle.

```
┌──────────────┬───────────────────────────────────────────────┐
│ campaign:8f2a │  ╭───────────╮   Run Progress                  │
│ ● RUNNING     │  │   62%     │   7 / 9 nodes succeeded         │
│ AUTOPILOT     │  ╰───────────╯   1 running · 1 blocked         │
│ Video Prod.   │                                                │
│ Studio        │  [Overview] [Run Graph] [Timeline] [Exceptions]│
│               │  [Revise]                                      │
│ ACTIONS       │  ┌───────────────────────────────────────────┐│
│ Inspect       │  │  (active tab panel — card-sectioned)       ││
│ source        │  │                                             ││
│ Export audit  │  └───────────────────────────────────────────┘│
│ Request       │                                                │
│ revision      │                                                │
└──────────────┴───────────────────────────────────────────────┘
```

---

## 6. Proposed Architecture and Workflows

### Component tree

```
CampaignDetail (route: /campaigns/$campaignId)
  useControlTower(campaignId)        ──> GET /api/campaigns/{id}/tower   (poll, 4s, disabled while WS is 'open')
  usePipelineStatus(campaignId, { onDirty: invalidateTower })
                                       ──> WS /api/campaigns/{id}/status  (+ REST fallback)
  ├── CampaignHeader                  (lifecycle badge, autonomy badge, primary_surface title)
  ├── RunProgressGauge                (hero — derived from tower.run_nodes)
  ├── ActionRail                      (available_actions → actionRegistry.ts)
  └── Tabs
      ├── ControlTower                (source/script/knowledge/runtime_health/artifacts)
      ├── RunGraph                    useControlTower (labels) + usePipelineStatus (pulse)
      ├── Timeline                    tower.timeline, refetched independently on tab activation
      ├── ExceptionQueue              tower.exception_packages + useExceptionResolve
      └── RevisionComposer            useControlTower (target/context) + useRevisionCompose/Execute
```

### Data flow and invalidation

1. `CampaignDetail` mounts `useControlTower(campaignId)`, which polls `GET /tower` every 4s by default.
2. `usePipelineStatus` opens the WS. On `node_state_changed`, it updates an in-memory `Map<node_id, CoarseNodeState>` used only by `RunGraph`'s pulse layer — no query invalidation on this message alone (too frequent; the tower poll will catch it within 4s, which satisfies "the operator sees it move within about a second" for the *pulse*, while the *label* catches up on the next poll tick or the next coarser event below).
3. On `run_state_changed` or `run_terminal`, `usePipelineStatus` calls `onDirty()`, which the page wires to `queryClient.invalidateQueries({ queryKey: ['campaign', campaignId] })` — this immediately refetches tower (and, if the Timeline tab is active, timeline), so exception counts, available actions, and node labels catch up right when something structurally significant happened, not just on the next poll tick.
4. While the WS `connectionState` is `'open'`, `useControlTower`'s poll interval is disabled (WS-driven invalidation is doing the job); on `'closed'`/`'errored'`, polling resumes as the sole freshness mechanism (ST-APP-07.02's "polling fallback" requirement, applied at the tower layer, not just the raw status layer `TS-APP-API-005` itself already falls back for).
5. `RevisionComposer`'s compile mutation does not invalidate anything (compiling doesn't change campaign state). Its execute mutation, and `ExceptionQueue`'s resolve mutation, both invalidate the same `['campaign', campaignId]` prefix on success.

### Node-state normalization (`lib/nodeState.ts`)

```ts
// Authoritative — sourced only from GET .../tower. Matches RunNodeProjectionModel.status exactly.
export type StudioNodeStatus =
  | "PENDING" | "READY" | "RUNNING" | "WAITING_HUMAN"
  | "SUCCEEDED" | "FAILED" | "CANCELLED" | "INVALIDATED";

// Coarse — sourced only from the WS stream (TS-APP-API-005's raw NodeState). Visual/pulse only.
export type CoarseNodeState = "idle" | "active" | "done" | "failed" | "stopped";

const WS_STATE_TO_COARSE: Record<string, CoarseNodeState> = {
  BLOCKED: "idle",
  READY: "active",
  DISPATCHED: "active",
  RUNNING: "active",
  SUCCEEDED: "done",
  FAILED: "failed",
  QUARANTINED: "failed",   // late/unconsumable result — same failed color family,
                            // distinct tooltip ("late result, not a content failure")
  CANCELLED: "stopped",
  INVALIDATED: "stopped",
};

export function coarseFromWsState(state: string): CoarseNodeState {
  return WS_STATE_TO_COARSE[state] ?? "idle"; // unknown future state: render inert, never crash
}

export const STUDIO_STATUS_TOKEN: Record<StudioNodeStatus, { color: string; label: string }> = {
  PENDING:       { color: "var(--ca-idle)",    label: "Pending" },
  READY:         { color: "var(--ca-gold-500)",label: "Ready" },
  RUNNING:       { color: "var(--ca-gold-500)",label: "Running" },
  WAITING_HUMAN: { color: "var(--ca-waiting)", label: "Needs you" },
  SUCCEEDED:     { color: "var(--ca-success)", label: "Succeeded" },
  FAILED:        { color: "var(--ca-danger)",  label: "Failed" },
  CANCELLED:     { color: "var(--ca-idle)",    label: "Cancelled" },
  INVALIDATED:   { color: "var(--ca-idle)",    label: "Invalidated" },
};
```

### Action registry (`lib/actionRegistry.ts`)

Total over the exact nine strings `controlTower.ts::availableActions()` can emit. `implemented: false` entries render as a visible, disabled chip with a "Coming soon" tooltip rather than being omitted — the operator should see the system knows this action exists, not wonder why a button vanished.

```ts
export type AvailableAction =
  | "INSPECT_SOURCE" | "INSPECT_SEMANTIC_PROGRAM" | "EXPORT_AUDIT"
  | "OPEN_TIMELINE" | "REQUEST_REVISION" | "DIRECT_MANIPULATION"
  | "COMPARE_ARTIFACTS" | "RESOLVE_EXCEPTION" | "REQUEST_SHIP_DECISION";

interface ActionEntry { label: string; icon: LucideIcon; implemented: boolean; onSelect?: (ctx: ActionContext) => void; }

export const ACTION_REGISTRY: Record<AvailableAction, ActionEntry> = {
  INSPECT_SOURCE:          { label: "Inspect source",       icon: FileSearch,  implemented: true,  onSelect: (ctx) => ctx.setTab("overview") },
  INSPECT_SEMANTIC_PROGRAM:{ label: "Inspect script",       icon: ScrollText,  implemented: true,  onSelect: (ctx) => ctx.setTab("overview") },
  EXPORT_AUDIT:            { label: "Export audit",         icon: Download,    implemented: false }, // needs SHIPPED — see Out of scope
  OPEN_TIMELINE:           { label: "Open timeline",        icon: Clapperboard,implemented: true,  onSelect: (ctx) => ctx.setTab("timeline") },
  REQUEST_REVISION:        { label: "Request revision",     icon: Wand2,       implemented: true,  onSelect: (ctx) => ctx.setTab("revise") },
  DIRECT_MANIPULATION:     { label: "Direct edit",          icon: MousePointerSquareDashed, implemented: false }, // Out of scope, Section 2
  COMPARE_ARTIFACTS:       { label: "Compare artifacts",    icon: Columns2,    implemented: true,  onSelect: (ctx) => ctx.setTab("overview") },
  RESOLVE_EXCEPTION:       { label: "Resolve exception",    icon: TriangleAlert, implemented: true, onSelect: (ctx) => ctx.setTab("exceptions") },
  REQUEST_SHIP_DECISION:   { label: "Request ship",         icon: Rocket,      implemented: false }, // Out of scope, Section 2
};

export function unknownActionEntry(code: string): ActionEntry {
  console.warn(`[control-tower] unrecognized available_action "${code}" — rendering as inert chip, not dropped`);
  return { label: code, icon: HelpCircle, implemented: false };
}
```

### Run graph layout

`RunGraph.tsx` lays out `tower.run_nodes` (which carry `dependency_ids`) as a layered DAG using longest-path-from-source layering — no new graph-layout dependency:

```ts
function layoutRunGraph(nodes: RunNodeProjection[]): Array<{ node_id: string; column: number }> {
  const byId = new Map(nodes.map((n) => [n.node_id, n]));
  const column = new Map<string, number>();
  function depth(id: string, seen: Set<string>): number {
    if (column.has(id)) return column.get(id)!;
    if (seen.has(id)) return 0; // cycle guard — should never occur, dependency graph is a DAG by construction
    seen.add(id);
    const deps = byId.get(id)?.dependency_ids ?? [];
    const d = deps.length ? Math.max(...deps.map((dep) => depth(dep, seen))) + 1 : 0;
    column.set(id, d);
    return d;
  }
  nodes.forEach((n) => depth(n.node_id, new Set()));
  return nodes.map((n) => ({ node_id: n.node_id, column: column.get(n.node_id)! }));
}
```
Bound: O(n·d) for n nodes of dependency-depth d. Fine for the harness-sized graphs (tens of nodes) this product produces; flagged here, not silently assumed, in case a future harness produces node counts where this needs revisiting.

### Revision workflow (`RevisionComposer.tsx`)

```
1. Operator types free text into a textarea.
2. Operator optionally multi-selects run nodes from a compact node-chip list
   (RunNodeProjection.node_id, filtered to status in {RUNNING, FAILED, SUCCEEDED, WAITING_HUMAN} —
   PENDING nodes have nothing yet to revise) → target_node_ids.
3. "Preview" button → useRevisionCompose.mutate({
       mode: "natural_language",
       target_refs: [tower.timeline.video_edit_program_ref],   // Source gap notice 2
       target_node_ids,
       category_id: tower.order.category_id,
       natural_language_request: text,
       current_state_ref: tower.timeline.video_edit_program_ref, // Source gap notice 3
     })
   Disabled with an inline "Open the Timeline tab first — no edit program exists yet for this
   campaign" message when tower.timeline === null.
4. Response renders regardless of compilation_status:
   - COMPILED: interpretation, exact_operations (tool_id + plain-language arguments),
     invalidated_downstream_nodes, confidence_micros as a percentage, preview_required badge,
     and a "Confirm & run" button.
   - NEEDS_CLARIFICATION: interpretation text (the system's best-effort read) plus escalation
     text, no Confirm button — an inline retry textarea instead.
   - DENIED: escalation text, no Confirm button, styled with --ca-danger.
5. "Confirm & run" → useRevisionExecute.mutate({ program_id }) → on 409 STALE_STATE_VERSION,
   toast "This campaign changed since you compiled that — recompiling" and auto-repeat step 3
   with the same text/targets against the now-current state.
```

---

## 7. Data Models, Contracts, Schemas, and APIs

### `apps/web/src/api/campaigns.ts` — typed endpoint bindings (reconciled to UI-001's `apiFetch`; Source Gap Notice 4 resolved 2026-07-27)

```ts
import { apiFetch } from "./http";
import type {
  ControlTowerProjection, TimelineProjection, ChangeRequestProgram,
  ExceptionReviewPackage, RevisionCompilationStatus,
} from "@studio/domain"; /*
  path alias into services/studio/src (not dist/).
  Reconciliation note: UI-001 exports the path alias "@ca/studio" → "services/studio/src"
  in tsconfig (confirmed 2026-07-27). UI-003 imports from "@studio/domain" in this shape —
  these two alias names resolve to the same tsconfig paths entry under one alias. The name
  "@studio/domain" is UI-003's choice; "@ca/studio" is UI-001's. Either works so long as
  tsconfig finalizes one canonical name. No source code change for UI-003 until alias is
  pinned by UI-001's author. */

export interface RefInput { object_id: string; sha256: string; version: string; }
export interface ActorInput {
  actor_id: string; actor_type: "human"; product_id: "conscious-activations-web";
  workflow_role: "operator";
}

export interface NaturalLanguageRevisionInput {
  mode: "natural_language";
  target_refs: RefInput[];
  target_node_ids: string[];
  category_id: string;
  natural_language_request: string;
  current_state_ref: RefInput;
}

export interface ExecuteRevisionResponse { campaign: unknown; rerun: unknown; episode: unknown; }
export interface ResolveExceptionResponse { campaign: unknown; episode: unknown; repair_plan: unknown | null; }

export const CampaignsApi = {
  getTower:  (id: string) => apiFetch<ControlTowerProjection>(`/api/campaigns/${id}/tower`),
  getTimeline: (id: string) => apiFetch<TimelineProjection>(`/api/campaigns/${id}/timeline`),
  getExceptions: (id: string) => apiFetch<ExceptionReviewPackage[]>(`/api/campaigns/${id}/exceptions`),
  compileRevision: (id: string, revision: NaturalLanguageRevisionInput, operator_actor: ActorInput) =>
    apiFetch<ChangeRequestProgram>(`/api/campaigns/${id}/revisions`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ revision, operator_actor }),
    }),
  executeRevision: (id: string, programId: string) =>
    apiFetch<ExecuteRevisionResponse>(`/api/campaigns/${id}/revisions/${programId}/execute`, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: "{}",
    }),
  resolveException: (id: string, packageId: string, decision: "REQUEST_REVISION" | "REJECT", operator_actor: ActorInput, notes?: string) =>
    apiFetch<ResolveExceptionResponse>(`/api/campaigns/${id}/exceptions/${packageId}/resolve`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ decision, operator_actor, notes }),
    }),
};
```

`ControlTowerProjection`/`TimelineProjection`/`ChangeRequestProgram`/`ExceptionReviewPackage` are imported, not redeclared — per the governing principle (Section 4) that this spec does not create a third copy of these shapes alongside `domain.ts` and `TS-APP-API-006`'s Pydantic models. Fields the Pydantic layer left as untyped `dict` (`campaign`, `order`, `studio_binding`, `knowledge`, `runtime_health` — `TS-APP-API-006` Section 6 passthrough note) are typed here against the TS domain shapes they actually are at runtime (`CampaignState`, `CampaignOrder`, `StudioSurfaceBinding`, `KnowledgeProjection`, `RuntimeHealthProjection[]`), since the browser receives real JSON matching those shapes even though the Python schema declined to assert it.

### `apps/web/src/hooks/useControlTower.ts`

```ts
export function useControlTower(campaignId: string) {
  const wsOpen = usePipelineStatusConnectionState(campaignId); // shared context, Section 6 data flow
  return useQuery({
    queryKey: ["campaign", campaignId, "tower"],
    queryFn: () => CampaignsApi.getTower(campaignId),
    refetchInterval: wsOpen === "open" ? false : 4000,
  });
}
```

### `apps/web/src/hooks/usePipelineStatus.ts`

```ts
export type ConnectionState = "connecting" | "open" | "closed" | "errored" | "no_run" | "multiple_runs";

export function usePipelineStatus(campaignId: string, opts: { onDirty: () => void }) {
  const [connectionState, setConnectionState] = useState<ConnectionState>("connecting");
  const [nodeVisual, setNodeVisual] = useState<Map<string, CoarseNodeState>>(new Map());

  useEffect(() => {
    let socket: WebSocket;
    let backoffMs = 1000;
    let stopped = false;

    function connect() {
      socket = new WebSocket(`${WS_BASE}/api/campaigns/${campaignId}/status`);
      socket.onopen = () => setConnectionState("open");
      socket.onmessage = (evt) => {
        const msg = JSON.parse(evt.data);
        switch (msg.type) {
          case "snapshot":
            setNodeVisual(new Map(msg.run.nodes.map((n: { node_id: string; state: string }) => [n.node_id, coarseFromWsState(n.state)])));
            break;
          case "node_state_changed":
            setNodeVisual((prev) => new Map(prev).set(msg.node.node_id, coarseFromWsState(msg.node.state)));
            break;
          case "run_state_changed":
            opts.onDirty();
            break;
          case "run_terminal":
            opts.onDirty();
            break;
        }
      };
      socket.onclose = (evt) => {
        if (stopped) return;
        if (evt.code === 4404) { setConnectionState("no_run"); return; }        // do not reconnect
        if (evt.code === 4409) { setConnectionState("multiple_runs"); return; } // do not reconnect
        setConnectionState("closed");
        backoffMs = Math.min(backoffMs * 2, 15000);
        setTimeout(connect, backoffMs);
      };
      socket.onerror = () => setConnectionState("errored");
    }
    connect();
    return () => { stopped = true; socket?.close(); };
  }, [campaignId]);

  return { connectionState, nodeVisual };
}
```

### `apps/web/src/hooks/useRevision.ts`

```ts
export function useRevisionCompose(campaignId: string) {
  return useMutation({
    mutationFn: (input: NaturalLanguageRevisionInput) =>
      CampaignsApi.compileRevision(campaignId, input, currentOperatorActor()),
  });
}

export function useRevisionExecute(campaignId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (programId: string) => CampaignsApi.executeRevision(campaignId, programId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["campaign", campaignId] }),
  });
}
```

### `apps/web/src/hooks/useExceptions.ts`

```ts
export function useExceptionResolve(campaignId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (args: { packageId: string; decision: "REQUEST_REVISION" | "REJECT"; notes?: string }) =>
      CampaignsApi.resolveException(campaignId, args.packageId, args.decision, currentOperatorActor(), args.notes),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["campaign", campaignId] }),
  });
}
```

### Component props (illustrative — exact prop lists finalized in Stage build, not re-litigated here)

```ts
interface ControlTowerProps { tower: ControlTowerProjection; }
interface RunGraphProps { runNodes: RunNodeProjection[]; nodeVisual: Map<string, CoarseNodeState>; connectionState: ConnectionState; }
interface TimelineProps { campaignId: string; boundTimeline: TimelineProjection | null; }
interface ExceptionQueueProps { campaignId: string; packages: ExceptionReviewPackage[]; }
interface RevisionComposerProps { campaignId: string; tower: ControlTowerProjection; }
```

---

## 8. Implementation Stages and Exact Target Paths

All paths relative to repository root, after the restructure in `CA_APP_FR_EPIC_SPEC_PLAN.md` Part 5.

### Stage 1 — Design tokens
- `apps/web/src/styles/tokens.css` — the Section 5 CSS custom properties, imported once at the app root (assumed to exist per `TS-APP-UI-001`).
- `apps/web/tailwind.config.ts` — extend `theme.colors` with the token names (`ca-bg`, `ca-surface`, `ca-gold-500`, etc.) referencing the CSS variables via `rgb(var(--ca-x) / <alpha-value>)` or direct `var()` passthrough, and register Space Grotesk / Inter / JetBrains Mono in `theme.fontFamily`.

### Stage 2 — Path alias to the Studio package
- Add `"@studio/*": ["../../services/studio/dist/*"]` to `apps/web/tsconfig.json` `compilerOptions.paths`, and the matching Vite `resolve.alias` entry in `apps/web/vite.config.ts`. `services/studio` must be built (`tsc`) before `apps/web` — document this as a one-line addition to the root build script, not a new CI stage.

### Stage 3 — Data layer
- `apps/web/src/lib/nodeState.ts` — Section 6, verbatim.
- `apps/web/src/lib/actionRegistry.ts` — Section 6, verbatim.
- `apps/web/src/api/campaigns.ts` — Section 7.
- `apps/web/src/hooks/useControlTower.ts`, `usePipelineStatus.ts`, `useRevision.ts`, `useExceptions.ts` — Section 6/7.

### Stage 4 — Components
- `apps/web/src/components/control-tower/CampaignHeader.tsx` — lifecycle badge (`STUDIO_STATUS_TOKEN`-style color mapping over `CampaignLifecycleState`, a small sibling table to `STUDIO_STATUS_TOKEN` covering the 8 lifecycle values), autonomy badge, `moduleById(tower.studio_binding.primary_surface).title`.
- `apps/web/src/components/control-tower/RunProgressGauge.tsx` — the hero (Section 5 signature), an SVG `<circle>` stroke-dashoffset ring computed from `succeeded / total` over `tower.run_nodes`.
- `apps/web/src/components/control-tower/ActionRail.tsx` — maps `tower.available_actions` through `ACTION_REGISTRY`/`unknownActionEntry`.
- `apps/web/src/components/control-tower/ControlTower.tsx` — overview panel: source_package_ref / final_script_ref / observed_activative_pack_ref / semantic_production_package_ref as a labeled ref list (`object_id` in monospace, click-to-copy `sha256`); `knowledge` counts; `runtime_health` as a small status grid (component_id, status dot using the same color tokens, budget_units_used/limit as a thin bar); `artifacts` as a typed list (media_type icon, bytes formatted, uri as a copy-link button — no inline preview, per Out of scope).
- `apps/web/src/components/control-tower/RunGraph.tsx` — `layoutRunGraph` (Section 6) + `nodeVisual` pulse + `STUDIO_STATUS_TOKEN` labels from `tower.run_nodes`; clicking a node opens a side panel with `blocker_codes`, `receipt_refs`, and `artifact_refs`.
- `apps/web/src/components/control-tower/Timeline.tsx` — track rows (`z_index` order, top = highest), items positioned via `start_frame`/`end_frame` scaled to a horizontal ruler in `duration_frames`/(`fps_numerator`/`fps_denominator`) seconds; item click shows a read-only detail panel including its `editable_operations` list, captioned "supported once direct editing ships" rather than acting on them.
- `apps/web/src/components/control-tower/ExceptionQueue.tsx` — one card per `ExceptionReviewPackage`: `summary`, `responsible_product`, `evidence_refs` as monospace ref chips, decision buttons rendered only for entries present in `allowed_decisions`.
- `apps/web/src/components/control-tower/RevisionComposer.tsx` — Section 6 workflow, verbatim.
- `apps/web/src/pages/CampaignDetail.tsx` — composes the above under the Section 5 layout, owns `activeTab` state passed to `ActionRail`'s `onSelect(ctx)`.

### Stage 5 — Wire the route
- `apps/web/src/pages/CampaignDetail.tsx` registered at route `/campaigns/$campaignId` (TanStack Router file-route convention — exact registration syntax depends on `TS-APP-UI-001`'s router setup, Section 4).

---

## 9. Failure, Empty, Loading, and Observability

| Situation | UI behavior |
|---|---|
| `GET /tower` 404 `CAMPAIGN_NOT_FOUND` | Full-page "This campaign doesn't exist or you don't have access to it" with a link back to the campaign list — no partial shell rendered |
| `GET /tower` loading (first fetch) | Skeleton cards matching the Section 5 card shapes — no spinner-only screen |
| WS `connectionState === "no_run"` (close 4404) | `RunGraph` shows "No production run is linked to this campaign yet" instead of an empty graph; does not retry |
| WS `connectionState === "multiple_runs"` (close 4409) | `RunGraph` shows "This campaign has more than one linked run — status can't be resolved automatically" with a link to the raw `GET /api/campaigns/{id}/status` JSON; does not retry |
| WS `connectionState === "closed"`/`"errored"`, reconnecting | A small, non-blocking inline indicator ("Reconnecting…") near the hero; polling fallback (Section 6) keeps data fresh in the meantime |
| `tower.timeline === null` | `Timeline` tab shows "Nothing has been compiled yet for this campaign" instead of an empty ruler; `RevisionComposer` disables its Preview button (Section 6, step 3) |
| `tower.exception_packages.length === 0` | `ExceptionQueue` shows "No open exceptions" rather than an empty list with no explanation |
| Revision compile `NEEDS_CLARIFICATION`/`DENIED` | Rendered as a normal 200 response per contract (Section 6) — never shown as an error toast, since it is not one |
| Revision execute `409 STALE_STATE_VERSION` | Auto-recompile flow (Section 6, step 5) — the operator is told what happened, not shown a raw error code |
| Any other 4xx/5xx from `api/client.ts` | Toast with `message` from the typed `ApiError`, plus the raw `error_code` in a collapsed "details" disclosure for support/debugging — never a blank failure |
| Component render throws | A route-level error boundary (assumed part of `TS-APP-UI-001`'s router scaffold) catches it; this spec does not add a second, redundant boundary inside `CampaignDetail` |

### Observability
- `console.warn` on every unrecognized `available_action` (Section 6) and every unrecognized WS `type` field, so a future backend addition is visible in the browser console during development rather than silently invisible.
- No client-side analytics/telemetry pipeline is specified here — out of scope until a product decision names one.

---

## 10. Acceptance Criteria

**AC-001 — Control Tower renders a running campaign's full projection**
Given a campaign with `lifecycle_state: "RUNNING"`, three `run_nodes` (two `SUCCEEDED`, one `RUNNING`), one artifact, and a bound `timeline`,
When the operator navigates to `/campaigns/{id}`,
Then the page shows the lifecycle badge "RUNNING", the run-progress gauge reading 67% (2/3), all three nodes in `RunGraph`, and the one artifact listed with its media type.
Failure example: gauge shows 0% or omits the running node.
Evidence: React Testing Library snapshot of rendered text content.
Test layer: component — `apps/web/src/components/control-tower/__tests__/ControlTower.test.tsx`.

**AC-002 — Available actions render exactly the affordances the projection allows, nothing invented**
Given `tower.available_actions = ["INSPECT_SOURCE", "EXPORT_AUDIT", "REQUEST_SHIP_DECISION"]`,
When `ActionRail` renders,
Then exactly three chips appear, "Request revision" and "Open timeline" are absent, and "Request ship" renders visibly but disabled.
Failure example: a fourth action appears, or "Request ship" is omitted instead of shown-disabled.
Evidence: DOM query for chip count and `disabled` attribute.
Test layer: component — `apps/web/src/components/control-tower/__tests__/ActionRail.test.tsx`.

**AC-003 — Unrecognized available action is never dropped**
Given `tower.available_actions` includes a string not in `ACTION_REGISTRY` (e.g. `"FUTURE_ACTION"`),
When `ActionRail` renders,
Then a chip labeled `"FUTURE_ACTION"` appears, disabled, and `console.warn` was called once with that string.
Failure example: the unknown action is silently filtered out.
Evidence: `vi.spyOn(console, "warn")` assertion + DOM query.
Test layer: component — same file as AC-002.

**AC-004 — Node label reflects Studio's authoritative status, not the WS's raw status**
Given a node with `tower.run_nodes[0].status === "WAITING_HUMAN"` and, simultaneously, a WS `node_state_changed` message for that node with raw `state: "READY"`,
When `RunGraph` renders,
Then the node's text label reads "Needs you" (from `STUDIO_STATUS_TOKEN.WAITING_HUMAN`), and only its pulse animation class reflects the WS's `"active"` coarse state.
Failure example: the label flips to "Ready" because the WS message overwrote it.
Evidence: DOM query for label text plus the node element's CSS class.
Test layer: component, with a mocked WS — `apps/web/src/components/control-tower/__tests__/RunGraph.test.tsx`.

**AC-005 — WS close code 4404 stops reconnection and shows the correct message**
Given the WS server closes the connection with code `4404` immediately after `onopen`,
When `usePipelineStatus` processes the close event,
Then `connectionState` becomes `"no_run"`, no further `WebSocket` construction occurs within 5 seconds, and `RunGraph` shows the "No production run is linked" message.
Failure example: the hook attempts to reconnect after a 4404.
Evidence: mock `WebSocket` constructor call count over time; DOM text assertion.
Test layer: hook — `apps/web/src/hooks/__tests__/usePipelineStatus.test.ts` (using `vitest-websocket-mock` or an equivalent in-process mock).

**AC-006 — Poll interval disables while the WS is open, resumes when it closes**
Given `usePipelineStatus` reports `connectionState: "open"`,
When `useControlTower` is evaluated,
Then `refetchInterval` is `false`; when `connectionState` transitions to `"closed"`, `refetchInterval` becomes `4000`.
Failure example: polling continues indefinitely alongside an open WS.
Evidence: inspect the `UseQueryOptions` passed to the mocked `useQuery`.
Test layer: hook — `apps/web/src/hooks/__tests__/useControlTower.test.ts`.

**AC-007 — `run_state_changed` triggers a tower refetch**
Given an open WS connection,
When a `run_state_changed` message arrives,
Then `queryClient.invalidateQueries` is called with `{ queryKey: ["campaign", campaignId] }` exactly once for that message.
Failure example: no invalidation occurs, or `node_state_changed` also triggers one (over-invalidation).
Evidence: spy on `invalidateQueries`.
Test layer: hook — same file as AC-006/AC-005 area, `usePipelineStatus.test.ts`.

**AC-008 — Revision compile renders all three compilation statuses correctly**
Given three separate compile responses with `compilation_status` of `COMPILED`, `NEEDS_CLARIFICATION`, and `DENIED` respectively,
When each is rendered in turn by `RevisionComposer`,
Then `COMPILED` shows a "Confirm & run" button and the operations list; `NEEDS_CLARIFICATION` shows a retry textarea and no confirm button; `DENIED` shows the escalation text in `--ca-danger` and no confirm button.
Failure example: a "Confirm & run" button appears for a `NEEDS_CLARIFICATION` response.
Evidence: DOM queries per rendered state.
Test layer: component — `apps/web/src/components/control-tower/__tests__/RevisionComposer.test.tsx`.

**AC-009 — Revision execute on stale state recompiles automatically**
Given `useRevisionExecute` receives a `409 STALE_STATE_VERSION` response,
When the mutation's error handler runs,
Then a toast reading "This campaign changed since you compiled that — recompiling" appears and `useRevisionCompose` is invoked again with the same `natural_language_request` and `target_node_ids`.
Failure example: the operator sees a raw 409 error with no recovery path.
Evidence: mock API sequence (409 then 200) + assertion that compile was called twice with identical text.
Test layer: component — same file as AC-008.

**AC-010 — Timeline disabled state when nothing is compiled yet**
Given `tower.timeline === null`,
When `RevisionComposer` renders,
Then the "Preview" button is disabled and the inline message "Open the Timeline tab first — no edit program exists yet for this campaign" is visible.
Failure example: the button is enabled and a compile request is sent with an undefined `target_refs[0]`.
Evidence: DOM query for `disabled` attribute and message text.
Test layer: component — same file as AC-008/AC-009.

**AC-011 — Exception resolve only offers allowed decisions**
Given an `ExceptionReviewPackage` with `allowed_decisions: ["REJECT"]` (not repairable by the Pipeline),
When `ExceptionQueue` renders that card,
Then only a "Reject" button appears — no "Request revision" button is rendered, not merely disabled.
Failure example: both buttons appear and "Request revision" is clickable.
Evidence: DOM query for button presence.
Test layer: component — `apps/web/src/components/control-tower/__tests__/ExceptionQueue.test.tsx`.

**AC-012 — Timeline renders tracks in z-index order with correctly scaled items**
Given a `TimelineProjection` with two tracks (`z_index: 0` and `z_index: 1`) and one item per track at known `start_frame`/`end_frame`, `fps_numerator: 30`, `fps_denominator: 1`,
When `Timeline` renders,
Then the `z_index: 1` track renders above the `z_index: 0` track in DOM order, and each item's rendered width is proportional to `(end_frame - start_frame) / duration_frames`.
Failure example: track order is reversed, or item width ignores `duration_frames` scaling.
Evidence: DOM order assertion + computed style width assertion (jsdom bounding-box mock or a snapshot of the inline `style` width percentage).
Test layer: component — `apps/web/src/components/control-tower/__tests__/Timeline.test.tsx`.

**AC-013 — Run progress gauge matches node counts exactly, including zero-node edge case**
Given `tower.run_nodes = []` (no run linked yet, tower still loads successfully),
When `RunProgressGauge` renders,
Then it shows "—" (not `NaN%`, not `0%`) with a caption "No production nodes yet."
Failure example: `NaN%` renders due to a `0/0` division.
Evidence: DOM text assertion.
Test layer: component — `apps/web/src/components/control-tower/__tests__/RunProgressGauge.test.tsx`.

---

## 11. Testing and Completion Evidence

### Test tooling
```bash
npm install -D vitest @testing-library/react @testing-library/user-event jsdom \
  msw vitest-websocket-mock --workspace apps/web
```
- **MSW** (Mock Service Worker) intercepts every `apiGet`/`apiPost` call at the network layer for component and hook tests — no component test mocks `campaigns.ts` directly, so the tests exercise the real fetch wrapper's error-parsing path too.
- **`vitest-websocket-mock`** (or an equivalent hand-rolled `WebSocket` mock behind a `global.WebSocket` override) drives the AC-004 through AC-007 scenarios deterministically, including simulated close codes.

### Test files to create
- `apps/web/src/lib/__tests__/nodeState.test.ts` — every `WS_STATE_TO_COARSE` entry, plus the unknown-state fallback (AC coverage: correctness of Section 6's table, feeding AC-004).
- `apps/web/src/lib/__tests__/actionRegistry.test.ts` — `unknownActionEntry` warns and returns an inert entry (AC-003).
- `apps/web/src/hooks/__tests__/usePipelineStatus.test.ts` — AC-005, AC-007, plus normal reconnect-with-backoff on an ordinary close (code not 4404/4409).
- `apps/web/src/hooks/__tests__/useControlTower.test.ts` — AC-006.
- `apps/web/src/components/control-tower/__tests__/ControlTower.test.tsx` — AC-001.
- `apps/web/src/components/control-tower/__tests__/ActionRail.test.tsx` — AC-002, AC-003.
- `apps/web/src/components/control-tower/__tests__/RunGraph.test.tsx` — AC-004, plus `layoutRunGraph` unit coverage (linear chain, diamond dependency, disconnected node).
- `apps/web/src/components/control-tower/__tests__/RevisionComposer.test.tsx` — AC-008, AC-009, AC-010.
- `apps/web/src/components/control-tower/__tests__/ExceptionQueue.test.tsx` — AC-011.
- `apps/web/src/components/control-tower/__tests__/Timeline.test.tsx` — AC-012.
- `apps/web/src/components/control-tower/__tests__/RunProgressGauge.test.tsx` — AC-013, plus the normal non-zero case from AC-001.

### Pre-existing regression
This spec adds a new workspace package (`apps/web`) rather than touching any existing Python or Studio TypeScript source. Run both suites before and after to confirm isolation:
```bash
python -m pytest tests/ -q --tb=short
npm test --workspace services/studio
```
Zero new failures in either is a hard gate.

### Build Receipt claim ceiling
`SUPERVISION_UI_DEVELOPMENT_EVIDENCE`

This spec does not claim:
- Ship gate functionality (`FR-APP-064`) — explicitly out of scope
- Direct-manipulation editing — explicitly out of scope
- Accessibility (WCAG) certification — component tests check semantics incidentally, not exhaustively
- Visual regression / pixel-perfect fidelity to the Section 5 reference — the token system and layout concept are specified; exact spacing is a build-time judgment call, not a tested contract
- Production readiness of `TS-APP-API-005`/`006` themselves — this spec tests its own code against their documented contracts, not their server-side implementations

---
spec_end: true
next_spec: TS-APP-UI-001 (React App Scaffold) — still required to resolve Source gap notice 4;
  alternatively TS-APP-UI-002 (Campaign List and Creation UI), since this spec's route assumes a
  campaign_id arrives from somewhere
prerequisite_for_next: none — this spec is self-contained against its stated ASSUMED_INTERFACE_
  PENDING_UI_001 scaffold surface and can be implemented as soon as TS-APP-UI-001 lands with a
  materially compatible shape
