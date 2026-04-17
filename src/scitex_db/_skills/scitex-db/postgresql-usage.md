---
description: PostgreSQL wrapper sharing a mixin architecture with SQLite3. Adds schema, backup/restore, batch insert, array/blob storage, and index management. Requires scitex-db[postgresql].
---

# PostgreSQL

`scitex_db.PostgreSQL` — PostgreSQL client. Composed from mixins:
`_BackupMixin`, `_BatchMixin`, `_ConnectionMixin`, `_ImportExportMixin`,
`_IndexMixin`, `_MaintenanceMixin`, `_QueryMixin`, `_RowMixin`, `_SchemaMixin`,
`_TableMixin`, `_TransactionMixin`, `_BlobMixin`.

Install the extras:

```bash
pip install scitex-db[postgresql]
```

## Connection

```python
from scitex_db import PostgreSQL

db = PostgreSQL(
    dbname="mydb",
    user="researcher",
    password="secret",
    host="localhost",
    port=5432,
)
db.connect()
db.close()

# Context-manager form works for cleanup where supported
with PostgreSQL(dbname="mydb", user="u", password="p") as db:
    rows = db.select("results", where="status = 'pending'")
```

## Core Operations

```python
# Raw SQL
db.execute("SELECT COUNT(*) FROM experiments")
db.executemany(sql, params_list)

# High-level rows
db.insert("experiments", {"name": "run_42", "status": "running"})
db.update("experiments", {"status": "done"}, where="name = 'run_42'")
db.delete("experiments", where="status = 'failed'")
rows = db.select("experiments", where="status = 'done'", limit=100)
db.count("experiments", where="status = 'done'")
db.execute_query(sql, params)

# Convenience wrappers (parallel to SQLite3 API)
db.get_rows(table, where=None)
db.get_row_count(table, where=None)
```

## Tables / Schema

```python
db.create_table(
    "results",
    {"id": "SERIAL PRIMARY KEY", "value": "DOUBLE PRECISION", "label": "TEXT"},
)
db.drop_table("results")
db.rename_table("old", "new")
db.get_table_names()
db.get_table_schema("results")

# Schema-level (PostgreSQL only)
db.get_tables()
db.get_columns("results")
db.get_primary_keys("results")
db.get_foreign_keys("results")
db.get_indexes("results")
db.table_exists("results")
db.column_exists("results", "value")
```

## Batch Insert & DataFrame

```python
db.insert_many("results", [{"value": v} for v in values])

import pandas as pd
db.dataframe_to_sql(df, table="results", if_exists="append")
db.copy_table(src="results", dst="results_backup")
```

## Numpy Array / Blob

`PostgreSQL` does expose `save_array` / `load_array` / `binary_to_array`
via its BatchMixin (stores via bytea); behavior differs from SQLite3's
`_ArrayMixin` — no compression by default, no sibling metadata columns.

```python
db.save_array(table, data=arr, column="payload")
arr = db.load_array(table, column="payload", where="...")
```

Generic blob:

```python
db.save_blob(...)
db.load_blob(...)
```

## Backup / Restore

```python
db.backup_database("dump.sql")
db.restore_database("dump.sql")
db.backup_table("results", "results.sql")
db.restore_table("results", "results.sql")
```

## Indexes & Maintenance

```python
db.create_index("results", columns=["value"], unique=False)
db.drop_index("results_value_idx")
db.get_indexes("results")

db.vacuum(table=None, full=False)
db.analyze(table=None)
db.reindex(table=None)
db.optimize(table=None)
db.get_table_size("results")
db.get_database_size()
with db.maintenance_lock(): ...
```

## Transactions

```python
db.begin(); db.commit(); db.rollback()
db.enable_foreign_keys(); db.disable_foreign_keys()
```

## Import / Export

```python
db.load_from_csv("results", "results.csv")
db.save_to_csv("results", "results.csv")
```

## Key Differences from SQLite3

- Requires a running PostgreSQL server and credentials.
- No git-based versioning (`_GitMixin` is SQLite3-only).
- Adds `_SchemaMixin` (introspection) and `_BackupMixin` (`pg_dump`-style
  helpers).
- BLOB/array storage uses `bytea`, no automatic compression.
