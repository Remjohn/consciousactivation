# Original BMAD Files Are Runtime Dependencies

The CAE bundle intentionally does not vendor-copy the entire BMAD repository.

The reason is not to reduce the method.

The reason is to prevent divergence from the real upstream method and to preserve all of the
original workflow mechanics as the authoritative implementation substrate.

The target environment therefore has two layers:

```text
BMAD-METHOD source tree
        +
.caebmad CAE overlay
```

The CAE overlay can call the original BMAD skills as specialized downstream tools.

The original skill files must remain present and usable.

This is why installation fails if the required original families are absent.

## Why this is stronger than copying tiny equivalents

Copying a shortened imitation of a large BMAD workflow creates a false sense of compatibility.

Keeping the actual base means:

- the original workflow instructions remain intact;
- future BMAD updates can be pulled intentionally;
- the CAE layer only owns CAE-specific behavior;
- original tests and tooling remain available;
- the operator can fall through to native BMAD workflows when appropriate.

## CAE-specific responsibility

The CAE layer owns the things that generic BMAD cannot know:

- CAE product history
- 216-source reconstruction
- CCP/CCF/CMF lineage
- Atomic Harnesses / Visual Syntax lineage
- one-question Grill
- operating-level inspection
- CAE truth-state model
- CAE brownfield reconciliation
- CAE runtime handoff

This is a true specialization boundary.
