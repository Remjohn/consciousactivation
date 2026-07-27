---
title: TS-DLG-03 Lifecycle Idempotency and Replay
product: CMF Content Harness Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: stage2_draft_for_review
created: 2026-07-14
---

# TS-DLG-03 Lifecycle, Idempotency and Replay

## 1. Identity and requirement coverage

- Primary features: F04 and lifecycle/integrity portions of F14
- Owned FRs: FR-025 through FR-032, FR-107 through FR-109, FR-112
- Owned NFRs: NFR-LIFE-001, NFR-REL-001, NFR-REL-002, NFR-REL-005, NFR-SEC-002, NFR-SEC-003, NFR-SEC-005, NFR-TRACE-003, NFR-TRACE-004, NFR-RES-003, NFR-RES-004, NFR-RES-005
- Decisions: D004, D014
- Resolves: ADR-DLG-008, ADR-DLG-009 and lifecycle portion of ADR-DLG-004
- Journeys: UJ-01, UJ-03, UJ-04, UJ-05, UJ-08, UJ-12, UJ-13

## 2. Sources read

Normative inputs are `prd/05-features/F04-external-lifecycle.md`, `prd/05-features/F14-trust-integrity.md`, `governance/LIFECYCLE_MACHINE.yaml`, `governance/FAILURE_TAXONOMY.yaml`, the envelope and audit schemas, lifecycle/resilience cases, TS-DLG-01, TS-DLG-02 and Stage 1 ADRs/issues.

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

The current lifecycle is declarative and cannot prove transition enforcement, ordering, reconstruction, duplicate handling or fail-closed audit behavior. This specification defines a deterministic event-sourced lifecycle kernel with per-correlation serialization, separate idempotency and replay controls, and an atomic message/state/audit/outbox transaction.

The kernel projects shared commitment only. It never exposes Content Harness sequencing internals or VAE production nodes.

## 4. Service and library boundaries

Required ports and modules are:

- `LifecycleMachine`: pure `decide(current_state, accepted_fact) -> transition|rejection`;
- `CorrelationRepository`: optimistic append by `(correlation_id, expected_sequence)`;
- `IdempotencyRepository`: command-key reservation and completed response lookup;
- `ReplayRepository`: message ID and signer nonce uniqueness checks;
- `AuditLedger`: append-only chained receipts in the same acceptance transaction;
- `TransactionalOutbox`: accepted fact and projection delivery;
- `ProjectionRebuilder`: deterministic fold from accepted facts and policy snapshots.

Storage technology is an adapter choice. Core semantics require serializable behavior per correlation and atomic commit of all protocol-owned records.

## 5. Canonical lifecycle

The external states remain `DRAFT`, `SUBMITTED`, `REJECTED`, `ACCEPTED`, `IN_PROGRESS`, `RESULT_READY`, `RESULT_REJECTED`, `COMPLETED`, `AMENDMENT_REQUIRED`, `SUPERSEDED`, `COST_APPROVAL_REQUIRED`, `CAPABILITY_GAP`, `HUMAN_REVIEW_REQUIRED`, `CANCELLATION_REQUESTED`, `CANCELLED`, `PARTIAL_RESULT_READY`, `INVALIDATED`, `REVOKED` and `REPLACED`.

Terminal means ordinary production progress is prohibited. `REJECTED`, `SUPERSEDED`, `CANCELLED`, `COMPLETED`, `INVALIDATED`, `REVOKED` and `REPLACED` are terminal for that lifecycle branch. Post-completion governance creates an authorized successor transition; it does not erase terminal history.

### Normative transition table

| From | Accepted fact and authority | To |
|---|---|---|
| DRAFT | `submission_validation_receipt.accepted`, protocol | SUBMITTED |
| DRAFT | `submission_validation_receipt.rejected`, protocol | REJECTED |
| SUBMITTED | `admission_receipt.accepted`, VAE | ACCEPTED |
| SUBMITTED | typed admission/contract rejection, VAE or protocol by reason | REJECTED |
| ACCEPTED | `visual_asset_event.execution_started`, VAE | IN_PROGRESS |
| ACCEPTED or IN_PROGRESS | `amendment_proposal`, VAE | AMENDMENT_REQUIRED |
| ACCEPTED or IN_PROGRESS | `budget_escalation_request`, VAE | COST_APPROVAL_REQUIRED |
| COST_APPROVAL_REQUIRED | approved response, Content Harness/operator | IN_PROGRESS |
| COST_APPROVAL_REQUIRED | denied terminal capability response, Content Harness/operator | CAPABILITY_GAP |
| ACCEPTED or IN_PROGRESS | capability-gap failure, VAE | CAPABILITY_GAP |
| ACCEPTED or IN_PROGRESS | human-exception failure, VAE | HUMAN_REVIEW_REQUIRED |
| IN_PROGRESS | complete production-accepted result, VAE | RESULT_READY |
| IN_PROGRESS | policy-valid partial result, VAE | PARTIAL_RESULT_READY |
| RESULT_READY | accepted acknowledgement, Content Harness/composition runtime | COMPLETED |
| RESULT_READY | rejected acknowledgement, Content Harness/composition runtime | RESULT_REJECTED |
| RESULT_REJECTED | revalidation started, VAE | IN_PROGRESS |
| SUBMITTED, ACCEPTED or IN_PROGRESS | accepted cancellation request, Content Harness/operator | CANCELLATION_REQUESTED |
| CANCELLATION_REQUESTED | cancellation receipt, VAE | CANCELLED |
| SUBMITTED, ACCEPTED, IN_PROGRESS, AMENDMENT_REQUIRED, COST_APPROVAL_REQUIRED, RESULT_READY, RESULT_REJECTED or PARTIAL_RESULT_READY | demand supersession, Content Harness | SUPERSEDED |
| AMENDMENT_REQUIRED | rejected amendment with terminal policy | CAPABILITY_GAP or CANCELLED as explicitly authorized |
| PARTIAL_RESULT_READY | accepted acknowledgement under `partial_allowed`/declared terminal policy | COMPLETED |
| PARTIAL_RESULT_READY | rejected acknowledgement or continuation authorized | RESULT_REJECTED or IN_PROGRESS |
| COMPLETED | invalidation notice, owning product | INVALIDATED |
| COMPLETED | revocation notice, VAE/integrity authority | REVOKED |
| COMPLETED, INVALIDATED or REVOKED | replacement notice plus accepted replacement acknowledgement | REPLACED |

Any absent pair is illegal and yields `reject_and_receipt` with no state change. Product status strings do not change state unless mapped to a registered accepted fact.

## 6. Correlation, causation and ordering

Each accepted fact receives a monotonically increasing `audit_sequence` within its correlation. Ordering authority is this committed sequence, not `occurred_at`, transport offset or arrival time. Every non-initial fact names its direct accepted `causation_id`; the referenced message must exist in the same correlation unless the schema explicitly permits a cross-correlation dependency reference.

Concurrent handlers use compare-and-append with expected sequence. One commits; losers reload and re-decide. A fact valid against stale state may become invalid after reload and is receipted accordingly.

Race rules are:

1. Integrity revocation/incident blocks acceptance before domain precedence.
2. Otherwise, the first valid committed sequence wins.
3. Accepted cancellation or supersession blocks later ordinary progress/results for the affected demand.
4. A result committed before cancellation is `RESULT_READY`; a later cancellation is illegal and the owner must acknowledge/reject or use post-completion governance.
5. Supersession may terminate a ready but unacknowledged old result; that result remains historical and cannot satisfy the new demand.
6. Acknowledgement is valid only for the currently projected exact result and demand identity.

## 7. Idempotency versus replay

Idempotency is a reliability contract for legitimate repeated delivery. Replay protection is a security control against reuse of a signed action outside its intended delivery.

### Idempotency

State-changing commands require a sender-generated key scoped by `(principal_id, message_type, correlation_id, idempotency_key)`. The repository stores payload hash, message ID, status and final receipt. Identical retries return the original receipt and never route twice. Reuse with a different message ID or payload hash returns `IDEMPOTENCY_CONFLICT` and is audited.

An in-progress reservation expires only through a recovery protocol that proves whether the acceptance transaction committed. It is never blindly cleared on process restart. Domain facts such as VAE progress use unique `message_id` deduplication and do not require command idempotency keys unless registered otherwise.

### Replay protection

Every signed state-changing message has a nonce unique within `(signer_principal, key_id)` and a bounded validity interval. A replay index records nonce, message ID, issued/expiry times and decision. Reuse of the same message as a legitimate transport retry is resolved through its message ID/idempotency record. Reuse of a nonce by different bytes or outside the delivery policy is `PROTOCOL_REPLAY_DETECTED`.

Message IDs remain unique for at least the full audit retention period. Nonce records remain until the later of message expiry plus skew or the configured security replay window, minimum 24 hours. High-risk actions may require longer negotiated windows.

## 8. Validation and atomic transaction boundary

The required order is:

1. strict decode and envelope/schema registry lookup;
2. payload resolution and hash verification;
3. principal/key/signature/expiry validation;
4. message ID and nonce replay checks;
5. schema and compatibility/pinned-profile validation;
6. authority and field-owner validation;
7. idempotency lookup/reservation;
8. correlation state load and lifecycle decision;
9. atomic append of accepted/rejected message record, idempotency result, lifecycle transition when accepted, audit receipt and outbox entry;
10. post-commit routing.

A failure in steps 1 through 8 produces a rejection receipt when the message is attributable and safely parseable. If audit persistence is unavailable, no state-changing acceptance commits. A post-commit delivery failure is retried from the outbox and cannot duplicate the domain effect.

## 9. Persistence, reconstruction and recovery

The authoritative protocol record is the append-only accepted/rejected message ledger plus chained audit receipts and pinned policy/schema snapshots. Current lifecycle and Control Tower views are projections.

Reconstruction folds accepted facts in audit sequence through the exact lifecycle-machine version pinned to each transition. Snapshots may accelerate recovery but include sequence, state, last receipt hash and machine version; they are verified against the ledger before use.

Restart recovery reconciles incomplete idempotency reservations, resumes outbox delivery and rebuilds projections from the last verified checkpoint. It never reissues VAE work solely because a boundary process restarted.

## 10. Compatibility, routing and domain interactions

The correlation pins protocol, message, policy, lifecycle-machine and adapter versions at admission. A lifecycle-machine major version is not changed in flight. Compatible minor rules may be used only if the pinned profile authorizes them.

Cancellation, supersession, amendment, result, acknowledgement, invalidation, revocation and replacement payload rules live in TS-DLG-05/06, but all use this ordering and atomicity model. Delegation Set member correlations use this machine independently; set status is a derived projection under TS-DLG-07.

Adapters execute before acceptance and produce immutable migrated facts. The source message and transformation receipt remain causally linked. Routing uses the transactional outbox; consumers must also deduplicate by message ID.

## 11. Failure, retry and invalidation behavior

Contract/authority/compatibility/security failures do not mutate state. Infrastructure failures before commit may be retried with identical bytes. Failures after commit retry outbox delivery only. Quality failures are VAE facts and consume a quality round only when the failure taxonomy says so.

Illegal transitions include current state, attempted fact, accepted sequence and permitted next facts in the receipt. They are not ordinary retryable without a new valid causing fact. Superseded/cancelled results are retained but fail current-use checks.

## 12. Threat model

Threats include duplicate production, nonce reuse, delayed valid-message attack, out-of-order acceptance, clock manipulation, split-brain correlation writers, audit omission, projection corruption and outbox redelivery. Controls are durable dedupe, bounded signatures, per-correlation compare-and-append, fail-closed audit transaction, deterministic replay and consumer dedupe.

The replay repository stores hashes and identifiers, not secret payloads. Clock time gates validity but never orders lifecycle events.

## 13. Observability and SLOs

Expose transition counts, illegal transitions, compare-and-append conflicts, idempotent hits/conflicts, replay detections, nonce-store freshness, reconstruction lag, outbox backlog, audit failures and projection divergence. Critical alerts cover accepted unaudited state, duplicate execution, replay acceptance, sequence gaps and projection hash mismatch.

Targets: 100% valid transitions, zero duplicate production, p99 duplicate resolution at or below 750 ms, 100% audit completeness and p99 projection freshness at or below five seconds after commit.

## 14. Compatibility, migration and rollback

Lifecycle schema/machine versions are compatibility dimensions. A migration may map historical state only through an immutable projection migration receipt; it cannot rewrite accepted facts. Rollback pins new correlations to the prior machine and continues existing correlations on their previously pinned machine unless a tested compatible patch applies.

## 15. Test architecture

- Pure transition-table tests cover every valid and illegal pair.
- Model-based/property tests generate sequences and assert terminal-state invariants.
- Concurrency tests race cancellation, supersession, result and acknowledgement.
- Idempotency tests cover same/different bytes, pending reservations and restarts.
- Replay tests cover nonce reuse, expiry, message-ID collision and legitimate retries.
- Fault injection interrupts each transaction step, audit append and outbox delivery.
- Reconstruction tests compare live and rebuilt projections bit-for-bit.

## 16. Given/When/Then acceptance criteria

1. Given two identical submissions with one idempotency key, when delivered concurrently, then one acceptance commits and both callers receive the same receipt.
2. Given the same key with a different payload hash, when submitted, then `IDEMPOTENCY_CONFLICT` is emitted and no second execution routes.
3. Given a valid old signature with a reused nonce and different bytes, when processed, then `PROTOCOL_REPLAY_DETECTED` blocks state change.
4. Given cancellation commits before a result, when the result arrives, then it is rejected as stale for the cancelled correlation.
5. Given a result commits first, when cancellation arrives from `RESULT_READY`, then cancellation is rejected and acknowledgement/post-completion rules govern.
6. Given an audit-store failure, when a valid transition is processed, then no lifecycle/message/outbox acceptance commits.
7. Given a service restart, when the ledger is replayed, then state, sequence and receipt hash equal the pre-restart projection.
8. Given a supersession of a ready old demand, when acknowledgement follows, then the old result cannot complete the new demand.

## 17. Implementation tasks

1. Generate the pure transition table and illegal matrix from canonical lifecycle metadata.
2. Define storage-neutral repositories and atomic unit-of-work interface.
3. Implement idempotency and replay schemas with retention policy.
4. Produce deterministic race and restart test fixtures.
5. Implement audit-chain and outbox transaction adapters for the reference persistence implementation.
6. Add projection rebuild/checkpoint verification.
7. Validate consumer dedupe requirements with both product repositories.

## 18. Explicit non-goals

- VAE internal workflow state, scheduling or checkpoints
- Content Harness internal sequencing state
- Transport ordering as lifecycle authority
- Exactly-once network delivery claims
- Deleting or rewriting historical facts
- Production implementation during Stage 2

## 19. Readiness and blockers

Specification verdict: `CONCERNS`. Semantics are implementable, but storage ownership under XRI-017, product consumer dedupe and executable cross-repository races must be confirmed before implementation authorization.

## 20. V1.1 constitutional alignment amendment

No lifecycle state or transition changes are introduced. A demand identity is
still the request ID, immutable demand version, full-payload hash, and canonical
reference; the new semantic objects are therefore covered by existing
idempotency and replay fingerprints. Exact retries reuse the original receipt.
Any changed Activative Intelligence Pack, Reaction Receipt, Expression Moment,
role, stance, narrative, feature, or wrong-reading byte produces a different
fingerprint and is rejected under the existing replay/idempotency rules without
an unauthorized state effect. Traceability: `RES-CONSTITUTION-001`.
