from src.models.user import User
from src.models.item import Item
from src.models.product import Product

from dataclasses import dataclass

@dataclass
class Store:
    users: list[User]
    products: list[Product]
    total_sales: float = 0.0

    def add_product_to_cart(self, user: User, product: Product, qty: float):
        item = user.cart.get_item_from_cart(product)
        if item:
            item.qty += qty
        else:
            user.cart.add_item(product, qty)

    def delete_item_from_cart(self, user: User, item: Item):
        user.cart.remove_item(item)
        item.product.units_available += item.qty

    def finish_order(self, user: User):
        self.total_sales += user.cart.calculate_total()
        for item in user.cart.items:
            item.product.units_available -= item.qty
        user.cart.items.clear()
        
    def can_purchase(self, user: User) -> bool:
        for item in user.cart.items:
            if item.qty > item.product.units_available:
                return False
        return True    
