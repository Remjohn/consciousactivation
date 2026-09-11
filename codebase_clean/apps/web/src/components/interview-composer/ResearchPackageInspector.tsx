import { useState } from "react";
import type { ContextClass, GuestResearchPackageResponse, UploadedDocumentSummary } from "../../api/types";
import { CONTEXT_CLASSES } from "../../api/types";
import { Badge } from "../ui/Badge";
import { Button } from "../ui/Button";
import { formatBytes } from "./DocumentDropzone";

interface ResearchPackageInspectorProps {
  readonly pkg: GuestResearchPackageResponse;
  readonly workspaceId?: string;
  readonly onProceedToBrief?: () => void;
}

const DOCTRINAL_SOURCES: Record<ContextClass, string> = {
  IDENTITY_DNA: "PRD §1.2 / CA-CAN-01B: Core Guest Persona & Biological/Biographical Grounding",
  CONTEXT_PREMISE: "PRD §1.2 / CA-CAN-01B: Situational Background & Episode Context",
  RESONANCE_REFERENCE: "PRD §1.2 / CA-CAN-01B: Aesthetic, Rhythm & Emotional Reference",
  BRAND_VOICE: "PRD §1.2 / CA-CAN-01B: Brand Identity, Tone & Style Guidelines",
  EVIDENCE_SOURCE: "PRD §1.2 / CA-CAN-01B: Supporting Research, Documents & Data",
  INTERVIEW_RECORDING: "PRD §1.2 / CA-CAN-01B: Master Audio/Video Media Source",
  CAPTION_TRACK: "Mandate 28 Amendment: Timed Captions & Transcripts (.vtt/.srt)",
};

export function ResearchPackageInspector({
  pkg,
  workspaceId,
  onProceedToBrief,
}: ResearchPackageInspectorProps) {
  const [selectedFilter, setSelectedFilter] = useState<ContextClass | "ALL">("ALL");
  const [copied, setCopied] = useState(false);

  function copyPackageId() {
    navigator.clipboard.writeText(pkg.research_package_id);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  // Group documents by context_class
  const docsByClass: Partial<Record<ContextClass, UploadedDocumentSummary[]>> = {};
  for (const doc of pkg.uploaded_documents) {
    const cls: ContextClass = doc.context_class || (
      doc.original_filename.toLowerCase().endsWith(".vtt") || doc.original_filename.toLowerCase().endsWith(".srt")
        ? "CAPTION_TRACK"
        : "EVIDENCE_SOURCE"
    );
    if (!docsByClass[cls]) docsByClass[cls] = [];
    docsByClass[cls]!.push(doc);
  }

  const activeClasses = CONTEXT_CLASSES.filter(
    (c) => (docsByClass[c] && docsByClass[c]!.length > 0) || (c === "EVIDENCE_SOURCE" && pkg.source_urls.length > 0)
  );

  const displayedClasses =
    selectedFilter === "ALL"
      ? CONTEXT_CLASSES.filter((c) => docsByClass[c]?.length || (c === "EVIDENCE_SOURCE" && pkg.source_urls.length > 0))
      : [selectedFilter];

  return (
    <div className="space-y-6 rounded-xl border border-border bg-surface p-5 shadow-sm" data-testid="research-inspector">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between border-b border-border pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-base font-semibold text-foreground">Verified Research Package</h3>
            <Badge tone="success">REV {pkg.revision}</Badge>
            {pkg.idempotent_replay && <Badge tone="muted">IDEMPOTENT REPLAY</Badge>}
          </div>
          <div className="flex flex-wrap items-center gap-3 mt-1 text-xs text-muted-foreground">
            <span>
              Guest: <strong className="text-foreground" data-testid="inspector-guest-name">{pkg.guest_name}</strong>
            </span>
            {workspaceId && (
              <span>
                Workspace: <strong className="font-mono text-foreground">{workspaceId}</strong>
              </span>
            )}
            <span>
              Assets: <strong className="text-foreground">{pkg.uploaded_documents.length}</strong>
            </span>
            <span>
              URLs: <strong className="text-foreground">{pkg.source_urls.length}</strong>
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 rounded border border-border bg-surface-raised px-2.5 py-1 text-xs font-mono">
            <span className="text-muted-foreground">ID:</span>
            <span className="truncate max-w-[140px] text-foreground" data-testid="inspector-package-id">
              {pkg.research_package_id}
            </span>
            <button
              type="button"
              onClick={copyPackageId}
              className="text-accent hover:underline ml-1"
              data-testid="copy-package-id-btn"
            >
              {copied ? "Copied!" : "Copy"}
            </button>
          </div>

          {onProceedToBrief && (
            <Button
              type="button"
              variant="solid"
              onClick={onProceedToBrief}
              data-testid="proceed-to-brief-btn"
            >
              Proceed to Brief →
            </Button>
          )}
        </div>
      </div>

      {/* Context Class Filter Chips */}
      <div className="flex flex-wrap items-center gap-1.5 text-xs" data-testid="inspector-filters">
        <button
          type="button"
          onClick={() => setSelectedFilter("ALL")}
          className={`rounded-full px-3 py-1 font-medium transition-colors ${
            selectedFilter === "ALL"
              ? "bg-accent-solid text-accent-foreground"
              : "border border-border bg-surface-raised text-muted-foreground hover:bg-surface-elevated"
          }`}
          data-testid="inspector-filter-ALL"
        >
          All Classes ({pkg.uploaded_documents.length + pkg.source_urls.length})
        </button>

        {activeClasses.map((c) => {
          const count = (docsByClass[c]?.length || 0) + (c === "EVIDENCE_SOURCE" ? pkg.source_urls.length : 0);
          return (
            <button
              key={c}
              type="button"
              onClick={() => setSelectedFilter(c)}
              className={`rounded-full px-3 py-1 font-medium transition-colors ${
                selectedFilter === c
                  ? "bg-accent-solid text-accent-foreground"
                  : "border border-border bg-surface-raised text-muted-foreground hover:bg-surface-elevated"
              }`}
              data-testid={`inspector-filter-${c}`}
            >
              {c} ({count})
            </button>
          );
        })}
      </div>

      {/* Grouped Asset Library */}
      <div className="space-y-6" data-testid="inspector-grouped-sections">
        {displayedClasses.length === 0 ? (
          <p className="text-xs text-muted-foreground italic">No assets registered in this package.</p>
        ) : (
          displayedClasses.map((cls) => {
            const classDocs = docsByClass[cls] || [];
            const isEvidenceSource = cls === "EVIDENCE_SOURCE";
            const showUrls = isEvidenceSource && (selectedFilter === "ALL" || selectedFilter === "EVIDENCE_SOURCE");

            if (classDocs.length === 0 && (!showUrls || pkg.source_urls.length === 0)) {
              return null;
            }

            return (
              <section
                key={cls}
                className="space-y-2.5 rounded-lg border border-border/80 bg-surface-raised/30 p-3.5"
                data-testid={`inspector-group-${cls}`}
              >
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1 border-b border-border/60 pb-2">
                  <div className="flex items-center gap-2">
                    <Badge tone="accent">{cls}</Badge>
                    <h4 className="text-xs font-semibold text-foreground uppercase tracking-wider">
                      {cls.replace("_", " ")}
                    </h4>
                  </div>
                  <span className="text-[11px] text-muted-foreground italic">
                    {DOCTRINAL_SOURCES[cls]}
                  </span>
                </div>

                {/* Uploaded Document Cards */}
                {classDocs.length > 0 && (
                  <ul className="space-y-2 pt-1" data-testid={`inspector-docs-${cls}`}>
                    {classDocs.map((doc) => (
                      <li
                        key={doc.asset_id}
                        className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 rounded border border-border bg-surface-raised p-2.5 text-xs shadow-sm"
                        data-testid="inspector-asset-item"
                      >
                        <div className="space-y-1 overflow-hidden">
                          <div className="flex items-center gap-2">
                            <span className="font-semibold text-foreground font-mono truncate" data-testid="inspector-asset-filename">
                              {doc.original_filename}
                            </span>
                            <span className="text-muted-foreground shrink-0">
                              ({formatBytes(doc.bytes)})
                            </span>
                            <span className="text-[10px] text-muted-foreground bg-surface-elevated px-1.5 py-0.5 rounded shrink-0">
                              {doc.media_type}
                            </span>
                            {doc.caption_for && (
                              <Badge tone="accent">Captions: {doc.caption_for}</Badge>
                            )}
                          </div>
                          <div className="flex items-center gap-1.5 font-mono text-[11px] text-muted-foreground truncate">
                            <span className="text-accent">URI:</span>
                            <span className="truncate">{doc.asset_id}</span>
                          </div>
                        </div>

                        <div className="flex items-center gap-2 shrink-0">
                          <div className="flex items-center gap-1 font-mono text-[11px] text-emerald-400 bg-emerald-950/30 border border-emerald-800/40 px-2 py-1 rounded">
                            <span className="font-semibold">SHA-256:</span>
                            <span className="truncate max-w-[140px]" data-testid="inspector-asset-sha256">
                              {doc.sha256}
                            </span>
                          </div>
                          <Badge tone="success">VERIFIED</Badge>
                        </div>
                      </li>
                    ))}
                  </ul>
                )}

                {/* Source URLs in Evidence Source */}
                {showUrls && pkg.source_urls.length > 0 && (
                  <div className="space-y-1.5 pt-2">
                    <h5 className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wider">
                      Reference URLs ({pkg.source_urls.length})
                    </h5>
                    <ul className="space-y-1" data-testid="inspector-urls-list">
                      {pkg.source_urls.map((url, i) => (
                        <li
                          key={`${url}-${i}`}
                          className="flex items-center justify-between gap-2 rounded bg-surface-raised px-2.5 py-1 text-xs"
                          data-testid="inspector-url-item"
                        >
                          <a
                            href={url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-accent hover:underline truncate"
                          >
                            {url}
                          </a>
                          <Badge tone="muted">URL SOURCE</Badge>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </section>
            );
          })
        )}
      </div>
    </div>
  );
}
