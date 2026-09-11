from __future__ import annotations

from cmf_pipeline.workflow.infrastructure.repository import PipelineRepository

CAMPAIGN_RUN_RELATION_TYPE = "campaign_produces_run"


class CampaignHasNoRun(Exception):
    def __init__(self, campaign_id: str):
        self.campaign_id = campaign_id
        super().__init__(f"No pipeline run is linked to campaign {campaign_id!r}.")


class CampaignHasMultipleRuns(Exception):
    def __init__(self, campaign_id: str, run_ids: list[str]):
        self.campaign_id = campaign_id
        self.run_ids = run_ids
        super().__init__(
            f"Campaign {campaign_id!r} has {len(run_ids)} linked runs; expected exactly one."
        )


def resolve_campaign_run_id(repository: PipelineRepository, campaign_id: str) -> str:
    """Read-only lookup over the pre-existing generic edge store.

    Writing the campaign_produces_run edge is TS-APP-API-004's responsibility,
    performed when it calls WorkflowRunService.create_run() for a Campaign Order:

        repository.add_edge(campaign_id, run_id, CAMPAIGN_RUN_RELATION_TYPE)

    This function does not write anything.
    """
    run_ids = repository.descendants(
        [campaign_id], relation_types={CAMPAIGN_RUN_RELATION_TYPE}
    )
    if not run_ids:
        raise CampaignHasNoRun(campaign_id)
    if len(run_ids) > 1:
        raise CampaignHasMultipleRuns(campaign_id, list(run_ids))
    return run_ids[0]