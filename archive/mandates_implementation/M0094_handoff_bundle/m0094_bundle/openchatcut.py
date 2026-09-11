from __future__ import annotations

import hashlib
import json
import os
import threading
from dataclasses import dataclass
from http.client import HTTPResponse
from pathlib import Path
from typing import Any, Mapping
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from uuid import uuid4
from fractions import Fraction

from ca_contracts import canonical_sha256

from ..domain.errors import PipelineError, PipelineValidationError
from ..domain.validation import reject_noncanonical, require_ref, require_string, semantic_identity
from ..workflow.infrastructure.repository import PipelineRepository


OPENCHATCUT_MCP_DEFAULT_URL = "http://localhost:5199/api/external-mcp/mcp"
OPENCHATCUT_PROTOCOL_VERSION = "2025-06-18"
OPENCHATCUT_CLIENT_NAME = "conscious-activation-engine"
OPENCHATCUT_CLIENT_VERSION = "0.1.0"
OPENCHATCUT_INVARIANT = "INV-VIDEO-RUNTIME-001"
OPENCHATCUT_BIDIRECTIONAL_INVARIANT = "INV-VIDEO-RUNTIME-002"
OPENCHATCUT_STATE_BOUND = "BOUND"
OPENCHATCUT_STATE_ADAPT = "ADAPT"
OPENCHATCUT_STATE_READY = "NATIVE_TIMELINE_READY"
OPENCHATCUT_STATE_EXECUTED = "EXECUTED"
OPENCHATCUT_STATE_BLOCKED = "BLOCKED"


class OpenChatCutRuntimeError(PipelineError):
    """The configured OpenChatCut runtime could not satisfy the governed handoff."""


class OpenChatCutProtocolError(OpenChatCutRuntimeError):
    """The OpenChatCut MCP endpoint returned an invalid MCP/JSON-RPC response."""


class OpenChatCutTimelineVerificationError(OpenChatCutRuntimeError):
    """The native OpenChatCut timeline did not preserve the CAE source program."""


class OpenChatCutUnavailableError(OpenChatCutRuntimeError):
    """The real OpenChatCut runtime is not reachable from the current environment."""


class OpenChatCutTimelineInspectionError(OpenChatCutRuntimeError):
    """The native timeline cannot be safely reconciled with the CAE program."""


@dataclass(frozen=True)
class OpenChatCutRuntimeConfig:
    endpoint_url: str = OPENCHATCUT_MCP_DEFAULT_URL
    bearer_token: str | None = None
    timeout_seconds: int = 30
    approval_mode: str = "auto"
    client_name: str = OPENCHATCUT_CLIENT_NAME
    client_version: str = OPENCHATCUT_CLIENT_VERSION

    @classmethod
    def from_environment(cls) -> "OpenChatCutRuntimeConfig":
        return cls(
            endpoint_url=os.getenv("OPENCHATCUT_MCP_URL", OPENCHATCUT_MCP_DEFAULT_URL),
            bearer_token=os.getenv("OPENCHATCUT_MCP_TOKEN"),
            timeout_seconds=int(os.getenv("OPENCHATCUT_MCP_TIMEOUT_SECONDS", "30")),
            approval_mode=os.getenv("OPENCHATCUT_APPROVAL_MODE", "auto"),
        )


class _McpStreamableHttpClient:
    def __init__(self, config: OpenChatCutRuntimeConfig, *, opener=urlopen):
        self.config = config
        self._opener = opener
        self._request_id = 0
        self._session_id: str | None = None
        self._lock = threading.Lock()
        self.server_info: dict[str, Any] | None = None

    @property
    def session_id(self) -> str | None:
        return self._session_id

    def _next_id(self) -> int:
        with self._lock:
            self._request_id += 1
            return self._request_id

    @staticmethod
    def _parse_sse(body: str) -> dict[str, Any]:
        payloads: list[str] = []
        data_lines: list[str] = []
        for line in body.splitlines():
            if line.startswith("data:"):
                data_lines.append(line[5:].lstrip())
            elif not line.strip() and data_lines:
                payloads.append("\n".join(data_lines))
                data_lines = []
        if data_lines:
            payloads.append("\n".join(data_lines))
        for payload in reversed(payloads):
            if not payload or payload == "[DONE]":
                continue
            try:
                parsed = json.loads(payload)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                return parsed
        raise OpenChatCutProtocolError("OpenChatCut MCP SSE response contained no JSON-RPC object")

    @classmethod
    def _parse_response(cls, response: HTTPResponse, body: bytes) -> dict[str, Any]:
        content_type = response.headers.get_content_type().lower()
        text = body.decode("utf-8")
        if content_type == "text/event-stream":
            return cls._parse_sse(text)
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as exc:
            raise OpenChatCutProtocolError("OpenChatCut MCP response was not JSON") from exc
        if not isinstance(parsed, dict):
            raise OpenChatCutProtocolError("OpenChatCut MCP response must be a JSON object")
        return parsed

    def request(self, method: str, params: Mapping[str, Any] | None = None) -> dict[str, Any]:
        request_id = self._next_id()
        payload: dict[str, Any] = {"jsonrpc": "2.0", "id": request_id, "method": method}
        if params is not None:
            payload["params"] = dict(params)
        headers = {
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
        }
        if self._session_id:
            headers["MCP-Session-Id"] = self._session_id
        if self.config.bearer_token:
            headers["Authorization"] = f"Bearer {self.config.bearer_token}"
        request = Request(
            self.config.endpoint_url,
            data=json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with self._opener(request, timeout=self.config.timeout_seconds) as response:
                body = response.read()
                session_id = response.headers.get("MCP-Session-Id")
                if session_id:
                    self._session_id = session_id
                result = self._parse_response(response, body)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            raise OpenChatCutUnavailableError(
                f"OpenChatCut MCP endpoint is unreachable: {self.config.endpoint_url}"
            ) from exc
        if result.get("jsonrpc") != "2.0":
            raise OpenChatCutProtocolError("OpenChatCut MCP response is not JSON-RPC 2.0")
        if result.get("id") != request_id:
            raise OpenChatCutProtocolError("OpenChatCut MCP response id does not match request")
        if "error" in result:
            error = result["error"]
            if isinstance(error, Mapping):
                message = str(error.get("message", "unknown MCP error"))
            else:
                message = str(error)
            raise OpenChatCutProtocolError(f"OpenChatCut MCP error: {message}")
        return result

    def initialize(self) -> dict[str, Any]:
        result = self.request(
            "initialize",
            {
                "protocolVersion": OPENCHATCUT_PROTOCOL_VERSION,
                "capabilities": {"roots": {"listChanged": False}},
                "clientInfo": {"name": self.config.client_name, "version": self.config.client_version},
            },
        )
        value = result.get("result")
        if not isinstance(value, Mapping):
            raise OpenChatCutProtocolError("OpenChatCut initialize result is missing")
        server_info = value.get("serverInfo")
        if not isinstance(server_info, Mapping):
            raise OpenChatCutProtocolError("OpenChatCut initialize result is missing serverInfo")
        self.server_info = dict(server_info)
        self.notify("notifications/initialized", {})
        return dict(value)

    def notify(self, method: str, params: Mapping[str, Any] | None = None) -> None:
        payload: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            payload["params"] = dict(params)
        headers = {
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
        }
        if self._session_id:
            headers["MCP-Session-Id"] = self._session_id
        if self.config.bearer_token:
            headers["Authorization"] = f"Bearer {self.config.bearer_token}"
        request = Request(
            self.config.endpoint_url,
            data=json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with self._opener(request, timeout=self.config.timeout_seconds) as response:
                response.read()
                session_id = response.headers.get("MCP-Session-Id")
                if session_id:
                    self._session_id = session_id
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            raise OpenChatCutUnavailableError(
                f"OpenChatCut MCP endpoint is unreachable: {self.config.endpoint_url}"
            ) from exc

    def list_tools(self) -> list[dict[str, Any]]:
        result = self.request("tools/list", {})
        tools = result.get("result", {}).get("tools")
        if not isinstance(tools, list):
            raise OpenChatCutProtocolError("OpenChatCut tools/list result is missing tools")
        return [dict(tool) for tool in tools if isinstance(tool, Mapping)]

    def call_tool(self, name: str, arguments: Mapping[str, Any] | None = None) -> Any:
        result = self.request("tools/call", {"name": name, "arguments": dict(arguments or {})})
        envelope = result.get("result")
        if not isinstance(envelope, Mapping):
            raise OpenChatCutProtocolError(f"OpenChatCut tool {name} returned no result envelope")
        if envelope.get("isError") is True:
            raise OpenChatCutProtocolError(f"OpenChatCut tool {name} returned isError=true")
        structured = envelope.get("structuredContent")
        if structured is not None:
            return structured
        content = envelope.get("content")
        if not isinstance(content, list):
            return envelope
        for entry in content:
            if not isinstance(entry, Mapping) or entry.get("type") != "text":
                continue
            text = entry.get("text")
            if isinstance(text, str):
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return {"text": text}
        return envelope


def _frame_count_from_ms(start_ms: int, end_ms: int, fps_num: int, fps_den: int, *, field: str) -> tuple[int, int]:
    if end_ms <= start_ms:
        raise PipelineValidationError(f"{field} must be a positive interval")
    start_frames = Fraction(start_ms * fps_num, 1000 * fps_den)
    end_frames = Fraction(end_ms * fps_num, 1000 * fps_den)
    if start_frames.denominator != 1 or end_frames.denominator != 1:
        raise PipelineValidationError(
            f"{field} is not frame-exact at program fps {fps_num}/{fps_den}: "
            f"{start_ms}->{end_ms} ms maps to {start_frames}->{end_frames} frames"
        )
    start_frame = start_frames.numerator
    duration = end_frames.numerator - start_frame
    if duration <= 0:
        raise PipelineValidationError(f"{field} maps to a non-positive frame duration")
    return start_frame, duration


def _track_kind(track_type: str) -> str:
    if track_type == "AUDIO":
        return "audio"
    if track_type == "CAPTION":
        return "caption"
    return "video"


def _element_type(element: Mapping[str, Any], track_type: str) -> str:
    if track_type == "CAPTION":
        if element["kind"] != "TEXT" or element["text"] == "NOT_APPLICABLE":
            raise PipelineValidationError(
                f"caption element {element['element_id']} must be TEXT with text content for native OpenChatCut"
            )
        return "text"
    if element["kind"] == "TEXT":
        return "text"
    if track_type == "AUDIO" or element["kind"] == "AUDIO":
        return "audio"
    if element["kind"] in {"APPROVED_ASSET", "SOURCE_SEGMENT", "MOTION_SLOT", "GENERATED_SLOT"}:
        return "video"
    raise PipelineValidationError(f"unsupported OpenChatCut element kind {element['kind']}")



def _extract_id(value: Any, candidate_keys: tuple[str, ...]) -> str | None:
    if isinstance(value, Mapping):
        for key in candidate_keys:
            raw = value.get(key)
            if isinstance(raw, str) and raw.strip():
                return raw.strip()
        for child in value.values():
            found = _extract_id(child, candidate_keys)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = _extract_id(child, candidate_keys)
            if found:
                return found
    return None


def _unwrap(value: Any) -> Any:
    if isinstance(value, Mapping):
        if set(value) == {"text"}:
            try:
                return json.loads(str(value["text"]))
            except json.JSONDecodeError:
                return value
        for key in ("result", "data", "timeline", "project"):
            if key in value and isinstance(value[key], (Mapping, list)):
                return value[key]
    return value


class OpenChatCutRuntimeAdapter:
    """Translate a canonical CAE Video Edit Program into native OpenChatCut commands."""

    def __init__(self, repository: PipelineRepository, config: OpenChatCutRuntimeConfig | None = None):
        self.repository = repository
        self.config = config or OpenChatCutRuntimeConfig.from_environment()

    @staticmethod
    def _validate_program(program: Mapping[str, Any]) -> None:
        required = {
            "program_id",
            "program_version",
            "derivative_job_ref",
            "source_registration_ref",
            "semantic_production_package_ref",
            "final_script_ref",
            "activation_transfer_contract_ref",
            "harness_binding_ref",
            "evaluation_profile_ref",
            "source_media_ref",
            "source_media_sha256",
            "source_authority",
            "canvas",
            "timebase",
            "tracks",
            "timeline_authority",
            "source_a_roll_required",
            "production_authorized",
        }
        missing = sorted(required - set(program))
        if missing:
            raise PipelineValidationError(f"video edit program is missing governed fields: {missing}")
        require_ref(program["source_registration_ref"], "source_registration_ref")
        if program["timeline_authority"] != "CANONICAL_VIDEO_EDIT_PROGRAM":
            raise OpenChatCutRuntimeError("OpenChatCut handoff requires CAE canonical timeline authority")
        if program["source_a_roll_required"] is not True:
            raise OpenChatCutRuntimeError("OpenChatCut handoff requires source A-roll spine")
        if program["production_authorized"] is not False:
            raise OpenChatCutRuntimeError("CAE must remain non-authorized for final production at M0065")
        require_string(program["source_authority"], "source_authority")

    @staticmethod
    def _tool_names(tools: list[dict[str, Any]]) -> set[str]:
        return {str(tool.get("name")) for tool in tools if str(tool.get("name", "")).strip()}

    def _require_tools(self, tools: set[str], required: set[str]) -> None:
        missing = sorted(required - tools)
        if missing:
            raise OpenChatCutRuntimeError(f"OpenChatCut runtime is missing required tools: {missing}")

    def _project(self, client: _McpStreamableHttpClient, project_id: str | None, program: Mapping[str, Any]) -> str:
        if project_id:
            client.call_tool("target_project", {"projectId": project_id})
            return project_id
        name = f"CAE {program['program_id']}"
        created = client.call_tool(
            "create_project",
            {
                "name": name,
                "description": "CAE-M0065 canonical video program handoff; CAE remains system of record.",
                "compositionWidth": program["canvas"]["width"],
                "compositionHeight": program["canvas"]["height"],
                "fps": Fraction(program["canvas"]["fps_numerator"], program["canvas"]["fps_denominator"]).numerator
                / Fraction(program["canvas"]["fps_numerator"], program["canvas"]["fps_denominator"]).denominator,
            },
        )
        created_id = _extract_id(created, ("id", "projectId"))
        if not created_id:
            raise OpenChatCutProtocolError("OpenChatCut create_project returned no project id")
        client.call_tool("target_project", {"projectId": created_id})
        return created_id

    @staticmethod
    def _read_timeline(client: _McpStreamableHttpClient, project_id: str, edit_session_id: str) -> Mapping[str, Any]:
        value = client.call_tool(
            "read_timeline",
            {"editorProjectId": project_id, "editSessionId": edit_session_id},
        )
        unwrapped = _unwrap(value)
        if not isinstance(unwrapped, Mapping):
            raise OpenChatCutProtocolError("OpenChatCut read_timeline did not return an object")
        return unwrapped

    @staticmethod
    def _native_items(timeline: Mapping[str, Any]) -> list[Mapping[str, Any]]:
        raw = timeline.get("items", [])
        if isinstance(raw, list):
            return [dict(item) for item in raw if isinstance(item, Mapping)]
        return []

    def _create_tracks(
        self,
        client: _McpStreamableHttpClient,
        project_id: str,
        edit_session_id: str,
        tracks: list[Mapping[str, Any]],
    ) -> dict[str, str]:
        native_before = self._read_timeline(client, project_id, edit_session_id)
        existing_by_name = {
            str(track.get("name")): str(track.get("id") or track.get("alias"))
            for track in native_before.get("tracks", [])
            if isinstance(track, Mapping) and track.get("name")
        }
        mapping: dict[str, str] = {}
        for index, track in enumerate(tracks):
            track_id = str(track["track_id"])
            track_name = f"CAE::{track['role']}::{track_id}"
            if track_name in existing_by_name:
                mapping[track_id] = existing_by_name[track_name]
                continue
            track_type = _track_kind(str(track["track_type"]))
            created = client.call_tool(
                "edit_track",
                {
                    "editorProjectId": project_id,
                    "editSessionId": edit_session_id,
                    "action": "create",
                    "json": json.dumps(
                        {
                            "trackType": track_type,
                            "name": track_name,
                            "role": "anchor" if track["role"] == "PRIMARY_A_ROLL_SPINE" else "follower",
                            "order": index,
                        },
                        separators=(",", ":"),
                    ),
                },
            )
            created_alias = _extract_id(created, ("id", "trackId", "alias"))
            if not created_alias:
                # A successful result without an id is still actionable if the readback exposes a new alias/name.
                after = self._read_timeline(client, project_id, edit_session_id)
                for native_track in after.get("tracks", []):
                    if isinstance(native_track, Mapping) and native_track.get("name") == track_name:
                        created_alias = str(native_track.get("id") or native_track.get("alias"))
                        break
            if not created_alias:
                raise OpenChatCutProtocolError(f"OpenChatCut edit_track create did not return {track_id}")
            mapping[track_id] = created_alias
        return mapping

    @staticmethod
    def _asset_key(element: Mapping[str, Any]) -> str | None:
        for field in ("source_registration_ref", "artifact_ref"):
            value = element.get(field)
            if isinstance(value, Mapping):
                object_id = value.get("object_id")
                if isinstance(object_id, str):
                    return object_id
        return None

    def _import_assets(
        self,
        client: _McpStreamableHttpClient,
        project_id: str,
        media_paths: Mapping[str, str | Path],
        program: Mapping[str, Any],
    ) -> tuple[dict[str, str], dict[str, str]]:
        keys: set[str] = set()
        for track in program["tracks"]:
            for element in track["elements"]:
                key = self._asset_key(element)
                if key and key != "NOT_APPLICABLE":
                    keys.add(key)
        source_id = program["source_registration_ref"]["object_id"]
        keys.add(source_id)
        missing = sorted(key for key in keys if key not in media_paths)
        if missing:
            raise PipelineValidationError(f"OpenChatCut handoff is missing local media paths for: {missing}")
        result: dict[str, str] = {}
        observed_digests: dict[str, str] = {}
        source_id = program["source_registration_ref"]["object_id"]
        resolved_paths: dict[str, Path] = {}
        for key in sorted(keys):
            path = Path(media_paths[key]).expanduser()
            if not path.is_file():
                raise PipelineValidationError(f"OpenChatCut media path does not exist: {key}")
            resolved_paths[key] = path
            digest = hashlib.sha256()
            with path.open("rb") as source_file:
                for chunk in iter(lambda: source_file.read(1024 * 1024), b""):
                    digest.update(chunk)
            observed_sha256 = digest.hexdigest()
            observed_digests[key] = observed_sha256
            if key == source_id and observed_sha256 != program["source_media_sha256"]:
                raise PipelineValidationError(
                    f"OpenChatCut source bytes do not match CAE source_media_sha256: expected {program['source_media_sha256']}, observed {observed_sha256}"
                )
        for key in sorted(keys):
            imported = client.call_tool(
                "import_asset",
                {
                    "editorProjectId": project_id,
                    "path": str(resolved_paths[key]),
                },
            )
            asset_id = _extract_id(imported, ("assetId", "id"))
            if not asset_id:
                raise OpenChatCutProtocolError(f"OpenChatCut import_asset returned no asset id for {key}")
            result[key] = asset_id
        return result, observed_digests

    def _build_adds(
        self,
        program: Mapping[str, Any],
        track_map: Mapping[str, str],
        asset_map: Mapping[str, str],
    ) -> list[dict[str, Any]]:
        fps_num = int(program["canvas"]["fps_numerator"])
        fps_den = int(program["canvas"]["fps_denominator"])
        adds: list[dict[str, Any]] = []
        for track in program["tracks"]:
            native_track = track_map[track["track_id"]]
            for element in track["elements"]:
                element_type = _element_type(element, track["track_type"])
                out_start, out_duration = _frame_count_from_ms(
                    int(element["output_start_ms"]),
                    int(element["output_end_ms"]),
                    fps_num,
                    fps_den,
                    field=f"{element['element_id']}.output",
                )
                semantic_label = f"CAE::{element['semantic_role']}::{element['sequence_role']}::{element['element_id']}"
                if element_type == "text":
                    adds.append(
                        {
                            "type": "text",
                            "track": native_track,
                            "fromFrame": out_start,
                            "durationInFrames": out_duration,
                            "name": semantic_label,
                            "text": element["text"],
                        }
                    )
                    continue
                key = self._asset_key(element)
                if not key:
                    raise PipelineValidationError(f"media element {element['element_id']} has no CAE media identity")
                asset_id = asset_map[key]
                add: dict[str, Any] = {
                    "type": element_type,
                    "assetId": asset_id,
                    "track": native_track,
                    "fromFrame": out_start,
                    "durationInFrames": out_duration,
                }
                if element["kind"] == "SOURCE_SEGMENT":
                    source_start, source_duration = _frame_count_from_ms(
                        int(element["source_start_ms"]),
                        int(element["source_end_ms"]),
                        fps_num,
                        fps_den,
                        field=f"{element['element_id']}.source",
                    )
                    add["sourceStartFrame"] = source_start
                    add["sourceDurationInFrames"] = source_duration
                adds.append(add)
        return adds

    @staticmethod
    def _verify_native_timeline(
        timeline: Mapping[str, Any],
        program: Mapping[str, Any],
        track_map: Mapping[str, str],
        asset_map: Mapping[str, str],
    ) -> dict[str, Any]:
        native_items = OpenChatCutRuntimeAdapter._native_items(timeline)
        expected_elements = [
            element
            for track in program["tracks"]
            for element in track["elements"]
        ]
        if len(native_items) != len(expected_elements):
            raise OpenChatCutTimelineVerificationError(
                f"native timeline item count {len(native_items)} != CAE element count {len(expected_elements)}"
            )
        fps_num = int(program["canvas"]["fps_numerator"])
        fps_den = int(program["canvas"]["fps_denominator"])
        verified: list[dict[str, Any]] = []
        for track in program["tracks"]:
            for element in track["elements"]:
                output_start, output_duration = _frame_count_from_ms(
                    int(element["output_start_ms"]),
                    int(element["output_end_ms"]),
                    fps_num,
                    fps_den,
                    field=f"{element['element_id']}.output",
                )
                expected_asset_id = None
                if element["kind"] != "TEXT":
                    key = OpenChatCutRuntimeAdapter._asset_key(element)
                    if key is None:
                        raise OpenChatCutTimelineVerificationError(f"media identity missing for {element['element_id']}")
                    expected_asset_id = asset_map[key]
                native_track = track_map[track["track_id"]]
                candidates = [
                    item for item in native_items
                    if str(item.get("track") or item.get("trackId") or "") == native_track
                    and int(item.get("startFrame", item.get("fromFrame", -1))) == output_start
                    and int(item.get("durationInFrames", -1)) == output_duration
                    and (expected_asset_id is None or item.get("sourceAssetId") == expected_asset_id or item.get("assetId") == expected_asset_id)
                ]
                if len(candidates) != 1:
                    raise OpenChatCutTimelineVerificationError(
                        f"native item identity is ambiguous or missing for {element['element_id']}: {len(candidates)} candidates"
                    )
                item = candidates[0]
                actual_track = str(item.get("track") or item.get("trackId") or "")
                expected_track = track_map[track["track_id"]]
                if actual_track not in {expected_track, str(track["track_id"])}:
                    raise OpenChatCutTimelineVerificationError(
                        f"native item {element['element_id']} is on {actual_track}, expected {expected_track}"
                    )
                actual_start = int(item.get("startFrame", item.get("fromFrame", -1)))
                actual_duration = int(item.get("durationInFrames", -1))
                if actual_start != output_start or actual_duration != output_duration:
                    raise OpenChatCutTimelineVerificationError(
                        f"native output timing mismatch for {element['element_id']}: "
                        f"got {actual_start}/{actual_duration}, expected {output_start}/{output_duration}"
                    )
                record: dict[str, Any] = {
                    "element_id": element["element_id"],
                    "semantic_role": element["semantic_role"],
                    "sequence_role": element["sequence_role"],
                    "native_item_id": str(item.get("id", "")),
                    "native_track": actual_track,
                    "native_source_asset_id": item.get("sourceAssetId", item.get("assetId")),
                    "output_start_frame": output_start,
                    "output_duration_frames": output_duration,
                }
                if element["kind"] == "SOURCE_SEGMENT":
                    source_start, source_duration = _frame_count_from_ms(
                        int(element["source_start_ms"]),
                        int(element["source_end_ms"]),
                        fps_num,
                        fps_den,
                        field=f"{element['element_id']}.source",
                    )
                    actual_src = int(item.get("srcInFrame", item.get("sourceStartFrame", -1)))
                    if actual_src != source_start:
                        raise OpenChatCutTimelineVerificationError(
                            f"native source in mismatch for {element['element_id']}: got {actual_src}, expected {source_start}"
                        )
                    record["source_start_frame"] = source_start
                    record["source_duration_frames"] = source_duration
                verified.append(record)
        return {
            "native_item_count": len(native_items),
            "verified_elements": verified,
            "timeline_fidelity": "NATIVE_TIMELINE_VERIFIED",
        }

    @staticmethod
    def _native_item_sort_key(item: Mapping[str, Any]) -> tuple[int, str]:
        return (
            int(item.get("startFrame", item.get("fromFrame", -1))),
            str(item.get("id", "")),
        )

    @staticmethod
    def inspect_native_timeline(
        timeline: Mapping[str, Any],
        program: Mapping[str, Any],
        track_map: Mapping[str, str],
        asset_map: Mapping[str, str],
    ) -> dict[str, Any]:
        """Compare native OpenChatCut state to CAE without mutating either side.

        Matching is deterministic by CAE track order plus native item start/id order.
        Topology changes, moves, substitutions, or ambiguous identity are never auto-
        reconciled; timing-only changes can be handed to the existing CAE human-
        resolution path after operator review.
        """
        native_items = OpenChatCutRuntimeAdapter._native_items(timeline)
        fps_num = int(program["canvas"]["fps_numerator"])
        fps_den = int(program["canvas"]["fps_denominator"])
        native_tracks = [
            dict(track) for track in timeline.get("tracks", [])
            if isinstance(track, Mapping)
        ]
        native_track_ids = {
            str(track.get("id") or track.get("alias") or ""): track
            for track in native_tracks
        }
        diffs: list[dict[str, Any]] = []
        candidates: list[dict[str, Any]] = []
        matched_items: list[dict[str, Any]] = []
        expected_total = 0

        for track in program["tracks"]:
            track_id = str(track["track_id"])
            native_track = str(track_map.get(track_id, ""))
            if not native_track or native_track not in native_track_ids:
                diffs.append({
                    "type": "TRACK_MISSING",
                    "track_id": track_id,
                    "native_track": native_track,
                    "severity": "BLOCKING",
                })
                continue
            actual = sorted(
                [
                    item for item in native_items
                    if str(item.get("track") or item.get("trackId") or "") == native_track
                ],
                key=OpenChatCutRuntimeAdapter._native_item_sort_key,
            )
            expected = list(track["elements"])
            expected_total += len(expected)
            if len(actual) != len(expected):
                diffs.append({
                    "type": "TOPOLOGY_DIVERGENCE",
                    "track_id": track_id,
                    "expected_item_count": len(expected),
                    "native_item_count": len(actual),
                    "severity": "BLOCKING",
                    "reconciliation": "OPERATOR_REQUIRED",
                })
                continue
            for ordinal, (element, item) in enumerate(zip(expected, actual)):
                output_start, output_duration = _frame_count_from_ms(
                    int(element["output_start_ms"]),
                    int(element["output_end_ms"]),
                    fps_num, fps_den,
                    field=f"{element['element_id']}.output",
                )
                actual_start = int(item.get("startFrame", item.get("fromFrame", -1)))
                actual_duration = int(item.get("durationInFrames", -1))
                expected_asset_id = None
                if element["kind"] != "TEXT":
                    key = OpenChatCutRuntimeAdapter._asset_key(element)
                    if not key or key not in asset_map:
                        diffs.append({
                            "type": "CAE_ASSET_IDENTITY_MISSING",
                            "element_id": element["element_id"],
                            "severity": "BLOCKING",
                        })
                        continue
                    expected_asset_id = asset_map[key]
                actual_asset_id = item.get("sourceAssetId", item.get("assetId"))
                timing_changed = actual_start != output_start or actual_duration != output_duration
                asset_changed = expected_asset_id is not None and actual_asset_id != expected_asset_id
                source_changed = False
                source_expected_start = None
                source_expected_duration = None
                if element["kind"] == "SOURCE_SEGMENT":
                    source_expected_start, source_expected_duration = _frame_count_from_ms(
                        int(element["source_start_ms"]),
                        int(element["source_end_ms"]),
                        fps_num, fps_den,
                        field=f"{element['element_id']}.source",
                    )
                    actual_source_start = int(item.get("srcInFrame", item.get("sourceStartFrame", -1)))
                    actual_source_duration = int(item.get("sourceDurationInFrames", -1))
                    source_changed = (
                        actual_source_start != source_expected_start
                        or actual_source_duration not in {-1, source_expected_duration}
                    )
                text_changed = False
                text_unverifiable = False
                if element["kind"] == "TEXT" and "text" in element:
                    native_text = item.get("text")
                    if native_text is None and isinstance(item.get("props"), Mapping):
                        native_text = item["props"].get("text")
                    if native_text is None:
                        text_unverifiable = True
                    else:
                        text_changed = str(native_text) != str(element["text"])
                entry = {
                    "element_id": element["element_id"],
                    "ordinal": ordinal,
                    "native_item_id": str(item.get("id", "")),
                    "native_track": native_track,
                    "expected_start_frame": output_start,
                    "actual_start_frame": actual_start,
                    "expected_duration_frames": output_duration,
                    "actual_duration_frames": actual_duration,
                    "expected_source_asset_id": expected_asset_id,
                    "actual_source_asset_id": actual_asset_id,
                    "source_changed": source_changed,
                    "text_changed": text_changed,
                    "text_unverifiable": text_unverifiable,
                }
                matched_items.append(entry)
                if asset_changed:
                    diffs.append({
                        "type": "ASSET_DIVERGENCE",
                        "element_id": element["element_id"],
                        "native_item_id": entry["native_item_id"],
                        "expected_source_asset_id": expected_asset_id,
                        "actual_source_asset_id": actual_asset_id,
                        "severity": "BLOCKING",
                        "reconciliation": "SUBSTITUTE_ASSET_REQUIRES_HUMAN_RESOLUTION",
                    })
                elif source_changed:
                    diffs.append({
                        "type": "SOURCE_WINDOW_DIVERGENCE",
                        "element_id": element["element_id"],
                        "native_item_id": entry["native_item_id"],
                        "expected_source_start_frame": source_expected_start,
                        "actual_source_start_frame": int(item.get("srcInFrame", item.get("sourceStartFrame", -1))),
                        "expected_source_duration_frames": source_expected_duration,
                        "actual_source_duration_frames": int(item.get("sourceDurationInFrames", -1)),
                        "severity": "BLOCKING",
                        "reconciliation": "HUMAN_RESOLUTION_REQUIRED",
                    })
                if text_unverifiable:
                    diffs.append({
                        "type": "TEXT_UNVERIFIABLE",
                        "element_id": element["element_id"],
                        "severity": "BLOCKING",
                        "reconciliation": "OPERATOR_REQUIRED",
                    })
                elif text_changed:
                    diffs.append({
                        "type": "TEXT_DIVERGENCE",
                        "element_id": element["element_id"],
                        "severity": "BLOCKING",
                        "reconciliation": "HUMAN_RESOLUTION_REQUIRED",
                    })
                if timing_changed:
                    if actual_start != output_start:
                        diffs.append({
                            "type": "MOVE_DIVERGENCE",
                            "element_id": element["element_id"],
                            "native_item_id": entry["native_item_id"],
                            "expected_start_frame": output_start,
                            "actual_start_frame": actual_start,
                            "severity": "BLOCKING",
                            "reconciliation": "HUMAN_RESOLUTION_REQUIRED",
                        })
                    elif actual_duration <= 0:
                        diffs.append({
                            "type": "INVALID_DURATION",
                            "element_id": element["element_id"],
                            "actual_duration_frames": actual_duration,
                            "severity": "BLOCKING",
                            "reconciliation": "REJECT",
                        })
                    else:
                        delta_frames = actual_duration - output_duration
                        if abs(delta_frames) <= 300:
                            candidates.append({
                                "target_node_id": element["element_id"],
                                "manipulation_type": "ADJUST_TIMING",
                                "arguments": {
                                    "delta_frames": delta_frames,
                                    "source_start_delta_ms": 0,
                                    "source_end_delta_ms": 0,
                                },
                                "native_item_id": entry["native_item_id"],
                                "requires_operator_approval": True,
                            })
                            diffs.append({
                                "type": "TIMING_DIVERGENCE",
                                "element_id": element["element_id"],
                                "native_item_id": entry["native_item_id"],
                                "delta_frames": delta_frames,
                                "severity": "REVIEW",
                                "reconciliation": "ADJUST_TIMING_VIA_CAE_HUMAN_RESOLUTION",
                            })
                        else:
                            diffs.append({
                                "type": "TIMING_OUT_OF_BOUNDS",
                                "element_id": element["element_id"],
                                "native_item_id": entry["native_item_id"],
                                "delta_frames": delta_frames,
                                "severity": "BLOCKING",
                                "reconciliation": "REJECT",
                            })

        if len(native_items) != expected_total:
            global_native_count = len(native_items)
            if not any(d.get("type") == "TOPOLOGY_DIVERGENCE" for d in diffs):
                diffs.append({
                    "type": "GLOBAL_ITEM_COUNT_DIVERGENCE",
                    "expected_item_count": expected_total,
                    "native_item_count": global_native_count,
                    "severity": "BLOCKING",
                    "reconciliation": "OPERATOR_REQUIRED",
                })

        status = "IN_SYNC" if not diffs else "DIVERGED"
        safe_updates = [d for d in diffs if d.get("reconciliation") == "ADJUST_TIMING_VIA_CAE_HUMAN_RESOLUTION"]
        blocked = [d for d in diffs if d.get("severity") == "BLOCKING"]
        return {
            "invariant": OPENCHATCUT_BIDIRECTIONAL_INVARIANT,
            "status": status,
            "safe_update_boundary": "CAE_HUMAN_RESOLUTION_ONLY",
            "auto_apply": False,
            "native_fps": timeline.get("fps"),
            "program_timeline_authority": program.get("timeline_authority"),
            "program_sha256": canonical_sha256(program),
            "source_media_sha256": program.get("source_media_sha256"),
            "native_timeline_sha256": canonical_sha256(timeline),
            "native_item_count": len(native_items),
            "expected_item_count": expected_total,
            "matched_items": matched_items,
            "differences": diffs,
            "reconciliation_candidates": candidates,
            "blocking_difference_count": len(blocked),
            "timing_review_count": len(safe_updates),
            "source_hash_contact": "CAE_SOURCE_MEDIA_SHA256_ONLY",
        }

    def inspect_runtime(
        self,
        program_id: str,
        *,
        project_id: str,
        track_map: Mapping[str, str],
        asset_map: Mapping[str, str],
    ) -> dict[str, Any]:
        """Read native runtime state in a discarded edit session and classify divergence."""
        program_obj = self.repository.get_object(program_id)
        program = program_obj["payload"]
        self._validate_program(program)
        client = _McpStreamableHttpClient(self.config)
        try:
            client.initialize()
            tools = self._tool_names(client.list_tools())
            self._require_tools(tools, {"target_project", "begin_edit_session", "read_timeline", "discard_edit_session"})
            client.call_tool("target_project", {"projectId": project_id})
            begun = client.call_tool(
                "begin_edit_session",
                {"editorProjectId": project_id, "approvalMode": "manual"},
            )
            edit_session_id = _extract_id(begun, ("editSessionId", "id"))
            if not edit_session_id:
                raise OpenChatCutProtocolError("OpenChatCut begin_edit_session returned no editSessionId")
            timeline = self._read_timeline(client, project_id, edit_session_id)
            report = self.inspect_native_timeline(timeline, program, track_map, asset_map)
            report["runtime_identity"] = {
                "server_name": str(client.server_info.get("name", "")) if client.server_info else "",
                "server_version": str(client.server_info.get("version", "")) if client.server_info else "",
                "endpoint_transport": "streamable_http_mcp",
            }
            client.call_tool("discard_edit_session", {"editorProjectId": project_id, "editSessionId": edit_session_id})
            report["edit_session_disposition"] = "DISCARDED_AFTER_READ"
            return report
        except OpenChatCutRuntimeError:
            raise
        except Exception as exc:
            raise OpenChatCutTimelineInspectionError(str(exc)) from exc

    @staticmethod
    def build_human_resolution_request(inspection: Mapping[str, Any], candidate_index: int = 0) -> dict[str, Any]:
        candidates = inspection.get("reconciliation_candidates")
        if not isinstance(candidates, list) or not candidates:
            raise OpenChatCutTimelineInspectionError("no safe native timing reconciliation candidate exists")
        try:
            candidate = candidates[candidate_index]
        except (IndexError, TypeError) as exc:
            raise OpenChatCutTimelineInspectionError("requested reconciliation candidate does not exist") from exc
        if candidate.get("manipulation_type") != "ADJUST_TIMING" or candidate.get("requires_operator_approval") is not True:
            raise OpenChatCutTimelineInspectionError("native update boundary only permits approved ADJUST_TIMING requests")
        return {
            "target_node_id": candidate["target_node_id"],
            "manipulation_type": "ADJUST_TIMING",
            "arguments": dict(candidate["arguments"]),
            "source": {
                "inspection_invariant": inspection.get("invariant"),
                "native_timeline_sha256": inspection.get("native_timeline_sha256"),
                "program_sha256": inspection.get("program_sha256"),
            },
            "operator_required": True,
            "apply_via": "api.services.human_resolution.compile_native_edit_program -> commit_native_edit",
            "direct_runtime_write": False,
        }

    def handoff(
        self,
        program_id: str,
        *,
        media_paths: Mapping[str, str | Path],
        project_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        if self.config.approval_mode not in {"auto", "manual"}:
            raise PipelineValidationError("OpenChatCut approval_mode must be auto or manual")
        program_obj = self.repository.get_object(program_id)
        program = program_obj["payload"]
        self._validate_program(program)
        client = _McpStreamableHttpClient(self.config)
        try:
            initialized = client.initialize()
            tools = client.list_tools()
            tool_names = self._tool_names(tools)
            self._require_tools(
                tool_names,
                {"create_project", "target_project", "begin_edit_session", "review_edit_session", "read_timeline", "edit_track", "edit_item", "import_asset"},
            )
            runtime_identity = {
                "server_name": str(client.server_info.get("name", "")) if client.server_info else "",
                "server_version": str(client.server_info.get("version", "")) if client.server_info else "",
                "protocol_version": str(initialized.get("protocolVersion", "")),
                "client_name": self.config.client_name,
                "client_version": self.config.client_version,
                "endpoint_transport": "streamable_http_mcp",
            }
            selected_project_id = self._project(client, project_id, program)
            bound_state = client.call_tool("openchatcut_status", {})
            asset_map, imported_media_sha256 = self._import_assets(client, selected_project_id, media_paths, program)
            begun = client.call_tool(
                "begin_edit_session",
                {
                    "editorProjectId": selected_project_id,
                    "approvalMode": self.config.approval_mode,
                },
            )
            edit_session_id = _extract_id(begun, ("editSessionId", "id"))
            if not edit_session_id:
                raise OpenChatCutProtocolError("OpenChatCut begin_edit_session returned no editSessionId")
            timeline_before = self._read_timeline(client, selected_project_id, edit_session_id)
            track_map = self._create_tracks(client, selected_project_id, edit_session_id, list(program["tracks"]))
            adds = self._build_adds(program, track_map, asset_map)
            if adds:
                client.call_tool(
                    "edit_item",
                    {
                        "editorProjectId": selected_project_id,
                        "editSessionId": edit_session_id,
                        "adds": adds,
                        "updates": [],
                        "deletes": [],
                    },
                )
            review = client.call_tool(
                "review_edit_session",
                {"editorProjectId": selected_project_id, "editSessionId": edit_session_id},
            )
            review_status = str(_unwrap(review).get("status", "")) if isinstance(_unwrap(review), Mapping) else ""
            if self.config.approval_mode == "manual" and review_status != "applied":
                state = OPENCHATCUT_STATE_BLOCKED
                verification: dict[str, Any] = {"timeline_fidelity": "OPERATOR_APPROVAL_REQUIRED", "verified": False}
            else:
                timeline_after = self._read_timeline(client, selected_project_id, edit_session_id)
                verification = self._verify_native_timeline(timeline_after, program, track_map, asset_map)
                state = OPENCHATCUT_STATE_EXECUTED
            receipt_core = {
                "mandate_id": "CAE-M0065",
                "mandate_title": "Native OpenChatCut Runtime and Timeline Handoff",
                "invariant": OPENCHATCUT_INVARIANT,
                "state": state,
                "program_ref": {
                    "object_id": program_obj["object_id"],
                    "version": program_obj["semantic_version"],
                    "sha256": program_obj["canonical_sha256"],
                },
                "timeline_authority": program["timeline_authority"],
                "source_media_ref": program["source_media_ref"],
                "source_media_sha256": program["source_media_sha256"],
                "source_authority": program["source_authority"],
                "workspace_refs": {
                    "derivative_job_ref": program["derivative_job_ref"],
                    "semantic_production_package_ref": program["semantic_production_package_ref"],
                    "final_script_ref": program["final_script_ref"],
                    "activation_transfer_contract_ref": program["activation_transfer_contract_ref"],
                    "harness_binding_ref": program["harness_binding_ref"],
                    "evaluation_profile_ref": program["evaluation_profile_ref"],
                },
                "runtime_identity": runtime_identity,
                "project_id": selected_project_id,
                "edit_session_id": edit_session_id,
                "bound_state": bound_state,
                "state_sequence": [OPENCHATCUT_STATE_BOUND, OPENCHATCUT_STATE_ADAPT, OPENCHATCUT_STATE_READY, state],
                "track_map": track_map,
                "asset_map": asset_map,
                "imported_media_sha256": imported_media_sha256,
                "timeline_before_digest": canonical_sha256(timeline_before),
                "review_status": review_status,
                "verification": verification,
                "operator_gate": {
                    "question": "Do you accept M0065 and authorize M0066?",
                    "choices": ["ACCEPT", "ACCEPT WITH LIMITATIONS", "REPAIR", "BLOCK"],
                    "decision": None,
                },
            }
            receipt_core["receipt_id"] = semantic_identity("openchatcut-handoff", receipt_core)
            reject_noncanonical(receipt_core)
            stored = self.repository.store_object(
                "openchatcut_runtime_handoff_receipt",
                receipt_core,
                idempotency_key=idempotency_key or f"openchatcut:{program_id}:{uuid4().hex}",
                object_id=receipt_core["receipt_id"],
                lifecycle_state=state,
            )
            self.repository.add_edge(program_id, receipt_core["receipt_id"], "openchatcut_runtime_handoff")
            return stored["object"]
        except OpenChatCutRuntimeError as exc:
            runtime_identity = {
                "endpoint_transport": "streamable_http_mcp",
                "reachable": getattr(client, "server_info", None) is not None,
            }
            server_info = getattr(client, "server_info", None)
            if server_info:
                runtime_identity.update({
                    "server_name": str(server_info.get("name", "")),
                    "server_version": str(server_info.get("version", "")),
                })
            receipt_core = {
                "mandate_id": "CAE-M0065",
                "mandate_title": "Native OpenChatCut Runtime and Timeline Handoff",
                "invariant": OPENCHATCUT_INVARIANT,
                "state": OPENCHATCUT_STATE_BLOCKED,
                "program_ref": {
                    "object_id": program_obj["object_id"],
                    "version": program_obj["semantic_version"],
                    "sha256": program_obj["canonical_sha256"],
                },
                "timeline_authority": program["timeline_authority"],
                "source_media_ref": program["source_media_ref"],
                "source_media_sha256": program["source_media_sha256"],
                "source_authority": program["source_authority"],
                "runtime_identity": runtime_identity,
                "state_sequence": [OPENCHATCUT_STATE_BOUND, OPENCHATCUT_STATE_BLOCKED],
                "blocking_reason": str(exc),
                "operator_gate": {
                    "question": "Do you accept M0065 and authorize M0066?",
                    "choices": ["ACCEPT", "ACCEPT WITH LIMITATIONS", "REPAIR", "BLOCK"],
                    "decision": None,
                },
            }
            receipt_core["receipt_id"] = semantic_identity("openchatcut-handoff", receipt_core)
            reject_noncanonical(receipt_core)
            stored = self.repository.store_object(
                "openchatcut_runtime_handoff_receipt",
                receipt_core,
                idempotency_key=idempotency_key or f"openchatcut-blocked:{program_id}:{canonical_sha256({"error": str(exc)})}",
                object_id=receipt_core["receipt_id"],
                lifecycle_state=OPENCHATCUT_STATE_BLOCKED,
            )
            self.repository.add_edge(program_id, receipt_core["receipt_id"], "openchatcut_runtime_handoff_blocked")
            return stored["object"]
