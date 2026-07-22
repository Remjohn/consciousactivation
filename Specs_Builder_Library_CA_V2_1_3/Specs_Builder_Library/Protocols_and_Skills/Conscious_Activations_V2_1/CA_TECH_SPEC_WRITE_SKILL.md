# SKILL — Conscious Activations Tech Spec Writer

## Role

Write exactly one implementation-grade Tech Spec from accepted authority, Functional Requirements, vertical Stories, current code, predecessor evidence, and the dependency inputs frozen for the current writing wave.

The writer does not audit, accept, build, or issue a Development Capsule.

## Required inputs

- `TARGET_SPEC_ID`
- canonical or proposal output path
- output path class
- controlling product and authority
- controlling FR IDs
- controlling Story IDs and acceptance criteria
- cross-product owner
- exact source and predecessor paths
- upstream writing inputs with quality states and hashes
- acceptance prerequisites
- build prerequisites
- downstream consumers
- allowed file scope
- relevant Primitive/archetype/brand/Voice DNA/Visual DNA sources
- current `SOURCE_DISPOSITION_LEDGER`
- current dependency-edge classification ledger

Missing inputs classified as `REQUIRED_AUTHORITY`, `REQUIRED_CURRENT_IMPLEMENTATION`, or `REQUIRED_UNIQUE_EVIDENCE` cause `WRITE_BLOCKED`. Missing optional or deferred references do not block writing.

## Upstream dependency rules

For WRITE, an upstream input is admissible when it is one of:

- an accepted authority or accepted Tech Spec;
- a hash-pinned spec in `WRITTEN_PENDING_AUDIT`;
- a hash-pinned spec in `REVISED_PENDING_REAUDIT`;
- a frozen `WRITE_TIME_CONTRACT_SEED` issued by Program Control.

A `QUEUED_FOR_WRITE` packet is not a readable dependency. The controller must dispatch its upstream wave first.

When reading a non-accepted upstream draft:

1. label it `DRAFT_DEPENDENCY_NOT_ACCEPTED`;
2. pin path, state, and SHA-256;
3. distinguish settled authority from draft interface detail;
4. avoid representing draft detail as ratified law;
5. record downstream sections likely to require revision if the upstream draft changes during audit.

`ACCEPTANCE_PREREQUISITE` and `BUILD_PREREQUISITE` edges do not block WRITE unless they are separately classified as write-interface or authority dependencies.

Create `DRAFT_DEPENDENCY_RECEIPT.yaml` whenever any non-accepted upstream spec or contract seed is used.

## Repository write-authority rules

Read the nearest applicable `AGENTS.md` before writing.

- For `DIRECT_PRODUCT_SPEC_PATH`, write only the exact allowed target path.
- For `PROGRAM_CONTROL_CROSS_PRODUCT_PROPOSAL`, do not modify the target product. Write the full proposed Tech Spec under the governed Program Control proposal path and include:
  - target product;
  - proposed adoption path;
  - current prohibition;
  - adoption requirements;
  - status `PRODUCT_ADOPTION_REQUIRED`.
- For `DEFERRED_UNTIL_PRODUCT_AUTHORIZATION`, stop with `WRITE_BLOCKED_PATH_AUTHORITY`.

A cross-product proposal cannot claim product-local acceptance or build readiness.

## Mandatory pre-work

Read in order:

1. current authority and product PRD;
2. controlling FRs;
3. controlling Stories;
4. cross-product ownership ledger;
5. upstream writing inputs admitted for this wave;
6. current implementation files named by the assignment;
7. predecessor files named by the assignment;
8. relevant tests and fixtures;
9. Primitive/archetype/CBAR/CCV/RSCS/SDA/SFL sources where applicable;
10. current product status and claim ceiling;
11. nearest applicable `AGENTS.md` and write-authority decision.

Create `FILES_READ_RECEIPT.yaml` with exact paths, hashes where available, lifecycle state, dependency class, and one specific fact extracted from each source.

Do not continue when a source classified as required by the current Source Disposition Ledger cannot be read. For an unavailable optional/deferred reference, create a `SOURCE_GAP_NOTICE`, do not attribute claims to it, and continue using the remaining authoritative and implementation evidence.

## Mandatory output structure

### 1. Files and authorities read

Exact paths, versions, hashes, authority class, dependency state, and draft/accepted status.

### 2. Problem, user outcome, solution, and scope

- concrete failure without the spec;
- user or system outcome;
- bounded solution;
- in scope;
- out of scope;
- non-goals.

### 3. Governing decisions and constraints

Include:

- product sovereignty;
- authority and object ownership;
- relevant doctrines;
- source fidelity and lineage;
- Primitive/archetype/Final Script rules where applicable;
- claim ceiling;
- explicitly forbidden behavior;
- any draft-dependency caveats.

### 4. Current brownfield architecture

For each relevant current or predecessor component state:

- exact path;
- actual behavior;
- disposition: `REUSE`, `ADAPT`, `ACTIVATE`, `REPLACE`, or `ARCHIVE`;
- reason;
- migration constraints.

### 5. Proposed architecture and workflows

Define:

- components;
- responsibilities;
- entry and exit objects;
- commands;
- events;
- state transitions;
- handoffs;
- synchronous/asynchronous behavior;
- idempotency;
- replay/cancellation/compensation where applicable.

### 6. Data models, contracts, schemas, and APIs

Every field must be typed and have one owner. Include:

- schema identity and version;
- validation;
- mutability;
- compatibility;
- supersession;
- canonical serialization and hashing where applicable;
- positive and negative examples.

No `Any`, untyped open dictionaries, placeholder fields, or implied defaults unless explicitly governed.

### 7. Implementation stages and exact target paths

Name exact files to create or modify. Every task must map to an FR/Story and an acceptance criterion.

For a Program Control cross-product proposal, distinguish the proposal path from the future product-adoption path and prohibit product-local edits until adoption.

### 8. Failure, migration, rollback, recovery, and observability

Define:

- typed failures;
- retries versus quality repair;
- cancellation races;
- late results;
- migration and backward compatibility;
- rollback;
- metrics/logs/events/receipts;
- degraded behavior.

### 9. Behavior-specific acceptance criteria

Use Given/When/Then. Every criterion includes:

- exact governing FR/Story;
- pass condition;
- concrete failure example;
- evidence artifact;
- responsible test layer.

Cover positive, negative, adversarial, boundary, recovery, and observability behavior.

### 10. Testing and completion evidence

Name exact test paths and test cases:

- unit;
- schema/contract;
- integration;
- architecture boundary;
- migration;
- replay/cancellation/recovery;
- clean environment;
- affected regression;
- reference-slice evidence where applicable.

Define the required Build Receipt and claim ceiling, but do not issue either.

For cross-product proposals, define product-adoption evidence before build readiness.

## Conscious Activations semantic requirements

Where relevant, the spec must explicitly use exact current objects rather than vague concepts:

- epistemic state;
- Matrix of Edging;
- psychological role inside a tension;
- exact Primitive IDs and Primitive Bindings;
- Primitive Coalition Contract;
- Coalition Signature;
- Edge Product;
- Primitive Misuse Risk;
- archetype coalition;
- Brand Context Version;
- Guest Voice DNA;
- Visual DNA;
- RSCS Distillation Layers;
- CBAR and CCV;
- SDA and SFL;
- approved Final Script;
- Activation Transfer Contract;
- HumanResolutionEpisode.

Use only objects required by the controlling FRs and Stories. Do not add ceremony where not applicable.

## Anti-laziness rejection conditions

Reject the output when it contains:

- generic acceptance criteria;
- invented source files or method signatures;
- fuzzy Primitive names;
- missing failure examples;
- placeholder schemas;
- TODOs;
- ambiguous product ownership;
- unbounded scope;
- implementation tasks without exact paths;
- a current behavior described only from historical documentation;
- a claim that package validation equals production evidence;
- an upstream draft represented as accepted authority;
- a product-local target that violates the current `AGENTS.md` allowlist.

## Writer completion

Create:

- target Tech Spec or cross-product proposal;
- `SPEC_WRITING_RECEIPT.yaml`;
- `FILES_READ_RECEIPT.yaml`;
- `SOURCE_TRACEABILITY.yaml`;
- `DRAFT_DEPENDENCY_RECEIPT.yaml` when applicable;
- `PRODUCT_ADOPTION_REQUIREMENTS.yaml` for cross-product proposals.

Final writer status:

- `WRITTEN_PENDING_AUDIT`, or
- `PRODUCT_ADOPTION_REQUIRED` with proposal quality state `WRITTEN_PENDING_AUDIT`.

The writer may not mark the spec `ACCEPTED_FOR_BUILD`.

## Source classification rules

- A spec assignment may list a source for research context without making it implementation authority.
- `REFERENCE`, `reference_only`, `OPTIONAL_REFERENCE`, and `DEFERRED_REFERENCE` sources cannot block the writer unless the controller promotes them to `REQUIRED_UNIQUE_EVIDENCE` with an attributable reason.
- The writer must never reconstruct or paraphrase an unavailable source from a title, filename, memory, or secondary summary.
- The files-read receipt must distinguish `READ`, `NOT_AVAILABLE_OPTIONAL`, `DEFERRED`, and `SUPERSEDED`.


## Candidate-authority writing rule

When specification work is explicitly authorized but the controlling V2.1 authority package is not yet ratified:

- label the controlling authority `CANDIDATE_NOT_CURRENT`;
- cite the explicit specification-work authorization receipt;
- distinguish current product authority from candidate future authority;
- write the complete technical proposal/specification;
- do not claim current product adoption, implementation authorization, or build readiness;
- set the post-write build gate to `RATIFICATION_OR_PRODUCT_ADOPTION_REQUIRED`.

This condition does not block WRITE.
