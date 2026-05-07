"""Test: markdownify"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    from markdownify import markdownify as md
    html = (
        "<h1>Title</h1>"
        "<p>See <a href=\"https://example.com\">example</a>.</p>"
        "<ul><li>one</li><li>two</li></ul>"
    )
    # markdownify uses BeautifulSoup under the hood.
    # This test validates the Markdown conversion result.
    out = md(html, heading_style="ATX")
    assert "# Title" in out, out
    assert "[example](https://example.com)" in out, out
    assert "* one" in out and "* two" in out, out
    print("markdownify: PASS")
except Exception as e:
    print(f"markdownify: FAIL: {e}")
    sys.exit(1)
