# Implementation scope

Implement one category-neutral vertical slice that reads the active immutable Harness IR capability list and the exact capsule ownership input, proves set equality, validates every explicit ownership decision, emits a canonical content-addressed graph, attaches its reference to the GENESIS run, and stores a PASS receipt atomically.

The graph must support the complete owner vocabulary (`CODE`, `AGENT`, `HUMAN`, `EXTERNAL`, `HYBRID`) while the authorized synthetic fixture assigns only evidence-backed Builder-code owners. No owner may be inferred from a universal default. Agent/external decisions require attributable authority and evidence; hybrid decisions require ordered participants and an explicit handoff responsibility. Unsupported decisions fail closed.

Additive changes are required in run replay/state, ports, the in-memory development adapter, and authorized descendant invalidation. Two new source modules, exact-source-set test updates, Story tests, and completion evidence are required. No fixture outside this capsule, registry, schema, dependency, API, UI, database, workflow, module, phase, context, handoff implementation, skill resolution, or task execution is authorized.
