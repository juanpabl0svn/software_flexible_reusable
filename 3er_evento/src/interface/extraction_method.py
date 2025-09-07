from abc import ABC, abstractmethod
from typing import Optional

class ExtractionMethod(ABC):
    @abstractmethod
    def extract(self, request) -> Optional[dict]:
        pass