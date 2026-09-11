import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, beforeAll, afterEach, afterAll, vi } from "vitest";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { setupServer } from "msw/node";
import { handlers } from "../../test/handlers";
import { DevOperatorProvider } from "../../auth/DevOperatorContext";
import { WorkspaceProvider } from "../../context/WorkspaceContext";
import { WorkspaceSelector } from "./WorkspaceSelector";

const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => {
  server.resetHandlers();
  localStorage.clear();
});
afterAll(() => server.close());

describe("WorkspaceSelector Component", () => {
  it("renders workspace selector dropdown and triggers creation callback", async () => {
    const handleOpenCreate = vi.fn();
    const queryClient = new QueryClient();

    render(
      <QueryClientProvider client={queryClient}>
        <DevOperatorProvider>
          <WorkspaceProvider initialWorkspaceId="11111111-1111-1111-1111-111111111111">
            <WorkspaceSelector onOpenCreate={handleOpenCreate} />
          </WorkspaceProvider>
        </DevOperatorProvider>
      </QueryClientProvider>,
    );

    const selector = await screen.findByTestId("workspace-selector");
    expect(selector).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText(/Acme Production/)).toBeInTheDocument();
    });

    // Select + New Workspace...
    fireEvent.change(selector, { target: { value: "__NEW__" } });
    expect(handleOpenCreate).toHaveBeenCalledTimes(1);
  });
});
