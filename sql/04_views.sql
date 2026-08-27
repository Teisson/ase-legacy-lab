CREATE VIEW supplier_analysis AS
SELECT 
s.supplier_id, 
s.supplier_name, 
s.country, 
SUM(po.amount) AS total_amount, 
COUNT(po.order_id) AS total_orders, 
AVG(po.amount) AS average_order_amount
FROM suppliers AS s
JOIN purchase_orders AS po 
ON s.supplier_id = po.supplier_id
GROUP BY 
s.supplier_id, 
s.supplier_name, 
s.country
go