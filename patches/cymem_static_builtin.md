# Cymem Static Built-in Patch for Nanvix

This patch integrates [cymem](https://github.com/explosion/cymem) (a
Cython memory pool helper used by spaCy) as a **statically linked
built-in module** in the CPython binary on Nanvix.

Two patch files are involved:

| File                      | Purpose                                                |
| ------------------------- | ------------------------------------------------------ |
| `patches/cymem_builtin.c` | C init-function shim for CPython `Modules/Setup.local` |
| `patches/cymem_shim.py`   | Python-side bridge installed as `cymem/cymem.py`       |

---

## 1. Init-function shim (`cymem_builtin.c`)

### Problem — dotted module names unsupported

CPython's `makesetup` utility does not support dotted module names.
Cymem's Cython extension is normally installed as `cymem.cymem` (a
sub-module), but `makesetup` requires a flat, non-dotted name for the
`Modules/Setup.local` entry.

### Fix — flat-name wrapper

The cymem static library (`libcymem.a`) exports `PyInit_cymem`.  The
shim provides a thin wrapper function `PyInit__cymem` that simply
forwards to `PyInit_cymem`:

```c
extern PyObject* PyInit_cymem(void);

PyMODINIT_FUNC
PyInit__cymem(void)
{
    return PyInit_cymem();
}
```

The corresponding `Modules/Setup.local` entry registers the built-in
as `_cymem` and links against `libcymem.a`:

```text
_cymem cymem_builtin.c -lcymem
```

---

## 2. Python-side bridge (`cymem_shim.py`)

### Problem — dotted import fails

Cymem's package code imports the native extension via
`from cymem.cymem import Pool`, which resolves to the `cymem.cymem`
sub-module.  The built-in module is registered under the flat name
`_cymem`, so the standard dotted import path fails.

### Fix — re-export shim

The shim is installed as `cymem/cymem.py` in the site-packages
directory, replacing the native `.so` that would normally be there.
It re-exports all symbols from the built-in:

```python
from _cymem import *
```

This allows existing code to call `from cymem.cymem import Pool`
transparently — the import resolves through the shim to the statically
linked built-in.

---

## Build integration (`z` script)

### Setup phase (`./z setup`)

* Registers `deps/cymem` as a git safe directory.
* Configures git excludes for build artifacts (`libcymem.a`, `*.o`).

### Build phase (`./z build`)

1. **Install CPython headers** into the sysroot so cymem can compile
   against them.
2. **Cross-compile `libcymem.a`** using the submodule's `Makefile.nanvix`.
3. **Copy `libcymem.a`** into `$SYSROOT/lib/`.
4. **Register `_cymem`** in CPython's `Modules/Setup.local` and copy
   `cymem_builtin.c` into `Modules/`.
5. **Install the Python shim** as `cymem/cymem.py` in site-packages.

---

## Companion files

| File                           | Role                                                |
| ------------------------------ | --------------------------------------------------- |
| `deps/cymem/Makefile.nanvix`   | Cross-compilation Makefile (lives in the submodule) |
| `tests/func/test_101_cymem.py` | Functional test: `from cymem.cymem import Pool`     |
