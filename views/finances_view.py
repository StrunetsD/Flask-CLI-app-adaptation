from flask import Blueprint, render_template

from models.order import *
from utils.utils_data import json_utils
finance_bp = Blueprint('finances', __name__)


@finance_bp.route('/finances', methods=['GET'])
def get_finances():

    completed_orders = [
        {
            "id": order.order_id,
            "client": order.client.name,
            "price": order.price,
            "completed_at": order.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for order in json_utils.pizzeria.orders.values()
        if isinstance(order.state, CompletedOrder)
    ]

    total_income = json_utils.pizzeria.total_income
    return render_template('finances.html', total_income=total_income, completed_orders=completed_orders)
