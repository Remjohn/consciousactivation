# Security and authority boundaries

Only an actor registered as Builder `CODE` with `INDEX_EVIDENCE` authority for the run
may commit an index. Human, agent, external and evaluator identities cannot impersonate
the deterministic indexer. No actor may mutate Source Lock descriptors or historical
indexes.

The index stores governed metadata and hashes, not source bytes, secrets or local
absolute paths. It receives no network, provider, external repository, database or
runtime capability. It neither infers semantic meaning nor promotes evidence
authority.

Constitution V1.1, Builder PRD V1.2 and the pinned Source Profile remain controlling.
The local contracts reference those sources and do not fork them. `NOT_APPLICABLE`
is an explicit knowledge status only where the contract permits it; it cannot replace
missing required evidence.

VAE and Delegation behavior and shared contracts remain externally owned. Format 02,
conversational Human Reaction material and production profiles require their own open
evidence and policy gates.
