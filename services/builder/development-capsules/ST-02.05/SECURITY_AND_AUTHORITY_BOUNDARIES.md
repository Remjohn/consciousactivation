# Security and authority boundaries

Atomicity decisions are deny-by-default. `APPROVE`, `REVISE`, `REJECT`, and `REOPEN` require a registered `HUMAN` actor with an unexpired exact action/resource grant. Agents may propose or explain. Code may validate, compile, hash, persist, replay, and emit evidence only after the human decision. External actors and evaluators cannot commit governed Builder state.

Implementation authorization and atomicity ratification are separate authorities. The phrase authorizing code work must never be stored as the product-boundary decision. Tests must exercise a typed human decision at the public application seam.

The adapter reads only the hash-pinned repository-local JSON input and the already locked synthetic source; it must resolve paths beneath the repository root, forbid network access and dynamic discovery, and reject byte drift. No content execution occurs.

Frozen versions are immutable. A reopen preserves prior events and hashes, emits a complete invalidation chain, and requires a new version. No hidden overwrite, deletion, history rewrite, or silent downstream consumption is allowed.

This Story owns no VAE or Delegation behavior or schema. Delegation `1.1.0-rc.4` is not a direct dependency. No Format 02, conversational, personal, Human Reaction, Identity DNA, provider, GPU, evaluator, or publication data enters the active mode.
