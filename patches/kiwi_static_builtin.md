# Kiwisolver Static Built-in Patch for Nanvix

This patch integrates [kiwisolver](https://github.com/nucleic/kiwi) 1.4.5
(the Python bindings for the Kiwi C++ Cassowary constraint solver) as a
**statically linked built-in module** in the CPython binary on Nanvix.

Three patch files are involved:

| File                        | Purpose                                                                                             |
| --------------------------- | --------------------------------------------------------------------------------------------------- |
| `patches/kiwi_builtin.c`    | C init-function shim for CPython `Modules/Setup.local`                                              |
| `patches/kiwi_cext_shim.py` | Python-side bridge installed as `kiwisolver/_cext.py`                                               |
| `z` (build script)          | Build orchestration: compiles `libkiwisolver.a`, links it into CPython, installs the Python package |

---

## 1. Init-function shim (`kiwi_builtin.c`)

### Problem

CPython's `makesetup` utility does not support dotted module names.
Kiwisolver's C++ extension is normally installed as `kiwisolver._cext`
(a sub-module), but `makesetup` requires a flat, non-dotted name for
the `Modules/Setup.local` entry.

### Fix

The kiwisolver static library (`libkiwisolver.a`) exports
`PyInit__cext`.  The shim provides a thin wrapper function
`PyInit__kiwi_cext` that simply forwards to `PyInit__cext`:

```c
extern PyObject* PyInit__cext(void);

PyMODINIT_FUNC
PyInit__kiwi_cext(void)
{
    return PyInit__cext();
}
```

The corresponding `Modules/Setup.local` entry registers the built-in
as `_kiwi_cext` and links against `libkiwisolver.a` plus `libstdc++`
(required by the C++ solver code):

```text
_kiwi_cext kiwi_builtin.c -lkiwisolver -lstdc++
```

---

## 2. Python-side bridge (`kiwi_cext_shim.py`)

### Problem — dotted import fails

Kiwisolver's `__init__.py` imports its native extension via
`from ._cext import ...`, which resolves to `kiwisolver._cext`.  The
built-in module is registered under the flat name `_kiwi_cext`, so the
standard dotted import path fails.

### Fix — re-export shim

The shim is installed as `kiwisolver/_cext.py` in the site-packages
directory, replacing the native `.so` that would normally be there.
It re-exports all symbols from the built-in:

```python
from _kiwi_cext import *
from _kiwi_cext import __kiwi_version__, __version__, strength
```

This allows the existing `kiwisolver/__init__.py` to work unmodified —
`from ._cext import Solver, Variable, ...` resolves through the shim
to the statically linked built-in.

---

## 3. Build integration (`z` script)

The `./z` build script orchestrates the following steps for kiwisolver:

### Setup phase (`./z setup`)

* Registers `deps/kiwi` as a git safe directory.
* Configures git excludes for build artifacts (`libkiwisolver.a`, `*.o`).
* Installs **cppy** (a C++ / Python header-only library required by
  kiwisolver) into the build virtual environment.

### Build phase (`./z build`)

1. **Install cppy headers** into the sysroot (`$SYSROOT/include/`) so
   they are accessible in Docker cross-compilation builds.
2. **Install kiwi C++ headers** (`kiwi/*.h`) into the sysroot so that
   `#include <kiwi/kiwi.h>` resolves inside the Docker container where
   the host `$(CURDIR)` path is not available.
3. **Cross-compile `libkiwisolver.a`** using the kiwi submodule's own
   `Makefile.nanvix`, with `CPPY_INCLUDE` pointing to the sysroot.
4. **Copy `libkiwisolver.a`** into `$SYSROOT/lib/`.
5. **Register `_kiwi_cext`** in CPython's `Modules/Setup.local` and
   copy `kiwi_builtin.c` into `Modules/`.
6. **Install the kiwisolver Python package** from
   `deps/kiwi/py/kiwisolver/` into the sysroot site-packages, with
   the `_cext.py` shim replacing the native extension.

---

## Companion files

| File                                    | Role                                                                          |
| --------------------------------------- | ----------------------------------------------------------------------------- |
| `deps/kiwi/Makefile.nanvix`             | Cross-compilation Makefile (lives in the submodule)                           |
| `deps/kiwi/py/kiwisolver/__init__.py`   | Upstream Python package entry point (unmodified)                              |
| `deps/kiwi/py/kiwisolver/exceptions.py` | Upstream exception classes (unmodified)                                       |
| `tests/func/test_103_kiwisolver.py`     | Functional test: creates a constraint system, solves it, and verifies results |
