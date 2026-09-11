/**
 * Workspace Detail & Management View.
 * Governed by SPEC-TWC-UI-001, MC-CAE-WS-001, and FR-APP-001..003.
 */

import { useState } from "react";
import { Button } from "../ui/Button";
import { Card } from "../ui/Card";
import { MembershipTable } from "./MembershipTable";
import { AddMemberModal } from "./AddMemberModal";
import { GrantTable } from "./GrantTable";
import { IssueGrantModal } from "./IssueGrantModal";
import { ErrorEnvelopeAlert } from "./ErrorEnvelopeAlert";
import { useWorkspace } from "../../context/WorkspaceContext";
import { useOperator } from "../../auth/DevOperatorContext";
import type { OperatorGrant, Workspace, WorkspaceMembership, WorkspaceStatus } from "../../api/tenancy";

export interface WorkspaceDetailProps {
  readonly workspace: Workspace;
  readonly members: readonly WorkspaceMembership[];
  readonly grants: readonly OperatorGrant[];
  readonly onMemberAdded: (member: WorkspaceMembership) => void;
  readonly onMemberRemoved: (actorId: string) => void;
  readonly onGrantIssued: (grant: OperatorGrant) => void;
  readonly onGrantRevoked: (grantId: string) => void;
}

export function WorkspaceDetail({
  workspace,
  members,
  grants,
  onMemberAdded,
  onMemberRemoved,
  onGrantIssued,
  onGrantRevoked,
}: WorkspaceDetailProps) {
  const operator = useOperator();
  const { updateActiveWorkspace } = useWorkspace();

  const [isEditingSettings, setIsEditingSettings] = useState(false);
  const [editDisplayName, setEditDisplayName] = useState(workspace.display_name);
  const [editStatus, setEditStatus] = useState<WorkspaceStatus>(workspace.status);
  const [isSavingSettings, setIsSavingSettings] = useState(false);
  const [settingsError, setSettingsError] = useState<Error | null>(null);

  const [isAddMemberOpen, setIsAddMemberOpen] = useState(false);
  const [isIssueGrantOpen, setIsIssueGrantOpen] = useState(false);

  const isSuspended = workspace.status === "SUSPENDED";

  const handleSaveSettings = async () => {
    setIsSavingSettings(true);
    setSettingsError(null);
    try {
      await updateActiveWorkspace({
        display_name: editDisplayName.trim() || workspace.display_name,
        status: editStatus,
      });
      setIsEditingSettings(false);
    } catch (err) {
      setSettingsError(err instanceof Error ? err : new Error("Failed to update workspace"));
    } finally {
      setIsSavingSettings(false);
    }
  };

  return (
    <div className="flex flex-col gap-6" data-testid="workspace-detail">
      {/* Workspace Overview & Identity */}
      <Card className="flex flex-col gap-4">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-xl font-bold text-foreground" data-testid="workspace-display-name">
                {workspace.display_name}
              </h1>
              <span
                data-testid="workspace-status-badge"
                className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                  isSuspended
                    ? "border border-amber-500/50 bg-amber-950/30 text-amber-300"
                    : "border border-success/40 bg-green-950/20 text-success"
                }`}
              >
                {workspace.status}
              </span>
            </div>
            <p className="mt-1 font-mono text-xs text-muted-foreground">
              Slug: <span className="text-foreground">{workspace.slug}</span> | ID:{" "}
              <span className="text-foreground">{workspace.workspace_id}</span>
            </p>
          </div>

          <div className="flex items-center gap-2">
            {!isEditingSettings ? (
              <Button
                variant="ghost"
                data-testid="edit-workspace-settings-button"
                onClick={() => {
                  setEditDisplayName(workspace.display_name);
                  setEditStatus(workspace.status);
                  setIsEditingSettings(true);
                }}
              >
                Settings
              </Button>
            ) : (
              <Button
                variant="ghost"
                onClick={() => {
                  setIsEditingSettings(false);
                  setSettingsError(null);
                }}
              >
                Cancel
              </Button>
            )}
          </div>
        </div>

        {isSuspended && (
          <div
            role="alert"
            data-testid="workspace-suspended-alert"
            className="rounded-md border border-amber-500/40 bg-amber-950/30 p-3 text-sm text-amber-200"
          >
            ⚠️ <strong>Workspace Suspended</strong>: All tenant mutations are frozen. Re-activate workspace under Settings to resume standard operations.
          </div>
        )}

        {isEditingSettings && (
          <div className="mt-2 flex flex-col gap-3 rounded-md border border-border bg-surface-elevated p-4">
            <h3 className="text-sm font-semibold text-foreground">Edit Workspace Settings</h3>
            <ErrorEnvelopeAlert error={settingsError} onDismiss={() => setSettingsError(null)} />

            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
              <div>
                <label className="block text-xs font-medium text-foreground">Display Name</label>
                <input
                  type="text"
                  data-testid="edit-display-name-input"
                  value={editDisplayName}
                  onChange={(e) => setEditDisplayName(e.target.value)}
                  className="mt-1 w-full rounded-md border border-border bg-surface px-3 py-1.5 text-sm text-foreground focus:border-accent focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-foreground">Status</label>
                <select
                  data-testid="edit-status-select"
                  value={editStatus}
                  onChange={(e) => setEditStatus(e.target.value as WorkspaceStatus)}
                  className="mt-1 w-full rounded-md border border-border bg-surface px-3 py-1.5 text-sm text-foreground focus:border-accent focus:outline-none"
                >
                  <option value="ACTIVE">ACTIVE</option>
                  <option value="SUSPENDED">SUSPENDED</option>
                  <option value="ARCHIVED">ARCHIVED</option>
                </select>
              </div>
            </div>

            <div className="flex justify-end gap-2 pt-2">
              <Button
                data-testid="save-workspace-settings-button"
                disabled={isSavingSettings}
                onClick={handleSaveSettings}
              >
                {isSavingSettings ? "Saving…" : "Save Changes"}
              </Button>
            </div>
          </div>
        )}

        <div className="flex flex-wrap items-center gap-x-6 gap-y-2 border-t border-border pt-3 text-xs text-muted-foreground">
          <div>
            Created: <span className="text-foreground">{new Date(workspace.created_at).toLocaleString()}</span>
          </div>
          {workspace.receipt_id && (
            <div>
              Receipt: <span className="font-mono text-foreground">{workspace.receipt_id.slice(0, 16)}…</span>
            </div>
          )}
        </div>
      </Card>

      {/* Membership Roster */}
      <div className="flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-base font-semibold text-foreground">Workspace Members</h2>
            <p className="text-xs text-muted-foreground">
              Actors with scoped access permissions to this workspace.
            </p>
          </div>
          <Button
            data-testid="open-add-member-button"
            disabled={isSuspended}
            onClick={() => setIsAddMemberOpen(true)}
          >
            + Add Member
          </Button>
        </div>

        <MembershipTable
          workspaceId={workspace.workspace_id}
          workspaceStatus={workspace.status}
          members={members}
          onMemberRemoved={onMemberRemoved}
          currentActorId={operator.actor_id}
        />
      </div>

      {/* Operator Access Grants */}
      <div className="flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-base font-semibold text-foreground">Operator Access Grants</h2>
            <p className="text-xs text-muted-foreground">
              Time-bounded cross-tenant access grants for support and governance (OPR-001).
            </p>
          </div>
          <Button
            variant="ghost"
            data-testid="open-issue-grant-button"
            disabled={isSuspended}
            onClick={() => setIsIssueGrantOpen(true)}
          >
            + Issue Operator Grant
          </Button>
        </div>

        <GrantTable
          workspaceId={workspace.workspace_id}
          workspaceStatus={workspace.status}
          grants={grants}
          onGrantRevoked={onGrantRevoked}
          currentActorId={operator.actor_id}
        />
      </div>

      {/* Add Member Dialog */}
      <AddMemberModal
        isOpen={isAddMemberOpen}
        onClose={() => setIsAddMemberOpen(false)}
        workspaceId={workspace.workspace_id}
        workspaceStatus={workspace.status}
        onMemberAdded={onMemberAdded}
        currentActorId={operator.actor_id}
      />

      {/* Issue Grant Dialog */}
      <IssueGrantModal
        isOpen={isIssueGrantOpen}
        onClose={() => setIsIssueGrantOpen(false)}
        workspaceId={workspace.workspace_id}
        workspaceStatus={workspace.status}
        onGrantIssued={onGrantIssued}
        currentActorId={operator.actor_id}
      />
    </div>
  );
}
