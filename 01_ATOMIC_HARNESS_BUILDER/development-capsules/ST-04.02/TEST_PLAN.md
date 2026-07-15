# Test plan

Use deterministic clocks and IDs, the completed ST-04.01 context, the exact hash-pinned module input, and the in-memory development adapter. Run the new Story suite twice and all 221 predecessor tests.

Required tests cover: successful two-module compilation; exact 3/3 capability partition; canonical ordering and content identity; parent graph and authority lineage; responsibilities and boundary rationales; public input/output contracts; invariants; exclusions; dependency resolution; failure ownership and modes; complete test seams; missing/extra/duplicate capability assignments; horizontal technology-layer module rejection; mixed owner-kind rejection; hidden side-effect rejection; missing seam fields; unresolved dependency; cycle and self-edge rejection; non-code writer rejection; stale version; payload conflict; injected atomic failure; replay; fresh-context determinism; run state reproduction; upstream invalidation; immutable history; required observations; exact source set; standard-library-only imports; and absence of Phase Graph, Context Graph, Workflow IR, Control Tower, external-runtime, or production behavior.

Completion requires all Story tests PASS twice, 221/221 predecessor tests PASS, full regression PASS with zero mandatory skips, and exact file-scope validation.
