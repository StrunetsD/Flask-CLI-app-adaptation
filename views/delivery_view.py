from flask import Blueprint, render_template, request

from models.order import *
from utils.utils_data import json_utils
delivery_bp = Blueprint('delivery', __name__)


@delivery_bp.route('/delivery', methods=['GET', 'POST'])
def delivery():

    if request.method == 'POST':
        order_id = int(request.form.get('order_id'))
        action = request.form.get('action')
        order = json_utils.pizzeria.orders.get(order_id)

        if order:
            if action == "start_delivery" and isinstance(order.state, CookedOrder):
                order.deliver()
                json_utils.save_data()
            elif action == "complete_delivery" and isinstance(order.state, DeliveringOrder):
                json_utils.pizzeria.total_income += order.price
                order.complete()
                json_utils.save_data()

    cooking_orders = [order for order in json_utils.pizzeria.orders.values() if isinstance(order.state, CookedOrder)]
    delivering_orders = [order for order in json_utils.pizzeria.orders.values() if
                         isinstance(order.state, DeliveringOrder)]

    return render_template('delivery.html', cooking_orders=cooking_orders, delivering_orders=delivering_orders)
