# VAE Delegation + Visual Asset Runtime Instructions

## Overview
The `vae_delegation_program` executes the governed receipt-driven delegation bridge between the Content Harness Pipeline and the Visual Asset Editor (VAE) for real `AssetAnnotation` demands.

## Operational Workflow
1. **Admit Visual Demand (`COMMANDER`):**
   - Ingest provider-neutral `VisualAssetDemandContract`.
   - Verify non-synthetic status, quote hashes, and wrong-reading locks.
2. **Compile Production Plan (`HUNTER`):**
   - Resolve dynamic workcell and stage bindings (`sam3-segmentation`, `lucida-matting`, `gnm-geometry`, `comfyui-flux`).
   - Store immutable `VAEProductionPlanRecord`.
3. **Generate Visual Asset (`COMPOSER`):**
   - Execute provider stages and compile ComfyUI generation graph.
   - Materialize candidate artifact in Content-Addressed Store.
4. **Evaluate Technical Quality & Dual-Axis QA (`ANALYST`):**
   - Verify negative space, source fidelity, and wrong-reading locks.
   - Validate dual-axis semantic narrative fit.
   - Package provider-neutral `AssetResult` (ensuring no consumption authority is asserted).
5. **Acknowledge Result & Emit Cryptographic Receipt (`COMMANDER`):**
   - Validate VAE result against delegation contract specifications.
   - Issue authoritative `ResultAcknowledgement` and cryptographic `DelegationReceipt`.
