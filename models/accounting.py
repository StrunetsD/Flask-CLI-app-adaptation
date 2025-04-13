class Accounting:
    def __init__(self) -> None:
        self._income: float = 0.0

    def add_income(self, amount: float) -> None:
        self._income += amount

    @property
    def income(self) -> float:
        return self._income

    @income.setter
    def income(self, amount: float) -> None:
        self._income = amount

    @property
    def profit(self) -> float:
        return self._income
