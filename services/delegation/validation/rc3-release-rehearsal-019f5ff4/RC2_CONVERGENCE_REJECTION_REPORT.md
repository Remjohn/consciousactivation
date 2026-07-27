# RC2 Cross-Repository Convergence Rejection Report

historical_evidence: true

Date: 2026-07-14  
Rejected release: `1.1.0-rc.2`  
Failure class: release identity and packaging convergence  
Disposition: immutable historical evidence; do not modify or overwrite

## Finding

The cross-repository convergence audit found three active distributed package
declarations that still identified `1.1.0-rc.1`/`1.1.0rc1`:

1. `contracts/package.json`
2. `contracts/pyproject.toml`
3. `validators/pyproject.toml`

All other exact RC1 references in RC2 are historical rejection, replacement,
or changelog evidence. The audit also found that the mutable producer checkout
had already diverged from the frozen RC2 source manifest in the five paths
recorded by `docs/releases/RC2_SOURCE_PROVENANCE_DRIFT_REPORT.md`.

## Impact

No schema field, Visual Asset Demand semantic, lifecycle transition, authority
rule, migration transformation, adapter rule, or protocol-engine behavior was
shown defective. The rejection is nevertheless release-significant because
active package identity and the validators enforcing that identity were not
converged in the immutable candidate.

## Integrity evidence

- RC2 release digest: `sha256:d4958cd3d02f0acef9d66bf245078ea70dab36b727d0c1541031fdceb63f6e41`
- RC2 release manifest SHA-256: `sha256:6e765eeef4ebed71d6e725cf11f49815f9cc0cafbe42ef157c8f189d8c7d582c`
- RC2 release receipt SHA-256: `sha256:ff97185ec1dfd1c2eaf936beec318e28b583fd2e3da809df9b860f504c7b6cff`
- Repository-local and Program Control RC2 trees were byte-identical at rejection.

## Required correction

Preserve RC2 exactly and issue a new immutable candidate whose active package
metadata resolves to the new candidate identity while the envelope protocol
remains `1.0` and Visual Asset Demand remains `1.1`.
