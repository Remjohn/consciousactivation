# Authority Load Order

For every mandate in this bundle, Gemini should load evidence in this order:

1. **Repository execution doctrine**
   - `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
   - `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
2. **Evidence procedure when applicable**
   - `docs/cae/skills/EVIDENCE_TO_AIR_FIRST_SLICE_SKILL.md`
3. **Current program-control state**
   - `governance/program-control/03_PROGRAM_STATUS/*`
4. **Canonical PRD and Tech Specs**
   - `docs/PRD/CURRENT.md`
   - relevant `docs/tech-specs/*`
5. **Editorial / CAE authority artifacts**
   - `docs/cae/editorial_intelligence/*`
6. **Execution history**
   - `docs/cae/cae_mandate_bundle/*`
   - relevant `.zcode/plans/*`
   - receipts/tests/commits discovered during the evidence sweep
7. **Executable reality**
   - services, API, packages, migrations, tests, scripts, apps, infrastructure

Higher-level authority always outranks lower-level convenience, but runtime claims must be proven against executable reality. If authorities conflict, preserve the conflict and route it rather than choosing silently.
