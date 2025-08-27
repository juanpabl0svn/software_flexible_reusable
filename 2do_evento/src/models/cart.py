from src.models.item import Item


class Cart:

    items: list[Item] = []

    def add_item(self, item: Item):
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
