# Phase 2 — CAE State ↔ Pi Runtime Mapping

This contract maps the existing CAE state model to Pi's current durable runtime. It does not create a second CAE state ontology.

| CAE authority | Pi/runtime representation | Authority | Required proof |
|---|---|---|---|
| Program Run | durable Pi session + CAE run ID | CAE run is canonical | matching identifiers |
| Program State Aggregate | CAE state aggregate | CAE | Pi cannot override |
| State Transition | CAE transition operation | CAE | transition contract proof |
| State Transition Contract | CAE transition validation | CAE | invalid transition blocked |
| Harness runtime state | Pi operation/lane state | Pi runtime | mapped/checkpointed |
| Authority Lane | Pi lane + CAE lane assignment | CAE | mismatch blocked |
| Typed Operation | CAE operation carried by Pi operation | CAE | mutation trace |
| Hook | Pi lifecycle hook/extension | runtime | guarantee proof |
| Receipt | CAE receipt/evidence | CAE | state/artifact/receipt agreement |
| Recovery | CAE recovery policy + Pi resume/replay | CAE policy | fault injection |

Rule: Pi events, assistant text and UI status never directly advance canonical CAE state.
