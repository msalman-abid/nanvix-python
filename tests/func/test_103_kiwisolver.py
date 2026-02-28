"""Test: kiwisolver"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    import kiwisolver
    from kiwisolver import Variable, Solver, Constraint, Expression, strength

    # Verify version is accessible
    assert hasattr(kiwisolver, '__version__'), "missing __version__"

    # Create a simple constraint system and solve it
    solver = Solver()
    x = Variable('x')
    y = Variable('y')

    # x + y == 10
    solver.addConstraint(x + y == 10)
    # x == 2 * y
    solver.addConstraint(x == 2 * y)

    solver.updateVariables()

    # x should be ~6.667 and y should be ~3.333
    assert abs(x.value() - 20.0 / 3.0) < 1e-6, f"x={x.value()}, expected {20.0/3.0}"
    assert abs(y.value() - 10.0 / 3.0) < 1e-6, f"y={y.value()}, expected {10.0/3.0}"

    print("kiwisolver: PASS")
except Exception as e:
    print(f"kiwisolver: FAIL: {e}")
    sys.exit(1)
