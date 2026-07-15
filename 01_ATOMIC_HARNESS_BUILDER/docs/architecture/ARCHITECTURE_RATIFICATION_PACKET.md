# Architecture Ratification Packet

Status: `RATIFIED_WITH_OPEN_EXTERNAL_AND_EMPIRICAL_BLOCKERS`

Architecture completion gate: `FAIL`

## Purpose

This packet turns the proposed architecture choices into explicit human decisions. It does not approve its own recommendations. Selections are recorded in `ARCHITECTURE_RATIFICATION_BALLOT.yaml`; accepted selections then require a governed update to the ADR Register and affected specifications.

## Ratification Outcome

On 2026-07-14, the human product authority approved RC-000 and all nine ADR recommendations. All 18 ADRs are now accepted. BD-001, BD-005, BD-006, BD-009, BD-011, BD-012, and BD-013 are resolved by that approval. BD-004, BD-007, BD-008, BD-010, and BD-014 remain open because they require external or empirical evidence.

Nine ADRs were proposed and approved on 2026-07-14. The other nine were already accepted because they directly encode locked product authority or verified repository evidence.

## Already Accepted Decisions

| ADR | Accepted boundary |
|---|---|
| ADR-001 | Builder boundary and modular-monolith architecture |
| ADR-002 | Separate Harness IR and Workflow IR |
| ADR-004 | Deterministic compilation and schema evolution |
| ADR-005 | Explicit human-agent-code authority |
| ADR-007 | Immutable evidence identity and source profiles |
| ADR-009 | Four-layer Skill Ecology and deterministic JIT compilation |
| ADR-013 | Three target compilers with frozen external-product boundaries |
| ADR-014 | Format 02 under 2D Character Animation as Release 1 reference |
| ADR-015 | No V2.1 migration without repository-local artifacts |

Accepted architecture patterns can still have external implementation prerequisites. Acceptance does not manufacture a corpus, seed skill, benchmark, or external contract snapshot.

## Decision Options

Every ratification item permits exactly one selection:

- `APPROVE_RECOMMENDATION`
- `APPROVE_WITH_AMENDMENTS`
- `REJECT_AND_REPLACE`
- `DEFER`

An amendment or replacement must state its mechanism, owner, consequences, affected FR/NFR/ADR IDs, required tests, and migration implications. `DEFER` keeps the architecture completion gate at `FAIL`.

## RC-000: Architecture Preservation Contract

Authority: Product lead. Blocker: BD-001.

**Recommendation:** Ratify `docs/tech-specs/ARCHITECTURE_PRESERVATION_CONTRACT.md` as the implementation-level preservation contract derived from the Product Constitution, D001-D033, AG-001-AG-022, and HG-001-HG-014.

**Alternatives:** Supply a separate authoritative contract and reconcile differences; approve with named amendments; defer architecture completion.

**Consequences:** Approval makes architecture boundaries executable without promoting this document above the PRD. Replacement requires rerunning all architecture, ADR, and tech-spec validators.

## RC-003: Authoritative State And Artifact Storage

ADR: ADR-003. Authority: Architecture and operations. Blocker: BD-005.

**Recommendation:** PostgreSQL owns event streams, snapshots, command receipts, registries, and projections. A SHA-256 content-addressed store owns immutable evidence derivatives and generated artifacts. Development uses a filesystem CAS adapter; production uses an S3-compatible adapter.

**Alternatives:** SQLite for production; document database; filesystem-only state; broker-owned events; another relational/object-store combination with equivalent contracts.

**Why recommended:** It provides shared-worker concurrency, optimistic stream versions, transactions, relational traceability, replay, and scalable media/artifact storage without making an event broker authoritative.

**Consequences:** Adds PostgreSQL/object-store operations, migrations, backup/restore, and referential-integrity tests. Approval authorizes dependencies only after exact versions and deployment policy are recorded.

## RC-006: Workflow Engine Adapter

ADR: ADR-006. Authority: Architecture and operations. Blocker: BD-006.

**Recommendation:** Use Temporal as the production scheduling adapter and a deterministic in-memory adapter for tests. Temporal coordinates; Builder commands/events remain product authority.

**Alternatives:** Custom PostgreSQL scheduler; another durable engine; Celery/RQ-style queues; defer engine selection while implementing only Workflow IR and in-memory conformance.

**Why recommended:** Human waits, durable timers, retries, signals, versioning, worker loss, incidents, and replay are core requirements rather than incidental queue work.

**Consequences:** Adds Temporal deployment and deterministic-workflow constraints. Rejection requires another engine to pass the same public-seam, replay, resume, migration, signal, and fault suite.

## RC-008: Visual Inference Architecture

ADR: ADR-008. Authority: Architecture, category steward, and benchmark team. Blockers: BD-004, BD-007.

**Recommendation:** Approve the provider-neutral VisualInferencePort, deterministic normalization/geometry baseline, typed provider output, knowledge-status separation, and independent evaluation. Do not select a production provider until the protected Format 02 comparison completes.

**Alternatives:** Fixed provider; human-only annotation; deterministic geometry only; another adapter/ensemble architecture preserving the same authority and schema boundaries.

**Why recommended:** Provider quality, privacy, cost, and category performance are empirical, while the boundary separating observation, hypothesis, and authority can be fixed now.

**Consequences:** Approval authorizes prototype adapters and benchmark fixtures only. Production visual parsing remains blocked until BD-004, BD-007, and BD-008 close.

## RC-010: Benchmark Governance And Maturity

ADR: ADR-010. Authority: Evaluation governance. Blockers: BD-004, BD-008.

**Recommendation:** Separate public/development/protected cases; isolate generators from label custody; require no-guidance controls, repeated fresh contexts, independent evaluators, multidimensional scorecards, hard gates, and exact-identity maturity receipts. Calibrate thresholds after Format 02 runs.

**Alternatives:** External benchmark service with equivalent controls; human-only protected evaluation; a different split/role model that prevents leakage and self-evaluation.

**Why recommended:** Readiness and skill maturity cannot rely on document completeness or one self-evaluated run.

**Consequences:** Increases evaluation cost and governance work. Approval fixes the control model but does not approve numerical thresholds or label contents.

## RC-011: Control Tower Surface

ADR: ADR-011. Authority: UX and architecture. Blocker: BD-009.

**Recommendation:** FastAPI command/query API plus React/TypeScript Control Tower, launched or linked from Pi. All visible status is event-derived; UI actions submit typed commands.

**Alternatives:** Pi-native custom surface; another web stack; desktop-native application; API-first with UI deferred. CLI-only is not recommended for Release 1 graph/evidence operations.

**Why recommended:** It keeps core contracts portable and testable while supporting accessible graph, evidence, workflow, and incident inspection.

**Consequences:** Creates separate backend/frontend deliverables and accessibility/performance obligations. Approval must name Pi integration and deployment mode before implementation.

## RC-012: Sandbox And Least Privilege

ADR: ADR-012. Authority: Security and architecture. Blocker: BD-012.

**Recommendation:** Ratify deny-by-default capability grants and three isolation profiles: deterministic process, provider-call, and implementation-task. Use read-only evidence, writable staging, ephemeral credentials, explicit tools/network, resource limits, and disposal receipts. Select container/worktree mechanisms per profile after host/security validation.

**Alternatives:** Containers for every node; OS process isolation; remote sandbox service; another mechanism meeting the same policy conformance tests.

**Why recommended:** Policy semantics should remain stable even when the platform mechanism differs by risk and workload.

**Consequences:** Adds startup overhead and platform-specific adapters. Approval fixes security behavior; implementation mechanism still requires conformance evidence.

## RC-016: Deployment And Observability

ADR: ADR-016. Authority: Operations, security, and architecture. Blockers: BD-005, BD-006, BD-009, BD-012.

**Recommendation:** Deploy API, workflow, deterministic, agent/evaluator, projection, and UI processes as independently scalable containers around PostgreSQL, CAS, the workflow engine, and OpenTelemetry. Use development, CI, shadow, and production environments.

**Alternatives:** Single desktop process; managed container platform; Kubernetes; another topology preserving process isolation, immutable identities, promotion, rollback, and backup/restore.

**Why recommended:** The split follows authority and failure boundaries without forcing microservices or a specific orchestrator.

**Consequences:** Adds container, telemetry, migration, backup, and environment operations. Exact hosting, SLOs, RPO/RTO, and orchestrator remain amendments required before production.

## RC-017: Mandatory Release 1 Workflow Profiles

ADR: ADR-017. Authority: Product lead and Builder maintainer. Blocker: BD-013.

**Recommendation:** Require new harness compilation, evidence refresh, benchmark regression, repair/re-certification, and constrained incident hotfix profiles.

**Alternatives:** New-harness only; add/remove named profiles; one profile with modes; broader profile registry.

**Why recommended:** Release 1 must prove operational changes, regressions, repair, and incidents, while a universal profile would hide materially different gates and permissions.

**Consequences:** Requires five workflow definitions and public-seam/fault/promotion suites. Format 02 new-harness compilation remains the primary shadow path.

## RC-018: Format 02 Asset Demand Boundary

ADR: ADR-018. Authority: Product lead and cross-product architecture. Blockers: BD-011, BD-014.

**Recommendation:** Use a contract-tested stub AssetDemandPort backed by hash-locked fixtures. Builder compiles demand contracts and validates provenance/semantic non-mutation; it never implements or invokes Visual Asset Editor production behavior.

**Alternatives:** No asset-delegation boundary if Format 02 can be proven independent; external editor sandbox after its repository supplies accepted contracts; another fixture-based adapter.

**Why recommended:** It exercises the cross-product contract without making Release 1 depend on an unbuilt external runtime.

**Consequences:** Requires interface snapshots and fixtures. Approval does not authorize editor runtime code, credentials, or networking inside Builder.

## External And Empirical Evidence Dispositions

| Blocker | Required disposition before production implementation |
|---|---|
| BD-004 | Supply a hash-locked Format 02 corpus manifest with authority, consent, license, privacy, and benchmark eligibility |
| BD-007 | Approve a prototype plan comparing two provider adapters and deterministic baseline on protected cases |
| BD-008 | Name label custodian/evaluation approver and ratify the threshold-calibration process |
| BD-010 | Supply evaluated seed skills or ratify an empty registry with Format 02 capability-gap-only creation |
| BD-014 | Supply read-only versioned interface snapshots from Visual Asset Editor and Delegation owners |

These inputs may remain open while architecture patterns are approved, but implementation readiness cannot become `PASS`. A narrowly scoped `PROTOTYPE_ONLY` authorization may cover provider and threshold experiments after evidence, isolation, and governance prerequisites are approved.

## Ratification Order

1. RC-000 preservation contract.
2. RC-003, RC-006, RC-012, RC-016 foundation and operations.
3. RC-011 and RC-017 operator surface and workflows.
4. RC-008 and RC-010 empirical architecture.
5. RC-018 external asset boundary.
6. External evidence dispositions BD-004, BD-007, BD-008, BD-010, BD-014.

## Exit Criteria

- Every ratification item has a selection, authority identity, date, and amendment/replacement where required.
- Every active blocker has a satisfied evidence reference or approved superseding decision.
- Proposed ADR statuses are updated through a separate governed change and validators pass.
- Architecture completion gate changes only when no required proposal or architecture blocker remains.
