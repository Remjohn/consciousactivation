---
document_class: SPEC_GAP_LEDGER
product: Conscious Activations
version: 1.1
status: ACTIVE
prepared: 2026-07-25
updated: 2026-07-27
purpose: >
  Catalog every cross-spec gap discovered while reading TS-APP-API-001 through
  TS-APP-UI-004 against each other. This is the same gap-closure pattern the
  project already used once, in CONSCIOUS_ACTIVATIONS_PHASE_01_03_TRACEABILITY_
  AND_GAP_CLOSURE_BUNDLE — applied here one layer earlier, at spec-authoring
  time instead of after implementation. Read this before implementing ANY
  spec that appears in the "blocks" column below.
scope_note: >
  This ledger does not rewrite any of the twelve existing specs. Each one made
  an honest, documented claim-ceiling decision when it hit a gap. This
  document exists so those decisions are visible in one place instead of
  buried in ten different "Source Gap Notice" sections.
---

# Conscious Activations — Spec Gap Ledger

## How to use this document

Each row is one gap. "Blocks" lists what cannot be truthfully claimed complete
until the gap closes. "Resolution" is what needs to be written or decided —
not yet written unless marked DONE.

---

## GAP-001 — No Activative Intelligence (AIR) HTTP API exists anywhere in the spec queue

**Severity: CRITICAL — blocks real Pipeline execution entirely**

**Discovered in:** TS-APP-API-004, Source Gap Notice 2

**What happened:** `ContentBatchService.compile_batch()` — the actual function
that starts a Pipeline run — requires `final_script_ref`,
`archetype_coalition_ref`, `primitive_coalition_ref`, and
`activation_transfer_contract_ref`. All four come from AIR. `CA_APP_FR_EPIC_
SPEC_PLAN.md` Part 4 never listed a Tech Spec for exposing AIR over HTTP —
Wave 1 and Wave 2 only cover Harness, Interview, Campaign, Pipeline-status,
and Supervision APIs.

**Consequence:** TS-APP-API-004 correctly refused to fake this. Every campaign
it creates carries `pipeline_ingestion_status: "NOT_YET_TRIGGERED"` forever.
As the spec set stands today, **no campaign created through this API can ever
actually execute a Pipeline run.** This is the single largest gap in the set.

**Blocks:**
- TS-APP-API-005 (Pipeline Status WebSocket) — has nothing real to report on
- TS-APP-API-006 (Control Tower) — Control Tower would show a permanently
  stalled campaign
- The entire Epic 7 ("Launch and Monitor a Production Campaign") value
  proposition in `CA_APP_FR_EPIC_SPEC_PLAN.md`
- Gate C ("A campaign runs and produces a real FFmpeg-cut MP4") in Part 7 of
  the FR plan

**Resolution required:** A new Tech Spec, **TS-APP-API-007 — Activative
Intelligence API**, covering at minimum:
- `GET /api/air/hypotheses/{package_id}` — list Activation Hypothesis Portfolio
- `POST /api/air/hypotheses/{id}/select` — operator selects one
- `GET /api/air/scripts/{id}` — Final Script review
- `POST /api/air/scripts/{id}/approve` — operator approval gate (FR-APP-032)
- A response shape exposing exactly the four refs `compile_batch()` needs,
  in the exact field names it expects (verify against
  `services/air/src/cmf_activative_intelligence/services/derivative_service.py`
  and `services/pipeline/src/cmf_pipeline/batch/service.py` directly — do not
  infer)

**Status:** SPEC WRITTEN — `TS-APP-API-007.md` now exists at
`docs/tech-specs/TS-APP-API-007.md` (quality_state: WRITTEN_PENDING_AUDIT);
its frontmatter declares itself "the direct resolution of GAP-001."
GAP-001 therefore moves from NOT-WRITTEN to IMPLEMENTATION-PENDING.
It cannot be implemented until TS-APP-API-001 exists, because API-007's
frontmatter lists `api/dependencies.py::get_air`, `api/config.py::AppConfig`,
and `api/errors.py::ErrorResponse` as upstream interfaces only API-001
creates. Once API-001 is implemented, API-007 closes GAP-001. After that,
TS-APP-API-004's `compile_batch()` Stage should be revisited — small patch,
not a rewrite: call the now-real AIR API instead of leaving
`pipeline_ingestion_status` permanently `NOT_YET_TRIGGERED` (this is the
same revisit the Resolution Sequence below already named, renumbered).

---

## GAP-002 — Builder output and Pipeline input are structurally incompatible

**Severity: CRITICAL — blocks Harness execution entirely**

**Discovered in:** TS-APP-API-002, "Gap 4"; independently re-confirmed by
TS-APP-API-004 (Source Gap Notice 1) and TS-APP-API-005 (flagged as blocking)

**What happened:** `POST /api/harnesses/build` (TS-APP-API-002) produces a
`PortableAtomicHarnessDefinition` whose content nests category under
`category_binding.category_id` and has no `workflow.nodes/edges` or
`capabilities[]` in the shape the Pipeline's `AtomicHarnessDefinitionIntake`
requires. **A Harness built through the API today cannot be ingested by the
Pipeline as-is.**

**Consequence:** Even once GAP-001 is closed and AIR can supply the refs
`compile_batch()` needs, the Harness itself — the thing that defines *how*
to execute — still cannot be loaded by the Pipeline. This gap and GAP-001
are independent; both must close before a campaign can run for real.

**Blocks:**
- TS-APP-API-004's `pipeline_ingestion_status` can never leave
  `NOT_YET_TRIGGERED` even after GAP-001 closes, until this also closes
- TS-APP-API-005 — flagged explicitly as **BLOCKED** by TS-APP-API-002's own
  author
- Epic 6 ("Manage the Harness Library") value proposition — a Harness the
  Pipeline can't run isn't usable yet
- Gate H ("Pi Coding Agent can POST a new Harness via API") in the FR plan

**Resolution required:** A translation/compiler layer between
`PortableAtomicHarnessDefinition` and `AtomicHarnessDefinitionIntake.
REQUIRED_KEYS`. TS-APP-API-002's own author was correct that this is "a
domain decision, not an HTTP-wrapping decision" — it does not belong inside
`api/routers/harnesses.py`. It belongs as new logic inside `cmf_pipeline` or
a new shared adapter package.

**Proposed new spec:** **TS-APP-BRIDGE-001 — Harness Definition Compiler**
(Python-only, no new HTTP routes), covering:
- Read both schemas exactly (`services/builder/src/cmf_builder/skills/
  portable_package.py` and `services/pipeline/src/cmf_pipeline/intake/
  definition_intake.py` — read these directly, do not infer field names)
- Write `compile_portable_to_intake(definition: PortableAtomicHarnessDefinition)
  -> AtomicHarnessDefinitionIntake` as a pure function
- Decide and document: does `workflow.nodes/edges` get derived automatically
  from the Builder's `task` object, or does the Builder need a new required
  field? This is a real product decision, not a mechanical mapping — flag
  for human decision if the two schemas don't have an obvious 1:1 mapping.

**Status:** DONE (2026-07-27) — TS-APP-BRIDGE-001 implemented in
`services/pipeline/src/cmf_pipeline/intake/harness_compiler.py` plus
`harness_compiler_contracts.py`. All 11 ACs verified by 17 pytest
assertions in `tests/pipeline/test_harness_compiler.py` (17/17 pass);
phase 9 regression suite shows no new failures (the same 2
PRM-HUM-006 hash-mismatch tests that failed pre-implementation still
fail — they fail content-integrity in AIR's primitive registry, unrelated
to this compiler). The compiler enforces all 7 blockers from §4 by raising
`HarnessCompilationBlocked(field, reason, blocker_ref)`; the four "no
source" blockers (1, 2, 5, 6) require caller-supplied params, Blocker 3
rejects generic-mode, Blocker 4 validates semver, Blocker 7 defaults
`invalidation_state` to `"NOT_INVALIDATED"`. Per §11 of the spec, the
compiler will raise `HarnessCompilationBlocked(field="workflow")` on
every real call until Blocker 5's human decision is made — that was the
spec author's explicit intent, documented in `BLOCKER_5_TEXT`, and is
NOT a defect. GAP-002 is therefore closed at claim ceiling
`HARNESS_COMPILER_PARTIAL_BRIDGE_EVIDENCE` (the narrower recognition this
spec honestly earns per §5), not at full GAP-closed.

---

## GAP-003 — Specs were authored out of dependency order, producing unverified "assumed interface" contracts

**Severity: MODERATE — will cause silent integration failures if implemented as-is**

**Discovered in:** TS-APP-UI-002 (Source Gap Notice 1 and 2), TS-APP-UI-003
(entire dependency section)

**What happened:**
- TS-APP-UI-002 was written before TS-APP-API-002 existed. Its `HarnessSummary`
  interface is explicitly labeled "inferred, not confirmed" — reconstructed
  from second-hand citations in TS-APP-API-004, not from reading
  TS-APP-API-002 itself.
- TS-APP-UI-002 was also written before TS-APP-UI-001 existed. Every Stage 4
  wiring step (router setup, `main.tsx`, `vite.config.ts`) is against an
  "assumed foundation," explicitly flagged `ASSUMED_INTERFACE_PENDING_UI_001`.
- TS-APP-UI-003 was written before both TS-APP-UI-001 AND TS-APP-UI-002
  existed, compounding the same problem one layer further.

**Consequence:** If an agent implements TS-APP-UI-002 today, `HarnessSummary`'s
field names are a guess. If TS-APP-API-002's real response uses
`definition_id` where TS-APP-UI-002 guessed `harness_definition_id` (or any
other mismatch), the Harness picker will silently render empty — no error,
no crash, just a blank list. This is worse than a build failure because it
looks like it's working.

**Blocks:** Correct implementation of TS-APP-UI-002 and TS-APP-UI-003 without
manual reconciliation first.

**Resolution required — this one does NOT need a new spec.** It needs a
**reconciliation pass**, done once, before implementation begins:

1. Read `TS-APP-API-002.md` §6 (the real `HarnessSummary`/`HarnessDetail`
   response shape) side by side with `TS-APP-UI-002.md` §6 (the guessed
   shape).
2. Where they differ, patch `TS-APP-UI-002.md` §6 and any code in §7 that
   references the wrong field name. This is a targeted edit, not a rewrite.
3. Do the same for `TS-APP-UI-003.md` against the real `TS-APP-UI-001.md`
   (router pattern, `apiFetch` signature, design token names) and against
   `TS-APP-UI-002.md` (does `CampaignList.tsx` link to `/campaigns/:id`
   exactly the way `CampaignDetail.tsx` expects to receive it?).
4. Mark each reconciled spec's `quality_state` from `WRITTEN_PENDING_AUDIT`
   to `RECONCILED_PENDING_AUDIT` once done, so a future reader knows this
   pass happened.

**Status:** DONE (2026-07-27). The reconciliation pass has been applied in full.
Both `TS-APP-UI-002.md` and `TS-APP-UI-003.md` have had their `quality_state`
flipped from `WRITTEN_PENDING_AUDIT` to `RECONCILED_PENDING_AUDIT`. Claim
ceiling for this reconciliation pass: `GAP_003_RECONCILIATION_EVIDENCE`
(spec-edit only, no code changed, no tests run — both specs remain
`RECONCILED_*PENDING_AUDIT*` rather than `RECONCILED_AUDITED` because a human
audit pass against the running system has not yet been performed).

**What was reconciled (evidence trail):**

TS-APP-UI-002 against TS-APP-API-002 §6 (the previously-inferred `HarnessSummary`
interface):

  1. `harness_definition_id` (UI-002 guess) → `definition_id` (API-002 real).
     This is the field whose value the operator's `POST /api/campaigns` body
     sends under the field name `harness_definition_id` (per API-004 §6
     `CampaignCreateRequest`) — the naming asymmetry between API-002's response
     field and API-004's request field is a real API design choice, not a
     UI-002 naming bug. `HarnessPicker.tsx` now reads `h.definition_id`.
  2. `version` (UI-002 guess) → `manifest_version` (API-002 real).
  3. `capability_ids` (UI-002 guess) → `capability_requirements` (API-002 real).
  4. `format_profile_ids: string[]` (UI-002 guess) → **does not exist** in
     API-002's response (API-002 §10 explicitly notes format-profile awareness
     is unavailable against the Builder's exported shape). UI-002's Picker
     Format-02 detection narrows to its `category_id ===
     "2d_character_animation"` subrule only; cases gated purely on
     `format_profile_id` are delegated to the server's authoritative
     `FORMAT02_DEFERRED` backstop at submit time. The narrowing is honest, not
     a silent gap.
  5. UI-002's prior `HarnessSummary` was missing seven real fields API-002
     does return: `mode` (essential — generic-mode Harnesses have
     `category_id: null` and must not be selectable for an activative campaign,
     matching API-002's `NOT_APPLICABLE` eligibility semantics), `category_name`,
     `classification`, `production_ready`, `certified`, `package_file`,
     `package_hash`, `added_at`. All seven were added.

TS-APP-UI-002 against TS-APP-UI-001 (the previously-assumed scaffold):

  6. UI-002's invented `parseJsonOrThrow` helper in `apps/web/src/api/errors.ts`
     is withdrawn. UI-001 owns the typed-error path as `apiFetch<T>(path, init?)
     in `apps/web/src/api/http.ts`, throwing `ApiError` on non-2xx. UI-002's
     `api/campaigns.ts`, `api/interviews.ts`, `api/harnesses.ts` Stage 1
     blocks were rewritten to call `apiFetch` instead of the withdrawn helper.
  7. UI-002's Stage 4 routing table (`apps/web/src/router.tsx` with imperative
     `{ path, component: () => import(...) }` entries) is withdrawn. UI-001 uses
     TanStack's file-based router under `apps/web/src/routes/` generated by
     `@tanstack/router-plugin/vite`, with route files at
     `routes/campaigns/index.tsx`, `routes/campaigns/new.tsx`, and the
     UI-001-owned `routes/campaigns/$campaignId.tsx` placeholder (which
     TS-APP-UI-003 will overwrite, not UI-002). UI-002's pages still live at
     `apps/web/src/pages/CampaignList.tsx` and `CampaignNew.tsx`; they are
     imported and re-exported from the new route files via `createFileRoute`.
  8. UI-002's additive `vite.config.ts` snippet (proxy `/api` to
     `localhost:8000`) is withdrawn — UI-001 already proxies both `/api` and
     `/ws`, so no additive change is needed.

TS-APP-UI-003 against TS-APP-UI-001:

  9. UI-003's invented `apiGet<T>`/`apiPost<T>` helpers in
     `apps/web/src/api/campaigns.ts::CampaignsApi` are replaced with
     UI-001's `apiFetch<T>(path, init?)`, including explicit `method`,
     `Content-Type`, and `body` for the three POST routes (`compileRevision`,
     `executeRevision`, `resolveException`).
 10. UI-003 §4 Brownfield rows for `apps/web/src/api/client.ts` (typed fetch
     wrapper) and the TanStack Router route tree were flipped from
     `ASSUMED_INTERFACE_PENDING_UI_001` to `RECONCILED` — both confirmed by
     reading UI-001 in full. The route file path
     `apps/web/src/routes/campaigns/$campaignId.tsx` (which UI-003 overwrites
     per its own §8 Stage 5) was confirmed against UI-001's scaffold.
 11. UI-003's `@studio/domain` alias and UI-001's `@ca/studio` alias are
     flagged as the same tsconfig `paths` entry under two naming variants —
     one canonical name must be pinned by UI-001's author during scaffold
     build. No source-code change in UI-003 until that pin lands.

**Out-of-scope for GAP-003 (NOT closed by this pass):**

  - UI-002 §3's `FORMAT02_DEFERRED` error-code reference inherits a separate
    API-004↔validators.ts wiring question that this reconciliation pass did not
    audit; UI-002's wiring note in §3 (server's authoritative backstop) is
    preserved as the safety net while that question waits for an API-004 audit.
  - The `@studio/domain` vs `@ca/studio` alias naming is left for UI-001's
    scaffold-build pass to pin; UI-003's spec text continues to use
    `@studio/domain` and UI-002's continues to use `@ca/studio` until then.
  - The `HarnessSummary` ↔ `HarnessCard` shared-component factoring decision
    UI-002's footer posed for TS-APP-UI-004 is not closed by this pass — it
    correctly belongs to TS-APP-UI-004 when it ships against the now-confirmed
    API-002 contract.

This reconciliation pass touched only `docs/tech-specs/TS-APP-UI-002.md`,
`docs/tech-specs/TS-APP-UI-003.md`, and `docs/tech-specs/SPEC_GAP_LEDGER.md` —
no code, no tests, no other specs. It ran in this session concurrently with
GAP-002 implementation (the user-requested plan called for the two to run in
parallel since they touch no overlapping files: BRIDGE-001 touches
`services/pipeline/src/...`; GAP-003 touches only `docs/tech-specs/*.md`).

---

## GAP-004 — `module` front-matter field is inconsistent across specs

**Severity: LOW — cosmetic, but will confuse spec indexing/tooling**

**Discovered in:** direct grep across all twelve specs' front matter

**What happened:**

| Spec | `module:` value |
|---|---|
| TS-APP-API-001 through TS-APP-API-006 | `api` |
| TS-APP-UI-001 | `web` |
| TS-APP-UI-002 | `web` |
| TS-APP-UI-003 | `apps/web` |
| TS-APP-UI-004 | `web` |

Three different conventions for what should be two consistent values.

**Blocks:** Nothing functionally — this is metadata, not implementation. But
it will break any future `docs/specs/current/SPEC_INDEX.yaml` tooling that
groups specs by module, and it's the same inconsistency you flagged in the
directory structure itself, now showing up in the specs about the directory
structure.

**Resolution required:** Standardize on `api` and `web` (not `apps/web` —
the directory is `apps/web/` but the module label should be the short form,
matching the other eleven specs). Edit `TS-APP-UI-003.md` front matter:
`module: apps/web` → `module: web`.

**Status:** DONE (2026-07-27). The one-line fix was applied to
`docs/tech-specs/TS-APP-UI-003.md` front matter during the TS-APP-SETUP-001
implementation pass. All twelve TS-APP-* specs now use `api` (API-001 through
API-007), `web` (UI-001 through UI-004), `repo` (SETUP-001), or `bridge`
(BRIDGE-001) — no `apps/web` remaining.

---

## GAP-005 — Hash format mismatch between Harness Library and Studio schemas

**Severity: LOW — already resolved by TS-APP-API-004, noted for awareness**

**Discovered in:** TS-APP-API-004, Source Gap Notice 4

**What happened:** `HarnessDetail.definition_hash` is formatted
`f"sha256:{digest}"` by `cmf_builder`, but Studio's
`campaign_order.schema.json` requires a bare 64-character hex digest with no
prefix.

**Resolution:** TS-APP-API-004 already handles this — it strips the
`sha256:` prefix when constructing `harness_ref` in its own router code.
This is a projection, not a schema change, and does not require either
upstream module to change.

**Status:** DONE — no action needed. Listed here only so the pattern
("format mismatch caught and handled locally, not propagated upstream") is
visible alongside the two unresolved gaps above, in case the same pattern
recurs elsewhere during implementation.

---

## GAP-006 — Studio TypeScript modules are not browser-safe

**Severity: LOW — already resolved by TS-APP-UI-002, noted for awareness**

**Discovered in:** TS-APP-UI-002, Source Gap Notice 3

**What happened:** `services/studio/src/canonical.ts` imports Node's
`node:crypto` at module top level. Any file that transitively imports it
(`validators.ts`, `campaign.ts`) cannot run in a Vite browser bundle without
a polyfill.

**Resolution:** TS-APP-UI-002 already handles this correctly — it uses
`import type` only (erases at compile time, zero runtime dependency) for
anything from those files, and reimplements the specific pure validation
rules it needs locally in `apps/web/src/lib/campaignFormValidation.ts`. ID
minting (`order_id`/`campaign_id`) is confirmed server-side only; the
browser only generates a random `idempotency_key` via
`crypto.randomUUID()` (browser-native, no Node dependency).

**Status:** DONE — no action needed. Any future UI spec that touches
`services/studio/src/*.ts` should follow the same `import type`-only pattern.

---

## Resolution Sequence

Updated 2026-07-27. TS-APP-SETUP-001 implemented (claim ceiling
`REPOSITORY_STRUCTURE_CLEANUP_EVIDENCE`; all ACs pass; services/{name} and
governance/program-control paths live). TS-APP-BRIDGE-001 implemented
(claim ceiling `HARNESS_COMPILER_PARTIAL_BRIDGE_EVIDENCE`; 17/17 AC tests
pass; phase 9 zero new regressions). Of the two specs this sequence
originally called "still need to be written" (`TS-APP-BRIDGE-001` and
`TS-APP-API-007`), BRIDGE-001 is now fully done and API-007 exists as
`WRITTEN_PENDING_AUDIT`, implementable only after step 5 (API-001)
provides the FastAPI gateway interfaces its upstream dependencies name.
The sequence below is therefore implementation-only. Gaps that can
close without HTTP are done first, so the API wave begins on a
foundation with no known gap lurking.

```
1. [DONE] TS-APP-SETUP-001 (repository restructure) — implemented 2026-07-27
2. [DONE] GAP-004 fix (module field)                 — closed during #1 setup
   Applied 2026-07-27: `module: apps/web` → `module: web` in
   TS-APP-UI-003.md front matter. Verified — no `apps/web` form remains.
3. [DONE] Implement TS-APP-BRIDGE-001                — closes GAP-002
   Implemented 2026-07-27. Output:
   `services/pipeline/src/cmf_pipeline/intake/harness_compiler.py`
   + `harness_compiler_contracts.py`. 17/17 AC tests pass; phase 9
   shows zero new regressions. Claim ceiling:
   `HARNESS_COMPILER_PARTIAL_BRIDGE_EVIDENCE` (per spec §5 — Blocker 5
   is escalated, not decided, so the compiler raises by design until
   that human decision is made).
4. [DONE] GAP-003 reconciliation pass                — closed 2026-07-27
   Applied to TS-APP-UI-002 + TS-APP-UI-003:
   * UI-002 HarnessSummary reconciled field-for-field against API-002 §6
     (5 corrections: harness_definition_id→definition_id, version→manifest_version,
     capability_ids→capability_requirements, format_profile_ids removed
     (does not exist in API-002), and 7 real fields added including essential
     `mode`). Both specs now carry quality_state: RECONCILED_PENDING_AUDIT.
   * UI-002's Stage 1 errors.ts/parseJsonOrThrow and Stage 4 routing-table
     withdrawn; rewritten to use UI-001's apiFetch<T>(path, init?) from
     src/api/http.ts and TanStack Router's file-based routes under
     apps/web/src/routes/.
   * UI-003's apiGet/apiPost helpers in CampaignsApi replaced with apiFetch.
     UI-003 §4 Brownfield rows for api/client.ts and the router tree flipped
     from ASSUMED_INTERFACE_PENDING_UI_001 to RECONCILED.
   See GAP-003 status block above for the full evidence trail.
5. Implement TS-APP-API-001                          — FastAPI gateway
   Now safe: paths exist, BRIDGE-001 is in place, GAP-003 is closed.
   Creates api/dependencies.py, api/config.py, api/errors.py that
   API-007 needs.
6. Implement TS-APP-API-002, TS-APP-API-003          — parallel, both only need -001
7. Implement TS-APP-API-007                          — closes GAP-001
   Needs API-001's get_air/AppConfig/ErrorResponse interfaces (step 5).
8. Revisit TS-APP-API-004 Stage covering compile_batch()
   — small patch, not a rewrite: call the now-real AIR API (step 7) + Bridge
     compiler (step 3) instead of leaving pipeline_ingestion_status
     permanently NOT_YET_TRIGGERED
9. Implement TS-APP-API-004, then -005, then -006    — in that order
10. Implement TS-APP-UI-001                          — scaffold
11. Implement TS-APP-UI-002 (reconciled)             — campaign list/create
12. Implement TS-APP-UI-004 (harness library UI)     — only needs UI-001 + API-002
13. Implement TS-APP-UI-003 (reconciled)             — control tower, needs everything above
```

**No specs remain to be written.** All twelve TS-APP-* specs
(SETUP-001, BRIDGE-001, API-001 through API-007, UI-001 through UI-004)
exist as `WRITTEN_PENDING_AUDIT` (except UI-002 and UI-003 which are now
`RECONCILED_PENDING_AUDIT` after the GAP-003 pass). All three closeable
gaps (GAP-002, GAP-003, GAP-004) are now closed. Gate C (a campaign that
actually executes) becomes reachable after steps 5, 7, and 8 — steps 3
(BRIDGE-001) and 4 (GAP-003 reconciliation) are already done.

---
document_end: true
next_action: >
  Implement TS-APP-API-001 next (FastAPI gateway, wave 1, first HTTP
  layer). Now safe: BRIDGE-001 is in place, GAP-003 is closed, paths
  exist (SETUP-001 done). API-001's outputs (api/dependencies.py with
  get_air(), api/config.py with AppConfig, api/errors.py with ErrorResponse)
  are what TS-APP-API-007 needs to close GAP-001 — the last open gap
  between current state and a campaign that actually executes
  (Gate C). After API-001, run API-002 and API-003 in parallel, then
  API-007, then revisit TS-APP-API-004's Stage covering compile_batch()
  to point it at the now-real AIR API and Bridge compiler. Note: BRIDGE-001's
  `compile_portable_to_intake()` still raises by design on `workflow`
  (Blocker 5) until a human product decision is made — that decision is
  independent of the API wave and can run in parallel with steps 5–8 if
  a human wants to make the call.
