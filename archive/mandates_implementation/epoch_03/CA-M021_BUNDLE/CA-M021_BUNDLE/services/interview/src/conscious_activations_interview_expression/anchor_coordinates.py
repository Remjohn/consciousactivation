"""
CA-M021 — Anchor Hits as Exact Coordinate References
Requirement: FR-ANCH-001

Anchor Hits must carry exact spatio-temporal coordinates derived from the
sovereign media container.  An Anchor Hit that holds only an approximate
millisecond range (as produced by the pre-mandate `require_source_span`
path) is *not* an exact coordinate reference and must be rejected at the
domain boundary.

Exact coordinate fields required by this mandate:
  - byte_offset_start (int, ≥ 0)   — byte offset of the first byte of the
                                       anchor window in the raw media bitstream
  - byte_offset_end   (int, ≥ 1)   — exclusive byte offset of the last byte
  - frame_number_start (int, ≥ 0)  — first frame number (0-based, derived from
                                       media container frame index)
  - frame_number_end   (int, ≥ 0)  — last frame number (inclusive)
  - microsecond_start (int, ≥ 0)   — presentation timestamp in microseconds
  - microsecond_end   (int, ≥ 1)   — exclusive PTS in microseconds

Additionally each coordinate span must be bound to its sovereign media
asset so the coordinates are not relocatable:
  - media_asset_id  (str)   — the `asset_id` of the sovereign media asset
  - media_sha256    (str)   — SHA-256 of that asset at time of indexing

The span must not exceed the declared raw source duration, which is stored
in the media asset's technical.duration_us field (or derived from
duration_ms when the finer-grained value is absent).

Interpretive summaries, free-text "anchor" strings, or objects that carry
only a start/end millisecond pair are explicitly rejected — they are NOT
Anchor Coordinate spans under FR-ANCH-001.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .canonical import (
    exact_keys,
    require_int,
    require_ref,
    require_sha,
    require_source_span,
    require_string,
    semantic_id,
)
from .errors import ValidationError
from .repository import InterviewRepository

# ---------------------------------------------------------------------------
# Mandate version sentinel — lets future auditors see which mandate minted
# the coordinate record.
# ---------------------------------------------------------------------------
ANCHOR_COORDINATE_MANDATE = "CA-M021"
ANCHOR_COORDINATE_SCHEMA_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# The full set of required coordinate fields per FR-ANCH-001.
# ---------------------------------------------------------------------------
_EXACT_COORD_FIELDS: frozenset[str] = frozenset(
    {
        "media_asset_id",
        "media_sha256",
        "byte_offset_start",
        "byte_offset_end",
        "frame_number_start",
        "frame_number_end",
        "microsecond_start",
        "microsecond_end",
    }
)

# Anchor kinds are open-ended but must be non-empty strings.
# The mandate does not restrict the vocabulary; enforcement is structural.
_MIN_ANCHOR_KIND_LEN = 1


# ---------------------------------------------------------------------------
# Low-level coordinate validator
# ---------------------------------------------------------------------------

def require_exact_anchor_coordinates(
    value: Any,
    name: str = "anchor_coordinates",
) -> dict[str, Any]:
    """
    Validate and normalise a raw coordinate mapping.

    Raises ValidationError for any of:
      - missing or extra fields
      - non-integer coordinate values
      - inverted or zero-length spans
      - byte or frame spans that are inverted
    Does NOT validate against a specific media asset's duration — that
    check requires the media asset record and is performed by
    `validate_coordinates_within_source`.
    """
    if not isinstance(value, Mapping):
        raise ValidationError(
            f"{name} must be a mapping",
            context={"classification": "FR_ANCH_001_TYPE_ERROR"},
        )

    exact_keys(value, _EXACT_COORD_FIELDS, name)

    media_asset_id = require_string(value["media_asset_id"], f"{name}.media_asset_id")
    media_sha256 = require_sha(value["media_sha256"], f"{name}.media_sha256")

    byte_start = require_int(
        value["byte_offset_start"], f"{name}.byte_offset_start", minimum=0
    )
    byte_end = require_int(
        value["byte_offset_end"], f"{name}.byte_offset_end", minimum=1
    )
    if byte_end <= byte_start:
        raise ValidationError(
            f"{name}.byte_offset_end must be greater than byte_offset_start",
            context={"classification": "FR_ANCH_001_INVERTED_BYTE_SPAN"},
        )

    frame_start = require_int(
        value["frame_number_start"], f"{name}.frame_number_start", minimum=0
    )
    frame_end = require_int(
        value["frame_number_end"], f"{name}.frame_number_end", minimum=0
    )
    if frame_end < frame_start:
        raise ValidationError(
            f"{name}.frame_number_end must be >= frame_number_start",
            context={"classification": "FR_ANCH_001_INVERTED_FRAME_SPAN"},
        )

    us_start = require_int(
        value["microsecond_start"], f"{name}.microsecond_start", minimum=0
    )
    us_end = require_int(
        value["microsecond_end"], f"{name}.microsecond_end", minimum=1
    )
    if us_end <= us_start:
        raise ValidationError(
            f"{name}.microsecond_end must be greater than microsecond_start",
            context={"classification": "FR_ANCH_001_INVERTED_MICROSECOND_SPAN"},
        )

    return {
        "media_asset_id": media_asset_id,
        "media_sha256": media_sha256,
        "byte_offset_start": byte_start,
        "byte_offset_end": byte_end,
        "frame_number_start": frame_start,
        "frame_number_end": frame_end,
        "microsecond_start": us_start,
        "microsecond_end": us_end,
    }


def validate_coordinates_within_source(
    coords: dict[str, Any],
    media_asset: Mapping[str, Any],
    name: str = "anchor_coordinates",
) -> None:
    """
    Verify that `coords` (already validated by `require_exact_anchor_coordinates`)
    does not exceed the declared duration of `media_asset`.

    The raw source duration is read from:
      technical.duration_us   (microseconds, preferred — highest precision)
      technical.duration_ms   (milliseconds, fallback — converted to µs)

    If neither field is present or is zero, the check is skipped and a
    limitation is recorded by the caller — the mandate says "reject any
    anchor whose boundary timestamps exceed raw source duration"; if the
    source duration is genuinely unknown we cannot enforce the bound, so
    we record the limitation rather than silently accept.

    Returns None on success; raises ValidationError if the span exceeds
    source duration.
    """
    asset_id = media_asset.get("asset_id", "")
    if coords["media_asset_id"] != asset_id:
        raise ValidationError(
            f"{name}.media_asset_id does not match the provided media asset",
            context={"classification": "FR_ANCH_001_MEDIA_MISMATCH"},
        )
    if coords["media_sha256"] != media_asset.get("sha256", ""):
        raise ValidationError(
            f"{name}.media_sha256 does not match the provided media asset digest",
            context={"classification": "FR_ANCH_001_MEDIA_DIGEST_MISMATCH"},
        )

    technical = media_asset.get("technical", {})
    duration_us: int | None = None

    raw_us = technical.get("duration_us")
    if isinstance(raw_us, int) and raw_us > 0:
        duration_us = raw_us
    else:
        raw_ms = technical.get("duration_ms")
        if isinstance(raw_ms, int) and raw_ms > 0:
            duration_us = raw_ms * 1000

    if duration_us is None:
        # Cannot enforce the bound — caller must record the limitation.
        return

    if coords["microsecond_end"] > duration_us:
        raise ValidationError(
            (
                f"{name}: anchor microsecond_end ({coords['microsecond_end']} µs) "
                f"exceeds raw source duration ({duration_us} µs)"
            ),
            context={"classification": "FR_ANCH_001_EXCEEDS_SOURCE_DURATION"},
        )


def reject_approximate_anchor(value: Any, name: str = "candidate") -> None:
    """
    Explicit fail-closed guard: raise ValidationError when `value` looks like
    an approximate time-range anchor rather than an exact coordinate span.

    This implements the mandate's negative path: "approximate time ranges,
    free-form 'anchor' strings, or interpretive summaries are rejected."

    Heuristic: an object is treated as an approximate anchor when it carries
    the millisecond-only source_span fields (`start_ms`, `end_ms`) but lacks
    ANY of the exact coordinate fields mandated by FR-ANCH-001.
    """
    if isinstance(value, Mapping):
        has_approx = "start_ms" in value or "end_ms" in value
        has_exact = any(field in value for field in _EXACT_COORD_FIELDS)
        if has_approx and not has_exact:
            raise ValidationError(
                (
                    f"{name} is an approximate millisecond span — "
                    "Anchor Hits require exact byte offsets, frame numbers, "
                    "and microsecond timestamps per FR-ANCH-001"
                ),
                context={"classification": "FR_ANCH_001_APPROXIMATE_ANCHOR_REJECTED"},
            )
        if isinstance(value, str):
            # A bare string is an interpretive label, not a coordinate.
            raise ValidationError(
                f"{name} is a free-text string — "
                "Anchor Hits must be exact coordinate structures per FR-ANCH-001",
                context={"classification": "FR_ANCH_001_INTERPRETIVE_ANCHOR_REJECTED"},
            )
    elif isinstance(value, str):
        raise ValidationError(
            f"{name} is a free-text string — "
            "Anchor Hits must be exact coordinate structures per FR-ANCH-001",
            context={"classification": "FR_ANCH_001_INTERPRETIVE_ANCHOR_REJECTED"},
        )


# ---------------------------------------------------------------------------
# AnchorCoordinateService — domain boundary service for CA-M021
# ---------------------------------------------------------------------------

class AnchorCoordinateService:
    """
    Service that admits and retrieves Anchor Coordinate records.

    An Anchor Coordinate record ties a verbatim quote, emotional cue, or
    reaction anchor to exact spatio-temporal coordinates in the master
    source media.  Approximate or interpretive forms are rejected at this
    boundary.

    This service is *not* a replacement for `ExpressionGovernanceService
    .create_anchor_hit`; it is the coordinate-precision layer mandated by
    CA-M021 that must be satisfied before an Anchor Hit can reference a
    coordinate span.
    """

    OBJECT_TYPE = "anchor_coordinate"

    def __init__(self, repository: InterviewRepository) -> None:
        self._repository = repository

    # ------------------------------------------------------------------
    # Admission
    # ------------------------------------------------------------------

    def admit(
        self,
        *,
        source_package_ref: Mapping[str, Any],
        anchor_kind: str,
        anchor_coordinates: Mapping[str, Any],
        evidence_refs: Sequence[Mapping[str, Any]],
        actor_id: str,
        limitations: Sequence[str] = (),
        idempotency_key: str,
    ) -> dict[str, Any]:
        """
        Admit an Anchor Coordinate record.

        Parameters
        ----------
        source_package_ref:
            Canonical ref to the source package that owns the sovereign media.
        anchor_kind:
            Non-empty string naming the anchor category (e.g.
            "VERBATIM_QUOTE", "EMOTIONAL_CUE", "REACTION_ANCHOR").
        anchor_coordinates:
            Exact coordinate mapping — must satisfy `_EXACT_COORD_FIELDS`.
            Approximate or interpretive forms are rejected fail-closed.
        evidence_refs:
            List of canonical refs to the evidence objects (verbatim,
            reaction observations, etc.) that produced this anchor.
        actor_id:
            Non-empty string identifying the producing actor.
        limitations:
            Optional list of non-empty limitation strings.
        idempotency_key:
            Idempotency key for the store operation.

        Returns
        -------
        dict with keys "object" and "receipt".
        """
        # 1 — Validate source package ref
        source_ref = require_ref(source_package_ref, "source_package_ref")

        # 2 — Resolve source package and extract the sovereign media asset
        try:
            package_obj = self._repository.get_object_by_sha(
                source_ref["object_id"], source_ref["sha256"]
            )
        except Exception as exc:
            raise ValidationError(
                "source_package_ref is stale or missing",
                context={"classification": "FR_ANCH_001_PROVENANCE_ERROR"},
            ) from exc

        package_payload = package_obj["payload"]
        media_assets: list[dict[str, Any]] = package_payload.get("media_assets", [])

        # 3 — Explicit rejection of approximate anchors before structural validation
        reject_approximate_anchor(anchor_coordinates, name="anchor_coordinates")

        # 4 — Structural validation of exact coordinate fields
        coords = require_exact_anchor_coordinates(anchor_coordinates, "anchor_coordinates")

        # 5 — Resolve the sovereign media asset referenced by the coordinates
        matched_asset = next(
            (
                asset
                for asset in media_assets
                if asset.get("asset_id") == coords["media_asset_id"]
                and asset.get("sha256") == coords["media_sha256"]
            ),
            None,
        )
        if matched_asset is None:
            raise ValidationError(
                "anchor_coordinates.media_asset_id / media_sha256 do not match "
                "any media asset in the admitted source package",
                context={"classification": "FR_ANCH_001_MEDIA_NOT_IN_PACKAGE"},
            )

        # 6 — Duration boundary check: reject if span exceeds source duration
        effective_limitations: list[str] = [
            require_string(lim, "limitations[]") for lim in limitations
        ]
        duration_unknown = False
        technical = matched_asset.get("technical", {})
        if not (
            (isinstance(technical.get("duration_us"), int) and technical["duration_us"] > 0)
            or (isinstance(technical.get("duration_ms"), int) and technical["duration_ms"] > 0)
        ):
            duration_unknown = True
            effective_limitations.append("SOURCE_DURATION_UNKNOWN_CANNOT_ENFORCE_BOUND")

        # Only call the bound-check when duration is known — it will raise on
        # overshoot; if unknown the limitation is already recorded above.
        if not duration_unknown:
            validate_coordinates_within_source(
                coords, matched_asset, "anchor_coordinates"
            )

        # 7 — Validate evidence refs
        evidence = [
            require_ref(r, f"evidence_refs[{i}]")
            for i, r in enumerate(evidence_refs)
        ]

        # 8 — Validate anchor_kind
        kind = require_string(anchor_kind, "anchor_kind")
        if len(kind) < _MIN_ANCHOR_KIND_LEN:
            raise ValidationError(
                "anchor_kind must be a non-empty string",
                context={"classification": "FR_ANCH_001_INVALID_KIND"},
            )

        # 9 — Build the identity core (deterministic for semantic_id)
        actor = require_string(actor_id, "actor_id")
        identity_core: dict[str, Any] = {
            "source_package_ref": dict(source_ref),
            "anchor_kind": kind,
            "anchor_coordinates": coords,
            "evidence_refs": sorted(
                [dict(r) for r in evidence], key=lambda x: x["object_id"]
            ),
            "actor_id": actor,
            "mandate_id": ANCHOR_COORDINATE_MANDATE,
            "schema_version": ANCHOR_COORDINATE_SCHEMA_VERSION,
        }
        object_id = semantic_id("ie:anchor-coordinate", identity_core)

        # 10 — Build full payload
        payload: dict[str, Any] = {
            "anchor_coordinate_id": object_id,
            "version": ANCHOR_COORDINATE_SCHEMA_VERSION,
            **identity_core,
            "limitations": effective_limitations,
            "validation": {
                "status": "PASS",
                "exact_coordinates": True,
                "approximate_anchor_rejected": True,
                "source_digest_bound": True,
                "duration_bound_checked": not duration_unknown,
                "mandate_id": ANCHOR_COORDINATE_MANDATE,
            },
            "lifecycle_state": "VALIDATED",
        }

        # 11 — Persist
        result = self._repository.store_object(
            self.OBJECT_TYPE,
            payload,
            object_id=object_id,
            idempotency_key=idempotency_key,
            lifecycle_state="VALIDATED",
        )

        # 12 — Record provenance edges
        self._repository.add_edge(
            source_ref["object_id"],
            object_id,
            "source_of_anchor_coordinate",
        )
        for ev_ref in evidence:
            self._repository.add_edge(
                ev_ref["object_id"],
                object_id,
                "evidence_supports_anchor_coordinate",
            )

        # 13 — Attach receipt
        result["receipt"] = {
            "command": "admit_anchor_coordinate",
            "mandate_id": ANCHOR_COORDINATE_MANDATE,
            "object_ref": {
                "object_id": result["object"]["object_id"],
                "version": result["object"]["version"],
                "sha256": result["object"]["sha256"],
            },
            "source_package_ref": dict(source_ref),
            "anchor_kind": kind,
            "anchor_coordinates": coords,
            "validation_status": "PASS",
            "exact_coordinates": True,
            "duration_bound_checked": not duration_unknown,
            "limitations": effective_limitations,
            "actor_id": actor,
        }
        return result

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def get(self, coordinate_ref: Mapping[str, Any]) -> dict[str, Any]:
        """Retrieve an Anchor Coordinate record by its canonical ref."""
        ref = require_ref(coordinate_ref, "anchor_coordinate_ref")
        return self._repository.get_object_by_sha(ref["object_id"], ref["sha256"])

    def list_for_source(self, source_package_id: str) -> list[dict[str, Any]]:
        """Return all Anchor Coordinate records for a given source package."""
        return [
            obj
            for obj in self._repository.list_objects(self.OBJECT_TYPE)
            if obj["payload"]["source_package_ref"]["object_id"] == source_package_id
        ]
