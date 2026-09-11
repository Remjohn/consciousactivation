---
spec_id: TS-APP-BRIDGE-001
title: Harness Definition Compiler
document_class: TECH_SPEC
product: Conscious Activations
module: bridge
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CURRENT
build_authority: false
controlling_frs:
  - FR-APP-041 (Harness selection for campaign — cannot be truthfully executable without this)
  - FR-APP-042 (Harness creation via Pi Coding Agent — the artifact this creates is currently unusable downstream)
controlling_stories:
  - ST-APP-06.01, ST-APP-06.02, ST-APP-06.03 (all three assume a built Harness can
    eventually run; this spec is the missing link that makes that true)
upstream_dependencies:
  - CA_PROJECT_SNAPSHOT_V2.md (authority — CURRENT)
  - CA_APP_FR_EPIC_SPEC_PLAN.md (authority — CURRENT)
  - SPEC_GAP_LEDGER.md (authority — CURRENT; this spec closes GAP-002)
  - TS-APP-API-002.md (quality_state: WRITTEN_PENDING_AUDIT — DRAFT_DEPENDENCY_NOT_ACCEPTED;
    that spec's own "Gap 4" is the problem statement this spec resolves. IMPORTANT
    CORRECTION: TS-APP-API-002's Gap 4 cites the file to read as
    `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/skills/portable_package.py`. That file
    was read directly for this spec (see Section 1) and is NOT the Harness definition
    format — it is `PortableSkillPackage`, a Skill artifact format
    (skill_id="activative_intelligence_pack_compiler"), structurally unrelated to
    Harnesses. The real class, `PortableAtomicHarnessDefinition`, lives at
    `cmf_builder/domain/portable_export.py`. This spec reads the correct file; the
    citation in TS-APP-API-002's frontmatter should be corrected to point here when
    that spec is next touched, but this spec does not modify TS-APP-API-002.md itself)
downstream_consumers:
  - TS-APP-API-004.md (Campaign CRUD — its Source Gap Notice 1 explicitly names
    this spec as required before `pipeline_ingestion_status` can ever leave
    `NOT_YET_TRIGGERED`)
  - TS-APP-API-005.md (Pipeline Status WebSocket — flagged BLOCKED on this exact gap)
  - Any future spec that calls `AtomicHarnessDefinitionIntake.validate()` with a
    Builder-produced definition
output_path: services/pipeline/src/cmf_pipeline/intake/harness_compiler.py
wave: 0.5 (between repository restructure and Wave 1 API implementation;
  no HTTP dependency, but blocks truthful completion of TS-APP-API-004/005)
---

# TS-APP-BRIDGE-001 — Harness Definition Compiler

## 1. Files and Authorities Read

| File | SHA-256 (short) | Status | Fact extracted |
|---|---|---|---|
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/skills/portable_package.py` | read in full | READ — CURRENT, **WRONG FILE FOR THIS PROBLEM** | Defines `PortableSkillPackage` / `PortablePackageError` for `skill_id="activative_intelligence_pack_compiler"` — a Skill artifact bundle (SKILL.md, contracts/, execution/, references/), not a Harness. TS-APP-API-002's Gap 4 citation of this path is incorrect; noted above, not corrected in place. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/portable_export.py` | read in full | READ — CURRENT, **THE REAL FILE** | Defines `PortableAtomicHarnessDefinition.create()`. Its `.content` dict has exactly 27 keys (enumerated Section 3). `category_binding` is nested; for `mode="activative"` it requires `wrong_reading_locks` (list, non-empty) and `runtime_law == "Activation First"` among 16 required keys. For `mode="generic"` it is a fixed 3-key object with `category_id: None`. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/application/export_service.py` | read in full | READ — CURRENT IMPLEMENTATION | `PortableAtomicHarnessCompiler.compile()` is the only caller of `PortableAtomicHarnessDefinition.create()`. It receives `manifest.normalized` — the parsed operator manifest — directly, meaning `content["goal"]`, `content["atomic_boundary"]` etc. originate from a single flat `task` object, never from a decomposed multi-step structure. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/operator_manifest.py` | read in part | READ — CURRENT IMPLEMENTATION | `OperatorTaskDefinition.capability_requirements: tuple[str, ...]` — confirmed a flat tuple of bare capability-name strings, not objects. `provenance_refs: tuple[str, ...]` — also bare strings, not `{object_id, version, sha256}` refs. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/application/manifest_parser.py` | read in part | READ — CURRENT IMPLEMENTATION | `manifest_version` is parsed via `require_text` only — **no semver format is enforced at the Builder side.** This is a genuine risk surface for this spec (Section 4). |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/intake/definition_intake.py` | read in full | READ — CURRENT IMPLEMENTATION | `AtomicHarnessDefinitionIntake.REQUIRED_KEYS` — exactly 14 keys (enumerated Section 3). `._workflow()` requires `nodes` (non-empty list, 10 required keys per node) and `edges` (list, 3 required keys per edge, each edge's `source_node_id`/`target_node_id` must both exist among node IDs). `._capabilities()` requires a non-empty list of `{capability_id, owner_kind, required_features, authority_boundary}` objects. |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/intake/compiler_profile_registry.py` | read in full | READ — CURRENT IMPLEMENTATION | `HarnessDefinitionProfileRegistry` holds exactly two `CompilerProfile` entries keyed by `package_profile`: `"portable_generic_v1"` → `profile_id="portable-generic-v1"`, and `"portable_activative_v1"` → `profile_id="portable-activative-v1"`. `.status()` reports `"shape_guessing_enabled": False` — an explicit, pre-existing project convention against exactly the kind of silent inference this spec must avoid. |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/domain/validation.py` | read in part | READ — CURRENT IMPLEMENTATION | `require_ref_list()` calls `require_ref()` per item, which demands **exactly** `{object_id, version, sha256}` per entry — `version` must itself pass `require_semver`, `sha256` must pass `require_sha`. `require_semver` pattern: `^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?$`. |

**Source Gap Notice — TS-APP-API-002's Gap 4 citation was itself imprecise.** Its problem statement ("Builder output and Pipeline input are structurally incompatible") is correct and independently reconfirmed by this spec's own file reads. But the specific file path it named as evidence was wrong. This spec relies on the correct files, read directly, and the finding is not weakened by the earlier citation error — if anything it is now on firmer ground because this spec verified the mismatch against the real `PortableAtomicHarnessDefinition`, not a same-named-sounding Skill package format.

---

## 2. Problem, User Outcome, Solution, and Scope

### Problem without this spec
`POST /api/harnesses/build` (TS-APP-API-002, once implemented) will call
`PortableAtomicHarnessCompiler.compile()` and produce a real, hash-verified,
tamper-evident `PortableAtomicHarnessDefinition`. Separately,
`AtomicHarnessDefinitionIntake.validate()` (called somewhere inside Pipeline
execution, not yet by any written spec) is the only way a Harness definition
becomes eligible to drive a workflow run. **The two shapes share almost no
field names, and where names do coincide the value shapes usually differ.**
A Harness built through the API today, handed directly to the Pipeline's
intake validator, raises `PipelineValidationError` on the first line
(`set(definition) != self.REQUIRED_KEYS`). There is currently no code
anywhere in the repository that attempts this translation.

### User outcome
An operator (or the Pi Coding Agent) builds a Harness through the Builder.
That Harness, once compiled by this spec's function, can be hand off to
`AtomicHarnessDefinitionIntake.validate()` and pass — for the cases this spec
can honestly resolve without inventing data. For the cases it cannot honestly
resolve (Section 4), the compiler raises a typed, specific error naming
exactly which Pipeline-required field has no legitimate source in the
Builder's output, instead of silently fabricating a plausible-looking value.

### Solution
One pure function, `compile_portable_to_intake()`, in a new module
`services/pipeline/src/cmf_pipeline/intake/harness_compiler.py`. It takes a
`PortableAtomicHarnessDefinition` (or its `.content` mapping) and returns a
`dict[str, Any]` shaped to exactly `AtomicHarnessDefinitionIntake.
REQUIRED_KEYS`, suitable for passing straight into
`AtomicHarnessDefinitionIntake().validate(result, profile)`. Where a
mechanical, defensible, zero-guessing mapping exists, it performs it. Where
none exists, it raises `HarnessCompilationBlocked` — a new typed exception —
naming the exact missing source field and the exact Pipeline field it cannot
populate.

### In scope
- `services/pipeline/src/cmf_pipeline/intake/harness_compiler.py` — the compiler function and its typed exception
- `services/pipeline/src/cmf_pipeline/intake/harness_compiler_contracts.py` — the `HarnessCompilationBlocked` exception and `CompilationOutcome` result type
- Unit tests proving every field mapping decision in Section 4, both the successful paths and the four blocked paths
- A written decision (Section 4) on the workflow node/edge question this spec was explicitly asked to resolve or escalate

### Out of scope
- Any change to `PortableAtomicHarnessDefinition`, `AtomicHarnessDefinitionIntake`, or any file read in Section 1 — this spec adds a new module, it does not modify either existing schema
- Any HTTP route — this is a pure Python compiler, called by future API specs, not exposed directly
- Resolving the capability-shape gap (Section 4, Blocker 2) by inventing `owner_kind`/`required_features`/`authority_boundary` values — this spec refuses to guess and says so explicitly in its error contract
- Extending the Builder's operator manifest schema to add new required fields — that would be a Builder-side spec, proposed but not written here (Section 4 names it as the likely real fix)
- Wiring this compiler into `POST /api/harnesses/build` or any campaign-creation flow — that is TS-APP-API-004's job, once it exists in patched form (see `SPEC_GAP_LEDGER.md` resolution sequence step 9)

---

## 3. The Two Schemas, Side by Side, Exactly as Read

### Builder produces (`PortableAtomicHarnessDefinition.content`, 27 keys)
```
schema_id, schema_version, compiler_id, compiler_version, amendment,
manifest_id, manifest_version, manifest_hash, task_id, mode, classification,
category_binding, atomic_boundary, goal, success_condition, input_contract,
output_contract, minimum_complete_context, capability_requirements,
acceptance_tests, execution_plan, authority_chain, provenance_refs,
activative_intelligence, external_skills_required,
external_runtime_dependencies, workflow_execution_performed,
production_eligible, certified, certification_state, compatibility_status,
lineage
```
(count note: 32 keys as enumerated above — corrected from the frontmatter's
approximate "27"; exact count taken from `required` set literal in
`portable_export.py::validate()`, not estimated)

For `mode="activative"`, `category_binding` additionally carries:
```
harness_id, harness_version, applicability, category_id, category_name,
category_registry_version, category_registry_hash,
constitutional_authority_ref, runtime_law, harness_development_law,
semantic_lineage_refs, wrong_reading_locks, not_applicable_basis,
certification_state, production_ready, certified, binding_hash
```

### Pipeline requires (`AtomicHarnessDefinitionIntake.REQUIRED_KEYS`, 14 keys)
```
definition_id, definition_version, category_id, profile_id, purpose,
semantic_dependencies, capabilities, workflow, evaluation_requirements,
repair_laws, wrong_reading_locks, production_ready, certified,
invalidation_state
```

`workflow` = `{nodes: [...], edges: [...]}`. Each node requires exactly:
```
node_id, capability_id, phase_order, purpose, actor_kind, role,
product_boundary, input_contracts, output_contracts, side_effect_class
```
Each edge requires exactly: `source_node_id, target_node_id, contract_id`.

`capabilities` = list of objects each requiring exactly:
```
capability_id, owner_kind, required_features, authority_boundary
```

`semantic_dependencies` = list of `{object_id, version, sha256}` — the
canonical `ImmutableRef` shape, verified by `require_ref_list` →
`require_ref`.

### Overlap analysis (every Pipeline-required key, mapped or not)

| Pipeline field | Source in Builder output | Mapping risk |
|---|---|---|
| `definition_id` | `content["manifest_id"]` is NOT it — use the definition's own top-level `definition_id` (`f"atomic-harness-definition_{digest}"`), available on the `PortableAtomicHarnessDefinition` object itself, not inside `.content` | **CLEAN** — pass through unchanged |
| `definition_version` | `content["manifest_version"]` | **RISK** — Builder enforces no semver format (`require_text` only); Pipeline enforces strict semver via `require_semver`. Must validate and fail loudly, not coerce (Section 4, Blocker 4) |
| `category_id` | `content["category_binding"]["category_id"]` for `mode="activative"`; is `None` for `mode="generic"` | **CLEAN for activative. BLOCKED for generic** — Pipeline's `require_string` rejects `None` (Section 4, Blocker 3) |
| `profile_id` | NOT a content field — resolved via `HarnessDefinitionProfileRegistry.resolve(f"portable_{content['mode']}_v1")`, then `.profile_id` | **CLEAN** — deterministic, zero-guessing, uses the existing Pipeline registry exactly as designed |
| `purpose` | `content["goal"]` | **CLEAN, low-risk semantic mapping** — "goal" and "purpose" are functionally synonymous in this domain; documented as a naming choice, not a data fabrication |
| `semantic_dependencies` | `content["provenance_refs"]` (`list[str]`) | **BLOCKED** — Pipeline wants `{object_id, version, sha256}` objects; Builder has bare strings with no version or hash. Cannot manufacture `version`/`sha256` without inventing data (Section 4, Blocker 1) |
| `capabilities` | `content["capability_requirements"]` (`list[str]`, bare capability names) | **BLOCKED** — Pipeline wants `{capability_id, owner_kind, required_features, authority_boundary}` objects; only `capability_id` has a source. `owner_kind`, `required_features`, `authority_boundary` have zero source anywhere in Builder's output (Section 4, Blocker 2) |
| `workflow` | no equivalent structure exists — Builder produces one flat task, not a node/edge graph | **BLOCKED, THE CENTRAL PRODUCT DECISION** (Section 4, Blocker 5) |
| `evaluation_requirements` | no equivalent field anywhere in Builder's output | **BLOCKED** — total absence, not a shape mismatch (Section 4, Blocker 6) |
| `repair_laws` | no equivalent field anywhere in Builder's output | **BLOCKED** — total absence (Section 4, Blocker 6) |
| `wrong_reading_locks` | `content["category_binding"]["wrong_reading_locks"]` for `mode="activative"` only; no field at all for `mode="generic"` | **CLEAN for activative** (Pipeline's `wrong_reading_locks` list has no `non_empty` requirement, so an empty list is legal for generic mode) |
| `production_ready` | `content["production_eligible"]` (always `False`) | **CLEAN** — rename only, boolean value already always `False` in both schemas |
| `certified` | `content["certified"]` (always `False`) | **CLEAN** — identical key name, identical always-`False` value |
| `invalidation_state` | no equivalent field anywhere in Builder's output | **BLOCKED** — total absence (Section 4, Blocker 7) |

**Result: 8 of 14 required Pipeline fields have a clean, zero-guessing
mapping. 6 do not.** Four of those six are genuine total absences (no
Builder field exists at all, in any mode); one is a partial absence
(generic-mode `category_id`); one — `workflow` — is the central structural
gap this spec was explicitly asked to resolve or escalate.

---

## 4. The Blockers — Decided, Escalated, or Both

This section is the actual product-decision work the spec was commissioned
to do. Each blocker gets: what was found, the options, this spec's
recommendation, and its formal status.

### Blocker 1 — `semantic_dependencies` needs `{object_id, version, sha256}`; Builder has bare strings

Builder's `provenance_refs` are free-text strings (per `operator_manifest.py`,
`provenance_refs: tuple[str, ...]`) — human-readable citations, not
resolvable object references with a version and content hash. There is no
registry this compiler can query to look up a `provenance_refs` string and
get back a real `sha256`.

**Options considered:**
- (a) Treat each `provenance_refs` string as `object_id`, synthesize
  `version="0.0.0"` and `sha256` of the string itself. **Rejected** — this
  fabricates a false claim of content-addressed identity for something that
  was never hashed as an object; it's exactly the kind of "shape guessing"
  `compiler_profile_registry.py` explicitly disclaims (`shape_guessing_
  enabled: False`).
- (b) Map only `content["lineage"]` entries that already look like real
  hashes (the list mixes `manifest_hash`, `authority_ref`, `provenance_refs`,
  and optionally `binding_hash`) — filter to items matching a `sha256:...`
  pattern. **Rejected** — still requires fabricating `object_id` and
  `version` for entries that were never meant to be `ImmutableRef`s.
- (c) Refuse to populate `semantic_dependencies` from inference; require it
  as an explicit, separate input to `compile_portable_to_intake()`, supplied
  by whatever caller has actual knowledge of the real upstream semantic
  objects (e.g., a future AIR API — see `SPEC_GAP_LEDGER.md` GAP-001).

**This spec's decision: (c).** `semantic_dependencies` is not derivable from
`PortableAtomicHarnessDefinition` alone — full stop, not a mapping problem.
The compiler function takes it as an explicit caller-supplied parameter,
typed `list[dict[str, str]] | None`. If the caller passes `None`, the
compiler raises `HarnessCompilationBlocked` naming this field. **Status:
DECIDED — resolved via explicit parameter, not by escalation, because there
is a real design pattern here (caller supplies what the artifact genuinely
doesn't contain) rather than a genuine open question.**

### Blocker 2 — `capabilities` needs `owner_kind`/`required_features`/`authority_boundary`; Builder has none of these

`capability_requirements` in Builder's output is a flat `tuple[str, ...]` of
capability names only. Pipeline's per-capability object requires
`owner_kind` (which actor type owns this capability — e.g. human, model,
tool), `required_features` (a list of feature flags), and
`authority_boundary` (a governance string). None of these three concepts
exist anywhere in the Builder's operator manifest schema.

**Options considered:**
- (a) Default `owner_kind="unspecified"`, `required_features=[]`,
  `authority_boundary="unspecified"`. **Rejected** — Pipeline's
  `_capabilities()` does not accept empty strings for these fields
  (`require_string` rejects empty), and even if it did, fabricating
  governance metadata is a worse failure mode than refusing outright.
- (b) Look these up from a static registry keyed by `capability_id`.
  **Considered, not implemented here** — this could work if such a registry
  existed, but none does today. This is the most promising real fix.
- (c) Refuse, same pattern as Blocker 1: take an optional caller-supplied
  `capability_metadata: dict[str, dict] | None` mapping each
  `capability_id` to its `owner_kind`/`required_features`/
  `authority_boundary`; raise if any `capability_id` from Builder's list is
  missing from the supplied metadata.

**This spec's decision: (c), with (b) flagged as the real long-term fix.**
The compiler accepts `capability_metadata` as an explicit parameter. This
spec does not build the registry — that's real, separate product work
(likely belongs in `cmf_pipeline`'s existing capability infrastructure, not
invented here). **Status: DECIDED for this spec's contract; ESCALATED as a
recommendation that a `CapabilityMetadataRegistry` be built as a follow-on
spec** — noted in Section 11.

### Blocker 3 — generic-mode Harnesses have `category_id: None`; Pipeline requires a non-empty string

**Options considered:**
- (a) Synthesize a sentinel category like `"generic"` or `"uncategorized"`.
  **Rejected without a human decision** — this silently changes what
  `category_id` means system-wide; every other consumer of `category_id`
  (the eligibility check in TS-APP-API-002, TS-APP-API-004's harness↔source
  compatibility check) assumes it names a real content category from the
  canonical category registry, not a placeholder.
- (b) This compiler simply does not support `mode="generic"` Harnesses;
  raise immediately if `content["mode"] != "activative"`.

**This spec's decision: (b), but flagged as a genuine open question, not a
unilateral call.** Every downstream consumer in the written specs — Campaign
creation, Control Tower, the entire content-production flow described in
`CA_PROJECT_SNAPSHOT_V2.md` §2 — operates on categorized content
(short video, Carousel, SuperVisual, animation). It is plausible that
`mode="generic"` Harnesses were only ever meant for Builder-internal
tooling tasks, never for the content-production Pipeline this app wraps. If
that reading is correct, refusing generic-mode input here is the right
permanent behavior, not a temporary limitation. **Status: DECIDED for this
spec (raises `HarnessCompilationBlocked`), but FLAGGED FOR HUMAN
CONFIRMATION — if generic-mode Harnesses do have a real, intended use inside
Pipeline execution, this decision needs to be revisited, and the fix is
product-level (define what a generic Harness's category should be), not a
code fix in this compiler.**

### Blocker 4 — `manifest_version` may not be valid semver

Builder's `manifest_version` is parsed with `require_text` only — an
operator could legally submit `"v2 draft"` or `"latest"`. Pipeline's
`definition_version` demands the exact pattern
`^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?$`.

**Decision:** The compiler validates `manifest_version` against Pipeline's
own `require_semver` pattern (imported, not reimplemented) before use. If it
fails, raise `HarnessCompilationBlocked` naming the exact invalid value —
never coerce or truncate a version string to make it fit. **Status:
DECIDED.** This is not a genuine ambiguity; it is a real, occasionally-true
input validation failure that must surface loudly, and the failure mode is
mechanical, not a design question.

### Blocker 5 — `workflow.nodes/edges` — the central structural gap

This is the blocker the spec commission specifically named. Builder produces
one flat, atomic `task` (`goal`, `success_condition`, `atomic_boundary`,
`input_contract`, `output_contract`, `capability_requirements`,
`acceptance_tests`) describing **a single indivisible unit of work.**
Pipeline's `workflow` is a directed graph of **multiple** nodes, each with
its own `actor_kind`, `role`, `product_boundary`, `phase_order`, and
`side_effect_class`, connected by typed edges.

**Options considered:**

*(a) One Builder definition compiles to exactly one Pipeline workflow node,
zero edges.* The node's fields derive as:
  - `node_id` — a fixed constant, e.g. `"root"`, or derived from `task_id`
  - `capability_id` — requires picking exactly one from
    `capability_requirements` if there are multiple, which is itself
    ambiguous when the list has more than one entry
  - `phase_order` — trivially `0` (only node)
  - `purpose` — `content["goal"]`, same source as top-level `purpose`
  - `actor_kind`, `role`, `product_boundary`, `side_effect_class` — **no
    source exists in Builder's output for any of these four**
  - `input_contracts`/`output_contracts` — Pipeline wants **lists of
    contract-ID strings**; Builder's `input_contract`/`output_contract` are
    **single Mapping objects** (JSON-schema-shaped), not ID strings — a
    second, independent shape mismatch nested inside this same field

*(b) A Harness definition never becomes a workflow directly; a separate,
explicit "workflow authoring" step (human or Pipeline-owned) always
constructs the `workflow` object, referencing the Harness definition by ID
for its semantic content but not deriving structure from it.* This treats
`workflow` as fundamentally Pipeline-owned data that merely *cites* a
Harness, never *derives from* one.

*(c) Extend the Builder's operator manifest schema with a new, optional
`workflow` object mirroring Pipeline's shape, so an operator who already
knows they're building a multi-step Harness can author the graph directly
at Builder time; this compiler then passes it through with validation
rather than deriving it.

**This spec's recommendation, offered for human decision, not decided
unilaterally:** Option (a), constrained to Harnesses whose
`capability_requirements` has **exactly one entry**, is the only variant of
"derive automatically" that doesn't require inventing data the Builder never
collected (`actor_kind`, `role`, `product_boundary`, `side_effect_class`
still have zero source under any variant of (a), so even the one-node case
needs *something* — see below). The word "Atomic" in "Atomic Harness
Definition" is suggestive of exactly this reading: one Harness, one
indivisible unit, one node. But **`actor_kind`, `role`, `product_boundary`,
`side_effect_class`, and the `input_contracts`/`output_contracts` shape
conversion remain unsolved even under this reading** — they are not derivable
from anything in Builder's `content`, the same total-absence problem as
Blockers 1, 2, 6, and 7, just inside a nested structure instead of a
top-level field.

Option (b) is architecturally the most honest given what the code actually
contains: `workflow_execution_performed: False` is a literal field in every
`PortableAtomicHarnessDefinition` — the Builder's own schema already asserts
that no execution planning happens at Builder time. Reading that field
alongside the rest of the schema, option (b) may be what the original schema
design intended: **a Harness Definition is semantic content and category
binding; a Workflow is a separate Pipeline-owned execution plan that
consumes a Harness Definition as one input among several, not the sole
source of its own shape.**

**Status: NOT DECIDED. ESCALATED FOR HUMAN DECISION.** This spec implements
neither (a) nor (b) as a silent default. Instead, `compile_portable_to_intake()`
requires `workflow: dict | None` as an explicit caller-supplied parameter,
exactly like Blockers 1 and 2. If `None`, it raises
`HarnessCompilationBlocked(field="workflow", reason=BLOCKER_5_TEXT)`, where
`BLOCKER_5_TEXT` is a constant reproducing this section's option summary, so
the error message itself carries the decision context for whoever resolves
it. **This is the single most consequential open question in the entire
spec set** — until it is decided, no Harness can ever automatically become
an executable workflow, regardless of what any other spec does.

### Blocker 6 — `evaluation_requirements` and `repair_laws` have zero source

No field in Builder's 32-key content object, nor in `category_binding`'s
17 activative-mode keys, corresponds to evaluation requirements or repair
laws. This is a clean total absence, not a shape mismatch.

**Decision:** Both are explicit optional caller-supplied parameters,
identical pattern to Blockers 1 and 2. If omitted, raise
`HarnessCompilationBlocked`. **Status: DECIDED** (mechanically, via the
same "no source, so require it explicitly" pattern) — **but the
underlying question of where these should come from long-term (a new
Builder manifest field vs. a Pipeline-side default policy) is the same
category of open question as Blocker 5, just lower-stakes.** Noted as a
follow-on item in Section 11.

### Blocker 7 — `invalidation_state` has zero source

Same total-absence pattern as Blocker 6.

**Decision:** Rather than requiring this as a caller parameter (every other
blocker's pattern), this spec defaults it to `"NOT_INVALIDATED"` when the
caller does not supply it — because a **freshly compiled** Harness
definition, by construction, has never been superseded or invalidated by
anything. This is not fabricating unknown data; it is a true statement
about a definition that is being compiled for the first time. **Status:
DECIDED, with justification, not escalated** — this is the one blocker
where "no source field" does not mean "unknowable," because the answer is
knowable from context (this is a brand-new compilation) rather than needing
to be invented.

---

## 5. Governing Decisions and Constraints

**This compiler never invents data to satisfy a schema.** Every blocker in
Section 4 that could not be mechanically and defensibly resolved is either
(a) required as an explicit caller-supplied parameter with no default, or
(b) resolved with a documented, narrow justification (Blocker 7 only). This
mirrors the existing codebase's own stated philosophy
(`"shape_guessing_enabled": False"` in `compiler_profile_registry.py`) —
this spec extends that philosophy to the compiler it adds, rather than
introducing a weaker standard.

**The function is pure.** `compile_portable_to_intake()` performs no I/O, no
database access, no network calls. It is a deterministic transformation:
same inputs always produce the same output or the same typed exception.

**Existing schemas are not modified.** Neither `PortableAtomicHarnessDefinition`
nor `AtomicHarnessDefinitionIntake` is changed by this spec. If Blocker 5's
resolution eventually favors extending the Builder's manifest schema
(Section 4, option (c)), that is a separate, future spec against
`cmf_builder`, not this one.

**Claim ceiling:** `HARNESS_COMPILER_PARTIAL_BRIDGE_EVIDENCE`. This spec does
not claim Gap 4 (from `SPEC_GAP_LEDGER.md`) is fully closed — it is
narrowed and made explicit, with 8 of 14 fields mechanically solved and 6
requiring either caller input or a human decision (Blocker 5) that this
spec surfaces but does not make unilaterally.

---

## 6. Data Models, Contracts, Schemas, and APIs

### `HarnessCompilationBlocked` (new exception)
```python
class HarnessCompilationBlocked(Exception):
    def __init__(self, *, field: str, reason: str, blocker_ref: str) -> None:
        super().__init__(f"{field}: {reason} (see {blocker_ref})")
        self.field = field
        self.reason = reason
        self.blocker_ref = blocker_ref  # e.g. "TS-APP-BRIDGE-001#blocker-5"
```

### `compile_portable_to_intake()` signature
```python
def compile_portable_to_intake(
    definition: PortableAtomicHarnessDefinition,
    *,
    semantic_dependencies: list[dict[str, str]] | None = None,
    capability_metadata: dict[str, dict[str, object]] | None = None,
    workflow: dict[str, object] | None = None,
    evaluation_requirements: list[str] | None = None,
    repair_laws: list[str] | None = None,
) -> dict[str, Any]:
    """
    Compiles a Builder-produced PortableAtomicHarnessDefinition into the
    exact shape AtomicHarnessDefinitionIntake.REQUIRED_KEYS expects.

    Raises HarnessCompilationBlocked if:
      - definition.content["mode"] != "activative" (Blocker 3)
      - definition.content["manifest_version"] is not valid semver (Blocker 4)
      - semantic_dependencies is None (Blocker 1)
      - capability_metadata is missing an entry for any capability_id in
        definition.content["capability_requirements"] (Blocker 2)
      - workflow is None (Blocker 5)
      - evaluation_requirements is None (Blocker 6)
      - repair_laws is None (Blocker 6)

    Returns a dict with all 14 AtomicHarnessDefinitionIntake.REQUIRED_KEYS
    populated, ready to pass to AtomicHarnessDefinitionIntake().validate().
    Does NOT call .validate() itself — that remains the caller's explicit
    next step, so the caller also supplies and controls the CompilerProfile.
    """
```

### Positive example — all parameters supplied, activative mode, valid semver
```python
result = compile_portable_to_intake(
    definition,  # mode="activative", manifest_version="1.0.0"
    semantic_dependencies=[
        {"object_id": "final-script_abc123", "version": "1.0.0", "sha256": "a1b2...64chars"},
    ],
    capability_metadata={
        "video_editing": {
            "owner_kind": "tool",
            "required_features": ["ffmpeg"],
            "authority_boundary": "pipeline_owned_execution",
        },
    },
    workflow={
        "nodes": [{
            "node_id": "root", "capability_id": "video_editing", "phase_order": 0,
            "purpose": "Edit source-led short video",
            "actor_kind": "tool", "role": "composer",
            "product_boundary": "pipeline",
            "input_contracts": ["source_package_v1"],
            "output_contracts": ["video_edit_program_v1"],
            "side_effect_class": "produces_artifact",
        }],
        "edges": [],
    },
    evaluation_requirements=["source_fidelity_check"],
    repair_laws=["bounded_local_repair_only"],
)
# result == {
#   "definition_id": "atomic-harness-definition_<digest>",
#   "definition_version": "1.0.0",
#   "category_id": "short_video",
#   "profile_id": "portable-activative-v1",
#   "purpose": "<content['goal']>",
#   "semantic_dependencies": [...],
#   "capabilities": [{"capability_id": "video_editing", "owner_kind": "tool", ...}],
#   "workflow": {"nodes": [...], "edges": []},
#   "evaluation_requirements": ["source_fidelity_check"],
#   "repair_laws": ["bounded_local_repair_only"],
#   "wrong_reading_locks": [...],  # from category_binding
#   "production_ready": False,
#   "certified": False,
#   "invalidation_state": "NOT_INVALIDATED",
# }
```

### Negative example — Blocker 5 triggered
```python
compile_portable_to_intake(definition, semantic_dependencies=[...], capability_metadata={...})
# raises HarnessCompilationBlocked(
#   field="workflow",
#   reason="no source field in PortableAtomicHarnessDefinition; caller must "
#          "supply an explicit workflow graph — see TS-APP-BRIDGE-001 Section 4 "
#          "Blocker 5 for the unresolved product decision",
#   blocker_ref="TS-APP-BRIDGE-001#blocker-5",
# )
```

### Negative example — Blocker 3 triggered
```python
compile_portable_to_intake(generic_mode_definition, ...)
# raises HarnessCompilationBlocked(
#   field="category_id",
#   reason="mode='generic' Harnesses have category_id=None; this compiler "
#          "only supports mode='activative' — see Blocker 3 for the open "
#          "question of whether generic Harnesses need Pipeline execution at all",
#   blocker_ref="TS-APP-BRIDGE-001#blocker-3",
# )
```

---

## 7. Implementation Stages and Exact Target Paths

### Stage 1 — Exception and result types

**`services/pipeline/src/cmf_pipeline/intake/harness_compiler_contracts.py`**
```python
from __future__ import annotations
from dataclasses import dataclass


class HarnessCompilationBlocked(Exception):
    def __init__(self, *, field: str, reason: str, blocker_ref: str) -> None:
        super().__init__(f"{field}: {reason} (see {blocker_ref})")
        self.field = field
        self.reason = reason
        self.blocker_ref = blocker_ref


BLOCKER_1_TEXT = (
    "no source field in PortableAtomicHarnessDefinition for versioned, "
    "hashed semantic references; provenance_refs are bare strings without "
    "version or sha256 — see TS-APP-BRIDGE-001 Section 4 Blocker 1"
)
BLOCKER_2_TEXT = (
    "capability_requirements are bare capability_id strings; owner_kind, "
    "required_features, and authority_boundary have no source — see "
    "TS-APP-BRIDGE-001 Section 4 Blocker 2"
)
BLOCKER_3_TEXT = (
    "mode='generic' Harnesses have category_id=None; this compiler only "
    "supports mode='activative' — see TS-APP-BRIDGE-001 Section 4 Blocker 3 "
    "for the open question of whether generic Harnesses need Pipeline "
    "execution at all"
)
BLOCKER_4_TEXT = (
    "manifest_version is not valid semantic version format "
    "(^[0-9]+.[0-9]+.[0-9]+...) — see TS-APP-BRIDGE-001 Section 4 Blocker 4"
)
BLOCKER_5_TEXT = (
    "no source structure in PortableAtomicHarnessDefinition for a "
    "multi-node workflow graph; Builder produces one flat atomic task, not "
    "a decomposed node/edge graph — this is the central unresolved product "
    "decision in TS-APP-BRIDGE-001 Section 4 Blocker 5, offered but not "
    "decided unilaterally"
)
BLOCKER_6_EVAL_TEXT = (
    "no source field in PortableAtomicHarnessDefinition for evaluation "
    "requirements — see TS-APP-BRIDGE-001 Section 4 Blocker 6"
)
BLOCKER_6_REPAIR_TEXT = (
    "no source field in PortableAtomicHarnessDefinition for repair laws — "
    "see TS-APP-BRIDGE-001 Section 4 Blocker 6"
)
```

### Stage 2 — The compiler

**`services/pipeline/src/cmf_pipeline/intake/harness_compiler.py`**
```python
from __future__ import annotations
from typing import Any, Mapping

from cmf_builder.domain.portable_export import PortableAtomicHarnessDefinition

from ..domain.validation import require_semver, PipelineValidationError
from .compiler_profile_registry import HarnessDefinitionProfileRegistry
from .harness_compiler_contracts import (
    HarnessCompilationBlocked,
    BLOCKER_1_TEXT, BLOCKER_2_TEXT, BLOCKER_3_TEXT, BLOCKER_4_TEXT,
    BLOCKER_5_TEXT, BLOCKER_6_EVAL_TEXT, BLOCKER_6_REPAIR_TEXT,
)

_profile_registry = HarnessDefinitionProfileRegistry()


def compile_portable_to_intake(
    definition: PortableAtomicHarnessDefinition,
    *,
    semantic_dependencies: list[dict[str, str]] | None = None,
    capability_metadata: dict[str, dict[str, object]] | None = None,
    workflow: dict[str, object] | None = None,
    evaluation_requirements: list[str] | None = None,
    repair_laws: list[str] | None = None,
) -> dict[str, Any]:
    content = definition.content

    # Blocker 3 — mode gate
    if content["mode"] != "activative":
        raise HarnessCompilationBlocked(
            field="category_id", reason=BLOCKER_3_TEXT,
            blocker_ref="TS-APP-BRIDGE-001#blocker-3",
        )
    category_binding = content["category_binding"]
    category_id = category_binding["category_id"]

    # Blocker 4 — semver gate (reuses Pipeline's own validator, not reimplemented)
    manifest_version = content["manifest_version"]
    try:
        definition_version = require_semver(manifest_version, "manifest_version")
    except PipelineValidationError as exc:
        raise HarnessCompilationBlocked(
            field="definition_version", reason=BLOCKER_4_TEXT,
            blocker_ref="TS-APP-BRIDGE-001#blocker-4",
        ) from exc

    # profile_id — clean, deterministic derivation via existing Pipeline registry
    profile = _profile_registry.resolve(f"portable_{content['mode']}_v1")

    # Blocker 1 — semantic_dependencies must be caller-supplied
    if semantic_dependencies is None:
        raise HarnessCompilationBlocked(
            field="semantic_dependencies", reason=BLOCKER_1_TEXT,
            blocker_ref="TS-APP-BRIDGE-001#blocker-1",
        )

    # Blocker 2 — capability_metadata must cover every required capability_id
    capability_ids: list[str] = list(content["capability_requirements"])
    if capability_metadata is None:
        raise HarnessCompilationBlocked(
            field="capabilities", reason=BLOCKER_2_TEXT,
            blocker_ref="TS-APP-BRIDGE-001#blocker-2",
        )
    missing = sorted(set(capability_ids) - set(capability_metadata))
    if missing:
        raise HarnessCompilationBlocked(
            field="capabilities",
            reason=f"{BLOCKER_2_TEXT}; missing metadata for: {missing}",
            blocker_ref="TS-APP-BRIDGE-001#blocker-2",
        )
    capabilities = [
        {
            "capability_id": cap_id,
            "owner_kind": capability_metadata[cap_id]["owner_kind"],
            "required_features": capability_metadata[cap_id]["required_features"],
            "authority_boundary": capability_metadata[cap_id]["authority_boundary"],
        }
        for cap_id in capability_ids
    ]

    # Blocker 5 — workflow must be caller-supplied; this compiler never derives it
    if workflow is None:
        raise HarnessCompilationBlocked(
            field="workflow", reason=BLOCKER_5_TEXT,
            blocker_ref="TS-APP-BRIDGE-001#blocker-5",
        )

    # Blocker 6 — evaluation_requirements / repair_laws must be caller-supplied
    if evaluation_requirements is None:
        raise HarnessCompilationBlocked(
            field="evaluation_requirements", reason=BLOCKER_6_EVAL_TEXT,
            blocker_ref="TS-APP-BRIDGE-001#blocker-6",
        )
    if repair_laws is None:
        raise HarnessCompilationBlocked(
            field="repair_laws", reason=BLOCKER_6_REPAIR_TEXT,
            blocker_ref="TS-APP-BRIDGE-001#blocker-6",
        )

    # wrong_reading_locks — clean derivation from category_binding (activative mode only, always present here)
    wrong_reading_locks = list(category_binding["wrong_reading_locks"])

    # Blocker 7 — invalidation_state defaults to NOT_INVALIDATED for fresh compilation
    invalidation_state = "NOT_INVALIDATED"

    return {
        "definition_id": definition.definition_id,
        "definition_version": definition_version,
        "category_id": category_id,
        "profile_id": profile.profile_id,
        "purpose": content["goal"],
        "semantic_dependencies": semantic_dependencies,
        "capabilities": capabilities,
        "workflow": workflow,
        "evaluation_requirements": evaluation_requirements,
        "repair_laws": repair_laws,
        "wrong_reading_locks": wrong_reading_locks,
        "production_ready": content["production_eligible"],
        "certified": content["certified"],
        "invalidation_state": invalidation_state,
    }
```

---

## 8. Failure, Migration, Rollback, Recovery, and Observability

| Failure | Cause | Behaviour | Recovery |
|---|---|---|---|
| `HarnessCompilationBlocked(field="category_id", ...)` | `mode="generic"` input | Raised before any other check runs | Caller must not attempt to compile generic-mode Harnesses until Blocker 3 is resolved by a human decision |
| `HarnessCompilationBlocked(field="definition_version", ...)` | `manifest_version` fails semver pattern | Raised after mode check, before any other blocker check | Operator must resubmit the Harness through the Builder with a valid `manifest_version` (e.g. `"1.0.0"` not `"v1"`) |
| `HarnessCompilationBlocked(field="semantic_dependencies", ...)` | caller omitted the parameter | Raised regardless of definition content | Caller (future AIR-integrated spec) must supply real `ImmutableRef` objects, not call with a default |
| `HarnessCompilationBlocked(field="capabilities", ...)` | caller omitted `capability_metadata`, or it's missing entries | Raised with the exact missing `capability_id` list in the message | Caller must supply metadata for every capability the Harness declares, or the Harness itself needs fewer/different `capability_requirements` |
| `HarnessCompilationBlocked(field="workflow", ...)` | caller omitted `workflow` | Raised — this is expected to fire on every call until Blocker 5 is decided and a caller is built that knows how to supply a real workflow graph | No code-level recovery until the human decision in Blocker 5 is made |
| `HarnessCompilationBlocked(field="evaluation_requirements"/"repair_laws", ...)` | caller omitted either | Raised | Caller must supply real values; see Section 11 for the proposed follow-on spec that would make these derivable instead of caller-supplied |

### Migration
This spec adds two new files. It does not modify `PortableAtomicHarnessDefinition`,
`AtomicHarnessDefinitionIntake`, or any existing Pipeline or Builder code. No
database migration, no schema version bump on either side.

### Observability
Every `HarnessCompilationBlocked` carries a `blocker_ref` pointing to this
spec's exact section, so a caller catching the exception (e.g. a future API
route) can surface the specific unresolved design decision to an operator or
log, not just a generic "compilation failed."

---

## 9. Acceptance Criteria

**AC-001 — Clean fields compile correctly when all blockers are supplied**
Given a `PortableAtomicHarnessDefinition` with `mode="activative"`,
`manifest_version="1.0.0"`, one `capability_requirements` entry, and all five
optional parameters supplied with valid values,
When `compile_portable_to_intake()` is called,
Then the returned dict has all 14 keys of `AtomicHarnessDefinitionIntake.REQUIRED_KEYS`
populated, and `AtomicHarnessDefinitionIntake().validate(result, profile)` — called
separately by the test, not by this function — succeeds without raising.
Test layer: unit — `tests/pipeline/test_harness_compiler.py::test_full_round_trip_validates`.

**AC-002 — Blocker 1 fires when semantic_dependencies is omitted**
Given a valid definition and no `semantic_dependencies` argument,
When `compile_portable_to_intake()` is called,
Then it raises `HarnessCompilationBlocked` with `field="semantic_dependencies"`
and `blocker_ref="TS-APP-BRIDGE-001#blocker-1"`.
Test layer: unit — `test_blocker_1_semantic_dependencies_required`.

**AC-003 — Blocker 2 fires when capability_metadata is missing an entry**
Given a definition with `capability_requirements=["video_editing", "audio_mix"]`
and `capability_metadata` supplying only `"video_editing"`,
When called,
Then it raises `HarnessCompilationBlocked` with `field="capabilities"` and the
message contains `"missing metadata for: ['audio_mix']"`.
Test layer: unit — `test_blocker_2_partial_capability_metadata`.

**AC-004 — Blocker 3 fires for generic mode**
Given a definition with `mode="generic"`,
When called with every other parameter valid,
Then it raises `HarnessCompilationBlocked` with `field="category_id"` before
checking any other parameter.
Test layer: unit — `test_blocker_3_generic_mode_rejected`.

**AC-005 — Blocker 4 fires for non-semver manifest_version**
Given a definition with `manifest_version="v1-draft"`,
When called,
Then it raises `HarnessCompilationBlocked` with `field="definition_version"`.
Given a definition with `manifest_version="1.0.0"`,
When called with all other parameters valid,
Then no Blocker 4 exception is raised (this half proves the check isn't
overly strict).
Test layer: unit — `test_blocker_4_semver_validation` (parametrized, both cases).

**AC-006 — Blocker 5 fires whenever workflow is omitted**
Given any valid definition and no `workflow` argument,
When called,
Then it raises `HarnessCompilationBlocked` with `field="workflow"` and
`blocker_ref="TS-APP-BRIDGE-001#blocker-5"`, regardless of what other
parameters were supplied.
Test layer: unit — `test_blocker_5_workflow_always_required`.

**AC-007 — Blocker 6 fires independently for evaluation_requirements and repair_laws**
Given a valid definition with `evaluation_requirements=None` but
`repair_laws=["x"]` supplied,
When called,
Then it raises `HarnessCompilationBlocked` with `field="evaluation_requirements"`
specifically (not `repair_laws`), proving the two checks are independent.
Test layer: unit — `test_blocker_6_independent_checks` (parametrized).

**AC-008 — Blocker 7 never blocks; invalidation_state always defaults correctly**
Given any successful compilation (all other parameters valid),
When called,
Then the returned dict's `invalidation_state` is always exactly
`"NOT_INVALIDATED"`, with no parameter able to override it (this spec does
not expose an `invalidation_state` parameter at all).
Test layer: unit — `test_blocker_7_default_always_not_invalidated`.

**AC-009 — profile_id derivation matches the existing Pipeline registry exactly**
Given a definition with `mode="activative"`,
When compiled successfully,
Then `result["profile_id"] == "portable-activative-v1"`, matching
`HarnessDefinitionProfileRegistry`'s real, unmodified entry — proving this
spec did not invent a parallel profile concept.
Test layer: unit — `test_profile_id_matches_existing_registry`.

**AC-010 — wrong_reading_locks derives from category_binding unchanged**
Given a definition whose `category_binding["wrong_reading_locks"]` is
`["lock_a", "lock_b"]`,
When compiled successfully,
Then `result["wrong_reading_locks"] == ["lock_a", "lock_b"]`, exactly, in
the same order, with no transformation applied.
Test layer: unit — `test_wrong_reading_locks_passthrough`.

**AC-011 — No modification to existing Builder or Pipeline files**
Given the pre-existing Phase 9 test suite,
When this spec's two new files are added and
`python -m pytest tests/ -q` is run,
Then all pre-existing tests still pass, and `git diff` shows zero changes
to any file outside `services/pipeline/src/cmf_pipeline/intake/harness_compiler.py`,
`harness_compiler_contracts.py`, and the new test file.
Test layer: regression.

---

## 10. Testing and Completion Evidence

### Test files to create

**`tests/pipeline/test_harness_compiler.py`**
- `test_full_round_trip_validates` — AC-001
- `test_blocker_1_semantic_dependencies_required` — AC-002
- `test_blocker_2_partial_capability_metadata` — AC-003
- `test_blocker_2_full_capability_metadata_succeeds` — positive counterpart of AC-003
- `test_blocker_3_generic_mode_rejected` — AC-004
- `test_blocker_3_activative_mode_proceeds` — positive counterpart of AC-004
- `test_blocker_4_semver_validation` (parametrized: `"1.0.0"` passes, `"v1-draft"` fails, `"1.0"` fails, `"1.0.0-beta.1"` passes) — AC-005
- `test_blocker_5_workflow_always_required` — AC-006
- `test_blocker_5_workflow_supplied_succeeds` — positive counterpart of AC-006
- `test_blocker_6_independent_checks` (parametrized: eval=None/repair=set, eval=set/repair=None) — AC-007
- `test_blocker_7_default_always_not_invalidated` — AC-008
- `test_profile_id_matches_existing_registry` — AC-009
- `test_wrong_reading_locks_passthrough` — AC-010

### Test fixture strategy
Build a real `PortableAtomicHarnessDefinition` via `.create()` (not a mock),
using a minimal valid `normalized` mapping and `category_binding` matching
`_valid_category_binding`'s exact required-key set — so tests exercise the
real class's real validation, not a stand-in. This matches the existing
codebase's own testing convention of using real objects wherever the object
construction itself is cheap and deterministic.

### Pre-existing regression
```bash
python -m pytest tests/ -q --tb=short
```
Zero new failures is a hard gate, per AC-011.

### Build Receipt claim ceiling
`HARNESS_COMPILER_PARTIAL_BRIDGE_EVIDENCE`

This spec does not claim:
- Gap 4 (from `SPEC_GAP_LEDGER.md`) is fully closed
- Blocker 5 (workflow derivation) has a final answer — it is escalated, not decided
- a `CapabilityMetadataRegistry` exists (Section 11 names it as future work)
- any caller (API route, campaign creation flow) actually supplies real
  `semantic_dependencies`, `capability_metadata`, or `workflow` values yet —
  that is the next integration spec's job, once Blocker 5 has a human answer

---

## 11. Recommended Follow-On Work (Not Built Here)

1. **A human decision on Blocker 5** is the single highest-priority next
   step. Until it exists, this compiler will raise `HarnessCompilationBlocked`
   on every real call, by design. The three options in Section 4 are laid
   out for that decision, not to be chosen by an implementing agent.
2. **`CapabilityMetadataRegistry`** (Blocker 2) — a small, separate,
   probably Pipeline-owned lookup service mapping `capability_id` to
   `owner_kind`/`required_features`/`authority_boundary`, so future callers
   don't need to hand-supply this metadata on every compilation.
3. **Revisit whether `semantic_dependencies` (Blocker 1) should instead be
   populated by GAP-001's proposed `TS-APP-API-007` (Activative Intelligence
   API)** — once that spec exists and can supply real
   `final_script_ref`/`archetype_coalition_ref`/etc. as proper `ImmutableRef`
   objects, those may be exactly the right values for this parameter,
   closing Blocker 1 and GAP-001 together rather than separately.
4. **Correct TS-APP-API-002.md's Gap 4 file citation** the next time that
   spec is touched, per the Source Gap Notice in Section 1 above.

---
spec_end: true
next_spec: A human decision on Blocker 5, then TS-APP-API-007 (Activative Intelligence API, per SPEC_GAP_LEDGER.md GAP-001)
prerequisite_for_next: This spec's AC-001 through AC-011 passing does not unblock real Harness execution by itself — Blocker 5's resolution is still required before any caller can supply a real workflow graph
