// TS-APP-API-006 Stage 1 — Studio RPC bridge entrypoint.
//
// stdin/stdout JSON command dispatcher over the pure functions already in
// controlTower.ts, timeline.ts, revision.ts, rerun.ts, resolutions.ts,
// ship.ts, auditExport.ts, surfaces.ts, and campaign.ts.  No business logic
// is added or changed here; this file only routes a JSON envelope to an
// existing exported function and serializes the result.
//
// Protocol:
//   stdin  -> one JSON object whose shape matches the dispatched command's input
//   stdout -> {"ok": true, "result": <json>}   on success (exit 0)
//          -> {"ok": false, "error": {"code","message","context"}} on a
//             StudioValidationError (exit 0; a validation failure is an
//             ordinary, well-formed answer, not a crash)
//   stderr -> stack trace, on an unexpected crash (exit 1)

import { readFileSync } from "node:fs";
import { buildControlTowerProjection, type ControlTowerInput } from "./controlTower.js";
import { projectVideoEditProgram, type VideoEditProgramInput } from "./timeline.js";
import { compileNaturalLanguageRevision, compileDirectManipulation, DEFAULT_STUDIO_TOOLS, type RevisionContext } from "./revision.js";
import { compileSelectiveRerun } from "./rerun.js";
import { createHumanResolutionEpisode, HumanResolutionLedger, type HumanResolutionInput } from "./resolutions.js";
import { evaluateShipRequest } from "./ship.js";
import { buildAuditExportManifest, writeAuditExport, type AuditExportInput } from "./auditExport.js";
import { routeHarnessToSurfaces } from "./surfaces.js";
import { buildExceptionReviewPackage, transitionCampaign } from "./campaign.js";
import { StudioValidationError } from "./validators.js";
import type {
  CampaignLifecycleState,
  CampaignState,
  DirectManipulationDelta,
  OperatorRevisionRequest,
} from "./domain.js";

type Envelope =
  | { ok: true; result: unknown }
  | { ok: false; error: { code: string; message: string; context: unknown } };

function readStdin(): any {
  // readFileSync accepts the fd number 0 (stdin) at runtime; the node-shims.d.ts
  // declares only the string overload, so cast through unknown.
  return JSON.parse(readFileSync(0 as unknown as string, "utf8"));
}

function handle(command: string, input: any): unknown {
  switch (command) {
    case "list-default-tools":
      return DEFAULT_STUDIO_TOOLS;
    case "route-harness-to-surfaces":
      return routeHarnessToSurfaces(input);
    case "project-video-edit-program":
      return projectVideoEditProgram(input as VideoEditProgramInput);
    case "build-control-tower-projection":
      return buildControlTowerProjection(input as ControlTowerInput);
    case "compile-natural-language-revision":
      return compileNaturalLanguageRevision(input.request as OperatorRevisionRequest, input.context as RevisionContext);
    case "compile-direct-manipulation":
      return compileDirectManipulation(input.delta as DirectManipulationDelta, input.context as RevisionContext);
    case "compile-selective-rerun":
      return compileSelectiveRerun(input);
    case "create-human-resolution-episode": {
      const episode = createHumanResolutionEpisode(input.episode as HumanResolutionInput);
      const ledger = new HumanResolutionLedger(input.ledger_path as string);
      ledger.append(episode);
      return { episode, ledger_sha256: ledger.ledgerSha256() };
    }
    case "list-human-resolution-episodes": {
      const ledger = new HumanResolutionLedger(input.ledger_path as string);
      return { episodes: ledger.all() };
    }
    case "evaluate-ship-request":
      return evaluateShipRequest(input.request, input.campaign as CampaignState);
    case "build-audit-export-manifest":
      return buildAuditExportManifest(input as AuditExportInput);
    case "write-audit-export": {
      const manifest = buildAuditExportManifest(input.manifest_input as AuditExportInput);
      writeAuditExport(input.path as string, manifest);
      return manifest;
    }
    case "build-exception-review-package":
      return buildExceptionReviewPackage(input);
    case "transition-campaign":
      return transitionCampaign(input.state as CampaignState, input.next as CampaignLifecycleState, input.updates ?? {});
    default:
      throw new StudioValidationError("UNKNOWN_RPC_COMMAND", `unknown command: ${command}`);
  }
}

function main(): number {
  const command = process.argv[2];
  if (!command) {
    process.stderr.write("usage: rpc.js <command> < input.json\n");
    return 2;
  }
  try {
    const input = readStdin();
    const result = handle(command, input);
    const envelope: Envelope = { ok: true, result };
    process.stdout.write(JSON.stringify(envelope));
    return 0;
  } catch (error) {
    if (error instanceof StudioValidationError) {
      const envelope: Envelope = {
        ok: false,
        error: { code: error.code, message: error.message, context: error.context },
      };
      process.stdout.write(JSON.stringify(envelope));
      return 0;
    }
    process.stderr.write(error instanceof Error ? (error.stack ?? error.message) : String(error));
    return 1;
  }
}

process.exitCode = main();