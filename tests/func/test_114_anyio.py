"""Test: anyio"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    import anyio
    from importlib.metadata import version as _v
    av = _v("anyio")
    assert isinstance(av, str) and av, av

    # Pure-sync surface: anyio.Path wraps pathlib.PurePath without touching
    # any async backend machinery. MUST NOT call anyio.run() — asyncio is
    # nonfunctional on Nanvix standalone (socket.socketpair ENOTCONN).
    p = anyio.Path("/tmp") / "anyio-smoke.txt"
    assert p.name == "anyio-smoke.txt", p.name
    assert str(p.parent) == "/tmp", p.parent
    assert p.suffix == ".txt", p.suffix

    print(f"anyio: PASS ({av})")
except Exception as e:
    print(f"anyio: FAIL: {e}")
    sys.exit(1)
