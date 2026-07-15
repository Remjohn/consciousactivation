# Delegation Adapter Test Plan

**Stage:** 3 - Contract integration  
**Status:** Delegation `1.1.0-rc.2` bounded boundary integration tested; runtime adapter not implemented  
**Dependency:** exact local unsigned pin in `contracts/integration/DELEGATION_CONTRACT_PIN.yaml`  
**Execution authorization:** not granted

## Batch B execution addendum — 2026-07-14

The current execution target is `delegation-contracts@1.1.0-rc.2`, not the historical `1.0.0-rc.2` registry described below and not rejected `1.1.0-rc.1`. The release validator passes in place and in a clean extracted layout; 61 validator tests, 33 protocol tests, and 12 VAE integration tests pass.

The executable VAE suite is `validation/tests/test_delegation_rc2_integration.py`, with boundary cases in `validation/fixtures/delegation-rc2/VAE_BOUNDARY_CASES.json`. It proves:

- all 24 Visual Asset Demand top-level fields and all protected semantic paths are preserved;
- `source_provenance.source_kind` is mandatory and typed;
- `interview_expression` requires non-empty Reaction Receipt and Expression Moment references;
- non-interview sources may omit those references and the adapter never synthesizes them;
- pre-discriminator migrations require an owner classification and never guess;
- parse-only claims and lossy semantic adapters are rejected;
- deterministic/non-semantic derivatives inherit all parent wrong-reading locks, may strengthen them, and require a new authorized upstream demand version to relax them;
- Content Harness Feature Contract references remain exact, typed, versioned and immutable while VAE emits separate feasibility, realization and receipt evidence;
- the asset result maps every canonical required field and cannot grant downstream consumption authority.

This is contract-boundary evidence, not a production runtime adapter or implementation authorization. The evaluation profile remains `specified_not_certified`.

## Objective

Prove that the VAE can consume and emit the published Delegation contract family without changing demand meaning, shared schema ownership, public lifecycle semantics, authority, integrity, or downstream approval. This plan is executable in design but no harness, production adapter, generated binding, CI workflow, or runtime code is created in Stage 3.

The current Delegation RC2 package contains 26 schemas, 26 examples, 26 messages, generated Python and TypeScript bindings, a passing package validator, and 42 passing validator tests. This does **not** prove VAE producer, consumer, adapter, recovery, or cross-product conformance. RC2 fixes the RC1 producer conflicts, but `amendment-response` still omits VAE from registered consumers.

## Test system architecture

| Test element | Responsibility |
|---|---|
| Pinned package loader | Resolve one immutable published coordinate, verify release/manifest/schema hashes, and refuse mutable local or draft dependencies in production mode |
| Schema validator | Validate envelope and payload using canonical Delegation schemas and format checks before mapping |
| Binding factory | Generate/import typed bindings from the published package and prove no VAE-owned shared schema is compiled |
| Adapter harness | Invoke one named mapping version with canonical input or internal fact and compare canonicalized output |
| Fake VAE application ports | Capture immutable commands/facts and prove raw payload maps do not cross the boundary |
| Authority oracle | Evaluate principal/action/field ownership from the Delegation authority registries |
| Lifecycle oracle | Evaluate legal transitions and public state vocabulary from the Delegation lifecycle machine |
| Integrity oracle | Canonicalize, hash, verify signature inputs, and distinguish duplicate retry from hostile replay |
| Fault scheduler | Inject ordering, restart, timeout, audit-store, event-bus, cancellation, and supersession races deterministically |
| Evidence reporter | Emit machine-readable fixture ID, package pin, adapter version, result, diff, authority/lifecycle decision, and receipt references |

No test double may make an authority decision on behalf of Content Harness or the Delegation boundary. Test doubles only present signed/validated decisions or assert rejection.

## Fixture policy

1. **Canonical producer/consumer fixtures:** the 26 Delegation RC examples are the minimum schema-valid fixtures.
2. **Delegation conformance fixtures:** all cases in `conformance/` and all `SCN-01` through `SCN-10` are mandatory after publication.
3. **VAE comparison fixtures:** `contracts/examples/format02_*` and `reference-slice/FORMAT02_MINIMAL_COACH_THEATRE/contracts/*` are provisional migration inputs only.
4. **Negative fixtures:** mutate one property at a time for missing required fields, unknown required features, bad identity/hash/signature, wrong principal, illegal state, replay, stale result, forbidden authorization, and private-state leakage.
5. **Golden adapter outputs:** canonicalized bytes are tied to the published package digest and adapter version. A package hash change invalidates the golden set.
6. **No invented defaults:** a fixture missing mandatory meaning must fail; the adapter may not make it pass using model inference or contextual guesswork.

## Planned test inventory

### Package and binding integrity

| ID | Test | Expected result |
|---|---|---|
| ADP-PKG-001 | Verify release coordinate, manifest, message registry, lifecycle, all schema hashes, and schema IDs | Exact published pin is accepted; draft/mutable/drifted content is rejected in production mode |
| ADP-PKG-002 | Enumerate registry, schemas, examples, generated bindings, and matrix entries | Exactly one entry per registered message; no missing/orphan binding and no local shared schema in build inputs |
| ADP-PKG-003 | Run canonical schema examples and all negative schema mutations | Canonical examples pass and each invalid mutation fails at the boundary |

### Inbound mapping

| ID | Test | Expected result |
|---|---|---|
| ADP-IN-001 | Canonical demand to immutable VAE demand fact | All mandatory semantic fields and exact owner evidence preserved; source object remains unchanged |
| ADP-IN-002 | Protocol-observed submission with demand hash and negotiated profile | Raw submission never crosses the VAE application port; its validated profile and exact demand context are carried by the split receipts |
| ADP-IN-003 | Delegation Set with independently versioned members | Set identity and each member lineage preserved; no merged demand is created |
| ADP-IN-004 | Budget authorization | Ceilings, policy, version, signature/owner evidence preserved; no widening/defaulting |
| ADP-IN-005 | Budget escalation response | Only validated approved/denied disposition applies to the waiting execution |
| ADP-IN-006 | Cancellation request | New work is blocked, safe stop is requested, and completed evidence remains immutable |
| ADP-IN-007 | Amendment response | Disposition is recorded; accepted demand is not changed in place |
| ADP-IN-008 | Demand supersession | Old/new exact identities link; old-only result promotion is blocked |
| ADP-IN-009 | Result acknowledgement | Exact current result receives downstream disposition; production evidence is unchanged |
| ADP-IN-010 | Delegation audit receipt | Receipt reconciles with VAE facts; projection cannot become authority |
| ADP-IN-011 | Contract migration | Only authorized, immutable, equivalence-evidenced migration is accepted; in-flight pin remains unchanged |
| ADP-IN-012 | Submission validation receipt | Only a protocol-authored accepted receipt can proceed to VAE admission; rejected or mismatched identity never reaches admission |

### Outbound mapping

| ID | Test | Expected result |
|---|---|---|
| ADP-OUT-001 | Stable VAE public event | Event metadata is placed in envelope/audit; no private candidate/evaluator/repair/workflow state leaks |
| ADP-OUT-002 | Budget escalation request | Evidence and bounded request map; active authorization remains unchanged |
| ADP-OUT-003 | Cancellation receipt | Safe-stop disposition, retained output, and compute evidence are complete and immutable |
| ADP-OUT-004 | Constraint conflict | Infeasibility/evidence map; local `proposed_amendments` is absent |
| ADP-OUT-005 | Amendment proposal | Typed non-binding options map separately with predicted effects and invalidation evidence |
| ADP-OUT-006 | Selective invalidation receipt | Reuse/invalidation/resume facts link exact old/new demand and plan identities |
| ADP-OUT-007 | Asset result | Canonical result fields and production receipts map; `authorized_for_composition` never appears |
| ADP-OUT-008 | Revocation notice | VAE-owned production/integrity scope maps; unrelated owner scope is rejected |
| ADP-OUT-009 | Compatibility manifest | Only versions, profiles, messages, adapters, and limitations backed by passing evidence are claimed |
| ADP-OUT-010 | VAE admission receipt | Admission is emitted only after accepted protocol validation and contains exact demand/execution identity; VAE cannot impersonate protocol validation |

### Bidirectional, identity, authority, and lifecycle

| ID | Test | Expected result |
|---|---|---|
| ADP-BI-001 | Invalidation notice in owner and non-owner roles | Owner scope maps; non-owner attempt is rejected with no state change |
| ADP-BI-002 | Replacement proposal and acknowledged replacement | Candidate is not promoted before governed acknowledgement |
| ADP-BI-003 | Delegation failure detection/decision split | Stable taxonomy maps; private diagnostics and unauthorized retry decisions remain internal |
| ADP-ID-001 | Exact demand identity across every related message | Request ID, version, hash, and canonical reference agree; missing/mismatch/invention fails |
| ADP-AUTH-001 | Submission receipt split | Protocol validation and VAE admission remain distinct through `submission-validation-receipt` and `admission-receipt`; neither principal can impersonate the other |
| ADP-AUTH-005 | RC authority and consumer reconciliation | Every producer and consumer matches the ownership specification; `amendment-response` remains fail-closed until VAE is a registered consumer |
| ADP-AUTH-002 | Budget field mutation attempt | VAE cannot raise ceilings, self-approve, or silently reduce owner policy |
| ADP-AUTH-003 | Conflict/amendment separation | Evidence cannot mutate demand; owner response still requires authoritative demand versioning |
| ADP-AUTH-004 | Production acceptance/downstream acknowledgement split | VAE can attest production acceptance only; Content Harness alone acknowledges downstream use |
| ADP-LIFE-001 | Full legal and illegal transition table | Every declared transition has exact trigger/authority; illegal transitions reject without state change |
| ADP-LIFE-002 | Public event vocabulary | Only governed stable states/events cross the boundary; arbitrary strings/private states reject |

### Compatibility, replay, resilience, and security

| ID | Test | Expected result |
|---|---|---|
| ADP-COMP-001 | Same, minor, adapter, declared degradation, migration, unsupported, and deprecated paths | Verdict exactly matches Delegation policy and is pinned for the delegation lifetime |
| ADP-COMP-002 | Adapter semantic loss mutations | Dropped continuity, wrong-reading lock, quality gate, identity, or mandatory receipt becomes INCOMPATIBLE |
| ADP-REP-001 | Duplicate retry versus replay | Same idempotency key returns existing receipt/no duplicate execution; hostile or invalid-state replay rejects |
| ADP-REP-002 | Out-of-order and duplicate event delivery | Ordering policy applies deterministically; projection and execution are not corrupted |
| ADP-RES-001 | Boundary/VAE restart with in-flight work | Projection and idempotency rebuild; same execution resumes without duplicate work |
| ADP-RES-002 | Event bus and audit store faults | Ordered delivery recovers; state-changing acceptance fails safe when durable audit is unavailable |
| ADP-RES-003 | Cancellation/result and supersession/GPU completion races | Precedence is deterministic; stale output is preserved as evidence but cannot be promoted |
| ADP-SEC-001 | Principal, signature, hash, reference, and audit-chain tampering | Boundary rejects before persistence/routing and records a non-authoritative failure receipt |
| ADP-SEC-002 | Parser limits, unknown extensions, and malicious nested input | Bounded validation rejects unsafe/ungoverned required content without best-effort parsing |

## Delegation conformance mapping

| Delegation suite | Existing cases | VAE harness mapping | Stage 3 state |
|---|---:|---|---|
| Authority | `AUTH-01` through `AUTH-10` (10) | ADP-AUTH plus boundary principal/action tests | declarative only |
| Lifecycle | `LIFE-V-01` through `LIFE-V-20`; `LIFE-I-01` through `LIFE-I-06` (26) | ADP-LIFE-001 plus per-message producer/consumer tests | declarative only |
| Compatibility | `COMP-01` through `COMP-10` (10) | ADP-COMP-001/002 and compatibility-manifest tests | declarative only |
| Resilience | `RES-01` through `RES-10` (10) | ADP-REP and ADP-RES fault-scheduler tests | declarative only |
| Format 02 | `SCN-01` through `SCN-10` (10) | End-to-end producer, protocol, VAE adapter, fake VAE ports, and downstream consumer | PRD fixtures only |

All 56 conformance cases must become executable assertions. Merely loading their YAML or checking that an `expected` property exists is not a pass.

## Format 02 end-to-end scenarios

| Scenario | Contract behavior to prove |
|---|---|
| SCN-01 | Successful single-character demand through acknowledged result |
| SCN-02 | Atomic multi-asset Delegation Set with independent member lineage |
| SCN-03 | In-flight supersession, selective invalidation, reuse, and stale-result block |
| SCN-04 | Budget escalation request, authoritative approval, and resumed same execution |
| SCN-05 | Constraint conflict, separate proposal, owner response, and immutable superseding demand |
| SCN-06 | Safe cancellation and complete cancellation receipt |
| SCN-07 | Result invalidation, governed replacement, and acknowledgement before promotion |
| SCN-08 | Authority violation rejection with no state change |
| SCN-09 | Migration-required compatibility path with immutable equivalence evidence |
| SCN-10 | Duplicate, replay, and out-of-order handling without duplicate execution |

Real Content Harness and composition-consumer fixtures are absent. Until supplied, these scenarios can validate adapter structure only and cannot certify interoperability or geometry effectiveness.

## Required evidence and CI gates

The future contract job shall produce:

- dependency coordinate and release/manifest/schema digests;
- generated-binding inventory and proof that no VAE snapshot entered build inputs;
- one result record for all 26 producer/consumer/observer message paths;
- all 56 conformance case results and all 10 Format 02 scenario results;
- golden canonical byte/hash comparisons for adapter paths;
- mutation results for authority, lifecycle, identity, required semantics, and authorization separation;
- restart/race/replay fault traces with execution and idempotency identities;
- compatibility manifest derived from, and linked to, passing evidence;
- explicit skipped/blocked cases. A skipped required case makes the gate fail.

Suggested Stage 4 gates are `delegation-package-integrity`, `delegation-schema-consumer`, `delegation-schema-producer`, `delegation-adapter`, `delegation-authority-lifecycle`, `delegation-resilience-security`, and `format02-cross-product`. Gate names are proposals until reconciled with the real Atomic Harness Builder CI owners.

## Acceptance criteria

1. **Given** the exact published dependency pin, **when** the package loader verifies it, **then** every registry/schema digest resolves and any drift fails closed.
2. **Given** all registered messages, **when** bindings and the compatibility matrix are enumerated, **then** all 26 appear exactly once with a tested VAE role and registered producer direction.
3. **Given** a canonical accepted demand, **when** it crosses the adapter, **then** its owner meaning and exact identity are immutable and lossless.
4. **Given** a VAE conflict with suggested changes, **when** outbound messages are built, **then** conflict evidence and non-binding amendment proposals are separate and no demand field changes.
5. **Given** a production-accepted asset, **when** VAE emits a result, **then** production evidence is complete and downstream composition authorization is absent.
6. **Given** a downstream result acknowledgement, **when** VAE consumes it, **then** the exact current result transitions according to owner disposition without rewriting production evidence.
7. **Given** arbitrary internal VAE state, **when** an event is requested, **then** only governed stable public facts can be emitted and metadata remains in envelope/audit.
8. **Given** an illegal principal/field action or lifecycle transition, **when** boundary validation runs, **then** it rejects before persistence/routing and state remains unchanged.
9. **Given** duplicate, replayed, out-of-order, restarted, or racing delivery, **when** the fault suite runs, **then** no duplicate execution or stale promotion occurs and audit evidence is retained.
10. **Given** an unsupported required semantic, **when** compatibility is negotiated, **then** the result is `INCOMPATIBLE` or `MIGRATION_REQUIRED`; best-effort adaptation is impossible.
11. **Given** a migration-required contract, **when** no authorized migration/equivalence evidence exists, **then** VAE rejects it and preserves the in-flight pin.
12. **Given** all mandatory suites, **when** readiness evidence is evaluated, **then** no conformance or production claim can pass with skipped tests, provisional fixtures, or a draft dependency.

## Entry and exit conditions

**Entry to implementation of this plan:** published Delegation package; resolved ADR-DLG-002 through ADR-DLG-009 as applicable; canonical IDs/versioning/serialization; authority split for receipt/result; exact demand identity; typed extension policy; Atomic Harness Builder port owners; implementation authorization.

**Exit for contract-integration PASS:** all message paths and mandatory conformance/Format 02 cases execute against pinned cross-product fixtures; no required skip; no unauthorized mutation; no private-state leakage; no self-approval; compatibility manifest matches evidence; rollback/deprecation behavior passes.

Current verdict: **CONCERNS**. The test architecture and cases are complete enough for readiness planning, but execution is blocked by unpublished contracts, unresolved authority/schema ADRs, absent upstream extension points, and absent real Format 02 producer/consumer fixtures.
