# Phase 2 Acceptance Matrix

| Capability | Normal | Denial/Block | Recovery | Receipt | Trace | Operator gate |
|---|---|---|---|---|---|---|
| Pi execution | required | n/a | required | required | required | n/a |
| Program discovery | required | invalid package | n/a | n/a | required | n/a |
| Harness binding | required | invalid contract | n/a | n/a | required | n/a |
| State runtime | required | invalid transition | required | required | required | when declared |
| Agent Team | required | wrong lane/capability | member failure | required | required | when declared |
| Skills | required | draft/nested/mismatch | n/a | load evidence | required | n/a |
| Hooks | required | unsafe call | recovery | required where mutation | required | n/a |
| Operator gate | required | unauthorized decision | repeated decision | required | required | required |
