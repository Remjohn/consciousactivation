---
title: TS-DLG-08 Audit Observability and Control Tower Projections
product: CMF Content Harness Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: stage2_draft_for_review
created: 2026-07-14
---

# TS-DLG-08 Audit, Observability and Control Tower Projections

## 1. Identity and requirement coverage

- Primary feature: observability portion of F15
- Owned FRs: FR-113 through FR-115
- Owned NFRs: NFR-OBS-001 through NFR-OBS-005, NFR-PERF-002, NFR-PERF-003, NFR-TRACE-001, NFR-DATA-003, NFR-DATA-004
- Decision: D015
- Resolves: ADR-DLG-016, ADR-DLG-018 and measurement portion of ADR-DLG-019
- Journeys: UJ-03, UJ-07, UJ-10, UJ-12, UJ-13, UJ-14

## 2. Sources read

Normative inputs are `prd/05-features/F15-observability-conformance.md`, `governance/PROTOCOL_SLO_TARGETS.yaml`, `governance/SUCCESS_METRICS.yaml`, audit schema/example, expected Format 02 Control Tower projection, architecture preservation rule PRES-012, TS-DLG-01 through TS-DLG-07 and XRI-014, XRI-015 and XRI-017.

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

The package defines expected fields and targets but has no audit ledger, projection contract, metrics or existing Control Tower interface. This specification defines append-only audit evidence and an additive read-model adapter into the validated Harness Control Tower. It explicitly prohibits a second operational source of truth.

Observability reports protocol health and shared state. It does not expose private VAE workflow nodes, model prompts, secrets or Content Harness reasoning traces.

## 4. Service and library boundaries

Required modules are `audit-receipt-builder`, `audit-chain-verifier`, `projection-fold`, `control-tower-port`, `metrics-port`, `incident-port`, `retention-policy` and `projection-reconciler`.

The protocol ledger is the source for shared facts. Control Tower owns its UI/query/runtime. The adapter publishes read-model updates and reconciliation evidence; it does not create an independent authority database. Product-internal telemetry remains in product observability systems and may be linked by stable diagnostic references.

## 5. Audit-chain implementation

Every attributable accepted or rejected boundary action produces a `DelegationAuditReceipt` containing:

- receipt/message/correlation IDs and per-correlation sequence;
- exact principal/key, schema/registry/profile/policy/machine versions and hashes;
- results for decode, payload hash, signature, replay, schema, compatibility, authority, idempotency and lifecycle checks;
- accepted transition or explicit no-state-change rejection;
- causation, persisted time, outbox reference and stable failure code;
- prior receipt hash and current receipt hash.

Receipt hash is SHA-256 over RFC 8785 canonical receipt bytes with `receipt_hash` omitted. `previous_receipt_hash` links the prior receipt in the correlation; the first is null. Periodic signed ledger checkpoints commit the latest receipt hash for each active partition and a Merkle root for tamper evidence across partitions.

Message/state/audit/outbox commit atomically under TS-DLG-03. Audit-store interruption fails state-changing acceptance closed. Read-only validation requests may return unavailable without mutation.

Audit access is role-scoped. Receipts store identifiers, hashes, decisions and references, not message bodies, media, credentials or private reasoning.

## 6. Canonical Control Tower read model

`DelegationProjection` is keyed by correlation and contains:

- current lifecycle state/sequence and authoritative last message/receipt;
- Content Harness, VAE, protocol and delegated composition principal/release IDs;
- exact demand, set and result identities;
- pinned protocol/message/policy/lifecycle/compatibility profile;
- authority owner summary and latest denied action;
- budget authorization/consumption/escalation state;
- target/hard/expiry timing and latest heartbeat/event;
- amendment, cancellation, supersession and selective-invalidation state;
- result readiness, acknowledgement and current-use authorization;
- invalidation/revocation/replacement/impact summary;
- audit-chain verification status and projection freshness;
- responsible owner, next action and stable failure when blocked.

`DelegationSetProjection` adds policy, member summaries, graph blockers and set evaluation/release state. `DelegationImpactProjection` lists active/rendered/published affected scopes and acknowledgement state.

Every field names its source message/receipt and sequence. Unknown/missing data is explicit, never inferred from UI state.

## 7. Projection flow, consistency and routing

After the acceptance transaction commits, the outbox publishes a canonical projection fact. The adapter idempotently folds by `(correlation_id, audit_sequence)`. Duplicate facts are ignored after hash comparison; gaps pause that correlation and trigger backfill. Out-of-order facts buffer within a bounded window and otherwise request replay from the ledger.

Projection freshness is measured from committed `persisted_at` to Control Tower acknowledgement, not sender `occurred_at`. Reconciliation periodically rebuilds a sampled/full projection from ledger facts and compares state, sequence and source hashes.

Control Tower commands, if any, return through normal signed protocol ports as owner messages. UI writes never mutate projection rows as authority facts.

## 8. Metrics, SLIs and SLOs

Normative SLIs include:

| SLI | Target |
|---|---|
| Valid submission receipt latency | p99 <= 1000 ms |
| Idempotent duplicate resolution | p99 <= 750 ms |
| Accepted event delivery | >= 99.9% |
| Lifecycle projection freshness | p99 <= 5 seconds |
| Eligible automatic acknowledgement | >= 99% within 10 seconds |
| Accepted cancellation to block-new-work boundary acknowledgement | p99 <= 10 seconds |
| Critical invalidation/revocation projection | p99 <= 10 seconds |
| Audit receipt completeness | 100% |
| Unauthorized state mutation | 0 |

Each SLI specification must define numerator, denominator, exclusions, rolling window, source event and owner. Quality failure or unavailable asset generation is not removed from boundary-health denominators unless the SLI explicitly measures protocol-valid input.

Metrics cover acceptance/rejection, delivery, duplicate suppression, replay, transition validity, acknowledgement, stale prevention, budget, set blockers, audit verification, projection gaps, stalled/orphaned work and critical impacts. Labels use bounded product type/version/profile/reason values; raw IDs and URIs belong in traces/audit, not metric labels.

ADR-DLG-019 requires benchmarks for canonicalization, signature, authority, compatibility, ledger and projection overhead using Format 02 payload distributions. SLOs may be tightened or relaxed only through an ADR with evidence, never by weakening quality or authority gates.

## 9. Failure detection and incident behavior

Detect at minimum:

- stalled correlations with no expected progress/owner action;
- orphaned VAE executions lacking a current accepted correlation;
- superseded/cancelled branches still producing;
- ready results beyond acknowledgement SLO;
- projection gaps/divergence or audit-chain mismatch;
- budget hard-ceiling attempts and overdue approvals;
- expired amendments/cancellations awaiting receipt;
- active use of invalidated/revoked assets;
- signature/replay/authority attack clusters.

Critical integrity, audit, stale-consumption and revocation incidents route immediately to the incident port with exact audit references. The incident system owns paging/workflow; the protocol owns the immutable incident fact and any state block defined by policy.

## 10. Correlation, authority and domain interactions

Traces link message, correlation, causation, receipt, set and impact IDs. The protocol owns shared projections; product owners remain authoritative for source facts. Operators can approve only through signed messages defined in the domain specs.

Cancellation, supersession, result acknowledgement and post-completion notices update their dedicated projection sections. Compatibility profile and adapter/migration receipts remain visible for the full lifecycle. Replay/idempotency outcomes are audit events even when no state changes.

## 11. Compatibility, migration and rollback

Projection schemas are versioned public consumer contracts. Additive optional fields are minor; changed meaning/removal is major. Control Tower declares accepted projection versions in its compatibility manifest.

An adapter may map a newer projection to an older read model only by omitting fields explicitly optional for that consumer; authority/current-use/security fields cannot be omitted. Projection migration rebuilds from the ledger. Rollback deploys a prior projector and rebuilds its read model; it never rolls back the ledger.

## 12. Persistence, retention and privacy

Audit receipts and accepted message metadata retain at least as long as the longest referenced contract/result/publication policy. Exact durations and legal holds are deployment policy. Idempotency/replay retention follows TS-DLG-03. Projection rows may be rebuilt and have shorter operational retention.

Large payloads/media use access-controlled immutable references/hashes. Reference resolvers enforce recipient scope, retention and availability policy. Negative/revoked evidence is quarantined from ordinary reuse. Secrets and unnecessary private reasoning are prohibited; diagnostics use restricted references.

## 13. Threat model

Threats include audit deletion/reordering, projection tampering, fake health, metric-cardinality denial, sensitive-data leakage, stale dashboard actions and Control Tower becoming authority. Controls are hash chains/checkpoints, rebuild/reconciliation, bounded labels, redaction/reference rules, source links and signed command return paths.

## 14. Test architecture

- Hash-chain vectors cover insertion, deletion, reorder and corruption.
- Transaction tests prove no accepted state without audit/outbox.
- Projection tests fold every lifecycle/domain fact and assert source references.
- Duplicate/out-of-order/gap/restart tests verify idempotent recovery.
- Reconciliation tests intentionally corrupt projections and detect divergence.
- SLI tests verify numerator/denominator math and synthetic breach alerts.
- Privacy tests reject secrets/media/private reasoning and verify access control.
- Control Tower consumer contract tests run against its declared interface when supplied.

## 15. Given/When/Then acceptance criteria

1. Given an accepted state change, when committed, then exactly one chained audit receipt and outbox fact exist atomically.
2. Given audit-store interruption, when a state-changing message arrives, then acceptance fails closed and an operational incident is raised when safely possible.
3. Given duplicate projection delivery, when folded, then state/sequence do not change and hash mismatch raises an incident.
4. Given an out-of-order sequence gap, when projected, then later facts do not advance visible state until backfill verifies the gap.
5. Given a Control Tower operator action, when submitted, then it returns as a signed authorized protocol message rather than mutating the view.
6. Given a revoked asset with published impacts, when projected, then active/published scopes and unresolved review acknowledgement are visible within the critical SLO.
7. Given a media binary or secret in a message, when validated, then data-minimization policy rejects it.

## 16. Implementation tasks

1. Close the audit-receipt schema and publish canonical hash vectors.
2. Define ledger/checkpoint, projection and incident fact schemas.
3. Implement pure projection folds and reconciliation interfaces.
4. Define every SLI formula, window and evidence query.
5. Build telemetry adapters with bounded labels and secure trace links.
6. Integrate the actual Harness Control Tower contract under XRI-014.
7. Benchmark Format 02 payloads and record ADR-DLG-019 evidence.
8. Finalize retention/access policy with platform/security owners.

## 17. Explicit non-goals

- A separate Control Tower or authority store
- VAE GPU/model/workflow monitoring
- Storage of message bodies or media in metrics/logs
- UI-driven state mutation
- Production implementation during Stage 2

## 18. Readiness and blockers

Specification verdict: `CONCERNS`. Audit/projection semantics are complete, but actual Control Tower, storage, incident and retention owner interfaces remain cross-repository blockers.

## 19. V1.1 constitutional alignment amendment

Audit and Control Tower state ownership is unchanged. Compatibility rejection
evidence must identify the missing semantic domain/mode, evaluator evidence, or
lossy adapter path. Migration audit evidence pins source and target demand
hashes and the immutable output reference. Projections may expose identifiers,
versions, hashes, verdicts, and failure codes, but must not copy private
semantic bodies or become an alternate authority store.
