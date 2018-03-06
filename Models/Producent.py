from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Models.Address import Address

app = Flask(__name__)
db = SQLAlchemy(app)


class Producent(db.Model):
    __tablename__ = 'producent'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Code = db.Column(db.String(30), unique=True)
    Telephone = db.Column(db.String(9))
    Email = db.Column(db.String(50))
    AddressID = db.Column(db.Integer, SQLAlchemy.ForeginKey("address.id"))
    Address = db.relationship("Address", )

    def __init__(self, name, code, telephone, email, address_id):
        self.Name = name
        self.Code = code
        self.Telephone = telephone
        self.Email = email
        self.AddressID = address_id

    def __repr__(self):
        return '<Producent %r %r >' % (self.Code, self.Name)


