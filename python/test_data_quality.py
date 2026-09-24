import pytest
from data_quality import check_suppliers, check_orders

def test_empty_suppliers_list():
    with pytest.raises(ValueError):
        check_suppliers([])

def test_empty_orders_list():
    with pytest.raises(ValueError):
            check_orders([])
