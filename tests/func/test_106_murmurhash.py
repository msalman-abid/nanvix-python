"""Test: murmurhash"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    from murmurhash.mrmr import hash, hash_unicode, hash_bytes

    # Test hashing a unicode string
    h1 = hash_unicode("hello", 0)
    assert isinstance(h1, int), f"expected int, got {type(h1)}"
    assert h1 != 0, "hash should be non-zero for non-empty input"

    # Test determinism
    h2 = hash_unicode("hello", 0)
    assert h1 == h2, f"hash not deterministic: {h1} != {h2}"

    # Test different seeds produce different hashes
    h3 = hash_unicode("hello", 1)
    assert h1 != h3, "different seeds should produce different hashes"

    print("murmurhash: PASS")
except Exception as e:
    print(f"murmurhash: FAIL: {e}")
    sys.exit(1)
