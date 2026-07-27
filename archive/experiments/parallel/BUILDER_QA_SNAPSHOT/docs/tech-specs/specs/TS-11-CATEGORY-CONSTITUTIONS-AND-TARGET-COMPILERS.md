# TS-11: Category Constitutions And Target Compilers

Status: `IMPLEMENTATION_SPEC_COMPLETE_PENDING_BD-004_BD-014`

## Traceability

- Owned: FR-137 through FR-150; FR-170 through FR-180; NFR-MAINT-003, NFR-CAT-001, NFR-CAT-002, NFR-CAT-003.
- Decisions: D004, D005, D006, D007, D008, D010, D011, D014, D021, D024, D026, D027, D029, D030, D031, D033.
- Supporting: NFR-ARCH-001, NFR-COMPAT-001 disposition, NFR-EVAL-004, NFR-PORT-002, NFR-SEC-003.

## Responsibility And Authority

Own Shared Activative Core, five versioned category constitutions, category-local format profiles, Activative Sequencing Intelligence, atomic creative ownership, three Builder compilation target profiles, target-specific source/IR/Genesis/artifact/evaluation policies, and cross-target contract validation.

Builder owns compilation only. Visual Asset Editor production behavior belongs to its repository. Shared Delegation contracts belong to the Delegation repository. ComfyUI, model execution, LoRA training, GPU scheduling, and Content Harness execution are external. Humans own category constitutions and semantic policy; deterministic compilers enforce them.

## Modules And Components

`domain/categories/{core,constitution,format_profile,sequence}.py`, `domain/targets/profile.py`, `compilers/targets/{content_harness,visual_asset_editor,delegation}.py`, `compilers/targets/compatibility.py`, and `application/category_commands.py`.

## Canonical Data Structures

- `SharedActivativeCore { version, universal_invariants, knowledge_status_rules, semantic_authority_rules }`
- `CategoryConstitution { category_id, version, visual_ontology_ref, temporal_ontology_ref, sequence_rules, capability_constraints, runtime_contracts, evaluation_policy, repair_policy, migration_policy }`
- Categories: `SHORT_FORM_EDITED_VIDEO`, `TWO_D_CHARACTER_ANIMATION`, `CAROUSELS`, `SUPERVISUALS`, `CONVERSATIONAL_ACTIVATION_EXPRESSION`.
- `FormatProfile { profile_id, category_ref, atomic_boundary_rules, registries, syntax_adaptations, sequence_program, legal_variation, exclusions }`
- `SequenceProgram { hidden_pressure, activation_direction, viewer_role, states, transitions, pacing, sonic_function?, prediction_gap, payoff, intended_reaction, evaluators }`
- `CompilationTargetProfile { target_kind, source_profile_ref, ir_profile_ref, genesis_graph_ref, compiler_ref, artifact_set, evaluation_gates, certification_scope }`
- `TargetPackageManifest { target_profile_hash, harness_ir_hash, external_contract_versions, artifacts, certification=UNCERTIFIED|AUTHORIZED }`

Format 02 Minimal Coach Theatre is a `TWO_D_CHARACTER_ANIMATION` profile with character, pose/expression, staging, continuity, beat, and performance registries.

## APIs, Commands, Events, Persistence

- Commands: `RegisterCategoryConstitution`, `RegisterFormatProfile`, `CompileSequenceProgram`, `RegisterTargetProfile`, `CompileTargetPackage`, `ValidateCrossTargetContracts`, `ChangeCertificationScope`.
- Events: `CategoryConstitutionRegistered`, `FormatProfileRegistered`, `SequenceProgramCompiled`, `TargetProfileRegistered`, `TargetPackageCompiled`, `CrossTargetContractFailed`, `TargetCertificationChanged`.
- Persistence: constitutions/profiles in versioned registry and Harness IR references; target packages in CAS; external interface snapshots as read-only versioned artifacts.
- Compiler interface: `compile(harness_ir, target_profile, external_contract_snapshots) -> TargetPackageManifest`.

## Dependency, Invalidation, Idempotency, Resume

Category/profile version, shared core, source profile, target profile, external contract, or sequence change invalidates dependent target packages and evaluations. Compiler cache key includes every identity. A run may resume compilation per target, but no package becomes authoritative until manifest and compatibility checks commit atomically.

## Security And Isolation

Target compilers run without external runtime credentials or network. External repository snapshots are read-only. Content semantic fields are producer-owned and cannot be mutated by editor/delegation compilers. `UNCERTIFIED` labels are machine-enforced and cannot be removed by document editing.

## Observability, Cost, And Performance

Record category/profile identity, compiler version, external contract versions, artifact hashes, compatibility failures, sequence evaluation, compilation latency, and certification scope. Format 02 receives production evaluation in Release 1; other categories and external targets receive structural conformance only.

## Failures And Recovery

Missing category, profile, or external contract blocks compilation. Cross-target contradiction routes to the owning contract without rewriting content authority. Category migration requires an explicit new version and impact report. A failed target does not invalidate a successful independent target package, but shared-IR defects invalidate all dependents.

## Acceptance Tests

1. Format 02 validates only under 2D Character Animation.
2. Every atomic harness belongs to one category and one format profile.
3. Sequence programs preserve category-native temporal and visual rules.
4. Visual Asset Editor and Delegation outputs contain contracts/specs only, no production runtime.
5. Content-owned semantic fields are immutable across target compilation.
6. Remaining categories and external targets are labeled `UNCERTIFIED` in Release 1.
7. Same IR/profile/contracts produce identical target package hashes.
8. Contract version changes produce exact compatibility and invalidation reports.

## Implementation Tasks

1. Define shared core, category, format, sequence, target, and manifest schemas.
2. Ratify the Format 02 constitution/profile and structural schemas for other categories.
3. Implement target compiler registry and content-harness compiler.
4. Implement schema-only editor/delegation compilers after BD-014.
5. Implement compatibility, authority, certification, and migration validators.
6. Add category isolation, sequence, cross-target, and frozen-boundary tests.

## V1.2 Constitutional Alignment Patch

| Requirement | Implementation owner | Component boundary | Data or contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Compile five category constitutions while preserving three target compilers | category_and_target_compiler_owner | Category/profile specializations live under Atomic Content Harness; Visual Asset Editor and Delegation remain external target contracts | category registry, conversational profile registry, `CompilationTargetProfile` | Reject category/target conflation, false certification, or external runtime import | five-category registry and three-target invariance tests | Five category IDs and four conversational profiles compile; compilation target count remains three | D031 current effect expands categories; target IDs and ADR-013 decision remain compatible |
| Emit activation-first visual-semantic and Delegation handoffs | target_compiler_owner | Builder emits schemas/fixtures/packages only; downstream owners execute | Visual Semantic Pack → Visual Narrative Program → feature contracts → Composition Asset Pack → Visual Syntax handoff → T/V route → Delegation handoff | Reject reordered chain, semantic mutation, missing snapshot, or runtime credential | contract fixtures and forbidden-runtime tests | Each handoff is versioned, hashed, non-mutating, and externally executable only | Additive snapshot fields; blocked on BD-014 authoritative external interface versions |

## Delegation RC4 Integration Correction Addendum

The active external contract snapshot is exactly `delegation-contracts@1.1.0-rc.4`, release digest `sha256:c614a4d9b705e382456f4d6cd1cd6b7bcbc892517a22b358950db7404e3b4c44`, under compatibility profile `cmf-delegation-compatibility-profile-1-0`. It is a `local_unsigned_release_candidate` and is not production-eligible. Builder consumes the pinned generated types and validates against the external schemas; it does not fork or own Delegation schemas. RC4 adds the portable `derivative-lock-inheritance@1.0` relationship while preserving Visual Asset Demand `1.1`.

| Requirement | Implementation owner | Component boundary | Data or contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Compile lossless RC4-compatible demand and derivative relationships | target_compiler_owner | Builder maps target specifications; Delegation owns schemas/runtime; VAE owns realization | exact pin plus Builder wire, provenance, lineage, category/profile, and derivative-lock mappings under `contracts/integration/` | Reject non-RC4 pins, local schema forks, missing semantic domains, missing parent evidence, or external runtime imports | exact-pin, external-ownership, schema, generated-type, lineage, and derivative-validator contract tests | A Builder target specification validates through pinned RC4 schemas without semantic flattening or guessed inheritance evidence | RC1/RC2/RC3 are historical only; production awaits an authorized signed release and readiness `PASS` |
| Resolve governed source kind without guessing | evidence_architecture_and_source_authority | Builder classifies only from authoritative source evidence | RC4 `source_provenance.source_kind`; interview provenance refs | Reject ambiguous, unknown, guessed, or unreceipted legacy classifications | source-kind table, ambiguous operator-authored, legacy migration, and interview/non-interview fixtures | Interview Expression and ReelCast resolve to `interview_expression` with non-empty Reaction Receipt and Expression Moment refs; optional non-interview refs validate when present | Pre-source-kind inputs require explicit owner classification; legacy inputs require a lossless migration receipt |
| Preserve wrong-reading locks across derivatives | target_compiler_owner | Builder emits authoritative inheritance policy and portable relationship; VAE enforces production realization | RC4 `wrong_reading_locks` plus `derivative-lock-inheritance@1.0` parent/demand refs, lock evidence, derivation classification, derivative locks, and authorization evidence | Reject empty locks, missing parent evidence, ambiguous derivation, removal, weakening, or unauthorized relaxation | exact inheritance, stricter derivative, missing evidence, ambiguous derivation, and authorized-new-demand fixtures | Every derivative carries a relationship accepted by the RC4 portable validator | Relaxation creates and identifies a new authoritative upstream demand; Builder does not implement VAE realization |
| Keep profile states independent | category_and_target_compiler_owner | Category/profile compilation stays Builder-owned; product certification authority stays with its owner | canonical `format02_minimal_coach_theatre` plus Program Control alias registry and six independent state fields | Reject unknown aliases, inherited certification, or unsupported production claims | alias, matrix completeness, and false-certification tests | Format 02 is the Release 1 `reference_profile`, is structurally supported and contract-compatible, and is not benchmarked or certified; all conversational profiles remain structural and uncertified | Historical `minimal_coach_theatre` resolves only through the governed alias registry; Interview Expression/ReelCast require owning PRDs for production |

## Non-Goals And Migration

No editor, delegation runtime, model execution, GPU work, or V2.1 profile migration is included. Category profile migration applies only to future Builder Next versions.
