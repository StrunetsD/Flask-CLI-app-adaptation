class Topping:
    def __init__(self, name: str) -> None:
        if not name:
            raise ValueError("Topping name required")
        self._name: str = name

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self.name
