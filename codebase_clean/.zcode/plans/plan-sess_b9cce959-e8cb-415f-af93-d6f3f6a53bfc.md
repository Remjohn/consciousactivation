## TS-APP-UI-004 — Finish the Harness Library UI

### State assessment
The previous session authored ~25 files but staged them in `docs/TS-APP-UI-004/` instead of landing them under `apps/web/src/`. I've verified the spec (`docs/tech-specs/TS-APP-UI-004.md`) against the real backend (`api/routers/harnesses.py:141-206, 463-510`) — **field names match exactly** (`definition_id`, `task_id`, `mode`, `category_id`, `category_name`, `production_ready`, `certified`, `capability_requirements`, etc.). The staged files are spec-faithful and import the existing primitives (`Card`/`Badge`/`apiFetch`/`ApiError`) correctly.

**One real gap:** the staging area has **no `$definitionId.test.tsx`**. The spec Section 10 requires it for AC-007 (full detail render), AC-008 (404 panel), and AC-010 (eligibility-call gating). I'll write this file fresh.

### Approach
Place the staged files into their real locations, extend `api/types.ts` additively, replace the two placeholder files, write the one missing test, then run the full AC suite. The route tree regenerates itself when Vitest runs (the `tanstackRouter` Vite plugin scans routes at startup).

### Step 1 — Extend `apps/web/src/api/types.ts` (additive)
Append the harness DTOs from the staged `types.ts` **after** the existing `WSMessage` export and **before** the Studio re-export block. Adds: `CanonicalCategoryId`, `CANONICAL_CATEGORIES`, `HarnessMode`, `HarnessSummary`, `CategoryBindingDetail`, `HarnessDetail`, `EligibilityStatus`, `EligibilityResponse`, `HarnessLibrarySearch`. Zero edits to existing lines (satisfies AC-011).

### Step 2 — `apps/web/src/lib/harnessEligibility.{ts,test.ts}` (new dir `lib/`)
Place the pure `computeEligibilityPreview` function + its 7-branch test (AC-009).

### Step 3 — `apps/web/src/hooks/{useHarnesses,useHarnessDetail,useHarnessEligibility}.{ts,test.ts}` (6 files)
Three TanStack Query hooks + their state tests. Hooks use the existing `apiFetch`/`ApiError` exactly like `useHealth`.

### Step 4 — `apps/web/src/components/harness/` (new dir, 10 components + 2 tests)
Place: `ModeBadge`, `EligibilityBadge`, `CategoryBadge`, `CertificationBadges`, `HarnessCard` (+test), `HarnessFilterBar` (+test), `HarnessLibraryEmptyState`, `HarnessLibraryErrorState`, `HarnessNotFoundPanel`, `ContractPanel`, `GovernancePanel`.

### Step 5 — `apps/web/src/test/renderWithRouter.tsx` (new shared util)
Memory-history `RouterProvider` wrapper backed by the generated `routeTree`. Reusable by future UI specs.

### Step 6 — Replace `apps/web/src/routes/harnesses/index.tsx` and `index.test.tsx`
Replace the placeholder route with the spec's `HarnessLibraryPage` (card grid + filter bar + empty/error states + URL-search-param filtering via `validateSearch`). Replace the placeholder smoke test with the full AC-001/002/003/004/009 composition test. Also place the co-located `apps/web/src/routes/harnesses/-validateHarnessSearch.ts`.

### Step 7 — Create `apps/web/src/routes/harnesses/$definitionId.tsx` + **write `$definitionId.test.tsx` (NEW)**
Place the detail route. **Write the missing `$definitionId.test.tsx`** — the one file not in the staging area. It covers:
- AC-007: success render asserts `goal`, `success_condition`, `atomic_boundary`, both contracts (via `ContractPanel`'s `<pre>`), and `GovernancePanel` content all present.
- AC-008: `GET /api/harnesses/{id}` → 404 renders `HarnessNotFoundPanel` + back-link, no crash.
- AC-010: three cases — (a) activative + sourceCategory → eligibility fetch fires; (b) generic + sourceCategory → zero eligibility fetches, `NOT_APPLICABLE` shown; (c) no sourceCategory → no eligibility UI, zero fetches.

Modeled on the existing `index.test.tsx` pattern (mock `global.fetch`, use `renderWithRouter`).

### Step 8 — Run every AC
```bash
npm run test --workspace=apps/web        # all Vitest tests incl. AC-001..AC-010
npm run typecheck --workspace=apps/web   # tsc -b
```
Confirm zero new failures (AC-011 also requires the pre-existing Python/Studio suites to remain untouched — verified by `git diff --stat` showing changes only under `apps/web/src/`).

### What I will NOT do (per spec Section 2 / AC-011)
- Touch any Python file, `api/routers/harnesses.py`, or `services/**`.
- Add a `profile_id` filter (inherited Gap 4 — the field doesn't exist).
- Build the "attach to Campaign" action (TS-APP-UI-002's job).
- Introduce any new dependency (zod/etc.) — `validateSearch` stays hand-written.

### Files to land (27 total, 1 newly written)
Under `apps/web/src/`: `api/types.ts` (edit), `routes/harnesses/{index.tsx,index.test.tsx,-validateHarnessSearch.ts,$definitionId.tsx,$definitionId.test.tsx}`, `components/harness/*` (12), `hooks/*` (6), `lib/*` (2), `test/renderWithRouter.tsx` (1).

The staging files in `docs/TS-APP-UI-004/` will be left in place (untracked working notes) — not part of the deliverable, not deleted.