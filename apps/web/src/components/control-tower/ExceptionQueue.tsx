// TS-APP-UI-003 - ExceptionQueue component
// Exception list with resolve functionality

import { useState } from "react";
import { Badge } from "../ui/Badge";
import type { ExceptionReviewPackage } from "../../api/campaigns";
import type { UseMutationResult } from "@tanstack/react-query";
import type { ResolveExceptionInput } from "../../hooks/useExceptions";

interface ExceptionQueueProps {
  campaignId: string;
  packages: ExceptionReviewPackage[];
  resolveMutation: UseMutationResult<void, Error, ResolveExceptionInput>;
}

export function ExceptionQueue({ campaignId, packages, resolveMutation }: ExceptionQueueProps) {
  const [selectedPackage, setSelectedPackage] = useState<string | null>(null);

  const handleResolve = (packageId: string, decision: "REQUEST_REVISION" | "REJECT") => {
    resolveMutation.mutate({ packageId, decision });
    setSelectedPackage(null);
  };

  if (!packages || packages.length === 0) {
    return (
      <div className="control-tower-card">
        <div className="control-tower-card-header">
          <span>Exceptions</span>
        </div>
        <p className="text-ca-text-secondary">No open exceptions</p>
      </div>
    );
  }

  return (
    <div className="control-tower-card">
      <div className="control-tower-card-header">
        <span>Exceptions</span>
        <Badge tone="danger">{packages.length}</Badge>
      </div>

      <div className="space-y-4">
        {packages.map((pkg) => (
          <div
            key={pkg.package_id}
            className="rounded-lg border border-ca-danger/30 bg-ca-surface-raised p-4"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium text-ca-text-primary">
                    {pkg.summary}
                  </span>
                  <Badge tone="muted">{pkg.responsible_product}</Badge>
                </div>

                {/* Evidence refs */}
                {pkg.evidence_refs && pkg.evidence_refs.length > 0 && (
                  <div className="mt-2 flex flex-wrap gap-1">
                    {pkg.evidence_refs.map((ref: string, idx: number) => (
                      <code key={idx} className="rounded bg-ca-bg px-1 py-0.5 text-xs text-ca-text-secondary">
                        {ref}
                      </code>
                    ))}
                  </div>
                )}
              </div>

              {/* Decision buttons - only show allowed decisions */}
              <div className="ml-4 flex gap-2">
                {pkg.allowed_decisions?.includes("REQUEST_REVISION") && (
                  <button
                    onClick={() => handleResolve(pkg.package_id, "REQUEST_REVISION")}
                    disabled={resolveMutation.isPending}
                    className="rounded bg-ca-gold-500 px-3 py-1 text-xs font-medium text-white hover:bg-ca-gold-600 disabled:opacity-50"
                  >
                    Request Revision
                  </button>
                )}
                {pkg.allowed_decisions?.includes("REJECT") && (
                  <button
                    onClick={() => handleResolve(pkg.package_id, "REJECT")}
                    disabled={resolveMutation.isPending}
                    className="rounded bg-ca-danger px-3 py-1 text-xs font-medium text-white hover:bg-ca-danger/80 disabled:opacity-50"
                  >
                    Reject
                  </button>
                )}
              </div>
            </div>

            {/* Notes input (optional) */}
            {selectedPackage === pkg.package_id && (
              <div className="mt-3">
                <textarea
                  placeholder="Add notes (optional)..."
                  className="w-full rounded border border-ca-border bg-ca-bg p-2 text-sm text-ca-text-primary"
                  rows={2}
                />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
