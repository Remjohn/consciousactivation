from __future__ import annotations

from _support import composer_app
from conscious_activations_interview_composer.errors import NotFoundError, ConflictError


def test_initialize_and_health(tmp_path):
    app = composer_app(tmp_path)
    health = app.repository.health()
    assert health["product_id"] == "interview-composer"
    assert health["ic_objects"] == 0
    assert health["ic_edges"] == 0
    assert health["ic_command_results"] == 0
    assert health["development_authorized"] is True


def test_store_and_get_object(tmp_path):
    app = composer_app(tmp_path)
    payload = {"hello": "world", "num": 42}
    result = app.repository.store_object(
        "test_type", payload,
        object_id="ic:test:abc123", idempotency_key="k1",
    )
    assert result["object"]["object_id"] == "ic:test:abc123"
    assert result["object"]["revision"] == 1
    assert result["created"] is True

    stored = app.repository.get_object("ic:test:abc123")
    assert stored["payload"] == payload


def test_get_object_not_found(tmp_path):
    app = composer_app(tmp_path)
    try:
        app.repository.get_object("ic:test:nonexistent")
        assert False, "expected NotFoundError"
    except NotFoundError:
        pass


def test_store_and_update_revision(tmp_path):
    app = composer_app(tmp_path)
    payload = {"x": 1}
    r1 = app.repository.store_object("t", payload, object_id="ic:t:1", idempotency_key="k1")
    assert r1["object"]["revision"] == 1

    payload2 = {"x": 2}
    r2 = app.repository.store_object("t", payload2, object_id="ic:t:1", idempotency_key="k2")
    assert r2["object"]["revision"] == 2

    # get returns current (revision 2)
    stored = app.repository.get_object("ic:t:1")
    assert stored["payload"] == {"x": 2}
    assert stored["revision"] == 2


def test_idempotent_replay(tmp_path):
    app = composer_app(tmp_path)
    payload = {"val": "same"}
    r1 = app.repository.store_object("t", payload, object_id="ic:t:idem", idempotency_key="idem-key")
    assert r1["created"] is True
    assert r1["idempotent_replay"] is False

    r2 = app.repository.store_object("t", payload, object_id="ic:t:idem", idempotency_key="idem-key")
    assert r2["idempotent_replay"] is True
    # same revision, not a new row
    assert r2["object"]["revision"] == r1["object"]["revision"]


def test_idempotency_conflict(tmp_path):
    app = composer_app(tmp_path)
    app.repository.store_object("t", {"a": 1}, object_id="ic:t:conflict", idempotency_key="key1")
    try:
        app.repository.store_object("t", {"a": 2}, object_id="ic:t:conflict", idempotency_key="key1")
        assert False, "expected ConflictError"
    except ConflictError:
        pass


def test_add_edge(tmp_path):
    app = composer_app(tmp_path)
    parent = "ic:parent:1"
    child = "ic:child:1"
    app.repository.store_object("t", {"p": True}, object_id=parent, idempotency_key="kp")
    app.repository.store_object("t", {"c": True}, object_id=child, idempotency_key="kc")
    app.repository.add_edge(parent, child, "test_rel")


def test_list_objects(tmp_path):
    app = composer_app(tmp_path)
    app.repository.store_object("type_a", {"a": 1}, object_id="ic:a:1", idempotency_key="ka1")
    app.repository.store_object("type_a", {"a": 2}, object_id="ic:a:2", idempotency_key="ka2")
    app.repository.store_object("type_b", {"b": 1}, object_id="ic:b:1", idempotency_key="kb1")
    all_objs = app.repository.list_objects()
    assert len(all_objs) == 3
    type_a = app.repository.list_objects(object_type="type_a")
    assert len(type_a) == 2
    type_b = app.repository.list_objects(object_type="type_b")
    assert len(type_b) == 1