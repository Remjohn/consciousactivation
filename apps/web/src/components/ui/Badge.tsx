import type { ReactNode } from "react";

export type BadgeTone = "accent" | "success" | "danger" | "muted";

interface BadgeProps {
  readonly children: ReactNode;
  readonly tone?: BadgeTone;
  readonly "data-testid"?: string;
}

const TONE_CLASS: Record<BadgeTone, string> = {
  accent: "border-accent text-accent",
  success: "border-success text-success",
  danger: "border-danger text-danger",
  muted: "border-border text-muted-foreground",
};

export function Badge({ children, tone = "muted", "data-testid": testId }: BadgeProps) {
  return (
    <span
      data-testid={testId}
      className={`inline-flex items-center rounded-full border px-2 py-0.5 text-xs ${TONE_CLASS[tone]}`}
    >
      {children}
    </span>
  );
}
