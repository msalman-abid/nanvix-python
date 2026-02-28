# srsly/ujson/ujson.py - Bridge to the _srsly_ujson built-in.
import sys
import _srsly_ujson

sys.modules[__name__] = _srsly_ujson
sys.modules['srsly.ujson.ujson'] = _srsly_ujson

from _srsly_ujson import *  # noqa: F401,F403
