"""Test: docx2txt"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    import io
    import zipfile
    import docx2txt

    # Build a minimal in-memory .docx (a ZIP container with an OOXML
    # word/document.xml part). Avoids shipping a binary fixture.
    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w='
        '"http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:body>'
        '<w:p><w:r><w:t>hello</w:t></w:r></w:p>'
        '<w:p><w:r><w:t>world</w:t><w:tab/><w:t>again</w:t></w:r></w:p>'
        '</w:body>'
        '</w:document>'
    )
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("word/document.xml", document_xml)
    buf.seek(0)

    text = docx2txt.process(buf)
    assert "hello" in text, text
    assert "world" in text, text
    assert "again" in text, text
    assert "\t" in text, repr(text)
    print("docx2txt: PASS")
except Exception as e:
    print(f"docx2txt: FAIL: {e}")
    sys.exit(1)
