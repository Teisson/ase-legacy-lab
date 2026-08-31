/*
    Transaction handling demonstration.

    Demonstrates atomic execution of multiple statements:
    - successful statements are committed together
    - an error causes the transaction to roll back
    - RETURN prevents execution from continuing after rollback

    This script uses fixed test IDs and is intended for demonstration,
    not as an idempotent deployment script.
*/

BEGIN TRAN

INSERT INTO purchase_orders (order_id, supplier_id, amount, order_date)
VALUES (6, 1, 4000, '2026-08-25 08:15:00')
IF @@error != 0
BEGIN
ROLLBACK TRAN
RETURN
END


INSERT INTO purchase_orders (order_id, supplier_id, amount, order_date)
VALUES (7, 3, 25000, '2026-08-03 14:30:00')
IF @@error != 0
BEGIN
ROLLBACK TRAN
RETURN
END

COMMIT TRAN
go