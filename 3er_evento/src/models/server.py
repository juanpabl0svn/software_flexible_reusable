
from typing import Optional
from ..interface.request_handler import RequestHandler
from .request import Request
from .response import Response
from ..controllers.order import OrderController



class Server:

    middlewares: list[RequestHandler]

    controller: RequestHandler

    def __init__(self):
        self.middlewares = []
        self.controller = OrderController()

    def add_middleware(self, middleware: RequestHandler):
        if self.middlewares:
            self.middlewares[-1].set_next(middleware)
        self.middlewares.append(middleware)

    def execute_middleware_chain(self, request: Request) -> Optional[Response]:
        if not self.middlewares:
            return None
        head = self.middlewares[0]
        return head.handle(request)

    def handle_request(self, request: Request) -> Optional[Response]:
        return self.controller.handle(request)

    def process_request(self, request: Request) -> Response:

      if not self.middlewares:
          return self.handle_request(request)
      # Siempre el controlador se ejecuta al final
      self.middlewares[-1].set_next(self.controller)
      return self.execute_middleware_chain(request)

