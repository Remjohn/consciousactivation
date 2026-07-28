import { createFileRoute } from "@tanstack/react-router";
import { PlaceholderPage } from "../../components/layout/PlaceholderPage";

export function CampaignsNewPage() {
  return (
    <PlaceholderPage title="New Campaign" frRange="FR-APP-050" builtIn="TS-APP-UI-002" />
  );
}

export const Route = createFileRoute("/campaigns/new")({
  component: CampaignsNewPage,
});
