# Srsly Static Built-in Patch for Nanvix

This patch integrates [srsly](https://github.com/explosion/srsly)'s
ujson (UltraJSON) C extension as a **statically linked built-in
module** in the CPython binary on Nanvix.  Srsly is a serialisation
library used by spaCy for fast JSON, MessagePack, and JSONL I/O.

Three patch files are involved:

| File                                | Purpose                                                |
| ----------------------------------- | ------------------------------------------------------ |
| `patches/srsly_ujson_builtin.c`     | C init-function shim for CPython `Modules/Setup.local` |
| `patches/srsly_ujson_shim.py`       | Python-side bridge installed as `srsly/ujson/ujson.py` |
| `patches/nanvix_srsly_bootstrap.py` | Runtime bootstrap appended to `sitecustomize.py`       |

---

## 1. Init-function shim (`srsly_ujson_builtin.c`)

### Problem — dotted module names unsupported

CPython's `makesetup` utility does not support dotted module names.
Srsly's ujson C extension is normally installed as `srsly.ujson.ujson`
(a deeply nested sub-module), but `makesetup` requires a flat,
non-dotted name for the `Modules/Setup.local` entry.

### Fix — flat-name wrapper

The static library (`libsrsly_ujson.a`) exports `PyInit_ujson`.  The
shim provides a thin wrapper function `PyInit__srsly_ujson` that
simply forwards to `PyInit_ujson`:

```c
extern PyObject* PyInit_ujson(void);

PyMODINIT_FUNC
PyInit__srsly_ujson(void)
{
    return PyInit_ujson();
}
```

The corresponding `Modules/Setup.local` entry registers the built-in
as `_srsly_ujson` and links against `libsrsly_ujson.a`:

```text
_srsly_ujson srsly_ujson_builtin.c -lsrsly_ujson
```

---

## 2. Python-side bridge (`srsly_ujson_shim.py`)

### Problem — dotted import fails

Srsly's code imports the ujson C extension via `srsly.ujson.ujson`,
which resolves to a nested sub-module.  The built-in is registered
under the flat name `_srsly_ujson`, so the standard dotted import
fails.

### Fix — sys.modules registration shim

The shim is installed as `srsly/ujson/ujson.py` in the site-packages
directory, replacing the native `.so`.  It registers the built-in
module under the expected dotted name in `sys.modules` and re-exports
all symbols:

```python
import sys
import _srsly_ujson

sys.modules[__name__] = _srsly_ujson
sys.modules['srsly.ujson.ujson'] = _srsly_ujson

from _srsly_ujson import *
```

---

## 3. Runtime bootstrap (`nanvix_srsly_bootstrap.py`)

### Problem — early import ordering

Some import paths in srsly resolve `srsly.ujson.ujson` before the
shim file has been loaded, causing an `ImportError`.

### Fix — eager pre-registration

The bootstrap script is appended to CPython's `sitecustomize.py`
(which runs during interpreter startup).  It eagerly imports
`_srsly_ujson` and pre-registers the module under its expected dotted
name in `sys.modules`:

```python
def _register_srsly_builtins():
    mod = importlib.import_module("_srsly_ujson")
    mod.__name__ = "srsly.ujson.ujson"
    mod.__package__ = "srsly.ujson"
    sys.modules["srsly.ujson.ujson"] = mod
```

This ensures the import chain works regardless of the order in which
srsly sub-modules are loaded.

---

## Build integration (`z` script)

### Setup phase (`./z setup`)

* Registers `deps/srsly` as a git safe directory.
* Configures git excludes for build artifacts (`libsrsly_ujson.a`,
  `*.o`).

### Build phase (`./z build`)

1. **Cross-compile `libsrsly_ujson.a`** using the submodule's
   `Makefile.nanvix`.
2. **Copy `libsrsly_ujson.a`** into `$SYSROOT/lib/`.
3. **Register `_srsly_ujson`** in CPython's `Modules/Setup.local` and
   copy `srsly_ujson_builtin.c` into `Modules/`.
4. **Install the srsly Python package** into site-packages with the
   shim replacing `srsly/ujson/ujson.py`.
5. **Append `nanvix_srsly_bootstrap.py`** to `sitecustomize.py` for
   early module registration.

---

## Companion files

| File                           | Role                                                   |
| ------------------------------ | ------------------------------------------------------ |
| `deps/srsly/Makefile.nanvix`   | Cross-compilation Makefile (lives in the submodule)    |
| `tests/func/test_108_srsly.py` | Functional test: `import srsly; srsly.json_dumps(...)` |
