/**
 * Membership Roster Table Component.
 * Governed by SPEC-TWC-UI-001, FR-APP-003, and HN-TWC-05.
 */

import { useState } from "react";
import { Badge } from "../ui/Badge";
import { Button } from "../ui/Button";
import { ErrorEnvelopeAlert } from "./ErrorEnvelopeAlert";
import { removeWorkspaceMembership, type WorkspaceMembership, type WorkspaceStatus } from "../../api/tenancy";
import { ApiError } from "../../api/ApiError";

export interface MembershipTableProps {
  readonly workspaceId: string;
  readonly workspaceStatus: WorkspaceStatus;
  readonly members: readonly WorkspaceMembership[];
  readonly onMemberRemoved: (actorId: string) => void;
  readonly currentActorId?: string;
}

export function MembershipTable({
  workspaceId,
  workspaceStatus,
  members = [],
  onMemberRemoved,
  currentActorId,
}: MembershipTableProps) {
  const [revokingActorId, setRevokingActorId] = useState<string | null>(null);
  const [error, setError] = useState<ApiError | Error | null>(null);

  const isSuspended = workspaceStatus === "SUSPENDED";

  const handleRevoke = async (actorId: string) => {
    if (isSuspended) return;
    setError(null);
    setRevokingActorId(actorId);
    try {
      await removeWorkspaceMembership(workspaceId, actorId, {
        actor_id: currentActorId,
        workspace_id: workspaceId,
        role: "ADMIN",
        is_operator: true,
      });
      // HN-TWC-05: Update membership state immediately without full-page reload
      onMemberRemoved(actorId);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err);
      } else if (err instanceof Error) {
        setError(err);
      } else {
        setError(new Error("Failed to remove member"));
      }
    } finally {
      setRevokingActorId(null);
    }
  };

  const roleTone = (role: string) => {
    switch (role) {
      case "ADMIN":
        return "accent";
      case "MEMBER":
        return "success";
      default:
        return "muted";
    }
  };

  return (
    <div className="flex flex-col gap-3">
      <ErrorEnvelopeAlert error={error} onDismiss={() => setError(null)} />

      {members.length === 0 ? (
        <div className="rounded-md border border-border bg-surface-elevated p-6 text-center text-sm text-muted-foreground">
          No members registered in this workspace yet.
        </div>
      ) : (
        <div className="overflow-x-auto rounded-md border border-border bg-surface">
          <table className="w-full text-left text-sm" data-testid="membership-table">
            <thead className="border-b border-border bg-surface-elevated text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              <tr>
                <th className="px-4 py-3">Actor / User ID</th>
                <th className="px-4 py-3">Role</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Joined Date</th>
                <th className="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {members.map((member) => {
                const isRevoking = revokingActorId === member.actor_id;
                const isCurrent = member.actor_id === currentActorId;
                const isRevoked = member.status === "REVOKED";

                return (
                  <tr
                    key={member.membership_id || member.actor_id}
                    data-testid={`member-row-${member.actor_id}`}
                    className="hover:bg-surface-elevated/50"
                  >
                    <td className="px-4 py-3 font-mono text-xs text-foreground">
                      {member.actor_id}
                      {isCurrent && (
                        <span className="ml-2 rounded bg-surface-elevated px-1.5 py-0.5 text-[10px] text-accent">
                          You
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-3">
                      <Badge tone={roleTone(member.role)} data-testid={`role-badge-${member.actor_id}`}>
                        {member.role}
                      </Badge>
                    </td>
                    <td className="px-4 py-3">
                      <span
                        data-testid={`status-badge-${member.actor_id}`}
                        className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${
                          isRevoked
                            ? "border border-danger/40 bg-red-950/20 text-danger"
                            : "border border-success/40 bg-green-950/20 text-success"
                        }`}
                      >
                        {member.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-xs text-muted-foreground">
                      {new Date(member.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-4 py-3 text-right">
                      {!isRevoked && (
                        <Button
                          variant="ghost"
                          data-testid={`revoke-member-button-${member.actor_id}`}
                          disabled={isSuspended || isRevoking}
                          onClick={() => handleRevoke(member.actor_id)}
                          className="text-xs text-danger hover:border-danger/60 hover:bg-danger/10"
                        >
                          {isRevoking ? "Revoking…" : "Revoke"}
                        </Button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
