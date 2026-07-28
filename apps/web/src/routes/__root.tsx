import { createRootRoute, Outlet, CatchBoundary, useLocation } from "@tanstack/react-router";
import { AppShell } from "../components/layout/AppShell";
import { RootErrorBoundary } from "../components/layout/RootErrorBoundary";

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

export const Route = createRootRoute({
  component: RootComponent,
  // Ultimate fallback if AppShell itself throws (outside the CatchBoundary above).
  errorComponent: RootErrorBoundary,
  notFoundComponent: () => (
    <div className="p-8 text-muted-foreground">
      <p className="text-lg font-semibold text-foreground">Not found</p>
      <p>No page is mounted at this path yet.</p>
    </div>
  ),
});
