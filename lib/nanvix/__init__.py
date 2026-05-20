# Copyright(c) The Maintainers of Nanvix.
# Licensed under the MIT License.

"""Nanvix OS interface for Python applications.

This package provides Python-level access to Nanvix VM features:

- **Snapshotting**: Capture VM state for instant warm-start restores.
- **Host mounting**: Mount host directories for live file access.

Quick Start
-----------

Warm-start pattern (snapshot + host mount)::

    import nanvix

    # Take a snapshot checkpoint. On first boot this saves state;
    # on subsequent restores, execution resumes here instantly.
    nanvix.snapshot()

    # Mount host directory (provided via nanvixd -mount <dir>)
    nanvix.mount()

    # Now /mnt contains the host directory contents.
    with open('/mnt/input.txt') as f:
        data = f.read()

    # Clean up before exit
    nanvix.umount()

Functions
---------
"""

import _nanvix

__all__ = ["snapshot", "mount", "umount", "is_nanvix"]


def is_nanvix() -> bool:
    """Return True if running on the Nanvix operating system."""
    import sys
    return sys.platform == "nanvix"


def snapshot() -> None:
    """Take a VM snapshot checkpoint.

    After this call returns, the VM state (memory, CPU, RAMFS) has been
    saved to disk. On subsequent boots with the same snapshot files,
    execution resumes immediately after this point — skipping kernel boot,
    daemon initialization, and RAMFS loading.

    This is the key primitive for warm-start patterns: expensive
    initialization only happens once (cold boot); all subsequent runs
    restore instantly.

    Raises
    ------
    OSError
        If the snapshot fails. Common causes:
        - Kernel not booted with 'snapshot' argument
        - Snapshot already taken during this boot (one-shot limit)
        - snapshots/ directory does not exist
    """
    _nanvix.snapshot()


def mount(target: str = "/mnt", source: str = "", fstype: str = "hostfs",
          flags: int = 0) -> None:
    """Mount a filesystem in the guest.

    By default, mounts the host directory (specified via ``nanvixd -mount``)
    at ``/mnt`` inside the guest using the hostfs filesystem type.

    Parameters
    ----------
    target : str
        Mount point inside the guest (default: '/mnt').
    source : str
        Source device or empty string for hostfs (default: '').
    fstype : str
        Filesystem type (default: 'hostfs').
    flags : int
        Mount flags, currently unused (default: 0).

    Raises
    ------
    OSError
        If the mount fails. Common causes:
        - nanvixd was not started with -mount flag
        - Target is already mounted (ResourceBusy)
    """
    _nanvix.mount(source, target, fstype, flags)


def umount(target: str = "/mnt") -> None:
    """Unmount a previously mounted filesystem.

    Parameters
    ----------
    target : str
        Mount point to unmount (default: '/mnt').

    Raises
    ------
    OSError
        If unmount fails (e.g. target was not mounted).
    """
    _nanvix.umount(target)
