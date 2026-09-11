import { useHealth } from "../../hooks/useHealth";
import { StatusPill } from "../ui/StatusPill";
import { useOperator } from "../../auth/DevOperatorContext";
import { WorkspaceSelector } from "../workspace/WorkspaceSelector";

export function TopBar() {
  const { data, isError, isLoading } = useHealth();
  const operator = useOperator();

  const tone = isError ? "danger" : isLoading ? "muted" : data?.status === "ok" ? "success" : "danger";
  const label = isError
    ? "API unreachable"
    : isLoading
      ? "Checking gateway…"
      : data?.status === "ok"
        ? "All systems operational"
        : "Degraded";

  return (
    <header className="flex items-center justify-between border-b border-border bg-surface px-6 py-3">
      <div className="flex items-center gap-4">
        <StatusPill tone={tone} label={label} />
        <WorkspaceSelector />
      </div>
      <span className="rounded-full border border-danger px-2 py-0.5 text-xs text-danger">
        DEV MODE — NOT AUTHENTICATED ({operator.actor_id})
      </span>
    </header>
  );
}
