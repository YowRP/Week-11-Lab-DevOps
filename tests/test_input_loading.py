import sys
from pathlib import Path
import unittest
from unittest.mock import patch
from io import StringIO
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from Inventory_manager import get_positive_float, load_products
from inventory import Inventory
from supplier import Supplier


class TestInputAndLoading(unittest.TestCase):

    def test_invalid_input_then_valid(self):
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]) as user_input:
            with patch("sys.stdout", new_callable=StringIO) as output:
                result = get_positive_float("Enter price: ")

        self.assertEqual(result, 12.5)
        self.assertEqual(user_input.call_count, 3)
        self.assertEqual(
            output.getvalue().splitlines(),
            [
                "Please enter a valid number, e.g. 12.50",
                "Please enter a number greater than zero.",
            ]
        )

    def test_missing_file(self):
        inventory = Inventory()
        supplier = Supplier("S1", "Acme", "acme@mail.com")

        with TemporaryDirectory() as folder:
            path = str(Path(folder) / "missing.csv")

            with patch("sys.stdout", new_callable=StringIO) as output:
                load_products(path, inventory, supplier)

        self.assertEqual(len(inventory.get_product()), 0)
        self.assertEqual(
            output.getvalue().splitlines(),
            [
                f"Products file not found: {path}",
                "Load attempt finished.",
            ]
        )

    def test_bad_rows_skipped(self):
        inventory = Inventory()
        supplier = Supplier("S1", "Acme", "acme@mail.com")

        csv_data = (
            "product_type,product_id,name,price,stock_quantity\n"
            "physical,P001,Desk Lamp,25.00,10\n"
            "digital,D001,Photo Editor,49.90,100\n"
            "service,S001,Installation,30.00,5\n"
            "physical,P002,Office Chair,abc,3\n"
            "physical,P003,Monitor Stand,39.50,7\n"
        )

        with TemporaryDirectory() as folder:
            path = Path(folder) / "products.csv"
            path.write_text(csv_data)

            with patch("sys.stdout", new_callable=StringIO) as output:
                load_products(str(path), inventory, supplier)

        product_ids = [
            product.get_product_id()
            for product in inventory.get_product()
        ]

        self.assertEqual(product_ids, ["P001", "D001", "P003"])

        messages = output.getvalue().splitlines()
        self.assertEqual(len(messages), 4)
        self.assertIn("Unknown product type", messages[0])
        self.assertIn("abc", messages[1])
        self.assertEqual(messages[2], "3 products loaded.")
        self.assertEqual(messages[3], "Load attempt finished.")


if __name__ == "__main__":
    unittest.main(verbosity=2)