from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from Services.CategoryService import cat_service
from Services.VatService import vat_service
from Services.AddressService import address_service
from Services.ProducentService import producent_service

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:zaq12345@localhost/sys'
db = SQLAlchemy(app)
ma = Marshmallow(app)

app.register_blueprint(cat_service)
app.register_blueprint(vat_service)
app.register_blueprint(address_service)
app.register_blueprint(producent_service)


@app.route("/")
def hello():
    return "Hello World!"


@app.errorhandler(404)
def not_found(error):
    return jsonify(error=404, text=str(error)), 404


if __name__ == '__main__':
    app.run(debug=True)
