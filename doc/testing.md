# Testing

## Smoke Test

[`tests/smoke_test_l2.py`](../tests/smoke_test_l2.py) validates core
CPython built-in modules: `sys`, `os`, `json`, `collections`, `math`,
`io`, `zlib`, `bz2`, `hashlib`, `sqlite3`, `ctypes`, `pyexpat`, and
`xml.etree`.

## Functional Tests

108 individual test files in [`tests/func/`](../tests/func/) each
cover one package. Tests are numbered `test_001_packaging.py` through
`test_108_srsly.py` and run sequentially on `nanvixd.elf`.

### Running Tests

```bash
./z test
```

### Running a Subset

Use `TEST_START` and `TEST_END` to restrict the range:

```bash
# Run only numpy and kiwisolver tests
TEST_START=102 TEST_END=103 ./z test
```

### Per-test Timeout

Each test is capped at `TIMEOUT_SECONDS` (default: 300). Override it
for slow environments:

```bash
TIMEOUT_SECONDS=600 ./z test
```
