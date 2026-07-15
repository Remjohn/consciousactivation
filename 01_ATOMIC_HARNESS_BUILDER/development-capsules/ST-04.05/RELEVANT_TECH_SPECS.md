# Governing technical specifications

## Primary: TS-07

`docs/tech-specs/specs/TS-07-OWNERSHIP-PHASE-CONTEXT-CONTRACT-REFERENCE-REPAIR-GRAPHS.md`

ST-04.05 implements only the versioned Reference Graph, Loading Graph, minimum-complete phase context, budget policy, overflow-blocking, influence-boundary, and complete context-manifest slice. Required context is never silently truncated; must-not-influence references never appear in active manifests.

## Boundary references

- `TS-00`: constitutional anti-goals AG-012 and AG-013 remain fail-closed.
- `TS-08`: the empty registry is an already governed input; no skill discovery or registry implementation is owned here.
- `TS-09`: progressive disclosure and budget semantics are contract references only; no JIT Execution Capsule is compiled.
- `TS-12`: context observations remain projectable; no Control Tower behavior is implemented.
- `TS-14`: deterministic control-plane responsibility is preserved; no Workflow IR or execution is implemented.

TS-01 and TS-06 continue to govern run authority, immutable identity, atomic commits, replay, and invalidation through predecessor contracts. No model, retrieval provider, external target, or runtime invocation is authorized.
