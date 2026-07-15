# Relevant Technical Specifications

## Implementation-governing specifications

### TS-00 — Architecture Preservation Contract

Source: `docs/tech-specs/ARCHITECTURE_PRESERVATION_CONTRACT.md`

Applies to authority precedence, modular-monolith boundaries, deterministic validation, immutable identities, event authority, external-product separation, and the rule that lower planning material cannot override the Constitution or PRD.

### TS-01 — Governed Lifecycle and Target Profiles

Source: `docs/tech-specs/specs/TS-01-GOVERNED-LIFECYCLE-AND-TARGET-PROFILES.md`

This is the primary implementation specification. Implement only its run aggregate, target-profile binding, lifecycle transition, authority, idempotency, event, checkpoint, resume, and boundary rules needed by ST-01.01. The public seam for this Story is the application command surface; API and CLI adapters are not required in this capsule. PostgreSQL, production object storage, workflow engines and external runtime activation are excluded.

### TS-15 — Format 02 Reference Slice

Source: `docs/tech-specs/specs/TS-15-FORMAT-02-REFERENCE-SLICE.md`

Applies only to the identity and bounded selection of `atomic_content_harness` plus the `2d_character_animation/format02_minimal_coach_theatre` profile. Format 02 remains `contract_compatible`, not benchmarked or production-certified. This Story does not ingest its corpus, compile its harness, or certify it.

## Boundary-governing references

### TS-02 — Configured Evidence Workspace

Source: `docs/tech-specs/specs/TS-02-CONFIGURED-EVIDENCE-WORKSPACE.md`

Reference only. ST-01.01 may expose the next required work as evidence-workspace readiness, but it must not register, normalize, lock, index, retain, redact, or withdraw evidence. Those outcomes begin at ST-01.02.

### TS-07 — Product Architecture Graphs

Source: `docs/tech-specs/specs/TS-07-PRODUCT-ARCHITECTURE-GRAPHS.md`

Reference only for module ownership and dependency boundaries. This Story does not compile architecture graphs or invalidation graphs.

### TS-11 — Category Constitutions and Target Compilers

Source: `docs/tech-specs/specs/TS-11-CATEGORY-CONSTITUTIONS-AND-TARGET-COMPILERS.md`

Reference only for immutable target/category/profile identities and false-certification rejection. No category compiler, target package, conversational execution, visual handoff, VAE contract, or Delegation contract is implemented.

### TS-13 — Implementation Authorization and Development Capsule

Source: `docs/tech-specs/specs/TS-13-IMPLEMENTATION-AUTHORIZATION-AND-DEVELOPMENT-CAPSULE.md`

Governs this capsule, its hash manifest, bounded authority, evidence requirements, and `StoryCompletionReceipt`. ST-01.01 does not implement the general authorization service or capsule compiler.

### TS-14 — Builder Workflow Runtime

Source: `docs/tech-specs/specs/TS-14-BUILDER-WORKFLOW-RUNTIME.md`

Negative boundary only. The Story must not introduce a scheduler, Workflow IR, Temporal adapter, worker routing, agent runtime, retry policy, or incident workflow.

## Precedence

If any reference specification appears to broaden this capsule, the capsule remains bounded by the Story's owned obligations, current explicit human direction, Builder PRD V1.2, the Activative Intelligence Constitution V1.1, and TS-00. A conflict stops implementation and requires human disposition.

