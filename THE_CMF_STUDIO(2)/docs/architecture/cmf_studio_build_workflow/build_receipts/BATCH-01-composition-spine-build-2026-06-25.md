---
title: "Batch 1 Composition Spine Build Receipt"
status: "implemented"
implemented_at: "2026-06-25"
batch: "Batch 1 - Composition Spine and Primitive-Gated Runtime Contracts"
specs:
  - "TS-CMF-072"
  - "TS-CMF-073"
  - "TS-CMF-074"
  - "TS-CMF-075"
  - "TS-CMF-076"
  - "TS-CMF-078"
  - "TS-CMF-079"
  - "TS-CMF-080"
  - "TS-CMF-081"
  - "TS-CMF-082"
  - "TS-CMF-083"
  - "TS-CMF-084"
  - "TS-CMF-085"
  - "TS-CMF-086"
  - "TS-CMF-087"
  - "TS-CMF-088"
  - "TS-CMF-089"
  - "TS-CMF-090"
  - "TS-CMF-091"
  - "TS-CMF-092"
---

# Batch 1 Composition Spine Build Receipt

## Implemented Files

- `THE CMF STUDIO/src/ccp_studio/contracts/composition_runtime.py`
- `THE CMF STUDIO/src/ccp_studio/repositories/composition_runtime.py`
- `THE CMF STUDIO/src/ccp_studio/services/composition_runtime_service.py`
- `THE CMF STUDIO/src/ccp_studio/api/v1/composition_runtime.py`
- `THE CMF STUDIO/src/ccp_studio/generated/typescript/composition_runtime_contracts.ts`
- `THE CMF STUDIO/tests/cmf_studio/test_batch1_composition_runtime_spine.py`

## Runtime Coverage

- Scene-template runtime binding for reaction clips.
- Canonical composition JSON registry and approval receipts.
- Upper reaction UI / lower human cutout renderer props.
- Operator read models, eval suite, and approval receipts.
- Open-source adapter fit evaluation and sandboxed conversion.
- Four canonical short-video format runtime crosswalk.
- Route-specific visual-feel contracts using the registered CMF composition primitive triads.
- Brand Genesis substrate, expression lineage, and transcript beat-map binding.
- Template family registry and content asset code reservation.
- 64-state performance selection, PaperCut runtime manifest, and micro-semiotic risk gate.
- Ideogram 4 composition-direction bridge into downstream production templates.
- Qwen/SAM-style layer extraction result and repair queue contract.
- Renderer prop compiler and component harness.

## Verification

Commands run:

```powershell
python -m pytest "THE CMF STUDIO/tests/cmf_studio/test_batch1_composition_runtime_spine.py"
python -m pytest "THE CMF STUDIO/tests/cmf_studio/test_batch1_composition_runtime_spine.py" "THE CMF STUDIO/tests/cmf_studio/test_reaction_editing_template_routing.py" "THE CMF STUDIO/tests/cmf_studio/test_doctrine_test_harness.py" "THE CMF STUDIO/tests/cmf_studio/test_doctrine_and_primitive_evals.py" "THE CMF STUDIO/tests/cmf_studio/test_ideogram_4_compositionjob_lineage.py"
python -m pytest "THE CMF STUDIO/tests/cmf_studio" -k "composition or reaction or doctrine or primitive or beat_map or papercut or ideogram"
python -m pytest "THE CMF STUDIO/tests/cmf_studio"
```

Results:

- Batch 1 spine test: 7 passed.
- Batch 1 target suite: 32 passed.
- Batch 1 broad composition/reaction/doctrine filter: 38 passed, 428 deselected.
- Full CMF Studio regression: 464 passed, 2 skipped.

## Exit Criteria Status

- Pydantic contracts validate.
- Composition JSON is canonical and preview refs are evidence only.
- Reaction, PaperCut, Ideogram bridge, and open-source adapter paths emit structured receipts.
- Primitive triads load from `registries/evals/composition/cmf_composition_primitive_triads.v1.json`.
- Transcript beat maps compile into timeline cues.
- Operator read model exposes evidence, blockers, eval suite refs, and approval state.
- Existing reaction routing, doctrine harness, primitive evals, and Ideogram lineage anchors still pass.
