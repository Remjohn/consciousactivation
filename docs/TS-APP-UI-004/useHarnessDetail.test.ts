import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { createElement, type ReactNode } from "react";
import { renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useHarnessDetail } from "./useHarnessDetail";

function wrapper({ children }: { children: ReactNode }) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return createElement(QueryClientProvider, { client: queryClient }, children);
}

const DETAIL = {
  definition_id: "def-1",
  definition_hash: "sha256:aaa",
  manifest_id: "generic_text_summary",
  manifest_version: "1.0.0",
  task_id: "generic_text_summary_v1",
  mode: "generic",
  category_id: null,
  category_name: null,
  classification: [],
  capability_requirements: [],
  production_ready: false,
  certified: false,
  package_file: "def-1.zip",
  package_hash: "sha256:bbb",
  added_at: "2026-07-01T00:00:00Z",
  goal: "Summarize a body of text.",
  success_condition: "Output is under 280 characters.",
  atomic_boundary: "Single-pass summarization only.",
  input_contract: {},
  output_contract: {},
  minimum_complete_context: [],
  acceptance_tests: [],
  authority_chain: [],
  provenance_refs: [],
  execution_plan: [],
  category_binding: { applicability: "NOT_APPLICABLE", basis: null, category_id: null },
  activative_intelligence: null,
  lineage: [],
  compiler_id: "cmf-builder",
  compiler_version: "1.0.0",
  schema_id: "atomic_harness_definition",
  schema_version: "1.0.0",
};

describe("useHarnessDetail", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("succeeds with the full HarnessDetail shape", async () => {
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => DETAIL,
    });
    const { result } = renderHook(() => useHarnessDetail("def-1"), { wrapper });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toEqual(DETAIL);
  });

  it("errors with status 404 for an unknown definitionId", async () => {
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: false,
      status: 404,
      json: async () => ({
        error_code: "NOT_FOUND",
        message: "No Harness with id 'nope' exists.",
        timestamp: "2026-07-01T00:00:00Z",
      }),
    });
    const { result } = renderHook(() => useHarnessDetail("nope"), { wrapper });
    await waitFor(() => expect(result.current.isError).toBe(true));
    expect(result.current.error?.status).toBe(404);
  });

  it("errors with a non-404 status for other failures", async () => {
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: false,
      status: 500,
      json: async () => ({
        error_code: "INTERNAL_ERROR",
        message: "unexpected failure",
        timestamp: "2026-07-01T00:00:00Z",
      }),
    });
    const { result } = renderHook(() => useHarnessDetail("def-1"), { wrapper });
    await waitFor(() => expect(result.current.isError).toBe(true));
    expect(result.current.error?.status).toBe(500);
  });
});
