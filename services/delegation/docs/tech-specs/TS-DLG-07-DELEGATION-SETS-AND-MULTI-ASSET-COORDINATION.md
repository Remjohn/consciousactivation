---
title: TS-DLG-07 Delegation Sets and Multi-Asset Coordination
product: CMF Content Harness Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: stage2_draft_for_review
created: 2026-07-14
---

# TS-DLG-07 Delegation Sets and Multi-Asset Coordination

## 1. Identity and requirement coverage

- Primary feature: F10
- Owned FRs: FR-073 through FR-080
- Owned NFRs: NFR-CONTRACT-004, NFR-LIFE-005, NFR-DATA-001
- Decision: D010
- Resolves: ADR-DLG-014
- Journeys: UJ-09, UJ-04, UJ-05, UJ-08, UJ-12

## 2. Sources read

Normative inputs are `prd/05-features/F10-delegation-sets.md`, delegation-set schema/example, authority/lifecycle/compatibility registries, Format 02 set fixture/scenarios, TS-DLG-01 through TS-DLG-06 and XRI-006, XRI-010 and XRI-017.

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

Related assets need shared continuity and completion policy without becoming a mutable batch or losing member lineage. The solution is an immutable versioned Delegation Set that references independent demand correlations, declares a typed dependency DAG and derives set status from member facts.

The protocol validates graph/authority/policy and projects status. It does not schedule VAE batches, author scene composition or evaluate creative quality.

## 4. Service and library boundaries

Required modules are `set-contract-validator`, `dependency-graph`, `constraint-inheritance`, `set-status-projector`, `set-impact-analyzer` and `set-release-guard`. Member lifecycle remains TS-DLG-03. Result/acknowledgement remains TS-DLG-06.

Content Harness creates set versions and owns shared constraints/completion policy. VAE creates member production and set-evaluation evidence. Content Harness/composition runtime owns assembled downstream acknowledgement.

## 5. Canonical Delegation Set contract

The closed payload contains:

- `set_id`, monotonic `version`, optional exact superseded set identity and owner principal;
- category, format, sequence, composition and Visual Syntax context references with versions/hashes;
- members with unique `member_id`, exact `DemandIdentityRef`, role, required flag and release order;
- shared constraints with typed identity, environment/world state, palette, lighting, camera axis, scale and geometry references;
- typed dependency edges;
- completion policy and required role set;
- set-level evaluation profile/reference requirements;
- effective budget/cancellation policy references where shared.

Accepted set versions are immutable. Adding/removing/changing a member or constraint creates a new set version and explicit supersession. Member demand identities are never embedded mutable bodies.

## 6. Dependency graph and constraint semantics

The member graph is a directed acyclic graph. Edge types are `identity_source`, `environment_source`, `lighting_reference`, `palette_reference`, `interaction_geometry`, `scale_reference`, `ordered_production` and `release_dependency`. Each edge declares upstream/downstream member IDs, required evidence, invalidation dimensions and whether downstream production or only release is blocked.

Self-edges, unknown members, duplicate edges and cycles are invalid. Topological order uses member ID as stable tie-breaker.

Shared constraints are Content Harness-owned. A member demand may refine a shared constraint only in a declared refinement field and may not contradict it. Effective constraints are a deterministic merge of set base plus member refinement. Conflicts are rejected before submission or returned as typed VAE constraint conflicts/amendments; the protocol never chooses which creative constraint to drop.

## 7. Member lifecycle and set status

Each member retains independent correlation, demand version, execution, result, acknowledgement, repair, cancellation, supersession and history. Set status is a read model, not a member state mutation.

Derived set statuses are `DRAFT`, `ACTIVE`, `BLOCKED`, `PARTIAL_READY`, `READY_FOR_SET_EVALUATION`, `RESULT_READY`, `COMPLETED`, `PARTIAL_COMPLETED`, `CANCELLED`, `SUPERSEDED`, `INVALIDATED` and `REVOKED`.

Derivation rules:

- `ACTIVE` when any required member is submitted/in progress and no terminal policy condition applies.
- `BLOCKED` when a required member is in amendment, cost approval, capability gap or human review and policy cannot proceed.
- `PARTIAL_READY` when at least one member is acknowledged and required completion is not met.
- `READY_FOR_SET_EVALUATION` when all members required by the policy have production-accepted results.
- `RESULT_READY` when required set-level evaluation passes and results await assembled acknowledgement/release.
- `COMPLETED` when policy-required members and set/assembled acknowledgements pass.
- `PARTIAL_COMPLETED` only for `partial_allowed` with every required role complete and optional failures recorded.
- Terminal cancellation/supersession/invalidation/revocation derives from accepted scoped facts, never member-count heuristics alone.

## 8. Completion and release policies

| Policy | Normative behavior |
|---|---|
| `independent` | Each member may release after its own acknowledgement; set projection summarizes progress. |
| `partial_allowed` | All declared required roles must complete; optional failures are explicit and do not block terminal partial completion. |
| `atomic_required` | No member becomes consumable through the set until all required members, set evaluation and assembled acknowledgement pass. |
| `ordered_release` | Members release in topological/declared order after each predecessor release condition passes. |

Policy is pinned at set admission. Changing it creates a new set version and impact analysis. Atomic policy does not hide member production facts; it only gates downstream authorization.

## 9. Set-level evaluation and acknowledgement

Where policy requires, the VAE assembles production outputs into a certified interaction/composition simulation and emits evidence for cross-asset identity, palette, lighting, scale, geometry and production-quality consistency. The VAE does not author sequence/composition meaning.

The Content Harness or composition runtime validates the simulation against current sequence/composition/Visual Syntax context and owns assembled consumption acknowledgement. The protocol validates receipts and dependencies but performs no visual evaluation.

Set evaluation/acknowledgement references exact member result hashes. A changed member invalidates the set evidence that depended on it.

## 10. Selective invalidation, cancellation and supersession

Impact starts from changed/failed/cancelled/revoked members or shared constraint paths and traverses outgoing edges whose invalidation dimensions match. Only reachable dependent members, set evaluations and release gates invalidate. Unrelated accepted members remain valid.

A shared constraint change may affect all members that inherit it. VAE provides production reuse evidence per member under TS-DLG-05. Set impact receipt lists preserved/invalidated member facts and evaluation references.

Cancellation scope may target one member, optional members, required-role group or entire set. `atomic_required` cancellation of a required member blocks set release and requires owner resolution; it does not automatically cancel unrelated running members unless policy says so. Supersession follows the same scope and creates new immutable member/set versions.

## 11. Correlation, causation, idempotency and routing

The set has a `set_correlation_id`; every member retains its own correlation and includes set ID/version/member ID references. Set commands causally reference member facts when applicable. Cross-member events route through accepted protocol facts, not direct VAE coupling.

Set creation/version commands are idempotent by owner/set/version/hash. Member facts deduplicate under TS-DLG-03. Replay of a set command against a different member graph is rejected.

## 12. Compatibility, adapters and migration

Negotiation covers completion policies, edge types, constraint fields, set evaluation/receipt support and maximum set size/depth. Missing required atomic/set-evaluation behavior is incompatible.

Adapters may rename edge/constraint representations but cannot flatten members, erase lineage, change required roles or weaken atomic policy. Migration creates a new set artifact and proves identical member identities and graph semantics.

## 13. Persistence and transactions

Set versions, member links, graph edges, projections, evaluation facts and impact receipts are immutable/event-sourced. Member acceptance remains an independent transaction. Set projection updates consume member outbox facts idempotently; projection lag never authorizes release early.

Release authorization transaction verifies current set version, member result/ack states, graph dependencies, set evidence and no active invalidation before emitting a set release receipt.

## 14. Failure, retry and recovery

Failures include graph cycle, unknown member, conflicting shared constraint, missing required role, dependency unavailable, member capability gap, set evaluation failure and stale set version. Product infrastructure retry does not change member quality rounds.

Projection rebuild folds set versions and member facts. If set evidence is missing/corrupt, release fails closed while member historical states remain intact.

## 15. Threat model

Threats include member substitution, hidden cycle, optional/required role tampering, atomic-gate bypass, stale set evidence, over-broad invalidation and cross-member authority leakage. Controls are exact member hashes, closed graph schema, deterministic derivation, signed policy, release guard and impact traversal tests.

## 16. Observability and SLOs

Project set/version/policy, member states, blockers, dependency edges, required roles, evaluation/acknowledgement and invalidation scope. Metrics include set completion latency, blocked age, projection lag, invalidation fanout and false broad invalidation.

Set projection follows the five-second p99 freshness target. No set metric should use member IDs or asset URIs as unbounded labels.

## 17. Test architecture

- Schema/graph tests cover cycles, missing members, duplicate roles and invalid refinements.
- Model tests derive status for every completion policy/member-state combination.
- Authority tests reject VAE set-policy changes and protocol creative constraint changes.
- Invalidation tests prove exact reachable fanout and preserved unrelated members.
- Race tests cover member completion/cancellation/supersession and set-version change.
- Atomic/ordered release guards receive adversarial stale evidence.
- Format 02 character/background/prop set runs through production evidence and acknowledgement.

## 18. Given/When/Then acceptance criteria

1. Given three independent member demands in an atomic set, when two complete, then their facts remain visible but no set release authorization is emitted.
2. Given a dependency cycle, when a set is submitted, then validation rejects it before member routing.
3. Given an optional overlay cancellation under `partial_allowed`, when required roles are complete, then the set may reach `PARTIAL_COMPLETED` with the omission recorded.
4. Given a shared palette change, when impact is computed, then only inheriting members and dependent set evaluations invalidate.
5. Given a completed unrelated member, when another branch fails, then the unrelated result retains its independent lineage and authorization.
6. Given stale set-evaluation evidence after member supersession, when release is attempted, then the release guard rejects it.
7. Given a VAE attempt to change required roles, when authority is checked, then the message is rejected.

## 19. Implementation tasks

1. Close the Delegation Set schema and vocabularies.
2. Implement pure DAG validation, topological order and status derivation.
3. Define set-evaluation, assembled-acknowledgement, impact and release-receipt schemas.
4. Implement storage-neutral member projection and release-guard interfaces.
5. Add policy matrices and property-based graph/invalidation tests.
6. Reconcile actual VAE composition-simulation and Content Harness composition adapters.

## 20. Explicit non-goals

- VAE batch scheduling or internal production graph
- Final scene composition or publication
- Merging member demand/result histories
- Protocol creative conflict resolution
- Production implementation during Stage 2

## 21. Readiness and blockers

Specification verdict: `CONCERNS`. Graph and policy semantics are defined, but real set-evaluation and assembled-acknowledgement adapter contracts require the upstream repositories before freeze.
