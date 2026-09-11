import { Link } from "@tanstack/react-router";

const NAV_ITEMS = [
  { to: "/workspace", label: "Workspace" },
  { to: "/interviews/compose", label: "Interview Composer" },
  { to: "/campaigns", label: "Campaigns" },
  { to: "/campaigns/new", label: "New Campaign" },
  { to: "/harnesses", label: "Harnesses" },
] as const;

const linkClassName =
  "rounded-md px-3 py-2 text-sm text-muted-foreground hover:bg-surface-elevated hover:text-foreground";
const activeLinkClassName =
  "rounded-md px-3 py-2 text-sm bg-surface-elevated text-accent font-medium";

export function Sidebar() {
  return (
    <nav className="flex w-56 flex-col gap-1 border-r border-border bg-surface p-4">
      <p className="mb-3 px-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
        Conscious Activations
      </p>
      {NAV_ITEMS.map((item) => (
        <Link
          key={item.to}
          to={item.to}
          className={linkClassName}
          activeProps={{ className: activeLinkClassName }}
        >
          {item.label}
        </Link>
      ))}
      {/* Control Tower (campaigns/$campaignId) has no static destination of its own —
          it's reached from a row in the Campaign List (TS-APP-UI-002). This demo link
          keeps the sixth Stage 4 page reachable from the sidebar for this scaffold. */}
      <Link
        to="/campaigns/$campaignId"
        params={{ campaignId: "demo-campaign" }}
        className={linkClassName}
        activeProps={{ className: activeLinkClassName }}
      >
        Control Tower (demo)
      </Link>
    </nav>
  );
}
