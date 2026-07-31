import { useState, useRef } from "react";
import { useCreateResearchPackage } from "../../hooks/useCreateResearchPackage";
import type { CreateResearchPackageInput } from "../../api/interviewComposer";
import { Button } from "../ui/Button";
import { Badge } from "../ui/Badge";

interface ResearchPanelProps {
  onReady: (researchPackageId: string) => void;
}

export function ResearchPanel({ onReady }: ResearchPanelProps) {
  const [guestName, setGuestName] = useState("");
  const [sourceUrls, setSourceUrls] = useState("");
  const [documents, setDocuments] = useState<File[]>([]);
  const [workspaceId, setWorkspaceId] = useState("");
  const [projectId, setProjectId] = useState("");
  const [operatorId, setOperatorId] = useState("");
  const [authorityScope, setAuthorityScope] = useState("");
  const [assertionId, setAssertionId] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const mutation = useCreateResearchPackage();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const input: CreateResearchPackageInput = {
      guestName,
      sourceUrls: sourceUrls.split("\n").map((u) => u.trim()).filter(Boolean),
      documents,
      workspaceId,
      projectId,
      operatorId,
      authorityScope,
      assertionId,
    };
    const result = await mutation.mutateAsync(input);
    onReady(result.research_package_id);
  }

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    if (e.target.files) {
      setDocuments(Array.from(e.target.files));
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4" data-testid="research-form">
      <div className="flex items-center gap-2">
        <h2 className="text-lg font-semibold text-foreground">Guest Research Package</h2>
        <Badge tone="muted">FR-APP-010</Badge>
      </div>

      <input
        type="text" value={guestName} onChange={(e) => setGuestName(e.target.value)}
        placeholder="Guest name" required
        className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground"
        data-testid="guest-name-input"
      />
      <textarea
        value={sourceUrls} onChange={(e) => setSourceUrls(e.target.value)}
        placeholder="Source URLs (one per line)"
        rows={3}
        className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground"
        data-testid="source-urls-input"
      />
      <div
        className="cursor-pointer rounded border-2 border-dashed border-border p-4 text-center text-sm text-muted-foreground"
        onClick={() => fileInputRef.current?.click()}
        data-testid="documents-dropzone"
      >
        {documents.length > 0 ? `${documents.length} document(s) selected` : "Click to upload documents"}
        <input ref={fileInputRef} type="file" multiple className="hidden" onChange={handleFileChange} data-testid="documents-input" />
      </div>
      <input type="text" value={workspaceId} onChange={(e) => setWorkspaceId(e.target.value)} placeholder="Workspace ID" required className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground" data-testid="workspace-id-input" />
      <input type="text" value={projectId} onChange={(e) => setProjectId(e.target.value)} placeholder="Project ID" required className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground" data-testid="project-id-input" />
      <input type="text" value={operatorId} onChange={(e) => setOperatorId(e.target.value)} placeholder="Operator ID" required className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground" data-testid="operator-id-input" />
      <input type="text" value={authorityScope} onChange={(e) => setAuthorityScope(e.target.value)} placeholder="Authority Scope" required className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground" data-testid="authority-scope-input" />
      <input type="text" value={assertionId} onChange={(e) => setAssertionId(e.target.value)} placeholder="Assertion ID" required className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground" data-testid="assertion-id-input" />

      {mutation.error && (
        <p className="text-sm text-red-600" data-testid="research-error">{mutation.error.message}</p>
      )}
      {mutation.data && (
        <p className="text-sm text-green-600" data-testid="research-success">
          Created: {mutation.data.research_package_id}
        </p>
      )}

      <Button type="submit" disabled={mutation.isPending} data-testid="research-submit-btn">
        {mutation.isPending ? "Creating..." : "Create Research Package"}
      </Button>
    </form>
  );
}
