"""Test: httpx"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    import httpx

    assert hasattr(httpx, "__version__")

    # Sync GET round-trip via MockTransport. No sockets, no asyncio
    # (asyncio is nonfunctional on Nanvix; see closure umbrella).
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert str(request.url) == "http://example.com/"
        return httpx.Response(
            200,
            headers={"Content-Type": "text/plain"},
            text="Hello, world!",
        )

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport) as client:
        response = client.get("http://example.com/")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain"
        assert response.text == "Hello, world!"

    print("httpx: PASS")
except Exception as e:
    print(f"httpx: FAIL: {e}")
    sys.exit(1)
