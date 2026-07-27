# Test Plan

Use governed `PYTHONPATH=src;.` and fresh processes.

1. Parameterize every `AtomicHarnessDefinition` semantic field and all 20 section
   identities/applicability/source references/bases. Forge, recanonicalize and rehash
   the definition; direct definition, receipt, report and command validation must reject.
2. Replace the compiler authority actor with unknown, unauthorized and stale identities;
   require zero partial state.
3. Recompile the untouched governed fixture and require byte-identical historical identity.
4. Use a throwing observation sink after atomic commit. Require returned committed receipt,
   deterministic pending outbox records, no false rejection and successful at-most-once retry.
5. Barrier two writers at the same expected version. Require one success, one conflict and
   one retained winner event/command record. Repeat enough times to prove scheduling independence.
6. Inject run-command failure at event, checkpoint and command-record boundaries across create,
   transition, waiver, checkpoint and resume. Require zero partial state and clean retry.
7. Replace a ZIP path between immutable read and inspection. Candidate hash and member
   descriptors must still describe the same original buffer. Preserve all archive safety tests.
8. Run new `tests/corrections` suite twice.
9. Run unchanged affected predecessor suites: `st_01_01`, supplemental proof, `st_01_02`,
   `st_07_02`, `st_07_04`, `st_11_01`, architecture and failure-boundary tests.
10. Run complete repository regression twice from fresh processes, compile all Python source,
    validate manifests/receipts, scan portable outputs for absolute paths/secrets, then rerun
    the synthetic demonstration integration gate.

Mandatory skips are prohibited.

