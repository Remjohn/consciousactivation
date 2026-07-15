# Proposed Technical-Specification Plan

## Entry Conditions

Specification authoring should begin only after:

1. The governing `AGENTS.md` is supplied in the PRD workspace or amended to define the exact Stage 1 requirement-coverage verdict vocabulary.
2. SRC-002 through SRC-010 and SRC-011 at the registered commit are made available and hash-verified, or an authorized waiver records why each is non-authoritative.
3. The reference harness, first release category, and three target repositories/owners are identified.
4. Owners decide the unresolved storage, UI/deployment, multimodal provider, benchmark governance, workflow engine, isolation, and Release 1 profile questions OQ-001 through OQ-013.

## Authoring Waves

| Wave | Specifications | Required outputs | Principal dependencies |
|---|---|---|---|
| 0. Governance closure | Taxonomy, source authority, open-question decision packets | Updated AGENTS, source availability manifest, decision/waiver records | Product and architecture owners |
| 1. Foundation | Lifecycle/authority, ID and artifact identity, event ledger, canonical Harness IR | State diagrams, schemas, transactions, migration/version rules, public APIs, conformance fixtures | ADR-001, ADR-006, ADR-011 |
| 2. Evidence and Genesis | Source profiles, evidence ingestion, Visual Syntax First, saturation, atomicity, Genesis | Media and archive threat model, parser contracts, confidence model, atomicity packet, Genesis transaction tests | SRC-004, reference harness, provider choice |
| 3. Harness architecture | Capability ownership, module/phase DAGs, handoffs, references/SPR/context, skill ecology, JIT capsules | Typed registries, graph constraints, loading/precedence algorithms, maturity and capsule contracts | Target seams, skill seeds, runtime adapters |
| 4. Evaluation and readiness | Corpus governance, benchmark runner, scorecard, repair, readiness and authorization | Protected split, evaluator boundaries, repeated-run protocol, failure taxonomy, hard-gate engine, receipts | Benchmark owner and thresholds |
| 5. Categories and targets | Four constitutions, sequencing, three target compilers, Development Capsule | Category-local IRs, target compatibility matrix, compiler contracts, capsule manifest and acceptance suite | Category source artifacts and target repos |
| 6. Workflow Runtime | Workflow IR, router, scheduler, retries, sandbox, telemetry, promotion/rollback | Node schemas, actor matrix, bounded-control algorithms, fault tests, CI gates | Workflow engine and isolation decision |
| 7. Migration and release | V2.1 migration, dual-run comparison, deprecation, rollback | Source-to-IR mappings, equivalence thresholds, release checklist, rollback evidence | Original bundles and target baselines |
| 8. Product surface and operations | Control Tower API/UI, security, deployment, SLOs, backup/restore | API contract, accessible interaction spec, topology, IaC/CI plan, threat model, runbooks | UI/backend/hosting/auth choices |

## Required Shape Of Every Feature Specification

Each specification should include: scope and anti-goals; requirement and locked-decision trace; observed brownfield behavior with code/test anchors; canonical types and invariants; API/events/storage; state and failure transitions; authority boundaries; security and privacy; performance budgets; migration and compatibility; observability; deterministic and behavioral tests; deployment impact; acceptance gates; unresolved decisions; and explicit target-repository ownership.

The specification set should be generated against one machine-readable trace graph so FRs, NFRs, decisions, anti-goals, hard gates, ADRs, schemas, tests, and release receipts cannot drift into separate authorities.

## Cross-Repository Blockers

| Blocker | Impact |
|---|---|
| Missing SRC-002-SRC-010 files | Doctrine, visual corpus, skill history, legacy examples, architecture protocols, and workflow evidence cannot be revalidated |
| Missing SRC-011 BMAD commit | Planning and handoff method cannot be checked against the registered source |
| Missing reference harness | Atomicity, parser quality, benchmark design, readiness, and migration cannot be grounded in a real target |
| Missing target repositories | Integration seams, package/deployment constraints, target-local IR, and Development Capsule acceptance cannot be specified concretely |
| No storage/event backend decision | Lifecycle, Genesis transactions, replay, Control Tower, and audit history remain underdetermined |
| No multimodal provider/model decision | Visual parser inputs, confidence, cost, privacy, and deterministic fallback cannot be bounded |
| No benchmark corpus/governance | Evaluation, repair, readiness, and release thresholds cannot be made testable |
| No workflow engine/isolation policy | F18 routing, retries, sandboxing, parallelism, and promotion cannot be specified at implementation depth |
| No UI/deployment/auth choices | Control Tower accessibility, security boundaries, SLOs, and operational topology remain unspecified |

