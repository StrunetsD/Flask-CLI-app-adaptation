from enum import Enum


class Dough:
    class TypeOfDough(Enum):
        THICK = 'thick'
        THIN = 'thin'

    def __init__(self, dough_type: TypeOfDough) -> None:
        if not isinstance(dough_type, self.TypeOfDough):
            raise ValueError("Invalid dough type")
        self._dough_type: Dough.TypeOfDough = dough_type

    @property
    def dough_type(self) -> TypeOfDough:
        return self._dough_type

    def prepare(self) -> None:
        print(f"Preparing {self.dough_type.value} dough")

    def __str__(self) -> str:
        return self.dough_type.value
