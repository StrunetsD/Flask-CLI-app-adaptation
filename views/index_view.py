from flask import Blueprint, render_template

from utils.utils_data import json_utils, menu_data

index_bp = Blueprint('index', __name__)


@index_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html',
                           clients=json_utils.clients,
                           orders=list(json_utils.pizzeria.orders.values()),
                           menu=menu_data['pizzas'])
