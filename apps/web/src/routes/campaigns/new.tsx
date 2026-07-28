import { createFileRoute } from "@tanstack/react-router";
import { CampaignNew } from "../../pages/CampaignNew";

export const Route = createFileRoute("/campaigns/new")({
  component: CampaignNew,
});
