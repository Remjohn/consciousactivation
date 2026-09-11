---
spec_id: TS-APP-UI-002
title: Campaign List and Creation UI
document_class: TECH_SPEC
product: Conscious Activations
module: web
quality_state: RECONCILED_PENDING_AUDIT
authority_state: CURRENT
build_authority: false
controlling_frs:
  - FR-APP-050 (Campaign Order creation)
controlling_stories:
  - ST-APP-07.01 (create a Campaign Order)
  - ST-APP-03.01 (upload an existing interview)
upstream_dependencies:
  - CA_PROJECT_SNAPSHOT_V2.md (authority — CURRENT; supplied to this spec as `CA_PROJECT_SNAPSHOT.md`, internally titled "Project Snapshot v2" — same document, one filename token different from how downstream specs cite it; noted once here, not treated as a discrepancy)
  - CA_APP_FR_EPIC_SPEC_PLAN.md (authority — CURRENT)
  - TS-APP-UI-001.md (quality_state: WRITTEN_PENDING_AUDIT — RECONCILED 2026-07-27. Read in full; canonical scaffold patterns (file-based TanStack Router under `apps/web/src/routes/`, `apiFetch<T>(path, init?)` in `src/api/http.ts`, `src/api/ws.ts::useTypedWebSocket<TMessage>`, query-key tuples like `["health"]`, Vite proxy of `/api` + `/ws` to `localhost:8000`, `@ca/studio` alias to `services/studio/src`) replace this spec's prior "assumed foundation" caveats. See Source Gap Notice 1 (resolved) and §7 Stage 4 (reconciled).)
  - TS-APP-API-003.md (quality_state: WRITTEN_PENDING_AUDIT — DRAFT_DEPENDENCY_NOT_ACCEPTED; this spec calls `POST /api/interviews/import` and `GET /api/interviews/{package_id}/status` unchanged)
  - TS-APP-API-004.md (quality_state: WRITTEN_PENDING_AUDIT — DRAFT_DEPENDENCY_NOT_ACCEPTED; this spec calls `POST /api/campaigns`, `GET /api/campaigns`, `GET /api/campaigns/{campaign_id}` unchanged)
  - TS-APP-API-002.md (quality_state: WRITTEN_PENDING_AUDIT — RECONCILED 2026-07-27. Read in full; this spec's previously-inferred `HarnessSummary` interface has been corrected field-for-field against API-002 §6's real `HarnessSummary` Pydantic model. See Source Gap Notice 2 (resolved) and §6.)
downstream_consumers:
  - TS-APP-UI-003 (Control Tower UI — every `CampaignCard` in `CampaignList.tsx` links to the `/campaigns/$campaignId` route this spec occupies `apps/web/src/routes/campaigns/$campaignId.tsx` for; UI-003's `CampaignDetail.tsx` overwrites UI-001's placeholder there)
  - TS-APP-UI-004 (Harness Library UI — will very likely want to share `HarnessSummary` typing and the `HarnessCard` visual language this spec introduces as a compact inline picker; both specs now depend on the same confirmed TS-APP-API-002 contract)
output_path: apps/web/src/routes/campaigns/index.tsx, apps/web/src/routes/campaigns/new.tsx (the route files), with page components at apps/web/src/pages/CampaignList.tsx, apps/web/src/pages/CampaignNew.tsx (and supporting files listed in section 7)
wave: 3
---

# TS-APP-UI-002 — Campaign List and Creation UI

## 1. Files and Authorities Read

| File | SHA-256 (short) | Status | Fact extracted |
|---|---|---|---|
| `CA_PROJECT_SNAPSHOT.md` | n/a | READ — AUTHORITY, CURRENT | §7 names `CampaignList.tsx`, `CampaignNew.tsx` as the two highest-priority React pages after the scaffold; §8 Week 2 shows the only confirmed frontend code sample in the whole authority set: relative-path `fetch(\`/api/campaigns/${id}\`)`, imported types from `services/studio/src/domain.js` — this is the one piece of concrete frontend convention that exists anywhere in the authority set, and this spec follows it exactly |
| `CA_APP_FR_EPIC_SPEC_PLAN.md` §Part 4 (TS-APP-UI-002 entry) | n/a | READ — AUTHORITY, CURRENT | Confirms scope files (`CampaignList.tsx`, `CampaignNew.tsx`), controlling FR (FR-APP-050 only), controlling stories (ST-APP-07.01, ST-APP-03.01), and declared dependency list (UI-001, API-003, API-004 — **not** API-002, despite ST-APP-07.01 requiring harness selection; see Source Gap Notice 2) |
| `CA_APP_FR_EPIC_SPEC_PLAN.md` §ST-APP-07.01 | n/a | READ — AUTHORITY, CURRENT | "`CampaignNew.tsx` — two-step form: (1) select source, (2) select harness + outputs + autonomy"; acceptance: "Campaign appears in list with LAUNCHED status; Pipeline nodes visible" — the second clause is a claim this spec cannot make (see §3 disposition) |
| `CA_APP_FR_EPIC_SPEC_PLAN.md` §ST-APP-03.01 | n/a | READ — AUTHORITY, CURRENT | "`CampaignNew.tsx` import tab — file dropzone for video + transcript"; acceptance references `planning_lineage: ABSENT_NOT_CREATED` |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/domain.ts` | `4fa1b8a5` | READ — CURRENT IMPLEMENTATION | `CampaignOrder`, `CampaignState`, `OutputTarget`, `AutonomyPolicy` field shapes; all fields are `snake_case`, matching the API JSON wire format field-for-field — no camelCase mapping layer is ever needed between this file's types and API responses |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/campaign.ts` | `6142cf1d` | READ — CURRENT IMPLEMENTATION | `defaultAutonomyPolicy(mode)` — the exact behavioural meaning of each `AutonomyMode` this UI must communicate to the operator (see §5); `allowedTransitions` confirms `DRAFT` is schema-valid but never actually produced — `POST /api/campaigns` always yields `LAUNCHED` directly, so this UI never needs to render a "Save as Draft" affordance |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/validators.ts` | `437b9aa8` | READ — CURRENT IMPLEMENTATION | `validateCampaignOrder`'s exact rule set and error codes (`EMPTY_VALUE`, `INVALID_INTEGER`, `OUTPUT_TARGET_REQUIRED`, `FORMAT02_DEFERRED`) — this spec mirrors these rules client-side for immediate feedback (§3), but **does not import this module at runtime** (see Source Gap Notice 3) |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/canonical.ts` | `8cb8ecb9` | READ — CURRENT IMPLEMENTATION | Imports `createHash` from `node:crypto` at module top level; `deterministicId`/`canonicalSha256` require it. This is a **Node-only dependency that cannot run in a browser bundle** — the concrete finding behind Source Gap Notice 3 |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/generated/contracts.ts` | `a38d316c` | READ — CURRENT IMPLEMENTATION | `ImmutableRef`, `ActorRef`, `ArtifactRef`, `AuthorityRef` — pure `interface` declarations, zero runtime code, safe to `import type` into any bundle target including the browser |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/contracts/schemas/campaign_order.schema.json` | (uses API-004's citation, not independently re-hashed here) | READ — CURRENT IMPLEMENTATION (already read by TS-APP-API-004) | Confirms `additionalProperties: false` on `CampaignOrder` — the create form must not send extra fields beyond what §6 lists |
| `TS-APP-API-003.md` §6 | n/a | READ — WRITTEN_PENDING_AUDIT (draft dependency) | `ImportInterviewResponse`, `InterviewStatusResponse` schemas and the exact shared multipart form field list this spec's import panel must collect |
| `TS-APP-API-004.md` §5, §6 | n/a | READ — WRITTEN_PENDING_AUDIT (draft dependency) | `CampaignCreateRequest`, `CampaignDetailResponse`, `CampaignSummary` schemas; the exact create-flow validation order (source → harness → domain validation → launch → idempotent persist) that this spec's client-side pre-checks are designed to shadow, not replace |
| `TS-APP-API-004.md` §1 (citing `TS-APP-API-002.md` §1 Gap 4, §7 Stage 1) | n/a | READ — WRITTEN_PENDING_AUDIT (draft dependency, second-hand) | Only source available to this spec for `api/harness_library.py::find_by_definition_id` and the fact that a `GET`-style harness listing router already exists under TS-APP-API-002's scope (`api/routers/harnesses.py`, cited in API-004 §4 as "REUSE, unmodified") |
| `TS-APP-API-001.md` §5 | n/a | READ — WRITTEN_PENDING_AUDIT (draft dependency) | CORS dev origins are `http://localhost:3000` and `http://localhost:5173` — confirms Vite's default dev port (5173) is the assumed frontend origin; `ErrorResponse` shape (`error_code`, `message`, `service`, `timestamp`) this spec's API client parses uniformly |
| `image-gen-1_4_.png`, `image-gen-4_3_.png` ("Fortress — CMF Studio Control Tower" mockups) | n/a | READ — VISUAL REFERENCE, not a code authority | Source of the design token system in §5: near-black canvas, warm gold/amber brand accent reserved for primary CTAs and the active nav state, dark elevated cards with hairline borders and large radii, bold sans stat numbers over small tracked all-caps labels, a secondary palette (teal, orange, green, red, muted gray) already in use for status/category differentiation rather than overloading gold for everything |
| `image-gen-1_10_.png` ("Truth Over Approval" Reelcast promo graphic) | n/a | READ — VISUAL REFERENCE, not a code authority | Confirms the same black/gold/white identity extends outside the Studio Control Tower screens (bold condensed display type, gold-filled rectangle tags, gold-ringed circular avatar frames) — used here only to confirm the palette is a brand constant, not a one-off screen; no literal layout from this asset is reused, since it depicts produced marketing content, not app chrome |
| `TS-APP-UI-001.md` | n/a | READ — RECONCILED 2026-07-27 (was: unread; written after this spec) | File-based TanStack Router under `apps/web/src/routes/` (route files like `routes/campaigns/index.tsx`, `routes/campaigns/new.tsx`, `routes/campaigns/$campaignId.tsx`). Typed fetch wrapper `apiFetch<T>(path: string, init?: RequestInit)` lives in `src/api/http.ts` and throws a typed `ApiError` on non-2xx — not a free-function `parseJsonOrThrow`. TanStack Query with tuple query keys (`["health"]` for health; `["campaigns", filters]` is consistent). Vite proxies both `/api` and `/ws` to `http://localhost:8000` so the browser is same-origin in dev. `@ca/studio` path alias resolves to `services/studio/src` (UI-003 uses `@studio/domain`; the alias is one tsconfig `paths` entry shared by both naming variants, finalized by UI-001's author during scaffold build). |
| `TS-APP-API-002.md` §6 | n/a | READ — RECONCILED 2026-07-27 (was: unread; written after this spec) | The real `HarnessSummary` Pydantic model: `definition_id, definition_hash, manifest_id, manifest_version, task_id, mode, category_id, category_name, classification, capability_requirements, production_ready, certified, package_file, package_hash, added_at`. **Five corrections** over this spec's prior inferred shape — see Source Gap Notice 2 (resolved) for the field-by-field table. |

**Source Gap Notice 1 — RESOLVED 2026-07-27.** `TS-APP-UI-001.md` now exists as `WRITTEN_PENDING_AUDIT` and was read in full during the GAP-003 reconciliation pass. The previously-assumed scaffold shape (Vite dev server on port 5173, TanStack Router, TanStack Query, Tailwind) is **confirmed**, with one important correction to this spec's Stage 4 wiring assumptions: UI-001 uses TanStack's **file-based**, `@tanstack/router-plugin`-generated router, with route files live at `apps/web/src/routes/...` (e.g. `routes/campaigns/index.tsx`, `routes/campaigns/new.tsx`, `routes/campaigns/$campaignId.tsx`). It does **not** use a hand-maintained `apps/web/src/router.tsx` with `{ path, component: () => import(...) }` entries, which is what §7 Stage 4 of this spec was originally written against. The page components this spec authors (`apps/web/src/pages/CampaignList.tsx`, `apps/web/src/pages/CampaignNew.tsx`) remain valid as the rendered content — they are just imported and re-exported from new file-route modules at `routes/campaigns/index.tsx` and `routes/campaigns/new.tsx` rather than registered through an imperative router table. §7 Stage 4 has been rewritten to match. UI-001's existing `routes/campaigns/$campaignId.tsx` placeholder will be overwritten by TS-APP-UI-003, not by this spec.

**Source Gap Notice 2 — RESOLVED 2026-07-27.** `TS-APP-API-002.md` now exists as `WRITTEN_PENDING_AUDIT` and was read in full during the GAP-003 reconciliation pass. The `HarnessSummary` interface in §6 of this spec has been corrected field-for-field against API-002 §6's real `HarnessSummary` Pydantic model. The exact reconciliation:

| This spec's prior (inferred) name | API-002's real name | Reconciliation |
|---|---|---|
| `harness_definition_id` | `definition_id` | field name changed in the §6 interface; this is the value the operator's `POST /api/campaigns` body sends as `harness_definition_id` (per API-004 §6 `CampaignCreateRequest`) — the discrepancy between API-002's response field name and API-004's request body field name is a real API design choice, not a UI-002 naming bug, and the Picker now reads `h.definition_id` to populate what it sends to API-004 as `harness_definition_id` |
| `version` | `manifest_version` | field name changed in the §6 interface |
| `capability_ids` | `capability_requirements` | field name changed in the §6 interface |
| `format_profile_ids: string[]` | (does not exist) | field removed from the §6 interface; API-002 §10 explicitly notes format-profile awareness is not possible against the Builder's exported shape, so a client-side `format_profile_ids`-driven Format 02 check cannot run. The Picker's Format-02 detection collapses to its `category_id === "2d_character_animation"` subrule only; Format 02 cases gated purely on a `format_profile_id` are delegated to the server's authoritative backstop at submit time (this honestly narrows the client check and is called out in §3 and §6) |
| (absent) | `mode` | added to the §6 interface; **essential** for the Picker — generic-mode Harnesses (`mode === "generic"`, `category_id === null`) must not be selectable for an activative campaign, matching API-002's `NOT_APPLICABLE` eligibility semantics |
| (absent) | `category_name`, `classification`, `production_ready`, `certified`, `package_file`, `package_hash`, `added_at` | added to the §6 interface; `category_name` is shown in the picker card, `added_at` enables the "newest-first" sort the original spec proposed, the rest are echoed for parity with API-002's surface |

**Source Gap Notice 3 — the browser cannot import `services/studio/src/canonical.ts`, `campaign.ts`, or `validators.ts` at runtime.** `canonical.ts` unconditionally imports Node's `node:crypto` module, which Vite does not polyfill for browser targets by default. `validators.ts` transitively imports from `canonical.ts` (`assertPortableUri`, `assertSha256`), and `campaign.ts` imports `canonicalSha256`/`deterministicId` from it directly to mint `order_id`/`campaign_id`. None of that ID-minting is needed client-side anyway — `TS-APP-API-004.md` §3 confirms `order_id`/`campaign_id` are always minted server-side, and the client only ever supplies a client-generated `idempotency_key` (a random UUID, not a canonical hash). This spec therefore **only ever `import type`s from `domain.ts`/`contracts.ts`** (interfaces and type aliases erase completely at compile time — zero runtime code, zero Node dependency) and **reimplements the handful of pure client-side validation predicates it needs locally**, in `apps/web/src/lib/campaignFormValidation.ts`, using the same rule names and error codes as `validators.ts` so error messages stay identical whether caught before or after the network round-trip — without ever executing `validators.ts`'s actual code path in the browser. **Note added during reconciliation**: UI-001 confirms the `@ca/studio` path alias targets `services/studio/src` for `import type` use, so the local browser-safe reimplementation rule for *runtime* code is unchanged.

---

## 2. Problem, User Outcome, Solution, and Scope

### Problem without this spec

`TS-APP-API-004` gives the product a working `POST /api/campaigns` / `GET /api/campaigns` / `GET /api/campaigns/{id}` surface, and `TS-APP-API-003` gives it a working interview import endpoint — but nothing can reach either one except a developer holding a terminal. Per `CA_PROJECT_SNAPSHOT.md` Gap 2, there is still no React component tree anywhere in the repository. An operator cannot see what campaigns exist, cannot tell a `RUNNING` campaign from a `BLOCKED_EXCEPTION` one at a glance, and has no way to launch a new one short of hand-writing a `curl` command that reproduces every field `CampaignCreateRequest` requires — including fields (`harness_ref`, `autonomy_policy`, `operator_actor`) that the API derives from simpler operator-facing choices.

### User outcome

An operator opens the app, sees every campaign in their workspace as a scannable list with a lifecycle badge and enough context (category, autonomy mode, output count, budget) to know what needs attention, and can start a new campaign in two guided steps — pick or import a source, then pick a Harness and describe the outputs — without ever typing a raw `harness_definition_id`, a `source_kind` literal, or an `ActorRef` by hand.

### Solution

Two React pages, `CampaignList.tsx` and `CampaignNew.tsx`, plus their supporting components, hooks, and a typed API client, built against the Wave 2 endpoints exactly as `TS-APP-API-003`/`004` defined them:

- `CampaignList.tsx` — fetches `GET /api/campaigns`, renders a filterable, badge-coded list of `CampaignSummary` rows, and links each row to the `/campaigns/:campaignId` route `TS-APP-UI-003` will fulfill.
- `CampaignNew.tsx` — a two-step wizard. Step 1 either verifies an existing, ready source package (`GET /api/interviews/{id}/status`) or imports a new one (`POST /api/interviews/import`). Step 2 selects a Harness, configures output targets/objective/budget/autonomy, and launches (`POST /api/campaigns`).
- A shared design system (design tokens, `LifecycleBadge`, layout primitives) matching the black/gold Control Tower visual identity established in the two reference mockups read in §1.

### In scope

- `apps/web/src/pages/CampaignList.tsx`, `apps/web/src/pages/CampaignNew.tsx`
- `apps/web/src/components/campaign-list/` — `CampaignCard.tsx`, `LifecycleBadge.tsx`, `CampaignFilters.tsx`, `EmptyCampaignState.tsx`
- `apps/web/src/components/campaign-new/` — `SourceStep.tsx`, `ExistingSourcePanel.tsx`, `ImportInterviewPanel.tsx`, `ConfigureStep.tsx`, `HarnessPicker.tsx`, `OutputTargetsEditor.tsx`, `AutonomyModeSelector.tsx`, `LaunchReview.tsx`
- `apps/web/src/api/campaigns.ts`, `apps/web/src/api/interviews.ts`, `apps/web/src/api/harnesses.ts`, `apps/web/src/api/types.ts`, `apps/web/src/api/errors.ts`
- `apps/web/src/hooks/useCampaigns.ts`, `useCreateCampaign.ts`, `useImportInterview.ts`, `useInterviewStatus.ts`, `useHarnesses.ts`
- `apps/web/src/lib/campaignFormValidation.ts`, `apps/web/src/lib/statusTokens.ts`
- Route registration for `/campaigns` and `/campaigns/new` (additive entries only, into whatever route tree TS-APP-UI-001 establishes)
- Design tokens (Tailwind theme extension + CSS custom properties) shared by both pages

### Out of scope

- `CampaignDetail.tsx` / Control Tower (`TS-APP-UI-003`) — this spec only defines the `/campaigns/:campaignId` navigation target
- `HarnessLibrary.tsx` full browse page (`TS-APP-UI-004`) — this spec's `HarnessPicker` is a compact inline picker, not the full library browser
- Brief-led interview admission (FR-APP-020, the "Start from Interview Brief" entry point) — blocked on `TS-APP-COMPOSER-001` (Wave 4, not yet integrated); Step 1 of this spec implements only the imported-interview path (FR-APP-021 / ST-APP-03.01)
- `GET /api/interviews` (a list/search endpoint for existing source packages) — does not exist in any read spec; see Source Gap Notice 1 in §3's workaround
- Authentication, multi-tenant workspace switching UI, WebSocket live status (`TS-APP-API-005`/`TS-APP-UI-003`)
- Any modification to `services/studio/src/*` — read-only reference for types and behavioural rules, never imported at runtime (Source Gap Notice 3)
- Cancel-campaign UI (`POST /api/campaigns/{id}/cancel` exists in `TS-APP-API-004` but no story in this spec's controlling set asks for a cancel button; left for `TS-APP-UI-003`, which owns campaign-in-flight actions)

---

## 3. Governing Decisions and Constraints

**The browser never mints `order_id`/`campaign_id`, and never imports `campaign.ts` or `validators.ts` at runtime.** Per Source Gap Notice 3, `canonical.ts` requires `node:crypto`. `TS-APP-API-004` already confirmed the server mints both IDs from a content-addressed hash of the order; the client's only obligation is a fresh `idempotency_key`, generated with the browser's native `crypto.randomUUID()` (available in every browser Vite targets by default, no polyfill needed). Every place this spec would otherwise be tempted to import `services/studio/src/*` for runtime logic, it instead does one of: (a) `import type` only (free, safe, erases at compile time), or (b) reimplements the specific pure rule locally in `campaignFormValidation.ts`.

**Category is derived from the selected Harness, never freely typed; `format_profile_id` is operator-typed with a server-side backstop.** `TS-APP-API-004`'s create flow rejects a request whose `category_id` doesn't match the selected harness's `category_binding.category_id` with `HARNESS_INELIGIBLE`. Rather than let an operator type a `category_id` that can only ever be wrong or right by luck, `ConfigureStep.tsx` auto-populates `category_id` the moment a Harness card is selected. Reconciliation note (Source Gap Notice 2 resolved): `format_profile_id` cannot be auto-populated from API-002's response — API-002's real `HarnessSummary` has no `format_profile_ids` field (API-002 §10 explicitly flags format-profile awareness as unavailable against the Builder's exported shape). `ConfigureStep.tsx` therefore exposes `format_profile_id` as an editable operator-typed field that defaults to an empty string; the server's authoritative `FORMAT02_DEFERRED` rejection remains the backstop, and the client's Format-02 detection (see next paragraph) is best-effort only.

**Format 02 is refused in the picker for the category-gated case, with a server-side backstop for the format-profile-gated case.** `validators.ts` rejects `category_id === "2d_character_animation"` or any `format_profile_id` starting with `format02_` with `FORMAT02_DEFERRED`. Reconciliation note (Source Gap Notice 2 resolved): API-002's response surface only allows the client to evaluate the `category_id` subrule (`category_id === "2d_character_animation"`); the `format_profile_id` subrule cannot be evaluated client-side because API-002 does not return a `format_profile_ids` field. `HarnessPicker.tsx` renders a card with `category_id === "2d_character_animation"` as a disabled "Deferred" card — the category-gated subset, enforced one step earlier, with the same wording the API uses. The format-profile-gated subset is delegated to the server's authoritative `FORMAT02_DEFERRED` backstop at submit time and is honestly NOT claimed as a client-side check.

**"Select an existing source" is a single-ID verify-then-select flow, not a browsable list — a known limitation, not a design choice.** No spec supplied to this author defines `GET /api/interviews` (list). `ExistingSourcePanel.tsx` therefore asks the operator to paste or recall a `package_id` (typically just returned to them by a prior import, or eventually by the Interview Composer) and calls `GET /api/interviews/{id}/status` to verify it before enabling "Continue." This mirrors `TS-APP-API-004`'s own `SOURCE_PACKAGE_NOT_READY` rule client-side (only `COMPONENTS_IN_PROGRESS` or `PUBLISHED_DERIVATIVE_ELIGIBLE` unlock Step 2) so an operator is never allowed to walk into a guaranteed-422. **This is a stopgap.** A future API spec adding `GET /api/interviews?workspace_id=&project_id=&lifecycle_state=` would let this panel become a real picker; this spec explicitly recommends that as the next API spec after TS-APP-API-006, and flags it again in the footer.

**The Harness picker's data contract is now confirmed against the real API-002 response shape (Source Gap Notice 2 resolved 2026-07-27).** `HarnessSummary` in §6 has been corrected field-for-field against `TS-APP-API-002.md` §6's real `HarnessSummary` Pydantic model — see §1's reconciliation table and §6's TypeScript interface. The operator's `POST /api/campaigns` body sends the chosen harness's `definition_id` as the value of its `harness_definition_id` field (this naming asymmetry is documented in §6 and is API-002↔API-004's design choice, not a UI-002 bug).
**The `/campaigns/$campaignId` route file is owned by UI-001 as a placeholder and overwritten by TS-APP-UI-003; this spec occupies `/campaigns/` (index) and `/campaigns/new`.** Reconciliation note (Source Gap Notice 1 resolved): UI-001 already scaffolds `apps/web/src/routes/campaigns/$campaignId.tsx` as a placeholder for FR-APP-060..064. `CampaignList.tsx`'s `Link to="/campaigns/$campaignId"` navigates to it; `CampaignNew.tsx`'s successful-launch navigation targets it. Until TS-APP-UI-003 ships the real `CampaignDetail.tsx`, that route renders whatever placeholder UI-001 ships — this spec does not stub a fake `CampaignDetail.tsx` to fill the gap, because a stub that isn't wired to real Control Tower data would be a more misleading placeholder than an honest UI-001 placeholder.

**Idempotency key lifecycle.** A single `idempotency_key` (UUID) is generated once, when the operator reaches the Launch Review screen in Step 2, and held in component state for the lifetime of that review screen — reused across an accidental double-click or a retried network failure, so a flaky connection can never create two campaigns from one intended action. The key is regenerated only if the operator navigates back into Step 1 or Step 2 and changes any field, since at that point a retry with the old key would (correctly, per `TS-APP-API-004` AC-010) just replay the *original* unedited order.

**Wire format has zero camelCase translation layer.** Every field in `domain.ts` and every pydantic model in `TS-APP-API-003`/`004` §6 is already `snake_case`. This spec's local TypeScript interfaces in `api/types.ts` use the identical field names the JSON response bodies use — no `campaignId` vs `campaign_id` mapping step exists anywhere in this codebase, deliberately, so a field seen in a network tab and a field referenced in a component are always spelled the same way.

**Claim ceiling:** `CAMPAIGN_LIST_CREATE_UI_ASSUMED_SCAFFOLD_EVIDENCE`. This spec does not claim TS-APP-UI-001's scaffold is confirmed to match its assumptions (Source Gap Notice 1), that the Harness picker's data contract is confirmed correct (Source Gap Notice 2), that a launched campaign has triggered real Pipeline execution (inherited, unresolved, from `TS-APP-API-004` Source Gap Notice 2 — this UI shows exactly the `pipeline_ingestion_status: "NOT_YET_TRIGGERED"` the API already returns, and never claims otherwise), or that any accessibility, internationalization, or authentication work has been done beyond baseline keyboard/focus support.

---

## 4. Current Brownfield Architecture

| Component | Path | Actual behaviour | Disposition | Reason |
|---|---|---|---|---|
| Studio `CampaignOrder`/`CampaignState`/`OutputTarget`/`AutonomyPolicy` types | `services/studio/src/domain.ts` | Correct, `snake_case`, framework-agnostic interfaces | **PORT (types only)** | `import type` directly; zero runtime cost, zero Node dependency |
| Studio `campaign.ts`, `validators.ts`, `canonical.ts` | `services/studio/src/*.ts` | Correct but transitively require `node:crypto` | **REFERENCE ONLY, NOT IMPORTED** | Source Gap Notice 3 — reimplemented locally where the browser needs equivalent behaviour |
| `POST /api/campaigns`, `GET /api/campaigns`, `GET /api/campaigns/{id}` | `api/routers/campaigns.py` (TS-APP-API-004) | Fully specified, `WRITTEN_PENDING_AUDIT` | **CONSUME AS-IS** | This spec calls these endpoints exactly as documented; no changes requested |
| `POST /api/interviews/import`, `GET /api/interviews/{id}/status` | `api/routers/interviews.py` (TS-APP-API-003) | Fully specified, `WRITTEN_PENDING_AUDIT` | **CONSUME AS-IS** | Same |
| `GET /api/harnesses` | `api/routers/harnesses.py` (TS-APP-API-002, unread) | Exists per second-hand citation only | **CONSUME, UNCONFIRMED SHAPE** | Source Gap Notice 2 |
| Vite + TanStack Router + TanStack Query + Tailwind scaffold | `apps/web/` (TS-APP-UI-001, not yet written) | Does not exist yet in any form this author could verify | **ASSUMED FOUNDATION** | Source Gap Notice 1 — every Stage 4 wiring step is additive against an unverified scaffold |
| React component tree of any kind | `apps/web/src/` | Does not exist (`CA_PROJECT_SNAPSHOT.md` Gap 2, confirmed empty in the supplied implementation archive — no `apps/` directory present anywhere in it) | **GREENFIELD** | This spec, together with TS-APP-UI-001, is the first React code in the repository |

---

## 5. Proposed Architecture and Workflows

### Design system (grounded in the supplied reference mockups, not invented)

The two "Fortress — CMF Studio Control Tower" screens and the "Truth Over Approval" promo graphic all share one identity: a near-black canvas, a single reserved warm-gold brand accent used sparingly for primary actions and the active navigation state, dark elevated cards with hairline borders and generous corner radius, bold sans stat numbers set against small tracked all-caps labels — and, importantly, a **secondary palette already doing status work** (a red flag for a blocked count, an orange flame for a streak, a green leaf for a healthy habit, a teal accent on one drill card) rather than every signal being gold. This spec follows that exactly rather than inventing a fresh palette:

```css
:root {
  --ca-bg-canvas: #0a0a0c;
  --ca-bg-surface: #141416;
  --ca-bg-surface-raised: #1b1b1e;
  --ca-border-subtle: rgba(255, 255, 255, 0.08);
  --ca-border-accent: rgba(232, 185, 35, 0.35);

  --ca-gold: #e8b923;          /* primary brand accent -- CTAs, active nav, LAUNCHED badge */
  --ca-gold-strong: #f4c842;   /* hover/active state of gold elements */
  --ca-on-gold: #0a0a0c;       /* text/icon color on a gold-filled surface */

  --ca-text-primary: #f5f5f2;
  --ca-text-muted: #8b8b93;
  --ca-text-faint: #5b5b63;

  /* status palette -- reused, not invented, from the reference screens */
  --ca-state-running: #2dd4bf;      /* teal */
  --ca-state-awaiting: #f2994a;     /* orange */
  --ca-state-blocked: #e5484d;      /* red */
  --ca-state-ready: #34c77b;        /* green */
  --ca-state-shipped: #1f9d57;      /* deep green */
  --ca-state-inactive: #6b6b74;     /* gray -- DRAFT, CANCELLED */
}
```

```ts
// tailwind.config.ts -- theme.extend excerpt
colors: {
  canvas: "var(--ca-bg-canvas)",
  surface: "var(--ca-bg-surface)",
  "surface-raised": "var(--ca-bg-surface-raised)",
  gold: { DEFAULT: "var(--ca-gold)", strong: "var(--ca-gold-strong)", on: "var(--ca-on-gold)" },
  ink: { primary: "var(--ca-text-primary)", muted: "var(--ca-text-muted)", faint: "var(--ca-text-faint)" },
  state: {
    running: "var(--ca-state-running)", awaiting: "var(--ca-state-awaiting)",
    blocked: "var(--ca-state-blocked)", ready: "var(--ca-state-ready)",
    shipped: "var(--ca-state-shipped)", inactive: "var(--ca-state-inactive)",
  },
},
borderRadius: { card: "16px" },
```

`LifecycleBadge` maps all eight `CampaignLifecycleState` values onto that palette -- gold is deliberately reserved for `LAUNCHED` (the moment of commitment, mirroring the reference's gold CTA) and never reused for a routine "in progress" state, which gets teal instead:

| `lifecycle_state` | Badge color | Icon cue |
|---|---|---|
| `DRAFT` | `state.inactive`, outline only | dashed circle |
| `LAUNCHED` | `gold`, filled | rocket |
| `RUNNING` | `state.running` (teal), filled | spinner |
| `AWAITING_REVIEW` | `state.awaiting` (orange), filled | pause |
| `BLOCKED_EXCEPTION` | `state.blocked` (red), filled | flag |
| `READY_TO_SHIP` | `state.ready` (green), filled | check |
| `SHIPPED` | `state.shipped` (deep green), filled | check-double |
| `CANCELLED` | `state.inactive`, filled, reduced-opacity row | x |

### Page: `CampaignList.tsx`

```
+-----------------------------------------------------------+
|  Campaigns                                [+ New Campaign]|  <- gold CTA, top-right
|  workspace: acme-coach v   project: q3-launch v            |
+-------------------------------------------------------------+
|  o 2 Running   o 1 Awaiting Review   o 1 Blocked           |  <- summary strip, counts by state
+-------------------------------------------------------------+
|  [DRAFT ] [LAUNCHED] [RUNNING] [BLOCKED] ... (chips)        |  <- lifecycle_state filter
+-------------------------------------------------------------+
|  +---------------------------------------------------+      |
|  | o RUNNING   short_form_edited_video     >          |      |  <- CampaignCard, whole row clickable
|  |   REVIEW_BEFORE_SHIP - 2 outputs - 100 budget       |      |
|  +---------------------------------------------------+      |
|  +---------------------------------------------------+      |
|  | o BLOCKED_EXCEPTION  carousels           >          |      |
|  +---------------------------------------------------+      |
+-------------------------------------------------------------+
```

Data flow: `useCampaigns({ workspace_id, project_id, lifecycle_state })` -> `useQuery(["campaigns", filters], () => listCampaigns(filters))` -> `GET /api/campaigns?...`. The endpoint always returns `200` with an array, even empty (`TS-APP-API-004` §6) -- so the empty state is a rendered choice, never an error branch. Clicking a `CampaignCard` navigates to `/campaigns/${campaign_id}`. The summary strip counts are computed client-side from the already-fetched list (no extra request) -- accurate for the current filter view, not a workspace-wide total, and labeled as such.

### Page: `CampaignNew.tsx` -- two-step wizard

```
Step 1: Source                          Step 2: Configure & Launch
+--------------+--------------+         +--------------------------+
| Use Existing | Import New   |         |  Harness picker (cards)  |
| Source       | Interview    |   ->    |  Output targets (list)   |
+--------------+--------------+         |  Objective / seed / tags |
                                         |  Budget / deadline       |
                                         |  Autonomy mode           |
                                         |  [ Launch Campaign ]     |  <- gold CTA
                                         +--------------------------+
```

**Step 1a -- Use Existing Source** (`ExistingSourcePanel.tsx`): a `package_id` text input + "Check Status" button -> `useInterviewStatus(packageId)` -> `GET /api/interviews/{id}/status`. On success, renders a read-only summary card (`lifecycle_state` badge, `word_count`/`phrase_count`/`shot_count`, `derivative_eligible`). "Continue" is enabled only when `lifecycle_state` is `COMPONENTS_IN_PROGRESS` or `PUBLISHED_DERIVATIVE_ELIGIBLE` -- otherwise an inline warning explains why, using the same wording `SOURCE_PACKAGE_NOT_READY` would.

**Step 1b -- Import New Interview** (`ImportInterviewPanel.tsx`): two dropzones (video, transcript) plus the shared form fields `TS-APP-API-003` §6 requires (`workspace_id`, `project_id`, `operator_id`, `authority_scope`, `assertion_id`, `transcript_format` radio, conditional `speaker_id`, optional `visual_profile_id`). Submits via `useImportInterview()` -> `POST /api/interviews/import` (multipart). On `201`, the returned `package_id` and counts populate the same summary card Step 1a shows, and "Continue" unlocks -- the two sub-tabs converge on identical downstream state.

**Step 2 -- Configure & Launch** (`ConfigureStep.tsx`):
- `HarnessPicker.tsx` -- card grid from `useHarnesses()` (§3, §6 caveats apply). Cards whose inferred category/profile match the Format 02 rule render disabled with a "Deferred" badge. Selecting a card sets `harness_definition_id`, auto-fills `category_id` and a default `format_profile_id`.
- `OutputTargetsEditor.tsx` -- a repeatable row list (`output_type` select, `quantity` stepper >= 1, `profile_id`). "Launch" stays disabled while the list is empty (`OUTPUT_TARGET_REQUIRED`, enforced before the network call ever fires).
- Plain fields: `objective`, `initial_seed` (textareas), `taste_direction` (tag input -> `string[]`), `budget_units` (integer stepper, min 1), optional `deadline_utc` (datetime picker).
- `AutonomyModeSelector.tsx` -- four options, each with one line of consequence pulled directly from `campaign.ts`'s `defaultAutonomyPolicy`/`shouldInterruptOperator`, not invented copy:
  - **Autopilot** -- "Runs without interruption unless something breaks." (`final_review_required: false`)
  - **Review Before Ship** -- "Runs freely, but pauses for your review at the final artifact." (`final_review_required: true`, interrupts only at `final-artifact-review`)
  - **Checkpointed** -- "Pauses at two fixed checkpoints: final script approval and final artifact review." (`checkpoint_ids` fixed pair)
  - **Shadow** -- "Runs silently for observation only -- this campaign can never be shipped." (`shouldInterruptOperator` always `false`; `transitionCampaign` rejects `SHIPPED` for `SHADOW` with `SHADOW_CANNOT_SHIP`)
- `LaunchReview.tsx` -- a final read-only summary of everything above, the gold "Launch Campaign" button, and the stable `idempotency_key` described in §3.

On `POST /api/campaigns` success (`201`), navigate to `/campaigns/${state.campaign_id}` (§3's route-contract caveat applies). On a mapped error, focus returns to the step/field that caused it:

| `error_code` | Where the UI sends focus |
|---|---|
| `SOURCE_PACKAGE_NOT_FOUND`, `SOURCE_PACKAGE_NOT_READY` | Back to Step 1, inline error on the source summary card |
| `HARNESS_NOT_FOUND`, `HARNESS_INELIGIBLE` | Step 2, inline error on `HarnessPicker` |
| `EMPTY_VALUE`, `INVALID_INTEGER`, `OUTPUT_TARGET_REQUIRED`, `FORMAT02_DEFERRED` | The specific field (already prevented client-side in the common case; this is the authoritative fallback) |
| network / 5xx / unrecognized code | Toast with "Retry" -- reuses the same `idempotency_key` |

---

## 6. Data Models, Contracts, Schemas, and APIs

### `apps/web/src/api/types.ts`

```ts
// Type-only imports -- erase completely at compile time, zero runtime/Node dependency (§3, Source Gap Notice 3).
import type {
  CampaignOrder, CampaignState, OutputTarget, AutonomyMode,
  AutonomyPolicy, CampaignLifecycleState,
} from "../../../../services/studio/src/domain";
import type { ImmutableRef, ArtifactRef } from "../../../../services/studio/src/generated/contracts";

export type { CampaignOrder, CampaignState, OutputTarget, AutonomyMode, AutonomyPolicy, CampaignLifecycleState, ImmutableRef, ArtifactRef };

// API-specific response shapes not present in domain.ts -- mirrors TS-APP-API-004 §6 field-for-field.
export interface CampaignSummary {
  campaign_id: string; order_id: string; workspace_id: string; project_id: string;
  category_id: string; lifecycle_state: CampaignLifecycleState; autonomy_mode: AutonomyMode;
  output_target_count: number; budget_units: number; version: number;
}

export interface CampaignDetailResponse {
  order: CampaignOrder; state: CampaignState;
  source_derivative_eligible: boolean; source_lifecycle_state: string;
  pipeline_ingestion_status: "NOT_YET_TRIGGERED";
  idempotent_replay: boolean;
}

export interface CampaignCreateRequest {
  idempotency_key: string; workspace_id: string; project_id: string;
  source_package_id: string; harness_definition_id: string;
  category_id: string; format_profile_id: string;
  objective: string; initial_seed: string; taste_direction: string[];
  output_targets: OutputTarget[]; budget_units: number;
  deadline_utc: string | null; autonomy_mode: AutonomyMode; operator_id: string;
}

// Mirrors TS-APP-API-003 §6 exactly.
export interface ImportInterviewResponse {
  package_id: string; revision: number; lifecycle_state: string;
  admission_mode: "IMPORTED" | "BRIEF_LED"; derivative_eligible: boolean;
  planning_lineage: Record<string, unknown>;
  word_count: number; phrase_count: number; shot_count: number; keyframe_count: number;
  idempotent_replay: boolean;
}

export interface InterviewStatusResponse {
  package_id: string; revision: number; lifecycle_state: string;
  admission_mode: "IMPORTED" | "BRIEF_LED"; derivative_eligible: boolean;
  word_count?: number; phrase_count?: number;
}

// CONFIRMED against TS-APP-API-002.md §6 (Reconciled 2026-07-27 during the GAP-003 pass).
// Mirrors the real `HarnessSummary` Pydantic model field-for-field.
export interface HarnessSummary {
  // The operator's POST /api/campaigns body sends this value as `harness_definition_id`
  // (API-004 §6 CampaignCreateRequest) — the naming asymmetry is API-002↔API-004's
  // design choice, not a UI-002 naming bug. The Picker reads `h.definition_id` here.
  definition_id: string;
  definition_hash: string;
  manifest_id: string;
  manifest_version: string;
  task_id: string;
  mode: "generic" | "activative";        // essential — generic-mode Harnesses have category_id: null
  category_id: string | null;            // null for generic mode
  category_name: string | null;
  classification: string[];
  capability_requirements: string[];
  production_ready: boolean;             // always false at this stage (API-002 §6)
  certified: boolean;                   // always false at this stage (API-002 §6)
  package_file: string;                 // "{definition_id}.zip"
  package_hash: string;                 // sha256 of the ZIP bytes on disk
  added_at: string | null;              // RFC 3339, from file mtime — NON-AUTHORITATIVE per API-002 §3
}

export interface ErrorResponse {
  error_code: string; message: string; service: string | null; timestamp: string;
}
```

### Endpoints this spec calls (defined elsewhere, not by this spec)

| Method | Path | Owning spec | Used by |
|---|---|---|---|
| `GET` | `/api/campaigns?workspace_id=&project_id=&lifecycle_state=` | TS-APP-API-004 | `useCampaigns` |
| `GET` | `/api/campaigns/{campaign_id}` | TS-APP-API-004 | (reserved for `TS-APP-UI-003`; not called by this spec's pages) |
| `POST` | `/api/campaigns` | TS-APP-API-004 | `useCreateCampaign` |
| `POST` | `/api/interviews/import` | TS-APP-API-003 | `useImportInterview` |
| `GET` | `/api/interviews/{package_id}/status` | TS-APP-API-003 | `useInterviewStatus` |
| `GET` | `/api/harnesses` | TS-APP-API-002 (reconciled 2026-07-27 — Source Gap Notice 2 resolved) | `useHarnesses` |

### `apps/web/src/api/errors.ts` — NOT authored by this spec

**Reconciliation note (Source Gap Notice 1 resolved):** UI-001 owns the typed-error path. UI-001's `apps/web/src/api/http.ts` already defines `apiFetch<T>(path: string, init?: RequestInit): Promise<T>`, which throws a typed `ApiError` (carrying `error_code`, `message`, `service`, `timestamp` from API-001's `ErrorResponse` shape) on any non-2xx response. This spec previously invented a parallel `parseJsonOrThrow` helper out of an inferred-scaffold assumption; that helper is **withdrawn**. Every Stage 1 client file in this spec now calls `apiFetch` instead. UI-002 therefore creates **no** `apps/web/src/api/errors.ts` file. The `ApiError` exception surface this spec's component-level error-code routing table in §5 keys against is the same `ApiError` shape UI-001 already exports; UI-002 imports it from `../api/http` (or wherever UI-001's scaffold re-exports it) rather than from a local file.

```ts
// apps/web/src/api/http.ts — owned by TS-APP-UI-001, shown here only to name the
// surface this spec depends on; do NOT create this file when implementing UI-002.
// import { apiFetch, ApiError } from "./http";
```

### `apps/web/src/api/campaigns.ts`

```ts
import { apiFetch } from "./http";
import type { CampaignSummary, CampaignDetailResponse, CampaignCreateRequest, CampaignLifecycleState } from "./types";

export interface CampaignListFilters {
  workspace_id?: string; project_id?: string; lifecycle_state?: CampaignLifecycleState;
}

export async function listCampaigns(filters: CampaignListFilters): Promise<CampaignSummary[]> {
  const params = new URLSearchParams(Object.entries(filters).filter(([, v]) => v) as [string, string][]);
  return apiFetch<CampaignSummary[]>(`/api/campaigns?${params.toString()}`);
}

export async function createCampaign(payload: CampaignCreateRequest): Promise<CampaignDetailResponse> {
  return apiFetch<CampaignDetailResponse>("/api/campaigns", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}
```

---

## 7. Implementation Stages and Exact Target Paths

All paths are relative to the repository root, using the restructured `apps/web/` location `CA_PROJECT_SNAPSHOT.md` §7 specifies (not a numbered legacy directory).

### Stage 1 -- API client, types, and browser-safe validation (no components yet)

**`apps/web/src/api/types.ts`** -- as shown in §6.

**`apps/web/src/api/campaigns.ts`** -- reconciles to use UI-001's `apiFetch` (Source Gap Notice 1 resolved: `errors.ts` is owned by UI-001, not authored by this spec).

**`apps/web/src/api/interviews.ts`**
```ts
import { apiFetch } from "./http";
import type { ImportInterviewResponse, InterviewStatusResponse } from "./types";

export async function getInterviewStatus(packageId: string): Promise<InterviewStatusResponse> {
  return apiFetch<InterviewStatusResponse>(`/api/interviews/${encodeURIComponent(packageId)}/status`);
}

export interface ImportInterviewInput {
  video: File; transcript: File;
  workspace_id: string; project_id: string; operator_id: string;
  authority_scope: string; assertion_id: string;
  transcript_format: "PRE_ALIGNED_JSON" | "SRT";
  speaker_id?: string; visual_profile_id?: string;
}

export async function importInterview(input: ImportInterviewInput): Promise<ImportInterviewResponse> {
  const form = new FormData();
  form.set("video", input.video);
  form.set("transcript", input.transcript);
  for (const [key, value] of Object.entries(input)) {
    if (key === "video" || key === "transcript" || value === undefined) continue;
    form.set(key, String(value));
  }
  return apiFetch<ImportInterviewResponse>("/api/interviews/import", {
    method: "POST",
    body: form,
  });
}
```

**`apps/web/src/api/harnesses.ts`** -- reconciles to confirmed API-002 §6 contract (Source Gap Notice 2 resolved 2026-07-27).
```ts
import { apiFetch } from "./http";
import type { HarnessSummary } from "./types";

/** CONFIRMED against TS-APP-API-002.md §6 (Reconciled 2026-07-27). */
export async function listHarnesses(): Promise<HarnessSummary[]> {
  return apiFetch<HarnessSummary[]>("/api/harnesses");
}
```

**`apps/web/src/lib/campaignFormValidation.ts`** -- mirrors `validators.ts`'s rules and error codes without importing it (Source Gap Notice 3).
```ts
export type ValidationCode = "EMPTY_VALUE" | "INVALID_INTEGER" | "OUTPUT_TARGET_REQUIRED" | "FORMAT02_DEFERRED";

export interface FieldError { code: ValidationCode; message: string; }

export function requireNonEmpty(value: string, label: string): FieldError | null {
  return value.trim() ? null : { code: "EMPTY_VALUE", message: `${label} must not be empty` };
}

export function requirePositiveInteger(value: number, label: string): FieldError | null {
  return Number.isSafeInteger(value) && value >= 1 ? null : { code: "INVALID_INTEGER", message: `${label} must be a whole number of at least 1` };
}

export function requireAtLeastOneOutputTarget(count: number): FieldError | null {
  return count >= 1 ? null : { code: "OUTPUT_TARGET_REQUIRED", message: "At least one output target is required" };
}

/** Same rule as validators.ts::validateCampaignOrder -- kept in exact sync by hand until a shared package exists. */
export function isFormat02Deferred(categoryId: string, formatProfileId: string): boolean {
  return categoryId === "2d_character_animation" || formatProfileId.startsWith("format02_");
}
```

**`apps/web/src/lib/statusTokens.ts`** -- the `LifecycleBadge` color/icon table from §5, as a typed lookup:
```ts
import type { CampaignLifecycleState } from "../api/types";

export const LIFECYCLE_TOKENS: Record<CampaignLifecycleState, { color: string; icon: string; filled: boolean }> = {
  DRAFT: { color: "state-inactive", icon: "circle-dashed", filled: false },
  LAUNCHED: { color: "gold", icon: "rocket", filled: true },
  RUNNING: { color: "state-running", icon: "loader", filled: true },
  AWAITING_REVIEW: { color: "state-awaiting", icon: "pause", filled: true },
  BLOCKED_EXCEPTION: { color: "state-blocked", icon: "flag", filled: true },
  READY_TO_SHIP: { color: "state-ready", icon: "check", filled: true },
  SHIPPED: { color: "state-shipped", icon: "check-check", filled: true },
  CANCELLED: { color: "state-inactive", icon: "x", filled: true },
};
```

### Stage 2 -- `CampaignList.tsx` and supporting components

**`apps/web/src/hooks/useCampaigns.ts`**
```ts
import { useQuery } from "@tanstack/react-query";
import { listCampaigns, type CampaignListFilters } from "../api/campaigns";

export function useCampaigns(filters: CampaignListFilters) {
  return useQuery({
    queryKey: ["campaigns", filters],
    queryFn: () => listCampaigns(filters),
  });
}
```

**`apps/web/src/components/campaign-list/LifecycleBadge.tsx`**
```tsx
import { LIFECYCLE_TOKENS } from "../../lib/statusTokens";
import type { CampaignLifecycleState } from "../../api/types";

export function LifecycleBadge({ state }: { state: CampaignLifecycleState }) {
  const token = LIFECYCLE_TOKENS[state];
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold tracking-wide uppercase
        ${token.filled ? `bg-${token.color} text-ink-primary` : `border border-${token.color} text-${token.color}`}`}
    >
      {state.replace(/_/g, " ")}
    </span>
  );
}
```

**`apps/web/src/components/campaign-list/CampaignCard.tsx`**
```tsx
import { Link } from "@tanstack/react-router";
import { LifecycleBadge } from "./LifecycleBadge";
import type { CampaignSummary } from "../../api/types";

export function CampaignCard({ campaign }: { campaign: CampaignSummary }) {
  return (
    <Link
      to="/campaigns/$campaignId"
      params={{ campaignId: campaign.campaign_id }}
      className="block rounded-card border border-[color:var(--ca-border-subtle)] bg-surface p-5 hover:border-[color:var(--ca-border-accent)] transition-colors"
    >
      <div className="flex items-center justify-between">
        <LifecycleBadge state={campaign.lifecycle_state} />
        <span className="text-ink-muted text-sm">{campaign.category_id}</span>
      </div>
      <div className="mt-2 text-ink-muted text-xs tracking-wide uppercase">
        {campaign.autonomy_mode} - {campaign.output_target_count} output{campaign.output_target_count === 1 ? "" : "s"} - {campaign.budget_units} budget
      </div>
    </Link>
  );
}
```

**`apps/web/src/components/campaign-list/EmptyCampaignState.tsx`** -- centered icon, "No campaigns yet," gold "Create your first campaign" button linking to `/campaigns/new`. (Prose spec; trivial enough not to warrant a full listing.)

**`apps/web/src/components/campaign-list/CampaignFilters.tsx`** -- a row of pill buttons, one per `CampaignLifecycleState`, using the same `LIFECYCLE_TOKENS` colors in outline form; clicking toggles `lifecycle_state` in the parent's filter state (single-select, not multi -- matches the API's single-value query param).

**`apps/web/src/pages/CampaignList.tsx`**
```tsx
import { useState } from "react";
import { Link } from "@tanstack/react-router";
import { useCampaigns } from "../hooks/useCampaigns";
import { CampaignCard } from "../components/campaign-list/CampaignCard";
import { CampaignFilters } from "../components/campaign-list/CampaignFilters";
import { EmptyCampaignState } from "../components/campaign-list/EmptyCampaignState";
import type { CampaignLifecycleState } from "../api/types";

export default function CampaignList() {
  const [lifecycleFilter, setLifecycleFilter] = useState<CampaignLifecycleState | undefined>();
  const { data: campaigns, isLoading, isError, refetch } = useCampaigns({ lifecycle_state: lifecycleFilter });

  return (
    <div className="min-h-screen bg-canvas p-8">
      <div className="flex items-center justify-between">
        <h1 className="text-ink-primary text-2xl font-bold">Campaigns</h1>
        <Link to="/campaigns/new" className="rounded-full bg-gold px-5 py-2.5 font-semibold text-gold-on">
          + New Campaign
        </Link>
      </div>
      <CampaignFilters value={lifecycleFilter} onChange={setLifecycleFilter} />
      {isLoading && <ListSkeleton />}
      {isError && <ErrorBanner onRetry={() => refetch()} />}
      {campaigns && campaigns.length === 0 && <EmptyCampaignState />}
      {campaigns && campaigns.length > 0 && (
        <div className="mt-6 space-y-4">
          {campaigns.map((c) => <CampaignCard key={c.campaign_id} campaign={c} />)}
        </div>
      )}
    </div>
  );
}
```
(`ListSkeleton`, `ErrorBanner` are small shared primitives -- pulse-animated card outlines and a dismissible inline banner with a retry button respectively; trivial enough to omit full listings here.)

### Stage 3 -- `CampaignNew.tsx` wizard

**`apps/web/src/hooks/useInterviewStatus.ts`**, **`useImportInterview.ts`**, **`useHarnesses.ts`**, **`useCreateCampaign.ts`** -- thin `useQuery`/`useMutation` wrappers around the Stage 1 API functions, following the exact pattern of `useCampaigns` above. `useCreateCampaign` additionally invalidates the `["campaigns"]` query key on success so `CampaignList` reflects the new row immediately if the operator navigates back.

**`apps/web/src/components/campaign-new/ExistingSourcePanel.tsx`** -- key logic:
```tsx
const READY_STATES = new Set(["COMPONENTS_IN_PROGRESS", "PUBLISHED_DERIVATIVE_ELIGIBLE"]);

function ExistingSourcePanel({ onReady }: { onReady: (packageId: string) => void }) {
  const [packageId, setPackageId] = useState("");
  const { data, error, refetch, isFetching } = useInterviewStatus(packageId, { enabled: false });
  const isReady = data ? READY_STATES.has(data.lifecycle_state) : false;

  return (
    <div>
      <input value={packageId} onChange={(e) => setPackageId(e.target.value)} placeholder="Source package ID" />
      <button onClick={() => refetch()} disabled={!packageId || isFetching}>Check Status</button>
      {data && !isReady && (
        <InlineWarning>
          This source is at {data.lifecycle_state} -- needs at least one bound component before a campaign can use it.
        </InlineWarning>
      )}
      {error && <InlineError code={error.code} message={error.message} />}
      <button disabled={!isReady} onClick={() => onReady(packageId)}>Continue</button>
    </div>
  );
}
```

**`apps/web/src/components/campaign-new/HarnessPicker.tsx`** -- reconciles field names to confirmed API-002 §6 contract (Source Gap Notice 2 resolved 2026-07-27). Format-02 detection drops the `format_profile_id` subrule (not available in API-002's response) and the `generic`-mode exclusion (no `category_id`); the server's authoritative backstop handles those cases at submit time.
```tsx
function HarnessPicker({ onSelect }: { onSelect: (harness: HarnessSummary) => void }) {
  const { data: harnesses } = useHarnesses();
  return (
    <div className="grid grid-cols-3 gap-4">
      {(harnesses ?? []).map((h) => {
        // Best-effort client-side check: the `format_profile_id` subrule is intentionally
        // omitted — API-002 has no `format_profile_ids` field, so the server's authoritative
        // FORMAT02_DEFERRED backstop is the only protection for format-profile-gated cases.
        const deferred = h.category_id === "2d_character_animation" || h.mode === "generic";
        return (
          <button
            key={h.definition_id}
            disabled={deferred}
            onClick={() => onSelect(h)}
            className={deferred ? "opacity-40 cursor-not-allowed" : ""}
          >
            <div>{h.category_name ?? h.category_id}</div>
            <div className="text-ink-muted text-xs">v{h.manifest_version}</div>
            {deferred && <span className="text-state-blocked text-xs">Deferred</span>}
          </button>
        );
      })}
    </div>
  );
}
```

**`apps/web/src/components/campaign-new/OutputTargetsEditor.tsx`** -- a `useState<OutputTarget[]>([])` list with add/remove rows; "Launch" upstream is gated on `requireAtLeastOneOutputTarget(targets.length) === null`.

**`apps/web/src/pages/CampaignNew.tsx`** -- top-level wizard state machine (`step: 1 | 2`, `sourcePackageId`, `harness`, form fields, `idempotencyKey` generated via `useRef(() => crypto.randomUUID())` on first entry to the review screen, regenerated on any edit after a failed submit per §3) orchestrating the components above; omitted here in full to avoid restating every field binding already enumerated in §5/§6 -- the two sub-panels and `ConfigureStep` above are the parts with real logic worth pinning in code.

### Stage 4 -- Routing and wiring (reconciled to UI-001's actual file-based TanStack Router; Source Gap Notice 1 resolved 2026-07-27)

UI-001 uses `@tanstack/router-plugin/vite` to generate a `routeTree.gen.ts` from files under `apps/web/src/routes/`. Each route file exports a default component via `createFileRoute("/path")(...)`. This spec's route files therefore **replace** UI-001's existing placeholders at the same paths — they do not register into a separate imperative router table.

**`apps/web/src/routes/campaigns/index.tsx`** — replaces UI-001's placeholder for `/campaigns`; renders `CampaignList` from `../../pages/CampaignList`:
```tsx
import { createFileRoute } from "@tanstack/react-router";
import { CampaignList } from "../../pages/CampaignList";

export const Route = createFileRoute("/campaigns/")({
  component: CampaignList,
});
```

**`apps/web/src/routes/campaigns/new.tsx`** — replaces UI-001's placeholder for `/campaigns/new`; renders `CampaignNew` from `../../pages/CampaignNew`:
```tsx
import { createFileRoute } from "@tanstack/react-router";
import { CampaignNew } from "../../pages/CampaignNew";

export const Route = createFileRoute("/campaigns/new")({
  component: CampaignNew,
});
```

**`apps/web/src/routes/campaigns/$campaignId.tsx`** — **not modified by this spec.** This file already exists as UI-001's placeholder for FR-APP-060..064. `CampaignList.tsx`'s `Link to="/campaigns/$campaignId"` and `CampaignNew.tsx`'s successful-launch navigation target it; TS-APP-UI-003 overwrites it with the real `CampaignDetail.tsx` content. This spec intentionally does not stub a fake `CampaignDetail.tsx` here — a stub wired to fake data would be a worse placeholder than UI-001's honest empty placeholder.

**`apps/web/src/pages/CampaignList.tsx`** and **`apps/web/src/pages/CampaignNew.tsx``** — the page components (no route registration; consumed by the route files above). All other component/hook/lib files in this spec live under `apps/web/src/components/campaign-list/`, `components/campaign-new/`, `hooks/`, `lib/` as enumerated in §2 — those paths are unchanged from the original spec.

**`apps/web/vite.config.ts`** — reconciliation note (Source Gap Notice 1 resolved): UI-001 already proxies both `/api` and `/ws` to `http://localhost:8000` (the TS-APP-API-001 gateway). This spec's original Vite snippet showing only the `/api` proxy is **withdrawn**; UI-001's existing `server.proxy` block (which already covers `/api`) is sufficient — no additive change is needed here. The `fetch("/api/campaigns")` calls throughout §6/§7 now resolve through UI-001's already-configured proxy (same-origin in dev, no CORS dependency for the browser). `CA_PROJECT_SNAPSHOT.md` §8's own code sample is matched by UI-001's proxy, not by an additive addition this spec makes.

**Tailwind config and `index.css`** -- the token blocks from §5, added to whatever `tailwind.config.ts`/`index.css` UI-001 scaffolds (or created here if it does not yet exist by the time this spec is implemented).

**Tailwind config and `index.css`** -- the token blocks from §5, added to whatever `tailwind.config.ts`/`index.css` TS-APP-UI-001 scaffolds (or created here if it does not yet exist by the time this spec is implemented).

---

## 8. Failure, Migration, Rollback, Recovery, and Observability

| Failure scenario | Behaviour | Evidence |
|---|---|---|
| `GET /api/campaigns` unreachable / 5xx | List shows an inline error banner with "Retry"; no stale data silently presented | TanStack Query `isError` branch renders `ErrorBanner`, not a blank screen |
| Empty campaign list | Renders `EmptyCampaignState`, never treated as an error (matches API's "200 always, even empty") | `campaigns.length === 0` branch, distinct from `isError` |
| `package_id` typo / unknown source in Step 1a | `GET .../status` 404 -> inline `NOT_FOUND` shown next to the input, "Continue" stays disabled | `InlineError` renders `error.code` |
| Source found but not ready | "Continue" stays disabled with an explanatory warning quoting the actual `lifecycle_state` | client-side `READY_STATES` check, no wasted `POST` |
| Harness list fetch fails | `HarnessPicker` shows an error state; "Launch" stays disabled (no harness can be selected) | `useHarnesses` `isError` branch |
| Format 02 harness somehow selected anyway (e.g., picker cache stale) | Server's `FORMAT02_DEFERRED` on submit is still the authoritative backstop; UI returns operator to the picker with the same message | client check is a UX improvement, not the only enforcement |
| Double-click "Launch" before the first response returns | Same `idempotency_key` reused; server-side idempotent replay (`TS-APP-API-004` AC-009) returns the same campaign, not a duplicate | `idempotencyKey` held in a `useRef`, not regenerated per click |
| Network failure on `POST /api/campaigns` | Toast + "Retry," same `idempotency_key` reused | §3 idempotency-key lifecycle rule |
| `SOURCE_PACKAGE_NOT_READY` returned at submit despite passing Step 1's check (race: source changed between check and submit) | Operator is routed back to Step 1 with the live error, not left stuck on a Step 2 screen referencing a source that's no longer eligible | error-code routing table in §5 |

**Migration:** none. This spec introduces no persistence layer; every new file is additive frontend code.

**Rollback:** remove the two route entries from Stage 4's router registration; delete `apps/web/src/pages/CampaignList.tsx`, `CampaignNew.tsx`, and the `campaign-list/`, `campaign-new/` component directories, plus the Stage 1 `api/`/`hooks/`/`lib/` files this spec introduces. No other module is touched -- this spec never modifies a file it did not itself create, aside from one additive proxy line in `vite.config.ts` and one additive Tailwind theme extension, both trivially revertible.

**Observability:** relies on the browser console and TanStack Query Devtools (dev-only) for now; no telemetry/analytics pipeline is defined by this spec or any upstream spec. This is a stated claim-ceiling boundary (§3), not an oversight.

---

## 9. Acceptance Criteria

**AC-001 -- Campaign list renders with correct badges**
Given `GET /api/campaigns` returns three campaigns in `RUNNING`, `BLOCKED_EXCEPTION`, and `SHIPPED`,
When `CampaignList` mounts,
Then each `CampaignCard` shows the `LifecycleBadge` color/icon from §5's table for its state.
Test layer: component -- `CampaignList.test.tsx::renders_lifecycle_badges`.

**AC-002 -- Empty list is not an error state**
Given `GET /api/campaigns` returns `[]`,
When `CampaignList` mounts,
Then `EmptyCampaignState` renders, and no error banner is shown.
Test layer: component -- `renders_empty_state_not_error`.

**AC-003 -- Lifecycle filter refetches with the correct query param**
Given the list is showing all campaigns,
When the operator clicks the `RUNNING` filter chip,
Then a new request is made to `GET /api/campaigns?lifecycle_state=RUNNING` and only matching rows render.
Test layer: component (MSW request assertion) -- `filter_chip_sets_query_param`.

**AC-004 -- Campaign row navigates to the detail route contract**
When a `CampaignCard` is clicked,
Then the router navigates to `/campaigns/{campaign_id}` using that exact campaign's ID.
Test layer: component (router mock) -- `card_click_navigates_to_detail_route`.

**AC-005 -- Existing-source check enables Continue only when ready**
Given `GET /api/interviews/{id}/status` returns `lifecycle_state: "ADMITTED"`,
When "Check Status" is clicked,
Then a warning renders and "Continue" remains disabled;
Given the same call instead returns `"COMPONENTS_IN_PROGRESS"`,
Then "Continue" becomes enabled.
Test layer: component -- `existing_source_gates_continue_on_readiness`.

**AC-006 -- Unknown source package shows the real error inline**
Given `GET /api/interviews/{id}/status` returns 404 `NOT_FOUND`,
When "Check Status" is clicked,
Then the panel shows that error code and message, not a generic failure.
Test layer: component -- `unknown_source_shows_not_found`.

**AC-007 -- Import panel success advances the wizard**
Given `POST /api/interviews/import` returns 201 with a `package_id`,
When the import form is submitted with valid files and fields,
Then the same summary card `ExistingSourcePanel` uses renders with that response's data, and "Continue" is enabled.
Test layer: component (MSW multipart mock) -- `import_success_unlocks_continue`.

**AC-008 -- Format 02 harnesses are disabled in the picker**
Given `GET /api/harnesses` returns one harness with `category_id: "2d_character_animation"`,
When `HarnessPicker` renders,
Then that card is disabled and labeled "Deferred," and clicking it does not call `onSelect`.
Test layer: component -- `format02_harness_is_disabled`.

**AC-009 -- Output target requirement blocks Launch client-side**
Given zero output targets have been added,
When the operator reaches the review screen,
Then "Launch Campaign" is disabled and no `POST /api/campaigns` call is ever made.
Test layer: component -- `launch_disabled_without_output_target`.

**AC-010 -- Idempotency key is stable across a double-click**
Given the review screen has generated an `idempotency_key`,
When "Launch Campaign" is clicked twice in rapid succession (before the first response resolves),
Then both underlying `fetch` calls (if the double-click isn't already debounced at the UI layer) carry the identical `idempotency_key` value.
Test layer: component (fetch spy) -- `idempotency_key_stable_across_double_click`.

**AC-011 -- Successful launch navigates to the campaign detail route**
Given `POST /api/campaigns` returns 201 with `state.campaign_id: "campaign:abc"`,
When Launch succeeds,
Then the router navigates to `/campaigns/campaign:abc`.
Test layer: component (router mock) -- `launch_success_navigates_to_detail`.

**AC-012 -- Server-side SOURCE_PACKAGE_NOT_READY on submit returns operator to Step 1**
Given the source passed its Step 1 check but the server rejects the eventual submit with 422 `SOURCE_PACKAGE_NOT_READY` (simulating a race),
When Launch is clicked,
Then the wizard returns to Step 1 and shows that error inline on the source summary card, per the routing table in §5.
Test layer: component -- `submit_time_source_not_ready_routes_back_to_step1`.

**AC-013 -- Network failure preserves the idempotency key for retry**
Given `POST /api/campaigns` fails with a network error,
When the operator clicks "Retry" on the resulting toast,
Then the retried request carries the same `idempotency_key` as the original attempt.
Test layer: component (fetch spy across two calls) -- `retry_reuses_idempotency_key`.

**AC-014 -- No regression to the existing backend test suite**
Given the Python backend test suite passes before this spec,
When this spec (a frontend-only change) is fully implemented,
Then `python -m pytest tests/ -q` still passes unchanged, since this spec touches zero backend files.
Test layer: regression -- run full existing suite.

---

## 10. Testing and Completion Evidence

### Test files to create

**`apps/web/src/lib/campaignFormValidation.test.ts`** (pure unit tests, no DOM)
- `requireNonEmpty`, `requirePositiveInteger`, `requireAtLeastOneOutputTarget`, `isFormat02Deferred` -- one test per rule, cross-checked by hand against `validators.ts`'s equivalent assertions (no automated cross-check is possible without importing the Node-only module -- see Source Gap Notice 3 -- so this parity is a manual review gate, noted explicitly here rather than silently assumed)

**`apps/web/src/components/campaign-list/CampaignList.test.tsx`** -- AC-001, AC-002, AC-003, AC-004

**`apps/web/src/components/campaign-new/ExistingSourcePanel.test.tsx`** -- AC-005, AC-006

**`apps/web/src/components/campaign-new/ImportInterviewPanel.test.tsx`** -- AC-007

**`apps/web/src/components/campaign-new/HarnessPicker.test.tsx`** -- AC-008

**`apps/web/src/pages/CampaignNew.test.tsx`** -- AC-009, AC-010, AC-011, AC-012, AC-013

### Test tooling

Vitest + React Testing Library + MSW (Mock Service Worker), stubbing exactly the JSON bodies `TS-APP-API-003.md`/`TS-APP-API-004.md` §6 already committed to in their own positive/negative examples -- reusing those literal fixture bodies keeps the frontend tests pinned to the same contract text the backend specs authored, rather than to a frontend author's guess at the shape:

```ts
// apps/web/src/test/handlers.ts
import { http, HttpResponse } from "msw";

export const handlers = [
  http.get("/api/campaigns", () => HttpResponse.json([])),
  http.post("/api/campaigns", () => HttpResponse.json({
    // literal body reused from TS-APP-API-004.md §6 positive example
    order: { /* ... */ }, state: { campaign_id: "campaign:1a2b3c4d5e6f70819293", lifecycle_state: "LAUNCHED", version: 1, /* ... */ },
    source_derivative_eligible: false, source_lifecycle_state: "COMPONENTS_IN_PROGRESS",
    pipeline_ingestion_status: "NOT_YET_TRIGGERED", idempotent_replay: false,
  }, { status: 201 })),
  http.get("/api/interviews/:id/status", ({ params }) =>
    params.id === "unknown"
      ? HttpResponse.json({ error_code: "NOT_FOUND", message: "object not found", service: null, timestamp: new Date().toISOString() }, { status: 404 })
      : HttpResponse.json({ package_id: params.id, lifecycle_state: "COMPONENTS_IN_PROGRESS", admission_mode: "IMPORTED", derivative_eligible: false, revision: 1 })),
];
```

### Pre-existing regression
```bash
python -m pytest tests/ -q --tb=short
```
Zero new failures is a hard gate (AC-014) -- this spec makes no backend changes, so this run should be a no-op diff.

### Build Receipt claim ceiling
`CAMPAIGN_LIST_CREATE_UI_ASSUMED_SCAFFOLD_EVIDENCE`

This spec does not claim:
- that `TS-APP-UI-001`'s actual scaffold matches the router/build assumptions made in §7 Stage 4 (Source Gap Notice 1, unresolved)
- that `HarnessSummary`'s field names match the real `GET /api/harnesses` response (Source Gap Notice 2, unresolved -- must be reconciled before Stage 3 ships)
- that a launched campaign has triggered real Pipeline execution (inherited from `TS-APP-API-004` -- this UI surfaces `pipeline_ingestion_status: "NOT_YET_TRIGGERED"` transparently and never claims otherwise)
- accessibility auditing beyond baseline keyboard focus order, authentication, or production CORS/security hardening

---
spec_end: true
next_spec: TS-APP-UI-004 (Harness Library UI) or TS-APP-UI-003 (Control Tower UI) -- either may proceed once TS-APP-API-002 is actually read; TS-APP-UI-003 additionally needs TS-APP-API-005/006
prerequisite_for_next: AC-001, AC-004, AC-011 must pass (a campaign can be listed, navigated into, and created) before TS-APP-UI-003 has anything real to land its Control Tower page on
blocking_risk_for_downstream: Source Gap Notice 1 (TS-APP-UI-001 not yet written) means every Stage 4 wiring step in this spec is provisional; Source Gap Notice 2 (TS-APP-API-002 not read) means HarnessPicker's data contract must be reconciled before Stage 3 is implemented, not after. Neither gap is this spec's to close -- the former belongs to TS-APP-UI-001's author, the latter to whoever next reads TS-APP-API-002.md in full.
open_question_for_next_spec_author: should `HarnessSummary` and `HarnessPicker`'s card visual language be extracted into a small shared package/module once TS-APP-API-002 is actually read, so `TS-APP-UI-004`'s full Harness Library page and this spec's compact inline picker don't independently drift from the real contract in two different directions? This spec deliberately leaves that factoring decision to whichever of TS-APP-UI-003/004 is authored next, rather than guessing at a shared-component boundary neither spec's author has confirmed is worth it.
---
