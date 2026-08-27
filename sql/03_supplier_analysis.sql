SELECT 
suppliers.supplier_name,
suppliers.country,
SUM(purchase_orders.amount) AS total_amount,
COUNT(purchase_orders.order_id) AS total_orders,
AVG(purchase_orders.amount) AS average_order_amount
FROM suppliers
JOIN purchase_orders ON suppliers.supplier_id = purchase_orders.supplier_id
GROUP BY suppliers.supplier_name, suppliers.country
HAVING SUM(purchase_orders.amount) > 5000
ORDER BY total_amount DESC
go