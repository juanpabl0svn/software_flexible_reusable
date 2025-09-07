from typing import Optional
from datetime import datetime
import uuid
from ..models.request import Request
from ..models.response import Response
from ..models.order import Order
from ..enum.status_code import StatusCode
from ..interface.request_handler import RequestHandler


class OrderService():

    def __init__(self):
        self.orders_db = [
            Order(id="1", user_id="user1", items=[
                  "item1", "item2"], total=100.0, created_at=datetime.now()),
            Order(id="2", user_id="user2", items=[
                  "item3"], total=50.0, created_at=datetime.now()),
            Order(id="3", user_id="user1", items=[
                  "item4", "item5"], total=150.0, created_at=datetime.now()),
        ]

    def _create_order(self, request: Request, items: list, total: float) -> Response:
        user = request.authenticated_user

        if not items or not total:
            return Response(
                status_code=StatusCode.BAD_REQUEST,
                headers={},
                body={"error": "Items y total son requeridos",
                      "code": "MISSING_DATA"}
            )

        order_id = str(uuid.uuid4())
        order = Order(
            id=order_id,
            user_id=user.username,
            items=items,
            total=total,
            created_at=datetime.now(),
        )

        self.orders_db.append(order)

        return Response(
            status_code=StatusCode.CREATED,
            headers={"Location": f"/orders/{order_id}"},
            body={
                "message": "Orden creada exitosamente",
                "order": order.to_json()
            }
        )

    def _get_orders(self, request: Request) -> Response:

        user = request.authenticated_user

        if user.is_admin:
            user_orders = list(self.orders_db)
        else:
            user_orders = [order for order in self.orders_db if order.user_id == user.username]

        orders_data = []
        for order in user_orders:
            orders_data.append({
                "id": order.id,
                "user_id": order.user_id,
                "items": order.items,
                "total": order.total,
                "status": order.status,
                "created_at": order.created_at.isoformat()
            })


        return Response(
            status_code=StatusCode.OK,
            headers={},
            body={"orders": orders_data, "count": len(orders_data)}
        )

    def _get_order(self, request: Request, order_id: str) -> Response:
        user = request.authenticated_user

        if order_id not in [order.id for order in self.orders_db]:
            return Response(
                status_code=StatusCode.NOT_FOUND,
                headers={},
                body={"error": "Orden no encontrada",
                      "code": StatusCode.NOT_FOUND}
            )

        order = next(order for order in self.orders_db if order.id == order_id)

        if not user.is_admin and order.user_id != user.username:
            return Response(
                status_code=StatusCode.FORBIDDEN,
                headers={},
                body={"error": "No tiene permisos para ver esta orden",
                      "code": StatusCode.FORBIDDEN}
            )

        return Response(
            status_code=StatusCode.OK,
            headers={},
            body={
                "order": {
                    "id": order.id,
                    "user_id": order.user_id,
                    "items": order.items,
                    "total": order.total,
                    "status": order.status,
                    "created_at": order.created_at.isoformat()
                }
            }
        )

    def _delete_order(self, request: Request, order_id: str) -> Response:
        user = request.authenticated_user

        if not user.is_admin:
            return Response(
                status_code=StatusCode.FORBIDDEN,
                headers={},
                body={"error": "Solo administradores pueden eliminar órdenes",
                      "code": StatusCode.FORBIDDEN}
            )

        if order_id not in [order.id for order in self.orders_db]:
            return Response(
                status_code=StatusCode.NOT_FOUND,
                headers={},
                body={"error": "Orden no encontrada",
                      "code": StatusCode.NOT_FOUND}
            )

        self.orders_db = [order for order in self.orders_db if order.id != order_id]

        return Response(
            status_code=StatusCode.OK,
            headers={},
            body={"message": "Orden eliminada exitosamente"}
        )
