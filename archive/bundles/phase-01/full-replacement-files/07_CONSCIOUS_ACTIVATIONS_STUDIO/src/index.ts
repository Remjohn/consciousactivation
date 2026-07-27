import type { AuthorityRef, ProductStatusEnvelope } from "./generated/contracts.js";

declare const process: {
  argv: string[];
  exitCode?: number;
};

export const PRODUCT_ID = "conscious-activations-studio";
export const PRODUCT_VERSION = "0.1.0-dev.1";

export const CANDIDATE_AUTHORITY: AuthorityRef = {
  authority_id: "ca-program-control-v2.1-candidate",
  authority_version: "2.1.0-candidate",
  authority_sha256: "cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39",
  authority_state: "candidate_not_current",
};

export function productStatus(now = new Date().toISOString()): ProductStatusEnvelope {
  return {
    product_id: PRODUCT_ID,
    product_version: PRODUCT_VERSION,
    lifecycle_state: "phase_01_development_foundation",
    development_authorized: true,
    production_authorized: false,
    certified: false,
    authority: CANDIDATE_AUTHORITY,
    updated_at_utc: now,
  };
}

export function main(argv = process.argv.slice(2)): number {
  const command = argv[0] ?? "health";
  const json = argv.includes("--json");
  if (command !== "health" && command !== "status") {
    console.error(`unsupported command: ${command}`);
    return 2;
  }
  const result = productStatus();
  if (json) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    for (const [key, value] of Object.entries(result)) {
      console.log(`${key}: ${typeof value === "object" ? JSON.stringify(value) : String(value)}`);
    }
  }
  return 0;
}

if (import.meta.url === `file://${process.argv[1]}` || import.meta.url.replace(/\\/g, "/") === `file:///${(process.argv[1] || "").replace(/\\/g, "/")}`) {
  process.exitCode = main();
}
