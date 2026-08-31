BEGIN TRAN

INSERT INTO purchase_orders (order_id, supplier_id, amount, order_date)
VALUES (6, 1, 4000, '2026-08-25 08:15:00')
IF @@error != 0
BEGIN
ROLLBACK TRAN
RETURN
END


INSERT INTO purchase_orders (order_id, supplier_id, amount, order_date)
VALUES (2, 3, 25000, '2026-08-03 14:30:00')
IF @@error != 0
BEGIN
ROLLBACK TRAN
RETURN
END

COMMIT TRAN
go