from models.item import Item


class Cart:

    items: list[Item] = []

    def add_item(self, item: Item):
        self.items.append(item)

    def calculate_total(self) -> float:
        pass
  
    def remove_item(self, item: Item):
        self.items.remove(item)
