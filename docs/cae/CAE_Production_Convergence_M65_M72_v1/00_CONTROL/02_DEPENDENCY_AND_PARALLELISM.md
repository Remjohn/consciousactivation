# M65–M72 Dependency + Parallelism

| Mandate | Depends on | Parallel work | Gate |
|---|---|---|---|
| M65 | M49–M64 + current repo | none | freezes canonical ownership |
| M66 | M65 | M67, M68 design | M69/M71 |
| M67 | M65 | M66, M68 design | M70/M71 |
| M68 | M65 | M66, M67 | M69/M71 |
| M69 | M65 + M66–M68 contracts | M70 design | M71/M72 |
| M70 | M67 + M68 | M69 design | M71 |
| M71 | M66–M70 | none | M72 |
| M72 | M69 + M71 + deployment evidence | none | final operator decision |

Safe concurrency: M66/M67/M68 may implement in parallel after M65 freezes ownership and shared contracts. M69 can design in parallel with M70 but certification execution waits for both. M71 is intentionally serial because it is the first golden end-to-end reality-contact proof. M72 is terminal.
