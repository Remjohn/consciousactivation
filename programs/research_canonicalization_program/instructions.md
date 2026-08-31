# Operating Instructions — Research Knowledge Extraction + Canonicalization + OKF Program

## Execution Flow
1. **Source Attachment (COMMANDER):** Validate attached research sources, verifying source IDs and SHA-256 digests.
2. **Candidate Extraction (HUNTER):** Extract structured `KnowledgeCandidate` records containing verbatim text and source back-pointers.
3. **Canonicalization & Relationship Classification (ANALYST):**
   - Cluster candidates by semantic identity (`SAME` &rarr; alias/synonym merge).
   - Enforce false-merge rejection (guard against homonyms and distinct concepts).
   - Identify hierarchical taxonomic relations (`SUBTYPE` / `SUPERTYPE`), associative relations (`RELATED`), and opposing claims (`CONTRADICTORY`).
   - Construct `CanonicalKnowledgeNode` instances with cryptographic SHA-256 lineage.
4. **OKF Markdown Projection (COMPOSER):**
   - Compile individual OKF Markdown documents with YAML frontmatter conforming to `cmf-okf-research-knowledge-1.0`.
   - Compile top-level catalog `index.md`.
   - Compute composite bundle SHA-256 hash.
5. **Adjudication & Commitment (COMMANDER):**
   - Review and adjudicate any detected contradiction edges or merge disputes.
   - Commit canonical knowledge nodes and OKF bundle to aggregate state.
