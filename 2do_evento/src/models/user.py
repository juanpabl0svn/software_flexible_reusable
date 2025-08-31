from src.models.item import Item
from src.models.cart import Cart
from src.models.product import Product

class User:
    def __init__(self):
        self.cart = Cart()

    def add_item_to_cart(self, product: Product, qty: float):
        self.cart.add_item(product, qty)

    def remove_item_from_cart(self, item: Item):
        self.cart.remove_item(item)