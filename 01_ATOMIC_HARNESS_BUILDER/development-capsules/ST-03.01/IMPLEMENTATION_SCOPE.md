# Implementation Scope

Implement a category-neutral decision-definition and question-package domain plus
one code-owned command. It must validate the active saturated evidence, frozen
boundary and explicitly unratified Draft Harness Model; validate all decision node
fields and affected paths; compute readiness from exact evidence and completed
dependencies; select at most one ready node deterministically; and compile a complete
recommendation with facts, inferences, alternatives, trade-offs and consequences.

The output is an immutable question package and receipt. It cannot contain a human
answer, final value, ratification, Harness IR change or implied approval. Identical
inputs replay; changed definitions or evidence produce a new identity. Invalidation
is non-destructive and preserves historical reproduction.
