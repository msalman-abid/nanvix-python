"""Test: pytest"""
import os
import sys
import tempfile
sys.stdout.reconfigure(line_buffering=True)
try:
    import pytest

    tmpdir = tempfile.mkdtemp()
    pass_dir = os.path.join(tmpdir, "pass")
    fail_dir = os.path.join(tmpdir, "fail")
    os.mkdir(pass_dir)
    os.mkdir(fail_dir)
    with open(os.path.join(pass_dir, "test_pass.py"), "w") as f:
        f.write("def test_ok():\n    assert 1 + 1 == 2\n")
    with open(os.path.join(fail_dir, "test_fail.py"), "w") as f:
        f.write("def test_bad():\n    assert 1 + 1 == 3\n")

    rc_pass = pytest.main([pass_dir, "-p", "no:faulthandler", "-p", "no:logging", "-p", "no:cacheprovider", "--capture=sys"])
    assert rc_pass == pytest.ExitCode.OK, rc_pass

    rc_fail = pytest.main([fail_dir, "-p", "no:faulthandler", "-p", "no:logging", "-p", "no:cacheprovider", "--capture=sys"])
    assert rc_fail == pytest.ExitCode.TESTS_FAILED, rc_fail

    print("pytest: PASS")
except Exception as e:
    print(f"pytest: FAIL: {e}")
    sys.exit(1)
