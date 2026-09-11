-- WP-03A: retain canonical command/event/receipt bytes alongside their hashes.
-- Preconditions: no command/event/receipt rows have been imported or written.

ALTER TABLE cae.command
  ADD COLUMN payload_canonical_json text NOT NULL,
  ADD COLUMN payload jsonb NOT NULL;

ALTER TABLE cae.event
  ADD COLUMN payload_canonical_json text NOT NULL,
  ADD COLUMN payload jsonb NOT NULL;

ALTER TABLE cae.receipt
  ADD COLUMN payload_canonical_json text NOT NULL,
  ADD COLUMN payload jsonb NOT NULL,
  ADD COLUMN payload_sha256 text NOT NULL CHECK (payload_sha256 ~ '^[a-f0-9]{64}$');

CREATE OR REPLACE FUNCTION cae.verify_immutable_payload()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = cae, extensions, pg_temp
AS $$
DECLARE
  supplied_hash text;
  computed_hash text;
  decoded_payload jsonb;
BEGIN
  IF NEW.payload_canonical_json IS NULL OR NEW.payload IS NULL THEN
    RAISE EXCEPTION 'canonical payload bytes and JSONB projection are required';
  END IF;
  BEGIN
    decoded_payload := NEW.payload_canonical_json::jsonb;
  EXCEPTION WHEN invalid_text_representation THEN
    RAISE EXCEPTION 'payload_canonical_json is not valid JSON';
  END;
  IF decoded_payload <> NEW.payload THEN
    RAISE EXCEPTION 'payload JSONB does not equal canonical payload bytes';
  END IF;
  supplied_hash := to_jsonb(NEW) ->> TG_ARGV[0];
  computed_hash := encode(digest(convert_to(NEW.payload_canonical_json, 'UTF8'), 'sha256'), 'hex');
  IF supplied_hash IS DISTINCT FROM computed_hash THEN
    RAISE EXCEPTION 'payload hash does not match canonical payload bytes';
  END IF;
  RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION cae.reject_immutable_evidence_mutation()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  RAISE EXCEPTION 'CAE immutable evidence table % cannot be %', TG_TABLE_NAME, TG_OP;
END;
$$;

CREATE TRIGGER cae_10_command_payload_integrity
  BEFORE INSERT OR UPDATE ON cae.command
  FOR EACH ROW EXECUTE FUNCTION cae.verify_immutable_payload('payload_sha256');
CREATE TRIGGER cae_10_event_payload_integrity
  BEFORE INSERT OR UPDATE ON cae.event
  FOR EACH ROW EXECUTE FUNCTION cae.verify_immutable_payload('payload_sha256');
CREATE TRIGGER cae_10_receipt_payload_integrity
  BEFORE INSERT OR UPDATE ON cae.receipt
  FOR EACH ROW EXECUTE FUNCTION cae.verify_immutable_payload('payload_sha256');

CREATE TRIGGER cae_00_command_immutable
  BEFORE UPDATE OR DELETE ON cae.command
  FOR EACH ROW EXECUTE FUNCTION cae.reject_immutable_evidence_mutation();
CREATE TRIGGER cae_00_event_immutable
  BEFORE UPDATE OR DELETE ON cae.event
  FOR EACH ROW EXECUTE FUNCTION cae.reject_immutable_evidence_mutation();
CREATE TRIGGER cae_00_receipt_immutable
  BEFORE UPDATE OR DELETE ON cae.receipt
  FOR EACH ROW EXECUTE FUNCTION cae.reject_immutable_evidence_mutation();

