"""Test: srsly (ujson)"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    import _srsly_ujson as ujson

    data = {"foo": "bar", "baz": 123, "nested": [1, 2, 3]}
    json_str = ujson.dumps(data)
    assert isinstance(json_str, str), f"expected str, got {type(json_str)}"
    restored = ujson.loads(json_str)
    assert restored == data, f"JSON roundtrip failed: {restored}"

    assert ujson.dumps(None) == "null"
    assert ujson.dumps(True) == "true"
    assert ujson.loads("42") == 42

    print("srsly: PASS")
except Exception as e:
    print(f"srsly: FAIL: {e}")
    sys.exit(1)
