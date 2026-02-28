"""Test: libexpat (via xml.parsers.expat)"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    import xml.parsers.expat

    elements = []
    def start_element(name, attrs):
        elements.append(name)

    parser = xml.parsers.expat.ParserCreate()
    parser.StartElementHandler = start_element
    parser.Parse('<root><child attr="1"/><child attr="2"/></root>', True)

    assert elements == ['root', 'child', 'child'], f"unexpected elements: {elements}"
    print("libexpat: PASS")
except Exception as e:
    print(f"libexpat: FAIL: {e}")
    sys.exit(1)
