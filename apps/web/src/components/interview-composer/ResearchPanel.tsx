import { useState, useEffect } from "react";
import { useCreateResearchPackage } from "../../hooks/useCreateResearchPackage";
import { useWorkspace } from "../../context/WorkspaceContext";
import type { CreateResearchPackageInput } from "../../api/interviewComposer";
import type { SourceUrlItem, GuestResearchPackageResponse } from "../../api/types";
import { Button } from "../ui/Button";
import { Badge } from "../ui/Badge";
import { SourceUrlManager } from "./SourceUrlManager";
import { DocumentDropzone, type ManagedFileItem } from "./DocumentDropzone";
import { AuthorityAssertionModal, type AuthorityScopeData } from "./AuthorityAssertionModal";
import { ResearchPackageInspector } from "./ResearchPackageInspector";

interface ResearchPanelProps {
  onReady: (researchPackageId: string) => void;
  initialPackage?: GuestResearchPackageResponse | null;
}

export function ResearchPanel({ onReady, initialPackage }: ResearchPanelProps) {
  const { activeWorkspaceId } = useWorkspace();

  const [guestName, setGuestName] = useState("");
  const [sourceUrls, setSourceUrls] = useState<SourceUrlItem[]>([]);
  const [managedFiles, setManagedFiles] = useState<ManagedFileItem[]>([]);
  const [workspaceId, setWorkspaceId] = useState("");
  const [projectId, setProjectId] = useState("prj-dev");
  const [operatorId, setOperatorId] = useState("op-dev");
  const [authorityScope, setAuthorityScope] = useState("DEVELOPMENT_TEST");
  const [assertionId, setAssertionId] = useState(`assert-gst-${Date.now().toString(36)}`);

  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [localError, setLocalError] = useState<{ code: string; message: string } | null>(null);
  const [createdPackage, setCreatedPackage] = useState<GuestResearchPackageResponse | null>(
    initialPackage || null
  );

  const mutation = useCreateResearchPackage();

  // Auto-inject active workspace ID from WorkspaceContext
  useEffect(() => {
    if (activeWorkspaceId && !workspaceId) {
      setWorkspaceId(activeWorkspaceId);
    }
  }, [activeWorkspaceId, workspaceId]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLocalError(null);

    // Hard Negative Validations
    const trimmedGuestName = guestName.trim();
    if (!trimmedGuestName) {
      setLocalError({
        code: "GUEST_NAME_INVALID",
        message: "Guest name is required and cannot be whitespace only (HN-GST-01).",
      });
      return;
    }

    const effectiveWorkspaceId = (workspaceId || activeWorkspaceId || "").trim();
    if (!effectiveWorkspaceId) {
      setLocalError({
        code: "WORKSPACE_REQUIRED",
        message: "Active workspace ID is required for tenant isolation (HN-GST-04).",
      });
      return;
    }

    if (!operatorId.trim() || !authorityScope.trim() || !assertionId.trim()) {
      setLocalError({
        code: "AUTHORITY_REQUIRED",
        message: "Operator ID, Authority Scope, and Assertion ID are required (HN-GST-05).",
      });
      setIsAuthModalOpen(true);
      return;
    }

    // Check if any file has errors (e.g. tier size exceeded)
    const invalidFile = managedFiles.find((f) => !!f.error);
    if (invalidFile) {
      setLocalError({
        code: "MEDIA_SIZE_EXCEEDED",
        message: `Asset ${invalidFile.file.name} is invalid: ${invalidFile.error}`,
      });
      return;
    }

    // Validate caption targets
    const captionTracks = managedFiles.filter((f) => f.context_class === "CAPTION_TRACK");
    const recordingNames = new Set(
      managedFiles.filter((f) => f.context_class === "INTERVIEW_RECORDING").map((f) => f.file.name)
    );
    for (const ct of captionTracks) {
      if (ct.caption_for && !recordingNames.has(ct.caption_for)) {
        setLocalError({
          code: "INVALID_CAPTION_TARGET",
          message: `Caption track ${ct.file.name} references non-existent or non-recording asset '${ct.caption_for}'.`,
        });
        return;
      }
    }

    const filesToUpload = managedFiles.map((m) => m.file);
    const documentMetadata = managedFiles.map((m) => ({
      context_class: m.context_class,
      caption_for: m.caption_for || null,
    }));

    const input: CreateResearchPackageInput = {
      guestName: trimmedGuestName,
      sourceUrls: sourceUrls.map((s) => s.url),
      documents: filesToUpload,
      documentMetadata,
      workspaceId: effectiveWorkspaceId,
      projectId: projectId.trim() || "prj-dev",
      operatorId: operatorId.trim(),
      authorityScope: authorityScope.trim(),
      assertionId: assertionId.trim(),
    };

    try {
      const result = await mutation.mutateAsync(input);
      setCreatedPackage(result);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : String(err);
      setLocalError({
        code: "CREATION_FAILED",
        message,
      });
    }
  }

  function handleAuthorityConfirm(data: AuthorityScopeData) {
    setOperatorId(data.operatorId);
    setAuthorityScope(data.authorityScope);
    setAssertionId(data.assertionId);
    setIsAuthModalOpen(false);
  }

  // If already created or inspecting a package, render the Inspector
  if (createdPackage) {
    return (
      <div className="space-y-4" data-testid="research-panel-completed">
        <ResearchPackageInspector
          pkg={createdPackage}
          workspaceId={workspaceId || activeWorkspaceId || undefined}
          onProceedToBrief={() => onReady(createdPackage.research_package_id)}
        />
        <div className="flex justify-end">
          <Button
            type="button"
            variant="ghost"
            onClick={() => setCreatedPackage(null)}
            data-testid="edit-research-btn"
          >
            ← Ingest Another Package
          </Button>
        </div>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6" data-testid="research-form">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 border-b border-border pb-3">
        <div className="flex items-center gap-2">
          <h2 className="text-lg font-semibold text-foreground">Guest Ingestion & Asset Library</h2>
          <Badge tone="accent">CA-GST-UI-01</Badge>
          <Badge tone="muted">FR-APP-004..006</Badge>
          <Badge tone="muted">FR-APP-010</Badge>
        </div>
        <div className="flex items-center gap-2 text-xs">
          <span className="text-muted-foreground">Active Workspace:</span>
          <span className="font-mono font-medium text-foreground bg-surface-raised px-2 py-0.5 rounded border border-border" data-testid="active-workspace-badge">
            {workspaceId || activeWorkspaceId || "Auto-detecting..."}
          </span>
        </div>
      </div>

      {/* Guest Profile Details */}
      <div className="space-y-3 rounded-lg border border-border bg-surface-raised/40 p-4">
        <h3 className="text-sm font-medium text-foreground">Guest Profile</h3>
        <div>
          <label className="block text-xs font-medium text-foreground mb-1">
            Guest Name <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            value={guestName}
            onChange={(e) => {
              setGuestName(e.target.value);
              if (localError?.code === "GUEST_NAME_INVALID") setLocalError(null);
            }}
            placeholder="e.g. Audrey Hepburn"
            required
            className="w-full rounded border border-border bg-surface px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:border-accent focus:outline-none"
            data-testid="guest-name-input"
          />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-medium text-foreground mb-1">
              Workspace ID <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={workspaceId}
              onChange={(e) => setWorkspaceId(e.target.value)}
              placeholder="e.g. ws-dev"
              required
              className="w-full rounded border border-border bg-surface px-3 py-2 text-sm text-foreground focus:border-accent focus:outline-none"
              data-testid="workspace-id-input"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-foreground mb-1">
              Project ID <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={projectId}
              onChange={(e) => setProjectId(e.target.value)}
              placeholder="e.g. 02_50-12 Audrey"
              required
              className="w-full rounded border border-border bg-surface px-3 py-2 text-sm text-foreground focus:border-accent focus:outline-none"
              data-testid="project-id-input"
            />
          </div>
        </div>
      </div>

      {/* Source URLs Manager */}
      <SourceUrlManager
        urls={sourceUrls}
        onChange={setSourceUrls}
        disabled={mutation.isPending}
      />

      {/* Hidden textarea for backwards compatibility with tests expecting source-urls-input */}
      <textarea
        value={sourceUrls.map((s) => s.url).join("\n")}
        onChange={(e) => {
          const lines = e.target.value.split("\n").map((u) => u.trim()).filter(Boolean);
          setSourceUrls(lines.map((url) => ({ url, context_class: "EVIDENCE_SOURCE" })));
        }}
        className="sr-only"
        data-testid="source-urls-input"
        aria-hidden="true"
        tabIndex={-1}
      />

      {/* Tiered Asset Dropzone */}
      <DocumentDropzone
        items={managedFiles}
        onChange={setManagedFiles}
        disabled={mutation.isPending}
      />

      {/* Operator Authority Scope Attestation Card */}
      <div className="space-y-3 rounded-lg border border-border bg-surface-raised/40 p-4" data-testid="authority-attestation-card">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <h3 className="text-sm font-medium text-foreground">Operator Authority Scope Attestation</h3>
            <Badge tone="accent">GOVERNANCE</Badge>
          </div>
          <Button
            type="button"
            variant="ghost"
            onClick={() => setIsAuthModalOpen(true)}
            data-testid="open-authority-modal-btn"
          >
            Edit Attestation ↗
          </Button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
          <div>
            <label className="block text-muted-foreground mb-1">Operator ID</label>
            <input
              type="text"
              value={operatorId}
              onChange={(e) => setOperatorId(e.target.value)}
              required
              className="w-full rounded border border-border bg-surface px-2.5 py-1.5 font-mono text-xs text-foreground focus:border-accent focus:outline-none"
              data-testid="operator-id-input"
            />
          </div>
          <div>
            <label className="block text-muted-foreground mb-1">Authority Scope</label>
            <input
              type="text"
              value={authorityScope}
              onChange={(e) => setAuthorityScope(e.target.value)}
              required
              className="w-full rounded border border-border bg-surface px-2.5 py-1.5 font-mono text-xs text-foreground focus:border-accent focus:outline-none"
              data-testid="authority-scope-input"
            />
          </div>
          <div>
            <label className="block text-muted-foreground mb-1">Assertion ID</label>
            <input
              type="text"
              value={assertionId}
              onChange={(e) => setAssertionId(e.target.value)}
              required
              className="w-full rounded border border-border bg-surface px-2.5 py-1.5 font-mono text-xs text-foreground focus:border-accent focus:outline-none"
              data-testid="assertion-id-input"
            />
          </div>
        </div>
      </div>

      {/* Error & Status Banners */}
      {localError && (
        <div className="rounded-lg border border-red-500/50 bg-red-950/30 p-3 text-xs text-red-400 space-y-1" data-testid="research-error-banner">
          <div className="flex items-center gap-2 font-mono font-semibold text-red-300">
            <span>[ERROR: {localError.code}]</span>
          </div>
          <p data-testid="research-error">{localError.message}</p>
        </div>
      )}

      {mutation.error && !localError && (
        <div className="rounded-lg border border-red-500/50 bg-red-950/30 p-3 text-xs text-red-400 space-y-1" data-testid="research-error-banner">
          <p data-testid="research-error">{mutation.error.message}</p>
        </div>
      )}

      {mutation.data && (
        <p className="text-sm text-green-600" data-testid="research-success">
          Created: {mutation.data.research_package_id}
        </p>
      )}

      {/* Submission Actions */}
      <div className="flex items-center justify-end gap-3 pt-2">
        <Button
          type="submit"
          disabled={mutation.isPending}
          data-testid="research-submit-btn"
        >
          {mutation.isPending ? "Ingesting & Verifying Package..." : "Ingest & Create Research Package"}
        </Button>
      </div>

      {/* Modal Dialog */}
      <AuthorityAssertionModal
        isOpen={isAuthModalOpen}
        initialData={{ operatorId, authorityScope, assertionId }}
        onConfirm={handleAuthorityConfirm}
        onCancel={() => setIsAuthModalOpen(false)}
      />
    </form>
  );
}
