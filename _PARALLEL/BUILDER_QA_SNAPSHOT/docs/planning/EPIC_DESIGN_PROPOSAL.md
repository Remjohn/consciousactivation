# Builder V1.2 Outcome-Centered Epic Design Proposal

Status: `PROPOSED_AWAITING_HUMAN_CONFIRMATION`

Step: `2 — Outcome-centered Epic design`

Authority: Builder PRD V1.2 under Activative Intelligence Constitution V1.1.

Confirmed planning baseline: 410 obligations, SHA-256 `d3db32a78f4acce25e5448ff7c6ecb765ba814c0bdbf1bb44d6b49de00c55923`.

This proposal assigns every confirmed obligation exactly once as a primary Epic responsibility in `EPIC_REQUIREMENT_COVERAGE.csv`. Secondary traceability is non-owning. The confirmed baseline CSV is not mutated. No vertical Stories or production implementation are included.

Planning may continue. Implementation remains prohibited while readiness is `FAIL`.

## Proposed Epic inventory

| Epic | Outcome-centered title | Primary obligations | Dependencies | Release 1 disposition |
| --- | --- | ---: | --- | --- |
| EP-01 | Governed Run Intake and Evidence Readiness | 33 | None | `RELEASE_1_INCLUDED` |
| EP-02 | Syntax-Grounded Understanding and Atomic Boundary | 28 | EP-01 | `RELEASE_1_INCLUDED` |
| EP-03 | Human-Ratified Genesis and Canonical Harness Definition | 35 | EP-01, EP-02 | `RELEASE_1_INCLUDED` |
| EP-04 | Owned Capability Graphs and Minimum Complete Context | 33 | EP-03 | `RELEASE_1_INCLUDED` |
| EP-05 | Reusable Evaluated Skills and Deterministic JIT Capsules | 32 | EP-04 | `RELEASE_1_INCLUDED` |
| EP-06 | Five-Category Activative Intelligence and Expression Compilation | 28 | EP-02, EP-03, EP-04 | `RELEASE_1_FORMAT02_PRODUCTION_OTHER_CATEGORIES_STRUCTURAL_UNCERTIFIED` |
| EP-07 | Three-Target Product Compilation and Cross-Product Handoff | 15 | EP-03, EP-04, EP-06 | `RELEASE_1_THREE_TARGET_STRUCTURAL_FORMAT02_STUBBED_EXTERNAL_HANDOFF` |
| EP-08 | Behavioral Proof, Repair, and Readiness Authorization | 44 | EP-02, EP-03, EP-04, EP-05, EP-06, EP-07 | `RELEASE_1_INCLUDED_CERTIFICATION_BLOCKED` |
| EP-09 | Governed Builder Workflow Factory | 62 | EP-01, EP-03, EP-04, EP-05, EP-06, EP-07, EP-08 | `RELEASE_1_INCLUDED_MANUAL_SHADOW_BEFORE_AUTOMATION` |
| EP-10 | Evidence-Derived Human Control Tower | 73 | EP-01, EP-03, EP-04, EP-05, EP-06, EP-07, EP-08, EP-09 | `RELEASE_1_INCLUDED` |
| EP-11 | Traceable Development Capsule and Implementation Handoff | 10 | EP-03, EP-04, EP-05, EP-06, EP-07, EP-08, EP-09, EP-10 | `RELEASE_1_INCLUDED_HANDOFF_ONLY_NO_IMPLEMENTATION_AUTHORIZATION` |
| EP-12 | Brownfield Migration and Release 1 Reference Proof | 17 | EP-06, EP-07, EP-08, EP-09, EP-10, EP-11 | `RELEASE_1_FORMAT02_REFERENCE_PROOF_GENERAL_CERTIFICATION_DEFERRED` |

## Canonical category preservation

| Category ID | Canonical category | Primary Epic |
| --- | --- | --- |
| `short_form_edited_video` | Short-Form Edited Video | EP-06 |
| `2d_character_animation` | 2D Character Animation | EP-06 |
| `carousels` | Carousels | EP-06 |
| `supervisuals` | Supervisuals | EP-06 |
| `conversational_activation_expression` | Conversational Activation / Human Expression | EP-06 |

## Conversational profile boundary

| Profile ID | Builder boundary | Primary Epic |
| --- | --- | --- |
| `public_comment` | `builder_compile_validate_and_handoff` | EP-06 |
| `reply_dm` | `builder_compile_validate_and_handoff` | EP-06 |
| `reelcast_expression` | `builder_compile_validate_and_handoff_only_external_execution` | EP-06 |
| `interview_expression` | `builder_compile_validate_and_handoff_only_external_execution` | EP-06 |

`reelcast_expression` and `interview_expression` are structurally compiled, validated, and handed off by Builder. Their live execution and final product PRDs remain outside this repository.

## Compilation target preservation

| Target ID | Compilation target | Primary Epic |
| --- | --- | --- |
| `atomic_content_harness` | Atomic Content Harness | EP-07 |
| `visual_asset_editor` | Visual Asset Editor | EP-07 |
| `content_asset_delegation_contract` | Content Asset Delegation Contract | EP-07 |

## Dependency ordering

The Epic IDs are a topological execution proposal: every dependency has a lower order number. This does not require horizontal implementation. Each Epic must deliver its stated end-to-end actor or system outcome, and Release 1 must demonstrate a complete Format 02 path through the needed portions of the sequence.

## Unresolved decisions, blockers, and gates

| Gate | Carried by | Effect |
| --- | --- | --- |
| `BD-004` | EP-01, EP-02, EP-03, EP-05, EP-06, EP-07, EP-08, EP-10, EP-11, EP-12 | OPEN — planning may continue; affected implementation or certification outcomes remain blocked |
| `BD-007` | EP-02, EP-06, EP-08, EP-12 | OPEN — planning may continue; affected implementation or certification outcomes remain blocked |
| `BD-008` | EP-02, EP-03, EP-05, EP-06, EP-07, EP-08, EP-09, EP-10, EP-11, EP-12 | OPEN — planning may continue; affected implementation or certification outcomes remain blocked |
| `BD-010` | EP-04, EP-05, EP-06, EP-08, EP-09, EP-10, EP-11, EP-12 | OPEN — planning may continue; affected implementation or certification outcomes remain blocked |
| `BD-014` | EP-01, EP-03, EP-04, EP-06, EP-07, EP-08, EP-09, EP-10, EP-11, EP-12 | OPEN — planning may continue; affected implementation or certification outcomes remain blocked |
| `HD-006` | EP-01, EP-02, EP-06, EP-08, EP-11, EP-12 | OPEN — planning may continue; affected implementation or certification outcomes remain blocked |
| `HD-007` | EP-05, EP-06, EP-08, EP-11, EP-12 | OPEN — planning may continue; affected implementation or certification outcomes remain blocked |

## Exact Epic proposals and primary requirement coverage

## EP-01 — Governed Run Intake and Evidence Readiness

**Outcome:** A Harness Architect can select exactly one compilation target, start or resume a constitutionally bounded run, lock target-specific evidence without source mutation, and receive an explicit readiness or saturation outcome before design decisions begin.

**Primary actor:** Harness Architect

**Release 1 disposition:** `RELEASE_1_INCLUDED`

**Depends on:** None

**Decision and blocker obligations:** `HD-006`, `BD-004`, `BD-014`

**Primary coverage (33 obligations):**

- `ARCHITECTURE_DECISION` (2): `ADR-001`, `ADR-007`
- `BINDING_ANTI_GOAL` (2): `AG-001`, `AG-002`
- `FUNCTIONAL_REQUIREMENT` (18): `FR-001`, `FR-002`, `FR-003`, `FR-004`, `FR-005`, `FR-006`, `FR-007`, `FR-008`, `FR-009`, `FR-010`, `FR-011`, `FR-012`, `FR-013`, `FR-014`, `FR-015`, `FR-016`, `FR-017`, `FR-018`
- `LOCKED_DECISION` (3): `D001`, `D005`, `D006`
- `NON_FUNCTIONAL_REQUIREMENT` (7): `NFR-PORT-001`, `NFR-REL-002`, `NFR-SCALE-001`, `NFR-SEC-001`, `NFR-SEC-002`, `NFR-SEC-003`, `NFR-TRACE-004`
- `READINESS_HARD_GATE` (1): `HG-002`

**Cross-repository dependencies:**

- `XDEP-001` — **CMF_PROGRAM_CONTROL**: Supplies constitutional and product authority, cross-repository decision governance, release pins, and convergence status. Constraint: Program records must be synchronized separately; Builder does not mutate program control during this Epic proposal.
- `XDEP-004` — **05_FUTURE_PRODUCTS/INTERVIEW_EXPRESSION_HARNESS**: Future owner of Interview Expression and ReelCast live execution, Reaction Receipt capture, Expression Moment extraction, and final content-type contracts. Constraint: Planning is paused after one locked atomic-boundary decision; Builder must not pre-write the final product PRD.
- `XDEP-006` — **Activation Compiler Harness**: Upstream semantic authority that produces the rich Activative Intelligence Pack referenced by Builder contracts. Constraint: Builder preserves frozen lineage and sparse references; it does not replace or implement the Activation Compiler.

**Included outcome boundary:**

- Governed lifecycle, run identity, target selection, source profiles, immutable source lock, evidence index, gap classification, and saturation.
- Consent-aware structural intake for conversational sources without authorizing their production use.

**Excluded boundary:**

- Final product execution, semantic invention from missing evidence, and mutation of source repositories.

**Completion evidence:** A target-profiled run can fail closed or proceed with immutable evidence identity, complete provenance, and resumable lifecycle receipts.

**Blocked outcomes and risk:** Production use of human-reaction evidence remains blocked by HD-006 and BD-004; external target source and interface proof remains constrained by BD-014.

## EP-02 — Syntax-Grounded Understanding and Atomic Boundary

**Outcome:** A reviewer can derive typed visual or conversational syntax evidence before meaning, distinguish observation from hypothesis, compare candidate product boundaries, and ratify one atomic Draft Harness Model with explicit uncertainty and wrong-boundary risk.

**Primary actor:** Harness Architect and constitutional reviewer

**Release 1 disposition:** `RELEASE_1_INCLUDED`

**Depends on:** `EP-01`

**Decision and blocker obligations:** `HD-006`, `BD-004`, `BD-007`, `BD-008`

**Primary coverage (28 obligations):**

- `ARCHITECTURE_DECISION` (1): `ADR-008`
- `BINDING_ANTI_GOAL` (2): `AG-006`, `AG-007`
- `FUNCTIONAL_REQUIREMENT` (22): `FR-019`, `FR-020`, `FR-021`, `FR-022`, `FR-023`, `FR-024`, `FR-025`, `FR-026`, `FR-027`, `FR-028`, `FR-029`, `FR-030`, `FR-031`, `FR-032`, `FR-033`, `FR-034`, `FR-035`, `FR-036`, `FR-037`, `FR-038`, `FR-039`, `FR-040`
- `LOCKED_DECISION` (2): `D007`, `D008`
- `READINESS_HARD_GATE` (1): `HG-003`

**Cross-repository dependencies:**

- `XDEP-001` — **CMF_PROGRAM_CONTROL**: Supplies constitutional and product authority, cross-repository decision governance, release pins, and convergence status. Constraint: Program records must be synchronized separately; Builder does not mutate program control during this Epic proposal.
- `XDEP-004` — **05_FUTURE_PRODUCTS/INTERVIEW_EXPRESSION_HARNESS**: Future owner of Interview Expression and ReelCast live execution, Reaction Receipt capture, Expression Moment extraction, and final content-type contracts. Constraint: Planning is paused after one locked atomic-boundary decision; Builder must not pre-write the final product PRD.

**Included outcome boundary:**

- Visual Syntax First for harness-development discovery, category-adapted conversational parsing evidence, knowledge status, spatial or temporal graphs, and atomicity ratification.
- Structural evidence seams for Activative Calls, turns, Reaction Receipts, Expression Moments, and micro-commitments where applicable.

**Excluded boundary:**

- Runtime semantic invention, live Interview or ReelCast execution, and unratified boundary promotion.

**Completion evidence:** One ratified atomic boundary is backed by reproducible syntax evidence, alternatives, confidence, and a frozen Genesis entry state.

**Blocked outcomes and risk:** Parser reliability and protected boundary thresholds cannot be certified until BD-004, BD-007, BD-008, and applicable HD-006 governance are resolved.

## EP-03 — Human-Ratified Genesis and Canonical Harness Definition

**Outcome:** Human authority can answer only dependency-ready constitutional questions, preserve the evidence and recommendation trail, freeze ratified decisions, and compile one provenance-rich canonical Harness IR into consistent human and machine artifacts.

**Primary actor:** Harness Architect and product authority

**Release 1 disposition:** `RELEASE_1_INCLUDED`

**Depends on:** `EP-01`, `EP-02`

**Decision and blocker obligations:** `BD-004`, `BD-008`, `BD-014`

**Primary coverage (35 obligations):**

- `ARCHITECTURE_DECISION` (3): `ADR-002`, `ADR-004`, `ADR-005`
- `BINDING_ANTI_GOAL` (1): `AG-018`
- `CONSTITUTIONAL_AMENDMENT` (1): `CONST-001`
- `FUNCTIONAL_REQUIREMENT` (19): `FR-041`, `FR-042`, `FR-043`, `FR-044`, `FR-045`, `FR-046`, `FR-047`, `FR-048`, `FR-049`, `FR-050`, `FR-051`, `FR-052`, `FR-053`, `FR-054`, `FR-055`, `FR-056`, `FR-057`, `FR-058`, `FR-059`
- `LOCKED_DECISION` (4): `D002`, `D009`, `D010`, `D011`
- `NON_FUNCTIONAL_REQUIREMENT` (6): `NFR-COMPAT-002`, `NFR-COMPAT-003`, `NFR-MAINT-001`, `NFR-REL-001`, `NFR-REL-003`, `NFR-TRACE-001`
- `READINESS_HARD_GATE` (1): `HG-001`

**Cross-repository dependencies:**

- `XDEP-001` — **CMF_PROGRAM_CONTROL**: Supplies constitutional and product authority, cross-repository decision governance, release pins, and convergence status. Constraint: Program records must be synchronized separately; Builder does not mutate program control during this Epic proposal.
- `XDEP-006` — **Activation Compiler Harness**: Upstream semantic authority that produces the rich Activative Intelligence Pack referenced by Builder contracts. Constraint: Builder preserves frozen lineage and sparse references; it does not replace or implement the Activation Compiler.

**Included outcome boundary:**

- Constitutional precedence, dependency-driven Genesis, transactionally updated Harness IR, schema evolution, deterministic compilation, drift detection, and decision receipts.
- Frozen references to rich Activative Intelligence Pack objects without lower-authority semantic rewrite.

**Excluded boundary:**

- Replacing the Activation Compiler, bypassing human authority, or treating generated documents as independent sources of truth.

**Completion evidence:** The same canonical IR deterministically produces complete sharded specifications and machine artifacts with hashes, migrations, provenance, and contradiction handling.

**Blocked outcomes and risk:** Full readiness remains unavailable where evidence or external interface authority is unresolved under BD-004, BD-008, or BD-014.

## EP-04 — Owned Capability Graphs and Minimum Complete Context

**Outcome:** A maintainer can see who or what owns every capability, how responsibility-centered modules and phases connect, what each handoff may change, and the minimum complete context required for reliable work.

**Primary actor:** Harness Architect and maintainer

**Release 1 disposition:** `RELEASE_1_INCLUDED`

**Depends on:** `EP-03`

**Decision and blocker obligations:** `BD-010`, `BD-014`

**Primary coverage (33 obligations):**

- `BINDING_ANTI_GOAL` (2): `AG-012`, `AG-013`
- `FUNCTIONAL_REQUIREMENT` (21): `FR-060`, `FR-061`, `FR-062`, `FR-063`, `FR-064`, `FR-065`, `FR-066`, `FR-067`, `FR-068`, `FR-069`, `FR-070`, `FR-071`, `FR-072`, `FR-073`, `FR-074`, `FR-075`, `FR-076`, `FR-077`, `FR-078`, `FR-079`, `FR-080`
- `LOCKED_DECISION` (6): `D012`, `D013`, `D014`, `D015`, `D016`, `D020`
- `NON_FUNCTIONAL_REQUIREMENT` (1): `NFR-ARCH-001`
- `READINESS_HARD_GATE` (3): `HG-004`, `HG-005`, `HG-007`

**Cross-repository dependencies:**

- `XDEP-001` — **CMF_PROGRAM_CONTROL**: Supplies constitutional and product authority, cross-repository decision governance, release pins, and convergence status. Constraint: Program records must be synchronized separately; Builder does not mutate program control during this Epic proposal.

**Included outcome boundary:**

- Capability ownership, module test seams, phase and context graphs, versioned handoffs, reference registry, SPR, progressive disclosure, and context budgets.

**Excluded boundary:**

- Horizontal infrastructure epics, silent downstream rewriting, conversation-history-as-interface, or universal context loading.

**Completion evidence:** Every required capability has an owner, module boundary, dependency path, typed contract, context manifest, and impact-analysis seam.

**Blocked outcomes and risk:** Final capability placement and external handoff closure remain conditional on BD-010 and BD-014.

## EP-05 — Reusable Evaluated Skills and Deterministic JIT Capsules

**Outcome:** A maintainer can reuse, adapt, or justify new skills through capability-gap evidence, bind them to behavioral evaluation, and assemble deterministic phase-local capsules containing only the authority and context needed for the current task.

**Primary actor:** Skill maintainer and Harness Architect

**Release 1 disposition:** `RELEASE_1_INCLUDED`

**Depends on:** `EP-04`

**Decision and blocker obligations:** `HD-007`, `BD-004`, `BD-008`, `BD-010`

**Primary coverage (32 obligations):**

- `ARCHITECTURE_DECISION` (1): `ADR-009`
- `BINDING_ANTI_GOAL` (3): `AG-008`, `AG-009`, `AG-010`
- `FUNCTIONAL_REQUIREMENT` (22): `FR-081`, `FR-082`, `FR-083`, `FR-084`, `FR-085`, `FR-086`, `FR-087`, `FR-088`, `FR-089`, `FR-090`, `FR-091`, `FR-092`, `FR-093`, `FR-094`, `FR-095`, `FR-096`, `FR-097`, `FR-098`, `FR-099`, `FR-100`, `FR-101`, `FR-102`
- `LOCKED_DECISION` (4): `D017`, `D018`, `D019`, `D021`
- `NON_FUNCTIONAL_REQUIREMENT` (1): `NFR-MAINT-002`
- `READINESS_HARD_GATE` (1): `HG-006`

**Cross-repository dependencies:**

- `XDEP-001` — **CMF_PROGRAM_CONTROL**: Supplies constitutional and product authority, cross-repository decision governance, release pins, and convergence status. Constraint: Program records must be synchronized separately; Builder does not mutate program control during this Epic proposal.

**Included outcome boundary:**

- Canonical skill ecology, authority lanes, maturity, design briefs, composition recipes, bindings, degradation, hashes, and ephemeral JIT capsules.

**Excluded boundary:**

- Turning every capability into a skill, hiding workflows inside skills, or shipping required skills without behavioral lift.

**Completion evidence:** A required capability resolves to a tested reusable skill or justified gap, and its capsule is reproducible, bounded, version-pinned, and behaviorally attributable.

**Blocked outcomes and risk:** Production skill maturity and conversational evaluators remain uncertifiable until HD-007, BD-004, BD-008, and BD-010 are resolved.

## EP-06 — Five-Category Activative Intelligence and Expression Compilation

**Outcome:** A category steward can preserve one Shared Activative Core and compile category-native syntax, sequence, runtime, evaluation, and repair contracts for all five canonical categories, including first-class Conversational Activation / Human Expression profiles.

**Primary actor:** Category steward and Harness Architect

**Release 1 disposition:** `RELEASE_1_FORMAT02_PRODUCTION_OTHER_CATEGORIES_STRUCTURAL_UNCERTIFIED`

**Depends on:** `EP-02`, `EP-03`, `EP-04`

**Decision and blocker obligations:** `HD-006`, `HD-007`, `BD-004`, `BD-007`, `BD-008`, `BD-010`, `BD-014`

**Primary coverage (28 obligations):**

- `BINDING_ANTI_GOAL` (3): `AG-003`, `AG-004`, `AG-005`
- `CONSTITUTIONAL_AMENDMENT` (4): `CONST-002`, `CONST-003`, `CONST-004`, `CONST-006`
- `FUNCTIONAL_REQUIREMENT` (14): `FR-137`, `FR-138`, `FR-139`, `FR-140`, `FR-141`, `FR-142`, `FR-143`, `FR-144`, `FR-145`, `FR-146`, `FR-147`, `FR-148`, `FR-149`, `FR-150`
- `LOCKED_DECISION` (2): `D030`, `D031`
- `NON_FUNCTIONAL_REQUIREMENT` (4): `NFR-CAT-001`, `NFR-CAT-002`, `NFR-CAT-003`, `NFR-MAINT-003`
- `READINESS_HARD_GATE` (1): `HG-015`

**Cross-repository dependencies:**

- `XDEP-001` — **CMF_PROGRAM_CONTROL**: Supplies constitutional and product authority, cross-repository decision governance, release pins, and convergence status. Constraint: Program records must be synchronized separately; Builder does not mutate program control during this Epic proposal.
- `XDEP-004` — **05_FUTURE_PRODUCTS/INTERVIEW_EXPRESSION_HARNESS**: Future owner of Interview Expression and ReelCast live execution, Reaction Receipt capture, Expression Moment extraction, and final content-type contracts. Constraint: Planning is paused after one locked atomic-boundary decision; Builder must not pre-write the final product PRD.
- `XDEP-006` — **Activation Compiler Harness**: Upstream semantic authority that produces the rich Activative Intelligence Pack referenced by Builder contracts. Constraint: Builder preserves frozen lineage and sparse references; it does not replace or implement the Activation Compiler.

**Included outcome boundary:**

- Short-Form Edited Video, 2D Character Animation, Carousels, Supervisuals, and Conversational Activation / Human Expression.
- Public Comment, Reply or DM, ReelCast Expression, and Interview Expression structural profiles.
- Activative Intelligence Pack lineage, Activative Calls, Reaction Receipts, Expression Moments, post-expression recompilation, wrong-reading locks, Activation First runtime ordering, and Visual Syntax First development ordering.

**Excluded boundary:**

- Live Interview or ReelCast execution, final Interview Expression PRD authoring, Identity DNA merge authority, and certification inheritance from Format 02.

**Completion evidence:** Each category and profile compiles distinct contracts without flattening shared meaning, and HG-015 fails closed when the semantic stack or conversational category is absent.

**Blocked outcomes and risk:** Conversational production use and general category certification remain blocked by HD-006, HD-007, BD-004, BD-007, BD-008, BD-010, and BD-014.

## EP-07 — Three-Target Product Compilation and Cross-Product Handoff

**Outcome:** A cross-product architect can compile distinct Atomic Content Harness, Visual Asset Editor, and Content Asset Delegation Contract profiles from shared governance while preserving target-specific evidence, ownership, artifacts, evaluation, compatibility, and frozen semantic handoffs.

**Primary actor:** Cross-product architect and Harness Architect

**Release 1 disposition:** `RELEASE_1_THREE_TARGET_STRUCTURAL_FORMAT02_STUBBED_EXTERNAL_HANDOFF`

**Depends on:** `EP-03`, `EP-04`, `EP-06`

**Decision and blocker obligations:** `BD-004`, `BD-008`, `BD-014`

**Primary coverage (15 obligations):**

- `ARCHITECTURE_DECISION` (2): `ADR-013`, `ADR-018`
- `CONSTITUTIONAL_AMENDMENT` (1): `CONST-005`
- `FUNCTIONAL_REQUIREMENT` (11): `FR-170`, `FR-171`, `FR-172`, `FR-173`, `FR-174`, `FR-175`, `FR-176`, `FR-177`, `FR-178`, `FR-179`, `FR-180`
- `LOCKED_DECISION` (1): `D004`

**Cross-repository dependencies:**

- `XDEP-001` — **CMF_PROGRAM_CONTROL**: Supplies constitutional and product authority, cross-repository decision governance, release pins, and convergence status. Constraint: Program records must be synchronized separately; Builder does not mutate program control during this Epic proposal.
- `XDEP-002` — **02_VISUAL_ASSET_EDITOR**: Consumes the Builder Visual Asset Editor target profile and visual-semantic or Asset Demand handoff contracts. Constraint: VAE implementation readiness is FAIL; Builder defines and validates the target profile but does not implement editor behavior.
- `XDEP-003` — **03_DELEGATION_PROTOCOL**: Owns the external Content-to-Asset Delegation runtime and shared contract release consumed by Builder target compilation. Constraint: The 1.1.0-rc.1 candidate is not production-authorized and cross-repository adoption or convergence remains gated.
- `XDEP-004` — **05_FUTURE_PRODUCTS/INTERVIEW_EXPRESSION_HARNESS**: Future owner of Interview Expression and ReelCast live execution, Reaction Receipt capture, Expression Moment extraction, and final content-type contracts. Constraint: Planning is paused after one locked atomic-boundary decision; Builder must not pre-write the final product PRD.

**Included outcome boundary:**

- Three versioned target profiles, target-specific source and IR profiles, artifact sets, evaluation gates, compatibility, visual-semantic and Delegation handoffs, Composition Asset Pack and T or V route request lineage.

**Excluded boundary:**

- Visual Asset Editor runtime behavior, Delegation Protocol runtime behavior, or a universal target profile.

**Completion evidence:** Target compilation proves profile separation, lossless lineage, explicit ownership, compatibility behavior, and stubbed Release 1 external ports.

**Blocked outcomes and risk:** Production cross-repository convergence and certification remain blocked by BD-004, BD-008, BD-014, and the external products' own readiness gates.

## EP-08 — Behavioral Proof, Repair, and Readiness Authorization

**Outcome:** Independent reviewers can measure whether the Builder, its skills, categories, profiles, and target artifacts improve behavior, reject wrong readings, repair only responsible layers, and issue immutable readiness or blocked authorization receipts.

**Primary actor:** Evaluator, reviewer, and product authority

**Release 1 disposition:** `RELEASE_1_INCLUDED_CERTIFICATION_BLOCKED`

**Depends on:** `EP-02`, `EP-03`, `EP-04`, `EP-05`, `EP-06`, `EP-07`

**Decision and blocker obligations:** `HD-006`, `HD-007`, `BD-004`, `BD-007`, `BD-008`, `BD-010`, `BD-014`

**Primary coverage (44 obligations):**

- `ARCHITECTURE_DECISION` (1): `ADR-010`
- `BINDING_ANTI_GOAL` (3): `AG-014`, `AG-015`, `AG-022`
- `CONSTITUTIONAL_AMENDMENT` (2): `CONST-007`, `CONST-008`
- `FUNCTIONAL_REQUIREMENT` (24): `FR-103`, `FR-104`, `FR-105`, `FR-106`, `FR-107`, `FR-108`, `FR-109`, `FR-110`, `FR-111`, `FR-112`, `FR-113`, `FR-114`, `FR-115`, `FR-116`, `FR-127`, `FR-128`, `FR-129`, `FR-130`, `FR-131`, `FR-132`, `FR-133`, `FR-134`, `FR-135`, `FR-136`
- `LOCKED_DECISION` (6): `D022`, `D023`, `D024`, `D026`, `D027`, `D033`
- `NON_FUNCTIONAL_REQUIREMENT` (5): `NFR-EVAL-001`, `NFR-EVAL-002`, `NFR-EVAL-003`, `NFR-EVAL-004`, `NFR-TRACE-003`
- `READINESS_HARD_GATE` (3): `HG-008`, `HG-009`, `HG-010`

**Cross-repository dependencies:**

- `XDEP-001` — **CMF_PROGRAM_CONTROL**: Supplies constitutional and product authority, cross-repository decision governance, release pins, and convergence status. Constraint: Program records must be synchronized separately; Builder does not mutate program control during this Epic proposal.
- `XDEP-002` — **02_VISUAL_ASSET_EDITOR**: Consumes the Builder Visual Asset Editor target profile and visual-semantic or Asset Demand handoff contracts. Constraint: VAE implementation readiness is FAIL; Builder defines and validates the target profile but does not implement editor behavior.
- `XDEP-003` — **03_DELEGATION_PROTOCOL**: Owns the external Content-to-Asset Delegation runtime and shared contract release consumed by Builder target compilation. Constraint: The 1.1.0-rc.1 candidate is not production-authorized and cross-repository adoption or convergence remains gated.
- `XDEP-004` — **05_FUTURE_PRODUCTS/INTERVIEW_EXPRESSION_HARNESS**: Future owner of Interview Expression and ReelCast live execution, Reaction Receipt capture, Expression Moment extraction, and final content-type contracts. Constraint: Planning is paused after one locked atomic-boundary decision; Builder must not pre-write the final product PRD.
- `XDEP-006` — **Activation Compiler Harness**: Upstream semantic authority that produces the rich Activative Intelligence Pack referenced by Builder contracts. Constraint: Builder preserves frozen lineage and sparse references; it does not replace or implement the Activation Compiler.

**Included outcome boundary:**

- No-guidance controls, fresh-context trials, protected benchmark portfolios, category-appropriate dimensions, evaluator isolation, non-compensable gates, repair and invalidation graphs, regressions, and authorization receipts.
- Role clarity, pattern match and interruption, prediction, payoff, affinity, anticipation, residue, anti-cliche, no-text survival, and wrong-reading rejection.

**Excluded boundary:**

- Readiness from document completeness, benchmark leakage, silent threshold invention, or repair outside the responsible layer.

**Completion evidence:** Every readiness outcome is traceable to protected evidence, evaluated artifact identity, threshold authority, targeted repair, and regression results.

**Blocked outcomes and risk:** Implementation readiness and conversational or general certification remain FAIL until both human decisions and all five blocker records are closed with evidence.

## EP-09 — Governed Builder Workflow Factory

**Outcome:** An operator can route a Builder request through a versioned, actor-explicit workflow; run deterministic and agent work at isolated public seams; recover from bounded failures; and promote only workflows that pass end-to-end and fault tests.

**Primary actor:** Builder operator and workflow maintainer

**Release 1 disposition:** `RELEASE_1_INCLUDED_MANUAL_SHADOW_BEFORE_AUTOMATION`

**Depends on:** `EP-01`, `EP-03`, `EP-04`, `EP-05`, `EP-06`, `EP-07`, `EP-08`

**Decision and blocker obligations:** `BD-008`, `BD-010`, `BD-014`

**Primary coverage (62 obligations):**

- `ARCHITECTURE_DECISION` (4): `ADR-006`, `ADR-012`, `ADR-016`, `ADR-017`
- `BINDING_ANTI_GOAL` (4): `AG-011`, `AG-019`, `AG-020`, `AG-021`
- `FUNCTIONAL_REQUIREMENT` (30): `FR-181`, `FR-182`, `FR-183`, `FR-184`, `FR-185`, `FR-186`, `FR-187`, `FR-188`, `FR-189`, `FR-190`, `FR-191`, `FR-192`, `FR-193`, `FR-194`, `FR-195`, `FR-196`, `FR-197`, `FR-198`, `FR-199`, `FR-200`, `FR-201`, `FR-202`, `FR-203`, `FR-204`, `FR-205`, `FR-206`, `FR-207`, `FR-208`, `FR-209`, `FR-210`
- `NON_FUNCTIONAL_REQUIREMENT` (20): `NFR-ARCH-002`, `NFR-PERF-002`, `NFR-PERF-003`, `NFR-PERF-004`, `NFR-PORT-002`, `NFR-REL-004`, `NFR-SEC-004`, `NFR-TEST-001`, `NFR-WORKFLOW-001`, `NFR-WORKFLOW-002`, `NFR-WORKFLOW-003`, `NFR-WORKFLOW-004`, `NFR-WORKFLOW-005`, `NFR-WORKFLOW-006`, `NFR-WORKFLOW-007`, `NFR-WORKFLOW-008`, `NFR-WORKFLOW-009`, `NFR-WORKFLOW-010`, `NFR-WORKFLOW-011`, `NFR-WORKFLOW-012`
- `READINESS_HARD_GATE` (4): `HG-011`, `HG-012`, `HG-013`, `HG-014`

**Cross-repository dependencies:**

- `XDEP-001` — **CMF_PROGRAM_CONTROL**: Supplies constitutional and product authority, cross-repository decision governance, release pins, and convergence status. Constraint: Program records must be synchronized separately; Builder does not mutate program control during this Epic proposal.
- `XDEP-005` — **04_OPERATOR_MANUAL**: Future consumer of approved Control Tower, workflow, incident, and authorization operating procedures. Constraint: Operational documentation follows stable Builder behavior and cannot substitute for implementation evidence.

**Included outcome boundary:**

- Builder Workflow IR, routing, manual shadow workflow, actor ownership, node validation, bounded retries, checkpoint resume, least privilege, safe parallelism, independent evaluation, telemetry, fault tests, CI promotion, migration, rollback, and incident workflows.

**Excluded boundary:**

- Monolithic agent sessions, production workflows hidden in skills, unbounded self-correction, or default parallelization.

**Completion evidence:** One complete Builder workflow can be replayed, observed, fault-injected, resumed, and rejected or promoted through explicit gates.

**Blocked outcomes and risk:** Production promotion remains prohibited while readiness is FAIL and benchmark, skill, or external interface dependencies remain open.

## EP-10 — Evidence-Derived Human Control Tower

**Outcome:** A human can supervise the full Builder run from one approved Control Tower, understand evidence and authority behind every status, inspect category or profile lineage and workflow state, and issue only governed commands without creating a second source of truth.

**Primary actor:** Harness Architect, reviewer, and operator

**Release 1 disposition:** `RELEASE_1_INCLUDED`

**Depends on:** `EP-01`, `EP-03`, `EP-04`, `EP-05`, `EP-06`, `EP-07`, `EP-08`, `EP-09`

**Decision and blocker obligations:** `BD-004`, `BD-008`, `BD-010`, `BD-014`

**Primary coverage (73 obligations):**

- `ARCHITECTURE_DECISION` (2): `ADR-003`, `ADR-011`
- `BINDING_ANTI_GOAL` (1): `AG-016`
- `FUNCTIONAL_REQUIREMENT` (10): `FR-117`, `FR-118`, `FR-119`, `FR-120`, `FR-121`, `FR-122`, `FR-123`, `FR-124`, `FR-125`, `FR-126`
- `LOCKED_DECISION` (1): `D025`
- `NON_FUNCTIONAL_REQUIREMENT` (8): `NFR-OBS-001`, `NFR-OBS-002`, `NFR-OBS-003`, `NFR-OBS-004`, `NFR-PERF-001`, `NFR-TRACE-002`, `NFR-UX-001`, `NFR-UX-002`
- `UX_CONTRACT_CLAUSE` (51): `UXC-001`, `UXC-002`, `UXC-003`, `UXC-004`, `UXC-005`, `UXC-006`, `UXC-007`, `UXC-008`, `UXC-009`, `UXC-010`, `UXC-101`, `UXC-102`, `UXC-103`, `UXC-104`, `UXC-105`, `UXC-106`, `UXC-107`, `UXC-108`, `UXC-109`, `UXC-110`, `UXC-111`, `UXC-112`, `UXC-113`, `UXC-201`, `UXC-202`, `UXC-203`, `UXC-204`, `UXC-205`, `UXC-206`, `UXC-207`, `UXC-208`, `UXC-209`, `UXC-301`, `UXC-302`, `UXC-303`, `UXC-304`, `UXC-305`, `UXC-306`, `UXC-307`, `UXC-401`, `UXC-402`, `UXC-403`, `UXC-404`, `UXC-405`, `UXC-406`, `UXC-407`, `UXC-408`, `UXC-501`, `UXC-502`, `UXC-503`, `UXC-504`

**Cross-repository dependencies:**

- `XDEP-001` — **CMF_PROGRAM_CONTROL**: Supplies constitutional and product authority, cross-repository decision governance, release pins, and convergence status. Constraint: Program records must be synchronized separately; Builder does not mutate program control during this Epic proposal.
- `XDEP-002` — **02_VISUAL_ASSET_EDITOR**: Consumes the Builder Visual Asset Editor target profile and visual-semantic or Asset Demand handoff contracts. Constraint: VAE implementation readiness is FAIL; Builder defines and validates the target profile but does not implement editor behavior.
- `XDEP-003` — **03_DELEGATION_PROTOCOL**: Owns the external Content-to-Asset Delegation runtime and shared contract release consumed by Builder target compilation. Constraint: The 1.1.0-rc.1 candidate is not production-authorized and cross-repository adoption or convergence remains gated.
- `XDEP-004` — **05_FUTURE_PRODUCTS/INTERVIEW_EXPRESSION_HARNESS**: Future owner of Interview Expression and ReelCast live execution, Reaction Receipt capture, Expression Moment extraction, and final content-type contracts. Constraint: Planning is paused after one locked atomic-boundary decision; Builder must not pre-write the final product PRD.
- `XDEP-005` — **04_OPERATOR_MANUAL**: Future consumer of approved Control Tower, workflow, incident, and authorization operating procedures. Constraint: Operational documentation follows stable Builder behavior and cannot substitute for implementation evidence.

**Included outcome boundary:**

- Approved Control Tower routes, projections, graphs, evidence, Genesis, skills, contracts, evaluation, repair, cost, queues, incidents, governed actions, accessibility, and export.

**Excluded boundary:**

- UI-owned authoritative state, hidden operational state, route redesign, or external product consoles.

**Completion evidence:** Every visible state is event-derived and provenance-linked, stale or unavailable projections fail explicitly, and all human actions produce typed command receipts.

**Blocked outcomes and risk:** Cross-product and certification views remain non-authoritative or blocked until their source evidence and external contracts close the relevant decisions.

## EP-11 — Traceable Development Capsule and Implementation Handoff

**Outcome:** An implementation team can receive one versioned Development Capsule containing only justified scaffolding, typed contracts, fixtures, dependency ordering, acceptance evidence, and frozen authority needed to implement a complete vertical slice without inventing product decisions.

**Primary actor:** Implementation lead and Harness Architect

**Release 1 disposition:** `RELEASE_1_INCLUDED_HANDOFF_ONLY_NO_IMPLEMENTATION_AUTHORIZATION`

**Depends on:** `EP-03`, `EP-04`, `EP-05`, `EP-06`, `EP-07`, `EP-08`, `EP-09`, `EP-10`

**Decision and blocker obligations:** `HD-006`, `HD-007`, `BD-004`, `BD-008`, `BD-010`, `BD-014`

**Primary coverage (10 obligations):**

- `FUNCTIONAL_REQUIREMENT` (9): `FR-151`, `FR-152`, `FR-153`, `FR-154`, `FR-155`, `FR-156`, `FR-157`, `FR-158`, `FR-159`
- `LOCKED_DECISION` (1): `D029`

**Cross-repository dependencies:**

- `XDEP-001` — **CMF_PROGRAM_CONTROL**: Supplies constitutional and product authority, cross-repository decision governance, release pins, and convergence status. Constraint: Program records must be synchronized separately; Builder does not mutate program control during this Epic proposal.
- `XDEP-002` — **02_VISUAL_ASSET_EDITOR**: Consumes the Builder Visual Asset Editor target profile and visual-semantic or Asset Demand handoff contracts. Constraint: VAE implementation readiness is FAIL; Builder defines and validates the target profile but does not implement editor behavior.
- `XDEP-003` — **03_DELEGATION_PROTOCOL**: Owns the external Content-to-Asset Delegation runtime and shared contract release consumed by Builder target compilation. Constraint: The 1.1.0-rc.1 candidate is not production-authorized and cross-repository adoption or convergence remains gated.
- `XDEP-004` — **05_FUTURE_PRODUCTS/INTERVIEW_EXPRESSION_HARNESS**: Future owner of Interview Expression and ReelCast live execution, Reaction Receipt capture, Expression Moment extraction, and final content-type contracts. Constraint: Planning is paused after one locked atomic-boundary decision; Builder must not pre-write the final product PRD.
- `XDEP-005` — **04_OPERATOR_MANUAL**: Future consumer of approved Control Tower, workflow, incident, and authorization operating procedures. Constraint: Operational documentation follows stable Builder behavior and cannot substitute for implementation evidence.

**Included outcome boundary:**

- Development Capsule generation, requirement traceability, contract examples, fixtures, first vertical-slice plan, implementation delta governance, and feedback ingestion.

**Excluded boundary:**

- Production implementation in this planning step, Story authoring before Step 3 confirmation, or external product runtime code.

**Completion evidence:** The capsule is complete, hash-bound, dependency-ordered, evidence-backed, and explicitly marked authorized, prototype-only, or blocked.

**Blocked outcomes and risk:** No implementation authorization may be issued while readiness is FAIL or any required human decision and blocker remains open.

## EP-12 — Brownfield Migration and Release 1 Reference Proof

**Outcome:** The team can preserve proven V2.1 behavior, migrate only with evidence and receipts, dual-compile eligible targets, and prove the complete Builder spine through one Format 02 reference path without overstating category or target certification.

**Primary actor:** Product lead, maintainer, and release reviewer

**Release 1 disposition:** `RELEASE_1_FORMAT02_REFERENCE_PROOF_GENERAL_CERTIFICATION_DEFERRED`

**Depends on:** `EP-06`, `EP-07`, `EP-08`, `EP-09`, `EP-10`, `EP-11`

**Decision and blocker obligations:** `HD-006`, `HD-007`, `BD-004`, `BD-007`, `BD-008`, `BD-010`, `BD-014`

**Primary coverage (17 obligations):**

- `ARCHITECTURE_DECISION` (2): `ADR-014`, `ADR-015`
- `BINDING_ANTI_GOAL` (1): `AG-017`
- `FUNCTIONAL_REQUIREMENT` (10): `FR-160`, `FR-161`, `FR-162`, `FR-163`, `FR-164`, `FR-165`, `FR-166`, `FR-167`, `FR-168`, `FR-169`
- `LOCKED_DECISION` (3): `D003`, `D028`, `D032`
- `NON_FUNCTIONAL_REQUIREMENT` (1): `NFR-COMPAT-001`

**Cross-repository dependencies:**

- `XDEP-001` — **CMF_PROGRAM_CONTROL**: Supplies constitutional and product authority, cross-repository decision governance, release pins, and convergence status. Constraint: Program records must be synchronized separately; Builder does not mutate program control during this Epic proposal.
- `XDEP-002` — **02_VISUAL_ASSET_EDITOR**: Consumes the Builder Visual Asset Editor target profile and visual-semantic or Asset Demand handoff contracts. Constraint: VAE implementation readiness is FAIL; Builder defines and validates the target profile but does not implement editor behavior.
- `XDEP-003` — **03_DELEGATION_PROTOCOL**: Owns the external Content-to-Asset Delegation runtime and shared contract release consumed by Builder target compilation. Constraint: The 1.1.0-rc.1 candidate is not production-authorized and cross-repository adoption or convergence remains gated.
- `XDEP-004` — **05_FUTURE_PRODUCTS/INTERVIEW_EXPRESSION_HARNESS**: Future owner of Interview Expression and ReelCast live execution, Reaction Receipt capture, Expression Moment extraction, and final content-type contracts. Constraint: Planning is paused after one locked atomic-boundary decision; Builder must not pre-write the final product PRD.
- `XDEP-005` — **04_OPERATOR_MANUAL**: Future consumer of approved Control Tower, workflow, incident, and authorization operating procedures. Constraint: Operational documentation follows stable Builder behavior and cannot substitute for implementation evidence.
- `XDEP-006` — **Activation Compiler Harness**: Upstream semantic authority that produces the rich Activative Intelligence Pack referenced by Builder contracts. Constraint: Builder preserves frozen lineage and sparse references; it does not replace or implement the Activation Compiler.

**Included outcome boundary:**

- V2.1 inventory and concept mapping, dual compilation, incremental regression, compatibility aliases, migration receipts, Format 02 Release 1 proof, structural support for other categories and targets, and bounded certification claims.

**Excluded boundary:**

- General Builder certification from one harness, production certification of Interview or ReelCast profiles, or production VAE and Delegation implementation.

**Completion evidence:** Release 1 proves one complete Format 02 vertical path and publishes an explicit certification matrix that leaves all unproven categories, profiles, and targets uncertified.

**Blocked outcomes and risk:** Release certification and production authorization remain blocked until HD-006, HD-007, BD-004, BD-007, BD-008, BD-010, BD-014, and cross-repository gates are resolved.


## Step boundary

- Epic proposal status: `AWAITING_HUMAN_CONFIRMATION`.
- Vertical Story authoring: `NOT_AUTHORIZED`.
- Production implementation: `PROHIBITED_READINESS_FAIL`.
- Visual Asset Editor and Delegation Protocol implementation: outside Builder ownership.
- Next action: human confirms or corrects the Epic inventory and primary coverage before Step 3 begins.
