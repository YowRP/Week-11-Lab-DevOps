import sys
from pathlib import Path
import unittest

# Find project files when running this file directly.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from supplier import Supplier
from product_factory import ProductFactory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from order_line import OrderLine


class TestProducts(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier("S1", "Acme", "acme@mail.com")

    def test_create_physical(self):
        product = ProductFactory.create(
            "Physical", "P1", "Lamp", 50.0, 10,
            self.supplier, weight=2.0
        )
        self.assertIsInstance(product, PhysicalProduct)

    def test_create_digital(self):
        product = ProductFactory.create(
            "Digital", "D1", "Ebook", 10.0, 100,
            self.supplier, download_size=5.0
        )
        self.assertIsInstance(product, DigitalProduct)

    def test_unknown_type(self):
        with self.assertRaisesRegex(ValueError, "Unknown product type"):
            ProductFactory.create(
                "service", "S1", "Installation", 30.0, 5,
                self.supplier
            )

    def test_invalid_price(self):
        for price in (0, -10):
            with self.subTest(price=price):
                with self.assertRaises(ValueError):
                    ProductFactory.create(
                        "Physical", "P1", "Lamp", price, 10,
                        self.supplier
                    )

    def test_negative_stock(self):
        with self.assertRaises(ValueError):
            ProductFactory.create(
                "Digital", "D1", "Ebook", 10.0, -1,
                self.supplier
            )

    def test_zero_stock_allowed(self):
        product = ProductFactory.create(
            "Physical", "P1", "Lamp", 50.0, 0,
            self.supplier
        )
        self.assertIsInstance(product, PhysicalProduct)

    def test_invalid_order_quantity(self):
        product = ProductFactory.create(
            "Physical", "P1", "Lamp", 50.0, 10,
            self.supplier
        )

        for quantity in (0, -1):
            with self.subTest(quantity=quantity):
                with self.assertRaises(ValueError):
                    OrderLine(product, quantity)

    def test_negative_stock_update(self):
        product = ProductFactory.create(
            "Physical", "P1", "Lamp", 50.0, 10,
            self.supplier
        )

        with self.assertRaises(ValueError):
            product.update_stock(-1)


if __name__ == "__main__":
    unittest.main(verbosity=2)