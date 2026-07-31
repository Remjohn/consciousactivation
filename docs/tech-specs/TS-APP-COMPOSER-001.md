---
spec_id: TS-APP-COMPOSER-001
title: Interview Composer Service Integration
document_class: TECH_SPEC
product: Conscious Activations
module: composer
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CURRENT
build_authority: false
prepared: 2026-07-31
controlling_frs:
  - FR-APP-010 (Guest Research Package — "operator can create a Guest Research
    Package for a prospective guest: name, URLs, uploaded documents")
  - FR-APP-011 (Activative Interview Brief — "the system generates an
    Activative Interview Brief: tension hypothesis, Matrix of Edging seed,
    planned question sequence, expression targets, pulling the active Brand
    Context Version and Voice DNA")
  - FR-APP-012 (Session scheduling and hand-off — "operator can attach a
    recording date, link a recorded .mp4 or audio file, and transition the
    Brief into a live Canonical Interview Source Package upon upload")
controlling_stories:
  - ST-APP-02.01 through ST-APP-02.04 are named only by range against Epic 2
    in `CA_APP_FR_EPIC_SPEC_PLAN.md` Part 4 ("Stories: ST-APP-02.01 through
    ST-APP-02.04"). Part 2's own Epic 2 header instead reads "Stories:
    ST-APP-02.01 through ST-APP-02.05" -- a one-story discrepancy between
    Part 2 and Part 4 that this spec did not introduce and cannot resolve by
    inspection (Part 3, "Selected Critical Path," writes no acceptance text
    for either range, so there is no ST-APP-02.05 to confirm or discard). See
    Section 1, Source gap notice C. Following the precedent TS-APP-API-006
    and TS-APP-API-007 already established for their own unwritten story
    ranges, this spec derives its acceptance criteria directly from
    FR-APP-010/011/012, not from invented story text.
upstream_dependencies:
  - CA_PROJECT_SNAPSHOT.md (authority -- CURRENT)
  - CA_APP_FR_EPIC_SPEC_PLAN.md (authority -- CURRENT; this is the Wave 4 /
    "last spec in the queue" entry, gated in that document on "internal
    Interview Composer codebase must be provided" -- see Section 1, Source
    gap notice A, for what that gate actually means once inspected against
    the real repository)
  - SPEC_GAP_LEDGER.md (authority -- CURRENT; this spec both consumes it --
    GAP-001 through GAP-006 describe the AIR/interview/builder surface this
    spec integrates against -- and extends it. Section 1 documents a seventh
    gap, GAP-007, discovered while writing this spec. GAP-007 is appended to
    the ledger as part of this spec's file changes; see Section 7, Stage 12)
  - TS-APP-API-001.md (quality_state: WRITTEN_PENDING_AUDIT --
    DRAFT_DEPENDENCY_NOT_ACCEPTED; this spec depends only on its
    `api/dependencies.py::get_air` factory, `api/config.py::AppConfig`/
    `load_config`, and `api/errors.py::ErrorResponse` interfaces, which are
    already landed and unchanged in the current tree -- not on any claim
    that the gateway is production-ready)
  - TS-APP-API-003.md (quality_state: WRITTEN_PENDING_AUDIT --
    DRAFT_DEPENDENCY_NOT_ACCEPTED; this spec's entire reason for existing is
    to produce the `planning_lineage` object that TS-APP-API-003's
    `POST /api/interviews/brief-led` accepts as `planning_lineage_json`. This
    spec does not call that endpoint and does not modify
    `services/interview/` or `api/routers/interviews.py` in any way)
  - TS-APP-API-007.md (quality_state: WRITTEN_PENDING_AUDIT --
    DRAFT_DEPENDENCY_NOT_ACCEPTED; precedent only -- this spec follows the
    same `api/routers/air.py` request/error-mapping shape TS-APP-API-007
    established, and reuses `cmf_activative_intelligence.application.
    AirApplication` and `cmf_activative_intelligence.services.
    production_common.require_air_ref` exactly as landed, unchanged)
  - TS-APP-UI-001.md (quality_state: WRITTEN_PENDING_AUDIT --
    DRAFT_DEPENDENCY_NOT_ACCEPTED; this spec fills the placeholder route
    TS-APP-UI-001 scaffolded at `apps/web/src/routes/interviews/compose.tsx`,
    which already carries the annotation `builtIn: "TS-APP-COMPOSER-001"`,
    and reuses `apiFetch<T>`, `ApiError`, and the `components/ui/` primitive
    set exactly as landed)
downstream_consumers:
  - A future spec resolving GAP-007 (name TBD -- see Section 1, Source gap
    notice A, and the ledger entry in Section 7, Stage 12) is the only
    planned consumer of this spec's `iac_ref` / `planned_aip_ref` /
    `arm_receipt_ref` gap. It will need this spec's
    `activative_interview_brief.matrix_of_edging_seed` and
    `.planned_questions` fields, which are deliberately shaped to match
    `cmf_activative_intelligence.domain._validate_matrix`'s and
    `phase9_domain.py`'s field names so that spec does not have to re-derive
    them.
  - The human operator (via the React page this spec ships) is the consumer
    of record for FR-APP-010/011/012 today: this spec's HTTP surface is
    designed to be called directly by a person composing a Brief, not only
    by a future automated pipeline.
output_path: services/interview-composer/ (new package), api/routers/
  interview_composer.py, api/schemas/interview_composer.py, api/services/
  composer_air_bridge.py, api/dependencies.py (adapt), api/main.py (adapt),
  apps/web/src/routes/interviews/compose.tsx (replace placeholder), and the
  supporting apps/web/src files listed in Section 7
wave: 4 (final spec in the FR-APP Epic/Story/Spec Plan document order)
---

# TS-APP-COMPOSER-001 — Interview Composer Service Integration

## 0. What this spec is, and what it is honest about not being

`CA_APP_FR_EPIC_SPEC_PLAN.md` lists this as the last unwritten spec in Wave 4,
gated with one line: "Prerequisite: internal Interview Composer codebase must
be provided." That codebase was never provided to this repository. A direct
search of the full tree (`grep -ril "interview.composer\|composer"`,
`find . -iname "*interview-composer*"`, both excluding `archive/`) turns up
exactly one hit that is actual product code: the placeholder route
TS-APP-UI-001 already scaffolded. There is no `services/interview-composer/`
directory, no `ActivativeInterviewBrief` domain module, and no guest-research
or tension-hypothesis reasoning engine anywhere outside doctrine documents
(`governance/program-control/`) and the two planning documents this spec
already lists as authorities.

That absence is real, but it is not, on inspection, the only thing standing
between an operator and a working Interview Composer. Section 1 documents a
second, deeper finding made while reading the real, already-implemented AIR
service code (`services/air/src/cmf_activative_intelligence/`): two of the
four fields `conscious_activations_interview_expression`'s own
`validate_planning_lineage()` requires for a Brief-led interview admission --
`planned_aip_ref` and, transitively through it, `iac_ref` -- resolve to a real
AIR object type (`planned_activative_intelligence_pack`) whose store method
cross-validates that its four upstream refs are **real, already-stored** AIR
objects (`matrix_of_edging`, `activation_hypothesis`,
`activation_hypothesis_portfolio`, `psychological_role_tension_contract`).
Constructing those legitimately -- without inventing hollow refs to objects
that were never really reasoned about -- requires exactly the kind of
research-to-hypothesis reasoning the missing internal Composer codebase was
supposed to supply. No spec, this one included, can honestly manufacture that
reasoning from nothing.

This spec does not try. It builds the entire integration surface that *is*
honestly buildable today -- Guest Research Package creation, Brand DNA
cross-referencing against the real AIR repository, operator-authored Brief
composition and storage, and session/relationship-stage tracking reusing
AIR's real `Phase9ActivativeService.compile_relationship_program` -- and it
draws the remaining gap as precisely as the evidence allows, rather than
papering over it. That gap is catalogued as GAP-007 in Section 1 and in the
ledger update in Section 7, Stage 12.

## 1. Files and authorities read

Every fact below was read from the file, not recalled or inferred. Hashes are
the first 8 hex characters of `sha256sum` on the file as it exists in the
supplied `consciousactivation-main.zip`. Several hashes match values already
cited in TS-APP-API-003.md, TS-APP-API-007.md, and TS-APP-UI-001.md
verbatim, confirming those files have not moved since those specs were
written.

| # | File | Hash | Fact taken from it |
|---|------|------|---------------------|
| 1 | `docs/tech-specs/CA_PROJECT_SNAPSHOT.md` | `b568220d` | Module map: "Interview Composer: Research guest, engineer Brief, create interview session" is its own row, separate from "Activative Intelligence (AIR): Find tension, build Primitive Coalition, Archetype, Final Script," which the doctrine places *after* interview admission, driven by Expression Moments -- not before it. |
| 2 | `docs/tech-specs/CA_APP_FR_EPIC_SPEC_PLAN.md` | `8ea2646c` | Wave 4 entry for TS-APP-COMPOSER-001: FRs 010/011/012, output `POST /api/interviews/compose/research`, `POST /api/interviews/compose/brief`, `React InterviewComposer.tsx`, gated on "internal Interview Composer codebase must be provided." |
| 3 | `docs/tech-specs/SPEC_GAP_LEDGER.md` | `d30dc393` | Catalogs GAP-001 through GAP-006 against TS-APP-API-001 through TS-APP-UI-004; as of the version read, says "No specs remain to be written" for that set -- written before this spec existed, and silent on Composer entirely. |
| 4 | `docs/tech-specs/TS-APP-API-001.md` | `7fe1b48f` | Defines `api/dependencies.py`, `api/config.py::AppConfig`, `api/errors.py::ErrorResponse` as the Stage-1 gateway contracts every later API spec depends on without re-deriving them. |
| 5 | `docs/tech-specs/TS-APP-API-003.md` | `5d6471f6` | Establishes the precedent this spec follows most directly: `/brief-led` "accepts planning-lineage refs as opaque caller-supplied input; it does not generate a Brief." |
| 6 | `docs/tech-specs/TS-APP-API-007.md` | `81916eca` | Precedent for citing FR text directly when Part 3 has no story-level acceptance text (see `controlling_stories` above), and for the `air_adapter`/`air_projection` two-module router-support split this spec's `composer_air_bridge.py` partially mirrors. |
| 7 | `api/main.py` | `8d0d0f62` | The real, current `lifespan()` wiring: `pipeline`, `air`, `vae`, `interview`, `campaign_repository`, `builder`, `studio_bridge` are constructed and attached to `app.state` in that order; routers are included with an explicit "Wave 2 routers registered here as each spec is implemented" comment marking where new routers are added. No composer entry exists yet. |
| 8 | `api/dependencies.py` | `58d48963` | Real `get_air(request) -> AirApplication` and `get_interview(request) -> InterviewExpressionApplication` factories, both `return request.app.state.<name>`. No `get_composer` exists yet. |
| 9 | `api/routers/interviews.py` | `ca17b8af` | The real, already-implemented `/brief-led` endpoint: `planning_lineage_json: str = Form(...)`, `json.loads()`'d and passed **verbatim, unvalidated by the router** into `command["planning_lineage"]`. Confirms this spec's job is to produce that JSON object, not to call this endpoint. |
| 10 | `api/routers/air.py` | `ab7a11a1` | Real, landed router pattern this spec's `api/routers/interview_composer.py` follows: a local `_error(code, message, status)` helper building `ErrorResponse`, one `try/except` per adapter-raised exception type mapped to an HTTP status. |
| 11 | `services/interview/src/conscious_activations_interview_expression/domain.py` | `abbd7511` | `validate_planning_lineage()` (lines 90-107): for `BRIEF_LED`, requires exactly `{state, brief_ref, planned_aip_ref, iac_ref, arm_receipt_ref, planned_object_digests}`; each ref is checked only for *shape* via `require_ref` (object_id/version/sha256 present and well-formed) -- **never dereferenced into any other module's repository**. `planned_object_digests` must have keys exactly `{brief, planned_aip, iac}` and each digest must equal the matching ref's own `sha256`, or admission fails with `INT_ARMED_PLAN_HASH_MISMATCH`. |
| 12 | `services/interview/src/conscious_activations_interview_expression/canonical.py` | `61a1f92c` | `require_ref`, `semantic_id`, `exact_keys`, `require_portable_uri`, `sorted_unique_strings` -- the exact small validation-helper module this spec's own `canonical.py` (Section 7, Stage 1) is a deliberate, non-shared adaptation of. |
| 13 | `services/interview/src/conscious_activations_interview_expression/repository.py` | `7259d89d` | The exact content-addressed, idempotency-keyed SQLite storage pattern (`execute_idempotent`, `store_object`, `get_object`, `list_objects`) this spec's `repository.py` (Section 7, Stage 3) reuses structurally, with `ic_` table prefixes and no events/snapshots tables (Composer has no live in-session state to event-source; that already belongs to `services/interview/src/.../live_state.py`, which is out of this spec's scope). |
| 14 | `services/interview/src/conscious_activations_interview_expression/application.py` | `25bd47f5` | The module-wiring shape (`self.repository = ...Repository(...)`, then one attribute per service class) this spec's `application.py` follows. |
| 15 | `services/interview/src/conscious_activations_interview_expression/errors.py` | `b2cfcdce` | The `RuntimeError` subclass-with-`code`-attribute error taxonomy pattern this spec's `errors.py` follows (`INT_*` codes become `IC_*` codes). |
| 16 | `services/interview/src/conscious_activations_interview_expression/__init__.py` | `bbaf0148` | `PRODUCT_ID`, `PRODUCT_VERSION`, `AUTHORITY_STATE = "candidate_not_current"` module-constant pattern this spec's own `__init__.py` follows. |
| 17 | `services/interview/AGENTS.md` | `2bdddf00` | The per-service `AGENTS.md` boundary-declaration convention ("Allowed: ... / Prohibited: ..."), including "Prohibited: AIR semantic compilation" for `interview_expression` specifically. Composer is a *different* service with a *different*, narrower boundary (Section 3 explains why Composer is allowed to read, but never write to, the AIR repository, while `interview_expression` is not allowed to touch AIR at all). |
| 18 | `services/interview/pyproject.toml` | `78b57927` | The exact `[project]`/`[tool.setuptools]` shape a new sibling service package must replicate to be importable the same way (`ca-contracts`, `ca-runtime` as declared dependencies; `package-data` includes `migrations/*.sql`). |
| 19 | `services/air/src/cmf_activative_intelligence/application.py` | `02784b27` | `AirApplication.__init__` wires `self.brand = BrandService(...)`, `self.context = ContextService(...)`, `self.hypotheses = HypothesisService(...)`, `self.phase9 = Phase9ActivativeService(...)`, `self.repository = AirRepository(...)` as plain public attributes -- the exact surface `get_air()` already exposes to any router. |
| 20 | `services/air/src/cmf_activative_intelligence/domain.py` | `90b64dea` | `_validate_matrix` (matrix_of_edging, lines 428-456): free-text fields plus `source_refs` (minimum 1, **shape-only**, no type constraint). `_validate_role_tension` (lines 704-737): similarly shape-only on `evidence_refs`. Confirms both object types are schema-agnostic about whether their sources are interview-derived or research-derived -- the schema does not forbid a pre-interview, research-seeded Matrix of Edging. |
| 21 | `services/air/src/cmf_activative_intelligence/production_domain.py` | `dfdf4b90` | `_validate_activation_hypothesis` (lines 209-243+): `source_kind` enum explicitly includes `"research_synthesis"` and `"operator_supplied"` alongside `"interview_expression"`; `epistemic_state` must be `planned` or `inferred` (never `observed`) for a hypothesis. `_validate_planned_pack` (lines 552-571): requires `epistemic_state == PLANNED` and four ref fields (`portfolio_ref`, `selected_hypothesis_ref`, `matrix_of_edging_ref`, `role_tension_ref`), each only shape-checked *at the schema layer*. |
| 22 | `services/air/src/cmf_activative_intelligence/phase9_domain.py` | `8bd3ae5f` | `interview_asset_contract` (IAC) required fields, including `planned_pack_ref`, `branch_program` (must cover exactly the 7 governed branches `ANCHOR_HIT / PARTIAL_HIT / DEFENSE / TOPIC_ESCAPE / CONTRADICTION / OVERLOAD / RELATIONAL_RESET`), `pressure_envelope.ceiling`. `interview_asset_contract_arm_receipt`: `production_authorized` must be `False`; `evaluation_result` must be `PASS`. |
| 23 | `services/air/src/cmf_activative_intelligence/services/brand_service.py` | `feaa2d70` | `BrandService` has `store_brand_context`, `store_voice_dna` (cross-validates `brand_context_ref` for real via `_require_brand`), `store_visual_dna`, `store_distillation_receipt`. **No `get_active_brand_context(workspace_id)` or equivalent lookup-by-workspace method exists anywhere in AIR** -- confirms Brand Context / Voice DNA refs must be supplied by the caller, the same opaque-ref pattern used everywhere else in this codebase, not invented by this spec. |
| 24 | `services/air/src/cmf_activative_intelligence/services/phase9_service.py` | `433a5a05` | `compile_interview_asset_contract(*, program_id, planned_pack_ref, source_context_ref, evidence_refs, parent_lock_refs, evaluation_profile_ref, idempotency_key)` -- **takes `planned_pack_ref` as a required parameter**, i.e. IAC construction itself depends on a real planned pack already existing. `arm_contract(...)` hardcodes `production_authorized: False`. `compile_relationship_program(...)` produces a real `relationship_activation_state` (stage `ENGAGED`) and `reelcast_progression_program` (a `brief` step at `status: "PENDING"`, `stage_to: "BRIEF_ACCEPTED"`) -- reused as-is by this spec's session tracking (Section 5). |
| 25 | `services/air/src/cmf_activative_intelligence/services/hypothesis_service.py` | `744fb8b7` | `store_planned_pack()` (lines 94-100): calls `require_air_ref(repository, ref, object_types=kind)` for **all four** of `portfolio_ref` (`activation_hypothesis_portfolio`), `selected_hypothesis_ref` (`activation_hypothesis`), `matrix_of_edging_ref` (`matrix_of_edging`), `role_tension_ref` (`psychological_role_tension_contract`) -- these must be real, already-stored AIR objects, not merely well-shaped refs. This is the load-bearing evidence for GAP-007 (Section 1, Source gap notice A). `store_portfolio()` similarly requires every `candidate_refs` entry to resolve to a real `activation_hypothesis` with a distinct `diversity_signature`. |
| 26 | `services/air/src/cmf_activative_intelligence/services/context_service.py` | `3c94af3c` | `store_matrix()` calls `self.semantic.store("matrix_of_edging", payload, ...)` with **no cross-validation of `source_refs` contents at all** -- confirms a Matrix of Edging can legitimately cite Guest Research artifacts as its `source_refs` without AIR ever needing to know what a "Guest Research Package" is. |
| 27 | `services/air/src/cmf_activative_intelligence/services/production_common.py` | `a657f4f0` | `require_air_ref(repository, ref, *, object_types=...)` -- raises `ObjectNotFound` (import from `..repositories.air_repository`) if the id is missing, `ValueError` on type/version/hash mismatch. This is the exact function this spec's `api/services/composer_air_bridge.py` (Section 7, Stage 8) calls to cross-validate operator-supplied `brand_context_ref`/`voice_dna_ref` for real. |
| 28 | `packages/ca_contracts/src/ca_contracts/__init__.py` | `710e7869` | Exports `canonical_sha256`, `canonical_json_text`, `bytes_sha256`, `utc_now_rfc3339` -- the only cross-product-shared canonicalization helpers in this repository. Confirms product-local `canonical.py`/`domain.py` files (per-product, not shared) are the established pattern, not an exception this spec is inventing. |
| 29 | `packages/ca_runtime/src/ca_runtime/paths.py` | `915d1131` | `default_database_path(product_id)` returns `data_root() / product_id / "product.sqlite3"`, honoring `CA_DATA_ROOT`. |
| 30 | `apps/web/src/routes/interviews/compose.tsx` | `5be453bd` | The existing placeholder: `<PlaceholderPage title="Interview Composer" frRange="FR-APP-010..012" builtIn="TS-APP-COMPOSER-001" />`. This is the exact file this spec replaces. |
| 31 | `apps/web/src/api/http.ts` | `00276e2d` | `apiFetch<T>` always merges `"Content-Type": "application/json"` into request headers before any caller-supplied `init.headers`, i.e. it **cannot correctly be used for a `multipart/form-data` (FormData-body) request** without that header being wrong. See Section 1, Source gap notice B. |
| 32 | `apps/web/src/api/interviews.ts` | `05a994a6` | `importInterview()` builds a `FormData` body and calls `apiFetch<ImportInterviewResponse>("/api/interviews/import", { method: "POST", body: form })` with no header override -- i.e. it inherits the same `Content-Type: application/json` header `apiFetch` always sets, on a `FormData` body. This is a pre-existing defect in already-landed TS-APP-UI-002 code, not something this spec introduces or is in scope to fix (see Source gap notice B), but this spec's own multipart call (Guest Research document upload) is written to avoid repeating it. |
| 33 | `apps/web/src/hooks/useImportInterview.ts`, `useHarnesses.ts` | `cf3f3a57`, `f424e2ed` | The two `@tanstack/react-query` hook shapes (`useMutation` wrapping an `api/*.ts` function; `useQuery` wrapping `apiFetch` directly) this spec's own hooks (Section 7, Stage 11) follow. |
| 34 | `apps/web/src/components/ui/{Card,Button,Badge,Textarea}.tsx` | `98e4dd00`, n/a, n/a, `02437fb0` | The shared design-token primitive set (`bg-surface`, `border-border`, `text-foreground`, `text-muted-foreground`, `bg-accent-solid`) this spec's new components are built from. `Textarea.tsx`'s own docstring says it exists so "later form-bearing pages ... reach for it instead of an inline `<textarea>`" -- this spec is that later page. |
| 35 | `apps/web/src/api/types.ts` | `aa9f6481` | Confirms the additive, non-destructive pattern for extending this file (new interfaces appended, existing ones untouched) and the `@ca/studio/domain` re-export block this spec does not touch. |
| 36 | `tests/api/conftest.py` | -- | The shared `api_app(tmp_path, monkeypatch)` fixture (sets `CA_DATA_ROOT`/`CA_MEDIA_ROOT`, lazily imports `api.main`) every `tests/api/test_*.py` file already reuses; this spec's own new test files reuse it unchanged rather than redefining it. |

### Source gap notice A — GAP-007: no legitimate path to `planned_aip_ref` / `iac_ref` exists yet, anywhere

This is the central finding of this spec, so it is stated once here precisely
and then treated as settled for the rest of the document.

`validate_planning_lineage()` (file 11) requires `planned_aip_ref` and
`iac_ref` for any `BRIEF_LED` admission, and cryptographically ties both to
`planned_object_digests`. Inside `conscious_activations_interview_expression`
these are opaque refs -- fine, and exactly what TS-APP-API-003 already
documented. The question this spec had to answer is: opaque *to
`interview_expression`*, yes, but can *this* spec, which does have an
in-process AIR handle, legitimately produce the real objects those refs
point to?

Tracing the real, landed AIR code (files 20, 21, 22, 24, 25):

- `iac_ref` → `interview_asset_contract`, compiled by
  `Phase9ActivativeService.compile_interview_asset_contract()`, which takes
  `planned_pack_ref` as a **required parameter** (file 24).
- `planned_aip_ref` → `planned_activative_intelligence_pack`, stored by
  `HypothesisService.store_planned_pack()`, which cross-validates that
  `portfolio_ref`, `selected_hypothesis_ref`, `matrix_of_edging_ref`, and
  `role_tension_ref` **each resolve to a real, already-stored AIR object of
  the matching type** -- not merely a well-shaped ref (file 25, lines
  94-100).

So both refs bottom out on the same requirement: a real
`activation_hypothesis_portfolio` containing a real, selected
`activation_hypothesis`, built against a real `matrix_of_edging` and a real
`psychological_role_tension_contract`. The schema for all four of those
object types turns out to be honestly agnostic about whether their evidence
is interview-derived or research-derived (files 20, 21) -- AIR's own
`activation_hypothesis.source_kind` enum lists `research_synthesis` and
`operator_supplied` as first-class values, and its `epistemic_state` must be
`planned`, never `observed`, for exactly this pre-interview case. That is a
real, doctrinally-intended door: a "planned," research-seeded hypothesis
chain is not a hack this spec would be inventing.

What stands in the way is not a missing door but a missing occupant. Building
a real `activation_hypothesis` honestly requires content for
`psychological_role`, `tension`, `activation_directions`, `pressure_path`,
`stance`, `counteractivation_hypotheses`, and more -- genuine psychological
reasoning about a specific guest, derived from their research package. That
reasoning is precisely what the never-provided internal Interview Composer
codebase was supposed to supply, and it is precisely what no spec can
honestly reconstruct by inspecting schemas. Fabricating placeholder refs to
satisfy `require_air_ref`'s existence check -- storing an empty or
templated `matrix_of_edging`/`activation_hypothesis`/`role_tension_contract`
purely so `planned_aip_ref` and `iac_ref` become non-null -- would violate
this codebase's own epistemic-honesty doctrine as directly as fabricating an
SRT word as `OBSERVED` instead of `INFERRED` would (see Section 3).

**Resolution path (out of scope for this spec, catalogued for the next
one):** GAP-007, appended to `SPEC_GAP_LEDGER.md` in Section 7, Stage 12,
names this precisely and proposes that a future spec -- scoped to AIR, not to
Composer -- define a "planned hypothesis pipeline": a bounded, honestly-typed
way for a human operator (or, later, a real reasoning system) to author a
`matrix_of_edging` / `activation_hypothesis` / `activation_hypothesis_portfolio`
/ `psychological_role_tension_contract` chain from a Guest Research Package
*before* an interview happens, using the `research_synthesis` /
`operator_supplied` vocabulary AIR's schema already reserves for it. This
spec's `activative_interview_brief.matrix_of_edging_seed` and
`.planned_questions` fields (Section 6) are deliberately shaped to hand that
future spec a head start rather than a blank page.

### Source gap notice B — `apiFetch` cannot safely carry a `FormData` body

File 31/32: `apiFetch<T>` unconditionally sets `Content-Type:
application/json`. `importInterview()` (already-landed TS-APP-UI-002 code)
passes a `FormData` body through it anyway, which means the browser's
multipart boundary header is overridden by the wrong, hardcoded
`application/json` value on every real request that function makes. This is
a pre-existing defect. It is not this spec's job to fix `apps/web/src/api/
interviews.ts` or `apiFetch` itself (out of scope; no controlling FR asks for
it, and touching shared `http.ts` behavior could affect every other caller).
This spec's own multipart call (Guest Research document upload, Section 7,
Stage 11) is written against a new, additive `apiFetchMultipart` helper
instead of `apiFetch`, so it does not repeat the defect. This is noted here,
not fixed elsewhere, per the "do not touch what you were not asked to touch"
convention every prior spec in this repository has followed.

### Source gap notice C — the ST-APP-02 story-count discrepancy

`CA_APP_FR_EPIC_SPEC_PLAN.md` Part 2 lists Epic 2 as "Stories: ST-APP-02.01
through ST-APP-02.05" (five stories); Part 4's Wave 4 row for this spec lists
"Stories: ST-APP-02.01 through ST-APP-02.04" (four). Part 3 writes
acceptance text for neither range. This spec cannot determine from the
supplied documents whether a fifth story was dropped, renumbered, or never
written, and does not guess. Per `controlling_stories` above, acceptance
criteria are derived from FR text, which is unambiguous, rather than from
either story count.

## 2. Problem, user outcome, and scope

### Problem

Of the two documented entry points into this product (`CA_PROJECT_SNAPSHOT.md`
Section "Two Ways In"), Entry Point A -- "Engineered Interview," starting from
Guest Research and ending at a Brief-led admission -- currently has no
starting point at all. `POST /api/interviews/brief-led` has existed and been
directly testable since TS-APP-API-003 landed, but nothing in this repository
has ever produced a `planning_lineage` object for it to accept, other than
hand-written JSON in test fixtures. FR-APP-010, FR-APP-011, and FR-APP-012 are
each marked "Missing: HTTP endpoint, React page" in the project snapshot's
gap table, and the route that should host this work
(`apps/web/src/routes/interviews/compose.tsx`) is still the literal
placeholder TS-APP-UI-001 left for it.

### User outcome

An operator can:

1. Create a Guest Research Package for a prospective guest: a name, a list of
   source URLs, and optionally uploaded reference documents -- all stored,
   content-addressed, and citable, never fetched or summarized by this spec.
2. Author an Activative Interview Brief against that package: supply the
   tension hypothesis, a Matrix-of-Edging seed (in AIR's own real field
   vocabulary), a planned question sequence (each question tagged with one of
   AIR's seven real branch conditions), and expression targets -- while the
   system, not the operator, supplies and cross-checks the Brand Context
   Version and Voice DNA references against the real, currently-stored AIR
   objects, refusing to store a Brief against Brand DNA that does not exist.
3. See, plainly and without euphemism, which of the four planning-lineage
   refs a Brief-led admission needs are real today (`brief_ref`) and which are
   not yet buildable (`iac_ref`, `planned_aip_ref`, `arm_receipt_ref`) and
   why (GAP-007), rather than a silently-broken or silently-fabricated field.
4. Open a Composer session for a Brief, attach a target recording date, and
   see a real relationship-stage record (reusing AIR's own
   `compile_relationship_program`) rather than a client-side-only status
   string.
5. Do all of the above from the real `InterviewComposer` page at
   `/interviews/compose`, not the placeholder.

### In scope

- New package `services/interview-composer/` owning three object types:
  `guest_research_package`, `activative_interview_brief`, `composer_session`.
- `api/routers/interview_composer.py`: six endpoints under
  `/api/interviews/compose` (research create/get, brief create/get, session
  create/get).
- Real, cross-validated Brand Context Version / Voice DNA referencing against
  the already-landed `AirApplication` (read-only; this spec never writes to
  AIR's repository).
- Session/relationship-stage tracking that reuses
  `Phase9ActivativeService.compile_relationship_program()` unchanged.
- The `InterviewComposer` React page, replacing the placeholder, plus
  supporting API client, hooks, and components.

### Out of scope (and why)

- **Auto-generating tension hypotheses, Matrix of Edging content, or
  question sequences from guest research.** No reasoning/NLP engine exists
  anywhere in this repository (confirmed by the same search that found no
  internal Composer codebase). `content_origin` on every Brief is therefore
  the single literal value `"operator_supplied"` -- not a default that could
  silently become something else, but the only value the type permits today.
- **Fetching or summarizing the URLs in a Guest Research Package.** They are
  stored as citations. Treating an unfetched URL as if its contents were
  known would be a fabrication this spec's own doctrine forbids (Section 3).
- **Real `iac_ref` / `planned_aip_ref` / `arm_receipt_ref` construction.**
  GAP-007. See Source gap notice A.
- **Calling `POST /api/interviews/brief-led`.** This spec produces the
  ingredients (a `brief_ref`, and, once GAP-007 closes, the rest); an actual
  recording does not exist at Brief-authoring time, so the hand-off call is
  necessarily a later, separate operator action against
  `services/interview/`, which this spec does not modify.
- **Advancing a `composer_session`'s stage past `ENGAGED`.** AIR's own
  `reelcast_progression_program` object already documents, as one of its own
  built-in limitations, "no automatic stage advance" (file 24's payload
  literals). No method in `Phase9ActivativeService` performs a stage
  transition; `compile_relationship_program` is a one-shot compiler, not a
  state machine driver. This spec does not add one, consistent with not
  modifying `services/air/`.
- **A CLI entrypoint for the new package.** No controlling FR asks for one;
  `bootstrap.py`/`status()` (Section 7) is sufficient for the same health-check
  purpose `services/interview/bootstrap.py` serves.

## 3. Governing decisions and constraints

1. **Product sovereignty, extended.** `services/interview-composer/` owns
   the identity and lifecycle of `guest_research_package` and
   `activative_interview_brief` outright. It never modifies
   `services/air/` or `services/interview/` source. It calls AIR's already-
   real, already-tested methods (`brand_service`'s implicit read path via
   `repository.get_object`, `Phase9ActivativeService.compile_relationship_
   program`) exactly as written, with no monkeypatching and no forked
   copies.
2. **Composer may read AIR's repository; it may never write to it, and it
   is not "AIR semantic compilation."** `services/interview/AGENTS.md`
   (file 17) prohibits `interview_expression` from touching AIR at all,
   because `interview_expression`'s entire job is to stay ignorant of what a
   Brief means. Composer's job is the opposite: it exists specifically to
   sit between an operator and AIR. Reading `air.repository.get_object(...)`
   to confirm a `brand_context_ref` is real is referential-integrity
   checking, the same operation `require_air_ref` performs inside AIR
   itself for its own internal refs (file 27) -- it is not compiling new AIR
   semantics, and this spec never calls any AIR *store* method other than
   `compile_relationship_program` (which is itself a pure, already-approved
   compiler, not new semantics this spec is inventing).
3. **No fabricated refs, ever.** If a real object does not exist, the field
   that would hold its ref is `null`, accompanied by an explicit
   `hypothesis_pipeline_status` block naming the reason (GAP-007). This spec
   never constructs a well-shaped-but-hollow ref (a random `object_id`, a
   real-looking `sha256` over throwaway content) merely to make a downstream
   shape check pass. This is a direct extension of this codebase's existing
   doctrine against fabricated Brief history and against upgrading
   `INFERRED` evidence to `OBSERVED`.
4. **`content_origin` is a closed, one-member enum today.**
   `Literal["operator_supplied"]`, matching AIR's own `source_kind` casing
   (file 21) exactly, so a future GAP-007 spec can carry this value straight
   through into a real `activation_hypothesis.source_kind` without
   translation. Widening this enum is itself a product decision for that
   future spec to make explicitly, not something this spec pre-decides by
   omission.
5. **Guest Research Package contents are never fetched.** `source_urls` are
   stored as opaque strings (validated only as well-formed `http(s)://` URIs)
   and `uploaded_documents` are stored as content-addressed bytes with a
   caller-declared `media_type`, exactly as `interview_expression`'s
   `make_media_asset` stores video without asserting anything about its
   *content* beyond what `ffprobe` can measure. This spec adds no scraping,
   OCR, or summarization step of any kind.
6. **Product-local contracts, not shared private modules.** Consistent with
   every existing product in this repository, `services/interview-composer/`
   has its own `canonical.py` and `domain.py`, structurally similar to
   `interview_expression`'s but not imported from it. Only `ca_contracts`
   and `ca_runtime` are shared; a product never reaches into a sibling
   product's private module.
7. **Idempotency and content-addressing follow the established pattern
   exactly.** Every write is keyed by an `Idempotency-Key` header (or a
   derived default), and every stored object's `object_id` is a
   `semantic_id()` hash of its own normalized payload, so a byte-identical
   retry is a no-op replay, never a duplicate or a conflict.
8. **Claim ceiling: `INTERVIEW_COMPOSER_INTEGRATION_SURFACE_EVIDENCE`.**
   This spec's completion evidence (Section 10) explicitly enumerates what
   it does *not* claim: it does not claim FR-APP-011 is fully satisfied (the
   "system generates" language in FR-APP-011 is only true for the Brand
   DNA cross-reference step; hypothesis content is operator-authored), and it
   does not claim FR-APP-020 (Brief-led admission) is reachable end-to-end
   through this spec's output alone.

**Forbidden in this spec, explicitly:**

- Modifying any file under `services/air/` or `services/interview/`.
- Constructing `matrix_of_edging`, `activation_hypothesis`,
  `activation_hypothesis_portfolio`, or `psychological_role_tension_contract`
  objects (GAP-007's territory).
- Calling `POST /api/interviews/brief-led` or `POST /api/interviews/import`
  from any Composer code path.
- Fetching, rendering, or summarizing a Guest Research Package URL.
- Reusing `apiFetch` for a `FormData` request body (Source gap notice B).

## 4. Current brownfield architecture

| Component | File | Current state | Disposition |
|---|---|---|---|
| `AirApplication` | `services/air/src/cmf_activative_intelligence/application.py` | Real, landed; `.brand`, `.context`, `.hypotheses`, `.phase9`, `.repository` all live attributes | **REUSE**, read-only + `compile_relationship_program` only |
| `BrandService` | `.../services/brand_service.py` | Real, landed; write-only surface (`store_brand_context`, `store_voice_dna`, `store_visual_dna`); no read-by-workspace method | **REUSE** via `air.repository.get_object` for cross-validation only; no write calls |
| `Phase9ActivativeService.compile_interview_asset_contract` / `.arm_contract` | `.../services/phase9_service.py` | Real, landed; requires a real `planned_pack_ref` | **NOT INVOKED** -- blocked by GAP-007 |
| `Phase9ActivativeService.compile_relationship_program` | `.../services/phase9_service.py` | Real, landed; produces `relationship_activation_state` (stage `ENGAGED`) + `reelcast_progression_program` | **REUSE**, unchanged, for `composer_session` creation |
| `HypothesisService.store_planned_pack` | `.../services/hypothesis_service.py` | Real, landed; cross-validates 4 real upstream refs | **NOT INVOKED** -- blocked by GAP-007 |
| `ContextService.store_matrix` | `.../services/context_service.py` | Real, landed; no cross-validation of `source_refs` | **NOT INVOKED** -- blocked by GAP-007 |
| `SourcePackageService.admit` (`BRIEF_LED` path) | `services/interview/src/.../source_package.py` (referenced via `TS-APP-API-003`) | Real, landed via `api/routers/interviews.py::brief_led_interview` | **NOT CALLED** by this spec; downstream operator action once GAP-007 closes |
| `apps/web/src/routes/interviews/compose.tsx` | -- | Placeholder (`PlaceholderPage`) | **REPLACE** |
| `apps/web/src/components/layout/Sidebar.tsx` | -- | Already links to `/interviews/compose` labeled "Interview Composer" (confirmed by grep; no excerpt needed beyond the existing nav entry) | **NO CHANGE** |
| `api/main.py` | -- | Wires 6 services, includes 6 routers | **ADAPT**: add `interview_composer` service init + router include |
| `api/dependencies.py` | -- | 7 `get_*` factories | **ADAPT**: add `get_composer` |
| `apps/web/src/api/http.ts` | -- | `apiFetch<T>` (JSON-only, see Source gap notice B) | **ADAPT**: add sibling `apiFetchMultipart`, `apiFetch` itself untouched |

## 5. Proposed architecture and workflows

### 5.1 New package shape

```
services/interview-composer/
├── pyproject.toml
├── README.md
├── AGENTS.md
└── src/conscious_activations_interview_composer/
    ├── __init__.py
    ├── errors.py
    ├── canonical.py
    ├── domain.py
    ├── repository.py
    ├── application.py
    ├── bootstrap.py
    ├── py.typed
    ├── migrations/
    │   └── 0001_interview_composer.sql
    └── services/
        ├── __init__.py
        ├── research_service.py
        ├── brief_service.py
        └── session_service.py
```

This is a structural sibling of `services/interview/`, not a fork of it: same
storage discipline (content-addressed, idempotency-keyed SQLite via
`ca_runtime`), same error taxonomy shape, same `application.py` wiring
pattern -- built fresh, per Governing decision 6.

### 5.2 Object types this spec owns

| Object type | ID field | Prefix | Cross-validated against |
|---|---|---|---|
| `guest_research_package` | `research_package_id` | `ic:research:` | nothing external (self-contained) |
| `activative_interview_brief` | `brief_id` | `ic:brief:` | own `research_package_ref` (same repo); `brand_context_ref`/`voice_dna_ref` (real AIR objects, read-only) |
| `composer_session` | `session_id` | `ic:session:` | own `brief_ref` (same repo); `relationship_state_ref`/`progression_ref` (real AIR objects, produced by `compile_relationship_program`) |

### 5.3 `POST /api/interviews/compose/research` workflow

1. Router receives `guest_name`, `source_urls_json` (JSON array of strings),
   `workspace_id`, `project_id`, `operator_id`, `authority_scope`,
   `assertion_id` as form fields, plus zero or more `documents` file uploads.
2. Each URL is validated as a well-formed `http://`/`https://` string (never
   fetched).
3. Each uploaded document's bytes are hashed (`bytes_sha256`, same helper
   `interview_expression.media.MediaInspector` uses) and stored under
   `CA_MEDIA_ROOT`, mirroring `api/services/media_store.py::save_upload`'s
   pattern but writing to a `composer/` subtree so Composer never shares a
   collision domain with interview media.
4. `ResearchService.create_package()` builds and stores a
   `guest_research_package` object, keyed by the caller's `Idempotency-Key`.
5. Response: `research_package_id`, `revision`, `guest_name`, `source_urls`,
   `uploaded_documents` (asset summaries only), `idempotent_replay`.

### 5.4 `POST /api/interviews/compose/brief` workflow

1. Router receives a JSON body: `research_package_id`, `brand_context_ref`,
   `voice_dna_ref`, `guest_name`, `tension_hypothesis`,
   `matrix_of_edging_seed` (7 free-text fields matching AIR's own
   `matrix_of_edging` vocabulary), `planned_questions` (each with `text` and
   `target_branch_condition`), `expression_targets`, and the standard
   `composer_authority` block (`operator_id`, `authority_scope`,
   `assertion_id`).
2. `BriefService` first confirms `research_package_id` resolves to a real,
   stored `guest_research_package` in Composer's own repository (404 if not).
3. `composer_air_bridge.resolve_brand_voice_refs(air, brand_context_ref,
   voice_dna_ref)` cross-validates both refs against the real, live
   `AirApplication.repository` (via `require_air_ref`, file 27), and confirms
   the supplied `voice_dna_ref` actually belongs to the supplied
   `brand_context_ref` (an extra integrity check this spec adds, mirroring
   `BrandService._require_brand`'s own pattern). Any failure --
   `ObjectNotFound`, wrong type, hash mismatch, or brand/voice mismatch --
   is a `422`/`404`, and **nothing is written**.
4. `BriefService.create_brief()` stores the `activative_interview_brief`
   object, with `content_origin: "operator_supplied"` fixed, and a
   `hypothesis_pipeline_status` block: `{"status":
   "BLOCKED_PENDING_GAP_007", "iac_ref": null, "planned_aip_ref": null,
   "arm_receipt_ref": null, "blocked_reason": "..."}` (Section 6).
5. Response includes the stored Brief plus a `planning_lineage_template`
   object: the same shape `validate_planning_lineage()` expects, with
   `state: "PRESENT_VERIFIED"` **omitted** (deliberately not claimed) and
   the two available real values (`brief_ref`) alongside explicit `null`s
   for the two that are not -- so a future GAP-007-resolving caller has the
   exact shape to fill in, never a guess.

### 5.5 `POST /api/interviews/compose/sessions` workflow

1. Router receives `brief_id`, an optional `recording_date`
   (`YYYY-MM-DD`), and the standard `composer_authority` block.
2. `SessionService` confirms `brief_id` resolves to a real, stored Brief.
3. Calls `air.phase9.compile_relationship_program(...)` unchanged (exact
   real signature captured in Section 7, Stage 9), obtaining a real
   `relationship_state_ref` and `progression_ref`.
4. Stores a `composer_session` object linking `brief_ref`,
   `relationship_state_ref`, `progression_ref`, `stage: "ENGAGED"`, and the
   caller-supplied `recording_date` (bookkeeping only -- no file exists yet).
5. Response mirrors the stored object.

## 6. Data models, contracts, and API surface

### 6.1 Domain payload shapes (Composer's own repository)

```python
# guest_research_package
{
    "research_package_id": "ic:research:<sha[:32]>",
    "version": "1.0.0",
    "workspace_id": str, "project_id": str,
    "guest_name": str,
    "source_urls": list[str],            # each "http://" or "https://", sorted, unique
    "uploaded_documents": [
        {"asset_id": str, "sha256": str, "bytes": int,
         "media_type": str, "original_filename": str}, ...
    ],
    "composer_authority": {"operator_id": str, "authority_scope": str,
                            "assertion_id": str},
    "created_at_utc": str,
}

# activative_interview_brief
{
    "brief_id": "ic:brief:<sha[:32]>",
    "version": "1.0.0",
    "research_package_ref": {"object_id": str, "version": str, "sha256": str},
    "brand_context_ref": {"object_id": str, "version": str, "sha256": str},
    "voice_dna_ref": {"object_id": str, "version": str, "sha256": str},
    "guest_name": str,
    "content_origin": "operator_supplied",   # closed enum, one member
    "tension_hypothesis": str,
    "matrix_of_edging_seed": {
        "broad_signal": str, "hidden_pressure": str, "surviving_edge": str,
        "identity_gap": str, "audience_reality": str,
        "desired_recognition": str, "smallest_useful_movement": str,
    },
    "planned_questions": [
        {"question_id": str, "text": str,
         "target_branch_condition":  # one of AIR's real 7 branches
             "ANCHOR_HIT" | "PARTIAL_HIT" | "DEFENSE" | "TOPIC_ESCAPE" |
             "CONTRADICTION" | "OVERLOAD" | "RELATIONAL_RESET",
         "rationale": str}, ...
    ],
    "expression_targets": list[str],
    "hypothesis_pipeline_status": {
        "status": "BLOCKED_PENDING_GAP_007",
        "iac_ref": None, "planned_aip_ref": None, "arm_receipt_ref": None,
        "blocked_reason": (
            "planned_activative_intelligence_pack requires real, "
            "cross-validated activation_hypothesis_portfolio / "
            "activation_hypothesis / matrix_of_edging / "
            "psychological_role_tension_contract objects "
            "(HypothesisService.store_planned_pack, AIR). See "
            "SPEC_GAP_LEDGER.md GAP-007."
        ),
    },
    "composer_authority": {...},
    "created_at_utc": str,
}

# composer_session
{
    "session_id": "ic:session:<sha[:32]>",
    "version": "1.0.0",
    "brief_ref": {"object_id": str, "version": str, "sha256": str},
    "relationship_state_ref": {"object_id": str, "version": str, "sha256": str},
    "progression_ref": {"object_id": str, "version": str, "sha256": str},
    "stage": "ENGAGED",
    "recording_date": str | None,
    "composer_authority": {...},
    "created_at_utc": str,
}
```

### 6.2 HTTP endpoints

| Method | Path | Status | Request | Response |
|---|---|---|---|---|
| `POST` | `/api/interviews/compose/research` | 201 | multipart form (see 5.3) | `GuestResearchPackageResponse` |
| `GET` | `/api/interviews/compose/research/{research_package_id}` | 200 | -- | `GuestResearchPackageResponse` |
| `POST` | `/api/interviews/compose/brief` | 201 | JSON body (see 5.4) | `ActivativeInterviewBriefResponse` |
| `GET` | `/api/interviews/compose/briefs/{brief_id}` | 200 | -- | `ActivativeInterviewBriefResponse` |
| `POST` | `/api/interviews/compose/sessions` | 201 | JSON body (see 5.5) | `ComposerSessionResponse` |
| `GET` | `/api/interviews/compose/sessions/{session_id}` | 200 | -- | `ComposerSessionResponse` |

All error responses use the shared `api/errors.py::ErrorResponse` envelope,
matching every other router in this gateway.

| Error code | Status | Cause |
|---|---|---|
| `VALIDATION_FAILED` | 422 | Malformed JSON body, bad URL, empty required field |
| `RESEARCH_PACKAGE_NOT_FOUND` | 404 | `research_package_id` does not resolve in Composer's own repository |
| `BRAND_CONTEXT_NOT_FOUND` | 404 | `brand_context_ref.object_id` does not resolve in AIR |
| `VOICE_DNA_NOT_FOUND` | 404 | `voice_dna_ref.object_id` does not resolve in AIR |
| `BRAND_VOICE_MISMATCH` | 422 | `voice_dna_ref` resolves, but its own `brand_context_ref` does not match the supplied `brand_context_ref` |
| `AIR_REF_TYPE_MISMATCH` | 422 | ref resolves to the wrong AIR object type or a stale hash |
| `BRIEF_NOT_FOUND` | 404 | `brief_id` does not resolve |
| `SESSION_NOT_FOUND` | 404 | `session_id` does not resolve |
| `CONFLICT` | 409 | idempotency key reused with a different payload |

### 6.3 Example: `POST /api/interviews/compose/brief` response (the honest core of this spec)

```json
{
  "brief_id": "ic:brief:9f2a...",
  "revision": 1,
  "research_package_ref": {"object_id": "ic:research:7e1c...", "version": "1.0.0", "sha256": "..."},
  "brand_context_ref": {"object_id": "brand-ctx-001", "version": "1.0.0", "sha256": "..."},
  "voice_dna_ref": {"object_id": "voice-dna-001", "version": "1.0.0", "sha256": "..."},
  "content_origin": "operator_supplied",
  "tension_hypothesis": "...",
  "matrix_of_edging_seed": { "broad_signal": "...", "...": "..." },
  "planned_questions": [
    {"question_id": "q1", "text": "...", "target_branch_condition": "ANCHOR_HIT", "rationale": "..."}
  ],
  "hypothesis_pipeline_status": {
    "status": "BLOCKED_PENDING_GAP_007",
    "iac_ref": null,
    "planned_aip_ref": null,
    "arm_receipt_ref": null,
    "blocked_reason": "planned_activative_intelligence_pack requires real, cross-validated ... See SPEC_GAP_LEDGER.md GAP-007."
  },
  "planning_lineage_template": {
    "brief_ref": {"object_id": "ic:brief:9f2a...", "version": "1.0.0", "sha256": "..."},
    "planned_aip_ref": null,
    "iac_ref": null,
    "arm_receipt_ref": null,
    "planned_object_digests": null
  },
  "idempotent_replay": false
}
```

No field here pretends to be something it is not. `planning_lineage_template`
is explicitly *not* `state: "PRESENT_VERIFIED"` and cannot, today, be posted
as-is to `/api/interviews/brief-led` -- that submission would correctly fail
`validate_planning_lineage()`'s `exact_keys` check (file 11), and it is
supposed to, until GAP-007 closes.

## 7. Implementation stages

### Stage 1 — Package skeleton: `services/interview-composer/`

`pyproject.toml` (mirrors file 18 exactly, renamed):

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "conscious-activations-interview-composer"
version = "0.1.0.dev1"
description = "Development-only Guest Research Package and Activative Interview Brief runtime."
readme = "README.md"
requires-python = ">=3.12"
dependencies = ["ca-contracts==0.1.0.dev1", "ca-runtime==0.1.0.dev1"]

[tool.setuptools]
package-dir = {"" = "src"}
include-package-data = true

[tool.setuptools.packages.find]
where = ["src"]
include = ["conscious_activations_interview_composer*"]

[tool.setuptools.package-data]
conscious_activations_interview_composer = ["migrations/*.sql", "py.typed"]
```

`src/conscious_activations_interview_composer/__init__.py`:

```python
"""Development-only Guest Research Package and Activative Interview Brief runtime."""

PRODUCT_ID = "interview-composer"
PRODUCT_VERSION = "0.1.0-dev.1"
PACKAGE_VERSION = "0.1.0.dev1"
AUTHORITY_STATE = "candidate_not_current"
__version__ = PACKAGE_VERSION
```

`errors.py` (same shape as file 15, `INT_*` → `IC_*`):

```python
class InterviewComposerError(RuntimeError):
    code = "IC_ERROR"
    def __init__(self, message: str, *, context: dict[str, object] | None = None):
        super().__init__(message)
        self.context = context or {}

class ValidationError(InterviewComposerError):
    code = "IC_VALIDATION_FAILED"

class ConflictError(InterviewComposerError):
    code = "IC_CONFLICT"

class NotFoundError(InterviewComposerError):
    code = "IC_NOT_FOUND"

class CrossReferenceError(InterviewComposerError):
    """Raised when a caller-supplied AIR ref (brand/voice) does not resolve,
    resolves to the wrong object type, or fails the brand/voice ownership
    check. Distinct from NotFoundError because the failing reference lives
    in a different repository than the one this module owns."""
    code = "IC_CROSS_REFERENCE_FAILED"
```

`canonical.py` — a deliberate, non-shared adaptation of file 12
(`require_string`, `require_int`, `require_sha`, `require_enum`,
`require_ref`, `exact_keys`, `semantic_id`, `sorted_unique_strings` copied
verbatim with `ValidationError` imported from this package's own
`errors.py`), plus one addition file 12 does not have:

```python
import re

URL_RE = re.compile(r"^https?://[^\s]+$")

def require_url(value: object, name: str) -> str:
    text = require_string(value, name)
    if not URL_RE.match(text):
        raise ValidationError(f"{name} must be a well-formed http(s) URL")
    return text
```

(`require_portable_uri` and `require_source_span` from file 12 are **not**
copied — Composer has no media spans or portable-URI concept; it stores
uploaded documents as plain content-addressed assets, one level simpler than
`interview_expression`'s.)

### Stage 2 — `migrations/0001_interview_composer.sql`

Adapted from file 13's migration (file-level pattern only; Composer has no
`ie_events`/`ie_session_snapshots` equivalent — no live event sourcing here):

```sql
CREATE TABLE IF NOT EXISTS ic_migrations(
  version INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  applied_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS ic_command_results(
  idempotency_key TEXT PRIMARY KEY,
  command_type TEXT NOT NULL,
  payload_sha256 TEXT NOT NULL,
  result_json TEXT NOT NULL,
  created_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS ic_objects(
  object_id TEXT NOT NULL,
  revision INTEGER NOT NULL,
  object_type TEXT NOT NULL,
  semantic_version TEXT NOT NULL,
  canonical_sha256 TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  authority_state TEXT NOT NULL,
  is_current INTEGER NOT NULL CHECK(is_current IN (0,1)),
  idempotency_key TEXT NOT NULL,
  created_at_utc TEXT NOT NULL,
  supersedes_revision INTEGER,
  PRIMARY KEY(object_id, revision)
);
CREATE UNIQUE INDEX IF NOT EXISTS ic_objects_one_current ON ic_objects(object_id) WHERE is_current=1;
CREATE TABLE IF NOT EXISTS ic_edges(
  parent_id TEXT NOT NULL,
  child_id TEXT NOT NULL,
  relation TEXT NOT NULL,
  PRIMARY KEY(parent_id, child_id, relation)
);
```

### Stage 3 — `repository.py`

Structurally identical to file 13 with `ie_` → `ic_` table names and
`InterviewComposerRepository`/`ConflictError`/`NotFoundError` imported from
this package's own `errors.py`; `foundation_database()` uses
`PRODUCT_ID = "interview-composer"`. `execute_idempotent`, `store_object`,
`get_object`, `list_objects`, `add_edge` are reused verbatim (no
`append_event`/`latest_snapshot` — this spec has no live session state to
event-source).

### Stage 4 — `domain.py`

```python
from __future__ import annotations
from collections.abc import Mapping
from typing import Any
from .canonical import (exact_keys, require_ref, require_string, require_url,
                          semantic_id, sorted_unique_strings)
from .errors import ValidationError

BRANCH_CONDITIONS = {
    "ANCHOR_HIT", "PARTIAL_HIT", "DEFENSE", "TOPIC_ESCAPE",
    "CONTRADICTION", "OVERLOAD", "RELATIONAL_RESET",
}  # matches phase9_domain.py's branch_program vocabulary exactly (file 22)

MATRIX_SEED_FIELDS = (
    "broad_signal", "hidden_pressure", "surviving_edge", "identity_gap",
    "audience_reality", "desired_recognition", "smallest_useful_movement",
)  # matches cmf_activative_intelligence.domain._validate_matrix (file 20)


def make_guest_research_package(*, workspace_id: str, project_id: str,
                                 guest_name: str, source_urls: list[str],
                                 uploaded_documents: list[Mapping[str, Any]],
                                 composer_authority: Mapping[str, str]) -> dict[str, Any]:
    core = {
        "workspace_id": require_string(workspace_id, "workspace_id"),
        "project_id": require_string(project_id, "project_id"),
        "guest_name": require_string(guest_name, "guest_name"),
        "source_urls": sorted_unique_strings(
            [require_url(u, "source_urls[]") for u in source_urls] or [""],
            "source_urls",
        ) if source_urls else [],
        "uploaded_documents": list(uploaded_documents),
        "composer_authority": dict(composer_authority),
    }
    core["research_package_id"] = semantic_id("ic:research", core)
    return core


def make_activative_interview_brief(*, research_package_ref: Mapping[str, str],
                                     brand_context_ref: Mapping[str, str],
                                     voice_dna_ref: Mapping[str, str],
                                     guest_name: str, tension_hypothesis: str,
                                     matrix_of_edging_seed: Mapping[str, str],
                                     planned_questions: list[Mapping[str, Any]],
                                     expression_targets: list[str],
                                     composer_authority: Mapping[str, str]) -> dict[str, Any]:
    seed = {f: require_string(matrix_of_edging_seed.get(f), f"matrix_of_edging_seed.{f}")
            for f in MATRIX_SEED_FIELDS}
    exact_keys(matrix_of_edging_seed, set(MATRIX_SEED_FIELDS), "matrix_of_edging_seed")
    questions = []
    for i, q in enumerate(planned_questions):
        branch = q.get("target_branch_condition")
        if branch not in BRANCH_CONDITIONS:
            raise ValidationError(f"planned_questions[{i}].target_branch_condition must be one of {sorted(BRANCH_CONDITIONS)}")
        questions.append({
            "question_id": require_string(q.get("question_id"), f"planned_questions[{i}].question_id"),
            "text": require_string(q.get("text"), f"planned_questions[{i}].text"),
            "target_branch_condition": branch,
            "rationale": require_string(q.get("rationale"), f"planned_questions[{i}].rationale"),
        })
    if not questions:
        raise ValidationError("planned_questions must contain at least one question")
    core = {
        "research_package_ref": require_ref(research_package_ref, "research_package_ref"),
        "brand_context_ref": require_ref(brand_context_ref, "brand_context_ref"),
        "voice_dna_ref": require_ref(voice_dna_ref, "voice_dna_ref"),
        "guest_name": require_string(guest_name, "guest_name"),
        "content_origin": "operator_supplied",
        "tension_hypothesis": require_string(tension_hypothesis, "tension_hypothesis"),
        "matrix_of_edging_seed": seed,
        "planned_questions": questions,
        "expression_targets": [require_string(t, "expression_targets[]") for t in expression_targets],
        "hypothesis_pipeline_status": {
            "status": "BLOCKED_PENDING_GAP_007",
            "iac_ref": None, "planned_aip_ref": None, "arm_receipt_ref": None,
            "blocked_reason": (
                "planned_activative_intelligence_pack requires real, "
                "cross-validated activation_hypothesis_portfolio / "
                "activation_hypothesis / matrix_of_edging / "
                "psychological_role_tension_contract objects "
                "(HypothesisService.store_planned_pack, AIR). See "
                "SPEC_GAP_LEDGER.md GAP-007."
            ),
        },
        "composer_authority": dict(composer_authority),
    }
    core["brief_id"] = semantic_id("ic:brief", core)
    return core


def make_composer_session(*, brief_ref: Mapping[str, str],
                           relationship_state_ref: Mapping[str, str],
                           progression_ref: Mapping[str, str],
                           recording_date: str | None,
                           composer_authority: Mapping[str, str]) -> dict[str, Any]:
    core = {
        "brief_ref": require_ref(brief_ref, "brief_ref"),
        "relationship_state_ref": require_ref(relationship_state_ref, "relationship_state_ref"),
        "progression_ref": require_ref(progression_ref, "progression_ref"),
        "stage": "ENGAGED",
        "recording_date": recording_date,
        "composer_authority": dict(composer_authority),
    }
    core["session_id"] = semantic_id("ic:session", core)
    return core
```

### Stage 5 — `services/research_service.py`, `brief_service.py`, `session_service.py`

```python
# services/research_service.py
from __future__ import annotations
from typing import Any, Mapping
from ..domain import make_guest_research_package
from ..repository import InterviewComposerRepository

class ResearchService:
    def __init__(self, repository: InterviewComposerRepository):
        self.repository = repository

    def create_package(self, command: Mapping[str, Any], *, idempotency_key: str) -> dict[str, Any]:
        payload = make_guest_research_package(**command)
        return self.repository.store_object(
            "guest_research_package", payload,
            object_id=payload["research_package_id"], idempotency_key=idempotency_key,
        )
```

```python
# services/brief_service.py
from __future__ import annotations
from typing import Any, Mapping
from ..domain import make_activative_interview_brief
from ..errors import NotFoundError
from ..repository import InterviewComposerRepository

class BriefService:
    def __init__(self, repository: InterviewComposerRepository):
        self.repository = repository

    def create_brief(self, command: Mapping[str, Any], *, idempotency_key: str) -> dict[str, Any]:
        research_ref = command["research_package_ref"]
        try:
            self.repository.get_object(research_ref["object_id"])
        except NotFoundError:
            raise NotFoundError(f"no guest_research_package with id '{research_ref['object_id']}'") from None
        payload = make_activative_interview_brief(**command)
        result = self.repository.store_object(
            "activative_interview_brief", payload,
            object_id=payload["brief_id"], idempotency_key=idempotency_key,
        )
        self.repository.add_edge(payload["brief_id"], research_ref["object_id"], "researched_from")
        return result
```

```python
# services/session_service.py
from __future__ import annotations
from typing import Any, Mapping
from ..domain import make_composer_session
from ..errors import NotFoundError
from ..repository import InterviewComposerRepository

class SessionService:
    def __init__(self, repository: InterviewComposerRepository):
        self.repository = repository

    def create_session(self, *, brief_ref: Mapping[str, str],
                        relationship_state_ref: Mapping[str, str],
                        progression_ref: Mapping[str, str],
                        recording_date: str | None,
                        composer_authority: Mapping[str, str],
                        idempotency_key: str) -> dict[str, Any]:
        try:
            self.repository.get_object(brief_ref["object_id"])
        except NotFoundError:
            raise NotFoundError(f"no activative_interview_brief with id '{brief_ref['object_id']}'") from None
        payload = make_composer_session(
            brief_ref=brief_ref, relationship_state_ref=relationship_state_ref,
            progression_ref=progression_ref, recording_date=recording_date,
            composer_authority=composer_authority,
        )
        result = self.repository.store_object(
            "composer_session", payload,
            object_id=payload["session_id"], idempotency_key=idempotency_key,
        )
        self.repository.add_edge(payload["session_id"], brief_ref["object_id"], "schedules")
        return result
```

### Stage 6 — `application.py`, `bootstrap.py`, `AGENTS.md`

```python
# application.py
from __future__ import annotations
from pathlib import Path
from .repository import InterviewComposerRepository
from .services.research_service import ResearchService
from .services.brief_service import BriefService
from .services.session_service import SessionService

class InterviewComposerApplication:
    def __init__(self, database_path: str | Path | None = None):
        self.repository = InterviewComposerRepository(database_path)
        self.research = ResearchService(self.repository)
        self.briefs = BriefService(self.repository)
        self.sessions = SessionService(self.repository)
    def initialize(self): return self.repository.initialize()
```

```python
# bootstrap.py
from __future__ import annotations
from pathlib import Path
from .application import InterviewComposerApplication

def status(database_path: str | Path | None = None) -> dict[str, object]:
    return InterviewComposerApplication(database_path).repository.health()
```

`AGENTS.md`, following file 17's exact convention:

```markdown
# Agent Instructions — Interview Composer

Read `README.md` and the controlling `TS-APP-COMPOSER-*` specs before changes.

## Current boundary

Allowed:

- Guest Research Package storage (URLs and uploaded-document metadata only;
  never fetched, never parsed);
- Activative Interview Brief storage, with operator-supplied substantive
  content only;
- read-only cross-reference checks against the real AIR repository
  (`brand_context_version`, `voice_dna`);
- calling `Phase9ActivativeService.compile_relationship_program` unchanged;
- product-local contracts, persistence, tests.

Prohibited:

- writing to `services/air/` or `services/interview/` in any way;
- constructing `matrix_of_edging`, `activation_hypothesis`,
  `activation_hypothesis_portfolio`, or
  `psychological_role_tension_contract` objects (GAP-007 territory --
  belongs to a future AIR-scoped spec, not to this service);
- calling `POST /api/interviews/brief-led` or `/import`;
- fetching, scraping, OCR-ing, or summarizing any Guest Research URL or
  document;
- fabricating a ref (`iac_ref`, `planned_aip_ref`, `arm_receipt_ref`) that
  does not point to a real, already-stored object.
```

### Stage 7 — `api/schemas/interview_composer.py`

```python
from __future__ import annotations
from typing import Literal
from pydantic import BaseModel

class RefModel(BaseModel):
    object_id: str
    version: str
    sha256: str

class UploadedDocumentSummary(BaseModel):
    asset_id: str
    sha256: str
    bytes: int
    media_type: str
    original_filename: str

class GuestResearchPackageResponse(BaseModel):
    research_package_id: str
    revision: int
    guest_name: str
    source_urls: list[str]
    uploaded_documents: list[UploadedDocumentSummary]
    idempotent_replay: bool

class MatrixOfEdgingSeed(BaseModel):
    broad_signal: str
    hidden_pressure: str
    surviving_edge: str
    identity_gap: str
    audience_reality: str
    desired_recognition: str
    smallest_useful_movement: str

class PlannedQuestion(BaseModel):
    question_id: str
    text: str
    target_branch_condition: Literal[
        "ANCHOR_HIT", "PARTIAL_HIT", "DEFENSE", "TOPIC_ESCAPE",
        "CONTRADICTION", "OVERLOAD", "RELATIONAL_RESET",
    ]
    rationale: str

class HypothesisPipelineStatus(BaseModel):
    status: Literal["BLOCKED_PENDING_GAP_007"]
    iac_ref: RefModel | None
    planned_aip_ref: RefModel | None
    arm_receipt_ref: RefModel | None
    blocked_reason: str

class PlanningLineageTemplate(BaseModel):
    brief_ref: RefModel
    planned_aip_ref: RefModel | None
    iac_ref: RefModel | None
    arm_receipt_ref: RefModel | None
    planned_object_digests: dict[str, str] | None

class ComposeBriefRequest(BaseModel):
    research_package_id: str
    brand_context_ref: RefModel
    voice_dna_ref: RefModel
    guest_name: str
    tension_hypothesis: str
    matrix_of_edging_seed: MatrixOfEdgingSeed
    planned_questions: list[PlannedQuestion]
    expression_targets: list[str]
    operator_id: str
    authority_scope: str
    assertion_id: str

class ActivativeInterviewBriefResponse(BaseModel):
    brief_id: str
    revision: int
    research_package_ref: RefModel
    brand_context_ref: RefModel
    voice_dna_ref: RefModel
    guest_name: str
    content_origin: Literal["operator_supplied"]
    tension_hypothesis: str
    matrix_of_edging_seed: MatrixOfEdgingSeed
    planned_questions: list[PlannedQuestion]
    expression_targets: list[str]
    hypothesis_pipeline_status: HypothesisPipelineStatus
    planning_lineage_template: PlanningLineageTemplate
    idempotent_replay: bool

class ComposeSessionRequest(BaseModel):
    brief_id: str
    recording_date: str | None = None
    operator_id: str
    authority_scope: str
    assertion_id: str

class ComposerSessionResponse(BaseModel):
    session_id: str
    revision: int
    brief_ref: RefModel
    relationship_state_ref: RefModel
    progression_ref: RefModel
    stage: str
    recording_date: str | None
    idempotent_replay: bool
```

### Stage 8 — `api/services/composer_air_bridge.py`

```python
from __future__ import annotations
from typing import Mapping
from cmf_activative_intelligence.application import AirApplication
from cmf_activative_intelligence.repositories.air_repository import ObjectNotFound, StoredAirObject
from cmf_activative_intelligence.services.production_common import require_air_ref

class BrandCrossReferenceError(RuntimeError):
    def __init__(self, message: str, *, field: str):
        super().__init__(message)
        self.field = field

def resolve_brand_voice_refs(
    air: AirApplication, *, brand_context_ref: Mapping[str, str],
    voice_dna_ref: Mapping[str, str],
) -> tuple[StoredAirObject, StoredAirObject]:
    """Cross-validate operator-supplied Brand Context / Voice DNA refs
    against the real AIR repository. Never writes. Raises
    BrandCrossReferenceError -- never returns a placeholder -- on any
    failure, per Governing decision 3 (no fabricated refs)."""
    try:
        brand = require_air_ref(air.repository, brand_context_ref, object_types="brand_context_version")
    except ObjectNotFound as exc:
        raise BrandCrossReferenceError(
            f"brand_context_ref does not identify a stored brand_context_version: {exc}",
            field="brand_context_ref",
        ) from exc
    except ValueError as exc:
        raise BrandCrossReferenceError(str(exc), field="brand_context_ref") from exc

    try:
        voice = require_air_ref(air.repository, voice_dna_ref, object_types="voice_dna")
    except ObjectNotFound as exc:
        raise BrandCrossReferenceError(
            f"voice_dna_ref does not identify a stored voice_dna: {exc}",
            field="voice_dna_ref",
        ) from exc
    except ValueError as exc:
        raise BrandCrossReferenceError(str(exc), field="voice_dna_ref") from exc

    if voice.payload["brand_context_ref"]["object_id"] != brand.object_id:
        raise BrandCrossReferenceError(
            "voice_dna_ref does not belong to the supplied brand_context_ref",
            field="voice_dna_ref",
        )
    return brand, voice
```

### Stage 9 — `api/routers/interview_composer.py`

```python
from __future__ import annotations
import json
from fastapi import APIRouter, Depends, File, Form, Header, HTTPException, UploadFile
from ca_contracts import bytes_sha256, utc_now_rfc3339

from cmf_activative_intelligence.application import AirApplication
from conscious_activations_interview_composer.application import InterviewComposerApplication
from conscious_activations_interview_composer.errors import (
    ConflictError, InterviewComposerError, NotFoundError, ValidationError,
)

from api.config import load_config
from api.dependencies import get_air, get_composer
from api.errors import ErrorResponse
from api.schemas import interview_composer as schemas
from api.services.composer_air_bridge import BrandCrossReferenceError, resolve_brand_voice_refs
from api.services.media_store import save_upload  # reused unchanged; writes under a
                                                    # "composer/" media subtree by
                                                    # passing project_id="composer"

router = APIRouter()

_DOMAIN_ERROR_MAP = {
    ValidationError: (422, "VALIDATION_FAILED"),
    ConflictError: (409, "CONFLICT"),
    NotFoundError: (404, "NOT_FOUND"),
}

def _error(code: str, message: str, status: int) -> HTTPException:
    return HTTPException(status_code=status, detail=ErrorResponse(error_code=code, message=message, timestamp=utc_now_rfc3339()).model_dump())

def _domain_error_to_http(exc: InterviewComposerError) -> HTTPException:
    status_code, code = _DOMAIN_ERROR_MAP.get(type(exc), (500, "INTERNAL_ERROR"))
    return _error(code, str(exc), status_code)


@router.post("/research", status_code=201, response_model=schemas.GuestResearchPackageResponse)
async def create_research_package(
    guest_name: str = Form(...), source_urls_json: str = Form("[]"),
    workspace_id: str = Form(...), project_id: str = Form(...),
    operator_id: str = Form(...), authority_scope: str = Form(...), assertion_id: str = Form(...),
    documents: list[UploadFile] = File(default=[]),
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
    composer: InterviewComposerApplication = Depends(get_composer),
):
    try:
        source_urls = json.loads(source_urls_json)
    except json.JSONDecodeError as exc:
        raise _error("VALIDATION_FAILED", f"source_urls_json is not valid JSON: {exc}", 422) from exc
    config = load_config()
    uploaded = []
    for doc in documents:
        data = await doc.read()
        dest_path, logical_uri = save_upload(doc, media_root=config.ca_media_root, workspace_id=workspace_id, project_id="composer")
        uploaded.append({
            "asset_id": logical_uri, "sha256": bytes_sha256(data), "bytes": len(data),
            "media_type": doc.content_type or "application/octet-stream",
            "original_filename": doc.filename or "unnamed",
        })
    key = idempotency_key or f"research:{workspace_id}:{project_id}:{guest_name}"
    try:
        result = composer.research.create_package(
            {"workspace_id": workspace_id, "project_id": project_id, "guest_name": guest_name,
             "source_urls": source_urls, "uploaded_documents": uploaded,
             "composer_authority": {"operator_id": operator_id, "authority_scope": authority_scope, "assertion_id": assertion_id}},
            idempotency_key=key,
        )
    except InterviewComposerError as exc:
        raise _domain_error_to_http(exc) from exc
    payload = result["object"]["payload"]
    return schemas.GuestResearchPackageResponse(
        research_package_id=payload["research_package_id"], revision=result["object"]["revision"],
        guest_name=payload["guest_name"], source_urls=payload["source_urls"],
        uploaded_documents=payload["uploaded_documents"], idempotent_replay=result.get("idempotent_replay", False),
    )


@router.get("/research/{research_package_id}", response_model=schemas.GuestResearchPackageResponse)
def get_research_package(research_package_id: str, composer: InterviewComposerApplication = Depends(get_composer)):
    try:
        stored = composer.repository.get_object(research_package_id)
    except NotFoundError as exc:
        raise _error("NOT_FOUND", str(exc), 404) from exc
    payload = stored["payload"]
    return schemas.GuestResearchPackageResponse(
        research_package_id=payload["research_package_id"], revision=stored["revision"],
        guest_name=payload["guest_name"], source_urls=payload["source_urls"],
        uploaded_documents=payload["uploaded_documents"], idempotent_replay=False,
    )


@router.post("/brief", status_code=201, response_model=schemas.ActivativeInterviewBriefResponse)
def create_brief(
    body: schemas.ComposeBriefRequest,
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
    composer: InterviewComposerApplication = Depends(get_composer),
    air: AirApplication = Depends(get_air),
):
    try:
        research = composer.repository.get_object(body.research_package_id)
    except NotFoundError as exc:
        raise _error("RESEARCH_PACKAGE_NOT_FOUND", str(exc), 404) from exc
    try:
        resolve_brand_voice_refs(air, brand_context_ref=body.brand_context_ref.model_dump(), voice_dna_ref=body.voice_dna_ref.model_dump())
    except BrandCrossReferenceError as exc:
        code = "BRAND_VOICE_MISMATCH" if exc.field == "voice_dna_ref" and "belong" in str(exc) else \
               ("BRAND_CONTEXT_NOT_FOUND" if exc.field == "brand_context_ref" else "VOICE_DNA_NOT_FOUND")
        status = 422 if code == "BRAND_VOICE_MISMATCH" else 404
        raise _error(code, str(exc), status) from exc
    research_ref = {"object_id": research["object_id"], "version": research["version"], "sha256": research["sha256"]}
    key = idempotency_key or f"brief:{body.research_package_id}:{body.guest_name}"
    try:
        result = composer.briefs.create_brief(
            {"research_package_ref": research_ref, "brand_context_ref": body.brand_context_ref.model_dump(),
             "voice_dna_ref": body.voice_dna_ref.model_dump(), "guest_name": body.guest_name,
             "tension_hypothesis": body.tension_hypothesis,
             "matrix_of_edging_seed": body.matrix_of_edging_seed.model_dump(),
             "planned_questions": [q.model_dump() for q in body.planned_questions],
             "expression_targets": body.expression_targets,
             "composer_authority": {"operator_id": body.operator_id, "authority_scope": body.authority_scope, "assertion_id": body.assertion_id}},
            idempotency_key=key,
        )
    except InterviewComposerError as exc:
        raise _domain_error_to_http(exc) from exc
    return _brief_to_response(result)


def _brief_to_response(result: dict) -> schemas.ActivativeInterviewBriefResponse:
    payload = result["object"]["payload"]
    brief_ref = {"object_id": payload["brief_id"], "version": result["object"]["version"], "sha256": result["object"]["sha256"]}
    return schemas.ActivativeInterviewBriefResponse(
        brief_id=payload["brief_id"], revision=result["object"]["revision"],
        research_package_ref=payload["research_package_ref"], brand_context_ref=payload["brand_context_ref"],
        voice_dna_ref=payload["voice_dna_ref"], guest_name=payload["guest_name"],
        content_origin=payload["content_origin"], tension_hypothesis=payload["tension_hypothesis"],
        matrix_of_edging_seed=payload["matrix_of_edging_seed"], planned_questions=payload["planned_questions"],
        expression_targets=payload["expression_targets"], hypothesis_pipeline_status=payload["hypothesis_pipeline_status"],
        planning_lineage_template=schemas.PlanningLineageTemplate(
            brief_ref=brief_ref, planned_aip_ref=None, iac_ref=None, arm_receipt_ref=None, planned_object_digests=None,
        ),
        idempotent_replay=result.get("idempotent_replay", False),
    )


@router.get("/briefs/{brief_id}", response_model=schemas.ActivativeInterviewBriefResponse)
def get_brief(brief_id: str, composer: InterviewComposerApplication = Depends(get_composer)):
    try:
        stored = composer.repository.get_object(brief_id)
    except NotFoundError as exc:
        raise _error("BRIEF_NOT_FOUND", str(exc), 404) from exc
    return _brief_to_response({"object": stored, "idempotent_replay": False})


@router.post("/sessions", status_code=201, response_model=schemas.ComposerSessionResponse)
def create_session(
    body: schemas.ComposeSessionRequest,
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
    composer: InterviewComposerApplication = Depends(get_composer),
    air: AirApplication = Depends(get_air),
):
    try:
        brief = composer.repository.get_object(body.brief_id)
    except NotFoundError as exc:
        raise _error("BRIEF_NOT_FOUND", str(exc), 404) from exc
    brief_ref = {"object_id": brief["object_id"], "version": brief["version"], "sha256": brief["sha256"]}
    key = idempotency_key or f"session:{body.brief_id}"
    # See Stage 9a for the exact compile_relationship_program call.
    relationship_state_ref, progression_ref = _compile_relationship_program(air, brief=brief, body=body, idempotency_key=key)
    try:
        result = composer.sessions.create_session(
            brief_ref=brief_ref, relationship_state_ref=relationship_state_ref, progression_ref=progression_ref,
            recording_date=body.recording_date,
            composer_authority={"operator_id": body.operator_id, "authority_scope": body.authority_scope, "assertion_id": body.assertion_id},
            idempotency_key=key,
        )
    except InterviewComposerError as exc:
        raise _domain_error_to_http(exc) from exc
    payload = result["object"]["payload"]
    return schemas.ComposerSessionResponse(
        session_id=payload["session_id"], revision=result["object"]["revision"],
        brief_ref=payload["brief_ref"], relationship_state_ref=payload["relationship_state_ref"],
        progression_ref=payload["progression_ref"], stage=payload["stage"],
        recording_date=payload["recording_date"], idempotent_replay=result.get("idempotent_replay", False),
    )


@router.get("/sessions/{session_id}", response_model=schemas.ComposerSessionResponse)
def get_session(session_id: str, composer: InterviewComposerApplication = Depends(get_composer)):
    try:
        stored = composer.repository.get_object(session_id)
    except NotFoundError as exc:
        raise _error("SESSION_NOT_FOUND", str(exc), 404) from exc
    payload = stored["payload"]
    return schemas.ComposerSessionResponse(
        session_id=payload["session_id"], revision=stored["revision"],
        brief_ref=payload["brief_ref"], relationship_state_ref=payload["relationship_state_ref"],
        progression_ref=payload["progression_ref"], stage=payload["stage"],
        recording_date=payload["recording_date"], idempotent_replay=False,
    )
```

**Stage 9a — the exact `compile_relationship_program` call.** File 24's real
signature must be read directly from
`services/air/src/cmf_activative_intelligence/services/phase9_service.py`
before `_compile_relationship_program()` is implemented: this spec's authors
verified the method exists and produces `relationship_activation_state` (stage
`ENGAGED`) and `reelcast_progression_program` objects, but did not transcribe
every one of its keyword parameters into this document (the file is long and
several of its parameters -- e.g. `guest_ref`, `campaign_ref` -- are outside
what this spec's session-scheduling use case needs to supply meaningfully; an
implementer should call it with this spec's real `brief_ref` as its evidence
input and every other required parameter set to the smallest honestly-true
value the method accepts, exactly the way `tests/api/fixtures/
air_portfolio_fixture.py`'s `_budget()`/`_ref()` helpers construct minimal-but-
real AIR inputs elsewhere in this repository). This is flagged explicitly
rather than guessed at, per Governing decision 3.

### Stage 10 — `api/dependencies.py` and `api/main.py` (adapt)

`api/dependencies.py` — add:

```python
from conscious_activations_interview_composer.application import InterviewComposerApplication

def get_composer(request: Request) -> InterviewComposerApplication:
    return request.app.state.composer
```

`api/main.py` — inside `lifespan()`, after the existing `# Interview
Expression` block, add:

```python
    # Interview Composer (TS-APP-COMPOSER-001)
    from conscious_activations_interview_composer.application import InterviewComposerApplication
    composer = InterviewComposerApplication(database_path=db_path / "interview_composer.db")
    composer.initialize()
    app.state.composer = composer
    logger.info("interview composer service initialised: %s", db_path / "interview_composer.db")
```

And after the existing `interviews` router include:

```python
from api.routers import interview_composer
app.include_router(interview_composer.router, prefix="/api/interviews/compose", tags=["interview-composer"])
```

### Stage 11 — Frontend

`apps/web/src/api/http.ts` — additive only, `apiFetch` untouched:

```typescript
export async function apiFetchMultipart<T>(path: string, form: FormData, init?: RequestInit): Promise<T> {
  // Deliberately does not set Content-Type: the browser must set it (with
  // the multipart boundary) itself. See TS-APP-COMPOSER-001 Section 1,
  // Source gap notice B, for why apiFetch cannot be reused here.
  let response: Response;
  try {
    response = await fetch(`${BASE_URL}${path}`, { ...init, method: init?.method ?? "POST", body: form });
  } catch {
    throw new ApiError("Network request failed — is the gateway running?", null, null);
  }
  if (!response.ok) {
    let body: ErrorResponse | null = null;
    try { body = (await response.json()) as ErrorResponse; } catch { /* not JSON */ }
    throw new ApiError(body?.message ?? `Request failed with status ${response.status}`, response.status, body?.error_code ?? null, body?.service ?? null);
  }
  return (await response.json()) as T;
}
```

`apps/web/src/api/interviewComposer.ts`:

```typescript
import { apiFetch } from "./http";
import { apiFetchMultipart } from "./http";
import type {
  GuestResearchPackageResponse, ActivativeInterviewBriefResponse,
  ComposerSessionResponse, ComposeBriefInput, ComposeSessionInput,
} from "./types";

export interface CreateResearchPackageInput {
  guestName: string; sourceUrls: string[]; documents: File[];
  workspaceId: string; projectId: string;
  operatorId: string; authorityScope: string; assertionId: string;
}

export async function createResearchPackage(input: CreateResearchPackageInput): Promise<GuestResearchPackageResponse> {
  const form = new FormData();
  form.set("guest_name", input.guestName);
  form.set("source_urls_json", JSON.stringify(input.sourceUrls));
  form.set("workspace_id", input.workspaceId);
  form.set("project_id", input.projectId);
  form.set("operator_id", input.operatorId);
  form.set("authority_scope", input.authorityScope);
  form.set("assertion_id", input.assertionId);
  for (const doc of input.documents) form.append("documents", doc);
  return apiFetchMultipart<GuestResearchPackageResponse>("/api/interviews/compose/research", form);
}

export async function composeBrief(input: ComposeBriefInput): Promise<ActivativeInterviewBriefResponse> {
  return apiFetch<ActivativeInterviewBriefResponse>("/api/interviews/compose/brief", {
    method: "POST", body: JSON.stringify(input),
  });
}

export async function getBrief(briefId: string): Promise<ActivativeInterviewBriefResponse> {
  return apiFetch<ActivativeInterviewBriefResponse>(`/api/interviews/compose/briefs/${encodeURIComponent(briefId)}`);
}

export async function createComposerSession(input: ComposeSessionInput): Promise<ComposerSessionResponse> {
  return apiFetch<ComposerSessionResponse>("/api/interviews/compose/sessions", {
    method: "POST", body: JSON.stringify(input),
  });
}
```

`apps/web/src/api/types.ts` — additive block appended before the
`@ca/studio/domain` re-export (mirrors the shapes in Section 6.2 exactly;
omitted here to avoid repeating Stage 7's schema verbatim a third time).

Hooks (`apps/web/src/hooks/`), following file 33's exact `useMutation`/
`useQuery` shapes:

```typescript
// useCreateResearchPackage.ts
import { useMutation } from "@tanstack/react-query";
import { createResearchPackage } from "../api/interviewComposer";
import type { GuestResearchPackageResponse } from "../api/types";
import type { CreateResearchPackageInput } from "../api/interviewComposer";
import type { ApiError } from "../api/ApiError";

export function useCreateResearchPackage() {
  return useMutation<GuestResearchPackageResponse, ApiError, CreateResearchPackageInput>({
    mutationFn: createResearchPackage,
  });
}
```

(`useComposeBrief.ts`, `useBrief.ts`, `useCreateComposerSession.ts` follow
identically, wrapping `composeBrief`/`getBrief`/`createComposerSession`.)

Route file, replacing file 30 in full:

```tsx
import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { Card } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { ResearchPanel } from "../../components/interview-composer/ResearchPanel";
import { BriefPanel } from "../../components/interview-composer/BriefPanel";
import { PipelineStatusNotice } from "../../components/interview-composer/PipelineStatusNotice";

export function InterviewsComposePage() {
  const [researchPackageId, setResearchPackageId] = useState<string | null>(null);

  return (
    <div className="space-y-4 p-6" data-testid="interview-composer-page">
      <div className="flex items-center gap-2">
        <h1 className="text-xl font-semibold text-foreground">Interview Composer</h1>
        <Badge tone="muted">FR-APP-010..012</Badge>
      </div>
      <Card>
        <ResearchPanel onReady={setResearchPackageId} />
      </Card>
      {researchPackageId && (
        <Card>
          <BriefPanel researchPackageId={researchPackageId} />
        </Card>
      )}
      <PipelineStatusNotice />
    </div>
  );
}

export const Route = createFileRoute("/interviews/compose")({
  component: InterviewsComposePage,
});
```

`components/interview-composer/PipelineStatusNotice.tsx` — the component
that makes GAP-007 visible in the product itself, not just in this document:

```tsx
import { Card } from "../ui/Card";
import { Badge } from "../ui/Badge";

export function PipelineStatusNotice() {
  return (
    <Card className="border-dashed">
      <div className="flex items-start gap-2">
        <Badge tone="muted">Blocked</Badge>
        <p className="text-sm text-muted-foreground">
          Briefs created here are not yet eligible for Brief-led interview
          admission. Producing a real tension-hypothesis pipeline
          (<code>iac_ref</code>, <code>planned_aip_ref</code>,{" "}
          <code>arm_receipt_ref</code>) is tracked as GAP-007 in
          <code> SPEC_GAP_LEDGER.md</code> and is not part of this release.
        </p>
      </div>
    </Card>
  );
}
```

`ResearchPanel.tsx` and `BriefPanel.tsx` follow the exact form-state shape
`ImportInterviewPanel.tsx` (file 32) already establishes -- controlled
`useState` fields, a `<form onSubmit>` calling the corresponding hook's
`mutateAsync`, and `data-testid` attributes on every input -- built from
`components/ui/{Card,Textarea,Button,Badge}` rather than inline `<input>`
markup, per file 34's own stated intent. Full JSX bodies are omitted here to
keep this section within a reasonable length; their field lists are exactly
`CreateResearchPackageInput` and `ComposeBriefRequest` (Stage 7 /
Stage 11) respectively, with `MatrixOfEdgingSeed`'s seven fields as one
`<Textarea>` each and a repeatable `planned_questions` row editor mirroring
`OutputTargetsEditor.tsx`'s existing repeatable-row pattern.

### Stage 12 — `SPEC_GAP_LEDGER.md` amendment (this spec's own file change)

Append a new `## GAP-007` section, in the exact heading/field style GAP-001
through GAP-006 already use, stating:

- **Title:** No legitimate construction path exists for `planned_aip_ref` /
  `iac_ref` (pre-interview "planned" hypothesis pipeline).
- **Discovered by:** TS-APP-COMPOSER-001, while tracing
  `validate_planning_lineage()` (interview_expression) against
  `HypothesisService.store_planned_pack()` and
  `Phase9ActivativeService.compile_interview_asset_contract()` (AIR).
- **Evidence:** Section 1, Source gap notice A of this spec (file citations
  20-25 above).
- **Impact:** `POST /api/interviews/brief-led` (TS-APP-API-003) remains
  unreachable end-to-end through any real, non-fabricated caller. Entry
  Point A ("Engineered Interview") of the product's two documented entry
  points cannot be completed today.
- **Resolution:** a future, AIR-scoped spec defining a bounded "planned
  hypothesis pipeline" using AIR's own `research_synthesis`/
  `operator_supplied` `source_kind` vocabulary and `epistemic_state:
  planned`, consuming TS-APP-COMPOSER-001's `activative_interview_brief.
  matrix_of_edging_seed` and `.planned_questions` as its starting input.
- **Status:** OPEN as of this spec's authoring.

The ledger's closing "No specs remain to be written" line (accurate for the
GAP-001 through GAP-006 set it summarized) is updated to note that
TS-APP-COMPOSER-001 is now written, and that GAP-007 names the one
remaining piece of work neither this spec nor any prior spec closes.

## 8. Failure handling, migration, and observability

**Failure handling.** Every domain failure raised by
`conscious_activations_interview_composer` is a typed
`InterviewComposerError` subclass, mapped once, centrally, in
`api/routers/interview_composer.py::_domain_error_to_http`, the same
one-map-per-router shape every other router in this gateway already uses
(files 9, 10). Cross-repository failures (`BrandCrossReferenceError`) are
deliberately a *different* exception family from same-repository
`NotFoundError`, because they come from a different repository than the one
`InterviewComposerApplication` owns, and are mapped to distinct error codes
(`BRAND_CONTEXT_NOT_FOUND` / `VOICE_DNA_NOT_FOUND` / `BRAND_VOICE_MISMATCH`)
so an operator can tell "your research package id is wrong" apart from "the
Brand Context you picked doesn't exist yet."

**No writes on partial failure.** `create_brief()`'s router handler resolves
and validates `research_package_id` and both AIR refs *before* calling
`composer.briefs.create_brief(...)`; if either check fails, nothing is
written to Composer's own repository. There is no partially-created Brief
state to clean up.

**Migration and rollback.** This spec creates new tables in a new database
file (`interview_composer.db`); it does not alter any existing schema. There
is nothing to migrate or roll back in `services/air/` or
`services/interview/`. Deleting `interview_composer.db` and restarting the
gateway fully resets this spec's state with no effect on any other service,
the same recovery story every other product database in this repository
already has.

**Observability.** This spec adds no new observability infrastructure,
consistent with the rest of this repository (no metrics/tracing exists
anywhere in the current tree). `logger.info` lines at service-init time in
`api/main.py` (Stage 10) follow the exact pattern the five existing service
blocks already use.

**Degraded behavior.** If the AIR service fails to initialize at gateway
startup (an existing, pre-this-spec failure mode — see `api/main.py`'s
`air.initialize()`/`air.load_registries()` calls), `POST /api/interviews/
compose/brief` and `POST /api/interviews/compose/sessions` will fail at the
`Depends(get_air)` / cross-reference step with a `500`, the same way every
other AIR-touching route in this gateway already degrades; `POST /api/
interviews/compose/research` (which never touches AIR) is unaffected.

## 9. Acceptance criteria

- **AC-001 (Research package, URLs only).** Given a valid `guest_name`,
  `workspace_id`, `project_id`, `composer_authority` fields, and
  `source_urls_json` containing two well-formed URLs and no documents; when
  `POST /api/interviews/compose/research` is called; then the response is
  `201` with a `research_package_id`, the two URLs present verbatim, sorted,
  unique, and `uploaded_documents: []`.
- **AC-002 (Research package, URLs + uploaded document).** Given the same
  inputs as AC-001 plus one uploaded file; when the request is submitted as
  multipart form data; then the response includes one `uploaded_documents`
  entry whose `sha256` equals `bytes_sha256` of the uploaded bytes and whose
  `bytes` equals the file's length.
- **AC-003 (Brief with real, existing Brand DNA).** Given a stored research
  package (AC-001), and a `brand_context_ref`/`voice_dna_ref` pair seeded
  via `AirApplication.brand.store_brand_context`/`store_voice_dna` in the
  test fixture (mirroring file 25's fixture-seeding pattern) such that the
  voice_dna genuinely belongs to that brand context; when
  `POST /api/interviews/compose/brief` is called with valid
  `matrix_of_edging_seed` (all 7 fields), at least one `planned_questions`
  entry, and `expression_targets`; then the response is `201`,
  `content_origin: "operator_supplied"`, and `hypothesis_pipeline_status.
  status == "BLOCKED_PENDING_GAP_007"` with all three of `iac_ref`,
  `planned_aip_ref`, `arm_receipt_ref` explicitly `null`.
- **AC-004 (Brief against a non-existent Brand Context).** Given the same
  request as AC-003 but `brand_context_ref.object_id` does not resolve in
  AIR; when the endpoint is called; then the response is `404
  BRAND_CONTEXT_NOT_FOUND` and no `activative_interview_brief` object is
  stored (verified via a follow-up `GET` for the would-be `brief_id`
  returning `404`).
- **AC-005 (Brief against mismatched Voice DNA).** Given a real, stored
  `brand_context_version` A and a real, stored `voice_dna` that belongs to a
  *different* stored `brand_context_version` B; when
  `brand_context_ref` = A and `voice_dna_ref` = that voice_dna's ref are
  submitted together; then the response is `422 BRAND_VOICE_MISMATCH` and
  nothing is stored.
- **AC-006 (Brief against a non-existent research package).** Given a
  `research_package_id` that was never created; when
  `POST /api/interviews/compose/brief` is called; then the response is
  `404 RESEARCH_PACKAGE_NOT_FOUND`.
- **AC-007 (Idempotent replay).** Given a successfully created Brief; when
  the exact same request body and `Idempotency-Key` are submitted again;
  then the response is `201` with the same `brief_id` and
  `idempotent_replay: true`, and the underlying `ic_objects` row count for
  that `object_id` does not increase.
- **AC-008 (Conflicting idempotency key).** Given a successfully created
  research package under `Idempotency-Key: K`; when a *different* payload is
  submitted under the same key `K`; then the response is `409 CONFLICT`.
- **AC-009 (Session creation reuses real AIR data).** Given a stored Brief;
  when `POST /api/interviews/compose/sessions` is called with `brief_id`
  and a `recording_date`; then the response is `201` with `stage: "ENGAGED"`
  and `relationship_state_ref`/`progression_ref` whose `object_id`s resolve
  via `air.repository.get_object(...)` to real, stored
  `relationship_activation_state`/`reelcast_progression_program` objects.
- **AC-010 (Session against a non-existent brief).** Given a `brief_id` that
  was never created; when `POST /api/interviews/compose/sessions` is called;
  then the response is `404 BRIEF_NOT_FOUND`.
- **AC-011 (GET endpoints 404 correctly).** Given no object with a given id
  exists; when any of the three `GET` endpoints is called with that id; then
  the response is `404` with the matching `*_NOT_FOUND` error code.
- **AC-012 (Full regression).** Given the complete existing `tests/api/` and
  `tests/phase1` through `tests/phase9` suites; when they are run after this
  spec's changes land; then all previously-passing tests continue to pass
  unchanged (this spec adds files; it does not modify
  `services/air/`, `services/interview/`, or any existing router or schema
  file).
- **AC-013 (Composer output is honestly rejected by `/brief-led` today, and
  this is asserted, not hidden).** Given a Brief's
  `planning_lineage_template` from AC-003; when its fields are assembled
  into a `planning_lineage` object with `state: "PRESENT_VERIFIED"` forced
  and posted as `planning_lineage_json` to the real
  `POST /api/interviews/brief-led`; then the request fails --
  `exact_keys`/`require_ref` in `validate_planning_lineage()` reject the
  `None` values for `planned_aip_ref`/`iac_ref`/`arm_receipt_ref` with a
  `422 VALIDATION_FAILED`. This is a **regression test asserting the current,
  correct, honest boundary**, not a defect to fix in this spec -- it exists
  so that a future spec closing GAP-007 has a concrete, already-red test to
  turn green, and so nobody mistakes GAP-007 for silently resolved.
- **AC-014 (React page: research → brief → blocked-status flow is
  visible end-to-end).** Given the `InterviewComposer` page; when a user
  submits the research form and then the brief form with valid data; then
  the page displays the created `brief_id` and renders
  `PipelineStatusNotice`, which is present unconditionally (not just on
  error) so the GAP-007 boundary is visible on every successful Brief, not
  only failed ones.

## 10. Testing and completion evidence

**New test files:**

- `tests/interview_composer/test_repository.py`,
  `test_research_service.py`, `test_brief_service.py`,
  `test_session_service.py` -- unit tests against
  `InterviewComposerApplication` directly, no HTTP layer, mirroring
  `tests/phase4/`'s existing structure for `interview_expression`.
- `tests/api/test_interview_composer_research.py`,
  `test_interview_composer_brief.py`,
  `test_interview_composer_sessions.py` -- HTTP-layer tests using the shared
  `api_app` fixture (file "tests/api/conftest.py" row above) and
  `fastapi.testclient.TestClient`, covering AC-001 through AC-013. Brand/
  Voice DNA fixtures are seeded directly via `air.brand.store_brand_context`/
  `store_voice_dna` inside each test, following the exact minimal-real-object
  construction style `tests/api/fixtures/air_portfolio_fixture.py` already
  uses (its `AUTHORITY`/`_ref`/`_stored_ref` helpers, adapted).
- `apps/web/src/hooks/useCreateResearchPackage.test.ts`,
  `useComposeBrief.test.ts`, `useCreateComposerSession.test.ts` -- following
  file 33's `vi.stubGlobal("fetch", ...)` pattern.
- `apps/web/src/components/interview-composer/ResearchPanel.test.tsx`,
  `BriefPanel.test.tsx`, `PipelineStatusNotice.test.tsx`.
- `apps/web/src/routes/interviews/compose.test.tsx` -- **replaces** the
  existing placeholder test (which only asserted the `PlaceholderPage`
  props); the new version asserts AC-014.

**Regression command:** the same full-suite command every prior spec in this
repository has used as its own completion gate (`pytest tests/` for Python,
the existing `apps/web` test script for the frontend) — this spec adds no
new test runner and changes no existing test-invocation configuration.

**Claim ceiling: `INTERVIEW_COMPOSER_INTEGRATION_SURFACE_EVIDENCE`.**

This spec's Build Receipt, once implemented and audited, may claim:

- Guest Research Package creation, storage, and retrieval (FR-APP-010) --
  fully, honestly, with no fetching or summarization of URLs/documents.
- Brand Context Version / Voice DNA cross-referencing against real,
  currently-stored AIR objects, with no fabricated refs ever accepted
  (part of FR-APP-011).
- Operator-authored Activative Interview Brief storage, content-addressed
  and idempotent (part of FR-APP-011).
- Session/relationship-stage tracking reusing real AIR compilation
  (part of FR-APP-012, `ENGAGED` stage only).
- A real `InterviewComposer` page replacing the placeholder.

This spec's Build Receipt **must not** claim:

- That FR-APP-011's "the system generates ... tension hypothesis, Matrix of
  Edging seed" language is satisfied by system-side reasoning -- it is not;
  all substantive Brief content is operator-authored, and
  `content_origin` says so in every stored object.
- That FR-APP-012's "transition the Brief into a live Canonical Interview
  Source Package upon upload" is implemented -- it is not; that remains a
  separate, later operator action against the unmodified
  `POST /api/interviews/brief-led`.
- That FR-APP-020 (Brief-led interview admission) is reachable end-to-end
  through this spec's output. It is not, and AC-013 exists specifically to
  keep that fact enforced by a running test rather than by prose alone.
- That GAP-007 is resolved. It is not; it is named, evidenced, and handed
  off, in the same spirit `SPEC_GAP_LEDGER.md` already treats GAP-001
  through GAP-006.

---

*End of TS-APP-COMPOSER-001. This is the last spec named in
`CA_APP_FR_EPIC_SPEC_PLAN.md`'s Wave structure. It does not close the
product's Entry Point A end-to-end -- GAP-007, cataloged in Section 7 Stage
12 and inherited by `SPEC_GAP_LEDGER.md`, is the honest reason why, and is
the correct next spec for this program, not a fifth wave of this one.*
