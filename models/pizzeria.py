import json
from typing import List, Dict, Any

from accounting import Accounting
from client import Client
from order import Order


class Pizzeria:
    def __init__(self) -> None:
        self._orders: Dict[int, Order] = {}
        self._accounting: Accounting = Accounting()
        self._next_order_id: int = 1
        self._menu: Dict[str, float] = {}

    @property
    def menu(self) -> Dict[str, float]:
        return self._menu

    @menu.setter
    def menu(self, value: Dict[str, float]) -> None:
        if not isinstance(value, dict):
            raise ValueError("Menu должно быть словарем.")

        for item, price in value.items():
            if not isinstance(item, str) or not isinstance(price, (int, float)):
                raise ValueError("Ключи должны быть строками, а значения — числами.")

        self._menu = value

    @property
    def accounting(self) -> Accounting:
        return self._accounting

    @property
    def orders(self) -> Dict[int, Order]:
        return self._orders

    @property
    def next_order_id(self) -> int:
        return self._next_order_id

    @next_order_id.setter
    def next_order_id(self, value: int) -> None:
        self._next_order_id = value

    @property
    def total_income(self) -> float:
        return self._accounting.income

    @total_income.setter
    def total_income(self, value: float) -> None:
        self._accounting.income = value

    def update_income(self, income_data: Dict[str, float]) -> None:
        if "income" in income_data:
            self._accounting.add_income(income_data["income"])
        else:
            print("Ключ 'income' не найден в данных.")

    def load_menu(self) -> None:
        with open('menu.json', 'r', encoding='utf-8') as file:
            menu_items: List[Dict[str, Any]] = json.load(file)
            self.menu = {item['name']: item['price'] for item in menu_items}

    def accept_order(self, client: Client) -> Order:
        if not self.menu:
            self.load_menu()

        print("Меню:")
        menu_items: List[str] = list(self.menu.keys())
        for idx, item in enumerate(menu_items, 1):
            print(f"{idx}. {item} - {self.menu[item]} руб.")

        selected_items: List[str] = []
        while True:
            choice: str = input("Введите номер пиццы (или 'done' для завершения): ")

            if choice.lower() == 'done':
                if not selected_items:
                    print("Вы не выбрали ни одной пиццы. Пожалуйста, выберите хотя бы одну.")
                    continue
                break

            try:
                index: int = int(choice) - 1
                if index < 0 or index >= len(menu_items):
                    raise ValueError("Неверный номер пиццы.")
                selected_items.append(menu_items[index])
            except ValueError as e:
                print(f"Ошибка: {e}")

        order: Order = Order(self.next_order_id, client, selected_items)
        order.price = sum(self.menu[item] for item in selected_items)
        self.orders[order.order_id] = order
        self.next_order_id += 1
        self.accounting.add_income(order.price)
        return order

    def serve_customer(self, client: Client) -> None:
        order: Order = self.accept_order(client)
        client.create_order(order)
