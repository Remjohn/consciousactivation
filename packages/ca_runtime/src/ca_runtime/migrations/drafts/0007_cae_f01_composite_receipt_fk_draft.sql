-- STATUS: DRAFT_NOT_APPLIED
-- DO NOT EXECUTE DIRECTLY OUTSIDE AN AUTHORIZED APPLICATION MANDATE
-- Migration ID: MIG-0007
-- Title: Technical Finding F-01 Composite Foreign Key Lineage Repair
-- Predecessor: MIG-0006
-- Preconditions: MIG-0006 applied; preflight sweep confirms zero cross-workspace evidence links
-- Data Action Class: SCHEMA_CONSTRAINT_REPAIR_NO_DML
-- Governing Phase: CA-INT-05 (F-01 Structural Integrity Repair)

-- 1. Drop existing single-column FK constraints if present
ALTER TABLE cae.receipt_evidence_link 
    DROP CONSTRAINT IF EXISTS fk_receipt;

ALTER TABLE cae.receipt_evidence_link 
    DROP CONSTRAINT IF EXISTS receipt_evidence_link_receipt_id_fkey;

-- 2. Add multi-tenant composite foreign key constraint
ALTER TABLE cae.receipt_evidence_link 
    ADD CONSTRAINT fk_workspace_receipt
    FOREIGN KEY (workspace_id, receipt_id) 
    REFERENCES cae.receipt(workspace_id, receipt_id) 
    ON DELETE RESTRICT;
