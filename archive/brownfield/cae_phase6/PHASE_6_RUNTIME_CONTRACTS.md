# Phase 6 Runtime Contracts

## Input contract

`SemanticEvidencePacket` MUST contain:
- source evidence IDs;
- authentication status;
- relevant Guest/Audience references;
- evidence scope;
- provenance;
- current semantic state snapshot.

## Candidate contract

`PrimitiveCandidate` MUST contain:
- candidate_id
- primitive_id
- evidence_ids
- operation
- geometry
- confidence
- survival status
- validator state

## Coalition contract

`CoalitionSignature` MUST contain:
- coalition_id
- selected candidate IDs
- primitive IDs
- weights
- ordering where relevant
- compatibility result
- routeability
- evidence lineage
- validation state

## Edge contract

`EdgeProduct` MUST contain:
- edge_id
- edge_type
- pressure_boundary
- invariant lineage
- coalition lineage
- audience/Guest context
- distinctiveness evidence
- routeability
- validation state.

## Runtime handoff

Phase 6 MUST hand downstream:
- selected Edge Product;
- coalition signature;
- relevant invariant/geometry packets;
- non-negotiable semantic invariants;
- evidence lineage;
- anti-centroid patrol result;
- known hard-negative risks.
