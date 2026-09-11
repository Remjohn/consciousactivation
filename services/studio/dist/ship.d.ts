import type { CampaignState, ShipDecision, ShipRequest } from "./domain.js";
export declare function evaluateShipRequest(request: ShipRequest, campaign: CampaignState): ShipDecision;
