---
description: SQLite3 wrapper with numpy array BLOB storage (compressed), blob storage, batch ops, git versioning, import/export, and maintenance.
---

# SQLite3

`scitex_db.SQLite3` — file-based SQLite with scientific extras. Composed from mixins:
`_ArrayMixin`, `_BlobMixin`, `_BatchMixin`, `_GitMixin`, `_ConnectionMixin`,
`_QueryMixin`, `_TransactionMixin`, `_ColumnMixin`, `_TableMixin`, `_IndexMixin`,
`_RowMixin`, `_ImportExportMixin`, `_MaintenanceMixin`.

**Context manager is required.** Using `SQLite3(...)` without a `with` block
raises at runtime.

## Basic Usage

```python
from scitex_db import SQLite3

with SQLite3("experiments.db", compress_by_default=True) as db:
    db.create_table(
        "results",
        {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "value": "REAL"},
    )
    db.insert_many("results", [
        {"name": "run_1", "value": 3.14},
        {"name": "run_2", "value": 2.71},
    ])
    rows = db.get_rows("results", where="value > 3.0")
    db.execute("UPDATE results SET value = 0 WHERE name = 'run_1'")
```

## Constructor

```python
SQLite3(
    db_path: str,
    use_temp: bool = False,             # work on a temp copy
    compress_by_default: bool = False,  # zlib BLOB compression
    autocommit: bool = False,
)
```

## Numpy Array Storage (`_ArrayMixin`)

Stores numpy arrays as BLOBs with auto-managed metadata columns
(`{column}_dtype`, `{column}_shape`, `{column}_compressed`). ~70–90% size
reduction with compression enabled.

```python
import numpy as np

with SQLite3("arrays.db", compress_by_default=True) as db:
    db.create_table(
        "measurements",
        {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "data": "BLOB"},
    )
    db.save_array(
        table_name="measurements",
        data=np.random.random((1000, 100)),
        column="data",
        additional_columns={"name": "experiment_1"},
    )
    loaded = db.load_array("measurements", column="data",
                           where="name = 'experiment_1'")
    # loaded.shape == (1000, 100)
```

Also available: `save_arrays`, `load_arrays`, `verify_array_hash`,
`get_array_dict`, `decode_array_columns`, `binary_to_array`.

## Generic Blob Storage (`_BlobMixin`)

```python
db.save_blob("models", data={"weights": arr, "cfg": {...}},
             column="checkpoint", additional_columns={"epoch": 10})
obj = db.load_blob("models", column="checkpoint", where="epoch = 10")
```

## Row / Table / Query Operations

```python
# Tables
db.create_table(name, schema_dict)
db.drop_table(name)
db.rename_table(old, new)
db.get_table_names()
db.get_table_schema(name)         # -> pd.DataFrame
db.get_primary_key(name)
db.get_table_stats(name)

# Columns
db.add_column(table, name, dtype)
db.drop_column(table, name)        # requires SQLite >= 3.35
db.rename_column(table, old, new)  # requires SQLite >= 3.25
db.get_column_info(table)
db.column_exists(table, column)
db.reorder_columns(...); db.sort_columns(...)

# Rows
db.insert_many(table, list_of_dicts)
db.update_many(...)
db.replace_many(...)
db.update_where(...); db.delete_where(...)
db.get_rows(table, where=None, order_by=None, limit=None)  # -> pd.DataFrame
db.get_row_count(table, where=None)

# Raw SQL
db.execute(sql, params=())
db.executemany(sql, params_list)
db.executescript(script)
```

## Transactions

```python
with db.transaction():
    db.insert_many("results", [...])
    db.insert_many("logs", [...])
# auto-commit on success, auto-rollback on exception

# Lower-level
db.begin(); db.commit(); db.rollback()
db.enable_foreign_keys(); db.disable_foreign_keys()
```

## Git Versioning (`_GitMixin`) — requires `scitex-db[git]`

Tracks the `.db` file (and sibling exports) with GitPython.

```python
db.git_init(force=False)
db.git_commit(message="snapshot", author="me")
db.git_log(limit=10)
db.git_status()
db.git_branch(...)
db.git_checkout(ref)
db.git_diff(...); db.git_reset(ref, mode="mixed")
```

## Import / Export

```python
db.load_from_csv(table_name, csv_path, ...)
db.save_to_csv(table_name, csv_path, ...)
```

## Indexes & Maintenance

```python
db.create_index(table, columns, unique=False)
db.drop_index(index_name)

db.vacuum(into=None)
db.optimize(analyze=True)
db.backup(...)
with db.maintenance_lock(): ...

db.fix_corruption(); db.fix_journal(); db.fix_indexes()
```

## Health and Duplicate Removal

```python
from scitex_db import check_health, batch_health_check, delete_sqlite3_duplicates

health = check_health("experiments.db", fix_issues=True)
all_health = batch_health_check(["db1.db", "db2.db"], fix_issues=False)

delete_sqlite3_duplicates("experiments.db", table_name="results",
                          columns=["name", "value"])
```

## Schema Inspection

```python
from scitex_db import inspect

info = inspect("experiments.db", table_names=None, sample_size=5, verbose=True)
# dict: table -> {columns, row_count, samples, ...}
```

## Database Summary

```python
with SQLite3("experiments.db") as db:
    db.summary                    # prints per-table summary
    s = db(return_summary=True, print_summary=False, limit=5)
```
