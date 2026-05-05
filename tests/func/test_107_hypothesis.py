"""Test: hypothesis"""

import sys

sys.stdout.reconfigure(line_buffering=True)
try:
    from hypothesis import given, settings, strategies as st

    @settings(max_examples=10, deadline=None)
    @given(x=st.integers(), y=st.integers())
    def test_addition_commutative(x, y):
        assert x + y == y + x

    test_addition_commutative()
    print("hypothesis: PASS")
except Exception as e:
    print(f"hypothesis: FAIL: {e}")
    sys.exit(1)
