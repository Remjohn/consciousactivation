-- WP-04 forward-only classifier correction. Primitive source documents are
-- immutable evidence, not a declared crosswalk namespace. Preserve each v1
-- row and append an invalid-classification disposition instead of deleting it.

INSERT INTO cae.registry_reference_disposition(
  registry_reference_disposition_id, registry_reference_id, disposition,
  rationale, classifier_version
)
SELECT
  'cae:registry-reference-disposition:' || substr(encode(extensions.digest(reference.registry_reference_id, 'sha256'), 'hex'), 1, 32),
  reference.registry_reference_id,
  'INVALID_CLASSIFICATION',
  'AIR Primitive YAML embedded identity fields are source evidence, not declared registry crosswalks.',
  'cae-wp04-reference-classifier/2.0.0'
FROM cae.registry_reference reference
JOIN cae.registry_item item ON item.registry_item_id = reference.source_registry_item_id
WHERE item.source_registry = 'air-primitive-registry'
ON CONFLICT (registry_reference_id) DO NOTHING;
