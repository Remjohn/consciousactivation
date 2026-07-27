# Test plan

Use deterministic clocks and IDs, the completed ST-03.05 context, exact capsule ownership input, and the in-memory development adapter. Run the new suite twice and all 186 predecessor tests.

Required tests cover: successful 3/3 inventory and graph/receipt; exact parent and authority lineage; canonical ordering and content identity; every owner kind contract; explicit code ownership; reliability and cost evidence; missing/extra/duplicate/renamed capabilities; implicit default rejection; unjustified agent/external ownership; hybrid without ordered participants or handoff; empty-registry policy separation; non-code writer rejection; stale version; payload conflict; injected atomic failure; replay; run state reproduction; upstream invalidation; immutable history; required observations; exact source set; standard-library-only imports; and absence of module, phase, context, handoff, skill-resolution, Workflow IR, external-runtime, or production behavior.

Completion requires all Story tests PASS twice, 186/186 predecessor tests PASS, full regression PASS with zero mandatory skips, and exact file-scope validation.
