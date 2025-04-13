from flask import Blueprint, render_template, request

from models.courier import Courier
from utils.utils_data import json_utils
courier_bp = Blueprint('couriers', __name__)


@courier_bp.route('/couriers', methods=['GET', 'POST'])
def create_courier():

    try:
        if request.method == 'POST':
            courier_name = request.form.get('name', '').strip()
            transport = request.form.get('transport', '').strip()

            if not courier_name.isalpha():
                raise ValueError("Имя курьера должно содержать только буквы.")
            if not courier_name or not transport:
                raise ValueError("Поля 'name' и 'transport' не могут быть пустыми.")
            if not all(c.isalpha() or c.isspace() for c in transport):
                raise ValueError("Поле 'transport' должно содержать только буквы и пробелы.")

            new_courier = Courier()
            new_courier.name = courier_name
            new_courier.transport = transport
            json_utils.couriers.append(new_courier)
            json_utils.save_data()

        courier_data = [{"name": courier.name, "transport": courier.transport} for courier in json_utils.couriers]
        return render_template('couriers.html', couriers=courier_data)

    except Exception as e:
        courier_data = [{"name": courier.name, "transport": courier.transport} for courier in json_utils.couriers]
        return render_template('couriers.html', couriers=courier_data, error=str(e))
