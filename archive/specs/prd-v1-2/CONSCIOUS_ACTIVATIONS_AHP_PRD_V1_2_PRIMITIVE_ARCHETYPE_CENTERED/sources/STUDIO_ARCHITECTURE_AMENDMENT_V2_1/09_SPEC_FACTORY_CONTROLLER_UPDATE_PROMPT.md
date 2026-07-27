# Spec Factory Controller Update Prompt — V2.1

Apply this amendment before continuing the Full Product Spec Factory V2.

## Required changes

1. Mark Format 02 runtime and UI specs as
   `DEFERRED_AWAITING_FORMAT02_HARNESS`.
2. Do not write or implement those specs until a current validated Harness exists.
3. Add the Human Resolution, Autonomy, Revision Compiler, Studio Plugin Registry, and
   Timeline Adoption specs listed in `08_SPEC_INVENTORY_AMENDMENTS.csv`.
4. Replace the current VideoTimelineWorkbench reuse disposition:
   - reuse shell, route, API patterns, review concepts and styling only where valuable;
   - archive the nonfunctional timeline panel;
   - run the bounded timeline-foundation adoption spike.
5. Amend every Studio interaction spec so every human resolution emits a
   `HumanResolutionEpisode`.
6. Amend every category Studio so the Harness executes by default and operator
   interaction is supervision/correction, not primary manual production.
7. Add category-specific Revision Compiler Programmed Model claims.
8. Add Dokploy deployment specifications for GCP/AWS and a worker-registration boundary.
9. Recompute the canonical raw and final spec inventory.
10. Release implementation lanes continuously after the amended Gate-A specs pass.

## Exact output

```text
CANONICAL_SPEC_RECONCILIATION_LEDGER_V2_1.csv
ACTIVE_SPEC_QUEUE_V2_1.yaml
DEFERRED_SPEC_QUEUE_V2_1.yaml
STUDIO_SURFACE_REGISTRY.yaml
HUMAN_RESOLUTION_EPISODE.schema.json
CHANGE_REQUEST_PROGRAM.schema.json
TIMELINE_FOUNDATION_DECISION_RECEIPT.yaml
DEPLOYMENT_TOPOLOGY.yaml
```
