# Visual Compute, ComfyUI, Models, and LoRA

## Why this belongs in the product

Visual production will occur through custom ComfyUI and other visual-model workflows hosted in controlled Docker/GPU environments and invoked through APIs. The product therefore needs explicit capabilities for:

- workflow graph compilation;
- model and VAE compatibility;
- LoRA/adaptation stacking;
- ControlNet, IP-Adapter, masks, pose/depth/edge and regional conditioning;
- custom-node dependency locking;
- local and cloud GPU routing;
- model mounting and caching;
- queueing, cancellation, health, timeout and failover;
- reproducibility and cost receipts.

## Architecture boundary

The PRD does not select:

- a cloud vendor;
- a Kubernetes or queue implementation;
- a base image/model/VLM;
- a database or object store;
- exact ComfyUI nodes;
- exact LoRA-training framework.

Architecture must choose these through representative proof and compatibility constraints.

## Provider-neutral compilation

```text
Visual Asset Demand
→ Visual Production Plan IR
→ capability resolution
→ Production Binding
→ ComfyUI/provider graph
→ runtime job
→ evaluation graph
→ repair graph
→ delivery
```

The provider graph is disposable and regenerable. The plan and contracts preserve product meaning.

## LoRA capability development

LoRA training is a governed reusable-capability workflow, not an ordinary repair:

```text
recurring capability gap
→ evidence sufficiency
→ dataset contract
→ sandbox preparation
→ training
→ control comparison
→ VLM and regression evaluation
→ experimental registry
→ shadow
→ limited production
→ production
```

Release 1 should prove one identity or visual-language adaptation useful to Format 02, but must not attempt a universal LoRA factory.

## Operator proficiency implications

The future Manual Course should teach:

- ComfyUI graphs and API execution;
- base model, VAE, text encoder, LoRA and control relationships;
- Docker/GPU runtime mental models;
- VRAM, caching, cold starts and cost;
- workflow and custom-node versioning;
- how to read production/evaluation receipts;
- how capability-development evidence differs from ordinary candidate exploration.
