from __future__ import annotations
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
IMPL_DIR = ROOT_DIR / "docs" / "cae" / "implementation"

REQUIRED_DOCS = [
    "CAE_TWC_01_ADMISSION_RECORD.md",
    "CAE_TWC_01_DEPLOYMENT_EVIDENCE.md",
    "CAE_TWC_01_TYPED_CORE_PROOF.md",
    "CAE_TWC_01_API_SURFACE_PROOF.md",
    "CAE_TWC_01_ISOLATION_AND_ADVERSARIAL_RESULTS.md",
    "CAE_TWC_01_COMPLETION_RECORD.md",
]


@pytest.mark.parametrize("doc_name", REQUIRED_DOCS)
def test_ca_twc_01_required_documents_exist(doc_name: str) -> None:
    doc_path = IMPL_DIR / doc_name
    assert doc_path.is_file(), f"Missing required document: {doc_name}"
    assert doc_path.stat().st_size > 0, f"Document is empty: {doc_name}"


def test_migration_drafts_exist() -> None:
    drafts_dir = ROOT_DIR / "packages" / "ca_runtime" / "src" / "ca_runtime" / "migrations" / "drafts"
    assert (drafts_dir / "0000R_staging_foundation_reset.sql").is_file()
    assert (drafts_dir / "0009_cae_rls_completion.sql").is_file()


def test_typed_core_module_exists() -> None:
    core_path = ROOT_DIR / "packages" / "ca_runtime" / "src" / "ca_runtime" / "workspace_core.py"
    assert core_path.is_file()
    assert core_path.stat().st_size > 0


def test_v1_tenancy_router_exists() -> None:
    router_path = ROOT_DIR / "api" / "routers" / "v1_tenancy.py"
    assert router_path.is_file()
    assert router_path.stat().st_size > 0
