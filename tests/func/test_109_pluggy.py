"""Test: pluggy"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    import pluggy
    hookspec = pluggy.HookspecMarker("nanvix_smoke")
    hookimpl = pluggy.HookimplMarker("nanvix_smoke")

    class Spec:
        @hookspec
        def add(self, a, b): ...

    class Impl:
        @hookimpl
        def add(self, a, b):
            return a + b

    pm = pluggy.PluginManager("nanvix_smoke")
    pm.add_hookspecs(Spec)
    pm.register(Impl())
    results = pm.hook.add(a=2, b=3)
    assert results == [5], results
    print("pluggy: PASS")
except Exception as e:
    print(f"pluggy: FAIL: {e}")
    sys.exit(1)
