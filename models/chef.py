from typing import List, Optional

from bake import Bake
from dough import Dough
from order import Order, NewOrder
from pizza import Pizza
from topping import Topping
from user import User


class Chef(User):
    def __init__(self) -> None:
        super().__init__(User.Role.KITCHENER)
        self._toppings: List[Topping] = []
        self._dough: Optional[Dough] = None
        self._bake: Optional[Bake] = None

    @property
    def toppings(self) -> List[Topping]:
        return self._toppings

    @toppings.setter
    def toppings(self, value: List[Topping]) -> None:
        self._toppings = value

    @property
    def dough(self) -> Optional[Dough]:
        return self._dough

    @dough.setter
    def dough(self, value: Optional[Dough]) -> None:
        self._dough = value

    @property
    def bake(self) -> Optional[Bake]:
        return self._bake

    @bake.setter
    def bake(self, value: Optional[Bake]) -> None:
        self._bake = value

    def prepare_pizza(self, order: Order) -> Pizza:
        if not isinstance(order.state, NewOrder):
            raise ValueError("Заказ не в состоянии для приготовления")

        if not self.dough or not self.toppings or not self.bake:
            raise ValueError("Не хватает ингредиентов для приготовления")

        pizza = Pizza(
            self.toppings,
            self.dough,
            self.bake,
            name=order.items[0],
            price=order.price
        )
        order.prepare()
        return pizza
