# CAE Question Heritage Audit Mandate — 12

**Book:** *Change Your Questions, Change Your Life*  
**Author:** Marilee Adams  
**Mandate status:** `EXECUTION-READY — AUDIT ONLY`

## Mandate Objective
Read the assigned source in full and produce one evidence-grounded Question Heritage Audit. The audit is the only deliverable authorized by this mandate. No Question Primitive YAML may be created or modified. No production runtime code may be changed.

## Required Source Procedure
1. Locate the actual PDF or verified full-text source in the local workspace.
2. If the source is PDF, run `python tools/prepare_book_markdown.py --input <pdf> --output <md> --overwrite`. Preserve the original PDF.
3. Inspect the conversion manifest and verify page continuity. Any empty or obviously corrupted extraction causes `SOURCE_ACCESS_FAILURE` and stops execution.
4. Read the complete assigned book, not selected excerpts, summaries, reviews, or prior AI answers.
5. Load the CAE Question Heritage Audit Protocol and existing CAE/CCP references identified by the execution environment.
6. Extract source-supported mechanisms; distinguish direct source claims from auditor synthesis and CAE application hypotheses.

## Required Audit Output
Write exactly one file under the configured Question Heritage audit directory using the audit template. Target 3,600–3,800 words without padding. The audit must contain candidate mechanisms, first principles, 0–200 MCDA, Pareto analysis, answer-transformation analysis, four CAE cases, SWOT, taxonomy/orthogonal-dimension review, cross-book hooks, promotion recommendations, and evidence limitations.

## Taxonomy Law
The existing Question taxonomy is provisional. Retain it only where the source supports it. If the book reveals a genuinely new dimension, record the evidence, collision with the current taxonomy, proposed distinction, and operational value. Do not force novelty and do not suppress it.

## Primitive Prohibition
The audit may recommend `PROMOTION_CANDIDATE`, but it MUST NOT assign a canonical primitive ID, create YAML, edit a registry, or imply that a mechanism is already canonical. Earlier `PRM-QST-*` artifacts must be treated as quarantined hypotheses.

## Evidence / Taste Law
Do not treat fluent wording, a citation-looking sentence, a high score, or successful automated checks as proof. Every important mechanism claim must be traceable to a source location. Cases and CAE mappings must be clearly labeled as applications or hypotheses. The audit must identify what would make the mechanism generic, cliché, manipulative, or operationally weak.

## Completion Test
Execution is complete only when: (a) the source-read record confirms the full assigned source was read; (b) the audit file exists; (c) source-integrity limitations are recorded; (d) no primitive registry was modified; and (e) a concise completion record names the exact source, output path, word count, and unresolved evidence issues.

## 200–300 Word Activation Prompt
You are executing **Question Heritage Audit 12** for *Change Your Questions, Change Your Life* by Marilee Adams. Treat the assigned book as the primary epistemic source. First locate the actual local source; if it is a PDF, convert it with the bundled PDF→Markdown tool and verify the conversion before reading. Then read the entire book. Do not use summaries or memory as substitutes. Extract the recurring questioning mechanisms that materially change what a person says, remembers, explains, contrasts, reveals, or decides. For every candidate mechanism, record where the source supports it, how the mechanism operates, what conditions it requires, what response transformation it is intended to produce, and where it can fail. Run the complete 0–200 MCDA using mechanism determinism, evidence yield, cognitive/narrative yield, contextual adaptability, CAE fit, and resistance to genericity/cliché. Analyze the book against the current Question taxonomy and explicitly report any novel dimension that the source forces us to add, split, rename, or reconsider. Produce four CAE-grounded application cases, clearly marking them as applications rather than book claims. End with recommendations for later primitive promotion, but do not create primitives, YAML, registry IDs, or runtime changes. If the full source is inaccessible, incomplete, corrupted, or materially unreadable, stop with `SOURCE_ACCESS_FAILURE`; never compensate by hallucinating an audit. Write one complete `AUDIT_12_...md` file only, then return a concise evidence record to the Operator.
