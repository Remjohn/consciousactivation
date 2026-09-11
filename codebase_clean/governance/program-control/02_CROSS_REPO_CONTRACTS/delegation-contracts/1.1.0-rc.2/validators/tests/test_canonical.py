from __future__ import annotations

import unittest

from cmf_delegation_validators.canonical import (
    CanonicalizationError,
    canonical_bytes,
    canonical_hash,
)


class CanonicalJsonTests(unittest.TestCase):
    def test_keys_are_sorted_and_whitespace_is_removed(self) -> None:
        self.assertEqual(canonical_bytes({"b": 1, "a": 2}), b'{"a":2,"b":1}')

    def test_semantically_equal_objects_have_identical_hashes(self) -> None:
        left = {"z": [3, 2, 1], "a": {"enabled": True}}
        right = {"a": {"enabled": True}, "z": [3, 2, 1]}
        self.assertEqual(canonical_hash(left), canonical_hash(right))

    def test_floats_are_rejected_by_the_protocol_profile(self) -> None:
        with self.assertRaises(CanonicalizationError):
            canonical_bytes({"confidence": 0.5})

    def test_unsafe_integers_are_rejected(self) -> None:
        with self.assertRaises(CanonicalizationError):
            canonical_bytes({"value": 9_007_199_254_740_992})

    def test_lone_surrogates_are_rejected(self) -> None:
        with self.assertRaises(CanonicalizationError):
            canonical_bytes({"value": "\ud800"})


if __name__ == "__main__":
    unittest.main()

