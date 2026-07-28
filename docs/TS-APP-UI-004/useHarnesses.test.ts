import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { createElement, type ReactNode } from "react";
import { renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useHarnesses } from "./useHarnesses";

function wrapper({ children }: { children: ReactNode }) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return createElement(QueryClientProvider, { client: queryClient }, children);
}

const SUMMARY = {
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
};

describe("useHarnesses", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("is loading before the first response resolves", () => {
    (fetch as ReturnType<typeof vi.fn>).mockImplementation(() => new Promise(() => {}));
    const { result } = renderHook(() => useHarnesses(), { wrapper });
    expect(result.current.isLoading).toBe(true);
  });

  it("succeeds with an empty array for an empty library", async () => {
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => [],
    });
    const { result } = renderHook(() => useHarnesses(), { wrapper });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toEqual([]);
  });

  it("succeeds with the full array for a non-empty library", async () => {
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => [SUMMARY],
    });
    const { result } = renderHook(() => useHarnesses(), { wrapper });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toEqual([SUMMARY]);
  });

  it("errors with LIBRARY_UNREADABLE on a 5xx response", async () => {
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: false,
      status: 500,
      json: async () => ({
        error_code: "LIBRARY_UNREADABLE",
        message: "Harness library directory is unreadable",
        timestamp: "2026-07-01T00:00:00Z",
      }),
    });
    const { result } = renderHook(() => useHarnesses(), { wrapper });
    await waitFor(() => expect(result.current.isError).toBe(true));
    expect(result.current.error?.status).toBe(500);
    expect(result.current.error?.errorCode).toBe("LIBRARY_UNREADABLE");
  });

  it("errors with a null status when the gateway is unreachable", async () => {
    (fetch as ReturnType<typeof vi.fn>).mockRejectedValue(new TypeError("Failed to fetch"));
    const { result } = renderHook(() => useHarnesses(), { wrapper });
    await waitFor(() => expect(result.current.isError).toBe(true));
    expect(result.current.error?.status).toBeNull();
  });
});
