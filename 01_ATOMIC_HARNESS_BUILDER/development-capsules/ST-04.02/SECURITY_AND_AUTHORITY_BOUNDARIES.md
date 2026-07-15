# Security and authority boundaries

- Deterministic Builder code alone may compile and commit the module graph.
- The compiler consumes the active ST-04.01 ownership graph without changing capability owners or authority boundaries.
- Module topology cannot grant authority, hide a mixed owner-kind pipeline, or convert agent, human, external, or hybrid ownership into code ownership.
- Inputs are repository-relative, immutable, hash-pinned, and read-only; arbitrary paths and hash drift fail closed.
- Domain code imports neither application nor adapters; application code imports no adapter.
- No network, provider, credential, external runtime, production persistence, subprocess, API, UI, or external-product write is permitted.
- Observations expose identities, coverage, counts, and typed failures only, never source or contract payloads.
- Program Control remains read-only governing authority; VAE and Delegation behavior and shared-contract ownership remain external.
