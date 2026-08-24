# Phase 6 Primitive Registry Integration

## Registry doctrine

The existing Primitive Registry remains canonical.

Phase 6 does not rewrite primitive definitions at runtime.

Each primitive definition should expose, at minimum:
- primitive_id
- name
- family
- canonical definition
- mechanistic analysis
- local geometry
- universal effect projection
- evidence provenance
- activation conditions
- anti-patterns
- coalition partners
- workflow integration
- version.

## Candidate lookup

Agents should query by:
- semantic relevance;
- family;
- invariant sensitivity;
- context;
- admissible range;
- routeability.

## Candidate instantiation

A candidate references:
```yaml
primitive_id:
evidence_ids:
activation_conditions:
proposed_operation:
expected_effect:
geometry:
confidence:
```

## Registry evolution

If Phase 6 repeatedly generates a semantic operation that cannot be represented by an existing primitive, that is a **registry gap**, not permission to invent a permanent primitive inline.

Registry-gap flow:

```text
candidate gap
→ evidence accumulation
→ repeated utility
→ proposed primitive definition
→ dual-source verification
→ human architecture review
→ canonical registry version
→ future candidate eligibility
```

This keeps the primitive canon controlled while allowing the system to evolve.
