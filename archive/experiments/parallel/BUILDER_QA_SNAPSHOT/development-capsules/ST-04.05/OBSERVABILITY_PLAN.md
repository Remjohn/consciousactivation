# Observability plan

Emit deterministic observations for context compilation accepted/rejected, budget validation, manifest completion, replay returned, descendant invalidation, active consumption blocked, and injected atomic failure. Every observation must include:

- run, Story, command, correlation, causation, authority, version, and outcome;
- Phase, Context, Handoff, reference/loading, budget, and manifest identities and hashes;
- included, excluded, summarized, retrieved, compressed, required, optional, and overflow counts;
- exact upstream lineage, provenance, receipt identity, failure code, and affected descendants.

No resource payload, conversation history, secret, machine path, timestamp, random identifier, or external-product data may enter identity-bearing evidence. Replay evidence cannot duplicate committed events.
