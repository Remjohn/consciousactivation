# Security and authority boundaries

- Deterministic Builder code alone may compile and commit the phase graph.
- Topology cannot grant authority, bypass human or validation gates, mutate parent graphs, or create implicit parallelism.
- Inputs are repository-relative, immutable, hash-pinned, and read-only; arbitrary paths and hash drift fail closed.
- Domain code imports neither application nor adapters; application code imports no adapter.
- No phase execution, network, provider, credential, subprocess, external runtime, production persistence, API, UI, or external-product write is permitted.
- Observations expose identities, counts, states, and typed failures only, never payload values.
- Program Control remains read-only governing authority; VAE and Delegation runtime behavior and shared-contract ownership remain external.
