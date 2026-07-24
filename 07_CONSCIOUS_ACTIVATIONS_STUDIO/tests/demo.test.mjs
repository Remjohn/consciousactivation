import test from "node:test";
import assert from "node:assert/strict";
import { existsSync, mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { runPhase7Demo } from "../dist/phase7_demo.js";

test("reference Studio flow compiles revision, reruns descendants and emits audit evidence", () => {
  const dir = mkdtempSync(join(tmpdir(), "ca-phase7-demo-"));
  try {
    const result = runPhase7Demo(dir);
    assert.equal(result.ship_decision, "AUTHORIZED");
    assert.deepEqual(result.invalidated_nodes, ["node:final-review", "node:static-eval", "node:supervisual-render"]);
    for (const file of result.output_files) assert.equal(existsSync(join(dir, file)), true, file);
    const html = readFileSync(join(dir, "studio-control-tower.html"), "utf8");
    assert.match(html, /Source-to-batch run graph/);
    assert.match(html, /Canonical timeline projection/);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
