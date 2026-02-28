"""
Lazy import redirector for NumPy built-in modules on Nanvix.
"""
import importlib
import importlib.abc
import importlib.machinery
import sys
import types

_ALIASES = {
    "numpy.core._multiarray_umath": "_np_multiarray_umath",
    "numpy._core._multiarray_umath": "_np_multiarray_umath",
    "_multiarray_umath": "_np_multiarray_umath",
}

# C extension modules that are not statically linked but numpy tries
# to import them during init.  Provide permissive stubs so init succeeds.
_STUBS = {
    "numpy.core._multiarray_tests",
    "numpy.core._simd",
    "numpy.linalg._umath_linalg",
    "numpy.linalg.lapack_lite",
    "numpy.fft._pocketfft_internal",
    "numpy.random._common",
    "numpy.random._bounded_integers",
    "numpy.random._generator",
    "numpy.random._mt19937",
    "numpy.random._pcg64",
    "numpy.random._philox",
    "numpy.random._sfc64",
    "numpy.random.bit_generator",
    "numpy.random.mtrand",
}

_loading = set()


class _StubModule(types.ModuleType):
    __all__ = []
    """Module stub that returns None for any missing attribute."""
    def __getattr__(self, name):
        return None


class _NanvixLoader(importlib.abc.Loader):
    def __init__(self, fullname):
        self._fullname = fullname

    def create_module(self, spec):
        fullname = self._fullname

        if fullname in _STUBS:
            mod = _StubModule(fullname)
            mod.__file__ = "<nanvix-stub>"
            return mod

        builtin_name = _ALIASES.get(fullname)
        if not builtin_name:
            return None

        # Try sys.modules first (C-level pre-registration)
        mod = sys.modules.get(builtin_name)
        if mod is not None:
            return mod

        _loading.add(fullname)
        try:
            mod = importlib.import_module(builtin_name)
        finally:
            _loading.discard(fullname)
        return mod

    def exec_module(self, module):
        fullname = self._fullname
        sys.modules[fullname] = module
        if fullname != "_multiarray_umath" and fullname in _ALIASES:
            sys.modules["_multiarray_umath"] = module


class _NanvixNumpyFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname in _STUBS:
            return importlib.machinery.ModuleSpec(fullname, _NanvixLoader(fullname))
        if fullname in _ALIASES and fullname not in _loading:
            return importlib.machinery.ModuleSpec(fullname, _NanvixLoader(fullname))
        return None


sys.meta_path.insert(0, _NanvixNumpyFinder())
