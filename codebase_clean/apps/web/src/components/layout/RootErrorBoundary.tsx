import type { ErrorComponentProps } from "@tanstack/react-router";

export function RootErrorBoundary({ error, reset }: ErrorComponentProps) {
  const message = error instanceof Error ? error.message : String(error);

  return (
    <div className="p-8" role="alert">
      <p className="text-lg font-semibold text-danger">Something went wrong</p>
      <p className="mt-2 text-sm text-muted-foreground">{message}</p>
      <button
        type="button"
        onClick={reset}
        className="mt-4 rounded-md border border-border px-3 py-1.5 text-sm text-foreground hover:bg-surface-elevated"
      >
        Reload this page
      </button>
    </div>
  );
}
