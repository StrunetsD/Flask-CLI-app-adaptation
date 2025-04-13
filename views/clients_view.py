import re

from flask import Blueprint, render_template, request

from models.client import Client
from utils.utils_data import json_utils

client_bp = Blueprint('clients', __name__)


@client_bp.route('/clients', methods=['GET', 'POST'])
def create_client():
    try:
        if request.method == 'POST':
            client_name = request.form.get('name', '').strip()
            address = request.form.get('address', '').strip()
            phone = request.form.get('phone', '').strip()

            if not client_name.isalpha():
                raise ValueError("Имя клиента должно содержать только буквы.")
            if not address:
                raise ValueError("Адрес не может быть пустым.")
            if not re.match(r'^\d+$', phone):
                raise ValueError("Номер телефона должен содержать только цифры.")

            new_client = Client(address)
            new_client.name = client_name
            new_client.phone_num = phone

            json_utils.clients.append(new_client)
            json_utils.save_data()

        clients_data = [{"name": client.name, "address": client.address, "phone": client.phone_num} for client in
                        json_utils.clients]
        return render_template('clients.html', clients=clients_data)

    except Exception as e:
        clients_data = [{"name": client.name, "address": client.address, "phone": client.phone_num} for client in
                        json_utils.clients]
        return render_template('clients.html', clients=clients_data, error=str(e))
