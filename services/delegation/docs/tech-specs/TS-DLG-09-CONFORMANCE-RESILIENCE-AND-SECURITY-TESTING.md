---
title: TS-DLG-09 Conformance Resilience and Security Testing
product: CMF Content Harness Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: stage2_draft_for_review
created: 2026-07-14
---

# TS-DLG-09 Conformance, Resilience and Security Testing

## 1. Identity and requirement coverage

- Primary features: F09, test/readiness portions of F14, F15 and F16
- Owned FRs: FR-065 through FR-072, FR-116 through FR-119, FR-121 through FR-125, FR-127, FR-128
- Owned NFRs: NFR-CONTRACT-003, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005, NFR-GOV-006
- Decisions: D009, D014, D015, D016
- Resolves: testing portions of ADR-DLG-008, ADR-DLG-017, ADR-DLG-018, ADR-DLG-019 and ADR-DLG-020
- Journeys: UJ-02, UJ-10, UJ-13, UJ-14
- Supporting spec: TS-DLG-10 owns FR-120 and FR-126 Format 02 proof

## 2. Sources read

Normative inputs are feature shards F09, F14, F15 and F16; failure taxonomy, hard gates, SLOs, success metrics and constitution; all declarative authority/lifecycle/compatibility/resilience cases; Development Capsule requirements; TS-DLG-01 through TS-DLG-08; and Stage 1 inventory/matrix/issues.

## 2A. Cross-cutting protocol obligations

| Concern | Normative obligation in this specification |
|---|---|
| Service and library boundaries | Only the modules and ports named here are owned; Content Harness meaning, VAE production and the existing Control Tower remain external owners. |
| Canonical schemas and field-level authority | Public payloads are closed, versioned and registry-owned; every value path has one owner and every state-changing principal/action is validated before effect. |
| Lifecycle, correlation and causation | TS-DLG-03 transition rules apply; every message keeps the exact correlation and names its direct accepted cause unless it is the initial command. |
| Idempotency versus replay | Legitimate identical command delivery returns the prior receipt; nonce/message/key reuse with different bytes, scope or invalid state is rejected as replay/conflict. |
| Compatibility, adapters and migrations | TS-DLG-04 negotiation is pinned before admission; adapters/migrations are deterministic, lossless for mandatory meaning and cannot transfer authority. |
| Event routing and audit chain | Accepted/rejected actions are receipted; accepted messages route only after atomic message/state/audit/outbox commit. |
| Cancellation and race precedence | TS-DLG-03/05 committed-sequence rules apply; accepted cancellation or supersession blocks later stale promotion for its scope. |
| Supersession and selective invalidation | Old facts remain immutable; owner-authored changed paths and VAE evidence determine conservative reuse and exact invalidation. |
| Result acknowledgement | VAE production acceptance remains separate from Content Harness/composition-runtime downstream acknowledgement under TS-DLG-06. |
| Invalidation, revocation and replacement | Post-completion authorization changes use new notices and impact analysis; no completed result or historical use is overwritten. |
| Failure, persistence and transactions | Failures use the canonical taxonomy; state-changing acceptance fails closed unless durable protocol records and audit commit atomically. |
| Observability and SLOs | TS-DLG-08 source-linked projections, bounded metrics, incident rules and SLO definitions apply to all behavior specified here. |
| Threat model and test architecture | The threat and test sections below include negative, adversarial, recovery and Given/When/Then evidence for this spec's owned behavior. |

## 3. Problem, solution and scope

Current cases are declarative YAML and the package validator does not execute a protocol, product adapter, fault or security control. This specification defines a transport-neutral conformance kit with a standard system-under-test adapter, deterministic fixtures, receipt assertions, fault controls and evidence bundles consumed by formal readiness gates.

Conformance proves public protocol behavior. It does not certify VAE visual quality, Content Harness creativity, non-Format 02 categories or production scale by document review alone.

## 4. Conformance architecture

The Stage 3/4 package shall provide:

- `conformance-runner`: loads a suite manifest and executes cases deterministically;
- `sut-adapter`: standard start/reset/submit/read-state/read-audit/inject-fault/advance-clock interface;
- `fixture-store`: immutable signed inputs/expected outputs by hash;
- `oracle`: schema, authority, lifecycle, compatibility, audit and projection assertions generated from canonical registries;
- `fault-controller`: process, bus, store, clock and delivery fault injection;
- `evidence-bundler`: signed machine-readable run result with versions/digests/log references;
- producer and consumer harness adapters for Content Harness, VAE, composition runtime, protocol and Control Tower.

The runner supports in-memory reference, local process and deployed endpoint profiles without changing expected semantics. A transport profile may supply delivery controls, never expected authority/lifecycle outcomes.

## 5. Canonical failure taxonomy

The protocol registry owns ten families: `contract_failure`, `authority_failure`, `compatibility_failure`, `dependency_staleness_failure`, `feasibility_failure`, `production_infrastructure_failure`, `quality_failure`, `budget_timing_exception`, `human_exception` and `security_integrity_failure`.

Every code record declares immutable meaning, allowed severity, terminality, responsible system, next-decision owner, enforcement owner, retry class, payload-change requirement, quality-round effect, invalidation/preservation rule, default next actions, deprecation replacement and diagnostic privacy class.

Retry classes are `none`, `transport_redelivery_same_message`, `operational_resume_same_execution`, `correct_and_new_message`, `owner_decision_required`, `amend_and_supersede`, `revalidate`, and `new_production_attempt`. Blind unchanged domain retries are prohibited.

The closed `DelegationFailure` carries exact demand/execution references, family/code/severity/terminal, detector/responsible/decision/enforcement owners, retry rule, remaining quality rounds, affected/preserved artifacts, downstream impact, next actions and restricted diagnostics reference. Products may attach details but cannot redefine protocol meaning.

Partial results identify accepted roles/results, unresolved roles with typed failures, original completion policy and whether acknowledgement is permitted. Partial output never bypasses set/result policy.

## 6. Required test suites

| Suite | Minimum proof |
|---|---|
| Schema | Positive/negative instance vectors, closed fields, canonical IDs/hashes, generated binding parity |
| Producer | Every emitted message version validates, signs and uses permitted fields |
| Consumer | Every claimed version is accepted/rejected correctly, including unknown mandatory features |
| Authority | Every principal/action/field allow and deny path, grants and conditional owners |
| Lifecycle | Every valid transition, every absent transition, terminal/post-completion paths and reconstruction |
| Idempotency/replay | Duplicate, key conflict, nonce reuse, expiry, delayed signed action and restart |
| Compatibility | Direct, minor, adapter, degradation, migration, deprecation, unsupported required behavior |
| Failure/recovery | Every family/code, owner/retry/quality-round/invalidation/partial-result semantics |
| Resilience | Duplicate/out-of-order/delay, process/bus/store outage, restart, timeout, race and recovery |
| Security | Spoofing, tampering, downgrade, cross-tenant, key rotation/revocation, reference abuse and audit attack |
| Control Tower | Projection source trace, gaps, reconciliation, freshness and incident routing |
| Format 02 | All TS-DLG-10 scenarios using pinned real product adapters |

Every case declares owned requirements/decisions, pre-state, principals, exact fixtures, action/fault, expected receipt/failure/state/outbox/projection, prohibited side effects and cleanup. Expected prose alone is insufficient.

## 7. Security and threat testing

The threat model covers STRIDE-style risks at envelope, resource resolver, policy, lifecycle, storage, adapter, transport and projection boundaries. Mandatory adversarial cases include:

- unsigned/forged/wrong-recipient/wrong-tenant messages;
- payload or schema hash substitution and duplicate JSON keys;
- expired/rotated/revoked keys and algorithm downgrade;
- valid-message nonce replay versus legitimate idempotent retry;
- unauthorized demand/result/acknowledgement/cancellation/budget/amendment actions;
- malicious extension fields and oversized/deep payloads;
- compatibility downgrade, adapter substitution and lossy migration;
- audit insertion/deletion/reorder and projection tampering;
- object-reference redirect, unavailable resource and credential leakage;
- race attempts to promote cancelled/superseded/revoked results.

Security/integrity violations block state, preserve bounded forensic metadata and emit incidents outside ordinary repair. No test may require production secrets or real customer media.

## 8. Resilience and deterministic fault model

Fault controls can pause/drop/duplicate/reorder transport deliveries; terminate/restart boundary/VAE adapters; fail audit, message, idempotency, replay, object and projection stores at named commit points; advance a virtual clock; and delay acknowledgements.

The reference suite includes existing RES-01 through RES-10 and expands each to assert message/audit/outbox counts, lifecycle state, duplicate VAE execution count, quality rounds and recovery receipts. Fault seeds and virtual times are recorded so failures reproduce.

No conformance test claims exactly-once network delivery. It proves exactly-once accepted protocol effect through idempotency, durable state and consumer dedupe.

## 9. Authority, lifecycle and cross-cutting cases

Authority tests are generated from closed schema owner metadata and principal policy, then supplemented with explicit prohibited cases. Lifecycle tests are generated from the transition table; every state/fact pair not registered is a negative case.

Cancellation/result, supersession/GPU completion, acknowledgement/revocation, escalation/cancellation and amendment/supersession races run under both delivery orders. Compatibility tests include all domain governance messages, not only demand/result.

Correlation/causation chains, idempotency result, replay decision, pinned profile, audit sequence/hash and current-use state are asserted for every state-changing case.

## 10. Persistence, isolation and test data

Each case receives an isolated tenant, namespace and deterministic IDs/clock. Reset must prove no state leaks across cases. The runner records storage adapter/version and verifies post-run invariants directly through read-only test ports.

Evidence bundles include suite/case versions, contract/registry/product/build digests, environment, seed, start/end, results, receipt hashes, sanitized logs/traces and failure references. Bundles are signed and immutable. Raw secrets/media/private reasoning are excluded.

## 11. Observability and performance evidence

The runner emits the SLIs in TS-DLG-08 and checks audit/projection completeness. Performance certification uses representative payload sizes, concurrency, duplicate ratio and reference latency; warm/cold paths are separate. Asset-generation duration is excluded from boundary-overhead calculations but VAE admission/acknowledgement end-to-end is reported.

SLO failures do not automatically imply semantic failure, but block production certification until dispositioned. Quality/authority gates cannot be disabled to make latency pass.

## 12. Compatibility, migration and rollback testing

Every supported release pair has a manifest test matrix. Adapter/migration fixtures assert all mandatory source fields and owner meanings at target. Repeated migrations must produce identical hashes. Rollback tests prove active profiles remain pinned and prior artifacts remain resolvable.

Breaking contract changes require old/new positive/negative fixtures, migration/adapter decision, deprecation timeline, rollback instructions and affected requirement/ADR references.

## 13. Readiness and certification state machine

The evidence evaluator permits only:

1. `PROTOCOL_PRD_DRAFT`
2. `PROTOCOL_PRD_APPROVED`
3. `ARCHITECTURE_IN_PROGRESS`
4. `CONTRACT_FAMILY_VALIDATED`
5. `CROSS_PRODUCT_FIXTURES_READY`
6. `CONFORMANCE_SUITE_PASSING`
7. `IMPLEMENTATION_AUTHORIZED`
8. `FORMAT02_INTEGRATION_CERTIFIED`
9. `PRODUCTION_PROTOCOL_CERTIFIED`

No state is skipped. Every transition emits an authorization/certification receipt naming exact scope, versions, evidence bundle hashes, limitations, approver and expiry/review date.

Implementation authorization requires all ten hard gates in `READINESS_HARD_GATES.yaml`, including closed ownership, executable lifecycle/illegal tests, adapter/migration/signature/replay proof, Format 02 portfolio, resilience, Control Tower integration, shared conformance and complete Development Capsule.

The Development Capsule includes approved PRD, architecture/ADRs, canonical packages, ownership/authority/lifecycle/failure/compatibility artifacts, fixtures/tests, deployment/observability, migration/rollback, epics/stories/specs and authorization receipt. A document placeholder is not gate evidence.

## 14. Failure, retry and incident behavior

Runner infrastructure failure is distinct from SUT conformance failure. A case may retry only if the SUT state is proven reset or the test explicitly verifies recovery. Flaky reruns never overwrite the original result; all attempts remain in the evidence bundle.

Any unauthorized accepted mutation, audit omission, duplicate production, lossy adapter or stale/revoked consumption is a release-blocking failure. Constitutional collision routes upstream and cannot be waived by ordinary test approval.

## 15. Given/When/Then acceptance criteria

1. Given any registered failure code, when its contract test runs, then family, owners, retry, quality-round and invalidation semantics match the canonical registry.
2. Given duplicate delivery after a timeout, when RES-01 runs, then one VAE execution and one accepted transition exist and both callers resolve the same receipt.
3. Given audit-store failure at commit, when RES-06 runs, then no state/outbox acceptance exists.
4. Given an adapter that drops continuity, when compatibility conformance runs, then release is blocked as incompatible.
5. Given a forged signed cancellation, when security tests run, then no lifecycle effect occurs and a security incident receipt exists.
6. Given all documents but no executable product adapters, when readiness is evaluated, then `IMPLEMENTATION_AUTHORIZED` is denied.
7. Given a passing suite, when evidence is bundled, then exact product/contract/environment digests and limitations are signed and reproducible.

## 16. Implementation tasks

1. Define versioned suite/case/evidence/SUT-adapter schemas.
2. Convert declarative cases into executable fixtures with full assertions.
3. Generate schema/authority/lifecycle negative matrices from canonical registries.
4. Implement deterministic fault-control and virtual-clock ports.
5. Build failure taxonomy registry/code generation and partial-result fixtures.
6. Define security test vectors, signing keys and sanitized forensic evidence.
7. Implement evidence evaluator and authorization/certification receipt schema.
8. Add deployment/rollback test profiles after platform topology is selected.

## 17. Explicit non-goals

- Visual-quality certification or VAE evaluator replacement
- Organization-wide penetration testing or IAM certification
- Waiving constitutional gates through test configuration
- Treating declarative YAML or document presence as executable proof
- Certifying categories beyond Format 02 in Release 1
- Production implementation during Stage 2

## 18. Readiness and blockers

Specification verdict: `CONCERNS`. The test/evidence architecture is complete, but no runner, SUT adapters, fault controls, deployment target or signed product releases exist. Current authorization remains below `CONTRACT_FAMILY_VALIDATED`; Stage 5 is not authorized.

## 19. V1.1 constitutional alignment amendment

The executable suite adds: Expression Moment drop rejection; wrong-reading
parse-only rejection; Activative Intelligence Pack version/hash preservation
through migration and replay; VAE protected-field authority rejection; and
evaluator-gap rejection before admission. Each case names input, expected
verdict/failure code, state effect, production effect, and audit evidence. All
existing lifecycle, cancellation, amendment, supersession, replacement,
Delegation Set, idempotency, and replay cases remain mandatory regressions.

## 20. RC2 consumer clean-room correction

Release conformance copies only the sealed candidate into a temporary
directory and runs shipped schema/example/generated-type, fixture, migration,
compatibility, validator, protocol, release-manifest, and receipt gates. The
source checkout, external `packages/...` tree, development working directory,
and absolute local paths are unavailable. Any cache, bytecode, temporary,
swap, or operating-system metadata path is a manifest failure.

## 21. RC4 derivative-lock conformance

The release-only suite executes exact inheritance, stricter addition, removal,
weakening, missing parent evidence, ambiguous classification, semantic shortcut
rejection, authorized successor-demand relaxation, generated binding
preservation, adapter preservation, no-guess migration, and parse-only
compatibility rejection. The same shipped validator runs from a clean extracted
candidate without source-repository or product-internal state. All RC3
lifecycle, authority, integrity, replay, idempotency, amendment, cancellation,
supersession, replacement, and Delegation Set cases remain mandatory.
