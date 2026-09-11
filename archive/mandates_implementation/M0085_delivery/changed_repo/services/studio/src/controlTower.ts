import { canonicalSha256, deterministicId } from "./canonical";
import type { ControlTowerProjection } from "./domain";
export function buildControlTowerProjection(input: any): ControlTowerProjection {
  const projected = { ...input, projection_id: input.projection_id ?? deterministicId("control-tower-projection", { campaign_id: input.campaign.campaign_id, version: input.campaign.version }), projection_sha256: canonicalSha256(input), available_actions: Array.from(new Set([...(input.available_actions ?? []), "DIRECT_MANIPULATION", "VISUAL_ASSET_STUDIO"])) };
  return projected as ControlTowerProjection;
}
