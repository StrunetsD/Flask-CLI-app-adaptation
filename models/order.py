from datetime import datetime
from typing import List


class OrderState:
    def prepare(self, order: 'Order') -> 'OrderState':
        return self

    def deliver(self, order: 'Order') -> 'OrderState':
        return self

    def complete(self, order: 'Order') -> 'OrderState':
        return self

    def __str__(self) -> str:
        return self.__class__.__name__


class NewOrder(OrderState):
    def prepare(self, order: 'Order') -> 'OrderState':
        print(
            f"Заказ #{order.order_id} принят, начинаем готовить: {', '.join(order.items)}")
        return CookedOrder()


class CookedOrder(OrderState):
    def deliver(self, order: 'Order') -> 'OrderState':
        print(f"Пицца {', '.join(order.items)} приготовлена, передаем курьеру")
        return DeliveringOrder()


class DeliveringOrder(OrderState):
    def complete(self, order: 'Order') -> 'OrderState':
        print(
            f"Заказ #{order.order_id} с пиццами {', '.join(order.items)} успешно доставлен")
        return CompletedOrder()


class CompletedOrder(OrderState):
    pass


class Order:
    def __init__(self, order_id: int, client: 'Client', items: List[str]) -> None:
        self.order_id = order_id
        self.client = client
        self.items = items
        self._state: OrderState = NewOrder()
        self.created_at: datetime = datetime.now()
        self.price: float = 0.0

    @property
    def state(self) -> OrderState:
        return self._state

    @state.setter
    def state(self, state: OrderState) -> None:
        self._state = state

    def prepare(self) -> None:
        self._state = self._state.prepare(self)

    def deliver(self) -> None:
        self._state = self._state.deliver(self)

    def complete(self) -> None:
        self._state = self._state.complete(self)

    def get_pizzas(self) -> List[str]:
        return self.items

    def __repr__(self):
        return f"Order(id={self.order_id}, client={self.client.name}, items={self.items})"