---
name: shell-injection-via-string-interpolation
description: Fix/spot shell (command) injection when untrusted input is interpolated into a shell string. Symptoms: os.system / subprocess(shell=True) / backticks built with %-format, f-string, or + concatenation of a filename, username, or any user-supplied value; crafted input like "x; rm -rf /" runs arbitrary commands.
---

## Problem

A command is built by interpolating untrusted input into a string that a shell
then parses — `os.system("tar czf %s.tgz %s" % (name, name))`,
`subprocess.run(f"...{arg}", shell=True)`, backticks, etc. Any shell metacharacter
in the input (`;`, `|`, `&&`, `$()`, backticks, spaces) breaks out of the intended
command. Working correctly for a normal name is not a defense.

Trigger input: `name = "x; rm -rf ~"` → the shell runs `tar ...` **and** `rm -rf ~`.

## Solution

Don't build a shell string. Pass an argument vector and let no shell interpret it:

```python
import subprocess
# Before (injectable):
os.system("tar czf backups/%s.tar.gz %s" % (name, name))
# After (no shell, args are literal):
subprocess.run(["tar", "czf", f"backups/{name}.tar.gz", name], check=True)
```

- `subprocess.run([...])` **without** `shell=True` passes args directly to execve —
  metacharacters are literal, not parsed.
- If you truly need a shell, quote every interpolated value with `shlex.quote(name)`.
- Same rule in other langs: parameterized APIs over string-built commands (and the
  identical pattern applies to SQL — use bound parameters, never string concat).

## Notes

- Also validate the value against an allowlist (e.g. filename charset) — quoting
  stops injection but not path traversal (`../../etc/...`); check both.
- `subprocess.run(..., shell=True)` with an interpolated string is the same bug as
  `os.system` — the fix is dropping `shell=True`, not switching functions.
