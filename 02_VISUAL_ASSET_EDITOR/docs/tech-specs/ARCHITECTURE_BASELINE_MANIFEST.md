# CMF Visual Asset Editor Architecture Baseline Manifest

Date: 2026-07-14  
Baseline class: documentary, contractual, and verified specification tooling  
Executable architecture status: VAE and target Atomic Harness Builder runtime absent; Spec Builder V2.1 verified

## Purpose

This manifest separates the frozen upstream architecture, the editor-owned product delta, the shared Delegation boundary, and provider artifacts. It is the Stage 1 guardrail for technical specification authoring. It does not claim that documentary architecture is executable.

## Authority and ownership

| Boundary | Owner | Visual Asset Editor obligation | Local evidence | Verification status |
|---|---|---|---|---|
| Content meaning, Activative purpose, sequence role, final composition intent | Content Harness | Consume immutable authorized demand; never reinterpret or silently relax it. | `governance/PRODUCT_CONSTITUTION.yaml`, PRES-017, AG-002, AG-018 | Contractual only; owner repository absent. |
| Harness IR, Builder Workflow Runtime, JIT Skills, category constitutions, Content Harness semantic authority | Atomic Harness Builder | Integrate through frozen interfaces; do not duplicate or redesign. | Exact-hash SRC-001 PRD archive; exact-hash SRC-002 Spec Builder archive; `validation/BUILDER_EVIDENCE_RECONCILIATION_2026-07-14.md` | PRD and executable Spec Builder verified; target runtime checkout, symbols, contracts, and extension points absent. |
| Shared demand, submission, event, conflict, and result contracts | Delegation repository | Consume a pinned version through an adapter; keep local fixtures provisional. | RC2 `packages/contracts/registry.json`; `docs/contracts/CONTRACT_COMPATIBILITY_MATRIX.yaml` | Coherent unsigned RC2 reconciled across 26 messages; one consumer path incompatible; no published production pin. |
| Production planning, capability routing, execution coordination, production evaluation, repair, promotion, and Asset Result acceptance | Visual Asset Editor | Define and implement editor-local canonical state and acceptance. | PRD features F01-F22; allowed extensions in preservation contract | Specified only; no executable implementation. |
| Final Format 02 sequence, deterministic text, timing, and composition | Format 02 Content Harness and downstream Remotion runtime | Return assets, geometry, receipts, and limitations; support downstream validation. | `reference-slice/FORMAT02_MINIMAL_COACH_THEATRE/README.md` | Reference doctrine only; consumer repository absent. |

## Canonical state boundaries

1. The accepted Visual Asset Demand is immutable external authority. Notes are non-authoritative enrichment.
2. Visual Production Plan IR is the editor-local canonical production plan. It may version and amend production bindings without mutating the accepted demand.
3. Runtime events and immutable asset/lifecycle records are operational truth for execution and production acceptance.
4. ComfyUI JSON is a compiled, pinned provider artifact. It is never canonical product state.
5. CMF-OKF is a portable knowledge projection. It is never canonical workflow, lifecycle, budget, queue, contract, registry, or secret state.
6. The producing model cannot approve its own output. Independent evaluation authority is mandatory.

## Frozen upstream architecture

All 18 preservation rules are applicable. Their source is `governance/ARCHITECTURE_PRESERVATION_CONTRACT.yaml`.

| ID | Frozen mechanism | Required editor treatment | Local executable evidence |
|---|---|---|---|
| PRES-001 | Three independent compilation targets | Keep Atomic Content Harness, Visual Asset Editor, and Delegation as separate products. | None |
| PRES-002 | Canonical Harness IR | Keep Harness IR upstream; Visual Production Plan IR is editor-local and cannot replace it. | None |
| PRES-003 | Capability Ownership Map | Preserve explicit ownership across code, typed model programs, JIT Skills, references, humans, evaluators, adapters, and hybrids. | None |
| PRES-004 | Phase and Context Graphs | Preserve phase-local context, progressive disclosure, and output-only downstream handoffs. | None |
| PRES-005 | Typed Contract Graph | Use typed, versioned, validated, non-mutable cross-phase and cross-product contracts. | Provisional schema seeds only |
| PRES-006 | Canonical Skill Ecology | Keep Canonical Skills, harness adaptations, composition recipes, and JIT Execution Capsules separate. | None |
| PRES-007 | Deterministic JIT compiler | Preserve deterministic, receipted capsule and context assembly. | None |
| PRES-008 | Reference and Loading Graph | Keep doctrine, registries, examples, and SPR resources versioned and phase-local. | Static registries only |
| PRES-009 | Dependency and Precedence Resolver | Resolve authority, conflict, missing data, invalidation, and degradation before execution. | None |
| PRES-010 | Behavioral evaluation and maturity | Require evidence before production maturity for skills, adaptations, recipes, capsules, and generated systems. | Maturity labels and benchmark seed only |
| PRES-011 | Builder Workflow Runtime | Preserve explicit human, agent, and deterministic actors in typed event-sourced workflows. | None |
| PRES-012 | Harness Control Tower | Extend the event-sourced Control Tower through projections; do not create a disconnected authority store. | None |
| PRES-013 | Repair and Invalidation Graph | Preserve smallest-responsible repair, frozen valid state, downstream invalidation, regression, and receipts. | Repair schema seed only |
| PRES-014 | Implementation Authorization Gate | Treat readiness as evidence-backed authorization, not document completion. | Static hard-gate registry only |
| PRES-015 | Development Capsule | Hand implementation a traceable authorized package, not speculative scaffolding. | No capsule present |
| PRES-016 | Four category constitutions | Preserve Short-Form Edited Video, 2D Character Animation, Carousels, and Supervisuals as separate governed categories. | Referenced doctrine only |
| PRES-017 | Content Harness semantic authority | Keep meaning, Activative purpose, sequence role, and final composition intent upstream. | Static constitution and schemas only |
| PRES-018 | Activative Sequencing Intelligence | Supply assets and geometry; do not replace category/format sequencing authority. | Format 02 reference fixtures only |

The exact frozen PRD and Spec Builder sources are now available, and the Spec Builder's 28 tests pass. Those artifacts do not contain the target Atomic Harness Builder runtime. The rows above remain constraints to verify against a pinned runtime release, not proof that runtime integration points exist.

## Editor-owned architecture delta

The preservation contract allows the editor to own these additions:

| Delta | Existing seed | Missing executable baseline |
|---|---|---|
| Demand intake and authority validation | Demand and submission schemas, Format 02 fixture | API, identity/authorization, validation, idempotency store |
| Visual Production Plan IR | Plan schema and fixture | Domain model, validator, versioning, compiler, persistence |
| Asset ontology and immutable lifecycle | Asset-family registry, memory/result schemas | Lifecycle store, transition engine, supersession, variants |
| Dynamic specialist workcell | Authority registry | Workcell compiler and workflow bindings |
| Capability and compatibility registries | Compatibility manifest seed | Workflow/model/VAE/LoRA/control/runtime registries and resolver |
| ComfyUI/provider compilation | Provider-binding fields in plan seed | Compiler, graph validation, lock manifests, adapters |
| Visual compute fabric | Benchmark release-proof declaration | Docker images, GPU workers, scheduler, storage, isolation, recovery |
| Independent evaluation and repair | Evaluation/repair schemas and fixtures | Deterministic validators, VLM adapters, calibration, repair runtime |
| Candidate portfolios and budgets | Budget schema and six-program registry | Estimator, scheduler enforcement, selector, receipts |
| Visual Asset Memory and steering | Memory/recipe schemas and OKF profile | Operational store, retrieval, projections, promotion workflow |
| Async service and Control Tower projections | Submission/event/result schemas | Service, queue, event store, public states, UI, telemetry |
| Release 1 Format 02 proof | Contract fixtures, six seed registries, benchmark manifest | Local/cloud execution, accepted asset, repair, geometry, Remotion consumption |

## Binding prohibitions

All 24 prohibitions in `governance/ARCHITECTURAL_PROHIBITIONS.json` are hard gates. The Stage 2 architecture must attach an enforcing component and a test to each prohibition. High-risk prohibitions are:

- no Builder redesign or duplication;
- no transfer of Content Harness meaning or final composition authority;
- no ComfyUI JSON as canonical state;
- no one-agent or fixed-chain workcell;
- no producer self-approval;
- no first-passing-candidate selection;
- no blind retries or more than three autonomous quality repairs;
- no frequency-only fatigue judgment;
- no OKF/vector store as canonical truth;
- no one-success Steering Recipe or one-failure LoRA training;
- no silent demand relaxation, unpinned in-flight update, or uncertified scope claim;
- no routine manual ComfyUI operation;
- no PRD-complete-equals-implementation-authorized shortcut.

## Version and compatibility baseline

| Layer | Current local version/status | Required Stage 2 decision |
|---|---|---|
| VAE PRD package | `0.1.0-draft`, `draft_for_review` | Define product/release versioning independently of document version. |
| Architecture preservation contract | `1.0.0`, binding | Pin the exact upstream Builder target profile and source hash. |
| Local schemas | PRD-level seeds | Split editor-local schemas from imported Delegation package schemas. |
| Delegation contract | Coherent unsigned RC2 reconciled; 26 messages; 20 `COMPATIBLE`, 4 adapter, 1 migration, 1 `INCOMPATIBLE`; package validator PASS and 42 tests PASS; no published production pin | Fix the missing VAE amendment-response consumer, publish/sign, pin generated bindings, and execute VAE adapter conformance. |
| Format 02 reference slice | Architecture seed | Pin category/format profile versions and downstream consumer contract. |
| Models, VAE, LoRA, workflows, custom nodes | Absent | Define immutable registries, hashes, compatibility, promotion, and rollback. |
| Local/cloud compute profiles | Absent | Define image digest, driver/CUDA constraints, storage, health, and recovery. |

## Baseline gaps that block architecture closure

1. The frozen Builder PRD and executable Spec Builder are available, but no tagged target Atomic Harness Builder runtime exists to map VAE ports to real workflow, event, Control Tower, repair, or Development Capsule extension symbols.
2. The Delegation RC2 registry is fully enumerated and coherent, but the package is unsigned/unpublished and `amendment-response` omits the required VAE consumer.
3. No product runtime exists from which to preserve local behavior, replace legacy behavior, or derive deployment constraints.
4. No local or cloud GPU environment, ComfyUI lock, model set, or custom-node set exists to establish a reproducible provider baseline.
5. No evaluator dataset or downstream composition consumer exists to establish production acceptance thresholds.

The locked decision-to-architecture delta is registered in `docs/tech-specs/DELTA_ADR_REGISTER.md`; per-requirement evidence is in `docs/tech-specs/VAE_REQUIREMENT_COVERAGE_MATRIX.csv`.
