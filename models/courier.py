from order import Order, CookedOrder, DeliveringOrder
from user import User


class Courier(User):
    def __init__(self) -> None:
        super().__init__(User.Role.COURIER)
        self._transport: str = ""

    @property
    def transport(self) -> str:
        return self._transport

    @transport.setter
    def transport(self, value: str) -> None:
        self._transport = value

    def deliver_order(self, order: Order) -> None:
        if not isinstance(order.state, CookedOrder):
            print("Заказ еще не готов к доставке")
            return

        order.deliver()
        if isinstance(order.state, DeliveringOrder):
            order.complete()
        print(f"Order #{order.order_id} delivered")
