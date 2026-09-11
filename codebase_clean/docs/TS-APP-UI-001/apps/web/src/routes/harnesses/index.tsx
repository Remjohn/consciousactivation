import { createFileRoute } from "@tanstack/react-router";
import { PlaceholderPage } from "../../components/layout/PlaceholderPage";

export function HarnessesIndexPage() {
  return (
    <PlaceholderPage title="Harness Library" frRange="FR-APP-040..041" builtIn="TS-APP-UI-004" />
  );
}

export const Route = createFileRoute("/harnesses/")({
  component: HarnessesIndexPage,
});
