from order import Order
from supplier import Supplier
from physical_product import PhysicalProduct
from discount_strategy import BulkDiscount, DiscountStrategy, PercentageDiscount

supplier = Supplier("S1", "Acme", "acme@mail.com")
product = PhysicalProduct("P1", "Lamp", 50.0, 10, 2.0, supplier)

order = Order("ORD01", BulkDiscount(200, 20))
order.add_order_line(product, 5)  

print(order.calculate_total())   

order.set_discount(PercentageDiscount(10))
print(order.calculate_total())   