# False-Proof Cases

These are mandatory adversarial checks for this program.

## Receipt laundering

A mandate has a completion receipt but the claimed code change is absent at the current commit.

Expected: `CLAIMED_UNVERIFIED`.

## Test laundering

A historical test result says PASS, but the relevant code changed afterward or the test was not run in the current environment.

Expected: historical evidence is preserved; current proof is absent.

## Documentation laundering

A Tech Spec says “implemented,” but no executable path or current test/receipt supports it.

Expected: not implemented proof.

## Status laundering

The PRD says COMPLETE because a mandate file exists, even though the mandate's runtime verification is absent.

Expected: PRD synchronization must retain incomplete status.

## Duplicate deletion

Two similarly named artifacts exist, but one is current authority and one is historical evidence.

Expected: preserve both; classify relationship.

## Textual agreement without runtime proof

PRD and reconciliation report agree perfectly, but direct repository checks contradict both.

Expected: final verification fails; upstream evidence is authoritative for the correction.

## “Green means complete”

A targeted unit test passes while the actual end-to-end path remains blocked.

Expected: report the exact property proven and the unproven wider property.
