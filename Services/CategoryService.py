from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from Models.Category import Category
from Models.CategorySchema import CategorySchema
from flask import Blueprint

import MySQLdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:zaq12345@localhost/sys'
db = SQLAlchemy(app)
ma = Marshmallow(app)

cat_service = Blueprint('cat_service', __name__)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


@cat_service.route("/category", methods=["GET"])
def category_list():
    all_categories = Category.query.all()
    result = categories_schema.dump(all_categories)
    return jsonify(result.data)


@cat_service.route("/category", methods=["POST"])
def add_category():

    json = request.get_json()
    name = json['name']
    code = json['code']
    desc = json['description']

    try:
        new_cat = Category(name, code, desc)
        db.session.add(new_cat)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return jsonify(new_cat), 200


@cat_service.route('/category/<code>', methods=['GET'])
def get_category(code):
    cat = Category.query.filter(Category.Code == code).first()
    if cat is None:
        return abort(404)
    return category_schema.jsonify(cat), 200


@cat_service.route('/category/<code>', methods=['PUT'])
def update_category(code):
    cat = Category.query.filter(Category.Code == code).first()
    if cat is None:
        return abort(404)

    json = request.get_json()
    cat.Name = json['name']
    cat.Code = json['code']
    cat.Description = json['description']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=400, text=str(e.message))

    return category_schema.jsonify(cat), 200


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

    return category_schema.jsonify(cat)


if __name__ == '__main__':
    app.run(debug=True)
