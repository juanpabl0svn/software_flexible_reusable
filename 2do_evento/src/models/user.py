from src.models.item import Item
from src.models.cart import Cart
from dataclasses import dataclass

@dataclass
class User:
  cart: Cart

  def add_item_to_cart(self, item: Item):
      self.cart.add_item(item)