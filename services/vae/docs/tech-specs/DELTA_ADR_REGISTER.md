# CMF Visual Asset Editor Delta ADR Register

Date: 2026-07-14  
Register status: Stage 1 proposed ADR set  
Decision authority: `governance/DECISION_REGISTER.md` and `governance/DECISION_REGISTER.json`

## Register rules

The 28 product decisions are locked and are not reopened by these ADRs. Each ADR must document how the decision is realized through existing upstream extension points and editor-owned components, including alternatives rejected, versioning, migration, rollback, enforcing tests, and prohibition checks.

`Verdict` uses only the attached Stage 1 taxonomy. It describes repository coverage, not the status of the locked product decision. Full decision-to-FR traceability remains in `governance/DECISION_TO_REQUIREMENT_MAP.csv` and `docs/tech-specs/VAE_REQUIREMENT_COVERAGE_MATRIX.csv`.

## Locked decision coverage

| ADR seed | Locked decision and features | Concrete repository evidence | Coverage verdict | Required implementation delta | Owning specification |
|---|---|---|---|---|---|
| ADR-VAE-001 | D001 Complete visual asset-resolution system; F01, F22 | `governance/PRODUCT_CONSTITUTION.yaml`; `governance/READINESS_HARD_GATES.yaml` | `PARTIALLY_IMPLEMENTED` | Define bounded contexts, canonical stores, service/runtime boundaries, and evidence-backed authorization across the whole product. | All; TS-VAE-10 integration |
| ADR-VAE-002 | D002 Autonomous production with exception-only human intervention; F01, F07, F15, F16, F18, F20 | `governance/WORKCELL_AUTHORITY_REGISTRY.yaml`; `governance/BUDGET_PROGRAM_REGISTRY.yaml` | `PARTIALLY_IMPLEMENTED` | Define policy engine, typed exceptions, human authority checks, autonomous transitions, and no-routine-approval tests. | TS-VAE-02, 05, 07, 09 |
| ADR-VAE-003 | D003 Typed Visual Asset Demand is authoritative; F02, F09, F19, F20, F22 | `contracts/schemas/VISUAL_ASSET_DEMAND.schema.yaml`; `contracts/README.md` | `PARTIALLY_IMPLEMENTED` | Import the Delegation-owned schema, pin its version, validate authority, preserve immutability, and isolate local enrichment. | TS-VAE-01, 09, 10 |
| ADR-VAE-004 | D004 Layered asset effectiveness; F01, F05, F14, F21 | `contracts/schemas/VISUAL_QUALITY_EVALUATION.schema.yaml`; Format 02 benchmark manifest | `NEEDS_EMPIRICAL_PROTOTYPE` | Establish measurable production-validity, semantic, Activative, and composition gates with calibrated independent evaluation. | TS-VAE-06, 10 |
| ADR-VAE-005 | D005 Governed multi-method resolution; F03, F06, F09 | `contracts/schemas/VISUAL_PRODUCTION_PLAN.schema.yaml#properties.route,fallback_routes`; asset-family registry | `PARTIALLY_IMPLEMENTED` | Define route registry, deterministic eligibility, expected-value selection, fallback, receipts, and route-learning boundaries. | TS-VAE-02, 03 |
| ADR-VAE-006 | D006 Canonical asset-family ontology; F03, F06, F11 | `governance/ASSET_FAMILY_REGISTRY.yaml` | `PARTIALLY_IMPLEMENTED` | Define persisted ontology versions, migration, subtype capability requirements, and represented-versus-certified scope checks. | TS-VAE-01, 08, 10 |
| ADR-VAE-007 | D007 Reference Evidence and Production Assets remain distinct; F03, F04 | Demand, memory, and result schemas | `PARTIALLY_IMPLEMENTED` | Define separate records, promotion authority, provenance, lifecycle transitions, and tests that references cannot ship as accepted assets implicitly. | TS-VAE-01, 08, 10 |
| ADR-VAE-008 | D008 Immutable versioned asset lineage; F04, F11, F19 | `VISUAL_ASSET_MEMORY_RECORD` and `ASSET_RESULT_CONTRACT` schemas | `PARTIALLY_IMPLEMENTED` | Select immutable persistence, content addressing, derivation graph, supersession events, variant rules, and retention. | TS-VAE-08, 09 |
| ADR-VAE-009 | D009 Typed Composition Intent and image-conditioned geometry; F02, F05, F09, F11, F19, F20 | Demand composition fields; `COMPOSITION_GEOMETRY` and `CONSTRAINT_CONFLICT` schemas | `NEEDS_EMPIRICAL_PROTOTYPE` | Prove extraction accuracy, coordinate conventions, tolerance checks, safe crops, collision analysis, and downstream Remotion consumption. | TS-VAE-01, 10 |
| ADR-VAE-010 | D010 Dynamic specialist workcell; F01, F06, F07, F14 | `governance/WORKCELL_AUTHORITY_REGISTRY.yaml` | `PARTIALLY_IMPLEMENTED` | Define smallest-sufficient workcell compilation, actor contracts, authority checks, and producer/evaluator separation. | TS-VAE-02, 06 |
| ADR-VAE-011 | D011 Versioned Visual Capability Registry; F06, F08, F09, F12 | Compatibility manifest has registry references; no capability registry implementation exists | `NEEDS_EMPIRICAL_PROTOTYPE` | Prototype provider discovery and define workflow, model, VAE, LoRA, control, runtime, compatibility, maturity, and impact registries. | TS-VAE-02, 03, 04 |
| ADR-VAE-012 | D012 Provider-neutral Visual Production Plan IR; F05, F06, F07, F09 | `VISUAL_PRODUCTION_PLAN.schema.yaml` and Format 02 fixture | `PARTIALLY_IMPLEMENTED` | Define canonical IR invariants, type system, plan amendments, preservation bindings, deterministic compilation, schema evolution, and validation. | TS-VAE-01, 03 |
| ADR-VAE-013 | D013 Event-sourced resumable production graph; F04, F07, F09, F10, F12, F15 | Plan, event, and repair schemas | `PARTIALLY_IMPLEMENTED` | Choose event store and workflow engine; define node state, sequence/order, idempotency, checkpoints, retries, cancellation, backpressure, replay, and recovery. | TS-VAE-07, 09 |
| ADR-VAE-014 | D014 Syntax-aware Visual Asset Memory; F04, F11, F17, F18 | Memory schema and `governance/CMF_OKF_PROFILE.yaml` | `NEEDS_EMPIRICAL_PROTOTYPE` | Prove contextual recurrence, multimodal retrieval, contradiction coverage, and fatigue classification while keeping OKF non-authoritative. | TS-VAE-08 |
| ADR-VAE-015 | D015 Hybrid containerized Visual Compute Fabric; F08, F10, F12 | Benchmark manifest requests local/cloud proof; no Docker or worker assets exist | `NEEDS_EMPIRICAL_PROTOTYPE` | Prove pinned local and cloud GPU execution; then define scheduling, mounted models, storage, isolation, health, failover, and receipts. | TS-VAE-04 |
| ADR-VAE-016 | D016 Governed visual capability development; F08, F13 | Benchmark manifest includes one capability-development cycle; no pipeline exists | `NEEDS_EMPIRICAL_PROTOTYPE` | Prove dataset preparation, baseline comparison, contamination checks, LoRA/workflow promotion, rollback, and one-failure prohibition. | TS-VAE-11 |
| ADR-VAE-017 | D017 Versioned Visual Evaluation Profiles; F04, F05, F07, F08, F10, F11, F14, F15, F21 | Quality-evaluation schema, fixture, and benchmark seed | `NEEDS_EMPIRICAL_PROTOTYPE` | Build a labeled set and calibrate profile gates, evaluator versions, arbitration, failure recall, temporal checks, and protected release cases. | TS-VAE-06 |
| ADR-VAE-018 | D018 Typed causal repair and invalidation; F04, F05, F06, F07, F09, F10, F14, F15, F20, F21 | Repair schema and fixture; three-round budget ceiling | `PARTIALLY_IMPLEMENTED` | Define causal binding deltas, preserve lists, invalidation graph, checkpoint reuse, regression tests, and terminal escalation. | TS-VAE-07 |
| ADR-VAE-019 | D019 Budgeted candidate portfolios and Budget Programs; F02, F06, F08, F09, F10, F12, F13, F16, F17, F18, F21 | Budget schema and six-program registry | `PARTIALLY_IMPLEMENTED` | Complete time/cost limits and define estimation, authorization, portfolio compilation, controlled variation, selection, early stop, adaptive expansion, and receipts. | TS-VAE-05 |
| ADR-VAE-020 | D020 Governed Visual Steering Intelligence with CMF-OKF projection; F06, F11, F13, F14, F15, F16, F17, F18, F21 | Steering-recipe schema, memory schema, and OKF profile | `NEEDS_EMPIRICAL_PROTOTYPE` | Prove retrieval/reranking and define evidence aggregation, promotion states, recipe compatibility, contradiction handling, projection, and rollback. | TS-VAE-08, 11 |
| ADR-VAE-021 | D021 Visual Asset Editor Control Tower specialization; F10, F11, F12, F16, F17, F18, F22 | PRES-012 and PRD F18 only; no UI or upstream extension point is locally available | `NEW_IMPLEMENTATION` | Verify the upstream event/projection API and define editor projections without creating a second authority store. | TS-VAE-09 |
| ADR-VAE-022 | D022 Inspectable supervisory console; F07, F16, F18 | Workcell and budget policy data only; no frontend exists | `NEW_IMPLEMENTATION` | Define views, policy-first controls, authorization, evidence comparison, accessibility, typed exceptions, and operational analytics. | TS-VAE-09 |
| ADR-VAE-023 | D023 Asynchronous contract-driven service; F02, F04, F10, F12, F18, F19, F22 | Submission, event, and result schemas; Delegation handoff | `PARTIALLY_IMPLEMENTED` | Consume the versioned Delegation dependency and define API, durable receipt, event delivery, polling/subscription, object references, cancellation, and backpressure. | TS-VAE-01, 09 |
| ADR-VAE-024 | D024 Typed constraint conflict and amendment proposal; F02, F05, F09, F15, F18, F19, F20 | Constraint-conflict schema and Format 02 fixture | `PARTIALLY_IMPLEMENTED` | Define conflict detection, internal plan amendments, upstream proposals, degraded acceptance authority, new demand versions, and audit events. | TS-VAE-01, 07, 09 |
| ADR-VAE-025 | D025 Layered benchmark portfolio and staged certification; F03, F08, F12, F13, F14, F16, F21, F22 | Format 02 benchmark manifest | `NEEDS_EMPIRICAL_PROTOTYPE` | Materialize cases, labels, runners, protected sets, promotion stages, recovery tests, compatibility tests, and evidence thresholds. | TS-VAE-06, 10, 11 |
| ADR-VAE-026 | D026 Release 1 Format 02 reference vertical slice; F03, F13, F21, F22 | Format 02 README, six contract fixtures, six seed registries, benchmark manifest | `PARTIALLY_IMPLEMENTED` | Bind one real demand through local/cloud provider interfaces, one portfolio, validation, independent evaluation, one repair, immutable result, geometry, and downstream composition. | TS-VAE-10 |
| ADR-VAE-027 | D027 Independent versioning with governed compatibility; F02, F03, F04, F08, F10, F12, F13, F14, F17, F19, F20, F21, F22 | `COMPATIBILITY_MANIFEST.schema.yaml`; version fields across schemas and registries | `PARTIALLY_IMPLEMENTED` | Define compatibility policy, package boundaries, pinning, semver behavior, migrations, release checks, in-flight immutability, rollback, and deprecation. | Cross-cutting; TS-VAE-03, 04, 09, 10 |
| ADR-VAE-028 | D028 Formal implementation authorization gate; F01, F02, F13, F19, F21, F22 | `governance/READINESS_HARD_GATES.yaml`; prohibitions; architecture handoff | `PARTIALLY_IMPLEMENTED` | Implement evidence collection and gate evaluation only after architecture, contracts, fixtures, compute/evaluator proof, benchmarks, stories, specs, compatibility, and capsule exist. | Cross-cutting; TS-VAE-10/readiness |

## Cross-repository dependencies

| Issue | Affected ADRs | Required resolution before ADR acceptance |
|---|---|---|
| CR-001 Target Builder runtime unavailable | 001, 002, 005, 010, 013, 021, 027, 028 | Recovered PRD/Spec Builder evidence is insufficient; pin the target runtime release and map real symbols, events, schemas, and extension points. |
| CR-002, CR-003, CR-007 Delegation package/boundary incomplete | 003, 008, 009, 012, 023, 024, 027, 028 | Fix package coherence and the missing VAE amendment-response consumer, publish/sign, pin generated bindings, complete result migration, and execute conformance. |
| CR-004 Format 02 downstream consumer unavailable | 004, 009, 017, 025, 026 | Supply the Content Harness/Remotion consumption contract and executable composition acceptance path. |
| CR-005 Source integrity incomplete | All | Restore exact `SRC-009`; nine other registered local sources now pass exact hashes. |

## ADR authoring order

1. Authority and canonical state: ADR-VAE-003, 012, 023, 024, 027.
2. Frozen integration model: ADR-VAE-001, 002, 005, 010, 013, 021, 028.
3. Provider and compute: ADR-VAE-011, 015.
4. Evaluation, repair, and budgets: ADR-VAE-004, 017, 018, 019, 025.
5. Memory and capability learning: ADR-VAE-006, 007, 008, 014, 016, 020.
6. Release 1 and operator surface: ADR-VAE-009, 022, 026.

No ADR may be marked accepted solely because its corresponding product decision is locked. Acceptance requires concrete upstream mappings, specified interfaces, failure behavior, migration/rollback, and executable test obligations.
