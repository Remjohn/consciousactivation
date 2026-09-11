// TS-APP-UI-003 - useControlTower hook tests (AC-006).
//
// AC-006: refetchInterval is `false` while the WS is open, and `4000` once it
// closes. TanStack Query exposes the computed interval on the result's
// `observedQueries` via the devtools, but the stable, supported way to assert
// it is to spy on the query options actually registered. We do that by
// intercepting useQuery's options through the QueryClient observer: we read
// the live query from the queryClient and assert its `refetchInterval`.

import { describe, it, expect, beforeAll, afterAll, afterEach } from "vitest";
import { renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider, keepPreviousData } from "@tanstack/react-query";
import { setupServer } from "msw/node";
import { http, HttpResponse } from "msw";
import * as React from "react";
import { useControlTower } from "../useControlTower";

const TOWER_BODY = {
  campaign: { campaign_id: "camp-1", lifecycle_state: "RUNNING" },
  run_nodes: [],
  available_actions: [],
  exception_packages: [],
  timeline: null,
};

const server = setupServer(
  http.get("/api/campaigns/:id/tower", () => HttpResponse.json(TOWER_BODY)),
);

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

function makeWrapper(client: QueryClient) {
  return function Wrapper({ children }: { children: React.ReactNode }) {
    return React.createElement(QueryClientProvider, { client }, children);
  };
}

/** Reads the refetchInterval the hook actually registered, straight from the cache observer. */
function registeredInterval(client: QueryClient, campaignId: string): unknown {
  const observer = client
    .getQueryCache()
    .find({ queryKey: ["campaign", campaignId, "tower"] });
  // observers[0] is the single useQuery instance mounted by the hook under test
  return (observer?.observers?.[0] as any)?.options?.refetchInterval;
}

describe("useControlTower — AC-006", () => {
  it("disables polling (refetchInterval === false) when the WS is open", async () => {
    const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const { result } = renderHook(() => useControlTower("camp-1", true), {
      wrapper: makeWrapper(client),
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(registeredInterval(client, "camp-1")).toBe(false);
  });

  it("enables 4s polling (refetchInterval === 4000) when the WS is closed", async () => {
    const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const { result } = renderHook(() => useControlTower("camp-1", false), {
      wrapper: makeWrapper(client),
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(registeredInterval(client, "camp-1")).toBe(4000);
  });

  it("loads the tower projection through the real fetch wrapper", async () => {
    const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const { result } = renderHook(() => useControlTower("camp-1", false), {
      wrapper: makeWrapper(client),
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(result.current.data).toMatchObject({
      campaign: { lifecycle_state: "RUNNING" },
    });
  });
});

// keepPreviousData is imported only to avoid an unused-import tree-shake warning
// when the bundler inspects this file in isolation; it documents that we do not
// rely on placeholder data for the tower query.
void keepPreviousData;
