"""Test: numpy"""
import sys

sys.stdout.reconfigure(line_buffering=True)

try:
    import numpy as np

    arr = np.array([1, 2, 3], dtype=np.int32)
    assert int(arr.sum()) == 6
    assert arr.dtype == np.int32
    print("numpy: PASS")
except Exception as e:
    print(f"numpy: FAIL: {e}")
    sys.exit(1)
