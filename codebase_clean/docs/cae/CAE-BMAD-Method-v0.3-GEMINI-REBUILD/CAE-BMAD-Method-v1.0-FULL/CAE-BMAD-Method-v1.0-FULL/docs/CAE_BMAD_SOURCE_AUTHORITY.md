# CAE-BMAD Source Authority

## Source hierarchy

### Class A — Current implementation evidence

- repository source
- database schema
- executable behavior
- tests with reality contact
- receipts
- execution traces

### Class B — Current product authority

- approved CAE PRD
- approved PRD Modules
- constitutions
- approved architecture
- approved Program definitions

### Class C — Historical product authority

- CCP PRDs
- CCF/CMF source docs
- Atomic Harness specifications
- visual syntax
- audits
- product transcripts
- research archives

### Class D — Methodological references

- BMAD
- grill-with-docs
- SSSF
- engineering method references

## Authority is contextual

A current runtime file can outrank a historical PRD when the question is "what happens now?"

A historical CCP source can outrank an invented CAE draft when the question is "where did this concept originate?"

An operator decision can outrank an agent recommendation when deciding a constitutional product question.

## Required evidence notation

Every consequential claim in a reconstruction or artifact should be traceable to one or more sources.

Use:

```text
[verified: SRC-xxx]
[inherited: SRC-xxx]
[repository: path:line/symbol]
[decision: DEC-xxx]
[proposed]
```

## Prohibited

- unsupported "standard practice" claims presented as CAE truth
- source-less architectural decisions
- deleting contradictions to make documents cleaner
- using a generated summary as the sole source for a consequential claim
