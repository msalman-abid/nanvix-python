# Building from Source

This guide covers building the Nanvix Python runtime from source, including cross-compiling
CPython 3.12 with statically linked C extensions.

## Prerequisites

| Requirement           | Notes                                                           |
| --------------------- | --------------------------------------------------------------- |
| **Linux x86-64 host** | Build scripts assume a Linux environment                        |
| **Nanvix toolchain**  | `nanvix/toolchain:latest-minimal` Docker image or `/opt/nanvix` |
| **Python 3.10+**      | Host Python for Cython, meson-python, and build orchestration   |
| **Docker** (optional) | Used automatically when a native toolchain is not available     |
| **KVM** (`/dev/kvm`)  | Required to run Nanvix guests during testing                    |
| **git**               | Submodule management                                            |

## Commands

All interaction is through the `./z` build script:

| Command       | Description                                                                                                                                                  |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `./z setup`   | Download the Nanvix runtime, initialise git submodules, install Cython/cppy, and fetch CPython build dependencies (sqlite, zlib, openssl, bzip2, libffi).    |
| `./z build`   | Cross-compile all C extension libraries, patch and build CPython 3.12 with statically linked built-in modules, and install Python packages into the sysroot. |
| `./z test`    | Install pip site-packages, run the smoke test (built-in modules), then run all 108 functional tests on `nanvixd.elf`.                                        |
| `./z release` | Package the sysroot into a standalone runtime tarball under `./release-assets/`.                                                                             |
| `./z clean`   | Remove all build artifacts, the sysroot, work directory, and release assets.                                                                                 |

## Build Walkthrough

```bash
# 1. Clone with submodules
git clone --recurse-submodules https://github.com/nanvix/nanvix-python.git
cd nanvix-python

# 2. Download the Nanvix runtime, init submodules, fetch build deps
./z setup

# 3. Cross-compile CPython with built-in C extensions
./z build

# 4. Install pip packages and run all tests
./z test

# 5. (Optional) Package a standalone runtime bundle
./z release
```

### Selecting a Platform

Set `NANVIX_PLATFORM` and `NANVIX_PROCESS_MODE` before running:

```bash
export NANVIX_PLATFORM=microvm
export NANVIX_PROCESS_MODE=single-process
./z setup && ./z build && ./z test
```

## Environment Variables

| Variable              | Default            | Description                                        |
| --------------------- | ------------------ | -------------------------------------------------- |
| `NANVIX_PLATFORM`     | `hyperlight`       | Target platform (`hyperlight` or `microvm`)        |
| `NANVIX_PROCESS_MODE` | `multi-process`    | Process mode (`multi-process` or `single-process`) |
| `NANVIX_TOOLCHAIN`    | `/opt/nanvix`      | Path to the Nanvix cross-compilation toolchain     |
| `RELEASE_DIR`         | `./release-assets` | Output directory for `./z release` artifacts       |
| `TEST_START`          | `1`                | First test number to run (inclusive)               |
| `TEST_END`            | `999`              | Last test number to run (inclusive)                |
| `TIMEOUT_SECONDS`     | `300`              | Per-test timeout in seconds                        |
| `GH_TOKEN`            | —                  | GitHub token for authenticated API calls (CI)      |

## Project Layout

```text
nanvix-python/
├── z                        # Build orchestration script (setup/build/test/release/clean)
├── deps/                    # Git submodules
│   ├── cpython/             # CPython 3.12.3 (Nanvix fork)
│   ├── numpy/               # NumPy 1.26.4
│   ├── cymem/               # cymem 2.0.11
│   ├── kiwi/                # kiwisolver 1.4.2
│   ├── libexpat/            # libexpat 2.6.4
│   ├── libffi/              # libffi 3.4.6
│   ├── murmurhash/          # murmurhash 1.0.13
│   ├── preshed/             # preshed 3.0.10
│   └── srsly/               # srsly 2.5.1
├── patches/                 # Static-builtin shims, C wrappers, and docs
├── requirements/            # Pip package lists (base + extra)
├── tests/
│   ├── smoke_test_l2.py     # Built-in module validation
│   └── func/                # 108 per-package functional tests
├── doc/                     # Documentation
├── scripts/                 # Helper scripts
└── release-assets/          # Output of ./z release
```
