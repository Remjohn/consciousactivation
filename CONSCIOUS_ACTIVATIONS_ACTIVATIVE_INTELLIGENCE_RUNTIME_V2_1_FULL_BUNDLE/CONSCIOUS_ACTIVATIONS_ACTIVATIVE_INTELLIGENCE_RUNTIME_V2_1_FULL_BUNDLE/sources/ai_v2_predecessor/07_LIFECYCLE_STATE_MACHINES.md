# Lifecycle State Machines

## Master lifecycle

```text
context_locked
→ hypotheses_compiled
→ planned
→ armed
→ live
→ observed
→ resolved
→ source_packaged
→ transferred
→ produced
→ published
→ evaluated
→ learned
→ superseded
```

Cancellation may occur at governed pre-terminal states.

## Tag epistemic lifecycle

```text
planned
observed / inferred
operator_confirmed
rejected or superseded
```

Planned and observed are not necessarily sequential; they are different evidence origins.

## Expression Moment lifecycle

```text
proposed
→ validated
→ approved
or
→ borderline
or
→ rejected
→ superseded when later resolution changes the route
```

## Steering Recipe lifecycle

```text
captured
→ candidate
→ locally_useful
→ repeated_evidence
→ promoted
→ deprecated / superseded
```

## Relationship lifecycle

```text
unobserved
→ observed
→ publicly_recognized
→ replied
→ idea_elevated
→ micro_committed
→ reelcast_proposed
→ scheduled
→ recorded
→ asset_delivered
→ offer_revealed
→ client
```

## Failure and repair lifecycle

```text
failure_detected
→ attributed
→ repair_programmed
→ descendants_invalidated
→ local_rerun
→ independent_re_evaluation
→ accepted / concerns / escalated
```
