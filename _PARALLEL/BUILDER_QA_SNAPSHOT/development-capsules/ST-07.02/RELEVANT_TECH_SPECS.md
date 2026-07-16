# Relevant Technical Specifications

## TS-06 — Canonical Harness IR and Compilation

Governs canonical Harness IR identity, deterministic projections, manifests, semantic non-mutation, explicit `NOT_APPLICABLE`, schema-version compatibility, reproducible hashes, failure behavior, and descendant invalidation. ST-07.02 consumes the existing active IR; it does not redesign or migrate it.

## TS-11 — Category Constitutions and Target Compilers

Primary Story specification. Governs the `atomic_content_harness` target, target-specific source/IR/Genesis references, deterministic target package identity, content semantic authority, three-target separation, and external runtime exclusion.

BF-AM-007 supplies the controlling conditional mode: `GENERIC_ATOMIC_CONTENT_HARNESS` depends on ST-03.05, ST-04.05, and ST-05.02; uses no category adapter; has no active blocker; and must emit `synthetic_not_certifiable`.

The capsule does not activate TS-11’s category-native, Format 02, Visual Asset Editor, Delegation, conversational, or production-certification branches.

