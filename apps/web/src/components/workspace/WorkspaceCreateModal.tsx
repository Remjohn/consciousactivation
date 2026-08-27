/**
 * Workspace Creation Dialog Component.
 * Governed by SPEC-TWC-UI-001, FR-APP-001, and HN-TWC-01.
 */

import { useState, type FormEvent } from "react";
import { useWorkspace } from "../../context/WorkspaceContext";
import { Button } from "../ui/Button";
import { ErrorEnvelopeAlert } from "./ErrorEnvelopeAlert";
import { ApiError } from "../../api/ApiError";

export interface WorkspaceCreateModalProps {
  readonly isOpen: boolean;
  readonly onClose: () => void;
  readonly onCreated?: (workspaceId: string) => void;
}

export function WorkspaceCreateModal({ isOpen, onClose, onCreated }: WorkspaceCreateModalProps) {
  const { createNewWorkspace } = useWorkspace();

  const [displayName, setDisplayName] = useState("");
  const [slug, setSlug] = useState("");
  const [isCustomSlug, setIsCustomSlug] = useState(false);
  const [validationError, setValidationError] = useState<string | null>(null);
  const [serverError, setServerError] = useState<ApiError | Error | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleDisplayNameChange = (value: string) => {
    setDisplayName(value);
    setValidationError(null);
    if (!isCustomSlug) {
      const autoSlug = value
        .toLowerCase()
        .trim()
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/^-+|-+$/g, "");
      setSlug(autoSlug);
    }
  };

  const handleSlugChange = (value: string) => {
    setIsCustomSlug(true);
    setSlug(value.toLowerCase().replace(/[^a-z0-9-]/g, ""));
    setValidationError(null);
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setValidationError(null);
    setServerError(null);

    const trimmedName = displayName.trim();
    const trimmedSlug = slug.trim();

    // HN-TWC-01: Client rejection of empty / whitespace-only name
    if (!trimmedName) {
      setValidationError("Workspace name cannot be empty or whitespace only.");
      return;
    }

    if (!trimmedSlug || trimmedSlug.length < 2) {
      setValidationError("Workspace slug must be at least 2 alphanumeric characters.");
      return;
    }

    if (!/^[a-z0-9-]+$/.test(trimmedSlug)) {
      setValidationError("Slug may only contain lowercase letters, numbers, and hyphens.");
      return;
    }

    setIsSubmitting(true);
    try {
      const created = await createNewWorkspace({
        slug: trimmedSlug,
        display_name: trimmedName,
      });
      setDisplayName("");
      setSlug("");
      setIsCustomSlug(false);
      if (onCreated) {
        onCreated(created.workspace_id);
      }
      onClose();
    } catch (err) {
      if (err instanceof ApiError) {
        setServerError(err);
      } else if (err instanceof Error) {
        setServerError(err);
      } else {
        setServerError(new Error("An unexpected error occurred."));
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="create-workspace-title"
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4"
    >
      <div className="w-full max-w-md rounded-lg border border-border bg-surface p-6 shadow-xl">
        <div className="flex items-center justify-between border-b border-border pb-3">
          <h2 id="create-workspace-title" className="text-lg font-semibold text-foreground">
            Create New Workspace
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
              data-testid="validation-error"
              className="rounded-md border border-danger/40 bg-red-950/30 p-2.5 text-xs text-red-200"
            >
              {validationError}
            </div>
          )}

          <div>
            <label htmlFor="workspace-name-input" className="block text-xs font-medium text-foreground">
              Workspace Name <span className="text-danger">*</span>
            </label>
            <input
              id="workspace-name-input"
              data-testid="workspace-name-input"
              type="text"
              required
              placeholder="e.g. Acme Media Production"
              value={displayName}
              onChange={(e) => handleDisplayNameChange(e.target.value)}
              className="mt-1 w-full rounded-md border border-border bg-surface-elevated px-3 py-1.5 text-sm text-foreground placeholder:text-muted-foreground focus:border-accent focus:outline-none"
            />
          </div>

          <div>
            <label htmlFor="workspace-slug-input" className="block text-xs font-medium text-foreground">
              Workspace Slug <span className="text-danger">*</span>
            </label>
            <input
              id="workspace-slug-input"
              data-testid="workspace-slug-input"
              type="text"
              required
              placeholder="e.g. acme-media-production"
              value={slug}
              onChange={(e) => handleSlugChange(e.target.value)}
              className="mt-1 w-full rounded-md border border-border bg-surface-elevated px-3 py-1.5 text-sm font-mono text-foreground placeholder:text-muted-foreground focus:border-accent focus:outline-none"
            />
            <p className="mt-1 text-[11px] text-muted-foreground">
              Unique identifier used in API headers and URLs (lowercase, numbers, hyphens).
            </p>
          </div>

          <div className="mt-2 flex justify-end gap-2 border-t border-border pt-3">
            <Button type="button" variant="ghost" onClick={onClose} disabled={isSubmitting}>
              Cancel
            </Button>
            <Button
              type="submit"
              data-testid="create-workspace-submit-button"
              disabled={isSubmitting}
            >
              {isSubmitting ? "Creating…" : "Create Workspace"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
