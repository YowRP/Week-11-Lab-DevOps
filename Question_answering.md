1. Diagnose: Before writing anything new, look through your Lab 8 code and note down: (1) any if/elif
block that chooses between different behaviours, (2) every place you create a PhysicalProduct or
DigitalProduct directly, and (3) one place where bad input or a missing file could crash your program.
Keep these notes; you will come back to them in Section 6.

    (1) In Inventory_manager.py, load_inventory() uses an if/elif/else block from the lines 25-33, to choose which product subclass to create. The add_products option also uses an if/elif block at lines 74-80 to create a physical or digital product. The menu at lines 53-132 chooses between user actions for different selections.

    (2) Under def main() of Inventory_manager.py, the elif == 2 for user choice calls the PhysicalProduct subclass and also DigitalProduct subclass to create a new product (add_product function). Under the load_inventory() def, the PhysicalProduct and DigitalProduct is called to create an object from saved product data, differentiating about into Physical and Digital data itself.

    (3) In Inventory_manager.py, line 22 accesses i["Supplier"] when loading the products. If a product record in inventory.json is missing the "Supplier" key, an unhandled KeyError will stop the program.


2. The business now wants a 5% student discount. Without the Strategy pattern, which class
and method must change? 

    Prediction: Without the strategy pattern, the class and method that would be needed to changed is the Order class where the method of calculation_total() method to handle the student discount. 

    After Completion of Step 2:

    Answer: The strategy version didn't alter the total_calculation defination a lot. The addition of set_discount as the setter for the order line will be added inside and also the import of the new file about it. Thus, the strategy implementation allows lesser alterations into the code and keeping the code clean and easy. 

3. Create an order whose lines add up to 250. What will calculate_total() return with
BulkDiscount(200, 20)? What if you then call set_discount(PercentageDiscount(10)) on the same order?
Write both answers down, then run your code and check.

    Prediction: After the BulkDiscount (200,20) will return 230 for the toal.
    If the call Percentage Discount happens on the same order, the total will be dicounted for 10%

4. Look back at Lab 8. Which relationship best describes Order and DiscountStrategy:
association, aggregation or composition? Hint: is a discount part of an order, or something the order
uses? Could two orders share the same PercentageDiscount object? Write your answer and a
multiplicity for each end, then check it against your code.

    Prediction: Order and Discount Strategy has a Association relation because the order uses a discount strategy, which can exist independantly and be shared by multiple orders. Each order uses exactly one Discount Strategy, while each Discount Strategy can be used by zero or more Orders. 

    Multiplicity for: Order "0..*" --------------- "1" Discount Strategy (One order uses exactly 1 discount strategy at 1 time; One Discount stratgy is used by 0..* orders because multiple orders can share it.)

5. What happens if you call ProductFactory.create("service", ...)? Which line raises the
exception, and what happens to your program if nothing catches it? Run it and check.

    Prediction: The use of ProductFactory.create("service", ....) will the following arguments will raise ValueError, because "service" is not a supported product type. The raise ValueErorr(...) line in the else block of product_factory.py raises the exception. If nothing catches it, the program stops and it displays a traceback. 

6. Suppose a new BundleProduct type is added. How many places in your code would need
to change before you added the factory, and how many after? Count them, then explain why the factory
still breaks OCP and why that is acceptable here.

    Prediction: Before using the product factory class, the method of load_inventory() and also add product function that is inside main() will be needed to be changed to accomodate this new item. After using this factory, the construction descision changes into one location, ProductFactory.create(). The menu or data handling may still need updating to support bundle-specific input. The factory still breaks OCP beacuse adding a product type requires modifying if/elif block. However, this is still acceptable for a small application because it centralise the change and avoids unnecessary complexity. 

7. Think back to the Lab 8 LSP discussion. If Product validates that stock cannot go negative,
should DigitalProduct be allowed to skip or change that rule? Why?

    No, Digital Product should not skip or change the non-negative stock rule. Under LSP, it must remain usable whereever a Product is expected and preserve the parent class's guarentees. 

8. A user enters abc, then -5, then 12.50. Write down exactly what prints after each entry and
what value is returned. Then run it and check.

    Prediction: 
        1st Entry (user enters 'abc'): The message of "Please enter a valid number, e.g. 12.50" printed and asks again.
        2nd Entry (user enters -5): The message of "Please enter a number greater than zero." printed and asks again.
        3rd Entery (user enters 12.50): Prints no error message and returns the float 12.50.

    Actual results:
        1st Entry : Please enter a valid number, e.g. 12.50
        2nd Entry: Please enter a number greater than zero.
        3rd Entry: Enter the price of the product: 12.50
                   Enter the stock amount of the product: 

9. Before running, write down how many products will load, which messages will print, and in
what order. Then rename products.csv and predict again: which of except, else and finally will run?

    Predict: Due to some differentiations in my current code, which physical is renamed as Physical, the code would not run. However, after the alterations, the product prediction would load as follows:
            Desk Lamp, Photo Editor and Monitor Stand

            For the messages that may appear will be :
            Product Skipped: Unkown product type: Service
            Product Skipped: could not convert string to float 'abc'
            3 products loaded 
            Load attempt failed
    
    Predict 2: The file name 'products.csv' will not be the same and hence the Python code could not load the file / find the file.
        The message printed for this will be:
        Products file not found: products.csv
        Load attempt finished.

