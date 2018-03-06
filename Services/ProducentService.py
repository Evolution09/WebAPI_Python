from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from Models.Producent import Producent
from Models.Address import Address
from Models.ProducentSchema import ProducentSchema
from flask import Blueprint

import MySQLdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:zaq12345@localhost/sys'
db = SQLAlchemy(app)
db.autocommit = False
ma = Marshmallow(app)

producent_service = Blueprint('producent_service', __name__)

producent_schema = ProducentSchema()
producents_schema = ProducentSchema(many=True)


@producent_service.route("/producent", methods=["GET"])
def producent_list():
    all_producents = Producent.query.all()
    result = producents_schema.dump(all_producents)
    return jsonify(result.data)


@producent_service.route("/producent", methods=["POST"])
def add_producent():

    json = request.get_json()
    name = json['name']
    code = json['code']
    tel = json['telephone']
    email = json['email']

    country = json['country']
    city = json['city']
    street = json['street']
    street_details = json['street_details']
    apart_no = json['apartament_no']

    try:
        new_address = Address(country, city, street, street_details, apart_no)
        db.session.add(new_address)
        db.session.flush()

        address = Address.query.filter(Address.ID == id).first()

        #new_producent = Producent(name, code, tel, email, )
        #db.session.add(new_producent)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return jsonify(new_address), 200


@producent_service.route('/producent/<code>', methods=['GET'])
def get_producent(code):
    producent = Producent.query.filter(Producent.Code == code).first()
    if producent is None:
        return abort(404)
    return producent_schema.jsonify(producent), 200


@producent_service.route('/producent/<code>', methods=['PUT'])
def update_producent(code):
    producent = Producent.query.filter(Producent.Code == code).first()
    if producent is None:
        return abort(404)

    json = request.get_json()
    producent.name = json['name']
    producent.code = json['code']
    producent.tel = json['telephone']
    producent.email = json['email']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return producent_schema.jsonify(producent), 200


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

    return producent_schema.jsonify(producent)


if __name__ == '__main__':
    app.run(debug=True)
