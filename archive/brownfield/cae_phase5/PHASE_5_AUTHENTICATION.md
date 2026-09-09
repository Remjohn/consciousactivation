# Phase 5 Authentication Protocol

## Purpose
Separate source capture from downstream trust. Authentication is a typed decision about the evidentiary status of a candidate claim for a declared use, not a claim that the system has discovered universal truth.

## Authentication classes

- `EXPLICIT` — directly and clearly stated by the Guest.
- `SPECIFIC` — supported by concrete event, example, mechanism, or first-person detail.
- `REPEATED` — independently repeated across turns or sessions.
- `CORROBORATED` — supported by additional first-party or explicitly permitted evidence.
- `PROVISIONAL` — plausible interpretation not yet sufficiently established.
- `AMBIGUOUS` — multiple interpretations remain viable.
- `CONTRADICTED` — materially opposed by other authenticated evidence.
- `UNSUPPORTED` — insufficient evidence.

## Important distinction
A statement can be authentic without being externally verified fact. Phase 5 must preserve that distinction.

Examples:

- "I felt like I had to be useful to deserve attention." → authentic Guest statement; may become first-person belief evidence.
- "My audience feels exactly the same." → claim about audience; requires separate audience evidence.
- "This happened because the industry is corrupt." → Guest interpretation; store as interpretation unless separately corroborated.

## Promotion rule
Only evidence whose authentication status satisfies the downstream consumer's declared threshold may enter that consumer's semantic packet.

## Rejection rule
Rejection of an interpretation must never delete the underlying response.
