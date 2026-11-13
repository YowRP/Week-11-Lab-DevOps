import unittest

from order import Order
from supplier import Supplier
from product_factory import ProductFactory
from discount_strategy import BulkDiscount, NoDiscount, PercentageDiscount, DiscountStrategy

class TestDiscounts(unittest.TestCase):

    def setUp(self):
        supplier = Supplier("S1", "Acme", "acme@mail.com")

        self.product = ProductFactory.create(
            "Physical", "P1", "Lamp", 50.0, 10,
            supplier, weight=2.0
        )

    def test_no_discount(self):
        order = Order("ORD01")
        order.add_order_line(self.product, 5)

        self.assertEqual(order.calculate_total(), 250.0)

    def test_percentage_discount(self):
        order = Order("ORD02", PercentageDiscount(10))
        order.add_order_line(self.product, 5)

        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_bulk_discount(self):
        order = Order("ORD03", BulkDiscount(200, 20))
        order.add_order_line(self.product, 5)

        self.assertEqual(order.calculate_total(), 230.0)

    def test_bulk_below_threshold(self):
        order = Order("ORD04", BulkDiscount(200, 20))
        order.add_order_line(self.product, 3)

        self.assertEqual(order.calculate_total(), 150.0)

    def test_bulk_at_threshold(self):
        order = Order("ORD05", BulkDiscount(200, 20))
        order.add_order_line(self.product, 4)

        self.assertEqual(order.calculate_total(), 180.0)

    def test_change_discount(self):
        order = Order("ORD06", BulkDiscount(200, 20))
        order.add_order_line(self.product, 5)

        self.assertEqual(order.calculate_total(), 230.0)

        order.set_discount(PercentageDiscount(10))

        self.assertAlmostEqual(order.calculate_total(), 225.0)


if __name__ == "__main__":
    unittest.main()