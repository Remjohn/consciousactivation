import { createFileRoute } from "@tanstack/react-router";
import { PlaceholderPage } from "../../components/layout/PlaceholderPage";

export function WorkspaceIndexPage() {
  return (
    <PlaceholderPage
      title="Workspace"
      frRange="FR-APP-001..003"
      builtIn="TS-APP-UI (not yet queued)"
    />
  );
}

export const Route = createFileRoute("/workspace/")({
  component: WorkspaceIndexPage,
});
