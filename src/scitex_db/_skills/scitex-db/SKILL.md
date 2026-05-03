---
name: scitex-db
description: |
  [WHAT] Relational-DB wrapper for scientific Python.
  [WHEN] Use when the user asks to "store numpy arrays in SQLite", "persist experiment results to Postgres", "dedupe rows in a table", "check this SQLite DB is healthy / not corrupt", "inspect the schema of a DB", "save/load compressed ndarrays a....
  [HOW] `import scitex_db` then call `SQLite3(db_path, ...)`.
tags: [scitex-db]
primary_interface: python
interfaces:
  python: 3
  cli: 1
  mcp: 0
  skills: 2
  hook: 0
  http: 0
---


# scitex-db

> **Interfaces:** Python ⭐⭐⭐ (primary) · CLI ⭐ · MCP — · Skills ⭐⭐ · Hook — · HTTP —

Two database classes (`SQLite3`, `PostgreSQL`) composed from a dozen
shared mixins, plus standalone maintenance helpers.

## Installation & import (two equivalent paths)

The same module is reachable via two install paths. Both forms work at
runtime; which one a user has depends on their install choice.

```python
# Standalone — pip install scitex-db
import scitex_db
scitex_db.SQLite3(...)

# Umbrella — pip install scitex
import scitex.db
scitex.db.SQLite3(...)
```

`pip install scitex-db` alone does NOT expose the `scitex` namespace;
`import scitex.db` raises `ModuleNotFoundError`. To use the
`scitex.db` form, also `pip install scitex`.

See [../../general/02_interface-python-api.md] for the ecosystem-wide
rule and empirical verification table.

## Sub-skills

### Core

* [01_quick-start](01_quick-start.md) — SQLite3 + PostgreSQL minimal examples
* [02_python-api](02_python-api.md) — Public symbols
* [03_mixins](03_mixins.md) — The mixin architecture (capability groups)
* [04_numpy-blob](04_numpy-blob.md) — Storing ndarrays with compression
* [05_maintenance](05_maintenance.md) — `check_health`, `delete_duplicates`, `inspect`

### Interface

* [10_cli-reference](10_cli-reference.md) — `scitex-db inspect` / `health`
