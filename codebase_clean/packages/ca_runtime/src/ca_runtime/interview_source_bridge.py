"""Read-only bridge from an existing Interview Expression package to CAE.

The bridge validates the legacy immutable package and local media bytes before
copying the bytes to private Supabase Storage. It then calls CAE's typed source
registration operation. It never writes to the Interview Expression SQLite DB.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Mapping
from urllib.error import HTTPError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

import psycopg

from ca_contracts import canonical_sha256

from .semantic_operations import FirstSliceSemanticOperations, OperationReceipt, SemanticOperationError


class InterviewSourceBridgeError(RuntimeError):
    """The legacy source cannot be verified and bridged safely."""


class InterviewExpressionSourceBridge:
    """Copies one verified source package without changing legacy authority."""

    def __init__(
        self,
        connection: psycopg.Connection[Any],
        *,
        media_root: Path,
        supabase_url: str,
        secret_key: str,
        bucket: str = "cae-media",
    ) -> None:
        self.connection = connection
        self.media_root = media_root.resolve()
        self.supabase_url = supabase_url.rstrip("/")
        self.secret_key = secret_key
        self.bucket = bucket

    def bridge_source_package(
        self,
        *,
        legacy_source: Mapping[str, Any],
        bridge_actor_id: str,
        idempotency_key: str,
    ) -> tuple[OperationReceipt, str]:
        """Verify and copy exactly one existing Interview Expression source."""
        source = self._validate_legacy_source(legacy_source)
        payload = source["payload"]
        media = payload["media_assets"][0]
        local_path = self._resolve_local_media(
            logical_uri=str(media["logical_uri"]),
            workspace_id=str(payload["workspace_id"]),
            project_id=str(payload["project_id"]),
        )
        source_bytes = local_path.read_bytes()
        content_sha256 = hashlib.sha256(source_bytes).hexdigest()
        if content_sha256 != media["sha256"] or len(source_bytes) != media["bytes"]:
            raise InterviewSourceBridgeError("legacy media bytes do not match the admitted Interview Expression asset")
        upstream_ref = {
            "object_id": str(source["object_id"]),
            "revision": str(source["revision"]),
            "sha256": str(source["sha256"]),
        }
        bridge_identity = canonical_sha256({"upstream_source_ref": upstream_ref, "content_sha256": content_sha256})[:32]
        storage_object_key = f"cae/interview-expression/{bridge_identity}/{content_sha256}.bin"
        storage_created = self._put_or_verify_object(
            storage_object_key, source_bytes, content_sha256, str(media["media_type"])
        )
        source_package_id = f"cae:source:ie:{bridge_identity}"
        media_asset_id = f"cae:media:ie:{bridge_identity}"
        try:
            receipt = FirstSliceSemanticOperations(self.connection).register_verified_interview_source(
                workspace_id=str(payload["workspace_id"]),
                project_id=str(payload["project_id"]),
                bridge_actor_id=bridge_actor_id,
                source_package_id=source_package_id,
                upstream_source_ref=upstream_ref,
                media_asset_id=media_asset_id,
                storage_bucket=self.bucket,
                storage_object_key=storage_object_key,
                content_sha256=content_sha256,
                byte_size=len(source_bytes),
                media_type=str(media["media_type"]),
                idempotency_key=idempotency_key,
            )
        except Exception:
            if storage_created:
                try:
                    self.delete_object(storage_object_key)
                except HTTPError:
                    pass
            raise
        return receipt, storage_object_key

    def delete_object(self, storage_object_key: str) -> None:
        self._request(storage_object_key, method="DELETE")

    def _validate_legacy_source(self, legacy_source: Mapping[str, Any]) -> Mapping[str, Any]:
        required = {"object_id", "revision", "object_type", "sha256", "payload", "lifecycle_state"}
        if not required <= set(legacy_source):
            raise InterviewSourceBridgeError("legacy source record is incomplete")
        if legacy_source["object_type"] != "canonical_interview_source_package":
            raise InterviewSourceBridgeError("legacy record is not an Interview Expression source package")
        payload = legacy_source["payload"]
        if not isinstance(payload, Mapping) or canonical_sha256(dict(payload)) != legacy_source["sha256"]:
            raise InterviewSourceBridgeError("legacy source package hash does not match its canonical payload")
        if payload.get("package_id") != legacy_source["object_id"]:
            raise InterviewSourceBridgeError("legacy source package identity does not match its payload")
        if payload.get("source_kind") != "INTERVIEW_EXPRESSION":
            raise InterviewSourceBridgeError("legacy source kind is not INTERVIEW_EXPRESSION")
        if payload.get("lifecycle_state") not in {"ADMITTED", "COMPONENTS_IN_PROGRESS"}:
            raise InterviewSourceBridgeError("legacy source lifecycle is not bridge-eligible")
        for field in ("workspace_id", "project_id"):
            if not isinstance(payload.get(field), str) or not payload[field].strip():
                raise InterviewSourceBridgeError(f"legacy source {field} is missing")
        authority = payload.get("source_authority")
        if not isinstance(authority, Mapping) or set(authority) != {"operator_id", "authority_scope", "assertion_id"}:
            raise InterviewSourceBridgeError("legacy source authority declaration is incomplete")
        assets = payload.get("media_assets")
        if not isinstance(assets, list) or len(assets) != 1 or not isinstance(assets[0], Mapping):
            raise InterviewSourceBridgeError("WP-09 supports exactly one legacy media asset")
        media = assets[0]
        required_media = {"asset_id", "logical_uri", "sha256", "bytes", "media_type", "technical"}
        if not required_media <= set(media):
            raise InterviewSourceBridgeError("legacy media asset is incomplete")
        if not isinstance(media["sha256"], str) or len(media["sha256"]) != 64:
            raise InterviewSourceBridgeError("legacy media asset hash is invalid")
        if isinstance(media["bytes"], bool) or not isinstance(media["bytes"], int) or media["bytes"] < 1:
            raise InterviewSourceBridgeError("legacy media asset byte count is invalid")
        return legacy_source

    def _resolve_local_media(self, *, logical_uri: str, workspace_id: str, project_id: str) -> Path:
        parsed = urlsplit(logical_uri)
        if parsed.scheme != "workspace" or parsed.query or parsed.fragment:
            raise InterviewSourceBridgeError("legacy media locator is not a clean workspace URI")
        if parsed.netloc != workspace_id:
            raise InterviewSourceBridgeError("legacy media workspace locator does not match source package")
        segments = [segment for segment in parsed.path.split("/") if segment]
        if len(segments) != 2 or segments[0] != project_id or any(segment in {".", ".."} for segment in segments):
            raise InterviewSourceBridgeError("legacy media locator does not match the admitted local-media layout")
        candidate = (self.media_root / "interviews" / workspace_id / project_id / segments[1]).resolve()
        root = (self.media_root / "interviews" / workspace_id / project_id).resolve()
        if root not in candidate.parents or not candidate.is_file():
            raise InterviewSourceBridgeError("legacy media file is unavailable at its admitted locator")
        return candidate

    def _put_or_verify_object(self, storage_object_key: str, source_bytes: bytes, expected_sha256: str, media_type: str) -> bool:
        try:
            self._request(storage_object_key, method="POST", body=source_bytes, content_type=media_type)
            return True
        except HTTPError as error:
            # Supabase Storage has returned both 400 and 409 for an existing
            # path with x-upsert=false. Neither is accepted on status alone:
            # read the existing bytes and compare their SHA-256 first.
            if error.code not in {400, 409}:
                raise
            existing = self._request(storage_object_key, method="GET")
            if hashlib.sha256(existing).hexdigest() != expected_sha256:
                raise InterviewSourceBridgeError("existing storage object conflicts with verified source bytes") from error
            return False

    def _request(self, storage_object_key: str, *, method: str, body: bytes | None = None, content_type: str | None = None) -> bytes:
        headers = {"apikey": self.secret_key, "Authorization": f"Bearer {self.secret_key}"}
        if content_type:
            headers["Content-Type"] = content_type
        if method == "POST":
            headers["x-upsert"] = "false"
        url = f"{self.supabase_url}/storage/v1/object/{self.bucket}/{quote(storage_object_key, safe='/')}"
        with urlopen(Request(url, method=method, headers=headers, data=body), timeout=20) as response:
            return response.read()
