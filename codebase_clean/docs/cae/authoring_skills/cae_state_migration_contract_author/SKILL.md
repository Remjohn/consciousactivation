# CAE State Migration Contract Author Skill

**Skill ID:** `cae_state_migration_contract_author`  
**Maturity:** `development_uncertified`  
**Authority:** Procedural control only; operates under Bundle v3 State and Transition Control Protocol (`14_CAE_STATE_AND_TRANSITION_CONTROL_PROTOCOL.md`).  

---

## 1. Purpose & Migration Laws

The `cae_state_migration_contract_author` specifies bounded, evidence-bearing state migration and cutover contracts for moving an existing service state aggregate from legacy persistence to PostgreSQL authority.

### Core Migration Laws
1. **One Aggregate per Contract:** A migration contract MUST govern exactly one state aggregate. Bundling multiple aggregates into one migration is strictly forbidden.
2. **Five Discrete Authority States:** State progression MUST explicitly model five discrete, evidence-bearing stages:
   - `LEGACY_ONLY`: Brownfield SQLite/local store is authoritative.
   - `DUAL_VERIFY`: Shadow execution writes to staging PostgreSQL with force-rollback verification; legacy remains authoritative.
   - `POSTGRES_AUTHORITATIVE`: PostgreSQL is authoritative current state; receipts and events are verified.
   - `LEGACY_READ_ONLY`: Legacy store is frozen/read-only for audit reconciliation.
   - `RETIRED`: Legacy store is decommissioned.
3. **Strict Zero-Data-Movement Rule:** An authoring skill authors CONTRACTS and VERIFICATION SPECIFICATIONS ONLY. It MUST NOT provision databases, run migration scripts, backfill data, or execute live cutovers.
4. **Explicit Data Disposition:** Legacy data disposition MUST be explicitly classified under operator governance (`MIGRATE`, `READ_THROUGH`, `RETAIN_OUT_OF_SCOPE`, `DISCARD_WITH_RECORD`, `QUARANTINE`).

---

## 2. Inputs & Preconditions

- Input MUST conform to `input_schema.yaml`.
- Requires aggregate ID, legacy source description, target PostgreSQL schema projection, and disposition classifications.
- Upstream object constitution and FR traceability must be ratified.

---

## 3. Procedure

1. **Verify Single Aggregate Scope:** Confirm that the contract covers exactly one distinct aggregate boundary.
2. **Define Current vs Target Authority:**
   - Explicitly document current brownfield state store, write boundary, and query surfaces.
   - Explicitly document target PostgreSQL 17.6 relational schema, RLS policies, and idempotency keys.
3. **Draft Five-Stage Migration Lifecycle:**
   - Define entry criteria, exit criteria, and evidence checks for each of the 5 states (`LEGACY_ONLY`, `DUAL_VERIFY`, `POSTGRES_AUTHORITATIVE`, `LEGACY_READ_ONLY`, `RETIRED`).
4. **Establish Reconciliation & Rollback Procedures:**
   - Define automated parity verification logic.
   - Define deterministic emergency rollback procedure without data loss.
5. **Enforce Disposition & Quarantines:**
   - Classify all legacy entities into one of the 5 allowed disposition modes.
   - Explicitly flag unresolved references as `QUARANTINE`.
6. **Emit Migration Contract & Receipt:** Output structured contract conforming to `output_schema.yaml`.

---

## 4. Prohibitions

- MUST NOT bundle multiple state aggregates into a single contract.
- MUST NOT execute DDL, SQL, or data backfill scripts.
- MUST NOT authorize cutover without dynamic staging parity proof.
- MUST NOT bypass operator review for data retirement or quarantines.

---

## 5. Escalation & Stop Conditions

- **Stop as `PROHIBITED_ACTION`:** If the contract attempts to directly execute data mutation or cutover.
- **Stop as `REJECTED_MULTI_AGGREGATE`:** If more than one state aggregate is detected in the input.
