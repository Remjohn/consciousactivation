# Relevant technical specifications

- `TS-03` governs the evidence-first boundary and forbids invented ownership derived from absent evidence.
- `TS-07` is primary: compile explicit capability ownership and reject unowned graph nodes, hidden authority, and invalid graph identities.
- `TS-08` distinguishes capability ownership from later skill selection; this Story may cite the governed empty registry but cannot resolve or package skills.
- `TS-09` preserves later JIT-capsule ownership; no JIT behavior is implemented here.
- `TS-14` supplies replay, idempotency, atomic commit, invalidation, and observation requirements without authorizing workflow execution.

Implementation owner: TS-07 Architecture Graphs owner. Component boundary: one immutable capability-ownership graph attached to the active synthetic run after ST-03.05 validation.
