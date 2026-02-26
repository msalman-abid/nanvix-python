# cymem/cymem.py - Pure-Python bridge to the _cymem built-in module.
#
# The Cython extension is statically linked into the CPython binary as the
# built-in module "_cymem".  This shim re-exports its contents so that the
# standard import path `from cymem.cymem import Pool` keeps working.

from _cymem import *  # noqa: F401,F403
