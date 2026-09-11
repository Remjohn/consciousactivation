export function HarnessLibraryEmptyState() {
  return (
    <div className="p-8 text-muted-foreground">
      <p className="text-lg font-semibold text-foreground">
        No Harnesses in this workspace's library yet
      </p>
      <p className="mt-2 text-sm">
        Harnesses are built by the Pi Coding Agent via <code>POST /api/harnesses/build</code> —
        they are not authored in this UI.
      </p>
    </div>
  );
}
