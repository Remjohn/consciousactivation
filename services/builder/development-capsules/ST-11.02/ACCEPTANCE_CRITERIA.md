# Acceptance criteria

1. Given the exact active ST-11.01 Development Capsule, when deterministic Builder
   code compiles the plan, then one immutable plan and receipt cover FR-156/FR-157.
2. Given the plan increments, when dependency order is validated, then every edge is
   backward, acyclic and references an earlier increment only.
3. Given each increment, then it has one user-observable outcome, one focused
   context, acceptance evidence, tests, observability, rollback and receipt needs.
4. Given a layer-only, forward-dependent, untestable or over-broad increment, then
   compilation fails closed with no partial state.
5. Given readiness remains non-production, then the plan records implementation,
   production and certification authorization as false.
6. Given an altered, stale or invalidated parent capsule, then active-plan access or
   compilation fails closed while historical bytes remain reproducible.
7. Given an identical command, then the original receipt is returned; a conflicting
   payload under the same command identity fails closed.
8. Given an injected commit failure, then no plan, receipt or command record remains.

