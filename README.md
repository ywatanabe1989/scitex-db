# scitex-db

Database utilities for scientific computing with SQLite3 and PostgreSQL.

Part of the [SciTeX ecosystem](https://github.com/ywatanabe1989).

## Overview

`scitex-db` provides two database wrappers that share a mixin-based API, so
most `create_table`, `insert_many`, `get_rows`, and transaction calls look the
same on both backends. On top of that it adds a few scientific niceties:

- **Numpy array storage (SQLite3)** — save/load `ndarray`s as BLOBs with
  automatic `dtype` / `shape` metadata and optional zlib compression.
- **Generic blob storage** — pickle-backed object store with metadata columns.
- **Git versioning (SQLite3, optional)** — commit the `.db` file on change
  via GitPython.
- **Health checks & duplicate removal** — standalone helpers for SQLite3.
- **Schema inspection** — one call returns a structural summary of a DB.
- **CLI** — `scitex-db inspect` / `scitex-db health`.

## Installation

```bash
pip install scitex-db                   # SQLite3 + core
pip install scitex-db[postgresql]       # + psycopg2-binary, sqlalchemy
pip install scitex-db[git]              # + GitPython (git versioning)
pip install scitex-db[all]              # everything above
```

Python >= 3.10.

## Quick Start

### SQLite3 (context manager required)

```python
from scitex_db import SQLite3

with SQLite3("experiments.db", compress_by_default=True) as db:
    db.create_table(
        "results",
        {"id": "INTEGER PRIMARY KEY", "experiment": "TEXT", "accuracy": "REAL"},
    )
    db.insert_many("results", [
        {"experiment": "exp1", "accuracy": 0.95},
        {"experiment": "exp2", "accuracy": 0.92},
    ])
    rows = db.get_rows("results", where="accuracy > 0.9")
    print(rows)
```

### Numpy array storage

```python
import numpy as np
from scitex_db import SQLite3

with SQLite3("features.db", compress_by_default=True) as db:
    db.create_table(
        "features",
        {"id": "INTEGER PRIMARY KEY", "model": "TEXT", "embeddings": "BLOB"},
    )
    db.save_array(
        table_name="features",
        data=np.random.rand(1000, 50),
        column="embeddings",
        additional_columns={"model": "bert"},
    )
    arr = db.load_array("features", column="embeddings",
                        where="model = 'bert'")
```

### Blob storage

```python
with SQLite3("models.db") as db:
    db.create_table("models",
                    {"id": "INTEGER PRIMARY KEY", "epoch": "INTEGER", "checkpoint": "BLOB"})
    db.save_blob("models", data={"weights": arr, "config": {...}},
                 column="checkpoint", additional_columns={"epoch": 10})
    obj = db.load_blob("models", column="checkpoint", where="epoch = 10")
```

### Git integration (optional)

Requires `pip install scitex-db[git]`.

```python
with SQLite3("versioned.db") as db:
    db.git_init()
    db.insert_many("results", [{"value": 42}])
    db.git_commit(message="Snapshot after run")
    db.git_log(limit=5)
```

### Transactions & batch operations

```python
with SQLite3("data.db") as db:
    with db.transaction():
        db.insert_many("a", [...])
        db.insert_many("b", [...])  # auto-rollback on exception

    db.insert_many("data", [{"id": i, "value": i**2} for i in range(10_000)])
```

### Inspection & health

```python
from scitex_db import inspect, check_health, batch_health_check

info = inspect("experiments.db")                         # dict summary
report = check_health("experiments.db", fix_issues=True) # single DB
all_reports = batch_health_check(["a.db", "b.db"])       # many
```

### PostgreSQL

```python
from scitex_db import PostgreSQL

db = PostgreSQL(dbname="mydb", user="u", password="p",
                host="localhost", port=5432)
db.connect()
db.insert("experiments", {"name": "run_42", "status": "running"})
rows = db.select("experiments", where="status = 'running'", limit=100)
db.close()
```

## CLI

```bash
scitex-db inspect database.db [--tables t1 t2] [--quiet]
scitex-db health db1.db [db2.db ...] [--fix] [--quiet]
```

## Public API

```python
from scitex_db import (
    SQLite3,
    PostgreSQL,
    inspect,
    check_health,
    batch_health_check,
    delete_duplicates,            # deprecated alias
    delete_sqlite3_duplicates,
)
```

## Part of SciTeX Ecosystem

- `scitex-core` — core infrastructure
- `scitex-io` — data I/O (30+ formats)
- `scitex-db` — this package
- `scitex` — umbrella package that re-exports `scitex_db` as `scitex.db`

## License

AGPL-3.0 — see [LICENSE](LICENSE).
