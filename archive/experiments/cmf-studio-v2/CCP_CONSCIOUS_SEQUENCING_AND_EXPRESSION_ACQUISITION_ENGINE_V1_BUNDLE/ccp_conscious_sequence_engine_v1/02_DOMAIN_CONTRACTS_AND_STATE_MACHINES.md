# Domain Contracts and State Machines

## 1. Canonical contracts

### InterviewBriefV2
Freezes the approved pre-interview procurement plan.

### SequenceHypothesis
Represents a provisional asset recipe and its required ingredients.

### ExpressionAcquisitionPlan
Aggregates and deduplicates all requirements across sequence hypotheses.

### InterviewAssetContractV2
Defines one conversational acquisition instrument and its routing intent.

### LiveIngredientCoverageState
Tracks planned ingredient coverage during the session.

### ExpressionIngredientInventory
Stores source-grounded, scored, reusable ingredients after the session.

### ContentSequenceProgram
Defines the final viewer-facing sequence for one asset.

### PackageSequenceProgram
Defines the relationship-level sequence of several assets.

### SequenceEvaluationReceipt
Records stage scores, doctrine checks, source grounding, and approval.

---

## 2. State machines

### Interview Brief

```text
draft
→ research_complete
→ sequence_hypotheses_compiled
→ acquisition_plan_ready
→ operator_review
→ approved
→ active_session
→ superseded
```

### Ingredient requirement

```text
planned
→ targeted
→ partial
→ captured
→ quality_passed
```

Alternative paths:

```text
planned → substituted
planned → missing → pickup_requested → captured
planned → waived
```

### Expression ingredient

```text
extracted
→ auto_evaluated
→ human_reviewed
→ approved
→ available_for_compilation
```

Alternative:

```text
extracted → rejected
extracted → needs_repair → repaired → reviewed
```

### Content Sequence Program

```text
draft
→ source_validated
→ doctrine_validated
→ format_adapted
→ operator_review
→ approved
→ frozen
→ rendered
→ evaluated
→ published
```

### Package Sequence Program

```text
draft
→ asset_candidates_bound
→ diversity_evaluated
→ schedule_proposed
→ operator_approved
→ scheduled
→ active
→ completed
→ learned
```

---

## 3. Invariants

1. Every required human-expression beat references at least one approved `ExpressionIngredient`.
2. Every open loop has a closure or an explicit `discussion_open` policy.
3. Every sequence program references immutable Brand Context and doctrine versions.
4. A live cue may not be emitted when the suppression policy is active.
5. Missing ingredients cannot be synthesized as guest speech.
6. Package-level expected future value is evaluated across at least two assets.
7. Composition and rendering may not change semantic beat order without creating a new sequence-program version.
8. Operator changes are typed commands and appear in the receipt chain.

---

## 4. Event model

Core events:

```text
InterviewBriefApproved
SequenceHypothesisCreated
IngredientRequirementAdded
InterviewAssetContractApproved
LiveIngredientCaptured
LiveCueSuppressed
ExpressionIngredientExtracted
ExpressionIngredientApproved
IngredientGapDetected
PickupRequested
ContentSequenceProgramCompiled
SequenceProgramApproved
PackageSequenceScheduled
SequenceEvaluationCompleted
```

Events should use an outbox pattern and carry organization, brand, session, user, and correlation IDs.
