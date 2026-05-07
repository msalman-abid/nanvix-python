"""Test: svgwrite"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    import svgwrite
    import xml.etree.ElementTree as ET
    dwg = svgwrite.Drawing("smoke.svg", size=(100, 100))
    dwg.add(dwg.circle(center=(50, 50), r=40, fill="red"))
    dwg.add(dwg.path(d="M10 10 L90 90", stroke="black"))
    xml = dwg.tostring()
    root = ET.fromstring(xml)
    assert root.tag.endswith("svg"), root.tag
    tags = [child.tag for child in root]
    assert any(t.endswith("circle") for t in tags), tags
    assert any(t.endswith("path") for t in tags), tags
    print("svgwrite: PASS")
except Exception as e:
    print(f"svgwrite: FAIL: {e}")
    sys.exit(1)
