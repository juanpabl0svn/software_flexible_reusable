from abc import ABC, abstractmethod
from ..models.request import Request
from ..models.response import Response



class Controller(ABC):
    @abstractmethod
    def handle(self, request: Request) -> Response:
        pass
    
    @abstractmethod
    def match(self, request: str, path: str) -> callable:
        pass