# Canonical Program Inventory Method

A Program is an operator-addressable unit of supervised work. It is not a service name, not a
Skill, not an Agent, and not automatically a new canonical database object.

Each Program must be inventoried with:

- Program ID / name
- business purpose
- operator trigger
- workspace/guest scope
- input artifacts/state
- preconditions
- upstream Programs
- downstream Programs
- existing services/routes
- existing typed operations
- existing Harness/Atomic Harness coverage
- Agent Team requirement
- Skills required
- Sub-agents required
- deterministic tools / MCP
- Hooks / Extensions
- Program state machine
- operator gates
- artifacts emitted
- receipts/evidence
- current implementation status
- runtime gap
- production-blocking gap
- proposed pilot role

Status vocabulary:
    EXISTS
    PARTIAL
    WIRED
    BUILT_UNWIRED
    BUILT_GATED
    SYNTHETIC_ONLY
    MISSING
    ARCHIVE_ONLY
    DECISION_REQUIRED

No Program is declared missing merely because no directory called "program" exists.
Services may implement Programs. Conversely, a service is not promoted into a Program merely
because its name sounds operational.
