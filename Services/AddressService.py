from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from Models.Address import Address
from flask import Blueprint
import MySQLdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:zaq12345@localhost/sys'
db = SQLAlchemy(app)
ma = Marshmallow(app)

address_service = Blueprint('address_service', __name__)


@address_service.route("/address", methods=["GET"])
def addresses_list():
    all_addresses = Address.query.all()
    return jsonify([e.serialize() for e in all_addresses])


@address_service.route("/address", methods=["POST"])
def add_address():
    json = request.get_json()
    country = json['country']
    city = json['city']
    street = json['street']
    street_details = app_no = None
    if 'street_details' in json:
        street_details = json['street_details']
    if 'apartament_no' in json:
        app_no = json['apartament_no']

    try:
        new_address = Address(country, city, street, street_details, app_no)
        db.session.add(new_address)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return jsonify(new_address.serialize()), 201


@address_service.route('/address/<id>', methods=['PUT'])
def update_address(id):
    address = Address.query.filter(Address.ID == id).first()
    if address is None:
        return abort(404)

    json = request.get_json()
    if 'country' in json:
        address.country = json['country']
    if 'city' in json:
        address.city = json['city']
    if 'street' in json:
        address.street = json['street']
    if 'street_details' in json:
        address.street_details = json['street_details']
    if 'apartament_no' in json:
        address.app_no = json['apartament_no']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return jsonify(address.serialize()), 200


@address_service.route('/address/<id>', methods=['DELETE'])
def delete_address(id):
    address = Address.query.filter(Address.ID == id).first()
    if address is None:
        return abort(404)

    try:
        db.session.delete(address)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return jsonify(code=200, text="OK")


if __name__ == '__main__':
    app.run(debug=True)
