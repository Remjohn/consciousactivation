import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ResearchPanel } from "./ResearchPanel";
import * as WorkspaceContextModule from "../../context/WorkspaceContext";
import * as useCreateResearchPackageModule from "../../hooks/useCreateResearchPackage";
import type { GuestResearchPackageResponse } from "../../api/types";

describe("ResearchPanel", () => {
  let queryClient: QueryClient;
  const mockMutateAsync = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });

    vi.spyOn(WorkspaceContextModule, "useWorkspace").mockReturnValue({
      activeWorkspace: {
        workspace_id: "ws-test-123",
        slug: "ws-test",
        display_name: "Test Workspace",
        created_at: "2026-08-27T00:00:00Z",
        updated_at: "2026-08-27T00:00:00Z",
      },
      activeWorkspaceId: "ws-test-123",
      workspaces: [],
      isLoading: false,
      error: null,
      selectWorkspace: vi.fn(),
      createNewWorkspace: vi.fn(),
      updateActiveWorkspace: vi.fn(),
      refreshWorkspaces: vi.fn(),
      clearError: vi.fn(),
    });

    vi.spyOn(useCreateResearchPackageModule, "useCreateResearchPackage").mockReturnValue({
      mutateAsync: mockMutateAsync,
      isPending: false,
      error: null,
      data: undefined,
    } as any);
  });

  function renderComponent(onReady = vi.fn()) {
    return render(
      <QueryClientProvider client={queryClient}>
        <ResearchPanel onReady={onReady} />
      </QueryClientProvider>
    );
  }

  it("auto-injects active workspace ID from context into the form", () => {
    renderComponent();
    expect(screen.getByTestId("active-workspace-badge")).toHaveTextContent("ws-test-123");
    expect(screen.getByTestId("workspace-id-input")).toHaveValue("ws-test-123");
  });

  it("HN-GST-01: Rejects empty or whitespace-only guest name", () => {
    renderComponent();

    const guestInput = screen.getByTestId("guest-name-input");
    fireEvent.change(guestInput, { target: { value: "   " } });

    const form = screen.getByTestId("research-form");
    fireEvent.submit(form);

    expect(mockMutateAsync).not.toHaveBeenCalled();
    expect(screen.getByTestId("research-error-banner")).toBeInTheDocument();
    expect(screen.getByTestId("research-error")).toHaveTextContent(/HN-GST-01/);
  });

  it("HN-GST-04: Rejects submission when active workspace ID is empty", () => {
    vi.spyOn(WorkspaceContextModule, "useWorkspace").mockReturnValue({
      activeWorkspace: null,
      activeWorkspaceId: null,
      workspaces: [],
      isLoading: false,
      error: null,
      selectWorkspace: vi.fn(),
      createNewWorkspace: vi.fn(),
      updateActiveWorkspace: vi.fn(),
      refreshWorkspaces: vi.fn(),
      clearError: vi.fn(),
    });

    renderComponent();

    const guestInput = screen.getByTestId("guest-name-input");
    fireEvent.change(guestInput, { target: { value: "Audrey Hepburn" } });

    const wsInput = screen.getByTestId("workspace-id-input");
    fireEvent.change(wsInput, { target: { value: "" } });

    const form = screen.getByTestId("research-form");
    fireEvent.submit(form);

    expect(mockMutateAsync).not.toHaveBeenCalled();
    expect(screen.getByTestId("research-error-banner")).toBeInTheDocument();
    expect(screen.getByTestId("research-error")).toHaveTextContent(/HN-GST-04/);
  });

  it("HN-GST-05: Rejects submission when operator authority fields are empty", () => {
    renderComponent();

    const guestInput = screen.getByTestId("guest-name-input");
    fireEvent.change(guestInput, { target: { value: "Audrey Hepburn" } });

    const opInput = screen.getByTestId("operator-id-input");
    fireEvent.change(opInput, { target: { value: "" } });

    const form = screen.getByTestId("research-form");
    fireEvent.submit(form);

    expect(mockMutateAsync).not.toHaveBeenCalled();
    expect(screen.getByTestId("research-error-banner")).toBeInTheDocument();
    expect(screen.getByTestId("research-error")).toHaveTextContent(/HN-GST-05/);
  });

  it("Successfully submits research package and renders ResearchPackageInspector", async () => {
    const handleReady = vi.fn();

    const mockResponse: GuestResearchPackageResponse = {
      research_package_id: "pkg-audrey-001",
      revision: 1,
      guest_name: "Audrey Hepburn",
      source_urls: ["https://example.com/audrey"],
      uploaded_documents: [
        {
          asset_id: "ast-001",
          original_filename: "audrey_bio.pdf",
          bytes: 45000,
          media_type: "application/pdf",
          sha256: "aabbcc11223344",
          context_class: "IDENTITY_DNA",
        },
      ],
      idempotent_replay: false,
    };

    mockMutateAsync.mockResolvedValueOnce(mockResponse);

    renderComponent(handleReady);

    const guestInput = screen.getByTestId("guest-name-input");
    fireEvent.change(guestInput, { target: { value: "Audrey Hepburn" } });

    const form = screen.getByTestId("research-form");
    fireEvent.submit(form);

    expect(mockMutateAsync).toHaveBeenCalledWith(
      expect.objectContaining({
        guestName: "Audrey Hepburn",
        workspaceId: "ws-test-123",
      })
    );

    // Inspector should now be rendered
    await waitFor(() => {
      expect(screen.getByTestId("research-inspector")).toBeInTheDocument();
    });
    expect(screen.getByTestId("inspector-package-id")).toHaveTextContent("pkg-audrey-001");

    // Proceed to brief
    const proceedBtn = screen.getByTestId("proceed-to-brief-btn");
    fireEvent.click(proceedBtn);
    expect(handleReady).toHaveBeenCalledWith("pkg-audrey-001");
  });
});
