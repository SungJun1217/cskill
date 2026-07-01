---
name: run-plain-assert-tests-without-pytest
description: Run assert-based test_*.py files when pytest is not installed. Symptoms: "No module named pytest", `python3 -m pytest` fails, you need to verify a change but the env has no test runner and the tests are plain `def test_*(): assert ...` functions.
---

## Problem

You need to verify a change by running the tests, but `pytest` isn't installed
(`No module named pytest`). The test file is just plain functions with `assert`
statements — no fixtures, no `pytest.raises`, no markers — so it doesn't actually
need pytest to run.

## Solution

Invoke every `test_*` function in the module directly:

```bash
python3 -c "import test_ports as t; [getattr(t,n)() for n in dir(t) if n.startswith('test_')]; print('ok')"
```

Run it from the directory containing the test file (or add that dir to
`sys.path`). A silent `ok` means all asserts passed; a traceback names the first
failing test and line — the same failure signal pytest would give.

For a test that expects an exception, wrap the call rather than reaching for
`pytest.raises`:

```python
try:
    parse_ports("80,abc"); assert False, "expected ValueError"
except ValueError:
    pass
```

## Notes

- Only works when tests are dependency-free plain functions. If a test uses
  fixtures, parametrize, or `pytest.raises`, install pytest instead
  (`pip install pytest`) — don't try to hand-roll those.
- Prefer this over skipping verification: "no pytest" is not a reason to report a
  change as unverified when the tests are runnable this way.
