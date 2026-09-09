# CAE-M0058 — Brownfield Product-Run Baseline

**Invariant:** `FR-OPS-BASELINE`
**Representative Program:** `research_canonicalization_program`
**Representative Harness:** `RESEARCH_CANONICALIZATION_HARNESS_V1`
**Evidence digest:** `8b51d861da4a9f4322db4fcf910c1a3433bdf3cacf645846fc61c1973d1edb21`

## Environment

- Python: `3.12.0`
- Platform: `Windows-10-10.0.19045-SP0`
- Working tree Git metadata present: `True`
- Source Git commit recorded by archive: `c41b68394ba8d1435c3cbb62b08f38908bbd3737`
- Source Git commit basis: Explicit externally verified repository-main commit supplied for this archive baseline; the uploaded archive has no .git metadata, so this is not a cryptographic attestation of archive provenance.

## Path classification

| Status | Count |
| --- | ---: |
| WORKING | 5 |
| PARTIAL | 1 |
| MOCKED | 1 |
| UNREACHABLE | 1 |
| CONFLICTING | 3 |

## Reachable-call-path ledger

| Segment | Source → target | Status | Evidence | Observed / limitation |
| --- | --- | --- | --- | --- |
| Product operator entry | `ProgramOperatorRuntimeService.dispatch_chat_command(/run)` → `ProgramOperatorRuntimeService.run_program` | **WORKING** | `EXECUTABLE` | The existing operator command dispatcher accepted the representative Program and returned an aggregate ID. |
| Program package resolution | `ProgramRegistry.inspect_and_validate_package` → `research_canonicalization_program` | **WORKING** | `REGISTRY_SOURCE` | Manifest/package validation succeeded; pinned manifest SHA-256 1068733381da230e…. |
| Harness dispatch | `manifest.harness=RESEARCH_CANONICALIZATION_HARNESS_V1` → `HarnessPackageLoader / executable harness binding` | **UNREACHABLE** | `REGISTRY_SOURCE` | No separate executable binding/package for the exact declared harness was found, and ProgramOperatorRuntimeService.run_program does not invoke HarnessPackageLoader. |
| Runtime state authority | `ProgramOperatorRuntimeService → UniversalProgramStateRuntime` → `SqliteProgramStateStore` | **WORKING** | `EXECUTABLE` | A durable aggregate, lease record, workflow-dispatch record, and gate-suspension transition were persisted and re-read from SQLite. |
| Declared storage connection | `research_canonicalization_program.program_manifest.yaml connections` → `PostgreSQL research connection` | **CONFLICTING** | `REGISTRY_SOURCE` | The manifest declares postgresql_research_slice while the executable operator path tested here uses SqliteProgramStateStore. |
| Operator gate | `UniversalProgramStateRuntime.evaluate_gate_milestone` → `AWAITING_APPROVAL + GateSuspensionSnapshot` | **WORKING** | `EXECUTABLE` | The declared canonical_knowledge_commit_gate was evaluated, persisted, and moved the aggregate into AWAITING_APPROVAL with a receipt. |
| Evaluation / trace | `ProgramOperatorRuntimeService.project_execution_trace` → `ExecutionTraceProjection` | **WORKING** | `EXECUTABLE` | The trace projection returned the persisted state, allowable transitions, and a blocker explaining the gate suspension. |
| Release / ship path | `ProgramOperatorRuntimeService.dispatch_chat_command(/ship)` → `completion-gated ship refusal` | **PARTIAL** | `EXECUTABLE` | The release command path is callable and fails closed after a non-completed state; the representative run does not reach COMPLETED. |
| M71 golden-run expectation | `tests/cae/test_m71_real_domain_program_golden_run_benchmark.py` → `assert agg.version == 2 after run_program` | **CONFLICTING** | `TEST` | Current sandbox observation returns version 1 after operator.run_program, causing existing M71 assertions to fail before downstream transitions. |
| 17-stage product claim | `docs/PRD/CURRENT.md` → `research_canonicalization_program` | **CONFLICTING** | `DOCUMENT` | Current representative runtime state machine contains five declared research transitions; the M057 proof harness enumerates a 17-stage broader proof narrative. |
| M057 provider/distribution boundary | `tests/e2e/test_live_e2e_proof_harness.py local HTTP fixtures` → `external inference/distribution services` | **MOCKED** | `TEST` | The M057 live-proof test passes against test-owned local HTTP servers; that proves fixture reachability, not production-provider or production-distribution reachability. |

## Program inventory

| Program | Version | Runtime SM | Harness | Gates | Classification | Limitation |
| --- | --- | --- | --- | --- | --- | --- |
| `audience_context_program` | `1.0.0` | `True` | `AUDIENCE_HARNESS_V1` | audience_context_activation_gate | **PARTIAL** | Declared harness identifier has no separate executable binding/package occurrence. |
| `collision_discovery_program` | `1.0.0` | `True` | `COLLISION_HARNESS_V1` | hypothesis_approval_gate | **PARTIAL** | Declared harness identifier has no separate executable binding/package occurrence. |
| `editorial_discovery_program` | `1.0.0` | `False` | `EDITORIAL_DISCOVERY_HARNESS_V1` | editorial_production_selection_gate, candidate_lock_gate, downstream_eligibility_gate | **PARTIAL** | Program manifest is valid but no canonical runtime state machine is registered. Declared harness identifier has no separate executable binding/package occurrence. |
| `editorial_storyboard_program` | `1.0.0` | `True` | `EDITORIAL_HARNESS_V1` | storyboard_editorial_approval | **PARTIAL** | Declared harness identifier has no separate executable binding/package occurrence. |
| `guest_genesis_semantic_territory_program` | `1.0.0` | `False` | `GUEST_GENESIS_HARNESS_V1` | territory_ratification_gate | **PARTIAL** | Program manifest is valid but no canonical runtime state machine is registered. Declared harness identifier has no separate executable binding/package occurrence. |
| `interview_semantic_program` | `1.0.0` | `True` | `INTERVIEW_HARNESS_V1` | guest_consent_gate, brief_operator_authorization_gate, evidence_authentication_gate | **PARTIAL** | Declared harness identifier has no separate executable binding/package occurrence. |
| `knowledge_cluster_signal_program` | `1.0.0` | `True` | `KNOWLEDGE_CLUSTER_HARNESS_V1` | projection_commitment_gate | **PARTIAL** | Declared harness identifier has no separate executable binding/package occurrence. |
| `knowledge_compiler_program` | `1.0.0` | `True` | `KNOWLEDGE_COMPILER_HARNESS_V1` | database_projection_commit_gate, rebuild_projection_authorization_gate | **PARTIAL** | Declared harness identifier has no separate executable binding/package occurrence. |
| `preparation_graph_program` | `1.0.0` | `False` | `PREPARATION_GRAPH_HARNESS_V1` | operator_preparation_approval | **PARTIAL** | Program manifest is valid but no canonical runtime state machine is registered. Declared harness identifier has no separate executable binding/package occurrence. |
| `release_ship_outcome_program` | `1.0.0` | `True` | `RELEASE_SHIP_OUTCOME_HARNESS_V1` | — | **PARTIAL** | Declared harness identifier has no separate executable binding/package occurrence. |
| `research_canonicalization_program` | `1.0.0` | `True` | `RESEARCH_CANONICALIZATION_HARNESS_V1` | contradiction_adjudication_gate, canonical_knowledge_commit_gate | **PARTIAL** | Declared harness identifier has no separate executable binding/package occurrence. |
| `script_program` | `1.0.0` | `True` | `SCRIPT_HARNESS_V1` | final_script_operator_approval_gate | **PARTIAL** | Declared harness identifier has no separate executable binding/package occurrence. |
| `vae_delegation_program` | `1.0.0` | `True` | `VAE_DELEGATION_HARNESS_V1` | delegation_acknowledgement_gate | **PARTIAL** | Declared harness identifier has no separate executable binding/package occurrence. |
| `video_edit_program` | `1.0.0` | `True` | `VIDEO_EDIT_PRODUCTION_HARNESS_V1` | video_release_authorization_gate | **PARTIAL** | Declared harness identifier has no separate executable binding/package occurrence. |
| `visual_derivative_production_program` | `1.0.0` | `True` | `VISUAL_DERIVATIVE_PRODUCTION_HARNESS_V1` | derivative_release_authorization_gate | **WORKING** |  |
| `visual_prompt_annotation_program` | `1.0.0` | `True` | `VISUAL_PROMPT_ANNOTATION_HARNESS_V1` | visual_package_approval_gate | **PARTIAL** | Declared harness identifier has no separate executable binding/package occurrence. |
| `workspace_guest_operating_context_program` | `1.0.0` | `True` | `WORKSPACE_GUEST_HARNESS_V1` | workspace_activation_gate | **PARTIAL** | Declared harness identifier has no separate executable binding/package occurrence. |

## Minimal real product-run probe

The probe enters through the existing operator command dispatcher, uses the existing `ProgramOperatorRuntimeService`, and persists state into a temporary `SqliteProgramStateStore`. It then exercises the existing gate evaluator and the existing `/ship` command refusal.

```json
{
  "aggregate_id": "prog-state:9e8d1e7c-c986-455c-998f-2d31b7f46597:research_canonicalization_program:run_cd179ae936904276",
  "db_path": "C:\\Users\\Mitano\\AppData\\Local\\Temp\\cae_m0058_d8mupfym\\m0058.sqlite3",
  "dispatch_persistence": {
    "lease": {
      "acquired_at": "2026-09-09T21:00:48.182854Z",
      "aggregate_id": "prog-state:9e8d1e7c-c986-455c-998f-2d31b7f46597:research_canonicalization_program:run_cd179ae936904276",
      "enqueued_at": "2026-09-09T21:00:48.057017Z",
      "holder_id": "m0058-probe-operator",
      "lease_id": "lease_0690da651eb32f33a3e4dd9a",
      "lease_version": 1,
      "status": "LEASE_ACQUIRED",
      "updated_at": "2026-09-09T21:00:48.182854Z"
    },
    "lease_present": true,
    "transition_count_after_dispatch": 0,
    "workflow_dispatch": {
      "actor_id": "m0058-probe-operator",
      "aggregate_id": "prog-state:9e8d1e7c-c986-455c-998f-2d31b7f46597:research_canonicalization_program:run_cd179ae936904276",
      "context_state_hash": "6f23eeebbea7b6bf3edacfcca4a835f33497f1bcfb07afa0128bfcda8d946ed3",
      "enqueued_at": "2026-09-09T21:00:48.182854Z",
      "lease_id": "lease_0690da651eb32f33a3e4dd9a",
      "payload": {
        "aggregate_id": "prog-state:9e8d1e7c-c986-455c-998f-2d31b7f46597:research_canonicalization_program:run_cd179ae936904276",
        "context_claims": [
          "false_merge_verified",
          "sources_verified",
          "workspace_active"
        ],
        "context_state_hash": "6f23eeebbea7b6bf3edacfcca4a835f33497f1bcfb07afa0128bfcda8d946ed3",
        "program_id": "research_canonicalization_program",
        "program_version": "1.0.0"
      },
      "status": "ENQUEUED",
      "trigger_operation": "cae.program.dispatch@1.0.0"
    },
    "workflow_dispatch_present": true
  },
  "gate": {
    "audit_digest": "c3fb664e92a51d6ad52cd1af64b6990d0039c39c0b4e79503745e6a2cd5903e3",
    "current_state": "INITIAL",
    "gate_id": "canonical_knowledge_commit_gate",
    "lifecycle": "AWAITING_APPROVAL",
    "receipt_id": "rcpt_gate_0f39a8a20fbf27130daeb514",
    "state_version": 2,
    "suspension_present": true
  },
  "persistence_recheck": {
    "aggregate_present": true,
    "same_state_hash": true,
    "transition_count": 1
  },
  "release": {
    "blocked_after_gate": true,
    "message": "Cannot ship program in state 'INITIAL' (lifecycle: AWAITING_APPROVAL). Must be COMPLETED.",
    "success": false
  },
  "run": {
    "current_state": "INITIAL",
    "last_receipt_id": "rcpt_dispatch_fae86a30b66917e8bae5c694",
    "lifecycle": "RUNNING",
    "message": "Program 'research_canonicalization_program' started successfully. Aggregate: prog-state:9e8d1e7c-c986-455c-998f-2d31b7f46597:research_canonicalization_program:run_cd179ae936904276",
    "state_version": 1,
    "success": true
  },
  "trace": {
    "allowable_transitions": [
      "attach_sources"
    ],
    "blockers": [
      "Program reached HUMAN_GATE 'canonical_knowledge_commit_gate'. Awaiting COMMANDER approval; downstream execution is blocked."
    ],
    "current_state": "INITIAL",
    "trace_node_count": 1,
    "version": 2
  },
  "workspace_id": "9e8d1e7c-c986-455c-998f-2d31b7f46597"
}
```

## Stateful behavior evidence

### Operator-mediated Program dispatch
- Source → operation → target: `ABSENT` → `dispatch_chat_command('/run research_canonicalization_program') → run_program → register_program_dispatch → acquire_execution_lease_and_trigger` → `INITIAL`
- Actor: `m0058-probe-operator / COMMANDER`
- Preconditions: `workspace_active`, `sources_verified`, `false_merge_verified`
- Validators: `ProgramRegistry preflight`, `canonical Program State Machine lookup`, `lease CAS`
- Postconditions: `aggregate persisted`, `lease record present`, `workflow dispatch record present`
- Receipt: `rcpt_dispatch_fae86a30b66917e8bae5c694`
- Error route: Dispatch/lease errors leave the aggregate in the durable pre-run path; no synthetic RUNNING state is manufactured.
- Recovery: Use existing operator control paths (inspect, pause/resume, repair) according to the aggregate lifecycle; no M0058 repair is introduced.

### Human gate suspension
- Source → operation → target: `INITIAL` → `evaluate_gate_milestone('canonical_knowledge_commit_gate')` → `INITIAL`
- Actor: `m0058-gate-evaluator / COMMANDER`
- Preconditions: `gate is declared by Program manifest`, `aggregate lifecycle is RUNNING`
- Validators: `declared-gate lookup`, `RUNNING lifecycle check`, `durable CAS/state write`
- Postconditions: `AWAITING_APPROVAL lifecycle`, `GateSuspensionSnapshot persisted`, `gate receipt persisted`
- Receipt: `rcpt_gate_0f39a8a20fbf27130daeb514`
- Error route: Undeclared gate or non-RUNNING lifecycle raises ProgramTransitionBlockedError.
- Recovery: Existing operator approve/reject route; downstream transitions remain fail-closed while awaiting approval.

## Blocker register

| ID | Class | Finding | Required authority/action |
| --- | --- | --- | --- |
| `B-M0058-RUNTIME-001` | `STATE_ERROR` | Existing M71 golden-run tests expect operator.run_program to return version 2, but the current runtime returns version 1 in this sandbox. | Correct runtime/test authority requires a separate repair decision; M0058 records but does not modify it. |
| `B-M0058-HARNESS-001` | `RELATION_ERROR` | research_canonicalization_program declares RESEARCH_CANONICALIZATION_HARNESS_V1, but the representative operator path does not bind/execute that harness. | Program/Harness integration owner; do not invent a new adapter under M0058. |
| `B-M0058-AUTH-001` | `AUTHORITY_ERROR` | The representative Program manifest declares a PostgreSQL research connection while the verified local state path uses SQLite; authority must remain explicitly separated rather than inferred from the connection field. | Change/promotion authority/operator gate. |
| `B-M0058-PROOF-001` | `EVIDENCE_ERROR` | A green M057 proof or M71 benchmark count alone cannot prove a full product campaign; the representative run must reach the intended runtime and state boundary. | M0058 verifier; require EXECUTABLE evidence for reachability. |

## Verification boundary

**What the verifier measures:** the concrete operator dispatch, state persistence, gate suspension, trace projection, and fail-closed release refusal observed in this sandbox; package manifest/runtime-state-machine reachability; and declared-to-executable call-path relationships.

**What it does not measure:** production PostgreSQL connectivity, external media retrieval, a production inference provider, a native OpenChatCut process, human approval quality, or the exact Git commit of the uploaded archive when `.git` metadata is absent.

**False-proof countercase:** All selected tests could be green while only dispatching an aggregate and never executing the intended five-transition research lifecycle. The existing M71 benchmark counts a successful command dispatch as a successful run, then uses max(1, transition_count) for phases/receipts. M0058 defeats that false proof by requiring an observed aggregate, durable state, gate suspension, trace projection, and release refusal.

**Environment-fidelity requirement:** The verifier's SQLite path is executable in this sandbox, but production-readiness claims require the governed repository environment, including the recorded Python 3.12 toolchain and all optional runtime dependencies. PostgreSQL, live provider, external distribution, and native media execution are outside this proof.

**Operator validation required:** `True`. The mandate's final disposition is an operator decision, not an automated pass.

## Stop state

This baseline does not repair the observed blockers. M0058 ends at the operator gate.
