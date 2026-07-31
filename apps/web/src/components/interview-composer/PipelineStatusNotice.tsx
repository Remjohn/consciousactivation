import { Card } from "../ui/Card";
import { Badge } from "../ui/Badge";

export function PipelineStatusNotice() {
  return (
    <Card className="border-dashed">
      <div className="flex items-start gap-2">
        <Badge tone="muted">Blocked</Badge>
        <p className="text-sm text-muted-foreground">
          Briefs created here are not yet eligible for Brief-led interview
          admission. Producing a real tension-hypothesis pipeline
          (<code>iac_ref</code>, <code>planned_aip_ref</code>,{" "}
          <code>arm_receipt_ref</code>) is tracked as GAP-007 in{" "}
          <code>SPEC_GAP_LEDGER.md</code> and is not part of this release.
        </p>
      </div>
    </Card>
  );
}
