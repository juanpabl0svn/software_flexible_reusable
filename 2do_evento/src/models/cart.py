from src.models.item import Item
from src.models.product import Product


class Cart:

    items: list[Item] = []

    def add_item(self, product: Product, qty: int):
        item = Item(product=product, qty=qty)   
        self.items.append(item)

    def calculate_total(self) -> float:
        total = 0
        for item in self.items:
            total += item.calculate_total()
        return total

    def remove_item(self, item: Item):
        self.items.remove(item)

    def show_items_prices(self):
        for item in self.items:
            print(f"{item.product.name} x {item.qty} | Precio total: ${item.calculate_total()}")
    
    def get_item_from_cart(self, product: Product) -> Item | None:
        for item in self.items:
            if item.product == product:
                return item
        return None
