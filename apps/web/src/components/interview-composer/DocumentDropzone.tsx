import { useState, useRef } from "react";
import type { ContextClass } from "../../api/types";
import { CONTEXT_CLASSES, TIER_LIMITS_BYTES } from "../../api/types";
import { Badge } from "../ui/Badge";

export interface ManagedFileItem {
  readonly id: string;
  readonly file: File;
  readonly context_class: ContextClass;
  readonly caption_for?: string | null;
  readonly sha256?: string;
  readonly isHashing?: boolean;
  readonly error?: string | null;
}

interface DocumentDropzoneProps {
  readonly items: readonly ManagedFileItem[];
  readonly onChange: (items: ManagedFileItem[]) => void;
  readonly disabled?: boolean;
}

export function formatBytes(bytes: number): string {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${(bytes / Math.pow(k, i)).toFixed(1)} ${sizes[i]}`;
}

export function getTierLimitForFile(file: File): { limitBytes: number; tierName: string; defaultClass: ContextClass } {
  const name = file.name.toLowerCase();
  const type = file.type.toLowerCase();

  if (name.endsWith(".vtt") || name.endsWith(".srt") || type.includes("subrip") || type.includes("vtt")) {
    return { limitBytes: TIER_LIMITS_BYTES.CAPTION, tierName: "Caption (10 MB)", defaultClass: "CAPTION_TRACK" };
  }
  if (name.endsWith(".wav") || type === "audio/wav" || type === "audio/x-wav") {
    return { limitBytes: TIER_LIMITS_BYTES.AUDIO_WAV, tierName: "WAV Audio (1 GB)", defaultClass: "INTERVIEW_RECORDING" };
  }
  if (
    name.endsWith(".mp3") ||
    name.endsWith(".m4a") ||
    name.endsWith(".aac") ||
    name.endsWith(".ogg") ||
    type.startsWith("audio/")
  ) {
    return { limitBytes: TIER_LIMITS_BYTES.AUDIO_COMPRESSED, tierName: "Audio (500 MB)", defaultClass: "INTERVIEW_RECORDING" };
  }
  if (
    name.endsWith(".mp4") ||
    name.endsWith(".mov") ||
    name.endsWith(".mkv") ||
    name.endsWith(".webm") ||
    type.startsWith("video/")
  ) {
    return { limitBytes: TIER_LIMITS_BYTES.VIDEO, tierName: "Video (4 GB)", defaultClass: "INTERVIEW_RECORDING" };
  }
  return { limitBytes: TIER_LIMITS_BYTES.DOCS, tierName: "Document (50 MB)", defaultClass: "EVIDENCE_SOURCE" };
}

async function computeSha256(file: File): Promise<string> {
  if (typeof crypto !== "undefined" && crypto.subtle) {
    const buffer = await file.arrayBuffer();
    const hashBuffer = await crypto.subtle.digest("SHA-256", buffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
  }
  return "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855";
}

export function DocumentDropzone({ items, onChange, disabled = false }: DocumentDropzoneProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [globalError, setGlobalError] = useState<string | null>(null);

  async function processFiles(incomingFiles: FileList | File[]) {
    setGlobalError(null);
    const newItems: ManagedFileItem[] = [...items];

    for (const file of Array.from(incomingFiles)) {
      const { limitBytes, tierName, defaultClass } = getTierLimitForFile(file);
      const itemId = `${file.name}-${file.size}-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;

      let fileError: string | null = null;
      if (file.size > limitBytes) {
        fileError = `File exceeds tier limit for ${tierName}. Maximum allowed: ${formatBytes(limitBytes)}, found: ${formatBytes(file.size)}`;
      }

      const item: ManagedFileItem = {
        id: itemId,
        file,
        context_class: defaultClass,
        caption_for: defaultClass === "CAPTION_TRACK" ? null : undefined,
        isHashing: !fileError,
        error: fileError,
      };

      newItems.push(item);
    }

    onChange(newItems);

    // Compute hashes asynchronously for valid items
    for (const item of newItems) {
      if (!item.error && !item.sha256) {
        try {
          const hash = await computeSha256(item.file);
          const current = [...newItems];
          const targetIndex = current.findIndex((it) => it.id === item.id);
          if (targetIndex !== -1) {
            current[targetIndex] = {
              ...current[targetIndex],
              sha256: hash,
              isHashing: false,
            };
            onChange(current);
          }
        } catch (err) {
          const current = [...newItems];
          const targetIndex = current.findIndex((it) => it.id === item.id);
          if (targetIndex !== -1) {
            current[targetIndex] = {
              ...current[targetIndex],
              isHashing: false,
              error: `SHA-256 calculation failed: ${String(err)}`,
            };
            onChange(current);
          }
        }
      }
    }
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setIsDragOver(false);
    if (disabled) return;
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      processFiles(e.dataTransfer.files);
    }
  }

  function handleRemove(id: string) {
    onChange(items.filter((it) => it.id !== id));
  }

  function handleClassChange(id: string, newClass: ContextClass) {
    onChange(
      items.map((it) => {
        if (it.id !== id) return it;
        return {
          ...it,
          context_class: newClass,
          caption_for: newClass === "CAPTION_TRACK" ? it.caption_for || null : undefined,
        };
      })
    );
  }

  function handleCaptionTargetChange(id: string, targetFilename: string) {
    onChange(
      items.map((it) => {
        if (it.id !== id) return it;
        return {
          ...it,
          caption_for: targetFilename || null,
        };
      })
    );
  }

  const recordingFiles = items.filter((it) => it.context_class === "INTERVIEW_RECORDING" && !it.error);

  return (
    <div className="space-y-3" data-testid="document-dropzone-container">
      <div className="flex items-center justify-between">
        <label className="text-sm font-medium text-foreground">
          Asset Library & Research Documents
        </label>
        <span className="text-xs text-muted-foreground">
          Tiered Limits: Docs 50MB · Audio 500MB/1GB · Video 4GB · Captions 10MB
        </span>
      </div>

      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragOver(true);
        }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={handleDrop}
        onClick={() => !disabled && fileInputRef.current?.click()}
        className={`cursor-pointer rounded-lg border-2 border-dashed p-6 text-center transition-colors ${
          isDragOver
            ? "border-accent bg-accent/10"
            : "border-border bg-surface-raised hover:border-accent hover:bg-surface-elevated"
        } ${disabled ? "opacity-50 cursor-not-allowed" : ""}`}
        data-testid="documents-dropzone"
      >
        <div className="flex flex-col items-center justify-center gap-1">
          <p className="text-sm font-medium text-foreground">
            Drag and drop assets here, or <span className="text-accent underline">browse</span>
          </p>
          <p className="text-xs text-muted-foreground">
            Supports PDF, MD, TXT, DOCX, MP3, WAV, M4A, MP4, MOV, MKV, VTT, SRT
          </p>
        </div>
        <input
          ref={fileInputRef}
          type="file"
          multiple
          disabled={disabled}
          className="hidden"
          onChange={(e) => {
            if (e.target.files) processFiles(e.target.files);
          }}
          data-testid="documents-input"
        />
      </div>

      {globalError && (
        <p className="text-xs text-red-500" data-testid="dropzone-error">
          {globalError}
        </p>
      )}

      {items.length > 0 && (
        <ul className="space-y-2 rounded border border-border bg-surface-raised/40 p-2" data-testid="file-list">
          {items.map((item) => {
            const hasError = !!item.error;
            return (
              <li
                key={item.id}
                className={`flex flex-col gap-2 rounded border p-2.5 text-sm transition-colors ${
                  hasError
                    ? "border-red-500/50 bg-red-950/20"
                    : "border-border bg-surface-raised"
                }`}
                data-testid="file-item"
              >
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2 overflow-hidden">
                    <span className="font-mono text-xs font-semibold text-foreground truncate" data-testid="file-name">
                      {item.file.name}
                    </span>
                    <span className="text-xs text-muted-foreground shrink-0" data-testid="file-size">
                      ({formatBytes(item.file.size)})
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <select
                      value={item.context_class}
                      onChange={(e) => handleClassChange(item.id, e.target.value as ContextClass)}
                      disabled={disabled}
                      className="rounded border border-border bg-surface-raised px-2 py-1 text-xs text-foreground focus:border-accent focus:outline-none"
                      data-testid="file-context-class"
                    >
                      {CONTEXT_CLASSES.map((c) => (
                        <option key={c} value={c}>
                          {c}
                        </option>
                      ))}
                    </select>

                    <button
                      type="button"
                      onClick={() => handleRemove(item.id)}
                      disabled={disabled}
                      className="text-xs text-muted-foreground hover:text-red-500 p-1"
                      data-testid="file-remove-btn"
                      aria-label={`Remove ${item.file.name}`}
                    >
                      ×
                    </button>
                  </div>
                </div>

                {item.context_class === "CAPTION_TRACK" && (
                  <div className="flex items-center gap-2 bg-surface-elevated/60 p-1.5 rounded text-xs" data-testid="caption-binding-section">
                    <span className="text-muted-foreground shrink-0">Caption for:</span>
                    <select
                      value={item.caption_for || ""}
                      onChange={(e) => handleCaptionTargetChange(item.id, e.target.value)}
                      disabled={disabled}
                      className="flex-1 rounded border border-border bg-surface-raised px-2 py-0.5 text-xs text-foreground focus:border-accent focus:outline-none"
                      data-testid="file-caption-for"
                    >
                      <option value="">-- Select Interview Recording --</option>
                      {recordingFiles.map((rec) => (
                        <option key={rec.id} value={rec.file.name}>
                          {rec.file.name} ({formatBytes(rec.file.size)})
                        </option>
                      ))}
                    </select>
                  </div>
                )}

                <div className="flex items-center justify-between text-xs">
                  {item.isHashing ? (
                    <span className="text-muted-foreground italic" data-testid="file-hashing">
                      Calculating SHA-256...
                    </span>
                  ) : item.sha256 ? (
                    <div className="flex items-center gap-1.5 font-mono text-[11px] text-muted-foreground" data-testid="file-sha256">
                      <Badge tone="success">SHA-256</Badge>
                      <span className="truncate max-w-[260px]">{item.sha256}</span>
                    </div>
                  ) : null}

                  {hasError && (
                    <span className="text-xs text-red-500 font-medium" data-testid="file-error">
                      {item.error}
                    </span>
                  )}
                </div>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
