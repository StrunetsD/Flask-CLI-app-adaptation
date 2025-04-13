class Bake:
    def __init__(self, temperature: float = 200) -> None:
        if temperature < 0:
            raise ValueError("Invalid temperature")
        self._temperature: float = temperature

    @property
    def temperature(self) -> float:
        return self._temperature

    def __str__(self) -> str:
        return f"Baking at {self.temperature}°C"
