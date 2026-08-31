# CONSTITUTIONAL AUTHORITY: Release / Ship / Outcome Program (`release_ship_outcome_program`)

## 1. Constitutional Mandate & Purpose
This document establishes the constitutional authority for `release_ship_outcome_program` v1.0.0, implementing CAE Phase 4 Mandate M45. It governs the transition from rendered production candidates through final Dual-Axis QA, backend-authoritative operator release authorization, distribution shipment, empirical outcome observation, and selective learning proposal distillation.

## 2. Invariants & Authority Rules
1. **Four Authority Lanes Separation:**
   - `COMMANDER`: Operator release gate approval, shipment authorization, learning proposal ratification, and bounded repair orchestration.
   - `HUNTER`: Empirical real-world outcome metric observation and collection (`ObservedOutcome`).
   - `COMPOSER`: Distribution shipment packaging, endpoint dispatch, and delivery execution (`ShipmentReceipt`).
   - `ANALYST`: Final Dual-Axis QA verification (Semantic + Render QA), EvaluationReceipt compilation, and SelectiveLearningProposal derivation.
   Cross-lane invocations fail closed immediately (`LaneAuthorityViolationError`).

2. **Decoupled Outcome & Anti-Reward Hacking:**
   - Empirical outcome collection strictly validates evidence grounding.
   - High viral engagement without truth is blocked (`EngagementWithoutTruthError`).
   - Misleading context reward hacking is blocked (`MisleadingContextRewardHackError`).
   - Averaged disagreement laundering is blocked (`AveragedDisagreementLaunderingError`).

3. **Failed Ship Never Reports Success:**
   - If physical/distribution delivery fails, the state machine strictly halts and never transitions to `SHIPPED` or reports success.

4. **Anti-Auto-Mutation of Ontology:**
   - Learning proposals are purely advisory. Any attempt to auto-mutate canonical ontology without explicit human Operator ratification raises `OntologyMutationViolationError`.

5. **Permanent Anti-Synthetic Fail-Closed Guard:**
   - Demands or candidates marked synthetic (`is_synthetic=True`) or missing authentic evidence segment quotes fail closed immediately (`SyntheticProductionBlockedError`).
