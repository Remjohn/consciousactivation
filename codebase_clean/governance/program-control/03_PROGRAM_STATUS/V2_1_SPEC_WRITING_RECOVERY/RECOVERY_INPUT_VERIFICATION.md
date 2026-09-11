# V2.1 Spec-Writing Recovery Input Verification

Date: 2026-07-22  
Result: **PASS**

## Durable gate inputs

The recovery uses committed or hash-locked Prompt 01/02 records. The absent Prompt 03 execution logs are noncanonical and were not reconstructed. `PROMPT_02B_MISSING_INPUT_REPORT.yaml` remains unchanged at SHA-256 `6481c36568ae6b7d6260500a900048cbca12b697a17f228b633a331018de0aa9`.

| Input | SHA-256 | Result |
|---|---|---|
| Prompt 01 completion receipt | `032b90b449fd5bafd96685ae40370f652bdfba38fdec1d0761be115c069f528f` | PASS |
| Prompt 02 gate receipt | `01f054b4e3efa67345a3fbd4b33fadc4f26b0174ffdfaa44d5090051cc214709` | PASS |
| Prompt 02 completion receipt | `bb0057effade4074c84063a376d61e908bb636d81e93141290c4a61112456105` | PASS |
| Prompt 02 manifest | `71f7b948926586593873a1d09e65bcc0957dc32fe8035ca73df1ca3c192fa7fd` | PASS, 21/21 entries |
| Canonical spec ledger | `acb0bd4b9d941c389b9a816ae00922770eafc9eafcab1ccf924f0e9b84dcbe2c` | PASS |
| Writing queue | `62ad5315d08dd2b205f21977e97cd7bc9623ca9f41a89f408c63788268e62082` | PASS |
| Original packets | `78d58372e0aab32aece23d3769a4e1382c9f4e7844c3cc301a65bddca154b1b2` | PASS |
| Dependency DAG | `1cf4299781e76c9c80f4489291a92b0a5e1f666f91b8cf9476307a03da5257eb` | PASS |
| Path registry | `f260e400384a67f837b67a8a8981a4b773cd8792135eeca20c94f065468296a7` | PASS |
| Lane manifests | `a647ea17d86c7c8c48075a87431332461c035189d1a2df00f03e5c81ca8611a2` | PASS |
| Quality registry | `3e42691dd8c7e3600c1c5ab5160642d5a01bc02c254610bc0ab73675a6913660` | PASS |
| Source disposition ledger | `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | PASS |

## Locked archives

The three live authority archives match the Prompt 02 lock. The tracked V2.1.1 Skills archive is deleted from the working tree but its committed HEAD blob remains byte-identical to the Prompt 02 lock, so no upload or reconstruction was required.

| Archive | Source | SHA-256 | Result |
|---|---|---|---|
| AIR V2.1 bundle | worktree | `985227a8645f050e4789456933ac8845108a070ad44441177601fc7c0e8d7e76` | MATCH |
| AHP V1.2 bundle | worktree | `b85a2888e33ec9d41e6a82461ec11f4d136b4b3cd42c06a67d94a470afbf0b9d` | MATCH |
| CMF Studio archive | worktree | `2fd48bb14f61890ffeb8d9999be6f55b79e8e1156067addc47a08d5cbb91ea4c` | MATCH |
| Skills V2.1.1 archive | committed HEAD blob | `e40a843d0748de78fce216fbb322437707a8eab0ca649e88bbfe7ab4bc99c69e` | MATCH |

## Current V3.3 workflow law

`CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3.zip` passes ZIP validation at SHA-256 `0bcd1e957301dbd8fc03dd6b74684a6d6b7fff148bd1401134f19db760c69eb7`; its extracted package manifest validates 33/33 entries. The lifecycle controller hash is `63b2ff363c4dc3457438f1bd693d29cf18adb6c4b2e66ebb7c093b0d765f59ae` and the writer Skill hash is `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520`.

## Repository instructions

There is no repository-root `AGENTS.md`. Builder, VAE, and Delegation product-local instructions were read and hashed. Only the VAE packet conflicts with a product-local allowlist; it is retargeted to this recovery root's `cross-product-proposals/` area. No product repository is modified by this package.

