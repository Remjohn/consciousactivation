# TS-APP-UI-001 — Apply Guide

This package is a **delta**, not a full repo. `apps/web/` is entirely new (the
checkout only had empty `.gitkeep` stubs there). Everything else in this zip
either creates a new path or replaces one existing file wholesale.

## 1. What to copy where

Unzip this archive over your repo root, preserving paths:

```
.gitignore                          → REPLACES the existing one (see §2 — it's an append, not a rewrite)
.nvmrc                              → new file
package.json                        → new file (root workspace manifest)
apps/web/**                         → new directory, copy wholesale
infra/docker/dockerfile.web         → new file
infra/docker/docker-compose.yml     → REPLACES the existing one (only the `web:` service block changed — see §2)
tests/web/**                        → new directory, copy wholesale (chmod +x already set on the .sh files)
```

Nothing under `services/**`, `packages/**`, or `api/**` is touched — confirmed
by diffing file mtimes before and after this work (see §4, AC-010).

## 2. The two files that replace existing ones

**`.gitignore`** — four lines were appended to the existing file:
```
apps/web/node_modules
apps/web/dist
apps/web/src/routeTree.gen.ts
apps/web/.tanstack
```
(The fourth line covers a runtime cache directory the router plugin creates
during `dev`/`build` — caught while re-verifying the final package, not
in the original spec.)
If you'd rather hand-edit instead of overwriting, just add those four lines
yourself and skip copying this file.

**`infra/docker/docker-compose.yml`** — only the `web:` service block changed
(it previously had no working build; see §3 for what changed and why). The
`api:` service and everything else in the file is untouched.

## 3. Real bugs found and fixed while actually running this (not just written from the spec)

The spec (Section 7) is correct in intent everywhere below; these are places
where the literal text, if typed verbatim, does not run on a real machine.
Every one of these was caught by actually installing, building, and testing
— not by inspection.

1. **`apps/web/package.json`'s dependency versions** — several of the spec's
   pinned exact versions are already stale (e.g. `@tanstack/router-plugin`
   and `@tanstack/react-router-devtools` don't version-lockstep with
   `@tanstack/react-router` the way the spec's table assumes). Resolved to
   the latest patch within each pinned **major**, per the spec's own
   instruction not to silently bump majors. `@types/node` was missing
   entirely (needed by `tsconfig.node.json`'s `"types": ["node"]` but never
   listed as a dependency) — added. `@testing-library/jest-dom@6.10.0` is a
   flagged broken release (npm deprecation warning); pinned to `6.9.1`.

2. **`tsconfig.node.json` needs `"composite": true`** — without it, `tsc -b`
   fails immediately with `TS6306: Referenced project ... must have setting
   "composite": true`, because `tsconfig.json` references it via
   `"references"`.

3. **`tsconfig.json` needs `"noEmit": true`** — without it, `tsc -b` (in the
   spec's literal build script) emits a `.js` file next to every `.tsx`
   source file, and the TanStack Router generator then treats those `.js`
   files as *additional, conflicting* route definitions, hard-failing the
   build. This also means the emit reached **outside** `apps/web/` — because
   `apps/web/src/api/types.ts` imports types from `@ca/studio/domain` via a
   path alias, TypeScript pulls `services/studio/src/domain.ts` into the
   same compilation program, and a `noEmit`-less `tsc -b` had emitted two
   stub `.js` files there too. Both were caught and deleted; a follow-up
   clean rebuild confirmed the fix stops it from recurring (see §4, AC-010).

4. **Composite projects can't disable emit** — once `noEmit` was added
   correctly, `tsconfig.node.json` (which must be `composite: true` to be a
   valid reference target) then legitimately needs to emit *something*.
   Rather than pollute `apps/web/` with `vite.config.js`/`vite.config.d.ts`,
   both `tsconfig.json` and `tsconfig.node.json` now redirect their
   `tsBuildInfoFile`/`outDir` into `apps/web/node_modules/.ts-build/`
   (already covered by the `node_modules` gitignore pattern).

5. **Build script ordering** — the spec's literal `"build": "tsc -b && vite
   build"` fails on a truly fresh checkout: `tsc -b` runs first and
   immediately fails on `Cannot find module './routeTree.gen'`, because that
   file doesn't exist until Vite's TanStack Router plugin generates it. The
   scripts are now `"build": "vite build && tsc -b"` and `"typecheck": "tsc
   -b"` — Vite generates the route tree as part of its own build, then `tsc`
   re-checks the now-complete tree as a real gate.

6. **`useHealth`'s query error wasn't typed** — `apiFetch` throws `ApiError`,
   but `useQuery` without an explicit error generic infers `Error`, so
   `result.current.error?.status` (an `ApiError`-only field) failed to
   typecheck anywhere the hook's error is read. Fixed with
   `useQuery<HealthResponse, ApiError>(...)`.

7. **`DevOperatorContext.tsx` legitimately fails lint** —
   `react-refresh/only-export-components` fires because the file exports
   both the `DevOperatorProvider` component and the `useOperator` hook. This
   is the standard, correct Context+hook co-location pattern, not a mistake,
   so it's suppressed with a one-line, commented `eslint-disable-next-line`
   rather than restructured.

8. **`Route.options.component` is empty at runtime under
   `autoCodeSplitting: true`** — this was the least obvious one. The
   router-plugin's code-splitting transform rewrites each route file at
   build/transform time, stripping the inline `component` out of the
   exported `Route.options` object (replacing it with a lazy reference).
   Vitest runs through the *same* Vite transform pipeline, so any test that
   imports a route file's `Route` export and reads `.options.component`
   gets `undefined` — even though a plain, untransformed Node script shows
   the field populated. **Fix:** each placeholder route now also exports its
   page as a named function (`WorkspaceIndexPage`, `CampaignsIndexPage`,
   etc.), and the six route tests import and render that named export
   directly instead of going through `Route.options.component`.
   **Known trade-off:** because these page components are now also exported
   (not just referenced inline), the code-splitting plugin can no longer
   safely extract them into separate chunks — it emits a build-time warning
   ("these exports will not be code-split...") and the production build is
   one ~98KB-gzipped bundle instead of ~8 small per-route chunks. For a
   scaffold with six placeholder pages this doesn't matter in practice, but
   if per-route code-splitting genuinely matters before this grows, the
   clean fix is to move each page component into a sibling non-route file
   (e.g. `workspace/index.page.tsx`) that the route file imports and that
   the test imports directly — the router-generator's own warning suggests
   exactly this. Left as-is here to stay within scope; flagging for a
   follow-up rather than silently declaring it done.

9. **`__root.tsx`'s error boundary was unmounting the whole shell, not just
   the page** — the most significant fix, and a genuine violation of AC-009
   as originally structured. Setting `errorComponent` directly on the root
   route (alongside a `component` that renders `<AppShell><Outlet/></AppShell>`)
   wraps *everything that route renders* — Sidebar and TopBar included — in
   one React error boundary. When a child route throws, React unmounts the
   entire subtree under that boundary, so the whole shell disappeared, not
   just the routed content. Confirmed empirically: a test asserting the
   Sidebar's "Conscious Activations" text survives a thrown child-route
   error failed outright with the original structure. **Fix:** `__root.tsx`
   now wraps only `<Outlet/>` in TanStack Router's exported `CatchBoundary`
   component (keyed on the current pathname, so navigating away
   auto-recovers), with `AppShell` sitting outside that boundary. Root's own
   `errorComponent` is kept only as a last-resort fallback for the
   (unlikely) case that `AppShell` itself throws.

10. **Vite's TanStack Router plugin's `routeFileIgnorePattern` option**
    doesn't suppress the "does not export a Route" warning for the
    colocated `*.test.tsx` files the spec explicitly wants inside
    `src/routes/` (Section 10). The option is documented and passed
    correctly, but the warning persists — this looks like a plugin-internal
    quirk in the installed version rather than a misconfiguration on this
    end. It's cosmetic only: build, lint, typecheck, and test all still
    exit 0. Not chased further; flagging honestly rather than hiding it.

## 4. What was actually run (not assumed)

All of the below were executed for real, in this order, from a clean
`npm install`, against the real `TS-APP-API-001` gateway (`uvicorn
api.main:app`, all nine local Python packages installed editable):

- `npm install` at repo root — exit 0, `apps/web/node_modules` populated
- `npm run typecheck --workspace=apps/web` — exit 0
- `npm run build --workspace=apps/web` — exit 0, `dist/` produced
- `npm run preview --workspace=apps/web` + `curl localhost:4173/` — HTTP 200
- `npm run lint --workspace=apps/web` — exit 0, zero warnings
- `npm run test --workspace=apps/web` — 9/9 files, 13/13 tests passing
- `npm run dev --workspace=apps/web` + `curl localhost:5173/` — HTTP 200
- `curl localhost:5173/api/health` (through the Vite proxy, gateway live) —
  real `200 {"status":"ok", ...}` payload from all five services
- A full leak check (`find services packages -newermt ... `) after every
  build, confirming zero files outside `apps/web/`, `infra/docker/`, and
  `tests/web/` were created or modified (AC-010) — this caught the two
  stub files described in §3.3 above, which were then deleted.

**Not run:** AC-007's `docker compose up --build -d web` smoke test. This
sandbox has no Docker daemon (`docker: not found`). The Dockerfile and
compose changes were reviewed carefully by hand (paths checked against the
real tree, build context fixed — see below), and `tests/web/test_docker_smoke.sh`
is included for you to run in an environment with Docker. If it fails, the
most likely culprit given everything else that surfaced above is the
`npm ci` layer needing the full `apps/web/` directory copied before it runs,
not just the manifests — the Dockerfile already does this in two steps
(manifests first for layer caching, then full source), but that's the first
thing to check.

**One deliberate deviation from the spec's literal Stage 9 sketch:**
`docker-compose.yml`'s `web` service uses `context: ../..` (repo root),
matching the pattern the pre-existing `api` service already uses from this
same file, rather than the spec's literal `context: .` — this compose file
lives at `infra/docker/docker-compose.yml`, not at the repo root, so `.`
would resolve to `infra/docker/`, and `dockerfile.web`'s `COPY` instructions
(`package.json`, `services/studio`, `apps/web`) are all repo-root-relative.

## 5. Acceptance criteria — verified status

| AC | What it checks | Status | Evidence |
|---|---|---|---|
| AC-001 | `npm install` clean, lockfile records pinned versions | **PASS** | exit 0, `apps/web/node_modules` populated, re-run from scratch a second time to confirm reproducibility |
| AC-002 | Dev server serves the shell (Sidebar+TopBar) | **PASS**, with a caveat | `curl localhost:5173/` → HTTP 200 with `<div id="root">`, confirmed against the real running gateway. No headless-browser DOM snapshot of the *client-rendered* page was taken against the live dev server (no Playwright/Puppeteer in this sandbox) — instead, `RootErrorBoundary.test.tsx` renders the real, unmocked `AppShell` (Sidebar+TopBar) in jsdom and confirms both render, which is the same component tree the dev server serves. |
| AC-003 | `/` redirects, all six placeholders reachable with correct title | **PASS** | Redirect logic reviewed (`beforeLoad` → `redirect`); all six route component tests pass; `routeTree.gen.ts` (generated by the real build) confirmed to contain all six paths. Did not individually curl/navigate each path against the live dev server. |
| AC-004 | Studio domain types resolve, zero `tsc` errors | **PASS** | `npm run typecheck` exit 0; confirmed all 12 re-exported type names exist in `services/studio/src/domain.ts` |
| AC-005 | Health check renders all three states | **PASS** | `useHealth.test.ts` — 3/3 (success/degraded/unreachable, mocked fetch); real-gateway case additionally confirmed live via the dev-server proxy |
| AC-006 | Production build succeeds and serves | **PASS** | `npm run build` exit 0; `npm run preview` + `curl localhost:4173/` → HTTP 200 |
| AC-007 | `docker compose up` serves on :3000 | **NOT RUN** | No Docker daemon in this sandbox. Dockerfile/compose reviewed by hand and one real bug fixed (build context). Script provided; please run it yourself. |
| AC-008 | Lint, zero warnings | **PASS** | `npm run lint` exit 0, zero warnings, zero errors |
| AC-009 | Thrown render error caught, shell stays mounted | **PASS**, after a real fix | See §3.9 — this AC failed with the spec's literal root-route structure and required restructuring around `CatchBoundary` to actually pass |
| AC-010 | Zero changes under `services/**` / Python packages | **PASS**, after cleanup | See §3.3/§4 — two stub files leaked into `services/studio/src/` during debugging, caught by an mtime sweep, deleted, and confirmed not to recur on a clean rebuild |

## 6. Quick start after applying

```bash
npm install
uvicorn api.main:app --reload &        # Wave 1 prerequisite
npm run dev --workspace=apps/web       # http://localhost:5173
```
