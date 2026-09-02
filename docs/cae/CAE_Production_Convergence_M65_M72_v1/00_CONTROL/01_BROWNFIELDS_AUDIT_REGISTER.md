# Brownfield Audit Register — Current main

| Area | Exact current evidence | Audit implication |
|---|---|---|
| Agent canonical object | `agent_registry.py`: `AgentRegistry`, `AgentDefinition`, lifecycle and collision checks | Reuse; do not create another Agent authority |
| Agent execution | `agent_invocation.py`: `AgentInvocationCompiler` + `AgentInvocationRuntime.execute()` | Real execution boundary exists |
| Model fallback | `AgentInvocationRuntime.execute()` has a default deterministic mock when neither `inference_fn` nor `model_reasoning_engine` is supplied | Production mode must not use this fallback as evidence |
| Program operator | `program_operator_runtime.py`: `dispatch_chat_command()` `/run` calls `run_program()` and returns aggregate/version/state_hash/receipt | Existing canonical operator run path should be reused |
| Program state | `program_state_runtime.py`: `UniversalProgramStateRuntime`, CAS, local context, transition receipts | Existing canonical state authority |
| Persistence | `program_state_runtime.py`: SQLite store methods for aggregate/transition persistence | Durable persistence exists; composition must be verified |
| Factory observability | `factory_observability.py`: `_live_runs`, `_replays`, RUN/REPLAY handlers | Potential duplicate execution truth |
| M64 certification | `factory_certification.py`: all criteria instantiated with `PASSED` | Certification not evidence-derived |
| SDLF Agent phases | `sdlf_factory.py`: SCOUT/PLAN/BUILD/REVIEW/REPAIR/DOCUMENT return hard-coded outputs with `success=True` | Role label is not execution proof |
| SDLF quality | `sdlf_factory.py`: quality defaults to pass when runner absent | Quality certification can be synthetic |
| Pipeline composition | `services/pipeline/.../application.py` constructs Workflow/Skills/Retrieval/etc. but not AgentInvocation runtime | Full Program→Agent path not proven |
| Current truth | `docs/PRD/CURRENT.md` still carries unresolved agentic/deployment/AWS notes | Must reconcile, not erase |
