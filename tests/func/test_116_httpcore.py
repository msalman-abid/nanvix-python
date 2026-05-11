"""Test: httpcore"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    import httpcore

    assert hasattr(httpcore, "__version__")

    # Sync HTTP/1.1 round-trip over an in-memory MockStream. No sockets,
    # no asyncio (asyncio is nonfunctional on Nanvix; see closure umbrella).
    from httpcore import MockStream
    from httpcore._sync.http11 import HTTP11Connection
    from httpcore._models import Origin, Request

    raw_response = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/plain\r\n"
        b"Content-Length: 13\r\n"
        b"\r\n"
        b"Hello, world!"
    )
    stream = MockStream([raw_response])
    origin = Origin(scheme=b"http", host=b"example.com", port=80)
    conn = HTTP11Connection(origin=origin, stream=stream)

    request = Request(
        method=b"GET",
        url=b"http://example.com/",
        headers=[(b"Host", b"example.com")],
    )
    response = conn.handle_request(request)
    assert response.status == 200
    body = response.read()
    assert body == b"Hello, world!"
    response.close()

    print("httpcore: PASS")
except Exception as e:
    print(f"httpcore: FAIL: {e}")
    sys.exit(1)
