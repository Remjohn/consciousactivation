# Phase 2 — Fault Injection / Recovery Matrix

Required faults:
1. crash before acceptance;
2. crash after effect-intent;
3. crash after external tool before settlement;
4. DB connection loss during settlement;
5. provider timeout;
6. tool failure;
7. MCP failure;
8. hook rejection;
9. missing Skill/hash mismatch;
10. operator rejection;
11. stale state;
12. duplicate resume;
13. duplicate external effect;
14. receipt/artifact mismatch;
15. wrong Workspace capability;
16. agent member failure;
17. subagent timeout/cancel;
18. partial package compilation.

Each test declares expected outcome: BLOCK / RETRY / RECONCILE / RESUME / REPAIR / FAIL-CLOSED.
