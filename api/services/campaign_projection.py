from __future__ import annotations

from typing import Any

from cmf_pipeline.application import PipelineApplication
from cmf_pipeline.domain.errors import PipelineConflict, PipelineNotFound

# TS-APP-API-006 Source gap notice 2 / ASSUMED_INTERFACE_PENDING_004:
# This spec defines and reads the Campaign persistence convention over
# PipelineRepository's generic, content-addressed, revisioned object store
# (the same store cmf_pipeline uses everywhere else). TS-APP-API-004's author
# must adopt this convention, or explicitly migrate away from it with a
# reconciliation note. Marked here, not in cmf_pipeline, since this spec
# deliberately adds nothing to that package.
CAMPAIGN_ORDER_TYPE = "studio_campaign_order"
CAMPAIGN_STATE_TYPE = "studio_campaign_state"


class CampaignNotFound(RuntimeError):
    pass


class CampaignStateConflict(RuntimeError):
    pass


def order_object_id(campaign_id: str) -> str:
    return f"studio-campaign-order:{campaign_id}"


def state_object_id(campaign_id: str) -> str:
    return f"studio-campaign-state:{campaign_id}"


def load_campaign(pipeline: PipelineApplication, campaign_id: str) -> dict[str, Any]:
    try:
        order = pipeline.repository.get_object(order_object_id(campaign_id))
        state = pipeline.repository.get_object(state_object_id(campaign_id))
    except PipelineNotFound as exc:
        raise CampaignNotFound(campaign_id) from exc
    return {"order": order["payload"], "state": state["payload"]}


def load_campaign_with_revisions(
    pipeline: PipelineApplication, campaign_id: str
) -> dict[str, Any]:
    """Like load_campaign but also returns the persisted state revision, so
    callers that need to advance the state can compute ``expected_revision``
    without an extra read-then-write race window."""
    try:
        order = pipeline.repository.get_object(order_object_id(campaign_id))
        state_row = pipeline.repository.get_object(state_object_id(campaign_id))
    except PipelineNotFound as exc:
        raise CampaignNotFound(campaign_id) from exc
    return {
        "order": order["payload"],
        "state": state_row["payload"],
        "state_revision": state_row["revision"],
    }


def save_campaign_state(
    pipeline: PipelineApplication,
    campaign_id: str,
    state: dict[str, Any],
    *,
    idempotency_key: str,
    expected_revision: int | None = None,
) -> dict[str, Any]:
    """Persist a new CampaignState revision.

    ``state`` must already carry the *next* version — Studio's own
    ``transitionCampaign()`` increments ``version`` before this is ever
    called. When ``expected_revision`` is None (the common path from the
    routers), the current revision is read here and used as the
    optimistic-concurrency guard, so a stale server-side read between this
    call's own read and write is caught by ``PipelineRepository``'s own
    ``PipelineConflict`` rather than silently overwriting a newer writer.
    """
    if expected_revision is None:
        try:
            current = pipeline.repository.get_object(state_object_id(campaign_id))
            expected_revision = current["revision"]
        except PipelineNotFound:
            expected_revision = 0
    try:
        result = pipeline.repository.store_object(
            CAMPAIGN_STATE_TYPE,
            state,
            idempotency_key=idempotency_key,
            object_id=state_object_id(campaign_id),
            expected_revision=expected_revision,
        )
    except PipelineConflict as exc:
        raise CampaignStateConflict(str(exc)) from exc
    return result["object"]["payload"]


def store_campaign(
    pipeline: PipelineApplication,
    campaign_id: str,
    order: dict[str, Any],
    state: dict[str, Any],
    *,
    idempotency_key: str,
) -> dict[str, Any]:
    """Persist both a CampaignOrder and its initial CampaignState.

    Used by fixtures (and, eventually, TS-APP-API-004's create endpoint) to
    write the pair this spec reads. The order is stored once, immutably; the
    state is the version-1 row that ``save_campaign_state`` will advance.
    """
    pipeline.repository.store_object(
        CAMPAIGN_ORDER_TYPE,
        order,
        idempotency_key=f"{idempotency_key}-order",
        object_id=order_object_id(campaign_id),
    )
    state_result = pipeline.repository.store_object(
        CAMPAIGN_STATE_TYPE,
        state,
        idempotency_key=f"{idempotency_key}-state",
        object_id=state_object_id(campaign_id),
    )
    return state_result["object"]["payload"]