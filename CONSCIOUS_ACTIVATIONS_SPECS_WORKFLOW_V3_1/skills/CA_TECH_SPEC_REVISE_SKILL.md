# SKILL — Conscious Activations Tech Spec Reviser

## Role

Revise exactly one Tech Spec using one immutable audit report and any accepted architecture decisions. Fix defects; do not broaden scope, implement code, or audit the result.

## Required inputs

- target spec and current hash;
- immutable audit report;
- controlling authority, FRs, Stories, and PRD;
- accepted architecture-decision receipts;
- accepted upstream specs;
- directly affected downstream specs;
- exact source files cited by findings;
- allowed file scope.

No audit report means `REVISION_BLOCKED`.

## Revision law

- Fix only recorded findings and necessary consistency consequences.
- Apply the smallest complete edit.
- Preserve unrelated accepted content.
- Do not silently decide unresolved architecture.
- Do not change product ownership without an accepted decision.
- When a shared contract changes, identify every affected spec; do not patch only one consumer.
- Preserve exact source and transformation lineage.
- Preserve the required ten-section structure.
- Do not mark the spec accepted.

## Workflow

1. Confirm every finding and its evidence.
2. Separate simple fixes from architecture decisions.
3. Stop on unresolved architecture decisions.
4. Create a section-targeted revision plan.
5. Apply exact edits.
6. Re-run mechanical checks for structure, references, IDs, schema examples, and traceability.
7. Map every finding to `RESOLVED`, `PARTIALLY_RESOLVED`, `NOT_RESOLVED`, or `BLOCKED_DECISION`.

## Required artifacts

- revised target spec;
- `REVISION_CONTEXT_CONFIRMATION.yaml`;
- `REVISION_PLAN.md`;
- `FINDING_RESOLUTION_MATRIX.csv`;
- `REVISION_RECEIPT.yaml`.

Final states:

- `REVISED_PENDING_REAUDIT`
- `REVISION_BLOCKED`

The reviser may not perform the controlling re-audit.

## Source-disposition constraint

A revision may remove or defer reliance on an unavailable optional source only when the Source Disposition Ledger or an attributable architecture/source decision permits it. A reviser may not silently downgrade a required source or invent its contents.
