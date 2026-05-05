"""Minimal ImageOps for python-pptx compatibility."""

from __future__ import annotations


def exif_transpose(image):
    """No-op — NanVix PIL shim does not handle EXIF rotation."""
    return image
