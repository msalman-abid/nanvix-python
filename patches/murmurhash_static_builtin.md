# MurmurHash Static Built-in Patch for Nanvix

This patch integrates
[murmurhash](https://github.com/explosion/murmurhash) (Cython bindings
for MurmurHash2/3, used by spaCy's preshed and other NLP libraries)
as a **statically linked built-in module** in the CPython binary on
Nanvix.

Three patch files are involved:

| File                                | Purpose                                                 |
| ----------------------------------- | ------------------------------------------------------- |
| `patches/murmurhash_builtin.c`      | C init-function shim for CPython `Modules/Setup.local`  |
| `patches/murmurhash_cwrap_nanvix.c` | Fixed C wrapper for C++ name-mangled MurmurHash symbols |
| `patches/murmurhash_mrmr_shim.py`   | Python-side bridge installed as `murmurhash/mrmr.py`    |

---

## 1. Init-function shim (`murmurhash_builtin.c`)

### Problem — dotted module names unsupported

CPython's `makesetup` utility does not support dotted module names.
MurmurHash's Cython extension is normally installed as
`murmurhash.mrmr` (a sub-module), but `makesetup` requires a flat,
non-dotted name for the `Modules/Setup.local` entry.

### Fix — flat-name wrapper

The static library (`libmurmurhash.a`) exports `PyInit_mrmr`.  The
shim provides a thin wrapper function `PyInit__murmurhash_mrmr` that
simply forwards to `PyInit_mrmr`:

```c
extern PyObject* PyInit_mrmr(void);

PyMODINIT_FUNC
PyInit__murmurhash_mrmr(void)
{
    return PyInit_mrmr();
}
```

The corresponding `Modules/Setup.local` entry registers the built-in
as `_murmurhash_mrmr` and links against `libmurmurhash.a` plus
`libstdc++` (required by the C++ hash implementations):

```text
_murmurhash_mrmr murmurhash_builtin.c -lmurmurhash -lstdc++
```

---

## 2. C wrapper for name-mangled symbols (`murmurhash_cwrap_nanvix.c`)

### Problem — incorrect mangled names

The upstream `murmurhash_cwrap.c` references specific C++ mangled
symbol names for MurmurHash3 functions that do not match the actual
symbols produced by the Nanvix cross-compiler.  MurmurHash2 functions
are compiled with C++ linkage (mangled names), while MurmurHash3
functions use `extern "C"` linkage (unmangled).

### Fix — corrected symbol references

The replacement wrapper correctly references:

* **MurmurHash2** (C++ linkage): Uses the actual mangled names
  (`_Z13MurmurHash64APKviy`, `_Z13MurmurHash64BPKviy`) and provides
  unmangled C wrappers `MurmurHash64A` / `MurmurHash64B`.
* **MurmurHash3** (`extern "C"` linkage): No wrappers needed — the
  linker resolves the unmangled symbols directly from `MurmurHash3.o`.

This file replaces the upstream `murmurhash/murmurhash_cwrap.c` during
the build.

---

## 3. Python-side bridge (`murmurhash_mrmr_shim.py`)

### Problem — dotted import fails

The murmurhash package imports its native extension via
`from murmurhash.mrmr import hash64`, which resolves to the
`murmurhash.mrmr` sub-module.  The built-in is registered under the
flat name `_murmurhash_mrmr`, so the standard dotted import fails.

### Fix — re-export shim

The shim is installed as `murmurhash/mrmr.py` in the site-packages
directory, replacing the native `.so`.  It re-exports all symbols:

```python
from _murmurhash_mrmr import *
```

---

## Build integration (`z` script)

### Setup phase (`./z setup`)

* Registers `deps/murmurhash` as a git safe directory.
* Configures git excludes for build artifacts (`libmurmurhash.a`,
  `*.o`).

### Build phase (`./z build`)

1. **Copy the fixed C wrapper** (`murmurhash_cwrap_nanvix.c`) into the
   submodule as `murmurhash/murmurhash_cwrap.c`.
2. **Cross-compile `libmurmurhash.a`** using the submodule's
   `Makefile.nanvix`.
3. **Copy `libmurmurhash.a`** into `$SYSROOT/lib/`.
4. **Register `_murmurhash_mrmr`** in CPython's `Modules/Setup.local`
   and copy `murmurhash_builtin.c` into `Modules/`.
5. **Install the murmurhash Python package** into site-packages with
   the shim replacing `mrmr.py`.

---

## Companion files

| File                                | Role                                                  |
| ----------------------------------- | ----------------------------------------------------- |
| `deps/murmurhash/Makefile.nanvix`   | Cross-compilation Makefile (lives in the submodule)   |
| `tests/func/test_106_murmurhash.py` | Functional test: `from murmurhash.mrmr import hash64` |
