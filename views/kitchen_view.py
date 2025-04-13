from flask import Blueprint, render_template, request

from models.order import *
from utils.utils_data import json_utils
kitchen_bp = Blueprint('kitchen', __name__)


@kitchen_bp.route('/kitchen', methods=['GET', 'POST'])
def kitchen():

    if request.method == 'POST':
        order_id = int(request.form.get('order_id'))
        order = json_utils.pizzeria.orders.get(order_id)

        if order and isinstance(order.state, NewOrder):
            order.prepare()
            json_utils.save_data()

    new_orders = [order for order in json_utils.pizzeria.orders.values() if isinstance(order.state, NewOrder)]
    return render_template('kitchen.html', orders=new_orders)
