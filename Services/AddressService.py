from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from Models.Address import Address
from Models.AddressSchema import AddressSchema
from flask import Blueprint
import MySQLdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:zaq12345@localhost/sys'
db = SQLAlchemy(app)
ma = Marshmallow(app)

address_service = Blueprint('address_service', __name__)

address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)


@address_service.route("/address", methods=["GET"])
def addresses_list():
    all_addresses = Address.query.all()
    result = addresses_schema.dump(all_addresses)
    return jsonify(result.data)


@address_service.route("/address", methods=["POST"])
def add_address():
    json = request.get_json()
    country = json['country']
    city = json['city']
    street = json['street']
    street_details = json['street_details']
    app_no = json['apartament_no']

    try:
        new_address = Address(country, city, street, street_details, app_no)
        db.session.add(new_address)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return jsonify(new_address), 200


@address_service.route('/address/<id>', methods=['PUT'])
def update_address(id):
    address = Address.query.filter(Address.ID == id).first()
    if address is None:
        return abort(404)

    json = request.get_json()
    address.country = json['country']
    address.city = json['city']
    address.street = json['street']
    address.street_details = json['street_details']
    address.app_no = json['apartament_no']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return address_schema.jsonify(address), 200


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

    return address_schema.jsonify(address)


if __name__ == '__main__':
    app.run(debug=True)
