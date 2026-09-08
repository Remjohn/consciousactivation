"""Canonical three-layer Audience Context boundary for CA-M001 / Q01.

The adapter intentionally keeps the three audience layers separate:
- Market Macro Signals
- Segment Cultural Archetypes
- Live Audience Tensions

Each layer is immutable in memory, independently digest-addressable, and persisted
through the PipelineRepository's revisioned object store.  An AudienceContext
contains references to the three layers; it never embeds a blended audience blob.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Mapping, Protocol, Sequence

from ca_contracts import canonical_json_text, canonical_sha256

from ..domain.errors import PipelineConflict, PipelineNotFound, PipelineValidationError
from ..domain.validation import (
    reject_noncanonical,
    require_int,
    require_semver,
    require_sha,
    require_string,
)


class AudienceContextAdapterError(PipelineValidationError):
    """Base error for the CA-M001 audience-context boundary."""


class AudienceContextMutationError(AudienceContextAdapterError):
    """Raised when immutable audience state is altered or a revision is reused."""


class AudienceContextAdmissionError(AudienceContextAdapterError):
    """Raised when audience context is incomplete, blended, or inconsistent."""


class AudienceContextRepository(Protocol):
    """Minimal repository contract required by the canonical read/write boundary."""

    def store_object(
        self,
        object_type: str,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        object_id: str,
        semantic_version: str = "1.0.0",
        lifecycle_state: str = "ACTIVE",
        authority_state: str = "candidate_not_current",
        expected_revision: int | None = None,
        now: str | None = None,
    ) -> dict[str, Any]:
        ...

    def get_object(self, object_id: str, *, revision: int | None = None) -> dict[str, Any]:
        ...


@dataclass(frozen=True, slots=True)
class AudienceLayer:
    """Frozen, independently versioned audience layer.

    ``payload_json`` is the immutable canonical representation.  ``to_dict()``
    returns a freshly parsed payload, so callers can inspect it without gaining
    a mutable reference to the internal state.
    """

    KIND: ClassVar[str] = "AUDIENCE_LAYER"

    workspace_id: str
    audience_id: str
    version: int
    semantic_version: str
    provenance_refs: tuple[str, ...]
    payload_json: str
    payload_sha256: str
    layer_id: str
    layer_sha256: str

    @classmethod
    def create(
        cls,
        *,
        workspace_id: str,
        audience_id: str,
        payload: Mapping[str, Any],
        version: int = 1,
        semantic_version: str = "1.0.0",
        provenance_refs: Sequence[str] = (),
    ) -> "AudienceLayer":
        workspace = require_string(workspace_id, "workspace_id")
        audience = require_string(audience_id, "audience_id")
        revision = require_int(version, "version", minimum=1)
        semver = require_semver(semantic_version, "semantic_version")
        refs = cls._normalize_provenance(provenance_refs)
        payload_map = cls._require_payload(payload)
        payload_json = canonical_json_text(payload_map)
        payload_sha = canonical_sha256(payload_map)
        identity_core = {
            "workspace_id": workspace,
            "audience_id": audience,
            "layer_type": cls.KIND,
        }
        layer_id = f"audience-layer:{canonical_sha256(identity_core)}"
        layer_core = {
            **identity_core,
            "version": revision,
            "semantic_version": semver,
            "provenance_refs": list(refs),
            "payload_sha256": payload_sha,
        }
        layer_sha = canonical_sha256({**layer_core, "payload_json": payload_json})
        return cls(
            workspace_id=workspace,
            audience_id=audience,
            version=revision,
            semantic_version=semver,
            provenance_refs=refs,
            payload_json=payload_json,
            payload_sha256=payload_sha,
            layer_id=layer_id,
            layer_sha256=layer_sha,
        )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "AudienceLayer":
        if not isinstance(payload, Mapping):
            raise AudienceContextAdmissionError("audience layer must be an object")
        expected = {
            "layer_type",
            "workspace_id",
            "audience_id",
            "version",
            "semantic_version",
            "provenance_refs",
            "payload",
            "payload_sha256",
            "layer_id",
            "layer_sha256",
        }
        if set(payload) != expected:
            raise AudienceContextAdmissionError(
                f"{cls.KIND} has invalid shape; expected exactly {sorted(expected)}"
            )
        layer_type = require_string(payload["layer_type"], "layer_type")
        if layer_type != cls.KIND:
            raise AudienceContextAdmissionError(
                f"expected layer_type {cls.KIND}, got {layer_type}"
            )
        obj = cls.create(
            workspace_id=require_string(payload["workspace_id"], "workspace_id"),
            audience_id=require_string(payload["audience_id"], "audience_id"),
            payload=cls._require_payload(payload["payload"]),
            version=require_int(payload["version"], "version", minimum=1),
            semantic_version=require_semver(payload["semantic_version"], "semantic_version"),
            provenance_refs=payload["provenance_refs"],
        )
        supplied_sha = require_sha(payload["payload_sha256"], "payload_sha256")
        supplied_id = require_string(payload["layer_id"], "layer_id")
        supplied_layer_sha = require_sha(payload["layer_sha256"], "layer_sha256")
        if obj.payload_sha256 != supplied_sha:
            raise AudienceContextMutationError(
                f"{cls.KIND} payload digest mismatch: expected {obj.payload_sha256}, got {supplied_sha}"
            )
        if obj.layer_id != supplied_id:
            raise AudienceContextMutationError(
                f"{cls.KIND} identity mismatch: expected {obj.layer_id}, got {supplied_id}"
            )
        if obj.layer_sha256 != supplied_layer_sha:
            raise AudienceContextMutationError(
                f"{cls.KIND} layer digest mismatch: expected {obj.layer_sha256}, got {supplied_layer_sha}"
            )
        return obj

    def revise(
        self,
        *,
        payload: Mapping[str, Any],
        provenance_refs: Sequence[str] | None = None,
        semantic_version: str | None = None,
    ) -> "AudienceLayer":
        """Return a new immutable revision; never mutates this revision in place."""
        return type(self).create(
            workspace_id=self.workspace_id,
            audience_id=self.audience_id,
            payload=payload,
            version=self.version + 1,
            semantic_version=semantic_version or self.semantic_version,
            provenance_refs=provenance_refs if provenance_refs is not None else self.provenance_refs,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer_type": self.KIND,
            "workspace_id": self.workspace_id,
            "audience_id": self.audience_id,
            "version": self.version,
            "semantic_version": self.semantic_version,
            "provenance_refs": list(self.provenance_refs),
            "payload": json_loads(self.payload_json),
            "payload_sha256": self.payload_sha256,
            "layer_id": self.layer_id,
            "layer_sha256": self.layer_sha256,
        }

    def reference(self) -> dict[str, Any]:
        return {
            "object_id": self.layer_id,
            "revision": self.version,
            "version": self.version,
            "semantic_version": self.semantic_version,
            "sha256": self.layer_sha256,
        }

    @staticmethod
    def _require_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, Mapping):
            raise AudienceContextAdmissionError("audience layer payload must be an object")
        normalized = dict(payload)
        reject_noncanonical(normalized)
        return normalized

    @staticmethod
    def _normalize_provenance(provenance_refs: Sequence[str]) -> tuple[str, ...]:
        if not isinstance(provenance_refs, Sequence) or isinstance(
            provenance_refs, (str, bytes, bytearray)
        ):
            raise AudienceContextAdmissionError("provenance_refs must be a sequence")
        refs = tuple(sorted({require_string(item, "provenance_refs[]") for item in provenance_refs}))
        if len(refs) != len(provenance_refs):
            raise AudienceContextAdmissionError("provenance_refs must not contain duplicates")
        return refs


@dataclass(frozen=True, slots=True)
class MarketMacroSignals(AudienceLayer):
    """Market Macro Signals layer."""

    KIND: ClassVar[str] = "MARKET_MACRO_SIGNALS"


@dataclass(frozen=True, slots=True)
class SegmentCulturalArchetypes(AudienceLayer):
    """Segment Cultural Archetypes layer."""

    KIND: ClassVar[str] = "SEGMENT_CULTURAL_ARCHETYPES"


@dataclass(frozen=True, slots=True)
class LiveAudienceTensions(AudienceLayer):
    """Live Audience Tensions layer."""

    KIND: ClassVar[str] = "LIVE_AUDIENCE_TENSIONS"


@dataclass(frozen=True, slots=True)
class AudienceContext:
    """Canonical parent reference containing exactly three segregated layers."""

    workspace_id: str
    audience_id: str
    version: int
    market_macro_signals: MarketMacroSignals
    segment_cultural_archetypes: SegmentCulturalArchetypes
    live_audience_tensions: LiveAudienceTensions
    context_id: str
    context_sha256: str

    @classmethod
    def create(
        cls,
        *,
        workspace_id: str,
        audience_id: str,
        market_macro_signals: MarketMacroSignals,
        segment_cultural_archetypes: SegmentCulturalArchetypes,
        live_audience_tensions: LiveAudienceTensions,
        version: int = 1,
    ) -> "AudienceContext":
        workspace = require_string(workspace_id, "workspace_id")
        audience = require_string(audience_id, "audience_id")
        revision = require_int(version, "version", minimum=1)

        layers: tuple[AudienceLayer, ...] = (
            market_macro_signals,
            segment_cultural_archetypes,
            live_audience_tensions,
        )
        expected_types = (
            MarketMacroSignals,
            SegmentCulturalArchetypes,
            LiveAudienceTensions,
        )
        expected_kinds = {
            MarketMacroSignals.KIND,
            SegmentCulturalArchetypes.KIND,
            LiveAudienceTensions.KIND,
        }
        if any(not isinstance(layer, expected_type) for layer, expected_type in zip(layers, expected_types)):
            raise AudienceContextAdmissionError(
                "AudienceContext requires the three explicit layer types in canonical order"
            )
        if len({layer.layer_id for layer in layers}) != 3:
            raise AudienceContextAdmissionError("AudienceContext layer identities must be unique")
        if {layer.KIND for layer in layers} != expected_kinds:
            raise AudienceContextAdmissionError(
                "AudienceContext must contain exactly the canonical three layer kinds"
            )
        for index, layer in enumerate(layers):
            if layer.workspace_id != workspace:
                raise AudienceContextAdmissionError(
                    f"layer {index} workspace_id does not match AudienceContext"
                )
            if layer.audience_id != audience:
                raise AudienceContextAdmissionError(
                    f"layer {index} audience_id does not match AudienceContext"
                )

        context_identity = {
            "workspace_id": workspace,
            "audience_id": audience,
        }
        context_id = f"audience-context:{canonical_sha256(context_identity)}"
        layer_refs = {
            "market_macro_signals": market_macro_signals.reference(),
            "segment_cultural_archetypes": segment_cultural_archetypes.reference(),
            "live_audience_tensions": live_audience_tensions.reference(),
        }
        context_core = {
            "context_id": context_id,
            "workspace_id": workspace,
            "audience_id": audience,
            "version": revision,
            "layers": layer_refs,
        }
        context_sha = canonical_sha256(context_core)
        return cls(
            workspace_id=workspace,
            audience_id=audience,
            version=revision,
            market_macro_signals=market_macro_signals,
            segment_cultural_archetypes=segment_cultural_archetypes,
            live_audience_tensions=live_audience_tensions,
            context_id=context_id,
            context_sha256=context_sha,
        )

    def revise(
        self,
        *,
        market_macro_signals: MarketMacroSignals | None = None,
        segment_cultural_archetypes: SegmentCulturalArchetypes | None = None,
        live_audience_tensions: LiveAudienceTensions | None = None,
    ) -> "AudienceContext":
        """Return a new context revision; this revision remains unchanged."""
        return type(self).create(
            workspace_id=self.workspace_id,
            audience_id=self.audience_id,
            market_macro_signals=market_macro_signals or self.market_macro_signals,
            segment_cultural_archetypes=segment_cultural_archetypes or self.segment_cultural_archetypes,
            live_audience_tensions=live_audience_tensions or self.live_audience_tensions,
            version=self.version + 1,
        )

    def layer_refs(self) -> dict[str, dict[str, Any]]:
        return {
            "market_macro_signals": self.market_macro_signals.reference(),
            "segment_cultural_archetypes": self.segment_cultural_archetypes.reference(),
            "live_audience_tensions": self.live_audience_tensions.reference(),
        }

    def to_dict(self) -> dict[str, Any]:
        """Return reference-only canonical context representation.

        Layer payloads are deliberately absent.  The context object is never a
        blended audience blob; exact layer content is loaded by its pinned refs.
        """
        return {
            "context_id": self.context_id,
            "workspace_id": self.workspace_id,
            "audience_id": self.audience_id,
            "version": self.version,
            "layers": self.layer_refs(),
            "context_sha256": self.context_sha256,
        }

    def operator_projection(self) -> dict[str, Any]:
        """Operator-readable projection of the authoritative three-layer boundary."""
        return {
            "context_id": self.context_id,
            "workspace_id": self.workspace_id,
            "audience_id": self.audience_id,
            "context_version": self.version,
            "context_sha256": self.context_sha256,
            "layers": {
                "market_macro_signals": _operator_layer(self.market_macro_signals),
                "segment_cultural_archetypes": _operator_layer(self.segment_cultural_archetypes),
                "live_audience_tensions": _operator_layer(self.live_audience_tensions),
            },
        }

    @classmethod
    def from_reference_payload(
        cls,
        payload: Mapping[str, Any],
        *,
        market_macro_signals: MarketMacroSignals,
        segment_cultural_archetypes: SegmentCulturalArchetypes,
        live_audience_tensions: LiveAudienceTensions,
    ) -> "AudienceContext":
        if not isinstance(payload, Mapping):
            raise AudienceContextAdmissionError("audience context must be an object")
        expected = {
            "context_id",
            "workspace_id",
            "audience_id",
            "version",
            "layers",
            "context_sha256",
        }
        if set(payload) != expected:
            raise AudienceContextAdmissionError(
                f"AudienceContext contains unknown/missing fields; expected exactly {sorted(expected)}"
            )
        layers = payload["layers"]
        if not isinstance(layers, Mapping):
            raise AudienceContextAdmissionError("AudienceContext.layers must be an object")
        expected_layer_keys = {
            "market_macro_signals",
            "segment_cultural_archetypes",
            "live_audience_tensions",
        }
        if set(layers) != expected_layer_keys:
            raise AudienceContextAdmissionError(
                "AudienceContext must name exactly the three governed layers"
            )
        cls._reject_blended_reference(layers)

        context = cls.create(
            workspace_id=payload["workspace_id"],
            audience_id=payload["audience_id"],
            market_macro_signals=market_macro_signals,
            segment_cultural_archetypes=segment_cultural_archetypes,
            live_audience_tensions=live_audience_tensions,
            version=payload["version"],
        )
        supplied_context_id = require_string(payload["context_id"], "context_id")
        supplied_context_sha = require_sha(payload["context_sha256"], "context_sha256")
        expected_refs = context.layer_refs()
        if dict(layers) != expected_refs:
            raise AudienceContextAdmissionError(
                "AudienceContext layer references do not match the pinned layer identities/revisions/digests"
            )
        if context.context_id != supplied_context_id:
            raise AudienceContextMutationError(
                f"AudienceContext identity mismatch: expected {context.context_id}, got {supplied_context_id}"
            )
        if context.context_sha256 != supplied_context_sha:
            raise AudienceContextMutationError(
                f"AudienceContext digest mismatch: expected {context.context_sha256}, got {supplied_context_sha}"
            )
        return context

    @staticmethod
    def _reject_blended_reference(layers: Mapping[str, Any]) -> None:
        required_ref_keys = {
            "object_id",
            "revision",
            "version",
            "semantic_version",
            "sha256",
        }
        for name, value in layers.items():
            if not isinstance(value, Mapping) or set(value) != required_ref_keys:
                raise AudienceContextAdmissionError(
                    f"{name} must be an immutable reference, not embedded audience content"
                )
            if "payload" in value or "content" in value or "data" in value:
                raise AudienceContextAdmissionError(
                    f"{name} contains embedded content; blended audience payloads are prohibited"
                )


class AudienceContextAdapter:
    """Canonical construction, persistence and read path for CA-M001."""

    LAYER_OBJECT_TYPE = "audience_context_layer"
    CONTEXT_OBJECT_TYPE = "audience_context"

    @classmethod
    def persist(
        cls,
        context: AudienceContext,
        repository: AudienceContextRepository,
        *,
        idempotency_key: str,
        now: str | None = None,
    ) -> dict[str, Any]:
        """Persist each layer independently, then persist the reference-only context."""
        require_string(idempotency_key, "idempotency_key")
        layer_results: dict[str, Any] = {}
        for name, layer in (
            ("market_macro_signals", context.market_macro_signals),
            ("segment_cultural_archetypes", context.segment_cultural_archetypes),
            ("live_audience_tensions", context.live_audience_tensions),
        ):
            cls._guard_revision_alignment(repository, layer.layer_id, layer.version)
            try:
                result = repository.store_object(
                    cls.LAYER_OBJECT_TYPE,
                    layer.to_dict(),
                    idempotency_key=f"{idempotency_key}:{name}:v{layer.version}",
                    object_id=layer.layer_id,
                    semantic_version=layer.semantic_version,
                    expected_revision=layer.version - 1,
                    now=now,
                )
            except PipelineConflict as exc:
                raise AudienceContextMutationError(
                    f"immutable revision persistence rejected for {name}: {exc}"
                ) from exc
            stored = result["object"]
            if stored["revision"] != layer.version or stored["canonical_sha256"] != canonical_sha256(layer.to_dict()):
                raise AudienceContextMutationError(
                    f"persisted {name} revision/digest does not match its immutable layer identity"
                )
            layer_results[name] = result

        cls._guard_revision_alignment(repository, context.context_id, context.version)
        context_payload = context.to_dict()
        try:
            context_result = repository.store_object(
                cls.CONTEXT_OBJECT_TYPE,
                context_payload,
                idempotency_key=f"{idempotency_key}:context:v{context.version}",
                object_id=context.context_id,
                semantic_version=f"1.0.{context.version - 1}",
                expected_revision=context.version - 1,
                now=now,
            )
        except PipelineConflict as exc:
            raise AudienceContextMutationError(
                f"immutable context revision persistence rejected: {exc}"
            ) from exc
        stored_context = context_result["object"]
        if (
            stored_context["revision"] != context.version
            or stored_context["canonical_sha256"] != canonical_sha256(context_payload)
        ):
            raise AudienceContextMutationError(
                "persisted AudienceContext revision/digest does not match its immutable reference set"
            )
        return {
            "context": context_result,
            "layers": layer_results,
        }

    @classmethod
    def read(
        cls,
        repository: AudienceContextRepository,
        *,
        workspace_id: str,
        audience_id: str,
        version: int | None = None,
    ) -> AudienceContext:
        """Read authoritative context and exact pinned layer revisions from storage."""
        workspace = require_string(workspace_id, "workspace_id")
        audience = require_string(audience_id, "audience_id")
        context_id = cls._context_id(workspace, audience)
        stored_context = repository.get_object(context_id, revision=version) if version is not None else repository.get_object(context_id)
        context_payload = stored_context["payload"]
        if stored_context["object_type"] != cls.CONTEXT_OBJECT_TYPE:
            raise AudienceContextAdmissionError("stored object is not an AudienceContext")
        context = cls._read_context_from_persisted_payload(repository, context_payload)
        if context.version != stored_context["revision"]:
            raise AudienceContextMutationError(
                "stored AudienceContext version does not match persistence revision"
            )
        if stored_context["canonical_sha256"] != canonical_sha256(context_payload):
            raise AudienceContextMutationError(
                "stored AudienceContext canonical digest is inconsistent with its payload"
            )
        return context

    @classmethod
    def _read_context_from_persisted_payload(
        cls,
        repository: AudienceContextRepository,
        payload: Mapping[str, Any],
    ) -> AudienceContext:
        cls._reject_noncanonical_context_payload(payload)
        layers = payload["layers"]

        market = cls._read_layer(repository, layers["market_macro_signals"], MarketMacroSignals)
        archetypes = cls._read_layer(
            repository,
            layers["segment_cultural_archetypes"],
            SegmentCulturalArchetypes,
        )
        tensions = cls._read_layer(repository, layers["live_audience_tensions"], LiveAudienceTensions)
        return AudienceContext.from_reference_payload(
            payload,
            market_macro_signals=market,
            segment_cultural_archetypes=archetypes,
            live_audience_tensions=tensions,
        )

    @classmethod
    def _read_layer(
        cls,
        repository: AudienceContextRepository,
        reference: Mapping[str, Any],
        layer_type: type[AudienceLayer],
    ) -> AudienceLayer:
        if not isinstance(reference, Mapping):
            raise AudienceContextAdmissionError("layer reference must be an object")
        required = {"object_id", "revision", "version", "semantic_version", "sha256"}
        if set(reference) != required:
            raise AudienceContextAdmissionError("layer reference has invalid shape")
        object_id = require_string(reference["object_id"], "layer_ref.object_id")
        revision = require_int(reference["revision"], "layer_ref.revision", minimum=1)
        version = require_int(reference["version"], "layer_ref.version", minimum=1)
        semver = require_semver(reference["semantic_version"], "layer_ref.semantic_version")
        sha = require_sha(reference["sha256"], "layer_ref.sha256")
        if revision != version:
            raise AudienceContextAdmissionError("layer reference revision and version must match")
        stored = repository.get_object(object_id, revision=revision)
        if stored["object_type"] != cls.LAYER_OBJECT_TYPE:
            raise AudienceContextAdmissionError("referenced object is not an audience layer")
        layer = layer_type.from_dict(stored["payload"])
        if layer.layer_id != object_id:
            raise AudienceContextMutationError(
                f"layer identity mismatch for {object_id}"
            )
        if layer.version != revision or layer.semantic_version != semver:
            raise AudienceContextMutationError(
                f"layer revision/version mismatch for {object_id}"
            )
        if layer.layer_sha256 != sha:
            raise AudienceContextMutationError(
                f"layer digest mismatch for {object_id}"
            )
        if stored["canonical_sha256"] != canonical_sha256(stored["payload"]):
            raise AudienceContextMutationError(
                f"persistence digest mismatch for {object_id}"
            )
        return layer

    @staticmethod
    def _guard_revision_alignment(
        repository: AudienceContextRepository,
        object_id: str,
        version: int,
    ) -> None:
        try:
            current = repository.get_object(object_id)
        except PipelineNotFound:
            if version != 1:
                raise AudienceContextMutationError(
                    f"cannot first-persist {object_id} at version {version}; first revision must be 1"
                )
            return
        current_revision = int(current["revision"])
        if version not in {current_revision, current_revision + 1}:
            raise AudienceContextMutationError(
                f"immutable revision contract violated for {object_id}: stored={current_revision}, requested={version}"
            )
        if version == current_revision:
            # store_object may safely replay exactly identical content; a changed payload
            # must not reuse an existing revision.
            return

    @staticmethod
    def _context_id(workspace_id: str, audience_id: str) -> str:
        return f"audience-context:{canonical_sha256({'workspace_id': workspace_id, 'audience_id': audience_id})}"

    @staticmethod
    def _reject_noncanonical_context_payload(payload: Mapping[str, Any]) -> None:
        if not isinstance(payload, Mapping):
            raise AudienceContextAdmissionError("AudienceContext payload must be an object")
        expected = {
            "context_id",
            "workspace_id",
            "audience_id",
            "version",
            "layers",
            "context_sha256",
        }
        if set(payload) != expected:
            raise AudienceContextAdmissionError(
                f"AudienceContext contains unknown/missing fields; expected exactly {sorted(expected)}"
            )
        reject_noncanonical(dict(payload))


def _operator_layer(layer: AudienceLayer) -> dict[str, Any]:
    return {
        "layer_type": layer.KIND,
        "object_id": layer.layer_id,
        "revision": layer.version,
        "semantic_version": layer.semantic_version,
        "sha256": layer.layer_sha256,
        "payload_sha256": layer.payload_sha256,
        "provenance_refs": list(layer.provenance_refs),
    }


def json_loads(value: str) -> dict[str, Any]:
    import json

    loaded = json.loads(value)
    if not isinstance(loaded, dict):
        raise AudienceContextAdmissionError("canonical layer payload must decode to an object")
    return loaded
