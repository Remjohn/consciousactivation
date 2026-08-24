"""Run the WP-07 proof over the real first-slice transition path.

The underlying verifier executes the five registered operations in one
force-rolled-back staging transaction and checks their execution receipts,
immutable evidence links, false-reference rejection, and lineage view.
"""

from __future__ import annotations

from verify_wp03_first_slice import main


if __name__ == "__main__":
    result = main()
    print(f"wp07_execution_receipt_lineage_proof={'PASS' if result == 0 else 'FAIL'}")
    raise SystemExit(result)
