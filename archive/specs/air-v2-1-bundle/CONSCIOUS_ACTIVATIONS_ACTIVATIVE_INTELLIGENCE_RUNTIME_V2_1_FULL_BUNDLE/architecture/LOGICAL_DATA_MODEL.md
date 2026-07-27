# Logical Data Model

The physical database is selected during architecture authorization. The logical model is fixed by product contracts.

| Logical store | Contents | Mutation law |
|---|---|---|
| semantic object store | immutable object payloads and canonical hashes | append only; successor versions supersede |
| lifecycle event store | transitions, commands, blockers, invalidation, replay | atomic event + receipt |
| dependency graph | typed object and cross-product edges | versioned edge additions and supersession |
| source evidence index | source packages, spans, keyframes, observations, tags | exact source-version binding |
| Primitive registry projection | exact YAML identity, plane, family, conditions, conflicts | imported from governed source snapshot; definitions are not authored here |
| archetype evidence index | historical prompts, current archetype programs, rejection evidence | historical evidence separated from current authority |
| human resolution ledger | before/after state, request, change program, evaluation, scope | immutable episode; promotion is separate |
| evaluation receipt store | deterministic, semantic, Primitive, transfer, visual, model, and handoff verdicts | producer cannot overwrite evaluator record |
| model claim registry | Programmed Model artifacts, claims, harness bindings, shadow and promotion evidence | claim-specific lifecycle and rollback |
| projection store | Studio and operations read models | reconstructable; never canonical |
