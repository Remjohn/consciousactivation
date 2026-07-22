# Current-State Reconciliation Requirement

The connected public repository currently exposes an older Builder status (`SRC-CUR-011`) than the operator-reported local terminal state described during this design session. The PRD therefore does not choose either as silently authoritative.

Before implementation:

1. Verify the exact operator-local files under `D:/Work/CONSCIOUS_ACTIVATIONS/01_ATOMIC_HARNESS_BUILDER/docs/implementation/offline-development/`, including the terminal summary, latest model-neutral handoff and OD-AM campaign receipts.
2. Verify the EC-AM evidence-closure files under `D:/Work/CONSCIOUS_ACTIVATIONS/01_ATOMIC_HARNESS_BUILDER/docs/evidence-closure/` and release files under `docs/release/`.
3. Reconcile those bytes into Program Control and the public repository without rewriting historical receipts.
4. Publish one new current status receipt used by all four products.

Until this gate passes, all file mappings in this PRD are architectural and migration-precise, but not an implementation allowlist.
