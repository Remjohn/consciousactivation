import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import {
  createRootRoute,
  createRoute,
  createRouter,
  createMemoryHistory,
  RouterProvider,
  Outlet,
  CatchBoundary,
  useLocation,
} from "@tanstack/react-router";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AppShell } from "./AppShell";
import { RootErrorBoundary } from "./RootErrorBoundary";

function ThrowingPage(): never {
  throw new Error("deliberate test failure");
}

// Mirrors the real __root.tsx shape exactly: AppShell wraps a CatchBoundary
// around Outlet, so a child-route error unmounts only the routed content,
// not AppShell's Sidebar/TopBar. This is AC-009's scenario.
function RootComponent() {
  const pathname = useLocation({ select: (location) => location.pathname });
  return (
    <AppShell>
      <CatchBoundary getResetKey={() => pathname} errorComponent={RootErrorBoundary}>
        <Outlet />
      </CatchBoundary>
    </AppShell>
  );
}

describe("RootErrorBoundary", () => {
  it("catches a render error without unmounting the shell", async () => {
    const rootRoute = createRootRoute({ component: RootComponent });

    const throwingRoute = createRoute({
      getParentRoute: () => rootRoute,
      path: "/throws",
      component: ThrowingPage,
    });

    const routeTree = rootRoute.addChildren([throwingRoute]);
    const router = createRouter({
      routeTree,
      history: createMemoryHistory({ initialEntries: ["/throws"] }),
    });
    const queryClient = new QueryClient({
      defaultOptions: { queries: { retry: false } },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
      </QueryClientProvider>,
    );

    // Sidebar (part of AppShell, outside the CatchBoundary) stays mounted.
    expect(await screen.findByText("Conscious Activations")).toBeInTheDocument();
    // The error message replaces only the page body — no white-screen.
    expect(await screen.findByText("Something went wrong")).toBeInTheDocument();
    expect(screen.getByText(/deliberate test failure/)).toBeInTheDocument();
  });
});
