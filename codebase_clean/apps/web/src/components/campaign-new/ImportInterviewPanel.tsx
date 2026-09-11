import { useState, useRef } from "react";
import { useImportInterview } from "../../hooks/useImportInterview";
import type { ImportInterviewResponse } from "../../api/types";

interface ImportInterviewPanelProps {
  onReady: (packageId: string) => void;
}

export function ImportInterviewPanel({ onReady }: ImportInterviewPanelProps) {
  const [video, setVideo] = useState<File | null>(null);
  const [transcript, setTranscript] = useState<File | null>(null);
  const [workspaceId, setWorkspaceId] = useState("");
  const [projectId, setProjectId] = useState("");
  const [operatorId, setOperatorId] = useState("");
  const [authorityScope, setAuthorityScope] = useState("");
  const [assertionId, setAssertionId] = useState("");
  const [transcriptFormat, setTranscriptFormat] = useState<"PRE_ALIGNED_JSON" | "SRT">("PRE_ALIGNED_JSON");
  const [speakerId, setSpeakerId] = useState("");
  const [visualProfileId, setVisualProfileId] = useState("");

  const videoInputRef = useRef<HTMLInputElement>(null);
  const transcriptInputRef = useRef<HTMLInputElement>(null);

  const importMutation = useImportInterview();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!video || !transcript) return;

    const result = await importMutation.mutateAsync({
      video,
      transcript,
      workspace_id: workspaceId,
      project_id: projectId,
      operator_id: operatorId,
      authority_scope: authorityScope,
      assertion_id: assertionId,
      transcript_format: transcriptFormat,
      speaker_id: speakerId || undefined,
      visual_profile_id: visualProfileId || undefined,
    });

    if (result) {
      onReady(result.package_id);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="rounded-[var(--radius-card)] border border-border-subtle bg-surface p-6" data-testid="import-form">
      <h3 className="text-ink-primary text-lg font-semibold">Import New Interview</h3>

      {/* File dropzones */}
      <div className="mt-4 grid grid-cols-2 gap-4">
        <div
          className="flex flex-col items-center justify-center rounded border-2 border-dashed border-border-subtle p-6 cursor-pointer hover:border-gold"
          onClick={() => videoInputRef.current?.click()}
        >
          <span className="text-ink-muted text-sm">{video ? video.name : "Drop video file"}</span>
          <input ref={videoInputRef} type="file" accept="video/*" className="hidden" onChange={(e) => e.target.files && setVideo(e.target.files[0])} data-testid="video-input" />
        </div>
        <div
          className="flex flex-col items-center justify-center rounded border-2 border-dashed border-border-subtle p-6 cursor-pointer hover:border-gold"
          onClick={() => transcriptInputRef.current?.click()}
        >
          <span className="text-ink-muted text-sm">{transcript ? transcript.name : "Drop transcript file"}</span>
          <input ref={transcriptInputRef} type="file" accept=".json,.srt" className="hidden" onChange={(e) => e.target.files && setTranscript(e.target.files[0])} data-testid="transcript-input" />
        </div>
      </div>

      {/* Form fields */}
      <div className="mt-4 grid grid-cols-2 gap-4">
        <input type="text" value={workspaceId} onChange={(e) => setWorkspaceId(e.target.value)} placeholder="Workspace ID" className="rounded border border-border-subtle bg-surface-raised px-3 py-2 text-sm text-ink-primary placeholder:text-ink-faint" data-testid="workspace-id-input" required />
        <input type="text" value={projectId} onChange={(e) => setProjectId(e.target.value)} placeholder="Project ID" className="rounded border border-border-subtle bg-surface-raised px-3 py-2 text-sm text-ink-primary placeholder:text-ink-faint" data-testid="project-id-input" required />
        <input type="text" value={operatorId} onChange={(e) => setOperatorId(e.target.value)} placeholder="Operator ID" className="rounded border border-border-subtle bg-surface-raised px-3 py-2 text-sm text-ink-primary placeholder:text-ink-faint" data-testid="operator-id-input" required />
        <input type="text" value={authorityScope} onChange={(e) => setAuthorityScope(e.target.value)} placeholder="Authority Scope" className="rounded border border-border-subtle bg-surface-raised px-3 py-2 text-sm text-ink-primary placeholder:text-ink-faint" data-testid="authority-scope-input" required />
        <input type="text" value={assertionId} onChange={(e) => setAssertionId(e.target.value)} placeholder="Assertion ID" className="rounded border border-border-subtle bg-surface-raised px-3 py-2 text-sm text-ink-primary placeholder:text-ink-faint" data-testid="assertion-id-input" required />
        <select value={transcriptFormat} onChange={(e) => setTranscriptFormat(e.target.value as "PRE_ALIGNED_JSON" | "SRT")} className="rounded border border-border-subtle bg-surface-raised px-3 py-2 text-sm text-ink-primary" data-testid="transcript-format-select">
          <option value="PRE_ALIGNED_JSON">PRE_ALIGNED_JSON</option>
          <option value="SRT">SRT</option>
        </select>
        <input type="text" value={speakerId} onChange={(e) => setSpeakerId(e.target.value)} placeholder="Speaker ID (optional)" className="rounded border border-border-subtle bg-surface-raised px-3 py-2 text-sm text-ink-primary placeholder:text-ink-faint" data-testid="speaker-id-input" />
        <input type="text" value={visualProfileId} onChange={(e) => setVisualProfileId(e.target.value)} placeholder="Visual Profile ID (optional)" className="rounded border border-border-subtle bg-surface-raised px-3 py-2 text-sm text-ink-primary placeholder:text-ink-faint" data-testid="visual-profile-id-input" />
      </div>

      {importMutation.error && (
        <div className="mt-3 rounded border border-state-blocked/50 bg-state-blocked/10 p-3 text-sm text-state-blocked" data-testid="import-error">
          {importMutation.error.error_code}: {importMutation.error.message}
        </div>
      )}

      <button
        type="submit"
        disabled={!video || !transcript || importMutation.isPending}
        className="mt-4 rounded-full bg-gold px-5 py-2.5 font-semibold text-gold-on disabled:opacity-40"
        data-testid="import-submit-btn"
      >
        {importMutation.isPending ? "Importing..." : "Import Interview"}
      </button>
    </form>
  );
}
