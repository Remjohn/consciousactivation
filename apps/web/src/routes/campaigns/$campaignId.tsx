import { createFileRoute } from "@tanstack/react-router";
import { CampaignDetail } from "../../pages/CampaignDetail";

export const Route = createFileRoute("/campaigns/$campaignId")({
  component: CampaignDetail,
});
