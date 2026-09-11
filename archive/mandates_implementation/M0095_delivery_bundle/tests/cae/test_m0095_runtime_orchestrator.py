from __future__ import annotations

import json
import socket
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

from deployment.dev.caestudio.orchestrator import ConfigurationError, LaunchError, RuntimeOrchestrator


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "deployment/dev/caestudio/manifest.json"


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _write_manifest(path: Path, runtimes: list[dict]) -> None:
    payload = {
        "schema_version": "1.0",
        "name": "test",
        "public_host": "127.0.0.1",
        "public_port": _free_port(),
        "control_host": "127.0.0.1",
        "control_port": _free_port(),
        "nginx_binary": "nginx",
        "runtimes": runtimes,
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def _sleep_runtime(tmp_path: Path, runtime_id: str, health: dict) -> dict:
    return {
        "id": runtime_id,
        "display_name": runtime_id,
        "enabled_default": True,
        "required": True,
        "capabilities": [runtime_id + "_capability"],
        "route_prefix": "/runtime/" + runtime_id,
        "command": [sys.executable, "-c", "import time; time.sleep(60)"],
        "cwd": str(tmp_path),
        "health": health,
        "authority_boundary": "downstream_runtime_only",
    }


def test_default_manifest_is_single_origin_and_external_runtime_is_fail_closed() -> None:
    orchestrator = RuntimeOrchestrator(MANIFEST, root_dir=ROOT)
    rendered = orchestrator.render_nginx_config()
    assert "listen 127.0.0.1:3000;" in rendered
    assert "location /api/" in rendered
    assert "location /ws/" in rendered
    assert "location / {" in rendered
    assert "location /runtime/openchatcut/" not in rendered
    assert rendered.count("listen 127.0.0.1:3000;") == 1
    capabilities = orchestrator.capabilities_document()["capabilities"]
    openchatcut = [item for item in capabilities if item["runtime_id"] == "openchatcut"]
    assert openchatcut and all(item["enabled"] is False for item in openchatcut)
    assert all(item["authority_boundary"] != "cae_authority" for item in openchatcut)


def test_render_is_deterministic_across_replay(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    _write_manifest(
        manifest,
        [
            _sleep_runtime(tmp_path, "alpha", {"kind": "process"}),
            _sleep_runtime(tmp_path, "beta", {"kind": "process"}),
        ],
    )
    first = RuntimeOrchestrator(manifest, root_dir=ROOT).render_nginx_config()
    second = RuntimeOrchestrator(manifest, root_dir=ROOT).render_nginx_config()
    assert first == second


def test_processes_are_isolated_and_successfully_health_checked(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    _write_manifest(
        manifest,
        [
            _sleep_runtime(tmp_path, "alpha", {"kind": "process"}),
            _sleep_runtime(tmp_path, "beta", {"kind": "process"}),
        ],
    )
    orchestrator = RuntimeOrchestrator(manifest, root_dir=ROOT, startup_probe_count=10, startup_probe_interval=0.1)
    try:
        orchestrator._launch_runtime_processes()
        orchestrator._probe_all()
        alpha = orchestrator.states["alpha"]
        beta = orchestrator.states["beta"]
        assert alpha.status == "healthy"
        assert beta.status == "healthy"
        assert alpha.pid is not None and beta.pid is not None
        assert alpha.pid != beta.pid
    finally:
        orchestrator.stop()


def test_good_looking_but_wrong_process_is_not_healthy(tmp_path: Path) -> None:
    class WrongHealthHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            self.send_response(404)
            self.end_headers()

        def log_message(self, format: str, *args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", _free_port()), WrongHealthHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        manifest = tmp_path / "manifest.json"
        _write_manifest(
            manifest,
            [_sleep_runtime(tmp_path, "looks_good", {"kind": "http", "url": f"http://127.0.0.1:{server.server_port}/health", "expected_status": 200, "timeout_seconds": 0.5})],
        )
        orchestrator = RuntimeOrchestrator(manifest, root_dir=ROOT, startup_probe_count=8, startup_probe_interval=0.1)
        try:
            orchestrator._launch_runtime_processes()
            orchestrator._probe_all()
            state = orchestrator.states["looks_good"]
            assert state.process is not None and state.process.poll() is None
            assert state.status == "unhealthy"
            assert state.last_health is False
            assert "http status 404" in (state.last_health_error or "")
        finally:
            orchestrator.stop()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_http_health_requires_expected_status(tmp_path: Path) -> None:
    class HealthyHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")

        def log_message(self, format: str, *args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", _free_port()), HealthyHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        manifest = tmp_path / "manifest.json"
        _write_manifest(
            manifest,
            [
                _sleep_runtime(
                    tmp_path,
                    "http_ok",
                    {"kind": "http", "url": f"http://127.0.0.1:{server.server_port}/health", "expected_status": 200},
                )
            ],
        )
        orchestrator = RuntimeOrchestrator(manifest, root_dir=ROOT)
        ok, detail = orchestrator._health_check(orchestrator.specs[0])
        assert ok is True
        assert "status 200" in detail
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_required_launch_failure_is_surfaceable(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    _write_manifest(
        manifest,
        [
            {
                "id": "broken",
                "display_name": "Broken",
                "enabled_default": True,
                "required": True,
                "capabilities": ["broken"],
                "command": [str(tmp_path / "does-not-exist")],
                "cwd": str(tmp_path),
                "health": {"kind": "process"},
                "authority_boundary": "downstream_runtime_only",
            }
        ],
    )
    orchestrator = RuntimeOrchestrator(manifest, root_dir=ROOT)
    with pytest.raises(LaunchError, match="broken"):
        orchestrator._launch_runtime_processes()
    assert orchestrator.states["broken"].launch_error


def test_enabled_optional_runtime_missing_contract_fails_closed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    manifest = tmp_path / "manifest.json"
    _write_manifest(
        manifest,
        [
            {
                "id": "external",
                "display_name": "External",
                "enabled_default": False,
                "enabled_env": "M0095_TEST_ENABLED",
                "required": False,
                "capabilities": ["external"],
                "command_env": "M0095_TEST_COMMAND",
                "target_url_env": "M0095_TEST_URL",
                "health": {"kind": "http", "url_env": "M0095_TEST_HEALTH"},
                "authority_boundary": "downstream_runtime_only",
            }
        ],
    )
    monkeypatch.setenv("M0095_TEST_ENABLED", "true")
    for key in ("M0095_TEST_COMMAND", "M0095_TEST_URL", "M0095_TEST_HEALTH"):
        monkeypatch.delenv(key, raising=False)
    with pytest.raises(ConfigurationError, match="external"):
        RuntimeOrchestrator(manifest, root_dir=ROOT)


def test_openchatcut_native_mcp_health_probe_checks_jsonrpc_and_server_info(tmp_path: Path) -> None:
    observed: dict[str, object] = {}

    class MCPHandler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:  # noqa: N802
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            observed.update(body)
            response = {
                "jsonrpc": "2.0",
                "id": body.get("id"),
                "result": {"serverInfo": {"name": "test-openchatcut", "version": "1"}},
            }
            encoded = json.dumps(response).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        def log_message(self, format: str, *args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", _free_port()), MCPHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        manifest = tmp_path / "manifest.json"
        _write_manifest(
            manifest,
            [
                {
                    "id": "openchatcut",
                    "display_name": "OpenChatCut",
                    "enabled_default": True,
                    "required": False,
                    "capabilities": ["native_video_editing"],
                    "command": [sys.executable, "-c", "import time; time.sleep(60)"],
                    "cwd": str(tmp_path),
                    "health": {"kind": "mcp_initialize", "url": f"http://127.0.0.1:{server.server_port}/mcp"},
                    "authority_boundary": "downstream_runtime_only",
                }
            ],
        )
        orchestrator = RuntimeOrchestrator(manifest, root_dir=ROOT)
        ok, detail = orchestrator._health_check(orchestrator.specs[0])
        assert ok is True
        assert "acknowledged" in detail
        assert observed["method"] == "initialize"
        assert observed["params"]["protocolVersion"] == "2025-06-18"  # type: ignore[index]
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_openchatcut_mcp_sse_response_is_accepted(tmp_path: Path) -> None:
    class SSEHandler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:  # noqa: N802
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            payload = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": body.get("id"),
                    "result": {"serverInfo": {"name": "test-openchatcut", "version": "1"}},
                }
            )
            encoded = f"event: message\ndata: {payload}\n\n".encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        def log_message(self, format: str, *args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", _free_port()), SSEHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        manifest = tmp_path / "manifest.json"
        _write_manifest(
            manifest,
            [
                {
                    "id": "openchatcut",
                    "display_name": "OpenChatCut",
                    "enabled_default": True,
                    "required": False,
                    "capabilities": ["native_video_editing"],
                    "command": [sys.executable, "-c", "import time; time.sleep(60)"],
                    "cwd": str(tmp_path),
                    "health": {"kind": "mcp_initialize", "url": f"http://127.0.0.1:{server.server_port}/mcp"},
                    "authority_boundary": "downstream_runtime_only",
                }
            ],
        )
        orchestrator = RuntimeOrchestrator(manifest, root_dir=ROOT)
        ok, detail = orchestrator._health_check(orchestrator.specs[0])
        assert ok is True
        assert "acknowledged" in detail
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
