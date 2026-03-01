# Nanvix Python

[![CI](https://github.com/nanvix/nanvix-python/actions/workflows/ci.yml/badge.svg)](https://github.com/nanvix/nanvix-python/actions/workflows/ci.yml)

CPython 3.12 distribution for the
[Nanvix](https://github.com/nanvix/nanvix) microkernel — a
self-contained Python runtime with 108 pip packages and 8 statically
linked C extensions.

## Getting Started

Download and run the installer script to fetch the latest
standalone runtime bundle:

```bash
curl -fsSL -o get-nanvix-python.sh https://raw.githubusercontent.com/nanvix/nanvix-python/main/scripts/get-nanvix-python.sh
bash get-nanvix-python.sh nanvix-python
```

Then extract and run Python:

```bash
cd nanvix-python
tar -xjf hyperlight-multi-process.tar.bz2
cd hyperlight-multi-process
echo 'print("Hello from Nanvix!")' > hello.py
./bin/nanvixd.elf -- ./bin/python3.12 hello.py
```

Alternatively, download a bundle manually from
[Releases](https://github.com/nanvix/nanvix-python/releases).

### Running Scripts

```bash
./bin/nanvixd.elf -- ./bin/python3.12 your_script.py
```

### Using Built-in Packages

All 108 packages and 8 C extensions are pre-installed. No `pip install`
is needed:

```bash
echo 'import numpy; print(numpy.__version__)' > test.py
./bin/nanvixd.elf -- ./bin/python3.12 test.py
```

> **Note:** The `-c` flag only works with code that contains no spaces
> (a nanvixd argument-splitting limitation). Use script files instead.

## Supported Platforms

| Platform     | Process Mode     |
| ------------ | ---------------- |
| `hyperlight` | `multi-process`  |
| `hyperlight` | `single-process` |
| `microvm`    | `multi-process`  |
| `microvm`    | `single-process` |

Each combination is tested in CI and published as a separate release
artifact.

## What's Included

- **CPython 3.12.3** — fully functional interpreter
- **8 statically linked C extensions** — NumPy 1.26.4, kiwisolver,
  cymem, murmurhash, preshed, srsly, libexpat, libffi
- **108 pip packages** — attrs, requests, flask, jinja2, numpy,
  beautifulsoup4, rich, click, and many more

## Documentation

| Document                                            | Description                                        |
| --------------------------------------------------- | -------------------------------------------------- |
| [Building from Source](doc/building.md)             | Prerequisites, commands, and environment variables |
| [Statically Linked C Extensions](doc/extensions.md) | Cross-compiled libraries and patch details         |
| [Supported Packages](doc/packages.md)               | Full list of 108 pip packages with versions        |
| [Testing](doc/testing.md)                           | Smoke test and 108 functional tests                |
| [Standalone Runtime Bundle](doc/release.md)         | Creating and using release bundles                 |
| [CI / CD](doc/ci.md)                                | GitHub Actions pipeline and platform matrix        |
| [Contributing](doc/contributing.md)                 | How to add packages, extensions, or fixes          |

## Usage Statement

This project is a prototype. As such, we provide no guarantees that it
will work and you are assuming any risks with using the code. We welcome
comments and feedback. Please send any questions or comments to any of
the following maintainers of the project:

- [Pedro Henrique Penna](https://github.com/ppenna) -
  [ppenna@microsoft.com](mailto:ppenna@microsoft.com)

> By sending feedback, you are consenting that it may be used
> in the further development of this project.

## License

This project is distributed under the [MIT License](LICENSE.txt).
