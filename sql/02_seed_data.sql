INSERT INTO suppliers (supplier_id, supplier_name, country) 
VALUES (1, 'Volvo', 'SE')
INSERT INTO suppliers (supplier_id, supplier_name, country) 
VALUES (2, 'Bosch', 'DE')
INSERT INTO suppliers (supplier_id, supplier_name, country) 
VALUES (3, 'Siemens', 'DE')
go

INSERT INTO purchase_orders (order_id, supplier_id, amount, order_date)
VALUES (1, 1, 500000, '2026-08-01 08:15:00')
INSERT INTO purchase_orders (order_id, supplier_id, amount, order_date)
VALUES (2, 3, 25000, '2026-08-03 14:30:00')
INSERT INTO purchase_orders (order_id, supplier_id, amount, order_date)
VALUES (3, 1, 200, '2026-08-03 16:45:00')
INSERT INTO purchase_orders (order_id, supplier_id, amount, order_date)
VALUES (4, 2, 7700, '2026-08-12 10:00:00')
INSERT INTO purchase_orders (order_id, supplier_id, amount, order_date)
VALUES (5, 2, 2300, '2026-08-20 13:20:00')
go  