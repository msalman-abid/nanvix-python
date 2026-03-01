# CI / CD

The GitHub Actions workflow
([`.github/workflows/ci.yml`](../.github/workflows/ci.yml)) runs on
every push, pull request, and `cpython-release` repository dispatch
event.

## Pipeline Stages

1. **Setup** — downloads the Nanvix runtime, initialises submodules,
   installs build dependencies.
2. **Build** — cross-compiles all C extensions and CPython.
3. **Test** — runs the smoke test and all 108 functional tests.
4. **Release** — packages standalone runtime bundles and publishes a
   GitHub release.

## Platform Matrix

The CI matrix tests every combination of platform and process mode:

| Platform     | Process Mode     | Status       |
| ------------ | ---------------- | ------------ |
| `hyperlight` | `multi-process`  | Tested in CI |
| `hyperlight` | `single-process` | Tested in CI |
| `microvm`    | `multi-process`  | Tested in CI |
| `microvm`    | `single-process` | Tested in CI |

## Failure Handling

On failure, debug logs are uploaded as workflow artifacts and a GitHub
issue is automatically created and assigned to the maintainers.
