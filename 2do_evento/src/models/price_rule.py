from src.interfaces.price_rule_interface import PriceRuleInterface



class RegularPriceRule(PriceRuleInterface):
    @staticmethod
    def is_applicable(sku: str):
        return sku[:2].upper() == "EA"

    @staticmethod
    def calculate_total(qty: float, price: float) -> float:
        qty = int(qty)
        return qty * price


class WeightBasedPriceRule(PriceRuleInterface):
    @staticmethod
    def is_applicable(sku: str):
        return sku[:2].upper() == "WE"

    @staticmethod
    def calculate_total(qty: float, price: float) -> float:
        return qty * price


class SpecialPriceRule(PriceRuleInterface):

    DISCOUNT = 0.2

    QUANTITY_THRESHOLD = 3

    DISCOUNT_TOP = 0.5

    @staticmethod
    def is_applicable(sku: str):
        return sku[:2].upper() == "SP"

    @staticmethod
    def calculate_total(qty: float, price: float) -> float:

        if(qty < SpecialPriceRule.QUANTITY_THRESHOLD):
            return qty * price

        total_discount = qty // SpecialPriceRule.QUANTITY_THRESHOLD

        if total_discount > SpecialPriceRule.DISCOUNT_TOP:
            return qty * price * (1 - SpecialPriceRule.DISCOUNT_TOP)

        return qty * price * (1 - SpecialPriceRule.DISCOUNT)
