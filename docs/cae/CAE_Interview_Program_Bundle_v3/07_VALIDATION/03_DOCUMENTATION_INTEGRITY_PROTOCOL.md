# Documentation Integrity Protocol

Before any mandate or program is marked ACCEPTED:

1. Check bundle version/name consistency.
2. Check manifest file count and hashes.
3. Check every internal link/path cited by the bundle.
4. Check that PRD/spec status reflects reality.
5. If durable semantics changed, verify the PRD was updated in the same session.
6. If implementation deviated from the tech spec, verify the spec was updated or the deviation was explicitly accepted.
7. Ensure no execution-completion claim exists without a matching receipt.
8. Ensure all unresolved gaps remain visible.

## Claim hygiene

Use only `VERIFIED`, `PARTIALLY_VERIFIED`, `UNVERIFIED`, `BLOCKED`, `NOT_APPLICABLE`.
