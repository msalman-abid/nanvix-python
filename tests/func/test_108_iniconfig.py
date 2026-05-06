"""Test: iniconfig"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    import textwrap
    import iniconfig
    src = textwrap.dedent("""\
        [section_a]
        key1 = value1
        key2 = value2

        [section_b]
        key3 = value3
        """)
    cfg = iniconfig.IniConfig("<in-memory>", data=src)
    assert "section_a" in cfg
    assert cfg["section_a"]["key1"] == "value1"
    assert cfg["section_a"]["key2"] == "value2"
    assert len(list(cfg)) == 2
    print("iniconfig: PASS")
except Exception as e:
    print(f"iniconfig: FAIL: {e}")
    sys.exit(1)
