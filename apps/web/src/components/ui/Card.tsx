import type { ReactNode } from "react";

interface CardProps {
  readonly children: ReactNode;
  readonly className?: string;
}

export function Card({ children, className = "" }: CardProps) {
  return (
    <div
      className={`rounded-card border border-border bg-surface p-4 ${className}`}
    >
      {children}
    </div>
  );
}
