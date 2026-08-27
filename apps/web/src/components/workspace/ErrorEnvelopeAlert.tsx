/**
 * Component for rendering TS-APP-API-004 §5 error envelopes.
 */

import type { ApiError } from "../../api/ApiError";

export interface ErrorEnvelopeAlertProps {
  readonly error: ApiError | Error | string | null;
  readonly onDismiss?: () => void;
  readonly className?: string;
}

export function ErrorEnvelopeAlert({ error, onDismiss, className = "" }: ErrorEnvelopeAlertProps) {
  if (!error) return null;

  let message = "";
  let errorCode: string | null = null;
  let status: number | null = null;

  if (typeof error === "string") {
    message = error;
  } else if ("errorCode" in error && typeof error.errorCode === "string") {
    message = error.message;
    errorCode = error.errorCode;
    status = (error as ApiError).status;
  } else {
    message = error.message || "An unexpected error occurred.";
  }

  const isWarning = errorCode === "WORKSPACE_SUSPENDED";
  const toneBg = isWarning ? "bg-amber-950/40 border-amber-500/50 text-amber-200" : "bg-red-950/40 border-danger/50 text-red-200";
  const badgeBg = isWarning ? "bg-amber-500/20 text-amber-300 border-amber-500/40" : "bg-red-500/20 text-danger border-danger/40";

  return (
    <div
      role="alert"
      data-testid="error-envelope-alert"
      className={`relative rounded-md border p-3 text-sm ${toneBg} ${className}`}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-2">
            {errorCode && (
              <span
                data-testid="error-code-badge"
                className={`rounded border px-1.5 py-0.5 text-xs font-mono font-semibold ${badgeBg}`}
              >
                {errorCode}
              </span>
            )}
            {status && <span className="text-xs text-muted-foreground font-mono">HTTP {status}</span>}
          </div>
          <p className="mt-0.5">{message}</p>
        </div>
        {onDismiss && (
          <button
            type="button"
            onClick={onDismiss}
            aria-label="Dismiss alert"
            className="rounded p-1 text-muted-foreground hover:bg-surface-elevated hover:text-foreground"
          >
            ✕
          </button>
        )}
      </div>
    </div>
  );
}
