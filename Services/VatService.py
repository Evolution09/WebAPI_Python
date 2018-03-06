from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from Models.Vat import Vat
from Models.VatSchema import VatSchema
from flask import Blueprint

import MySQLdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:zaq12345@localhost/sys'
db = SQLAlchemy(app)
ma = Marshmallow(app)

vat_service = Blueprint('vat_service', __name__)

vat_schema = VatSchema()
vats_schema = VatSchema(many=True)


@vat_service.route("/vat", methods=["GET"])
def vats_list():
    all_vats = Vat.query.all()
    result = vats_schema.dump(all_vats)
    return jsonify(result.data)


@vat_service.route("/vat", methods=["POST"])
def add_vat():
    json = request.get_json()
    name = json['name']
    code = json['code']
    val = json['value']

    try:
        new_vat = Vat(name, code, val)
        db.session.add(new_vat)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return jsonify(new_vat), 200


@vat_service.route('/vat/<code>', methods=['GET'])
def get_vat(code):
    vat = Vat.query.filter(Vat.Code == code).first()
    if vat is None:
        return abort(404)
    return vat_schema.jsonify(vat), 200


@vat_service.route('/vat/<code>', methods=['PUT'])
def update_vat(code):
    vat = Vat.query.filter(Vat.Code == code).first()
    if vat is None:
        return abort(404)

    json = request.get_json()
    vat.Name = json['name']
    vat.Code = json['code']
    vat.Value = json['value']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return vat_schema.jsonify(vat), 200


@vat_service.route('/vat/<code>', methods=['DELETE'])
def delete_vat(code):
    vat = Vat.query.filter(Vat.Code == code).first()
    if vat is None:
        return abort(404)

    try:
        db.session.delete(vat)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return vat_schema.jsonify(vat)


if __name__ == '__main__':
    app.run(debug=True)
