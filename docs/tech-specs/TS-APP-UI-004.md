---
spec_id: TS-APP-UI-004
title: Harness Library UI
document_class: TECH_SPEC
product: Conscious Activations
module: web
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CURRENT
build_authority: false
controlling_frs:
  - FR-APP-040 (harness library browsing — fully owned by this spec)
  - FR-APP-041 (harness selection for campaign — partially owned; this spec builds the
    eligibility *display*, not the campaign-attachment *action*; see Section 2 scope split)
controlling_stories:
  - ST-APP-06.01 (browse available Harnesses — fully specified in CA_APP_FR_EPIC_SPEC_PLAN.md
    Part 3: "operator sees at least one Harness; clicking shows capability list")
upstream_dependencies:
  - CA_PROJECT_SNAPSHOT_V2.md (authority — CURRENT)
  - CA_APP_FR_EPIC_SPEC_PLAN.md (authority — CURRENT)
  - TS-APP-UI-001.md (quality_state: WRITTEN_PENDING_AUDIT — DRAFT_DEPENDENCY_NOT_ACCEPTED;
    this spec replaces the `routes/harnesses/index.tsx` placeholder it created and reuses its
    `apiFetch`/`ApiError`/`queryClient` data layer, `Card`/`Badge`/`StatusPill`/`Button`
    primitives, and provisional design tokens, all unmodified; TS-APP-UI-001's AC-002, AC-003,
    and AC-004 must already pass before this spec's own routes can be exercised)
  - TS-APP-API-002.md (quality_state: WRITTEN_PENDING_AUDIT — DRAFT_DEPENDENCY_NOT_ACCEPTED;
    this spec consumes its four routes and `HarnessSummary`/`HarnessDetail`/`EligibilityResponse`
    shapes verbatim; zero new backend code is added here; this spec inherits, and does not
    resolve, that spec's Gap 4 and Gap 5 claim-ceiling limitations)
downstream_consumers:
  - TS-APP-UI-002 (Campaign List and Creation UI — not yet written; its harness-selection step
    will need to deep-link into this page's list route and define its own "attach to Campaign
    Order" return-value contract, which this spec deliberately does not build — see Section 2)
output_path: apps/web/src/routes/harnesses/ (and supporting files listed in Section 7)
wave: 3
---

# TS-APP-UI-004 — Harness Library UI

## 1. Files and Authorities Read

| File | SHA-256 (short) | Status | Fact extracted |
|---|---|---|---|
| `CA_PROJECT_SNAPSHOT_V2.md` | `b568220d` | READ — CURRENT AUTHORITY | Section 7 names `HarnessLibrary.tsx` in the target `apps/web/src/pages/` tree. Section 9's Pi-Coding-Agent flow diagram states plainly: "Harness appears in UI → `HarnessLibrary.tsx` shows it as selectable → Operator selects it in `CampaignNew`" — confirming the *browse* half of that chain is this spec's job and the *select-for-a-campaign* half belongs to whatever builds `CampaignNew`. |
| `CA_APP_FR_EPIC_SPEC_PLAN.md` | `8ea2646c` | READ — CURRENT AUTHORITY | Part 1 gives FR-APP-040 (browsing: category, format profile, version, capability requirements) and FR-APP-041 (selection + compatibility validation) verbatim. Part 4 defines this spec's nominal scope as `apps/web/src/pages/HarnessLibrary.tsx, components/HarnessCard.tsx`, depending on `TS-APP-UI-001` and `TS-APP-API-002`. Part 3's `ST-APP-06.01` is the only story with a written acceptance line for this Epic. |
| `TS-APP-API-002.md` | `a61d6b93` | READ — DRAFT_DEPENDENCY_NOT_ACCEPTED | Full `HarnessSummary`/`HarnessDetail`/`BuildHarnessResponse`/`EligibilityResponse` Pydantic shapes and worked JSON examples (§6); the four route paths, status codes, and error-code table (§6); the eligibility decision flow (§5); Gap 1 (filesystem-scan library, no DB listing), Gap 3 (eligibility is net-new, additive), Gap 4 (Builder-export schema and Pipeline-intake schema are incompatible — no `profile_id` exists anywhere in this data), and Gap 5 (only structural `CategoryBinding` validation runs; no constitutional-authority check is reachable) (§1). |
| `TS-APP-UI-001.md` | `f76a6d9a` | READ — DRAFT_DEPENDENCY_NOT_ACCEPTED | The exact placeholder this spec replaces — `routes/harnesses/index.tsx` renders `<PlaceholderPage title="Harness Library" frRange="FR-APP-040..041" builtIn="TS-APP-UI-004" />`, i.e. TS-APP-UI-001 itself names this spec as the owner of that route (§7 Stage 4 table). The `apiFetch`/`ApiError` data layer and `QueryClient` defaults (§7 Stage 5). The `Card`/`Badge`/`StatusPill`/`Button` UI primitives and `--color-*` design tokens (§7 Stage 3, Stage 7). Confirmation that routing is TanStack Router, file-based, with a precedent for a typed dynamic segment (`campaigns/$campaignId.tsx`) that this spec's `harnesses/$definitionId.tsx` follows the same way. No mention anywhere of a `src/pages/` directory actually being built — see Governing Decision in Section 3. |
| `services/builder/src/cmf_builder/domain/category_binding.py` | `05cc1e52` | READ — CURRENT IMPLEMENTATION (independently re-read from the Phase-09 archive, not merely cited secondhand from `TS-APP-API-002`) | The exact five `CanonicalCategory(category_id, canonical_name, governance_owner)` tuples this spec's category filter and `CategoryBadge` labels are drawn from verbatim (see Section 6). `CategoryBinding.canonical_dict()` returns a 17-field governance record when `applicability == "REQUIRED"` (activative mode); `CategoryBinding.portable_projection()` — the method actually used when compiling the *portable* export this API's `HarnessDetail.category_binding` field ultimately reflects — collapses to a 3-field `{applicability: "NOT_APPLICABLE", basis, category_id: null}` shape for generic-mode Harnesses. `TS-APP-API-002` §6 types `category_binding` as a bare `dict` without this distinction; this spec models it precisely as a discriminated union instead (Section 6). |
| `image-gen-1_10_.png`, `image-gen-1_4_.png`, `image-gen-4_3_.png` (branding reference) | — | REFERENCE, NOT RE-SAMPLED | Already sampled once by `TS-APP-UI-001` §3 into the provisional `--color-*` token set (`background`, `surface`, `accent`, `accent-solid`, `success`, `danger`, `info`, …). This spec consumes those tokens unmodified through the existing `Badge`/`Card` primitives; no new colour sampling is performed here. |

**Source gap notice:** both upstream Tech Specs this one depends on carry `quality_state: WRITTEN_PENDING_AUDIT`. This spec is written against their *documented* contracts — the exact route paths, field names, and error codes stated in `TS-APP-API-002` §6 and the exact file layout and primitives stated in `TS-APP-UI-001` §7 — not against any claim that either is bug-free or has passed its own audit yet. If either spec's audit changes a field name, a status code, or a file path before this one is implemented, this spec's Section 6 and Section 7 need a corresponding correction before implementation begins, the same way `TS-APP-API-002` itself needed a corrective patch (its own Gap 2) against `TS-APP-API-001`'s output.

---

## 2. Problem, User Outcome, Solution, and Scope

### Problem without this spec
`TS-APP-API-002` gives the gateway four working Harness routes, and `TS-APP-UI-001` gives the operator a reachable `/harnesses` URL — but that URL renders nothing but a title and the sentence "Built in TS-APP-UI-004." An operator cannot see what Harnesses exist, what a Harness actually promises to do, whether it is category-bound or category-neutral, or whether it would even be a legal choice for the kind of source material they have, without leaving the browser entirely and running `cmf-builder inspect --artifact-id <id>` from a shell.

### User outcome
An operator opens `/harnesses` and sees every Harness in the workspace library as a card: task, mode, category (or "Category-neutral"), capability requirements, and honest certification status (today, always "not production-ready, not certified" — and the UI never hides or softens that). They can narrow the grid by category, by mode, or by a free-text search over the task and manifest identifiers. Clicking a card opens a full detail page: the Harness's stated goal, success condition, atomic boundary, input/output contracts, capability requirements, acceptance tests, and its full governance record (constitutional authority reference, runtime law, wrong-reading locks, lineage). If the operator (or, later, the campaign-creation flow) arrives with a `?sourceCategory=` in the URL, every card instantly shows an eligibility preview — computed locally, with no extra network round trip — and the detail page additionally makes one real call to the authoritative eligibility endpoint to show the server's own reasoning in words.

### Solution
Two new TanStack Router file routes — `apps/web/src/routes/harnesses/index.tsx` (replacing the Stage-4 placeholder from `TS-APP-UI-001`) and `apps/web/src/routes/harnesses/$definitionId.tsx` (new) — backed by three TanStack Query hooks that call the three read routes `TS-APP-API-002` already defines (`GET /api/harnesses`, `GET /api/harnesses/{id}`, `GET /api/harnesses/{id}/eligibility`), a small presentational component set under `src/components/harness/`, and one pure function (`computeEligibilityPreview`) that mirrors the server's own eligibility logic client-side so the list page's per-card badges cost zero extra requests.

### In scope
- `apps/web/src/routes/harnesses/index.tsx` — replaces the `TS-APP-UI-001` placeholder; card grid, filter bar, empty/error states, URL-search-param-driven filtering
- `apps/web/src/routes/harnesses/$definitionId.tsx` — new; full `HarnessDetail` view, not-found handling, opt-in authoritative eligibility check
- `apps/web/src/components/harness/{HarnessCard,HarnessFilterBar,HarnessLibraryEmptyState,HarnessLibraryErrorState,HarnessNotFoundPanel,ModeBadge,CategoryBadge,EligibilityBadge,CertificationBadges,ContractPanel,GovernancePanel}.tsx`
- `apps/web/src/hooks/{useHarnesses,useHarnessDetail,useHarnessEligibility}.ts`
- `apps/web/src/lib/harnessEligibility.ts` — the pure, network-free preview function
- `apps/web/src/api/types.ts` additions: `HarnessMode`, `CanonicalCategoryId`, `CANONICAL_CATEGORIES`, `HarnessSummary`, `CategoryBindingDetail`, `HarnessDetail`, `EligibilityResponse`, `EligibilityStatus`
- A small router test harness (`apps/web/src/test/renderWithRouter.tsx`) — new, shared, reusable by later UI specs that also need search-param-aware route tests

### Out of scope
- Any modification to `api/routers/harnesses.py`, `api/harness_library.py`, or any Python package — this spec is a read-only consumer of an already-defined API
- A human-authoring form for `POST /api/harnesses/build` (FR-APP-042). That route exists to let the Pi Coding Agent submit a governed operator manifest as raw JSON; no spec in `CA_APP_FR_EPIC_SPEC_PLAN.md` Part 4 currently queues a React form for hand-authoring one, and this spec does not add one either — **flagged as a real, currently-unqueued gap** for anyone who wants a human-facing Harness-creation UI rather than an agent-facing endpoint
- The actual "attach this Harness to a Campaign Order" action and any return-value contract to `CampaignNew` (the second half of FR-APP-041). `TS-APP-UI-002` does not exist yet; inventing its callback shape here would be speculative. This spec's contribution to FR-APP-041 is limited to making eligibility *visible* — a plain, shareable `?sourceCategory=` URL parameter any future page can deep-link with, and nothing more
- Downloading the raw exported ZIP. No endpoint in `TS-APP-API-002` serves the package bytes themselves (only its parsed manifest metadata); `package_file`/`package_hash` are shown as inspectable metadata, not as a download link
- Server-side filtering, search, or pagination. `GET /api/harnesses` takes no query parameters (`TS-APP-API-002` §6 endpoint table) and returns the whole library in one response; all filtering in this spec is client-side over that one response — **flagged as a forward scale risk**, not a defect at today's expected library size
- Real-time updates when the Pi Coding Agent builds a new Harness while this page is open. No WebSocket exists for this resource; the page relies on TanStack Query's normal stale-time/refetch behavior and a manual browser refresh
- Format-profile browsing or filtering, as FR-APP-040's literal text describes. No `profile_id` field exists anywhere in the data this API returns — `TS-APP-API-002`'s own Gap 4 already establishes this is impossible until a schema-reconciliation spec closes it; this UI inherits that limitation rather than fabricating a filter for a field that does not exist

---

## 3. Governing Decisions and Constraints

**Component location follows the scaffold that was actually built, not the older plan sketch.** Both `CA_PROJECT_SNAPSHOT_V2.md` §7 and `CA_APP_FR_EPIC_SPEC_PLAN.md` Part 4 say `apps/web/src/pages/HarnessLibrary.tsx`. But `TS-APP-UI-001` — the spec that actually built `apps/web/` — uses TanStack Router's file-based routing under `src/routes/` and creates no `src/pages/` directory at all; it explicitly names `routes/harnesses/index.tsx` as the file this spec fills in. This spec follows the built scaffold, the same way `TS-APP-UI-001` itself superseded the Epic Plan's Part 5 Step 4 skeleton rather than re-litigating an older planning document once a more specific, already-implemented authority exists.

**Eligibility has two tiers, and this is deliberate, not a shortcut.** `TS-APP-API-002`'s eligibility logic is: generic mode → `NOT_APPLICABLE`; activative mode → compare `category_binding.category_id` to the caller's `source_category`. Every field that comparison needs (`mode`, `category_id`) is already present on `HarnessSummary` — the same object `GET /api/harnesses` already returned to render the grid. Calling the real eligibility endpoint once per visible card to re-derive a fact the client can already compute would be a pure N+1 request pattern with no new information gained on the list page. So: the **list page** computes an eligibility *preview* with a pure, zero-network function (`computeEligibilityPreview`, Section 6) that mirrors the server's own branching exactly; the **detail page** — visited deliberately, one Harness at a time — makes the one real call to `GET /api/harnesses/{id}/eligibility` to surface the server's authoritative `reason` string, which the client cannot fabricate on its own. This mirrors `TS-APP-UI-001`'s own doctrine of wiring exactly one real network call where it earns its cost (`GET /api/health` in that spec) rather than wiring speculative calls everywhere a call is possible.

**Filter state lives in the URL, not in local component state.** `apps/web/src/routes/harnesses/index.tsx` declares a typed `validateSearch` (`category`, `mode`, `q`, `sourceCategory`) so that a filtered view is a real, shareable, back-button-safe URL — consistent with the router-first architecture `TS-APP-UI-001` established (typed routes, typed dynamic segments) and useful in practice: a future `CampaignNew` step can link an operator straight into `/harnesses?sourceCategory=carousels` and get a pre-filtered, badge-annotated view for free. No schema-validation library (`zod`, `valibot`, …) is introduced for this — `TS-APP-UI-001`'s `package.json` pins no such dependency, and a four-field, all-optional-string search object does not justify adding one; `validateSearch` is one small hand-written function (Section 7).

**`category_binding` is modeled as a discriminated union, not a bare `dict`.** `TS-APP-API-002` §6 types `HarnessDetail.category_binding` as an untyped `dict` because the Builder's own `CategoryBinding.portable_projection()` — read directly in this spec, Section 1 — returns one of two structurally different shapes depending on `applicability`. Modeling it precisely here (Section 6) lets `GovernancePanel` render each shape correctly instead of defensively probing for optional fields at render time.

**No modification to `HarnessSummary`/`HarnessDetail`/`EligibilityResponse` field names.** This spec's TypeScript interfaces mirror `TS-APP-API-002` §6 field-for-field, in the same snake_case the API actually returns (matching the convention `TS-APP-UI-001` already established for `HealthResponse`/`ServiceHealthItem` — the wire shape is not translated into camelCase at the boundary). Each interface carries the same "mirrors `TS-APP-API-002` §6 — keep in sync" comment convention.

**Certification status is always shown, never hidden or styled to look better than it is.** Every `HarnessSummary`/`HarnessDetail` in the library self-reports `production_ready: false, certified: false` today (`TS-APP-API-002` Gap 4/5). `CertificationBadges` renders both fields in a neutral/muted tone in every case — there is no "hide when false" toggle and no green styling applied to `false`. This spec's own claim ceiling (Section 10) depends on this: it must not visually launder a state the backend itself has not certified.

**Claim ceiling:** `HARNESS_LIBRARY_UI_DEVELOPMENT_EVIDENCE`. This spec does not claim Pipeline-execution readiness, constitutional-authority certification, or production eligibility for anything it displays — it renders exactly what `TS-APP-API-002` returns, unmodified, including that API's own `false` values.

---

## 4. Current Brownfield Architecture

| Component | Path | Actual behaviour | Disposition | Reason |
|---|---|---|---|---|
| `routes/harnesses/index.tsx` (from `TS-APP-UI-001`) | `apps/web/src/routes/harnesses/index.tsx` | Renders `<PlaceholderPage title="Harness Library" frRange="FR-APP-040..041" builtIn="TS-APP-UI-004" />`, no data fetching | **REPLACE** | `TS-APP-UI-001` §7 names this spec as the exact owner of this route |
| `api/types.ts` (from `TS-APP-UI-001`) | `apps/web/src/api/types.ts` | Exports `HealthResponse`/`ServiceHealthItem`/`ErrorResponse`/WS message union; re-exports Studio domain types; no Harness types | **EXTEND, ADDITIVE ONLY** | New interfaces appended below the existing exports, same "keep in sync" comment convention, zero edits to existing lines |
| `api/http.ts` / `api/ApiError.ts` / `api/queryClient.ts` (from `TS-APP-UI-001`) | `apps/web/src/api/` | `apiFetch<T>`, typed `ApiError`, one shared `QueryClient` | **REUSE, UNMODIFIED** | Every hook in this spec calls `apiFetch` exactly the way `useHealth` already does |
| `components/ui/{Card,Badge,StatusPill,Button}.tsx` (from `TS-APP-UI-001`) | `apps/web/src/components/ui/` | Small, token-driven presentational primitives | **REUSE, UNMODIFIED** | `Card` wraps every `HarnessCard`'s outer shell; `Badge` is the base every Mode/Category/Certification/Eligibility badge composes; `Button` is reused for filter-bar controls |
| `services/studio/src/domain.ts` | `services/studio/src/` | `CampaignOrder`, `ControlTowerProjection`, etc. | **NOT CONSUMED** | A Harness is a Builder/Pipeline concept, not a Studio domain object; nothing in this spec imports `@ca/studio/*` |
| `api/routers/harnesses.py` (`TS-APP-API-002`) | `api/routers/harnesses.py` | Four routes: list, detail, build, eligibility | **REUSE, UNMODIFIED (consumed only)** | This spec adds zero backend code; `POST /api/harnesses/build` specifically has no UI consumer here (see Section 2, Out of scope) |
| `cmf_builder/domain/category_binding.py` | `services/builder/src/cmf_builder/domain/` | Five canonical categories; `canonical_dict()` / `portable_projection()` | **REUSE (read-only, via the API response body)** | Never imported by the frontend directly; its exact category id/name pairs are hand-copied into `CANONICAL_CATEGORIES` (Section 6) because the frontend has no Python import path, and its two-shape `category_binding` output informs the `CategoryBindingDetail` union |
| `THE_CMF_STUDIO(2)/operator-web` (archived reference) | `archive/experiments/cmf-studio-v2/` (post-restructure) | 1,210-line static demo, no router, no API calls | **NOT CONSULTED** | `TS-APP-UI-001` §4 already confirmed this directory contains no Harness-related UI; not re-checked here |

---

## 5. Proposed Architecture and Workflows

### Browse flow — `/harnesses`

```
Operator navigates to /harnesses
  (optionally with ?category=&mode=&q=&sourceCategory= already in the URL)
  → useHarnesses(): useQuery(["harnesses"],
      () => apiFetch<HarnessSummary[]>("/api/harnesses"))
  → outcome:
      isLoading           → HarnessCardGridSkeleton (fixed number of placeholder cards)
      isError              → HarnessLibraryErrorState
                              (distinguishes ApiError.status === null, "gateway unreachable,"
                              from a real 5xx LIBRARY_UNREADABLE response — never the same
                              message for both)
      data.length === 0    → HarnessLibraryEmptyState
                              ("No Harnesses in this workspace's library yet — these are
                              built by the Pi Coding Agent via POST /api/harnesses/build,
                              not authored here.")
      data.length > 0      → client-side filter over `data`, driven by the URL search params
                              (category / mode / q — exact-match category+mode,
                              case-insensitive substring match on task_id OR manifest_id
                              for q) → HarnessFilterBar + a grid of HarnessCard
  → each HarnessCard renders:
      - ModeBadge(mode)
      - CategoryBadge(category_name)  — "Category-neutral" when category_name is null
      - CertificationBadges(production_ready, certified)  — always visible, always honest
      - capability_requirements as a truncated tag list (first 3, "+N more" beyond that)
      - IF search.sourceCategory is set:
          EligibilityBadge(computeEligibilityPreview(harness, search.sourceCategory))
          — pure function, zero network call (Section 6)
      - onClick → <Link to="/harnesses/$definitionId"
                        params={{ definitionId: harness.definition_id }}
                        search={(prev) => prev} />
                  (preserves sourceCategory, and any other active filter, across navigation)
```

### Detail flow — `/harnesses/$definitionId`

```
Operator navigates to /harnesses/$definitionId
  (optionally carrying ?sourceCategory= forwarded from the list page's Link)
  → useHarnessDetail(definitionId): useQuery(["harnesses", definitionId],
      () => apiFetch<HarnessDetail>(`/api/harnesses/${definitionId}`))
  → outcome:
      isLoading                        → detail-page skeleton
      isError && error.status === 404   → HarnessNotFoundPanel + a Link back to /harnesses
      isError (anything else)           → HarnessLibraryErrorState (reused from list page)
      success                           → full render:
          - header: task_id, manifest_id + manifest_version, ModeBadge, CategoryBadge,
            CertificationBadges
          - "What this Harness does": goal, success_condition, atomic_boundary (prose)
          - ContractPanel: input_contract / output_contract — these are JSON Schema
            fragments, rendered as a collapsible, pretty-printed JSON block, not free text
          - tag lists: capability_requirements, acceptance_tests, minimum_complete_context
          - GovernancePanel: category_binding, rendered via the discriminated union
            (Section 6) —
              applicability === "NOT_APPLICABLE" → shows only `basis` ("Harness is
                category-neutral (generic mode).")
              applicability === "REQUIRED"        → shows the full governance record:
                runtime_law, harness_development_law, certification_state,
                wrong_reading_locks, semantic_lineage_refs, category_registry_version/hash,
                constitutional_authority_ref, binding_hash
          - lineage, compiler_id/version, schema_id/version, package_file/package_hash
            shown as inspectable metadata only (no download action)
  → IF search.sourceCategory is present AND detail.mode === "activative":
      useHarnessEligibility(definitionId, sourceCategory) fires — the one real backend call
      this spec makes beyond list/detail:
        GET /api/harnesses/{id}/eligibility?source_category=<sourceCategory>
      → renders the authoritative EligibilityResponse (status + reason text) next to the
        header badge, superseding the client-computed preview the list page showed
  → IF search.sourceCategory is present AND detail.mode === "generic":
      no network call is made — NOT_APPLICABLE is rendered directly and immediately,
      because that is exactly what the server itself would answer (TS-APP-API-002 §5),
      and firing the request anyway would violate the "never fetch what you already know"
      decision in Section 3
```

---

## 6. Data Models, Contracts, Schemas, and APIs

### `CanonicalCategoryId` and `CANONICAL_CATEGORIES` (from `cmf_builder/domain/category_binding.py`, read directly — Section 1)

```typescript
// apps/web/src/api/types.ts

export type CanonicalCategoryId =
  | "short_form_edited_video"
  | "2d_character_animation"
  | "carousels"
  | "supervisuals"
  | "conversational_activation_expression";

export const CANONICAL_CATEGORIES: ReadonlyArray<{
  readonly id: CanonicalCategoryId;
  readonly label: string;
}> = [
  { id: "short_form_edited_video", label: "Short-Form Edited Video" },
  { id: "2d_character_animation", label: "2D Character Animation" },
  { id: "carousels", label: "Carousels" },
  { id: "supervisuals", label: "Supervisuals" },
  {
    id: "conversational_activation_expression",
    label: "Conversational Activation / Human Expression",
  },
];

export type HarnessMode = "generic" | "activative";
```

### `HarnessSummary` (mirrors `TS-APP-API-002` §6 exactly — keep in sync)

```typescript
export interface HarnessSummary {
  readonly definition_id: string;
  readonly definition_hash: string;
  readonly manifest_id: string;
  readonly manifest_version: string;
  readonly task_id: string;
  readonly mode: HarnessMode;
  readonly category_id: CanonicalCategoryId | null;
  readonly category_name: string | null;
  readonly classification: ReadonlyArray<string>;
  readonly capability_requirements: ReadonlyArray<string>;
  readonly production_ready: boolean;   // always false today — never hidden or restyled
  readonly certified: boolean;          // always false today — never hidden or restyled
  readonly package_file: string;
  readonly package_hash: string;
  readonly added_at: string | null;     // RFC 3339, non-authoritative (file mtime), display only
}
```

### `CategoryBindingDetail` — discriminated union (derived directly from `CategoryBinding.canonical_dict()` vs `.portable_projection()`, Section 1; **not** modeled this precisely in `TS-APP-API-002` §6, which types the field as a bare `dict`)

```typescript
export type CategoryBindingDetail =
  | {
      readonly applicability: "NOT_APPLICABLE";
      readonly basis: string | null;
      readonly category_id: null;
    }
  | {
      readonly applicability: "REQUIRED";
      readonly harness_id: string;
      readonly harness_version: string;
      readonly category_id: CanonicalCategoryId;
      readonly category_name: string;
      readonly category_registry_version: string;
      readonly category_registry_hash: string;
      readonly constitutional_authority_ref: string;
      readonly runtime_law: string;
      readonly harness_development_law: string;
      readonly semantic_lineage_refs: ReadonlyArray<string>;
      readonly wrong_reading_locks: ReadonlyArray<string>;
      readonly not_applicable_basis: null;
      readonly certification_state: string;
      readonly production_ready: boolean;
      readonly certified: boolean;
      readonly binding_hash: string;
    };
```

`GovernancePanel` (Section 7) discriminates purely on `applicability`; no other field is assumed present until that check passes.

### `HarnessDetail` — extends `HarnessSummary` (mirrors `TS-APP-API-002` §6 exactly — keep in sync)

```typescript
export interface HarnessDetail extends HarnessSummary {
  readonly goal: string;
  readonly success_condition: string;
  readonly atomic_boundary: string;
  readonly input_contract: Record<string, unknown>;   // JSON Schema fragment
  readonly output_contract: Record<string, unknown>;  // JSON Schema fragment
  readonly minimum_complete_context: ReadonlyArray<string>;
  readonly acceptance_tests: ReadonlyArray<string>;
  readonly authority_chain: ReadonlyArray<string>;
  readonly provenance_refs: ReadonlyArray<string>;
  readonly execution_plan: ReadonlyArray<string>;
  readonly category_binding: CategoryBindingDetail;
  readonly activative_intelligence: Record<string, unknown> | null;
  readonly lineage: ReadonlyArray<string>;
  readonly compiler_id: string;
  readonly compiler_version: string;
  readonly schema_id: string;
  readonly schema_version: string;
}
```

### `EligibilityResponse` (mirrors `TS-APP-API-002` §6 exactly — keep in sync)

```typescript
export type EligibilityStatus = "ELIGIBLE" | "INELIGIBLE" | "NOT_APPLICABLE";

export interface EligibilityResponse {
  readonly definition_id: string;
  readonly harness_category: CanonicalCategoryId | null;
  readonly source_category: string;
  readonly status: EligibilityStatus;
  readonly reason: string | null;
}
```

### `computeEligibilityPreview` — the zero-network client mirror of `TS-APP-API-002` §5's eligibility flow

```typescript
// apps/web/src/lib/harnessEligibility.ts
import type { EligibilityStatus, HarnessMode, CanonicalCategoryId } from "../api/types";

interface EligibilityPreviewInput {
  readonly mode: HarnessMode;
  readonly category_id: CanonicalCategoryId | null;
}

/**
 * Mirrors the server's own branching in TS-APP-API-002 §5 exactly, using only fields
 * already present on HarnessSummary. Returns null when no sourceCategory context was
 * supplied — the caller renders no badge at all in that case, not a default status.
 */
export function computeEligibilityPreview(
  harness: EligibilityPreviewInput,
  sourceCategory: string | undefined,
): EligibilityStatus | null {
  if (!sourceCategory) return null;
  if (harness.mode === "generic") return "NOT_APPLICABLE";
  return harness.category_id === sourceCategory ? "ELIGIBLE" : "INELIGIBLE";
}
```

### URL search params — `apps/web/src/routes/harnesses/index.tsx`

```typescript
export interface HarnessLibrarySearch {
  readonly category?: CanonicalCategoryId;
  readonly mode?: HarnessMode;
  readonly q?: string;
  readonly sourceCategory?: string;
}

function validateSearch(search: Record<string, unknown>): HarnessLibrarySearch {
  const categoryIds = new Set(CANONICAL_CATEGORIES.map((c) => c.id));
  return {
    category:
      typeof search.category === "string" && categoryIds.has(search.category as CanonicalCategoryId)
        ? (search.category as CanonicalCategoryId)
        : undefined,
    mode:
      search.mode === "generic" || search.mode === "activative" ? search.mode : undefined,
    q: typeof search.q === "string" && search.q.length > 0 ? search.q : undefined,
    sourceCategory: typeof search.sourceCategory === "string" ? search.sourceCategory : undefined,
  };
}
```

An unrecognized or malformed `sourceCategory` (not one of the five canonical ids) is **not** rejected by `validateSearch` — it is passed through as-is. `computeEligibilityPreview` and the server's own eligibility route both handle that case safely and identically: the equality check simply never matches any real `category_id`, so every activative Harness reports `INELIGIBLE` and every generic Harness still reports `NOT_APPLICABLE`. No special-cased client validation is needed for this because the comparison is trivially safe either way.

### Route table this spec produces

| Path | Component | Network calls |
|---|---|---|
| `/harnesses` | `HarnessLibraryRoute` (replaces `TS-APP-UI-001`'s placeholder) | `GET /api/harnesses` (once, via `useHarnesses`) |
| `/harnesses/$definitionId` | `HarnessDetailRoute` (new) | `GET /api/harnesses/{id}` (once, via `useHarnessDetail`); `GET /api/harnesses/{id}/eligibility?source_category=` (only if `search.sourceCategory` is set **and** `detail.mode === "activative"`, via `useHarnessEligibility`) |

---

## 7. Implementation Stages and Exact Target Paths

All paths are relative to the repository root, after the `CA_APP_FR_EPIC_SPEC_PLAN.md` Part 5 restructure and after `TS-APP-UI-001`'s scaffold already exist.

### Stage 1 — Types

Append to `apps/web/src/api/types.ts` (existing exports untouched): `CanonicalCategoryId`, `CANONICAL_CATEGORIES`, `HarnessMode`, `HarnessSummary`, `CategoryBindingDetail`, `HarnessDetail`, `EligibilityStatus`, `EligibilityResponse` — all as specified in full in Section 6.

### Stage 2 — Pure eligibility preview

**`apps/web/src/lib/harnessEligibility.ts`** — `computeEligibilityPreview`, as specified in full in Section 6.

### Stage 3 — Hooks

**`apps/web/src/hooks/useHarnesses.ts`**
```typescript
import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "../api/http";
import type { HarnessSummary } from "../api/types";

export function useHarnesses() {
  return useQuery({
    queryKey: ["harnesses"],
    queryFn: () => apiFetch<HarnessSummary[]>("/api/harnesses"),
  });
}
```

**`apps/web/src/hooks/useHarnessDetail.ts`**
```typescript
import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "../api/http";
import type { HarnessDetail } from "../api/types";

export function useHarnessDetail(definitionId: string) {
  return useQuery({
    queryKey: ["harnesses", definitionId],
    queryFn: () => apiFetch<HarnessDetail>(`/api/harnesses/${definitionId}`),
  });
}
```

**`apps/web/src/hooks/useHarnessEligibility.ts`**
```typescript
import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "../api/http";
import type { EligibilityResponse } from "../api/types";

export function useHarnessEligibility(
  definitionId: string,
  sourceCategory: string | undefined,
  mode: "generic" | "activative",
) {
  return useQuery({
    queryKey: ["harnesses", definitionId, "eligibility", sourceCategory],
    queryFn: () =>
      apiFetch<EligibilityResponse>(
        `/api/harnesses/${definitionId}/eligibility?source_category=${encodeURIComponent(sourceCategory!)}`,
      ),
    // Never fires for generic-mode Harnesses or with no sourceCategory context — see
    // Section 3, "never fetch what you already know."
    enabled: Boolean(sourceCategory) && mode === "activative",
  });
}
```

### Stage 4 — Badge primitives

**`apps/web/src/components/harness/ModeBadge.tsx`**
```tsx
import { Badge } from "../ui/Badge";
import type { HarnessMode } from "../../api/types";

export function ModeBadge({ mode }: { mode: HarnessMode }) {
  return (
    <Badge tone={mode === "activative" ? "accent" : "muted"}>
      {mode === "activative" ? "Activative" : "Generic"}
    </Badge>
  );
}
```

**`apps/web/src/components/harness/EligibilityBadge.tsx`**
```tsx
import { Badge } from "../ui/Badge";
import type { EligibilityStatus } from "../../api/types";

const TONE: Record<EligibilityStatus, "success" | "danger" | "muted"> = {
  ELIGIBLE: "success",
  INELIGIBLE: "danger",
  NOT_APPLICABLE: "muted",
};

const LABEL: Record<EligibilityStatus, string> = {
  ELIGIBLE: "Eligible",
  INELIGIBLE: "Not eligible",
  NOT_APPLICABLE: "Category-neutral",
};

export function EligibilityBadge({ status }: { status: EligibilityStatus }) {
  return <Badge tone={TONE[status]}>{LABEL[status]}</Badge>;
}
```

**`CategoryBadge.tsx`** and **`CertificationBadges.tsx`** follow the same shape (each under 30 lines, omitted here for length, required by AC-001/AC-007): `CategoryBadge` renders `category_name ?? "Category-neutral"` in a muted tone; `CertificationBadges` renders two always-visible, always-muted-tone badges for `production_ready` and `certified` — never a green/success tone for either, per the Section 3 governing decision.

### Stage 5 — `HarnessCard.tsx`

**`apps/web/src/components/harness/HarnessCard.tsx`**
```tsx
import { Link } from "@tanstack/react-router";
import { Card } from "../ui/Card";
import { ModeBadge } from "./ModeBadge";
import { CategoryBadge } from "./CategoryBadge";
import { CertificationBadges } from "./CertificationBadges";
import { EligibilityBadge } from "./EligibilityBadge";
import { computeEligibilityPreview } from "../../lib/harnessEligibility";
import type { HarnessSummary } from "../../api/types";

const CAPABILITY_PREVIEW_COUNT = 3;

export function HarnessCard({
  harness,
  sourceCategory,
}: {
  readonly harness: HarnessSummary;
  readonly sourceCategory: string | undefined;
}) {
  const preview = computeEligibilityPreview(harness, sourceCategory);
  const extraCapabilities = harness.capability_requirements.length - CAPABILITY_PREVIEW_COUNT;

  return (
    <Link
      to="/harnesses/$definitionId"
      params={{ definitionId: harness.definition_id }}
      search={(prev) => prev}
      className="block"
    >
      <Card>
        <div className="flex items-center justify-between gap-2">
          <h3 className="font-semibold text-foreground">{harness.task_id}</h3>
          {preview !== null && <EligibilityBadge status={preview} />}
        </div>
        <p className="text-sm text-muted-foreground">
          {harness.manifest_id} · v{harness.manifest_version}
        </p>
        <div className="mt-2 flex flex-wrap gap-1">
          <ModeBadge mode={harness.mode} />
          <CategoryBadge categoryName={harness.category_name} />
        </div>
        <CertificationBadges
          productionReady={harness.production_ready}
          certified={harness.certified}
        />
        <div className="mt-2 flex flex-wrap gap-1 text-xs text-muted-foreground">
          {harness.capability_requirements.slice(0, CAPABILITY_PREVIEW_COUNT).map((cap) => (
            <span key={cap} className="rounded border border-border px-1.5 py-0.5">
              {cap}
            </span>
          ))}
          {extraCapabilities > 0 && <span>+{extraCapabilities} more</span>}
        </div>
      </Card>
    </Link>
  );
}
```

### Stage 6 — `HarnessFilterBar.tsx`

**`apps/web/src/components/harness/HarnessFilterBar.tsx`** — reads and writes `category`, `mode`, and `q` via `useSearch({ from: "/harnesses/" })` and `useNavigate({ from: "/harnesses/" })`; three controls (a category `<select>` seeded from `CANONICAL_CATEGORIES` plus a "Category-neutral" option, a mode toggle, and a debounced text input for `q`), each writing back into the URL search params on change rather than local state, consistent with Section 3. Omitted in full here for length (required by AC-004/AC-005); under 80 lines.

### Stage 7 — Empty and error states

**`HarnessLibraryEmptyState.tsx`** — shown only when `data.length === 0` (a successful, empty response — never conflated with an error): explains that Harnesses are built by the Pi Coding Agent via `POST /api/harnesses/build`, not authored in this UI (Section 2, Out of scope).

**`HarnessLibraryErrorState.tsx`** — shown on `isError`; branches its message on `error.status === null` ("gateway unreachable — is the API running?") versus a real HTTP status ("the harness library could not be read"), reusing the `ApiError` shape from `TS-APP-UI-001` exactly as `TopBar` already does for `/api/health`.

**`HarnessNotFoundPanel.tsx`** — shown when `useHarnessDetail`'s error has `status === 404`; a short message plus a `<Link to="/harnesses">` back to the grid.

### Stage 8 — `routes/harnesses/index.tsx` (replaces the `TS-APP-UI-001` placeholder)

```tsx
import { createFileRoute } from "@tanstack/react-router";
import { useHarnesses } from "../../hooks/useHarnesses";
import { HarnessFilterBar } from "../../components/harness/HarnessFilterBar";
import { HarnessCard } from "../../components/harness/HarnessCard";
import { HarnessLibraryEmptyState } from "../../components/harness/HarnessLibraryEmptyState";
import { HarnessLibraryErrorState } from "../../components/harness/HarnessLibraryErrorState";
import type { HarnessLibrarySearch } from "../../api/types";
import { validateSearch } from "./-validateHarnessSearch"; // co-located, see Section 6

export const Route = createFileRoute("/harnesses/")({
  validateSearch,
  component: HarnessLibraryPage,
});

function HarnessLibraryPage() {
  const search = Route.useSearch();
  const { data, isLoading, isError, error } = useHarnesses();

  if (isError) return <HarnessLibraryErrorState error={error} />;
  if (isLoading) return <div className="p-8 text-muted-foreground">Loading harnesses…</div>;
  if (data.length === 0) return <HarnessLibraryEmptyState />;

  const filtered = data.filter((h) => {
    if (search.category && h.category_id !== search.category) return false;
    if (search.mode && h.mode !== search.mode) return false;
    if (search.q) {
      const needle = search.q.toLowerCase();
      if (!h.task_id.toLowerCase().includes(needle) && !h.manifest_id.toLowerCase().includes(needle)) {
        return false;
      }
    }
    return true;
  });

  return (
    <div className="p-8">
      <h1 className="text-2xl font-semibold text-foreground">Harness Library</h1>
      <HarnessFilterBar />
      <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filtered.map((harness) => (
          <HarnessCard key={harness.definition_id} harness={harness} sourceCategory={search.sourceCategory} />
        ))}
      </div>
    </div>
  );
}
```

`HarnessLibrarySearch` (Section 6) is declared once in `api/types.ts`; `validateSearch` is a small, co-located, non-exported route file (`-validateHarnessSearch.ts`, TanStack Router's convention for a file that participates in a route without itself being a route) so it is trivially unit-testable in isolation from the component (Section 10).

### Stage 9 — `routes/harnesses/$definitionId.tsx` (new)

```tsx
import { createFileRoute, Link } from "@tanstack/react-router";
import { useHarnessDetail } from "../../hooks/useHarnessDetail";
import { useHarnessEligibility } from "../../hooks/useHarnessEligibility";
import { ModeBadge } from "../../components/harness/ModeBadge";
import { CategoryBadge } from "../../components/harness/CategoryBadge";
import { CertificationBadges } from "../../components/harness/CertificationBadges";
import { EligibilityBadge } from "../../components/harness/EligibilityBadge";
import { ContractPanel } from "../../components/harness/ContractPanel";
import { GovernancePanel } from "../../components/harness/GovernancePanel";
import { HarnessNotFoundPanel } from "../../components/harness/HarnessNotFoundPanel";
import { HarnessLibraryErrorState } from "../../components/harness/HarnessLibraryErrorState";

export const Route = createFileRoute("/harnesses/$definitionId")({
  component: HarnessDetailPage,
});

function HarnessDetailPage() {
  const { definitionId } = Route.useParams();
  const { sourceCategory } = Route.useSearch() as { sourceCategory?: string };
  const { data, isLoading, isError, error } = useHarnessDetail(definitionId);
  const eligibility = useHarnessEligibility(definitionId, sourceCategory, data?.mode ?? "generic");

  if (isError && error.status === 404) return <HarnessNotFoundPanel />;
  if (isError) return <HarnessLibraryErrorState error={error} />;
  if (isLoading || !data) return <div className="p-8 text-muted-foreground">Loading…</div>;

  return (
    <div className="p-8">
      <Link to="/harnesses" search={(prev) => prev} className="text-sm text-accent">
        ← Back to library
      </Link>
      <div className="mt-2 flex items-center gap-2">
        <h1 className="text-2xl font-semibold text-foreground">{data.task_id}</h1>
        <ModeBadge mode={data.mode} />
        <CategoryBadge categoryName={data.category_name} />
        {sourceCategory && data.mode === "generic" && <EligibilityBadge status="NOT_APPLICABLE" />}
        {eligibility.data && <EligibilityBadge status={eligibility.data.status} />}
      </div>
      {eligibility.data?.reason && (
        <p className="mt-1 text-sm text-muted-foreground">{eligibility.data.reason}</p>
      )}
      <CertificationBadges productionReady={data.production_ready} certified={data.certified} />

      <section className="mt-6">
        <h2 className="font-semibold text-foreground">What this Harness does</h2>
        <p className="text-sm">{data.goal}</p>
        <p className="mt-2 text-sm text-muted-foreground">Success condition: {data.success_condition}</p>
        <p className="mt-2 text-sm text-muted-foreground">Atomic boundary: {data.atomic_boundary}</p>
      </section>

      <ContractPanel input={data.input_contract} output={data.output_contract} />
      <GovernancePanel binding={data.category_binding} />
    </div>
  );
}
```

**`ContractPanel.tsx`** — renders `input_contract`/`output_contract` as two collapsible, pretty-printed (`JSON.stringify(value, null, 2)`) `<pre>` blocks; under 40 lines.

**`GovernancePanel.tsx`** — the `CategoryBindingDetail` discriminated-union consumer described in Section 5/6: switches on `binding.applicability`; `"NOT_APPLICABLE"` renders only `basis`; `"REQUIRED"` renders the full 14-field record as a labeled definition list. Under 60 lines.

### Stage 10 — Test harness

**`apps/web/src/test/renderWithRouter.tsx`** — new, shared utility: wraps a component tree in a TanStack Router `RouterProvider` backed by a memory history and a given starting URL (including search params), so route-level tests (Section 10) can assert on filtered/linked behavior without a real browser. This is the first spec in this project to need URL-search-param-aware route tests; later specs (e.g. `TS-APP-UI-002`'s `CampaignNew`) can reuse this same helper instead of re-inventing one.

---

## 8. Failure, Migration, Rollback, Recovery, and Observability

### Failure modes handled

| Failure | Where handled | Behaviour |
|---|---|---|
| `GET /api/harnesses` returns `LIBRARY_UNREADABLE` (5xx) | `useHarnesses` → `isError` | `HarnessLibraryErrorState`, explicitly distinct wording from the empty-list case — an empty library and an unreadable library must never look the same to the operator |
| Gateway not running at all | `apiFetch` throws `ApiError(status: null)` (reused from `TS-APP-UI-001`) | `HarnessLibraryErrorState` shows "gateway unreachable" specifically, not a generic error |
| `GET /api/harnesses/{id}` returns `404` | `useHarnessDetail` → `error.status === 404` | `HarnessNotFoundPanel` + a `Link` back to `/harnesses`, never an unhandled crash |
| `GET /api/harnesses/{id}/eligibility` fails (e.g. the definition vanished from the library between page load and this call — a genuine race, since the two calls are not atomic) | `useHarnessEligibility` | The eligibility panel is silently omitted; the rest of the already-successfully-loaded `HarnessDetail` still renders in full — one subsystem's failure does not blank the page |
| `?sourceCategory=` in the URL is not one of the five canonical ids | `computeEligibilityPreview` / the server's own eligibility route | Falls through to `INELIGIBLE` for every activative Harness (no id will ever match), exactly matching what the real server route would also compute — no special client-side validation is required because the comparison is safe by construction |
| Very large `capability_requirements` / `semantic_lineage_refs` / `wrong_reading_locks` arrays | `HarnessCard` (truncates with "+N more") / `GovernancePanel` (never truncates — the detail page is where the full list belongs) | Card stays a fixed, scannable size; nothing is ever silently dropped, only deferred to the detail page |
| A malformed `category`/`mode` value is hand-typed into the URL | `validateSearch` | Silently discarded (returns `undefined` for that field) rather than crashing the route loader or applying a nonsense filter |

### Migration / rollback
This spec only adds new files and appends new, non-overlapping exports to `apps/web/src/api/types.ts`; it replaces exactly one existing file (`routes/harnesses/index.tsx`) whose entire prior content was a placeholder `TS-APP-UI-001` itself designated for replacement here. Rollback is `git revert` of this spec's commit(s). No data migration exists at this layer — this spec introduces no persistent client-side state.

### Observability
- TanStack Query devtools (already mounted dev-only by `TS-APP-UI-001`) show the `["harnesses"]`, `["harnesses", definitionId]`, and `["harnesses", definitionId, "eligibility", sourceCategory]` query keys live, including cache status and last-fetch time
- No new logging, metrics, or external monitoring is wired in this spec, matching `TS-APP-UI-001`'s own observability scope at this wave

---

## 9. Acceptance Criteria

**AC-001 — Library lists real Harnesses**
Given at least one exported `AtomicHarnessDefinition` package exists in the library (per `TS-APP-API-002` AC-002/AC-003),
When an operator navigates to `/harnesses`,
Then a `HarnessCard` renders for every item `GET /api/harnesses` returned, each showing its `task_id`, mode, category (or "Category-neutral"), and certification badges.
Failure example: the grid renders only the first page of a paginated response that does not actually exist (`GET /api/harnesses` returns the full list in one call — there is no pagination to mis-handle, but a client-side `slice()` bug could still truncate the render).
Evidence: rendered card count equals response array length.
Test layer: component (mocked `apiFetch`) — `apps/web/src/routes/harnesses/index.test.tsx`.

**AC-002 — Empty library shows the empty state, never the error state**
Given `GET /api/harnesses` returns `200 []`,
When the list route renders,
Then `HarnessLibraryEmptyState` is shown, and `HarnessLibraryErrorState` is not.
Failure example: an empty array is treated as falsy and routed into the same branch as a fetch failure.
Evidence: DOM assertion — empty-state copy present, error-state copy absent.
Test layer: component — `apps/web/src/routes/harnesses/index.test.tsx`.

**AC-003 — `LIBRARY_UNREADABLE` renders a distinct error state**
Given `GET /api/harnesses` returns a 5xx `ErrorResponse`,
When the list route renders,
Then `HarnessLibraryErrorState` is shown with wording distinct from both the empty state and the "gateway unreachable" (`status: null`) case.
Failure example: a caught `ApiError` is rendered with the same generic "something went wrong" text regardless of `status`, losing the empty-vs-unreadable-vs-unreachable distinction Section 8 requires.
Evidence: DOM assertion per case — three different message strings for three different `useHarnesses()` mock outcomes.
Test layer: component — `apps/web/src/routes/harnesses/index.test.tsx`.

**AC-004 — Category and mode filters narrow the grid via URL search params**
Given the library contains Harnesses of more than one category and mode,
When an operator sets the category filter to `carousels`,
Then only `HarnessCard`s with `category_id === "carousels"` remain visible, and the URL updates to include `?category=carousels`; reloading that URL directly reproduces the same filtered view with no user interaction.
Failure example: filter state lives only in `useState` and is lost on reload, or on the browser back button.
Evidence: rendered card count before/after; URL string assertion; a direct-navigation test using `renderWithRouter` (Stage 10) starting from the filtered URL.
Test layer: component + routing — `apps/web/src/routes/harnesses/index.test.tsx`.

**AC-005 — Free-text search matches `task_id` or `manifest_id`, case-insensitively**
Given a Harness with `task_id: "generic_text_summary_v1"`,
When the operator types `"SUMMARY"` into the search field,
Then that card remains visible and cards with neither field containing the (case-folded) substring are hidden.
Failure example: the search only checks `task_id`, silently missing a match that exists only in `manifest_id`.
Evidence: rendered card set before/after typing.
Test layer: component — `apps/web/src/components/harness/HarnessFilterBar.test.tsx`.

**AC-006 — Clicking a card navigates to the detail route and preserves `sourceCategory`**
Given the operator is at `/harnesses?sourceCategory=carousels`,
When they click any `HarnessCard`,
Then the browser navigates to `/harnesses/{definitionId}?sourceCategory=carousels` — the query parameter is carried over, not dropped.
Failure example: the `Link`'s `search` prop is hardcoded to `{}` instead of `(prev) => prev`, silently losing the parameter on every card click.
Evidence: resulting URL assertion after a simulated click.
Test layer: component + routing — `apps/web/src/components/harness/HarnessCard.test.tsx`.

**AC-007 — Detail route renders the full `HarnessDetail` contract**
Given a valid `definition_id`,
When the detail route loads successfully,
Then `goal`, `success_condition`, `atomic_boundary`, both contracts (`ContractPanel`), and the governance record (`GovernancePanel`) are all present in the rendered output — not a subset.
Failure example: `capability_requirements` (already on the summary) is shown but `minimum_complete_context` (detail-only) is silently omitted because a component was copy-pasted from `HarnessCard`.
Evidence: DOM assertion per field/section.
Test layer: component — `apps/web/src/routes/harnesses/$definitionId.test.tsx`.

**AC-008 — Unknown `definitionId` shows a 404 panel, not a crash**
Given `GET /api/harnesses/{id}` returns `404`,
When the detail route renders,
Then `HarnessNotFoundPanel` is shown with a working `Link` back to `/harnesses`, and no unhandled exception reaches `RootErrorBoundary`.
Failure example: the component assumes `data` is defined once `isLoading` is `false`, throwing on `data.task_id` when `data` is actually `undefined` after a 404.
Evidence: DOM assertion — not-found copy present, back-link present, no thrown error.
Test layer: component — `apps/web/src/routes/harnesses/$definitionId.test.tsx`.

**AC-009 — Client-computed eligibility preview is correct with zero extra network calls**
Given a `sourceCategory` is present in the URL and the library contains at least one `ELIGIBLE`, one `INELIGIBLE`, and one `NOT_APPLICABLE` case,
When the list route renders,
Then every card shows the correct `EligibilityBadge`, and no request to `GET /api/harnesses/{id}/eligibility` is made by the list page for any of them.
Failure example: the list page calls `useHarnessEligibility` per card "just to be safe," reintroducing the N+1 pattern Section 3 explicitly rejects.
Evidence: badge text/tone per card; mock `fetch` call count for the eligibility path is exactly zero on the list route.
Test layer: component — `apps/web/src/routes/harnesses/index.test.tsx`; pure-function unit coverage of all branches — `apps/web/src/lib/harnessEligibility.test.ts`.

**AC-010 — Detail page's authoritative eligibility call fires only when it should**
Given the detail route is visited (a) with a `sourceCategory` on an activative Harness, (b) with a `sourceCategory` on a generic Harness, (c) with no `sourceCategory` at all,
When the page renders in each case,
Then `GET /api/harnesses/{id}/eligibility` is called only in case (a); case (b) renders `NOT_APPLICABLE` immediately with zero calls; case (c) renders no eligibility UI at all.
Failure example: the `enabled` condition on `useHarnessEligibility` checks only `Boolean(sourceCategory)`, firing an avoidable request for every generic-mode Harness too.
Evidence: mock `fetch` call count per case.
Test layer: component (mocked `apiFetch`) — `apps/web/src/routes/harnesses/$definitionId.test.tsx`.

**AC-011 — No modification to existing service packages or API routers**
Given the Phase-09 Python test suite, `services/studio`'s own test suite, and `TS-APP-UI-001`'s own web test suite were all passing before this spec,
When this spec is fully implemented,
Then `git diff` shows zero changes under `services/**`, `api/**` (beyond `apps/web/**`), or any Python package directory, and all three pre-existing suites still pass unmodified.
Failure example: a developer "just quickly" adds a `profile_id` field to `HarnessSummary` on the Python side to make a planned-but-not-yet-built filter easier, contradicting this spec's explicit read-only scope.
Evidence: `git diff --stat` outside `apps/web/`; pytest output; `node --test` output; `apps/web` pre-existing Vitest output.
Test layer: regression.

---

## 10. Testing and Completion Evidence

### Test files to create

- **`apps/web/src/lib/harnessEligibility.test.ts`** — all six `(mode, category match)` branch combinations for `computeEligibilityPreview`, plus the `sourceCategory === undefined` → `null` case — AC-009
- **`apps/web/src/hooks/useHarnesses.test.ts`** — loading / empty / error / success states, mocked `apiFetch` — AC-001, AC-002, AC-003
- **`apps/web/src/hooks/useHarnessDetail.test.ts`** — success / 404 / other-error states — AC-007, AC-008
- **`apps/web/src/hooks/useHarnessEligibility.test.ts`** — `enabled` gating across the three cases in AC-010
- **`apps/web/src/components/harness/HarnessCard.test.tsx`** — renders expected badges/tags; `Link` preserves search params — AC-006, AC-009
- **`apps/web/src/components/harness/HarnessFilterBar.test.tsx`** — category/mode/search interactions update the URL — AC-004, AC-005
- **`apps/web/src/routes/harnesses/index.test.tsx`** — full-page composition across all `useHarnesses` outcomes, filter interactions, direct-navigation-with-search-params via `renderWithRouter` — AC-001 through AC-004, AC-009
- **`apps/web/src/routes/harnesses/$definitionId.test.tsx`** — full-page composition across all `useHarnessDetail`/`useHarnessEligibility` outcome combinations — AC-007, AC-008, AC-010
- **`apps/web/src/test/renderWithRouter.tsx`** — shared test utility, not itself a test file, described in Section 7 Stage 10

### Test tooling
Reuses Vitest + Testing Library exactly as pinned by `TS-APP-UI-001` (`apps/web/package.json` devDependencies) — no new testing dependency is introduced. `apiFetch`/`fetch` is mocked at the module boundary the same way `useHealth.test.ts` already does in `TS-APP-UI-001`.

```typescript
// apps/web/src/routes/harnesses/index.test.tsx (excerpt)
import { renderWithRouter } from "../../test/renderWithRouter";

test("empty library shows the empty state, not the error state", async () => {
  vi.spyOn(global, "fetch").mockResolvedValue(
    new Response(JSON.stringify([]), { status: 200 }),
  );
  const { findByText, queryByText } = renderWithRouter("/harnesses");
  expect(await findByText(/no harnesses in this workspace/i)).toBeInTheDocument();
  expect(queryByText(/could not be read/i)).not.toBeInTheDocument();
});
```

### Pre-existing regression
Run before and after implementing this spec:
```bash
python -m pytest tests/ -q --tb=short
node --test services/studio/tests/*.test.mjs
npm run test --workspace=apps/web
```
Zero new failures in any of the three is a hard gate (AC-011).

### Build Receipt claim ceiling
`HARNESS_LIBRARY_UI_DEVELOPMENT_EVIDENCE`

This spec does not claim:
- Pipeline-execution readiness for any Harness it displays (inherited from `TS-APP-API-002` Gap 4 — unresolved)
- constitutional-authority certification of any Harness (inherited from `TS-APP-API-002` Gap 5 — only structural validation ever ran)
- production eligibility of any kind — every `production_ready`/`certified` badge this spec renders is `false`, unmodified, and never hidden
- a human-facing Harness-authoring UI (FR-APP-042 remains Pi-Coding-Agent-only, via direct HTTP, with no queued React form)
- a working "attach this Harness to a Campaign Order" action (the second half of FR-APP-041 remains `TS-APP-UI-002`'s job, not yet written)
- correctness or performance at library sizes beyond what one unfiltered `GET /api/harnesses` response can reasonably hold in memory and filter client-side
- real-time reflection of Harnesses built while this page is already open (no WebSocket exists for this resource)

---
spec_end: true
next_spec: none formally queued — TS-APP-UI-004 is the last spec CA_APP_FR_EPIC_SPEC_PLAN.md
  Part 4 names inside Wave 3. TS-APP-COMPOSER-001 (Wave 4) is next in document order but is
  blocked on the internal Interview Composer codebase being provided, not on this spec.
prerequisite_for_next: none — no downstream Tech Spec is currently queued against this one.
  TS-APP-UI-002's harness-selection step (not yet written) will need to define its own
  return-value contract into this page's list route; that contract does not exist yet and is
  explicitly out of scope here (Section 2).
blocking_risk_for_downstream: none new. This spec inherits, and does not resolve,
  TS-APP-API-002's Gap 4 (Builder-export/Pipeline-intake schema mismatch) and Gap 5 (no
  constitutional-authority check is reachable) — every field this UI renders is read verbatim
  from that API's response, so both claim-ceiling limitations pass through unchanged.
---
