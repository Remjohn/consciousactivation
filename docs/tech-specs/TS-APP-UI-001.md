---
spec_id: TS-APP-UI-001
title: React App Scaffold
document_class: TECH_SPEC
product: Conscious Activations
module: web
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CURRENT
build_authority: false
controlling_frs:
  - all FR-APP-* (UI layer) — CA_APP_FR_EPIC_SPEC_PLAN.md Part 4 names this spec as
    "FRs: all FR-APP-* (UI layer)"; the scaffold is the shared shell every page-level
    FR is eventually rendered inside, not an owner of any single FR's behaviour
controlling_stories:
  - all ST-APP-* (every UI story in Part 3 needs a running app, a route to mount into,
    and an API client before its own Tech Spec can add real behaviour)
upstream_dependencies:
  - CA_PROJECT_SNAPSHOT_V2.md (authority — CURRENT)
  - CA_APP_FR_EPIC_SPEC_PLAN.md (authority — CURRENT)
  - TS-APP-API-001.md (quality_state: WRITTEN_PENDING_AUDIT — DRAFT_DEPENDENCY_NOT_ACCEPTED;
    this spec depends only on its documented CORS origins, `ErrorResponse` shape, and
    `GET /api/health` / `GET /api/health/{service}` response shape, not on any claim
    that the gateway is production-ready)
  - TS-APP-API-003.md (quality_state: WRITTEN_PENDING_AUDIT — DRAFT_DEPENDENCY_NOT_ACCEPTED;
    referenced only for its endpoint path list, to confirm the Vite dev proxy pattern
    generalises; no interview DTOs are consumed here — those belong to TS-APP-UI-002)
  - TS-APP-API-005.md (quality_state: WRITTEN_PENDING_AUDIT — DRAFT_DEPENDENCY_NOT_ACCEPTED;
    referenced only for its WebSocket URL pattern and message envelope shapes, to build
    a generic transport hook; no campaign-status rendering is built here — that belongs
    to TS-APP-UI-003)
  - services/studio/src/domain.ts and services/studio/src/generated/contracts.ts
    (existing code — CampaignOrder, ControlTowerProjection, ChangeRequestProgram, and
    the ImmutableRef/ArtifactRef/ActorRef/AuthorityRef base types this spec imports
    without modification)
downstream_consumers:
  - TS-APP-UI-002 (Campaign List and Creation UI — mounts into routes/campaigns/index.tsx
    and routes/campaigns/new.tsx placeholders created here)
  - TS-APP-UI-003 (Control Tower UI — mounts into routes/campaigns/$campaignId.tsx;
    consumes the WebSocket hook and query client built here)
  - TS-APP-UI-004 (Harness Library UI — mounts into routes/harnesses/index.tsx)
  - TS-APP-COMPOSER-001 (Interview Composer Service Integration — mounts into
    routes/interviews/compose.tsx once the internal Composer codebase is provided)
output_path: apps/web/ (and root-level workspace files listed in section 7)
wave: 3
---

# TS-APP-UI-001 — React App Scaffold

## 1. Files and Authorities Read

| File | SHA-256 (short) | Status | Fact extracted |
|---|---|---|---|
| `CA_PROJECT_SNAPSHOT_V2.md` | `b568220d` | READ — CURRENT AUTHORITY | Section 7 names the target `apps/web/src/` tree exactly (`pages/`, `components/`, `hooks/`, `api/`) and gives the literal import `from "../../services/studio/src/domain.js"` as the intended pattern — the React app imports Studio's TS source directly, it is not redesigned. Section 8 states the stack as "Vite + TanStack Router + TanStack Query + Tailwind." |
| `CA_APP_FR_EPIC_SPEC_PLAN.md` | `8ea2646c` | READ — CURRENT AUTHORITY | Part 4 defines this spec exactly: scope is `apps/web/` scaffold only, imports `services/studio/src/domain.ts` types directly, output is "running dev server, routing structure, API client, auth scaffold," and it is the "Build prerequisite for: all UI component specs." Part 5 Step 4 sketches a starter `apps/web/package.json`/`vite.config.ts`/`src/main.tsx`/`src/App.tsx` skeleton this spec supersedes with a complete one. |
| `TS-APP-API-001.md` | `7fe1b48f` | READ — DRAFT_DEPENDENCY_NOT_ACCEPTED | CORS policy is `allow_origins=["http://localhost:3000", "http://localhost:5173"]`, `allow_credentials=False`. Error contract shape is `{error_code, message, service, timestamp}`. `GET /api/health` returns `HealthResponse{status, timestamp, gateway_version, ca_data_root, services: dict[str, ServiceHealthItem]}` with 200 on `status: "ok"`, 503 on `"degraded"`. |
| `TS-APP-API-003.md` | `5d6471f6` | READ — DRAFT_DEPENDENCY_NOT_ACCEPTED | Confirms endpoint paths follow `/api/{resource}/{action}` under the same gateway; no new proxy pattern needed beyond what API-001 already establishes. Not otherwise consumed by this spec. |
| `TS-APP-API-005.md` | `93d601aa` | READ — DRAFT_DEPENDENCY_NOT_ACCEPTED | WebSocket paths are `ws://.../api/runs/{run_id}/status` and `ws://.../api/campaigns/{campaign_id}/status`. Message envelope `type` values: `snapshot`, `history`, `node_state_changed`, `run_state_changed`, `run_terminal`. Close codes `4404` (not found) and `4409` (ambiguous run). REST polling fallback exists at the same paths without the `ws://` scheme. |
| `services/studio/src/domain.ts` | `4fa1b8a5` | READ — CURRENT IMPLEMENTATION | 393 lines. Exports `CampaignOrder`, `ControlTowerProjection`, `ChangeRequestProgram`, `TimelineProjection`, `ShipDecision`, `HumanResolutionEpisode`, and 20+ related interfaces, all `readonly`-field, all importing base refs from `./generated/contracts.js` (note the `.js` specifier on a `.ts` source file — TypeScript ESM convention). |
| `services/studio/src/generated/contracts.ts` | `a38d316c` | READ — CURRENT IMPLEMENTATION | Defines `ActorRef`, `ArtifactRef`, `AuthorityRef`, `ImmutableRef` — the base types every Studio domain object composes. Header says "Generated ... Do not edit manually." |
| `services/studio/package.json` | `fcc83abe` | READ — CURRENT IMPLEMENTATION | `"name": "@conscious-activations/studio"`, `"private": true`, `"type": "module"`, no `"main"` or `"exports"` field, no dependency on React/Vite/anything. It is a bare TypeScript library compiled by `tsc`. |
| `services/studio/tsconfig.json` | `2288a69d` | READ — CURRENT IMPLEMENTATION | `target: ES2022`, `module: ES2022`, `moduleResolution: Bundler`, `strict: true`. This is the compiler mode apps/web's tsconfig must be compatible with. |
| `THE_CMF_STUDIO(2)/operator-web/package.json` | `b681cae7` | READ — REFERENCE, NOT REUSED | `react: 19.2.0`, `react-dom: 19.2.0`, `vite: 6.4.2`, `@vitejs/plugin-react: 5.0.4`. No router, no query library, no CSS framework. |
| `THE_CMF_STUDIO(2)/operator-web/src/App.jsx` | `72c4be95` | READ — REFERENCE, NOT REUSED | 1,210 lines, one file, no routing (single component tree), imports static fixture data from `data.js` (454 lines), zero `fetch` calls. This is the "reference HTML Control Tower" the Project Snapshot calls "a static demo, not a UI." |
| `THE_CMF_STUDIO(2)/operator-web/src/styles.css` | `a8156e6b` | READ — REFERENCE, NOT REUSED | 1,869 lines of hand-written CSS, no design-token layer, no Tailwind. |
| `image-gen-1_10_.png`, `image-gen-1_4_.png` (branding reference, user-supplied) | — | READ — DIRECT PIXEL SAMPLE | Quantized colour histogram of both screenshots (method in Section 3) confirms a near-black background (`#000000`–`#101010`), a bright amber accent (`#F0A800`/`#F8B000`), a more muted amber used specifically on filled buttons (`#D8A830`), a positive-delta green (`#10C058`), and an alert red (`#E02828`). Not a formal design system — see Section 3 caveat. |

**Source gap notice:** the branding reference is two dashboard screenshots and one podcast promo graphic for a *different, unnamed consumer app* ("Fortress"), not a Conscious Activations style guide. No Figma file, font license, or exact token sheet exists. Section 3 treats the sampled palette as a provisional starting point, not an accepted brand authority. This does not block writing.

---

## 2. Problem, User Outcome, Solution, and Scope

### Problem without this spec
`services/studio/src/` has correct, complete TypeScript domain types and zero UI. The Project Snapshot's own reference demo (`operator-web/`) proves what happens without a real scaffold: a single 1,210-line component with no router, no data layer, and static fixture data standing in for a backend that now exists. Every Wave 3 UI spec (`TS-APP-UI-002` through `TS-APP-UI-004`) needs somewhere to put a page, a way to call the gateway from `TS-APP-API-001`, and a way to consume the WebSocket from `TS-APP-API-005`. None of that exists yet.

### User outcome
A developer runs one command from the repository root and gets a live dev server on `http://localhost:5173` showing an application shell — sidebar, top bar with a live gateway health indicator, six routable (empty) pages matching the Project Snapshot's target page list. `services/studio/src/domain.ts` types resolve with no `tsc` errors from inside `apps/web`. Every subsequent UI spec starts by filling in one route file instead of inventing project structure.

### Solution
An `apps/web/` Vite + React + TypeScript application, added to an npm workspace at the repository root, using TanStack Router for typed file-based routing, TanStack Query plus a small typed `fetch`/`WebSocket` layer for data access, and Tailwind CSS v4 for styling against a provisional dark/amber design-token set. The only real network call wired end-to-end in this spec is `GET /api/health`, because it is the only route `TS-APP-API-001` defines — it exists here to prove the client, the dev proxy, and the CORS contract all actually work together, not as a feature.

### In scope
- Root workspace: `package.json` (npm workspaces), `.nvmrc`, `.gitignore` additions
- `apps/web/` project: `package.json`, `tsconfig.json` (+ `tsconfig.node.json`), `vite.config.ts`, `index.html`, `.env.example`, `.env.development`
- Design tokens: `src/styles/index.css` (Tailwind v4 `@theme`, provisional palette from Section 3)
- Routing: `src/routes/__root.tsx`, `src/routes/index.tsx`, and one placeholder route per Project Snapshot page (`WorkspaceSetup`, `InterviewComposer`, `CampaignList`, `CampaignNew`, `CampaignDetail`, `HarnessLibrary`)
- Data layer: `src/api/http.ts` (typed `fetch` wrapper + `ApiError`), `src/api/types.ts` (Health/Error DTOs mirroring `TS-APP-API-001`, WebSocket envelope union mirroring `TS-APP-API-005`, re-export of `services/studio/src` domain types), `src/api/queryClient.ts`, `src/api/ws.ts` (generic reusable WebSocket hook)
- One live example: `src/hooks/useHealth.ts` + a status pill in the top bar, consuming the one real endpoint
- Dev-only auth scaffold: `src/auth/DevOperatorContext.tsx`, `src/hooks/useOperator.ts` — a hardcoded `ActorRef`-shaped operator identity, explicitly not real authentication
- Shell + primitives: `src/components/layout/{AppShell,Sidebar,TopBar}.tsx`, `src/components/ui/{Card,Badge,StatusPill,Button}.tsx`
- Tooling: ESLint flat config, Vitest + Testing Library config, one smoke script
- `infra/docker/dockerfile.web`, and the `web` service block in `infra/docker/docker-compose.yml`

### Out of scope
- Any page's real behaviour beyond a labeled placeholder (campaign list rendering, harness cards, control tower, revision composer — all later UI specs)
- Any endpoint beyond `GET /api/health` (every other DTO and hook belongs to the spec that owns that route)
- Real authentication/authorisation (the dev operator context is a stand-in; a real auth spec comes after MVP routes work, matching `TS-APP-API-001`'s own out-of-scope note)
- A finished visual design system (Section 3's palette is provisional — see the caveat)
- Any modification to `services/studio/src/**` or any Python service package
- Production `nginx.conf` routing rules for `/api` and `/ws` (owned by the infra spec that finalises `infra/nginx/nginx.conf`; this spec's Dockerfile only builds static assets for that proxy to serve)

---

## 3. Governing Decisions and Constraints

**The domain types are consumed by source import, not as an installed package.** `services/studio/package.json` has no `"main"` or `"exports"` field, so `import ... from "@conscious-activations/studio"` will not resolve. Adding an exports map to a package owned by a different Wave is out of scope for a UI scaffold spec. Instead, `apps/web/tsconfig.json` defines a path alias `"@ca/studio/*": ["../../services/studio/src/*"]` that resolves to the literal relative import the Project Snapshot already shows (`../../services/studio/src/domain.js`) — the alias is ergonomic sugar over that exact path, not a redefinition of it. Direct relative imports also work without the alias.

**Vite must be told to serve outside `apps/web/`.** Vite's dev server refuses by default to serve files outside the project root (`server.fs.strict`). Because `services/studio/src` sits two directories above `apps/web`, `vite.config.ts` sets `server.fs.allow` to the repository root explicitly. Without this, the domain-type imports resolve at `tsc` time but 404 at dev-server runtime.

**`moduleResolution` must be `"bundler"`, matching `services/studio`'s `"Bundler"`.** `domain.ts` imports its own sibling files with a `.js` specifier (`from "./generated/contracts.js"`) even though the file on disk is `contracts.ts` — correct modern TS-ESM style, but it only type-checks under `"moduleResolution": "bundler"` (or `"nodenext"`). Vite's official React+TS template has defaulted to `"bundler"` since Vite 5, so this is not a special-case for apps/web; it is stated here because it is load-bearing for the cross-package import to type-check at all.

**Framework versions are pinned to what is current now, not to what `operator-web` used.** `operator-web` pinned `vite@6.4.2`; as of this spec's writing date Vite's supported line is `8.1.x` (regular patches), with `7.3.x` and `6.4.x` receiving security-fix backports only. Starting a new, permanent scaffold on a soon-to-be-legacy major would be a bad trade for the one-time cost of adopting the current major now. This spec pins Vite 8 and the React plugin that pairs with it (`@vitejs/plugin-react` v6, which drops the Babel dependency in favour of Oxc for Fast Refresh — no config-surface change for this spec, since neither the React Compiler nor custom Babel transforms are in scope). `react`/`react-dom` at `19.2.0` are reused from `operator-web` because that major is still current, not because it was already there.

**Exact versions are pinned in the lockfile; do not drift on `^` ranges.** All framework-critical packages (`react`, `vite`, `@vitejs/plugin-react`, `tailwindcss`, `@tailwindcss/vite`, `@tanstack/react-router`, `@tanstack/router-plugin`, `@tanstack/react-router-devtools`, `@tanstack/react-query`, `@tanstack/react-query-devtools`) are pinned to an exact version in `package.json`, not a caret range, and `package-lock.json` is committed. This is standard practice for a scaffold meant to be reproduced by CI and by every downstream spec's author, and it costs nothing here; it becomes cheap insurance given that npm's registry has had at least one documented supply-chain compromise event in this ecosystem in the months before this spec was written. Bumping a pinned version is a one-line PR, not a silent `npm install`.

**Design tokens are provisional, derived by direct pixel sampling — not an accepted brand authority.** Two dashboard screenshots and one promo graphic for a *different* consumer app ("Fortress") were supplied as "one example of our branding identity." No Conscious Activations style guide, font license, or exact token sheet exists yet. Rather than eyeballing the screenshots, this spec ran a quantized colour-histogram over both dashboard images and picked the mechanically most-frequent non-background hues:
```
background        #000000   (dominant background pixel, both images)
surface            #0D0D0F   (interpolated — cards render visually indistinct from
                              background at this resolution; a slightly lifted value
                              is used so bordered panels are legible, not sampled)
foreground         #F8F8F8   (sampled — primary text/numerals)
muted-foreground   #9A9AA0   (estimated — no clean isolated sample of secondary-label
                              gray was recoverable at this resolution)
accent             #F0A800   (sampled — ring highlights, active nav state, headline
                              numerals; matches an exact histogram-top pixel value)
accent-solid       #D8A830   (sampled — filled CTA button background; a visibly
                              distinct, more muted gold from `accent`, sampled off
                              the "OPEN WORK QUEUE" button)
accent-foreground  #0A0700   (near-black text placed on `accent-solid` fills)
success            #10C058   (sampled — weekly-activity checkmarks / positive deltas)
danger             #E02828   (sampled — alert/notification-dot red)
info               #1070F0   (sampled — a blue UI accent present in the dashboard;
                              exact role unconfirmed, kept as an available token)
```
The per-module icon colours visible in the "Practice Stack" cards (a violet and a teal) were not recoverable as clean isolated samples at the supplied resolution and are **not** promoted to tokens here. This palette gives the mechanism (CSS variables consumed by every component in Section 7) a real, evidenced starting point. It is explicitly not a finished design system; if a formal CA brand authority is produced later, only `src/styles/index.css`'s `@theme` block needs to change, not any component.

**The dev-mode API base URL is same-origin, proxied — not cross-origin `fetch`.** `vite.config.ts` proxies `/api` and `/ws` to `http://localhost:8000` (the `TS-APP-API-001` gateway's default bind). The browser never makes a cross-origin request in dev, so `TS-APP-API-001`'s CORS allowlist (`localhost:3000`, `localhost:5173`) is a defense-in-depth backstop, not something apps/web relies on. This also means production (behind `infra/nginx/nginx.conf`, which is expected to proxy `/api` and `/ws` to the api container the same way) needs no separate client configuration — `src/api/http.ts` always calls a relative `/api/...` path.

**The auth scaffold is a stand-in, not a feature.** `TS-APP-API-001` explicitly defers authentication. There is nothing for a login page to call. `src/auth/DevOperatorContext.tsx` supplies a single hardcoded `ActorRef` (`workflow_role: "operator"`) so every component that will eventually need "who is the operator" has one call site (`useOperator()`) to update later, instead of every future spec inventing its own placeholder. It renders a visible `DEV MODE — NOT AUTHENTICATED` badge in the top bar so it cannot be mistaken for a real session.

**Claim ceiling:** `UI_SCAFFOLD_DEVELOPMENT_EVIDENCE`. This spec does not claim any page's business logic is complete, that the design system is final, or that authentication exists.

---

## 4. Current Brownfield Architecture

| Component | Path | Actual behaviour | Disposition | Reason |
|---|---|---|---|---|
| `operator-web/` (whole directory) | `THE_CMF_STUDIO(2)/operator-web/` | Vite 6 + React 19 static demo; one 1,210-line `App.jsx`; fixture data from `data.js`; no router, no query library, no API calls | ARCHIVE, NOT PORTED | Per `CA_PROJECT_SNAPSHOT_V2.md` Section 7, `THE_CMF_STUDIO(2)` moves to `archive/experiments/cmf-studio-v2/` in the Part 5 restructure. Its component tree is not reused; it is read here only as a UX inventory of what a Control Tower screen has previously tried to show (informs `TS-APP-UI-003`, not this spec) |
| `operator-web/src/styles.css` | same | 1,869 lines of hand CSS, no token layer | REPLACE | Superseded by Tailwind v4 `@theme` tokens (Section 3) |
| `operator-web/package.json` version pins | same | `vite@6.4.2`, `@vitejs/plugin-react@5.0.4`, no router/query/css-framework deps | REPLACE | Vite 6.4.x is now security-patch-only upstream; new scaffold pins current majors (Section 3) |
| `services/studio/src/*.ts` (18 files) | `services/studio/src/` | Complete, correct domain types; compiled by bare `tsc`; no consumer today | REUSE, UNMODIFIED | Imported by relative/aliased path from `apps/web`; zero edits per "no type redesign" doctrine in the Project Snapshot |
| `services/studio/package.json` | `services/studio/package.json` | No `exports` field, not installable as a bare specifier | REUSE, UNMODIFIED | Adding an exports map is a Studio-package decision, out of this spec's scope (see Section 3) |
| `CA_APP_FR_EPIC_SPEC_PLAN.md` Part 5 Step 4 skeleton | plan document, not code | Sketches a minimal `apps/web/package.json`/`vite.config.ts`/`main.tsx`/`App.tsx` as a "create the skeleton" step | SUPERSEDE | This spec is the full, buildable version of that sketch — it exists as a stage-4 planning note, not as shipped code, so there is nothing to migrate away from |
| `infra/docker/docker-compose.yml` `web` service (sketched, not yet written) | Project Snapshot Section 8, "Day 5" | Sketch only: `build: { context: ./apps/web }` | IMPLEMENT | This spec writes the real `infra/docker/dockerfile.web` the sketch assumed exists |

---

## 5. Proposed Architecture and Workflows

### Workspace and package boundary

```
conscious-activations/                 (npm workspace root)
  package.json                         workspaces: ["apps/web"]
  apps/web/                            this spec's package — builds independently
    package.json
  services/studio/                     unmodified — a sibling source tree, not a
                                        workspace dependency of apps/web
```

`services/studio` is deliberately **not** added as an npm-installed dependency of `apps/web`. It is read as source through the filesystem (Governing Decision, Section 3). This keeps the dependency direction honest: `apps/web` reads Studio's types; it does not "depend on a package" that Studio's own `package.json` doesn't actually publish.

### Request flow (the one wired example)

```
Browser
  useHealth() hook (TanStack Query)
    → src/api/http.ts::apiFetch("/api/health")
      → same-origin GET /api/health
        → [dev] Vite proxy → http://localhost:8000/api/health   (TS-APP-API-001)
        → [prod] nginx  → api container :8000/api/health          (future infra spec)
      ← HealthResponse | ErrorResponse (503) | network failure
  ← TopBar renders a StatusPill: green "operational" / amber "degraded" / red "unreachable"
```

Three outcomes are handled, not just the happy path: **200 `status: "ok"`**, **503 `status: "degraded"`** (a typed `HealthResponse` the gateway itself returns per its own AC-004), and **the fetch throwing** (gateway not running at all, e.g. before `TS-APP-API-001` is deployed locally) — the third case is the one a scaffold spec must not skip, since apps/web is expected to run and be reviewable *before* the gateway is guaranteed to be up.

### Routing tree

TanStack Router, file-based, generated by `@tanstack/router-plugin/vite` into a git-ignored `src/routeTree.gen.ts`:

```
src/routes/
  __root.tsx              AppShell (Sidebar + TopBar) + <Outlet/> + NotFoundComponent
                           + a root ErrorBoundary
  index.tsx                redirects to /campaigns
  workspace/
    index.tsx              placeholder for FR-APP-001..003 (WorkspaceSetup)
  interviews/
    compose.tsx             placeholder for FR-APP-010..012 (InterviewComposer)
  campaigns/
    index.tsx                placeholder for FR-APP-050 list view (CampaignList)
    new.tsx                   placeholder for FR-APP-050 creation flow (CampaignNew)
    $campaignId.tsx            placeholder for FR-APP-060..064 (CampaignDetail / Control
                               Tower) — the dynamic segment is typed by TanStack Router
                               from the filename, no manual param typing needed
  harnesses/
    index.tsx                 placeholder for FR-APP-040..041 (HarnessLibrary)
```

Every placeholder route renders the same minimal shape: a page title, a one-line "this page is built in {spec-id}" note, and nothing else. This is intentional — a placeholder that tries to look finished invites someone to build real behaviour inside the wrong spec.

### Data layer shape

```
src/api/
  http.ts          apiFetch<T>(path, init?) → Promise<T>, throws ApiError on non-2xx
                    or network failure; single fetch call site for the whole app
  types.ts          HealthResponse, ServiceHealthItem, ErrorResponse  (mirrors
                    TS-APP-API-001 §6 exactly — comment marks it "keep in sync")
                    WSSnapshotMessage | WSHistoryMessage | WSNodeStateChangedMessage |
                    WSRunStateChangedMessage | WSRunTerminalMessage  (mirrors
                    TS-APP-API-005 §6 exactly — same sync comment)
                    re-exports * from "@ca/studio/domain" and "@ca/studio/canonical" etc.
  queryClient.ts    one QueryClient instance, sane defaults (staleTime, retry policy)
  ws.ts             useTypedWebSocket<TMessage>(url, { enabled }) — generic reconnect-
                    aware hook; not campaign-specific; TS-APP-UI-003 supplies the URL
                    and the message union
src/hooks/
  useHealth.ts       useQuery(["health"], () => apiFetch<HealthResponse>("/api/health"))
                     — the one hook with a real, working query key in this spec
```

---

## 6. Data Models, Contracts, Schemas, and APIs

### `HealthResponse` / `ServiceHealthItem` / `ErrorResponse` (TypeScript mirror of `TS-APP-API-001` §6)

```typescript
// src/api/types.ts
export interface ServiceHealthItem {
  readonly service: string;
  readonly product_id: string;
  readonly product_version: string;
  readonly authority_state: string;
  readonly database_path: string;
  readonly integrity: "ok" | "error";
  readonly command_count: number;
  readonly event_count: number;
  readonly receipt_count: number;
  readonly production_authorized: boolean;
  readonly certified: boolean;
  readonly claim_ceiling: string;
}

export interface HealthResponse {
  readonly status: "ok" | "degraded" | "error";
  readonly timestamp: string;
  readonly gateway_version: string;
  readonly ca_data_root: string;
  readonly services: Readonly<Record<string, ServiceHealthItem>>;
}

export interface ErrorResponse {
  readonly error_code: string;
  readonly message: string;
  readonly service?: string | null;
  readonly timestamp: string;
}
```

### WebSocket message envelope union (TypeScript mirror of `TS-APP-API-005` §6)

```typescript
// src/api/types.ts (continued)
interface NodeStatus {
  readonly node_id: string;
  readonly state: string;
  readonly attempt_count: number;
  readonly dispatch_ordinal: number | null;
  readonly output_ref: Record<string, unknown> | null;
  readonly failure: Record<string, unknown> | null;
}

interface RunStatus {
  readonly run_id: string;
  readonly workflow_id: string;
  readonly state: string;
  readonly revision: number;
  readonly cancel_requested: boolean;
  readonly current_checkpoint_id: string | null;
  readonly nodes: ReadonlyArray<NodeStatus>;
}

export type WSMessage =
  | { readonly type: "snapshot"; readonly retrieved_at_utc: string; readonly run: RunStatus }
  | { readonly type: "history"; readonly retrieved_at_utc: string; readonly event_count: number; readonly event_stream_sha256: string; readonly events: ReadonlyArray<unknown> }
  | { readonly type: "node_state_changed"; readonly retrieved_at_utc: string; readonly run_id: string; readonly node: NodeStatus }
  | { readonly type: "run_state_changed"; readonly retrieved_at_utc: string; readonly run_id: string; readonly workflow_id: string; readonly state: string; readonly revision: number; readonly cancel_requested: boolean; readonly current_checkpoint_id: string | null }
  | { readonly type: "run_terminal"; readonly retrieved_at_utc: string; readonly run: RunStatus };
```

### `ApiError`

```typescript
// src/api/http.ts
export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number | null,     // null = network failure, never reached the server
    readonly errorCode: string | null,
    readonly service: string | null = null,
  ) {
    super(message);
    this.name = "ApiError";
  }
}
```

### Route table this spec produces (all placeholder, no new backend routes)

| Path | Component | FR range rendered later by | Backend calls made by this spec |
|---|---|---|---|
| `/` | redirect → `/campaigns` | — | none |
| `/workspace` | placeholder | FR-APP-001..003 | none |
| `/interviews/compose` | placeholder | FR-APP-010..012 | none |
| `/campaigns` | placeholder | FR-APP-050 | none |
| `/campaigns/new` | placeholder | FR-APP-050 | none |
| `/campaigns/$campaignId` | placeholder | FR-APP-060..064 | none |
| `/harnesses` | placeholder | FR-APP-040..041 | none |
| *(top bar, every route)* | `<StatusPill>` | — | `GET /api/health` via `useHealth()` |

---

## 7. Implementation Stages and Exact Target Paths

All paths are relative to the repository root, after the Part 5 restructure in `CA_APP_FR_EPIC_SPEC_PLAN.md` has already been applied (`services/studio/` exists at that path, not `07_CONSCIOUS_ACTIVATIONS_STUDIO/`).

### Stage 1 — Root workspace

**`package.json`** (repository root — create if it does not already exist from an earlier spec; otherwise merge the `workspaces` key)
```json
{
  "name": "conscious-activations",
  "private": true,
  "workspaces": [
    "apps/web"
  ],
  "engines": {
    "node": ">=20.19.0"
  }
}
```

**`.nvmrc`**
```
22.12.0
```

**`.gitignore`** (append)
```
apps/web/node_modules
apps/web/dist
apps/web/src/routeTree.gen.ts
```

### Stage 2 — `apps/web` project files

**`apps/web/package.json`**
```json
{
  "name": "@conscious-activations/web",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview --port 4173",
    "typecheck": "tsc -b --noEmit",
    "lint": "eslint . --max-warnings 0",
    "test": "vitest run",
    "test:watch": "vitest"
  },
  "dependencies": {
    "react": "19.2.0",
    "react-dom": "19.2.0",
    "@tanstack/react-router": "1.170.18",
    "@tanstack/react-query": "5.101.2"
  },
  "devDependencies": {
    "vite": "8.1.5",
    "@vitejs/plugin-react": "6.0.4",
    "@tanstack/router-plugin": "1.170.18",
    "@tanstack/react-router-devtools": "1.170.18",
    "@tanstack/react-query-devtools": "5.101.2",
    "tailwindcss": "4.3.3",
    "@tailwindcss/vite": "4.3.3",
    "typescript": "5.9.2",
    "@types/react": "19.2.0",
    "@types/react-dom": "19.2.0",
    "vitest": "3.2.4",
    "@testing-library/react": "16.1.0",
    "@testing-library/jest-dom": "6.6.3",
    "jsdom": "25.0.1",
    "eslint": "9.19.0",
    "typescript-eslint": "8.22.0",
    "eslint-plugin-react-hooks": "5.1.0",
    "eslint-plugin-react-refresh": "0.4.19"
  }
}
```
Note: exact patch versions above are current as of this spec's writing date (2026-07-26). Confirm the latest patch within each pinned minor via `npm view <package> version` at implementation time; do not change a pinned **major** version without amending this spec (Section 3, "exact versions" decision).

**`apps/web/vite.config.ts`**
```typescript
import { defineConfig } from "vite";
import path from "node:path";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { tanstackRouter } from "@tanstack/router-plugin/vite";

const repoRoot = path.resolve(__dirname, "../..");

export default defineConfig({
  plugins: [
    tanstackRouter({ target: "react", autoCodeSplitting: true }),
    react(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      "@ca/studio": path.resolve(repoRoot, "services/studio/src"),
    },
  },
  server: {
    port: 5173,
    fs: {
      // services/studio/src sits outside apps/web/ — Vite's dev server refuses to
      // serve files outside its root unless explicitly allowed. See Section 3.
      allow: [repoRoot],
    },
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/ws": {
        target: "ws://localhost:8000",
        ws: true,
      },
    },
  },
  build: {
    outDir: "dist",
    sourcemap: true,
  },
});
```

**`apps/web/tsconfig.json`**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "skipLibCheck": true,
    "isolatedModules": true,
    "resolveJsonModule": true,
    "baseUrl": ".",
    "paths": {
      "@ca/studio/*": ["../../services/studio/src/*"]
    },
    "types": ["vite/client"]
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

**`apps/web/tsconfig.node.json`**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "types": ["node"]
  },
  "include": ["vite.config.ts"]
}
```

**`apps/web/index.html`**
```html
<!doctype html>
<html lang="en" class="dark">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Conscious Activations — Studio</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

**`apps/web/.env.example`**
```
# Base path the browser calls; left empty in dev because Vite's proxy (vite.config.ts)
# handles /api and /ws same-origin. Set only for a build that will NOT sit behind the
# nginx proxy described in CA_PROJECT_SNAPSHOT_V2.md Section 7.
VITE_API_BASE_URL=
```

**`apps/web/.env.development`**
```
VITE_API_BASE_URL=
```

### Stage 3 — Design tokens

**`apps/web/src/styles/index.css`**
```css
@import "tailwindcss";

@theme {
  /* Provisional palette — direct pixel sample of user-supplied branding
     reference screenshots. Not a formal design system. See TS-APP-UI-001 §3. */
  --color-background: #000000;
  --color-surface: #0d0d0f;
  --color-surface-elevated: #131316;
  --color-border: rgb(255 255 255 / 8%);
  --color-foreground: #f8f8f8;
  --color-muted-foreground: #9a9aa0;

  --color-accent: #f0a800;
  --color-accent-solid: #d8a830;
  --color-accent-foreground: #0a0700;

  --color-success: #10c058;
  --color-danger: #e02828;
  --color-info: #1070f0;

  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --radius-card: 1rem;
}

body {
  background-color: var(--color-background);
  color: var(--color-foreground);
  font-family: var(--font-sans);
}
```

### Stage 4 — Router and shell

**`apps/web/src/main.tsx`**
```tsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { RouterProvider, createRouter } from "@tanstack/react-router";
import { QueryClientProvider } from "@tanstack/react-query";
import { routeTree } from "./routeTree.gen";
import { queryClient } from "./api/queryClient";
import { DevOperatorProvider } from "./auth/DevOperatorContext";
import "./styles/index.css";

const router = createRouter({ routeTree, defaultPreload: "intent" });

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

const rootElement = document.getElementById("root")!;
createRoot(rootElement).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <DevOperatorProvider>
        <RouterProvider router={router} />
      </DevOperatorProvider>
    </QueryClientProvider>
  </StrictMode>,
);
```

**`apps/web/src/routes/__root.tsx`**
```tsx
import { createRootRoute, Outlet } from "@tanstack/react-router";
import { AppShell } from "../components/layout/AppShell";
import { RootErrorBoundary } from "../components/layout/RootErrorBoundary";

export const Route = createRootRoute({
  component: () => (
    <AppShell>
      <Outlet />
    </AppShell>
  ),
  errorComponent: RootErrorBoundary,
  notFoundComponent: () => (
    <div className="p-8 text-muted-foreground">
      <p className="text-lg font-semibold text-foreground">Not found</p>
      <p>No page is mounted at this path yet.</p>
    </div>
  ),
});
```

**`apps/web/src/routes/index.tsx`**
```tsx
import { createFileRoute, redirect } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  beforeLoad: () => {
    throw redirect({ to: "/campaigns" });
  },
});
```

**Placeholder route pattern** (repeated for each of the six pages — `campaigns/index.tsx` shown, the rest follow identically with the FR range and spec id substituted):

**`apps/web/src/routes/campaigns/index.tsx`**
```tsx
import { createFileRoute } from "@tanstack/react-router";
import { PlaceholderPage } from "../../components/layout/PlaceholderPage";

export const Route = createFileRoute("/campaigns/")({
  component: () => (
    <PlaceholderPage
      title="Campaigns"
      frRange="FR-APP-050"
      builtIn="TS-APP-UI-002"
    />
  ),
});
```

The remaining five follow the same shape:

| File | title | frRange | builtIn |
|---|---|---|---|
| `routes/workspace/index.tsx` | Workspace | FR-APP-001..003 | TS-APP-UI (not yet queued) |
| `routes/interviews/compose.tsx` | Interview Composer | FR-APP-010..012 | TS-APP-COMPOSER-001 |
| `routes/campaigns/new.tsx` | New Campaign | FR-APP-050 | TS-APP-UI-002 |
| `routes/campaigns/$campaignId.tsx` | Control Tower | FR-APP-060..064 | TS-APP-UI-003 |
| `routes/harnesses/index.tsx` | Harness Library | FR-APP-040..041 | TS-APP-UI-004 |

**`apps/web/src/components/layout/PlaceholderPage.tsx`**
```tsx
interface PlaceholderPageProps {
  readonly title: string;
  readonly frRange: string;
  readonly builtIn: string;
}

export function PlaceholderPage({ title, frRange, builtIn }: PlaceholderPageProps) {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-semibold text-foreground">{title}</h1>
      <p className="mt-2 text-sm text-muted-foreground">
        Governed by {frRange}. Built in {builtIn}.
      </p>
    </div>
  );
}
```

### Stage 5 — API client foundation

**`apps/web/src/api/http.ts`**
```typescript
import { ApiError } from "./ApiError";
import type { ErrorResponse } from "./types";

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      ...init,
      headers: { "Content-Type": "application/json", ...init?.headers },
    });
  } catch (cause) {
    throw new ApiError("Network request failed — is the gateway running?", null, null);
  }

  if (!response.ok) {
    let body: ErrorResponse | null = null;
    try {
      body = (await response.json()) as ErrorResponse;
    } catch {
      // response body was not JSON — fall through with a generic message
    }
    throw new ApiError(
      body?.message ?? `Request failed with status ${response.status}`,
      response.status,
      body?.error_code ?? null,
      body?.service ?? null,
    );
  }

  return (await response.json()) as T;
}
```

**`apps/web/src/api/ApiError.ts`**
```typescript
export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number | null,
    readonly errorCode: string | null,
    readonly service: string | null = null,
  ) {
    super(message);
    this.name = "ApiError";
  }
}
```

**`apps/web/src/api/types.ts`** — as specified in full in Section 6, plus:
```typescript
// Re-export of the Studio domain types this scaffold exists to make available.
// No modification. See TS-APP-UI-001 §3 ("consumed by source import").
export type {
  CampaignOrder,
  CampaignState,
  ControlTowerProjection,
  TimelineProjection,
  ChangeRequestProgram,
  ShipDecision,
  ShipRequest,
  HumanResolutionEpisode,
  AuditExportManifest,
  AutonomyMode,
  CampaignLifecycleState,
  OutputTarget,
} from "@ca/studio/domain";
```

**`apps/web/src/api/queryClient.ts`**
```typescript
import { QueryClient } from "@tanstack/react-query";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 10_000,
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});
```

**`apps/web/src/api/ws.ts`**
```typescript
import { useEffect, useRef, useState } from "react";

type ConnectionState = "idle" | "connecting" | "open" | "closed" | "error";

interface UseTypedWebSocketOptions {
  readonly enabled: boolean;
}

/**
 * Generic, reconnect-free WebSocket subscription. Deliberately does not retry —
 * the caller (e.g. TS-APP-UI-003's RunGraph) owns reconnect/backoff policy, since
 * TS-APP-API-005's close codes (4404/4409) mean "don't retry," not "retry."
 */
export function useTypedWebSocket<TMessage>(
  url: string | null,
  { enabled }: UseTypedWebSocketOptions,
) {
  const [state, setState] = useState<ConnectionState>("idle");
  const [lastMessage, setLastMessage] = useState<TMessage | null>(null);
  const [closeInfo, setCloseInfo] = useState<{ code: number; reason: string } | null>(null);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!enabled || !url) {
      setState("idle");
      return;
    }
    setState("connecting");
    const socket = new WebSocket(url);
    socketRef.current = socket;

    socket.onopen = () => setState("open");
    socket.onmessage = (event) => {
      try {
        setLastMessage(JSON.parse(event.data) as TMessage);
      } catch {
        // malformed frame — ignored, connection stays open
      }
    };
    socket.onerror = () => setState("error");
    socket.onclose = (event) => {
      setState("closed");
      setCloseInfo({ code: event.code, reason: event.reason });
    };

    return () => socket.close();
  }, [url, enabled]);

  return { state, lastMessage, closeInfo };
}
```

**`apps/web/src/hooks/useHealth.ts`**
```typescript
import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "../api/http";
import type { HealthResponse } from "../api/types";

export function useHealth() {
  return useQuery({
    queryKey: ["health"],
    queryFn: () => apiFetch<HealthResponse>("/api/health"),
    refetchInterval: 30_000,
  });
}
```

### Stage 6 — Dev-only auth scaffold

**`apps/web/src/auth/DevOperatorContext.tsx`**
```tsx
import { createContext, useContext, type ReactNode } from "react";

// NOT AUTHENTICATION. TS-APP-API-001 has no auth routes yet (see its own
// "Out of scope"). This exists so every future component has one place to read
// "who is the operator" from, instead of inventing its own placeholder.
interface DevOperatorActor {
  readonly actor_id: string;
  readonly actor_type: "human";
  readonly product_id: string;
  readonly workflow_role: "operator";
}

const DEV_OPERATOR: DevOperatorActor = {
  actor_id: "dev-operator-local",
  actor_type: "human",
  product_id: "conscious-activations-web",
  workflow_role: "operator",
};

const DevOperatorContext = createContext<DevOperatorActor>(DEV_OPERATOR);

export function DevOperatorProvider({ children }: { children: ReactNode }) {
  return (
    <DevOperatorContext.Provider value={DEV_OPERATOR}>
      {children}
    </DevOperatorContext.Provider>
  );
}

export function useOperator(): DevOperatorActor {
  return useContext(DevOperatorContext);
}
```

### Stage 7 — Layout shell and UI primitives

**`apps/web/src/components/layout/AppShell.tsx`**
```tsx
import type { ReactNode } from "react";
import { Sidebar } from "./Sidebar";
import { TopBar } from "./TopBar";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen bg-background text-foreground">
      <Sidebar />
      <div className="flex flex-1 flex-col">
        <TopBar />
        <main className="flex-1">{children}</main>
      </div>
    </div>
  );
}
```

**`apps/web/src/components/layout/Sidebar.tsx`** — six `<Link>`s (TanStack Router, typed `to` props) to the routes in Stage 4, styled with `--color-surface` background and `--color-accent` active state, matching the sampled palette.

**`apps/web/src/components/layout/TopBar.tsx`**
```tsx
import { useHealth } from "../../hooks/useHealth";
import { StatusPill } from "../ui/StatusPill";
import { useOperator } from "../../auth/DevOperatorContext";

export function TopBar() {
  const { data, isError, isLoading } = useHealth();
  const operator = useOperator();

  const tone = isError ? "danger" : isLoading ? "muted" : data?.status === "ok" ? "success" : "danger";
  const label = isError
    ? "API unreachable"
    : isLoading
      ? "Checking gateway…"
      : data?.status === "ok"
        ? "All systems operational"
        : "Degraded";

  return (
    <header className="flex items-center justify-between border-b border-border bg-surface px-6 py-3">
      <StatusPill tone={tone} label={label} />
      <span className="rounded-full border border-danger px-2 py-0.5 text-xs text-danger">
        DEV MODE — NOT AUTHENTICATED ({operator.actor_id})
      </span>
    </header>
  );
}
```

**`apps/web/src/components/ui/StatusPill.tsx`**, **`Card.tsx`**, **`Badge.tsx`**, **`Button.tsx`** — small, unstyled-logic presentational primitives consuming only the `--color-*` tokens from Stage 3 (each under 40 lines; omitted here for length, required by AC-004).

**`apps/web/src/components/layout/RootErrorBoundary.tsx`** — TanStack Router `errorComponent`, renders the caught error's message plus a "reload" action; does not swallow the error silently (required by AC-009).

### Stage 8 — Tooling

**`apps/web/eslint.config.js`** — flat config: `@eslint/js` recommended + `typescript-eslint` recommended + `eslint-plugin-react-hooks` + `eslint-plugin-react-refresh`, `ignores: ["dist", "routeTree.gen.ts"]`.

**`apps/web/vitest.config.ts`**
```typescript
import { defineConfig, mergeConfig } from "vitest/config";
import viteConfig from "./vite.config";

export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      environment: "jsdom",
      setupFiles: ["./src/test/setup.ts"],
      globals: true,
    },
  }),
);
```

**`apps/web/src/test/setup.ts`**
```typescript
import "@testing-library/jest-dom/vitest";
```

### Stage 9 — Docker

**`infra/docker/dockerfile.web`**
```dockerfile
FROM node:22.12.0-slim AS build
WORKDIR /repo
COPY package.json package-lock.json ./
COPY apps/web/package.json apps/web/package.json
RUN npm ci
COPY services/studio services/studio
COPY apps/web apps/web
WORKDIR /repo/apps/web
RUN npm run build

FROM nginx:1.27-alpine AS serve
COPY --from=build /repo/apps/web/dist /usr/share/nginx/html
EXPOSE 80
```
The `nginx:alpine` stage here only serves static assets on port 80 inside the container; it is **not** the same `nginx.conf` that will proxy `/api`/`/ws` for the whole deployment — that reverse-proxy config is a separate, not-yet-written infra spec (Section 2, "Out of scope"). This Dockerfile only needs to exist so `docker compose up` produces a `web` container at all.

**`infra/docker/docker-compose.yml`** — add/replace the `web` service block:
```yaml
  web:
    build:
      context: .
      dockerfile: infra/docker/dockerfile.web
    ports:
      - "3000:80"
    depends_on:
      - api
```

---

## 8. Failure, Migration, Rollback, Recovery, and Observability

### Failure modes handled

| Failure | Where handled | Behaviour |
|---|---|---|
| Gateway (`TS-APP-API-001`) not running | `src/api/http.ts` catches the `fetch` rejection | `ApiError(status: null)`; `TopBar` shows "API unreachable" in danger tone, app does not crash |
| Gateway returns 503 degraded | `apiFetch` reads the typed `ErrorResponse`/`HealthResponse` body | `TopBar` shows "Degraded"; other pages are unaffected (no other route calls the API yet) |
| Unknown route typed by hand | TanStack Router's generated route tree | Compile-time error — `routeTree.gen.ts` won't include a path that doesn't exist, so a typo in a `<Link to="...">` fails `tsc`, not at runtime |
| Component render throws | `RootErrorBoundary` (root `errorComponent`) | Caught at the shell boundary; the sidebar/top bar stay mounted, only the page body shows the error |
| `services/studio/src` moves or is deleted | `vite.config.ts` `resolve.alias` + `tsconfig.json` `paths` both point at one literal path | Both fail loudly (`tsc` error, then a Vite "Failed to resolve import" overlay) — no silent fallback |

### Migration / rollback
This spec adds new files; it does not alter `services/studio/**` or any Python package. Rollback is `git revert` of the commit(s) introducing `apps/web/`, `infra/docker/dockerfile.web`, and the root `package.json` workspace addition. No data migration exists at this layer.

### Observability
- Vite dev server logs every proxied `/api` request to its own console with target and status
- `useHealth`'s TanStack Query cache is inspectable live via `@tanstack/react-query-devtools`, mounted only when `import.meta.env.DEV`
- TanStack Router's own devtools (`@tanstack/react-router-devtools`) are mounted the same way, showing the live route tree and match state
- No external monitoring is wired in this spec; `GET /api/health`'s own polling in `TopBar` is the only "is anything alive" signal a developer needs at this wave

---

## 9. Acceptance Criteria

**AC-001 — Workspace installs cleanly**
Given a clean checkout with `.nvmrc`'s Node version active,
When `npm install` is run from the repository root,
Then `apps/web/node_modules` is populated and `package-lock.json` at the root records exact resolved versions for every package pinned in Section 7 Stage 2.
Failure example: `npm install` fails to resolve `@tanstack/router-plugin` against the pinned `vite` major.
Evidence: exit code 0, `package-lock.json` diff.
Test layer: CI — `tests/web/test_install.sh`.

**AC-002 — Dev server starts and serves the shell**
Given `npm install` succeeded,
When `npm run dev --workspace=apps/web` is run and `http://localhost:5173/` is requested,
Then the response is HTTP 200 HTML containing `<div id="root">`, and the client-rendered page (verified via a headless browser check) shows the Sidebar and TopBar.
Failure example: Vite dev server throws on `services/studio/src` import because `server.fs.allow` was omitted.
Evidence: HTTP status + rendered DOM snapshot.
Test layer: integration — `apps/web/tests/e2e/shell.spec.ts` (smoke, via Vitest browser mode or a plain `fetch`+DOM check, not full Playwright — see Section 10).

**AC-003 — Root route redirects, all six placeholders are reachable**
Given the dev server is running,
When `/` is requested, and then each of `/workspace`, `/interviews/compose`, `/campaigns`, `/campaigns/new`, `/campaigns/$campaignId` (with any string param), `/harnesses` is requested directly (not via client-side nav),
Then `/` redirects to `/campaigns`, and each other path renders its `PlaceholderPage` with the correct title and no console error.
Failure example: `/campaigns/$campaignId` 404s on direct navigation because the dynamic segment isn't registered.
Evidence: rendered title text per route.
Test layer: component — `apps/web/src/routes/*.test.tsx`.

**AC-004 — Studio domain types resolve with zero `tsc` errors**
Given `apps/web/src/api/types.ts` re-exports `CampaignOrder`, `ControlTowerProjection`, and `ChangeRequestProgram` from `@ca/studio/domain`,
When `npm run typecheck --workspace=apps/web` is run,
Then it exits 0 with no errors referencing `services/studio` or the `@ca/studio` alias.
Failure example: `moduleResolution` set to `"node"` instead of `"bundler"`, causing the `.js`-specifier imports inside `domain.ts` to fail resolution.
Evidence: `tsc` exit code and stdout.
Test layer: CI — `tests/web/test_typecheck.sh`.

**AC-005 — Live health check renders all three states**
Given the dev server is running,
When (a) `TS-APP-API-001`'s gateway is running and healthy, (b) the gateway responds 503 degraded, (c) the gateway is not running at all,
Then the `TopBar` `StatusPill` shows, respectively: "All systems operational" (success tone), "Degraded" (danger tone), "API unreachable" (danger tone) — and in no case does the page fail to render.
Failure example: case (c) throws an unhandled promise rejection instead of being caught by `apiFetch`.
Evidence: rendered pill text + tone class, per case.
Test layer: component (mocked `fetch`) — `apps/web/src/hooks/useHealth.test.ts`; one manual/CI case with a real gateway per AC-007.

**AC-006 — Production build succeeds and serves**
Given `npm run typecheck` has passed,
When `npm run build --workspace=apps/web` then `npm run preview --workspace=apps/web` is run and `http://localhost:4173/` is requested,
Then the build completes with no errors and the preview server returns HTTP 200.
Failure example: a dev-only import (e.g. router/query devtools) is not tree-shaken behind `import.meta.env.DEV` and breaks the production bundle.
Evidence: build exit code, curl exit code.
Test layer: smoke — `tests/web/test_build_smoke.sh` (bash, mirrors `TS-APP-API-001` AC-006's pattern).

**AC-007 — Docker Compose brings up a live static site**
Given `infra/docker/dockerfile.web` and `infra/docker/docker-compose.yml` are present,
When `docker compose -f infra/docker/docker-compose.yml up --build -d web` is run,
Then within 30 seconds `curl http://localhost:3000/` returns HTTP 200 containing `<div id="root">`.
Failure example: `npm ci` inside the build stage fails because `services/studio` wasn't copied into the build context before `npm run build`.
Evidence: curl exit code and response body.
Test layer: deployment smoke test — `tests/web/test_docker_smoke.sh`.

**AC-008 — Lint passes with zero warnings on the scaffold as written**
Given the scaffold from Stages 1–9 is fully in place,
When `npm run lint --workspace=apps/web` is run,
Then it exits 0 with zero errors and zero warnings (the config uses `--max-warnings 0`).
Failure example: an unused import left in a placeholder route file.
Evidence: ESLint exit code and output.
Test layer: CI — `tests/web/test_lint.sh`.

**AC-009 — A thrown render error is caught, not fatal**
Given the app is running,
When a component beneath the root route throws during render (simulated in a test via a deliberately-throwing test route),
Then `RootErrorBoundary` renders in place of that page, the `Sidebar` and `TopBar` remain mounted and interactive, and no white-screen occurs.
Failure example: the error boundary is registered on an individual route instead of the root, so navigating away doesn't recover.
Evidence: DOM assertion — sidebar present, error message present, page body replaced.
Test layer: component — `apps/web/src/components/layout/RootErrorBoundary.test.tsx`.

**AC-010 — No modification to existing service packages**
Given the Phase 9 Python test suite and `services/studio`'s own `node --test tests/*.test.mjs` were both passing before this spec,
When this spec is fully implemented,
Then `git diff` shows zero changes under `services/**` and zero changes under any Python package directory, and both pre-existing suites still pass unmodified.
Failure example: `services/studio/package.json` was edited to add an `"exports"` field to make a bare-specifier import work, contradicting Section 3's governing decision.
Evidence: `git diff --stat services/`, pytest output, `node --test` output.
Test layer: regression.

---

## 10. Testing and Completion Evidence

### Test files to create

**`apps/web/src/hooks/useHealth.test.ts`**
- `renders success state when status is ok` — AC-005(a)
- `renders degraded state when gateway returns 503` — AC-005(b)
- `renders unreachable state when fetch rejects` — AC-005(c)

**`apps/web/src/routes/*.test.tsx`** (one per placeholder route)
- `renders the correct title and FR range` — AC-003

**`apps/web/src/components/layout/RootErrorBoundary.test.tsx`**
- `catches a render error without unmounting the shell` — AC-009

**`apps/web/src/api/http.test.ts`**
- `throws ApiError with status null on network failure`
- `throws ApiError with parsed error_code on a typed 4xx/5xx body`
- `returns parsed JSON on 200`

**`tests/web/test_install.sh`** — bash, CI: `npm install` at repo root, asserts exit 0 and lockfile contains pinned versions — AC-001

**`tests/web/test_typecheck.sh`** — bash: `npm run typecheck --workspace=apps/web`, asserts exit 0 — AC-004

**`tests/web/test_lint.sh`** — bash: `npm run lint --workspace=apps/web`, asserts exit 0 — AC-008

**`tests/web/test_build_smoke.sh`** — bash, mirrors `TS-APP-API-001`'s `test_smoke.sh` pattern:
```bash
#!/usr/bin/env bash
set -euo pipefail
npm run build --workspace=apps/web
npm run preview --workspace=apps/web &
PREVIEW_PID=$!
trap "kill $PREVIEW_PID" EXIT
for i in $(seq 1 15); do
  if curl -sf http://localhost:4173/ > /dev/null; then
    echo "OK"
    exit 0
  fi
  sleep 2
done
echo "preview server did not become ready" >&2
exit 1
```
AC-006.

**`tests/web/test_docker_smoke.sh`** — same polling pattern against `docker compose up -d web` and port 3000 — AC-007.

### Test tooling
```bash
npm install --workspace=apps/web -D vitest @testing-library/react @testing-library/jest-dom jsdom
```
Component tests use Vitest + Testing Library, not Playwright — a full browser-automation dependency is not justified for a scaffold whose only interactive logic this spec introduces is a health-status pill and route placeholders. `TS-APP-UI-003` (Control Tower, WebSocket-driven) is the first spec where a real end-to-end browser test earns its cost; it can add Playwright then without this spec having pre-committed the whole app to it.

### Pre-existing regression
Run before and after implementing this spec:
```bash
python -m pytest tests/ -q --tb=short
node --test services/studio/tests/*.test.mjs
```
Zero new failures in either suite is a hard gate (AC-010).

### Build Receipt claim ceiling
`UI_SCAFFOLD_DEVELOPMENT_EVIDENCE`

This spec does not claim:
- any page's real functionality (campaign list, campaign creation, control tower, harness library, interview composer, workspace setup — all later specs)
- a finished or brand-authority-approved design system (Section 3 palette is provisional)
- authentication or authorization
- WebSocket-driven UI (the transport hook exists; no component consumes it yet)
- production nginx routing (only a static-asset-serving Dockerfile stage)
- certified operation

---
spec_end: true
next_spec: TS-APP-UI-002 (Campaign List and Creation UI)
prerequisite_for_next: AC-002, AC-003, and AC-004 must pass (dev server runs, all placeholder
  routes reachable, Studio types resolve) before TS-APP-UI-002 implementation begins
