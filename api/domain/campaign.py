from __future__ import annotations

"""TS-APP-API-004 Stage 1 -- pure-logic port of Studio's CampaignOrder /
CampaignState domain (services/studio/src/domain.ts, campaign.ts,
validators.ts, canonical.ts). No I/O, no FastAPI dependency. Every error
code below is copied verbatim from validators.ts / campaign.ts, not
invented -- see docs/tech-specs/TS-APP-API-004.md Section 3.
"""

import re
from typing import Any, Mapping, Sequence

from ca_contracts import canonical_sha256

_PREFIX_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._:-]*$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

ALLOWED_TRANSITIONS: dict[str, tuple[str, ...]] = {
    "DRAFT": ("LAUNCHED", "CANCELLED"),
    "LAUNCHED": ("RUNNING", "CANCELLED"),
    "RUNNING": ("AWAITING_REVIEW", "BLOCKED_EXCEPTION", "READY_TO_SHIP", "CANCELLED"),
    "AWAITING_REVIEW": ("RUNNING", "READY_TO_SHIP", "CANCELLED"),
    "BLOCKED_EXCEPTION": ("RUNNING", "AWAITING_REVIEW", "CANCELLED"),
    "READY_TO_SHIP": ("SHIPPED", "AWAITING_REVIEW", "CANCELLED"),
    "SHIPPED": (),
    "CANCELLED": (),
}


class CampaignValidationError(ValueError):
    """Python port of Studio's StudioValidationError, scoped to CampaignOrder /
    CampaignState. Error codes are copied verbatim from
    services/studio/src/validators.ts and campaign.ts."""

    def __init__(self, code: str, message: str, context: Mapping[str, Any] | None = None):
        super().__init__(message)
        self.code = code
        self.context = dict(context or {})


def deterministic_id(prefix: str, value: Any) -> str:
    """Port of services/studio/src/canonical.ts::deterministicId. Uses
    ca_contracts.canonical_sha256, confirmed algorithmically identical to
    canonicalSha256 in canonical.ts, so IDs minted here are bit-identical
    to IDs the TS domain would mint for the same logical payload."""
    if not _PREFIX_RE.match(prefix):
        raise CampaignValidationError("INVALID_ID_PREFIX", f"invalid deterministic ID prefix: {prefix}")
    return f"{prefix}:{canonical_sha256(value)[:24]}"


def _require_non_empty(value: str, label: str) -> None:
    if not value or not value.strip():
        raise CampaignValidationError("EMPTY_VALUE", f"{label} must not be empty", {"label": label})


def _require_safe_integer(value: int, label: str, minimum: int = 0) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise CampaignValidationError(
            "INVALID_INTEGER", f"{label} must be an integer >= {minimum}", {"label": label, "value": value}
        )


def _validate_ref(ref: Mapping[str, Any], label: str) -> None:
    _require_non_empty(ref["object_id"], f"{label}.object_id")
    _require_non_empty(ref["version"], f"{label}.version")
    if not _SHA256_RE.match(ref["sha256"]):
        raise CampaignValidationError("INVALID_SHA256", f"{label}.sha256 must be lowercase SHA-256", {"label": label})


def _validate_actor(actor: Mapping[str, Any]) -> None:
    _require_non_empty(actor["actor_id"], "actor_id")
    _require_non_empty(actor["product_id"], "product_id")


def validate_campaign_order(order: Mapping[str, Any]) -> None:
    """Direct port of validateCampaignOrder (validators.ts). Deliberately does
    NOT validate deadline_utc, taste_direction, source_kind, or authority --
    matching the TS function exactly, not a superset of it."""
    _require_non_empty(order["workspace_id"], "workspace_id")
    _require_non_empty(order["project_id"], "project_id")
    _validate_ref(order["source_ref"], "source_ref")
    _validate_ref(order["harness_ref"], "harness_ref")
    _require_non_empty(order["category_id"], "category_id")
    _require_non_empty(order["objective"], "objective")
    _require_non_empty(order["initial_seed"], "initial_seed")
    _require_safe_integer(order["budget_units"], "budget_units", 1)
    if not order["output_targets"]:
        raise CampaignValidationError("OUTPUT_TARGET_REQUIRED", "at least one output target is required")
    for target in order["output_targets"]:
        _require_safe_integer(target["quantity"], "output_target.quantity", 1)
    if order["category_id"] == "2d_character_animation" or order["format_profile_id"].startswith("format02_"):
        raise CampaignValidationError("FORMAT02_DEFERRED", "Format 02 is deferred pending a current validated Atomic Harness")
    _validate_actor(order["operator_actor"])


def default_autonomy_policy(mode: str) -> dict[str, Any]:
    """Port of defaultAutonomyPolicy (campaign.ts)."""
    return {
        "mode": mode,
        "checkpoint_ids": ["final-script-approval", "final-artifact-review"] if mode == "CHECKPOINTED" else [],
        "exception_only": mode in ("AUTOPILOT", "REVIEW_BEFORE_SHIP"),
        "final_review_required": mode != "AUTOPILOT",
        "publication_authority_required": True,
    }


def create_campaign_order(core: Mapping[str, Any]) -> dict[str, Any]:
    """Port of createCampaignOrder (campaign.ts). `core` is every CampaignOrder
    field except order_id."""
    order = {**core, "order_id": deterministic_id("campaign-order", core)}
    validate_campaign_order(order)
    return order


def launch_campaign(order: Mapping[str, Any]) -> dict[str, Any]:
    """Port of launchCampaign (campaign.ts). Produces LAUNCHED directly -- no
    code path in the ported TS domain ever constructs a DRAFT CampaignState."""
    validate_campaign_order(order)
    order_ref = {"object_id": order["order_id"], "version": "1.0.0", "sha256": canonical_sha256(order)}
    return {
        "campaign_id": deterministic_id("campaign", {"order_ref": order_ref}),
        "order_ref": order_ref,
        "lifecycle_state": "LAUNCHED",
        "autonomy_mode": order["autonomy_policy"]["mode"],
        "active_checkpoint_id": None,
        "exception_ids": [],
        "run_refs": [],
        "artifact_refs": [],
        "evaluation_refs": [],
        "version": 1,
    }


_UNSET = object()


def transition_campaign(
    state: Mapping[str, Any],
    next_state: str,
    *,
    checkpoint_id: str | None = _UNSET,  # type: ignore[assignment]
    exception_ids: Sequence[str] | None = None,
    run_refs: Sequence[Mapping[str, Any]] | None = None,
    artifact_refs: Sequence[Mapping[str, Any]] | None = None,
    evaluation_refs: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Port of transitionCampaign (campaign.ts). `checkpoint_id` uses the
    _UNSET sentinel (not None) to mirror TS's undefined-vs-null distinction:
    "caller didn't pass this" vs "caller wants it explicitly cleared".
    Reused unchanged by TS-APP-API-005/006 for RUNNING/AWAITING_REVIEW/
    BLOCKED_EXCEPTION/READY_TO_SHIP/SHIPPED transitions -- this spec only
    calls it with next_state="CANCELLED"."""
    current = state["lifecycle_state"]
    if next_state not in ALLOWED_TRANSITIONS.get(current, ()):
        raise CampaignValidationError("CAMPAIGN_TRANSITION_DENIED", f"{current} cannot transition to {next_state}")
    if next_state == "SHIPPED" and state["autonomy_mode"] == "SHADOW":
        raise CampaignValidationError("SHADOW_CANNOT_SHIP", "SHADOW campaigns cannot transition to SHIPPED")
    return {
        **state,
        "lifecycle_state": next_state,
        "active_checkpoint_id": state["active_checkpoint_id"] if checkpoint_id is _UNSET else checkpoint_id,
        "exception_ids": sorted(set(state["exception_ids"] if exception_ids is None else exception_ids)),
        "run_refs": list(state["run_refs"] if run_refs is None else run_refs),
        "artifact_refs": list(state["artifact_refs"] if artifact_refs is None else artifact_refs),
        "evaluation_refs": list(state["evaluation_refs"] if evaluation_refs is None else evaluation_refs),
        "version": state["version"] + 1,
    }
