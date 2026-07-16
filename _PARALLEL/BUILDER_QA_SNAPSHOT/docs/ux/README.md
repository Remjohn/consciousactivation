# Builder Next UX Package

Status: `APPROVED`

This package contains the PRD-mandated Harness Control Tower UX contract. It defines implementation-boundary behavior and contains no production UI code.

| Artifact | Purpose |
|---|---|
| `HARNESS_CONTROL_TOWER_UX_CONTRACT.md` | Binding information architecture, interaction, authority, accessibility, degraded-state, security, and acceptance contract |
| `CONTROL_TOWER_UX_APPROVAL_RECEIPT.yaml` | Governed human approval record and pre-approval contract hash |
| `CONTROL_TOWER_UX_TRACEABILITY_MATRIX.csv` | Owned and supporting PRD requirements mapped to contract clauses, surfaces, and acceptance tests |
| `CONTROL_TOWER_UX_VALIDATION_REPORT.json` | Machine-readable structural and traceability validation result |
| `tools/validate_control_tower_ux.py` | Documentation-only validator |

Human product and UX authority approved the contract on 2026-07-14. The Epics and Stories prerequisite is satisfied; the production implementation gate remains closed.
