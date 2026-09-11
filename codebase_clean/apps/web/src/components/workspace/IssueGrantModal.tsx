/**
 * Issue Operator Grant Dialog Component.
 * Governed by SPEC-TWC-UI-001, OPR-001, and TS-CAE-TEN-001.
 */

import { useState, type FormEvent } from "react";
import { Button } from "../ui/Button";
import { ErrorEnvelopeAlert } from "./ErrorEnvelopeAlert";
import {
  issueOperatorGrant,
  type IssueOperatorGrantPayload,
  type OperatorGrant,
  type WorkspaceStatus,
} from "../../api/tenancy";
import { ApiError } from "../../api/ApiError";

export interface IssueGrantModalProps {
  readonly isOpen: boolean;
  readonly onClose: () => void;
  readonly workspaceId: string;
  readonly workspaceStatus: WorkspaceStatus;
  readonly onGrantIssued: (grant: OperatorGrant) => void;
  readonly currentActorId?: string;
}

export function IssueGrantModal({
  isOpen,
  onClose,
  workspaceId,
  workspaceStatus,
  onGrantIssued,
  currentActorId,
}: IssueGrantModalProps) {
  const [operatorOrgId, setOperatorOrgId] = useState("00000000-0000-0000-0000-000000000001");
  const [operatorActorId, setOperatorActorId] = useState("");
  const [justification, setJustification] = useState("");
  const [durationHours, setDurationHours] = useState(24);
  const [validationError, setValidationError] = useState<string | null>(null);
  const [serverError, setServerError] = useState<ApiError | Error | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen) return null;

  const isSuspended = workspaceStatus === "SUSPENDED";

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setValidationError(null);
    setServerError(null);

    if (isSuspended) {
      setValidationError("Cannot issue grants for a SUSPENDED workspace.");
      return;
    }

    if (!operatorActorId.trim()) {
      setValidationError("Operator Actor ID cannot be empty.");
      return;
    }

    if (!justification.trim()) {
      setValidationError("Justification is required for operator access.");
      return;
    }

    const expiresAt = new Date(Date.now() + durationHours * 3600 * 1000).toISOString();

    setIsSubmitting(true);
    try {
      const payload: IssueOperatorGrantPayload = {
        operator_org_id: operatorOrgId.trim(),
        operator_actor_id: operatorActorId.trim(),
        justification: justification.trim(),
        expires_at: expiresAt,
      };

      const result = await issueOperatorGrant(workspaceId, payload, {
        actor_id: currentActorId,
        workspace_id: workspaceId,
        role: "ADMIN",
        is_operator: true,
      });

      onGrantIssued(result);
      setOperatorActorId("");
      setJustification("");
      onClose();
    } catch (err) {
      if (err instanceof ApiError) {
        setServerError(err);
      } else if (err instanceof Error) {
        setServerError(err);
      } else {
        setServerError(new Error("Failed to issue operator grant"));
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="issue-grant-title"
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4"
    >
      <div className="w-full max-w-md rounded-lg border border-border bg-surface p-6 shadow-xl">
        <div className="flex items-center justify-between border-b border-border pb-3">
          <h2 id="issue-grant-title" className="text-lg font-semibold text-foreground">
            Issue Operator Access Grant
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

        <form onSubmit={handleSubmit} noValidate className="mt-4 flex flex-col gap-4">
          <ErrorEnvelopeAlert error={serverError} onDismiss={() => setServerError(null)} />

          {validationError && (
            <div
              role="alert"
              data-testid="grant-validation-error"
              className="rounded-md border border-danger/40 bg-red-950/30 p-2.5 text-xs text-red-200"
            >
              {validationError}
            </div>
          )}

          <div>
            <label htmlFor="grant-actor-input" className="block text-xs font-medium text-foreground">
              Operator Actor ID <span className="text-danger">*</span>
            </label>
            <input
              id="grant-actor-input"
              data-testid="grant-actor-input"
              type="text"
              required
              disabled={isSuspended}
              placeholder="e.g. op-support-01"
              value={operatorActorId}
              onChange={(e) => {
                setOperatorActorId(e.target.value);
                setValidationError(null);
              }}
              className="mt-1 w-full rounded-md border border-border bg-surface-elevated px-3 py-1.5 text-sm text-foreground placeholder:text-muted-foreground focus:border-accent focus:outline-none disabled:opacity-50"
            />
          </div>

          <div>
            <label htmlFor="grant-org-input" className="block text-xs font-medium text-foreground">
              Operator Organization UUID <span className="text-danger">*</span>
            </label>
            <input
              id="grant-org-input"
              data-testid="grant-org-input"
              type="text"
              required
              disabled={isSuspended}
              value={operatorOrgId}
              onChange={(e) => setOperatorOrgId(e.target.value)}
              className="mt-1 w-full rounded-md border border-border bg-surface-elevated px-3 py-1.5 font-mono text-xs text-foreground placeholder:text-muted-foreground focus:border-accent focus:outline-none disabled:opacity-50"
            />
          </div>

          <div>
            <label htmlFor="grant-duration-select" className="block text-xs font-medium text-foreground">
              Grant Duration
            </label>
            <select
              id="grant-duration-select"
              data-testid="grant-duration-select"
              disabled={isSuspended}
              value={durationHours}
              onChange={(e) => setDurationHours(Number(e.target.value))}
              className="mt-1 w-full rounded-md border border-border bg-surface-elevated px-3 py-1.5 text-sm text-foreground focus:border-accent focus:outline-none disabled:opacity-50"
            >
              <option value={1}>1 Hour (Emergency Diagnosis)</option>
              <option value={8}>8 Hours (Standard Shift)</option>
              <option value={24}>24 Hours (1 Day Maintenance)</option>
              <option value={72}>72 Hours (Extended Investigation)</option>
            </select>
          </div>

          <div>
            <label htmlFor="grant-justification-input" className="block text-xs font-medium text-foreground">
              Justification / Ticket Reference <span className="text-danger">*</span>
            </label>
            <textarea
              id="grant-justification-input"
              data-testid="grant-justification-input"
              required
              disabled={isSuspended}
              rows={3}
              placeholder="e.g. Investigating pipeline compilation latency issue #402"
              value={justification}
              onChange={(e) => {
                setJustification(e.target.value);
                setValidationError(null);
              }}
              className="mt-1 w-full rounded-md border border-border bg-surface-elevated px-3 py-1.5 text-sm text-foreground placeholder:text-muted-foreground focus:border-accent focus:outline-none disabled:opacity-50"
            />
          </div>

          <div className="mt-2 flex justify-end gap-2 border-t border-border pt-3">
            <Button type="button" variant="ghost" onClick={onClose} disabled={isSubmitting}>
              Cancel
            </Button>
            <Button
              type="submit"
              data-testid="issue-grant-submit-button"
              disabled={isSubmitting || isSuspended}
            >
              {isSubmitting ? "Issuing…" : "Issue Grant"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
