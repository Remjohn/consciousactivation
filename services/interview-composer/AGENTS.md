# Agent Instructions — Interview Composer

Read `README.md` and the controlling `TS-APP-COMPOSER-*` specs before changes.

## Current boundary

Allowed:

- Guest Research Package storage (URLs and uploaded-document metadata only;
  never fetched, never parsed);
- Activative Interview Brief storage, with operator-supplied substantive
  content only;
- read-only cross-reference checks against the real AIR repository
  (`brand_context_version`, `voice_dna`);
- calling `Phase9ActivativeService.compile_relationship_program` unchanged;
- product-local contracts, persistence, tests.

Prohibited:

- writing to `services/air/` or `services/interview/` in any way;
- constructing `matrix_of_edging`, `activation_hypothesis`,
  `activation_hypothesis_portfolio`, or
  `psychological_role_tension_contract` objects (GAP-007 territory --
  belongs to a future AIR-scoped spec, not to this service);
- calling `POST /api/interviews/brief-led` or `/import`;
- fetching, scraping, OCR-ing, or summarizing any Guest Research URL or
  document;
- fabricating a ref (`iac_ref`, `planned_aip_ref`, `arm_receipt_ref`) that
  does not point to a real, already-stored object.
