# Mandate 59 — Workflow Control-Flow Compiler

    Status: PROPOSED — OPERATOR-RATIFICATION-REQUIRED
    Phase: PHASE 7 — WORKFLOW ENGINEERING
    Parallel group: P7-B
    PRD ownership: Relevant PRD sections are owned by this mandate; update the relevant `docs/PRD/CURRENT.md` section in the same execution session and record the exact commit SHA. If a local `CURRENT.md`/`CURRENT_PROJECT_STATUS.md` is affected, update it in the same session as well.

    ## 1. Decision / Objective

    Extend CAE’s deterministic scheduler/compiler so all approved workflow primitives have executable semantics for routing, looping, retry, fan-out, joins, timeouts, repair and human suspension/resume.

    This mandate is an implementation-and-proof mandate, not a permission to redesign CAE from scratch. The execution agent MUST first reconcile the requested behavior against the current brownfield implementation and existing object authorities.

    ## 2. Governing doctrine and authority

    This mandate is subordinate to:
    - Current CAE constitutions and object constitutions.
    - Current PRD and Technical Specifications.
    - Canonical Skill Authoring & Authority Lane Governance.
    - Existing Program, Harness, Atomic Harness, Skill, Hook, State, Receipt and Operation authorities.
    - Existing Pipeline/runtime authorities discovered during mandatory reading.
    - Existing Program packages and `CAE.md` local governance.
    - Explicit Operator decisions and phase gates.
    - External reference repositories only as implementation patterns; never as CAE authority.

    **Core doctrine for this wave:** code owns deterministic control flow; Agents own bounded reasoning; Skills remain passive; Hooks provide deterministic event guarantees; typed Operations remain mutation boundaries; evidence/receipts establish what actually occurred.

    ## 3. Mandatory reading before action

    ### Baseline
    - `docs/PRD/CURRENT.md`
- `docs/CANONICAL_SKILL_AUTHORING_CONSTITUTION.md`
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `governance/program-control/`
- `docs/cae/constitutions/`
- `docs/cae/implementation/`
- `services/pipeline/AGENTS.md`
- `services/pipeline/src/cmf_pipeline/`
- `packages/ca_runtime/`
- `tests/cae/`
- `services/pipeline/src/cmf_pipeline/workflow/application/compiler.py`
- `services/pipeline/src/cmf_pipeline/workflow/application/scheduler.py`
- `services/pipeline/src/cmf_pipeline/workflow/application/run_service.py`

    ### Reference implementation
    Read the SSSF reference repository, especially:
    - `.claude/skills/sssf/templates/sssf.config.yaml`
    - `.claude/skills/sssf/templates/adws/adw_simple_sdlc.py`
    - `.claude/skills/sssf/templates/adws/adw_modules/gates.py`
    - `.claude/skills/sssf/templates/adws/adw_modules/agent_pi.py`
    - `.claude/skills/sssf/apps/visualizer/`
    - `justfile`

    The execution agent must report the exact files actually read. A directory name is not evidence that its contents were read.

    ## 4. Exact scope

    ### Allowed work
    Reuse `RuntimeWorkflowCompiler`, `DeterministicScheduler` and `WorkflowRunService`. Add only missing control-flow realization and validation. Define termination proofs for loops and bounded behavior for retries. Do not permit model-generated changes to graph control.

    ### Required artifacts
    Control-flow compiler; scheduler extensions; failure-routing tests; loop/parallel fixtures; state/trace evidence; CURRENT update.

    ### Prohibited work
    - No new canonical object when an existing object can represent the requirement.
    - No second workflow engine.
    - No replacement of CAE state, receipt, Skill, Harness, Program or authority systems with framework-local equivalents.
    - No Skill-to-Skill invocation.
    - No collapse of HUNTER / ANALYST / COMPOSER / COMMANDER authority boundaries.
    - No direct Agent SQL mutation; use authorized CAE Operations.
    - No silent model/provider/runtime substitutions.
    - No synthetic evidence presented as production evidence.
    - No production cutover outside the mandate scope.
    - No widening into adjacent mandates except to preserve dependency integrity.

    ## 5. Required implementation behavior

    The execution must follow:

    `source/baseline → object/contract reconciliation → smallest implementation → deterministic validator/gate → reality-contact test → evidence → receipt → CURRENT.md update`.

    Where an Agent is invoked, the runtime must make explicit:

    `Agent → compiled context → model/tool policy → typed output contract → gate → result/receipt`.

    Where a workflow step is deterministic, prefer code over an Agent call. Do not spend model tokens on work that is already an executable function, condition, database query, formatter, linter, type-check, hash computation, or state check.

    ## 6. Verification and evidence

    The mandate is not complete because files exist or unit tests are green.

    Record:
    - exact commands;
    - environment/runtime versions;
    - fixtures and source artifacts;
    - test results;
    - runtime traces;
    - artifact IDs and receipt IDs;
    - prompt/context/package hashes where applicable;
    - exact commit SHA.

    Every important validator MUST include at least one contrastive false-proof case.

    ### Current-code example
    ```python
    ready = scheduler.ready_nodes(workflow, states)
batch = scheduler.safe_parallel_batch(workflow, states)
    ```

    ### SSSF reference example
    ```text
    SSSF explicitly keeps sequencing, retries and acceptance in Python. This mandate makes that discipline explicit inside CAE’s already-existing compiler/scheduler.
    ```

    The examples above are reference material. The executing Agent must reconcile them with the current CAE objects before coding.

## StateM alignment obligations

This mandate MUST preserve the CAE State authority while applying the bundle-level StateM contract (`00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md`) where relevant:
- treat state as a context-and-contract boundary, with state/phase entry refreshing the applicable context and recording inclusions/exclusions;
- keep executable transition rules, checks, hooks, retry budgets, persistence and timeouts outside the model;
- use checked transfer semantics and keep the run in the source state when a blocking check/hook fails;
- preserve recoverable per-run state/history/receipts across repair and retry;
- do not create a second state/runbook ontology;
- expose Agent and Operator views from the same canonical control/execution truth;
- do not promote Agent-generated lessons into binding procedure without versioned validation through existing authority.

    ## 7. Completion / stop condition

    Acceptance gates for this mandate:
    - Same workflow + same state snapshot gives same routing decision.
- Loop cannot exceed bound.
- JOIN waits for declared predecessors.
- TIMEOUT transitions to defined failure/recovery state.
- Human gate blocks until explicit operator result.

    STOP immediately if:
    - an object-constitution conflict is discovered;
    - implementation ownership is ambiguous;
    - the proposed change would duplicate an existing authority;
    - a test cannot distinguish false proof from genuine completion;
    - the required runtime environment is unavailable;
    - an existing production blocker is encountered outside this mandate's authorized scope.

    After reporting the result and limitations, STOP. Do not silently begin the next mandate.

    ## 8. Rollback / recovery

    If new semantics break existing runs, preserve backward compatibility through versioned runtime workflow definitions. No silent reinterpretation of historical graphs.

    ## 9. Operator decision

    The Operator must explicitly choose one:

    `ACCEPT` — mandate evidence satisfies all gates.

    `ACCEPT-WITH-LIMITATIONS` — bounded limitations are explicitly recorded and do not invalidate the next phase.

    `REJECT` — corrections/rework required.

    `STOP-BLOCKED` — authority, environment, or proof boundary prevents safe continuation.

    ## 10. False-proof / reward-hacking defense

    Attempt to escape an IF through an Agent-generated narrative; set max_retries=0 but still loop; create a JOIN with missing branch; invoke a human-gated step from an unauthorised lane.

    ## 11. Out-of-scope but recorded

    Any discovered gap outside scope must be recorded in the evidence ledger and left for a later mandate; do not patch it opportunistically.
