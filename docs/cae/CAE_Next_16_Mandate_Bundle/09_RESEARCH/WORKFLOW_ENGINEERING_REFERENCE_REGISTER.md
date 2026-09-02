# Workflow Engineering Research Register

These sources are reference material for the workflow-engineering layer. They do not override CAE doctrine.

1. **Blueprint First, Model Second** — https://arxiv.org/abs/2508.02721
   Key lesson: codify workflow control deterministically; use LLMs for bounded specialist work.

2. **Plan with Code** — https://arxiv.org/abs/2408.08335
   Key lesson: executable plans expose control flow and allow syntactic/runtime checking.

3. **AutoFlow** — https://arxiv.org/abs/2407.12821
   Key lesson: the workflow itself can be generated/optimized and should be evaluated as a first-class object.

4. **QualityFlow** — https://arxiv.org/abs/2501.17167
   Key lesson: verification can dynamically route execution into revise/retry paths.

5. **SWE-agent** — https://arxiv.org/abs/2405.15793
   Key lesson: the Agent–environment interface materially affects reliability and task performance.

6. **AgentR** — https://arxiv.org/abs/2608.15264
   Key lesson: persistent state, recovery, retries, asynchronous execution and cost/observability are execution concerns, not prompt concerns.

7. **Agentic Computation Graphs / static-to-dynamic workflow graphs** — https://arxiv.org/abs/2603.22386
   Key lesson: distinguish workflow templates, realized execution graphs and traces; evaluate structure, robustness and cost alongside final outcome.

## Reading doctrine

Use research to compare implementation patterns and evaluate design options. Do not promote a pattern into CAE simply because a paper describes it. Every adopted mechanism must reconcile with CAE objects, authority, state, evidence and brownfield code.

8. **StateM — Stateful Execution for Long-Horizon Agents** — https://arxiv.org/pdf/2608.15089
   Adopted principles for this bundle: state as context/contract boundary; state-entry context refresh; host-controlled checked transitions; recoverable per-run state/history; shared human/agent control surface; versioned procedural practice; preserve the general-purpose Agent as the executive rather than decomposing every state into a new model call.
   Constraint: StateM is a reference pattern, not a CAE authority or license to introduce a parallel state/runbook ontology. See `00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md`.

8. **StateM — Stateful Execution for Long-Horizon Agents** — https://arxiv.org/pdf/2608.15089
   Adopted principles for this bundle: state as context/contract boundary; state-entry context refresh; host-controlled checked transitions; recoverable per-run state/history; shared human/agent control surface; versioned procedural practice; preserve the general-purpose Agent as the executive rather than decomposing every state into a new model call.
   Constraint: StateM is a reference pattern, not a CAE authority or license to introduce a parallel state/runbook ontology. See `00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md`.
