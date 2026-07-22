# CCP Asset Intelligence V1

## Definition

Asset Intelligence V1 is the canonical system for ingesting, classifying, evaluating, retrieving, versioning, and remembering creative assets and creative ingredients across a Brand Workspace.

It is not a simple media library.

It knows:

```text
what an asset is
where it came from
whether it can be used
what it means
which primitives it supports
where it works
where it fails
how often it has been used
whether it should be promoted, reused, repaired, or blocked
```

## Position in the architecture

```text
Brand Context
Primitive Coalition
Visual Schema
Creative Ingredient Requirements
        ↓
Asset Intelligence
        ↓
SuperVisual / Carousel / Video / 2D Character / Paper-Cut / CAC / GMG
```

Asset Intelligence is a shared ingredient layer. Creative engines must not each invent their own unmanaged asset search.

## Scope

Asset Intelligence V1 owns:

```text
asset ingestion
asset fingerprinting
rights/provenance
classification
semantic enrichment
primitive fit
visual ingredient matching
asset retrieval
reference board support
asset evaluation
asset variants
usage receipts
performance memory
fatigue tracking
winner promotion
blocked/deprecated asset handling
```

It does not own:

```text
composition
final rendering
provider execution
publishing
timeline editing
carousel sequencing
scriptwriting
visual schema creation
```

## Core laws

```text
No direct-use asset without rights/provenance.
No creative engine performs unmanaged asset search.
No provider output disappears after generation; it becomes an AssetVariant.
No asset is reused without AssetUsageReceipt.
No asset is promoted without evaluation/performance evidence.
No blocked asset appears in retrieval.
No source-sensitive asset is used without brand_context_version_id.
No style route gets reference assets that violate its hard preconditions.
No CAC/Paper-Cut/Documentary Proof job proceeds without real-life/source reference.
```
