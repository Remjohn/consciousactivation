# CAE Governance — Research Knowledge Extraction + Canonicalization + OKF Program

## Authoritative Non-Negotiables
1. **Source Immutability:** Protected source-bearing records (`ResearchSourceRecord`, `RawObservation`, `EvidenceSegment`) are immutable and cannot be silently rewritten by canonicalization.
2. **Derived Expression Lineage:** Derived canonical nodes, aliases, definitions, and OKF projections must preserve SHA-256 evidence digests (`source_evidence_hashes`, `source_record_refs`).
3. **Four Authority Lanes:**
   - `HUNTER`: Candidate extraction from raw research sources.
   - `ANALYST`: Semantic relationship classification (SAME/RELATED/SUBTYPE/CONTRADICTORY/DISTINCT) and false-merge rejection.
   - `COMPOSER`: Canonical knowledge node composition and OKF Markdown artifact compilation.
   - `COMMANDER`: Operator adjudication, contradiction resolution, canonical node commitment, retraction, and recovery.
4. **Passive Flat Skills:** Skills are passive, versioned, independently routable, and flat. Zero Skill-to-Skill invocation.
5. **OKF Representation / PostgreSQL Operational Authority:** OKF is the curated knowledge representation; PostgreSQL/RLS is the operational state authority. Redis is not used for canonical knowledge or state.
6. **False-Merge Guard:** Distinct homonyms and ambiguous concepts must be kept as distinct canonical nodes; false merges are prohibited.
