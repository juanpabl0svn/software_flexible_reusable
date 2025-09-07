from abc import ABC, abstractmethod
from typing import Optional
from ..models import Request, Response


class RequestHandler(ABC):
    
    def __init__(self):
        self._next_handler: Optional['RequestHandler'] = None
    
    def set_next(self, handler: 'RequestHandler') -> 'RequestHandler':
        self._next_handler = handler
        return handler
    
    @abstractmethod
    def handle(self, request: Request) -> Optional[Response]:
        pass
    
    def _pass_to_next(self, request: Request) -> Optional[Response]:
        if self._next_handler:
            return self._next_handler.handle(request)
        return 
