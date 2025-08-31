from src.interfaces.product_rule_interface import IProductRule


class RegularProductRule(IProductRule):
    @staticmethod
    def is_applicable(sku: str):
        return sku[:2].upper() == "EA"

    @staticmethod
    def calculate_total(qty: float, price: float) -> float:
        qty = int(qty)
        return qty * price
    
    @staticmethod
    def get_qty(qty: float) -> float | int:
        return int(qty)


class WeightBasedProductRule(IProductRule):
    @staticmethod
    def is_applicable(sku: str):
        return sku[:2].upper() == "WE"

    @staticmethod
    def calculate_total(qty: float, price: float) -> float:
        return qty * price

    @staticmethod
    def get_qty(qty: float) -> float | int:
        return qty


class SpecialProductRule(IProductRule):

    DISCOUNT = 0.2

    QUANTITY_THRESHOLD = 3

    DISCOUNT_TOP = 0.5

    @staticmethod
    def is_applicable(sku: str):
        return sku[:2].upper() == "SP"

    @staticmethod
    def get_qty(qty: float) -> float | int:
        return int(qty)

    @staticmethod
    def calculate_total(qty: float, price: float) -> float:
        qty = int(qty)  

        if(qty < SpecialProductRule.QUANTITY_THRESHOLD):
            return qty * price

        amount_buyed_to_discount = qty // SpecialProductRule.QUANTITY_THRESHOLD

        total_discount = amount_buyed_to_discount * SpecialProductRule.DISCOUNT

        if total_discount > SpecialProductRule.DISCOUNT_TOP:
            return qty * price * (1 - SpecialProductRule.DISCOUNT_TOP)

        return qty * price * (1 - total_discount)
