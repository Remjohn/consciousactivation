# Observability plan

Emit deterministic observations for compilation accepted/rejected, replay returned, handoff descendant invalidated, active consumption blocked, and injected atomic failure. Every observation must include:

- `run_id`, `story_id`, command and mode;
- Phase Graph, Context Graph and handoff graph identities and hashes;
- producer phase, consumer phases, context and contract versions;
- authoritative field owners and authority identity;
- upstream lineage and provenance identity;
- outcome, failure code and affected descendant identities;
- deterministic receipt identity and run state hash.

No raw source payload, secret, machine path, clock time, random identifier or external-product data may enter identity-bearing observations. Replay emits evidence without duplicating committed artifact events. Failure observations are append-only diagnostics and cannot create active domain state.
