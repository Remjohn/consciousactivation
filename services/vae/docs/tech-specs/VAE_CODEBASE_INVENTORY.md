# CMF Visual Asset Editor Codebase Inventory

Date: 2026-07-14  
Stage: 1 - repository and requirement audit  
Implementation authorization: not granted

## Audit authority and method

The attached lead-architect directive supplies the Stage 1 verdict taxonomy and output contract. No `AGENTS.md` exists in this checkout, either workspace root, or the searched parent package directory. The attachment therefore governs this audit.

The complete primary PRD package was read through its combined view, canonical shards, 22 feature shards, cross-cutting NFRs, governance registers, handoff documents, contracts, reference slice, validation artifacts, and utility scripts. Coverage was not inferred from names or prose. Schema fields, fixtures, registry records, and script behavior were inspected; repository-wide searches were used to establish absent code, tests, workflows, and deployment assets.

## Repository identity

| Property | Verified result | Evidence |
|---|---|---|
| Checkout type | PRD, governance, contract-seed, and reference-fixture package | `README.md`, `prd/index.md`, full file inventory |
| Git metadata | Not present; `git status --short` returns `not a git repository` | Repository root inspection |
| Pre-audit package files | 123 | Recursive file inventory before Stage 1 outputs |
| Pre-audit extensions | 64 Markdown, 44 YAML, 11 JSON, 2 Python, 2 CSV | Recursive extension inventory |
| Product source code | None | No application/source package or service entry point found |
| Executable tests | None | No test suite, test runner, or test directory found |
| Build/package manifests | None | No npm, Python packaging, Rust, Go, Java, .NET, Make, or Just manifest found |
| CI/CD workflows | None | No `.github`, GitLab CI, Azure pipeline, or equivalent workflow asset found |
| Deployment assets | None | No Dockerfile, Compose, Helm, Kubernetes, Terraform, or deployment directory found |

## Existing executable code

Only two PRD-package utilities exist:

| File and symbol | Actual behavior | Coverage boundary |
|---|---|---|
| `scripts/rebuild_combined_prd.py` | Rebuilds `prd/PRD_COMBINED.md` from an explicit ordered shard list, strips shard frontmatter, and rebases local links. | Documentation assembly only; no product behavior. |
| `scripts/validate_prd_package.py::main` | Checks requirement and decision counts, feature-shard ID continuity, selected schema root keys, preservation-contract size, placeholders, links, source hashes, and manifest hashes. | PRD package structure only. It does not execute product contracts, validate all examples, run services, compile ComfyUI graphs, or test runtime behavior. |

No service, worker, scheduler, API, UI, database layer, event store, object-store adapter, provider adapter, ComfyUI compiler, VLM evaluator, repair engine, or Control Tower projection is present.

## Schemas and contract fixtures

The package contains 13 YAML JSON Schemas under `contracts/schemas/`:

- Shared-boundary provisional schemas: `VISUAL_ASSET_DEMAND`, `VISUAL_ASSET_SUBMISSION`, `VISUAL_ASSET_EVENT`, `ASSET_RESULT_CONTRACT`, and `CONSTRAINT_CONFLICT`.
- Editor-local seed schemas: `VISUAL_PRODUCTION_PLAN`, `VISUAL_QUALITY_EVALUATION`, `VISUAL_REPAIR_CONTRACT`, `COMPOSITION_GEOMETRY`, `BUDGET_PROGRAM`, `VISUAL_ASSET_MEMORY_RECORD`, `VISUAL_STEERING_RECIPE`, and `COMPATIBILITY_MANIFEST`.

Six Format 02 examples exist under `contracts/examples/`, with six corresponding reference contracts under `reference-slice/FORMAT02_MINIMAL_COACH_THEATRE/contracts/`. `contracts/README.md` explicitly classifies these as PRD-level starting points, not production protocol releases. The shared schemas are therefore provisional evidence and must not be promoted as editor-owned canonical contracts.

`validation/SCHEMA_VALIDATION_REPORT.json` records six example/schema PASS results. There is no checked-in executable that reproduces those instance validations. The current validator only checks that each schema parses and has `$schema`, `title`, `type`, `required`, and `properties` at its root.

As an independent Stage 1 check, all six example/schema pairs were validated directly with a Draft 2020-12 JSON Schema validator and passed. This confirms the current fixture shapes, but the one-off audit command is not a substitute for a checked-in conformance test suite.

## Registries and structured governance

| Asset | Concrete content | Current status |
|---|---|---|
| `governance/ASSET_FAMILY_REGISTRY.yaml` | Eight asset families, required bindings, lifecycle labels, and Release 1 certification scope. | Draft architecture input; no runtime consumer. |
| `governance/BUDGET_PROGRAM_REGISTRY.yaml` | Six programs and the three-round constitutional repair ceiling. | Draft architecture input; no scheduler or enforcement. |
| `governance/WORKCELL_AUTHORITY_REGISTRY.yaml` | Seven authorities with `owns` and `must_not_own` boundaries. | Binding design data; no workcell compiler. |
| `governance/CMF_OKF_PROFILE.yaml` | Non-authoritative knowledge projection, typed edges, and retrieval pipeline. | Draft profile; no storage or retrieval implementation. |
| `governance/READINESS_HARD_GATES.yaml` | Authorization states, ten implementation gates, production hard gates, and blockers. | Binding governance data; no transition/enforcement engine. |
| `governance/ARCHITECTURE_PRESERVATION_CONTRACT.yaml` | Eighteen frozen upstream rules and allowed editor extensions. | Binding architecture constraint; upstream implementation unavailable locally. |
| `governance/ARCHITECTURAL_PROHIBITIONS.json` | Twenty-four hard-gate prohibitions. | Binding design constraint; no executable policy checks. |

The Format 02 reference slice also has six seed registries for character identity, pose, expression, gesture, animation primitives, and scene configuration. These are architecture seeds, not certified runtime registries.

## Tests and validation

No executable product tests exist. The checked-in reports establish document-package consistency at a prior point in time, not current product readiness:

- `validation/ID_COVERAGE_REPORT.json` records 176 FRs, 70 NFRs, 28 decisions, and 16 journeys with no duplicate requirement IDs.
- `validation/SCHEMA_VALIDATION_REPORT.json` records six representative example passes, but the generating validator is absent.
- Independent Stage 1 validation reproduced six of six example/schema passes with Draft 2020-12 validation.
- All 44 YAML files, 11 JSON files, and two Python utilities parse successfully in the current checkout.
- `validation/PRD_VALIDATION_REPORT.md` and `LOCAL_VERIFICATION.json` record PASS on 2026-07-13.
- A current run of `python scripts/validate_prd_package.py` returns FAIL because registered local sources SRC-001 through SRC-010 are absent at their `/mnt/data/...` paths.
- The current source-integrity failure and the saved PASS reports are inconsistent until the registered source bundle is restored or the source register is intentionally rebased and re-hashed.

## Workflows and deployment

There are no production workflows or deployment assets to preserve or align. In particular, the repository has no:

- ComfyUI workflow JSON, graph compiler, custom-node lock, model manifest, VAE registry, or LoRA registry;
- Docker image, GPU worker image, local runtime profile, cloud runtime profile, or provider adapter;
- queue, event bus, database schema, migration, object-storage layout, checkpoint store, or recovery script;
- authentication, authorization, secret-management, sandbox, network policy, or tenancy configuration;
- frontend, Control Tower view, telemetry collector, dashboard, alert, runbook, or release pipeline.

## Requirement coverage summary

The canonical matrix is `docs/tech-specs/VAE_REQUIREMENT_COVERAGE_MATRIX.csv`.

| Verdict | Count | Meaning in this checkout |
|---|---:|---|
| `IMPLEMENTED_AND_KEEP` | 0 | No complete executable product behavior was verified. |
| `IMPLEMENTED_BUT_ALIGN` | 1 | The Delegation handoff exists but still describes the Delegation PRD as future work; the attached authority says that boundary now has an owner. |
| `PARTIALLY_IMPLEMENTED` | 105 | A concrete schema, registry, fixture, or governance object covers part of the requirement, without an enforcing product path. |
| `NEW_IMPLEMENTATION` | 66 | No executable implementation exists and no empirical uncertainty must be retired before design. |
| `REPLACE_LEGACY_BEHAVIOR` | 0 | No local legacy runtime behavior was found to replace. |
| `NEEDS_EMPIRICAL_PROTOTYPE` | 74 | Provider, GPU, VLM, geometry, retrieval, quality, repair, recovery, or performance claims require measured proof. |
| `DEFERRED` | 0 | The PRD does not defer any listed requirement itself. Broader asset-family production certification is out of Release 1, but honest structural representation remains a Release 1 requirement. |

## Missing technical specifications

No implementation-ready specification currently defines:

- the authority and adapter boundary for the published Delegation contract package;
- Visual Production Plan IR invariants, canonical state, schema evolution, and provider compilation;
- capability registries, compatibility resolution, ComfyUI compilation, node locking, model/VAE/LoRA pinning, and reproducibility;
- local and cloud GPU scheduling, container isolation, mounted model storage, object storage, queues, checkpoints, recovery, and cost accounting;
- deterministic validation versus independent VLM authority, evaluator calibration, hard gates, arbitration, and evaluator failure handling;
- typed causal repair, invalidation, bounded reruns, preservation tests, and amendment escalation;
- candidate portfolio selection, adaptive expansion, early stopping, and Budget Program enforcement;
- immutable lifecycle persistence, Visual Asset Memory, CMF-OKF projection, retrieval receipts, and Steering Recipe promotion;
- asynchronous API semantics, events, idempotency, cancellation, backpressure, security, Control Tower projections, migration, and rollback;
- the complete Format 02 local/cloud vertical-slice test architecture and downstream composition acceptance.

## Cross-repository blockers

1. The frozen Atomic Harness Builder implementation and V2.1 brownfield sources registered as SRC-001 and SRC-002 are not present. Their actual Harness IR, Workflow Runtime, JIT Skills, Control Tower, repair, and Development Capsule owners cannot be verified.
2. The authoritative Delegation Protocol draft repository is now available as a sibling workspace and validates 25 schemas/examples/messages. It is not yet a published pinned dependency, and its own Stage 1 ownership register blocks schema freeze on unresolved field ownership and open nested objects.
3. The downstream Format 02 Content Harness and Remotion consumer are not present, so geometry/result consumption and end-to-end ownership cannot be verified.
4. The ten registered local evidence sources are missing, causing current source-integrity validation to fail.
5. This directory is not a Git checkout, so history, branch state, release tags, and provenance of package changes cannot be established.

Cross-product conflicts and requested resolutions are tracked in `CROSS_REPO_ISSUES.md`.

## Proposed technical-specification plan

### Gate 0 - restore authoritative evidence

Pin and make available the Atomic Harness Builder release, publish/pin the currently available Delegation Protocol draft schema package, and supply the Format 02 downstream consumer contract. Reconcile the source register so the package validator is reproducible. Do not finalize canonical shared fields before this gate closes.

### Gate 1 - authority, contracts, and canonical state

Author `TS-VAE-01-DEMAND-INTAKE-AND-PRODUCTION-PLAN-IR.md`, including immutable demand intake, ownership checks, provisional-to-published Delegation adapters, Visual Production Plan IR, conflict/amendment handling, and canonical state boundaries. Resolve ADR seeds D003, D009, D012, D023, D024, and D027 first.

### Gate 2 - routing, compilation, and compute

Author TS-VAE-02, TS-VAE-03, TS-VAE-04, and the runtime portions of TS-VAE-09. Define capability compatibility, smallest-sufficient workcells, ComfyUI compilation as a provider artifact, immutable images and nodes, GPU scheduling, storage, queues, events, checkpoints, cancellation, and recovery.

### Gate 3 - budgets, evaluation, and repair

Author TS-VAE-05, TS-VAE-06, and TS-VAE-07. Run specification-supporting prototypes for candidate selection, evaluator calibration, deterministic/VLM authority separation, causal repair, invalidation precision, three-round stopping, and cost/latency behavior.

### Gate 4 - memory and capability learning

Author TS-VAE-08 and TS-VAE-11. Specify operational truth versus OKF projection, authority-aware multimodal retrieval, Steering Recipe evidence and promotion, isolated capability-development pipelines, contamination checks, and rollback.

### Gate 5 - service and Format 02 proof

Complete TS-VAE-09 and author TS-VAE-10. Bind every Release 1 FR/NFR/decision to APIs, events, fixtures, local/cloud execution, evaluator cases, one repair path, immutable result promotion, geometry receipt, downstream Remotion consumption, migration, rollback, and Given/When/Then tests.

Every Stage 2 specification must use `handoff/FEATURE_TECH_SPEC_TEMPLATE.md` and include the additional mandatory sections in the attached directive: owned requirements and decisions, state/data models, APIs/queues/events, adapters, graph compilation, locks and registries, GPU/storage, deterministic/VLM authority, budgets, selection, repair/invalidation, idempotency/checkpoints, observability/cost, security, migration/rollback, tests, acceptance criteria, tasks, and non-goals.

## Proceed-to-specification verdict

**CONCERNS**

The verdict taxonomy and Delegation draft authority are now available. Stage 2 specification authoring may proceed with explicit blocked interfaces, but implementation authorization remains failed while the frozen upstream implementation, published Delegation package/version, downstream Format 02 consumer boundary, and registered evidence sources are unavailable. Stage 2 artifacts must remain draft for architecture validation until those blockers are resolved or explicitly governed by a documented waiver.
