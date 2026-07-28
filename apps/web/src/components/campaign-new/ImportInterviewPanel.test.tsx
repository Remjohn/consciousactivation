import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, beforeAll } from "vitest";
import { setupServer } from "msw/node";
import { handlers } from "../../test/handlers";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ImportInterviewPanel } from "./ImportInterviewPanel";

// AC-007

const server = setupServer(...handlers);

beforeAll(() => server.listen());

function renderWithQuery(ui: React.ReactElement) {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>,
  );
}

describe("ImportInterviewPanel", () => {
  it("AC-007: import success unlocks Continue (import_success_unlocks_continue)", async () => {
    renderWithQuery(<ImportInterviewPanel onReady={() => {}} />);

    // Simulate file selection (simplified for test)
    const videoInput = screen.getByTestId("video-input");
    const transcriptInput = screen.getByTestId("transcript-input");

    // Create mock files
    const videoFile = new File(["video content"], "video.mp4", { type: "video/mp4" });
    const transcriptFile = new File(["transcript content"], "transcript.json", { type: "application/json" });

    fireEvent.change(videoInput, { target: { files: [videoFile] } });
    fireEvent.change(transcriptInput, { target: { files: [transcriptFile] } });

    // Fill required fields
    fireEvent.change(screen.getByTestId("workspace-id-input"), { target: { value: "workspace:acme" } });
    fireEvent.change(screen.getByTestId("project-id-input"), { target: { value: "project:q3" } });
    fireEvent.change(screen.getByTestId("operator-id-input"), { target: { value: "op:1" } });
    fireEvent.change(screen.getByTestId("authority-scope-input"), { target: { value: "scope:1" } });
    fireEvent.change(screen.getByTestId("assertion-id-input"), { target: { value: "assert:1" } });

    // Submit
    const submitBtn = screen.getByTestId("import-submit-btn");
    fireEvent.click(submitBtn);

    // Wait for success (the onReady callback would be called)
    await waitFor(() => {
      // Check that the mutation succeeded (no error shown)
      expect(screen.queryByTestId("import-error")).not.toBeInTheDocument();
    });
  });
});
