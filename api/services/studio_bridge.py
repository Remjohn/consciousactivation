from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


class StudioBridgeError(RuntimeError):
    """A well-formed StudioValidationError returned from the Node bridge."""

    def __init__(self, code: str, message: str, context: dict[str, Any] | None = None):
        super().__init__(message)
        self.code = code
        self.context = context or {}


class StudioBridgeCrash(RuntimeError):
    """The Node process exited non-zero: a bug in the bridge or Studio package."""


class StudioBridge:
    """Per-call Node subprocess bridge to ``services/studio/dist/rpc.js``.

    Every ``call()`` spawns ``node <rpc_entrypoint> <command>``, writes one
    JSON object to stdin, and reads one JSON object from stdout.  See
    TS-APP-API-006 Section 5 ("The RPC bridge protocol") for the envelope
    shape and the rationale for a per-call subprocess over a persistent
    worker (deferred until profiling warrants it).
    """

    def __init__(self, rpc_entrypoint: Path, node_binary: str = "node"):
        self.rpc_entrypoint = rpc_entrypoint
        self.node_binary = node_binary

    def call(
        self,
        command: str,
        payload: Any,
        *,
        timeout_seconds: float = 10.0,
    ) -> Any:
        process = subprocess.run(
            [self.node_binary, str(self.rpc_entrypoint), command],
            input=json.dumps(payload).encode("utf-8"),
            capture_output=True,
            timeout=timeout_seconds,
        )
        if process.returncode != 0:
            raise StudioBridgeCrash(
                f"studio rpc '{command}' crashed (exit {process.returncode}): "
                f"{process.stderr.decode('utf-8', errors='replace')[:2000]}"
            )
        envelope = json.loads(process.stdout.decode("utf-8"))
        if not envelope.get("ok"):
            error = envelope["error"]
            raise StudioBridgeError(
                error["code"],
                error["message"],
                error.get("context"),
            )
        return envelope["result"]