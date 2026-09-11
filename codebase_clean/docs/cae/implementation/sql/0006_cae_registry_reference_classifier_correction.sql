-- WP-04 forward-only correction: retain v1 reference rows but mark false
-- primitive self-reference classifications as invalid. No evidence is updated
-- or deleted; callers use this disposition when resolving references.

CREATE TABLE cae.registry_reference_disposition (
  registry_reference_disposition_id text PRIMARY KEY,
  registry_reference_id text NOT NULL UNIQUE REFERENCES cae.registry_reference(registry_reference_id),
  disposition text NOT NULL CHECK (disposition IN ('INVALID_CLASSIFICATION')),
  rationale text NOT NULL,
  classifier_version text NOT NULL,
  recorded_at timestamptz NOT NULL DEFAULT now()
);

CREATE TRIGGER cae_00_registry_reference_disposition_immutable
  BEFORE UPDATE OR DELETE ON cae.registry_reference_disposition
  FOR EACH ROW EXECUTE FUNCTION cae.reject_immutable_registry_mutation();

ALTER TABLE cae.registry_reference_disposition ENABLE ROW LEVEL SECURITY;

INSERT INTO cae.registry_reference_disposition(
  registry_reference_disposition_id, registry_reference_id, disposition,
  rationale, classifier_version
)
SELECT
  'cae:registry-reference-disposition:' || substr(encode(extensions.digest(reference.registry_reference_id, 'sha256'), 'hex'), 1, 32),
  reference.registry_reference_id,
  'INVALID_CLASSIFICATION',
  'Primitive source documents may state their own identity; that is not a declared registry crosswalk.',
  'cae-wp04-reference-classifier/2.0.0'
FROM cae.registry_reference reference
JOIN cae.registry_item item ON item.registry_item_id = reference.source_registry_item_id
WHERE item.source_registry = 'air-primitive-registry'
  AND item.source_id = 'EXP-TRG-001'
  AND reference.relation_type = 'PRIMITIVE_ID'
  AND reference.target_id = 'EXP-TRG-001';
