from abc import ABC, abstractmethod


class IPriceRule(ABC):

    @abstractmethod
    def is_applicable(self, sku: str):
        pass

    @abstractmethod
    def calculate_total(self, qty: float, price: float) -> float:
        pass