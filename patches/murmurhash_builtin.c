/*
 * murmurhash_builtin.c - Shim to register murmurhash.mrmr as a CPython built-in module.
 *
 * The static library (libmurmurhash.a) exports PyInit_mrmr.
 * This wrapper provides PyInit__murmurhash_mrmr so the name matches the
 * entry in Modules/Setup.local.
 */

#include "Python.h"

extern PyObject* PyInit_mrmr(void);

PyMODINIT_FUNC
PyInit__murmurhash_mrmr(void)
{
    return PyInit_mrmr();
}
