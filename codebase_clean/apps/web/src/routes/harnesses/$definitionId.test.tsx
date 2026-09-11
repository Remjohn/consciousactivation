import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { waitFor } from "@testing-library/react";
import { renderWithRouter } from "../../test/renderWithRouter";
import { createUrlRouter } from "../../test/mockFetch";

const GENERIC_DETAIL = {
  definition_id: "def-1",
  definition_hash: "sha256:aaa",
  manifest_id: "generic_text_summary",
  manifest_version: "1.0.0",
  task_id: "generic_text_summary_v1",
  mode: "generic",
  category_id: null,
  category_name: null,
  classification: [],
  capability_requirements: ["text_understanding"],
  production_ready: false,
  certified: false,
  package_file: "def-1.zip",
  package_hash: "sha256:bbb",
  added_at: "2026-07-01T00:00:00Z",
  goal: "Summarize a body of text into a concise abstract.",
  success_condition: "Output is under 280 characters and retains key claims.",
  atomic_boundary: "Single-pass summarization only; no iterative refinement.",
  input_contract: { type: "object", properties: { body: { type: "string" } } },
  output_contract: { type: "object", properties: { summary: { type: "string" } } },
  minimum_complete_context: ["source_material"],
  acceptance_tests: ["test_summary_length", "test_key_claims_retained"],
  authority_chain: [],
  provenance_refs: [],
  execution_plan: [],
  category_binding: { applicability: "NOT_APPLICABLE", basis: "Harness is category-neutral (generic mode).", category_id: null },
  activative_intelligence: null,
  lineage: ["lineage-ref-1"],
  compiler_id: "cmf-builder",
  compiler_version: "1.0.0",
  schema_id: "atomic_harness_definition",
  schema_version: "1.0.0",
};

const ACTIVATIVE_DETAIL = {
  ...GENERIC_DETAIL,
  definition_id: "def-carousel",
  task_id: "carousel_builder_v1",
  manifest_id: "carousel_builder",
  mode: "activative",
  category_id: "carousels",
  category_name: "Carousels",
  category_binding: {
    applicability: "REQUIRED",
    harness_id: "def-carousel",
    harness_version: "1.0.0",
    category_id: "carousels",
    category_name: "Carousels",
    category_registry_version: "2.1.0",
    category_registry_hash: "sha256:reg",
    constitutional_authority_ref: "CA-REF-001",
    runtime_law: "RL-001",
    harness_development_law: "HDL-001",
    semantic_lineage_refs: ["slr-1"],
    wrong_reading_locks: ["wrl-1"],
    not_applicable_basis: null,
    certification_state: "pending",
    production_ready: false,
    certified: false,
    binding_hash: "sha256:bind",
  },
};

const HEALTH_OK = {
  status: "ok",
  timestamp: "2026-07-01T00:00:00Z",
  gateway_version: "0.1.0",
  ca_data_root: "/state",
  services: {},
};

const ELIGIBLE_RESPONSE = {
  definition_id: "def-carousel",
  harness_category: "carousels",
  source_category: "carousels",
  status: "ELIGIBLE",
  reason: null,
};

describe("harnesses/$definitionId route", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("AC-007: renders the full HarnessDetail contract", async () => {
    vi.stubGlobal(
      "fetch",
      createUrlRouter({
        "/api/health": { status: 200, body: HEALTH_OK },
        "/api/harnesses/def-1": { status: 200, body: GENERIC_DETAIL },
      }),
    );
    const { findByText, getByText } = renderWithRouter("/harnesses/def-1");

    expect(await findByText("generic_text_summary_v1")).toBeInTheDocument();
    expect(getByText("Generic")).toBeInTheDocument();
    expect(getByText("Category-neutral")).toBeInTheDocument();
    expect(getByText(/Production-ready: No/)).toBeInTheDocument();
    expect(getByText(/Certified: No/)).toBeInTheDocument();

    expect(getByText("What this Harness does")).toBeInTheDocument();
    expect(getByText("Summarize a body of text into a concise abstract.")).toBeInTheDocument();
    expect(getByText(/Success condition:.*under 280 characters/)).toBeInTheDocument();
    expect(getByText(/Atomic boundary:.*Single-pass/)).toBeInTheDocument();

    expect(getByText("Contracts")).toBeInTheDocument();
    expect(getByText("Input contract")).toBeInTheDocument();
    expect(getByText("Output contract")).toBeInTheDocument();

    expect(getByText("Governance record")).toBeInTheDocument();
    expect(getByText(/category-neutral.*generic mode/i)).toBeInTheDocument();
  });

  it("AC-008: unknown definitionId shows a 404 panel, not a crash", async () => {
    vi.stubGlobal(
      "fetch",
      createUrlRouter({
        "/api/health": { status: 200, body: HEALTH_OK },
        "/api/harnesses/nope": {
          status: 404,
          body: {
            error_code: "NOT_FOUND",
            message: "No Harness with id 'nope' exists.",
            timestamp: "2026-07-01T00:00:00Z",
          },
        },
      }),
    );
    const { findByText, queryByText } = renderWithRouter("/harnesses/nope");

    expect(await findByText("Harness not found")).toBeInTheDocument();
    expect(await findByText(/Back to library/i)).toBeInTheDocument();
    expect(queryByText("What this Harness does")).not.toBeInTheDocument();
  });

  it("AC-010 (a): fires eligibility call when sourceCategory is present on an activative harness", async () => {
    const fetchRouter = createUrlRouter({
      "/api/health": { status: 200, body: HEALTH_OK },
      "/api/harnesses/def-carousel": { status: 200, body: ACTIVATIVE_DETAIL },
      "/api/harnesses/def-carousel/eligibility": { status: 200, body: ELIGIBLE_RESPONSE },
    });
    vi.stubGlobal("fetch", fetchRouter);

    const { findByText } = renderWithRouter("/harnesses/def-carousel?sourceCategory=carousels");
    expect(await findByText("Eligible")).toBeInTheDocument();

    const eligibilityCalls = fetchRouter.mock.calls.filter((call) =>
      String(call[0]).includes("/eligibility"),
    );
    expect(eligibilityCalls).toHaveLength(1);
  });

  it("AC-010 (b): does not fire eligibility call when sourceCategory is present on a generic harness", async () => {
    const fetchRouter = createUrlRouter({
      "/api/health": { status: 200, body: HEALTH_OK },
      "/api/harnesses/def-1": { status: 200, body: GENERIC_DETAIL },
    });
    vi.stubGlobal("fetch", fetchRouter);

    const { findByTestId } = renderWithRouter("/harnesses/def-1?sourceCategory=carousels");
    // Generic-mode detail: NOT_APPLICABLE rendered client-side, no eligibility fetch.
    // Use data-testid to distinguish from CategoryBadge which also says "Category-neutral".
    expect(await findByTestId("eligibility-badge-NOT_APPLICABLE")).toBeInTheDocument();

    const eligibilityCalls = fetchRouter.mock.calls.filter((call) =>
      String(call[0]).includes("/eligibility"),
    );
    expect(eligibilityCalls).toHaveLength(0);
  });

  it("AC-010 (c): no eligibility UI and no eligibility call when no sourceCategory is present", async () => {
    const fetchRouter = createUrlRouter({
      "/api/health": { status: 200, body: HEALTH_OK },
      "/api/harnesses/def-1": { status: 200, body: GENERIC_DETAIL },
    });
    vi.stubGlobal("fetch", fetchRouter);

    const { findByText, queryByTestId } = renderWithRouter("/harnesses/def-1");

    expect(await findByText("generic_text_summary_v1")).toBeInTheDocument();
    expect(queryByTestId("eligibility-badge-ELIGIBLE")).not.toBeInTheDocument();
    expect(queryByTestId("eligibility-badge-INELIGIBLE")).not.toBeInTheDocument();
    expect(queryByTestId("eligibility-badge-NOT_APPLICABLE")).not.toBeInTheDocument();

    const eligibilityCalls = fetchRouter.mock.calls.filter((call) =>
      String(call[0]).includes("/eligibility"),
    );
    expect(eligibilityCalls).toHaveLength(0);
  });
});
