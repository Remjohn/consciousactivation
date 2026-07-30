import type { TextareaHTMLAttributes } from "react";

/**
 * UI primitive matching the contract of {@link Button} / {@link Badge}:
 * a single styled form control surfacing the native attribute set with no
 * extra abstraction. Used first by TS-APP-UI-003's RevisionComposer; kept in
 * `components/ui/` so later form-bearing pages (e.g. CampaignNew-style flows)
 * reach for it instead of an inline `<textarea>`.
 */
export function Textarea({ className = "", ...props }: TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea
      className={`rounded-md border border-border bg-surface px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:border-accent focus:outline-none ${className}`}
      {...props}
    />
  );
}
