import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { fireEvent, waitFor } from "@testing-library/react";
import { renderWithRouter } from "../../test/renderWithRouter";

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

describe("HarnessCard (rendered via /harnesses)", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({ ok: true, status: 200, json: async () => [HARNESS] }),
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("renders task_id, mode badge, category badge, certification badges, and a truncated capability list", async () => {
    const { findByText } = renderWithRouter("/harnesses");
    expect(await findByText("generic_text_summary_v1")).toBeInTheDocument();
    expect(await findByText("Generic")).toBeInTheDocument();
    expect(await findByText("Category-neutral")).toBeInTheDocument();
    expect(await findByText(/Production-ready: No/)).toBeInTheDocument();
    expect(await findByText(/Certified: No/)).toBeInTheDocument();
    expect(await findByText("+1 more")).toBeInTheDocument();
  });

  it("does not render an EligibilityBadge when no sourceCategory is in the URL", async () => {
    const { findByText, queryByText } = renderWithRouter("/harnesses");
    await findByText("generic_text_summary_v1");
    expect(queryByText("Eligible")).not.toBeInTheDocument();
    expect(queryByText("Not eligible")).not.toBeInTheDocument();
  });

  it("preserves sourceCategory when navigating to the detail route (AC-006)", async () => {
    const { findByText, router } = renderWithRouter("/harnesses?sourceCategory=carousels");
    const cardTitle = await findByText("generic_text_summary_v1");
    fireEvent.click(cardTitle);
    await waitFor(() => expect(router.state.location.pathname).toBe("/harnesses/def-1"));
    expect(router.state.location.search).toEqual({ sourceCategory: "carousels" });
  });
});
