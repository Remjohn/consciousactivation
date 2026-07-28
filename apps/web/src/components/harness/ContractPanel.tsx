interface ContractPanelProps {
  readonly input: Record<string, unknown>;
  readonly output: Record<string, unknown>;
}

export function ContractPanel({ input, output }: ContractPanelProps) {
  return (
    <section className="mt-6">
      <h2 className="font-semibold text-foreground">Contracts</h2>
      <details className="mt-2" open>
        <summary className="cursor-pointer text-sm text-foreground">Input contract</summary>
        <pre className="mt-1 overflow-x-auto rounded-md border border-border bg-surface p-3 text-xs">
          {JSON.stringify(input, null, 2)}
        </pre>
      </details>
      <details className="mt-2" open>
        <summary className="cursor-pointer text-sm text-foreground">Output contract</summary>
        <pre className="mt-1 overflow-x-auto rounded-md border border-border bg-surface p-3 text-xs">
          {JSON.stringify(output, null, 2)}
        </pre>
      </details>
    </section>
  );
}
