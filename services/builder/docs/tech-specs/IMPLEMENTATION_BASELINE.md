# Implementation Baseline

## Baseline Verdict

`IMPLEMENTATION_READINESS: FAIL`

Technical specification authoring and the approved V1.2 alignment patches are complete. Production implementation is not authorized. Missing evidence/consent inputs, empirical provider and benchmark decisions, seed capability inputs, and authoritative external interface snapshots prevent a truthful `PASS`.

## Authority Precedence

1. Current explicit human direction.
2. Activative Intelligence Constitution V1.1 and its pinned hash.
3. Builder PRD V1.2 and binding constitutional amendment.
4. `governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`, current-effect governance registries, hard gates, and anti-goals.
5. Functional and non-functional requirements.
6. Accepted ADRs and these technical specifications.
7. Planning artifacts and historical V2.1 descriptions, which cannot override higher authority.

When a lower layer conflicts with a higher layer, implementation must stop and emit a decision request. It must not silently preserve historical behavior.

## Coverage Baseline

The authoritative registries contain 210 FRs and 53 NFRs. Current implementation coverage is:

- `NEW_IMPLEMENTATION`: requirements with deterministic, structural, security, governance, or interface behavior that can be specified now.
- `NEEDS_EMPIRICAL_PROTOTYPE`: visual inference, category grammar, evaluation, thresholds, scale, and reference-slice behavior that requires corpus-backed experiments before production authorization.
- `NOT_APPLICABLE`: FR-160 through FR-166 and NFR-COMPAT-001 because no V2.1 implementation artifact exists in this repository.
- `DEFERRED`: FR-169 general Builder certification, scheduled after the Release 1 reference and transfer portfolio.

The exact per-requirement classification and evidence is in `REQUIREMENT_COVERAGE_MATRIX.csv`.

## Proposed System Boundary

Builder Next is a governed compiler and control plane. It owns evidence registration, product/workflow state, typed IR, decisions, compilers, evaluation orchestration, repair/invalidation, authorization, and Development Capsule generation. It does not own generated harness production behavior or external target runtimes.

The proposed implementation is a modular monolith with explicit ports. This keeps Release 1 transaction and traceability boundaries coherent while allowing workflow workers, model providers, storage, and target compilers to be isolated behind contracts.

```text
src/cmf_builder/
  domain/          # immutable IDs, IR, graphs, events, policies, receipts
  application/     # commands, queries, transactions, lifecycle services
  evidence/        # source profiles, adapters, normalization, indexes
  visual/          # parser ports, ontology, induction, confidence
  genesis/         # decisions, recommendations, ratification
  skills/          # registry, recipes, capsule compiler, maturity
  evaluation/      # corpora, runs, evaluators, scorecards, gates
  workflow/        # Workflow IR, router, executors, checkpoints, incidents
  compilers/       # specification, OpenSpec, target, and capsule compilers
  control_tower/   # API, projections, governed commands
  adapters/        # persistence, CAS, Temporal/model/sandbox integrations
  cli/             # operator commands over application services
schemas/           # generated JSON Schemas; never independently authored truth
tests/             # unit, contract, integration, e2e, fault, benchmark
```

## Common Architecture Contracts

- IDs are opaque UUIDv7 values plus a human-readable kind prefix.
- Authoritative writes are commands producing immutable domain events.
- Events append to a Run Ledger with optimistic stream versions and idempotency keys.
- Harness IR and Workflow IR are separate versioned aggregates.
- Material values carry knowledge status, evidence references, authority, confidence, and provenance.
- Human ratification and authorization are signed receipts, never mutable booleans.
- Artifacts are content-addressed and bound to source, IR, compiler, workflow, and evaluator identities.
- Read models and the Control Tower are projections, never a second source of truth.
- All external providers are ports with deterministic fixtures and failure contracts.
- Generated JSON Schema, Markdown, OpenSpec, and target packages compile from canonical IR.

## Ratified Technology Profile

The architecture ratification approved these Release 1 choices. Production dependency installation remains prohibited until the implementation-readiness gate is `PASS`; explicitly authorized empirical prototypes remain `PROTOTYPE_ONLY`.

| Concern | Recommended Release 1 choice | Ratification state |
|---|---|---|
| Language and contracts | Python 3.12, Pydantic v2, generated JSON Schema | Accepted architecture baseline; exact dependency versions remain implementation inputs |
| Authoritative state | PostgreSQL event ledger and JSONB snapshots | Accepted by ADR-003 |
| Artifact storage | SHA-256 content-addressed store; filesystem dev adapter and S3-compatible production adapter | Accepted by ADR-003 |
| Workflow execution | Temporal adapter compiling governed Workflow IR, with deterministic in-memory test adapter | Accepted by ADR-006 |
| API and CLI | FastAPI command/query API and Typer CLI | FastAPI accepted by ADR-011; CLI remains a replaceable adapter |
| Control Tower | React/TypeScript web UI embedded or linked from Pi | Accepted by ADR-011 |
| Telemetry | OpenTelemetry traces, metrics, structured events | Accepted by ADR-016 |
| Isolation | container/worktree sandbox profiles with deny-by-default network, source, secret, and tool grants | Accepted by ADR-012 |

No production dependency may be added until the implementation-readiness gate is `PASS`. Prototype dependencies require explicit `PROTOTYPE_ONLY` authorization and may not create production authority.

## Release 1 Baseline

Format 02 Minimal Coach Theatre is the reference Atomic Content Harness and belongs to the 2D Character Animation category. Release 1 must prove the complete Builder spine from configured evidence through an authorized Development Capsule and downstream certification evidence.

The remaining four categories—including all four Conversational Activation / Human Expression profiles—plus the Visual Asset Editor and Delegation Contract targets receive schema-valid structural support labeled `UNCERTIFIED`. Their production behavior remains outside this repository.

Runtime semantics are **Activation First**. **Visual Syntax First** is the harness-development evidence order. Rich Shared Activative Core references, Activative Calls, Reaction Receipts, Expression Moments, and the complete visual-semantic/narrative/composition/T/V handoff chain are mandatory where applicable.

## Implementation Gate

The verdict may become `PASS` only when:

1. All blocking decisions in `BLOCKING_DECISIONS.yaml` are resolved or explicitly waived by the correct human authority.
2. Every Release 1 FR/NFR has an accepted technical owner, schema/API contract, and acceptance test.
3. The Format 02 evidence corpus and protected benchmark governance are available.
4. Architecture-preservation constraints are ratified.
5. Cross-product interface snapshots are supplied and contract-tested without importing external production behavior.
6. The specification linter reports complete FR/NFR/decision ownership and no hard-gate contradiction.
