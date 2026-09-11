---
document_class: CANDIDATE_CANONICAL_TECH_SPEC
spec_id: TS-AIR-006
title: Archetype Coalition and Psychological Role Inside a Tension
product: Activative Intelligence Runtime
version: 2.1.0-candidate
date: 2026-07-22
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
build_state: NOT_BUILD_READY
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
writing_wave: 3
output_path_class: DIRECT_PRODUCT_SPEC_PATH
controlling_frs:
  - AIR-FR-031
  - AIR-FR-032
  - AIR-FR-033
  - AIR-FR-034
  - AIR-FR-035
  - AIR-FR-036
  - FR-163
  - FR-165
controlling_stories:
  - AIR-ST-06.01
  - AIR-ST-06.02
  - AIR-ST-06.03
  - ST-12.01
  - ST-12.02
draft_dependencies:
  - spec_id: TS-AIR-002
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: 258c711d84dbbf2e8abc79e910d825cb8370dd0b7e0940e81d91d8a93e1b43e5
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
  - spec_id: TS-AIR-005
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: 5dcf631efc4f68f40edd0991ca3ae4be9073da68aa441c52d37e874e70a43e49
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
---

# TS-AIR-006 — Archetype Coalition and Psychological Role Inside a Tension

This document is authorized for specification writing only under the Prompt 02C recovery chain. It is not current authority, implementation authorization, build readiness, production authority, or a Development Capsule. AIR-002 and AIR-005 are consumed only as exact hash-pinned `WRITTEN_PENDING_AUDIT` interfaces and are labelled `DRAFT_DEPENDENCY_NOT_ACCEPTED` throughout.

## 1. Files and authorities read

| Class | Exact file | State / SHA-256 | Specific use |
|---|---|---|---|
| Writer law | `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | V3.3; `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | One-spec scope, ten sections, source evidence and writer ceiling. |
| Source-package instructions | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/AGENTS.md` | `fb2836248358c69474cef24d925608534e7da87ec88041b3e9d660039fcc4732` | Requires source, Primitive and ownership lock before normative writing. |
| Frozen packet | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | recovery authorized; `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Exact FRs, Stories, path authority and dependency policy. |
| Dispatch lock | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_03_DISPATCH_LOCK.yaml` | dispatched; `e8137e45a267767fd3e0b2f5bdc278ac66d570187b34b4a48ef282db84bdca65` | Admits only AIR-002 and AIR-005 to this writer. |
| Authority stage | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | ratification pending; `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Candidate remains non-current and cannot receive build authority. |
| Write authorization | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | specification work only; `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Authorizes writing and later technical review, not build. |
| Candidate product authority | `.../CURRENT_AUTHORITY.md` | `DRAFT_FOR_HUMAN_RATIFICATION`; `493fd0f21661ca136e72e1136586703be9c48e443a4dd5056d0413ba18501bf0` | AIR owns semantic activation programs; Pipeline executes them. |
| Candidate constitutional root | `.../doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | `2.1.0-draft`; `abdb79fa6a59b4651332cd86cf51f796a4468110c917c126c62760e3f1d58a85` | Role-inside-tension law; Primitive coalition before archetype; SDA/SFL evidence status. |
| Program ownership | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate; `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | AIR owns archetype coalition and downstream semantic meaning. |
| Cross-product boundary | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate; `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | Pipeline may not reinterpret source, Edge Product, Primitive coalition or Final Script. |
| Upstream draft | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-002.md` | `WRITTEN_PENDING_AUDIT`; `258c711d84dbbf2e8abc79e910d825cb8370dd0b7e0940e81d91d8a93e1b43e5`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Exact Matrix, Broad Signal, tension-site, source and epistemic interface assumptions. |
| Upstream draft | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-005.md` | `WRITTEN_PENDING_AUDIT`; `5dcf631efc4f68f40edd0991ca3ae4be9073da68aa441c52d37e874e70a43e49`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Exact Primitive coalition, signature, Edge Product, routeability and evaluation interface assumptions. |
| Primary full draft | `.../specs/TS-AIR-006-archetype-coalition-and-psychological-role-inside-tension.md` | `DRAFT_AFTER_PRD_PENDING_RATIFICATION`; `158696ad8f135c3bb52f225d85174bdc5daeb2afa261ee6a82a60e556c9f1c52` | Existing implementation-grade baseline amended to current ownership and deterministic law. |
| Controlling feature | `.../prd/features/F06-archetype-coalition-and-psychological-role-inside-tension.md` | candidate; `62b6e7e9dfb5cf5201abac9026faa5b77beee485030b6389e40520a0bad0228f` | AIR-FR-031–036 and F06 terminal state. |
| AIR Stories | `.../planning/EPICS_AND_VERTICAL_STORIES.md` | candidate; `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45bdb8df2010592fd7da0` | AIR-ST-06.01–06.03, CBAR and recovery expectations. |
| AHP Stories | `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/planning/EPICS_AND_VERTICAL_STORIES.md` | candidate; `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | FR-163/ST-12.01 and FR-165/ST-12.02. |
| Required doctrine | `.../sources/doctrine/F28-psychological-role-archetype-coalition-and-final-script-authority.md` | SRC-AHP-F28-001; `0a130c459707e309ae323f769b00d0f82f866b8bfddf6eb42546a5de4f78370c` | Role/tension, archetype coalition and Final Script sequence. |
| Archetype evidence | `.../sources/doctrine/CCP_ARCHETYPE_SYSTEM_MIGRATION_PROPOSITION.md` | SRC-ARCH-001/SRC-DOCT-002; `2d7aa11b72c83a95d9240784978e3b9af4944a3e037f18746f8b204bc3287188` | Separates Core Content Archetypes from Asset Derivative schemas and render routes. |
| Archetype prompt snapshot | `.../sources/cmf_archetype_prompt_snapshot/SOURCE_SNAPSHOT_MANIFEST.json` | SRC-ARCH-002 aggregate digest `2dc58719949f1da027f20253baa74dd88b82ea20d39bc0aa63201c4ffeb8bcf6`; manifest SHA `f9fe32e59bbeb685a1e613af8abb2fb1c36524930acb573f5daca525a2edf99a` | Exact historical prompt members are evidence, not live profiles. |
| SDA snapshot | `.../sources/cmf_sda_registry_snapshot/SOURCE_SNAPSHOT_MANIFEST.json` | SRC-SDA-001 digest `ded8e22b39a4bbefa394b86a7b379f880ef83f56c8f901b12eb5dfac5f642200`; manifest SHA `d9012f38f869dbaba5742e8eefe27e33f6a8b1be2ea9df2f3016b7566bd8676f` | Exact geometry, invariant and crosswalk evidence. |
| SFL snapshot | `.../sources/cmf_sfl_registry_snapshot/SOURCE_SNAPSHOT_MANIFEST.json` | SRC-SFL-001 digest `327cc36abee9428e416fab6b4d1880a26c02bf4082b16a52f6184c7dfdbb7ad1`; manifest SHA `c5e1dbf182743276a577bd2e915030eb32b5731d1f268c1d2ba3fb07dfb63aa0` | Exact surface-function, compression, crosswalk and failure-corpus evidence. |
| Controlled variation | `.../sources/doctrine/CCV_COMBINATORIAL_CONTROLLED_VARIATION.md` | SRC-DOCT-005; `0869ff50e4bdaba3dc1854183100826d0de9568b9ed5558bf68b4590834a62c4` | Controlled variation preserves coalition and rejects centroid blending. |
| Source routing evidence | `.../sources/doctrine/CCP_V9_1_EXPRESSION_CAPTURE_ARCHETYPE_ROUTING.md` | SRC-INT-002/SRC-INT-003; `58e92fee3f9486ab524d1229c4759566f760b6cc91472aff279e457b0b52482b` | Expression Moment provenance and historical route metadata. |
| Candidate schemas | `.../contracts/schemas/psychological_role_tension_contract.schema.json`; `.../contracts/schemas/archetype_coalition_program.schema.json` | `c4dec03ff25a57b47013afec50f10f212fc7d83854eaa064e56446f3ccc8272b`; `7b547dcdd02198597570f78b519b8a4fde76f64495d8f5bca7c5d401c563a751` | Closed candidate shapes needing lifecycle, typed geometry and deterministic extensions. |
| Candidate examples | `.../examples/25_psychological_role_tension_contract.json`; `.../examples/26_archetype_coalition_program.json` | `4eb8cd1dd3f75ce28e5dadee74a13e72bca3883ebc66d8968409ea2b5bfb45d3`; `754b2c9b2dd542671545852986861dbaf2ed3b2d811364a3d1821d9cc7337942` | Concrete source-backed role and recognition-story coalition evidence. |
| Brownfield compiler | `THE_CMF_STUDIO(2)/src/ccp_studio/services/archetype_subsystem_compiler_service.py` | predecessor; `510cd7ec05485f397e3f371c396f98654c2e901cc5f6b1c67aa38810175eae0d` | Thin story-doctor chain currently conflates score, archetype program and delivery recipe. |
| Brownfield route service | `THE_CMF_STUDIO(2)/src/ccp_studio/services/routing_service.py` | predecessor; `97e2be50b1bcc7421889f2b74e89b25c8638164c50fb63a5182573df9affe7cf` | Active-entry filtering and source-insufficient denial, but non-atomic mutable repository writes. |
| Brownfield contracts/tests | `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/routing.py`; `THE_CMF_STUDIO(2)/tests/cmf_studio/test_archetype_and_asset_derivative_routing.py` | `59b128a377abe43439961f4e4ca5242d3ac891fa59cbf3829b641d510e99c1cf`; `04d2dec22580098e6979e316b14b4490b761cd7f072a8da99cfb59d0c6ab0b15` | Useful typed rejection/receipt cases; random IDs/times and path injection prevent canonical reuse. |

The `...` prefix expands to the AIR V2.1 full-bundle root. Active Primitive pins are PRM-PSY-001 SHA `77c09b403aca66e77b2c71b1faa4dbeacd410d9d6c69685f9c2222dc65bf8ca7`, PRM-PRS-002 SHA `4fba8edcb439c296a610b53a45ce76b9a002b4a128338e3302ddbb1cc49e242e`, and PRM-HUM-021 SHA `53712577ba9f27112afce11fd022a94033f44ceca5f910c6eec2e3c8fae39253`.

AIR-002 and AIR-005 govern draft interface details in sections 3, 5, 6, 8, 9 and 10. A byte change to either pin reopens all six sections before this draft may advance.

## 2. Problem, user outcome, solution, and scope

### Problem and outcome

An archetype selected by popularity, filename, topic similarity or familiar prompt form can be polished while giving the viewer no participation position. It can also flatten the approved Edge Product into a safe template centroid, conflate meaning geometry with a derivative format, or allow mutually incompatible archetypes to compete. The operator instead needs an inspectable AIR-owned program that proves why a source-backed Edge Product belongs in a particular Core Content Archetype, which psychological role the person enters inside which tension, how supporting/transition archetypes cooperate without blending, and which exact SDA/SFL evidence preserves function through derivative routing.

### Bounded solution

AIR consumes exact AIR-002 Matrix/tension evidence and AIR-005 coalition/signature/Edge Product refs. It resolves historical archetype, SDA and SFL evidence through exact versioned registry adapters; proposes and independently evaluates bounded archetype routes; compiles an immutable `PsychologicalRoleTensionContract` and `ArchetypeCoalitionProgram`; and emits an `ArchetypeRouteReceipt` containing alternatives, approval state and full lineage. Deterministic hard gates run before ranking or model judgment. Pipeline may execute an eligible semantic route but cannot reconstruct it.

### In scope

- source-supported Core Content Archetype and semantic derivative-route references;
- explicit participant/viewer role, tension, recognition path, stance, intended movement and participation threshold;
- primary, supporting, transition and excluded archetype bindings with anti-centroid conflict checks;
- exact SDA/SFL snapshot/profile refs and route-evidence receipts;
- immutable commands, events, repository transactions, replay, supersession and selective invalidation;
- typed operator review and HumanResolution evidence without hidden state mutation.

### Out of scope and non-goals

- generating or approving the Guest Voice DNA Final Script, composition, editing, render, production route or visual assets;
- creating an archetype from a prompt filename or making historical prompts live authority;
- redefining AIR-002 Matrix objects or AIR-005 Primitive coalition/Edge Product meaning;
- letting Pipeline, Builder, VAE, Studio, Delegation, a renderer or a model own AIR semantic acceptance;
- activating Format 02, VAE Stage 5, code, schemas, shared release bytes, a Development Capsule, build, production or certification.

## 3. Governing decisions and constraints

1. **Role inside tension is the activation gate.** An audience-facing route is not Activative unless it names who the person becomes, what unresolved pressure makes that role meaningful, how recognition occurs, the stance, smallest participation threshold, counteractivation roles and must-survive transfer invariants.
2. **AIR owns semantic geometry.** AIR owns role/tension, Core Content Archetype, archetype coalition, SDA/SFL semantic binding and route-receipt meaning under the candidate ownership ledger. Pipeline executes exact approved refs; Builder declares dependencies; VAE realizes typed visual demands; Studio projects state and captures commands.
3. **Draft inputs remain drafts.** AIR-002 and AIR-005 are `DRAFT_DEPENDENCY_NOT_ACCEPTED`. No field from either is represented as ratified law.
4. **Primitive coalition precedes archetype eligibility.** A route requires an exact AIR-005 coalition, signature, Edge Product and passing Primitive evaluation. An archetype cannot supply missing Primitive meaning or rescue an ineligible Edge Product.
5. **Draft role/tension ambiguity is explicit.** AIR-005 currently carries a `psychological_role_tension_ref` while F06 owns the terminal `PsychologicalRoleTensionContract`. This specification interprets the upstream ref only as exact role/tension hypothesis or evidence lineage, not as the F06 terminal object. If independent audit determines AIR-005 requires the F06 terminal contract as its own prerequisite, `AIR_ARCH_DRAFT_INTERFACE_CYCLE` blocks acceptance and the affected sections must be revised; no circular seed is invented.
6. **Archetypes are meaning/sequence geometry, not format or render routes.** `CoreContentArchetypeRef` identifies semantic structure. `DerivativeArchetypeRef` identifies a semantic derivative route and category scope. Provider/render/production routing remains downstream-owned.
7. **One primary, bounded support.** Every coalition has exactly one primary archetype. Supporting and transition archetypes have distinct local functions and explicit compatibility. Unbounded hybridization and centroid blending are illegal.
8. **Source fills geometry.** Every archetype beat/function required for eligibility maps to exact source evidence, Expression Moment, Matrix, Edge Product or operator-confirmed assertion. Missing material remains absent and blocks a claim that needs it.
9. **Historical prompt evidence is not authority.** Prompt members, Studio registry entries and migration prose are candidate evidence. Name similarity, old popularity and prior route success do not make a current route eligible.
10. **SDA/SFL are exact evidence refs.** Route bindings pin snapshot digest, artifact ID/version/hash, crosswalk decision and applicable constraints. Historical snapshots do not become current production profiles without ratification.
11. **Controlled variation preserves geometry.** CCV may vary declared axes only. It cannot change role, tension, Edge Product, required archetype functions, source truth or wrong-reading/anti-centroid locks.
12. **Producer cannot approve itself.** Deterministic validation and independent evaluation precede attributable operator approval where the active route policy requires it. Approval state is explicit, never inferred from a passing model score.
13. **`NOT_APPLICABLE` cannot hide missing route proof.** Required role/tension, primary archetype, Edge Product, Primitive coalition, SDA, SFL, category and source-fit dimensions cannot be N/A. Conditional checks need an exact profile rule and evidence.
14. **Final Script authority remains downstream.** F06 supplies approved semantic geometry to F07. It does not write, approve or simulate the Guest Voice DNA Final Script.
15. **Canonical identity is portable.** No current time, randomness, environment, absolute path, filesystem traversal order or insertion-order accident enters canonical bytes.
16. **Claim ceiling.** While ratification remains pending, this document stays `WRITTEN_PENDING_AUDIT`; no later state may exceed `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`, and build/capsule authority remains false.

## 4. Current brownfield architecture

| Artifact | Actual behavior | Disposition | Constraint |
|---|---|---|---|
| AIR candidate role/tension schema | Closed basic strings/refs, but no version/hash, authority, epistemic assertions, typed counteractivation, lifecycle or supersession. | `ADAPT` | Preserve example meaning; add immutable shared refs and closed types. |
| AIR candidate coalition schema | Primary/supporting bindings, category, sequence, anti-centroid and wrong-reading fields. | `ADAPT` | Replace embedded role contract and free strings with exact refs/typed decisions; add transition/excluded roles, SDA/SFL and receipts. |
| Archetype prompt snapshot | Exact historical prompts and variants. | `ARCHIVE_AS_EVIDENCE` plus selective `ADAPT` into registry candidates | Prompt text never runs as hidden current authority. |
| SDA snapshot | Typed geometry, invariants and crosswalk members, including float weights. | `ACTIVATE_AS_HASH_LOCKED_EVIDENCE` | Runtime candidate contract converts governed decimal values to integer micros; production profile still needs ratification. |
| SFL snapshot | Functions, families, compression rules, crosswalks and failure corpus. | `ACTIVATE_AS_HASH_LOCKED_EVIDENCE` | Preserve exact member hashes; never infer function from archetype name alone. |
| `ArchetypeSubsystemCompilerService` | Chains story-doctor score, program and delivery recipe without typed authority or receipts. | `REPLACE` for current semantic compilation | A delivery recipe cannot be emitted inside the semantic owner as a side effect. |
| Studio `RoutingService` / routing contracts | Filters active entries, rejects weak source/unsupported formats and emits receipts through mutable in-memory writes. | `ADAPT` as regression and adapter evidence | Replace UUID4/time, open payloads, sequential partial writes and Studio ownership. |
| Studio route tests | Cover active-entry filtering, source denial, unsupported format, lineage and command receipt. | `REUSE` as regression seeds | Add role/tension, coalition, SDA/SFL, determinism, atomicity, replay and sovereignty cases. |

Migration never turns an old prompt, filename, route string or open registry payload directly into an approved F06 object. A versioned migration either proves each required field from exact evidence and emits a proposed immutable object, or returns a typed blocker while preserving original bytes and aliases.

## 5. Proposed architecture and workflows

### Components

| Component | Responsibility | Forbidden responsibility |
|---|---|---|
| `ArchetypeEvidenceRegistryAdapter` | Resolve exact historical archetype, SDA, SFL and migration evidence by digest/member hash. | Promote a prompt or snapshot to current authority. |
| `RoleTensionCompiler` | Compile source-backed role, tension, recognition, stance, movement, participation and counteractivation. | Invent missing source or overwrite AIR-002/AIR-005. |
| `ArchetypeCandidateResolver` | Propose Core Content and derivative-route candidates after hard source/category/function filters. | Select by name/popularity alone or choose production route. |
| `ArchetypeCoalitionCompiler` | Bind one primary plus bounded support/transition functions and explicit exclusions. | Average geometry conflicts or mutate Primitive coalition. |
| `SDASFLRouteBinder` | Resolve exact geometry/function members, crosswalks and constraints. | Treat historical snapshot as ratified production profile. |
| `ArchetypeRouteEvaluator` | Independently evaluate source fit, role/tension, Edge fit, coalition geometry, SDA/SFL and wrong readings. | Produce or approve its own subject. |
| `ArchetypeProgramRepository` | Atomic immutable artifacts, commands, events, edges and receipts; replay and invalidation. | Overwrite history or store receipt/artifact without parity. |

### Workflow A — compile role/tension contract

1. Accept `CompilePsychologicalRoleTensionCommand` with caller-supplied ID/time, idempotency key, expected stream version, actor/authority refs, activation domain, exact AIR-002 Matrix/tension refs, AIR-005 coalition/signature/Edge Product/evaluation refs, source evidence refs and profile ref.
2. Resolve all refs by ID/version/SHA-256; reject stale, invalidated, unsupported or cross-scope inputs. The Edge Product must be eligible and distinct from its Broad Signal.
3. Derive candidate role/tension only from evidenced pressure, role at stake, intended movement and source/audience context. Preserve planned, observed, inferred and operator-confirmed assertions separately.
4. Validate recognition path, stance, participation threshold, counteractivation roles and transfer invariants. A topic label or generic motivation fails.
5. Atomically commit candidate contract, decisions, dependency edges, event and receipt. It remains proposed until independent evaluation and required human resolution.

### Workflow B — resolve and compile archetype coalition

1. `ResolveArchetypeRouteCommand` pins the exact role/tension contract, AIR-005 objects, category, semantic derivative-route scope, archetype evidence snapshot, SDA/SFL snapshots and evaluation profile.
2. Filter before ranking: source material coverage, Edge/role/tension fit, Primitive compatibility, activation domain, category support, SDA geometry, SFL functions, wrong-reading locks and lifecycle validity.
3. Preserve every candidate and rejection reason. Rank only surviving candidates; similarity cannot override a hard gate.
4. Bind exactly one primary archetype. Add a support or transition archetype only when it performs a distinct required function and passes pairwise geometry compatibility. Excluded candidates remain typed evidence.
5. Bind exact SDA/SFL artifact refs plus crosswalk decisions. Compile sequence logic for temporal categories or reading logic for static categories as a tagged union.
6. Atomically commit proposed `ArchetypeCoalitionProgram`, dependency edges, event and compile receipt.

### Workflow C — evaluate, review and route

1. An independently identified evaluator loads the exact proposed bytes and dependency snapshot.
2. Deterministic gates precede judgment. Findings remain separate for source fit, Edge Product fidelity, role/tension, Primitive coalition, archetype compatibility, SDA geometry, SFL function, category/route scope, counteractivation, anti-centroid and wrong-reading behavior.
3. A fatal failure blocks route eligibility and attributes repair to source, Matrix, Primitive coalition, role/tension, archetype binding, category or later layer. Scores never compensate.
4. If operator approval is required, Studio submits a typed `ResolveArchetypeRouteCommand`; AIR validates authority and appends a HumanResolution ref. UI manipulation alone changes no canonical state.
5. AIR emits `ArchetypeRouteReceipt` with approval state, alternatives, evaluation and exact handoff refs. Pipeline receives immutable semantic route refs only.

### Workflow D — idempotency, concurrency, cancellation and replay

- Same idempotency key plus same canonical command hash returns the original receipt/hashes. Different bytes emit `AIR_ARCH_IDEMPOTENCY_CONFLICT` and write nothing.
- Stale `expected_stream_version` emits `AIR_ARCH_CONCURRENT_MODIFICATION`; no partial artifacts appear.
- Cancellation before commit records a cancellation receipt without semantic output. A post-commit cancellation reports already committed and cannot erase history.
- Replay uses exact historical source/registry/profile versions and reproduces canonical bytes. It never substitutes a newer prompt or crosswalk.
- Supersession appends a successor and deterministic dependency traversal. Only typed descendants become stale; unrelated routes and historical outputs remain reproducible.

## 6. Data models, contracts, schemas, and APIs

All schemas reject unknown fields, require non-empty semantic strings, use exact enums, immutable tuples and explicit optionality. Canonical serialization is UTF-8 without BOM, Unicode NFC, LF, sorted object keys, declared tuple order, lowercase SHA-256 and no insignificant whitespace. Set-like refs are deduplicated and sorted by canonical ref URI. Scores/weights are integer micros; NaN, Infinity and identity-bearing binary floats are forbidden.

Shared immutable, authority, actor, epistemic and lifecycle types are imported by exact draft schema/hash from AIR-002. Coalition/signature/Edge Product/evaluation refs are imported by exact draft schema/hash from AIR-005. No copied local fork is permitted.

### `CoreContentArchetypeRef` — `ca.air.core-content-archetype-ref/2.1.0-candidate`

Required fields: `archetype_id`, `version`, `member_sha256`, `registry_snapshot_ref`, `canonical_name`, `meaning_geometry_ref`, `required_source_material`, `required_beat_or_reading_functions`, `compatible_derivative_route_refs`, `known_failure_refs`, `migration_evidence_refs`, `lifecycle_state`, `authority_ref`, `canonical_hash`.

The ref is eligible only when the exact member exists under the pinned snapshot and its candidate/adopted lifecycle is explicit. `canonical_name` is display data, never identity.

### `DerivativeArchetypeRef` — `ca.air.derivative-archetype-ref/2.1.0-candidate`

Required fields: `derivative_route_id`, `version`, `registry_snapshot_ref`, `category_id`, `route_scope`, `semantic_function_refs`, `compatible_core_archetype_refs`, `required_source_material`, `required_category_grammar_refs`, `unsupported_route_conditions`, `authority_ref`, `canonical_hash`.

This is a semantic derivative route. It cannot contain provider, model, LoRA, render workflow or VAE production-route selection.

### `PsychologicalRoleTensionContract` — `ca.air.psychological-role-tension-contract/2.1.0-candidate`

Required fields: `contract_id`, `version`, `activation_domain`, `matrix_ref`, `tension_site_refs`, `primitive_coalition_ref`, `coalition_signature_ref`, `edge_product_ref`, `source_evidence_refs`, `role`, `tension`, `recognition_path`, `stance`, `intended_movement`, `enabled_action_or_recognition`, `participation_threshold`, `counteractivation_roles`, `transfer_invariants`, `wrong_reading_locks`, `epistemic_assertions`, `evaluation_profile_ref`, `authority_ref`, `lifecycle_state`, `supersedes_ref`, `canonical_hash`.

`participation_threshold` is a typed action/recognition rule, not an unstructured threshold string. `counteractivation_roles` may be empty only when the evaluation profile records an evidenced `NONE_OBSERVED` finding; unknown is not empty. The upstream AIR-005 role/tension ref, if present, is recorded as evidence lineage and cannot point to this contract before it exists.

### `ArchetypeBinding`

Required fields: `binding_id`, `archetype_ref`, `coalition_role` (`PRIMARY`, `SUPPORT`, `TRANSITION`), `local_function`, `role_tension_fit`, `edge_product_fit`, `source_coverage_decisions`, `primitive_compatibility_refs`, `sda_geometry_refs`, `sfl_function_refs`, `category_geometry_ref`, `activation_domain`, `rejection_conditions`, `evidence_refs`, `canonical_hash`. Exactly one binding is `PRIMARY`.

### `ArchetypeCoalitionProgram` — `ca.air.archetype-coalition-program/2.1.0-candidate`

Required fields: `program_id`, `version`, `role_tension_contract_ref`, `primitive_coalition_ref`, `coalition_signature_ref`, `edge_product_ref`, `primary_binding`, `supporting_bindings`, `transition_bindings`, `excluded_candidate_decisions`, `source_expression_refs`, `category_id`, `derivative_route_ref`, `composition_logic`, `sda_refs`, `sfl_refs`, `pairwise_compatibility_decisions`, `anti_centroid_locks`, `wrong_reading_locks`, `evaluation_profile_ref`, `authority_ref`, `lifecycle_state`, `dependency_refs`, `supersedes_ref`, `canonical_hash`.

`composition_logic` is a tagged union: `TemporalSequenceLogic{ordered_function_refs, transition_conditions}` or `StaticReadingLogic{ordered_attention_refs, adjacency_constraints}`. It states semantic function, not layout or edit instructions. Empty support/transition tuples are valid and preferable to ceremonial hybridization.

### `SDARef` and `SFLRef`

Each contains `artifact_id`, `artifact_class`, `version`, `member_sha256`, `snapshot_digest`, `crosswalk_decision_ref`, `applicability_evidence_refs`, `constraints`, `lifecycle_state`, and `canonical_hash`. Historical snapshot lifecycle is `HASH_LOCKED_EVIDENCE`; it is not `CURRENT_PRODUCTION_PROFILE`. Decimal weights from evidence are normalized to governed integer micros during migration with the original lexeme and member hash retained in the migration receipt.

### `ArchetypeRouteReceipt` — `ca.air.archetype-route-receipt/2.1.0-candidate`

Required fields: `receipt_id`, `program_ref`, `role_tension_contract_ref`, `edge_product_fit_finding_ref`, `coalition_structure_refs`, `sda_sfl_resolution_refs`, `source_lineage_refs`, `accepted_route_ref`, `rejected_alternative_decisions`, `deterministic_gate_receipt_ref`, `independent_evaluation_receipt_ref`, `approval_state`, `approval_authority_ref`, `human_resolution_ref`, `downstream_limitations`, `dependency_edge_refs`, `command_record_ref`, `repository_transaction_id`, `canonical_hash`.

`approval_state` is `PROPOSED`, `EVALUATED`, `OPERATOR_APPROVED`, `REJECTED`, or `SUPERSEDED`. A passing evaluator does not create `OPERATOR_APPROVED`; absence of required approval is not N/A.

### Commands, events, states and repository APIs

- Commands: `CompilePsychologicalRoleTensionCommand`, `ResolveArchetypeRouteCommand`, `EvaluateArchetypeRouteCommand`, `ResolveArchetypeRouteApprovalCommand`, `SupersedeArchetypeProgramCommand`, `CancelArchetypeCommand`, `ReplayArchetypeProgramCommand`.
- Events: `PsychologicalRoleTensionCompiled`, `ArchetypeRouteProposed`, `ArchetypeCoalitionCompiled`, `ArchetypeRouteEvaluated`, `ArchetypeRouteResolved`, `ArchetypeProgramSuperseded`, `ArchetypeDescendantsInvalidated`, `ArchetypeCommandCancelled`.
- Repository transaction: `append(expected_stream_version, command_record, artifacts, events, dependency_edges, receipts) -> CommitResult`.
- Read API: `get_exact(ref)`, `get_receipt(ref)`, `get_command(command_id)`, `list_dependencies(ref)`, `list_descendants(ref, edge_types)`, `replay(stream_id, through_version)`, `find_by_idempotency_key(key)`.
- Service result is a closed union: `Committed`, `Replayed`, `Blocked`, or `Cancelled`. Semantic failures are typed receipts, not bare exceptions.

No state may commit without its corresponding command, event, dependency edges and receipt; no success receipt may commit without every referenced artifact.

## 7. Implementation stages and exact target paths

These are proposed future paths only. Ratification, independent acceptance, a bounded Development Capsule and separate build authorization are required before creation.

| Stage | Exact future paths | FR / evidence boundary |
|---|---|---|
| 1 — domain kernel | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/psychological_role_tension.py`; `domain/archetype_coalition.py`; `domain/archetype_registry_refs.py` | AIR-FR-031–035, FR-163, FR-165; pure closed invariants. |
| 2 — schemas/fixtures | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/air.psychological-role-tension.schema.json`; `air.archetype-coalition-program.schema.json`; `air.archetype-route-receipt.schema.json`; `contracts/fixtures/air_f06/` | Schema/model parity, positive/negative canonical vectors; no release bytes. |
| 3 — registry adapters | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/adapters/archetype_evidence_registry.py`; `adapters/sda_registry.py`; `adapters/sfl_registry.py` | AIR-FR-031, AIR-FR-035; exact digest/member resolution. |
| 4 — repository/services | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/ports/archetype_program_repository.py`; `repositories/archetype_program_repository.py`; `services/archetype_program_service.py` | All eight FRs; atomicity, idempotency, concurrency, replay/invalidation. |
| 5 — independent evaluation | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/evaluation/archetype_route_evaluator.py` | AIR-FR-033–036; independent non-compensable findings. |
| 6 — migration/handoff | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/migrations/cmf_archetype_route_v1_to_air_f06.py`; `adapters/pipeline_archetype_program_adapter.py`; `projections/studio_archetype_review.py` | FR-165 and AIR-FR-036; lossless-or-blocked migration and sovereign handoff. |
| 7 — tests/evidence | Exact paths in section 10 | Every criterion, CBAR case, draft caveat and claim ceiling. |

No stage writes the F07 Final Script, Pipeline execution, Builder harness, VAE production plan, Studio canonical state, Delegation release or Format 02 activation.

## 8. Failure, migration, rollback, recovery, and observability

### Typed failures

| Code | Condition | Required outcome |
|---|---|---|
| `AIR_ARCH_DRAFT_INTERFACE_HASH_MISMATCH` | AIR-002 or AIR-005 differs from the dispatch pin. | Stop and reopen all six revision-impact sections. |
| `AIR_ARCH_DRAFT_INTERFACE_CYCLE` | AIR-005 is interpreted to require the terminal F06 contract as its prerequisite. | Block acceptance; request bounded interface decision, invent no seed. |
| `AIR_ARCH_SOURCE_OR_EDGE_STALE` | Source, Matrix, coalition, signature, Edge or evaluation ref is stale/invalid. | Reject before candidate routing. |
| `AIR_ARCH_ROLE_TENSION_UNSUPPORTED` | Role/tension/recognition/movement lacks exact evidence. | Reject; do not create generic role language. |
| `AIR_ARCH_ARCHETYPE_MEMBER_UNRESOLVED` | Candidate resolves only by name or missing snapshot/member hash. | Reject candidate. |
| `AIR_ARCH_SOURCE_COVERAGE_INCOMPLETE` | Required archetype function cannot be filled from eligible source. | Reject or retain as non-eligible candidate. |
| `AIR_ARCH_PRIMARY_COUNT_INVALID` | Zero or multiple primary bindings. | Reject coalition. |
| `AIR_ARCH_GEOMETRY_CONFLICT` | Support/transition binding conflicts with primary or Edge Product. | Reject conflicting binding/program; never average. |
| `AIR_ARCH_CENTROID_BLEND` | Coalition smooths source-specific force or role/tension into generic form. | Reject under anti-centroid gate. |
| `AIR_ARCH_SDA_SFL_UNRESOLVED` | Exact artifact, digest, crosswalk or applicability is missing. | Block route; no filename inference. |
| `AIR_ARCH_CATEGORY_ROUTE_UNSUPPORTED` | Semantic derivative route/category pair lacks governed support. | Reject without selecting a production fallback. |
| `AIR_ARCH_NA_INVALID` | Required route dimension is marked N/A or lacks condition evidence. | Reject receipt. |
| `AIR_ARCH_EVALUATOR_NOT_INDEPENDENT` | Producer and evaluator share unapproved authority context. | Reject route eligibility. |
| `AIR_ARCH_APPROVAL_REQUIRED` | Policy requires attributable operator approval and none exists. | Keep `EVALUATED`; do not project eligible approval. |
| `AIR_ARCH_IDEMPOTENCY_CONFLICT` | Same key, different canonical command bytes. | Return conflict and write nothing. |
| `AIR_ARCH_CONCURRENT_MODIFICATION` | Expected stream version is stale. | Return current ref; no partial write. |
| `AIR_ARCH_ATOMIC_COMMIT_FAILED` | Artifact/event/edge/receipt commit fails. | Roll back complete transaction. |
| `AIR_ARCH_MIGRATION_MEANING_MISSING` | Legacy prompt/route lacks required typed meaning/evidence. | Preserve bytes and emit migration blocker. |

### Migration and compatibility

- Historical prompt, route, schema and receipt bytes remain readable and hash-verifiable. Migration creates new immutable candidate artifacts linked by `migrated_from`; it never edits history.
- An old prompt is decomposed into candidate meaning geometry, source requirements, beat/function evidence and failure constraints only when each field is attributable. Missing role/tension, coalition, SDA/SFL or authority is not guessed.
- Legacy random UUID/time values remain historical identifiers. New canonical identity is content-derived or caller-supplied.
- Adapters preserve every constraint. Parsing old route strings without enforcing source, role/tension and geometry is incompatible.
- Active delegations/handoffs remain pinned to versions/profile accepted at submission. Deprecation does not invalidate historical replay.

### Retry, rollback, recovery and late results

Infrastructure retries use the same idempotency key; quality failures require a new command linked to the blocker. A late evaluator result is accepted only for the exact still-valid subject/profile bytes; otherwise it is retained as stale evidence and cannot change status. Deployment rollback selects a last-known-good service/registry/profile for new work but preserves every prior output. Recovery checks artifact/command/event/edge/receipt parity and quarantines orphans. Selective repair reruns only the responsible layer and typed descendants.

### Observability

Structured telemetry records command/trace IDs, exact dependency/profile digests, candidate/filter counts, role/tension finding codes, primary/support/transition counts, geometry conflict codes, SDA/SFL IDs, category/route decisions, approval state, idempotent replay, stream version, commit outcome, invalidation count and repair owner. Logs exclude source payloads, absolute machine paths, secrets, environment values and unbounded model text. Metrics are operational signals, never canonical evidence.

## 9. Behavior-specific acceptance criteria

1. **AIR-FR-031 / AIR-ST-06.01 — source-supported Core Content Archetype.** Given an eligible AIR-005 Edge Product and exact source/audience state, when candidates are resolved, then only geometry fitting pressure, role at stake and intended movement survives. A familiar prompt name without member hash/source coverage fails. Evidence: candidate decision receipt. Test: unit + integration.
2. **AIR-FR-032 / AIR-ST-06.01 — semantic derivative route.** Given a surviving core archetype, when a derivative is declared, then category, semantic derivative route and route scope are explicit and production routing remains absent. A generic content type or hidden VAE/provider route fails. Evidence: route contract. Test: contract + architecture.
3. **AIR-FR-033 / AIR-ST-06.02 — participant role inside tension.** Given Matrix/tension evidence and Edge Product, when role/tension compiles, then role, tension, recognition, stance, movement, enabled action, threshold, counteractivation and transfer invariants are all evidenced. Topic-only intent fails. Evidence: role/tension receipt. Test: domain + integration.
4. **AIR-FR-034 / AIR-ST-06.02 — bounded coalition.** Given multiple eligible archetypes, compilation produces exactly one primary plus only functionally distinct compatible support/transition bindings, with all exclusions preserved. Multiple primaries, unbounded hybrids or centroid blending fail. Evidence: compatibility matrix and compile receipt. Test: unit + adversarial.
5. **AIR-FR-035 / AIR-ST-06.03 — SDA/SFL binding.** Given a route candidate, exact snapshot digest/member ID/version/hash and crosswalk/applicability evidence resolve for every required geometry/function. Name-only or historical-production-status inference fails. Evidence: registry-resolution receipt. Test: adapter + contract.
6. **AIR-FR-036 / AIR-ST-06.03 — route receipt.** An eligible receipt pins Edge fit, role/tension, coalition, alternatives, source lineage, SDA/SFL, evaluation and approval state. A passing evaluator without required human approval remains `EVALUATED`, not approved. Evidence: route receipt. Test: integration + authority.
7. **FR-163 / ST-12.01 — viewer role before routing.** Every derivative route references a versioned role/tension contract derived from source spans and Matrix/Edge lineage before archetype or category execution. Jumping from quote/topic to format fails. Evidence: end-to-end lineage graph. Test: reference slice.
8. **FR-165 / ST-12.02 — coherent Archetype Coalition Contract.** The program binds primary/support/transition/excluded archetypes, semantic derivative route, category grammar, psychological geometry and tension progression in one immutable hash. A pile of labels or popular-template retrofit fails. Evidence: coalition/CBAR receipt. Test: integration.
9. **Draft interface boundary.** AIR-002/AIR-005 exact pins and `DRAFT_DEPENDENCY_NOT_ACCEPTED` appear in receipts. If AIR-005's role/tension ref is proven circular with F06, acceptance is blocked by `AIR_ARCH_DRAFT_INTERFACE_CYCLE`. Evidence: dependency conformance. Test: architecture.
10. **Active Primitive CBAR.** PRM-PSY-001 preserves practical/emotional/social layer matching and blocks performative or inflexible matching; PRM-PRS-002 preserves tension/release and blocks unresolved/exhausting tension; PRM-HUM-021 preserves committed subtext inversion and blocks broken-voice or no-subtext irony. Evidence: exact YAML hash matrix and denial fixtures. Test: CBAR.
11. **`NOT_APPLICABLE`.** Required role, tension, Edge, coalition, primary, source fit, SDA, SFL and category findings reject N/A. A profile-declared conditional check may use N/A only with condition and evidence refs. Evidence: evaluation receipt. Test: schema + adversarial.
12. **Determinism and atomicity.** Fresh processes, reordered set-like inputs, time/random/env changes and different machine paths produce identical canonical outputs. Failure injection leaves no artifact/receipt orphan. Evidence: canonical vectors and transaction trace. Test: determinism + repository.
13. **Replay, supersession and recovery.** Exact historical versions reproduce after upstream supersession; only typed descendants become stale; unrelated branches remain eligible. Evidence: replay and invalidation receipts. Test: recovery.
14. **Authority boundary.** Pipeline cannot rewrite role/archetype meaning; VAE cannot claim semantic approval; Studio UI cannot mutate canonical state; AIR cannot issue production-route acceptance. Evidence: denial receipts. Test: architecture boundary.
15. **Claim ceiling.** While ratification is pending, output remains `WRITTEN_PENDING_AUDIT`, `CANDIDATE_NOT_CURRENT`, write authorized, build false, maximum later state `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`; no capsule is issuable. Evidence: lifecycle projection. Test: policy.

## 10. Testing and completion evidence

| Exact future path | Required tests/evidence |
|---|---|
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_psychological_role_tension.py` | All role/tension fields, epistemic separation, counteractivation and required N/A denial. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_archetype_coalition.py` | One-primary invariant, support/transition functions, exclusions, pairwise conflict and anti-centroid behavior. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contract/test_air_f06_schemas.py` | Closed schemas, model/type parity, exact refs, tagged composition logic and invalid examples. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/adapters/test_archetype_sda_sfl_registry.py` | Snapshot/member digest, crosswalk, lifecycle and decimal-to-micros migration. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_archetype_coalition_and_psychological_role_inside_tension.py` | Eight FRs, five Stories, evaluation and approval workflow. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_air_f06_repository.py` | Idempotency, concurrency, atomic rollback, cancellation race and state/receipt parity. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/architecture/test_air_f06_product_boundaries.py` | AIR/Pipeline/Builder/VAE/Studio/Delegation sovereignty and no production route in semantic models. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/migration/test_cmf_archetype_route_v1_to_air_f06.py` | Lossless mapping or typed block; historical aliases and bytes preserved. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/replay/test_air_f06_replay_invalidation.py` | Historical reproduction, late result, supersession and selective descendant invalidation. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/cbar/test_air_f06_active_primitives.py` | PRM-PSY-001, PRM-PRS-002 and PRM-HUM-021 exact hashes, core moves, misuse and suppression. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/reference_slice/test_f05_to_f06_to_f07_handoff.py` | Exact Matrix/coalition/Edge input, F06 role/archetype route output and Final Script boundary. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/determinism/test_air_f06_portability.py` | Fresh-process equality and independence from clock, random, environment, insertion/traversal order and paths. |

The adversarial suite includes stale source/Edge, draft hash drift, circular terminal-role dependency, label-only archetype, missing prompt member, unsupported source beat, generic role, missing counteractivation, multiple primary archetypes, geometry conflict, popular-template retrofit, centroid smoothing, unresolved SDA/SFL member, unsupported category route, production-route leakage, invalid N/A, producer self-evaluation, missing approval, current-time/random UUID, partial commit, idempotency conflict, stale expected version, cancellation/late evaluation race, invalidation overreach, lossy migration, absolute-path contamination and unauthorized capsule/build projection.

Future completion evidence requires exact source/snapshot/Primitive hash matrices, generated schema/type parity, canonical fixtures, candidate/rejection and route receipts, independent evaluator and attributable approval evidence, atomicity/concurrency traces, migration and compatibility reports, replay/invalidation proof, clean-environment proof, full suite twice in fresh processes, compilation/type checks, reference-slice proof and independent audit by a different agent. A future Build Receipt must bind ratified authority, accepted upstream spec hashes, exact Development Capsule, source snapshots, implementation/test revision, evaluator profile, migration evidence and claim ceiling; this document issues none.

Final writer state: `WRITTEN_PENDING_AUDIT`; authority `CANDIDATE_NOT_CURRENT`; specification work authorized; build authority false; later acceptance ceiling `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.
