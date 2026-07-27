---
title: TS-DLG-05 Budget Cancellation Amendments and Supersession
product: CMF Content Harness Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: stage2_draft_for_review
created: 2026-07-14
---

# TS-DLG-05 Budget, Cancellation, Amendments and Supersession

## 1. Identity and requirement coverage

- Primary features: F05, F07, F08, F12
- Owned FRs: FR-033 through FR-040, FR-049 through FR-064, FR-089 through FR-096
- Owned NFRs: NFR-LIFE-002, NFR-LIFE-004, NFR-REL-003, NFR-PERF-001, NFR-RES-001, NFR-RES-002, NFR-TRACE-002, NFR-TRACE-005
- Decisions: D005, D007, D008, D012
- Resolves: ADR-DLG-011, ADR-DLG-012
- Journeys: UJ-05, UJ-06, UJ-07, UJ-08, UJ-09, UJ-12

## 2. Sources read

Normative inputs are feature shards F05, F07, F08 and F12; authority/lifecycle/failure/compatibility registries; budget, cancellation, amendment, supersession and selective-invalidation schemas/examples; lifecycle/resilience/Format 02 cases; TS-DLG-01 through TS-DLG-04; and Stage 1 XRI-005, XRI-006, XRI-010, XRI-011 and XRI-017.

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

These four flows all modify an in-flight commitment without mutating an accepted demand or exposing VAE internals. The solution is a set of immutable owner-authored commands and VAE evidence facts governed by exact demand identity, JSON Pointer changes, per-correlation ordering and selective invalidation.

The protocol validates and routes. It does not choose budgets, creative amendments, VAE checkpoints, reusable production nodes or production allocation.

## 4. Service and library boundaries

Required protocol modules are `budget-policy-validator`, `change-set-validator`, `amendment-policy-validator`, `race-policy`, `staleness-guard` and `impact-receipt-validator`. VAE-owned adapters implement internal budget allocation, safe stopping and production-plan impact analysis. Content Harness owns new demand versions and policy decisions.

Control Tower receives projections from TS-DLG-08. It may expose approvals and impact but cannot edit canonical messages in place.

## 5. Canonical contracts

### Budget authorization

The closed `BudgetAuthorization` contains ID/version, owner principal, program (`lean`, `standard`, `premium`, `exploration`, `capability_learning`, `custom`), currency, hard cost/time/GPU/candidate/repair ceilings, priority, experimental/capability-learning permissions, escalation threshold/timeout and effective demand/set scope. `custom` requires every hard bound.

The Content Harness/operator owns the envelope and ceilings. The VAE owns allocation inside them. VAE-internal model, provider, seed, workflow and parallelism choices are prohibited public demand fields.

### Budget escalation

`BudgetEscalationRequest` includes exact demand/execution/authorization identities, consumed and committed amounts, requested deltas, evidence, predicted outcome with uncertainty, alternatives and safe checkpoint. `BudgetEscalationResponse` is owner-authored and either approves a new immutable authorization version, denies, cancels or requests an alternative. Approval never patches an authorization in place.

### Cancellation

`CancellationRequest` contains ID, exact demand identity, target scope (`delegation`, `set`, `members`), reason code, stop mode (`nearest_safe_checkpoint`, `finish_current_atomic_step`, `immediate_if_safe`), disposition policy and owner authorization. `CancellationReceipt` contains accepted request, exact execution, final checkpoint, in-flight disposition, typed retained/discarded/quarantined artifact references, consumed/avoided compute and derived `downstream_consumption_authorized=false`.

### Amendment

`AmendmentProposal` contains exact demand identity, trigger/evidence, expiry, and independent options. Every proposed change uses RFC 6901 JSON Pointer, current value hash, proposed canonical value, authority class (`internal_production`, `execution_policy`, `composition`, `semantic_activative`, `constitutional`), rationale and predicted semantic/Activative/composition/cost/time/reuse/invalidation effects with uncertainty/evidence version.

`AmendmentResponse` contains proposal/option identity, `accepted`, `rejected` or `alternative_requested`, decision principal/policy and reason. It never embeds a mutable replacement demand. An accepted demand-owned option is followed by a separately signed new demand and supersession.

### Supersession and impact

`DemandSupersession` contains exact old/new `DemandIdentityRef`, proposal reference when applicable, complete changed-field list and unchanged authority domains. The protocol recomputes canonical JSON diffs and requires an exact match. Change classes are `semantic`, `activative`, `sequence`, `composition`, `identity_continuity`, `delivery`, `evaluation_policy`, `execution_policy`, `budget` or `non_authoritative_notes`.

The VAE returns `SelectiveInvalidationReceipt` with prior/new execution and plan references, changed paths, reusable outputs with lineage/evidence, invalidated outputs/nodes, resume point, uncertainty and production-plan version. Uncertainty or missing evidence defaults to invalidation, never speculative reuse.

## 6. Authority and principal permissions

- Content Harness creates/supersedes demands, budget authorization, cancellation and amendment response.
- Operator policy may approve only actions and ranges in its signed grant.
- VAE requests budget, proposes amendments, computes reuse/invalidations and emits cancellation disposition.
- Protocol validates owners, JSON Pointer paths, policy bounds, ordering and receipts; it never selects an amendment or resume node.
- Composition runtime cannot supersede demand or budget. It may only request owner action through a non-authoritative signal outside these contracts.

A bounded auto-amendment policy names exact schema version, JSON Pointer allowlist, numeric/enum bounds, expiry and maximum approvals. It cannot cover semantic/Activative, sequence role, identity, wrong-reading, constitutional or quality-gate changes.

## 7. Lifecycle and message flows

### Budget

An accepted delegation pins budget authorization. Before a VAE atomic commitment that could breach a hard ceiling, VAE stops scheduling new work and emits escalation, causing `ACCEPTED|IN_PROGRESS -> COST_APPROVAL_REQUIRED`. Approval with a new authorization causes `-> IN_PROGRESS`; terminal denial causes capability gap or cancellation according to the signed response. Existing safe work/evidence is retained.

### Amendment

Constraint conflict or proposal causes `ACCEPTED|IN_PROGRESS -> AMENDMENT_REQUIRED`. A rejected option leaves the demand unchanged and either resumes if the original is feasible, requests another option or terminates through a typed decision. Accepted demand-owned change creates new demand/supersession; it never directly resumes the old demand.

### Supersession

After authority/diff validation, the old branch becomes `SUPERSEDED`. New execution uses a new correlation or an explicitly linked successor branch according to the implementation profile; in both cases it references the old correlation and impact receipt. Old late facts are retained and rejected for current promotion.

### Cancellation

Accepted cancellation causes `SUBMITTED|ACCEPTED|IN_PROGRESS -> CANCELLATION_REQUESTED`, immediately blocking new VAE work for scope. VAE reaches the nearest allowed safe atomic boundary and returns a receipt, causing `CANCELLED`. Cancellation does not delete evidence.

## 8. Race and precedence rules

Per TS-DLG-03, committed sequence is authoritative. Domain rules are:

1. A committed supersession/cancellation blocks later progress and result promotion for the old scope.
2. If result readiness committed first, cancellation from `RESULT_READY` is illegal; current acknowledgement/rejection governs.
3. If budget escalation committed first, a later cancellation is valid and supersedes waiting for approval; a later approval is stale.
4. If cancellation committed first, later amendment/escalation responses are stale.
5. If amendment acceptance and supersession are concurrent, only the exact response-caused new demand/supersession pair is accepted; duplicates resolve idempotently.
6. A supersession of a completed result routes through invalidation/replacement under TS-DLG-06.

Deadlines are distinct: target completion is advisory; approval timeout triggers typed policy; hard cutoff requires stop/checkpoint; delegation expiry rejects new actions after its instant. Clock events are protocol-authored timer facts and are audited.

## 9. Budget enforcement and quality preservation

The VAE must expose a certified budget-admission interface that compares consumed plus committed maximum cost against hard ceilings before scheduling each chargeable atomic unit. The protocol validates authorizations/escalations and audits VAE usage facts; it does not schedule nodes.

Budget pressure may stop with no asset, return an already production-accepted candidate or request authority. It may not lower hard quality gates, wrong-reading locks or required evaluations. Capability Learning requires explicit authorization and produces controlled-variable/evidence receipts separated from ordinary production cost.

Every terminal branch carries a final budget receipt with authorization versions, estimated/actual cost, wall/GPU time, candidate/repair counts, compliance and measurable avoided cost.

## 10. Correlation, idempotency, replay and routing

Every flow uses the original correlation and direct causation. A successor demand/execution also references the prior correlation. Commands are idempotent by owner/scope/key/payload hash; VAE evidence facts deduplicate by message ID. Reusing a signed approval for another proposal, demand, scope or amount is replay and rejected.

Messages route through the transactional outbox after authority/lifecycle acceptance. Cancellation is delivered on the highest-priority control channel available, but channel priority does not bypass validation or determine order.

## 11. Compatibility, adapters and migration

Support for budget programs, deadline modes, amendment authority classes, change classes, cancellation scopes and selective-invalidation evidence is negotiated. Missing required cancellation/supersession behavior is incompatible.

Adapters may normalize units or wrap exact fields but cannot weaken ceilings, omit changed paths, broaden policy ranges or turn uncertainty into reusable evidence. Migrations preserve old/new identities and owner decisions. In-flight correlations remain pinned.

## 12. Persistence and transaction boundaries

Budget authorizations, proposals/responses, new demands, supersessions, cancellation commands/receipts and impact receipts are immutable resources. Command acceptance, lifecycle change, stale-scope guard, audit and outbox are atomic. VAE compute checkpoints remain VAE-owned but are referenced by immutable IDs/hashes.

The staleness guard is queried during result and acknowledgement acceptance. It derives from committed cancellation/supersession facts, not mutable flags.

## 13. Failure, retry and recovery

Failures include unauthorized action/path, diff mismatch, unknown budget program, hard-ceiling breach, approval timeout, capability gap, amendment expiry, invalid impact evidence and stale post-cancellation facts. Infrastructure retries do not consume quality rounds. VAE quality repairs do only when classified as quality failures.

After restart, protocol projections rebuild from facts; VAE resumes only from its certified checkpoint and linked plan version. If impact evidence cannot be recovered, affected outputs are invalidated and work restarts from a safe earlier point.

## 14. Threat model

Threats include ceiling bypass, forged approval, under-reported committed cost, cancellation suppression, stale result race, malicious changed-path omission, overclaimed reuse and broad auto-amendment policies. Controls are signed exact scopes, diff recomputation, committed-sequence ordering, independent receipts, policy bounds, conservative invalidation and cross-product conformance.

## 15. Observability and SLOs

Project current authorization/remaining ceilings, escalation age, cancellation acceptance/checkpoint age, supersession lineage, amendment owner/expiry and reuse/invalidated counts. Metrics include hard-ceiling rejections, stale facts, auto-policy approvals, impact uncertainty and cancellation response.

Target p99 boundary action for cancellation is at or below ten seconds, excluding VAE atomic-step duration but including immediate block-new-work acknowledgement. Budget overruns and stale promotion target zero.

## 16. Test architecture

- Schema/property tests for units, bounds, JSON Pointer diffs and closed nested shapes.
- Authority tests for every command/evidence producer and bounded policy edge.
- Race tests for cancellation/result, escalation/cancellation, supersession/result and amendment/supersession.
- Budget boundary tests at exactly below/equal/above ceilings and Capability Learning authorization.
- Restart/checkpoint tests preserving evidence and quality-round accounting.
- Selective-invalidation fixtures with valid reuse, uncertainty and malicious overclaim.
- Format 02 escalation, amendment, cancellation and supersession scenarios.

## 17. Given/When/Then acceptance criteria

1. Given a changed demand whose declared paths omit a semantic diff, when supersession is validated, then diff mismatch is rejected.
2. Given a valid composition-only supersession, when VAE impact evidence certifies identity artifacts reusable, then those references retain lineage and only affected outputs invalidate.
3. Given insufficient remaining budget, when the next atomic commitment exceeds a hard ceiling, then no new work starts and escalation is emitted.
4. Given a denied escalation, when production stops, then checkpoint evidence and final spend remain available without quality-gate degradation.
5. Given a VAE amendment option affecting semantic intent, when an auto-policy attempts approval, then policy authorization is denied.
6. Given cancellation commits before a late result, when the result arrives, then it cannot receive downstream authorization.
7. Given an accepted amendment, when the owner proceeds, then a new immutable demand and supersession are required before production resumes.
8. Given uncertain reuse evidence, when impact is applied, then the affected output is invalidated rather than reused.

## 18. Implementation tasks

1. Close/revise all budget, cancellation, amendment, supersession and impact schemas.
2. Add exact demand/execution/authorization reference types and JSON Pointer diff validator.
3. Define bounded auto-policy schema/evaluator.
4. Implement storage-neutral stale-scope and race-policy interfaces.
5. Define VAE budget-admission/checkpoint adapter contracts without exposing internals.
6. Build deterministic race, budget and selective-reuse fixture suites.
7. Reconcile behavior with real product adapters under XRI-002.

## 19. Explicit non-goals

- Cloud billing, VAE scheduling or internal production-plan invalidation algorithms
- Protocol ranking of amendment options
- Silent quality degradation or constitutional changes
- Deleting cancelled/superseded evidence
- Production implementation during Stage 2

## 20. Readiness and blockers

Specification verdict: `CONCERNS`. Shared semantics are defined, but VAE checkpoint/budget-admission and Content Harness demand-version adapters require cross-repository confirmation before contract freeze.

## 21. V1.1 constitutional alignment amendment

Cancellation, amendment, and supersession precedence is unchanged. A migrated
V1.1 demand is a new immutable version whose `supersedes` tuple pins the exact
V1 source. An amendment proposal may identify protected semantic paths but may
not mutate them; only Content Harness can issue the successor demand. Selective
reuse is prohibited when any Activative lineage, Activation Contract, Visual
Semantic/Narrative, Feature Contract, T/V route, Expression Moment, or
wrong-reading dependency changed without evidence.
