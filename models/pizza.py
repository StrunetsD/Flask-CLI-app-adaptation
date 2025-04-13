from typing import List

from bake import Bake
from dough import Dough
from topping import Topping


class Pizza:
    def __init__(
            self,
            toppings: List[Topping],
            dough: Dough,
            bake: Bake,
            name: str,
            price: float
    ) -> None:
        self._name_to_pizza: str = name
        self._price: float = price
        self._toppings: List[Topping] = toppings
        self._dough: Dough = dough
        self._bake: Bake = bake

    @property
    def toppings(self) -> List[Topping]:
        return self._toppings

    @property
    def dough(self) -> Dough:
        return self._dough

    def __str__(self) -> str:
        return f"Pizza with {len(self.toppings)} toppings"
