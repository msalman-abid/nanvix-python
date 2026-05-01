"""Pure-Python font metrics for NanVix.

Provides deterministic text metrics used by python-pptx layout code when
computing text box dimensions.  No actual font rendering.
"""

from __future__ import annotations


class FreeTypeFont:
    """Minimal font metrics stub."""

    def __init__(self, font=None, size=10, index=0, encoding="", layout_engine=None):
        self.size = size
        self.path = font

    def getlength(self, text, mode="", direction="", features=None, language=None):
        return len(text) * self.size * 0.6

    def getbbox(self, text, mode="", direction="", features=None, language=None, anchor=None):
        w = self.getlength(text)
        return (0, 0, int(w), int(self.size * 1.2))

    getsize = getbbox


def truetype(font=None, size=10, index=0, encoding="", layout_engine=None):
    return FreeTypeFont(font=font, size=size, index=index, encoding=encoding)


def load_default():
    return FreeTypeFont(size=10)
