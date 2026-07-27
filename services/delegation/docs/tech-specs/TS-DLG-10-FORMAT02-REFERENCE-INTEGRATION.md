---
title: TS-DLG-10 Format 02 Reference Integration
product: CMF Content Harness Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: stage2_draft_for_review
created: 2026-07-14
---

# TS-DLG-10 Format 02 Reference Integration

## 1. Identity and requirement coverage

- Primary release slice: Format 02 Minimal Coach Theatre
- Owned FRs: FR-120, FR-126
- Verification overlay: all D001 through D016, all 128 FRs and all 60 NFRs as applicable to the scenario portfolio
- Decision: D016 with D015 conformance support
- Journeys: UJ-01 through UJ-14
- Depends on: TS-DLG-01 through TS-DLG-09

## 2. Sources read

Normative inputs are the complete `reference-slice/FORMAT02_MINIMAL_COACH_THEATRE/` package, all ten fixtures, `conformance/format02-end-to-end/EXPECTED_SCENARIOS.yaml`, Content Harness/VAE/protocol compatibility manifests, negotiated profile, expected authority/compatibility/Control Tower files, the example Visual Asset Demand and all preceding technical specifications.

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

## 3. Reference purpose and scope

Format 02 is the first mandatory cross-product certification profile. It proves a 2D character-animation Content Harness can delegate assets for Minimal Coach Theatre while preserving Content Harness meaning/composition authority, VAE production authority and deterministic protocol governance.

The reference demand uses a 1080x1920 9:16 canvas, a skeptical-listener reaction role, recognition-before-explanation Activative function, foreground-right region, reserved caption region, left gaze, character/environment continuity, wrong-reading locks and certified evaluation gates. These are owner-authored fixture facts, not protocol defaults.

Certification covers the shared boundary and downstream consumption representation. It does not certify general 2D animation, other formats, real customer content, all VAE models/workflows or Remotion publication quality.

## 4. Required product and environment bindings

Before execution, the suite pins signed immutable releases for:

- Content Harness `HARNESS-F02-MCT-001` and its producer/consumer adapter;
- Visual Asset Editor principal/product ID and its adapter;
- Delegation Protocol contract/runtime/conformance package;
- authorized composition/Remotion fixture consumer;
- principal/key registry, object store, audit ledger, event transport and Control Tower adapter;
- canonical schemas/registry, policy/lifecycle/failure/compatibility versions;
- fixture/evidence bundle digest and deterministic clock/ID seed.

The current local manifests are PRD fixtures, unsigned and not bound to accessible builds. `VAE-PROD` identity must be normalized and every manifest updated for the split validation/admission receipts and corrected result authority. XRI-002, XRI-013 through XRI-017 remain blocking until real bindings are supplied.

## 5. Negotiated Format 02 profile

The executable profile must pin protocol/message versions, schema hashes, authority model, lifecycle machine, failure taxonomy, signing suite, adapters/migrations and required features:

- typed composition intent and exact geometry/mask/timing references;
- demand supersession/selective invalidation;
- Delegation Sets and set-level evaluation;
- budget escalation and immutable receipts;
- syntax/evaluation/production receipts;
- result acknowledgement and post-completion notices;
- idempotency/replay/audit/Control Tower behavior.

Missing any mandatory feature is `INCOMPATIBLE`. Unsupported optional telemetry may use owner-declared degradation. The profile remains pinned for each scenario.

## 6. Field authority and principal permissions

The fixture Content Harness owns semantic intent, Activative function, sequence/asset role, composition intent, identity/continuity, wrong-reading locks, delivery, budget, cancellation, supersession, amendment response and acknowledgement. VAE owns admission, production plan/execution/evaluation/repair, assets, production acceptance and production evidence. Protocol owns validation, compatibility, lifecycle, idempotency/replay, routing, audit and projection. Composition runtime owns only exact delegated acknowledgement/consumption facts.

Every scenario includes at least one authority assertion; SCN-08 explicitly attempts VAE mutation of a demand-owned path and must start no production.

## 7. Scenario portfolio

| Scenario | Executable flow and mandatory proof |
|---|---|
| SCN-01 Successful single character asset | Signed demand/submission, protocol validation, VAE admission/progress/result, deterministic acknowledgement and `DRAFT -> SUBMITTED -> ACCEPTED -> IN_PROGRESS -> RESULT_READY -> COMPLETED`; exact demand/result hashes, all receipts and Control Tower projection match. |
| SCN-02 Atomic multi-asset Delegation Set | Character, environment and prop demands retain independent correlations; atomic policy withholds release until required members, set evaluation and assembled acknowledgement pass; no member lineage is merged. |
| SCN-03 In-flight demand supersession | Owner changes declared composition field(s), protocol recomputes diff, old branch becomes `SUPERSEDED`, VAE returns selective reuse evidence and late old result cannot satisfy the new demand. |
| SCN-04 Budget escalation and approval | VAE reaches commitment boundary, no work breaches hard ceiling, `IN_PROGRESS -> COST_APPROVAL_REQUIRED`, owner approves a new immutable authorization and execution resumes with final reconciliation. |
| SCN-05 Constraint conflict and amendment | VAE emits evidence/non-binding options, demand remains unchanged, owner accepts one option through a new demand/supersession and impact receipt; constitutional/semantic auto-approval is rejected. |
| SCN-06 Safe cancellation | Owner cancellation blocks new work, VAE reaches safe checkpoint, retains classified evidence, emits compute/disposition receipt and late output is not consumption-authorized. |
| SCN-07 Result invalidation and replacement | Completed result is invalidated without deletion, consumption impacts are enumerated, replacement passes current geometry/context checks and separate acknowledgement before `REPLACED`. |
| SCN-08 Authority violation rejection | VAE-authored demand mutation is rejected with authority/security receipt, lifecycle does not progress to production and Control Tower identifies the denied paths/principal. |
| SCN-09 Compatibility migration | Signed manifests produce migration-required/compatible verdict as fixture dictates, immutable deterministic migration preserves all mandatory fields and pins the resulting profile before submission. |
| SCN-10 Replay and out-of-order resilience | Identical duplicate returns original receipt/no duplicate execution; altered/replayed signed message is rejected; progress before admission cannot create an illegal transition; reconstruction/audit remain complete. |

Each current fixture's generic assertions are expanded to exact messages, principals, hashes, states, audit sequences, outbox deliveries, product execution counts, projections and prohibited effects.

## 8. Lifecycle, correlation and event routing

SCN-01 uses the split `submission-validation-receipt` and VAE `admission-receipt`; the old conditional receipt is not used in the canonical run. Every scenario uses deterministic correlation/causation IDs and virtual time. Delegation Set members retain member correlations linked to the set correlation.

All events pass the same inbound validation and transactional outbox. Direct Content Harness-to-VAE or VAE-to-Remotion production calls are test failures. Product internal events are translated to registered public facts; internal VAE node names never become lifecycle states.

## 9. Idempotency, replay and race coverage

SCN-10 is the primary duplicate/replay case, but every command is delivered at least twice in one suite variant to assert idempotent effects. Security variants reuse nonce, message ID and idempotency key with changed bytes. Race variants cover cancellation/result, supersession/node completion, acknowledgement/revocation and escalation/cancellation using both commit orders.

Expected state follows committed audit sequence, not fixture file order or sender time.

## 10. Compatibility, adapters and migration

SCN-09 includes direct compatibility, one lossless adapter or migration-required path, and negative vectors dropping wrong-reading/continuity fields. Output hashes must repeat deterministically. All other scenarios execute under the negotiated profile and assert no silent upgrades.

Contract rollback is tested by retaining an active scenario on its pinned profile while a new correlation selects a prior compatible package. Historical schema/receipt resolution must continue.

## 11. Cancellation, supersession and post-completion behavior

SCN-03 and SCN-06 prove old/late output remains historical but not current. SCN-07 proves invalidation/revocation/replacement do not overwrite assets or publication records. SCN-02 adds member-scoped cancellation/supersession and exact set invalidation fanout.

Result acknowledgement always checks current Format 02 composition/Visual Syntax geometry and dependencies without re-running VAE visual evaluation.

## 12. Persistence and transaction boundaries

The executable environment supplies durable message/lifecycle/idempotency/replay/audit/outbox state, immutable fixture/resource storage and rebuildable projections. Named failpoints interrupt before/after each acceptance commit. The suite asserts no partial acceptance and exact recovery after restart.

VAE execution persistence remains VAE-owned; the adapter exposes only execution count, exact checkpoint references and public receipts needed for assertions.

## 13. Failure, recovery and security behavior

Every scenario has negative variants mapped to canonical failure families/codes, owner, retry, quality-round and invalidation effects. Infrastructure failures do not consume quality rounds. Authority/integrity/replay failures do not ordinary-retry or start production.

Security vectors include forged principal, payload tamper, expired signature, cross-tenant reference, malicious extension and audit interruption. Fixture keys are non-production and deterministic only in isolated conformance environments.

## 14. Audit, Control Tower and SLO evidence

For every accepted/rejected action, assert chained receipt, source message, validation results and transition/no-transition. The expected Control Tower projection includes current state, exact demand/execution/profile, authority owners, budget/timing, latest event, exceptions, acknowledgement, current-use state and audit sequence.

The suite measures submission, duplicate resolution, projection freshness, acknowledgement, cancellation and critical notice SLIs. Production certification requires all mandatory semantic assertions plus declared SLO thresholds; latency cannot waive quality/authority failures.

## 15. Threat model

Format-specific threats include a VAE interpreting notes as authority, wrong-reading locks dropped by migration, stale character/environment continuity, geometry mismatch in Remotion, atomic set bypass, revoked pose reuse and direct production invocation. Controls are closed schemas, exact owner metadata, compatibility fixtures, current dependency snapshots, set release guard and current-use filtering.

## 16. Test architecture and evidence

TS-DLG-09 runner executes all scenarios against in-memory reference and pinned product adapters. Each scenario has setup, deterministic fixture builder, actions/fault schedule, expected messages/states/receipts/projections, prohibited effects and teardown.

Certification evidence is one signed bundle containing product/build/contract digests, scenario results, SLI report, audit-chain/checkpoint roots, sanitized traces, known limitations and expiry. Any skipped mandatory assertion is a failed certification, not a warning.

## 17. Given/When/Then acceptance criteria

1. Given all ten PRD fixtures but no real signed product adapters, when readiness is evaluated, then Format 02 remains not certified.
2. Given the single-asset demand, when the complete flow runs, then exact authority, six lifecycle states, one VAE execution, acknowledgement and audit/projection evidence pass.
3. Given an atomic set with one missing required member, when release is attempted, then no set/member downstream release occurs through the atomic policy.
4. Given supersession or cancellation before late output, when that output arrives, then it is retained but cannot be acknowledged current.
5. Given a migration that drops a wrong-reading lock, when SCN-09 runs, then compatibility fails and no submission is admitted.
6. Given duplicate and replay variants, when SCN-10 runs, then duplicate effect count is one and hostile replay effect count is zero.
7. Given a replacement with altered BBOX, when SCN-07 runs, then compatibility/acknowledgement is required before replacement current use.
8. Given a complete passing run, when the evidence bundle is verified, then all exact release digests, limitations and audit roots are present.

## 18. Implementation tasks

1. Upgrade all ten fixtures from generic examples to complete canonical message sequences and negative variants.
2. Replace conditional submission/result authority fields with TS-DLG-02/06 contracts.
3. Pin accessible Content Harness, VAE, composition runtime, Control Tower and protocol builds.
4. Sign/close manifests and negotiated profiles with exact schema/package hashes.
5. Implement SUT adapters, fault schedules, projection/audit assertions and evidence bundling under TS-DLG-09.
6. Add real Format 02 visual syntax, character/environment/geometry evidence references with governed test assets.
7. Run all scenarios and record certification limitations before requesting authorization.

## 19. Explicit non-goals

- General certification for all four categories or non-Format 02 profiles
- Evaluation of visual aesthetics by the protocol suite
- Real production credentials or customer media
- Publication/recall execution
- Production implementation during Stage 2

## 20. Readiness and blockers

Specification verdict: `CONCERNS`. The complete scenario contract is defined, but current fixtures remain declarative and product/build bindings are absent. Format 02 certification and implementation authorization remain blocked.

## 21. V1.1 constitutional alignment amendment

Format 02 pins envelope protocol `1.0`, Visual Asset Demand `1.1`, and package
`1.1.0-rc.1`. SCN-08 proves protected semantic authority rejection; SCN-09
proves traceable owner-evidenced migration and behavioral compatibility;
SCN-10 proves exact Activative Intelligence Pack, Reaction Receipt, and
Expression Moment lineage across retry/replay. These assertions extend the ten
existing scenarios without changing their lifecycle or effect-count baselines.
