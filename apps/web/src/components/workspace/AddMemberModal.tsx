/**
 * Add / Invite Member Dialog Component.
 * Governed by SPEC-TWC-UI-001, FR-APP-003, HN-TWC-02, and HN-TWC-03.
 */

import { useState, type FormEvent } from "react";
import { Button } from "../ui/Button";
import { ErrorEnvelopeAlert } from "./ErrorEnvelopeAlert";
import {
  addWorkspaceMembership,
  type AddMembershipPayload,
  type WorkspaceMembership,
  type WorkspaceRole,
  type WorkspaceStatus,
} from "../../api/tenancy";
import { ApiError } from "../../api/ApiError";

export interface AddMemberModalProps {
  readonly isOpen: boolean;
  readonly onClose: () => void;
  readonly workspaceId: string;
  readonly workspaceStatus: WorkspaceStatus;
  readonly onMemberAdded: (member: WorkspaceMembership) => void;
  readonly currentActorId?: string;
}

const ALLOWED_ROLES: readonly WorkspaceRole[] = ["ADMIN", "MEMBER", "VIEWER"];

export function AddMemberModal({
  isOpen,
  onClose,
  workspaceId,
  workspaceStatus,
  onMemberAdded,
  currentActorId,
}: AddMemberModalProps) {
  const [actorId, setActorId] = useState("");
  const [role, setRole] = useState<WorkspaceRole>("MEMBER");
  const [validationError, setValidationError] = useState<string | null>(null);
  const [serverError, setServerError] = useState<ApiError | Error | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen) return null;

  const isSuspended = workspaceStatus === "SUSPENDED";

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setValidationError(null);
    setServerError(null);

    // HN-TWC-03: Block adding members to suspended workspace
    if (isSuspended) {
      setValidationError("Cannot add members: Workspace is SUSPENDED.");
      return;
    }

    const trimmedActorId = actorId.trim();
    if (!trimmedActorId) {
      setValidationError("Actor / User ID cannot be empty.");
      return;
    }

    // HN-TWC-02: Validate role against allowed roles enum
    if (!ALLOWED_ROLES.includes(role)) {
      setValidationError(`Invalid role "${role}". Allowed roles are: ${ALLOWED_ROLES.join(", ")}.`);
      return;
    }

    setIsSubmitting(true);
    try {
      const payload: AddMembershipPayload = {
        actor_id: trimmedActorId,
        role,
      };

      const result = await addWorkspaceMembership(workspaceId, payload, {
        actor_id: currentActorId,
        workspace_id: workspaceId,
        role: "ADMIN",
        is_operator: true,
      });

      onMemberAdded(result);
      setActorId("");
      setRole("MEMBER");
      onClose();
    } catch (err) {
      if (err instanceof ApiError) {
        setServerError(err);
      } else if (err instanceof Error) {
        setServerError(err);
      } else {
        setServerError(new Error("Failed to add member."));
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="add-member-title"
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4"
    >
      <div className="w-full max-w-md rounded-lg border border-border bg-surface p-6 shadow-xl">
        <div className="flex items-center justify-between border-b border-border pb-3">
          <h2 id="add-member-title" className="text-lg font-semibold text-foreground">
            Add Workspace Member
          </h2>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close modal"
            className="rounded p-1 text-muted-foreground hover:bg-surface-elevated hover:text-foreground"
          >
            ✕
          </button>
        </div>

        {isSuspended && (
          <div
            role="alert"
            data-testid="suspended-workspace-warning"
            className="mt-4 rounded-md border border-amber-500/40 bg-amber-950/30 p-3 text-xs text-amber-200"
          >
            ⚠️ This workspace is currently <strong>SUSPENDED</strong>. Adding new members is disabled until the workspace is reactivated.
          </div>
        )}

        <form onSubmit={handleSubmit} noValidate className="mt-4 flex flex-col gap-4">
          <ErrorEnvelopeAlert error={serverError} onDismiss={() => setServerError(null)} />

          {validationError && (
            <div
              role="alert"
              data-testid="validation-error"
              className="rounded-md border border-danger/40 bg-red-950/30 p-2.5 text-xs text-red-200"
            >
              {validationError}
            </div>
          )}

          <div>
            <label htmlFor="member-actor-id-input" className="block text-xs font-medium text-foreground">
              Actor / User Identifier <span className="text-danger">*</span>
            </label>
            <input
              id="member-actor-id-input"
              data-testid="member-actor-id-input"
              type="text"
              required
              disabled={isSuspended}
              placeholder="e.g. user@example.com or actor-123"
              value={actorId}
              onChange={(e) => {
                setActorId(e.target.value);
                setValidationError(null);
              }}
              className="mt-1 w-full rounded-md border border-border bg-surface-elevated px-3 py-1.5 text-sm text-foreground placeholder:text-muted-foreground focus:border-accent focus:outline-none disabled:opacity-50"
            />
          </div>

          <div>
            <label htmlFor="member-role-select" className="block text-xs font-medium text-foreground">
              Workspace Role <span className="text-danger">*</span>
            </label>
            <select
              id="member-role-select"
              data-testid="member-role-select"
              disabled={isSuspended}
              value={role}
              onChange={(e) => setRole(e.target.value as WorkspaceRole)}
              className="mt-1 w-full rounded-md border border-border bg-surface-elevated px-3 py-1.5 text-sm text-foreground focus:border-accent focus:outline-none disabled:opacity-50"
            >
              <option value="MEMBER">MEMBER (Standard Access)</option>
              <option value="ADMIN">ADMIN (Full Workspace Management)</option>
              <option value="VIEWER">VIEWER (Read-Only Access)</option>
            </select>
          </div>

          <div className="mt-2 flex justify-end gap-2 border-t border-border pt-3">
            <Button type="button" variant="ghost" onClick={onClose} disabled={isSubmitting}>
              Cancel
            </Button>
            <Button
              type="submit"
              data-testid="add-member-submit-button"
              disabled={isSubmitting || isSuspended}
            >
              {isSubmitting ? "Adding…" : "Add Member"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
