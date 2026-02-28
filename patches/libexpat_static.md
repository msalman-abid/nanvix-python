# Libexpat Static Library Integration for Nanvix

This patch integrates [libexpat](https://github.com/libexpat/libexpat) 2.6.4
as a **statically compiled C library** in the Nanvix sysroot, enabling
CPython's `pyexpat` module to function correctly.

## Overview

libexpat is a stream-oriented XML parser library written in C99. CPython's
`xml.parsers.expat` module (and by extension `xml.etree.ElementTree`) depends
on libexpat for XML parsing functionality.

## Build Integration (`z` script)

### Setup phase (`./z setup`)

* Registers `deps/libexpat` as a git safe directory.
* Configures git excludes for build artifacts (`libexpat.a`, `*.o`,
  `expat_test.elf`).

### Build phase (`./z build`)

1. **Cross-compile `libexpat.a`** using the submodule's `Makefile.nanvix`,
   which compiles `xmlparse.c`, `xmlrole.c`, and `xmltok.c` from
   `expat/lib/`.
2. **Install `libexpat.a`** into `$SYSROOT/lib/`.
3. **Install headers** (`expat.h`, `expat_external.h`) into
   `$SYSROOT/include/`.

No CPython built-in module registration is needed — CPython's own build
system detects `libexpat.a` and headers in the sysroot and links the
`pyexpat` extension module accordingly.

## Companion files

| File | Role |
|------|------|
| `deps/libexpat/Makefile.nanvix` | Cross-compilation Makefile (lives in the submodule) |
| `deps/libexpat/expat/lib/expat.h` | Public API header |
| `tests/func/test_104_libexpat.py` | Functional test: XML parsing via `xml.parsers.expat` |
