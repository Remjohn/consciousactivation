# Phase 2 Operator Checklist

Before Phase 2: M12 accepted and baseline commit pinned.

During Phase 2 verify:
- Program discovery is a projection, not a second authority.
- Builder export feeds the existing binding compiler.
- Pi state never overrides CAE state.
- State transition proof exists for every runtime boundary.
- Agents receive explicit lane/capability projections.
- Sub-agents are isolated and bounded.
- Skills remain passive and flat.
- Hooks enforce deterministic guarantees.
- Operator gates are backend-authoritative.
- Receipts match actual state/artifact effects.
- Replay/duplicate effects are reconciled.
- runtime trace is causally coherent.

At M24: require all evidence, exact commit SHAs and CURRENT.md synchronization before Phase 3.
