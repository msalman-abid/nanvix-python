/*
 * cymem_builtin.c - Shim to register cymem as a CPython built-in module.
 *
 * makesetup does not support dotted module names, so the Cython extension
 * is registered under the flat name "_cymem".  A pure-Python shim at
 * cymem/cymem.py re-exports everything via `from _cymem import *`,
 * making `from cymem.cymem import Pool` work transparently.
 *
 * The Cython-generated code in libcymem.a exports PyInit_cymem.
 * This wrapper provides PyInit__cymem so the name matches the
 * entry in Modules/Setup.local.
 */

#include "Python.h"

extern PyObject* PyInit_cymem(void);

PyMODINIT_FUNC
PyInit__cymem(void)
{
    return PyInit_cymem();
}
