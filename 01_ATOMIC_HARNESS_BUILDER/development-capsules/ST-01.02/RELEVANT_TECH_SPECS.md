# Relevant Technical Specifications

## TS-02 — Configured Evidence Workspace (primary)

Authoritative path:
`docs/tech-specs/specs/TS-02-CONFIGURED-EVIDENCE-WORKSPACE.md`
(SHA-256 `76232c0b5f5ab4e9d1f7423824fbbc1759380bf5457e6dedaccda2c9f17d9619`).

ST-01.02 implements only the first vertical evidence-workspace outcome:
versioned `SourceProfile`, pre-commit diagnostics, immutable
`SourceDescriptor` records, aggregate `SourceLock`, read-only file/directory/ZIP
inspection, typed safety failures, deterministic identity, and exact run
binding. Specimen parsing, claims, gaps/conflicts, saturation, media inference,
CAS, and production persistence remain later work.

The TS-02 Format 02 acceptance clause and conversational amendment are
conditional specializations and are not active for this repository-owned,
non-personal synthetic source.

## TS-01 — Governed Lifecycle and Target Profiles (dependency boundary)

Authoritative path:
`docs/tech-specs/specs/TS-01-GOVERNED-LIFECYCLE-AND-TARGET-PROFILES.md`
(SHA-256 `4fd7b94505518877cf1f87f417527ac9be305317408300e2c2da618e84eee1a5`).

The implementation must reuse the ST-01.01 run identity, authority,
idempotency, event replay, and optimistic-version seams. It may add only the
`SOURCE_DIAGNOSTIC -> SOURCE_LOCKED` path and exact source-lock reference for
the already governed synthetic profile. It may not broaden target selection.

## TS-11 — Category Constitutions and Target Compilers (negative boundary)

Authoritative path:
`docs/tech-specs/specs/TS-11-CATEGORY-CONSTITUTIONS-AND-TARGET-COMPILERS.md`
(SHA-256 `f6a269e974ef44dc169790b82effa6b1c00b880e5915fd52df2172eee4d64de3`).

The synthetic definition remains category-neutral, does not enter the five
canonical category registry, and does not compile a target package. No
Delegation RC4 runtime or schema behavior is needed by this Story.
