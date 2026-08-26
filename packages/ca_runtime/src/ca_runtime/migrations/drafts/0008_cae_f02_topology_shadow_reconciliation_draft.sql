-- STATUS: DRAFT_NOT_APPLIED
-- DO NOT EXECUTE DIRECTLY OUTSIDE AN AUTHORIZED APPLICATION MANDATE
-- Migration ID: MIG-0008
-- Title: Technical Finding F-02 Staging Shadow Table Reconciliation
-- Predecessor: MIG-0007
-- Preconditions: MIG-0007 applied; operator approves legacy WP-03 table deprecation/aliasing
-- Data Action Class: SCHEMA_TOPOLOGY_REPAIR_NO_DML
-- Governing Phase: CA-MIG-03 (Candidate Draft for Future Application Phase)

-- Non-destructively rename legacy WP-03 tables to preserve historical records while clearing namespace
ALTER TABLE IF EXISTS cae.workspace RENAME TO legacy_wp03_workspace;
ALTER TABLE IF EXISTS cae.media_asset RENAME TO legacy_wp03_media_asset;
ALTER TABLE IF EXISTS cae.execution_receipt RENAME TO legacy_wp03_execution_receipt;
