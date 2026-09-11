-- STATUS: APPLIED_STAGING
-- DO NOT EXECUTE DIRECTLY OUTSIDE AN AUTHORIZED APPLICATION MANDATE
-- Migration ID: MIG-0001
-- Title: Initialize Extensions and CAE Schema
-- Predecessor: NONE
-- Preconditions: PostgreSQL >= 15.0; User has CREATE privilege on database
-- Data Action Class: SCHEMA_ONLY_NO_DML
-- Governing Phase: CA-MIG-03

CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE SCHEMA IF NOT EXISTS cae;
