# Proposed Target File Tree

This tree is a target location plan, not an implementation allowlist. It is intentionally precise so implementation campaigns can assign ownership without recreating the predecessor monolith.

```text
04_ATOMIC_HARNESS_PIPELINE/
├── 00_ALIGNMENT_START_HERE.md
├── AGENTS.md
├── README.md
├── CURRENT_PROJECT_STATUS.md
├── PROGRAM_STATUS_EXPORT.yaml
├── pyproject.toml
├── uv.lock
├── docs/
│   ├── product-authority/CURRENT_AUTHORITY.md
│   ├── architecture/
│   ├── implementation/
│   └── operations/
├── prd/
├── governance/
├── contracts/
│   ├── harness_execution_binding_manifest.schema.json
│   ├── workflow_node_execution_request.schema.json
│   ├── workflow_node_execution_receipt.schema.json
│   ├── execution_stack_fingerprint.schema.json
│   ├── transformation_contract.schema.json
│   ├── composition_ir.schema.json
│   ├── timeline_ir.schema.json
│   ├── character_performance_program.schema.json
│   ├── programmed_model_artifact.schema.json
│   ├── learned_capability_claim.schema.json
│   ├── model_program_binding.schema.json
│   ├── retrieval_receipt.schema.json
│   ├── process_receipt.schema.json
│   └── incident_receipt.schema.json
├── src/cmf_pipeline/
│   ├── domain/
│   │   ├── harness_intake.py
│   │   ├── execution_binding.py
│   │   ├── workflow_node.py
│   │   ├── transformation_contract.py
│   │   ├── receipts.py
│   │   └── run_state.py
│   ├── application/
│   │   ├── execute_harness.py
│   │   ├── schedule_workflow.py
│   │   ├── resolve_capability.py
│   │   ├── compile_jit_context.py
│   │   ├── evaluate_result.py
│   │   └── repair_result.py
│   ├── workflow/
│   │   ├── scheduler.py
│   │   ├── checkpoints.py
│   │   ├── cancellation.py
│   │   ├── candidate_search.py
│   │   └── sandbox.py
│   ├── retrieval/
│   │   ├── eligibility.py
│   │   ├── lexical.py
│   │   ├── dense.py
│   │   ├── graph.py
│   │   ├── multimodal.py
│   │   ├── reranking.py
│   │   └── jit_compiler.py
│   ├── model_programs/
│   │   ├── registry.py
│   │   ├── resolver.py
│   │   ├── execution.py
│   │   ├── lifecycle.py
│   │   └── evidence.py
│   ├── evaluation/
│   │   ├── deterministic.py
│   │   ├── independent.py
│   │   ├── visual_syntax_reparse.py
│   │   ├── diagnosis.py
│   │   └── selective_repair.py
│   ├── adapters/
│   │   ├── builder/
│   │   ├── delegation/
│   │   ├── vae/
│   │   ├── runtimes/
│   │   └── legacy_cmf/
│   └── cli/
├── packages/
│   ├── cmf_render_contracts/
│   ├── cmf_composition_runtime/
│   ├── cmf_static_skia_runtime/
│   ├── cmf_video_editing_runtime/
│   ├── cmf_remotion_adapter/
│   ├── cmf_hyperframes_adapter/
│   ├── cmf_ffmpeg_adapter/
│   └── cmf_render_qa/
└── tests/
    ├── contracts/
    ├── domain/
    ├── workflow/
    ├── retrieval/
    ├── model_programs/
    ├── runtimes/
    ├── reference_slices/
    └── architecture/
```

## Visual Asset Editor target additions

```text
02_VISUAL_ASSET_EDITOR/
└── src/cmf_vae/adapters/
    ├── sam3/
    ├── lucida/
    ├── qwen_image_layered/
    └── provider_runtime/
```

PRETEXT and Rough Annotation Cue implementations belong in the composition/runtime packages, not in the VAE. SAM3 and Lucida belong behind VAE provider interfaces.
