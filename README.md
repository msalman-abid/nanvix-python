# Nanvix Python

Functional tests for [Nanvix CPython](https://github.com/nanvix/cpython) — validates pip-installed Python packages on the Nanvix platform.

## Overview

This repository runs comprehensive functional tests against CPython builds released by [`nanvix/cpython`](https://github.com/nanvix/cpython). It is automatically triggered when a new CPython release is published, and tests 99 pip-installed packages plus a smoke test of built-in modules.

## How It Works

1. **`nanvix/cpython`** builds CPython, creates a release, and sends a `cpython-release` repository dispatch event.
2. **This repository** receives the event, downloads the Nanvix runtime and CPython release artifacts, installs pip packages, and runs all tests on `nanvixd.elf`.

## Tests

- **Smoke test** (`tests/smoke_test_l2.py`): Validates built-in CPython modules (sys, os, json, zlib, bz2, hashlib, sqlite3, ctypes, pyexpat, xml.etree).
- **Functional tests** (`tests/func/test_*.py`): 99 tests covering pip-installed packages (packaging, attrs, requests, flask, jinja2, etc.).

## Usage

```bash
# Setup: download Nanvix runtime and CPython release artifacts
export NANVIX_PLATFORM=hyperlight    # or microvm
export NANVIX_PROCESS_MODE=multi-process  # or single-process
./z setup

# Run tests
./z test
```

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `NANVIX_PLATFORM` | `hyperlight` | Target platform |
| `NANVIX_PROCESS_MODE` | `multi-process` | Process mode |
| `NANVIX_TOOLCHAIN` | `/opt/nanvix` | Toolchain root |
| `CPYTHON_TAG` | *(latest)* | CPython release tag to test |
| `TEST_START` | `1` | First test number to run |
| `TEST_END` | `999` | Last test number to run |
| `TIMEOUT_SECONDS` | `300` | Per-test timeout |

## License

MIT
