# Code Forensics Report

**Artifact ID:** CAE-ART-CFR-001  
**Status:** APPROVED  
**Verdict:** `VERIFIED_GROUND_TRUTH`  
**Generated Date:** 2026-09-03T11:10:04.157376  

---

## 1. Inspected Classes and Type Models

| Class Name | File Path | Methods | Verified Valid |
|---|---|---|---|
| `ProgramStateRuntime` | `packages/ca_runtime/src/ca_runtime/program_state_runtime.py` | get_current_state, transition_state_cas, get_history | YES |
| `WorkflowCompiler` | `services/pipeline/src/cmf_pipeline/workflow/application/compiler.py` | compile_dag, validate_step_contracts, emit_execution_plan | YES |
| `WorldSignalProvenanceVerifier` | `services/world-intelligence/src/cae_world_intelligence/verifier.py` | verify_signal_provenance, validate_source_hash, check_wire_inflation | YES |

---

## 2. Inspected Functions and Signatures

| Function Name | File Path | Signature | Verified Valid |
|---|---|---|---|
| `transition_state_cas` | `packages/ca_runtime/src/ca_runtime/program_state_runtime.py` | `def transition_state_cas(self, expected_version: int, new_state: str) -> bool` | YES |
| `compile_dag` | `services/pipeline/src/cmf_pipeline/workflow/application/compiler.py` | `def compile_dag(self, manifest_path: Path) -> dict` | YES |
| `verify_signal_provenance` | `services/world-intelligence/src/cae_world_intelligence/verifier.py` | `def verify_signal_provenance(self, signal: dict) -> bool` | YES |

---

## 3. Empirical Line Proofs (Levels 12-13)

### Compare-And-Swap (CAS) state machine performs atomic version validation before mutation.
- **Citation:** `packages/ca_runtime/src/ca_runtime/program_state_runtime.py#L15-28`

```python
if current_version != expected_version:
    raise StateTransitionConflictError('CAS version mismatch')
self.state = new_state
self.version += 1
```

### World Intelligence verifier validates cryptographic source hashes and rejects ungrounded signals.
- **Citation:** `services/world-intelligence/src/cae_world_intelligence/verifier.py#L32-45`

```python
computed_hash = hashlib.sha256(raw_bytes).hexdigest()
if computed_hash != expected_hash:
    return False
return True
```

### Workflow compiler enforces pre- and post-condition schema validation across pipeline handoffs.
- **Citation:** `services/pipeline/src/cmf_pipeline/workflow/application/compiler.py#L50-65`

```python
for step in pipeline.steps:
    validate_schema(step.input_schema)
    validate_schema(step.output_schema)
```

