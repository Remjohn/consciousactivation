# Production Claim Ceiling

Until M72 is accepted:
- `DOCUMENTED` is not `CODE_EXISTS`.
- `CODE_EXISTS` is not `TEST_VERIFIED`.
- `TEST_VERIFIED` is not `INTEGRATION_VERIFIED`.
- `INTEGRATION_VERIFIED` is not `RUNTIME_VERIFIED`.
- `RUNTIME_VERIFIED` is not `OPERATOR_ACCEPTED`.

Specific exclusions:
- AgentInvocation existence does not prove all production Agent calls use it.
- SQLite store availability does not prove deployment uses it.
- Program `/run` availability does not prove factory `RUN` uses it.
- Certification report existence does not prove certification truth.
- `AGENT_CALL` labels do not prove Agent execution.
- `production_ready` strings do not prove production authorization.
