# Statically Linked C Extensions

The following C/C++ libraries are cross-compiled into static archives
and linked directly into the CPython binary as built-in modules. Each
has a corresponding patch documented in
[`patches/`](../patches/).

| Library                                               | Version | Built-in Name                                         | Patch Docs                                                                |
| ----------------------------------------------------- | ------- | ----------------------------------------------------- | ------------------------------------------------------------------------- |
| [NumPy](https://numpy.org/)                           | 1.26.4  | `_np_multiarray_umath`                                | [`numpy_static_builtin.md`](../patches/numpy_static_builtin.md)           |
| [kiwisolver](https://github.com/nucleic/kiwi)         | 1.4.2   | `_kiwi_cext`                                          | [`kiwi_static_builtin.md`](../patches/kiwi_static_builtin.md)             |
| [cymem](https://github.com/explosion/cymem)           | 2.0.11  | `_cymem`                                              | [`cymem_static_builtin.md`](../patches/cymem_static_builtin.md)           |
| [murmurhash](https://github.com/explosion/murmurhash) | 1.0.13  | `_murmurhash_mrmr`                                    | [`murmurhash_static_builtin.md`](../patches/murmurhash_static_builtin.md) |
| [preshed](https://github.com/explosion/preshed)       | 3.0.10  | `_preshed_maps`, `_preshed_counter`, `_preshed_bloom` | [`preshed_static_builtin.md`](../patches/preshed_static_builtin.md)       |
| [srsly](https://github.com/explosion/srsly) (ujson)   | 2.5.1   | `_srsly_ujson`                                        | [`srsly_static_builtin.md`](../patches/srsly_static_builtin.md)           |
| [libexpat](https://github.com/libexpat/libexpat)      | 2.6.4   | *(detected by CPython)*                               | [`libexpat_static.md`](../patches/libexpat_static.md)                     |
| [libffi](https://github.com/libffi/libffi)            | 3.4.6   | *(detected by CPython)*                               | —                                                                         |

## How It Works

CPython's `makesetup` utility does not support dotted module names
(e.g., `cymem.cymem`). Each extension is therefore registered under a
flat name (e.g., `_cymem`) in `Modules/Setup.local`, and a thin
Python-side shim re-exports the symbols under the original dotted
path.

For each library the `patches/` directory contains:

- A **C init-function shim** (`*_builtin.c`) that wraps the static
  library's `PyInit_*` function under the flat name.
- A **Python bridge** (`*_shim.py`) installed into site-packages so
  that `from <package>.<module> import ...` works transparently.
- A **documentation file** (`*_static_builtin.md`) describing the
  problem, fix, and build integration.

See the individual patch docs linked above for full details.
