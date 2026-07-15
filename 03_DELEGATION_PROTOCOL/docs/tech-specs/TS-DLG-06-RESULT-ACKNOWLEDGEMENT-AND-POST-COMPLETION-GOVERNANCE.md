---
title: TS-DLG-06 Result Acknowledgement and Post-Completion Governance
product: CMF Content Harness Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: stage2_draft_for_review
created: 2026-07-14
---

# TS-DLG-06 Result Acknowledgement and Post-Completion Governance

## 1. Identity and requirement coverage

- Primary features: F06, F13
- Owned FRs: FR-041 through FR-048 and FR-097 through FR-104
- Owned NFRs: NFR-LIFE-003, NFR-REL-004, NFR-DATA-002, NFR-DATA-005
- Decisions: D006, D013
- Resolves: ADR-DLG-005, ADR-DLG-013 and result portion of ADR-DLG-012
- Journeys: UJ-04, UJ-05, UJ-09, UJ-12, UJ-14

## 2. Sources read

Normative inputs are feature shards F06 and F13; result, acknowledgement, invalidation, revocation and replacement schemas/examples; authority/lifecycle/failure registries; Format 02 result/replacement scenarios; TS-DLG-01 through TS-DLG-05; and Stage 1 XRI-004, XRI-006, XRI-010, XRI-014 and XRI-017.

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

Production acceptance and downstream compatibility are separate authorities, but the provisional result schema conflates them. Completed facts also need current-use governance without deletion or mutation. The solution is a VAE-owned immutable production result, an owner-authored acknowledgement and append-only authorization notices over a retained consumption graph.

The protocol validates identity, authority, current dependencies and receipts. It does not repeat VAE visual-quality evaluation, publish media or decide recall policy.

## 4. Service and library boundaries

Required protocol modules are `result-contract-validator`, `acknowledgement-validator`, `current-use-guard`, `consumption-link-registry`, `impact-traversal`, `post-completion-policy` and `replacement-validator`. Content Harness/composition adapters provide current sequence/composition dependency snapshots. VAE provides production/evaluation receipt references.

Control Tower projects current authorization and impact from immutable facts; it is not an editable result database.

## 5. Canonical result contract

The next-major `AssetResultContract` is a closed VAE-authored payload containing:

- result ID and exact `DemandIdentityRef`;
- VAE release, execution and Visual Production Plan references;
- `production_acceptance=true` plus certified profile and evaluation/production receipt references;
- one or more accepted assets with immutable asset ID/version/hash/URI, role, delivery metadata, composition geometry/mask/timing references and lineage;
- typed unresolved roles for a policy-valid partial result;
- final budget receipt reference;
- produced-at time and retention/access class.

It does not contain `downstream_consumption_authorized`. A false default is also prohibited because it still gives the VAE ownership of another principal's fact. The shared current-use state derives from acknowledgement and later notices.

Only the VAE may assert production acceptance. Raw candidates or assets lacking certified receipts cannot enter `RESULT_READY`.

## 6. Result acknowledgement

`ResultAcknowledgement` is authored by the owning Content Harness or an exactly delegated composition runtime. It contains result identity/hash, exact demand identity, current sequence/composition/category/profile/dependency snapshot references, deterministic check results, `accepted` or `rejected`, stable reason/next action and `downstream_consumption_authorized`.

Automatic acceptance requires all of:

1. exact current demand ID/version/hash and non-supersession;
2. result production acceptance and required receipt availability/hash validity;
3. required asset roles and completion policy satisfied;
4. current sequence/composition/category/profile references match the owner snapshot;
5. geometry, masks, timing and delivery contracts are compatible;
6. upstream dependencies are current and not invalidated/revoked;
7. every asset reference is resolvable and authorized;
8. no cancellation, supersession or post-completion block applies.

The checker validates downstream compatibility only. It does not re-score semantic fidelity, Activative effectiveness, visual quality or VAE candidate ranking.

Stable rejection codes include `STALE_DEMAND_VERSION`, `STALE_SEQUENCE_VERSION`, `STALE_COMPOSITION_VERSION`, `MISSING_PRODUCTION_RECEIPT`, `INCOMPATIBLE_GEOMETRY_PROFILE`, `ASSET_REFERENCE_UNAVAILABLE`, `DEPENDENCY_INVALIDATED`, `RESULT_SUPERSEDED`, `REQUIRED_ROLE_MISSING` and `RESULT_REVOKED`. Free-form aesthetic dislike is not valid.

## 7. Lifecycle and message flows

- VAE result acceptance causes `IN_PROGRESS -> RESULT_READY` or `PARTIAL_RESULT_READY`.
- Accepted acknowledgement causes `RESULT_READY -> COMPLETED` and records exact consumed assets/state.
- Rejected acknowledgement causes `RESULT_READY -> RESULT_REJECTED`; a VAE revalidation fact may return to `IN_PROGRESS`.
- A terminal partial result completes only when the pinned completion policy permits it and all required roles/checks pass.
- Demand supersession before acknowledgement causes the old branch to `SUPERSEDED`; its result remains historical.
- After completion, invalidation causes `COMPLETED -> INVALIDATED`, revocation causes `COMPLETED -> REVOKED`, and replacement plus accepted replacement acknowledgement causes `COMPLETED|INVALIDATED|REVOKED -> REPLACED`.

Acknowledgement is idempotent for the same result and dependency snapshot. A contradictory second decision is rejected; changes require a new causally linked message or governance notice.

## 8. Post-completion notices and current-use state

### Invalidation

An owning product emits invalidation when a dependency, demand, sequence, composition or authority context changed without proving an asset defect. The notice names affected result/assets, trigger fact, affected/unaffected dimensions, scope and required revalidation. It may block new/active consumption pending review while preserving historical use.

### Revocation

The VAE or registered integrity authority emits revocation for critical production defect, integrity/security failure, evaluator regression or withdrawn capability. Severity, effective time, new/active/published-use policy and evidence are required. New consumption is blocked immediately after acceptance.

### Supersession and replacement

A preferred newer result is not automatically a mandatory replacement. `ReplacementNotice` links old/new exact result identities, reason, impact evidence and compatibility status. The candidate replacement must pass current demand, geometry, masks, timing, Visual Syntax context and composition checks and receive its own acknowledgement before current-use authorization moves.

Original result, assets, receipts and acknowledgement never change. Current-use queries fold all accepted notices by sequence and scope.

## 9. Consumption links and impact analysis

Every successful consumption records an immutable link from result/asset to variant, composition, scene/slide, sequence, rendered output and publication when applicable. Each link includes exact consumer version/hash, use interval/geometry and parent link.

Impact traversal starts at affected result/assets and follows links breadth-first with cycle detection and stable ordering. It separates planned, active, rendered and published uses; records unreachable references; and emits typed actions such as `block_new_use`, `stop_active_composition`, `revalidate`, `rerender`, `review_publication` or `no_action_historical_only`.

The protocol recommends review for publications and tracks owner acknowledgement. It never edits or republishes media.

## 10. Authority, correlation and routing

VAE owns result/production facts and production revocation reasons. Content Harness/composition runtime owns acknowledgement and consumption links. The product owning a changed dependency owns invalidation. Integrity authority is limited to registered reason families. Protocol owns validation, lifecycle/current-use projection, impact receipt and routing.

All notices retain the original correlation where possible and causally reference result/acknowledgement/trigger. Cross-correlation impacts use exact link references. Critical revocations use priority delivery but still pass standard validation and audit.

## 11. Cancellation, supersession and race behavior

Cancellation/supersession committed before result acceptance blocks promotion. Result acceptance committed first yields `RESULT_READY`; acknowledgement evaluates current cancellation/supersession state. A supersession committed while ready moves the old branch to `SUPERSEDED` and rejects later acknowledgement for current use.

Revocation accepted concurrently with acknowledgement is serialized. If acknowledgement commits first, revocation immediately changes current-use state and triggers impact. If revocation commits first, acknowledgement fails `RESULT_REVOKED`. Historical facts remain in either ordering.

## 12. Compatibility, adapters and migration

Negotiated profiles must include result/receipt/geometry/acknowledgement/post-completion versions required by the demand. Adapters may normalize exact geometry representations only with lossless evidence; they cannot synthesize production acceptance or consumption authorization.

Migration from the provisional result removes the conflicting downstream authorization field from the canonical target. If a historical source says `true`, migration requires a separately verifiable Content Harness acknowledgement; without it, the migrated result remains not consumption-authorized.

## 13. Persistence and retention

Results, assets, receipts, acknowledgements, notices, consumption links and impact reports are append-only immutable resources. Acceptance and lifecycle/current-use projection/outbox/audit commit atomically. Assets may live in governed object storage; references/hashes and retention policy remain durable.

Invalidated, revoked, superseded and replaced artifacts remain historically reproducible under policy. Negative evidence is tagged and access-controlled; ordinary reuse queries exclude it by default. Legal hold and security quarantine may restrict access without breaking audit identity.

## 14. Failure, recovery and rollback

Missing/unavailable receipts, stale dependencies, incompatible geometry and invalidated references cause typed acknowledgement rejection without quality-round consumption. A VAE quality dispute routes to production evaluation/repair or amendment, not a second protocol evaluator.

Impact traversal failures retain a pending incident and conservatively block affected unknown scopes. Projection rebuild folds immutable links/notices. Rollback never reauthorizes a revoked result automatically; a new owner fact is required.

## 15. Threat model

Threats include forged production acceptance, VAE self-acknowledgement, stale dependency snapshots, asset reference substitution, suppressed revocation, unauthorized current-use override, replacement confusion and negative-evidence leakage. Controls are split authorities, exact hashes, signed dependency snapshots, current-use guard, priority audited notices, immutable history and access-class filters.

## 16. Observability and SLOs

Project result readiness age, acknowledgement eligibility/check failures, unacknowledged results, current authorization, active invalidations/revocations, impact counts, unresolved published reviews and replacement status. Metrics avoid asset URI labels.

Targets: at least 99% eligible automatic acknowledgements within ten seconds, zero stale/revoked current consumption, p99 critical notice projection at or below ten seconds and 100% notice/audit completeness.

## 17. Test architecture

- Producer tests prove only VAE can emit production acceptance.
- Consumer tests exercise every deterministic acknowledgement check/rejection code.
- Authority tests reject VAE acknowledgement and Content Harness production acceptance.
- Race tests cover result/cancellation, result/supersession, acknowledgement/revocation and replacement acknowledgement.
- Impact graph tests cover cycles, missing links, active/published scopes and conservative failure.
- Retention tests prove historical reproducibility and ordinary-reuse exclusion.
- Format 02 result, acknowledgement and replacement scenarios run end to end.

## 18. Given/When/Then acceptance criteria

1. Given a production-accepted result with current dependencies, when all deterministic checks pass, then acknowledgement authorizes exact assets and lifecycle becomes `COMPLETED`.
2. Given a result without an evaluation receipt, when acknowledged, then it is rejected with `MISSING_PRODUCTION_RECEIPT` without duplicate visual evaluation.
3. Given a VAE-authored downstream authorization field, when the next-major result is validated, then schema/authority validation rejects it.
4. Given a changed composition geometry, when the old result arrives, then acknowledgement rejects it as stale/incompatible.
5. Given a critical revocation, when accepted, then new use is blocked and active/published impacts are projected without deleting history.
6. Given a replacement with different geometry, when proposed, then it remains pending until compatibility checks and acknowledgement pass.
7. Given a revoked asset in the negative-evidence store, when ordinary reuse is queried, then it is excluded while authorized evaluation remains possible.

## 19. Implementation tasks

1. Close the result, acknowledgement and notice schemas and remove the conflicting result field.
2. Define exact result/asset/dependency-snapshot/consumption-link identities.
3. Implement the pure acknowledgement checker interface and stable rejection taxonomy.
4. Define current-use fold and impact traversal interfaces.
5. Add retention/access classifications and negative-evidence filters.
6. Build product adapter contracts for dependency snapshots, receipts and consumption links.
7. Verify Control Tower integration and published-use owner under XRI-014.

## 20. Explicit non-goals

- Re-running VAE visual evaluation in the protocol or Content Harness
- Publication editing/recall execution
- Overwriting or deleting historical results
- VAE regression investigation internals
- Production implementation during Stage 2

## 21. Readiness and blockers

Specification verdict: `CONCERNS`. Authority is now unambiguous, but dependency snapshots, consumption links and Control Tower/publication interfaces require upstream repository contracts before implementation authorization.
