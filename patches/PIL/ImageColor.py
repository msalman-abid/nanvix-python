"""Minimal color name/hex parser for python-pptx."""

from __future__ import annotations

_NAMED_COLORS = {
    "red": (255, 0, 0), "green": (0, 128, 0), "blue": (0, 0, 255),
    "white": (255, 255, 255), "black": (0, 0, 0), "yellow": (255, 255, 0),
    "cyan": (0, 255, 255), "magenta": (255, 0, 255), "gray": (128, 128, 128),
    "grey": (128, 128, 128), "orange": (255, 165, 0), "purple": (128, 0, 128),
    "pink": (255, 192, 203), "brown": (165, 42, 42), "lime": (0, 255, 0),
}


def getrgb(color: str) -> tuple[int, ...]:
    low = color.strip().lower()
    if low in _NAMED_COLORS:
        return _NAMED_COLORS[low]
    if low.startswith("#"):
        h = low[1:]
        if len(h) == 3:
            return tuple(int(c * 2, 16) for c in h)
        if len(h) == 6:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
        if len(h) == 8:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16))
    raise ValueError(f"Unknown color: {color!r}")
