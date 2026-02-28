/*
 * srsly_ujson_builtin.c - Shim for srsly.ujson.ujson built-in.
 */

#include "Python.h"

extern PyObject* PyInit_ujson(void);

PyMODINIT_FUNC
PyInit__srsly_ujson(void)
{
    return PyInit_ujson();
}
