from dataclasses import dataclass

@dataclass
class Product:
  sku: str
  name: str
  description: str
  units_available: int
  unit_price: float

  def has_units(self) -> bool:
      return self.units_available > 0

  def reduce_units(self, qty: int) -> bool:
      if self.has_units() and self.units_available >= qty:
          self.units_available -= qty
          return True
      return False
