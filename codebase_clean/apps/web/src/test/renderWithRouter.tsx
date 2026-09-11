import { render } from "@testing-library/react";
import { RouterProvider, createRouter, createMemoryHistory } from "@tanstack/react-router";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { routeTree } from "../routeTree.gen";
import { DevOperatorProvider } from "../auth/DevOperatorContext";
import { WorkspaceProvider } from "../context/WorkspaceContext";

/**
 * Mounts the real route tree behind a memory-history RouterProvider, starting at
 * `initialUrl` (which may include a search-param query string). Lets route-level tests
 * assert on filtered/linked/navigated behavior without a real browser. Shared across
 * this spec's own route tests; later UI specs (e.g. TS-APP-UI-002's CampaignNew) can
 * reuse this instead of re-inventing one (TS-APP-UI-004 §7 Stage 10).
 */
export function renderWithRouter(initialUrl: string) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  const history = createMemoryHistory({ initialEntries: [initialUrl] });
  const router = createRouter({ routeTree, history });

  const utils = render(
    <QueryClientProvider client={queryClient}>
      <DevOperatorProvider>
        <WorkspaceProvider>
          <RouterProvider router={router} />
        </WorkspaceProvider>
      </DevOperatorProvider>
    </QueryClientProvider>,
  );

  return { ...utils, router, queryClient };
}
