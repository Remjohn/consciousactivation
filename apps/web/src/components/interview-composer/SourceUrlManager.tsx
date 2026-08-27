import { useState } from "react";
import type { ContextClass, SourceUrlItem } from "../../api/types";
import { CONTEXT_CLASSES } from "../../api/types";
import { Button } from "../ui/Button";
import { Badge } from "../ui/Badge";

interface SourceUrlManagerProps {
  readonly urls: readonly SourceUrlItem[];
  readonly onChange: (urls: SourceUrlItem[]) => void;
  readonly disabled?: boolean;
}

const URL_REGEX = /^https?:\/\/[a-zA-Z0-9][-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_+.~#?&//=]*)$/;

export function SourceUrlManager({ urls, onChange, disabled = false }: SourceUrlManagerProps) {
  const [inputUrl, setInputUrl] = useState("");
  const [selectedClass, setSelectedClass] = useState<ContextClass>("EVIDENCE_SOURCE");
  const [error, setError] = useState<string | null>(null);

  function handleAdd() {
    setError(null);
    const trimmed = inputUrl.trim();
    if (!trimmed) {
      setError("Please enter a URL");
      return;
    }
    if (!URL_REGEX.test(trimmed)) {
      setError("Invalid URL format. Must start with http:// or https://");
      return;
    }
    if (urls.some((item) => item.url.toLowerCase() === trimmed.toLowerCase())) {
      setError("This URL has already been added");
      return;
    }

    onChange([...urls, { url: trimmed, context_class: selectedClass }]);
    setInputUrl("");
  }

  function handleRemove(index: number) {
    onChange(urls.filter((_, i) => i !== index));
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") {
      e.preventDefault();
      handleAdd();
    }
  }

  return (
    <div className="space-y-3" data-testid="source-url-manager">
      <div className="flex items-center justify-between">
        <label className="text-sm font-medium text-foreground">
          Source URLs & Reference Research
        </label>
        <span className="text-xs text-muted-foreground">{urls.length} added</span>
      </div>

      <div className="flex flex-col gap-2 sm:flex-row">
        <input
          type="url"
          value={inputUrl}
          onChange={(e) => {
            setInputUrl(e.target.value);
            if (error) setError(null);
          }}
          onKeyDown={handleKeyDown}
          placeholder="https://example.com/source-or-bio"
          disabled={disabled}
          className="flex-1 rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:border-accent focus:outline-none"
          data-testid="source-url-input"
        />

        <select
          value={selectedClass}
          onChange={(e) => setSelectedClass(e.target.value as ContextClass)}
          disabled={disabled}
          className="rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground focus:border-accent focus:outline-none"
          data-testid="source-url-class-select"
        >
          {CONTEXT_CLASSES.filter((c) => c !== "CAPTION_TRACK").map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>

        <Button
          type="button"
          onClick={handleAdd}
          disabled={disabled || !inputUrl.trim()}
          data-testid="source-url-add-btn"
        >
          Add URL
        </Button>
      </div>

      {error && (
        <p className="text-xs text-red-500" data-testid="source-url-error">
          {error}
        </p>
      )}

      {urls.length > 0 && (
        <ul className="space-y-1.5 rounded border border-border bg-surface-raised/40 p-2" data-testid="source-url-list">
          {urls.map((item, idx) => (
            <li
              key={`${item.url}-${idx}`}
              className="flex items-center justify-between gap-2 rounded px-2 py-1 text-sm hover:bg-surface-elevated"
              data-testid="source-url-item"
            >
              <div className="flex items-center gap-2 overflow-hidden">
                <Badge tone="accent">{item.context_class}</Badge>
                <a
                  href={item.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="truncate text-accent hover:underline text-xs"
                >
                  {item.url}
                </a>
              </div>
              <button
                type="button"
                onClick={() => handleRemove(idx)}
                disabled={disabled}
                className="text-xs text-muted-foreground hover:text-red-500"
                data-testid="source-url-remove-btn"
                aria-label={`Remove URL ${item.url}`}
              >
                ×
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
