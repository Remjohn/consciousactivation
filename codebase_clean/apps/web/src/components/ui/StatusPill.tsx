export type StatusTone = "success" | "danger" | "muted" | "info";

interface StatusPillProps {
  readonly tone: StatusTone;
  readonly label: string;
}

const DOT_CLASS: Record<StatusTone, string> = {
  success: "bg-success",
  danger: "bg-danger",
  muted: "bg-muted-foreground",
  info: "bg-info",
};

const TEXT_CLASS: Record<StatusTone, string> = {
  success: "text-success",
  danger: "text-danger",
  muted: "text-muted-foreground",
  info: "text-info",
};

export function StatusPill({ tone, label }: StatusPillProps) {
  return (
    <span className="inline-flex items-center gap-2 rounded-full border border-border bg-surface-elevated px-3 py-1 text-xs">
      <span className={`h-2 w-2 rounded-full ${DOT_CLASS[tone]}`} aria-hidden="true" />
      <span className={TEXT_CLASS[tone]}>{label}</span>
    </span>
  );
}
