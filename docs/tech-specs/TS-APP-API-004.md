---
spec_id: TS-APP-API-004
title: Campaign CRUD API
document_class: TECH_SPEC
product: Conscious Activations
module: api
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CURRENT
build_authority: false
controlling_frs:
  - FR-APP-050 (Campaign Order creation)
controlling_stories:
  - ST-APP-07.01 (create a Campaign Order)
upstream_dependencies:
  - CA_PROJECT_SNAPSHOT_V2.md (authority — CURRENT)
  - CA_APP_FR_EPIC_SPEC_PLAN.md (authority — CURRENT)
  - TS-APP-API-001.md (quality_state: WRITTEN_PENDING_AUDIT — DRAFT_DEPENDENCY_NOT_ACCEPTED; this spec depends only on `api/dependencies.py::get_interview`/`get_harness_library_root`, `api/config.py::AppConfig`, and `api/errors.py::ErrorResponse`, not on any claim that the gateway is production-ready)
  - TS-APP-API-002.md (quality_state: WRITTEN_PENDING_AUDIT — DRAFT_DEPENDENCY_NOT_ACCEPTED; this spec depends on `api/harness_library.py::find_by_definition_id` and inherits Gap 4 unresolved, see Source Gap Notice 1)
  - TS-APP-API-003.md (quality_state: WRITTEN_PENDING_AUDIT — DRAFT_DEPENDENCY_NOT_ACCEPTED; this spec depends on `InterviewExpressionApplication.repository.get_object()` and resolves the open question TS-APP-API-003 left for this spec, see Source Gap Notice 3)
downstream_consumers:
  - TS-APP-API-005 (Pipeline Status WebSocket — needs a `campaign_id` to subscribe against; cannot report real node status until Source Gap Notice 2 is closed)
  - TS-APP-API-006 (Control Tower and Supervision API — needs `campaign_id`/`order_ref` to assemble a ControlTowerProjection; needs `transition_campaign` reused, not reimplemented)
  - TS-APP-UI-002 (Campaign List and Creation UI — CampaignList.tsx and CampaignNew.tsx call these endpoints directly)
output_path: api/routers/campaigns.py (and supporting files listed in section 7)
wave: 2
---

# TS-APP-API-004 — Campaign CRUD API

## 1. Files and Authorities Read

| File | SHA-256 (short) | Status | Fact extracted |
|---|---|---|---|
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/domain.ts` | `f1a4c9e2` | READ — CURRENT IMPLEMENTATION | `CampaignOrder`, `CampaignState`, `AutonomyPolicy`, `OutputTarget` field shapes; `CampaignLifecycleState` has 8 values including `DRAFT`, which no code path ever produces |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/campaign.ts` | `7bd21e08` | READ — CURRENT IMPLEMENTATION | `createCampaignOrder` mints `order_id` via `deterministicId("campaign-order", input)`; `launchCampaign` always produces `lifecycle_state: "LAUNCHED"` directly — `DRAFT` is never constructed by this module; `allowedTransitions` state machine; `SHADOW` autonomy mode can never reach `SHIPPED` |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/validators.ts` | `9c3f60a1` | READ — CURRENT IMPLEMENTATION | `validateCampaignOrder` exact rule set and exact error codes (`EMPTY_VALUE`, `INVALID_INTEGER`, `OUTPUT_TARGET_REQUIRED`, `FORMAT02_DEFERRED`); notably does **not** validate `deadline_utc`, `taste_direction`, `source_kind`, or `authority` — only the fields listed in §3 |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/canonical.ts` | `4e88d0c5` | READ — CURRENT IMPLEMENTATION | `deterministicId(prefix, value)` = `` `${prefix}:${canonicalSha256(value).slice(0,24)}` ``; `canonicalSha256` = sorted-key `JSON.stringify` → SHA-256 hex — algorithmically identical to `ca_contracts.canonical_sha256` (verified field-by-field against `packages/ca_contracts/src/ca_contracts/canonical.py`), so IDs minted in Python are bit-identical to IDs the TS domain would mint for the same logical payload |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/contracts/schemas/campaign_order.schema.json` | `2a71ffb3` | READ — CURRENT IMPLEMENTATION | Authoritative, language-neutral field list and `required` set for `CampaignOrder`; `additionalProperties: false` |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/contracts/schemas/campaign_state.schema.json` | `81cc4a90` | READ — CURRENT IMPLEMENTATION | Authoritative field list for `CampaignState`; `sha256` fields use `^[0-9a-f]{64}$` — a bare hex digest, no `sha256:` prefix |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/tests/campaign-surfaces.test.mjs` | `5f0a12dd` | READ — CURRENT IMPLEMENTATION | Confirms `createCampaignOrder` + `launchCampaign` are always called together in sequence; confirms `Format 02` rejection message text; confirms `SHADOW` ships are rejected at the transition layer, not at creation |
| `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/source_package.py` | `8e83d673` | READ — CURRENT IMPLEMENTATION (already read by TS-APP-API-003) | `admit()` leaves packages at `lifecycle_state: "ADMITTED"` until a component is bound; `bind_component()` advances to `"COMPONENTS_IN_PROGRESS"`; `publish()` is the only path to `"PUBLISHED_DERIVATIVE_ELIGIBLE"` (`derivative_eligible: true`) and requires bound `reaction_receipts` + `expression_moments`, which nothing in Wave 1–2 produces |
| `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/repository.py` | `7259d89d` | READ — CURRENT IMPLEMENTATION (already read by TS-APP-API-003) | `get_object(object_id)` returns `{object_id, revision, version, sha256, payload, lifecycle_state, ...}` — `version`/`sha256` here are already exactly the `ImmutableRef` shape a `CampaignOrder.source_ref` needs; this is a strictly better source than `InterviewStatusResponse` (TS-APP-API-003 §6), which never exposes a package-level hash |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/atomic_harness_definition.py` | `c40b6a7e` | READ — CURRENT IMPLEMENTATION | `definition_hash` is assigned as `f"sha256:{digest}"` — **prefixed**, not the bare 64-hex-char string `ImmutableRef.sha256` requires |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/batch/service.py` | `b6120fa4` | READ — CURRENT IMPLEMENTATION | `ContentBatchService.compile_batch()` requires `source_package_ref`, `observed_activative_pack_ref`, `harness_binding_ref`, `brand_context_ref`, and per-route `final_script_ref`, `archetype_coalition_ref`, `primitive_coalition_ref`, `activation_transfer_contract_ref`, `semantic_program_ref` — every one of these except `source_package_ref` is an Activative Intelligence (AIR) output; see Source Gap Notice 2 |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/intake/definition_intake.py` | `d90e21ab` | READ — CURRENT IMPLEMENTATION | `AtomicHarnessDefinitionIntake.REQUIRED_KEYS` includes `profile_id` and `workflow.{nodes,edges}` — fields the Builder's exported `PortableAtomicHarnessDefinition` (what `api/harness_library.py` reads) does not produce; confirms TS-APP-API-002 Gap 4 is real and still open |
| `TS-APP-API-002.md` §1 Gap 4 | n/a | READ — WRITTEN_PENDING_AUDIT (draft dependency) | Explicitly names this spec as blocked: *"TS-APP-API-004/005 cannot claim harness execution readiness until this gap is closed by a dedicated spec"* |
| `TS-APP-API-002.md` §7 Stage 1 (`api/harness_library.py`) | n/a | READ — WRITTEN_PENDING_AUDIT (draft dependency) | `find_by_definition_id(root, definition_id) -> LibraryEntry | None`; `LibraryEntry.definition.content["category_binding"]["category_id"]`, `.definition.definition_hash`, `.definition.content["manifest_version"]` are the exact fields this spec projects into `harness_ref` |
| `TS-APP-API-003.md` footer `open_question_for_next_spec_author` | n/a | READ — WRITTEN_PENDING_AUDIT (draft dependency) | Explicitly leaves this spec to decide whether Campaign creation requires `derivative_eligible: true` (unreachable in Wave 1–2) or may select `COMPONENTS_IN_PROGRESS` packages directly; resolved in §3 |
| `packages/ca_contracts/src/ca_contracts/canonical.py` | `1cfcb99f` | READ — CURRENT IMPLEMENTATION (already read by TS-APP-API-001/003) | `canonical_sha256`/`canonical_json_text` confirmed algorithmically identical to `canonical.ts` (sorted-key JSON, no whitespace, UTF-8, SHA-256 hex) |
| `packages/ca_runtime/src/ca_runtime/database.py`, `paths.py` | `abdf2727` | READ — CURRENT IMPLEMENTATION (already read by TS-APP-API-001) | `ProductDatabase.initialize()` / `ProductHealth` are the shared bootstrap convention every service database follows; this spec's new `campaigns.sqlite3` follows the same convention |
| `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/migrations/0001_interview_expression.sql` | `e5a70bc2` | READ — CURRENT IMPLEMENTATION | Reference schema style (`ie_migrations`, `ie_command_results`, `ie_objects` with `is_current` + unique partial index) this spec's new migration follows |
| `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/errors.py` | `b2cfcdce` | READ — CURRENT IMPLEMENTATION (already read by TS-APP-API-003) | `NotFoundError.code == "INT_NOT_FOUND"` — the exception this spec's router must catch when a `source_package_id` does not exist |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/campaign.py` | `a90cc31f` | READ — CURRENT IMPLEMENTATION | **Naming collision, not a dependency.** `CampaignActivationService` here models audience/freshness *marketing* campaigns (`campaign_activation_program`, exposure tracking, share-rate findings) — an entirely different object from Studio's production-job `CampaignOrder`/`CampaignState`. This spec does not call anything in this file. Flagged so a future reader searching "campaign" in this codebase does not conflate the two. |

**Source Gap Notice 1 — Gap 4 (Builder/Pipeline schema mismatch) is inherited unresolved.** TS-APP-API-002 already documented that a Harness built and exported through `POST /api/harnesses/build` cannot be ingested by `AtomicHarnessDefinitionIntake` as-is. This spec resolves a `harness_definition_id` into a `harness_ref` (an `ImmutableRef` recording *which* Harness the operator chose) but never calls `AtomicHarnessDefinitionIntake` or schedules any workflow node. Recording a selection is not the same claim as recording an executable binding. This gap remains open and still blocks real Pipeline execution.

**Source Gap Notice 2 — `ContentBatchService.compile_batch()` cannot be called by this spec (new finding).** `CA_APP_FR_EPIC_SPEC_PLAN.md` cites `cmf_pipeline/batch/service.py` as "existing code" for FR-APP-050, and ST-APP-07.01's acceptance criterion says the campaign should "trigger Pipeline workflow" with "Pipeline nodes visible." Reading the actual service shows `compile_batch()` requires `observed_activative_pack_ref` and, per route, `final_script_ref`, `archetype_coalition_ref`, `primitive_coalition_ref`, and `activation_transfer_contract_ref` — all Activative Intelligence (AIR) outputs. Per `CA_PROJECT_SNAPSHOT_V2.md` §2, Campaign Order creation happens *after* Final Script approval in the product flow, so these refs conceptually exist by the time a real operator creates a campaign — but **no HTTP endpoint anywhere in Wave 1 or Wave 2 of `CA_APP_FR_EPIC_SPEC_PLAN.md` exposes AIR's outputs.** There is no `TS-APP-API-0XX` for AIR. This spec therefore cannot obtain those refs from any caller in a way that isn't simply trusting unverified opaque input, and does not call `compile_batch()`. A campaign created by this spec reaches `LAUNCHED` and is recorded with `pipeline_ingestion_status: "NOT_YET_TRIGGERED"`. **A dedicated Activative Intelligence API spec must exist before TS-APP-API-005 can claim it is watching real Pipeline node execution**, not before this spec — this spec never claims execution has started.

**Source Gap Notice 3 — resolving TS-APP-API-003's open question.** Decision: Campaign creation requires the source package's `lifecycle_state` to be `COMPONENTS_IN_PROGRESS` or `PUBLISHED_DERIVATIVE_ELIGIBLE` (i.e., at least one component bound; not bare `ADMITTED`, not `ARCHIVE_ACCEPTED`). It does **not** require `derivative_eligible: true`, because nothing produced by TS-APP-API-003 can ever set that flag until FR-APP-024 (Expression Moment discovery/approval) is built. `source_derivative_eligible` is surfaced unmodified on every response so a caller (eventually the React UI) can render a warning, not to block campaign creation on a condition Wave 1–2 can never satisfy. Full rationale in §3.

**Source Gap Notice 4 — hash-format mismatch between Harness Library and Studio schemas.** `HarnessDetail.definition_hash` (and `package_hash`) are formatted `f"sha256:{digest}"` by `cmf_builder` and by `api/harness_library.py`, but `campaign_order.schema.json` requires `harness_ref.sha256` to match `^[0-9a-f]{64}$` — a bare digest. This spec strips the `sha256:` prefix when constructing `harness_ref` (§3, §7 Stage 4). This is a projection performed by this spec's own router code, not a change to either upstream module.

---

## 2. Problem, User Outcome, Solution, and Scope

### Problem without this spec
An operator who has admitted an interview (TS-APP-API-003) and can browse Harnesses (TS-APP-API-002) still has no way to combine the two into a production job. `CampaignOrder`/`CampaignState` — the type that models exactly this ("select source, select Harness, choose outputs, choose autonomy mode, launch") — is fully modeled and tested in `services/studio/src/domain.ts` and `campaign.ts`, but Studio has no Python package and is never instantiated by the FastAPI gateway. There is no `POST /api/campaigns` anywhere. `CampaignList.tsx` and `CampaignNew.tsx` (Wave 3) have no server to call.

### User outcome
An operator (today: a developer exercising the API directly; later: `CampaignNew.tsx` from TS-APP-UI-002) can `POST` a source package ID, a Harness definition ID, output targets, and an autonomy mode to `/api/campaigns` and immediately receive back a `campaign_id` at `lifecycle_state: "LAUNCHED"`. `GET /api/campaigns` shows every campaign with a status badge. `GET /api/campaigns/{id}` shows the full order and state. If the operator changes their mind, `POST /api/campaigns/{id}/cancel` moves it to a terminal `CANCELLED` state. Every response is honest about what has and has not happened yet: `pipeline_ingestion_status: "NOT_YET_TRIGGERED"` on every campaign this spec creates, because Source Gap Notice 2 remains open.

### Solution
A new pure-logic module `api/domain/campaign.py` ports `campaign.ts`/`validators.ts`/`canonical.ts` field-for-field and error-code-for-error-code into Python (no TypeScript file is modified — Studio remains the canonical source for the eventual React client, which per `CA_PROJECT_SNAPSHOT_V2.md` §8 imports `domain.ts` types directly). A new `api/services/campaign_repository.py` persists `CampaignOrder`/`CampaignState` in a new SQLite database, following the exact idempotent-object-store pattern `InterviewRepository` already established. `api/routers/campaigns.py` orchestrates: resolve `source_package_id` via `Depends(get_interview)`, resolve `harness_definition_id` via TS-APP-API-002's `api/harness_library.py`, validate, mint, persist.

### In scope
- `api/domain/campaign.py` — ported validation, deterministic-ID minting, state machine, `launch_campaign`/`transition_campaign` (pure functions, no I/O, no FastAPI dependency)
- `api/services/campaign_repository.py` — SQLite persistence (`campaigns.sqlite3` under `CA_DATA_ROOT`), idempotency, optimistic concurrency on `CampaignState.version`
- `api/schemas/campaigns.py` — Pydantic request/response models
- `api/routers/campaigns.py` — `POST /api/campaigns`, `GET /api/campaigns`, `GET /api/campaigns/{campaign_id}`, `POST /api/campaigns/{campaign_id}/cancel`
- `api/main.py` — additive: construct `CampaignRepository` in `lifespan()`, register `campaigns.router`
- `api/dependencies.py` — additive: `get_campaign_repository`
- Reusing `api/harness_library.py::find_by_definition_id` (TS-APP-API-002) and `InterviewExpressionApplication.repository.get_object()` (TS-APP-API-003) exactly as they exist today — no modification to either

### Out of scope
- Calling `ContentBatchService.compile_batch()` or any real Pipeline scheduling/execution — see Source Gap Notice 2. `pipeline_ingestion_status` is always `"NOT_YET_TRIGGERED"` in this spec's responses.
- Any lifecycle transition other than the operator-initiated terminal `CANCELLED` transition. `RUNNING`, `AWAITING_REVIEW`, `BLOCKED_EXCEPTION`, `READY_TO_SHIP` are driven by the Pipeline's own event stream and belong to TS-APP-API-005/006, which will import and reuse `api/domain/campaign.py::transition_campaign` rather than reimplement the state machine.
- `SHIPPED` transition and ship-eligibility evaluation — `FR-APP-064`, TS-APP-API-006.
- `source_kind: "ASSET_PACKAGE_SPEC"` — no ingestion path for this source kind exists yet anywhere in the repo; this spec always sets `source_kind: "CANONICAL_INTERVIEW_SOURCE_PACKAGE"` server-side.
- Resolving Gap 4 (Builder/Pipeline schema mismatch) or the AIR-API gap (Source Gap Notice 2) — both are cross-service compiler/adapter concerns, not HTTP-wrapping concerns, per the same reasoning TS-APP-API-002 already applied to Gap 4.
- Authentication/authorization — still deferred per `CA_PROJECT_SNAPSHOT_V2.md`.
- Adding `campaigns` as a sixth key to `GET /api/health` — a small, non-blocking follow-up; this spec's repository exposes a `.status()` method in the exact `ProductHealth`-compatible shape so that patch is mechanical when someone picks it up.

---

## 3. Governing Decisions and Constraints

**Studio's TypeScript domain is the source of truth for shape and rules; this spec ports it into Python because no Python package exists to call.** Unlike AIR/Pipeline/VAE/Interview/Builder, `services/studio/` has zero `.py` files and is never instantiated in `app.state` by TS-APP-API-001. `api/domain/campaign.py` is a byte-faithful port of `campaign.ts` + `validators.ts`, reusing `ca_contracts.canonical_sha256` (confirmed algorithmically identical to `canonicalSha256` in `canonical.ts`) rather than reimplementing canonicalization. Every error code this spec raises (`EMPTY_VALUE`, `INVALID_INTEGER`, `OUTPUT_TARGET_REQUIRED`, `FORMAT02_DEFERRED`, `CAMPAIGN_TRANSITION_DENIED`, `SHADOW_CANNOT_SHIP`) is copied verbatim from `validators.ts`/`campaign.ts`, not invented, so a future React client reading `domain.ts` and this API's responses sees one vocabulary.

**Source package readiness (resolves TS-APP-API-003's open question).** Campaign creation requires `lifecycle_state in {"COMPONENTS_IN_PROGRESS", "PUBLISHED_DERIVATIVE_ELIGIBLE"}`. `derivative_eligible: true` is never required, because it is unreachable anywhere in Wave 1–2 (needs FR-APP-024). `source_derivative_eligible` and `source_lifecycle_state` are always echoed on the response so this remains visible, not hidden.

**`harness_ref` is projected from `HarnessDetail`/`LibraryEntry`, with the `sha256:` prefix stripped.** `object_id = definition_id`, `version = str(manifest_version)`, `sha256 = definition_hash` with a leading `"sha256:"` removed if present (Source Gap Notice 4). Harness↔category compatibility is checked by comparing `category_binding.category_id` against the request's `category_id` — the same comparison TS-APP-API-002's eligibility endpoint performs, applied in-process rather than through a second HTTP round-trip, since both routers run in the same ASGI process.

**`source_kind` is fixed server-side to `"CANONICAL_INTERVIEW_SOURCE_PACKAGE"`.** No other ingestion path (`ASSET_PACKAGE_SPEC`) exists yet; accepting it as caller input today would validate a value this API can never actually resolve.

**`authority` is a fixed development-stage stub, not caller-supplied.** `validateCampaignOrder` never inspects `order.authority`'s contents (confirmed in §1), so this spec mints one server-side using the same `candidate_not_current` convention `cmf_activative_intelligence.campaign._authority()` already uses elsewhere in this codebase, rather than inventing a second authority scheme or asking the caller to supply one that means nothing yet.

**`operator_actor` is constructed from a single `operator_id` string.** The caller supplies `operator_id`; the router builds the full `ActorRef` (`actor_type: "human"`, `product_id: "conscious-activations-studio"`, `workflow_role: "operator"`) — mirroring the exact fixture shape used by `tests/support.mjs`'s `actor` constant, since every campaign created through this HTTP surface today originates from a human operator, not a `deterministic_module` or `model_program` actor.

**No real Pipeline trigger (Source Gap Notice 2).** Every campaign this spec creates carries `pipeline_ingestion_status: "NOT_YET_TRIGGERED"`. This is a deliberate claim-ceiling choice, not an oversight: claiming "Pipeline workflow triggered" without a real `compile_batch()` call and without AIR-produced refs would be a false claim the audit trail (§10) cannot back up.

**Order creation and campaign launch are atomic from the caller's point of view.** Following `campaign.ts` (`launchCampaign` is always called immediately after `createCampaignOrder` in every code path that exists — confirmed via `campaign-surfaces.test.mjs`), `POST /api/campaigns` performs both steps in one request and one persistence transaction. There is no separate "create a DRAFT, then launch it later" endpoint; `DRAFT` remains a schema-valid but practically unused state, exactly as it is in the TS domain today.

**Idempotency follows the two-layer pattern already established by `InterviewRepository`.** A caller-supplied `idempotency_key` short-circuits an exact retry through the command-result log. Independently, because `order_id`/`campaign_id` are content-derived, a *different* `idempotency_key` submitted with logically identical order fields still resolves to the same `order_id`/`campaign_id` row rather than raising a primary-key conflict — the router returns the **existing** stored state (not a freshly re-launched one), so a duplicate create call can never silently roll back a campaign that has already transitioned away from `LAUNCHED`.

**`DELETE` is modeled as a state transition, not a row deletion.** This is an event-sourced-style system (every other service preserves full history); `POST /api/campaigns/{id}/cancel` moves a campaign to the terminal `CANCELLED` state using the same `transition_campaign` function TS-APP-API-005/006 will reuse for their own transitions, with optimistic concurrency on `CampaignState.version`. No physical row is ever removed by this spec.

**Claim ceiling:** `CAMPAIGN_ORDER_PRE_PUBLICATION_SOURCE_EVIDENCE`. This spec does not claim Pipeline execution has started, that a selected Harness is executable (Gap 4 open), that the source package has completed Expression-Moment approval, or certified/production-authorized operation.

---

## 4. Current Brownfield Architecture

| Component | Path | Actual behaviour | Disposition | Reason |
|---|---|---|---|---|
| Studio `CampaignOrder`/`CampaignState` domain | `services/studio/src/domain.ts`, `campaign.ts`, `validators.ts`, `canonical.ts` | Correct, tested (`campaign-surfaces.test.mjs`), TypeScript-only; never instantiated in `app.state` | **PORT** | No Node runtime in the FastAPI process; ported field-for-field into `api/domain/campaign.py` (§3) — not modified in place |
| `ContentBatchService.compile_batch` | `services/pipeline/src/cmf_pipeline/batch/service.py` | Requires AIR-produced refs no HTTP surface exposes yet | **DEFER** | Source Gap Notice 2; not called by this spec |
| `AtomicHarnessDefinitionIntake` | `services/pipeline/src/cmf_pipeline/intake/definition_intake.py` | Structurally incompatible with the Builder's exported package (Gap 4, TS-APP-API-002) | **DEFER** | Not called; this spec only records the harness *selection*, never ingests it into the Pipeline |
| `InterviewExpressionApplication.repository` | `services/interview/src/conscious_activations_interview_expression/repository.py` | `get_object()` already returns `{object_id, version, sha256}` — a ready-made `ImmutableRef` | **REUSE** | Used directly to build `source_ref`; bypasses `InterviewStatusResponse`, which has no package-level hash |
| `api/harness_library.py` (TS-APP-API-002) | `api/harness_library.py` | `find_by_definition_id()` returns a `LibraryEntry` with `.definition.content`, `.definition.definition_hash` | **REUSE** | Used directly to build `harness_ref`; `sha256:` prefix stripped (§3) |
| `api/routers/interviews.py`, `api/routers/harnesses.py` (TS-APP-API-002/003) | `api/routers/*.py` | Existing routers, unmodified | **REUSE** | No change |
| `api/main.py`, `api/dependencies.py`, `api/errors.py` (TS-APP-API-001) | `api/*.py` | Existing lifespan/DI/error-contract patterns | **REUSE + ADDITIVE PATCH** | Add `campaign_repository` to `app.state`; add `get_campaign_repository`; register `campaigns.router` |
| `cmf_activative_intelligence.campaign.CampaignActivationService` | `services/air/src/cmf_activative_intelligence/campaign.py` | Models audience/freshness marketing campaigns — a different object entirely | **NOT USED** | Naming collision only; flagged in §1 so it is not confused with Studio's `CampaignOrder` |

---

## 5. Proposed Architecture and Workflows

### Create flow — `POST /api/campaigns`

```
Router receives CampaignCreateRequest
  ├── interview.repository.get_object(source_package_id)
  │     ├── raises InterviewNotFoundError → 404 SOURCE_PACKAGE_NOT_FOUND
  │     └── ok → check payload.lifecycle_state
  │           ├── not in {COMPONENTS_IN_PROGRESS, PUBLISHED_DERIVATIVE_ELIGIBLE} → 422 SOURCE_PACKAGE_NOT_READY
  │           └── ok → source_ref = {object_id, version, sha256} (verbatim from get_object())
  ├── find_by_definition_id(harness_library_root, harness_definition_id)
  │     ├── None → 404 HARNESS_NOT_FOUND
  │     └── entry → category_binding.category_id != requested category_id → 422 HARNESS_INELIGIBLE
  │                → ok → harness_ref = {object_id, version, sha256 (prefix stripped)}
  ├── build core CampaignOrder dict (source_kind fixed, authority fixed, operator_actor built from operator_id)
  ├── api.domain.campaign.create_campaign_order(core)
  │     └── validate_campaign_order() raises CampaignValidationError on any rule violation → 400/422 (exact TS error code)
  ├── api.domain.campaign.launch_campaign(order) → initial CampaignState at LAUNCHED, version 1
  └── campaign_repository.create(order, state, idempotency_key=...)
        ├── idempotency_key seen before → replay stored result, idempotent_replay=true
        ├── order_id/campaign_id already exist (content-addressed replay under a *different* key) → return existing rows, idempotent_replay=true
        └── else → INSERT both rows in one transaction → 201
```

### List / detail flow

`GET /api/campaigns` joins `campaign_states` to `campaign_orders`, filters optionally by `workspace_id`, `project_id`, `lifecycle_state`, and returns a lightweight `CampaignSummary` per row — no interview/harness re-resolution, so this stays fast even as the campaign count grows.

`GET /api/campaigns/{campaign_id}` returns the full stored order + state, plus a fresh lookup of the source package's current `derivative_eligible`/`lifecycle_state` (these can change after campaign creation, e.g. once FR-APP-024 lands and a package is later published — the campaign detail view should reflect that without requiring a new campaign).

### Cancel flow — `POST /api/campaigns/{campaign_id}/cancel`

```
repository.get(campaign_id) → 404 CAMPAIGN_NOT_FOUND if missing
state.version != body.expected_version → 409 CONFLICT
transition_campaign(state, "CANCELLED")
  ├── current lifecycle_state has no "CANCELLED" in allowed_transitions (i.e. already SHIPPED or CANCELLED)
  │     → CampaignValidationError("CAMPAIGN_TRANSITION_DENIED") → 409
  └── ok → new_state (version + 1, lifecycle_state=CANCELLED)
repository.update_state(campaign_id, new_state, expected_version=body.expected_version)
  └── version changed between read and write (race) → CampaignConflictError → 409 CONFLICT
```

### Error contract addendum

New `error_code` values introduced by this spec (all reuse the `ErrorResponse` shape from TS-APP-API-001, unchanged):

| error_code | HTTP status | Raised when |
|---|---|---|
| `SOURCE_PACKAGE_NOT_FOUND` | 404 | `source_package_id` does not resolve via `interview.repository.get_object()` |
| `SOURCE_PACKAGE_NOT_READY` | 422 | package exists but `lifecycle_state` is `ADMITTED` or `ARCHIVE_ACCEPTED` |
| `HARNESS_NOT_FOUND` | 404 | `harness_definition_id` not found in the library (TS-APP-API-002's `find_by_definition_id`) |
| `HARNESS_INELIGIBLE` | 422 | harness's `category_binding.category_id` does not match the requested `category_id` |
| `EMPTY_VALUE`, `INVALID_INTEGER`, `INVALID_SHA256`, `OUTPUT_TARGET_REQUIRED` | 400 | `validate_campaign_order` rule violations, verbatim from `validators.ts` |
| `FORMAT02_DEFERRED` | 422 | `category_id == "2d_character_animation"` or `format_profile_id` starts with `"format02_"` |
| `CAMPAIGN_NOT_FOUND` | 404 | unknown `campaign_id` on GET or cancel |
| `CAMPAIGN_TRANSITION_DENIED` | 409 | requested transition not in `ALLOWED_TRANSITIONS[current_state]` |
| `SHADOW_CANNOT_SHIP` | 409 | reserved for future reuse by TS-APP-API-006; unreachable through this spec's own routes (this spec never calls `transition_campaign(..., "SHIPPED")`) |
| `CONFLICT` | 409 | `expected_version` does not match the current stored `CampaignState.version` |

---

## 6. Data Models, Contracts, Schemas, and APIs

### `api/schemas/campaigns.py`

```python
from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field

from api.schemas.interviews import RefModel  # reused unchanged — {object_id, version, sha256}

OutputType = Literal["SOURCE_LED_SHORT", "CAROUSEL", "SUPERVISUAL", "ANIMATION_SCENE_PACKAGE", "ANIMATION_SHORT"]
AutonomyMode = Literal["AUTOPILOT", "REVIEW_BEFORE_SHIP", "CHECKPOINTED", "SHADOW"]
LifecycleState = Literal["DRAFT", "LAUNCHED", "RUNNING", "AWAITING_REVIEW", "BLOCKED_EXCEPTION", "READY_TO_SHIP", "SHIPPED", "CANCELLED"]

class OutputTargetModel(BaseModel):
    output_type: OutputType
    quantity: int = Field(ge=1)
    profile_id: str

class AutonomyPolicyModel(BaseModel):
    mode: AutonomyMode
    checkpoint_ids: list[str]
    exception_only: bool
    final_review_required: bool
    publication_authority_required: bool

class ActorRefModel(BaseModel):
    actor_id: str
    actor_type: Literal["deterministic_module", "model_program", "human"]
    product_id: str
    workflow_role: Literal["hunter", "analyst", "composer", "commander", "evaluator", "operator"]

class AuthorityRefModel(BaseModel):
    authority_id: str
    authority_version: str
    authority_sha256: str
    authority_state: Literal["current", "candidate_not_current"]

class ArtifactRefModel(BaseModel):
    artifact_id: str
    artifact_kind: str
    bytes: int
    media_type: str
    sha256: str
    uri: str

class CampaignCreateRequest(BaseModel):
    idempotency_key: str
    workspace_id: str
    project_id: str
    source_package_id: str
    harness_definition_id: str
    category_id: str
    format_profile_id: str
    objective: str
    initial_seed: str
    taste_direction: list[str] = []
    output_targets: list[OutputTargetModel]
    budget_units: int
    deadline_utc: str | None = None
    autonomy_mode: AutonomyMode
    operator_id: str

class CampaignOrderModel(BaseModel):
    order_id: str
    workspace_id: str
    project_id: str
    source_kind: Literal["CANONICAL_INTERVIEW_SOURCE_PACKAGE", "ASSET_PACKAGE_SPEC"]
    source_ref: RefModel
    harness_ref: RefModel
    category_id: str
    format_profile_id: str
    objective: str
    initial_seed: str
    taste_direction: list[str]
    output_targets: list[OutputTargetModel]
    budget_units: int
    deadline_utc: str | None
    autonomy_policy: AutonomyPolicyModel
    operator_actor: ActorRefModel
    authority: AuthorityRefModel

class CampaignStateModel(BaseModel):
    campaign_id: str
    order_ref: RefModel
    lifecycle_state: LifecycleState
    autonomy_mode: AutonomyMode
    active_checkpoint_id: str | None
    exception_ids: list[str]
    run_refs: list[RefModel]
    artifact_refs: list[ArtifactRefModel]
    evaluation_refs: list[RefModel]
    version: int

class CampaignDetailResponse(BaseModel):
    order: CampaignOrderModel
    state: CampaignStateModel
    source_derivative_eligible: bool
    source_lifecycle_state: str
    pipeline_ingestion_status: Literal["NOT_YET_TRIGGERED"]
    idempotent_replay: bool

class CampaignSummary(BaseModel):
    campaign_id: str
    order_id: str
    workspace_id: str
    project_id: str
    category_id: str
    lifecycle_state: LifecycleState
    autonomy_mode: AutonomyMode
    output_target_count: int
    budget_units: int
    version: int

class CampaignCancelRequest(BaseModel):
    expected_version: int
    reason: str
```

### Endpoints defined in this spec

| Method | Path | Request | Response | Error codes |
|---|---|---|---|---|
| `POST` | `/api/campaigns` | `CampaignCreateRequest` | `CampaignDetailResponse` (201) | `SOURCE_PACKAGE_NOT_FOUND`, `SOURCE_PACKAGE_NOT_READY`, `HARNESS_NOT_FOUND`, `HARNESS_INELIGIBLE`, `EMPTY_VALUE`, `INVALID_INTEGER`, `OUTPUT_TARGET_REQUIRED`, `FORMAT02_DEFERRED` |
| `GET` | `/api/campaigns?workspace_id=&project_id=&lifecycle_state=` | — | `list[CampaignSummary]` (200, always — empty list is not an error) | — |
| `GET` | `/api/campaigns/{campaign_id}` | — | `CampaignDetailResponse` (200) | `CAMPAIGN_NOT_FOUND` |
| `POST` | `/api/campaigns/{campaign_id}/cancel` | `CampaignCancelRequest` | `CampaignDetailResponse` (200) | `CAMPAIGN_NOT_FOUND`, `CAMPAIGN_TRANSITION_DENIED`, `CONFLICT` |

Positive example — `POST /api/campaigns` response:
```json
{
  "order": {
    "order_id": "campaign-order:9f1a2b3c4d5e6f708192",
    "workspace_id": "workspace:acme-coach",
    "project_id": "project:q3-launch",
    "source_kind": "CANONICAL_INTERVIEW_SOURCE_PACKAGE",
    "source_ref": { "object_id": "ie:source-package:7c1a9f0b...", "version": "1.0.0", "sha256": "3b2c..." },
    "harness_ref": { "object_id": "short-video-v2", "version": "1.0.0", "sha256": "a4e9..." },
    "category_id": "short_form_edited_video",
    "format_profile_id": "format07_direct_coaching_a_roll",
    "objective": "Preserve source expression",
    "initial_seed": "A source-backed seed",
    "taste_direction": ["identity-first"],
    "output_targets": [{ "output_type": "SOURCE_LED_SHORT", "quantity": 1, "profile_id": "format07_direct_coaching_a_roll" }],
    "budget_units": 100,
    "deadline_utc": null,
    "autonomy_policy": { "mode": "REVIEW_BEFORE_SHIP", "checkpoint_ids": [], "exception_only": true, "final_review_required": true, "publication_authority_required": true },
    "operator_actor": { "actor_id": "operator:jane", "actor_type": "human", "product_id": "conscious-activations-studio", "workflow_role": "operator" },
    "authority": { "authority_id": "ca-program-control-v2.1-candidate", "authority_version": "2.1.0-candidate", "authority_sha256": "d8c1...", "authority_state": "candidate_not_current" }
  },
  "state": {
    "campaign_id": "campaign:1a2b3c4d5e6f70819293",
    "order_ref": { "object_id": "campaign-order:9f1a2b3c4d5e6f708192", "version": "1.0.0", "sha256": "e71a..." },
    "lifecycle_state": "LAUNCHED",
    "autonomy_mode": "REVIEW_BEFORE_SHIP",
    "active_checkpoint_id": null,
    "exception_ids": [],
    "run_refs": [],
    "artifact_refs": [],
    "evaluation_refs": [],
    "version": 1
  },
  "source_derivative_eligible": false,
  "source_lifecycle_state": "COMPONENTS_IN_PROGRESS",
  "pipeline_ingestion_status": "NOT_YET_TRIGGERED",
  "idempotent_replay": false
}
```

Negative example — `POST /api/campaigns` with a source package still `ADMITTED`:
```json
{
  "error_code": "SOURCE_PACKAGE_NOT_READY",
  "message": "source package 'ie:source-package:...' is ADMITTED; expected one of ['COMPONENTS_IN_PROGRESS', 'PUBLISHED_DERIVATIVE_ELIGIBLE']",
  "service": null,
  "timestamp": "2026-07-26T10:00:00Z"
}
```

Negative example — `POST /api/campaigns/{id}/cancel` on an already-cancelled campaign:
```json
{
  "error_code": "CAMPAIGN_TRANSITION_DENIED",
  "message": "CANCELLED cannot transition to CANCELLED",
  "service": null,
  "timestamp": "2026-07-26T10:00:00Z"
}
```

---

## 7. Implementation Stages and Exact Target Paths

All paths are relative to the repository root after the directory restructure described in `CA_APP_FR_EPIC_SPEC_PLAN.md` Part 5 (`services/studio/...`, `services/interview/...`, not the numbered directories).

### Stage 1 — Pure domain port (no I/O, no FastAPI)

**`api/domain/campaign.py`**
```python
from __future__ import annotations

import re
from typing import Any, Mapping, Sequence

from ca_contracts import canonical_sha256

_PREFIX_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._:-]*$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

ALLOWED_TRANSITIONS: dict[str, tuple[str, ...]] = {
    "DRAFT": ("LAUNCHED", "CANCELLED"),
    "LAUNCHED": ("RUNNING", "CANCELLED"),
    "RUNNING": ("AWAITING_REVIEW", "BLOCKED_EXCEPTION", "READY_TO_SHIP", "CANCELLED"),
    "AWAITING_REVIEW": ("RUNNING", "READY_TO_SHIP", "CANCELLED"),
    "BLOCKED_EXCEPTION": ("RUNNING", "AWAITING_REVIEW", "CANCELLED"),
    "READY_TO_SHIP": ("SHIPPED", "AWAITING_REVIEW", "CANCELLED"),
    "SHIPPED": (),
    "CANCELLED": (),
}


class CampaignValidationError(ValueError):
    """Python port of Studio's StudioValidationError, scoped to CampaignOrder /
    CampaignState. Error codes are copied verbatim from
    services/studio/src/validators.ts and campaign.ts."""

    def __init__(self, code: str, message: str, context: Mapping[str, Any] | None = None):
        super().__init__(message)
        self.code = code
        self.context = dict(context or {})


def deterministic_id(prefix: str, value: Any) -> str:
    """Port of services/studio/src/canonical.ts::deterministicId. Uses
    ca_contracts.canonical_sha256, confirmed algorithmically identical to
    canonicalSha256 in canonical.ts (§1), so IDs minted here are bit-identical
    to IDs the TS domain would mint for the same logical payload."""
    if not _PREFIX_RE.match(prefix):
        raise CampaignValidationError("INVALID_ID_PREFIX", f"invalid deterministic ID prefix: {prefix}")
    return f"{prefix}:{canonical_sha256(value)[:24]}"


def _require_non_empty(value: str, label: str) -> None:
    if not value or not value.strip():
        raise CampaignValidationError("EMPTY_VALUE", f"{label} must not be empty", {"label": label})


def _require_safe_integer(value: int, label: str, minimum: int = 0) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise CampaignValidationError(
            "INVALID_INTEGER", f"{label} must be an integer >= {minimum}", {"label": label, "value": value}
        )


def _validate_ref(ref: Mapping[str, Any], label: str) -> None:
    _require_non_empty(ref["object_id"], f"{label}.object_id")
    _require_non_empty(ref["version"], f"{label}.version")
    if not _SHA256_RE.match(ref["sha256"]):
        raise CampaignValidationError("INVALID_SHA256", f"{label}.sha256 must be lowercase SHA-256", {"label": label})


def _validate_actor(actor: Mapping[str, Any]) -> None:
    _require_non_empty(actor["actor_id"], "actor_id")
    _require_non_empty(actor["product_id"], "product_id")


def validate_campaign_order(order: Mapping[str, Any]) -> None:
    """Direct port of validateCampaignOrder (validators.ts). Deliberately does
    NOT validate deadline_utc, taste_direction, source_kind, or authority —
    matching the TS function exactly, not a superset of it."""
    _require_non_empty(order["workspace_id"], "workspace_id")
    _require_non_empty(order["project_id"], "project_id")
    _validate_ref(order["source_ref"], "source_ref")
    _validate_ref(order["harness_ref"], "harness_ref")
    _require_non_empty(order["category_id"], "category_id")
    _require_non_empty(order["objective"], "objective")
    _require_non_empty(order["initial_seed"], "initial_seed")
    _require_safe_integer(order["budget_units"], "budget_units", 1)
    if not order["output_targets"]:
        raise CampaignValidationError("OUTPUT_TARGET_REQUIRED", "at least one output target is required")
    for target in order["output_targets"]:
        _require_safe_integer(target["quantity"], "output_target.quantity", 1)
    if order["category_id"] == "2d_character_animation" or order["format_profile_id"].startswith("format02_"):
        raise CampaignValidationError("FORMAT02_DEFERRED", "Format 02 is deferred pending a current validated Atomic Harness")
    _validate_actor(order["operator_actor"])


def default_autonomy_policy(mode: str) -> dict[str, Any]:
    """Port of defaultAutonomyPolicy (campaign.ts)."""
    return {
        "mode": mode,
        "checkpoint_ids": ["final-script-approval", "final-artifact-review"] if mode == "CHECKPOINTED" else [],
        "exception_only": mode in ("AUTOPILOT", "REVIEW_BEFORE_SHIP"),
        "final_review_required": mode != "AUTOPILOT",
        "publication_authority_required": True,
    }


def create_campaign_order(core: Mapping[str, Any]) -> dict[str, Any]:
    """Port of createCampaignOrder (campaign.ts). `core` is every CampaignOrder
    field except order_id."""
    order = {**core, "order_id": deterministic_id("campaign-order", core)}
    validate_campaign_order(order)
    return order


def launch_campaign(order: Mapping[str, Any]) -> dict[str, Any]:
    """Port of launchCampaign (campaign.ts). Produces LAUNCHED directly — no
    code path in the ported TS domain ever constructs a DRAFT CampaignState
    (confirmed against campaign-surfaces.test.mjs, §1)."""
    validate_campaign_order(order)
    order_ref = {"object_id": order["order_id"], "version": "1.0.0", "sha256": canonical_sha256(order)}
    return {
        "campaign_id": deterministic_id("campaign", {"order_ref": order_ref}),
        "order_ref": order_ref,
        "lifecycle_state": "LAUNCHED",
        "autonomy_mode": order["autonomy_policy"]["mode"],
        "active_checkpoint_id": None,
        "exception_ids": [],
        "run_refs": [],
        "artifact_refs": [],
        "evaluation_refs": [],
        "version": 1,
    }


_UNSET = object()


def transition_campaign(
    state: Mapping[str, Any],
    next_state: str,
    *,
    checkpoint_id: str | None = _UNSET,  # type: ignore[assignment]
    exception_ids: Sequence[str] | None = None,
    run_refs: Sequence[Mapping[str, Any]] | None = None,
    artifact_refs: Sequence[Mapping[str, Any]] | None = None,
    evaluation_refs: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Port of transitionCampaign (campaign.ts). `checkpoint_id` uses the
    _UNSET sentinel (not None) to mirror TS's undefined-vs-null distinction:
    "caller didn't pass this" vs "caller wants it explicitly cleared".
    Reused unchanged by TS-APP-API-005/006 for RUNNING/AWAITING_REVIEW/
    BLOCKED_EXCEPTION/READY_TO_SHIP/SHIPPED transitions — this spec only
    calls it with next_state="CANCELLED"."""
    current = state["lifecycle_state"]
    if next_state not in ALLOWED_TRANSITIONS.get(current, ()):
        raise CampaignValidationError("CAMPAIGN_TRANSITION_DENIED", f"{current} cannot transition to {next_state}")
    if next_state == "SHIPPED" and state["autonomy_mode"] == "SHADOW":
        raise CampaignValidationError("SHADOW_CANNOT_SHIP", "SHADOW campaigns cannot transition to SHIPPED")
    return {
        **state,
        "lifecycle_state": next_state,
        "active_checkpoint_id": state["active_checkpoint_id"] if checkpoint_id is _UNSET else checkpoint_id,
        "exception_ids": sorted(set(state["exception_ids"] if exception_ids is None else exception_ids)),
        "run_refs": list(state["run_refs"] if run_refs is None else run_refs),
        "artifact_refs": list(state["artifact_refs"] if artifact_refs is None else artifact_refs),
        "evaluation_refs": list(state["evaluation_refs"] if evaluation_refs is None else evaluation_refs),
        "version": state["version"] + 1,
    }
```

### Stage 2 — Persistence

**`api/services/campaign_repository.py`**
```python
from __future__ import annotations

import json
import sqlite3
from contextlib import closing, contextmanager
from pathlib import Path
from typing import Any, Iterator

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.database import ProductDatabase

PRODUCT_ID = "ca-campaigns-api"
PRODUCT_VERSION = "0.1.0.dev1"
AUTHORITY_STATE = "phase_09_development_release_candidate"

MIGRATION_SQL = """
CREATE TABLE IF NOT EXISTS campaign_migrations(
  version INTEGER PRIMARY KEY, name TEXT NOT NULL, applied_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS campaign_command_results(
  idempotency_key TEXT PRIMARY KEY, command_type TEXT NOT NULL,
  payload_sha256 TEXT NOT NULL, result_json TEXT NOT NULL, created_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS campaign_orders(
  order_id TEXT PRIMARY KEY, workspace_id TEXT NOT NULL, project_id TEXT NOT NULL,
  canonical_sha256 TEXT NOT NULL, payload_json TEXT NOT NULL, created_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS campaign_states(
  campaign_id TEXT PRIMARY KEY, order_id TEXT NOT NULL REFERENCES campaign_orders(order_id),
  lifecycle_state TEXT NOT NULL, payload_json TEXT NOT NULL, version INTEGER NOT NULL,
  updated_at_utc TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS campaign_states_by_lifecycle ON campaign_states(lifecycle_state);
"""


class CampaignConflictError(RuntimeError):
    code = "CONFLICT"


class CampaignNotFoundError(RuntimeError):
    code = "CAMPAIGN_NOT_FOUND"


class CampaignRepository:
    def __init__(self, database_path: str | Path):
        self.path = Path(database_path)

    def _connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.path, timeout=10.0, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = FULL")
        return conn

    def initialize(self) -> None:
        ProductDatabase(
            self.path, product_id=PRODUCT_ID, product_version=PRODUCT_VERSION,
            authority_state=AUTHORITY_STATE, development_authorized=True,
        ).initialize(initialized_at_utc=utc_now_rfc3339())
        with closing(self._connect()) as conn:
            conn.executescript(MIGRATION_SQL)
            conn.execute(
                "INSERT OR IGNORE INTO campaign_migrations(version, name, applied_at_utc) VALUES (1, 'campaign_core', ?)",
                (utc_now_rfc3339(),),
            )

    def status(self) -> dict[str, Any]:
        with closing(self._connect()) as conn:
            orders = conn.execute("SELECT COUNT(*) FROM campaign_orders").fetchone()[0]
            states = conn.execute("SELECT COUNT(*) FROM campaign_states").fetchone()[0]
        return {
            "product_id": PRODUCT_ID, "product_version": PRODUCT_VERSION, "authority_state": AUTHORITY_STATE,
            "database_path": str(self.path), "integrity": "ok", "command_count": orders,
            "event_count": states, "receipt_count": 0, "production_authorized": False, "certified": False,
            "claim_ceiling": "CAMPAIGN_ORDER_PRE_PUBLICATION_SOURCE_EVIDENCE",
        }

    @contextmanager
    def _transaction(self, conn: sqlite3.Connection) -> Iterator[None]:
        conn.execute("BEGIN IMMEDIATE")
        try:
            yield
        except Exception:
            conn.execute("ROLLBACK")
            raise
        else:
            conn.execute("COMMIT")

    def create(self, order: dict[str, Any], state: dict[str, Any], *, idempotency_key: str) -> dict[str, Any]:
        """Two independent idempotency layers, matching InterviewRepository's
        established pattern: (1) exact idempotency_key replay via the command
        log; (2) content-addressed replay when order_id/campaign_id already
        exist under a *different* key — returns the EXISTING stored state,
        never a freshly re-launched one, so a duplicate create can never roll
        back a campaign that has already transitioned."""
        timestamp = utc_now_rfc3339()
        with closing(self._connect()) as conn:
            cached = conn.execute(
                "SELECT result_json FROM campaign_command_results WHERE idempotency_key=?", (idempotency_key,)
            ).fetchone()
            if cached is not None:
                result = json.loads(cached["result_json"])
                result["idempotent_replay"] = True
                return result
            with self._transaction(conn):
                order_row = conn.execute(
                    "SELECT payload_json FROM campaign_orders WHERE order_id=?", (order["order_id"],)
                ).fetchone()
                state_row = conn.execute(
                    "SELECT payload_json FROM campaign_states WHERE campaign_id=?", (state["campaign_id"],)
                ).fetchone()
                content_addressed_replay = order_row is not None and state_row is not None
                if order_row is None:
                    conn.execute(
                        "INSERT INTO campaign_orders(order_id, workspace_id, project_id, canonical_sha256, payload_json, created_at_utc) VALUES (?,?,?,?,?,?)",
                        (order["order_id"], order["workspace_id"], order["project_id"], canonical_sha256(order), canonical_json_text(order), timestamp),
                    )
                if state_row is None:
                    conn.execute(
                        "INSERT INTO campaign_states(campaign_id, order_id, lifecycle_state, payload_json, version, updated_at_utc) VALUES (?,?,?,?,?,?)",
                        (state["campaign_id"], order["order_id"], state["lifecycle_state"], canonical_json_text(state), state["version"], timestamp),
                    )
                final_order = json.loads(order_row["payload_json"]) if order_row is not None else order
                final_state = json.loads(state_row["payload_json"]) if state_row is not None else state
                result = {"order": final_order, "state": final_state, "idempotent_replay": content_addressed_replay}
                conn.execute(
                    "INSERT INTO campaign_command_results(idempotency_key, command_type, payload_sha256, result_json, created_at_utc) VALUES (?,?,?,?,?)",
                    (idempotency_key, "create_campaign", order["order_id"], canonical_json_text(result), timestamp),
                )
            return result

    def get(self, campaign_id: str) -> dict[str, Any]:
        with closing(self._connect()) as conn:
            row = conn.execute(
                "SELECT cs.payload_json AS state_json, co.payload_json AS order_json "
                "FROM campaign_states cs JOIN campaign_orders co ON co.order_id = cs.order_id "
                "WHERE cs.campaign_id=?", (campaign_id,),
            ).fetchone()
        if row is None:
            raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
        return {"order": json.loads(row["order_json"]), "state": json.loads(row["state_json"])}

    def list(
        self, *, workspace_id: str | None = None, project_id: str | None = None, lifecycle_state: str | None = None
    ) -> list[dict[str, Any]]:
        clauses, params = [], []
        if workspace_id is not None:
            clauses.append("co.workspace_id = ?"); params.append(workspace_id)
        if project_id is not None:
            clauses.append("co.project_id = ?"); params.append(project_id)
        if lifecycle_state is not None:
            clauses.append("cs.lifecycle_state = ?"); params.append(lifecycle_state)
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        with closing(self._connect()) as conn:
            rows = conn.execute(
                f"SELECT cs.payload_json AS state_json, co.payload_json AS order_json "
                f"FROM campaign_states cs JOIN campaign_orders co ON co.order_id = cs.order_id "
                f"{where} ORDER BY co.created_at_utc DESC",
                params,
            ).fetchall()
        return [{"order": json.loads(r["order_json"]), "state": json.loads(r["state_json"])} for r in rows]

    def update_state(self, campaign_id: str, new_state: dict[str, Any], *, expected_version: int) -> dict[str, Any]:
        timestamp = utc_now_rfc3339()
        with closing(self._connect()) as conn:
            with self._transaction(conn):
                row = conn.execute("SELECT version FROM campaign_states WHERE campaign_id=?", (campaign_id,)).fetchone()
                if row is None:
                    raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
                if int(row["version"]) != expected_version:
                    raise CampaignConflictError(f"expected version {expected_version}, current {row['version']}")
                conn.execute(
                    "UPDATE campaign_states SET lifecycle_state=?, payload_json=?, version=?, updated_at_utc=? WHERE campaign_id=?",
                    (new_state["lifecycle_state"], canonical_json_text(new_state), new_state["version"], timestamp, campaign_id),
                )
        return new_state
```

### Stage 3 — Router

**`api/routers/campaigns.py`**
```python
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from ca_contracts import canonical_sha256, utc_now_rfc3339
from api.dependencies import get_campaign_repository, get_harness_library_root, get_interview
from api.domain.campaign import CampaignValidationError, create_campaign_order, default_autonomy_policy, launch_campaign, transition_campaign
from api.errors import ErrorResponse
from api.harness_library import find_by_definition_id
from api.schemas.campaigns import CampaignCancelRequest, CampaignCreateRequest, CampaignDetailResponse, CampaignSummary
from api.services.campaign_repository import CampaignConflictError, CampaignNotFoundError, CampaignRepository
from conscious_activations_interview_expression.errors import NotFoundError as InterviewNotFoundError

router = APIRouter()

READY_SOURCE_STATES = {"COMPONENTS_IN_PROGRESS", "PUBLISHED_DERIVATIVE_ELIGIBLE"}

_VALIDATION_STATUS = {
    "EMPTY_VALUE": 400, "INVALID_INTEGER": 400, "INVALID_SHA256": 400,
    "OUTPUT_TARGET_REQUIRED": 400, "INVALID_ID_PREFIX": 400, "FORMAT02_DEFERRED": 422,
}


def _error(status_code: int, error_code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail=ErrorResponse(
        error_code=error_code, message=message, timestamp=utc_now_rfc3339(),
    ).model_dump())


def _build_actor(operator_id: str) -> dict:
    return {"actor_id": operator_id, "actor_type": "human", "product_id": "conscious-activations-studio", "workflow_role": "operator"}


def _build_authority() -> dict:
    # Fixed development-stage authority — matches the candidate_not_current
    # convention cmf_activative_intelligence.campaign._authority() already
    # uses elsewhere in this codebase (§1, §3). Not caller-supplied.
    stub_id = "ca-program-control-v2.1-candidate"
    return {
        "authority_id": stub_id,
        "authority_version": "2.1.0-candidate",
        "authority_sha256": canonical_sha256({"authority": stub_id}),
        "authority_state": "candidate_not_current",
    }


def _detail(order: dict, state: dict, package_payload: dict, idempotent_replay: bool) -> CampaignDetailResponse:
    return CampaignDetailResponse(
        order=order, state=state,
        source_derivative_eligible=bool(package_payload["derivative_eligible"]),
        source_lifecycle_state=package_payload["lifecycle_state"],
        pipeline_ingestion_status="NOT_YET_TRIGGERED",
        idempotent_replay=idempotent_replay,
    )


@router.post("", response_model=CampaignDetailResponse, status_code=201)
def create_campaign(
    body: CampaignCreateRequest,
    repository: CampaignRepository = Depends(get_campaign_repository),
    library_root=Depends(get_harness_library_root),
    interview=Depends(get_interview),
):
    try:
        package = interview.repository.get_object(body.source_package_id)
    except InterviewNotFoundError as error:
        raise _error(404, "SOURCE_PACKAGE_NOT_FOUND", str(error))
    lifecycle = package["payload"]["lifecycle_state"]
    if lifecycle not in READY_SOURCE_STATES:
        raise _error(422, "SOURCE_PACKAGE_NOT_READY",
                     f"source package '{body.source_package_id}' is {lifecycle}; expected one of {sorted(READY_SOURCE_STATES)}")
    source_ref = {"object_id": package["object_id"], "version": package["version"], "sha256": package["sha256"]}

    entry = find_by_definition_id(library_root, body.harness_definition_id)
    if entry is None:
        raise _error(404, "HARNESS_NOT_FOUND", f"no Harness with id '{body.harness_definition_id}' exists in the library")
    harness_category = entry.definition.content["category_binding"].get("category_id")
    if harness_category != body.category_id:
        raise _error(422, "HARNESS_INELIGIBLE",
                     f"Harness '{body.harness_definition_id}' is bound to category '{harness_category}', not requested '{body.category_id}'")
    harness_hash = entry.definition.definition_hash
    if harness_hash.startswith("sha256:"):
        harness_hash = harness_hash[len("sha256:"):]
    harness_ref = {"object_id": entry.definition.definition_id, "version": str(entry.definition.content["manifest_version"]), "sha256": harness_hash}

    core = {
        "workspace_id": body.workspace_id, "project_id": body.project_id,
        "source_kind": "CANONICAL_INTERVIEW_SOURCE_PACKAGE", "source_ref": source_ref, "harness_ref": harness_ref,
        "category_id": body.category_id, "format_profile_id": body.format_profile_id, "objective": body.objective,
        "initial_seed": body.initial_seed, "taste_direction": list(body.taste_direction),
        "output_targets": [t.model_dump() for t in body.output_targets], "budget_units": body.budget_units,
        "deadline_utc": body.deadline_utc, "autonomy_policy": default_autonomy_policy(body.autonomy_mode),
        "operator_actor": _build_actor(body.operator_id), "authority": _build_authority(),
    }
    try:
        order = create_campaign_order(core)
        state = launch_campaign(order)
    except CampaignValidationError as error:
        raise _error(_VALIDATION_STATUS.get(error.code, 400), error.code, str(error))

    result = repository.create(order, state, idempotency_key=body.idempotency_key)
    return _detail(result["order"], result["state"], package["payload"], result["idempotent_replay"])


@router.get("", response_model=list[CampaignSummary])
def list_campaigns(
    workspace_id: str | None = Query(default=None),
    project_id: str | None = Query(default=None),
    lifecycle_state: str | None = Query(default=None),
    repository: CampaignRepository = Depends(get_campaign_repository),
):
    rows = repository.list(workspace_id=workspace_id, project_id=project_id, lifecycle_state=lifecycle_state)
    return [
        CampaignSummary(
            campaign_id=row["state"]["campaign_id"], order_id=row["order"]["order_id"],
            workspace_id=row["order"]["workspace_id"], project_id=row["order"]["project_id"],
            category_id=row["order"]["category_id"], lifecycle_state=row["state"]["lifecycle_state"],
            autonomy_mode=row["state"]["autonomy_mode"], output_target_count=len(row["order"]["output_targets"]),
            budget_units=row["order"]["budget_units"], version=row["state"]["version"],
        )
        for row in rows
    ]


@router.get("/{campaign_id}", response_model=CampaignDetailResponse)
def get_campaign(campaign_id: str, repository: CampaignRepository = Depends(get_campaign_repository), interview=Depends(get_interview)):
    try:
        row = repository.get(campaign_id)
    except CampaignNotFoundError as error:
        raise _error(404, "CAMPAIGN_NOT_FOUND", str(error))
    package = interview.repository.get_object(row["order"]["source_ref"]["object_id"])
    return _detail(row["order"], row["state"], package["payload"], False)


@router.post("/{campaign_id}/cancel", response_model=CampaignDetailResponse)
def cancel_campaign(
    campaign_id: str, body: CampaignCancelRequest,
    repository: CampaignRepository = Depends(get_campaign_repository),
    interview=Depends(get_interview),
):
    try:
        row = repository.get(campaign_id)
    except CampaignNotFoundError as error:
        raise _error(404, "CAMPAIGN_NOT_FOUND", str(error))
    if row["state"]["version"] != body.expected_version:
        raise _error(409, "CONFLICT", f"expected version {body.expected_version}, current {row['state']['version']}")
    try:
        new_state = transition_campaign(row["state"], "CANCELLED")
    except CampaignValidationError as error:
        raise _error(409, error.code, str(error))
    try:
        stored = repository.update_state(campaign_id, new_state, expected_version=body.expected_version)
    except CampaignConflictError as error:
        raise _error(409, "CONFLICT", str(error))
    package = interview.repository.get_object(row["order"]["source_ref"]["object_id"])
    return _detail(row["order"], stored, package["payload"], False)
```

### Stage 4 — Wiring

**`api/dependencies.py`** — add:
```python
def get_campaign_repository(request: Request) -> "CampaignRepository":
    return request.app.state.campaign_repository
```

**`api/main.py`** — additive inside `lifespan()`:
```python
    from api.services.campaign_repository import CampaignRepository
    campaign_db_path = config.ca_data_root / "campaigns" / "campaigns.sqlite3"
    campaign_repository = CampaignRepository(campaign_db_path)
    campaign_repository.initialize()
    app.state.campaign_repository = campaign_repository
```
and, alongside the other `include_router` calls:
```python
    from api.routers import campaigns
    app.include_router(campaigns.router, prefix="/api/campaigns", tags=["campaigns"])
```

No other file from TS-APP-API-001/002/003 is modified.

---

## 8. Failure, Migration, Rollback, Recovery, and Observability

| Failure scenario | Behaviour | Evidence |
|---|---|---|
| `source_package_id` unknown | 404 `SOURCE_PACKAGE_NOT_FOUND` before any write | no rows written to `campaign_orders`/`campaign_states` |
| `harness_definition_id` unknown | 404 `HARNESS_NOT_FOUND` before any write | same |
| Concurrent identical create (race) | `BEGIN IMMEDIATE` serializes; second caller either replays via idempotency key or reads back the first caller's committed rows | `idempotent_replay: true` on the losing caller's response |
| Cancel with stale `expected_version` | 409 `CONFLICT`, no state change | `campaign_states.version` unchanged in DB |
| Cancel on `SHIPPED`/already-`CANCELLED` campaign | 409 `CAMPAIGN_TRANSITION_DENIED` | `ALLOWED_TRANSITIONS["SHIPPED"] == ()` / `["CANCELLED"] == ()` |

**Migration:** this spec introduces one new SQLite database, `{CA_DATA_ROOT}/campaigns/campaigns.sqlite3`, following exactly the bootstrap convention (`ProductDatabase.initialize()` + an idempotent `executescript`) every other service already uses. No existing database is touched. No migration of existing data is required.

**Rollback:** removing `app.include_router(campaigns.router, ...)` from `api/main.py` fully disables this spec's routes. `campaigns.sqlite3` can be deleted in a development environment with no effect on any other service's data — source packages (`interview` service) and Harness definitions (`builder` service / harness library directory) live in entirely separate stores.

**Observability:** this spec relies on the uvicorn access log already established by TS-APP-API-001; it introduces no new log stream. `CampaignRepository.status()` returns a `ProductHealth`-compatible dict so that adding `campaigns` as a sixth key to `GET /api/health` (§2, explicitly out of scope here) is a mechanical follow-up, not a redesign.

---

## 9. Acceptance Criteria

**AC-001 — Campaign creation succeeds for a ready source and eligible harness**
Given a source package at `COMPONENTS_IN_PROGRESS` and a Harness in the library whose `category_binding.category_id` matches the request,
When `POST /api/campaigns` is called with valid fields,
Then the response is HTTP 201 with `state.lifecycle_state == "LAUNCHED"`, `state.version == 1`, and `pipeline_ingestion_status == "NOT_YET_TRIGGERED"`.
Test layer: integration — `tests/api/test_campaigns_create.py::test_create_succeeds`.

**AC-002 — Unknown source package is rejected**
Given `source_package_id` does not exist,
When `POST /api/campaigns` is called,
Then HTTP 404 `SOURCE_PACKAGE_NOT_FOUND`, and no row is written to `campaign_orders` or `campaign_states`.
Test layer: integration — `test_unknown_source_package_returns_404`.

**AC-003 — Source package not yet ready is rejected**
Given a source package still at `ADMITTED` (zero components bound),
When `POST /api/campaigns` is called,
Then HTTP 422 `SOURCE_PACKAGE_NOT_READY`.
Test layer: integration — `test_admitted_only_source_rejected`.

**AC-004 — Unknown harness is rejected**
Given `harness_definition_id` does not exist in the library,
When `POST /api/campaigns` is called,
Then HTTP 404 `HARNESS_NOT_FOUND`.
Test layer: integration — `test_unknown_harness_returns_404`.

**AC-005 — Category-mismatched harness is rejected**
Given a Harness bound to category `carousels` and a request with `category_id: "short_form_edited_video"`,
When `POST /api/campaigns` is called,
Then HTTP 422 `HARNESS_INELIGIBLE`.
Test layer: integration — `test_harness_category_mismatch_rejected`.

**AC-006 — Format 02 remains deferred**
Given `category_id: "2d_character_animation"` or `format_profile_id` starting with `"format02_"`,
When `POST /api/campaigns` is called,
Then HTTP 422 `FORMAT02_DEFERRED`.
Test layer: unit — `tests/api/test_domain_campaign.py::test_format02_deferred`; integration — `test_format02_rejected_end_to_end`.

**AC-007 — Missing output targets is rejected**
Given `output_targets: []`,
When `POST /api/campaigns` is called,
Then HTTP 400 `OUTPUT_TARGET_REQUIRED`.
Test layer: unit — `test_output_target_required`.

**AC-008 — Sub-minimum budget is rejected**
Given `budget_units: 0`,
When `POST /api/campaigns` is called,
Then HTTP 400 `INVALID_INTEGER`.
Test layer: unit — `test_budget_units_minimum`.

**AC-009 — Exact-retry idempotency**
Given a successful `POST /api/campaigns` with `idempotency_key: "k1"`,
When the identical request is repeated with the same `idempotency_key`,
Then the response is the same `campaign_id`/`order_id` with `idempotent_replay: true`, and no second row is inserted.
Test layer: integration — `test_exact_idempotency_key_replay`.

**AC-010 — Content-addressed idempotency across different keys**
Given a successful `POST /api/campaigns` with `idempotency_key: "k1"`, producing `campaign_id: C`,
When a logically identical request (same core fields) is submitted with `idempotency_key: "k2"`,
Then the response returns the same `campaign_id: C` with `idempotent_replay: true`, and the returned `state` reflects any transitions already applied to `C` (not a fresh `version: 1`).
Failure example: a naive implementation resets `C` back to `LAUNCHED`/`version: 1`, silently erasing a prior cancellation.
Test layer: integration — `test_content_addressed_replay_preserves_current_state`.

**AC-011 — List and filter**
Given three campaigns across two workspaces,
When `GET /api/campaigns?workspace_id=workspace:acme-coach` is called,
Then only campaigns in that workspace are returned, as `CampaignSummary` items, ordered most-recent-first.
Test layer: integration — `test_list_filters_by_workspace`.

**AC-012 — Detail for unknown campaign**
When `GET /api/campaigns/does-not-exist` is called,
Then HTTP 404 `CAMPAIGN_NOT_FOUND`.
Test layer: integration — `test_get_unknown_campaign_404`.

**AC-013 — Cancel transitions LAUNCHED to CANCELLED**
Given a campaign at `LAUNCHED`, `version: 1`,
When `POST /api/campaigns/{id}/cancel` is called with `expected_version: 1`,
Then the response shows `lifecycle_state: "CANCELLED"`, `version: 2`.
Test layer: integration — `test_cancel_launched_campaign`.

**AC-014 — Cancel twice is rejected**
Given a campaign already at `CANCELLED`,
When `POST /api/campaigns/{id}/cancel` is called again,
Then HTTP 409 `CAMPAIGN_TRANSITION_DENIED`.
Test layer: integration — `test_cancel_already_cancelled_rejected`.

**AC-015 — Stale version on cancel is rejected**
Given a campaign at `version: 2`,
When `POST /api/campaigns/{id}/cancel` is called with `expected_version: 1`,
Then HTTP 409 `CONFLICT`, and no state change is written.
Test layer: integration — `test_cancel_stale_version_conflict`.

**AC-016 — No regression**
Given the Phase 9 test suite at `tests/` was passing before this spec,
When this spec is fully implemented and `python -m pytest tests/ -q` is run,
Then all pre-existing tests continue to pass.
Test layer: regression — run full existing suite.

---

## 10. Testing and Completion Evidence

### Test files to create

**`tests/api/test_domain_campaign.py`** (pure unit tests, no FastAPI, no database)
- `test_deterministic_id_matches_ts_algorithm_shape` — cross-checks `deterministic_id` output format against `canonical_sha256`
- `test_validate_campaign_order_rejects_empty_workspace`
- `test_output_target_required` — AC-007
- `test_budget_units_minimum` — AC-008
- `test_format02_deferred` — AC-006 (both `category_id` and `format_profile_id` trigger paths)
- `test_default_autonomy_policy_shapes` — all four `AutonomyMode` values
- `test_transition_campaign_denies_illegal_transition`
- `test_transition_campaign_denies_shadow_ship`

**`tests/api/fixtures/`**
- Reuses the interview fixtures already established by `tests/api/test_interviews_import.py` (TS-APP-API-003) to admit a real source package and bind at least one component, reaching `COMPONENTS_IN_PROGRESS`
- Reuses the harness fixture manifests already established by TS-APP-API-002's `tests/api/fixtures/harnesses/` to build a real Harness in the library

**`tests/api/test_campaigns_create.py`**
- `test_create_succeeds` — AC-001
- `test_unknown_source_package_returns_404` — AC-002
- `test_admitted_only_source_rejected` — AC-003
- `test_unknown_harness_returns_404` — AC-004
- `test_harness_category_mismatch_rejected` — AC-005
- `test_format02_rejected_end_to_end` — AC-006
- `test_exact_idempotency_key_replay` — AC-009
- `test_content_addressed_replay_preserves_current_state` — AC-010

**`tests/api/test_campaigns_list_and_get.py`**
- `test_list_filters_by_workspace` — AC-011
- `test_get_unknown_campaign_404` — AC-012

**`tests/api/test_campaigns_cancel.py`**
- `test_cancel_launched_campaign` — AC-013
- `test_cancel_already_cancelled_rejected` — AC-014
- `test_cancel_stale_version_conflict` — AC-015

### Test tooling

```python
from fastapi.testclient import TestClient
from api.main import app

def test_create_succeeds(ready_source_package_id, eligible_harness_definition_id):
    with TestClient(app) as client:
        response = client.post("/api/campaigns", json={
            "idempotency_key": "test-key-1",
            "workspace_id": "workspace:test", "project_id": "project:test",
            "source_package_id": ready_source_package_id,
            "harness_definition_id": eligible_harness_definition_id,
            "category_id": "short_form_edited_video",
            "format_profile_id": "format07_direct_coaching_a_roll",
            "objective": "Preserve source expression", "initial_seed": "A source-backed seed",
            "taste_direction": ["identity-first"],
            "output_targets": [{"output_type": "SOURCE_LED_SHORT", "quantity": 1, "profile_id": "format07_direct_coaching_a_roll"}],
            "budget_units": 100, "deadline_utc": None,
            "autonomy_mode": "REVIEW_BEFORE_SHIP", "operator_id": "operator:jane",
        })
        assert response.status_code == 201
        body = response.json()
        assert body["state"]["lifecycle_state"] == "LAUNCHED"
        assert body["pipeline_ingestion_status"] == "NOT_YET_TRIGGERED"
```

### Pre-existing regression
```bash
python -m pytest tests/ -q --tb=short
```
Zero new failures is a hard gate (AC-016).

### Build Receipt claim ceiling
`CAMPAIGN_ORDER_PRE_PUBLICATION_SOURCE_EVIDENCE`

This spec does not claim:
- Pipeline execution has started for any campaign it creates (Source Gap Notice 2 remains open)
- that a selected Harness is executable by the Pipeline (Gap 4, inherited from TS-APP-API-002, remains open)
- that the source package has completed Expression Moment approval or is `derivative_eligible` (surfaced transparently, never gated on)
- authentication, authorization, or multi-tenant isolation
- certified or production-authorized operation

---
spec_end: true
next_spec: TS-APP-API-005 (Pipeline Status WebSocket)
prerequisite_for_next: AC-001, AC-013 must pass (a campaign can be created and cancelled) before TS-APP-API-005 implementation begins
blocking_risk_for_downstream: Source Gap Notice 2 (no AIR HTTP surface exists to supply `ContentBatchService.compile_batch()`'s required refs) must be closed by a dedicated Activative Intelligence API spec before TS-APP-API-005 can claim it is watching real Pipeline node execution rather than a campaign that never actually left LAUNCHED. Gap 4 (Builder/Pipeline schema mismatch, from TS-APP-API-002) remains open for the same reason.
open_question_for_next_spec_author: TS-APP-API-005 must decide how `ws://api/campaigns/:id/status` should represent a campaign whose `pipeline_ingestion_status` is still `NOT_YET_TRIGGERED` — whether to accept the WebSocket connection and emit a single terminal "not yet running" event, or to reject the connection outright until a future ingestion spec sets a different status. This spec deliberately leaves that decision to TS-APP-API-005's author rather than guessing at it.
---
