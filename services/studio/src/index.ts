import { resolve } from "node:path";
import type { AuthorityRef, ProductStatusEnvelope } from "./generated/contracts.js";
import { runPhase7Demo } from "./phase7_demo.js";

export * from "./auditExport.js";
export * from "./campaign.js";
export * from "./canonical.js";
export * from "./controlTower.js";
export * from "./domain.js";
export * from "./html.js";
export * from "./resolutions.js";
export * from "./revision.js";
export * from "./rerun.js";
export * from "./ship.js";
export * from "./store.js";
export * from "./surfaces.js";
export * from "./timeline.js";
export * from "./validators.js";

export const PRODUCT_ID = "conscious-activations-studio";
export const PRODUCT_VERSION = "0.7.0-dev.1";

export const CANDIDATE_AUTHORITY: AuthorityRef = {
  authority_id: "ca-program-control-v2.1-candidate",
  authority_version: "2.1.0-candidate",
  authority_sha256: "cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39",
  authority_state: "candidate_not_current",
};

export function productStatus(now = new Date().toISOString()): ProductStatusEnvelope {
  return { product_id: PRODUCT_ID, product_version: PRODUCT_VERSION, lifecycle_state: "phase_07_studio_supervision_development", development_authorized: true, production_authorized: false, certified: false, authority: CANDIDATE_AUTHORITY, updated_at_utc: now };
}

function argument(argv: ReadonlyArray<string>, name: string): string | null {
  const index = argv.indexOf(name);
  return index >= 0 && index + 1 < argv.length ? argv[index + 1]! : null;
}

export function main(argv = process.argv.slice(2)): number {
  const command = argv[0] ?? "health";
  const json = argv.includes("--json");
  if (command === "health" || command === "status") {
    const result = productStatus();
    console.log(json ? JSON.stringify(result, null, 2) : Object.entries(result).map(([key, value]) => `${key}: ${typeof value === "object" ? JSON.stringify(value) : String(value)}`).join("\n"));
    return 0;
  }
  if (command === "demo") {
    const output = resolve(argument(argv, "--output-dir") ?? "phase7-demo-output");
    const result = runPhase7Demo(output);
    console.log(json ? JSON.stringify(result, null, 2) : Object.entries(result).map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(",") : String(value)}`).join("\n"));
    return 0;
  }
  console.error(`unsupported command: ${command}`);
  return 2;
}

if (process.argv[1] && (import.meta.url === `file://${process.argv[1]}` || import.meta.url === `file:///${process.argv[1].replace(/\\/g, "/")}`)) process.exitCode = main();
