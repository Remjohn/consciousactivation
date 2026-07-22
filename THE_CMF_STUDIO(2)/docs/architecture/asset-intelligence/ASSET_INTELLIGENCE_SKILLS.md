# Shared Asset Intelligence Skills V1

Asset Intelligence skills are shared skills, not SuperVisual-only skills.

Location:

```text
registries/canonical/skills/shared/asset_intelligence/
```

## V1 skill set

```text
asset.ingest
asset.fingerprint
asset.rights_provenance.check
asset.classify
asset.semantic_profile.compile
asset.primitive_affinity.score
asset.intrinsic_eval.run
asset.contextual_eval.run
asset.retrieve
asset.requirement_match.score
asset.reference_board.compile
asset.variant.materialize
asset.usage.record
asset.performance.update
asset.fatigue.compute
asset.winner.promote
```

## Runtime policy

Pydantic is mandatory for all contract objects.

DSPy may be used for:

```text
classification
semantic profile compilation
primitive affinity reasoning
contextual fit scoring
reference board rationale
gap explanation
winner pattern summary
operator-friendly asset explanation
```

DSPy must not decide alone:

```text
rights clearance
direct-use permission
blocking status
hash/fingerprint
provider job preconditions
asset status transitions
approval
deletion
```

Those must be deterministic and/or operator-approved.
