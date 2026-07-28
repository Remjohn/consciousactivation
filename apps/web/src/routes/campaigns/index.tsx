import { createFileRoute } from "@tanstack/react-router";
import { CampaignList } from "../../pages/CampaignList";

export const Route = createFileRoute("/campaigns/")({
  component: CampaignList,
});
