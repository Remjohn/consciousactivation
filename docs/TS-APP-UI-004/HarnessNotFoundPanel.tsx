import { Link } from "@tanstack/react-router";

export function HarnessNotFoundPanel() {
  return (
    <div className="p-8">
      <p className="text-lg font-semibold text-foreground">Harness not found</p>
      <p className="mt-2 text-sm text-muted-foreground">
        No Harness exists with this id in the workspace library.
      </p>
      <Link to="/harnesses" className="mt-4 inline-block text-sm text-accent">
        ← Back to library
      </Link>
    </div>
  );
}
