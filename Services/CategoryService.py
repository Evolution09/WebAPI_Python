from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from Models.Category import Category
from Models.Product import Product
from flask import Blueprint

import MySQLdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:zaq12345@localhost/sys'
db = SQLAlchemy(app)
ma = Marshmallow(app)

cat_service = Blueprint('cat_service', __name__)


@cat_service.route("/category", methods=["GET"])
def category_list():
    all_categories = Category.query.all()
    return jsonify([e.serialize() for e in all_categories])


@cat_service.route('/category/<code>', methods=['GET'])
def get_category(code):
    cat = Category.query.filter(Category.Code == code).first()
    if cat is None:
        return abort(404)
    return jsonify(cat.serialize()), 200


@cat_service.route('/category/<code>/product', methods=['GET'])
def get_category_products(code):
    category = Category.query.filter(Category.Code == code).first()
    if category is None:
        return abort(404)

    prods = Product.query.filter(Product.CategoryID == category.ID).all()
    return jsonify([e.serialize() for e in prods])


@cat_service.route("/category", methods=["POST"])
def add_category():

    json = request.get_json()
    name = json['name']
    code = json['code']
    if 'description' in json:
        desc = json['description']

    try:
        new_cat = Category(name, code, desc)
        db.session.add(new_cat)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return jsonify(new_cat.serialize()), 201


@cat_service.route('/category/<code>', methods=['PUT'])
def update_category(code):
    cat = Category.query.filter(Category.Code == code).first()
    if cat is None:
        return abort(404)

    json = request.get_json()
    if 'name' in json:
        cat.Name = json['name']
    if 'code' in json:
        cat.Code = json['code']
    if 'description' in json:
        cat.Description = json['description']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return jsonify(cat.serialize()), 200


@cat_service.route('/category/<code>', methods=['DELETE'])
def delete_category(code):
    cat = Category.query.filter(Category.Code == code).first()
    if cat is None:
        return abort(404)

    try:
        db.session.delete(cat)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return jsonify(code=200, text="OK")


if __name__ == '__main__':
    app.run(debug=True)
