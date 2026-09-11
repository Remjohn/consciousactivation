import { createFileRoute } from "@tanstack/react-router";
import { PlaceholderPage } from "../../components/layout/PlaceholderPage";

export function CampaignsIndexPage() {
  return (
    <PlaceholderPage title="Campaigns" frRange="FR-APP-050" builtIn="TS-APP-UI-002" />
  );
}

export const Route = createFileRoute("/campaigns/")({
  component: CampaignsIndexPage,
});
