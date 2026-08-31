# Hook Guarantee Matrix

| Event | Target | Preconditions | Hook | Action | Block/Observe | Failure route | Receipt/evidence | Idempotency |
|---|---|---|---|---|---|---|---|---|

Required classes:
- Program start
- before tool/mutation
- after mutation
- state transfer
- Program completion
- recovery

Rule: deterministically enforceable process behavior must not remain only in prose.
