# CCP Provider Runtime Ideogram + Flux V1 Integration Bundle

This bundle turns provider contracts into governed provider jobs.

## Provider roles

```text
Ideogram = composition plate generator
Flux = reference-based object editor
```

## Sample-first law

Batch generation is blocked until required samples are approved:

```text
1 scene sample
1 face plate sample
1 template preview sample
then batch
```

## V1 posture

V1 is fake/deterministic provider execution only. It does not call Ideogram or Flux.

## Do not

```text
Do not call Ideogram.
Do not call Flux.
Do not call any provider API.
Do not read or infer secrets.
Do not allow batch before scene sample, face plate sample, and template preview sample are approved.
Do not execute a provider job without a decision log.
Do not create a provider output asset ref without a job receipt.
Do not retry forever.
```
