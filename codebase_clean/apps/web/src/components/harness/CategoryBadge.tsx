import { Badge } from "../ui/Badge";

export function CategoryBadge({ categoryName }: { readonly categoryName: string | null }) {
  return <Badge tone="muted">{categoryName ?? "Category-neutral"}</Badge>;
}
