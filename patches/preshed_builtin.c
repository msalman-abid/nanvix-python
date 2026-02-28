/*
 * preshed_builtin.c - Shim to register preshed modules as CPython built-ins.
 */

#include "Python.h"

extern PyObject* PyInit_maps(void);
extern PyObject* PyInit_counter(void);
extern PyObject* PyInit_bloom(void);

PyMODINIT_FUNC PyInit__preshed_maps(void) { return PyInit_maps(); }
PyMODINIT_FUNC PyInit__preshed_counter(void) { return PyInit_counter(); }
PyMODINIT_FUNC PyInit__preshed_bloom(void) { return PyInit_bloom(); }
