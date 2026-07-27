import assert from "node:assert/strict";
import { productStatus } from "../dist/index.js";

const status = productStatus("2026-07-23T12:00:00.000Z");
assert.equal(status.product_id, "conscious-activations-studio");
assert.equal(status.development_authorized, true);
assert.equal(status.production_authorized, false);
assert.equal(status.certified, false);
assert.equal(status.authority.authority_state, "candidate_not_current");
console.log("studio health test: PASS");
