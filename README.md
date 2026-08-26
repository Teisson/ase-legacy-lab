# SAP ASE 16 Legacy Data Lab

Small hands-on lab for learning SAP Adaptive Server Enterprise 16
and exploring legacy-to-modern data engineering patterns.

## Environment

Host OS:
- Red Hat Enterprise Linux 9.8
- x86_64
- VMware virtual machine

Container runtime:
- Podman 5.8.2

ASE:
- SAP Adaptive Server Enterprise 16.0 SP02
- Container image: docker.io/datagrip/sybase:16.0
- Container name: ase16
- ASE port: 5000
- Database: testdb

## Starting the Environment

Check container status:

    podman ps -a

Start ASE if required:

    podman start ase16

Enter the container:

    podman exec -it ase16 bash

Load the Sybase environment:

    source /opt/sybase/SYBASE.sh

Important environment variables:

    SYBASE=/opt/sybase
    SYBASE_ASE=ASE-16_0
    SYBASE_OCS=OCS-16_0

The `isql` client is located at:

    /opt/sybase/OCS-16_0/bin/isql

## Connecting with isql

The ASE server alias is:

    MYSYBASE

The lab database is:

    testdb

A test login was created by the container initialization script:

    username: tester

Do not store passwords in this repository.

Set the default ASE server:

    export DSQUERY=MYSYBASE

Connect:

    isql -U tester

Enter the password interactively.

Switch to the lab database:

    use testdb
    go

Verify current database:

    select db_name()
    go

Verify ASE version:

    select @@version
    go

## Database Schema

### suppliers

Grain:
One row per supplier.

Columns:

| Column | Type | Constraint |
| --- | --- | --- |
| supplier_id | int | PRIMARY KEY, NOT NULL |
| supplier_name | varchar(100) | NOT NULL |
| country | varchar(2) | nullable |

Relationship:

    suppliers (1) ----< purchase_orders (many)

### purchase_orders

Grain:
One row per purchase order.

Columns:

| Column | Type |
| --- | --- |
| order_id | int |
| supplier_id | int |
| amount | numeric(12,2) |
| order_date | datetime |

`supplier_id` relates purchase orders to `suppliers.supplier_id`.

## Current Test Data

Suppliers:

- Volvo / SE
- Bosch / DE
- Siemens / DE

Five purchase orders have been created across the three suppliers.

## ASE Notes / Differences Encountered

### Batch execution

`isql` uses:

    go

to send the current SQL batch to ASE.

### Primary keys

In this ASE environment, the primary-key column had to be explicitly
declared `NOT NULL`.

### INSERT syntax

The multi-row VALUES syntax commonly used in modern SQL:

    INSERT INTO table (...)
    VALUES (...),
           (...),
           (...)

was not accepted by this ASE version.

Separate INSERT statements were used instead.

### GROUP BY

ASE can allow non-aggregated SELECT columns that are not included in
GROUP BY, which can produce surprising results.

For predictable queries, explicitly group all selected
non-aggregated columns.

### Aggregation and grain

`purchase_orders` has order-level grain.

The supplier-spend query changes the grain to one row per supplier
using:

- COUNT()
- SUM()
- AVG()
- GROUP BY

HAVING is then used to filter the aggregated result.

## Next Steps

- Create supplier spend view
- Explore transactions: BEGIN TRAN / COMMIT / ROLLBACK
- Create stored procedure
- Explore indexes and query plans
- Inspect ASE metadata/system tables
- Connect to ASE from Python
- Extract and validate legacy data
- Model data for a modern target platform
