# Atomic Harness Pipeline contracts

The Pipeline consumes the exact shared Program Control contract pin in `SHARED_CONTRACT_PIN.yaml` and adds 16 closed, product-local Phase 3 schema families under `schemas/`.

These schemas define Pipeline-owned execution projections, bindings, batches, Workflow Nodes, JIT Capsules, invalidation, assurance and candidate portfolios. They do not transfer ownership of AIR, Interview Expression, Builder, VAE, Delegation or Studio objects.

Run:

```bash
python -m cmf_pipeline export-schemas ./phase3-schemas --json
```

The export is deterministic and includes `CONTRACT_REGISTRY.json` plus all 16 schema files.
