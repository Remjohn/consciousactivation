# SSSF Reference Register

## Canonical reference

Repository: https://github.com/disler/super-simple-software-factory
Example branch: https://github.com/disler/super-simple-software-factory/tree/example

## Specific patterns to study

### Agent roster/configuration
`sssf.config.yaml` makes the agent roster explicit and separates agent configuration from workflow call sites.

### Workflow as code
ADW scripts are Python and own sequencing, retries and acceptance. The reference deliberately stays in ordinary Python/YAML rather than inventing a DSL.

### Typed handoffs
Phase outputs use explicit envelopes/output types; downstream phases consume those typed artifacts rather than relying on conversational memory.

### Deterministic gates
Gate functions are code and represent the definition of done for a phase.

### Same-session repair
A failed quality/review result can be routed back to the builder without throwing away the active Agent session.

### Trace
Events stream into SQLite during execution. The same underlying trace powers live observation and historical inspection.

### Operator surface
The stamped factory provides `just` recipes for demos, sessions, phases, tailing and processes, plus a read-only Vue/Vite/Bun visualizer.

## CAE adaptation rule

Borrow the separation and execution discipline. Do not import SSSF's SQLite database as CAE authority, its agent names as CAE ontology, or its workflow scripts as a parallel CAE runtime. PostgreSQL/CAE registries/state/receipts remain authoritative where already established.
