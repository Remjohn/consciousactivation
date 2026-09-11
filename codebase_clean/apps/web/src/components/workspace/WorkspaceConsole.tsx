/**
 * Workspace Management Console Main View.
 * Governed by SPEC-TWC-UI-001, FR-APP-001..003, MC-CAE-WS-001, and TS-APP-API-004 §5.
 */

import { useEffect, useMemo, useState } from "react";
import { useWorkspace } from "../../context/WorkspaceContext";
import { Button } from "../ui/Button";
import { WorkspaceDetail } from "./WorkspaceDetail";
import { WorkspaceCreateModal } from "./WorkspaceCreateModal";
import { ErrorEnvelopeAlert } from "./ErrorEnvelopeAlert";
import { Badge } from "../ui/Badge";
import type { OperatorGrant, WorkspaceMembership } from "../../api/tenancy";

export function WorkspaceConsole() {
  const {
    activeWorkspace,
    workspaces,
    selectWorkspace,
    isLoading,
    error,
    clearError,
  } = useWorkspace();

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

  // Local state for additional memberships & grants scoped to the active workspace
  const [extraMemberships, setExtraMemberships] = useState<WorkspaceMembership[]>([]);
  const [grants, setGrants] = useState<OperatorGrant[]>([]);

  // Reset workspace scoped extra members and grants on workspace switch
  useEffect(() => {
    setExtraMemberships([]);
    setGrants([]);
  }, [activeWorkspace?.workspace_id]);

  // Derived memberships: include base operator admin plus any created members
  const memberships = useMemo<WorkspaceMembership[]>(() => {
    if (!activeWorkspace) return [];
    const base: WorkspaceMembership = {
      membership_id: `mem-${activeWorkspace.workspace_id.slice(0, 8)}`,
      workspace_id: activeWorkspace.workspace_id,
      actor_id: "dev-operator",
      role: "ADMIN",
      status: "ACTIVE",
      created_at: activeWorkspace.created_at,
      receipt_id: activeWorkspace.receipt_id || "rcpt-initial-admin",
    };
    const overriddenBase = extraMemberships.find((m) => m.actor_id === "dev-operator");
    const list = overriddenBase
      ? [overriddenBase, ...extraMemberships.filter((m) => m.actor_id !== "dev-operator")]
      : [base, ...extraMemberships.filter((m) => m.actor_id !== "dev-operator")];
    return list;
  }, [activeWorkspace, extraMemberships]);

  const handleMemberAdded = (newMember: WorkspaceMembership) => {
    setExtraMemberships((prev) => [
      ...prev.filter((m) => m.actor_id !== newMember.actor_id),
      newMember,
    ]);
  };

  const handleMemberRemoved = (actorId: string) => {
    setExtraMemberships((prev) => {
      const exists = prev.some((m) => m.actor_id === actorId);
      if (exists) {
        return prev.map((m) =>
          m.actor_id === actorId ? { ...m, status: "REVOKED" } : m,
        );
      }
      return [
        ...prev,
        {
          membership_id: `mem-revoked-${actorId}`,
          workspace_id: activeWorkspace?.workspace_id || "",
          actor_id: actorId,
          role: "MEMBER",
          status: "REVOKED",
          created_at: new Date().toISOString(),
          receipt_id: "rcpt-revoked",
        },
      ];
    });
  };

  const handleGrantIssued = (newGrant: OperatorGrant) => {
    setGrants((prev) => [
      ...prev.filter((g) => g.grant_id !== newGrant.grant_id),
      newGrant,
    ]);
  };

  const handleGrantRevoked = (grantId: string) => {
    setGrants((prev) =>
      prev.map((g) =>
        g.grant_id === grantId
          ? { ...g, revoked_at: new Date().toISOString() }
          : g,
      ),
    );
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-slate-800 pb-5">
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold tracking-tight text-white">
                Workspace Management Console
              </h1>
              <Badge variant="neutral">CA-TWC-UI-01</Badge>
              <Badge variant="outline" data-testid="spec-badge">FR-APP-001..003</Badge>
            </div>
            <p className="text-sm text-slate-400 mt-1">
              Multi-tenant isolated workspace administration, member rosters, and operator emergency grants (FR-CAE-TEN-001..005).
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Button
              variant="primary"
              onClick={() => setIsCreateModalOpen(true)}
              data-testid="create-new-workspace-button"
            >
              + Create Workspace
            </Button>
          </div>
        </div>

        {/* Global Error Banner if any */}
        {error && (
          <ErrorEnvelopeAlert
            error={error}
            onDismiss={clearError}
            data-testid="workspace-global-error"
          />
        )}

        {/* Workspace Quick-Switcher Bar */}
        <div className="bg-slate-900 border border-slate-800 rounded-lg p-4 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Workspaces ({workspaces.length})
            </span>
            <div className="flex flex-wrap gap-2">
              {workspaces.map((ws) => {
                const isActive = activeWorkspace?.workspace_id === ws.workspace_id;
                return (
                  <button
                    key={ws.workspace_id}
                    data-testid={`workspace-nav-item-${ws.slug}`}
                    onClick={() => selectWorkspace(ws.workspace_id)}
                    className={`px-3 py-1.5 rounded text-xs font-medium transition-colors border ${
                      isActive
                        ? "bg-indigo-600/30 text-indigo-200 border-indigo-500/50 shadow-sm"
                        : "bg-slate-800/80 text-slate-300 border-slate-700 hover:bg-slate-700 hover:text-white"
                    }`}
                  >
                    {ws.display_name}
                    {isActive && (
                      <span className="ml-2 text-[10px] bg-indigo-500 text-white px-1.5 py-0.5 rounded-full font-bold">
                        ACTIVE
                      </span>
                    )}
                  </button>
                );
              })}
            </div>
          </div>

          {isLoading && (
            <span className="text-xs text-indigo-400 animate-pulse">
              Syncing tenant state...
            </span>
          )}
        </div>

        {/* Active Workspace Detail or Empty State */}
        {activeWorkspace ? (
          <WorkspaceDetail
            workspace={activeWorkspace}
            members={memberships}
            grants={grants}
            onMemberAdded={handleMemberAdded}
            onMemberRemoved={handleMemberRemoved}
            onGrantIssued={handleGrantIssued}
            onGrantRevoked={handleGrantRevoked}
          />
        ) : (
          <div className="bg-slate-900/50 border border-slate-800/80 rounded-xl p-12 text-center">
            <p className="text-slate-400 text-sm">
              {isLoading
                ? "Loading active workspace..."
                : "No workspace selected. Please select or create a workspace to proceed."}
            </p>
          </div>
        )}
      </div>

      {/* Creation Modal */}
      <WorkspaceCreateModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
      />
    </div>
  );
}
