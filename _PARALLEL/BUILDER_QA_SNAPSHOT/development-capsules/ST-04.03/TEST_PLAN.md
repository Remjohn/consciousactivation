# Test plan

Use deterministic clocks and IDs, the completed ST-04.02 context, the exact hash-pinned phase input, and the in-memory development adapter. Run the new Story suite twice and all 256 predecessor tests.

Required tests cover: successful phase-graph compilation; exact parent and lineage; complete phase fields; canonical topological order; runnable and blocked-state derivation; explicit symmetric parallelism; no default parallelism; missing or unknown module references; missing or duplicate phase identity; self-edge; unresolved dependency; cycle; dependency/parallel conflict; asymmetric parallelism; gate bypass; non-code writer; stale version; input hash drift; payload conflict; injected atomic failure; replay; fresh-context determinism; run replay; upstream invalidation; immutable history; required observations; exact source set; standard-library-only imports; and absence of Context Graph, handoff execution, Workflow IR, Control Tower, external runtime, or production behavior.

Completion requires all Story tests PASS twice, 256/256 predecessor tests PASS, full regression PASS with zero mandatory skips, and exact file-scope validation.
