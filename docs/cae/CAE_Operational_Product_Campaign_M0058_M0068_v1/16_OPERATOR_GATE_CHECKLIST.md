# Operator Gate Checklist — M0058–M0068

After each mandate:
- Verify exact mandate ID.
- Verify exact commit.
- Verify requested files/artifacts.
- Verify current tests and command output.
- Verify evidence class for every material claim.
- Verify facts vs hypotheses vs operator decisions.
- Verify no prohibited architecture surface changed.
- Verify real runtime/environment fidelity where required.
- Verify the required false-proof case was exercised.
- Verify control state and receipt updates.
- Verify rollback/recovery is possible.

Choose exactly one:
`ACCEPT → AUTHORIZE NEXT`
`ACCEPT WITH LIMITATIONS → AUTHORIZE NEXT`
`REPAIR → RETURN TO CURRENT MANDATE`
`BLOCK → DO NOT PROCEED`

A green unit test or green UI is never sufficient proof of product operability by itself.
