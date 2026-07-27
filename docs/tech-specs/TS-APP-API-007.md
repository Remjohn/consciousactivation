---
spec_id: TS-APP-API-007
title: Activative Intelligence API
document_class: TECH_SPEC
product: Conscious Activations
module: api
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CURRENT
build_authority: false
controlling_frs:
  - FR-APP-031 (Activation Hypothesis Portfolio — "AIR generates a portfolio of
    meaningfully different Activation Hypotheses ... The operator reviews and
    selects one")
  - FR-APP-032 (Final Script compilation and approval — "The operator approves
    before composition begins")
controlling_stories:
  - ST-APP-05.01 through ST-APP-05.04 are named only by range against Epic 5
    in `CA_APP_FR_EPIC_SPEC_PLAN.md` Part 2; Part 3 ("Selected Critical Path")
    contains no written acceptance text for any of them — the same situation
    TS-APP-API-006 already documented for ST-APP-08.02/03/05. Following that
    precedent, this spec derives its acceptance criteria directly from
    FR-APP-031 and FR-APP-032, not from invented story text.
upstream_dependencies:
  - CA_PROJECT_SNAPSHOT.md (authority — CURRENT)
  - CA_APP_FR_EPIC_SPEC_PLAN.md (authority — CURRENT)
  - SPEC_GAP_LEDGER.md (authority — CURRENT; this spec is the direct
    resolution of GAP-001, "No Activative Intelligence (AIR) HTTP API exists
    anywhere in the spec queue")
  - TS-APP-API-001.md (quality_state: WRITTEN_PENDING_AUDIT —
    DRAFT_DEPENDENCY_NOT_ACCEPTED; this spec depends only on its
    `api/dependencies.py::get_air` factory, `api/config.py::AppConfig`/
    `load_config`, and `api/errors.py::ErrorResponse` interfaces, not on any
    claim that the gateway is production-ready)
  - TS-APP-API-003.md (quality_state: WRITTEN_PENDING_AUDIT —
    DRAFT_DEPENDENCY_NOT_ACCEPTED; this spec reuses `api/schemas/interviews.py::
    RefModel` unchanged, the same reuse TS-APP-API-004 already performed)
  - TS-APP-API-004.md (quality_state: WRITTEN_PENDING_AUDIT —
    DRAFT_DEPENDENCY_NOT_ACCEPTED; TS-APP-API-004's Source Gap Notice 2 is
    the finding this spec exists to close — see Section 1, Source gap notice A)
downstream_consumers:
  - TS-APP-API-004 (Campaign CRUD API — its `compile_batch()` Stage must be
    revisited once this spec exists, per SPEC_GAP_LEDGER.md "Resolution
    Sequence" step 9; this spec's `GET /api/air/scripts/{script_id}` response
    is the read path that supplies the refs that revisit needs)
  - TS-APP-UI-002 / TS-APP-UI-003 (not yet written — the future hypothesis
    comparison UI (FR-APP-031) and Final Script review/approval UI (FR-APP-032)
    are direct consumers of every endpoint in this spec)
output_path: api/routers/air.py (and supporting files listed in Section 7)
wave: 1
---

# TS-APP-API-007 — Activative Intelligence API

## 1. Files and Authorities Read

| File | SHA-256 (short) | Status | Fact extracted |
|---|---|---|---|
| `services/air/src/cmf_activative_intelligence/services/hypothesis_service.py` | `744fb8b7` | READ — CURRENT IMPLEMENTATION | `HypothesisService` exposes `store_hypothesis`, `store_portfolio`, `gate_hypothesis`, `compare_portfolio`, `stop_search`, `store_planned_pack`, `promote` — seven separate methods, none of which call each other. `gate_hypothesis`/`compare_portfolio` take `outcomes`/`candidate_scores` as **caller-supplied** judgment inputs; the code performs no evaluation of its own (comment: `"deterministic development check"`) |
| `services/air/src/cmf_activative_intelligence/services/derivative_service.py` | `604fea5f` | READ — CURRENT IMPLEMENTATION | `DerivativeService.store_script` stores a `final_script_package` whose payload already embeds `archetype_coalition_ref` and `primitive_coalition_ref` directly. `approve_script(candidate_script_ref, operator_id, operator_decision_ref, evaluation_refs, rationale, approval_idempotency_key, script_revision_idempotency_key)` stores a `final_script_approval_receipt` and then a **new revision** of the same `script_id` with `operator_approved: true, composition_eligible: true` |
| `services/air/src/cmf_activative_intelligence/services/transfer_service.py` | `e729d448` | READ — CURRENT IMPLEMENTATION | `TransferService.store_contract` is the **only** code path that produces an `activation_transfer_contract` object. It is never called by `derivative_service.py`, never called by any demo flow automatically after approval, and is not named anywhere in `SPEC_GAP_LEDGER.md` GAP-001's four-ref list — see Source gap notice B below |
| `services/air/src/cmf_activative_intelligence/services/production_common.py` | `a657f4f0` | READ — CURRENT IMPLEMENTATION | `require_air_ref` fetches by `object_id` and checks `object_type`, `semantic_version`, and `canonical_sha256` against the caller-supplied ref — the same three-field shape as Pipeline's `require_ref`. `add_lineage_edges` writes edges **from** the newly-stored object **to** every ref in `target_refs`, via `repository.add_object_edge(source_ref=<new object>, target_ref=<input ref>, ...)` |
| `services/air/src/cmf_activative_intelligence/services/semantic_authority.py` | `8ea76a8e` | READ — CURRENT IMPLEMENTATION | `SemanticAuthorityService.validate`/`.store` are thin wrappers around `domain.py::validate_air_object` and `AirRepository.store_object`; no HTTP concerns, safe to call directly from a router |
| `services/air/src/cmf_activative_intelligence/production_domain.py` | `dfdf4b90` | READ — CURRENT IMPLEMENTATION | Exact required-field sets for every object type this spec touches (`activation_hypothesis`, `activation_hypothesis_portfolio`, `hypothesis_gate_result`, `comparative_evaluation_receipt`, `hypothesis_stopping_receipt`, `planned_activative_intelligence_pack`, `hypothesis_promotion_receipt`, `final_script_package`, `final_script_approval_receipt`, `activation_transfer_contract`). `PRODUCTION_ID_FIELDS` confirms the id-field name for every one — `portfolio_id` for the portfolio, `script_id` for Final Script, `contract_id` for the transfer contract. **There is no object type anywhere named or shaped like `package_id` for a hypothesis portfolio** — see Source gap notice C |
| `services/air/src/cmf_activative_intelligence/domain.py` | `90b64dea` | READ — CURRENT IMPLEMENTATION | `_ref`/`_refs` enforce refs are exactly `{object_id, version, sha256}` — byte-identical to Pipeline's `require_ref` allowed-field set; no translation needed between AIR refs and Pipeline refs (contrast with Gap 4/GAP-002, a real Builder↔Pipeline mismatch this spec does **not** have) |
| `services/air/src/cmf_activative_intelligence/repositories/air_repository.py` | `b9748b8d` | READ — CURRENT IMPLEMENTATION | `AirRepository.get_object(object_id)` always returns the current (`is_current=1`) revision. `list_edges(object_id, *, outgoing=True)` supports **incoming** edges (`outgoing=False`) — this is how this spec resolves "which transfer contract governs this script" without any new index or migration. `store_object(..., expected_revision=...)` is optimistic-concurrency revisioning; `StoredAirObject.immutable_ref()` returns exactly `{object_id, version: semantic_version, sha256: canonical_sha256}` |
| `services/air/src/cmf_activative_intelligence/application.py` | `02784b27` | READ — CURRENT IMPLEMENTATION | `AirApplication` exposes `.hypotheses` (`HypothesisService`), `.derivatives` (`DerivativeService`), `.transfer` (`TransferService`), `.repository` (`AirRepository`) as public attributes — exactly what `api/dependencies.py::get_air` (TS-APP-API-001) already returns |
| `services/air/src/cmf_activative_intelligence/production_demo.py` | `1c01678c` | READ — CURRENT IMPLEMENTATION | The only place in the whole codebase that exercises the full hypothesis chain end to end (`store_portfolio` → `gate_hypothesis` ×N → `compare_portfolio` → `stop_search` → `store_planned_pack` → `promote` → **`store_portfolio` again**, `expected_revision=1`, with `portfolio_state: "PROMOTED"`). This confirms the service methods do **not** update the portfolio object themselves — the caller must re-store it. This spec's `expected_revision` is read from the fetched object at request time, not hardcoded to `1` as the demo does (the demo only ever runs once per fresh database) |
| `services/pipeline/src/cmf_pipeline/batch/service.py` | `d1553853` | READ — CURRENT IMPLEMENTATION | `ContentBatchService._compile_job` requires, per route: `semantic_program_ref`, `final_script_ref`, `archetype_coalition_ref`, `primitive_coalition_ref`, `activation_transfer_contract_ref` — **five** AIR-sourced refs, not four. `SPEC_GAP_LEDGER.md` GAP-001 named only four; `semantic_program_ref` is the fifth and is also produced by AIR (`derivative_activation_program.program_id` — see Source gap notice D) |
| `services/pipeline/src/cmf_pipeline/domain/validation.py` | `7efb85f4` | READ — CURRENT IMPLEMENTATION | `require_ref` requires exactly `{object_id, version, sha256}` with `version` matching `_SEMVER` and `sha256` a bare 64-char lowercase hex digest (`sha256:` prefix stripped if present). AIR's own `_ref` never emits a `sha256:` prefix, so — unlike GAP-005 (Harness `definition_hash`) — **no projection is needed** between an AIR ref and a Pipeline `require_ref` value; they are structurally identical already |
| `SPEC_GAP_LEDGER.md` | `941de7ba` | READ — AUTHORITY, CURRENT | GAP-001 is this spec's mandate. Its four required endpoints and four-ref claim are the floor this spec must meet, not the ceiling — see Source gap notices B and D for where the floor undercounts what `compile_batch()` actually needs |
| `CA_APP_FR_EPIC_SPEC_PLAN.md` | `8ea2646c` | READ — AUTHORITY, CURRENT | FR-APP-031/032 text and the `services/air/src/` path convention this spec's file citations follow |
| `TS-APP-API-004.md` | `4d261cc7` | READ — WRITTEN_PENDING_AUDIT | Source Gap Notice 2 is the finding this spec closes. Its own file-read table (line citing `batch/service.py`) already lists `semantic_program_ref` alongside the other four AIR refs — TS-APP-API-004 saw the fifth ref too; GAP-001's ledger summary just didn't carry it forward |
| `TS-APP-API-005.md` | `93d601aa` | READ — WRITTEN_PENDING_AUDIT | **ID collision, not a technical dependency.** TS-APP-API-005's own "Gap A" (no autonomous Pipeline worker/dispatcher exists) recommends `"suggested id TS-APP-API-007"` for a future Worker/Dispatcher spec. `SPEC_GAP_LEDGER.md` GAP-001 independently assigned the same ID to *this* spec (Activative Intelligence API). This document is written under the ledger's assignment, per the user's explicit instruction. The Worker/Dispatcher spec TS-APP-API-005 recommended still needs to be written — under a different ID (`TS-APP-API-008` is the next free slot) — see Source gap notice E |
| `TS-APP-API-002.md` | `a61d6b93` | READ — WRITTEN_PENDING_AUDIT | Confirms the "wrap an existing, already-persistent Python service" spec shape this document follows (Stage 1 adapter module → Stage 2 router → Stage 3 wiring), as opposed to TS-APP-API-004's shape (which had to invent its own domain + persistence because no `cmf_campaigns` package exists). AIR already owns persistence for everything this spec touches, so this spec follows API-002's shape, not API-004's |
| `TS-APP-API-003.md` | (not independently hashed; content quoted from TS-APP-API-004's own citation) | READ — WRITTEN_PENDING_AUDIT | Origin of the shared `RefModel` (`{object_id, version, sha256}`) this spec imports unchanged |
| `TS-APP-API-006.md` | `bfed8e44` | READ — WRITTEN_PENDING_AUDIT | Precedent for deriving acceptance criteria from FR text directly when story text doesn't exist (used in `controlling_stories` above) |

### Source gap notices (read carefully — these govern this spec's design)

**Source gap notice A — this spec is the direct closure of TS-APP-API-004 Source Gap Notice 2 / SPEC_GAP_LEDGER GAP-001.** No further explanation needed beyond what GAP-001 already documented; this spec exists because that gap does.

**Source gap notice B — GAP-001's own resolution instructions omit the one endpoint that actually produces `activation_transfer_contract_ref`.** GAP-001 asked for exactly four endpoints: list portfolio, select hypothesis, view Final Script, approve Final Script. None of those four — read literally — ever calls `TransferService.store_contract()`. Approving a Final Script (`DerivativeService.approve_script`) only sets `operator_approved: true` on the script; it does not create an `activation_transfer_contract`. Without one, `activation_transfer_contract_ref` — one of GAP-001's own four named refs — can never be obtained through the four endpoints GAP-001 asked for. **This spec adds a fifth endpoint, `POST /api/air/scripts/{script_id}/transfer-contract`, beyond GAP-001's literal list, because without it this spec would satisfy the letter of GAP-001 while leaving its stated goal ("compile_batch() can get the four refs it needs") unmet.** This is flagged prominently rather than silently added — see Section 2, In scope.

**Source gap notice C — GAP-001's suggested route `GET /api/air/hypotheses/{package_id}` names the wrong path parameter.** `production_domain.py::PRODUCTION_ID_FIELDS` shows the hypothesis portfolio's id field is `portfolio_id`; `package_id` belongs to two unrelated object types (`animation_scene_package`, `semantic_production_package`) that this spec does not touch. This spec uses `{portfolio_id}` and `{script_id}` throughout, not `{package_id}`/`{id}` as GAP-001's prose loosely wrote them, per the "verify against the code directly, do not infer" instruction GAP-001 itself gives.

**Source gap notice D — `compile_batch()` needs a fifth AIR-sourced ref, `semantic_program_ref`, that GAP-001 did not name.** `batch/service.py::_compile_job` requires `semantic_program_ref` per route in addition to the four GAP-001 named. It is the immutable ref to the `derivative_activation_program` object (`program_id`) that produced the Final Script — the same object AIR's own `final_script_package.program_ref` field already points to (field name differs: AIR calls it `program_ref`, Pipeline calls the equivalent route field `semantic_program_ref`; both reference the same `derivative_activation_program` object type, confirmed by reading both schemas directly — this is a naming difference, not a structural one, so no translation layer is needed, only a field-name projection at the response boundary, the same pattern GAP-005 already established for `HarnessDetail.definition_hash`). `GET /api/air/scripts/{script_id}` exposes it as `semantic_program_ref` in its `batch_compilation_refs` sub-object for exactly this reason.

**Source gap notice E — the Worker/Dispatcher spec TS-APP-API-005 recommended under the ID `TS-APP-API-007` still needs to be written, under a new ID.** This is not a defect in this spec; it is a bookkeeping note for whoever writes it: use `TS-APP-API-008`, since `TS-APP-API-007` is now this document.

**Source gap notice F — FR-APP-030/FR-APP-031's own "Missing" lines never asked for an HTTP trigger to *create* a hypothesis or portfolio, and this spec does not add one.** `CA_APP_FR_EPIC_SPEC_PLAN.md` lists FR-APP-030 as missing "HTTP trigger endpoint" and FR-APP-031 as missing "HTTP endpoint" (singular, for the review/selection surface) — read together with the story text ("The operator reviews and selects one"), the product flow this spec is chartered to build is *review and select an already-generated portfolio*, not *generate* one. Portfolio/hypothesis generation (calling `store_hypothesis`/`store_portfolio` for the first time, with `portfolio_state: "OPEN"`) remains development-mode-only, reachable today solely through `production_demo.py` or direct Python. **This is a real, separate gap** — an operator cannot get a portfolio to review without either a not-yet-written FR-APP-030/031 "generate" endpoint or someone running the demo/CLI by hand — but it is not this spec's gap to close, and closing it here would silently expand scope past what GAP-001 asked for. Flagged and left open.

---

## 2. Problem, User Outcome, Solution, and Scope

### Problem without this spec
Every object Activative Intelligence produces — the Activation Hypothesis Portfolio an operator must compare and choose from, the Final Script an operator must review and approve, the Activation Transfer Contract that governs what may change between script and finished video — exists only as rows in an AIR SQLite database, reachable only by importing `cmf_activative_intelligence` in a Python shell or by re-running `production_demo.py`. `ContentBatchService.compile_batch()` — the one function that actually starts a real Pipeline run — requires five refs from these objects, in exact field names, and today there is no way for an HTTP caller (a future React UI, or the Pi Coding Agent) to obtain even one of them. Every campaign TS-APP-API-004 can create is permanently stuck at `pipeline_ingestion_status: "NOT_YET_TRIGGERED"` because of this.

### User outcome
An operator (today: a developer calling the API directly; later: the FR-APP-031/032 review screens) can `GET /api/air/hypotheses/{portfolio_id}` and see every candidate hypothesis side by side — role, tension, stakes, activation directions, and (once gated/compared) eligibility and score. They call `POST /api/air/hypotheses/{portfolio_id}/select` once, supplying their judgment for every candidate, and the portfolio is gated, compared, stopped, and promoted in one call, with their chosen candidate now the durable `selected_hypothesis_ref`. They call `GET /api/air/scripts/{script_id}` to read the Final Script's exact segment text, transformation classes, and source lineage, and `POST /api/air/scripts/{script_id}/approve` to approve it — the same operator-approval gate FR-APP-032 requires before composition begins. Once approved, they call `POST /api/air/scripts/{script_id}/transfer-contract` to record what must survive and what may change downstream, and from that point on `GET /api/air/scripts/{script_id}` returns a `batch_compilation_refs` object holding exactly the five refs `ContentBatchService.compile_batch()` needs, in its exact field names, ready to paste into a Pipeline route.

### Solution
`api/routers/air.py` exposing five routes, backed by a new `api/services/air_adapter.py` module that owns every multi-step AIR orchestration (the hypothesis-selection chain, the transfer-contract-lookup-by-reverse-edge) so the router itself stays a thin request/response translation layer, and a new `api/schemas/air.py` module holding every Pydantic model:

- `GET /api/air/hypotheses/{portfolio_id}` — full portfolio detail with per-candidate comparison data
- `POST /api/air/hypotheses/{portfolio_id}/select` — orchestrates gate → compare → stop → plan → promote → portfolio-revision in one call
- `GET /api/air/scripts/{script_id}` — full Final Script detail, including `batch_compilation_refs` once approved and a transfer contract exists
- `POST /api/air/scripts/{script_id}/approve` — the FR-APP-032 operator approval gate
- `POST /api/air/scripts/{script_id}/transfer-contract` — closes Source gap notice B; the only way to obtain `activation_transfer_contract_ref`

### In scope
- `api/schemas/air.py` — every request/response Pydantic model for this spec
- `api/services/air_adapter.py` — pure-ish orchestration functions that call into `AirApplication.hypotheses` / `.derivatives` / `.transfer` / `.repository`; the reverse-edge lookup that finds a script's transfer contract; the field-name projection from AIR's `program_ref` to Pipeline's `semantic_program_ref`
- `api/routers/air.py` — the five routes, error mapping
- `api/main.py` — register `air.router` (additive; `get_air` already exists from TS-APP-API-001, no patch needed — contrast with TS-APP-API-002's Stage 0 corrective patch, which this spec does not need)
- The fifth endpoint (`POST /api/air/scripts/{script_id}/transfer-contract`), added beyond GAP-001's literal four, per Source gap notice B

### Out of scope
- Generating a hypothesis or a portfolio for the first time (`store_hypothesis`, first `store_portfolio` call with `portfolio_state: "OPEN"`) — per Source gap notice F, this is a separate, still-open gap (FR-APP-030/031's own "generate" endpoints), not GAP-001's
- Matrix of Edging / Edge Product formation (FR-APP-030) — upstream of everything this spec touches; still missing its own HTTP trigger per the FR plan
- `POST /api/air/scripts/{script_id}/proposal` or any other JIT-authoring/proposal-generation route (`store_jit_request`, `store_proposal`) — those produce the *candidate* script content this spec's `/approve` route only reviews and approves; generating proposal content is out of scope for the same reason hypothesis generation is
- Calling `ContentBatchService.compile_batch()` itself — that remains TS-APP-API-004's responsibility once it revisits its Stage per SPEC_GAP_LEDGER.md's Resolution Sequence step 9; this spec only makes the refs obtainable
- Resolving GAP-002 (Harness/Pipeline schema mismatch) — unrelated to AIR, tracked separately under TS-APP-BRIDGE-001
- Animation Scene Package or Semantic Production Package endpoints (`store_animation_package`, `store_semantic_package`) — downstream of Final Script approval but not required by `compile_batch()`'s route fields; deferred to a future spec if a real product need appears
- Authentication/authorization — still deferred per `CA_PROJECT_SNAPSHOT.md`, same as every other Wave 1/2 API spec
- Any modification to `cmf_activative_intelligence` or `cmf_pipeline` Python packages themselves

---

## 3. Governing Decisions and Constraints

**AIR already owns persistence; this spec adds no database of its own.** Every object this spec's routes read or write is stored by `AirRepository` (SQLite, already initialized by `AirApplication.initialize()` per TS-APP-API-001). This spec's `api/services/air_adapter.py` module holds orchestration logic only — no `CREATE TABLE`, no new SQLite file.

**`POST /api/air/hypotheses/{portfolio_id}/select` performs the entire gate → compare → stop → plan → promote chain as one synchronous HTTP call, and this spec performs no evaluation of its own.** `HypothesisService.gate_hypothesis` and `.compare_portfolio` take `outcomes: Mapping[str, bool]` and `candidate_scores: Mapping[str, Mapping[str, int]]` as caller-supplied inputs — the underlying code does not judge anything; its own comment calls this a `"deterministic development check"`. Consistent with that, this endpoint requires the caller (the operator, via a future comparison UI, or a developer today) to supply a `CandidateJudgment` for **every** candidate in the portfolio: per-gate pass/fail for all ten `HYPOTHESIS_GATES`, and per-dimension integer-micro scores for all seven `EVALUATION_DIMENSIONS`. This spec does not fabricate, infer, or default any of these values — doing so would be inventing the exact judgment the codebase itself explicitly reserves for a human or a not-yet-built model step. `AirApplication.status()` reports `external_model_calls: 0`; this spec keeps that true.

**The endpoint validates that the caller's stated pick is what the comparison actually decides, and refuses to silently override either.** If `compare_portfolio`'s resulting `decision` is not `DECISIVE_WINNER`, or is `DECISIVE_WINNER` for a *different* candidate than `selected_hypothesis_id`, this endpoint returns `409 SELECTION_NOT_SUPPORTED_BY_SCORES` with the actual decision and (if any) actual selected candidate in the response body, and performs no further writes (no `stop_search`, no `promote`, no portfolio revision). The operator must either change their pick or revise their per-candidate scores and retry. This is a deliberate design choice, not an oversight: silently promoting whichever candidate the scores decide, ignoring what the operator asked to select, would misrepresent whose decision `authority_decision_ref` records.

**The portfolio's `expected_revision` is read at request time, not hardcoded.** `production_demo.py` hardcodes `expected_revision=1` in its final `store_portfolio` call because the demo only ever runs once against a fresh database. This spec's adapter calls `air_app.repository.get_object(portfolio_id).revision` immediately before the final re-store and passes that value, so a portfolio that has already accumulated other (out-of-scope, not-yet-existing) revisions is still handled correctly under optimistic concurrency. A `409 CONFLICT` is returned if the revision changes between the initial fetch and the final write (see Section 8).

**A single caller-supplied `authority` value is reused across every AIR object this spec writes within one HTTP call.** `_base()` in `services/air/.../domain.py` requires an `authority: {authority_id, authority_version, authority_sha256, authority_state}` block on every object AIR stores. Rather than asking the caller for a separate authority block per gate result, per comparison, per stop receipt, per planned pack, per promotion receipt, and per portfolio revision — six to `10+N` separate identical-in-practice values — this spec accepts **one** `authority` field per request and reuses it verbatim for every object that request's orchestration creates. This mirrors how one HTTP call represents one coherent operator action taken under one authority context; it does not change what any individual AIR object requires.

**`api/schemas/air.py` defines its own `AirAuthorityRefModel` rather than importing `AuthorityRefModel` from `api/schemas/campaigns.py`.** `AuthorityRefModel` is defined inside TS-APP-API-004 (wave 2). This spec is wave 1 (it depends only on TS-APP-API-001, the same dependency depth as TS-APP-API-002/003) and importing from a later-wave module would invert the dependency direction the other wave-1 specs establish. The two models are structurally identical (`authority_id: str, authority_version: str, authority_sha256: str, authority_state: Literal["current", "candidate_not_current"]`, confirmed against `production_demo.py::_AUTHORITY`, whose `authority_state` value is `"candidate_not_current"`) — this is a deliberate duplication of a four-field model to avoid a wave-ordering violation, not a divergence in shape. `RefModel` (`{object_id, version, sha256}`), by contrast, is imported unchanged from `api/schemas/interviews.py` (also wave 1), the same reuse TS-APP-API-004 already performed.

**This spec enforces one precondition the underlying AIR code does not: a transfer contract may only be created for an *approved* Final Script.** `TransferService.store_contract` itself never checks `final_script.payload["operator_approved"]` — it only checks that `final_script_ref` resolves to a `final_script_package` at all. Left unchecked, `POST /api/air/scripts/{script_id}/transfer-contract` could be called against an unapproved candidate script, producing a transfer contract that could never legitimately support a `compile_batch()` call (whose route also carries the still-unapproved `final_script_ref`, but nothing downstream would ever reach it honestly). This spec's router checks `operator_approved is True` before calling `store_contract` and returns `409 SCRIPT_NOT_APPROVED` otherwise — a constraint this spec adds at the HTTP boundary, not a change to `cmf_activative_intelligence` itself.

**`GET /api/air/scripts/{script_id}` resolves `activation_transfer_contract_ref` by a reverse edge lookup, filtered to this exact script revision.** `add_lineage_edges` (called by `store_contract`) writes an edge from the new contract **to** `final_script_ref` with `relation_type="governs_transfer_of"`. `AirRepository.list_edges(script_id, outgoing=False)` returns every edge where `script_id` is the target, regardless of which revision of the contract's own `final_script_ref` pointed at it. Because `object_id` is stable across revisions but `version`/`sha256` are not, this spec's adapter fetches each matching edge's source object and keeps only contracts whose *own* `payload["final_script_ref"]` — version and sha256 included — matches the exact script revision currently being read, not just the same `object_id`. If more than one matching contract exists (not expected in normal use, since contract creation is content-addressed and idempotent, but not structurally prevented), the adapter selects the one with the latest `created_at_utc` and this is documented as a known limitation, not silently hidden.

**No float in canonical responses**, RFC 3339 timestamps, following the same `ca_contracts` conventions every prior API spec in this set established.

**Claim ceiling:** `ACTIVATIVE_INTELLIGENCE_API_DEVELOPMENT_EVIDENCE`. This spec does not claim: that any hypothesis judgment or script content was produced by a real model (`external_model_calls: 0` remains true); that Pipeline execution has started for any script this spec approves (that remains TS-APP-API-004's and, ultimately, TS-APP-API-007/008's — the not-yet-written Worker/Dispatcher spec's — claim to make); or that portfolio/hypothesis *generation* is reachable over HTTP (Source gap notice F).

---

## 4. Current Brownfield Architecture

| Component | Path | Actual behaviour | Disposition | Reason |
|---|---|---|---|---|
| `HypothesisService` | `services/air/src/cmf_activative_intelligence/services/hypothesis_service.py` | Seven independent methods; caller orchestrates and re-stores the portfolio | REUSE | Called by `air_adapter.py`'s orchestration functions; not modified |
| `DerivativeService` | `services/air/src/cmf_activative_intelligence/services/derivative_service.py` | `store_script`/`approve_script` fully implement the Final Script lifecycle including the approval-creates-new-revision pattern | REUSE | Called directly by the router for `/approve`; `store_script`/proposal-chain methods are out of scope (Source gap notice, In/Out of scope) |
| `TransferService` | `services/air/src/cmf_activative_intelligence/services/transfer_service.py` | `store_contract` is the only path to `activation_transfer_contract` | REUSE | Called by the new `/transfer-contract` route (Source gap notice B) |
| `AirRepository` | `services/air/src/cmf_activative_intelligence/repositories/air_repository.py` | `get_object`, `list_edges(outgoing=False)`, `store_object(expected_revision=...)` | REUSE (read-heavy) | `list_edges` is the load-bearing capability for the transfer-contract lookup; no repository change needed |
| `ContentBatchService.compile_batch` | `services/pipeline/src/cmf_pipeline/batch/service.py` | Requires five AIR-produced refs no HTTP surface exposed until this spec | **UNBLOCKED, NOT CALLED** | This spec makes the refs obtainable; it does not call `compile_batch()` itself — that is TS-APP-API-004's revisit per the Ledger's Resolution Sequence |
| `AirApplication` (from TS-APP-API-001) | `api/dependencies.py::get_air` | Already correctly constructed (`AirApplication(database_path)`, no missing-argument defect like TS-APP-API-002's Gap 2) | REUSE, UNCHANGED | Confirmed by reading `application.py` directly; no Stage 0 corrective patch needed in this spec, unlike TS-APP-API-002 |
| `api/schemas/interviews.py::RefModel` | (TS-APP-API-003 output) | `{object_id: str, version: str, sha256: str}` | REUSE, UNCHANGED | Imported by `api/schemas/air.py` |
| `services/pipeline/src/cmf_pipeline/domain/validation.py::require_ref` | Pipeline | Structurally identical allowed-field set to AIR's own `_ref` | **CONFIRMED COMPATIBLE — no adapter needed** | Contrast with GAP-002 (Builder↔Pipeline), which does need one; this spec found no equivalent AIR↔Pipeline ref-shape gap |

---

## 5. Proposed Architecture and Workflows

### Portfolio read flow — `GET /api/air/hypotheses/{portfolio_id}`

```
Router
  ├── air_app.repository.get_object(portfolio_id)
  │     └── ObjectNotFound → 404 PORTFOLIO_NOT_FOUND
  ├── if stored.object_type != "activation_hypothesis_portfolio" → 404 PORTFOLIO_NOT_FOUND
  │     (wrong object type is treated as "no portfolio with this id", not a 400 —
  │      the caller asked for a portfolio and none exists at that id)
  ├── for each ref in payload["candidate_refs"]:
  │     air_app.repository.get_object(ref["object_id"]) → HypothesisCandidateSummary fields
  ├── for each ref in payload["gate_result_refs"]:
  │     air_app.repository.get_object(ref["object_id"]) → attach to matching candidate by hypothesis_ref.object_id
  ├── for each ref in payload["comparative_evaluation_refs"]:
  │     air_app.repository.get_object(ref["object_id"]) → attach candidate_scores rows to matching candidates
  └── assemble HypothesisPortfolioDetail, 200
```

### Selection flow — `POST /api/air/hypotheses/{portfolio_id}/select`

```
Router → air_adapter.select_hypothesis(air_app, portfolio_id, request)
  1. portfolio = repository.get_object(portfolio_id); validate object_type; 404 if missing/wrong type
  2. if portfolio.payload["portfolio_state"] != "OPEN": 409 PORTFOLIO_NOT_OPEN
  3. candidate_ids = {ref["object_id"] for ref in portfolio.payload["candidate_refs"]}
     judged_ids = {j.hypothesis_id for j in request.candidate_judgments}
     if candidate_ids != judged_ids: 422 CANDIDATE_JUDGMENTS_INCOMPLETE
  4. if request.selected_hypothesis_id not in candidate_ids: 404 UNKNOWN_CANDIDATE
  5. for each judgment: hypotheses.gate_hypothesis(
        portfolio_ref=portfolio.immutable_ref(), hypothesis_ref=<candidate ref>,
        outcomes=judgment.gate_outcomes, producer_actor_id=judgment.producer_actor_id,
        evaluator_actor_id=request.evaluator_actor_id, gate_profile_ref=request.gate_profile_ref,
        evidence_refs=request.evidence_refs,
        idempotency_key=f"{request.idempotency_key}:gate:{judgment.hypothesis_id}")
     → collect gate_refs
  6. comparison = hypotheses.compare_portfolio(
        portfolio_ref=..., evaluation_profile_ref=request.evaluation_profile_ref,
        evaluator_actor_id=request.evaluator_actor_id,
        producer_actor_ids=[j.producer_actor_id for j in judgments],
        gate_receipt_refs=gate_refs,
        candidate_scores={j.hypothesis_id: j.dimension_scores_micros for j in judgments},
        decisive_margin_micros=request.decisive_margin_micros,
        idempotency_key=f"{request.idempotency_key}:comparison")
  7. if comparison.payload["decision"] != "DECISIVE_WINNER"
        or comparison.payload["selected_hypothesis_ref"]["object_id"] != request.selected_hypothesis_id:
        409 SELECTION_NOT_SUPPORTED_BY_SCORES (no further writes)
  8. stopping = hypotheses.stop_search(
        portfolio_ref=..., evaluation_ref=comparison_ref,
        remaining_budget=request.remaining_budget or portfolio.payload["search_budget"],
        diversity_exhausted=request.diversity_exhausted,
        idempotency_key=f"{request.idempotency_key}:stop")
        # decision was DECISIVE_WINNER, so stop_reason is guaranteed "DECISIVE_ELIGIBLE_WINNER"
  9. planned_pack = hypotheses.store_planned_pack(
        {pack_id: deterministic, portfolio_ref, selected_hypothesis_ref, matrix_of_edging_ref:
         request.matrix_of_edging_ref, role_tension_ref: request.role_tension_ref,
         source_refs: request.source_refs, ...}, idempotency_key=f"{...}:planned-pack")
 10. promotion = hypotheses.promote(
        {receipt_id: deterministic, portfolio_ref, selected_hypothesis_ref, stopping_receipt_ref,
         planned_pack_ref, authority_decision_ref: request.authority_decision_ref},
        idempotency_key=f"{...}:promotion")
 11. revision = repository.get_object(portfolio_id).revision   # re-read; Governing Decision, not hardcoded
     promoted = hypotheses.store_portfolio(
        {**portfolio.payload, supersedes_ref: portfolio.immutable_ref(),
         gate_result_refs: gate_refs, comparative_evaluation_refs: [comparison_ref],
         portfolio_state: "PROMOTED", stopping_receipt_ref, selected_hypothesis_ref,
         promotion_ref, candidate_state_records: <updated>},
        idempotency_key=f"{...}:portfolio-promoted", expected_revision=revision)
        # ObjectVersionConflict → 409 CONFLICT
 12. 200 HypothesisSelectionResponse
```

### Script read flow — `GET /api/air/scripts/{script_id}`

```
Router
  ├── air_app.repository.get_object(script_id)
  │     └── ObjectNotFound / wrong object_type → 404 SCRIPT_NOT_FOUND
  ├── batch_compilation_refs = air_adapter.resolve_batch_refs(air_app, stored)
  │     ├── if not payload["operator_approved"]: None, reason="SCRIPT_NOT_APPROVED"
  │     └── else:
  │           edges = repository.list_edges(script_id, outgoing=False)
  │           candidates = [e for e in edges if e["relation_type"] == "governs_transfer_of"]
  │           contracts = [repository.get_object(e["source_object_id"]) for e in candidates]
  │           contracts = [c for c in contracts if c.object_type == "activation_transfer_contract"
  │                        and c.payload["final_script_ref"] == stored.immutable_ref()]
  │           if not contracts: None, reason="NO_TRANSFER_CONTRACT_YET"
  │           else: pick max(contracts, key=created_at_utc) →
  │                 {final_script_ref: stored.immutable_ref(),
  │                  semantic_program_ref: payload["program_ref"],       # field-name projection, Source gap notice D
  │                  archetype_coalition_ref: payload["archetype_coalition_ref"],
  │                  primitive_coalition_ref: payload["primitive_coalition_ref"],
  │                  activation_transfer_contract_ref: contract.immutable_ref()}
  └── assemble FinalScriptDetail, 200
```

### Approval flow — `POST /api/air/scripts/{script_id}/approve`

```
Router
  ├── script = repository.get_object(script_id); 404 if missing/wrong type
  ├── if script.payload["operator_approved"] is True: 409 ALREADY_APPROVED
  │     (idempotent replay with the *same* idempotency_key is still safe — AirRepository's
  │      own idempotency-key dedupe at the store_object layer handles that transparently;
  │      this check only rejects a *second, distinct* approval attempt)
  ├── evaluation_refs = request.evaluation_refs or script.payload["evaluation_receipt_refs"]
  ├── air_app.derivatives.approve_script(
  │       candidate_script_ref=script.immutable_ref(), operator_id=request.operator_id,
  │       operator_decision_ref=request.operator_decision_ref, evaluation_refs=evaluation_refs,
  │       rationale=request.rationale,
  │       approval_idempotency_key=f"{request.idempotency_key}:approval",
  │       script_revision_idempotency_key=f"{request.idempotency_key}:script-revision")
  └── 200 ScriptApprovalResponse — script.batch_compilation_refs is still null here
        (reason="NO_TRANSFER_CONTRACT_YET") — approval alone does not create a contract
```

### Transfer contract flow — `POST /api/air/scripts/{script_id}/transfer-contract`

```
Router
  ├── script = repository.get_object(script_id); 404 if missing/wrong type
  ├── if not script.payload["operator_approved"]: 409 SCRIPT_NOT_APPROVED   (Governing Decision)
  ├── air_app.transfer.store_contract({
  │       contract_id: deterministic, version, authority: request.authority,
  │       source_expression_refs: request.source_expression_refs,
  │       source_package_refs: request.source_package_refs,
  │       expression_moment_refs: request.expression_moment_refs,
  │       reaction_receipt_refs: request.reaction_receipt_refs,
  │       selected_hypothesis_ref: request.selected_hypothesis_ref,
  │       role_tension_ref: script.payload["role_tension_ref"],            # defaulted from script
  │       primitive_coalition_ref: script.payload["primitive_coalition_ref"],
  │       archetype_coalition_ref: script.payload["archetype_coalition_ref"],
  │       final_script_ref: script.immutable_ref(),
  │       must_survive_properties: request.must_survive_properties,
  │       transformation_rules: request.transformation_rules,
  │       required_changes: request.required_changes,
  │       wrong_reading_lock_refs: script.payload["wrong_reading_lock_refs"], # defaulted from script
  │       evaluation_profile_ref: request.evaluation_profile_ref,
  │       limitations: request.limitations,
  │     }, idempotency_key=request.idempotency_key)
  └── 200 TransferContractResponse — GET /api/air/scripts/{script_id} now returns
        batch_compilation_refs populated (edge is written by store_contract itself)
```

### Error contract addendum
Every non-2xx response body follows `api/errors.py::ErrorResponse` (TS-APP-API-001), unchanged: `{error_code, message, service: null, timestamp}`.

---

## 6. Data Models, Contracts, Schemas, and APIs

### `api/schemas/air.py`

```python
from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field

from api.schemas.interviews import RefModel  # {object_id, version, sha256}, reused unchanged


class AirAuthorityRefModel(BaseModel):
    """Deliberately not imported from api/schemas/campaigns.py — see Governing
    Decisions §3 (wave-ordering)."""
    authority_id: str
    authority_version: str
    authority_sha256: str
    authority_state: Literal["current", "candidate_not_current"]


HypothesisGateName = Literal[
    "SOURCE_FIDELITY", "EPISTEMIC_LEGALITY", "IDENTITY_FIT", "DOMAIN_FIT",
    "OPERATOR_CONSTRAINTS", "FATAL_PRIMITIVE_CONFLICT", "WRONG_READING_LOCKS",
    "LINEAGE_COMPLETE", "CURRENT_VERSION", "SEMANTIC_DUPLICATE",
]
EvaluationDimension = Literal[
    "source_fidelity", "role_tension_integrity", "primitive_coalition_fitness",
    "archetype_fit", "edge_integrity", "anti_centroid_distinctiveness",
    "execution_feasibility",
]
PortfolioState = Literal["OPEN", "GATED", "COMPARED", "STOPPED", "PROMOTED", "CANCELLED", "SUPERSEDED"]
CandidateState = Literal["PROPOSED", "GATE_REJECTED", "ELIGIBLE", "REPAIRED", "SUPERSEDED", "SELECTED", "PROMOTED"]


class SearchBudgetModel(BaseModel):
    maximum_candidate_count: int
    maximum_round_count: int
    maximum_model_tokens: int
    maximum_provider_cost_micros: int
    consumed_candidate_count: int
    consumed_round_count: int
    consumed_model_tokens: int
    consumed_provider_cost_micros: int


class DiversitySignatureModel(BaseModel):
    axes: dict[str, str]
    proof_sha256: str


# ---- GET /api/air/hypotheses/{portfolio_id} ----

class GateCheckModel(BaseModel):
    gate: HypothesisGateName
    applicability: Literal["APPLIES", "NOT_APPLICABLE"]
    verdict: Literal["PASS", "FAIL"]
    reason: str


class CandidateGateResultModel(BaseModel):
    receipt_ref: RefModel
    overall: Literal["ELIGIBLE", "INELIGIBLE"]
    checks: list[GateCheckModel]


class CandidateScoreModel(BaseModel):
    dimension_scores_micros: dict[str, int]
    total_micros: int
    eligible: bool


class HypothesisCandidateSummary(BaseModel):
    hypothesis_ref: RefModel
    psychological_role: str
    tension: str
    activation_directions: list[str]
    pressure_path: str
    stance: str
    stakes: list[str]
    pressure_dose: int
    participation_design: str
    smallest_useful_commitment: str
    diversity_signature: DiversitySignatureModel
    state: CandidateState
    gate_result: CandidateGateResultModel | None
    comparative_score: CandidateScoreModel | None


class HypothesisPortfolioDetail(BaseModel):
    portfolio_ref: RefModel
    portfolio_state: PortfolioState
    search_policy_ref: RefModel
    search_budget: SearchBudgetModel
    upstream_snapshot_refs: list[RefModel]
    candidates: list[HypothesisCandidateSummary]
    gate_result_refs: list[RefModel]
    comparative_evaluation_refs: list[RefModel]
    stopping_receipt_ref: RefModel | None
    selected_hypothesis_ref: RefModel | None
    promotion_ref: RefModel | None


# ---- POST /api/air/hypotheses/{portfolio_id}/select ----

class CandidateJudgment(BaseModel):
    hypothesis_id: str
    producer_actor_id: str
    gate_outcomes: dict[HypothesisGateName, bool]
    dimension_scores_micros: dict[EvaluationDimension, int] = Field(
        description="Each value must be an integer in [0, 1_000_000] (micros)."
    )


class HypothesisSelectionRequest(BaseModel):
    idempotency_key: str
    authority: AirAuthorityRefModel
    selected_hypothesis_id: str
    evaluator_actor_id: str
    candidate_judgments: list[CandidateJudgment]
    gate_profile_ref: RefModel
    evaluation_profile_ref: RefModel
    evidence_refs: list[RefModel]
    matrix_of_edging_ref: RefModel
    role_tension_ref: RefModel
    source_refs: list[RefModel]
    authority_decision_ref: RefModel
    decisive_margin_micros: int = 100_000
    diversity_exhausted: bool = False
    remaining_budget: SearchBudgetModel | None = None


class HypothesisSelectionResponse(BaseModel):
    portfolio: HypothesisPortfolioDetail
    decision: Literal["DECISIVE_WINNER"]
    stop_reason: Literal["DECISIVE_ELIGIBLE_WINNER"]
    selected_hypothesis_ref: RefModel
    comparison_ref: RefModel
    stopping_receipt_ref: RefModel
    planned_pack_ref: RefModel
    promotion_ref: RefModel


# ---- GET /api/air/scripts/{script_id} ----

class ScriptSegmentModel(BaseModel):
    order: int
    segment_id: str
    transformation_class: Literal["VERBATIM", "CONDENSATION", "REWRITE", "REORDER", "VISUAL_TRANSLATION", "AUDIO_REUSE", "ANIMATION_TRANSLATION"]
    source_text: str | None
    final_text: str
    transformation_operations: list[str]
    source_span_refs: list[RefModel]
    voice_dna_applied: bool | None


class BatchCompilationRefs(BaseModel):
    """Exactly the field names services/pipeline/src/cmf_pipeline/batch/service.py
    ::_compile_job reads off each `routes[]` entry — ready to paste in unchanged.
    Route-authoring fields (route_id, derivative_type, source_spans, priority,
    animation_scene_package_ref, not_applicable_reason) are NOT AIR's concern
    and are not included here — see Section 2, Out of scope."""
    final_script_ref: RefModel
    semantic_program_ref: RefModel
    archetype_coalition_ref: RefModel
    primitive_coalition_ref: RefModel
    activation_transfer_contract_ref: RefModel


class BatchCompilationRefsUnavailable(BaseModel):
    reason: Literal["SCRIPT_NOT_APPROVED", "NO_TRANSFER_CONTRACT_YET"]


class FinalScriptDetail(BaseModel):
    script_ref: RefModel
    lifecycle_state: str
    epistemic_state: str
    operator_approved: bool
    composition_eligible: bool
    program_ref: RefModel
    proposal_ref: RefModel
    segments: list[ScriptSegmentModel]
    script_sha256: str
    evaluation_receipt_refs: list[RefModel]
    source_lineage_refs: list[RefModel]
    role_tension_ref: RefModel
    primitive_coalition_ref: RefModel
    archetype_coalition_ref: RefModel
    brand_context_ref: RefModel
    voice_dna_ref: RefModel
    distillation_receipt_refs: list[RefModel]
    ccv_axes: dict[str, str]
    wrong_reading_lock_refs: list[RefModel]
    maximum_claim: str
    approval_receipt_ref: RefModel | None
    limitations: list[str]
    batch_compilation_refs: BatchCompilationRefs | BatchCompilationRefsUnavailable


# ---- POST /api/air/scripts/{script_id}/approve ----

class ScriptApprovalRequest(BaseModel):
    idempotency_key: str
    operator_id: str
    operator_decision_ref: RefModel
    rationale: str
    evaluation_refs: list[RefModel] | None = Field(
        default=None,
        description="Defaults to the candidate script's own evaluation_receipt_refs if omitted."
    )


class ScriptApprovalResponse(BaseModel):
    approval_ref: RefModel
    decision: Literal["APPROVE"]
    script: FinalScriptDetail


# ---- POST /api/air/scripts/{script_id}/transfer-contract ----

class MustSurvivePropertyModel(BaseModel):
    property_id: str
    property_kind: Literal["SOURCE_MEANING", "ROLE_TENSION", "EDGE_PRODUCT", "VOICE", "VISUAL", "WRONG_READING_LOCK", "IDENTITY_CONTINUITY", "SEQUENCE_FUNCTION"]
    statement: str
    evidence_refs: list[RefModel]
    hard_gate: bool


class TransformationRuleModel(BaseModel):
    operation_class: Literal["VERBATIM", "CONDENSATION", "REWRITE", "REORDER", "VISUAL_TRANSLATION", "AUDIO_REUSE", "ANIMATION_TRANSLATION"]
    allowed: bool
    constraints: list[str]


class RequiredChangeModel(BaseModel):
    change_id: str
    reason: str
    target_property_ids: list[str]
    required_operations: list[str]


class TransferContractRequest(BaseModel):
    idempotency_key: str
    authority: AirAuthorityRefModel
    source_expression_refs: list[RefModel]
    source_package_refs: list[RefModel]
    expression_moment_refs: list[RefModel]
    reaction_receipt_refs: list[RefModel]
    selected_hypothesis_ref: RefModel
    must_survive_properties: list[MustSurvivePropertyModel]
    transformation_rules: list[TransformationRuleModel]
    required_changes: list[RequiredChangeModel]
    evaluation_profile_ref: RefModel
    limitations: list[str]


class TransferContractResponse(BaseModel):
    contract_ref: RefModel
    final_script_ref: RefModel
```

### Endpoints defined in this spec

| Method | Path | Request | Response | Error codes |
|---|---|---|---|---|
| `GET` | `/api/air/hypotheses/{portfolio_id}` | — | `HypothesisPortfolioDetail` (200) | `PORTFOLIO_NOT_FOUND` |
| `POST` | `/api/air/hypotheses/{portfolio_id}/select` | `HypothesisSelectionRequest` | `HypothesisSelectionResponse` (200) | `PORTFOLIO_NOT_FOUND`, `PORTFOLIO_NOT_OPEN`, `CANDIDATE_JUDGMENTS_INCOMPLETE`, `UNKNOWN_CANDIDATE`, `SELECTION_NOT_SUPPORTED_BY_SCORES`, `CONFLICT`, `VALIDATION_ERROR` |
| `GET` | `/api/air/scripts/{script_id}` | — | `FinalScriptDetail` (200) | `SCRIPT_NOT_FOUND` |
| `POST` | `/api/air/scripts/{script_id}/approve` | `ScriptApprovalRequest` | `ScriptApprovalResponse` (200) | `SCRIPT_NOT_FOUND`, `ALREADY_APPROVED`, `VALIDATION_ERROR` |
| `POST` | `/api/air/scripts/{script_id}/transfer-contract` | `TransferContractRequest` | `TransferContractResponse` (200) | `SCRIPT_NOT_FOUND`, `SCRIPT_NOT_APPROVED`, `VALIDATION_ERROR` |

Positive example — `GET /api/air/scripts/{script_id}` for an approved script with a transfer contract already recorded:
```json
{
  "script_ref": { "object_id": "demo:final-script", "version": "2.0.0", "sha256": "7c1a..." },
  "lifecycle_state": "approved",
  "epistemic_state": "operator_confirmed",
  "operator_approved": true,
  "composition_eligible": true,
  "program_ref": { "object_id": "demo:derivative-program:source-short", "version": "1.0.0", "sha256": "9b2e..." },
  "...": "... (segments, refs, etc. omitted for brevity)",
  "batch_compilation_refs": {
    "final_script_ref": { "object_id": "demo:final-script", "version": "2.0.0", "sha256": "7c1a..." },
    "semantic_program_ref": { "object_id": "demo:derivative-program:source-short", "version": "1.0.0", "sha256": "9b2e..." },
    "archetype_coalition_ref": { "object_id": "demo:archetype-coalition", "version": "1.0.0", "sha256": "4f0d..." },
    "primitive_coalition_ref": { "object_id": "demo:primitive-coalition", "version": "1.0.0", "sha256": "e81a..." },
    "activation_transfer_contract_ref": { "object_id": "demo:transfer-contract", "version": "1.0.0", "sha256": "c30b..." }
  }
}
```

Positive example — the same script before a transfer contract exists (post-approval, pre-`/transfer-contract`):
```json
{
  "operator_approved": true,
  "composition_eligible": true,
  "batch_compilation_refs": { "reason": "NO_TRANSFER_CONTRACT_YET" }
}
```

Negative example — `POST /api/air/hypotheses/{portfolio_id}/select` where the caller's scores don't decisively support their own pick:
```json
{
  "error_code": "SELECTION_NOT_SUPPORTED_BY_SCORES",
  "message": "comparison decided AMBIGUOUS, not a decisive win for 'demo:hypothesis:2'; no writes were made past compare_portfolio",
  "service": null,
  "timestamp": "2026-07-26T10:00:00Z"
}
```

Negative example — `POST /api/air/scripts/{script_id}/transfer-contract` before approval:
```json
{
  "error_code": "SCRIPT_NOT_APPROVED",
  "message": "final_script_package 'demo:final-script' has operator_approved=false; a transfer contract cannot be created until FR-APP-032 approval is recorded",
  "service": null,
  "timestamp": "2026-07-26T10:00:00Z"
}
```

---

## 7. Implementation Stages and Exact Target Paths

All paths are relative to the repository root after the directory restructure described in `CA_APP_FR_EPIC_SPEC_PLAN.md` (`services/air/...`, not `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/...`).

### Stage 1 — AIR adapter module (orchestration, no FastAPI)

**`api/services/air_adapter.py`**
```python
from __future__ import annotations

from typing import Any, Mapping

from cmf_activative_intelligence.application import AirApplication
from cmf_activative_intelligence.repositories.air_repository import ObjectNotFound, ObjectVersionConflict, StoredAirObject


class PortfolioNotFound(Exception):
    pass


class ScriptNotFound(Exception):
    pass


class PortfolioNotOpen(Exception):
    pass


class CandidateJudgmentsIncomplete(Exception):
    def __init__(self, missing: set[str], extra: set[str]):
        self.missing, self.extra = missing, extra
        super().__init__(f"missing={sorted(missing)} extra={sorted(extra)}")


class UnknownCandidate(Exception):
    pass


class SelectionNotSupportedByScores(Exception):
    def __init__(self, decision: str, actual_selected: Mapping[str, Any] | None):
        self.decision, self.actual_selected = decision, actual_selected
        super().__init__(f"decision={decision} actual_selected={actual_selected}")


class ScriptAlreadyApproved(Exception):
    pass


class ScriptNotApproved(Exception):
    pass


def _get_typed(air: AirApplication, object_id: str, expected_type: str, not_found_exc: type[Exception]) -> StoredAirObject:
    try:
        stored = air.repository.get_object(object_id)
    except ObjectNotFound as exc:
        raise not_found_exc(object_id) from exc
    if stored.object_type != expected_type:
        raise not_found_exc(object_id)
    return stored


def get_portfolio(air: AirApplication, portfolio_id: str) -> StoredAirObject:
    return _get_typed(air, portfolio_id, "activation_hypothesis_portfolio", PortfolioNotFound)


def get_script(air: AirApplication, script_id: str) -> StoredAirObject:
    return _get_typed(air, script_id, "final_script_package", ScriptNotFound)


def resolve_batch_refs(air: AirApplication, script: StoredAirObject) -> dict[str, Any]:
    """Returns either a full BatchCompilationRefs dict or {"reason": ...}."""
    if not script.payload["operator_approved"]:
        return {"reason": "SCRIPT_NOT_APPROVED"}
    script_ref = script.immutable_ref()
    edges = air.repository.list_edges(script.object_id, outgoing=False)
    contracts: list[StoredAirObject] = []
    for edge in edges:
        if edge["relation_type"] != "governs_transfer_of":
            continue
        try:
            source = air.repository.get_object(edge["source_object_id"])
        except ObjectNotFound:
            continue
        if source.object_type != "activation_transfer_contract":
            continue
        if dict(source.payload["final_script_ref"]) != script_ref:
            continue  # governs a different revision of this same object_id
        contracts.append(source)
    if not contracts:
        return {"reason": "NO_TRANSFER_CONTRACT_YET"}
    chosen = max(contracts, key=lambda c: c.created_at_utc)
    return {
        "final_script_ref": script_ref,
        "semantic_program_ref": dict(script.payload["program_ref"]),  # AIR name -> Pipeline name projection
        "archetype_coalition_ref": dict(script.payload["archetype_coalition_ref"]),
        "primitive_coalition_ref": dict(script.payload["primitive_coalition_ref"]),
        "activation_transfer_contract_ref": chosen.immutable_ref(),
    }


def select_hypothesis(air: AirApplication, portfolio_id: str, request: Mapping[str, Any]) -> dict[str, Any]:
    portfolio = get_portfolio(air, portfolio_id)
    if portfolio.payload["portfolio_state"] != "OPEN":
        raise PortfolioNotOpen(portfolio.payload["portfolio_state"])

    candidate_refs = list(portfolio.payload["candidate_refs"])
    candidate_ids = {ref["object_id"] for ref in candidate_refs}
    judgments = {j["hypothesis_id"]: j for j in request["candidate_judgments"]}
    judged_ids = set(judgments)
    if candidate_ids != judged_ids:
        raise CandidateJudgmentsIncomplete(candidate_ids - judged_ids, judged_ids - candidate_ids)
    if request["selected_hypothesis_id"] not in candidate_ids:
        raise UnknownCandidate(request["selected_hypothesis_id"])

    idem = request["idempotency_key"]
    authority = dict(request["authority"])
    portfolio_ref = portfolio.immutable_ref()

    gate_refs: list[dict[str, str]] = []
    for ref in candidate_refs:
        judgment = judgments[ref["object_id"]]
        gate = air.hypotheses.gate_hypothesis(
            receipt_id=f"{portfolio_id}:gate:{ref['object_id']}",
            version="1.0.0",
            authority=authority,
            portfolio_ref=portfolio_ref,
            hypothesis_ref=ref,
            gate_profile_ref=request["gate_profile_ref"],
            evaluator_actor_id=request["evaluator_actor_id"],
            producer_actor_id=judgment["producer_actor_id"],
            outcomes=judgment["gate_outcomes"],
            evidence_refs=request["evidence_refs"],
            idempotency_key=f"{idem}:gate:{ref['object_id']}",
        )["object"]
        gate_refs.append({"object_id": gate["object_id"], "version": gate["semantic_version"], "sha256": gate["canonical_sha256"]})

    comparison = air.hypotheses.compare_portfolio(
        receipt_id=f"{portfolio_id}:comparison",
        version="1.0.0",
        authority=authority,
        portfolio_ref=portfolio_ref,
        evaluation_profile_ref=request["evaluation_profile_ref"],
        evaluator_actor_id=request["evaluator_actor_id"],
        producer_actor_ids=[judgments[ref["object_id"]]["producer_actor_id"] for ref in candidate_refs],
        gate_receipt_refs=gate_refs,
        candidate_scores={rid: dict(j["dimension_scores_micros"]) for rid, j in judgments.items()},
        decisive_margin_micros=request["decisive_margin_micros"],
        idempotency_key=f"{idem}:comparison",
    )["object"]
    comparison_ref = {"object_id": comparison["object_id"], "version": comparison["semantic_version"], "sha256": comparison["canonical_sha256"]}

    decision = comparison["payload"]["decision"]
    actual_selected = comparison["payload"].get("selected_hypothesis_ref")
    if decision != "DECISIVE_WINNER" or (actual_selected or {}).get("object_id") != request["selected_hypothesis_id"]:
        raise SelectionNotSupportedByScores(decision, actual_selected)

    selected_ref = dict(actual_selected)

    stopping = air.hypotheses.stop_search(
        receipt_id=f"{portfolio_id}:stop",
        version="1.0.0",
        authority=authority,
        portfolio_ref=portfolio_ref,
        evaluation_ref=comparison_ref,
        remaining_budget=request.get("remaining_budget") or dict(portfolio.payload["search_budget"]),
        diversity_exhausted=request["diversity_exhausted"],
        idempotency_key=f"{idem}:stop",
    )["object"]
    stopping_ref = {"object_id": stopping["object_id"], "version": stopping["semantic_version"], "sha256": stopping["canonical_sha256"]}

    planned_pack = air.hypotheses.store_planned_pack(
        {
            "pack_id": f"{portfolio_id}:planned-pack",
            "version": "1.0.0",
            "authority": authority,
            "lifecycle_state": "approved",
            "epistemic_state": "planned",
            "portfolio_ref": portfolio_ref,
            "selected_hypothesis_ref": selected_ref,
            "matrix_of_edging_ref": request["matrix_of_edging_ref"],
            "role_tension_ref": request["role_tension_ref"],
            "source_refs": request["source_refs"],
            "limitations": ["development evidence; no real-human activation claim"],
        },
        idempotency_key=f"{idem}:planned-pack",
    )["object"]
    planned_pack_ref = {"object_id": planned_pack["object_id"], "version": planned_pack["semantic_version"], "sha256": planned_pack["canonical_sha256"]}

    promotion = air.hypotheses.promote(
        {
            "receipt_id": f"{portfolio_id}:promotion",
            "version": "1.0.0",
            "authority": authority,
            "portfolio_ref": portfolio_ref,
            "selected_hypothesis_ref": selected_ref,
            "stopping_receipt_ref": stopping_ref,
            "planned_pack_ref": planned_pack_ref,
            "authority_decision_ref": request["authority_decision_ref"],
        },
        idempotency_key=f"{idem}:promotion",
    )["object"]
    promotion_ref = {"object_id": promotion["object_id"], "version": promotion["semantic_version"], "sha256": promotion["canonical_sha256"]}

    current_revision = air.repository.get_object(portfolio_id).revision  # re-read; Governing Decision §3
    try:
        promoted = air.hypotheses.store_portfolio(
            {
                **portfolio.payload,
                "supersedes_ref": portfolio_ref,
                "gate_result_refs": gate_refs,
                "comparative_evaluation_refs": [comparison_ref],
                "portfolio_state": "PROMOTED",
                "stopping_receipt_ref": stopping_ref,
                "selected_hypothesis_ref": selected_ref,
                "promotion_ref": promotion_ref,
                "candidate_state_records": [
                    {
                        "candidate_ref": ref,
                        "state": "PROMOTED" if ref["object_id"] == selected_ref["object_id"] else "ELIGIBLE",
                        "reason_codes": ["SELECTED_BY_DECISIVE_COMPARISON"] if ref["object_id"] == selected_ref["object_id"] else ["NOT_SELECTED"],
                        "caused_by_receipt_ref": promotion_ref if ref["object_id"] == selected_ref["object_id"] else comparison_ref,
                    }
                    for ref in candidate_refs
                ],
            },
            idempotency_key=f"{idem}:portfolio-promoted",
            expected_revision=current_revision,
        )["object"]
    except ObjectVersionConflict as exc:
        raise  # surfaced as 409 CONFLICT by the router

    return {
        "portfolio": promoted,
        "decision": decision,
        "stop_reason": stopping["payload"]["stop_reason"],
        "selected_hypothesis_ref": selected_ref,
        "comparison_ref": comparison_ref,
        "stopping_receipt_ref": stopping_ref,
        "planned_pack_ref": planned_pack_ref,
        "promotion_ref": promotion_ref,
    }


def approve_script(air: AirApplication, script_id: str, request: Mapping[str, Any]) -> dict[str, Any]:
    script = get_script(air, script_id)
    if script.payload["operator_approved"] is True:
        raise ScriptAlreadyApproved(script_id)
    evaluation_refs = request.get("evaluation_refs") or list(script.payload["evaluation_receipt_refs"])
    idem = request["idempotency_key"]
    result = air.derivatives.approve_script(
        candidate_script_ref=script.immutable_ref(),
        operator_id=request["operator_id"],
        operator_decision_ref=request["operator_decision_ref"],
        evaluation_refs=evaluation_refs,
        rationale=request["rationale"],
        approval_idempotency_key=f"{idem}:approval",
        script_revision_idempotency_key=f"{idem}:script-revision",
    )
    approved_script = air.repository.get_object(script_id)  # re-read current (now-approved) revision
    return {"approval": result["approval"]["object"], "script": approved_script}


def create_transfer_contract(air: AirApplication, script_id: str, request: Mapping[str, Any]) -> dict[str, Any]:
    script = get_script(air, script_id)
    if not script.payload["operator_approved"]:
        raise ScriptNotApproved(script_id)
    result = air.transfer.store_contract(
        {
            "contract_id": f"{script_id}:transfer-contract",
            "version": "1.0.0",
            "authority": dict(request["authority"]),
            "source_expression_refs": request["source_expression_refs"],
            "source_package_refs": request["source_package_refs"],
            "expression_moment_refs": request["expression_moment_refs"],
            "reaction_receipt_refs": request["reaction_receipt_refs"],
            "selected_hypothesis_ref": request["selected_hypothesis_ref"],
            "role_tension_ref": dict(script.payload["role_tension_ref"]),
            "primitive_coalition_ref": dict(script.payload["primitive_coalition_ref"]),
            "archetype_coalition_ref": dict(script.payload["archetype_coalition_ref"]),
            "final_script_ref": script.immutable_ref(),
            "must_survive_properties": request["must_survive_properties"],
            "transformation_rules": request["transformation_rules"],
            "required_changes": request["required_changes"],
            "wrong_reading_lock_refs": list(script.payload["wrong_reading_lock_refs"]),
            "evaluation_profile_ref": request["evaluation_profile_ref"],
            "limitations": request["limitations"],
        },
        idempotency_key=request["idempotency_key"],
    )
    return result["object"]
```

### Stage 2 — Projection helpers (StoredAirObject → response dict)

**`api/services/air_projection.py`**
```python
from __future__ import annotations
from typing import Any
from cmf_activative_intelligence.application import AirApplication
from cmf_activative_intelligence.repositories.air_repository import ObjectNotFound, StoredAirObject
from .air_adapter import resolve_batch_refs


def _ref(obj: dict[str, Any]) -> dict[str, str]:
    return {"object_id": obj["object_id"], "version": obj["semantic_version"], "sha256": obj["canonical_sha256"]}


def project_candidate_summary(air: AirApplication, ref: dict[str, str], portfolio_payload: dict[str, Any]) -> dict[str, Any]:
    hypothesis = air.repository.get_object(ref["object_id"])
    p = hypothesis.payload
    state = next(
        (r["state"] for r in portfolio_payload["candidate_state_records"] if r["candidate_ref"]["object_id"] == ref["object_id"]),
        "PROPOSED",
    )
    gate_result = None
    for gref in portfolio_payload.get("gate_result_refs", []):
        gate = air.repository.get_object(gref["object_id"])
        if gate.payload["hypothesis_ref"]["object_id"] == ref["object_id"]:
            gate_result = {
                "receipt_ref": gref,
                "overall": gate.payload["overall"],
                "checks": [{"gate": c["gate"], "applicability": c["applicability"], "verdict": c["verdict"], "reason": c["reason"]} for c in gate.payload["checks"]],
            }
            break
    comparative_score = None
    for cref in portfolio_payload.get("comparative_evaluation_refs", []):
        comparison = air.repository.get_object(cref["object_id"])
        for row in comparison.payload["candidate_scores"]:
            if row["hypothesis_ref"]["object_id"] == ref["object_id"]:
                comparative_score = {"dimension_scores_micros": row["dimension_scores_micros"], "total_micros": row["total_micros"], "eligible": row["eligible"]}
                break
    return {
        "hypothesis_ref": ref,
        "psychological_role": p["psychological_role"],
        "tension": p["tension"],
        "activation_directions": p["activation_directions"],
        "pressure_path": p["pressure_path"],
        "stance": p["stance"],
        "stakes": p["stakes"],
        "pressure_dose": p["pressure_dose"],
        "participation_design": p["participation_design"],
        "smallest_useful_commitment": p["smallest_useful_commitment"],
        "diversity_signature": p["diversity_signature"],
        "state": state,
        "gate_result": gate_result,
        "comparative_score": comparative_score,
    }


def project_portfolio_detail(air: AirApplication, portfolio: StoredAirObject) -> dict[str, Any]:
    p = portfolio.payload
    return {
        "portfolio_ref": portfolio.immutable_ref(),
        "portfolio_state": p["portfolio_state"],
        "search_policy_ref": p["search_policy_ref"],
        "search_budget": p["search_budget"],
        "upstream_snapshot_refs": p["upstream_snapshot_refs"],
        "candidates": [project_candidate_summary(air, ref, p) for ref in p["candidate_refs"]],
        "gate_result_refs": p["gate_result_refs"],
        "comparative_evaluation_refs": p["comparative_evaluation_refs"],
        "stopping_receipt_ref": p.get("stopping_receipt_ref"),
        "selected_hypothesis_ref": p.get("selected_hypothesis_ref"),
        "promotion_ref": p.get("promotion_ref"),
    }


def project_script_detail(air: AirApplication, script: StoredAirObject) -> dict[str, Any]:
    p = script.payload
    return {
        "script_ref": script.immutable_ref(),
        "lifecycle_state": script.lifecycle_state,
        "epistemic_state": script.epistemic_state,
        "operator_approved": p["operator_approved"],
        "composition_eligible": p["composition_eligible"],
        "program_ref": p["program_ref"],
        "proposal_ref": p["proposal_ref"],
        "segments": p["segments"],
        "script_sha256": p["script_sha256"],
        "evaluation_receipt_refs": p["evaluation_receipt_refs"],
        "source_lineage_refs": p["source_lineage_refs"],
        "role_tension_ref": p["role_tension_ref"],
        "primitive_coalition_ref": p["primitive_coalition_ref"],
        "archetype_coalition_ref": p["archetype_coalition_ref"],
        "brand_context_ref": p["brand_context_ref"],
        "voice_dna_ref": p["voice_dna_ref"],
        "distillation_receipt_refs": p["distillation_receipt_refs"],
        "ccv_axes": p["ccv_axes"],
        "wrong_reading_lock_refs": p["wrong_reading_lock_refs"],
        "maximum_claim": p["maximum_claim"],
        "approval_receipt_ref": p.get("approval_receipt_ref"),
        "limitations": p["limitations"],
        "batch_compilation_refs": resolve_batch_refs(air, script),
    }
```

### Stage 3 — Router

**`api/routers/air.py`**
```python
from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from ca_contracts import utc_now_rfc3339

from api.dependencies import get_air
from api.errors import ErrorResponse
from api.schemas import air as schemas
from api.services import air_adapter, air_projection
from cmf_activative_intelligence.domain import AirValidationError
from cmf_activative_intelligence.repositories.air_repository import ObjectVersionConflict

router = APIRouter()


def _error(code: str, message: str, status: int) -> HTTPException:
    return HTTPException(status_code=status, detail=ErrorResponse(error_code=code, message=message, timestamp=utc_now_rfc3339()).model_dump())


@router.get("/hypotheses/{portfolio_id}", response_model=schemas.HypothesisPortfolioDetail)
def get_hypothesis_portfolio(portfolio_id: str, air=Depends(get_air)):
    try:
        portfolio = air_adapter.get_portfolio(air, portfolio_id)
    except air_adapter.PortfolioNotFound:
        raise _error("PORTFOLIO_NOT_FOUND", f"no activation_hypothesis_portfolio with id '{portfolio_id}'", 404)
    return air_projection.project_portfolio_detail(air, portfolio)


@router.post("/hypotheses/{portfolio_id}/select", response_model=schemas.HypothesisSelectionResponse)
def select_hypothesis(portfolio_id: str, body: schemas.HypothesisSelectionRequest, air=Depends(get_air)):
    try:
        result = air_adapter.select_hypothesis(air, portfolio_id, body.model_dump())
    except air_adapter.PortfolioNotFound:
        raise _error("PORTFOLIO_NOT_FOUND", f"no activation_hypothesis_portfolio with id '{portfolio_id}'", 404)
    except air_adapter.PortfolioNotOpen as exc:
        raise _error("PORTFOLIO_NOT_OPEN", f"portfolio_state is '{exc}', expected 'OPEN'", 409)
    except air_adapter.CandidateJudgmentsIncomplete as exc:
        raise _error("CANDIDATE_JUDGMENTS_INCOMPLETE", f"missing={sorted(exc.missing)} extra={sorted(exc.extra)}", 422)
    except air_adapter.UnknownCandidate as exc:
        raise _error("UNKNOWN_CANDIDATE", f"'{exc}' is not a candidate in this portfolio", 404)
    except air_adapter.SelectionNotSupportedByScores as exc:
        raise _error("SELECTION_NOT_SUPPORTED_BY_SCORES", f"comparison decided {exc.decision}, not a decisive win for '{body.selected_hypothesis_id}'; no writes were made past compare_portfolio", 409)
    except ObjectVersionConflict:
        raise _error("CONFLICT", "portfolio was modified concurrently; re-fetch and retry", 409)
    except AirValidationError as exc:
        raise _error("VALIDATION_ERROR", str(exc), 422)
    return {
        "portfolio": air_projection.project_portfolio_detail(air, air_adapter.get_portfolio(air, portfolio_id)),
        "decision": result["decision"],
        "stop_reason": result["stop_reason"],
        "selected_hypothesis_ref": result["selected_hypothesis_ref"],
        "comparison_ref": result["comparison_ref"],
        "stopping_receipt_ref": result["stopping_receipt_ref"],
        "planned_pack_ref": result["planned_pack_ref"],
        "promotion_ref": result["promotion_ref"],
    }


@router.get("/scripts/{script_id}", response_model=schemas.FinalScriptDetail)
def get_script(script_id: str, air=Depends(get_air)):
    try:
        script = air_adapter.get_script(air, script_id)
    except air_adapter.ScriptNotFound:
        raise _error("SCRIPT_NOT_FOUND", f"no final_script_package with id '{script_id}'", 404)
    return air_projection.project_script_detail(air, script)


@router.post("/scripts/{script_id}/approve", response_model=schemas.ScriptApprovalResponse)
def approve_script(script_id: str, body: schemas.ScriptApprovalRequest, air=Depends(get_air)):
    try:
        result = air_adapter.approve_script(air, script_id, body.model_dump())
    except air_adapter.ScriptNotFound:
        raise _error("SCRIPT_NOT_FOUND", f"no final_script_package with id '{script_id}'", 404)
    except air_adapter.ScriptAlreadyApproved:
        raise _error("ALREADY_APPROVED", f"'{script_id}' is already operator_approved; retry with the same idempotency_key if this was meant to be a replay", 409)
    except AirValidationError as exc:
        raise _error("VALIDATION_ERROR", str(exc), 422)
    return {
        "approval_ref": {k: result["approval"][k2] for k, k2 in (("object_id", "object_id"), ("version", "semantic_version"), ("sha256", "canonical_sha256"))},
        "decision": "APPROVE",
        "script": air_projection.project_script_detail(air, result["script"]),
    }


@router.post("/scripts/{script_id}/transfer-contract", response_model=schemas.TransferContractResponse)
def create_transfer_contract(script_id: str, body: schemas.TransferContractRequest, air=Depends(get_air)):
    try:
        contract = air_adapter.create_transfer_contract(air, script_id, body.model_dump())
    except air_adapter.ScriptNotFound:
        raise _error("SCRIPT_NOT_FOUND", f"no final_script_package with id '{script_id}'", 404)
    except air_adapter.ScriptNotApproved:
        raise _error("SCRIPT_NOT_APPROVED", f"final_script_package '{script_id}' has operator_approved=false; a transfer contract cannot be created until FR-APP-032 approval is recorded", 409)
    except AirValidationError as exc:
        raise _error("VALIDATION_ERROR", str(exc), 422)
    return {
        "contract_ref": {"object_id": contract["object_id"], "version": contract["semantic_version"], "sha256": contract["canonical_sha256"]},
        "final_script_ref": contract["payload"]["final_script_ref"],
    }
```

### Stage 4 — Wiring

**`api/main.py`** (additive only — no corrective patch needed, contrast TS-APP-API-002 Stage 0):
```python
from api.routers import air as air_router
# ... existing router registrations from TS-APP-API-002/003/004/006 ...
app.include_router(air_router.router, prefix="/api/air", tags=["air"])
```

**`api/schemas/__init__.py`** — no change needed; `api/schemas/air.py` is imported directly as `from api.schemas import air as schemas` per Stage 3.

---

## 8. Failure, Migration, Rollback, Recovery, and Observability

### Typed failures
| Failure | HTTP status | error_code |
|---|---|---|
| Portfolio/script id does not resolve, or resolves to the wrong object type | 404 | `PORTFOLIO_NOT_FOUND` / `SCRIPT_NOT_FOUND` |
| `portfolio_state != "OPEN"` at select time | 409 | `PORTFOLIO_NOT_OPEN` |
| `candidate_judgments` doesn't cover exactly the portfolio's candidates | 422 | `CANDIDATE_JUDGMENTS_INCOMPLETE` |
| `selected_hypothesis_id` not among the portfolio's candidates | 404 | `UNKNOWN_CANDIDATE` |
| Comparison result doesn't decisively match the caller's stated pick | 409 | `SELECTION_NOT_SUPPORTED_BY_SCORES` |
| Optimistic-concurrency race on the final portfolio re-store | 409 | `CONFLICT` |
| Script already `operator_approved` | 409 | `ALREADY_APPROVED` |
| Transfer contract requested before approval | 409 | `SCRIPT_NOT_APPROVED` |
| Any `AirValidationError` from `domain.py::validate_air_object` (malformed refs, wrong enum values, missing required fields the Pydantic layer didn't already catch) | 422 | `VALIDATION_ERROR` |

### Migration
None. No new tables; `AirRepository`'s existing schema (initialized by TS-APP-API-001's lifespan) is unchanged.

### Rollback
Revert `api/main.py`'s one `include_router` line and delete the three new files. No data migration to reverse — this spec never alters AIR's schema, only reads/writes through its existing service methods.

### Recovery
Every multi-step write in `select_hypothesis` uses a suffixed idempotency key per sub-call (`f"{idempotency_key}:gate:{hypothesis_id}"`, etc.), the same pattern `ContentBatchService.compile_batch` already established for its own per-job keys. A client that retries a failed `POST /api/air/hypotheses/{portfolio_id}/select` with the **same** top-level `idempotency_key` replays every already-committed sub-step idempotently (AIR's `store_object` dedupes on idempotency key) and only re-attempts the step that actually failed. A client that fails partway and retries with a **different** `idempotency_key` on a portfolio already left in a partially-gated state (some `gate_hypothesis` calls succeeded, `compare_portfolio` did not) will simply re-run `gate_hypothesis` for every candidate again under new keys — each call is independently content-addressed and safe to repeat; no partial state is corrupted, only some redundant `hypothesis_gate_result` objects may accumulate. This is a known, accepted cost, not silently hidden.

### Observability
No new logging/metrics infrastructure — this spec relies on whatever `api/main.py` already established in TS-APP-API-001. Every error response's `message` field includes the specific object id and, where relevant, the exact decision/state that caused the failure, per the examples in Section 6.

---

## 9. Acceptance Criteria

- **AC-001** `GET /api/air/hypotheses/{portfolio_id}` against a portfolio created by `production_demo.py`'s fixture data (or an equivalent test fixture) returns every candidate with `psychological_role`, `tension`, and `diversity_signature` populated, and returns `404 PORTFOLIO_NOT_FOUND` for an unknown id.
- **AC-002** `GET /api/air/hypotheses/{portfolio_id}` against an id that resolves to a `final_script_package` (wrong object type) returns `404 PORTFOLIO_NOT_FOUND`, not a 500 or a 400.
- **AC-003** `POST /api/air/hypotheses/{portfolio_id}/select`, given per-candidate judgments engineered so one candidate decisively wins by more than `decisive_margin_micros`, returns `200` with `decision: "DECISIVE_WINNER"`, `stop_reason: "DECISIVE_ELIGIBLE_WINNER"`, and the response `portfolio.portfolio_state == "PROMOTED"`.
- **AC-004** The same request, re-sent with the identical `idempotency_key`, returns the same `200` response (idempotent replay) without creating duplicate `hypothesis_gate_result`/`comparative_evaluation_receipt` objects — verified by asserting `air_app.repository.list_current(object_type="hypothesis_gate_result")` count is unchanged between the two calls.
- **AC-005** `POST /api/air/hypotheses/{portfolio_id}/select` with `candidate_judgments` missing one candidate returns `422 CANDIDATE_JUDGMENTS_INCOMPLETE` and performs **no** AIR writes — verified by asserting the portfolio's `revision` is unchanged after the call.
- **AC-006** `POST /api/air/hypotheses/{portfolio_id}/select` with scores engineered to produce `AMBIGUOUS` (two candidates within `decisive_margin_micros` of each other) returns `409 SELECTION_NOT_SUPPORTED_BY_SCORES` and performs no writes past the `compare_portfolio` call — verified by asserting no `hypothesis_stopping_receipt`, `planned_activative_intelligence_pack`, or `hypothesis_promotion_receipt` object was created.
- **AC-007** `POST /api/air/hypotheses/{portfolio_id}/select` against a portfolio whose `portfolio_state` is already `"PROMOTED"` (from a prior successful select) returns `409 PORTFOLIO_NOT_OPEN`.
- **AC-008** `GET /api/air/scripts/{script_id}` for a script with `operator_approved: false` returns `batch_compilation_refs: {"reason": "SCRIPT_NOT_APPROVED"}`.
- **AC-009** `POST /api/air/scripts/{script_id}/approve` against that same script returns `200`, and a subsequent `GET /api/air/scripts/{script_id}` shows `operator_approved: true, composition_eligible: true`, and `batch_compilation_refs: {"reason": "NO_TRANSFER_CONTRACT_YET"}` — proving approval alone is honestly insufficient for a batch-ready ref set (Source gap notice B).
- **AC-010** `POST /api/air/scripts/{script_id}/approve` against an already-approved script returns `409 ALREADY_APPROVED`.
- **AC-011** `POST /api/air/scripts/{script_id}/transfer-contract` against an unapproved script returns `409 SCRIPT_NOT_APPROVED` (this spec's own added precondition — Governing Decisions §3).
- **AC-012** `POST /api/air/scripts/{script_id}/transfer-contract` against the now-approved script from AC-009 returns `200`, and a subsequent `GET /api/air/scripts/{script_id}` returns a populated `batch_compilation_refs` object whose five fields — `final_script_ref`, `semantic_program_ref`, `archetype_coalition_ref`, `primitive_coalition_ref`, `activation_transfer_contract_ref` — each independently pass `services/pipeline/src/cmf_pipeline/domain/validation.py::require_ref` unchanged (this is the spec's central claim and must be tested against the real Pipeline validator function, imported directly, not a re-implementation of it).
- **AC-013** The `semantic_program_ref` value returned in AC-012 is byte-identical to the script's own `program_ref` field (proves the field-name projection in Source gap notice D is a rename, not a different value).
- **AC-014** `GET /api/air/scripts/{script_id}` for a script revision that existed **before** approval (fetched via `air_app.repository.history(script_id)[0]`, not the current revision) is not reachable through this spec's routes at all — `GET` only ever resolves the current revision, per `AirRepository.get_object`'s own behavior; no test asserts otherwise, this is a documented limitation (Section 3, `list_edges` note) not a bug.
- **AC-015** A transfer contract created for revision N of a script, followed by a second, unrelated approval-triggered revision N+1 of the *same* `script_id` (out of scope to trigger via this spec's own routes, but constructible directly against `AirRepository` in a test), does **not** cause `resolve_batch_refs` to return the stale contract for revision N+1 — proving the exact-ref match (not just matching `object_id`) in Governing Decisions §3 actually discriminates by revision.

### Build Receipt claim ceiling
This spec's Build Receipt, once implemented, may claim:
- `ACTIVATIVE_INTELLIGENCE_API_DEVELOPMENT_EVIDENCE`
- The five refs `ContentBatchService.compile_batch()` requires from AIR are obtainable over HTTP, in the exact field names Pipeline's `require_ref` expects, once a script has been approved and a transfer contract created

This spec's Build Receipt may **not** claim:
- That any hypothesis judgment or Final Script content was produced by a real evaluative model (`external_model_calls: 0` remains true — see Governing Decisions §3)
- That a hypothesis portfolio can be generated over HTTP (Source gap notice F remains open)
- That `ContentBatchService.compile_batch()` has ever actually been called by this spec or any spec before it (that remains TS-APP-API-004's revisit, per the Ledger's Resolution Sequence step 9)
- That GAP-002 (Harness/Pipeline schema mismatch) is resolved — unrelated, still open under TS-APP-BRIDGE-001

---

## 10. Testing and Completion Evidence

### Test files to create
- `tests/api/test_air_hypotheses_get.py` — AC-001, AC-002
- `tests/api/test_air_hypotheses_select.py` — AC-003 through AC-007
- `tests/api/test_air_scripts_get.py` — AC-008, AC-014, AC-015
- `tests/api/test_air_scripts_approve.py` — AC-009, AC-010
- `tests/api/test_air_transfer_contract.py` — AC-011, AC-012, AC-013
- `tests/api/fixtures/air_portfolio_fixture.py` — a shared pytest fixture that builds a fresh 3-candidate portfolio the same way `production_demo.py` lines ~190–240 do (`store_hypothesis` ×3, `store_portfolio`), reused by every test file above rather than re-running the full demo (which also builds VAE/Interview state this spec's tests don't need)

### Test tooling
- `pytest`, `httpx.AsyncClient` against the FastAPI app with `app.state.air = AirApplication(tmp_path / "air.sqlite3")`, matching the pattern already established by TS-APP-API-002/003/004's own test Stages
- `services.pipeline.src.cmf_pipeline.domain.validation.require_ref` imported directly in `test_air_transfer_contract.py` for AC-012 — this spec's central claim must be verified against the real Pipeline function, not a hand-written lookalike

### Pre-existing regression
Run `tests/phase5/test_derivative_compiler.py` and `tests/phase3/test_authority_and_batch.py` unchanged before and after this spec's implementation, to confirm no existing AIR/Pipeline behavior was altered — this spec adds a new HTTP layer and orchestration module but modifies no file under `services/air/` or `services/pipeline/`.

### Build Receipt claim ceiling
See Section 9.

---
document_end: true
next_action: >
  Per SPEC_GAP_LEDGER.md's Resolution Sequence, TS-APP-BRIDGE-001 (Harness
  Definition Compiler, closing GAP-002) is the other spec that must exist
  before Gate C. This spec (TS-APP-API-007) and TS-APP-BRIDGE-001 have no
  dependency on each other and can be implemented in either order or in
  parallel. Once both exist, TS-APP-API-004's compile_batch()-covering Stage
  should be revisited (Ledger step 9) to actually call
  ContentBatchService.compile_batch() using this spec's
  batch_compilation_refs and TS-APP-BRIDGE-001's compiled harness binding.
  Separately: whoever writes the Worker/Dispatcher spec TS-APP-API-005
  recommended should use the ID TS-APP-API-008, not TS-APP-API-007 (Source
  gap notice E).
---
