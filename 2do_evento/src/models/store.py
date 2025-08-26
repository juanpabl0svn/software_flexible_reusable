from models.user import User
from models.item import Item


class Store:

  total_sells: float = 0.0

  def add_product_to_cart(self, user: User, item: Item):
      user.cart.add_item(item)

  def delete_item_from_cart(self, user: User, item: Item):
      user.cart.remove_item(item)

  def finish_order(self, user: User):
      self.total_sells += user.cart.calculate_total()
      user.cart.items.clear()
