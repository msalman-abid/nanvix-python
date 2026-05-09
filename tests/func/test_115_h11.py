"""Test: h11"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    import h11

    # In-memory HTTP/1.1 round-trip via the sans-I/O state machine.
    client = h11.Connection(our_role=h11.CLIENT)
    server = h11.Connection(our_role=h11.SERVER)

    # Client sends a request + end-of-message.
    req = h11.Request(
        method="GET",
        target="/hello",
        headers=[("Host", "example.com"), ("Connection", "close")],
    )
    data = client.send(req) + client.send(h11.EndOfMessage())
    assert data.startswith(b"GET /hello HTTP/1.1\r\n")

    # Server parses the request.
    server.receive_data(data)
    parsed_req = server.next_event()
    assert isinstance(parsed_req, h11.Request)
    assert parsed_req.method == b"GET"
    assert parsed_req.target == b"/hello"
    assert isinstance(server.next_event(), h11.EndOfMessage)

    # Server sends a response with a small body.
    body = b"hi"
    resp = h11.Response(
        status_code=200,
        headers=[("Content-Length", str(len(body))), ("Connection", "close")],
    )
    out = server.send(resp) + server.send(h11.Data(data=body)) + server.send(h11.EndOfMessage())
    assert b"HTTP/1.1 200" in out

    # Client parses the response.
    client.receive_data(out)
    parsed_resp = client.next_event()
    assert isinstance(parsed_resp, h11.Response)
    assert parsed_resp.status_code == 200
    parsed_data = client.next_event()
    assert isinstance(parsed_data, h11.Data)
    assert parsed_data.data == body
    assert isinstance(client.next_event(), h11.EndOfMessage)

    print("h11: PASS")
except Exception as e:
    print(f"h11: FAIL: {e}")
    sys.exit(1)
