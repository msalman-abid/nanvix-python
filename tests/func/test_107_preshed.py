"""Test: preshed"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    from preshed.maps import PreshMap

    # Create a hash map and insert/retrieve values
    table = PreshMap()
    table[12345] = 42
    assert table[12345] == 42, f"expected 42, got {table[12345]}"

    table[67890] = 99
    assert table[67890] == 99, f"expected 99, got {table[67890]}"
    assert len(table) == 2, f"expected length 2, got {len(table)}"

    print("preshed: PASS")
except Exception as e:
    print(f"preshed: FAIL: {e}")
    sys.exit(1)
