# SAP ASE 16 Legacy Data Lab

Small hands-on lab for learning SAP Adaptive Server Enterprise 16 and exploring legacy-to-modern data engineering patterns.

The project uses a containerized ASE environment on RHEL and implements a complete Python ETL workflow from SAP ASE to Google BigQuery, including extraction, data-quality validation, transformation, testing and least-privilege cloud loading.

## Pipeline Overview

```text
SAP ASE 16
    ↓
pyodbc / FreeTDS / unixODBC
    ↓
Python Extract
    ↓
Data Quality
    ↓
Python Transform
    ↓
BigQuery Load
    ↓
ase_legacy_data.enriched_purchase_orders
```

The source system remains at order-level grain. Purchase orders are enriched with supplier attributes in Python before being loaded to BigQuery.

## Environment

### Host

- Red Hat Enterprise Linux 9.8
- x86_64
- VMware virtual machine
- Python 3.11

### Container runtime

- Podman 5.8.2

### SAP ASE

- SAP Adaptive Server Enterprise 16.0 SP02
- Container image: `docker.io/datagrip/sybase:16.0`
- Container name: `ase16`
- ASE port: `5000`
- Database: `testdb`
- Server alias: `MYSYBASE`

### Google Cloud

- Project: `ase-legacy-lab`
- BigQuery dataset: `ase_legacy_data`
- Target table: `enriched_purchase_orders`
- Runtime identity: `ase-etl-runner`
- Local authentication: Application Default Credentials with service-account impersonation

No service-account key file is stored in the repository.

## Repository Structure

```text
ase-legacy-lab/
├── sql/
│   ├── 01_schema.sql
│   ├── 02_seed_data.sql
│   ├── 03_supplier_analysis.sql
│   ├── 04_views.sql
│   └── 05_transactions.sql
├── scripts/
│   └── run_sql.sh
├── python/
│   ├── db.py
│   ├── extract_suppliers.py
│   ├── extract_purchase_orders.py
│   ├── data_quality.py
│   ├── transform.py
│   ├── load.py
│   ├── test_data_quality.py
│   └── main.py
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

Local ASE connection settings are stored in `.env`, which is excluded from version control.

`.env.example` documents the required configuration without storing credentials in the repository.

## Python Environment

Create a Python 3.11 virtual environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Install runtime dependencies:

```bash
python -m pip install -r requirements.txt
```

For development and tests:

```bash
python -m pip install -r requirements-dev.txt
```

Primary direct dependencies are:

```text
google-cloud-bigquery
pyodbc
python-dotenv
pytest  # development only
```

## Starting the ASE Environment

Check container status:

```bash
podman ps -a
```

Start ASE if required:

```bash
podman start ase16
```

Enter the container:

```bash
podman exec -it ase16 bash
```

Load the SAP ASE environment:

```bash
source /opt/sybase/SYBASE.sh
```

Important environment variables include:

```text
SYBASE=/opt/sybase
SYBASE_ASE=ASE-16_0
SYBASE_OCS=OCS-16_0
```

The `isql` client is located at:

```text
/opt/sybase/OCS-16_0/bin/isql
```

## Local Configuration

Create the local environment file from the example:

```bash
cp .env.example .env
```

Configure the ASE connection:

```text
ASE_USER=<lab-user>
ASE_PASSWORD=<lab-password>
ASE_DATABASE=testdb
ASE_SERVER=MYSYBASE
ASE_HOST=127.0.0.1
ASE_PORT=5000
```

`.env` is ignored by Git and should not be committed.

## Connecting with isql

Set the default ASE server:

```bash
export DSQUERY=MYSYBASE
```

Connect using the lab user:

```bash
isql -U tester
```

Enter the password interactively.

Switch to the lab database:

```sql
use testdb
go
```

Verify the current database:

```sql
select db_name()
go
```

Verify the ASE version:

```sql
select @@version
go
```

## Running SQL Files

SQL files can be executed from the repository root using the Bash runner:

```bash
./scripts/run_sql.sh sql/03_supplier_analysis.sql
```

The runner:

- loads local connection settings from `.env`
- passes the required environment variables into the ASE container
- loads the SAP ASE environment
- sets `DSQUERY`
- executes the selected SQL file through `isql`

This keeps environment-specific configuration and credentials outside the SQL files and version control.

## Python Connectivity

Python connects to SAP ASE from the RHEL host using:

```text
Python
  ↓
pyodbc
  ↓
unixODBC
  ↓
FreeTDS
  ↓
TCP 127.0.0.1:5000
  ↓
Podman
  ↓
SAP ASE 16
```

The working FreeTDS connection uses TDS version `5.0`.

Connectivity was verified independently at multiple layers:

```text
ASE/isql
   ↓
FreeTDS/tsql
   ↓
unixODBC/isql
   ↓
pyodbc
```

This made it possible to isolate driver and configuration problems from Python application problems.

## Extract

The extraction layer is separated into distinct responsibilities:

- `db.py` loads local configuration and creates the ASE connection
- `extract_suppliers.py` extracts supplier data
- `extract_purchase_orders.py` extracts purchase-order data
- `main.py` owns the source connection lifecycle and orchestrates the pipeline

Both extractor functions receive an existing connection rather than creating their own.

Queries are executed through a `pyodbc` cursor. Column names are taken from `cursor.description` and combined with each row to produce:

```text
list[dict]
```

Example:

```python
[
    {
        "supplier_id": 1,
        "supplier_name": "Volvo",
        "country": "SE",
    }
]
```

Database-native values are preserved by the driver where possible. For example, ASE numeric values are returned as Python `Decimal` objects and ASE datetime values as `datetime` objects.

## Data Quality

`data_quality.py` provides explicit validation before transformation.

Supplier checks include:

- empty supplier input
- missing required keys
- invalid supplier IDs
- duplicate supplier IDs

Order checks include:

- empty order input
- missing required keys
- invalid order IDs
- duplicate order IDs

Referential integrity is also validated:

```text
purchase_orders.supplier_id
        ↓ must exist in
suppliers.supplier_id
```

An order referencing an unknown supplier causes the pipeline to fail before transformation.

## Tests

Data-quality rules are tested with `pytest`.

The test suite includes both positive and negative cases, including:

- empty suppliers
- empty orders
- duplicate supplier IDs
- duplicate order IDs
- valid suppliers
- valid orders
- invalid supplier references
- valid supplier references

Run the tests from the repository root:

```bash
python -m pytest python/test_data_quality.py -v
```

Current suite:

```text
8 passed
```

## Transform

`transform.py` enriches each purchase order with supplier attributes while preserving order-level grain.

A supplier lookup dictionary is built using `supplier_id`:

```text
supplier_id → supplier row
```

Each purchase order is then merged with its matching supplier data.

Example enriched order:

```python
{
    "order_id": 1,
    "supplier_id": 1,
    "amount": Decimal("500000.00"),
    "order_date": datetime(...),
    "supplier_name": "Volvo",
    "country": "SE",
}
```

The transformation does not aggregate the source orders. Business-level aggregation can be performed later in the target platform without losing source grain.

## Load to BigQuery

The target is:

```text
ase-legacy-lab.ase_legacy_data.enriched_purchase_orders
```

Target schema:

| Column | BigQuery type |
| --- | --- |
| `order_id` | INTEGER |
| `supplier_id` | INTEGER |
| `amount` | NUMERIC |
| `order_date` | DATETIME |
| `supplier_name` | STRING |
| `country` | STRING |

The loader uses the official `google-cloud-bigquery` Python client.

Before loading:

- `Decimal` values are converted to decimal string representations
- Python `datetime` values are converted using `isoformat()`

The BigQuery load job uses:

- `WRITE_TRUNCATE` to maintain a complete current snapshot rather than appending duplicates on repeated runs
- `CREATE_NEVER` so the pipeline expects the target table and schema to exist explicitly

The target table is therefore treated as a defined contract rather than being created implicitly by the pipeline.

## BigQuery Authentication and IAM

Local development uses Application Default Credentials with service-account impersonation.

```text
Developer Google account
        ↓ impersonates
ase-etl-runner
        ↓
BigQuery
```

The workload identity is separated from the personal developer identity.

The runner receives only the BigQuery permissions required by the pipeline, while no long-lived service-account key is stored locally or in Git.

## Running the End-to-End ETL

With ASE running, the Python environment active and BigQuery authentication configured:

```bash
python python/main.py
```

The pipeline performs:

```text
1. Open ASE connection
2. Extract purchase orders
3. Extract suppliers
4. Validate source data
5. Validate supplier references
6. Enrich purchase orders
7. Load the enriched snapshot to BigQuery
8. Close the ASE connection
```

A successful run reports the number of enriched and loaded orders.

The loaded data can be verified in BigQuery:

```sql
SELECT *
FROM `ase-legacy-lab.ase_legacy_data.enriched_purchase_orders`
ORDER BY order_id;
```

## Database Schema

### `suppliers`

**Grain:** one row per supplier.

| Column | Type | Constraint |
| --- | --- | --- |
| `supplier_id` | int | PRIMARY KEY, NOT NULL |
| `supplier_name` | varchar(100) | NOT NULL |
| `country` | varchar(2) | nullable |

Relationship:

```text
suppliers (1) ----< purchase_orders (many)
```

### `purchase_orders`

**Grain:** one row per purchase order.

| Column | Type | Constraint |
| --- | --- | --- |
| `order_id` | int | PRIMARY KEY, NOT NULL |
| `supplier_id` | int | FOREIGN KEY, NOT NULL |
| `amount` | numeric(12,2) | NOT NULL |
| `order_date` | datetime | NOT NULL |

`supplier_id` references `suppliers.supplier_id`.

## Seed Data

The seed dataset contains three suppliers:

- Volvo / SE
- Bosch / DE
- Siemens / DE

Five purchase orders are created by `02_seed_data.sql`.

Additional rows may be created temporarily or permanently when running the transaction demonstrations. The current end-to-end ETL test dataset contains seven purchase orders.

## Supplier Analysis

`03_supplier_analysis.sql` aggregates purchase-order data from order-level grain to supplier-level grain.

The analysis calculates:

- total purchase amount
- number of purchase orders
- average order amount

The supplier ID is retained as the stable entity key rather than relying only on supplier name.

`HAVING` is used to filter suppliers based on aggregated purchase value.

## Analytical View

`04_views.sql` creates the reusable `supplier_analysis` view.

The view exposes supplier-level measures while preserving `supplier_id` for lineage and stable entity identification.

Ordering is intentionally left to queries consuming the view rather than being defined as part of the view.

## Transaction Demonstration

`05_transactions.sql` demonstrates explicit transaction and error handling using:

- `BEGIN TRAN`
- `COMMIT TRAN`
- `ROLLBACK TRAN`
- `@@error`
- `RETURN`

Multiple statements are treated as a single unit of work.

After each data-modification statement, `@@error` is checked immediately. If an operation fails, the transaction is rolled back and execution stops. The transaction is committed only when all operations succeed.

The script uses fixed test IDs for demonstration purposes and is not intended to be an idempotent deployment script.

Both execution paths were tested:

```text
all statements succeed
        ↓
      COMMIT
        ↓
changes persist
```

```text
statement fails
        ↓
     ROLLBACK
        ↓
previous changes in the transaction are undone
```

## ASE Notes / Differences Encountered

### Batch execution

`isql` uses:

```sql
go
```

to send the current SQL batch to ASE.

### Object ownership

Objects created by the lab user are owned by `tester` rather than `dbo`.

ASE objects can be qualified using:

```text
database.owner.object
```

For example:

```text
testdb.tester.purchase_orders
```

This became relevant while investigating object resolution and ASE error 208.

### Primary keys

In this ASE environment, primary-key columns had to be explicitly declared `NOT NULL`.

### INSERT syntax

The multi-row `VALUES` syntax commonly used in modern SQL:

```sql
INSERT INTO table (...)
VALUES (...),
       (...),
       (...)
```

was not accepted by this ASE version.

Separate `INSERT` statements were used instead.

### GROUP BY

ASE can allow non-aggregated `SELECT` columns that are not included in `GROUP BY`, which can produce surprising results compared with more restrictive SQL implementations.

For predictable aggregation queries, all selected non-aggregated columns are explicitly included in `GROUP BY`.

### Aggregation and grain

`purchase_orders` has order-level grain.

The supplier analysis changes the grain to one row per supplier using:

- `COUNT()`
- `SUM()`
- `AVG()`
- `GROUP BY`

`HAVING` is then used to filter the aggregated result.

### Transaction behavior

A failed statement does not necessarily roll back previous successful statements in the same transaction.

This was tested interactively by:

1. starting a transaction
2. successfully inserting a row
3. deliberately causing a duplicate primary-key error
4. verifying that the first insert remained visible within the open transaction
5. explicitly rolling back the transaction
6. verifying that the first insert had been removed

The scripted transaction handling then reproduced this behavior with automatic rollback using `@@error`.

## Design Decisions

### Connection ownership

ASE connections are created centrally rather than independently inside each extractor.

Extractor functions receive the connection as an argument:

```python
extract_suppliers(connection)
extract_purchase_orders(connection)
```

This separates resource ownership from extraction logic and lets the orchestrator manage cleanup centrally.

### Source and target connectors are separate

The source connection uses `pyodbc`, FreeTDS and unixODBC.

The target uses the Google BigQuery Python client.

`main.py` orchestrates the two systems without requiring the extract or load modules to share connector-specific logic.

### Preserve source grain

The Python transformation enriches purchase orders but does not aggregate them.

This preserves the order-level source grain and allows downstream business logic to remain traceable to the original legacy records.

### Fail before load

Data-quality and referential-integrity checks run before transformation and loading.

Invalid data therefore fails before reaching the target platform.

### Snapshot load semantics

The lab uses a full snapshot load rather than incremental loading.

`WRITE_TRUNCATE` makes repeated executions idempotent with respect to target row count and avoids accumulating duplicate snapshots.

## Status

The first end-to-end version of the lab is complete:

```text
SAP ASE
  ↓
Python Extract
  ↓
Data Quality
  ↓
Python Transform
  ↓
BigQuery Load
```

The pipeline has been executed successfully with seven enriched purchase orders loaded and verified in BigQuery.

## Possible Later Extensions

The lab is intentionally feature-frozen at the completed ETL milestone. Possible future experiments include:

- incremental extraction and loading
- pipeline logging and execution metadata
- scheduling/orchestration
- CI/CD
- schema management / infrastructure as code
- indexes and query-plan exploration
- ASE metadata and system tables
- stored procedures
- repeatable/idempotent ASE deployment patterns
- broader transformation test coverage
