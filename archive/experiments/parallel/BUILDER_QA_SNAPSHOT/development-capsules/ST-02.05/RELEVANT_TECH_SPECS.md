# Governing technical specifications

## TS-04 — Atomicity and Draft Harness Model

- Path: `docs/tech-specs/specs/TS-04-ATOMICITY-AND-DRAFT-HARNESS-MODEL.md`
- SHA-256: `7062674691058ecfa7e85483814ff43fcc7fdd202642c91d546e44c95921ca5a`
- Governs: typed `DraftHarnessModel`, `AtomicityRatification`, human ratify/reject/reopen commands, immutable boundary freeze, invalidation, idempotency, authority, failure behavior, events, tests, and receipts.
- Active-mode interpretation: BF-AM-003 supplies the already declared category-neutral boundary, so visual-syntax discovery and provider evidence are inactive prerequisites. TS-04 authority, field-status, freeze, failure, and traceability rules remain binding.

## TS-11 — Category constitutions and target compilers

- Path: `docs/tech-specs/specs/TS-11-CATEGORY-CONSTITUTIONS-AND-TARGET-COMPILERS.md`
- SHA-256: `f6a269e974ef44dc169790b82effa6b1c00b880e5915fd52df2172eee4d64de3`
- Governs the negative boundary: the synthetic proof has `category_binding: none`, is not a sixth category, and cannot inherit certification or category semantics. No category compiler is implemented here.

## TS-15 — Format 02 Release 1 vertical slice

- Path: `docs/tech-specs/specs/TS-15-FORMAT-02-RELEASE-1-VERTICAL-SLICE.md`
- SHA-256: `74a0f48eaa6d9f2998d8a573ff0261187be4d693527cd66207f34a34c2183271`
- Applies only as a negative compatibility boundary in this capsule. Format 02 corpus, baselines, VAE evidence, provider comparison, and production certification are not inputs to `DECLARED_BOUNDARY` mode and must not be implemented or claimed.

## Binding requirement sources

- `docs/planning/PLANNING_REQUIREMENTS_INVENTORY.csv`, SHA-256 `d3db32a78f4acce25e5448ff7c6ecb765ba814c0bdbf1bb44d6b49de00c55923`
- `governance/READINESS_HARD_GATES.yaml`, SHA-256 `f1d431738086484978df71243f9bbddd049aadf31341d2e5cea354772c292800`

No technical specification may be edited during this Story.
