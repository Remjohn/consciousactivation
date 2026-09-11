/**
 * Header dropdown switcher for switching active workspace context.
 * Governed by SPEC-TWC-UI-001 §2 and FR-APP-002.
 */

import { useWorkspace } from "../../context/WorkspaceContext";

export interface WorkspaceSelectorProps {
  readonly onOpenCreate?: () => void;
  readonly className?: string;
}

export function WorkspaceSelector({ onOpenCreate, className = "" }: WorkspaceSelectorProps) {
  const { activeWorkspaceId, workspaces, selectWorkspace, isLoading } = useWorkspace();

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <label htmlFor="workspace-selector" className="text-xs font-medium text-muted-foreground">
        Workspace:
      </label>
      <select
        id="workspace-selector"
        data-testid="workspace-selector"
        value={activeWorkspaceId ?? ""}
        disabled={isLoading || workspaces.length === 0}
        onChange={(e) => {
          if (e.target.value === "__NEW__") {
            if (onOpenCreate) onOpenCreate();
          } else if (e.target.value) {
            selectWorkspace(e.target.value);
          }
        }}
        className="rounded-md border border-border bg-surface px-2.5 py-1 text-xs font-medium text-foreground focus:border-accent focus:outline-none"
      >
        {workspaces.map((ws) => (
          <option key={ws.workspace_id} value={ws.workspace_id}>
            {ws.display_name} {ws.status === "SUSPENDED" ? "(SUSPENDED)" : ""}
          </option>
        ))}
        {onOpenCreate && (
          <option value="__NEW__">+ New Workspace…</option>
        )}
      </select>
    </div>
  );
}
