# PROMPT 03 — Dependency-Safe Full Canonical Tech Spec Writing Factory

**Controller:** GPT-5.6 Sol Extra High  
**Child writers:** GPT-5.6 Sol High  
**Parallel:** Yes within each topological writing wave. Writing waves are sequential.

Execute the Full Canonical V2.1 Tech Spec Writing Factory.

Do not implement code.

Do not create shared contract release bytes.

Do not rewrite accepted AIR specs merely for uniformity.

Do not let writers audit their own output.

Do not require upstream specifications to be `ACCEPTED_FOR_BUILD` merely to write downstream specifications.

The purpose is to write all queued implementation-grade Tech Specs in dependency-safe topological waves, while preserving the later independent Audit → Revision → Re-Audit → Acceptance lifecycle.

## Required gate

Verify either:

* the original Prompt 02 completion receipt is PASS and its packet set already satisfies V3.2 dependency-stage and write-authority rules; or
* `PROMPT_02B_COMPLETION_RECEIPT.yaml` and `PROMPT_03_REAUTHORIZATION.yaml` are PASS.

Also verify:

* source locks still match;
* all 60 writer packets pass the corrected packet schema;
* all dependency edges have lifecycle-stage classifications;
* the writing-wave DAG exists;
* every output path has a repository write-authority class.

If any condition fails, stop only the affected component where possible and produce a typed controller report.

## Controller work

### 1. Validate packets and path authority

For every packet verify:

* target spec ID;
* controlling FRs and Stories;
* authority owner;
* exact output path;
* output path class;
* nearest `AGENTS.md`;
* source dispositions;
* upstream writing inputs;
* acceptance prerequisites;
* build prerequisites;
* writing wave;
* disjoint file scope.

Do not dispatch a product-local target that violates current `AGENTS.md`.

A `PROGRAM_CONTROL_CROSS_PRODUCT_PROPOSAL` must remain under Program Control and carry `PRODUCT_ADOPTION_REQUIRED`.

### 2. Execute topological writing waves

Use `SPEC_WRITING_WAVE_DAG.yaml`.

For each wave:

1. verify all WRITE-blocking upstream inputs are readable and hash-pinned;
2. permit upstream states:
   * `WRITTEN_PENDING_AUDIT`;
   * `REVISED_PENDING_REAUDIT`;
   * `ACCEPTED_FOR_BUILD`;
   * exact frozen `WRITE_TIME_CONTRACT_SEED`;
3. label non-accepted upstream inputs `DRAFT_DEPENDENCY_NOT_ACCEPTED`;
4. freeze disjoint one-spec writer packets;
5. spawn one GPT-5.6 Sol High child per spec in the wave;
6. collect writing, files-read, source-traceability, and draft-dependency receipts;
7. validate exact outputs and hashes;
8. update wave status;
9. release the next wave.

Specs within a wave may run in parallel. A later wave must not start before required prior-wave draft receipts exist.

Acceptance is not performed during this prompt.

### 3. Child-writer law

Each child:

* writes exactly one spec;
* uses `CA_TECH_SPEC_WRITE_SKILL.md` V3.2 or later;
* reads its admitted upstream drafts without representing them as accepted authority;
* writes only its exact allowed output path;
* emits `WRITTEN_PENDING_AUDIT`;
* does not audit, revise, accept, build, or issue a capsule.

### 4. Cross-product proposals

For a Program Control cross-product proposal:

* write the complete implementation-grade proposed spec;
* record the target product and proposed adoption path;
* record the current repository prohibition;
* set `PRODUCT_ADOPTION_REQUIRED`;
* do not edit the target product;
* do not claim build readiness.

`TS-VAE-BOUND-001` must follow this path while the current VAE `AGENTS.md` limits writes to constitutional alignment outputs and Program Status Export.

### 5. Wave-local validation

After each wave verify:

* ten-section structure;
* source and dependency receipts;
* exact output path;
* no out-of-scope edits;
* no writer self-acceptance;
* no product-local allowlist violation;
* no upstream draft represented as ratified authority;
* no implementation code.

A failed child blocks only its dependent descendants, not unrelated waves.

### 6. Final integration

After all writable waves return:

* verify FR/Story coverage;
* verify all active queued specs are written or have an exact typed blocker;
* validate cross-references mechanically;
* preserve architecture conflicts for independent audit rather than resolving them silently;
* create the full spec index and traceability;
* create writer and wave completion matrices;
* issue the factory completion receipt.

Create:

* `FULL_TECH_SPEC_INDEX.yaml`
* `FULL_TECH_SPEC_TRACEABILITY.csv`
* `SPEC_WRITER_COMPLETION_MATRIX.csv`
* `SPEC_WRITING_WAVE_COMPLETION_MATRIX.csv`
* `CROSS_PRODUCT_PROPOSAL_INDEX.yaml`
* `FULL_SPEC_FACTORY_VALIDATION_REPORT.md`
* `FULL_SPEC_FACTORY_TEST_RESULTS.json`
* `FULL_SPEC_FACTORY_COMPLETION_RECEIPT.yaml`

## Completion states

Direct product specs finish as:

`WRITTEN_PENDING_AUDIT`

Program Control cross-product proposals finish with:

```yaml
quality_state: WRITTEN_PENDING_AUDIT
adoption_state: PRODUCT_ADOPTION_REQUIRED
build_state: NOT_BUILD_READY
```

## Acceptance criteria

Pass when:

* dependency roots were written before dependent specs;
* every admitted draft dependency is hash-pinned and labeled non-accepted;
* acceptance/build dependencies did not incorrectly block writing;
* all disjoint specs in a wave were parallelized;
* every output respects repository write authority;
* VAE was not modified outside its allowlist;
* no writer audited or accepted its own output;
* all writable queued specs are `WRITTEN_PENDING_AUDIT`;
* no code or Development Capsule was created.

Stop after the writing factory. The next step is Prompt 04 Independent Audit Factory.
