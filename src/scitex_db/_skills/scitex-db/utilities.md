---
description: Inspect SQLite database structure (inspect), remove duplicate rows (delete_sqlite3_duplicates / delete_duplicates), and run health checks (check_health / batch_health_check).
---

# Database Utilities

All top-level helpers are SQLite3-oriented — PostgreSQL callers should use
the equivalent methods on the `PostgreSQL` class itself.

## inspect

Return a structured summary of a SQLite database (tables, columns,
row counts, sample rows).

```python
from scitex_db import inspect

info = inspect(
    lpath_db="experiment.db",
    table_names=None,        # or ["results", "logs"]
    sample_size=5,
    verbose=True,
)
# -> dict keyed by table name with columns / row counts / samples
```

Also exposed as `scitex-db inspect <path>` CLI.

---

## check_health

Run a health check on one SQLite3 file. Optionally attempts fixes.

```python
from scitex_db import check_health

report = check_health(
    db_path="experiment.db",
    verbose=True,
    fix_issues=False,
)
# -> dict with keys like 'integrity', 'rows_loadable', 'arrays_loadable',
#    'blobs_loadable', 'errors', ...
```

## batch_health_check

```python
from scitex_db import batch_health_check

reports = batch_health_check(
    db_paths=["a.db", "b.db"],
    verbose=False,
    fix_issues=False,
)
# -> dict[db_path] -> health dict
```

Also exposed as `scitex-db health <path1> [<path2> ...] [--fix]` CLI.

---

## delete_sqlite3_duplicates

Remove duplicate rows from a SQLite3 table (keeps one copy per
(column-subset) key).

```python
from scitex_db import delete_sqlite3_duplicates

delete_sqlite3_duplicates(
    lpath_db="experiment.db",
    table_name="results",
    columns="all",            # or list[str] subset
)
```

## delete_duplicates

Deprecated alias that forwards to `delete_sqlite3_duplicates` — prefer
the explicit name in new code.

```python
from scitex_db import delete_duplicates

delete_duplicates("experiment.db", "results", columns=["name", "value"])
```
