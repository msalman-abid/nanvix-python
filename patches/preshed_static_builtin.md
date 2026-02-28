# Preshed Static Built-in Patch for Nanvix

This patch integrates [preshed](https://github.com/explosion/preshed)
(Cython hash table data structures used by spaCy) as **statically
linked built-in modules** in the CPython binary on Nanvix.

Preshed ships three Cython extensions that are all compiled into a
single static archive (`libpreshed.a`) and registered as separate
CPython built-ins.

Four patch files are involved:

| File                              | Purpose                                              |
| --------------------------------- | ---------------------------------------------------- |
| `patches/preshed_builtin.c`       | C init-function shims for all three preshed modules  |
| `patches/preshed_maps_shim.py`    | Python-side bridge installed as `preshed/maps.py`    |
| `patches/preshed_counter_shim.py` | Python-side bridge installed as `preshed/counter.py` |
| `patches/preshed_bloom_shim.py`   | Python-side bridge installed as `preshed/bloom.py`   |

---

## 1. Init-function shims (`preshed_builtin.c`)

### Problem — dotted module names unsupported

CPython's `makesetup` utility does not support dotted module names.
Preshed's Cython extensions are normally installed as `preshed.maps`,
`preshed.counter`, and `preshed.bloom`, but `makesetup` requires flat,
non-dotted names for the `Modules/Setup.local` entries.

### Fix — flat-name wrappers

The static library (`libpreshed.a`) exports `PyInit_maps`,
`PyInit_counter`, and `PyInit_bloom`.  The shim file provides three
thin wrapper functions that forward to these init functions:

```c
extern PyObject* PyInit_maps(void);
extern PyObject* PyInit_counter(void);
extern PyObject* PyInit_bloom(void);

PyMODINIT_FUNC PyInit__preshed_maps(void)    { return PyInit_maps(); }
PyMODINIT_FUNC PyInit__preshed_counter(void) { return PyInit_counter(); }
PyMODINIT_FUNC PyInit__preshed_bloom(void)   { return PyInit_bloom(); }
```

The corresponding `Modules/Setup.local` entries register each built-in
under its flat name and link against `libpreshed.a`:

```text
_preshed_maps    preshed_builtin.c -lpreshed
_preshed_counter preshed_builtin.c -lpreshed
_preshed_bloom   preshed_builtin.c -lpreshed
```

---

## 2. Python-side bridges (shim files)

### Problem — dotted imports fail

The preshed package imports its native extensions via dotted paths
(e.g., `from preshed.maps import PreshMap`).  The built-ins are
registered under flat names (`_preshed_maps`, `_preshed_counter`,
`_preshed_bloom`), so the standard import paths fail.

### Fix — re-export shims

Each shim is installed into the `preshed/` site-packages directory,
replacing the native `.so` that would normally be there:

| Shim file                 | Installed as         | Re-exports from    |
| ------------------------- | -------------------- | ------------------ |
| `preshed_maps_shim.py`    | `preshed/maps.py`    | `_preshed_maps`    |
| `preshed_counter_shim.py` | `preshed/counter.py` | `_preshed_counter` |
| `preshed_bloom_shim.py`   | `preshed/bloom.py`   | `_preshed_bloom`   |

Each shim simply re-exports all symbols:

```python
from _preshed_maps import *    # maps.py
from _preshed_counter import * # counter.py
from _preshed_bloom import *   # bloom.py
```

---

## Build integration (`z` script)

### Setup phase (`./z setup`)

* Registers `deps/preshed` as a git safe directory.
* Configures git excludes for build artifacts (`libpreshed.a`, `*.o`).

### Build phase (`./z build`)

1. **Cross-compile `libpreshed.a`** using the submodule's
   `Makefile.nanvix`, with `CYMEM_DIR` and `MURMURHASH_DIR` pointing
   to their respective submodules (preshed depends on cymem and
   murmurhash headers).
2. **Copy `libpreshed.a`** into `$SYSROOT/lib/`.
3. **Register `_preshed_maps`, `_preshed_counter`, and
   `_preshed_bloom`** in CPython's `Modules/Setup.local` and copy
   `preshed_builtin.c` into `Modules/`.
4. **Install the preshed Python package** into site-packages with the
   three shims replacing `maps.py`, `counter.py`, and `bloom.py`.

---

## Companion files

| File                             | Role                                                 |
| -------------------------------- | ---------------------------------------------------- |
| `deps/preshed/Makefile.nanvix`   | Cross-compilation Makefile (lives in the submodule)  |
| `tests/func/test_107_preshed.py` | Functional test: `from preshed.maps import PreshMap` |
