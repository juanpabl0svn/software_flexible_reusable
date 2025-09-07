
from dataclasses import dataclass
from datetime import datetime
from ..enum.order import OrderStatus


@dataclass
class Order:
    id: str
    user_id: str
    items: list
    total: float
    created_at: datetime
    status: OrderStatus = OrderStatus.PENDING

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "items": self.items,
            "total": self.total,
            "status": self.status.value,
            "created_at": self.created_at.isoformat()
        }
