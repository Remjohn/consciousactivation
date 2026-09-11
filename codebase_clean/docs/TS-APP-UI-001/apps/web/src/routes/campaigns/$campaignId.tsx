import { createFileRoute } from "@tanstack/react-router";
import { PlaceholderPage } from "../../components/layout/PlaceholderPage";

export function CampaignDetailPage() {
  return (
    <PlaceholderPage title="Control Tower" frRange="FR-APP-060..064" builtIn="TS-APP-UI-003" />
  );
}

export const Route = createFileRoute("/campaigns/$campaignId")({
  component: CampaignDetailPage,
});
