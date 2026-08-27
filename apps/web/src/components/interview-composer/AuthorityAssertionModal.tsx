import { useState } from "react";
import { Button } from "../ui/Button";
import { Badge } from "../ui/Badge";

export interface AuthorityScopeData {
  readonly operatorId: string;
  readonly authorityScope: string;
  readonly assertionId: string;
}

interface AuthorityAssertionModalProps {
  readonly isOpen: boolean;
  readonly initialData?: Partial<AuthorityScopeData>;
  readonly onConfirm: (data: AuthorityScopeData) => void;
  readonly onCancel: () => void;
}

const DEFAULT_SCOPES = [
  { value: "DEVELOPMENT_TEST", label: "DEVELOPMENT_TEST — Dev & Stage Testing" },
  { value: "EDITORIAL_PRODUCER", label: "EDITORIAL_PRODUCER — Episode Production" },
  { value: "GOVERNANCE_AUDITOR", label: "GOVERNANCE_AUDITOR — Compliance Audit" },
] as const;

export function AuthorityAssertionModal({
  isOpen,
  initialData,
  onConfirm,
  onCancel,
}: AuthorityAssertionModalProps) {
  const [operatorId, setOperatorId] = useState(initialData?.operatorId || "op-dev");
  const [authorityScope, setAuthorityScope] = useState(
    initialData?.authorityScope || "DEVELOPMENT_TEST"
  );
  const [assertionId, setAssertionId] = useState(
    initialData?.assertionId || `assert-gst-${Date.now().toString(36)}`
  );
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  function handleConfirm(e?: React.SyntheticEvent) {
    e?.preventDefault();
    setError(null);
    if (!operatorId.trim()) {
      setError("Operator ID is required");
      return;
    }
    if (!authorityScope.trim()) {
      setError("Authority Scope is required");
      return;
    }
    if (!assertionId.trim()) {
      setError("Assertion ID is required");
      return;
    }

    onConfirm({
      operatorId: operatorId.trim(),
      authorityScope: authorityScope.trim(),
      assertionId: assertionId.trim(),
    });
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm"
      data-testid="authority-modal"
    >
      <div className="w-full max-w-md rounded-xl border border-border bg-surface p-6 shadow-2xl space-y-4">
        <div className="flex items-center justify-between border-b border-border pb-3">
          <div className="flex items-center gap-2">
            <h3 className="text-base font-semibold text-foreground">Operator Authority Scope Attestation</h3>
            <Badge tone="accent">FR-APP-006</Badge>
          </div>
          <button
            type="button"
            onClick={onCancel}
            className="text-muted-foreground hover:text-foreground text-sm"
            data-testid="authority-cancel-btn"
          >
            ✕
          </button>
        </div>

        <p className="text-xs text-muted-foreground">
          Per TS-APP-API-004 §5 and Mandate 28 governance rules, research package ingestion requires explicit operator authority binding.
        </p>

        <div className="space-y-3">
          <div>
            <label className="block text-xs font-medium text-foreground mb-1">
              Operator ID <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={operatorId}
              onChange={(e) => {
                setOperatorId(e.target.value);
                if (error) setError(null);
              }}
              placeholder="e.g. op-dev or operator email"
              className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground focus:border-accent focus:outline-none"
              data-testid="operator-id-input"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-foreground mb-1">
              Authority Scope <span className="text-red-500">*</span>
            </label>
            <select
              value={authorityScope}
              onChange={(e) => setAuthorityScope(e.target.value)}
              className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground focus:border-accent focus:outline-none"
              data-testid="authority-scope-select"
            >
              {DEFAULT_SCOPES.map((s) => (
                <option key={s.value} value={s.value}>
                  {s.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-foreground mb-1">
              Assertion ID <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={assertionId}
              onChange={(e) => {
                setAssertionId(e.target.value);
                if (error) setError(null);
              }}
              placeholder="e.g. assert-gst-001"
              className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground focus:border-accent focus:outline-none"
              data-testid="assertion-id-input"
            />
          </div>

          {error && (
            <p className="text-xs text-red-500 font-medium" data-testid="authority-error">
              {error}
            </p>
          )}

          <div className="flex justify-end gap-2 pt-2 border-t border-border">
            <Button
              type="button"
              variant="ghost"
              onClick={onCancel}
              data-testid="authority-modal-cancel"
            >
              Cancel
            </Button>
            <Button
              type="button"
              variant="solid"
              onClick={handleConfirm}
              data-testid="authority-confirm-btn"
            >
              Attest & Proceed
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
