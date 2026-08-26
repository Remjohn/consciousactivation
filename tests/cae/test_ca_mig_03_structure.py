"""
Pure local structure test for CA-MIG-03 Forward-Only Migration Design Artifacts.
Validates schema inventory, dependency graph, safety rehearsal, and SQL draft guards without DB/network.
"""

from __future__ import annotations

import re
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


def test_ca_mig_03_docs_exist_and_non_empty():
    required_docs = [
        "docs/cae/implementation/CAE_MIG_03_SCHEMA_INVENTORY.md",
        "docs/cae/implementation/CAE_MIG_03_FORWARD_MIGRATION_PLAN.md",
        "docs/cae/implementation/CAE_MIG_03_MIGRATION_DEPENDENCY_GRAPH.md",
        "docs/cae/implementation/CAE_MIG_03_SAFETY_REHEARSAL.md",
        "docs/cae/implementation/CAE_MIG_03_F01_F02_REPAIR_BOUNDARY.md",
        "docs/cae/implementation/CAE_MIG_03_COMPLETION_RECORD.md",
        "docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md",
    ]
    for rel_path in required_docs:
        full_path = ROOT_DIR / rel_path
        assert full_path.is_file(), f"Document missing: {rel_path}"
        assert full_path.stat().st_size > 400, f"Document too small: {rel_path}"


def test_sql_drafts_exist_and_guarded():
    drafts_dir = ROOT_DIR / "packages/ca_runtime/src/ca_runtime/migrations/drafts"
    expected_drafts = [
        "0001_cae_extensions_and_schema.sql",
        "0002_cae_tenancy_and_membership.sql",
        "0003_cae_engagement_guest_media.sql",
        "0004_cae_harness_and_immutable_receipts.sql",
        "0005_cae_row_level_security.sql",
        "0006_cae_indexes_and_constraints.sql",
        "0007_cae_f01_composite_receipt_fk_draft.sql",
        "0008_cae_f02_topology_shadow_reconciliation_draft.sql",
    ]
    for fname in expected_drafts:
        p = drafts_dir / fname
        assert p.is_file(), f"SQL draft missing: {fname}"
        content = p.read_text(encoding="utf-8")
        assert "-- STATUS: DRAFT_NOT_APPLIED" in content, f"Missing guard header in {fname}"


def test_foundation_drafts_non_destructive():
    drafts_dir = ROOT_DIR / "packages/ca_runtime/src/ca_runtime/migrations/drafts"
    foundation_drafts = [
        "0001_cae_extensions_and_schema.sql",
        "0002_cae_tenancy_and_membership.sql",
        "0003_cae_engagement_guest_media.sql",
        "0004_cae_harness_and_immutable_receipts.sql",
        "0005_cae_row_level_security.sql",
        "0006_cae_indexes_and_constraints.sql",
    ]
    for fname in foundation_drafts:
        content = (drafts_dir / fname).read_text(encoding="utf-8")
        cleaned = re.sub(r"\bDROP\s+(TRIGGER|POLICY|EXTENSION)\b", "", content, flags=re.IGNORECASE)
        assert not re.search(r"\bDROP\s+TABLE\b", cleaned, re.IGNORECASE), f"Destructive DROP TABLE in {fname}"
        assert not re.search(r"\bTRUNCATE\b", cleaned, re.IGNORECASE), f"Destructive TRUNCATE in {fname}"
        assert not re.search(r"\bDROP\s+SCHEMA\b", cleaned, re.IGNORECASE), f"Destructive DROP SCHEMA in {fname}"


def test_ten_point_no_go_checklist_present():
    safe_path = ROOT_DIR / "docs/cae/implementation/CAE_MIG_03_SAFETY_REHEARSAL.md"
    content = safe_path.read_text(encoding="utf-8")
    for i in range(1, 11):
        assert f"NOGO-{i:02d}" in content, f"Missing NOGO-{i:02d} in safety rehearsal"


def test_completion_record_verbatim_question():
    comp_path = ROOT_DIR / "docs/cae/implementation/CAE_MIG_03_COMPLETION_RECORD.md"
    content = comp_path.read_text(encoding="utf-8")
    exact_question = (
        "Accept CA-MIG-03 as a forward-only migration design and offline safety rehearsal only, "
        "preserve every listed no-go condition and open F-01/F-02 decision, and authorize a "
        "separately bounded disposable-environment migration-application proof for the exact "
        "approved draft IDs—without changing staging authority, migrating client data, or enabling "
        "production routing?"
    )
    assert exact_question in content
