from __future__ import annotations

from ._support import composer_app, ref, valid_seed, valid_question
from conscious_activations_interview_composer.domain import make_guest_research_package


def test_create_research_package(tmp_path):
    app = composer_app(tmp_path)
    result = app.research.create_package(
        {
            "workspace_id": "ws-1",
            "project_id": "prj-1",
            "guest_name": "Alice",
            "source_urls": ["https://example.com/bio", "https://example.com/article"],
            "uploaded_documents": [],
            "composer_authority": {
                "operator_id": "op-1",
                "authority_scope": "DEVELOPMENT_TEST",
                "assertion_id": "assert-1",
            },
        },
        idempotency_key="research:ws-1:prj-1:Alice",
    )
    payload = result["object"]["payload"]
    assert payload["guest_name"] == "Alice"
    assert payload["research_package_id"].startswith("ic:research:")
    assert len(payload["source_urls"]) == 2
    assert payload["source_urls"][0].startswith("http")
    assert payload["uploaded_documents"] == []


def test_create_package_with_documents(tmp_path):
    app = composer_app(tmp_path)
    docs = [{
        "asset_id": "workspace://ws-1/composer/doc.pdf",
        "sha256": "a" * 64,
        "bytes": 1024,
        "media_type": "application/pdf",
        "original_filename": "ref.pdf",
    }]
    result = app.research.create_package(
        {
            "workspace_id": "ws-1",
            "project_id": "prj-1",
            "guest_name": "Bob",
            "source_urls": [],
            "uploaded_documents": docs,
            "composer_authority": {
                "operator_id": "op-1",
                "authority_scope": "DEVELOPMENT_TEST",
                "assertion_id": "assert-1",
            },
        },
        idempotency_key="research:ws-1:prj-1:Bob",
    )
    payload = result["object"]["payload"]
    assert len(payload["uploaded_documents"]) == 1
    assert payload["uploaded_documents"][0]["sha256"] == "a" * 64


def test_get_research_package(tmp_path):
    app = composer_app(tmp_path)
    result = app.research.create_package(
        {
            "workspace_id": "ws-1", "project_id": "prj-1",
            "guest_name": "Charlie", "source_urls": [],
            "uploaded_documents": [],
            "composer_authority": {"operator_id": "op-1", "authority_scope": "DEV", "assertion_id": "a1"},
        },
        idempotency_key="r1",
    )
    pid = result["object"]["payload"]["research_package_id"]
    stored = app.repository.get_object(pid)
    assert stored["payload"]["guest_name"] == "Charlie"


def test_create_research_package_idempotent(tmp_path):
    app = composer_app(tmp_path)
    cmd = {
        "workspace_id": "ws-1", "project_id": "prj-1",
        "guest_name": "Diana", "source_urls": [],
        "uploaded_documents": [],
        "composer_authority": {"operator_id": "op-1", "authority_scope": "DEV", "assertion_id": "a1"},
    }
    r1 = app.research.create_package(cmd, idempotency_key="idem-research")
    r2 = app.research.create_package(cmd, idempotency_key="idem-research")
    assert r2["idempotent_replay"] is True
    assert r2["object"]["object_id"] == r1["object"]["object_id"]