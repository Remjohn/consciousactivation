---
title: Delegation Issue Register and Program XRI References
product: CMF Content Harness Visual Asset Editor Delegation Protocol
status: active
updated: 2026-07-15
---

# Delegation Issue Register and Program XRI References

Program-level `XRI-*` identity, title, scope, owner, severity, status and
resolution criteria are governed only by:

`../CMF_PROGRAM_CONTROL/04_CROSS_REPO_ISSUES/XRI_REGISTRY.yaml`

This repository records only exact XRI identifiers as references. It does not
cache or redefine their canonical fields.

## Repository-local issues

| ID | Status | Severity | Local condition | Historical identifiers | Resolution or next evidence |
|---|---|---|---|---|---|
| `DLG-ISSUE-001` | open | critical | Exact pinned upstream source coordinates needed to reproduce every source-to-local diff are not all available to this repository. | `XRI-001` (mistaken local use) | Supply immutable source artifacts or repository/tag coordinates and verify recorded hashes. |
| `DLG-ISSUE-002` | open | critical | Pinned product implementation revisions, public adapter surfaces, executable tests and owner-ratification evidence are not all available to this repository. | `XRI-002` (mistaken local use) | Supply pinned product revisions, ratification receipts and adapter/test entry points. |
| `DLG-ISSUE-018` | closed | medium | The repository-governed agent workflow file was absent during the original audit. | `XRI-018` | Closed by `AGENTS.md` and `00_ALIGNMENT_START_HERE.md`; renamed because `XRI-*` is reserved for program issues. |

`DLG-ISSUE-018` preserves the following traceability fields:

```yaml
historical_identifiers:
  - XRI-018
renamed_because: reserved_program_namespace
status: closed
resolution_evidence:
  - AGENTS.md
  - 00_ALIGNMENT_START_HERE.md
```

## Canonical program issue references

The Delegation repository currently references these Program Control records:

- Resolved shared-contract records: `XRI-003` through `XRI-012`.
- Open cross-product readiness records: `XRI-013` through `XRI-017`.
- In-remediation cross-product execution-evidence records: `XRI-019` through
  `XRI-021`.

The ranges above are identifier references only. The authoritative meanings and
statuses must be read from the Program Control registry.

## Historical traceability

Immutable release candidates, release rehearsals, Stage 1 through Stage 4
reports, technical specifications and VAE Stage 2/3 mappings retain their
original XRI text as historical evidence. They are not active issue registries
and do not override Program Control.

RC1 remains a historical consumer rejection, RC2 and RC3 remain historical
convergence rejections, and RC4 remains the current local unsigned candidate.
No issue resolution or namespace reconciliation authorizes production.
