from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier
from product_factory import ProductFactory
import os 
import json
import csv

INVENTORY_FILE = "inventory.json"

def save_inventory (inventory: Inventory) -> None :
    with open (INVENTORY_FILE, "w") as f:
        json.dump(inventory.get_all_as_dicts(), f, indent = 4)

def load_inventory () -> Inventory :
    inventory = Inventory ()
    if os.path.exists(INVENTORY_FILE):
        print("Inventory.json Found")
        with open (INVENTORY_FILE, "r") as f:
            data = json.load(f)
            
            for i in data:
                s = i["Supplier"]
                supplier = Supplier(s["SupplierID"], s["Name"], s["ContactEmail"])

                if i ["Type"] == "Physical":
                    product = PhysicalProduct(i["Product ID"], i["Product Name"], i["Price"], i["Stock"], i["Weight"], supplier )

                elif i["Type"] == "Digital":
                    product = DigitalProduct(i["Product ID"], i["Product Name"], i["Price"], i["Stock"], i["Download Size"], supplier)

                else: 
                    print("Unknown Type. Skipped")
                    continue
                inventory.add_product(product)
    else:
        print("Inventory not found.")

    return inventory

def get_positive_float(prompt:str) -> float:
    while True: 
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")

def load_products(path:str, inventory:Inventory, supplier:Supplier) -> None:
    try: 
        file = open(path, newline ="")

    except FileNotFoundError:
        print(f"Products file not found: {path}")

    else:
        loaded = 0

        with file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                try:
                    product = ProductFactory.create(
                        row[0].capitalize(),
                        row[1],
                        row[2],
                        float(row[3]),
                        int(row[4]),
                        supplier
                    )

                    if inventory.add_product(product):
                        loaded += 1

                except ValueError as error:
                    print(f"Product skipped: {error}")

        print(f"{loaded} products loaded.")

    finally:
        print("Load attmept finished.")

def main() -> None:
    inventory = load_inventory()

    while True:
        print("----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        choice = input("Enter option: ").strip()

        if choice == "1":
            inventory.display_all()

        elif choice == "2":
            product_type = input("Product type (1. Physical, 2. Digital): ").strip()
            if product_type not in ("1", "2"):
                print("Invalid product type.")
                continue 

            product_id = input("Enter Product ID: ").strip()
            name = input("Enter Product Name: ").strip()

            supplier_id = input("Enter Supplier ID: ").strip()
            supplier_name = input("Enter Supplier Name: ").strip()
            contact_email = input("Enter Contact Email: ").strip()
            supplier = Supplier(supplier_id, supplier_name, contact_email)

            try:
                price = get_positive_float("Enter the price of the product: ")
                stock = int(input("Enter the stock amount of the product: ").strip())

                if product_type == "1":
                    weight = float(input("Enter the weight (kg): ").strip())
                    product = ProductFactory.create("Physical", product_id, name, price, stock, supplier, weight = weight)

                elif product_type == "2":
                    download_size = float(input("Enter the download size (MB): ").strip())
                    product = ProductFactory.create("Digital", product_id, name, price, stock, supplier, download_size = download_size )

            except ValueError:
                print("Invalid input, Product not added.")
                continue

            if inventory.add_product(product):
                print("Product added succesfully!")

            else:
                print("Product already exists.")

        elif choice == "3":
            product_id = input("Enter Product ID: ").strip()
            product = inventory.find_product(product_id)
            if product is None:
                print("Product not found")
                continue

            try:
                new_stock = int(input("Enter the new stock quantity: ").strip())

            except ValueError:
                print("Invalid value. Stock not updated.")
                continue

            if product.update_stock(new_stock):
                print("Stock updated sucessfully.")

            else:
                print("Stock cannot be negative. Stock not updated.")

        elif choice == "4":
            product_id = input("Enter Product ID: ").strip()
            product = inventory.find_product(product_id)
            if product is None:
                print("Product not found")
            else:
                product.display_information()


        elif choice == "5":
            save_inventory(inventory)
            print("Inventory Saved")

        elif choice == "6":
            save_inventory(inventory)
            print("Inventory saved")
            print("Thank you for your use!")
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
