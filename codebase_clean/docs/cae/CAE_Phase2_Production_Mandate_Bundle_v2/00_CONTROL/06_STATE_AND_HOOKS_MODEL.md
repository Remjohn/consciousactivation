# Program State + Hooks Model

CAE already has canonical state aggregate / transition / transition-contract concepts.
Do not create a second state ontology.

Use the StateM research pattern as a runtime execution pattern:
    Plan
    -> Execute State
       in_hook
       state body / agent work
       out_hook
       before_transfer
    -> Verify
    -> Repair or Handoff

Map this to CAE:
- Program State Aggregate = canonical CAE state authority
- State Transition = canonical CAE transition
- State Transition Contract = canonical preconditions/postconditions/receipt/error route
- in_hook = state-context preparation and invariant loading
- out_hook = persistence/checkpoint/receipt preparation
- before_transfer = deterministic blocking checks
- repair = governed reroute/recovery, not hidden improvisation

Every executable Program must declare an explicit state machine, even when small.
Not every Program needs the same number of states.

Hook rules:
- Pre hooks gate.
- Post hooks observe/record/react.
- Hook side effects must be idempotent or reconciled.
- Hooks cannot be relied on for exactly-once external side effects.
- Agent completion text is never proof of completion.
