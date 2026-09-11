/**
 * Operator Access Grant Table Component.
 * Governed by SPEC-TWC-UI-001, OPR-001, and TS-CAE-TEN-001.
 */

import { useState } from "react";
import { Button } from "../ui/Button";
import { ErrorEnvelopeAlert } from "./ErrorEnvelopeAlert";
import { revokeOperatorGrant, type OperatorGrant, type WorkspaceStatus } from "../../api/tenancy";
import { ApiError } from "../../api/ApiError";

export interface GrantTableProps {
  readonly workspaceId: string;
  readonly workspaceStatus: WorkspaceStatus;
  readonly grants: readonly OperatorGrant[];
  readonly onGrantRevoked: (grantId: string) => void;
  readonly currentActorId?: string;
}

export function GrantTable({
  workspaceId,
  workspaceStatus,
  grants = [],
  onGrantRevoked,
  currentActorId,
}: GrantTableProps) {
  const [revokingGrantId, setRevokingGrantId] = useState<string | null>(null);
  const [error, setError] = useState<ApiError | Error | null>(null);

  const isSuspended = workspaceStatus === "SUSPENDED";

  const handleRevoke = async (grantId: string) => {
    if (isSuspended) return;
    setError(null);
    setRevokingGrantId(grantId);
    try {
      await revokeOperatorGrant(workspaceId, grantId, {
        actor_id: currentActorId,
        workspace_id: workspaceId,
        role: "ADMIN",
        is_operator: true,
      });
      onGrantRevoked(grantId);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err);
      } else if (err instanceof Error) {
        setError(err);
      } else {
        setError(new Error("Failed to revoke operator grant"));
      }
    } finally {
      setRevokingGrantId(null);
    }
  };

  return (
    <div className="flex flex-col gap-3">
      <ErrorEnvelopeAlert error={error} onDismiss={() => setError(null)} />

      {grants.length === 0 ? (
        <div className="rounded-md border border-border bg-surface-elevated p-6 text-center text-sm text-muted-foreground">
          No operator access grants active for this workspace.
        </div>
      ) : (
        <div className="overflow-x-auto rounded-md border border-border bg-surface">
          <table className="w-full text-left text-sm" data-testid="grant-table">
            <thead className="border-b border-border bg-surface-elevated text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              <tr>
                <th className="px-4 py-3">Operator Actor</th>
                <th className="px-4 py-3">Operator Org</th>
                <th className="px-4 py-3">Justification</th>
                <th className="px-4 py-3">Expires At</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {grants.map((grant) => {
                const isRevoking = revokingGrantId === grant.grant_id;
                const isRevoked = Boolean(grant.revoked_at);
                const isExpired = new Date(grant.expires_at).getTime() <= Date.now();

                return (
                  <tr
                    key={grant.grant_id}
                    data-testid={`grant-row-${grant.grant_id}`}
                    className="hover:bg-surface-elevated/50"
                  >
                    <td className="px-4 py-3 font-mono text-xs text-foreground">
                      {grant.operator_actor_id}
                    </td>
                    <td className="px-4 py-3 font-mono text-xs text-muted-foreground">
                      {grant.operator_org_id.slice(0, 8)}…
                    </td>
                    <td className="px-4 py-3 text-xs text-foreground">
                      {grant.justification}
                    </td>
                    <td className="px-4 py-3 text-xs text-muted-foreground">
                      {new Date(grant.expires_at).toLocaleString()}
                    </td>
                    <td className="px-4 py-3">
                      <span
                        data-testid={`grant-status-${grant.grant_id}`}
                        className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${
                          isRevoked
                            ? "border border-danger/40 bg-red-950/20 text-danger"
                            : isExpired
                              ? "border border-muted/40 bg-surface-elevated text-muted-foreground"
                              : "border border-accent/40 bg-amber-950/20 text-accent"
                        }`}
                      >
                        {isRevoked ? "REVOKED" : isExpired ? "EXPIRED" : "ACTIVE"}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-right">
                      {!isRevoked && !isExpired && (
                        <Button
                          variant="ghost"
                          data-testid={`revoke-grant-button-${grant.grant_id}`}
                          disabled={isSuspended || isRevoking}
                          onClick={() => handleRevoke(grant.grant_id)}
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
