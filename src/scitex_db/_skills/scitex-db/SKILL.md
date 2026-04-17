---
name: scitex-db
description: Database utilities for scientific computing. Provides SQLite3 (with numpy BLOB storage, compression, optional git versioning) and PostgreSQL wrappers sharing a mixin-based API, plus health checks, duplicate removal, and schema inspection.
---

# scitex-db

Database utilities for scientific computing with SQLite3 and PostgreSQL. Both
backends share a mixin architecture, so most row/table/query/transaction
methods have the same names on each class.

## Sub-skills

- [sqlite3-usage.md](sqlite3-usage.md) — `SQLite3` class, numpy array/BLOB storage, compression, git versioning, mixin capabilities
- [postgresql-usage.md](postgresql-usage.md) — `PostgreSQL` class, connection, schema/backup, differences from SQLite3
- [utilities.md](utilities.md) — `inspect`, `check_health`, `batch_health_check`, `delete_duplicates`, `delete_sqlite3_duplicates`

## Python API (top-level exports)

```python
from scitex_db import (
    SQLite3,
    PostgreSQL,
    inspect,
    check_health,
    batch_health_check,
    delete_duplicates,
    delete_sqlite3_duplicates,
)
```

The canonical module path is `scitex_db`. If you have `scitex` (the umbrella
package) installed it re-exports this module under `scitex.db`.

## Quick Reference

```python
from scitex_db import SQLite3, PostgreSQL, check_health, inspect
import numpy as np

# SQLite3 — MUST be used with a context manager
with SQLite3("experiments.db", compress_by_default=True) as db:
    db.create_table(
        "results",
        {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "value": "REAL", "data": "BLOB"},
    )
    db.insert_many("results", [{"name": "a", "value": 3.14}, {"name": "b", "value": 2.71}])
    rows = db.get_rows("results", where="value > 3.0")

    # Numpy array storage (SQLite3 only) — compressed BLOB with shape/dtype metadata
    db.save_array("results", np.random.rand(1000, 50),
                  column="data", additional_columns={"name": "embeddings"})
    arr = db.load_array("results", column="data", where="name = 'embeddings'")

# PostgreSQL
with PostgreSQL(host="localhost", dbname="mydb", user="u", password="p") as db:
    db.insert("results", {"name": "run_42", "value": 0.95})
    rows = db.select("results", where="value > 0.9")

# Utilities
schema = inspect("experiments.db")                     # dict of tables/columns/stats
health = check_health("experiments.db", fix_issues=True)
```

## CLI

The `scitex-db` command (from `python -m scitex_db`) exposes two subcommands:

```bash
scitex-db inspect database.db [--tables t1 t2] [--quiet]
scitex-db health db1.db db2.db [--fix] [--quiet]
```

## Exports

| Name | Description |
|------|-------------|
| `SQLite3` | SQLite3 wrapper with compression, numpy array storage, git versioning, context-manager required |
| `PostgreSQL` | PostgreSQL wrapper with connection, schema, batch, blob, backup operations |
| `check_health` | Health check for a single SQLite3 database; can attempt repairs |
| `batch_health_check` | Health check across a list of SQLite3 databases |
| `delete_duplicates` | Deprecated alias — delegates to `delete_sqlite3_duplicates` |
| `delete_sqlite3_duplicates` | Remove duplicate rows by column subset from a SQLite3 table |
| `inspect` | Dict-structured summary of a SQLite3 database (tables, columns, stats, samples) |

## Installation

```bash
pip install scitex-db                 # SQLite3 + core
pip install scitex-db[postgresql]     # + psycopg2-binary, sqlalchemy
pip install scitex-db[git]            # + GitPython (git versioning)
pip install scitex-db[all]            # everything above
```

Python >= 3.10, license AGPL-3.0.
