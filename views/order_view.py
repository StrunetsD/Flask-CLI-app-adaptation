from flask import Blueprint, render_template, request

from models.order import Order
from utils.utils_data import json_utils, menu_data

order_bp = Blueprint('orders', __name__)



@order_bp.route('/orders', methods=['GET', 'POST'])
def create_order():
    clients = json_utils.clients
    error = None
    try:
        if request.method == 'POST':
            if not json_utils.chefs:
                raise ValueError("Извините, сейчас нет свободных поваров. Заказ невозможен.")
            if not json_utils.couriers:
                raise ValueError("Извините, сейчас нет свободных курьеров. Заказ невозможен.")

            client_name = request.form.get('client_name', '').strip()
            selected_items = [item.strip() for item in request.form.getlist('items') if item.strip()]

            if not selected_items:
                raise ValueError("Выберите хотя бы одну пиццу.")

            client = next((c for c in clients if c.name == client_name), None)
            if not client:
                raise ValueError(f"Клиент '{client_name}' не найден.")

            total_price = sum(pizza['price'] for pizza in menu_data['pizzas'] if pizza['name'] in selected_items)

            new_order = Order(
                order_id=json_utils.pizzeria.next_order_id,
                client=client,
                items=selected_items
            )
            new_order.price = total_price

            json_utils.pizzeria.orders[new_order.order_id] = new_order
            json_utils.pizzeria.next_order_id += 1
            json_utils.save_data()

        orders_data = [
            {
                "id": order.order_id,
                "client": order.client.name,
                "items": ", ".join(order.items),
                "state": str(order.state),
            }
            for order in json_utils.pizzeria.orders.values()
        ]

        return render_template(
            'orders.html',
            clients=clients,
            pizzas=menu_data['pizzas'],
            orders=orders_data,
            error=error
        )

    except Exception as e:
        error = f"Ошибка: {str(e)}"
        return render_template(
            'orders.html',
            clients=clients,
            pizzas=menu_data.get('pizzas'),
            orders=[],
            error=error
        )
