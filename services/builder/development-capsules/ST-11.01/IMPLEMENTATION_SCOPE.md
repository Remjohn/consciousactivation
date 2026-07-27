# Implementation Scope

Implement one deterministic compiler that consumes the exact active `synthetic_text_normalization_v1` `AtomicHarnessDefinition`, its PASS ST-07.04 validation, the four direct dependency receipts, and the hash-pinned `SYNTHETIC_DEVELOPMENT_CAPSULE_INPUT.json`.

It emits an immutable `VersionedTraceableDevelopmentCapsule`, receipt, run reference, deterministic observations, replay/idempotency behavior, and descendant invalidation support.

The generated capsule must provide complete, hash-pinned and portable authority for implementing the synthetic Harness. Every section and reference must be justified, and the capsule must remain explicitly repository-owned, synthetic, non-production, non-certified, `synthetic_not_certifiable`, with no external runtime or skill.

The Story does not implement the generated capsule, execute the Harness, generate workflows, compile external targets, or authorize production work.
