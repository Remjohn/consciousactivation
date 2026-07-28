import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { waitFor, within } from "@testing-library/react";
import { renderWithRouter } from "../../test/renderWithRouter";
import { createUrlRouter } from "../../test/mockFetch";

function makeHarness(overrides: Record<string, unknown>) {
  return {
    definition_id: `def-${overrides.task_id}`,
    definition_hash: "sha256:aaa",
    manifest_id: "some_manifest",
    manifest_version: "1.0.0",
    task_id: "some_task_v1",
    mode: "generic",
    category_id: null,
    category_name: null,
    classification: [],
    capability_requirements: [],
    production_ready: false,
    certified: false,
    package_file: "pkg.zip",
    package_hash: "sha256:bbb",
    added_at: "2026-07-01T00:00:00Z",
    ...overrides,
  };
}

const ELIGIBLE_HARNESS = makeHarness({
  task_id: "carousel_builder_v1",
  mode: "activative",
  category_id: "carousels",
  category_name: "Carousels",
});
const INELIGIBLE_HARNESS = makeHarness({
  task_id: "supervisual_builder_v1",
  mode: "activative",
  category_id: "supervisuals",
  category_name: "Supervisuals",
});
const NEUTRAL_HARNESS = makeHarness({ task_id: "generic_text_summary_v1" });

// renderWithRouter mounts the full AppShell, whose TopBar calls useHealth() → an extra
// fetch to /api/health on every render. Registering a health handler on the URL router
// (returning a valid HealthResponse) means that fetch resolves cleanly instead of
// stealing a mockResolvedValueOnce entry that a route test expected for its own fetch.
const HEALTH_OK = {
  status: "ok",
  timestamp: "2026-07-01T00:00:00Z",
  gateway_version: "0.1.0",
  ca_data_root: "/state",
  services: {},
};

describe("harnesses/index route", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("empty library shows the empty state, not the error state", async () => {
    vi.stubGlobal(
      "fetch",
      createUrlRouter({
        "/api/health": { status: 200, body: HEALTH_OK },
        "/api/harnesses": { status: 200, body: [] },
      }),
    );
    const { findByText, queryByText } = renderWithRouter("/harnesses");
    expect(await findByText(/no harnesses in this workspace/i)).toBeInTheDocument();
    expect(queryByText(/could not be read/i)).not.toBeInTheDocument();
  });

  it("AC-001: renders a HarnessCard for every item the response returned", async () => {
    vi.stubGlobal(
      "fetch",
      createUrlRouter({
        "/api/health": { status: 200, body: HEALTH_OK },
        "/api/harnesses": {
          status: 200,
          body: [ELIGIBLE_HARNESS, INELIGIBLE_HARNESS, NEUTRAL_HARNESS],
        },
      }),
    );
    const { findByText } = renderWithRouter("/harnesses");
    expect(await findByText("carousel_builder_v1")).toBeInTheDocument();
    expect(await findByText("supervisual_builder_v1")).toBeInTheDocument();
    expect(await findByText("generic_text_summary_v1")).toBeInTheDocument();
  });

  it("AC-003: a 5xx LIBRARY_UNREADABLE response renders wording distinct from empty and unreachable", async () => {
    vi.stubGlobal(
      "fetch",
      createUrlRouter({
        "/api/health": { status: 200, body: HEALTH_OK },
        "/api/harnesses": {
          status: 500,
          body: {
            error_code: "LIBRARY_UNREADABLE",
            message: "Harness library directory is unreadable: permission denied",
            timestamp: "2026-07-01T00:00:00Z",
          },
        },
      }),
    );
    const { findByText, queryByText } = renderWithRouter("/harnesses");
    expect(await findByText(/could not be read/i)).toBeInTheDocument();
    expect(queryByText(/no harnesses in this workspace/i)).not.toBeInTheDocument();
    expect(queryByText(/gateway unreachable/i)).not.toBeInTheDocument();
  });

  it("AC-003: an unreachable gateway renders wording distinct from empty and 5xx", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockRejectedValue(new TypeError("Failed to fetch")),
    );
    const { findByText, queryByText } = renderWithRouter("/harnesses");
    expect(await findByText(/gateway unreachable/i)).toBeInTheDocument();
    expect(queryByText(/no harnesses in this workspace/i)).not.toBeInTheDocument();
    expect(queryByText(/^the harness library could not be read$/i)).not.toBeInTheDocument();
  });

  it("AC-004: direct navigation to a filtered URL reproduces the filtered view", async () => {
    vi.stubGlobal(
      "fetch",
      createUrlRouter({
        "/api/health": { status: 200, body: HEALTH_OK },
        "/api/harnesses": {
          status: 200,
          body: [ELIGIBLE_HARNESS, INELIGIBLE_HARNESS, NEUTRAL_HARNESS],
        },
      }),
    );
    const { findByText, queryByText } = renderWithRouter("/harnesses?category=carousels");
    expect(await findByText("carousel_builder_v1")).toBeInTheDocument();
    await waitFor(() => expect(queryByText("supervisual_builder_v1")).not.toBeInTheDocument());
    await waitFor(() => expect(queryByText("generic_text_summary_v1")).not.toBeInTheDocument());
  });

  it("AC-009: every card shows the correct client-computed EligibilityBadge with zero eligibility network calls", async () => {
    const fetchRouter = createUrlRouter({
      "/api/health": { status: 200, body: HEALTH_OK },
      "/api/harnesses": {
        status: 200,
        body: [ELIGIBLE_HARNESS, INELIGIBLE_HARNESS, NEUTRAL_HARNESS],
      },
    });
    vi.stubGlobal("fetch", fetchRouter);

    const { findByTestId } = renderWithRouter("/harnesses?sourceCategory=carousels");
    // Use data-testid on each harness card + eligibility badge to avoid collisions with
    // CategoryBadge (which also says "Category-neutral" for generic-mode harnesses) and
    // HarnessFilterBar <option> elements.
    const eligibleCard = await findByTestId("harness-card-def-carousel_builder_v1");
    const ineligibleCard = await findByTestId("harness-card-def-supervisual_builder_v1");
    const neutralCard = await findByTestId("harness-card-def-generic_text_summary_v1");

    expect(within(eligibleCard).getByTestId("eligibility-badge-ELIGIBLE")).toBeInTheDocument();
    expect(within(ineligibleCard).getByTestId("eligibility-badge-INELIGIBLE")).toBeInTheDocument();
    expect(within(neutralCard).getByTestId("eligibility-badge-NOT_APPLICABLE")).toBeInTheDocument();

    const eligibilityCalls = fetchRouter.mock.calls.filter((call) =>
      String(call[0]).includes("/eligibility"),
    );
    expect(eligibilityCalls).toHaveLength(0);
  });
});
