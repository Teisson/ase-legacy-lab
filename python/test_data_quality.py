import pytest
from data_quality import check_suppliers, check_orders

def test_empty_suppliers_list():
    with pytest.raises(ValueError):
        check_suppliers([])

def test_empty_orders_list():
    with pytest.raises(ValueError):
            check_orders([])

def test_duplicate_supplier_id():
    suppliers = [
        {"supplier_id": 1, "supplier_name": "Volvo"},
        {"supplier_id": 1, "supplier_name": "Bosch"}
    ]
    with pytest.raises(ValueError, match="Duplicate supplier_id found: 1"):
        check_suppliers(suppliers)

def test_duplicate_order_id():
    orders = [
        {"order_id": 1, "supplier_id": 1},
        {"order_id": 1, "supplier_id": 1}
    ]
    with pytest.raises(ValueError, match="Duplicate order_id found: 1"):
        check_orders(orders)
    
def test_valid_suppliers():
    suppliers = [
        {"supplier_id": 1, "supplier_name": "Volvo"},
        {"supplier_id": 2, "supplier_name": "Bosch"}
    ]
    try:
        check_suppliers(suppliers)
    except ValueError:
        pytest.fail("check_suppliers raised ValueError unexpectedly!")

def test_valid_orders():
    orders = [
        {"order_id": 1, "supplier_id": 1},
        {"order_id": 2, "supplier_id": 2}
    ]
    try:
        check_orders(orders)
    except ValueError:
        pytest.fail("check_orders raised ValueError unexpectedly!")