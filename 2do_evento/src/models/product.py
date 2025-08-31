from dataclasses import dataclass
from src.models.rules_manager import RulesManager

@dataclass
class Product:
  sku: str
  name: str
  description: str
  units_available: float
  unit_price: float

  def has_units(self) -> bool:
      return self.units_available > 0

  def reduce_units(self, qty: float) -> bool:
      if self.has_units() and self.units_available >= qty:
          self.units_available -= qty
          return True
      return False
  
  def get_qty(self, qty: float) -> float | int:
      rule = RulesManager.get_rule(self.sku)
      if rule:
          return rule.get_qty(qty)
      raise ValueError("No applicable pricing rule found.")
