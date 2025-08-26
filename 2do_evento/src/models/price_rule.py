from interfaces.price_rule_interface import PriceRuleInterface



class RegularPriceRule(PriceRuleInterface):
    def is_applicable(self, sku: str):
        pass

    def calculate_total(self, qty: float, price: float) -> float:
        pass


class WeightBasedPriceRule(PriceRuleInterface):
    def is_applicable(self, sku: str):
        pass

    def calculate_total(self, qty: float, price: float) -> float:
          pass


class SpecialPriceRule(PriceRuleInterface):
    def is_applicable(self, sku: str):
        pass

    def calculate_total(self, qty: float, price: float) -> float:
        pass
