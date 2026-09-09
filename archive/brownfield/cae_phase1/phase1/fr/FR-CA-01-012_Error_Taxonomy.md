# FR-CA-01-012 — Architecture Error Taxonomy

## Requirement
The engine SHALL classify failures structurally before repair.

## Minimum Categories
SCHEMA_ERROR, TAXONOMY_ERROR, RELATION_ERROR, STATE_ERROR, EVIDENCE_ERROR, ONTOLOGY_ERROR, PRIMITIVE_ERROR, COALITION_ERROR, SEMANTIC_DRIFT, FORMAT_DRIFT, COMPOSITION_ERROR, RUNTIME_ERROR, GOVERNANCE_ERROR, ANTI_CENTROID_ERROR.

## Acceptance Criteria
A repair workflow must receive a typed failure class and concrete diagnostic context rather than an unstructured retry instruction.
