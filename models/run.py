import json
from typing import List, Dict, Optional, Any

from bake import Bake
from chef import Chef
from client import Client
from courier import Courier
from dough import Dough
from order import NewOrder, CompletedOrder, CookedOrder, DeliveringOrder
from order import Order
from pizza import Pizza
from pizzeria import Pizzeria
from topping import Topping


class ConsoleApp:
    def __init__(self) -> None:
        self.pizzeria: Pizzeria = Pizzeria()
        self.clients: List[Client] = []
        self.chefs: List[Chef] = []
        self.couriers: List[Courier] = []
        self.current_order: Optional[Order] = None
        self.load_data()

    def save_data(self) -> None:
        try:
            with open("data.json", "r") as f:
                existing_data: Dict[str, Any] = json.load(f)
        except FileNotFoundError:
            existing_data: Dict[str, Any] = {
                "clients": [],
                "chefs": [],
                "couriers": [],
                "orders": [],
                "finances": {"income": 0.0},
                "last_order_id": 0
            }

        new_data: Dict[str, Any] = {
            "clients": [{"name": client.name, "address": client.address, "phone": client.phone_num}
                        for client in self.clients],
            "chefs": [{"name": chef.name} for chef in self.chefs],
            "couriers": [{"name": courier.name, "transport": courier.transport}
                         for courier in self.couriers],
            "orders": [{
                "order_id": order.order_id,
                "client": order.client.name,
                "items": order.items,
                "state": order.state.__class__.__name__
            } for order in self.pizzeria.orders.values()],
            "finances": {
                "income": self.pizzeria.total_income,
            },
            "last_order_id": self.pizzeria.next_order_id
        }

        with open("data.json", "w") as f:
            json.dump(new_data, f, indent=4)
        print("Данные сохранены!")

    def load_data(self) -> None:
        try:
            with open("data.json", "r") as f:
                data: Dict[str, Any] = json.load(f)

                state_classes: Dict[str, Any] = {
                    'NewOrder': NewOrder,
                    'CookingOrder': CookedOrder,
                    'DeliveringOrder': DeliveringOrder,
                    'CompletedOrder': CompletedOrder
                }

                for client_data in data["clients"]:
                    client: Client = Client(client_data["address"])
                    client.name = client_data["name"]
                    client.phone_num = client_data["phone"]
                    self.clients.append(client)

                for chef_data in data["chefs"]:
                    chef: Chef = Chef()
                    chef.name = chef_data["name"]
                    self.chefs.append(chef)

                for courier_data in data["couriers"]:
                    courier: Courier = Courier()
                    courier.name = courier_data["name"]
                    courier.transport = courier_data["transport"]
                    self.couriers.append(courier)

                for order_data in data["orders"]:
                    client: Optional[Client] = next(
                        (c for c in self.clients if c.name ==
                         order_data["client"]),
                        None
                    )
                    if client:
                        order: Order = Order(
                            order_data["order_id"], client, order_data["items"])
                        state_class: Any = state_classes.get(
                            order_data["state"], NewOrder)
                        order.state = state_class()
                        self.pizzeria.orders[order.order_id] = order

                self.pizzeria.update_income(data["finances"])
                self.pizzeria.next_order_id = data.get("last_order_id", 0) + 1

            print("Данные загружены!")
        except FileNotFoundError:
            print("Файл данных не найден. Будет создан новый файл.")
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")

    def run(self) -> None:
        while True:
            print("\n1. Создать клиента")
            print("2. Создать повара")
            print("3. Создать курьера")
            print("4. Сделать заказ")
            print("5. Приготовить пиццу")
            print("6. Доставить заказ")
            print("7. Показать финансы")
            print("8. Выход")

            choice: str = input("Выберите действие: ")

            if choice == "1":
                self.create_client()
            elif choice == "2":
                self.create_kitchener()
            elif choice == "3":
                self.create_courier()
            elif choice == "4":
                self.create_order()
            elif choice == "5":
                self.prepare_pizza()
            elif choice == "6":
                self.deliver_order()
            elif choice == "7":
                self.show_finance()
            elif choice == "8":
                self.save_data()
                break
            else:
                print("Неверный выбор")

    def create_client(self) -> None:
        while True:
            name: str = input("Имя клиента: ").strip()
            if name:
                break
            print("Ошибка: имя клиента не может быть пустым")
        while True:
            address: str = input("Адрес: ")
            if address:
                break
            print("Оишбка: адрес не может быть пустым")

        while True:
            phone: str = input("Номер телефона: ")
            if phone.isdigit() and len(phone) == 8:
                print(f"ok:  {phone}")
                break
            else:
                print("Ошибка: телефон должен содержать только 8 цифр")

        client: Client = Client(address)
        client.name = name
        client.phone_num = phone
        self.clients.append(client)
        self.save_data()
        print(f"Клиент {name} создан")

    def create_kitchener(self) -> None:
        while True:
            name: str = input("Имя повара: ").strip()
            if name:
                break
            print("Ошибка: имя повара не может быть пустым")

        kitchener: Chef = Chef()
        kitchener.name = name
        self.chefs.append(kitchener)
        self.save_data()
        print(f"Повар {name} создан")

    def create_courier(self) -> None:
        while True:
            name: str = input("Имя курьера: ").strip()
            if name:
                break
            print("Ошибка: имя курьера не может быть пустым")
        while True:
            transport: str = input("Транспорт: ")
            if transport:
                break
            print("Ошибка: транспорт не может быть пустым")
        courier: Courier = Courier()
        courier.name = name
        courier.transport = transport
        self.couriers.append(courier)
        self.save_data()
        print(f"Курьер {name} создан")

    def create_order(self) -> None:
        if not self.clients:
            print("Нет клиентов!")
            return

        print("Доступные клиенты:")
        for i, client in enumerate(self.clients, 1):
            print(f"{i}. {client.name}")

        while True:
            choice: str = input("Выберите клиента (введите номер): ")

            if choice.isdigit():
                client_idx: int = int(choice) - 1

                if 0 <= client_idx < len(self.clients):
                    break
                else:
                    print(f"Ошибка: введите число от 1 до {len(self.clients)}")
            else:
                print("Ошибка: введите только цифры.")

        client: Client = self.clients[client_idx]

        self.current_order = self.pizzeria.accept_order(client)
        if self.current_order:
            client.create_order(self.current_order)
            self.current_order.state = NewOrder()
            self.save_data()
            print(f"Заказ #{self.current_order.order_id} создан")

    def prepare_pizza(self) -> None:
        preparing_orders: List[Order] = [
            order for order in self.pizzeria.orders.values()
            if isinstance(order.state, NewOrder)
        ]

        if not preparing_orders:
            print("Нет новых заказов для приготовления!")
            return

        print("Доступные заказы для приготовления:")
        for i, order in enumerate(preparing_orders, 1):
            print(f"{i}. Заказ #{order.order_id} от клиента {order.client.name}")

        try:
            order_idx: int = int(
                input("Выберите номер заказа для приготовления: ")) - 1
            if order_idx < 0 or order_idx >= len(preparing_orders):
                print("Неверный выбор")
                return

            selected_order: Order = preparing_orders[order_idx]

            if not isinstance(selected_order.state, NewOrder):
                print("Заказ уже готовится или готов!")
                return

            chef: Optional[Chef] = self.chefs[0] if self.chefs else None
            if not chef:
                print("Нет доступных поваров!")
                return

            chef.dough = Dough(Dough.TypeOfDough.THIN)
            chef.toppings = [Topping("сыр"), Topping("томаты")]
            chef.bake = Bake(200)

            pizza: Pizza = chef.prepare_pizza(selected_order)
            print(f"Пицца приготовлена: {pizza}")
            self.save_data()
        except ValueError:
            print("Ошибка: введите номер заказа.")
        except Exception as e:
            print(f"Ошибка при приготовлении: {e}")

    def deliver_order(self) -> None:
        delivering_orders: List[Order] = [
            order for order in self.pizzeria.orders.values()
            if isinstance(order.state, CookedOrder)
        ]

        if not delivering_orders:
            print("Нет заказов, готовящихся к доставке!")
            return

        print("Доступные заказы для доставки:")
        for i, order in enumerate(delivering_orders, 1):
            print(f"{i}. Заказ #{order.order_id} от клиента {order.client.name}")

        try:
            order_idx: int = int(
                input("Выберите номер заказа для доставки: ")) - 1
            if order_idx < 0 or order_idx >= len(delivering_orders):
                print("Неверный выбор")
                return

            selected_order: Order = delivering_orders[order_idx]

            courier: Optional[Courier] = self.couriers[0] if self.couriers else None
            if not courier:
                print("Нет доступных курьеров!")
                return

            courier.deliver_order(selected_order)
            self.save_data()
            print(f"Заказ #{selected_order.order_id} доставлен")
        except ValueError:
            print("Ошибка: введите номер заказа.")

    def show_finance(self) -> None:
        profit: float = self.pizzeria.total_income
        print(f"\nТекущая прибыль: {profit} руб.")


if __name__ == "__main__":
    app: ConsoleApp = ConsoleApp()
    app.run()
