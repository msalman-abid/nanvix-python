"""Test: sniffio"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    import sniffio

    # Outside any async context: AsyncLibraryNotFoundError.
    try:
        sniffio.current_async_library()
    except sniffio.AsyncLibraryNotFoundError:
        pass
    else:
        raise AssertionError("expected AsyncLibraryNotFoundError outside async context")

    # Public contextvar override: detection round-trip without an event loop.
    token = sniffio.current_async_library_cvar.set("asyncio")
    try:
        assert sniffio.current_async_library() == "asyncio"
    finally:
        sniffio.current_async_library_cvar.reset(token)

    # After reset: back to AsyncLibraryNotFoundError.
    try:
        sniffio.current_async_library()
    except sniffio.AsyncLibraryNotFoundError:
        pass
    else:
        raise AssertionError("contextvar reset did not clear detection")

    print("sniffio: PASS")
except Exception as e:
    import traceback
    tb = traceback.format_exc().replace("\n", " | ")
    print(f"sniffio: FAIL: {tb}")
    sys.exit(1)
