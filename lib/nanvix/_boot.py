# Copyright(c) The Maintainers of Nanvix.
# Licensed under the MIT License.

"""Nanvix warm-start launcher for Python applications.

This module implements the guest-side warm-start protocol:

1. Take a VM snapshot (captures fully initialized Python + stdlib in RAMFS)
2. Mount the host directory at /mnt
3. Read the workload specification from /mnt
4. Execute the workload

On cold boot, step 1 saves the snapshot and execution continues.
On warm restore, execution resumes at step 2 — skipping kernel boot,
daemon initialization, and RAMFS loading entirely.

Usage (from nanvixd command line)::

    nanvixd -snapshot snapshots/kernel.whp.cbor -mount ./workdir -ramfs cpython.img \\
        -- ./bin/python3.12 "-S -B -m nanvix._boot;PYTHONHOME=/ ..."

The workload specification is a simple text file at /mnt/argv.txt containing
one argument per line. The first line is the Python script or module to run.

Alternatively, if /mnt/bootstrap.py exists, it is executed directly.
"""

import sys


def _do_warm_start():
    """Execute the warm-start protocol."""
    import nanvix

    # Pre-warm the UTF-8 codec so the first encode/decode after restore
    # does not trigger lazy codec registry initialization.
    "".encode("utf-8")
    b"".decode("utf-8")

    # Step 1: Take snapshot. On cold boot this saves state and continues.
    # On warm restore, execution resumes right after this call.
    # On platforms without snapshot support (e.g. Linux/KVM), this is
    # a no-op — execution simply continues to the mount step.
    try:
        nanvix.snapshot()
    except OSError:
        pass  # Snapshot not supported on this platform/configuration

    # Step 2: Mount host directory. The nanvixd -mount flag specifies
    # which host directory appears at /mnt.
    try:
        nanvix.mount("/mnt")
    except OSError:
        # No mount directory available (e.g. snapshot-creation mode).
        # Exit cleanly — the snapshot was already captured in step 1.
        sys.exit(0)

    # Step 3: Read workload specification from /mnt.
    # Note: Nanvix hostfs does not support stat(), so os.path.isfile()
    # always returns False. Use try/except open() instead.
    argv_file = "/mnt/argv.txt"
    bootstrap_script = "/mnt/bootstrap.py"

    code_text = None
    try:
        with open(bootstrap_script, "r") as f:
            code_text = f.read()
    except OSError:
        pass

    if code_text is not None:
        # Direct script execution mode.
        sys.argv = [bootstrap_script]
        # Read any extra args from argv.txt if it exists.
        try:
            with open(argv_file, "r") as f:
                extra_args = [line.strip() for line in f if line.strip()]
            sys.argv.extend(extra_args)
        except OSError:
            pass

        # Execute the script.
        exec(compile(code_text, bootstrap_script, "exec"), {"__name__": "__main__"})

    else:
        # Try argument-based execution mode.
        args = None
        try:
            with open(argv_file, "r") as f:
                args = [line.strip() for line in f if line.strip()]
        except OSError:
            pass

        if args:
            # Reconstruct sys.argv and run as module or script.
            if args[0] == "-m":
                # Module mode: python -m <module> [args...]
                sys.argv = args[1:]
                import runpy
                runpy.run_module(args[1], run_name="__main__", alter_sys=True)
            else:
                # Script mode: python <script> [args...]
                sys.argv = args
                script = args[0]
                with open(script, "r") as f:
                    script_code = f.read()
                exec(compile(script_code, script, "exec"), {"__name__": "__main__"})
        else:
            # No workload found — drop into interactive REPL.
            import code
            code.interact(exitmsg="")

    # Step 4: Unmount before exit.
    try:
        nanvix.umount("/mnt")
    except OSError:
        pass  # Best-effort unmount


if __name__ == "__main__":
    _do_warm_start()
