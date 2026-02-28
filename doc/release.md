# Standalone Runtime Bundle

## Downloading a Pre-built Bundle

Download and run the installer script:

```bash
curl -fsSL -o get-nanvix-python.sh https://raw.githubusercontent.com/nanvix/nanvix-python/main/scripts/get-nanvix-python.sh
bash get-nanvix-python.sh nanvix-python
```

Use `--force` to re-download existing files:

```bash
bash get-nanvix-python.sh --force /tmp/nanvix-python
```

The script accepts the same environment variables as `get-nanvix.sh`:

| Variable                    | Default | Description                                                      |
| --------------------------- | ------- | ---------------------------------------------------------------- |
| `GITHUB_TOKEN` / `GH_TOKEN` | —       | GitHub token for authenticated API requests (avoids rate limits) |
| `NANVIX_CONNECT_TIMEOUT`    | `30`    | Connection timeout in seconds                                    |
| `NANVIX_MAX_TIMEOUT`        | `300`   | Maximum total timeout in seconds                                 |
| `NANVIX_FORCE_DOWNLOAD`     | `false` | Force re-download if `true`                                      |

You can also download bundles manually from
[Releases](https://github.com/nanvix/nanvix-python/releases).

## Building a Bundle from Source

After a successful build and test, package a self-contained tarball
that can run Python scripts on any Linux host with KVM support.

```bash
./z release
```

This writes artifacts to `./release-assets/` (override with
`RELEASE_DIR`).

## Bundle Contents

```text
<platform>-<mode>/
  bin/              # nanvixd.elf, kernel.elf, linuxd.elf, uservm.elf, python3.12
  lib/              # Python standard library, site-packages, user.ld
  README.md         # Usage instructions
```

Only runtime-essential files are included — no static libraries,
headers, or build tools. All `.pyc` bytecode caches are pre-compiled
to avoid runtime file-creation issues
([nanvix/nanvix#1493](https://github.com/nanvix/nanvix/issues/1493)).

## Running from a Bundle

```bash
tar -xjf release-assets/hyperlight-multi-process.tar.bz2
cd hyperlight-multi-process

# Run a script
echo 'import numpy; print(numpy.__version__)' > test.py
./bin/nanvixd.elf -- ./bin/python3.12 test.py
```

> **Note:** The `-c` flag only works with code that contains no spaces
> (a nanvixd argument-splitting limitation). Use script files instead.
