# Conscious Activations — Phase 1 Development Foundation

Phase 1 creates the shared application foundation for the new product roots.

## Included

- `activative-production-spine@0.1.0-dev.1` language-neutral contract snapshot;
- generated Python and TypeScript declarations;
- strict canonical JSON and contract validation;
- shared SQLite development runtime;
- AIR, AHP, and Interview Expression Python shells;
- Conscious Activations Studio TypeScript shell;
- deterministic bootstrap, health, and validation commands;
- development-only receipts and tests.

## Not included

Phase 1 does not implement semantic activation, Harness scheduling, interview analysis,
composition, media rendering, VAE Stage 5, GNM, cloud infrastructure, production,
certification, or Format 02 activation.

## Quick start

```bash
python scripts/phase1/install_workspace.py --venv .venv-phase1
.venv-phase1/bin/python scripts/phase1/bootstrap_products.py --data-root .conscious-activations/dev
.venv-phase1/bin/python scripts/phase1/validate_phase1.py
```

On Windows use `.venv-phase1\\Scripts\\python.exe`.
