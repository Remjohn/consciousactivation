# Canonical Contract Paths

Status: frozen V1

These paths are the canonical V1 contract kernel for CMF Studio ontology, primitive coalition, frame profiles, style routes, visual preproduction, creative ingredients, and registry consolidation.

## Frozen V1 Paths

| Contract Area | Canonical Path |
|---|---|
| Ontology | `src/ccp_studio/contracts/ontology.py` |
| Primitive Coalition | `src/ccp_studio/contracts/primitive_coalition.py` |
| Frame Profiles | `src/ccp_studio/contracts/frame_profiles.py` |
| Style Routes | `src/ccp_studio/contracts/style_routes.py` |
| Visual Preproduction | `src/ccp_studio/contracts/visual_preproduction.py` |
| Creative Ingredients | `src/ccp_studio/contracts/creative_ingredients.py` |
| Registry Consolidation | `src/ccp_studio/contracts/registry_consolidation.py` |

## Freeze Rule

These paths must not be moved, renamed, or replaced without a migration ADR. Existing contracts may adapt into them through projection or wrapper services, but canonical V1 imports should stabilize around these paths.

## Adapter Rule

Legacy objects such as `PrimitiveTriadContract` remain valid while downstream modules migrate. They must be projected into canonical contracts, not deleted in-place.
