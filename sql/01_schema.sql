CREATE TABLE suppliers (
    supplier_id INT PRIMARY KEY NOT NULL,
    supplier_name VARCHAR(100) NOT NULL,
    country VARCHAR(2)
)
go

CREATE TABLE purchase_orders (
    order_id INT PRIMARY KEY NOT NULL,
    supplier_id INT NOT NULL,
    FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id),
    amount NUMERIC(12, 2) NOT NULL,
    order_date DATETIME NOT NULL
)
go