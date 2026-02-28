# kiwisolver/_cext.py - Pure-Python bridge to the _kiwi_cext built-in module.
#
# The C++ extension is statically linked into the CPython binary as the
# built-in module "_kiwi_cext".  This shim re-exports its contents so that the
# standard import path `from kiwisolver._cext import ...` keeps working.

from _kiwi_cext import *  # noqa: F401,F403
from _kiwi_cext import __kiwi_version__, __version__, strength  # noqa: F401
