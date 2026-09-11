# Acceptance Evidence Schema — M49–M64

Every mandate report must preserve the existing CAE evidence style.

```yaml
mandate_id: M00
commit_sha: <exact>
files_read: []
files_changed: []
object_authority: []
implemented_behavior: []
commands: []
fixtures: []
tests:
  - command: <exact>
    result: PASS|FAIL|BLOCKED
    environment: <versions>
runtime_evidence:
  traces: []
  invocation_ids: []
  artifact_ids: []
  receipt_ids: []
false_proof_cases: []
remaining_gaps: []
current_md_updates: []
operator_decision: ACCEPT|ACCEPT-WITH-LIMITATIONS|REJECT|STOP-BLOCKED
```

No empty evidence field may be treated as positive evidence.
