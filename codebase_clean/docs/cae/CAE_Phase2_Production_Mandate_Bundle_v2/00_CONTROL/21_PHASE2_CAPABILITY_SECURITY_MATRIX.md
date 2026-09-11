# Phase 2 — Capability / Security Boundary

Agent capabilities are explicit projections, not ambient access.

| Capability | Scope | Read/Write | Workspace bound | Approval | Sandbox | Audit |
|---|---|---|---|---|---|---|
| CAE typed operation | declared | declared | required | declared | N/A | receipt |
| Postgres/Storage | declared | declared | required | mutation dependent | runtime policy | trace |
| filesystem | declared | declared | required | risky ops | required | trace |
| process/CLI | declared | declared | required | risky ops | required | trace |
| network | declared | declared | required | external side effect | required | connection trace |
| secrets | named refs only | never raw by default | required | declared | secure store | access audit |
| MCP | named server/tool | declared | required | server/tool policy | required | invocation trace |

Fail closed when a capability, scope, authority lane or workspace cannot be resolved.
