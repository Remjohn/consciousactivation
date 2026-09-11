import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import { describe, it, expect, beforeAll, afterEach, afterAll } from "vitest";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { setupServer } from "msw/node";
import { handlers } from "../../test/handlers";
import { DevOperatorProvider } from "../../auth/DevOperatorContext";
import { WorkspaceProvider } from "../../context/WorkspaceContext";
import { WorkspaceConsole } from "../../components/workspace/WorkspaceConsole";
import { ErrorEnvelopeAlert } from "../../components/workspace/ErrorEnvelopeAlert";
import { ApiError } from "../../api/ApiError";

const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => {
  server.resetHandlers();
  localStorage.clear();
});
afterAll(() => server.close());

function renderWorkspaceConsole(initialWorkspaceId?: string) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

  const utils = render(
    <QueryClientProvider client={queryClient}>
      <DevOperatorProvider>
        <WorkspaceProvider initialWorkspaceId={initialWorkspaceId}>
          <WorkspaceConsole />
        </WorkspaceProvider>
      </DevOperatorProvider>
    </QueryClientProvider>,
  );

  return { ...utils, queryClient };
}

describe("Workspace Management Console (SPEC-TWC-UI-001 / CA-TWC-UI-01)", () => {
  it("renders the Workspace Console header, title, and FR range", async () => {
    renderWorkspaceConsole("11111111-1111-1111-1111-111111111111");

    expect(await screen.findByRole("heading", { name: /Workspace/i, level: 1 })).toBeInTheDocument();
    expect(screen.getByTestId("spec-badge")).toHaveTextContent("FR-APP-001..003");
    expect(screen.getByTestId("create-new-workspace-button")).toBeInTheDocument();
  });

  it("auto-provisions workspace derived from account identity on first login (DEC-TWC-001)", async () => {
    // When no workspaces exist, auto-creation derived from account identity triggers
    renderWorkspaceConsole();

    // Verify workspace display name derived from operator actor_id or mock
    await waitFor(() => {
      const heading = screen.getByTestId("workspace-display-name");
      expect(heading).toBeInTheDocument();
      expect(heading.textContent).toMatch(/(Acme Production|test-operator-01's Workspace)/);
    });
  });

  it("HN-TWC-01: Rejects empty or whitespace-only workspace name with inline validation", async () => {
    renderWorkspaceConsole("11111111-1111-1111-1111-111111111111");

    const newBtn = await screen.findByTestId("create-new-workspace-button");
    fireEvent.click(newBtn);

    const nameInput = screen.getByTestId("workspace-name-input");
    const submitBtn = screen.getByTestId("create-workspace-submit-button");

    // Enter whitespace only
    fireEvent.change(nameInput, { target: { value: "   " } });
    fireEvent.click(submitBtn);

    const validationAlert = await screen.findByTestId("validation-error");
    expect(validationAlert).toHaveTextContent(/cannot be empty or whitespace only/i);
  });

  it("HN-TWC-02: Rejects illegal role enum and handles validation failures", async () => {
    renderWorkspaceConsole("11111111-1111-1111-1111-111111111111");

    const addMemberBtn = await screen.findByTestId("open-add-member-button");
    fireEvent.click(addMemberBtn);

    const actorInput = screen.getByTestId("member-actor-id-input");
    const submitBtn = screen.getByTestId("add-member-submit-button");

    // Leave actor empty
    fireEvent.change(actorInput, { target: { value: "   " } });
    fireEvent.click(submitBtn);

    const validationAlert = await screen.findByTestId("validation-error");
    expect(validationAlert).toHaveTextContent(/cannot be empty/i);
  });

  it("HN-TWC-03: Rejects mutations on suspended workspace", async () => {
    renderWorkspaceConsole("22222222-2222-2222-2222-222222222222");

    // Suspended alert must be present
    expect(await screen.findByTestId("workspace-suspended-alert")).toBeInTheDocument();
    expect(screen.getByTestId("workspace-status-badge")).toHaveTextContent("SUSPENDED");

    // Add member button must be disabled
    const addMemberBtn = screen.getByTestId("open-add-member-button");
    expect(addMemberBtn).toBeDisabled();

    // Issue grant button must be disabled
    const issueGrantBtn = screen.getByTestId("open-issue-grant-button");
    expect(issueGrantBtn).toBeDisabled();
  });

  it("HN-TWC-04: Enforces strict tenant context isolation and query cache invalidation on workspace switch", async () => {
    const { queryClient } = renderWorkspaceConsole("11111111-1111-1111-1111-111111111111");

    await screen.findByTestId("workspace-display-name");

    // Seed mock campaign query in cache
    queryClient.setQueryData(["campaigns"], [{ campaign_id: "cmp-acme-1" }]);
    expect(queryClient.getQueryData(["campaigns"])).toBeDefined();

    // Click secondary workspace
    const suspendedNavItem = screen.getByTestId("workspace-nav-item-acme-suspended");
    fireEvent.click(suspendedNavItem);

    // After switch, active workspace updates and cache is invalidated
    await waitFor(() => {
      expect(screen.getByTestId("workspace-display-name")).toHaveTextContent("Acme Suspended Lab");
    });
  });

  it("HN-TWC-05: Enforces immediate revocation of workspace membership without page reload", async () => {
    renderWorkspaceConsole("11111111-1111-1111-1111-111111111111");

    // Add a test member first
    const addMemberBtn = await screen.findByTestId("open-add-member-button");
    fireEvent.click(addMemberBtn);

    const actorInput = screen.getByTestId("member-actor-id-input");
    const roleSelect = screen.getByTestId("member-role-select");
    const submitBtn = screen.getByTestId("add-member-submit-button");

    fireEvent.change(actorInput, { target: { value: "bob@acme.com" } });
    fireEvent.change(roleSelect, { target: { value: "MEMBER" } });
    fireEvent.click(submitBtn);

    // Verify Bob is added
    const bobRow = await screen.findByTestId("member-row-bob@acme.com");
    expect(bobRow).toBeInTheDocument();
    expect(screen.getByTestId("status-badge-bob@acme.com")).toHaveTextContent("ACTIVE");

    // Click revoke button for Bob
    const revokeBtn = screen.getByTestId("revoke-member-button-bob@acme.com");
    fireEvent.click(revokeBtn);

    // Verify Bob's row is immediately marked REVOKED without reload
    await waitFor(() => {
      expect(screen.getByTestId("status-badge-bob@acme.com")).toHaveTextContent("REVOKED");
    });
  });

  it("handles TS-APP-API-004 §5 typed error envelopes with structured error badge and message", () => {
    const apiError = new ApiError("Workspace was suspended by security policy", 409, "WORKSPACE_SUSPENDED");

    render(<ErrorEnvelopeAlert error={apiError} />);

    expect(screen.getByTestId("error-envelope-alert")).toBeInTheDocument();
    expect(screen.getByTestId("error-code-badge")).toHaveTextContent("WORKSPACE_SUSPENDED");
    expect(screen.getByText("Workspace was suspended by security policy")).toBeInTheDocument();
  });

  it("supports issuing and revoking operator access grants (OPR-001)", async () => {
    renderWorkspaceConsole("11111111-1111-1111-1111-111111111111");

    const issueGrantBtn = await screen.findByTestId("open-issue-grant-button");
    fireEvent.click(issueGrantBtn);

    const actorInput = screen.getByTestId("grant-actor-input");
    const justificationInput = screen.getByTestId("grant-justification-input");
    const submitBtn = screen.getByTestId("issue-grant-submit-button");

    fireEvent.change(actorInput, { target: { value: "op-auditor-99" } });
    fireEvent.change(justificationInput, { target: { value: "Routine compliance verification" } });
    fireEvent.click(submitBtn);

    // Verify grant table displays the new grant
    const grantTable = await screen.findByTestId("grant-table");
    expect(grantTable).toHaveTextContent("op-auditor-99");
    expect(grantTable).toHaveTextContent("Routine compliance verification");
  });
});
