"""
frozen_portfolio.py
-------------------
CA-M008 — Frozen Campaign Content Portfolio Contract.

Invariant: FR-008 / FR-PORT-001

The FrozenPortfolioSnapshot is a versioned, content-addressed, immutable
contract that captures the authoritative deliverable quantities, target
aspect ratios, and format requirements for a campaign before physical
evidence acquisition begins.

Lifecycle
---------
    DRAFT  ->  SEALED  ->  (downstream execution)

Once sealed, no field of the portfolio contract may be changed in place.
Downstream mutation is explicitly prohibited.  If a new target set is
required after sealing, a new governed revision must be created before the
relevant execution boundary.

Admission Gate
--------------
The canonical admission predicate ``require_admitted_portfolio`` re-validates
the snapshot digest on every downstream call.  Any in-memory or storage
mutation that would alter the deliverable contract is detected and raises
``PortfolioMutationError`` before downstream execution proceeds.

This module intentionally does not persist or update upstream artifacts.  It
stores immutable references to the approved revision and its content-addressed
digest.  Downstream callers are expected to call ``require_admitted_portfolio``
before starting evidence acquisition.

Authority
---------
- Master 57-Question Canon: Q08
- Canonical invariant: FR-PORT-001
- Mandate: CA-M008
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional, Sequence

from ca_contracts import canonical_sha256, utc_now_rfc3339


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PORTFOLIO_SCHEMA_VERSION = "CA-M008.frozen-portfolio.v1"
INVARIANT_ID = "FR-008 / FR-PORT-001"


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class PortfolioError(RuntimeError):
    """Base error for CA-M008 Frozen Portfolio contract violations."""


class PortfolioMutationError(PortfolioError):
    """Raised when a caller attempts to mutate a sealed portfolio contract."""


class PortfolioAdmissionError(PortfolioError):
    """Raised when a portfolio is missing or not in the required state for evidence acquisition."""


class PortfolioDigestMismatchError(PortfolioError):
    """Raised when a portfolio's content digest does not match its declared revision digest."""


class InvalidDeliverableError(PortfolioError):
    """Raised when a deliverable entry fails structural or field validation."""


class DuplicatePortfolioRevisionError(PortfolioError):
    """Raised when a caller attempts to register a revision_id that already exists."""


class MissingPortfolioError(PortfolioAdmissionError):
    """Raised when no sealed portfolio is found for a workspace/campaign."""


# ---------------------------------------------------------------------------
# Supporting data structures
# ---------------------------------------------------------------------------


class PortfolioLifecycleState(str, enum.Enum):
    """Ordered lifecycle states for a portfolio contract.

    Only SEALED snapshots are admitted for evidence acquisition.
    """

    DRAFT = "DRAFT"
    SEALED = "SEALED"


@dataclass(frozen=True, slots=True)
class AspectRatioSpec:
    """Immutable representation of a required aspect ratio deliverable slot.

    ``ratio_label`` is human-readable (e.g. "16:9", "9:16", "1:1").
    ``width_px`` and ``height_px`` are the canonical pixel dimensions used
    for yield comparison; both must be positive integers.
    """

    ratio_label: str
    width_px: int
    height_px: int

    def __post_init__(self) -> None:
        if not isinstance(self.ratio_label, str) or not self.ratio_label.strip():
            raise InvalidDeliverableError("ratio_label must be a non-empty string")
        if not isinstance(self.width_px, int) or self.width_px <= 0:
            raise InvalidDeliverableError("width_px must be a positive integer")
        if not isinstance(self.height_px, int) or self.height_px <= 0:
            raise InvalidDeliverableError("height_px must be a positive integer")

    def to_dict(self) -> dict[str, Any]:
        return {
            "ratio_label": self.ratio_label,
            "width_px": self.width_px,
            "height_px": self.height_px,
        }


@dataclass(frozen=True, slots=True)
class FormatRequirement:
    """Immutable representation of a format requirement for a deliverable.

    ``format_id`` is a stable, project-scoped identifier (e.g.
    "short-form-video", "image-still", "carousel-card").
    ``codec_or_mime`` is optional technical detail used by downstream yield
    evaluation (e.g. "video/mp4", "image/jpeg").
    ``notes`` is a human-readable free-text annotation only; it does not
    affect the content digest.
    """

    format_id: str
    codec_or_mime: Optional[str] = None
    notes: Optional[str] = None

    def __post_init__(self) -> None:
        if not isinstance(self.format_id, str) or not self.format_id.strip():
            raise InvalidDeliverableError("format_id must be a non-empty string")

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"format_id": self.format_id}
        if self.codec_or_mime is not None:
            d["codec_or_mime"] = self.codec_or_mime
        if self.notes is not None:
            d["notes"] = self.notes
        return d


@dataclass(frozen=True, slots=True)
class DeliverableEntry:
    """Immutable specification of a single deliverable within the portfolio.

    A deliverable entry captures:
    - ``deliverable_id``   — stable unique identifier within the portfolio
    - ``label``            — human-readable name
    - ``quantity``         — how many of this deliverable the campaign targets
    - ``aspect_ratio``     — canonical pixel-dimension and label requirement
    - ``format_requirement`` — the required format contract
    """

    deliverable_id: str
    label: str
    quantity: int
    aspect_ratio: AspectRatioSpec
    format_requirement: FormatRequirement

    def __post_init__(self) -> None:
        if not isinstance(self.deliverable_id, str) or not self.deliverable_id.strip():
            raise InvalidDeliverableError("deliverable_id must be a non-empty string")
        if not isinstance(self.label, str) or not self.label.strip():
            raise InvalidDeliverableError("label must be a non-empty string")
        if not isinstance(self.quantity, int) or self.quantity <= 0:
            raise InvalidDeliverableError("quantity must be a positive integer")
        if not isinstance(self.aspect_ratio, AspectRatioSpec):
            raise InvalidDeliverableError("aspect_ratio must be an AspectRatioSpec")
        if not isinstance(self.format_requirement, FormatRequirement):
            raise InvalidDeliverableError("format_requirement must be a FormatRequirement")

    def to_dict(self) -> dict[str, Any]:
        return {
            "deliverable_id": self.deliverable_id,
            "label": self.label,
            "quantity": self.quantity,
            "aspect_ratio": self.aspect_ratio.to_dict(),
            "format_requirement": self.format_requirement.to_dict(),
        }


# ---------------------------------------------------------------------------
# Core frozen snapshot
# ---------------------------------------------------------------------------


def _portfolio_digest_payload(
    *,
    portfolio_id: str,
    revision_id: str,
    workspace_id: str,
    campaign_id: str,
    narrative_context: str,
    deliverables: Sequence[DeliverableEntry],
    created_at: str,
) -> dict[str, Any]:
    """Build the canonical digest payload for a portfolio snapshot.

    ``notes`` is intentionally excluded from the digest so that operator
    annotations cannot accidentally mutate the contract identity.
    """
    return {
        "schema": PORTFOLIO_SCHEMA_VERSION,
        "invariant_id": INVARIANT_ID,
        "portfolio_id": portfolio_id,
        "revision_id": revision_id,
        "workspace_id": workspace_id,
        "campaign_id": campaign_id,
        "narrative_context": narrative_context,
        "deliverables": [d.to_dict() for d in deliverables],
        "created_at": created_at,
    }


@dataclass(frozen=True, slots=True)
class FrozenPortfolioSnapshot:
    """Immutable, content-addressed campaign content portfolio contract.

    This is the authoritative production target for downstream yield
    evaluation.  It cannot be changed once sealed.  Downstream mutation
    or format reallocation is prohibited.

    Fields
    ------
    portfolio_id        Stable identifier for this portfolio series.
    revision_id         Unique revision identifier (monotonically increasing
                        within a portfolio series; a new revision MUST be
                        created rather than mutating an existing one).
    workspace_id        Workspace scope.
    campaign_id         The campaign this portfolio serves as the production
                        target for.
    narrative_context   Human-readable campaign/narrative context required to
                        interpret the contract (e.g. "Q4 launch campaign —
                        guest: Jane Doe — tension: autonomy vs. accountability").
    deliverables        Ordered, immutable list of DeliverableEntry objects
                        specifying deliverable identity, quantity, aspect
                        ratio, and format requirements.
    lifecycle_state     DRAFT or SEALED.  Only SEALED snapshots are admitted
                        for evidence acquisition.
    revision_digest     SHA-256 content address of the canonical digest
                        payload for this revision.  Must match the computed
                        digest on every downstream admission call.
    created_at          ISO-8601 UTC timestamp of snapshot creation.
    notes               Optional operator annotation; excluded from digest.
    """

    portfolio_id: str
    revision_id: str
    workspace_id: str
    campaign_id: str
    narrative_context: str
    deliverables: tuple[DeliverableEntry, ...]
    lifecycle_state: PortfolioLifecycleState
    revision_digest: str
    created_at: str
    notes: Optional[str] = None

    # ------------------------------------------------------------------
    # Construction helpers
    # ------------------------------------------------------------------

    @classmethod
    def create_draft(
        cls,
        *,
        portfolio_id: str,
        revision_id: str,
        workspace_id: str,
        campaign_id: str,
        narrative_context: str,
        deliverables: Sequence[DeliverableEntry],
        notes: Optional[str] = None,
        created_at: Optional[str] = None,
    ) -> "FrozenPortfolioSnapshot":
        """Construct a DRAFT portfolio snapshot with a computed content digest.

        The digest is computed immediately so that any mutation to the
        snapshot fields after construction would be detectable via
        ``verify_digest()``.
        """
        _require_non_empty(portfolio_id, "portfolio_id")
        _require_non_empty(revision_id, "revision_id")
        _require_non_empty(workspace_id, "workspace_id")
        _require_non_empty(campaign_id, "campaign_id")
        _require_non_empty(narrative_context, "narrative_context")
        if not deliverables:
            raise InvalidDeliverableError(
                "at least one deliverable is required to define a portfolio contract"
            )
        deliverable_ids = [d.deliverable_id for d in deliverables]
        if len(deliverable_ids) != len(set(deliverable_ids)):
            raise InvalidDeliverableError(
                "deliverable_ids must be unique within a portfolio"
            )

        ts = created_at or utc_now_rfc3339()
        deliverables_tuple = tuple(deliverables)
        digest = canonical_sha256(
            _portfolio_digest_payload(
                portfolio_id=portfolio_id,
                revision_id=revision_id,
                workspace_id=workspace_id,
                campaign_id=campaign_id,
                narrative_context=narrative_context,
                deliverables=deliverables_tuple,
                created_at=ts,
            )
        )
        return cls(
            portfolio_id=portfolio_id,
            revision_id=revision_id,
            workspace_id=workspace_id,
            campaign_id=campaign_id,
            narrative_context=narrative_context,
            deliverables=deliverables_tuple,
            lifecycle_state=PortfolioLifecycleState.DRAFT,
            revision_digest=digest,
            created_at=ts,
            notes=notes,
        )

    def seal(self) -> "FrozenPortfolioSnapshot":
        """Return a new SEALED snapshot from this DRAFT.

        Re-verifies the digest before sealing.  Raises
        ``PortfolioDigestMismatchError`` if the digest is already corrupt.
        Raises ``PortfolioMutationError`` if this snapshot is already sealed.
        """
        if self.lifecycle_state == PortfolioLifecycleState.SEALED:
            raise PortfolioMutationError(
                f"portfolio revision '{self.revision_id}' is already SEALED; "
                "create a new revision rather than re-sealing"
            )
        self.verify_digest()  # fail-closed pre-seal validation
        return _replace_state(self, PortfolioLifecycleState.SEALED)

    # ------------------------------------------------------------------
    # Integrity
    # ------------------------------------------------------------------

    def verify_digest(self) -> None:
        """Re-compute and validate the content digest.

        Raises ``PortfolioDigestMismatchError`` if the stored
        ``revision_digest`` does not match the re-computed digest over the
        canonical payload fields.
        """
        expected = canonical_sha256(
            _portfolio_digest_payload(
                portfolio_id=self.portfolio_id,
                revision_id=self.revision_id,
                workspace_id=self.workspace_id,
                campaign_id=self.campaign_id,
                narrative_context=self.narrative_context,
                deliverables=self.deliverables,
                created_at=self.created_at,
            )
        )
        if self.revision_digest != expected:
            raise PortfolioDigestMismatchError(
                f"portfolio revision '{self.revision_id}' digest mismatch: "
                f"stored={self.revision_digest!r} expected={expected!r}"
            )

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Return a fully serialisable canonical representation."""
        result: dict[str, Any] = {
            "schema": PORTFOLIO_SCHEMA_VERSION,
            "invariant_id": INVARIANT_ID,
            "portfolio_id": self.portfolio_id,
            "revision_id": self.revision_id,
            "workspace_id": self.workspace_id,
            "campaign_id": self.campaign_id,
            "narrative_context": self.narrative_context,
            "deliverables": [d.to_dict() for d in self.deliverables],
            "lifecycle_state": self.lifecycle_state.value,
            "revision_digest": self.revision_digest,
            "created_at": self.created_at,
        }
        if self.notes is not None:
            result["notes"] = self.notes
        return result


# ---------------------------------------------------------------------------
# Frozen internal replace helper (avoids importing dataclasses at module init)
# ---------------------------------------------------------------------------


def _replace_state(
    snapshot: FrozenPortfolioSnapshot,
    new_state: PortfolioLifecycleState,
) -> "FrozenPortfolioSnapshot":
    """Return a new snapshot with a different lifecycle_state.

    Uses ``object.__setattr__`` to bypass frozen=True for the controlled
    lifecycle transition only.  The digest is NOT recomputed: the state
    field is intentionally excluded from the canonical digest payload so
    that DRAFT→SEALED transitions are cryptographically stable.
    """
    import dataclasses as _dc

    return _dc.replace(snapshot, lifecycle_state=new_state)


# ---------------------------------------------------------------------------
# Admission gate
# ---------------------------------------------------------------------------


def require_admitted_portfolio(
    snapshot: FrozenPortfolioSnapshot,
    *,
    workspace_id: str,
    campaign_id: str,
) -> FrozenPortfolioSnapshot:
    """Fail-closed admission predicate for downstream evidence acquisition.

    Validates that:
    1. The snapshot is a ``FrozenPortfolioSnapshot`` instance.
    2. The workspace_id and campaign_id match (cross-workspace guard).
    3. The lifecycle_state is SEALED.
    4. The revision_digest has not been mutated.

    Raises
    ------
    PortfolioAdmissionError
        If the snapshot is None, not an instance, in the wrong state, or
        bound to a different workspace/campaign.
    PortfolioDigestMismatchError
        If the revision_digest no longer matches the canonical payload.

    Returns the validated snapshot unchanged so callers can use it inline.
    """
    if not isinstance(snapshot, FrozenPortfolioSnapshot):
        raise PortfolioAdmissionError(
            "evidence acquisition requires a FrozenPortfolioSnapshot; got "
            f"{type(snapshot).__name__!r}"
        )
    if snapshot.workspace_id != workspace_id:
        raise PortfolioAdmissionError(
            f"portfolio workspace_id '{snapshot.workspace_id}' does not match "
            f"requested workspace_id '{workspace_id}'"
        )
    if snapshot.campaign_id != campaign_id:
        raise PortfolioAdmissionError(
            f"portfolio campaign_id '{snapshot.campaign_id}' does not match "
            f"requested campaign_id '{campaign_id}'"
        )
    if snapshot.lifecycle_state != PortfolioLifecycleState.SEALED:
        raise PortfolioAdmissionError(
            f"portfolio revision '{snapshot.revision_id}' must be SEALED before "
            f"evidence acquisition; current state is '{snapshot.lifecycle_state.value}'"
        )
    snapshot.verify_digest()  # raises PortfolioDigestMismatchError on corrupt digest
    return snapshot


# ---------------------------------------------------------------------------
# In-process portfolio registry (process-local, not persisted)
# ---------------------------------------------------------------------------


class FrozenPortfolioRegistry:
    """Process-local registry of frozen portfolio snapshots.

    This registry tracks sealed revisions per workspace/portfolio series.  It
    enforces:
    - No duplicate revision_id registration within a workspace+portfolio.
    - Only SEALED snapshots can be registered as the active revision.
    - The active revision cannot be overwritten in place; a new revision must
      be registered.

    This is an in-process adapter.  For production use, the caller must
    persist ``snapshot.to_dict()`` to the authoritative store via the
    ``CollisionHypothesisStore`` or equivalent SQLite/PostgreSQL adapter and
    reconstitute from that store.
    """

    def __init__(self) -> None:
        # Maps (workspace_id, portfolio_id, revision_id) -> snapshot
        self._revisions: dict[tuple[str, str, str], FrozenPortfolioSnapshot] = {}
        # Maps (workspace_id, portfolio_id) -> active revision_id
        self._active: dict[tuple[str, str], str] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, snapshot: FrozenPortfolioSnapshot) -> None:
        """Register a sealed portfolio snapshot as an available revision.

        Raises
        ------
        PortfolioAdmissionError
            If the snapshot is not SEALED.
        PortfolioDigestMismatchError
            If the snapshot digest is invalid.
        DuplicatePortfolioRevisionError
            If this (workspace_id, portfolio_id, revision_id) triple already
            exists in the registry.
        """
        if snapshot.lifecycle_state != PortfolioLifecycleState.SEALED:
            raise PortfolioAdmissionError(
                f"only SEALED snapshots may be registered; "
                f"revision '{snapshot.revision_id}' is '{snapshot.lifecycle_state.value}'"
            )
        snapshot.verify_digest()

        key = (snapshot.workspace_id, snapshot.portfolio_id, snapshot.revision_id)
        if key in self._revisions:
            raise DuplicatePortfolioRevisionError(
                f"portfolio revision '{snapshot.revision_id}' already registered for "
                f"workspace='{snapshot.workspace_id}' portfolio='{snapshot.portfolio_id}'; "
                "create a new revision_id rather than overwriting"
            )
        self._revisions[key] = snapshot
        # Update the active pointer to the latest registered revision
        active_key = (snapshot.workspace_id, snapshot.portfolio_id)
        self._active[active_key] = snapshot.revision_id

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def get_revision(
        self,
        workspace_id: str,
        portfolio_id: str,
        revision_id: str,
    ) -> Optional[FrozenPortfolioSnapshot]:
        """Retrieve a specific revision or None if not found."""
        return self._revisions.get((workspace_id, portfolio_id, revision_id))

    def get_active_revision(
        self,
        workspace_id: str,
        portfolio_id: str,
    ) -> Optional[FrozenPortfolioSnapshot]:
        """Retrieve the current active (most-recently-registered) revision."""
        active_key = (workspace_id, portfolio_id)
        revision_id = self._active.get(active_key)
        if revision_id is None:
            return None
        return self._revisions.get((workspace_id, portfolio_id, revision_id))

    def list_revision_ids(
        self,
        workspace_id: str,
        portfolio_id: str,
    ) -> list[str]:
        """Return all registered revision_ids for a workspace/portfolio, insertion order."""
        prefix = (workspace_id, portfolio_id)
        return [
            rev_id
            for (ws, pid, rev_id) in self._revisions.keys()
            if (ws, pid) == prefix
        ]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value
