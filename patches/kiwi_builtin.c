/*
 * kiwi_builtin.c - Shim to register kiwisolver._cext as a CPython built-in module.
 *
 * makesetup does not support dotted module names, so the C++ extension
 * is registered under the flat name "_kiwi_cext".  A Python-side shim at
 * kiwisolver/_cext.py re-exports everything via `from _kiwi_cext import *`,
 * making `from kiwisolver import Solver` work transparently.
 *
 * The kiwisolver static library (libkiwisolver.a) exports PyInit__cext.
 * This wrapper provides PyInit__kiwi_cext so the name matches the
 * entry in Modules/Setup.local.
 */

#include "Python.h"

extern PyObject* PyInit__cext(void);

PyMODINIT_FUNC
PyInit__kiwi_cext(void)
{
    return PyInit__cext();
}
