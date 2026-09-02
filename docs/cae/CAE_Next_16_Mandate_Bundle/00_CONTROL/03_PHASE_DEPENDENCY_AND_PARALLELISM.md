# M49–M64 Dependency + Parallelism Matrix

| Mandate | Depends on | Parallelizable with | Must close before |
|---|---|---|---|
| M49 | M48 | — | M50, M53 |
| M50 | M49 | M51 | M52 |
| M51 | M50 | — | M52 |
| M52 | M49–M51 | — | M53, phase close |
| M53 | M52 + Program manifests | M54 design | M55 |
| M54 | M52 | M53 implementation after contract frozen | M55 |
| M55 | M54 + existing repair semantics | — | M56 |
| M56 | M52 + M55 | M57 design | M60 |
| M57 | M48 baseline | M49–M56 documentation | M58 |
| M58 | M57 | — | M59 |
| M59 | M58 | — | M60 |
| M60 | M59 | — | M61 |
| M61 | M52–M60 | — | M62, M63 |
| M62 | M61 + existing sandbox/concurrency evidence | M63 UI design | M64 |
| M63 | M56 + M61 | M62 | M64 |
| M64 | M61–M63 | — | Phase 8 close |

## Parallelism rules

Safe parallel design/research is allowed where contracts are read-only and no shared runtime authority is mutated.

Do NOT parallelize two mandates that modify the same canonical registry/schema or competing workflow compiler semantics.
Do NOT parallelize phase-close mandates.
