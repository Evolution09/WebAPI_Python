from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)


class Address(db.Model):
    __tablename__ = 'address'
    ID = db.Column(db.Integer, primary_key=True)
    Country = db.Column(db.String(50))
    City = db.Column(db.String(50))
    Street = db.Column(db.String(50))
    Street_details = db.Column(db.String(10))
    ApartamentNo = db.Column(db.String(10))

    def __init__(self, country, city, street, street_details, apno):
        self.Country = country
        self.City = city
        self.Street = street
        self.Street_details = street_details
        self.ApartamentNo = apno

    def serialize(self):
        return \
            {
                'Country': self.Country,
                'City': self.City,
                'Street': self.Street,
                'Street_details': self.Street_details,
                'ApartamentNo': self.ApartamentNo
            }

    def __repr__(self):
        return '<Address %r %r %r >' % (self.Country, self.City, self.Street)
