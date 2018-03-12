from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from Models.Producent import Producent
from Models.Product import Product
from Models.Address import Address
from flask import Blueprint

import MySQLdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:zaq12345@localhost/sys'
db = SQLAlchemy(app)
db.autocommit = False
ma = Marshmallow(app)

producent_service = Blueprint('producent_service', __name__)


@producent_service.route("/producent", methods=["GET"])
def producent_list():
    all_producents = Producent.query.all()
    return jsonify([e.serialize() for e in all_producents])


@producent_service.route('/producent/<code>', methods=['GET'])
def get_producent(code):
    producent = Producent.query.filter(Producent.Code == code).first()

    if producent is None:
        return abort(404)

    if producent.AddressID is not None:
        address = Address.query.filter(Address.ID == producent.AddressID).first()
        producent.Address = address

    return jsonify(producent.serialize()), 200


@producent_service.route('/producent/<code>/product', methods=['GET'])
def get_producent_products(code):
    producent = Producent.query.filter(Producent.Code == code).first()
    if producent is None:
        return abort(404)

    prods = Product.query.filter(Product.ProducentID == producent.ID).all()
    return jsonify([e.serialize() for e in prods])


@producent_service.route("/producent", methods=["POST"])
def add_producent():

    json = request.get_json()
    name = json['name']
    code = json['code']
    tel = None
    if 'telephone' in json:
        tel = json['telephone']
    email = None
    if 'email' in json:
        email = json['email']

    country = json['address']['country']
    city = json['address']['city']
    street = json['address']['street']
    street_details = None
    if 'address' in json and 'street_details' in json['address']:
        street_details = json['address']['street_details']
    apart_no = None
    if 'address' in json and 'apartament_no' in json['address']:
        apart_no = json['address']['apartament_no']

    try:
        new_address = Address(country, city, street, street_details, apart_no)
        db.session.add(new_address)
        db.session.flush()

        db.session.refresh(new_address)

        new_producent = Producent(name, code, tel, email, new_address.ID)
        db.session.add(new_producent)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return jsonify(new_producent.serialize()), 201


@producent_service.route('/producent/<code>', methods=['PUT'])
def update_producent(code):
    producent = Producent.query.filter(Producent.Code == code).first()
    if producent is None:
        return abort(404)

    json = request.get_json()
    if 'name' in json:
        producent.name = json['name']
    if 'code' in json:
        producent.code = json['code']
    if 'telephone' in json:
        producent.tel = json['telephone']
    if 'email' in json:
        producent.email = json['email']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return jsonify(producent.serialize()), 200


@producent_service.route('/producent/<code>', methods=['DELETE'])
def delete_producent(code):
    producent = Producent.query.filter(Producent.Code == code).first()
    if producent is None:
        return abort(404)

    try:
        db.session.delete(producent)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return jsonify(code=200, text="OK")


if __name__ == '__main__':
    app.run(debug=True)
