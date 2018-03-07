from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Models.Producent import Producent
from Models.Vat import Vat
from Models.Category import Category

app = Flask(__name__)
db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = 'producent'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Code = db.Column(db.String(30), unique=True)
    EAN = db.Column(db.String(13))
    Description = db.Column(db.String(300))
    Price = db.Column(db.Float(10, 0))
    ProducentID = db.Column(db.Integer)
    CategoryID = db.Column(db.Integer)
    VATID = db.Column(db.Integer)
    Producent
    Category
    Vat

    def __init__(self, name, code, ean, description, price, producent_id, category_id, vat_id):
        self.Name = name
        self.Code = code
        self.EAN = ean
        self.Description = description
        self.Price = price
        self.ProducentID = producent_id
        self.CategoryID = category_id
        self.VATID = vat_id

    def serialize(self):
        return \
            {
                'Name': self.Name,
                'Code': self.Code,
                'EAN': self.EAN,
                'Description': self.Description,
                'Price': self.Price,
                'Producent': self.Producent.serialize(),
                'Category': self.Category.serialize(),
                'VAT': self.VAT.serialize()
            }

    def __repr__(self):
        return '<Product %r %r >' % (self.Code, self.Name)
