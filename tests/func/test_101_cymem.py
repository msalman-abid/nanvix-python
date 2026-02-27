"""Test: cymem"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    from cymem.cymem import Pool
    mem = Pool()
    assert mem.size == 0
    print("cymem: PASS")
except Exception as e:
    print(f"cymem: FAIL: {e}")
    sys.exit(1)
