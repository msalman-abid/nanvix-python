"""Test: srt"""
import sys
sys.stdout.reconfigure(line_buffering=True)
try:
    import srt
    import textwrap
    from datetime import timedelta
    sample = textwrap.dedent("""\
        1
        00:00:01,000 --> 00:00:02,000
        hello

        2
        00:00:03,000 --> 00:00:04,500
        world
        """)
    subs = list(srt.parse(sample))
    assert len(subs) == 2
    assert subs[0].content == "hello"
    assert subs[1].index == 2
    # timecode parsing (datetime/timedelta path)
    assert subs[0].start == timedelta(seconds=1)
    assert subs[0].end == timedelta(seconds=2)
    assert subs[1].end - subs[1].start == timedelta(milliseconds=1500)
    # round-trip
    assert list(srt.parse(srt.compose(subs))) == subs
    print("srt: PASS")
except Exception as e:
    print(f"srt: FAIL: {e}")
    sys.exit(1)
