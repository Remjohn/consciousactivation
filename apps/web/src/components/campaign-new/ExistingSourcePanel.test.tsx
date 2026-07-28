import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, beforeAll, afterEach } from "vitest";
import { setupServer } from "msw/node";
import { handlers } from "../../test/handlers";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ExistingSourcePanel } from "./ExistingSourcePanel";

// AC-005, AC-006

const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());

function renderWithQuery(ui: React.ReactElement) {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>,
  );
}

describe("ExistingSourcePanel", () => {
  it("AC-005: gates Continue on readiness (existing_source_gates_continue_on_readiness)", async () => {
    renderWithQuery(<ExistingSourcePanel onReady={() => {}} />);

    const input = screen.getByTestId("existing-source-input");
    const checkBtn = screen.getByTestId("check-status-btn");
    const continueBtn = screen.getByTestId("existing-continue-btn");

    // Enter a valid package ID and check status
    fireEvent.change(input, { target: { value: "pkg:valid" } });
    fireEvent.click(checkBtn);

    // Wait for status to load and Continue to be enabled
    await waitFor(() => {
      expect(continueBtn).not.toBeDisabled();
    });
  });

  it("AC-006: shows NOT_FOUND error for unknown source (unknown_source_shows_not_found)", async () => {
    renderWithQuery(<ExistingSourcePanel onReady={() => {}} />);

    const input = screen.getByTestId("existing-source-input");
    const checkBtn = screen.getByTestId("check-status-btn");

    fireEvent.change(input, { target: { value: "unknown" } });
    fireEvent.click(checkBtn);

    await waitFor(() => {
      expect(screen.getByTestId("source-error")).toHaveTextContent("NOT_FOUND");
    });
  });
});
