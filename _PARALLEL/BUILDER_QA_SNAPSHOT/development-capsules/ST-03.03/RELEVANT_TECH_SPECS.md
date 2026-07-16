# Governing technical specifications

## Primary

- `TS-06 — Canonical Harness IR And Compilation`  
  Path: `docs/tech-specs/specs/TS-06-CANONICAL-HARNESS-IR-AND-COMPILATION.md`  
  SHA-256: `f00a3213b25eca31fb33481c92b4b650e3ebf14bc0ee72c9fce8f9c215a87a93`  
  Governs canonical root/value contracts, provenance, versioning, compatibility, serialization, identity, atomic snapshots, drift boundaries, lineage, and failures. This Story implements only initial IR creation/snapshot; artifact compilers remain later.

## Upstream and active-mode boundaries

- `TS-04 — Atomicity And Draft Harness Model`, SHA-256 `7062674691058ecfa7e85483814ff43fcc7fdd202642c91d546e44c95921ca5a`: consume only the frozen boundary, attributable ratification, model statuses, and invalidation chain.
- `TS-05 — Dependency-Driven Genesis`, SHA-256 `e9e4fb040df5d65b7038123c86b24669570b9c9190bd7be0fdcf730554135038`: interactive Genesis is inactive under BF-AM-004; authority separation, transactional state, and no provisional promotion remain binding.
- `TS-03 — Visual Syntax First`, SHA-256 `d2287b754e24cf7dc9350cf378f825d9a501b16d33b6fafd600f48033a218c27`: visual discovery is inactive; no visual evidence or meaning is invented.
- `TS-07 — Ownership, Phase, Context, Contract, Reference, Repair Graphs`, SHA-256 `f59fb61b439967b33447002e6a2d92b1e74cdb75d761e19cff86903798f474a6`: IR sections may preserve typed hypotheses/statuses but this Story does not compile final graphs.
- `TS-11 — Category Constitutions And Target Compilers`, SHA-256 `f6a269e974ef44dc169790b82effa6b1c00b880e5915fd52df2172eee4d64de3`: the synthetic profile is category-neutral, non-certified, and not a sixth category; no category compiler is implemented.
- `TS-12 — Harness Control Tower`, SHA-256 `40deeef95e2e9730fb18e22588b62c7448d0c6372dc8429960329d5f0ce75946`: no Control Tower projection or behavior is implemented.
- `TS-13 — Implementation Authorization And Development Capsule`, SHA-256 `231ce20ed1c1f34c58a8841b69db6f4bd642e85eef8ec781ee6fd088788abc95`: governs this capsule, completion receipt, exact file scope, and separate next-Story authorization.
- `TS-14 — Builder Workflow Runtime`, SHA-256 `df092317d49f7bb36fe53b91022355949480180e095d89df5922f5086ff4e802`: governs the negative aggregate boundary; Workflow IR/runtime state cannot enter Harness IR and no runtime is implemented.

Binding precedence is `governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`, SHA-256 `8903d96f1eacb7d6076c81f934fa7c571b025f595ec797d679acde2b1ae922d7`. No technical specification may be edited.
