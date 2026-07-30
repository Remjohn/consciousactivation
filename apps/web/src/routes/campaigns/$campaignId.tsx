import { createFileRoute } from "@tanstack/react-router";
import { CampaignDetail } from "../../pages/CampaignDetail";

export const Route = createFileRoute("/campaigns/$campaignId")({
  component: CampaignDetailRoute,
});

function CampaignDetailRoute() {
  const { campaignId } = Route.useParams();
  return <CampaignDetail campaignId={campaignId} />;
}
