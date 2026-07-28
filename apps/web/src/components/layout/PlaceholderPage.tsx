interface PlaceholderPageProps {
  readonly title: string;
  readonly frRange: string;
  readonly builtIn: string;
}

export function PlaceholderPage({ title, frRange, builtIn }: PlaceholderPageProps) {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-semibold text-foreground">{title}</h1>
      <p className="mt-2 text-sm text-muted-foreground">
        Governed by {frRange}. Built in {builtIn}.
      </p>
    </div>
  );
}
