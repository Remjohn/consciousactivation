# Implementation scope

Implement a category-neutral deterministic evidence-index compiler that consumes the
active `SourceLock`. For each ordered descriptor it emits exactly one immutable
`Specimen`, an exact provenance record and governed relationships to the source and
lock. The resulting index supports deterministic queries by specimen identity,
source identity, role, governed status and knowledge status.

The command validates the active run and Source Lock, authorizes the actor for the
new Builder-owned indexing action, builds and validates the complete index, attaches
its identity to the run and commits the index, receipt, run event, command record and
observation intents atomically. Duplicate identical commands return the original
receipt; conflicting payloads fail closed.

An index is active only while its exact Source Lock is active. Explicit invalidation
preserves the historical index and creates an immutable invalidation record. No
source bytes are mutated and no external system is invoked.

Additive code changes are required in two new source modules plus Run, authority,
ports and the current in-memory repository. Exact-source architecture tests receive
only the two authorized source paths. No registry, shared schema or dependency change
is allowed.
