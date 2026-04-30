# Statically Linked C Extensions

> **Note:** C extension packages have been temporarily removed from this
> distribution. Only CPython's own built-in dependencies (libexpat and
> libffi) are currently included. The extension packages listed below
> will be re-added in a future release.

## CPython Built-in Dependencies

These C libraries are linked into CPython itself and are **not**
separate pip packages:

| Library                                          | Version | CPython Module   | Notes                                                    |
| ------------------------------------------------ | ------- | ---------------- | -------------------------------------------------------- |
| [libexpat](https://github.com/libexpat/libexpat) | 2.6.4   | `pyexpat`        | [`libexpat_static.md`](../patches/libexpat_static.md)    |
| [libffi](https://github.com/libffi/libffi)       | 3.4.6   | `_ctypes`        | Provided via `nanvix.toml` dependency                    |

## Previously Supported Extensions (Temporarily Removed)

The following C extension packages were previously cross-compiled and
statically linked. They will be restored in a future release:

- NumPy 1.26.4
- kiwisolver 1.4.2
- cymem 2.0.11
- murmurhash 1.0.13
- preshed 3.0.10
- srsly (ujson) 2.5.1
