import type { ButtonHTMLAttributes } from "react";

type ButtonVariant = "solid" | "ghost";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  readonly variant?: ButtonVariant;
}

const VARIANT_CLASS: Record<ButtonVariant, string> = {
  solid: "bg-accent-solid text-accent-foreground hover:brightness-110",
  ghost: "border border-border text-foreground hover:bg-surface-elevated",
};

export function Button({ variant = "solid", className = "", ...props }: ButtonProps) {
  return (
    <button
      className={`rounded-md px-3 py-1.5 text-sm font-medium transition-colors ${VARIANT_CLASS[variant]} ${className}`}
      {...props}
    />
  );
}
