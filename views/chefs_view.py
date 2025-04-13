from flask import Blueprint, render_template, request

from models.chef import Chef
from utils.utils_data import json_utils
chef_bp = Blueprint('chefs', __name__)


@chef_bp.route('/chefs', methods=['GET', 'POST'])
def create_chef():
    try:
        if request.method == 'POST':
            chef_name = request.form.get('name', '').strip()
            if not chef_name.isalpha():
                raise ValueError("Имя повара должно содержать только буквы.")
            if not chef_name:
                raise ValueError("Имя повара не может быть пустым.")

            new_chef = Chef()
            new_chef.name = chef_name
            json_utils.chefs.append(new_chef)
            json_utils.save_data()

        chef_data = [{"name": chef.name} for chef in json_utils.chefs]
        return render_template('chefs.html', chefs=chef_data)

    except Exception as e:
        chef_data = [{"name": chef.name} for chef in json_utils.chefs]
        return render_template('chefs.html', chefs=chef_data, error=str(e))
