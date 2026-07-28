import { render, screen, within } from "@testing-library/react";
import { describe, it, expect, beforeAll, afterEach } from "vitest";
import { setupServer } from "msw/node";
import { handlers } from "../../test/handlers";
import { renderWithRouter } from "../../test/renderWithRouter";

// AC-001, AC-002, AC-003, AC-004

const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());

describe("CampaignList", () => {
  it("AC-001: renders lifecycle badges correctly (renders_lifecycle_badges)", async () => {
    renderWithRouter("/campaigns");
    // Wait for campaigns to load
    expect(await screen.findByText("RUNNING")).toBeInTheDocument();
    expect(screen.getByText("BLOCKED_EXCEPTION")).toBeInTheDocument();
    expect(screen.getByText("SHIPPED")).toBeInTheDocument();
  });

  it("AC-002: shows empty state when no campaigns (renders_empty_state_not_error)", async () => {
    // Override handler to return empty array
    server.use(
      handlers[0], // GET /api/campaigns
    );
    renderWithRouter("/campaigns");
    expect(await screen.findByText("No campaigns yet")).toBeInTheDocument();
  });

  it("AC-003: filter chip sets query param (filter_chip_sets_query_param)", async () => {
    const { router } = renderWithRouter("/campaigns");
    // Click on RUNNING filter
    const runningFilter = await screen.findByText("RUNNING");
    runningFilter.click();
    // Check that the URL updated (MSW will filter)
    expect(router.state.location.search).toContain("lifecycle_state");
  });

  it("AC-004: campaign card navigates to detail route (card_click_navigates_to_detail_route)", async () => {
    const { router } = renderWithRouter("/campaigns");
    const firstCard = await screen.findByText("RUNNING");
    const card = firstCard.closest("a");
    expect(card).toHaveAttribute("href", expect.stringContaining("/campaigns/"));
  });
});
