# Phase 7 Receipts

## Phase7CompilationReceipt

```yaml
receipt_id:
program_id:
edge_product_id:
archetype_selection_id:
sfl_stack_id:
depth_profile_id:
input_state_refs: []
directive_set_id:
canonical_versions:
  archetype:
  sfl:
  sda:
selection_trace:
  rejected_archetypes: []
  rejected_sfl_functions: []
validation:
  archetype: pass
  sfl: pass
  edge_preservation: pass
  anti_centroid: pass
  semantic_program: pass
errors: []
operator:
agent_run_id:
timestamp:
```

## Receipt law

Receipts must answer:

> Why does this SemanticProgram exist, and what would have happened if the selected carrier or SFL stack had not been chosen?

Receipts preserve the chain:

```text
Edge
→ Archetype candidates
→ Selection
→ SFL stack
→ Depth profile
→ Directives
→ Validators
→ SemanticProgram
```
