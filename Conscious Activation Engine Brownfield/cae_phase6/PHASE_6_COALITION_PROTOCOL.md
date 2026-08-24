# Phase 6 Coalition Formation Protocol

## Coalition definition

A coalition is a sparse, weighted set of surviving PrimitiveCandidates whose combined geometry is intended to produce a specific semantic force object.

## Mandatory passes

### 1. Eligibility
Only surviving candidates may enter coalition selection.

### 2. Compatibility
Evaluate:
- synergy;
- antagonism;
- cancellation;
- redundancy;
- family saturation;
- directional conflict.

### 3. Weighting
Every selected primitive receives an explicit contribution weight.

Weights must sum according to the canonical coalition policy in force.

### 4. Sequencing
Where order matters, encode sequence explicitly rather than relying on prose.

### 5. Routeability
The coalition must map to at least one authorized downstream semantic route.

### 6. Sparsity
The active set should normally remain small. Add a primitive only when it contributes a distinct function that cannot be absorbed by another active member.

## Coalition states

```text
candidate
→ assembled
→ validated
→ executable
→ executed
→ benchmarked
```

Failure states:

```text
incompatible
overloaded
redundant
unrouteable
directionally_invalid
fatal
```

## Coalition receipt minimum

```yaml
coalition_id:
candidate_ids:
primitive_weights:
compatibility_verdict:
route:
evidence_lineage:
invariant_lineage:
edge_hypothesis:
fatality_flags:
validator_status:
```
