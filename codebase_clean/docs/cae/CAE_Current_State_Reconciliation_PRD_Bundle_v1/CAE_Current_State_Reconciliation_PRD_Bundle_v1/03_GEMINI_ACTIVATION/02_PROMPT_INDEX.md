# Gemini Activation Prompt Index

Each prompt is embedded as Section 13 of its corresponding mandate, following the repository's mandate-authoring protocol.

| Mandate | Prompt location | Dependency | Mutating authority | Stop point |
|---|---|---|---|---|
| CA-CSR-01 | `02_MANDATES/CA-CSR-01_REPOSITORY_EVIDENCE_SWEEP.md` §13 | none | reconciliation evidence surface only | before reconciliation |
| CA-CSR-02 | `02_MANDATES/CA-CSR-02_AUTHORITY_STATUS_RECONCILIATION.md` §13 | accepted CA-CSR-01 | reconciliation ledger/report | before PRD edit |
| CA-CSR-03 | `02_MANDATES/CA-CSR-03_PRD_SYNCHRONIZATION.md` §13 | accepted CA-CSR-02 | `docs/PRD/CURRENT.md` | before final verification |
| CA-CSR-04 | `02_MANDATES/CA-CSR-04_FINAL_VERIFICATION_AND_HANDOFF.md` §13 | synchronized PRD | final verdict/handoff | before runtime-convergence |

Do not extract all prompts and run them as one composite instruction. The repository execution skill requires one mandate at a time, with an explicit operator decision and stop between mandates.
