#!/usr/bin/env python3
"""CAE Studio development/runtime orchestrator.

This module is intentionally a topology/runtime boundary. It owns process
launching, health observation, deterministic capability registration, and the
single-origin nginx gateway. It does not own CAE semantic state or promotion.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import signal
import socket
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Mapping
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_MANIFEST = Path(__file__).with_name("manifest.json")
_TOKEN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


class OrchestratorError(RuntimeError):
    """Base orchestrator error."""


class ConfigurationError(OrchestratorError):
    """Manifest/environment is incomplete or invalid."""


class LaunchError(OrchestratorError):
    """A required process could not be launched or exited during startup."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _env_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ConfigurationError(f"invalid boolean value: {value!r}")


def _expand(value: str, env: Mapping[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in env:
            raise ConfigurationError(f"missing environment variable for template: {key}")
        return env[key]

    return _TOKEN.sub(replace, value)


def _command_from_env(value: str) -> list[str]:
    parts = shlex.split(value, posix=(os.name != "nt"))
    if not parts:
        raise ConfigurationError("command environment value is empty")
    return parts


def _ensure_url(value: str, *, field_name: str) -> str:
    if not value.startswith(("http://", "https://")):
        raise ConfigurationError(f"{field_name} must be an http(s) URL: {value!r}")
    return value.rstrip("/")


def _url_host_port(url: str) -> tuple[str, int]:
    from urllib.parse import urlparse

    parsed = urlparse(url)
    if parsed.hostname is None or parsed.port is None:
        raise ConfigurationError(f"target URL must contain a host and port for tcp health: {url}")
    return parsed.hostname, parsed.port


@dataclass(frozen=True)
class HealthSpec:
    kind: str
    url: str | None = None
    expected_status: int = 200
    timeout_seconds: float = 2.0
    bearer_token: str | None = None


@dataclass(frozen=True)
class RuntimeSpec:
    runtime_id: str
    display_name: str
    enabled: bool
    required: bool
    capabilities: tuple[str, ...]
    route_prefix: str | None
    command: tuple[str, ...] | None
    cwd: Path
    env: Mapping[str, str]
    health: HealthSpec
    target_url: str | None
    authority_boundary: str
    notes: tuple[str, ...] = ()


@dataclass
class RuntimeState:
    spec: RuntimeSpec
    process: subprocess.Popen[bytes] | None = None
    pid: int | None = None
    log_path: Path | None = None
    launch_error: str | None = None
    last_health: bool | None = None
    last_health_error: str | None = None
    started_at: str | None = None
    stopped_at: str | None = None

    @property
    def status(self) -> str:
        if not self.spec.enabled:
            return "disabled"
        if self.launch_error:
            return "failed"
        if self.process is None:
            return "configured"
        code = self.process.poll()
        if code is not None:
            return "failed" if code != 0 else "stopped"
        if self.last_health is True:
            return "healthy"
        if self.last_health is False:
            return "unhealthy"
        return "starting"

    def log_tail(self, limit: int = 4000) -> str:
        if not self.log_path or not self.log_path.exists():
            return ""
        try:
            data = self.log_path.read_bytes()
        except OSError:
            return ""
        return data[-limit:].decode("utf-8", errors="replace")


class _ControlHandler(BaseHTTPRequestHandler):
    server: "_ControlServer"

    def do_GET(self) -> None:  # noqa: N802
        if self.path in {"/__studio/health", "/__studio/health/"}:
            self._json(200, self.server.orchestrator.health_document())
            return
        if self.path in {"/__studio/capabilities", "/__studio/capabilities/"}:
            self._json(200, self.server.orchestrator.capabilities_document())
            return
        if self.path in {"/__studio/topology", "/__studio/topology/"}:
            self._json(200, self.server.orchestrator.topology_document())
            return
        self._json(404, {"error": "not_found"})

    def _json(self, status: int, document: Mapping[str, Any]) -> None:
        payload = json.dumps(document, separators=(",", ":"), sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: Any) -> None:
        sys.stderr.write("[cae-studio-control] " + format % args + "\n")


class _ControlServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], orchestrator: "RuntimeOrchestrator") -> None:
        self.orchestrator = orchestrator
        super().__init__(address, _ControlHandler)


class RuntimeOrchestrator:
    """Owns only runtime topology; CAE services remain the authorities."""

    def __init__(
        self,
        manifest_path: str | Path = DEFAULT_MANIFEST,
        *,
        root_dir: str | Path | None = None,
        startup_probe_count: int = 8,
        startup_probe_interval: float = 0.5,
    ) -> None:
        self.manifest_path = Path(manifest_path).resolve()
        self.manifest = self._load_manifest(self.manifest_path)
        self.manifest_sha256 = hashlib.sha256(self.manifest_path.read_bytes()).hexdigest()
        self.repo_root = Path(root_dir or self.manifest_path.parents[3]).resolve()
        self.runtime_root = Path(
            os.environ.get("CAE_STUDIO_RUNTIME_ROOT", self.manifest_path.parent / ".runtime")
        ).resolve()
        self.startup_probe_count = startup_probe_count
        self.startup_probe_interval = startup_probe_interval
        self.public_host = self.manifest.get("public_host", "127.0.0.1")
        self.public_port = int(self.manifest.get("public_port", 3000))
        self.control_host = self.manifest.get("control_host", "127.0.0.1")
        self.control_port = int(self.manifest.get("control_port", 3100))
        self.nginx_binary = os.environ.get("CAE_STUDIO_NGINX_BIN", self.manifest.get("nginx_binary", "nginx"))
        self.specs = self._build_specs()
        self.states: dict[str, RuntimeState] = {spec.runtime_id: RuntimeState(spec) for spec in self.specs}
        self.control_server: _ControlServer | None = None
        self.nginx_process: subprocess.Popen[bytes] | None = None
        self.nginx_log_path = self.runtime_root / "logs" / "nginx.log"
        self.config_path = self.runtime_root / "nginx.conf"
        self._started = False

    @staticmethod
    def _load_manifest(path: Path) -> dict[str, Any]:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ConfigurationError(f"unable to load manifest {path}: {exc}") from exc
        if not isinstance(data, dict):
            raise ConfigurationError("manifest root must be an object")
        if data.get("schema_version") != "1.0":
            raise ConfigurationError("unsupported manifest schema_version")
        return data

    def _build_specs(self) -> tuple[RuntimeSpec, ...]:
        runtimes = self.manifest.get("runtimes")
        if not isinstance(runtimes, list) or not runtimes:
            raise ConfigurationError("manifest runtimes must be a non-empty list")
        seen: set[str] = set()
        routes: set[str] = set()
        base_env = dict(os.environ)
        base_env.setdefault("CAE_STUDIO_REPO_ROOT", str(self.repo_root))
        base_env.setdefault("CAE_STUDIO_RUNTIME_ROOT", str(self.runtime_root))
        specs: list[RuntimeSpec] = []
        for raw in runtimes:
            if not isinstance(raw, dict):
                raise ConfigurationError("runtime entry must be an object")
            runtime_id = str(raw.get("id", ""))
            if not runtime_id or runtime_id in seen:
                raise ConfigurationError(f"duplicate or missing runtime id: {runtime_id!r}")
            seen.add(runtime_id)

            enabled_default = bool(raw.get("enabled_default", False))
            enabled_env = raw.get("enabled_env")
            enabled = _env_bool(base_env.get(str(enabled_env)), enabled_default) if enabled_env else enabled_default
            required = bool(raw.get("required", False))
            capabilities = tuple(str(v) for v in raw.get("capabilities", []))
            route_prefix = raw.get("route_prefix")
            if route_prefix:
                route_prefix = "/" + str(route_prefix).strip("/") + "/"
                if route_prefix in routes:
                    raise ConfigurationError(f"duplicate runtime route: {route_prefix}")
                routes.add(route_prefix)

            target_url = None
            target_url_env = raw.get("target_url_env")
            if target_url_env:
                target_value = base_env.get(str(target_url_env))
                if target_value:
                    target_url = _ensure_url(target_value, field_name=str(target_url_env))
                elif enabled:
                    raise ConfigurationError(f"enabled runtime {runtime_id} is missing {target_url_env}")

            command: tuple[str, ...] | None = None
            command_env = raw.get("command_env")
            if command_env:
                command_value = base_env.get(str(command_env))
                if command_value:
                    command = tuple(_command_from_env(command_value))
                elif enabled:
                    raise ConfigurationError(f"enabled runtime {runtime_id} is missing {command_env}")
            elif raw.get("command"):
                raw_command = raw["command"]
                if not isinstance(raw_command, list) or not all(isinstance(v, str) for v in raw_command):
                    raise ConfigurationError(f"runtime {runtime_id} command must be an array of strings")
                command = tuple(_expand(v, base_env) for v in raw_command)

            if enabled and not command:
                raise ConfigurationError(f"enabled runtime {runtime_id} has no command")

            raw_cwd = str(raw.get("cwd", "."))
            cwd = Path(_expand(raw_cwd, base_env))
            if not cwd.is_absolute():
                cwd = (self.repo_root / cwd).resolve()

            runtime_env = dict(base_env)
            for key, value in dict(raw.get("env", {})).items():
                runtime_env[str(key)] = _expand(str(value), base_env)

            health_raw = raw.get("health", {})
            if not isinstance(health_raw, dict):
                raise ConfigurationError(f"runtime {runtime_id} health must be an object")
            health_kind = str(health_raw.get("kind", "process"))
            health_url = None
            health_env = health_raw.get("url_env")
            if health_env:
                health_value = base_env.get(str(health_env))
                if health_value:
                    health_url = _ensure_url(health_value, field_name=str(health_env))
                elif enabled:
                    raise ConfigurationError(f"enabled runtime {runtime_id} is missing {health_env}")
            elif health_raw.get("url"):
                health_url = _ensure_url(_expand(str(health_raw["url"]), base_env), field_name=f"health.{runtime_id}")

            if health_kind == "tcp_target" and enabled and not target_url:
                raise ConfigurationError(f"runtime {runtime_id} uses tcp_target health but has no target URL")

            bearer_token = None
            token_env = health_raw.get("bearer_token_env")
            if token_env:
                bearer_token = base_env.get(str(token_env))
                if enabled and bearer_token is None:
                    # Tokens are optional unless the runtime explicitly supplies one.
                    bearer_token = None

            specs.append(
                RuntimeSpec(
                    runtime_id=runtime_id,
                    display_name=str(raw.get("display_name", runtime_id)),
                    enabled=enabled,
                    required=required,
                    capabilities=capabilities,
                    route_prefix=route_prefix,
                    command=command,
                    cwd=cwd,
                    env=runtime_env,
                    health=HealthSpec(
                        kind=health_kind,
                        url=health_url,
                        expected_status=int(health_raw.get("expected_status", 200)),
                        timeout_seconds=float(health_raw.get("timeout_seconds", 2.0)),
                        bearer_token=bearer_token,
                    ),
                    target_url=target_url,
                    authority_boundary=str(raw.get("authority_boundary", "downstream_runtime_only")),
                    notes=tuple(str(v) for v in raw.get("notes", [])),
                )
            )
        return tuple(specs)

    def start(self) -> None:
        if self._started:
            return
        self.runtime_root.mkdir(parents=True, exist_ok=True)
        (self.runtime_root / "logs").mkdir(parents=True, exist_ok=True)
        self._launch_runtime_processes()
        self._start_control_server()
        try:
            self.config_path.write_text(self.render_nginx_config(), encoding="utf-8")
            self._launch_nginx()
        except Exception:
            self.stop()
            raise
        self._started = True
        self._probe_all()

    def _launch_runtime_processes(self) -> None:
        self.runtime_root.mkdir(parents=True, exist_ok=True)
        (self.runtime_root / "logs").mkdir(parents=True, exist_ok=True)
        for spec in self.specs:
            state = self.states[spec.runtime_id]
            if not spec.enabled:
                continue
            assert spec.command is not None
            log_path = self.runtime_root / "logs" / f"{spec.runtime_id}.log"
            state.log_path = log_path
            try:
                with log_path.open("ab") as log_handle:
                    kwargs: dict[str, Any] = {
                        "cwd": str(spec.cwd),
                        "env": dict(spec.env),
                        "stdout": log_handle,
                        "stderr": subprocess.STDOUT,
                    }
                    if os.name == "nt":
                        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
                    else:
                        kwargs["start_new_session"] = True
                    process = subprocess.Popen(list(spec.command), **kwargs)
            except (OSError, ValueError) as exc:
                state.launch_error = str(exc)
                if spec.required:
                    raise LaunchError(f"failed to launch required runtime {spec.runtime_id}: {exc}") from exc
                continue
            state.process = process
            state.pid = process.pid
            state.started_at = _now()
            # Give immediately-crashing processes one observable turn before continuing.
            time.sleep(0.05)
            if process.poll() is not None:
                state.launch_error = f"process exited during startup with code {process.returncode}"
                if spec.required:
                    raise LaunchError(
                        f"required runtime {spec.runtime_id} exited during startup; log={log_path}"
                    )

    def _start_control_server(self) -> None:
        try:
            self.control_server = _ControlServer((self.control_host, self.control_port), self)
        except OSError as exc:
            raise LaunchError(f"failed to bind Studio control server: {exc}") from exc
        self.control_server_thread = __import__("threading").Thread(
            target=self.control_server.serve_forever,
            name="cae-studio-control",
            daemon=True,
        )
        self.control_server_thread.start()

    def _launch_nginx(self) -> None:
        log_path = self.nginx_log_path
        with log_path.open("ab") as log_handle:
            kwargs: dict[str, Any] = {
                "cwd": str(self.runtime_root),
                "stdout": log_handle,
                "stderr": subprocess.STDOUT,
            }
            if os.name == "nt":
                kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
            else:
                kwargs["start_new_session"] = True
            try:
                process = subprocess.Popen(
                    [self.nginx_binary, "-c", str(self.config_path), "-p", str(self.runtime_root), "-g", "daemon off;"],
                    **kwargs,
                )
            except (OSError, ValueError) as exc:
                raise LaunchError(f"failed to launch nginx gateway: {exc}") from exc
        self.nginx_process = process
        time.sleep(0.05)
        if process.poll() is not None:
            raise LaunchError(f"nginx exited during startup with code {process.returncode}; log={log_path}")

    def _probe_all(self) -> None:
        for _ in range(self.startup_probe_count):
            all_settled = True
            for state in self.states.values():
                if state.spec.enabled:
                    self._probe_state(state)
                    if state.status == "starting":
                        all_settled = False
            if all_settled:
                break
            time.sleep(self.startup_probe_interval)

    def _probe_state(self, state: RuntimeState) -> None:
        if not state.spec.enabled or state.process is None:
            return
        if state.process.poll() is not None:
            state.last_health = False
            state.last_health_error = f"process exited with code {state.process.returncode}"
            return
        try:
            ok, detail = self._health_check(state.spec)
        except Exception as exc:  # health must never crash the control plane
            ok, detail = False, str(exc)
        state.last_health = ok
        state.last_health_error = None if ok else detail

    def _health_check(self, spec: RuntimeSpec) -> tuple[bool, str]:
        kind = spec.health.kind
        if kind == "process":
            return True, "process alive"
        if kind == "tcp_target":
            assert spec.target_url is not None
            host, port = _url_host_port(spec.target_url)
            with socket.create_connection((host, port), timeout=spec.health.timeout_seconds):
                return True, "tcp listener reachable"
        if kind == "http":
            if not spec.health.url:
                raise ConfigurationError(f"runtime {spec.runtime_id} http health missing URL")
            headers = {"User-Agent": "cae-studio-orchestrator/1.0"}
            if spec.health.bearer_token:
                headers["Authorization"] = f"Bearer {spec.health.bearer_token}"
            request = Request(spec.health.url, headers=headers, method="GET")
            try:
                with urlopen(request, timeout=spec.health.timeout_seconds) as response:
                    code = int(response.status)
                    response.read(4096)
            except HTTPError as exc:
                code = exc.code
            except (URLError, TimeoutError, OSError) as exc:
                return False, f"http unreachable: {exc}"
            return (code == spec.health.expected_status, f"http status {code}, expected {spec.health.expected_status}")
        if kind == "mcp_initialize":
            if not spec.health.url:
                raise ConfigurationError(f"runtime {spec.runtime_id} mcp_initialize health missing URL")
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {"roots": {"listChanged": False}},
                    "clientInfo": {"name": "cae-studio-orchestrator", "version": "1.0"},
                },
            }
            headers = {
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
                "User-Agent": "cae-studio-orchestrator/1.0",
            }
            if spec.health.bearer_token:
                headers["Authorization"] = f"Bearer {spec.health.bearer_token}"
            request = Request(
                spec.health.url,
                data=json.dumps(payload, separators=(",", ":")).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            try:
                with urlopen(request, timeout=spec.health.timeout_seconds) as response:
                    body = response.read(64 * 1024)
            except HTTPError as exc:
                return False, f"mcp http status {exc.code}"
            except (URLError, TimeoutError, OSError) as exc:
                return False, f"mcp unreachable: {exc}"
            content_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
            text = body.decode("utf-8", errors="replace")
            if content_type == "text/event-stream":
                documents: list[dict[str, Any]] = []
                data_lines: list[str] = []
                for line in text.splitlines():
                    if line.startswith("data:"):
                        data_lines.append(line[5:].lstrip())
                    elif not line.strip() and data_lines:
                        payload_text = "\n".join(data_lines)
                        data_lines = []
                        if payload_text and payload_text != "[DONE]":
                            try:
                                parsed = json.loads(payload_text)
                            except json.JSONDecodeError:
                                continue
                            if isinstance(parsed, dict):
                                documents.append(parsed)
                if data_lines:
                    payload_text = "\n".join(data_lines)
                    if payload_text and payload_text != "[DONE]":
                        try:
                            parsed = json.loads(payload_text)
                        except json.JSONDecodeError:
                            parsed = None
                        if isinstance(parsed, dict):
                            documents.append(parsed)
                document = documents[-1] if documents else None
            else:
                try:
                    document = json.loads(text)
                except json.JSONDecodeError:
                    document = None
            if not isinstance(document, dict):
                return False, "mcp response was not a JSON-RPC object"
            if document.get("jsonrpc") != "2.0" or document.get("id") != 1:
                return False, "mcp response is not the expected JSON-RPC envelope"
            if "error" in document:
                return False, f"mcp error: {document['error']}"
            server_info = document.get("result", {}).get("serverInfo")
            if not isinstance(server_info, dict):
                return False, "mcp initialize result is missing serverInfo"
            return True, "mcp initialize acknowledged"
        raise ConfigurationError(f"unsupported health kind: {kind}")

    def render_nginx_config(self) -> str:
        """Pure deterministic rendering; used by tests and evidence replay."""
        lines = [
            "worker_processes 1;",
            f"pid {self.runtime_root / 'nginx.pid'};",
            "error_log logs/nginx-error.log warn;",
            "events {",
            "    worker_connections 2048;",
            "}",
            "http {",
            "    include /etc/nginx/mime.types;",
            "    default_type application/octet-stream;",
            "    sendfile on;",
            "    client_max_body_size 2g;",
            "    map $http_upgrade $connection_upgrade {",
            "        default upgrade;",
            "        '' close;",
            "    }",
            "    server {",
            f"        listen {self.public_host}:{self.public_port};",
            "        server_name _;",
            "        proxy_http_version 1.1;",
            "        proxy_set_header Host $host;",
            "        proxy_set_header X-Forwarded-Host $host;",
            "        proxy_set_header X-Forwarded-Proto $scheme;",
            "        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;",
            "        proxy_set_header X-CAE-Studio-Origin $scheme://$host:$server_port;",
            "        proxy_set_header Upgrade $http_upgrade;",
            "        proxy_set_header Connection $connection_upgrade;",
            "",
            f"        location /__studio/ {{",
            f"            proxy_pass http://{self.control_host}:{self.control_port};",
            "            proxy_buffering off;",
            "        }",
        ]
        for spec in self.specs:
            if not spec.enabled or not spec.route_prefix or not spec.target_url:
                continue
            lines.extend(
                [
                    f"        location {spec.route_prefix} {{",
                    f"            proxy_pass {spec.target_url}/;",
                    f"            proxy_set_header X-CAE-Runtime-ID {spec.runtime_id};",
                    f"            proxy_set_header X-CAE-Runtime-Route {spec.route_prefix};",
                    "            proxy_buffering off;",
                    "        }",
                    "",
                ]
            )
        lines.extend(
            [
                "        location /api/ {",
                "            proxy_pass http://127.0.0.1:8000;",
                "            proxy_buffering off;",
                "        }",
                "        location /ws/ {",
                "            proxy_pass http://127.0.0.1:8000;",
                "            proxy_read_timeout 3600s;",
                "            proxy_buffering off;",
                "        }",
                "        location / {",
                "            proxy_pass http://127.0.0.1:5173;",
                "            proxy_buffering off;",
                "        }",
                "    }",
                "}",
                "",
            ]
        )
        return "\n".join(lines)

    def health_document(self) -> dict[str, Any]:
        runtime_health: dict[str, Any] = {}
        overall = "healthy"
        for runtime_id, state in self.states.items():
            self._probe_state(state)
            runtime_health[runtime_id] = {
                "status": state.status,
                "enabled": state.spec.enabled,
                "required": state.spec.required,
                "pid": state.pid,
                "started_at": state.started_at,
                "stopped_at": state.stopped_at,
                "health_ok": state.last_health,
                "health_error": state.last_health_error,
                "launch_error": state.launch_error,
                "log_path": str(state.log_path) if state.log_path else None,
                "log_tail": state.log_tail(),
            }
            if state.spec.required and state.status != "healthy":
                overall = "degraded"
            elif state.spec.enabled and state.status in {"failed", "unhealthy"}:
                if overall == "healthy":
                    overall = "degraded"
        if self.nginx_process and self.nginx_process.poll() is not None:
            overall = "degraded"
        return {
            "schema_version": "1.0",
            "manifest_sha256": self.manifest_sha256,
            "timestamp": _now(),
            "origin": f"http://{self.public_host}:{self.public_port}",
            "control_origin": f"http://{self.control_host}:{self.control_port}",
            "status": overall,
            "gateway": {
                "status": "healthy" if self.nginx_process and self.nginx_process.poll() is None else "failed",
                "pid": self.nginx_process.pid if self.nginx_process else None,
                "log_path": str(self.nginx_log_path),
            },
            "runtimes": runtime_health,
        }

    def capabilities_document(self) -> dict[str, Any]:
        capabilities: list[dict[str, Any]] = []
        for state in self.states.values():
            for capability in state.spec.capabilities:
                capabilities.append(
                    {
                        "capability": capability,
                        "runtime_id": state.spec.runtime_id,
                        "enabled": state.spec.enabled,
                        "status": state.status,
                        "route_prefix": state.spec.route_prefix,
                        "authority_boundary": state.spec.authority_boundary,
                    }
                )
        capabilities.sort(key=lambda item: (item["runtime_id"], item["capability"]))
        return {
            "schema_version": "1.0",
            "manifest_sha256": self.manifest_sha256,
            "origin": f"http://{self.public_host}:{self.public_port}",
            "authority": "CAE semantic meaning/state/provenance remain outside the orchestrator; external runtimes are downstream and replaceable.",
            "capabilities": capabilities,
        }

    def topology_document(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "manifest_sha256": self.manifest_sha256,
            "origin": f"http://{self.public_host}:{self.public_port}",
            "control_prefix": "/__studio/",
            "runtimes": [
                {
                    "id": spec.runtime_id,
                    "display_name": spec.display_name,
                    "enabled": spec.enabled,
                    "required": spec.required,
                    "route_prefix": spec.route_prefix,
                    "target_url": spec.target_url,
                    "capabilities": list(spec.capabilities),
                    "authority_boundary": spec.authority_boundary,
                    "notes": list(spec.notes),
                }
                for spec in self.specs
            ],
        }

    def stop(self) -> None:
        if self.control_server:
            self.control_server.shutdown()
            self.control_server.server_close()
            self.control_server = None
        if self.nginx_process:
            self._terminate_process(self.nginx_process)
            self.nginx_process = None
        for state in self.states.values():
            if state.process:
                self._terminate_process(state.process)
                state.stopped_at = _now()
                state.process = None

    @staticmethod
    def _terminate_process(process: subprocess.Popen[bytes]) -> None:
        if process.poll() is not None:
            return
        try:
            if os.name == "nt":
                process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                os.killpg(process.pid, signal.SIGTERM)
        except (OSError, ValueError):
            try:
                process.terminate()
            except OSError:
                return
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            try:
                if os.name == "nt":
                    process.kill()
                else:
                    os.killpg(process.pid, signal.SIGKILL)
            except OSError:
                process.kill()
            process.wait(timeout=3)

    def validate(self) -> None:
        """Fail closed on configuration; render the deterministic gateway."""
        self.runtime_root.mkdir(parents=True, exist_ok=True)
        (self.runtime_root / "logs").mkdir(parents=True, exist_ok=True)
        rendered = self.render_nginx_config()
        self.config_path.write_text(rendered, encoding="utf-8")
        try:
            result = subprocess.run(
                [self.nginx_binary, "-t", "-c", str(self.config_path), "-p", str(self.runtime_root)],
                cwd=self.runtime_root,
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError as exc:
            raise ConfigurationError(f"nginx validation could not execute: {exc}") from exc
        if result.returncode != 0:
            raise ConfigurationError(f"nginx -t failed: {result.stderr.strip() or result.stdout.strip()}")


def _print_json(document: Mapping[str, Any]) -> None:
    print(json.dumps(document, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CAE Studio runtime orchestrator")
    parser.add_argument("command", choices=("validate", "start", "stop"), nargs="?", default="validate")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    args = parser.parse_args(argv)
    orchestrator: RuntimeOrchestrator | None = None
    try:
        orchestrator = RuntimeOrchestrator(args.manifest)
        if args.command == "validate":
            orchestrator.validate()
            _print_json(orchestrator.topology_document())
            return 0
        if args.command == "start":
            orchestrator.start()
            _print_json(orchestrator.health_document())
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                return 0
            finally:
                orchestrator.stop()
        if args.command == "stop":
            # Intentionally no cross-process discovery: stop is for an in-process owner.
            print("stop requires the orchestrator process that owns the runtime tree")
            return 0
    except (OrchestratorError, OSError) as exc:
        print(json.dumps({"error": str(exc), "type": type(exc).__name__}, indent=2), file=sys.stderr)
        if orchestrator is not None:
            orchestrator.stop()
        return 2
    finally:
        if args.command != "start" and orchestrator is not None:
            orchestrator.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
