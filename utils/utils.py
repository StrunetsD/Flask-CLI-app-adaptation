import json
from typing import Any, Dict, Optional

from models.chef import Chef
from models.client import Client
from models.courier import Courier
from models.order import *
from models.pizzeria import Pizzeria
import os



class JsonUtils:
    def __init__(self) -> None:
        self.pizzeria: Pizzeria = Pizzeria()
        self.clients: List[Client] = []
        self.chefs: List[Chef] = []
        self.couriers: List[Courier] = []
        self.menu: List = []
        self.current_order: Optional[Order] = None

    def load_menu(self):
        with open('data/menu.json', 'r') as f:
            return json.load(f)

    def load_data(self) -> None:
        try:
            with open("data/data.json", "r") as f:
                data: Dict[str, Any] = json.load(f)

                state_classes: Dict[str, Any] = {
                    'NewOrder': NewOrder,
                    'CookedOrder': CookedOrder,
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
                        order.price = order_data.get("price", 0.0)
                        self.pizzeria.orders[order.order_id] = order

                self.pizzeria.total_income = data["finances"]["income"]
                self.pizzeria.next_order_id = data.get("last_order_id", 0) + 1

            print("Данные загружены!")
        except FileNotFoundError:
            print("Файл данных не найден. Будет создан новый файл.")
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")

    def save_data(self) -> None:
        try:
            new_data: Dict[str, Any] = {
                "clients": [
                    {"name": client.name, "address": client.address, "phone": client.phone_num}
                    for client in self.clients
                ],
                "chefs": [{"name": chef.name} for chef in self.chefs],
                "couriers": [
                    {"name": courier.name, "transport": courier.transport}
                    for courier in self.couriers
                ],
                "orders": [
                    {
                        "order_id": order.order_id,
                        "client": order.client.name,
                        "items": list(order.items),
                        "price": order.price,
                        "state": order.state.__class__.__name__
                    }
                    for order in self.pizzeria.orders.values()
                ],
                "finances": {
                    "income": self.pizzeria.total_income,
                },
                "last_order_id": self.pizzeria.next_order_id
            }

            with open("data/data.json", "w") as f:
                json.dump(new_data, f, indent=4, ensure_ascii=False)

            print("Данные сохранены!")
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
            raise
