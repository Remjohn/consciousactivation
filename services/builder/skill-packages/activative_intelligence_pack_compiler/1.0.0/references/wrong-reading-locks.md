# Wrong-reading-lock rules

1. At least one non-empty wrong-reading lock is mandatory.
2. Locks are semantic constraints, not optional style preferences.
3. The compiler may preserve or strengthen a lock but may not remove or weaken it.
4. A contradictory requested output fails closed.
5. A lock must identify the interpretation to prevent or the governing meaning to
   preserve.
6. Applicability does not relax locks on an applicable branch.
7. A downstream derivative must inherit the authoritative parent locks; realization
   enforcement remains with the owning downstream product.
