# CCP Studio Ontology Architecture

This folder is the canonical planning surface for Contract Convergence and Registry Consolidation.

## Source-of-truth sequence

1. `MASTER_ONTOLOGY.md`
2. `MASTER_GLOSSARY.json`
3. `MASTER_GLOSSARY.csv`
4. `INTEGRATION_MATRIX.csv`
5. `CONTRACT_CONVERGENCE_PLAN.md`
6. `REGISTRY_CONSOLIDATION_PLAN.md`
7. `CANONICAL_CREATIVE_PIPELINE_DOCTRINE.md`
8. `CANONICAL_CONTRACT_PATHS.md`
9. `ADR-001-CONTRACT-CONVERGENCE-AND-REGISTRY-CONSOLIDATION.md`
10. `BASELINE_VERIFICATION.md`

## Runtime contracts

The executable Pydantic contracts live in:

- `src/ccp_studio/contracts/ontology.py`
- `src/ccp_studio/contracts/primitive_coalition.py`
- `src/ccp_studio/contracts/frame_profiles.py`
- `src/ccp_studio/contracts/style_routes.py`
- `src/ccp_studio/contracts/creative_ingredients.py`
- `src/ccp_studio/contracts/visual_preproduction.py`
- `src/ccp_studio/contracts/registry_consolidation.py`

## Hard integration rule

No component should introduce a new concept without adding or mapping an `OntologyTerm`.
No registry should remain active without a canonical namespace or crosswalk entry.
No frozen V1 contract path should move without a migration ADR.
