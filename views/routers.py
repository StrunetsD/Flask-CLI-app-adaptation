from flask import Flask
from views.chefs_view import chef_bp
from views.order_view import order_bp
from views.couriers_view import courier_bp
from views.clients_view import client_bp
from views.delivery_view import delivery_bp
from views.finances_view import finance_bp
from views.index_view import index_bp
from views.kitchen_view import kitchen_bp


app = Flask(__name__,template_folder="../templates", static_folder="../static")
app.register_blueprint(index_bp)
app.register_blueprint(chef_bp)
app.register_blueprint(courier_bp)
app.register_blueprint(client_bp)
app.register_blueprint(order_bp)
app.register_blueprint(delivery_bp)
app.register_blueprint(finance_bp)
app.register_blueprint(kitchen_bp)

if __name__ == '__main__':
    app.run(debug=True)