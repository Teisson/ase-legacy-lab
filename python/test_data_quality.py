from unittest import TestCase
from data_quality import check_suppliers, check_orders

class TestDataQualityChecker(TestCase):
    def test_empty_suppliers_list(self):
        with self.assertRaises(ValueError):
            check_suppliers([])

    def test_empty_orders_list(self):
        with self.assertRaises(ValueError):
            check_orders([])
