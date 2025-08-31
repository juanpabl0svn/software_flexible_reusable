from src.models.product import Product
from dataclasses import dataclass
from src.models.rules_manager import RulesManager

@dataclass
class Item:
  product: Product
  qty: float

  def calculate_total(self) -> float:
    price_rule = RulesManager.get_rule(self.product.sku)
    if price_rule:
        return price_rule.calculate_total(self.qty, self.product.unit_price)
    raise Exception("No applicable price rule found")
