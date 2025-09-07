from typing import Optional
from ..models.request import Request
from ..models.response import Response
from ..enum.status_code import StatusCode
from ..services.order_service import OrderService
from ..interface.controller import Controller


class OrderController(Controller):
    order_service: OrderService

    def __init__(self):
        super().__init__()
        self.order_service = OrderService()

    def match(self, request: str, path: str) -> callable:
        if request == "POST" and path == "/orders":
            return self.order_service._create_order
        elif request == "GET" and path == "/orders":
            return self.order_service._get_orders
        elif request == "GET" and path.startswith("/orders/"):
            return self.order_service._get_order
        elif request == "DELETE" and path.startswith("/orders/"):
            return lambda: self.order_service._delete_order
        else:
            return None

    def handle(self, request: Request) -> Optional[Response]:

        request_method = request.method.upper()

        path = request.path

        try:
            if request_method == "POST" and path == "/orders":
                items = request.body.get("items", [])
                total = request.body.get("total", 0.0)
                return self.order_service._create_order(request, items, total)
            
            elif request_method == "GET" and path == "/orders":
                return self.order_service._get_orders(request)
            
            elif request_method == "GET" and path.startswith("/orders/"):
                order_id = path.split("/")[-1]
                return self.order_service._get_order(request, order_id)
            
            elif request_method == "DELETE" and path.startswith("/orders/"):
                # Extract order ID from path
                order_id = path.split("/")[-1]
                return self.order_service._delete_order(request, order_id)
            
            return Response(
                status_code=StatusCode.NOT_FOUND,
                headers={},
                body={"error": "Endpoint no encontrado",
                      "code": StatusCode.NOT_FOUND}
            )

        except Exception as e:
            return Response(
                status_code=StatusCode.SERVER_ERROR,
                headers={},
                body={"error": "Error interno del servidor",
                      "code": StatusCode.SERVER_ERROR}
            )
