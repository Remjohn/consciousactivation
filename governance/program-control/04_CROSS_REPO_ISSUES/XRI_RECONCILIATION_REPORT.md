# XRI-001 and XRI-002 Identity and Status Reconciliation

Date: 2026-07-15  
Scope: bounded issue identity and status reconciliation  
Canonical registry: `XRI_REGISTRY.yaml`  
Validation: `../03_PROGRAM_STATUS/XRI_RECONCILIATION_VALIDATION.json`  
Full convergence audit rerun: no  
RC4 release-byte changes: none

## Outcome

Program-level `XRI-*` authority now resides in
`CMF_PROGRAM_CONTROL/04_CROSS_REPO_ISSUES/XRI_REGISTRY.yaml`. Repository files
may cite a canonical XRI but cannot independently redefine its title, meaning,
scope, owner, severity, status, resolution criteria, or supersession relation.

| Identifier | Canonical meaning | Owner | Severity | Canonical status |
|---|---|---|---|---|
| `XRI-001` | Delegation RC1 source-kind and interview-provenance consumer-conformance failure | Delegation Protocol | blocking | `resolved` |
| `XRI-002` | Conversational Activation category adoption in Builder governance | Atomic Harness Builder | high | `resolved` |

## Occurrence inventory

The final evidence table is `XRI_REFERENCE_MAP.csv`. It contains 78
file/identifier rows across 41 files: 67 rows capture the source evidence found
before active reconciliation and 11 rows capture the canonical registry,
status, report, and validation references produced by this pass.

For every row the table records the path, identifier, described meaning,
reported owner, reported status, severity, available date, active or
historical classification, program or repository scope, reconciliation
disposition, and canonical registry pointer. The map itself is excluded from
self-inventory to avoid recursive rows.

No Builder or VAE status export contained an active contradictory definition.
Their exports were therefore not changed.

## Canonical identity reasoning

### XRI-001

The earliest authoritative Program Control registration is
`04_CROSS_REPO_ISSUES/XRI-001.yaml`. It is backed by the dated VAE RC1 consumer
validation and Delegation's VAE rejection receipt. That evidence defines the
issue as RC1's missing source-kind discriminator, unenforced interview Reaction
Receipt and Expression Moment provenance, parse-without-enforcement behavior,
release-layout validator assumption, and transient source-manifest entries.

RC1 remains `consumer_rejected`. RC2 and RC3 remain historically
`convergence_rejected` for their later independent convergence defects. RC4
preserves the source/provenance and packaging corrections, passes clean-room
validation, and has been adopted by VAE as the current local unsigned
candidate. The original XRI is therefore `resolved`; it does not block RC4.

### XRI-002

Program Control's issue index registered XRI-002 as Builder adoption of
Conversational Activation / Human Expression as the fifth canonical category.
The controlling Builder V1.2 constitutional amendment, Builder PRD V1.2
category requirements, current canonical category registry, and planning
metadata all contain the category and governed conversational profiles.

The adoption issue is therefore `resolved`. Structural category adoption does
not imply benchmark completion, Format 02 certification transfer, or
production certification.

## Delegation-local replacements

Delegation had reused the two identifiers for unrelated local evidence gaps.
Those meanings remain open without reopening the canonical XRIs:

- `DLG-ISSUE-001`: missing pinned upstream source coordinates required to
  reproduce exact source-to-local diffs. Historical mistaken alias:
  `XRI-001`.
- `DLG-ISSUE-002`: missing pinned product revisions, public adapter and test
  entry points, executable cross-product evidence, and owner-ratification
  receipts. Historical mistaken alias: `XRI-002`.

The local IDs are defined in `03_DELEGATION_PROTOCOL/CROSS_REPO_ISSUES.md` and
referenced by Delegation's current status surfaces. They are not program-level
XRI records.

## Conflicting active references corrected

| File | Correction |
|---|---|
| `CMF_PROGRAM_CONTROL/04_CROSS_REPO_ISSUES/XRI-001.yaml` | Recast as a historical resolution receipt and changed its state to controlled value `resolved`. |
| `CMF_PROGRAM_CONTROL/04_CROSS_REPO_ISSUES/CROSS_REPO_ISSUES.md` | Made the canonical registry controlling and aligned both navigation rows. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/STATUS_TRUTH_RECONCILIATION.yaml` | Recorded the RC4 audit result and the completed bounded XRI reconciliation. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/MASTER_STATUS.md` | Recorded post-audit remediation truth without changing the last formal audit verdict. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/ALIGNMENT_DASHBOARD.md` | Recorded XRI reconciliation validation PASS and retained the formal-audit boundary. |
| `03_DELEGATION_PROTOCOL/CROSS_REPO_ISSUES.md` | Replaced the two local meanings with `DLG-ISSUE-001` and `DLG-ISSUE-002` and added the canonical authority pointer. |
| `03_DELEGATION_PROTOCOL/PROGRAM_STATUS_EXPORT.yaml` | Removed both XRIs from active blocker identity and added canonical resolved states plus open local replacements. |
| `03_DELEGATION_PROTOCOL/CURRENT_PROJECT_STATUS.md` | Added canonical XRI status and local replacement truth. |
| `03_DELEGATION_PROTOCOL/COMPATIBILITY_MANIFEST.yaml` | Replaced publication blockers with local IDs and added the canonical registry pointer. |
| `03_DELEGATION_PROTOCOL/_bmad-output/project-context.md` | Replaced active blocker references and explicitly classified the old XRI labels as mistaken aliases. |
| `03_DELEGATION_PROTOCOL/docs/implementation/IMPLEMENTATION_READINESS.md` | Replaced active blocker references and separated canonical resolution from continuing local readiness blockers. |

## Historical records retained unchanged

The reconciliation did not rewrite:

- Delegation or Program Control immutable release candidates, including RC4;
- RC3/RC4 release rehearsals;
- technical specifications and Stage 3 baseline reports;
- Epics, Stories, dependency planning, ADRs, PRDs, schemas, or lifecycle logic;
- the latest formal convergence report, verdict, and audit hash matrix.

Those references remain reproducible snapshots. Their former meanings and
states are explicitly classified in `XRI_REFERENCE_MAP.csv` and superseded by
the canonical registry for current status decisions.

## Separate open production concerns

Production trust, signing, publication, operational ownership, product
readiness, and certification remain open under the distinct `CRC-403` concern
and Delegation's applicable local/operational blockers. They are not part of
either resolved XRI. Production authorization remains false.

## Validation result

`XRI_RECONCILIATION_VALIDATION.json` records **PASS** for unique canonical
meaning, unique canonical status, absence of active repository redefinition,
historical traceability, status-export agreement, controlled vocabulary, and
unchanged RC4 bytes.

All prerequisites for a fresh read-only convergence audit are satisfied. This
reconciliation did not rerun that audit and cannot change its formal verdict.
