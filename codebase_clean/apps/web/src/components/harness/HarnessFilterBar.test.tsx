import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { fireEvent, waitFor } from "@testing-library/react";
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

const CAROUSEL = makeHarness({
  task_id: "carousel_builder_v1",
  manifest_id: "carousel_builder",
  mode: "activative",
  category_id: "carousels",
  category_name: "Carousels",
});
const GENERIC_SUMMARY = makeHarness({
  task_id: "generic_text_summary_v1",
  manifest_id: "generic_text_summary",
});
const MANIFEST_ONLY_MATCH = makeHarness({
  task_id: "totally_different_task_v2",
  manifest_id: "special_needle_manifest",
});

const HEALTH_OK = {
  status: "ok",
  timestamp: "2026-07-01T00:00:00Z",
  gateway_version: "0.1.0",
  ca_data_root: "/state",
  services: {},
};

function harnessFetch() {
  return createUrlRouter({
    "/api/health": { status: 200, body: HEALTH_OK },
    "/api/harnesses": {
      status: 200,
      body: [CAROUSEL, GENERIC_SUMMARY, MANIFEST_ONLY_MATCH],
    },
  });
}

describe("HarnessFilterBar (rendered via /harnesses)", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", harnessFetch());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("narrows the grid and updates the URL when the category filter changes (AC-004)", async () => {
    const { findByText, findByLabelText, queryByText, router } = renderWithRouter("/harnesses");
    await findByText("carousel_builder_v1");

    fireEvent.change(await findByLabelText("Filter by category"), { target: { value: "carousels" } });

    await waitFor(() => expect(queryByText("generic_text_summary_v1")).not.toBeInTheDocument());
    expect(await findByText("carousel_builder_v1")).toBeInTheDocument();
    expect(router.state.location.search).toEqual({ category: "carousels" });
  });

  it("reproduces the same filtered view on direct navigation to the filtered URL", async () => {
    const { findByText, queryByText } = renderWithRouter("/harnesses?category=carousels");
    expect(await findByText("carousel_builder_v1")).toBeInTheDocument();
    await waitFor(() => expect(queryByText("generic_text_summary_v1")).not.toBeInTheDocument());
  });

  it("narrows the grid via the mode filter", async () => {
    const { findByText, findByLabelText, queryByText } = renderWithRouter("/harnesses");
    await findByText("carousel_builder_v1");

    fireEvent.change(await findByLabelText("Filter by mode"), { target: { value: "activative" } });

    await waitFor(() => expect(queryByText("generic_text_summary_v1")).not.toBeInTheDocument());
    expect(await findByText("carousel_builder_v1")).toBeInTheDocument();
  });

  it("matches on task_id, case-insensitively, via the search field", async () => {
    const { findByText, findByLabelText, queryByText } = renderWithRouter("/harnesses");
    await findByText("carousel_builder_v1");

    fireEvent.change(await findByLabelText("Search by task or manifest id"), {
      target: { value: "SUMMARY" },
    });
    await new Promise((resolve) => setTimeout(resolve, 350));

    await waitFor(() => expect(queryByText("carousel_builder_v1")).not.toBeInTheDocument());
    expect(await findByText("generic_text_summary_v1")).toBeInTheDocument();
  });

  it("matches on manifest_id when task_id does not contain the needle (AC-005)", async () => {
    const { findByText, findByLabelText, queryByText } = renderWithRouter("/harnesses");
    await findByText("carousel_builder_v1");

    fireEvent.change(await findByLabelText("Search by task or manifest id"), {
      target: { value: "needle" },
    });
    await new Promise((resolve) => setTimeout(resolve, 350));

    await waitFor(() => expect(queryByText("carousel_builder_v1")).not.toBeInTheDocument());
    expect(await findByText("totally_different_task_v2")).toBeInTheDocument();
  });
});
