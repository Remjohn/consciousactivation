# Epic Validation-Report Hash Reconciliation

## Verdict

`RECONCILED_NON_SEMANTIC`

The confirmed Epic design has not changed. The discrepancy is a phase-sensitive validation-report regeneration after the program had legitimately advanced beyond the Step 2 confirmation gate. The current report's two failures describe current program phase, not changes to the 12-Epic design or its 410 primary obligation assignments.

## Authority determination

The authoritative confirmed Epic content is the combination of:

1. `docs/planning/EPIC_INVENTORY_CONFIRMATION_RECEIPT.yaml`, which records the human confirmation of the 12-Epic inventory;
2. `docs/planning/EPIC_INVENTORY.yaml`, whose current SHA-256 still equals its confirmed hash;
3. `docs/planning/EPIC_REQUIREMENT_COVERAGE.csv`, whose current SHA-256 still equals its confirmed hash; and
4. `docs/planning/EPIC_DESIGN_PROPOSAL.md`, whose current SHA-256 still equals its confirmed hash.

`docs/planning/EPIC_DESIGN_VALIDATION_REPORT.json` is a derived validation result. Its confirmation-time byte identity is pinned by the Epic manifest and confirmation receipt, but its validator also reads mutable program-phase status. It is therefore evidence about the phase at which it was run, not a substitute for the confirmed Epic content artifacts.

## Expected and observed hashes

| Artifact state | SHA-256 |
| --- | --- |
| Confirmation-time expected validation report | `f6306221a8d891fb497638b8156b6469cf275da7854017c29eab72043b62f989` |
| Current observed validation report | `dac666f0ee991926f9407d3289ae99d746dd965d78a7240a4af6b52a84f7728b` |

The expected hash is independently recorded in both `EPIC_DESIGN_FILE_MANIFEST.yaml` and `EPIC_INVENTORY_CONFIRMATION_RECEIPT.yaml`. The observed hash is recorded in `STORY_INVENTORY_CONFIRMATION_RECEIPT.yaml` and was reproduced from the current file.

## Semantic comparison

Reconstructing the confirmation-time report from the current report requires exactly these semantic edits:

- `status`: `FAIL` -> `PASS`;
- remove `program status does not report Step 2 complete pending human confirmation` from `errors`;
- remove `program status improperly authorizes vertical Story authoring` from `errors`.

With CRLF serialization preserved, those edits reproduce the expected `f630...` hash exactly. Every Epic-design datum remains identical:

- 410 confirmed obligations;
- 410 primary assignments and 410 unique primary assignments;
- no missing or duplicate primary assignments;
- 12 Epics;
- 46 dependency edges with dependency-order validation `PASS`;
- identical per-Epic obligation and authority-type counts;
- all five canonical categories;
- all four conversational profiles;
- all three compilation targets;
- HD-006, HD-007, BD-004, BD-007, BD-008, BD-010 and BD-014;
- XDEP-001 through XDEP-006.

The current errors arise because `docs/planning/tools/validate_epic_design.py` still tests for the historical Step 2 state (`epic_step_2_complete_pending_human_confirmation` with Story authoring unauthorized). The program has since completed confirmed Step 3 and Step 4 planning. Rerunning the validator on 2026-07-15 therefore regenerated only its phase-sensitive status fields.

## Cause classification

- Formatting or regeneration: **yes** -- the derived report was regenerated after phase advancement.
- Timestamp or metadata changes: **no direct report field change** -- the meaningful difference is phase status, not an embedded timestamp.
- Intentionally amended file: **yes, as a derived current-phase diagnostic**, not as an Epic amendment.
- Accidental content drift: **no**.
- Incorrect recorded hash: **no** -- the recorded expected hash is reproducible.
- Unknown cause: **no**.

## Disposition

The current `dac666...` report hash is accepted as a non-semantic successor for the post-confirmation phase-sensitive diagnostic. It does not replace the confirmation-time identity as historical evidence and does not amend the confirmed Epic inventory. The unchanged hashes of the inventory, coverage matrix and proposal preserve the human-confirmed authority.

No renewed Epic confirmation is required. Any future difference in Epic count, primary assignment, obligation identity, dependency design, category/profile/target coverage, or the confirmed content-artifact hashes invalidates this disposition and requires human reconfirmation.

