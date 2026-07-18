from __future__ import annotations

import hashlib
import importlib.resources
import pathlib
import tomllib


ROOT = pathlib.Path(__file__).resolve().parents[2]


def test_pyproject_declares_rc1_identity_and_console_entry_point() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert data["project"]["name"] == "atomic-harness-builder"
    assert data["project"]["version"] == "0.1.0rc1"
    assert data["project"]["requires-python"] == ">=3.12"
    assert data["project"]["dependencies"] == []
    assert data["project"]["scripts"]["cmf-builder"] == "cmf_builder.cli.bootstrap:local_main"
    assert data["build-system"]["build-backend"] == "setuptools.build_meta"
    assert data["build-system"]["requires"] == ["setuptools==80.9.0"]


def test_runtime_category_registry_is_packaged_with_exact_governed_bytes() -> None:
    source = ROOT / "governance" / "CANONICAL_CATEGORY_REGISTRY.yaml"
    packaged = (
        importlib.resources.files("cmf_builder.resources.governance")
        .joinpath("CANONICAL_CATEGORY_REGISTRY.yaml")
        .read_bytes()
    )
    assert packaged == source.read_bytes()
    assert hashlib.sha256(packaged).hexdigest() == hashlib.sha256(source.read_bytes()).hexdigest()


def test_runtime_and_dev_locks_are_separated() -> None:
    runtime_lock = (ROOT / "requirements.lock").read_text(encoding="utf-8")
    dev_lock = (ROOT / "requirements-dev.lock").read_text(encoding="utf-8")
    assert "runtime dependencies: none" in runtime_lock
    assert "pytest==8.3.4" in dev_lock
    assert "openai" not in runtime_lock.lower()
    assert "qwen" not in runtime_lock.lower()
    assert "vllm" not in runtime_lock.lower()
    assert "boto" not in runtime_lock.lower()
    assert "google-cloud" not in runtime_lock.lower()

