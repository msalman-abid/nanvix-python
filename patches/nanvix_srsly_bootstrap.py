"""
Import registration for srsly ujson built-in module on Nanvix.

The ujson C extension is statically linked as _srsly_ujson. This bootstrap
registers it under its expected dotted name so srsly's import chain works.
"""
import importlib
import sys


def _register_srsly_builtins():
    """Pre-register srsly ujson built-in under its dotted name."""
    try:
        mod = importlib.import_module("_srsly_ujson")
        mod.__name__ = "srsly.ujson.ujson"
        mod.__package__ = "srsly.ujson"
        sys.modules["srsly.ujson.ujson"] = mod
    except ImportError:
        pass


_register_srsly_builtins()
