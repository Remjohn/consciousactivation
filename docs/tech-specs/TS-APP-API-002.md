---
spec_id: TS-APP-API-002
title: Harness Library API
document_class: TECH_SPEC
product: Conscious Activations
module: api
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CURRENT
build_authority: false
controlling_frs:
  - FR-APP-040 (harness library browsing)
  - FR-APP-041 (harness selection for campaign)
  - FR-APP-042 (harness creation via Pi Coding Agent)
controlling_stories:
  - ST-APP-06.01 (browse available Harnesses — fully specified in CA_APP_FR_EPIC_SPEC_PLAN.md Part 3)
  - ST-APP-06.02 (Pi Coding Agent builds a Harness — NOT detailed in Part 3; derived here directly from FR-APP-042)
  - ST-APP-06.03 (select/validate a Harness for a campaign — NOT detailed in Part 3; derived here directly from FR-APP-041)
upstream_dependencies:
  - CA_PROJECT_SNAPSHOT_V2.md (authority — CURRENT)
  - CA_APP_FR_EPIC_SPEC_PLAN.md (authority — CURRENT)
  - TS-APP-API-001.md (build prerequisite — gateway, config, dependency wiring, error contract; AC-006 must already pass)
downstream_consumers:
  - TS-APP-API-004 (Campaign CRUD — needs harness_id selection and compatibility check)
  - TS-APP-API-005 (Pipeline Status — needs a Harness workflow structure; currently BLOCKED, see Source Gap 4)
  - TS-APP-UI-004 (Harness Library UI)
output_path: api/routers/harnesses.py (and supporting files listed in section 7)
wave: 1
---

# TS-APP-API-002 — Harness Library API

## 1. Files and Authorities Read

| File | SHA-256 (short) | Status | Fact extracted |
|---|---|---|---|
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/application/productization_service.py` | `76bb1d59` | READ — CURRENT IMPLEMENTATION | `BuilderProductizationService.execute()` only supports commands `ingest`, `build`, `inspect`, `export`; there is no `list` command |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/application/productization_contracts.py` | `1ef2fc13` | READ — CURRENT IMPLEMENTATION | `ProductizationErrorCode` enum and `ProductizationCommandRequest`/`Result` are the exact shapes the CLI and this API must both wrap |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/application/manifest_parser.py` | `aa9404c7` | READ — CURRENT IMPLEMENTATION | Operator manifest JSON schema: root fields `manifest_id, manifest_version, task_id, mode, task` (+ `category_id, activative_input` when `mode="activative"`); rejects unknown fields, forbidden claim keys, and BOM |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/operator_manifest.py` | `67945326` | READ — CURRENT IMPLEMENTATION | `task` object requires exactly `goal, success_condition, atomic_boundary, input_contract, output_contract, required_context, capability_requirements, acceptance_tests, authority_ref, provenance_refs` |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/application/export_service.py` | `930bfbac` | READ — CURRENT IMPLEMENTATION | `PortableAtomicHarnessCompiler.compile()` builds the definition via `CategoryBinding.create(...)`; `DeterministicPortableExportService.export()` writes a 4-file deterministic ZIP (`atomic_harness_definition.json`, `package_manifest.json`, `export_receipt.json`, `SHA256SUMS`) using atomic temp-file-then-`os.replace` |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/portable_export.py` | `30350ca3` | READ — CURRENT IMPLEMENTATION | Exact field set of the `definition` object inside `atomic_harness_definition.json`; `PortableAtomicHarnessDefinition.from_payload_bytes()` is the safe parser for reading a package back |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/category_binding.py` | `05cc1e52` | READ — CURRENT IMPLEMENTATION | Five canonical categories: `short_form_edited_video, 2d_character_animation, carousels, supervisuals, conversational_activation_expression`; generic-mode `category_binding` collapses to `{applicability: NOT_APPLICABLE, basis, category_id: null}` |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/adapters/sqlite_productization_repository.py` | `bb373b41` | READ — CURRENT IMPLEMENTATION | `get_record(kind, id)` is the only read path — exact `(record_kind, record_id)` lookup. **No `list`, `scan`, or `query` method exists anywhere in this file.** |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/cli/bootstrap.py` | `ac782ece` | READ — CURRENT IMPLEMENTATION | `build_local_service(database_path)` is the only place `BuilderProductizationService` is correctly constructed: `repository=SQLiteProductizationRepository(db)`, `compiler=PortableAtomicHarnessCompiler()`, `exporter=DeterministicPortableExportService(repository)` |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/cli/commands.py`, `parser.py`, `exit_codes.py`, `output.py` | `91893369`, `7c467aef`, `e126b908`, `c52d55fa` | READ — CURRENT IMPLEMENTATION | CLI subcommands are exactly `ingest MANIFEST`, `build --artifact-id`, `inspect --artifact-id`, `export --artifact-id --output`; `CLIExitCode`↔`ProductizationErrorCode` mapping used as the basis for this spec's HTTP status mapping |
| `01_ATOMIC_HARNESS_BUILDER/pyproject.toml` | `ede097dc` | READ — CURRENT | Package name `atomic-harness-builder`, CLI entry `cmf-builder`, env var `CMF_BUILDER_DB` for the SQLite path |
| `01_ATOMIC_HARNESS_BUILDER/tests/productization/integration/test_local_cli_subprocess.py` | READ | READ — CURRENT | Confirms the real chain: `ingest` returns `artifact_id = manifest_id`; `build --artifact-id <manifest_id>` returns `artifact_id = definition_id`; `export --artifact-id <definition_id> --output <path>` writes the ZIP |
| `01_ATOMIC_HARNESS_BUILDER/tests/fixtures/productization/manifests/generic_text_summary.json`, `activative_expression.json` | READ | READ — CURRENT FIXTURE | Used verbatim as the positive examples in section 6 |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/intake/definition_intake.py` | `5c5cf0b5` | READ — CURRENT IMPLEMENTATION | `AtomicHarnessDefinitionIntake.REQUIRED_KEYS` expects a *different* flat schema (`definition_id, definition_version, category_id, profile_id, purpose, semantic_dependencies, capabilities, workflow{nodes,edges}, evaluation_requirements, repair_laws, wrong_reading_locks, production_ready, certified, invalidation_state`) than what the Builder exports |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/bindings/eligibility_registry.py` | `4dfeca27` | READ — CURRENT IMPLEMENTATION | `ImplementationEligibilityRegistry` registers *Programmed Model implementation candidates* by `capability_id`; it has nothing to do with Harness-to-source-package category compatibility |

### Source gap notices (read carefully — these govern this spec's design)

**Gap 1 — No listing capability anywhere in the Builder stack.** Neither `SQLiteProductizationRepository` nor `BuilderProductizationService` nor the CLI can enumerate stored artifacts; every read requires an exact `record_id` the caller already knows. `GET /api/harnesses` therefore **cannot** be served by querying the Builder's SQLite store. This spec follows the approach the Epic Plan itself already anticipated for ST-APP-06.01 ("scan Harness library directory, parse each ZIP manifest"): the harness library is a plain filesystem directory of exported portable ZIP packages, and this spec adds new, additive scanning/parsing code in the `api/` layer — not a modification to `cmf_builder`.

**Gap 2 — `BuilderProductizationService` cannot be constructed with zero arguments.** TS-APP-API-001 §7 Stage 3 instantiates `app.state.builder = BuilderProductizationService()`. The real constructor (see `cli/bootstrap.py:build_local_service`) requires `repository`, `compiler`, and `exporter`. This is a defect in Wave 1's own foundation output, and it blocks every route in this spec. §7 Stage 0 below is a corrective patch to `api/main.py` that fixes this wiring. It is in scope for this spec because the harnesses router cannot function against an incorrectly constructed service object, and this spec is the first consumer of `get_builder()`.

**Gap 3 — No existing code performs the FR-APP-041 compatibility check.** The Epic Plan cites `cmf_pipeline/bindings/eligibility_registry.py` as the existing code for "validates that the Harness is compatible with the source package category," but that module is about Programmed Model implementation eligibility by capability, not Harness↔category compatibility. This spec implements the check net-new, entirely in the API layer, by comparing the exported definition's `category_binding.category_id` against a caller-supplied `source_category`.

**Gap 4 — Builder output and Pipeline input are structurally incompatible (blocking risk, not fixed here).** `PortableAtomicHarnessDefinition.content` (what this spec's `POST /api/harnesses/build` produces) and `AtomicHarnessDefinitionIntake.REQUIRED_KEYS` (what the Pipeline will need to ingest a Harness in TS-APP-API-004/005) share almost no field names. The Builder's package has no `profile_id`, no `workflow.nodes/edges`, no `capabilities[]` in the Pipeline's shape, and nests category under `category_binding.category_id` instead of a flat `category_id`. **A Harness built and exported through this spec today cannot be ingested by the Pipeline as-is.** Reconciling the two schemas is a cross-service compiler/adapter concern outside `api/routers/harnesses.py`. This spec surfaces the exact `PortableAtomicHarnessDefinition` shape unchanged and flags this gap prominently; it does not attempt a translation layer, because translating one governed schema into another is a domain decision, not an HTTP-wrapping decision. **TS-APP-API-004/005 cannot claim harness execution readiness until this gap is closed by a dedicated spec.**

**Gap 5 — `AUTHORITY_REJECTED` is defined but never raised by the code path this spec wraps.** `application/harness_ir_commands.py`, `application/governed_command_surface.py`, and `application/authority.py::AuthorityService` implement a richer HarnessIR/atomicity/authority domain model that would raise `HarnessIRAuthorityRejected`, but none of it is wired to `BuilderProductizationService` and none of it has a CLI entrypoint. The CLI-operational (and therefore API-operational) constitutional check is limited to `CategoryBinding.create()` structural validation, which raises `CategoryBindingError` and is caught by `PortableAtomicHarnessCompiler.compile()` and re-raised as `ProductizationErrorCode.INVALID_MANIFEST`. This spec's error contract reflects what the code actually does, not the fuller claim in CA_PROJECT_SNAPSHOT_V2.md §5 ("validates against constitutional authority, builds HarnessIR").

---

## 2. Problem, User Outcome, Solution, and Scope

### Problem without this spec
An operator has no way to see what Harnesses exist before creating a Campaign — the only way to inspect a built AtomicHarnessDefinition today is to already know its exact `artifact_id` and run `cmf-builder inspect --artifact-id <id>` from a shell with repository access. The Pi Coding Agent has no HTTP surface to submit a new Harness definition; someone would have to hand-run `cmf-builder ingest` → `build` → `export` on a machine with the repo checked out. Campaign creation (TS-APP-API-004, not yet built) has no way to ask "is Harness X even eligible for a source package of category Y?" before launching a Pipeline run.

### User outcome
An operator opens the (future) Harness Library page and sees every AtomicHarnessDefinition package that has been exported into the shared library, with category, mode, capability requirements, and version. The Pi Coding Agent POSTs a governed operator manifest as a JSON body and, in one call, receives back an exported, portable AtomicHarnessDefinition already sitting in the library — no shell access to the Builder host required. Campaign creation can call one endpoint to find out whether a chosen Harness is eligible for a chosen source package's category before committing to a Pipeline run.

### Solution
`api/routers/harnesses.py` exposing four routes, backed by a new `api/harness_library.py` module that scans a filesystem directory of exported packages:

- `GET /api/harnesses` — list every package in the shared harness library directory
- `GET /api/harnesses/{definition_id}` — full detail for one package (library directory first, Builder's durable store as fallback for a built-but-not-yet-exported definition)
- `POST /api/harnesses/build` — accepts a governed operator manifest as the request body; chains `ingest` → `build` → `export` against the (correctly wired) `BuilderProductizationService`; writes the resulting ZIP into the library directory; returns the created definition's summary
- `GET /api/harnesses/{definition_id}/eligibility` — given a `source_category` query parameter, returns `ELIGIBLE` / `INELIGIBLE` / `NOT_APPLICABLE`

### In scope
- `api/harness_library.py` — filesystem scan, ZIP parsing, definition lookup by ID
- `api/routers/harnesses.py` — the four routes above, request/response Pydantic models, error mapping
- `api/config.py` — add `CA_HARNESS_LIBRARY_ROOT` (corrective addition, additive only)
- `api/main.py` — **corrective patch**: fix `BuilderProductizationService` construction (Gap 2), register `harnesses.router`
- `api/dependencies.py` — add `get_harness_library_root()`
- Copying the two existing test fixture manifests into `tests/api/fixtures/harnesses/` for use by this spec's own tests

### Out of scope
- Reconciling the Builder-export schema with the Pipeline-intake schema (Gap 4) — flagged as a blocking risk for TS-APP-API-004/005, not fixed here
- Wiring the richer HarnessIR/authority/atomicity command surface (`harness_ir_commands.py`, `governed_command_surface.py`) into either the CLI or this API — out of scope; the CLI-operational path is what this spec wraps
- Any modification to the `cmf_builder` or `cmf_pipeline` Python packages themselves
- Deleting or superseding Harness versions, or any Harness lifecycle state beyond "exists in the library"
- Authentication / authorization on any route (still deferred per CA_PROJECT_SNAPSHOT_V2.md)
- Campaign creation itself (TS-APP-API-004) — this spec only provides the eligibility check it will call

---

## 3. Governing Decisions and Constraints

**The harness library is a filesystem directory, not a database query.** `CA_HARNESS_LIBRARY_ROOT` (default `{CA_DATA_ROOT}/harness-library`) holds one `.zip` per exported `AtomicHarnessDefinition`, named `{definition_id}.zip`. `GET /api/harnesses` opens every `.zip` in that directory, reads `atomic_harness_definition.json` from inside it, and parses it with `PortableAtomicHarnessDefinition.from_payload_bytes()` — the same safe parser the Builder itself uses, so a corrupted or hand-edited package is rejected the same way the Builder would reject it, not silently trusted.

**`POST /api/harnesses/build` performs `ingest → build → export` as one synchronous HTTP call.** The CLI's three-step flow requires the caller to already know the intermediate `manifest_id` (returned by `ingest`) and `definition_id` (returned by `build`) before it can call `export`. A stateless HTTP client (the Pi Coding Agent) should not have to orchestrate that three-call round trip itself, retry-safety included. This route performs all three `service.execute()` calls inside a single request handler and returns one response. If any of the three steps fails, no partial package appears in the library directory — the export step's own atomic temp-file-then-`os.replace` guarantees this, and the ingest/build durable records that DID commit before a later failure are harmless: they are content-addressed and idempotent, so retrying the whole build is always safe (see AC-008).

**The Builder's `_ingest` command requires a filesystem path, not bytes.** `ProductizationCommandRequest.manifest_path` is a `Path`; `_ingest()` calls `path.read_bytes()`. `POST /api/harnesses/build` writes the JSON request body to a private `NamedTemporaryFile` before calling `service.execute(command="ingest", manifest_path=<tmp path>)`, and always deletes the temp file in a `finally` block — whether ingest succeeds or fails.

**Eligibility is a net-new, additive check (Gap 3).** `GET /api/harnesses/{id}/eligibility` compares `definition.category_binding.category_id` against the caller's `source_category` query parameter. A `generic`-mode Harness (no category) always returns `NOT_APPLICABLE`, never `ELIGIBLE` or `INELIGIBLE` — a category-neutral Harness is not "compatible," it is out of the question entirely.

**Definitions are read preferentially from the library, with the durable store as fallback.** `GET /api/harnesses/{id}` first looks for `{id}.zip` in the library directory (the common case — a fully built-and-exported Harness). If not found there, it falls back to `builder.execute(inspect, artifact_id=id)` against the durable store, so a definition that was `build`-ed but not yet `export`-ed (state that can only happen via direct CLI use outside this API, since this spec's own build route always exports) is still inspectable. If neither has it, `404 NOT_FOUND`.

**No canonical export timestamp exists.** `export_receipt.json` has no timestamp field (see `export_service.py::receipt_base`). `HarnessSummary.added_at` is populated from the `.zip` file's filesystem `mtime`, explicitly documented as non-authoritative and for display/sort ordering only — never used for any correctness decision.

**Claim ceiling:** `HARNESS_LIBRARY_API_DEVELOPMENT_EVIDENCE`. This spec does not claim Pipeline-execution readiness for any Harness it lists or builds (see Gap 4), constitutional-authority certification (see Gap 5), or production eligibility of any kind — every definition surfaced by this API already self-reports `production_eligible: false, certified: false`, and this spec's own responses echo those fields unmodified rather than upgrading them.

**No float in canonical responses**, RFC 3339 timestamps, following the same `ca_contracts` conventions TS-APP-API-001 established.

---

## 4. Current Brownfield Architecture

| Component | Path | Actual behaviour | Disposition | Reason |
|---|---|---|---|---|
| `BuilderProductizationService` | `services/builder/src/cmf_builder/application/productization_service.py` | `execute()` dispatches `ingest`/`build`/`inspect`/`export`; no listing | REUSE (via corrected construction) | Exactly the operations `POST /api/harnesses/build` and the durable-store fallback need |
| `SQLiteProductizationRepository` | `services/builder/src/cmf_builder/adapters/sqlite_productization_repository.py` | `get_record(kind, id)` exact lookup only | REUSE (indirect, via `builder.execute`) | Never queried directly by this spec's code — always through the service |
| `PortableAtomicHarnessCompiler` / `DeterministicPortableExportService` | `services/builder/src/cmf_builder/application/export_service.py` | Compiles + exports a deterministic 4-file ZIP | REUSE | Called by `builder.execute(command="build")` and `execute(command="export")`; not modified |
| `PortableAtomicHarnessDefinition` | `services/builder/src/cmf_builder/domain/portable_export.py` | Safe parse/validate of the `atomic_harness_definition.json` payload | REUSE | Imported directly by `api/harness_library.py` to parse packages read off disk |
| `CategoryBinding` | `services/builder/src/cmf_builder/domain/category_binding.py` | Five canonical categories; validated binding shape | REUSE (read-only) | `category_binding.category_id` is read from parsed definitions for the eligibility check; `CategoryBinding.create()` itself is never called by this spec — only by the Builder's own `build` command |
| `AtomicHarnessDefinitionIntake` | `services/pipeline/src/cmf_pipeline/intake/definition_intake.py` | Expects a structurally different flat schema | **FLAG — INCOMPATIBLE** | See Gap 4. Not called by this spec. Documented as a blocking risk for TS-APP-API-004/005 |
| `ImplementationEligibilityRegistry` | `services/pipeline/src/cmf_pipeline/bindings/eligibility_registry.py` | Programmed Model capability eligibility, unrelated concept | **FLAG — NOT APPLICABLE** | Epic Plan's citation for FR-APP-041 is incorrect; not called by this spec |
| `application/harness_ir_commands.py`, `application/governed_command_surface.py`, `application/authority.py` | `services/builder/src/cmf_builder/application/` | Richer HarnessIR/atomicity/authority development-time command surface | **NOT WIRED — OUT OF SCOPE** | No CLI entrypoint, not reachable from `BuilderProductizationService`; left untouched |
| `api/main.py` (from TS-APP-API-001) | `api/main.py` | `app.state.builder = BuilderProductizationService()` — will raise `TypeError` at startup | **DEFECT — PATCH IN THIS SPEC** | See Gap 2; corrected in §7 Stage 0 |

---

## 5. Proposed Architecture and Workflows

### Browse flow — `GET /api/harnesses`

```
Request
  → list every *.zip directly under CA_HARNESS_LIBRARY_ROOT (non-recursive)
  → for each file:
      open as zipfile, read "atomic_harness_definition.json"
      PortableAtomicHarnessDefinition.from_payload_bytes(bytes)
        success → project to HarnessSummary, include file mtime as added_at
        PortableDefinitionInvalid / BadZipFile / KeyError → skip this file,
          record a warning (definition_id unknown, file name logged);
          do not fail the whole request
  → sort by added_at descending, then definition_id ascending (stable order
    when many packages share a second-resolution mtime)
  → return 200 with the list (empty list, not 404, when the library is empty
    or the directory does not yet exist)
```

### Detail flow — `GET /api/harnesses/{definition_id}`

```
Request
  → does {CA_HARNESS_LIBRARY_ROOT}/{definition_id}.zip exist?
      yes → parse it exactly as in the browse flow → 200 HarnessDetail
      no  → call builder.execute(ProductizationCommandRequest(
              command="inspect", artifact_id=definition_id))
            PASS + record_kind == "atomic_harness_definition"
              → project builder's inspect payload to HarnessDetail → 200
            ProductizationError(NOT_FOUND)
              → 404 NOT_FOUND
            PASS + record_kind == "operator_manifest"
              → this id names an ingested-but-not-yet-built manifest, not a
                Harness → 404 NOT_FOUND (a manifest is not a Harness)
```

### Build flow — `POST /api/harnesses/build` (Pi Coding Agent)

```
Request body: raw operator manifest JSON (see §6 for schema + examples)
  → write body bytes to a private NamedTemporaryFile (see §3)
  → try:
      ingest_result = builder.execute(command="ingest", manifest_path=tmp)
        → manifest_id = ingest_result.artifact_id
      build_result  = builder.execute(command="build", artifact_id=manifest_id)
        → definition_id = build_result.artifact_id
      destination   = CA_HARNESS_LIBRARY_ROOT / f"{definition_id}.zip"
      export_result = builder.execute(command="export",
                                       artifact_id=definition_id,
                                       output_path=destination)
    finally:
      delete the temp file
  → any ProductizationError at any of the three steps → mapped HTTP error
    (see §6 error table); no package is left in the library on failure,
    because export is the last step and export itself is atomic
  → on success: read the just-written ZIP back with the same parser used by
    the browse/detail flows (proves the file that will be served on the next
    GET /api/harnesses call is exactly what was just built) → 201
```

### Eligibility flow — `GET /api/harnesses/{definition_id}/eligibility?source_category=...`

```
Request
  → resolve the definition exactly as in the detail flow (library, then
    durable-store fallback); 404 if neither has it
  → mode == "generic"
      → { status: "NOT_APPLICABLE", harness_category: null,
          reason: "Harness is category-neutral (generic mode)." }
  → mode == "activative"
      → harness_category = definition.category_binding.category_id
      → harness_category == source_category
          → { status: "ELIGIBLE", harness_category, reason: null }
      → else
          → { status: "INELIGIBLE", harness_category,
              reason: "Harness is bound to category '<harness_category>',
                       not '<source_category>'." }
  → 200 in every case (an ineligible match is a successful answer, not an
    error — the client decides what to do with it)
```

---

## 6. Data Models, Contracts, Schemas, and APIs

### Operator manifest — request body of `POST /api/harnesses/build`

Passed through unchanged to `OperatorManifestParser`; this spec does **not** re-implement its validation in Pydantic, to avoid two divergent copies of a governed schema. Root shape (generic mode):

```json
{
  "manifest_id": "operator-manifest-generic-summary",
  "manifest_version": "1.0.0",
  "task_id": "generic_text_summary_v1",
  "mode": "generic",
  "task": {
    "goal": "Summarize governed plain text without changing its stated meaning.",
    "success_condition": "Return one concise summary that preserves every declared constraint.",
    "atomic_boundary": "One UTF-8 source document becomes one UTF-8 summary document.",
    "input_contract": {"type": "object", "required": ["text"], "properties": {"text": {"type": "string", "minLength": 1}}},
    "output_contract": {"type": "object", "required": ["summary"], "properties": {"summary": {"type": "string", "minLength": 1}}},
    "required_context": ["source_text", "declared_constraints"],
    "capability_requirements": ["governed_text_read", "deterministic_contract_validation"],
    "acceptance_tests": ["summary_is_non_empty", "declared_constraints_are_preserved"],
    "authority_ref": "builder-prd@1.2#sha256:11445848904b61a72fbe500f6a184084e153419a2844243c0bca5f31ef87506c",
    "provenance_refs": ["operator-source@1.0.0#sha256:1111111111111111111111111111111111111111111111111111111111111111"]
  }
}
```

Root shape (activative mode) adds `category_id` (one of the five canonical categories) and `activative_input` with 18 required fields — full example is `tests/fixtures/productization/manifests/activative_expression.json`, reused verbatim by this spec's own test fixtures.

### `HarnessSummary` — item shape returned by `GET /api/harnesses`

```python
class HarnessSummary(BaseModel):
    definition_id: str
    definition_hash: str
    manifest_id: str
    manifest_version: str
    task_id: str
    mode: str                        # "generic" | "activative"
    category_id: str | None
    category_name: str | None
    classification: list[str]
    capability_requirements: list[str]
    production_ready: bool           # always False at this stage
    certified: bool                  # always False at this stage
    package_file: str                # "{definition_id}.zip"
    package_hash: str                # sha256 of the ZIP bytes on disk
    added_at: str | None             # RFC 3339, from file mtime — NON-AUTHORITATIVE
```

### `HarnessDetail` — `GET /api/harnesses/{id}` response, extends `HarnessSummary`

```python
class HarnessDetail(HarnessSummary):
    goal: str
    success_condition: str
    atomic_boundary: str
    input_contract: dict
    output_contract: dict
    minimum_complete_context: list[str]
    acceptance_tests: list[str]
    authority_chain: list[str]
    provenance_refs: list[str]
    execution_plan: list[str]
    category_binding: dict           # full CategoryBinding.canonical_dict(), or
                                      # {"applicability": "NOT_APPLICABLE", ...} for generic
    activative_intelligence: dict | None
    lineage: list[str]
    compiler_id: str
    compiler_version: str
    schema_id: str
    schema_version: str
```

### `BuildHarnessResponse` — `POST /api/harnesses/build` response

```python
class BuildHarnessResponse(BaseModel):
    definition_id: str
    definition_hash: str
    manifest_id: str
    manifest_version: str
    task_id: str
    mode: str
    category_id: str | None
    package_file: str
    package_hash: str
    ingest_receipt_id: str
    build_receipt_id: str
    export_receipt_id: str
```

### `EligibilityResponse` — `GET /api/harnesses/{id}/eligibility` response

```python
class EligibilityResponse(BaseModel):
    definition_id: str
    harness_category: str | None
    source_category: str
    status: str                      # "ELIGIBLE" | "INELIGIBLE" | "NOT_APPLICABLE"
    reason: str | None
```

### `ErrorResponse`

Reused unchanged from `api/errors.py` (TS-APP-API-001). No new fields.

### Endpoints defined in this spec

| Method | Path | Response | Error codes |
|---|---|---|---|
| `GET` | `/api/harnesses` | `list[HarnessSummary]` (200, always — empty list is not an error) | `LIBRARY_UNREADABLE` |
| `GET` | `/api/harnesses/{definition_id}` | `HarnessDetail` (200) | `NOT_FOUND` |
| `POST` | `/api/harnesses/build` | `BuildHarnessResponse` (201) | `INVALID_MANIFEST`, `INVALID_ACTIVATIVE_INPUT`, `CONFLICT`, `HASH_MISMATCH`, `EXPORT_REJECTED`, `INTERNAL_ERROR` |
| `GET` | `/api/harnesses/{definition_id}/eligibility?source_category=` | `EligibilityResponse` (200) | `NOT_FOUND`, `MISSING_QUERY_PARAM` |

### `ProductizationErrorCode` → HTTP status mapping used by this router

| `ProductizationErrorCode` | HTTP status | Notes |
|---|---|---|
| `INVALID_MANIFEST` | 400 | Malformed JSON, unknown/missing fields, forbidden claim keys, or a rejected `CategoryBinding` (see Gap 5 — surfaces here, not as `AUTHORITY_REJECTED`) |
| `INVALID_ACTIVATIVE_INPUT` | 400 | Activative-mode field set is wrong |
| `AUTHORITY_REJECTED` | 422 | Mapped defensively; **unreachable** in the code path this spec wraps (Gap 5) — kept in the table so the contract does not silently break if the richer authority surface is ever wired in later |
| `HASH_MISMATCH` | 500 | Stored bytes fail to reproduce their declared hash — storage-level, not the caller's fault |
| `NOT_FOUND` | 404 | Unknown `artifact_id` passed to `build`/`inspect`/`export` |
| `CONFLICT` | 409 | Same `manifest_id` re-ingested with **different** bytes (see AC-008 for the idempotent, *same*-bytes case, which is 201, not 409) |
| `STORAGE_INTEGRITY` | 500 | SQLite-level failure |
| `EXPORT_REJECTED` | 500 | Only reachable via the Builder's own injected-failure test hook; kept mapped for completeness |
| `INTERNAL_ERROR` | 500 | Unclassified |

Positive example — `GET /api/harnesses` with one generic and one activative package in the library:

```json
[
  {
    "definition_id": "atomic-harness-definition_7f2c...",
    "definition_hash": "sha256:7f2c...",
    "manifest_id": "operator-manifest-activative-expression",
    "manifest_version": "1.0.0",
    "task_id": "activative_expression_contract_v1",
    "mode": "activative",
    "category_id": "conversational_activation_expression",
    "category_name": "Conversational Activation / Human Expression",
    "classification": ["canonical_category_bound", "conversational_activation_expression", "activative_operator_manifest", "non_certified", "non_production"],
    "capability_requirements": ["activative_contract_validation", "lineage_preservation"],
    "production_ready": false,
    "certified": false,
    "package_file": "atomic-harness-definition_7f2c....zip",
    "package_hash": "sha256:9a11...",
    "added_at": "2026-07-25T18:03:11Z"
  },
  {
    "definition_id": "atomic-harness-definition_c410...",
    "definition_hash": "sha256:c410...",
    "manifest_id": "operator-manifest-generic-summary",
    "manifest_version": "1.0.0",
    "task_id": "generic_text_summary_v1",
    "mode": "generic",
    "category_id": null,
    "category_name": null,
    "classification": ["category_neutral", "generic_operator_manifest", "non_certified", "non_production"],
    "capability_requirements": ["governed_text_read", "deterministic_contract_validation"],
    "production_ready": false,
    "certified": false,
    "package_file": "atomic-harness-definition_c410....zip",
    "package_hash": "sha256:1b77...",
    "added_at": "2026-07-25T17:58:02Z"
  }
]
```

Negative example — `GET /api/harnesses/{id}/eligibility?source_category=carousels` for the activative package above:

```json
{
  "definition_id": "atomic-harness-definition_7f2c...",
  "harness_category": "conversational_activation_expression",
  "source_category": "carousels",
  "status": "INELIGIBLE",
  "reason": "Harness is bound to category 'conversational_activation_expression', not 'carousels'."
}
```

---

## 7. Implementation Stages and Exact Target Paths

All paths are relative to the repository root after the directory restructure described in CA_APP_FR_EPIC_SPEC_PLAN.md Part 5 has been applied (`services/builder/...`, not `01_ATOMIC_HARNESS_BUILDER/...`).

### Stage 0 — Corrective patch to TS-APP-API-001 output (Gap 2)

**`api/config.py`** — add one field:
```python
@dataclass(frozen=True)
class AppConfig:
    ca_data_root: Path
    ca_media_root: Path
    ca_delegation_root: Path
    ca_harness_library_root: Path      # NEW
    gateway_version: str = "0.1.0"

def load_config() -> AppConfig:
    data_root = Path(os.environ.get("CA_DATA_ROOT", "/state"))
    return AppConfig(
        ca_data_root=data_root,
        ca_media_root=Path(os.environ.get("CA_MEDIA_ROOT", data_root / "media")),
        ca_delegation_root=Path(
            os.environ.get("CA_DELEGATION_ROOT",
            Path(__file__).parent.parent / "packages" / "ca_delegation_rc4")
        ),
        ca_harness_library_root=Path(          # NEW
            os.environ.get("CA_HARNESS_LIBRARY_ROOT", data_root / "harness-library")
        ),
    )
```

**`api/main.py`** — replace the Builder construction line inside `lifespan()`:
```python
    # Builder — CORRECTED from TS-APP-API-001 (Gap 2): the zero-argument
    # construction there raises TypeError at startup. Wire it the same way
    # cli/bootstrap.py:build_local_service does.
    from cmf_builder.adapters.sqlite_productization_repository import (
        SQLiteProductizationRepository,
    )
    from cmf_builder.application.export_service import (
        DeterministicPortableExportService,
        PortableAtomicHarnessCompiler,
    )
    from cmf_builder.application.productization_service import BuilderProductizationService

    builder_db_path = db_path / "builder.sqlite3"
    builder_repository = SQLiteProductizationRepository(builder_db_path)
    builder = BuilderProductizationService(
        repository=builder_repository,
        compiler=PortableAtomicHarnessCompiler(),
        exporter=DeterministicPortableExportService(builder_repository),
    )
    app.state.builder = builder

    # Harness library directory — ensure it exists so a fresh deployment's
    # first GET /api/harnesses does not have to special-case a missing dir
    config.ca_harness_library_root.mkdir(parents=True, exist_ok=True)
```

**`api/dependencies.py`** — add:
```python
def get_harness_library_root(request: Request) -> Path:
    return request.app.state.config.ca_harness_library_root
```

### Stage 1 — Library scanning module

**`api/harness_library.py`**
```python
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import logging
import zipfile

from cmf_builder.domain.portable_export import (
    PortableAtomicHarnessDefinition,
    PortableDefinitionInvalid,
)

logger = logging.getLogger("ca.api.harness_library")

DEFINITION_ENTRY = "atomic_harness_definition.json"


@dataclass(frozen=True, slots=True)
class LibraryEntry:
    definition: PortableAtomicHarnessDefinition
    package_file: str
    package_hash: str
    added_at: str | None   # RFC 3339, from mtime — see governing decisions §3


def list_library(root: Path) -> list[LibraryEntry]:
    if not root.is_dir():
        return []
    entries: list[LibraryEntry] = []
    for path in sorted(root.glob("*.zip")):
        entry = _read_package(path)
        if entry is not None:
            entries.append(entry)
    entries.sort(key=lambda e: (e.added_at or "", e.definition.definition_id), reverse=True)
    return entries


def find_by_definition_id(root: Path, definition_id: str) -> LibraryEntry | None:
    path = root / f"{definition_id}.zip"
    if not path.is_file():
        return None
    return _read_package(path)


def _read_package(path: Path) -> LibraryEntry | None:
    try:
        archive_bytes = path.read_bytes()
        with zipfile.ZipFile(path) as archive:
            payload = archive.read(DEFINITION_ENTRY)
        definition = PortableAtomicHarnessDefinition.from_payload_bytes(payload)
    except (OSError, zipfile.BadZipFile, KeyError, PortableDefinitionInvalid) as error:
        logger.warning(
            "harness_library: skipping unreadable package file=%s error=%s",
            path.name, error,
        )
        return None
    mtime = path.stat().st_mtime
    added_at = datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return LibraryEntry(
        definition=definition,
        package_file=path.name,
        package_hash=f"sha256:{sha256(archive_bytes).hexdigest()}",
        added_at=added_at,
    )
```

### Stage 2 — Router

**`api/routers/harnesses.py`**
```python
from __future__ import annotations
from pathlib import Path
import tempfile

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ca_contracts import utc_now_rfc3339
from api.dependencies import get_builder, get_harness_library_root
from api.errors import ErrorResponse
from api.harness_library import LibraryEntry, find_by_definition_id, list_library
from cmf_builder.application.productization_contracts import (
    ProductizationCommandRequest,
    ProductizationError,
    ProductizationErrorCode,
)

router = APIRouter()

_STATUS_FOR_ERROR: dict[ProductizationErrorCode, int] = {
    ProductizationErrorCode.INVALID_MANIFEST: 400,
    ProductizationErrorCode.INVALID_ACTIVATIVE_INPUT: 400,
    ProductizationErrorCode.AUTHORITY_REJECTED: 422,
    ProductizationErrorCode.HASH_MISMATCH: 500,
    ProductizationErrorCode.NOT_FOUND: 404,
    ProductizationErrorCode.CONFLICT: 409,
    ProductizationErrorCode.STORAGE_INTEGRITY: 500,
    ProductizationErrorCode.EXPORT_REJECTED: 500,
    ProductizationErrorCode.INTERNAL_ERROR: 500,
}


class HarnessSummary(BaseModel):
    definition_id: str
    definition_hash: str
    manifest_id: str
    manifest_version: str
    task_id: str
    mode: str
    category_id: str | None
    category_name: str | None
    classification: list[str]
    capability_requirements: list[str]
    production_ready: bool
    certified: bool
    package_file: str
    package_hash: str
    added_at: str | None


class HarnessDetail(HarnessSummary):
    goal: str
    success_condition: str
    atomic_boundary: str
    input_contract: dict
    output_contract: dict
    minimum_complete_context: list[str]
    acceptance_tests: list[str]
    authority_chain: list[str]
    provenance_refs: list[str]
    execution_plan: list[str]
    category_binding: dict
    activative_intelligence: dict | None
    lineage: list[str]
    compiler_id: str
    compiler_version: str
    schema_id: str
    schema_version: str


class BuildHarnessResponse(BaseModel):
    definition_id: str
    definition_hash: str
    manifest_id: str
    manifest_version: str
    task_id: str
    mode: str
    category_id: str | None
    package_file: str
    package_hash: str
    ingest_receipt_id: str
    build_receipt_id: str
    export_receipt_id: str


class EligibilityResponse(BaseModel):
    definition_id: str
    harness_category: str | None
    source_category: str
    status: str
    reason: str | None


def _summary_from_entry(entry: LibraryEntry) -> HarnessSummary:
    content = entry.definition.content
    binding = content["category_binding"]
    return HarnessSummary(
        definition_id=entry.definition.definition_id,
        definition_hash=entry.definition.definition_hash,
        manifest_id=str(content["manifest_id"]),
        manifest_version=str(content["manifest_version"]),
        task_id=str(content["task_id"]),
        mode=str(content["mode"]),
        category_id=binding.get("category_id"),
        category_name=binding.get("category_name"),
        classification=list(content["classification"]),
        capability_requirements=list(content.get("capability_requirements") or []),
        production_ready=bool(content["production_eligible"]),
        certified=bool(content["certified"]),
        package_file=entry.package_file,
        package_hash=entry.package_hash,
        added_at=entry.added_at,
    )


def _detail_from_entry(entry: LibraryEntry) -> HarnessDetail:
    content = entry.definition.content
    summary = _summary_from_entry(entry)
    return HarnessDetail(
        **summary.model_dump(),
        goal=str(content["goal"]),
        success_condition=str(content["success_condition"]),
        atomic_boundary=str(content["atomic_boundary"]),
        input_contract=dict(content["input_contract"]),
        output_contract=dict(content["output_contract"]),
        minimum_complete_context=list(content["minimum_complete_context"]),
        acceptance_tests=list(content["acceptance_tests"]),
        authority_chain=list(content["authority_chain"]),
        provenance_refs=list(content["provenance_refs"]),
        execution_plan=list(content["execution_plan"]),
        category_binding=dict(content["category_binding"]),
        activative_intelligence=(
            dict(content["activative_intelligence"])
            if content["activative_intelligence"] is not None else None
        ),
        lineage=list(content["lineage"]),
        compiler_id=str(content["compiler_id"]),
        compiler_version=str(content["compiler_version"]),
        schema_id=str(content["schema_id"]),
        schema_version=str(content["schema_version"]),
    )


def _raise_for(error: ProductizationError) -> None:
    status_code = _STATUS_FOR_ERROR.get(error.code, 500)
    raise HTTPException(
        status_code=status_code,
        detail=ErrorResponse(
            error_code=error.code.value,
            message=str(error),
            timestamp=utc_now_rfc3339(),
        ).model_dump(),
    )


@router.get("", response_model=list[HarnessSummary])
def list_harnesses(library_root: Path = Depends(get_harness_library_root)):
    entries = list_library(library_root)
    return [_summary_from_entry(entry) for entry in entries]


@router.get("/{definition_id}", response_model=HarnessDetail)
def get_harness(
    definition_id: str,
    library_root: Path = Depends(get_harness_library_root),
    builder=Depends(get_builder),
):
    entry = find_by_definition_id(library_root, definition_id)
    if entry is not None:
        return _detail_from_entry(entry)
    try:
        result = builder.execute(
            ProductizationCommandRequest(command="inspect", artifact_id=definition_id)
        )
    except ProductizationError as error:
        _raise_for(error)
    if result.payload.get("record_kind") != "atomic_harness_definition":
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error_code="NOT_FOUND",
                message=f"No Harness with id '{definition_id}' exists.",
                timestamp=utc_now_rfc3339(),
            ).model_dump(),
        )
    artifact = result.payload["artifact"]["definition"]
    binding = artifact["category_binding"]
    return HarnessDetail(
        definition_id=result.artifact_id,
        definition_hash=result.artifact_hash,
        manifest_id=artifact["manifest_id"],
        manifest_version=artifact["manifest_version"],
        task_id=artifact["task_id"],
        mode=artifact["mode"],
        category_id=binding.get("category_id"),
        category_name=binding.get("category_name"),
        classification=artifact["classification"],
        capability_requirements=artifact.get("capability_requirements") or [],
        production_ready=artifact["production_eligible"],
        certified=artifact["certified"],
        package_file="",
        package_hash="",
        added_at=None,
        goal=artifact["goal"],
        success_condition=artifact["success_condition"],
        atomic_boundary=artifact["atomic_boundary"],
        input_contract=artifact["input_contract"],
        output_contract=artifact["output_contract"],
        minimum_complete_context=artifact["minimum_complete_context"],
        acceptance_tests=artifact["acceptance_tests"],
        authority_chain=artifact["authority_chain"],
        provenance_refs=artifact["provenance_refs"],
        execution_plan=artifact["execution_plan"],
        category_binding=binding,
        activative_intelligence=artifact["activative_intelligence"],
        lineage=artifact["lineage"],
        compiler_id=artifact["compiler_id"],
        compiler_version=artifact["compiler_version"],
        schema_id=artifact["schema_id"],
        schema_version=artifact["schema_version"],
    )


@router.post("/build", response_model=BuildHarnessResponse, status_code=201)
async def build_harness(
    request: Request,
    library_root: Path = Depends(get_harness_library_root),
    builder=Depends(get_builder),
):
    manifest_bytes = await request.body()
    tmp = tempfile.NamedTemporaryFile(
        suffix=".manifest.json", delete=False, dir=library_root.parent
    )
    tmp_path = Path(tmp.name)
    try:
        tmp.write(manifest_bytes)
        tmp.close()

        try:
            ingest_result = builder.execute(
                ProductizationCommandRequest(command="ingest", manifest_path=tmp_path)
            )
            build_result = builder.execute(
                ProductizationCommandRequest(
                    command="build", artifact_id=ingest_result.artifact_id
                )
            )
            library_root.mkdir(parents=True, exist_ok=True)
            destination = library_root / f"{build_result.artifact_id}.zip"
            export_result = builder.execute(
                ProductizationCommandRequest(
                    command="export",
                    artifact_id=build_result.artifact_id,
                    output_path=destination,
                )
            )
        except ProductizationError as error:
            _raise_for(error)
    finally:
        tmp_path.unlink(missing_ok=True)

    entry = find_by_definition_id(library_root, build_result.artifact_id)
    if entry is None:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error_code="INTERNAL_ERROR",
                message="Export reported success but the package is not readable.",
                timestamp=utc_now_rfc3339(),
            ).model_dump(),
        )
    content = entry.definition.content
    binding = content["category_binding"]
    return BuildHarnessResponse(
        definition_id=entry.definition.definition_id,
        definition_hash=entry.definition.definition_hash,
        manifest_id=str(content["manifest_id"]),
        manifest_version=str(content["manifest_version"]),
        task_id=str(content["task_id"]),
        mode=str(content["mode"]),
        category_id=binding.get("category_id"),
        package_file=entry.package_file,
        package_hash=entry.package_hash,
        ingest_receipt_id=ingest_result.receipt_id,
        build_receipt_id=build_result.receipt_id,
        export_receipt_id=export_result.receipt_id,
    )


@router.get("/{definition_id}/eligibility", response_model=EligibilityResponse)
def check_eligibility(
    definition_id: str,
    source_category: str = Query(..., min_length=1),
    library_root: Path = Depends(get_harness_library_root),
    builder=Depends(get_builder),
):
    detail = get_harness(definition_id, library_root=library_root, builder=builder)
    if detail.mode == "generic":
        return EligibilityResponse(
            definition_id=definition_id,
            harness_category=None,
            source_category=source_category,
            status="NOT_APPLICABLE",
            reason="Harness is category-neutral (generic mode); it has no category to match.",
        )
    harness_category = detail.category_binding.get("category_id")
    if harness_category == source_category:
        return EligibilityResponse(
            definition_id=definition_id,
            harness_category=harness_category,
            source_category=source_category,
            status="ELIGIBLE",
            reason=None,
        )
    return EligibilityResponse(
        definition_id=definition_id,
        harness_category=harness_category,
        source_category=source_category,
        status="INELIGIBLE",
        reason=(
            f"Harness is bound to category '{harness_category}', "
            f"not '{source_category}'."
        ),
    )
```

### Stage 3 — Register the router

**`api/main.py`** — replace the commented placeholder line with:
```python
from api.routers import harnesses
app.include_router(harnesses.router, prefix="/api/harnesses", tags=["harnesses"])
```

---

## 8. Failure, Migration, Rollback, Recovery, and Observability

### Typed failures

| Failure | Cause | Behaviour | Recovery |
|---|---|---|---|
| `LIBRARY_ROOT_UNREADABLE` | `CA_HARNESS_LIBRARY_ROOT` exists but is not a directory, or has no read permission | `list_library()` catches the `OSError` from `root.glob()`... — **note:** current implementation returns `[]` for a *missing* directory but will raise for a directory with bad permissions; router does not currently catch this at the route level | Add a `try/except OSError` around the `list_harnesses` route body, returning 500 `LIBRARY_UNREADABLE` — **flagged as a required addition during implementation, not covered by the code in §7** |
| Corrupt individual package | A `.zip` in the library is truncated, hand-edited, or has a hash mismatch | `_read_package()` catches `BadZipFile`/`KeyError`/`PortableDefinitionInvalid`, logs a warning, and excludes that one file; the rest of the listing still succeeds | Operator inspects the log, deletes or re-exports the offending file |
| `NOT_FOUND` on build's ingest step | Malformed manifest JSON body, unknown/missing fields | 400 `INVALID_MANIFEST` — never reaches the library | Caller fixes the manifest and re-POSTs |
| `CONFLICT` on build | Same `manifest_id` previously ingested with **different** canonical bytes | 409 `CONFLICT`; no package written | Caller must use a new `manifest_id` (or `manifest_version`) for a genuinely different manifest |
| Export step fails after ingest+build succeeded | Disk full, permission error, or (in tests only) the injected `inject_failure_before_replace()` hook | `export_service.py`'s own temp-file-then-`os.replace` never leaves a partial file at the final destination; the durable `operator_manifest` and `atomic_harness_definition` records DO remain committed (they are harmless, content-addressed, and re-usable) | Caller retries `POST /api/harnesses/build` with the identical manifest body; ingest and build are idempotent replays (AC-008), so only the export step actually re-runs |
| Detail lookup for an id that is only an `operator_manifest`, never built | Caller passes a manifest_id, not a definition_id, to `GET /api/harnesses/{id}` | 404 `NOT_FOUND` — a manifest is not a Harness | Caller uses the `definition_id` returned by a prior `build` call |

### Migration
This spec introduces the `CA_HARNESS_LIBRARY_ROOT` directory (created on startup by the Stage 0 patch if missing) and one new SQLite database file, `builder.sqlite3`, under `CA_DATA_ROOT` (previously the Builder had no database path configured at all, per Gap 2). No migration of existing data is required — `SQLiteProductizationRepository.initialize()` runs its own schema migration on first use, exactly as the other four services already do.

### Rollback
Removing `app.include_router(harnesses.router, ...)` from `api/main.py` fully disables this spec's routes. The Stage 0 corrective patch (fixing `BuilderProductizationService` construction) should **not** be rolled back independently — every other route that will eventually depend on `get_builder()` needs it fixed too. The harness library directory is read-only from every other service's perspective; deleting it is safe and just empties `GET /api/harnesses`.

### Observability
- Every skipped/corrupt package logs a `WARNING` via `logging.getLogger("ca.api.harness_library")`, including the filename (never the full parsed content, in case parsing itself is what failed)
- Every successful `POST /api/harnesses/build` should log an `INFO` line with `definition_id`, `manifest_id`, and all three receipt IDs (recommended addition during implementation; not shown as code above to keep §7 focused on request/response logic)
- `GET /api/harnesses` and `GET /api/harnesses/{id}` are read-only and idempotent; no additional audit trail is required beyond the uvicorn access log already established by TS-APP-API-001

---

## 9. Acceptance Criteria

**AC-001 — Empty library returns an empty list, not an error**
Given `CA_HARNESS_LIBRARY_ROOT` does not yet exist,
When `GET /api/harnesses` is called,
Then the response is HTTP 200 with body `[]`.
Failure example: 404 or 500 returned for a library that simply has nothing in it yet.
Evidence: response status and body.
Test layer: integration — `tests/api/test_harnesses.py::test_empty_library_returns_empty_list`.

**AC-002 — Building a generic-mode Harness makes it listable**
Given the server is running with an empty library,
When `POST /api/harnesses/build` is called with `tests/fixtures/productization/manifests/generic_text_summary.json` as the body,
Then the response is HTTP 201 with `mode: "generic"`, `category_id: null`, and a `definition_id` starting with `atomic-harness-definition_`,
And a subsequent `GET /api/harnesses` includes exactly that `definition_id` in the list.
Failure example: build succeeds (201) but the package never appears in a later list call.
Evidence: response bodies of both calls.
Test layer: integration — `tests/api/test_harnesses.py::test_build_generic_then_list`.

**AC-003 — Building an activative-mode Harness records its category**
Given the server is running,
When `POST /api/harnesses/build` is called with `tests/fixtures/productization/manifests/activative_expression.json` as the body,
Then the response is HTTP 201 with `mode: "activative"` and `category_id: "conversational_activation_expression"`.
Failure example: `category_id` is `null` or missing for an activative manifest.
Evidence: response body.
Test layer: integration — `tests/api/test_harnesses.py::test_build_activative_records_category`.

**AC-004 — Malformed manifest is rejected before touching the library**
Given the server is running,
When `POST /api/harnesses/build` is called with a body missing the required `task.authority_ref` field,
Then the response is HTTP 400 with `error_code: "INVALID_MANIFEST"`,
And `GET /api/harnesses` afterward shows no new entry.
Failure example: a 500 is returned instead of 400, or a partial package appears in the library.
Evidence: response status/body of the build call, and the list call after it.
Test layer: integration — `tests/api/test_harnesses.py::test_invalid_manifest_rejected`.

**AC-005 — Detail view returns full contract fields**
Given a Harness has been built per AC-003,
When `GET /api/harnesses/{definition_id}` is called,
Then the response is HTTP 200 and includes `goal`, `success_condition`, `input_contract`, `output_contract`, and a `category_binding` object whose `category_id` equals `"conversational_activation_expression"`.
Failure example: `category_binding` is absent or flattened incorrectly.
Evidence: response body.
Test layer: integration — `tests/api/test_harnesses.py::test_detail_view_full_contract`.

**AC-006 — Unknown definition_id returns 404**
Given the server is running,
When `GET /api/harnesses/does-not-exist` is called,
Then the response is HTTP 404 with `error_code: "NOT_FOUND"`.
Failure example: 500 returned instead of a typed 404.
Evidence: response status and body.
Test layer: integration — `tests/api/test_harnesses.py::test_unknown_id_404`.

**AC-007 — Eligibility check matches, mismatches, and generic-mode correctly**
Given the activative Harness from AC-003 (`category_id: conversational_activation_expression`),
When `GET /api/harnesses/{id}/eligibility?source_category=conversational_activation_expression` is called, Then `status: "ELIGIBLE"`.
When `GET /api/harnesses/{id}/eligibility?source_category=carousels` is called, Then `status: "INELIGIBLE"` and `reason` names both categories.
Given the generic Harness from AC-002,
When `GET /api/harnesses/{id}/eligibility?source_category=carousels` is called, Then `status: "NOT_APPLICABLE"`.
Failure example: a generic-mode Harness returns `"INELIGIBLE"` instead of `"NOT_APPLICABLE"`.
Evidence: three response bodies.
Test layer: integration — `tests/api/test_harnesses.py::test_eligibility_matrix`.

**AC-008 — Rebuilding an unchanged manifest is idempotent**
Given the generic Harness from AC-002 already exists in the library,
When `POST /api/harnesses/build` is called again with the byte-identical manifest body,
Then the response is HTTP 201 with the same `definition_id`, `definition_hash`, and `package_hash` as the first build,
And the library still contains exactly one file for that `definition_id` (the second export overwrote it with byte-identical content, not a duplicate).
Failure example: the second call returns 409 `CONFLICT`, or produces a second, differently-named package.
Evidence: both response bodies; directory listing of `CA_HARNESS_LIBRARY_ROOT`.
Test layer: integration — `tests/api/test_harnesses.py::test_rebuild_is_idempotent`.

**AC-009 — Same manifest_id with different content is a real conflict**
Given the generic Harness from AC-002 already exists,
When `POST /api/harnesses/build` is called with a body that reuses `manifest_id: "operator-manifest-generic-summary"` but changes `task.goal` to different text,
Then the response is HTTP 409 with `error_code: "CONFLICT"`.
Failure example: the second, different manifest silently overwrites the first under the same `manifest_id`.
Evidence: response status and body.
Test layer: integration — `tests/api/test_harnesses.py::test_conflicting_manifest_id_rejected`.

**AC-010 — A corrupt package does not break the whole listing**
Given the library contains one valid built Harness and one hand-created invalid `.zip` file (e.g. containing only a text file, no `atomic_harness_definition.json`),
When `GET /api/harnesses` is called,
Then the response is HTTP 200 and contains exactly the one valid entry; the corrupt file is silently excluded, and a warning is logged.
Failure example: the whole request 500s because one file in the directory is unreadable.
Evidence: response body; captured log output.
Test layer: integration — `tests/api/test_harnesses.py::test_corrupt_package_excluded_not_fatal`.

**AC-011 — No modification to existing service packages**
Given the Phase 9 test suite at `tests/` was passing before this spec,
When this spec is fully implemented and `python -m pytest tests/ -q` is run,
Then all pre-existing tests continue to pass.
Failure example: any previously-passing test now fails.
Evidence: pytest output — 0 failures.
Test layer: regression — run full existing suite.

---

## 10. Testing and Completion Evidence

### Test files to create

**`tests/api/fixtures/harnesses/`** — copy (not symlink, so the API test suite does not depend on the Builder package's internal test layout) of:
- `generic_text_summary.json`
- `activative_expression.json`
from `01_ATOMIC_HARNESS_BUILDER/tests/fixtures/productization/manifests/` (post-restructure: `services/builder/tests/fixtures/productization/manifests/`)

**`tests/api/test_harnesses.py`**
- `test_empty_library_returns_empty_list` — AC-001
- `test_build_generic_then_list` — AC-002
- `test_build_activative_records_category` — AC-003
- `test_invalid_manifest_rejected` — AC-004
- `test_detail_view_full_contract` — AC-005
- `test_unknown_id_404` — AC-006
- `test_eligibility_matrix` — AC-007
- `test_rebuild_is_idempotent` — AC-008
- `test_conflicting_manifest_id_rejected` — AC-009
- `test_corrupt_package_excluded_not_fatal` — AC-010

### Test tooling

Reuses `httpx` + FastAPI `TestClient` already established by TS-APP-API-001. Each test uses a fresh `tmp_path` for `CA_DATA_ROOT` (and therefore `CA_HARNESS_LIBRARY_ROOT` and `builder.sqlite3`) so tests never share state:

```python
import os
from fastapi.testclient import TestClient

def test_build_generic_then_list(tmp_path, monkeypatch):
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path))
    from api.main import app
    with TestClient(app) as client:
        manifest = (Path(__file__).parent / "fixtures/harnesses/generic_text_summary.json").read_bytes()
        build = client.post("/api/harnesses/build", content=manifest,
                             headers={"Content-Type": "application/json"})
        assert build.status_code == 201
        definition_id = build.json()["definition_id"]

        listing = client.get("/api/harnesses")
        assert listing.status_code == 200
        assert definition_id in [item["definition_id"] for item in listing.json()]
```

### Pre-existing regression
```bash
python -m pytest tests/ -q --tb=short
```
Zero new failures is a hard gate (AC-011).

### Build Receipt claim ceiling
`HARNESS_LIBRARY_API_DEVELOPMENT_EVIDENCE`

This spec does not claim:
- Pipeline execution readiness for any listed or built Harness (Gap 4 — schema mismatch is unresolved)
- constitutional-authority certification of any Harness (Gap 5 — only structural `CategoryBinding` validation runs)
- production eligibility of any kind (every definition self-reports `production_eligible: false, certified: false`, unmodified)
- authentication or authorization on any route
- format-profile (`profile_id`) awareness — the Builder's exported definition has no such field (see Gap 4); browsing by "format profile" as FR-APP-040 describes is not possible until that gap is closed

---
spec_end: true
next_spec: TS-APP-API-003 (Interview Admission API)
prerequisite_for_next: none — TS-APP-API-003 does not depend on this spec
blocking_risk_for_downstream: Gap 4 (Builder/Pipeline schema mismatch) must be resolved by a dedicated reconciliation spec before TS-APP-API-004 can claim that a selected Harness is actually executable by the Pipeline, and before TS-APP-API-005 can report meaningful workflow node status for it
---
