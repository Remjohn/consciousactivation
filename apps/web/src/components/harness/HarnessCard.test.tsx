import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { fireEvent, waitFor, within } from "@testing-library/react";
import { renderWithRouter } from "../../test/renderWithRouter";
import { createUrlRouter } from "../../test/mockFetch";

const HARNESS = {
  definition_id: "def-1",
  definition_hash: "sha256:aaa",
  manifest_id: "generic_text_summary",
  manifest_version: "1.0.0",
  task_id: "generic_text_summary_v1",
  mode: "generic",
  category_id: null,
  category_name: null,
  classification: [],
  capability_requirements: ["cap_a", "cap_b", "cap_c", "cap_d"],
  production_ready: false,
  certified: false,
  package_file: "def-1.zip",
  package_hash: "sha256:bbb",
  added_at: "2026-07-01T00:00:00Z",
};

// renderWithRouter mounts the full AppShell, whose TopBar calls useHealth() → an extra
// fetch to /api/health. Register a health handler so it resolves cleanly and doesn't
// steal the route's own mock entry (see TS-APP-UI-004 test harness notes).
const HEALTH_OK = {
  status: "ok",
  timestamp: "2026-07-01T00:00:00Z",
  gateway_version: "0.1.0",
  ca_data_root: "/state",
  services: {},
};

function harnessFetch(body: unknown) {
  return createUrlRouter({
    "/api/health": { status: 200, body: HEALTH_OK },
    "/api/harnesses": { status: 200, body },
  });
}

describe("HarnessCard (rendered via /harnesses)", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", harnessFetch([HARNESS]));
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("renders task_id, mode badge, category badge, certification badges, and a truncated capability list", async () => {
    const { findByTestId } = renderWithRouter("/harnesses");
    // Scope to the card (data-testid on HarnessCard's root <Link>) so badge-text
    // assertions don't also match the HarnessFilterBar <option> labels.
    const card = await findByTestId("harness-card-def-1");
    const cardScope = within(card);
    expect(cardScope.getByText("generic_text_summary_v1")).toBeInTheDocument();
    expect(cardScope.getByText("Generic")).toBeInTheDocument();
    expect(cardScope.getByText("Category-neutral")).toBeInTheDocument();
    expect(cardScope.getByText(/Production-ready: No/)).toBeInTheDocument();
    expect(cardScope.getByText(/Certified: No/)).toBeInTheDocument();
    expect(cardScope.getByText("+1 more")).toBeInTheDocument();
  });

  it("does not render an EligibilityBadge when no sourceCategory is in the URL", async () => {
    const { findByTestId } = renderWithRouter("/harnesses");
    const card = await findByTestId("harness-card-def-1");
    expect(within(card).queryByText("Eligible")).not.toBeInTheDocument();
    expect(within(card).queryByText("Not eligible")).not.toBeInTheDocument();
  });

  it("preserves sourceCategory when navigating to the detail route (AC-006)", async () => {
    const { findByTestId, router } = renderWithRouter("/harnesses?sourceCategory=carousels");
    await findByTestId("harness-card-def-1");
    fireEvent.click(await within(await findByTestId("harness-card-def-1")).getByText("generic_text_summary_v1"));
    await waitFor(() => expect(router.state.location.pathname).toBe("/harnesses/def-1"));
    expect(router.state.location.search).toEqual({ sourceCategory: "carousels" });
  });
});
