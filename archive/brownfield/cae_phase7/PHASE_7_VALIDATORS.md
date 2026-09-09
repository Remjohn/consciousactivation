# Phase 7 Validators

## Required validators

### ArchetypeEligibilityValidator
Confirms the selected container can carry the Edge without semantic distortion.

### StructuralInvariantValidator
Confirms required archetype structure is bound and unbroken.

### SFLRegistryValidator
Confirms every activated function is canonical, versioned, and retrievable.

### SFLAlignmentValidator
Checks influence/alignment policies without inventing generic safety constraints.

### DepthProfileValidator
Checks admissible profile use and range.

### EdgePreservationValidator
Confirms the SemanticProgram still identifies the same Edge Product and invariant lineage.

### AntiCentroidValidator
Checks for mean reversion / needless softening.

### DirectiveValidator
Ensures JIT directives are typed, scoped, prioritized, and traceable.

### SemanticProgramValidator
Checks program completeness and phase boundary compliance.

### DownstreamContractValidator
Ensures Phase 8 receives enough structure without receiving forbidden implementation details.

## Validation rule

Every validator returns:

```yaml
status: pass | fail | warn | escalate
code:
message:
evidence:
repair_route:
severity:
```

No validator may return only free-form prose.
