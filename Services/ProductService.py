from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from Models.Product import Product
from Models.Producent import Producent
from Models.Address import Address
from Models.Category import Category
from Models.Vat import Vat
from flask import Blueprint

import MySQLdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:zaq12345@localhost/sys'
db = SQLAlchemy(app)
db.autocommit = False
ma = Marshmallow(app)

product_service = Blueprint('product_service', __name__)


@product_service.route("/product", methods=["GET"])
def product_list():
    all_products = Product.query.all()
    return jsonify([e.serialize() for e in all_products])


@product_service.route("/product", methods=["POST"])
def add_product():

    json = request.get_json()
    name = json['name']
    code = json['code']
    ean = json['ean']
    description = None
    if 'description' in json:
        description = json['description']
    price = json['price']
    producent_id = json['producentID']
    category_id = json['categoryID']
    vat_id = json['VatID']

    try:
        new_product = Product(name, code, ean, description, price, producent_id, category_id, vat_id)
        db.session.add(new_product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return jsonify(new_product.serialize()), 201


@product_service.route('/product/<code>', methods=['GET'])
def get_product(code):
    product = Product.query.filter(Product.Code == code).first()

    if product is None:
        return abort(404)

    product.Producent = Producent.query.filter(Producent.ID == product.ProducentID).first()
    if product.Producent.AddressID is not None:
        product.Producent = Address.query.filter(Address.ID == product.AddressID).first()

    product.Category = Category.query.filter(Category.ID == product.CategoryID).first()
    product.Vat = Vat.query.filter(Vat.ID == product.VatID).first()

    return jsonify(product.serialize()), 200


@product_service.route('/product/<code>', methods=['PUT'])
def update_product(code):
    product = Product.query.filter(Product.Code == code).first()
    if product is None:
        return abort(404)

    json = request.get_json()
    if 'name' in json:
        product.Name = json['name']
    if 'code' in json:
        product.Code = json['code']
    if 'ean' in json:
        product.EAN = json['ean']
    if 'description' in json:
        product.Description = json['description']
    if 'price' in json:
        product.Price = json['price']
    if 'producentID' in json:
        product.ProducentID = json['producentID']
    if 'categoryID' in json:
        product.CategoryID = json['categoryID']
    if 'vatID' in json:
        product.VATID = json['vatID']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return jsonify(product.serialize()), 200


@product_service.route('/product/<code>', methods=['DELETE'])
def delete_product(code):
    product = Product.query.filter(Product.Code == code).first()
    if product is None:
        return abort(404)

    try:
        db.session.delete(product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return jsonify(code=200, text="OK")


if __name__ == '__main__':
    app.run(debug=True)
