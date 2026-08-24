# Phase 6 Brownfield Integration

## Existing sources to inspect first

### Primitive layer
- Meaning Primitive Registry
- Experience Primitive Registry
- Primitive Family Classification
- Primitive Crosswalk
- Primitive Packets and Registry specification
- Primitive Conscious Orchestration architecture

### Semantic layer
- SDA ontology registry
- SDA artifact taxonomy
- SDA runtime packet specification
- Directional Integrity
- Hard Negative corpus

### Tension layer
- Matrix of Edging
- Perceptual Primitives Architecture

### CCF
- coalition signatures
- candidate survival
- routeability
- receipts
- anti-centroid validators.

## Brownfield rule

Do not create a parallel Primitive Registry.

Do not create a second Coalition system if a current implementation exists.

Do not duplicate SDA ontology.

Phase 6 should:
1. discover existing modules;
2. map them to the Phase 6 conceptual objects;
3. reuse stable code;
4. wrap legacy structures with adapters where necessary;
5. mark missing relations/state/receipt behavior as brownfield gaps;
6. migrate incrementally.

## Required audit

```text
object already in code
object only in docs
duplicate object
missing relation
missing state
missing validator
missing receipt
missing runtime consumer
```

Each must be logged before implementation claims are made.
