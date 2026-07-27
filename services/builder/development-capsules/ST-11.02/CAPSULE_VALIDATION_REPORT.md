# ST-11.02 capsule validation

Verdict: `PASS`.

- Immutable inputs: `18/18 PASS`.
- Bundle digest: `170f8ca2ba8ba168b789da380daf3be7b6f74a2d64026aee1a00c57115edd369`.
- Direct dependency: ST-11.01 receipt and file manifest hash-valid.
- Owned obligations: FR-156 and FR-157, exactly as confirmed.
- Applicable blocker cut: empty in `SYNTHETIC_BUILDER_PROOF_HANDOFF_ONLY` mode.
- Conditional inactive gates: BD-008, HD-006 and HD-007; no maturity,
  conversational data or certification behavior is invoked.
- File allowlist: bounded to two new source modules, typed port/repository additions,
  exact-source test updates, Story tests and completion evidence.
- Acceptance, deterministic tests, observability and rollback are executable.
- The compiled plan cannot authorize its downstream implementation and cannot claim
  production or certification.

