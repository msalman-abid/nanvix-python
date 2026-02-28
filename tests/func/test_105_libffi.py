"""Test: libffi (via ctypes)"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    import ctypes

    # Verify ctypes module loads (depends on libffi)
    assert hasattr(ctypes, 'c_int'), "missing c_int type"
    assert hasattr(ctypes, 'CDLL'), "missing CDLL"

    # Test basic ctypes type operations
    val = ctypes.c_int(42)
    assert val.value == 42, f"c_int value mismatch: {val.value}"

    arr_type = ctypes.c_int * 3
    arr = arr_type(1, 2, 3)
    assert list(arr) == [1, 2, 3], f"array mismatch: {list(arr)}"

    print("libffi: PASS")
except Exception as e:
    print(f"libffi: FAIL: {e}")
    sys.exit(1)
