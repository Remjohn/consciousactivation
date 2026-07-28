import { createFileRoute } from "@tanstack/react-router";
import { PlaceholderPage } from "../../components/layout/PlaceholderPage";

export function InterviewsComposePage() {
  return (
    <PlaceholderPage
      title="Interview Composer"
      frRange="FR-APP-010..012"
      builtIn="TS-APP-COMPOSER-001"
    />
  );
}

export const Route = createFileRoute("/interviews/compose")({
  component: InterviewsComposePage,
});
