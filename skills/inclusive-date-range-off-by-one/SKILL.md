---
name: inclusive-date-range-off-by-one
description: Fix off-by-one when a date window should include the boundary day. Symptoms: test fails because a task/event due exactly N days out is excluded; filter uses `< cutoff` where cutoff = today + N.
---

## Problem

A date range filter is meant to be inclusive of the last day (e.g. "due within 7 days" should include items due exactly 7 days from now), but items on the boundary date are excluded.

## Solution

When `cutoff = today + N` and the filter is `today <= due < cutoff`, change the comparison to `<=`:

```python
# Before (excludes boundary — off by one)
cutoff = date.fromordinal(today.toordinal() + days)
return [t for t in tasks if today <= t.due < cutoff]

# After (includes boundary)
return [t for t in tasks if today <= t.due <= cutoff]
```

Alternatively, keep `<` and bump the cutoff by one:

```python
cutoff = date.fromordinal(today.toordinal() + days + 1)
return [t for t in tasks if today <= t.due < cutoff]
```

## Notes

- The `<` form is idiomatic for half-open ranges and pairs naturally with `timedelta` arithmetic; prefer it when the inclusive form would surprise readers.
- Only one of these two fixes is needed — applying both double-counts the extra day.
