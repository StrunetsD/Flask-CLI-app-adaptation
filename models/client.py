from typing import List

from order import Order
from user import User


class Client(User):
    def __init__(self, address: str) -> None:
        super().__init__(User.Role.CLIENT)
        self._address: str = address
        self._orders: List[Order] = []

    @property
    def address(self) -> str:
        return self._address

    def create_order(self, order: Order) -> None:
        self._orders.append(order)
        print(f"Order #{order.order_id} created")
