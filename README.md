# SAP ASE 16 Legacy Data Lab

Small hands-on lab for learning SAP Adaptive Server Enterprise 16 and exploring legacy-to-modern data engineering patterns.

The project uses a containerized ASE environment on RHEL and focuses on practical database behavior, SQL workflows, transaction handling and patterns relevant when working with legacy data sources.

## Environment

**Host**

- Red Hat Enterprise Linux 9.8
- x86_64
- VMware virtual machine

**Container runtime**

- Podman 5.8.2

**SAP ASE**

- SAP Adaptive Server Enterprise 16.0 SP02
- Container image: `docker.io/datagrip/sybase:16.0`
- Container name: `ase16`
- ASE port: `5000`
- Database: `testdb`
- Server alias: `MYSYBASE`

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
├── .env.example
├── .gitignore
└── README.md
```

Local connection settings are stored in `.env`, which is excluded from version control.

`.env.example` documents the required configuration without storing credentials in the repository.

## Starting the Environment

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

Configure the local ASE connection:

```text
ASE_USER=<lab-user>
ASE_PASSWORD=<lab-password>
ASE_DATABASE=testdb
ASE_SERVER=MYSYBASE
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

Additional rows may be created temporarily or permanently when running the transaction demonstrations.

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

## Next Steps

- Connect to ASE from Python
- Extract and validate legacy data
- Explore indexes and query plans
- Inspect ASE metadata and system tables
- Model extracted data for a modern target platform

### Possible Later Extensions

- Stored procedures
- Repeatable/idempotent database deployment patterns
- Automated data-quality checks