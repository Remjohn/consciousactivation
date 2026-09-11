import { buildControlTowerProjection } from "./controlTower";
import { buildAuditExportManifest } from "./auditExport";
import { compileDirectManipulation, compileNaturalLanguageRevision } from "./revision";
import { evaluateShipRequest } from "./ship";
import { projectVideoEditProgram } from "./timeline";
import { StudioValidationError } from "./errors";

declare const process: any;

type Handler = (payload: any) => unknown;
const handlers: Record<string, Handler> = {
  "build-control-tower-projection": buildControlTowerProjection,
  "project-video-edit-program": projectVideoEditProgram,
  "compile-natural-language-revision": (payload) => compileNaturalLanguageRevision(payload.request, payload.context),
  "compile-direct-manipulation": (payload) => compileDirectManipulation(payload.delta, payload.context),
  "evaluate-ship-request": evaluateShipRequest,
  "build-audit-export-manifest": buildAuditExportManifest,
};

async function main(): Promise<void> {
  const command = process.argv[2] as string | undefined;
  let input = "";
  process.stdin.setEncoding("utf8");
  for await (const chunk of process.stdin) input += chunk;
  try {
    const payload = input.trim() ? JSON.parse(input) : {};
    if (!command || !handlers[command]) throw new StudioValidationError("UNKNOWN_COMMAND", `unknown Studio RPC command: ${command ?? ""}`);
    const result = await handlers[command](payload);
    process.stdout.write(JSON.stringify({ ok: true, result }) + "\n");
  } catch (error) {
    if (error instanceof StudioValidationError) {
      process.stdout.write(JSON.stringify({ ok: false, error: { code: error.code, message: error.message, context: error.context } }) + "\n");
      return;
    }
    process.stderr.write(error instanceof Error ? error.stack ?? error.message : String(error));
    process.stderr.write("\n");
    process.exitCode = 1;
  }
}

void main();
