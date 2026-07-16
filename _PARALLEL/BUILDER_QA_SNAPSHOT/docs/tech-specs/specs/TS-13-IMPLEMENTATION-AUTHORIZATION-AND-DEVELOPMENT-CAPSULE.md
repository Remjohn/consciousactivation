# TS-13: Implementation Authorization And Development Capsule

Status: `IMPLEMENTATION_SPEC_COMPLETE_PENDING_BD-008`

## Traceability

- Owned: FR-127 through FR-136; FR-151 through FR-159.
- Decisions: D001, D002, D003, D010, D011, D014, D015, D021, D022, D023, D026, D027, D028, D029, D032, D033.
- Supporting NFRs: NFR-EVAL-003, NFR-OBS-002, NFR-REL-004, NFR-SEC-001, NFR-TRACE-001, NFR-TRACE-003, NFR-MAINT-001, NFR-PORT-001, NFR-TEST-001.

## Responsibility And Authority

Own failure taxonomy, root-cause investigation, Repair and Invalidation Graph application, targeted regression, escalation, readiness evaluation, prototype/implementation authorization, immutable receipts, requirement traceability, Development Capsule generation, justified scaffolding, contracts/examples, fixtures, dependency-ordered vertical stories, implementation delta intake, and downstream feedback.

Deterministic code evaluates gates and compiles capsules. Agents investigate root cause and propose repair. Independent evaluators provide receipts. Humans approve risk, prototype scope, implementation authorization, waivers, and implementation-discovered product deltas.

## Modules And Components

`domain/repair.py`, `domain/authorization.py`, `application/repair_commands.py`, `application/authorization.py`, `compilers/development_capsule.py`, `compilers/stories.py`, and `evaluation/readiness.py`.

## Canonical Data Structures

- `Failure { failure_id, class, severity, subject_ref, evidence, responsible_layer, affected_dependencies, repeat_count }`
- `RootCauseReport { failure_ref, hypotheses, tests, confirmed_cause, owner, repair_scope, evidence_refs }`
- `RepairPlan { root_cause_ref, changes, invalidations, targeted_suites, rollback, escalation }`
- `ReadinessReport { subject_hashes, structural_receipts, benchmark_receipts, hard_gates, unresolved_risks, outcome }`
- Outcomes: `FAIL`, `CONCERNS`, `PROTOTYPE_ONLY`, `IMPLEMENTATION_AUTHORIZED`.
- `AuthorizationReceipt { outcome, exact_ir/artifact/workflow/evaluator_hashes, allowed_scope, restrictions, human_signer, expiry, revocation_conditions }`
- `DevelopmentCapsuleManifest { capsule_id, authority_hashes, specifications, schemas, contracts, fixtures, stories, dependency_order, scaffolding, non_goals, receipt_ref }`

## APIs, Commands, Events, Persistence

- Commands: `InvestigateFailure`, `ApproveRepairPlan`, `ApplyRepair`, `RunTargetedRegression`, `EvaluateReadiness`, `AuthorizePrototype`, `AuthorizeImplementation`, `RevokeAuthorization`, `CompileDevelopmentCapsule`, `RecordImplementationDelta`, `IngestCertificationFeedback`.
- Events: `FailureClassified`, `RootCauseConfirmed`, `RepairApproved`, `DependenciesInvalidated`, `RegressionCompleted`, `ReadinessEvaluated`, `AuthorizationIssued`, `AuthorizationRevoked`, `DevelopmentCapsuleCompiled`, `ImplementationDeltaRaised`.
- Persistence: failures/repairs/authorization in IR plus ledger; reports/capsules in CAS; trace projection maps requirement to artifact/test/receipt.

## Dependency, Invalidation, Idempotency, Resume

Repair starts only after root cause is confirmed or a human grants a time-bounded incident waiver. Invalidations are computed from TS-07 graphs. Readiness identity includes all required receipts and exact hashes. Re-evaluation with identical inputs returns the prior report. Any relevant source, IR, workflow, skill, evaluator, threshold, or artifact change revokes/stales authorization. Capsule compilation is atomic and resumable per artifact before manifest commit.

## Security And Isolation

Authorization requires human identity and separation from generator/evaluator roles. Capsules contain no secrets, protected labels, production credentials, or unrelated source material. Scaffolding is allowlisted by IR responsibility and cannot include external product runtime implementations.

## Observability, Cost, And Performance

Report failures by layer, time to root cause, invalidation size, regression duration, repeated failure, gate outcomes, waiver use, capsule size, trace coverage, and cost per authorized capsule. Readiness query target is under 10 seconds excluding evaluation runs.

## Failures And Recovery

Unknown root cause blocks broad repair. Repeated failure escalates to human/architecture. A hard-gate failure forces `FAIL`; missing empirical thresholds may permit only restricted `PROTOTYPE_ONLY`. Capsule hash mismatch or incomplete trace closes the implementation gate. Revocation emits exact affected work and rollback guidance.

## Acceptance Tests

1. Readiness cannot pass from document/file presence alone.
2. Every failure maps to one smallest responsible layer or escalates explicitly.
3. Repair preserves unaffected upstream state and reruns targeted suites.
4. Hard-gate failure cannot be waived by an agent or averaged away.
5. Prototype authorization has scope, expiry, disposal, and prohibited claims.
6. Implementation authorization binds exact IR/artifact/workflow/evaluator identities.
7. Development Capsule covers every owned requirement with artifact and test links.
8. Capsule scaffolding contains no Visual Asset Editor, Delegation, or final harness production implementation.

## Implementation Tasks

1. Define failure, root cause, repair, readiness, authorization, trace, and capsule schemas.
2. Implement graph-driven invalidation and targeted-suite selector.
3. Implement hard-gate/readiness evaluator and human authorization commands.
4. Implement deterministic Development Capsule/story/fixture compiler.
5. Implement implementation-delta and downstream feedback workflows.
6. Add false-readiness, repeated-failure, revocation, trace, and boundary tests.

## V1.2 Constitutional Alignment Patch

| Requirement | Implementation owner | Component boundary | Data or contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Require constitutional readiness evidence and HG-015 | readiness_and_authorization_owner | Readiness aggregates exact receipts; it does not waive source, privacy, benchmark, or external-interface owners | `ConstitutionalReadinessReceipt`, contract registry hash, evaluation refs, HG-001-HG-015 results | Emit FAIL on missing semantic stack, category profile, rich lineage, policy, or non-compensable evidence | false-PASS and stale-receipt fixtures | Authorization pins all schema/evaluator/corpus/gate versions and remains FAIL while blockers persist | Additive readiness receipt version; prior authorization cannot inherit V1.2 scope automatically |

## Non-Goals And Migration

No implementation work is performed by the capsule compiler, and no V2.1 migration capsule is generated while the baseline is absent.
