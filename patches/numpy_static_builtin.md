# NumPy Static Built-in Patch for Nanvix

This patch modifies NumPy 1.26.4 so that its core C extension
(`_multiarray_umath`) can be **statically linked into the CPython binary**
as a built-in module on the Nanvix microkernel.

Two files are touched:

| File | Purpose |
|------|---------|
| `numpy/core/src/common/npy_cpu_features.c` | CPU feature detection |
| `numpy/core/src/multiarray/multiarraymodule.c` | Module initialisation |

---

## 1. CPU feature detection (`npy_cpu_features.c`)

### Problem

NumPy probes the host CPU at import time with the privileged `CPUID` and
`XGETBV` instructions (inline assembly).  On Nanvix these instructions
are not emulated in user mode and cause the process to **hang
indefinitely**.

### Fix

Guard both `npy__cpu_cpuid()` and `npy__cpu_getxcr0()` with
`#ifdef __nanvix__` so that on Nanvix they return zeroed-out results
instead of executing the instructions.  NumPy then treats the CPU as
having no optional SIMD extensions, which is correct for the Nanvix
i686 target.

---

## 2. Module initialisation (`multiarraymodule.c`)

Three separate issues are addressed in this file.

### 2a. Import-lock deadlock during `npy_cache_import`

#### Problem

`initialize_static_globals()` calls
`npy_cache_import("numpy.exceptions", ...)` and
`npy_cache_import("numpy.core._exceptions", ...)`.  These trigger
`import numpy`, which in turn imports `numpy.core._multiarray_umath` —
the very module whose `PyInit` is currently executing.  Because CPython
holds a **per-module import lock** for the duration of `PyInit`, the
re-entrant import attempt deadlocks.

#### Fix

Wrap both `npy_cache_import` calls in `#ifndef __nanvix__`.  The two
global pointers (`npy_DTypePromotionError`, `npy_UFuncNoLoopError`)
remain `NULL` after init; they are populated lazily by
`npy_cache_import`'s own `*cache == NULL` guard on first actual use.

An early-return guard (`if (npy_DTypePromotionError != NULL && …)`) is
also added so that a re-entrant call into `initialize_static_globals()`
is a harmless no-op instead of hitting the original `assert()` (which
would abort the process).

### 2b. Module renamed to `_np_multiarray_umath`

#### Problem

If the built-in is registered under the canonical name
`_multiarray_umath`, any Python code that does
`import _multiarray_umath` during `PyInit` will re-enter the same
`PyInit` function (import-lock deadlock, same as 2a but from a different
call site).

#### Fix

On Nanvix the module name in `PyModuleDef` is changed to
`_np_multiarray_umath` and the init function is renamed to
`PyInit__np_multiarray_umath`.  A meta-path finder installed in
`sitecustomize.py` at runtime redirects all imports of the dotted name
(`numpy.core._multiarray_umath`) to the renamed flat built-in, breaking
the circular chain.

### 2c. Pre-registration in `sys.modules`

#### Problem

CPython only adds a built-in module to `sys.modules` **after** `PyInit`
returns.  Any Python-level import triggered during `PyInit` (e.g.
`import datetime` via `PyDateTime_IMPORT`) that transitively tries to
resolve `numpy.core._multiarray_umath` will not find the module in
`sys.modules` yet, causing an `ImportError` or a second call to
`PyInit`.

#### Fix

Immediately after `PyModule_Create`, the partially-initialised module
object is inserted into `sys.modules` under three keys:

| Key | Why |
|-----|-----|
| `_np_multiarray_umath` | The built-in's own name |
| `_multiarray_umath` | The name NumPy Python code expects |
| `numpy.core._multiarray_umath` | The fully-qualified dotted path |

This lets the import machinery return the already-created (but not yet
fully populated) module object instead of calling `PyInit` again.

---

## Runtime companion: `nanvix_numpy_bootstrap.py`

The patch alone is not sufficient — a Python-side `sitecustomize.py`
module (`patches/nanvix_numpy_bootstrap.py`) is installed alongside
NumPy.  It provides:

* A **`find_spec`-based meta-path finder** that intercepts
  `import numpy.core._multiarray_umath` (and similar dotted paths) and
  redirects them to the renamed `_np_multiarray_umath` built-in.
* **Permissive stub modules** (`_StubModule`) for C extensions that are
  not statically linked (e.g. `_multiarray_tests`, `_simd`, linalg,
  fft, random sub-modules).  These stubs have `__all__ = []` and a
  `__getattr__` that returns `None`, allowing NumPy's init to complete
  without those extensions.

---

## Companion files

| File | Role |
|------|------|
| `patches/numpy_libm_compat.c` | Provides `__kernel_tanl` stub missing from Nanvix newlib |
| `patches/nanvix_numpy_bootstrap.py` | Runtime meta-path finder and stub modules |
