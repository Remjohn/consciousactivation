# Phase 6 Build Order

## Wave 0 — Audit
1. Inventory existing primitive registries.
2. Inventory existing SDA packets.
3. Inventory existing coalition code.
4. Inventory receipts and validator code.
5. Identify duplicate candidate / edge objects.

## Wave 1 — Canonical contracts
6. Freeze PrimitiveDefinition adapter contract.
7. Freeze Candidate / Coalition / Edge schemas.
8. Freeze compatibility and geometry contracts.
9. Freeze error taxonomy.

## Wave 2 — Retrieval surface
10. Implement controlled SQL views/functions.
11. Implement vector retrieval for semantic neighborhoods.
12. Implement crosswalk retrieval.

## Wave 3 — Candidate engine
13. Build candidate generator.
14. Build eligibility gate.
15. Build survival scoring.
16. Build rejection receipts.

## Wave 4 — Coalition engine
17. Build compatibility matrix.
18. Build sparse weighting.
19. Build coalition validator.
20. Build coalition receipts.

## Wave 5 — Edge engine
21. Build Edge Product derivation.
22. Build distinctiveness retrieval.
23. Build directional/hard-negative evaluation.
24. Build Edge Product receipt.

## Wave 6 — Anti-centroid and repair
25. Deploy SemanticCentroidPatrol.
26. Implement typed repair routing.
27. Prevent silent flattening.

## Wave 7 — Benchmarking
28. Build coalition/edge benchmark memory.
29. Replay known examples.
30. Compare against baseline / generic generation.

## Wave 8 — Integration
31. Emit Phase 6 packet to Phase 7.
32. End-to-end trace from Guest evidence to Edge Product.
