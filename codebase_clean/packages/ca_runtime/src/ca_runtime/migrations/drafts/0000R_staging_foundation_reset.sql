-- STATUS: APPLIED_STAGING
-- DO NOT EXECUTE DIRECTLY OUTSIDE AN AUTHORIZED APPLICATION MANDATE
-- Migration ID: MIG-0000R
-- Title: CAE Staging Foundation Reset (Enumerated Empty WP-era Relations)
-- Predecessor: NONE
-- Preconditions: All slated relations verified empty (0 rows); PostgreSQL >= 15.0
-- Data Action Class: SCHEMA_RESET_EMPTY_OBJECTS_ONLY
-- Governing Mandate: CA-TWC-01 (Sub-workstream T1)

-- Drop only the enumerated proven-empty WP-era relations in dependency order
DROP TABLE IF EXISTS cae.assessment_evidence_link CASCADE;
DROP TABLE IF EXISTS cae.evidence_authentication CASCADE;
DROP TABLE IF EXISTS cae.evidence_span CASCADE;
DROP TABLE IF EXISTS cae.evidence_item CASCADE;
DROP TABLE IF EXISTS cae.interview_turn CASCADE;
DROP TABLE IF EXISTS cae.interview_session CASCADE;
DROP TABLE IF EXISTS cae.legacy_import_record CASCADE;
DROP TABLE IF EXISTS cae.legacy_import_run CASCADE;
DROP TABLE IF EXISTS cae.source_package CASCADE;
DROP TABLE IF EXISTS cae.event CASCADE;
DROP TABLE IF EXISTS cae.state_transition CASCADE;
DROP TABLE IF EXISTS cae.state_aggregate CASCADE;
DROP TABLE IF EXISTS cae.command CASCADE;
DROP TABLE IF EXISTS cae.semantic_assessment CASCADE;
DROP TABLE IF EXISTS cae.receipt_evidence_link CASCADE;
DROP TABLE IF EXISTS cae.receipt CASCADE;
DROP TABLE IF EXISTS cae.harness_run CASCADE;
DROP TABLE IF EXISTS cae.harness_template CASCADE;
DROP TABLE IF EXISTS cae.media_asset CASCADE;
DROP TABLE IF EXISTS cae.engagement CASCADE;
DROP TABLE IF EXISTS cae.operator_access_grant CASCADE;
DROP TABLE IF EXISTS cae.operator_organization CASCADE;
DROP TABLE IF EXISTS cae.guest CASCADE;
DROP TABLE IF EXISTS cae.workspace_membership CASCADE;
DROP TABLE IF EXISTS cae.project CASCADE;
DROP TABLE IF EXISTS cae.actor CASCADE;
DROP TABLE IF EXISTS cae.workspace CASCADE;
DROP TABLE IF EXISTS cae.execution_receipt CASCADE;
DROP TABLE IF EXISTS cae.legacy_wp03_workspace CASCADE;
DROP TABLE IF EXISTS cae.legacy_wp03_media_asset CASCADE;
DROP TABLE IF EXISTS cae.legacy_wp03_execution_receipt CASCADE;

-- Drop legacy trigger functions if present
DROP FUNCTION IF EXISTS cae.fn_prevent_receipt_mutation() CASCADE;
DROP FUNCTION IF EXISTS cae.fn_prevent_execution_receipt_mutation() CASCADE;
